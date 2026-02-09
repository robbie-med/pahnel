#!/usr/bin/env python3
"""
Spec-Kit Bridge for Hegemon Framework
Manages input/output between Hegemon and spec-kit tool
"""

import os
import json
import shutil
import tempfile
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import hashlib
from datetime import datetime
import re
import yaml


class SpecKitBridge:
    """Bridge between Hegemon Framework and spec-kit tool"""
    
    def __init__(self, framework_root: str):
        self.framework_root = Path(framework_root)
        self.spec_kit_path = self.framework_root / "ai_framework" / "tools" / "spec-kit"
        self.project_specs_dir = self.framework_root / "ai_project" / "specs"
        self.uv_path = self._find_uv()
        
    def _find_uv(self) -> str:
        """Find uv executable in common locations"""
        common_paths = [
            "uv",  # In PATH
            os.path.expanduser("~/.local/bin/uv"),
            os.path.expanduser("~/.cargo/bin/uv"),
            "/usr/local/bin/uv",
        ]
        
        for path in common_paths:
            if shutil.which(path):
                return path
                
        raise RuntimeError("uv not found. Install with: curl -LsSf https://astral.sh/uv/install.sh | sh")
    
    def create_spec_kit_workspace(self) -> Path:
        """Create isolated temporary workspace for spec-kit execution"""
        workspace = Path(tempfile.mkdtemp(prefix="spec-kit-work-", suffix=f"-{datetime.now():%Y%m%d-%H%M%S}"))
        
        # Create spec-kit expected structure
        (workspace / "specs").mkdir(parents=True)
        (workspace / ".specify").mkdir(parents=True)

        # Create a virtual environment in the workspace
        subprocess.run([self.uv_path, "venv"], cwd=str(workspace), check=True, capture_output=True)
        
        return workspace
    
    def validate_prd_for_spec_kit(self, prd_path: Path) -> Dict[str, any]:
        """Validate PRD has sufficient detail for spec-kit generation"""
        validation_result = {
            "is_ready": False,
            "completeness_score": 0,
            "missing_sections": [],
            "weak_sections": [],
            "recommendations": [],
            "extracted_features": []
        }

        if not prd_path.exists():
            validation_result["recommendations"].append("PRD file not found. Run /init to create from template.")
            return validation_result

        prd_content = prd_path.read_text()
        sections = self._parse_prd_sections(prd_content)

        # Required sections for spec-kit
        required_sections = {
            'Core Features': 40,  # Weight for scoring
            'Technical Requirements': 30,
            'Problem Statement': 15,
            'Target Audience': 10,
            'Success Metrics': 5
        }

        total_score = 0
        max_score = sum(required_sections.values())

        for section, weight in required_sections.items():
            content = sections.get(section, '').strip()

            if not content or '[NEEDS ATTENTION' in content or '[CRITICAL NEED' in content:
                validation_result["missing_sections"].append(section)
            elif len(content) < 100:  # Too brief
                validation_result["weak_sections"].append(f"{section} (too brief - {len(content)} chars)")
            else:
                # Check for concrete details
                if section == 'Core Features':
                    features = self._extract_features(content)
                    validation_result["extracted_features"] = features
                    if len(features) < 2:
                        validation_result["weak_sections"].append(f"{section} (need at least 2 concrete features)")
                    else:
                        total_score += weight
                elif section == 'Technical Requirements':
                    if not self._has_technical_details(content):
                        validation_result["weak_sections"].append(f"{section} (needs specific tech stack/constraints)")
                    else:
                        total_score += weight
                else:
                    total_score += weight

        validation_result["completeness_score"] = int((total_score / max_score) * 100)
        validation_result["is_ready"] = validation_result["completeness_score"] >= 70

        # Generate recommendations
        if validation_result["missing_sections"]:
            validation_result["recommendations"].append(
                f"Complete these required sections: {', '.join(validation_result['missing_sections'])}"
            )

        if validation_result["weak_sections"]:
            validation_result["recommendations"].append(
                f"Expand these sections with more detail: {', '.join(validation_result['weak_sections'])}"
            )

        if not validation_result["extracted_features"]:
            validation_result["recommendations"].append(
                "Define at least 2-3 concrete features with clear descriptions"
            )

        return validation_result

    def _parse_prd_sections(self, prd_content: str) -> Dict[str, str]:
        """Parse PRD content into sections"""
        sections = {}
        current_section = None
        current_content = []

        for line in prd_content.split('\n'):
            if line.startswith('## '):
                if current_section:
                    sections[current_section] = '\n'.join(current_content)
                current_section = line[3:].strip()
                current_content = []
            elif current_section:
                current_content.append(line)

        if current_section:
            sections[current_section] = '\n'.join(current_content)

        return sections

    def _extract_features(self, content: str) -> List[str]:
        """Extract concrete features from Core Features section"""
        features = []

        # Look for bullet points or numbered items
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if re.match(r'^[-*•]\s+(.+)', line):
                feature = re.sub(r'^[-*•]\s+', '', line)
                if len(feature) > 10 and not feature.startswith('['):
                    features.append(feature)
            elif re.match(r'^\d+\.\s+(.+)', line):
                feature = re.sub(r'^\d+\.\s+', '', line)
                if len(feature) > 10 and not feature.startswith('['):
                    features.append(feature)

        return features

    def _has_technical_details(self, content: str) -> bool:
        """Check if technical requirements have specific details"""
        tech_indicators = [
            r'\b(python|javascript|typescript|java|go|rust|ruby|php)\b',
            r'\b(react|vue|angular|django|flask|fastapi|express|spring)\b',
            r'\b(postgres|mysql|mongodb|redis|elasticsearch)\b',
            r'\b(aws|azure|gcp|docker|kubernetes)\b',
            r'\b(api|rest|graphql|grpc|websocket)\b',
            r'\b(microservice|monolith|serverless|container)\b'
        ]

        content_lower = content.lower()
        matches = sum(1 for pattern in tech_indicators if re.search(pattern, content_lower))

        return matches >= 2  # At least 2 technical specifics mentioned

    def extract_prd_context(self, prd_path: Path, enrich_with_yaml: bool = True) -> Dict[str, str]:
        """Extract relevant sections from PRD for spec-kit context with optional YAML enrichment"""
        if not prd_path.exists():
            raise FileNotFoundError(f"PRD not found at {prd_path}")

        prd_content = prd_path.read_text()
        sections = self._parse_prd_sections(prd_content)

        # Build spec-kit description from PRD sections
        description_parts = []

        # Priority sections for spec-kit
        priority_sections = [
            'Executive Summary',
            'Problem Statement',
            'Core Features',
            'Technical Requirements',
            'Target Audience',
            'Success Metrics'
        ]

        for section in priority_sections:
            if section in sections and sections[section].strip():
                # Clean up template markers
                content = sections[section].strip()
                content = re.sub(r'\[NEEDS ATTENTION:.*?\]', '', content)
                content = re.sub(r'\[CRITICAL NEED:.*?\]', '', content)

                if content:
                    description_parts.append(f"### {section}")
                    description_parts.append(content)
                    description_parts.append("")

        # Enrich with YAML data if available
        if enrich_with_yaml:
            entity_data = self._load_yaml_enrichment('PRD_Entity.yaml')
            branding_data = self._load_yaml_enrichment('PRD_Branding.yaml')

            if entity_data:
                description_parts.append("### Organization Context")
                description_parts.append(self._format_entity_context(entity_data))
                description_parts.append("")

            if branding_data:
                description_parts.append("### Brand Guidelines")
                description_parts.append(self._format_branding_context(branding_data))
                description_parts.append("")

        return {
            "description": '\n'.join(description_parts),
            "title": sections.get('Project Name', 'Untitled Project').strip(),
            "status": self._determine_prd_status(sections),
            "features": self._extract_features(sections.get('Core Features', ''))
        }

    def _load_yaml_enrichment(self, yaml_file: str) -> Optional[Dict]:
        """Load YAML file for context enrichment"""
        yaml_path = self.framework_root / yaml_file
        if not yaml_path.exists():
            yaml_path = self.framework_root / "ai_framework" / yaml_file

        if yaml_path.exists():
            try:
                with open(yaml_path, 'r') as f:
                    return yaml.safe_load(f)
            except:
                pass

        return None

    def _format_entity_context(self, entity_data: Dict) -> str:
        """Format entity data for spec-kit context"""
        parts = []

        if 'organization' in entity_data:
            org = entity_data['organization']
            if 'name' in org:
                parts.append(f"Organization: {org['name']}")
            if 'domain' in org:
                parts.append(f"Domain: {org['domain']}")

        if 'stakeholders' in entity_data:
            parts.append("Key Stakeholders: " + ', '.join(
                s.get('name', 'Unknown') for s in entity_data['stakeholders']
            ))

        return '\n'.join(parts)

    def _format_branding_context(self, branding_data: Dict) -> str:
        """Format branding data for spec-kit context"""
        parts = []

        if 'values' in branding_data:
            parts.append("Core Values: " + ', '.join(branding_data['values']))

        if 'tone' in branding_data:
            parts.append(f"Communication Tone: {branding_data['tone']}")

        if 'design_principles' in branding_data:
            parts.append("Design Principles: " + ', '.join(branding_data['design_principles']))

        return '\n'.join(parts)
    
    def _determine_prd_status(self, sections: Dict[str, str]) -> str:
        """Determine PRD completion status"""
        required_sections = ['Project Overview', 'Core Features', 'Technical Requirements']
        filled_sections = [s for s in required_sections if sections.get(s, '').strip()]
        
        if len(filled_sections) == len(required_sections):
            return "MAINTAINED"
        elif filled_sections:
            return "BUILDING"
        else:
            return "TEMPLATE"
    
    def prepare_spec_kit_input(self, description: str, feat_id: str, workspace: Path) -> Path:
        """Prepare input for spec-kit specify command"""
        # Create a description file for spec-kit
        desc_file = workspace / "description.md"
        desc_file.write_text(description)
        
        # Create metadata for tracking
        metadata = {
            "feat_id": feat_id,
            "created_at": datetime.now().isoformat(),
            "source": "hegemon_framework",
            "description_hash": hashlib.md5(description.encode()).hexdigest()
        }
        
        meta_file = workspace / ".hegemon_meta.json"
        meta_file.write_text(json.dumps(metadata, indent=2))
        
        return desc_file
    
    def run_spec_kit_command(self, command: str, args: List[str], workspace: Path) -> Tuple[int, str, str]:
        """Execute spec-kit command via uvx - SAFELY wrapped to prevent initialization"""

        # CRITICAL: Block dangerous commands
        blocked_commands = ['init', 'install', 'setup']
        if command in blocked_commands:
            error_msg = f"""
            ❌ BLOCKED: Attempted to run 'specify {command}'

            Spec-kit is already integrated! Use these instead:
            • /specify "feature" - Generate specifications
            • /plan FEAT-XXX - Create implementation plan
            • /tasks - Generate test-first tasks

            Never initialize or install spec-kit!
            """
            return 1, "", error_msg

        # Ensure we're in safe workspace
        if not str(workspace).startswith("/tmp/"):
            raise ValueError(f"Unsafe workspace: {workspace}. Must be in /tmp/")

        # Step 1: Install specify-cli in editable mode into the workspace's uv environment
        print(f"DEBUG: Installing specify-cli in editable mode in {workspace}...")
        install_cmd = [
            self.uv_path, "pip", "install", "-e", str(self.spec_kit_path)
        ]
        
        install_result = subprocess.run(
            install_cmd,
            cwd=str(workspace),
            capture_output=True,
            text=True
        )

        if install_result.returncode != 0:
            print(f"DEBUG: specify-cli installation failed. Stdout: {install_result.stdout}", file=sys.stderr)
            print(f"DEBUG: specify-cli installation failed. Stderr: {install_result.stderr}", file=sys.stderr)
            return install_result.returncode, install_result.stdout, install_result.stderr
        print("DEBUG: specify-cli installed successfully.")

        # Step 2: Run the 'specify' command (now that it's installed)
        # Directly execute the script using uv run python
        python_executable = workspace / ".venv" / "bin" / "python"
        main_script_path = self.spec_kit_path / "src" / "specify_cli" / "__main__.py"

        cmd = [
            str(python_executable),
            str(main_script_path),
            command # The 'specify' subcommand, e.g., 'generate'
        ] + args

        print(f"DEBUG: Executing spec-kit command: {' '.join(cmd)} in {workspace}")

        result = subprocess.run(
            cmd,
            cwd=str(workspace),
            capture_output=True,
            text=True,
            timeout=120  # Increased timeout for spec generation
        )

        return result.returncode, result.stdout, result.stderr
    
    def scan_spec_kit_output(self, workspace: Path) -> Dict[str, Path]:
        """Scan workspace for spec-kit generated files"""
        output_files = {}
        specs_dir = workspace / "specs"
        
        if specs_dir.exists():
            for spec_dir in specs_dir.iterdir():
                if spec_dir.is_dir():
                    # Scan for standard spec-kit artifacts
                    artifact_patterns = [
                        "spec.md",
                        "plan.md",
                        "research.md",
                        "data-model.md",
                        "quickstart.md",
                        "tasks.md"
                    ]
                    
                    for pattern in artifact_patterns:
                        artifact_path = spec_dir / pattern
                        if artifact_path.exists():
                            output_files[pattern] = artifact_path
                    
                    # Check for contracts directory
                    contracts_dir = spec_dir / "contracts"
                    if contracts_dir.exists():
                        output_files["contracts"] = contracts_dir
        
        return output_files
    
    def port_to_hegemon(self, spec_kit_files: Dict[str, Path], feat_id: str) -> Path:
        """Port spec-kit output to Hegemon project structure"""
        target_dir = self.project_specs_dir / feat_id
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy all artifacts
        for artifact_name, source_path in spec_kit_files.items():
            if artifact_name == "contracts" and source_path.is_dir():
                # Copy contracts directory
                target_contracts = target_dir / "contracts"
                if target_contracts.exists():
                    shutil.rmtree(target_contracts)
                shutil.copytree(source_path, target_contracts)
            else:
                # Copy individual files
                target_path = target_dir / artifact_name
                shutil.copy2(source_path, target_path)
        
        # Add CASCADE metadata
        self._add_cascade_metadata(target_dir, feat_id)
        
        return target_dir
    
    def _add_cascade_metadata(self, spec_dir: Path, feat_id: str):
        """Add CASCADE tracking metadata to specification"""
        prd_path = self.framework_root / "PRD.md"
        prd_hash = ""
        
        if prd_path.exists():
            prd_hash = hashlib.md5(prd_path.read_bytes()).hexdigest()
        
        spec_files = list(spec_dir.glob("*.md"))
        spec_hash = hashlib.md5(
            ''.join(f.read_text() for f in spec_files).encode()
        ).hexdigest()
        
        cascade_meta = {
            "feat_id": feat_id,
            "prd_hash": prd_hash,
            "spec_hash": spec_hash,
            "created_at": datetime.now().isoformat(),
            "spec_kit_version": self._get_spec_kit_version(),
            "artifacts": [f.name for f in spec_dir.iterdir() if f.is_file()]
        }
        
        meta_path = spec_dir / "_cascade_meta.json"
        meta_path.write_text(json.dumps(cascade_meta, indent=2))
    
    def _get_spec_kit_version(self) -> str:
        """Get current spec-kit version"""
        try:
            result = subprocess.run(
                ["git", "describe", "--tags", "--always"],
                cwd=str(self.spec_kit_path),
                capture_output=True,
                text=True
            )
            return result.stdout.strip() if result.returncode == 0 else "unknown"
        except:
            return "unknown"
    
    def scope_feature_interactively(self, initial_description: str, prd_context: Dict) -> Dict[str, str]:
        """Interactive feature scoping assistant"""
        scoped_feature = {
            "description": initial_description,
            "complexity": "medium",
            "breakdown_needed": False,
            "missing_details": [],
            "enriched_description": initial_description
        }

        # Analyze complexity
        complexity_score = self._analyze_feature_complexity(initial_description)

        if complexity_score > 8:
            scoped_feature["complexity"] = "high"
            scoped_feature["breakdown_needed"] = True
            scoped_feature["suggested_breakdown"] = self._suggest_feature_breakdown(initial_description)
        elif complexity_score > 4:
            scoped_feature["complexity"] = "medium"
        else:
            scoped_feature["complexity"] = "low"

        # Check for missing details
        missing = []

        # Check for user stories
        if not re.search(r'(as a|user|when|should|must|need)', initial_description.lower()):
            missing.append("user_story")
            scoped_feature["missing_details"].append("Consider adding: 'As a [user type], I want to [action] so that [benefit]'")

        # Check for acceptance criteria
        if not re.search(r'(given|when|then|accept|criteria|requirement)', initial_description.lower()):
            missing.append("acceptance_criteria")
            scoped_feature["missing_details"].append("Consider adding specific acceptance criteria")

        # Check for technical constraints mentioned in PRD
        if prd_context.get("status") == "MAINTAINED":
            tech_reqs = prd_context.get("technical_requirements", "")
            if tech_reqs and not self._references_tech_constraints(initial_description, tech_reqs):
                missing.append("technical_alignment")
                scoped_feature["missing_details"].append("Ensure alignment with technical requirements from PRD")

        # Enrich description with PRD context
        if missing:
            enriched_parts = [initial_description]

            if "user_story" in missing and prd_context.get("target_audience"):
                enriched_parts.append(f"\nTarget Users: {prd_context['target_audience']}")

            if prd_context.get("features"):
                related_features = self._find_related_features(initial_description, prd_context["features"])
                if related_features:
                    enriched_parts.append(f"\nRelated Features from PRD: {', '.join(related_features[:3])}")

            scoped_feature["enriched_description"] = '\n'.join(enriched_parts)

        return scoped_feature

    def _analyze_feature_complexity(self, description: str) -> int:
        """Analyze feature complexity on scale of 1-10"""
        score = 0

        # Length indicates complexity
        if len(description) > 500:
            score += 3
        elif len(description) > 200:
            score += 2
        else:
            score += 1

        # Multiple components mentioned
        component_keywords = ['and', 'also', 'additionally', 'furthermore', 'plus']
        component_count = sum(1 for kw in component_keywords if kw in description.lower())
        score += min(component_count * 2, 4)

        # Technical complexity indicators
        tech_complexity = ['integration', 'migration', 'synchronization', 'real-time', 'distributed']
        tech_count = sum(1 for tc in tech_complexity if tc in description.lower())
        score += min(tech_count * 2, 3)

        return min(score, 10)

    def _suggest_feature_breakdown(self, description: str) -> List[str]:
        """Suggest breaking down complex features"""
        suggestions = []

        # Look for conjunctions that might indicate multiple features
        if ' and ' in description.lower():
            parts = description.split(' and ')
            if len(parts) > 2:
                suggestions.append("Consider splitting into separate features at 'and' conjunctions")

        # Look for multiple user actions
        action_verbs = re.findall(r'\b(create|read|update|delete|view|manage|configure|export|import)\b',
                                   description.lower())
        if len(set(action_verbs)) > 3:
            suggestions.append(f"Multiple actions detected ({len(set(action_verbs))}). Consider separate features for each action type.")

        # Check for multiple user types
        user_indicators = re.findall(r'\b(admin|user|customer|manager|developer|analyst)\b', description.lower())
        if len(set(user_indicators)) > 2:
            suggestions.append(f"Multiple user types ({len(set(user_indicators))}). Consider role-specific features.")

        if not suggestions:
            suggestions.append("Consider breaking into: 1) Core functionality, 2) Advanced features, 3) Admin controls")

        return suggestions

    def _references_tech_constraints(self, description: str, tech_requirements: str) -> bool:
        """Check if feature description references technical constraints"""
        # Extract key technical terms from requirements
        tech_terms = re.findall(r'\b[A-Z][a-zA-Z]+\b', tech_requirements)  # Capitalized tech terms
        tech_terms.extend(re.findall(r'\b(API|REST|SQL|NoSQL|AWS|GCP|Azure)\b', tech_requirements))

        description_lower = description.lower()
        tech_requirements_lower = tech_requirements.lower()

        # Check for any overlap
        for term in tech_terms:
            if term.lower() in description_lower:
                return True

        return False

    def _find_related_features(self, description: str, existing_features: List[str]) -> List[str]:
        """Find features from PRD that relate to the current description"""
        related = []
        desc_words = set(description.lower().split())

        for feature in existing_features:
            feature_words = set(feature.lower().split())
            # Simple word overlap check
            overlap = len(desc_words.intersection(feature_words))
            if overlap > 2:  # More than 2 words in common
                related.append(feature)

        return related

    def generate_pre_spec_validation_report(self, prd_path: Path, feature_description: Optional[str] = None) -> str:
        """Generate a pre-specification validation report"""
        report_lines = ["# Pre-Specification Validation Report\n"]

        # Validate PRD
        validation = self.validate_prd_for_spec_kit(prd_path)

        report_lines.append("## PRD Readiness")
        report_lines.append(f"- **Status**: {'✅ Ready' if validation['is_ready'] else '❌ Not Ready'}")
        report_lines.append(f"- **Completeness Score**: {validation['completeness_score']}%")

        if validation['missing_sections']:
            report_lines.append(f"- **Missing Sections**: {', '.join(validation['missing_sections'])}")

        if validation['weak_sections']:
            report_lines.append(f"- **Weak Sections**: {', '.join(validation['weak_sections'])}")

        if validation['extracted_features']:
            report_lines.append(f"\n## Detected Features ({len(validation['extracted_features'])})")
            for i, feature in enumerate(validation['extracted_features'][:5], 1):
                report_lines.append(f"{i}. {feature}")

        # Feature-specific validation if provided
        if feature_description:
            report_lines.append(f"\n## Feature Scope Analysis")
            prd_context = self.extract_prd_context(prd_path)
            scope_analysis = self.scope_feature_interactively(feature_description, prd_context)

            report_lines.append(f"- **Complexity**: {scope_analysis['complexity'].upper()}")
            report_lines.append(f"- **Breakdown Needed**: {'Yes' if scope_analysis['breakdown_needed'] else 'No'}")

            if scope_analysis['breakdown_needed']:
                report_lines.append("\n### Suggested Breakdown:")
                for suggestion in scope_analysis.get('suggested_breakdown', []):
                    report_lines.append(f"- {suggestion}")

            if scope_analysis['missing_details']:
                report_lines.append("\n### Missing Details:")
                for detail in scope_analysis['missing_details']:
                    report_lines.append(f"- {detail}")

        # Recommendations
        if validation['recommendations']:
            report_lines.append("\n## Recommendations")
            for rec in validation['recommendations']:
                report_lines.append(f"- {rec}")

        # What spec-kit will receive
        report_lines.append("\n## Context for Spec-Kit")
        try:
            context = self.extract_prd_context(prd_path, enrich_with_yaml=True)
            report_lines.append(f"- **PRD Status**: {context['status']}")
            report_lines.append(f"- **Feature Count**: {len(context.get('features', []))}")
            report_lines.append(f"- **Description Length**: {len(context['description'])} characters")
            report_lines.append("- **Enrichment**: YAML files will be included")
        except Exception as e:
            report_lines.append(f"- ⚠️ Error extracting context: {str(e)}")

        return '\n'.join(report_lines)

    def cleanup_workspace(self, workspace: Path):
        """Clean up temporary workspace"""
        if workspace.exists() and str(workspace).startswith("/tmp/"):
            shutil.rmtree(workspace)
    
    def validate_spec_kit_output(self, spec_dir: Path) -> bool:
        """Validate that spec-kit output meets Hegemon requirements"""
        required_files = ["spec.md"]
        
        for required in required_files:
            if not (spec_dir / required).exists():
                return False
        
        # Check CASCADE metadata exists
        if not (spec_dir / "_cascade_meta.json").exists():
            return False
        
        return True


