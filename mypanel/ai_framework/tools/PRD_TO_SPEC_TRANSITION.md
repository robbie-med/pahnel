# PRD to Specification Transition Guide

## Overview

This guide ensures smooth transition from PRD completion to high-quality specification generation using spec-kit integration.

## Pre-Flight Checklist

### 1. Validate PRD Completeness

Run validation check:
```bash
python ai_framework/tools/spec_kit_bridge.py validate
```

Or programmatically:
```python
from ai_framework.tools.spec_kit_bridge import SpecKitBridge

bridge = SpecKitBridge(".")
validation = bridge.validate_prd_for_spec_kit(Path("PRD.md"))

if validation["completeness_score"] < 70:
    print("⚠️ PRD needs more work before specifications")
    print(f"Score: {validation['completeness_score']}%")
    print(f"Recommendations: {validation['recommendations']}")
```

### 2. Review Quality Gates

#### Minimum Requirements (70% Score)
- [ ] **Core Features**: At least 2 concrete, well-defined features
- [ ] **Technical Requirements**: Specific tech stack mentioned
- [ ] **Problem Statement**: Clear problem definition
- [ ] **Target Audience**: User segments identified
- [ ] **Success Metrics**: Measurable outcomes defined

#### Optimal Requirements (90% Score)
- [ ] All minimum requirements met
- [ ] **Executive Summary**: Comprehensive overview
- [ ] **User Personas**: Detailed with behaviors/needs
- [ ] **Non-functional Requirements**: Performance, security, scalability
- [ ] **Integration Points**: External systems identified
- [ ] **Constraints**: Budget, timeline, technical limitations

## Transition Workflow

### Step 1: PRD Status Check

```python
def check_prd_status():
    # Check PRD header for status
    with open("PRD.md", "r") as f:
        content = f.read()

    if "Status: MAINTAINED" not in content:
        print("PRD must be in MAINTAINED status")
        print("Run: /prd --transition-to-maintained")
        return False

    return True
```

### Step 2: Feature Scoping

Before running `/specs`, ensure features are properly scoped:

```python
from ai_framework.tools.spec_kit_bridge import SpecKitBridge

bridge = SpecKitBridge(".")
prd_context = bridge.extract_prd_context(Path("PRD.md"))

# For each feature description
for feature in prd_context["features"]:
    scope_analysis = bridge.scope_feature_interactively(feature, prd_context)

    if scope_analysis["breakdown_needed"]:
        print(f"⚠️ Feature too complex: {feature[:50]}...")
        print("Suggestions:", scope_analysis["suggested_breakdown"])
```

### Step 3: Context Enrichment

Ensure YAML files are complete:

#### PRD_Entity.yaml
```yaml
organization:
  name: "Company Name"
  domain: "industry/sector"
  size: "startup/SMB/enterprise"

stakeholders:
  - name: "Product Owner"
    role: "Decision maker"
  - name: "Tech Lead"
    role: "Technical approval"
```

#### PRD_Branding.yaml
```yaml
values:
  - "Innovation"
  - "User-centric"
  - "Reliability"

tone: "professional yet approachable"

design_principles:
  - "Simplicity first"
  - "Mobile responsive"
  - "Accessibility compliant"
```

### Step 4: Pre-Specification Validation

Generate validation report:

```python
from ai_framework.tools.spec_kit_bridge import SpecKitBridge

bridge = SpecKitBridge(".")
report = bridge.generate_pre_spec_validation_report(
    Path("PRD.md"),
    feature_description="optional specific feature"
)

print(report)
```

## Running Specification Generation

### Option 1: Generate All Specifications

```bash
/specs
```

This will:
1. Validate PRD completeness
2. Extract all features from PRD
3. Generate specs for each feature
4. Create `/ai_project/specs/FEAT-XXX/` directories

### Option 2: Generate Specific Feature

```bash
/specs "user authentication with SSO support"
```

This will:
1. Validate PRD completeness
2. Scope the specific feature
3. Check complexity and suggest breakdown if needed
4. Generate single feature specification

### Option 3: With Pre-validation

```bash
/specs --validate-first "feature description"
```

