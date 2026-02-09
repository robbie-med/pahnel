# Universal Migration Tool - Hegemon Framework v3.2
**Safe Migration from Any Project State to Current Hegemon**

## 🛡️ CRITICAL SAFETY DIRECTIVES

### Zero Data Loss Guarantee
1. **NO DELETIONS** - Nothing is ever deleted
2. **ARCHIVE EVERYTHING** - All changes go to `MIGRATION_ARCHIVE/`
3. **USER CONSULTATION** - Ask before any structural changes
4. **PRESERVE PROJECT FILES** - Your code is sacred, framework adapts
5. **DETAILED REPORTING** - Every action documented

### Migration Archive Structure
```
MIGRATION_ARCHIVE/
├── MIGRATION_REPORT.md          # Complete migration log
├── MIGRATION_DECISIONS.md       # User choices made
├── original_structure/          # Backup of original files
├── replaced_files/              # Files that were updated
├── deprecated_templates/        # Old framework files
└── timestamp_[YYYY-MM-DD]/      # Timestamped backups
```

## Project Type Detection

### Automatic Detection Process
```python
def detect_project_type():
    """Detect what we're migrating from"""
    
    if exists("AI_CONTEXT.md"):
        version = extract_version()
        if "v3.2" in version:
            return "current"
        elif "v3.1" in version:
            return "hegemon_3.1"
        elif "v3.0" in version:
            return "hegemon_3.0"
        else:
            return "hegemon_legacy"
    
    elif exists(".claude/") and exists("ai_docs/"):
        return "hegemon_1.0"
    
    elif exists("CLAUDE.md") or exists(".claude/"):
        return "pre_hegemon"  # Has AI instructions but no framework
    
    else:
        return "non_framework"  # Raw project, needs full setup
```

## Migration Paths

### Path A: Non-Framework Project → Hegemon 3.2

**For projects with no AI framework at all**

#### Step 1: Initial Assessment
```bash
# CREATE SAFETY ARCHIVE
mkdir -p MIGRATION_ARCHIVE/original_structure
cp -r . MIGRATION_ARCHIVE/original_structure/

# ANALYZE PROJECT
echo "Analyzing project structure..."
```

#### Step 2: Detect Existing AI Instructions
```python
def find_ai_instructions():
    """Find any existing AI guidance"""
    ai_files = []
    
    # Check common locations
    for pattern in ["CLAUDE.md", "README.md", ".claude/*", "docs/AI*"]:
        if files_match(pattern):
            ai_files.extend(matched_files)
    
    if ai_files:
        print("Found existing AI instructions:")
        for file in ai_files:
            print(f"  - {file}")
        
        if user_confirms("Port these to AI_PROJ_CONTEXT.md?"):
            merge_ai_instructions(ai_files)
```

#### Step 3: Framework Installation
```bash
# CONSULT USER
echo "This will add Hegemon Framework to your project"
echo "Your existing files will NOT be modified"
echo "Framework files will be added to:"
echo "  - /ai_docs/ (project management)"
echo "  - /.claude/ (AI configuration)"
echo "Continue? [y/n]"

# CREATE STRUCTURE
mkdir -p ai_docs/{templates,specs,tasks,state,resources,tools}
mkdir -p .claude/{agents,commands,hooks}

# COPY FRAMEWORK FILES
cp -r [FRAMEWORK]/ai_docs/templates/* ai_docs/templates/
cp -r [FRAMEWORK]/.claude/* .claude/
cp [FRAMEWORK]/AI_CONTEXT.md .
```

#### Step 4: Project Analysis & PRD Creation
```python
def analyze_for_prd():
    """Analyze project to pre-fill PRD"""
    
    analysis = {
        "project_type": detect_tech_stack(),
        "existing_features": scan_for_features(),
        "dependencies": parse_package_files(),
        "structure": analyze_directory_structure()
    }
    
    print("\n=== PROJECT ANALYSIS ===")
    print(f"Detected: {analysis['project_type']}")
    print(f"Features found: {len(analysis['existing_features'])}")
    
    if user_confirms("Create PRD from analysis?"):
        generate_smart_prd(analysis)
```