# CLI interface for testing
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: spec_kit_bridge.py <command> [args]")
        print("Commands: test, specify, plan, tasks")
        sys.exit(1)
    
    bridge = SpecKitBridge(os.getcwd())
    command = sys.argv[1]
    
    if command == "test":
        print(f"Spec-kit path: {bridge.spec_kit_path}")
        print(f"uv path: {bridge.uv_path}")
        print(f"Project specs dir: {bridge.project_specs_dir}")
        print("Bridge configured successfully!")
    
    elif command == "specify":
        if len(sys.argv) < 4:
            print("Usage: spec_kit_bridge.py specify <feat-id> <description>")
            sys.exit(1)
        
        feat_id = sys.argv[2]
        description = sys.argv[3]
        
        workspace = bridge.create_spec_kit_workspace()
        try:
            bridge.prepare_spec_kit_input(description, feat_id, workspace)
            
            # Copy PRD.md to the temporary workspace for spec-kit to find
            prd_source_path = bridge.framework_root / "PRD.md"
            if prd_source_path.exists():
                shutil.copy2(prd_source_path, workspace / "PRD.md")
            else:
                print(f"Warning: PRD.md not found at {prd_source_path}. Spec-kit might lack full context.", file=sys.stderr)

            returncode, stdout, stderr = bridge.run_spec_kit_command("specify", [], workspace)
            
            if returncode == 0:
                output_files = bridge.scan_spec_kit_output(workspace)
                target_dir = bridge.port_to_hegemon(output_files, feat_id)
                print(f"Specification created at: {target_dir}")
            else:
                print(f"Error running spec-kit: {stderr}")
        finally:
            bridge.cleanup_workspace(workspace)