Shows what spec-kit will receive before generation.

## Expected Outputs

### Successful Generation

```
/ai_project/specs/FEAT-001-user-authentication/
├── spec.md              # Main specification
├── plan.md              # Implementation plan
├── research.md          # Background research
├── data-model.md        # Data structures
├── contracts/           # API contracts
│   ├── auth-api.yaml
│   └── user-api.yaml
├── quickstart.md        # Getting started guide
├── tasks.md             # Implementation tasks
└── _cascade_meta.json   # Hegemon tracking
```

### Quality Indicators

Good specification will have:
- Clear acceptance criteria
- Concrete API contracts
- Testable requirements
- Implementation tasks with estimates
- No ambiguity markers

## Troubleshooting

### "PRD not ready for specifications"

**Symptom**: Completeness score below 70%

**Solution**:
1. Review missing sections
2. Add concrete details to weak sections
3. Define at least 2-3 specific features
4. Include technical stack details

### "Feature too complex"

**Symptom**: Breakdown suggested for feature

**Solution**:
1. Split into smaller, focused features
2. Create parent epic with sub-features
3. Focus on single user journey per feature

### "Spec-kit failed"

**Symptom**: Generation error

**Solution**:
1. Check `uv` installation: `which uv`
2. Verify spec-kit submodule: `git submodule status`
3. Review temp workspace logs
4. Fall back to native generation: `/specs --native`

### "Missing context"

**Symptom**: Generated specs lack detail

**Solution**:
1. Enrich PRD with more specifics
2. Complete YAML configuration files
3. Add examples to `/ai_project/resources/`
4. Include user stories in feature descriptions

## Best Practices

### 1. Feature Definition

**Good**:
```markdown
Users can register with email and password, receive verification email,
and activate account within 24 hours. Password must meet security requirements.
```

**Poor**:
```markdown
User registration system
```

### 2. Technical Requirements

**Good**:
```markdown
- Backend: Python 3.11 with FastAPI
- Database: PostgreSQL 15 with Redis cache
- Auth: JWT with refresh tokens
- API: REST with OpenAPI 3.0 specs
```

**Poor**:
```markdown
- Modern tech stack
- Scalable architecture
```

### 3. Success Metrics

**Good**:
```markdown
- Registration completion rate > 80%
- Email verification within 5 minutes
- Page load time < 2 seconds
- 99.9% uptime
```

**Poor**:
```markdown
- Good performance
- High availability
```

## Validation Scripts

### Quick Validation

```bash
# Check if ready for specs
python -c "
from ai_framework.tools.spec_kit_bridge import SpecKitBridge
b = SpecKitBridge('.')
v = b.validate_prd_for_spec_kit('PRD.md')
print(f'Ready: {v[\"is_ready\"]} ({v[\"completeness_score\"]}%)')
"
```

### Feature Count

```bash
# Count detected features
python -c "
from ai_framework.tools.spec_kit_bridge import SpecKitBridge
b = SpecKitBridge('.')
c = b.extract_prd_context('PRD.md')
print(f'Features found: {len(c[\"features\"])}')
for i, f in enumerate(c['features'], 1):
    print(f'{i}. {f[:60]}...')
"
```

## Next Steps After Specification

Once specifications are generated:

1. **Review Generated Specs**
   - Check `/ai_project/specs/FEAT-XXX/spec.md`
   - Verify contracts in `contracts/` directory
   - Review tasks in `tasks.md`

2. **Run Task Generation**
   ```bash
   /tasks init
   ```
   This enhances spec-kit tasks with:
   - Agent assignments
   - Parallel execution markers [P]
   - Test-first approach

3. **Begin Implementation**
   ```bash
   /tasks next
   ```
   Start with first task, following TDD approach.

## Summary

The PRD → Specification transition succeeds when:

1. ✅ PRD completeness ≥ 70%
2. ✅ Features are concrete and scoped
3. ✅ Technical requirements specified
4. ✅ YAML enrichment files complete
5. ✅ Validation report shows readiness

Following this guide ensures spec-kit generates high-quality, actionable specifications that accelerate development.