### Path B: Pre-Hegemon Project → Hegemon 3.2

**For projects with CLAUDE.md or basic AI instructions**

#### Step 1: Preserve Existing Instructions
```bash
# ARCHIVE ORIGINALS
mkdir -p MIGRATION_ARCHIVE/original_ai_instructions
cp CLAUDE.md MIGRATION_ARCHIVE/original_ai_instructions/
cp -r .claude MIGRATION_ARCHIVE/original_ai_instructions/
```

#### Step 2: Extract & Merge Directives
```python
def extract_directives():
    """Extract useful directives from existing files"""
    
    directives = {
        "project_specific": [],
        "code_standards": [],
        "workflows": [],
        "constraints": []
    }
    
    # Parse CLAUDE.md
    if exists("CLAUDE.md"):
        content = read_file("CLAUDE.md")
        directives = parse_directives(content)
    
    # Check for .claude/instructions
    if exists(".claude/"):
        for file in glob(".claude/**/*.md"):
            merge_directives(directives, file)
    
    return directives

def create_ai_proj_context(directives):
    """Create new AI_PROJ_CONTEXT.md from extracted directives"""
    
    template = load_template("AI_PROJ_CONTEXT.md")
    
    # Intelligently merge directives
    for section in directives:
        if directives[section]:
            print(f"\nFound {len(directives[section])} {section} directives")
            if user_confirms(f"Include these in AI_PROJ_CONTEXT.md?"):
                template = merge_section(template, section, directives[section])
    
    save_file("ai_docs/AI_PROJ_CONTEXT.md", template)
```

### Path C: Hegemon 1.0 → Hegemon 3.2

#### Step 1: Backup & Assessment
```bash
# FULL BACKUP
mkdir -p MIGRATION_ARCHIVE/hegemon_1.0_backup
cp -r ai_docs MIGRATION_ARCHIVE/hegemon_1.0_backup/
cp -r .claude MIGRATION_ARCHIVE/hegemon_1.0_backup/
```

#### Step 2: Structure Migration
```python
def migrate_v1_structure():
    """Migrate v1.0 structure to v3.2"""
    
    migrations = {
        # Old location → New location
        "ai_docs/BRANDING.md": "ai_docs/PRD_Branding.yaml",
        "ai_docs/ENTITY.md": "ai_docs/PRD_Entity.yaml",
        "ai_docs/PROJECT_DIRECTIVES.md": "ai_docs/AI_PROJ_CONTEXT.md",
        "ai_docs/CONSTITUTION.md": "ai_docs/PROJ_Constitution.md"
    }
    
    for old_path, new_path in migrations.items():
        if exists(old_path):
            print(f"Migrate {old_path} → {new_path}?")
            if user_confirms():
                # Archive original
                archive_path = f"MIGRATION_ARCHIVE/replaced_files/{old_path}"
                copy_file(old_path, archive_path)
                
                # Migrate with format conversion if needed
                if old_path.endswith(".md") and new_path.endswith(".yaml"):
                    convert_md_to_yaml(old_path, new_path)
                else:
                    move_file(old_path, new_path)
```

### Path D: Hegemon 3.0/3.1 → Hegemon 3.2

#### Step 1: Template Reorganization
```python
def migrate_templates():
    """Update template naming to v3.2 standards"""
    
    template_migrations = {
        "prd-template.md": "PRD.md",
        "sub-prd-template.md": "PRD_Asset.md",
        "branding-template.md": None,  # Merged into PRD_Branding.yaml
        "entity-template.md": None,     # Merged into PRD_Entity.yaml
        "BRANDING.yaml": "PRD_Branding.yaml",
        "ENTITY.yaml": "PRD_Entity.yaml",
        "constitution-template.md": "PROJ_Constitution.md",
        "project-directives-template.md": "AI_PROJ_CONTEXT.md",
        "spec-template.md": "Template_Spec.md",
        "plan-template.md": "Template_Plan.md",
        "TEMPLATE_GUIDE.md": "AI_TEMPLATE_RULES.md",
        "FEATURE_CONTEXT_GUIDE.md": "AI_CONTEXT_UPDATE_GUIDE.md"
    }
    
    for old_name, new_name in template_migrations.items():
        old_path = f"ai_docs/templates/{old_name}"
        if exists(old_path):
            if new_name:
                new_path = f"ai_docs/templates/{new_name}"
                archive_and_move(old_path, new_path)
            else:
                archive_file(old_path)
```

## Migration Execution Process

### Phase 1: Safety Check
```python
def pre_migration_safety():
    """Ensure safe migration environment"""
    
    print("=== PRE-MIGRATION SAFETY CHECK ===")
    
    # Check for uncommitted changes
    if has_uncommitted_changes():
        print("⚠️  Uncommitted changes detected!")
        if not user_confirms("Continue anyway?"):
            exit("Commit changes before migration")
    
    # Create archive directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_dir = f"MIGRATION_ARCHIVE/timestamp_{timestamp}"
    create_directory(archive_dir)
    
    # Full backup
    print("Creating complete backup...")
    backup_project(archive_dir)
    
    return archive_dir
```

### Phase 2: Interactive Migration
```python
def interactive_migration():
    """Guide user through migration decisions"""
    
    decisions = []
    
    print("\n=== MIGRATION CONFIGURATION ===")
    
    # Asset detection
    if has_multiple_deliverables():
        print("\nMultiple deliverables detected:")
        assets = detect_assets()
        for asset in assets:
            print(f"  - {asset}")
        
        if user_confirms("Create separate PRDs for each asset?"):
            decisions.append(("multi_asset_prds", True))
            for asset in assets:
                create_asset_prd(asset)
    
    # Existing content preservation
    if has_existing_specs():
        print("\nExisting specifications found")
        if user_confirms("Preserve and migrate existing specs?"):
            migrate_specs()
            decisions.append(("preserve_specs", True))
    
    # State management
    if has_state_files():
        print("\nState files detected")
        print("Options:")
        print("1. Archive old state (recommended)")
        print("2. Attempt to migrate state")
        choice = get_user_choice()
        decisions.append(("state_handling", choice))
    
    save_decisions(decisions)
    return decisions
```

### Phase 3: Migration Execution
```python
def execute_migration(project_type, decisions):
    """Execute the migration plan"""
    
    report = MigrationReport()
    
    try:
        # Step 1: Framework files
        report.log("Installing framework files...")
        install_framework_files(project_type)
        
        # Step 2: Project files
        report.log("Migrating project files...")
        migrate_project_files(project_type, decisions)
        
        # Step 3: Template updates
        report.log("Updating templates...")
        update_templates(project_type)
        
        # Step 4: Reference updates
        report.log("Updating file references...")
        update_all_references()
        
        # Step 5: CASCADE setup
        report.log("Setting up CASCADE validation...")
        setup_cascade_validation()
        
        # Step 6: Validation
        report.log("Validating migration...")
        validation_results = validate_migration()
        
        report.finalize(validation_results)
        
    except Exception as e:
        report.error(f"Migration failed: {e}")
        rollback_migration()
        raise
    
    return report
```

### Phase 4: Post-Migration Validation
```python
def validate_migration():
    """Comprehensive validation of migrated project"""
    
    validation = {
        "framework_files": check_framework_files(),
        "templates": check_templates(),
        "references": check_references(),
        "cascade": check_cascade_integrity(),
        "project_files": check_project_preservation()
    }
    
    print("\n=== MIGRATION VALIDATION ===")
    for check, result in validation.items():
        status = "✅" if result["passed"] else "⚠️"
        print(f"{status} {check}: {result['message']}")
    
    return validation
```

## Migration Report Generation

### Report Template
```markdown
# Migration Report
**Date**: [TIMESTAMP]
**From**: [SOURCE_TYPE]
**To**: Hegemon Framework v3.2

## Migration Summary
- Files Processed: [COUNT]
- Files Archived: [COUNT]
- New Files Created: [COUNT]
- References Updated: [COUNT]

## Decisions Made
[List of user decisions during migration]

## Actions Taken
[Detailed list of all migration actions]

## Validation Results
[Results of post-migration validation]

## Manual Actions Required
[Any remaining manual steps]

## Archive Contents
- Original files: MIGRATION_ARCHIVE/original_structure/
- Replaced files: MIGRATION_ARCHIVE/replaced_files/
- Deprecated items: MIGRATION_ARCHIVE/deprecated_templates/

## Rollback Instructions
If needed, restore from: MIGRATION_ARCHIVE/timestamp_[TIMESTAMP]/
```

## Special Handling Cases

### Multi-Asset Projects
```python
def handle_multi_asset():
    """Special handling for projects with multiple deliverables"""
    
    print("Detecting project assets...")
    assets = []
    
    # Check for obvious indicators
    if exists("frontend/") and exists("backend/"):
        assets.extend(["Frontend", "Backend"])
    if exists("mobile/"):
        assets.append("MobileApp")
    if exists("api/"):
        assets.append("API")
    if exists("admin/"):
        assets.append("AdminPanel")
    
    # Ask user to confirm/modify
    print(f"Detected assets: {assets}")
    if user_confirms("Modify this list?"):
        assets = get_asset_list_from_user()
    
    # Create PRD structure
    for asset in assets:
        create_from_template("PRD_Asset.md", f"PRD_{asset}.md")
    
    return assets
```

### Legacy State Files
```python
def handle_legacy_state():
    """Carefully handle old state files"""
    
    legacy_state = read_state_files()
    
    if legacy_state["has_active_work"]:
        print("⚠️  Active work detected in state files!")
        print("Options:")
        print("1. Complete work before migration")
        print("2. Archive state and start fresh")
        print("3. Attempt to migrate state (risky)")
        
        choice = get_user_choice()
        handle_state_choice(choice, legacy_state)
```

## Emergency Procedures

### Rollback Process
```bash
# If migration fails or causes issues
cd MIGRATION_ARCHIVE/timestamp_[TIMESTAMP]/
cp -r * ../../
cd ../../
rm -rf ai_docs .claude AI_CONTEXT.md
mv ai_docs.backup ai_docs
mv .claude.backup .claude
```

### Partial Migration Recovery
```python
def recover_partial_migration():
    """Recover from incomplete migration"""
    
    checkpoint = load_migration_checkpoint()
    
    print(f"Migration failed at: {checkpoint['last_step']}")
    print("Options:")
    print("1. Resume from checkpoint")
    print("2. Rollback completely")
    print("3. Keep partial migration")
    
    choice = get_user_choice()
    handle_recovery(choice, checkpoint)
```

## Usage Instructions

### Running the Migration
```bash
# 1. Navigate to project root
cd /path/to/your/project

# 2. Start migration (AI will guide you)
@hege migrate

# Or manually:
# 3. AI reads this file and executes migration
"Read /ai_docs/tools/MIGRATION.md and execute migration"
```

### Migration Checklist
- [ ] Backup created in MIGRATION_ARCHIVE/
- [ ] Project type detected correctly
- [ ] Existing AI instructions preserved
- [ ] Framework files installed
- [ ] Templates updated to v3.2 naming
- [ ] References updated throughout
- [ ] CASCADE validation configured
- [ ] Migration report generated
- [ ] Validation passed
- [ ] Manual review completed

## Important Notes

1. **NEVER DELETE** - All replaced files go to MIGRATION_ARCHIVE/
2. **ALWAYS ASK** - User confirmation for structural changes
3. **PRESERVE PROJECT** - User's code is never modified
4. **DOCUMENT EVERYTHING** - Full report in MIGRATION_ARCHIVE/
5. **TEST FIRST** - Run on a copy if unsure

## Support

If migration fails or you need help:
1. Check MIGRATION_ARCHIVE/MIGRATION_REPORT.md
2. Review validation results
3. Use rollback if needed
4. All original files are in MIGRATION_ARCHIVE/original_structure/

---

**Remember**: This migration tool prioritizes safety over speed. Your project files are sacred and will never be deleted, only archived if replaced.