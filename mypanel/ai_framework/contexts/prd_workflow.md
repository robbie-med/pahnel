# PRD Development Workflow
**CONDITIONAL LOAD**: Only load this file when ANY PRD (master or asset) needs development

**Valid PRD Statuses**:
- `nonexistent` - PRD not created yet
- `draft` - Being written
- `in_review` - Under stakeholder review
- `editing` - Being revised
- `approved` - Approved but not locked
- `locked` - Finalized, no changes
- `maintained` - Locked but monitored for updates

## When This File Loads
```python
def should_load_prd_workflow():
    """
    Load PRD workflow if ANY PRD (master or asset) needs work
    Also loads interview_protocol.md if interview mode active
    """
    # Check main PRD
    main_prd_status = get_prd_status("PRD.md")
    if main_prd_status in ['nonexistent', 'draft', 'in_review', 'editing']:
        return True

    # Check all asset PRDs
    asset_prds = find_files("PRD_*.md")
    for asset_prd in asset_prds:
        status = get_prd_status(asset_prd)
        if status in ['nonexistent', 'draft', 'in_review', 'editing']:
            return True

    # Check for active interview session
    if exists("/ai_project/state/interview_progress.json"):
        return True

    # All PRDs are locked/approved - no workflow needed
    return False
```

## 🎯 INTERVIEW MODE (NEW)

### Extended Thinking Activation
**CRITICAL**: Extended Thinking is automatically ACTIVE for ALL PRD development work.

When working on PRDs:
- Extended Thinking analyzes project structure and complexity
- Deep reasoning applied to problem-solution fit
- Architecture pattern matching for technical decisions
- Business viability analysis for success metrics

Visual indicator shown to user:
```
[🧠 Extended Thinking Active - Deep Analysis Mode]
```

### Interview vs Conversational Mode

When `/prd` command starts, check for user preference:

```python
def start_prd_development():
    """
    Entry point for PRD development - choose mode
    Extended Thinking: ACTIVE
    """

    # Check for interrupted interview first
    interrupted_interview = check_for_interrupted_interview()
    if interrupted_interview:
        # Resume from interview_protocol.md
        load_context("interview_protocol.md")
        return resume_interview(interrupted_interview)

    # Check if user has saved preference
    if has_preference("prd_mode"):
        mode = get_preference("prd_mode")
    else:
        # First time - ask preference with AskUserQuestion
        from interview_protocol import ask_mode_preference
        response = AskUserQuestion([{
            "question": "How would you like to develop the PRD?",
            "header": "PRD Mode",
            "multiSelect": False,
            "options": [
                {
                    "label": "Interactive Interview",
                    "description": "Guided questions with multiple choice (recommended - ensures completeness)"
                },
                {
                    "label": "Conversational Mode",
                    "description": "Free-form discussion (classic mode - more flexibility)"
                }
            ]
        }])

        mode = response["answers"]["prd_mode"]

        # Ask if they want to save preference
        save_pref = AskUserQuestion([{
            "question": "Remember this choice for future PRDs?",
            "header": "Save",
            "multiSelect": False,
            "options": [
                {"label": "Yes", "description": "Use this mode by default"},
                {"label": "No", "description": "Ask me each time"}
            ]
        }])

        if save_pref["answers"]["save"] == "Yes":
            save_preference("prd_mode", mode)

    # Launch appropriate mode
    if mode == "Interactive Interview":
        load_context("interview_protocol.md")
        return start_interview_mode()
    else:
        return start_conversational_mode()
```

### Interview Mode Flow

When interview mode is selected:

1. **Load interview_protocol.md** - Contains all question sets and logic
2. **Show Extended Thinking indicator** - User sees analysis is active
3. **Run Stage 1: Project Discovery** - Determine structure
4. **Create PRD structure** - Single or multi-asset based on answers
5. **Progress through stages** - Purpose → Audience → Features → Technical → Business
6. **Checkpoint after each stage** - Save progress, allow review/edit
7. **Complete and validate** - Check spec-kit readiness, offer next steps

### Resuming Interrupted Interviews

If `/ai_project/state/interview_progress.json` exists:

```python
def check_for_interrupted_interview():
    """Check for active interview to resume"""
    if exists("/ai_project/state/interview_progress.json"):
        state = load_json("/ai_project/state/interview_progress.json")

        # Check age
        age = now() - parse_datetime(state["started"])
        if age > timedelta(hours=24):
            # Old session - ask what to do
            response = AskUserQuestion([{
                "question": "Found an old interview session (>24h old). What would you like to do?",
                "header": "Action",
                "multiSelect": False,
                "options": [
                    {"label": "Resume", "description": "Continue where I left off"},
                    {"label": "Start Over", "description": "Begin fresh interview"},
                    {"label": "Review Progress", "description": "Show what was completed"}
                ]
            }])

            action = response["answers"]["action"]
            if action == "Start Over":
                clear_interview_state()
                return None
            elif action == "Review Progress":
                show_interview_progress(state)
                return check_for_interrupted_interview()  # Ask again

        # Valid resume
        print(f"\n🔄 Resuming PRD Interview")
        print(f"Completed: {', '.join(state['completed_stages'])}")
        print(f"Next: {state['current_stage']}\n")

        return state

    return None
```

---

## CONVERSATIONAL MODE (Classic Workflow)

**The sections below describe the original conversational PRD workflow.**

When user selects "Conversational Mode" or has it as their saved preference, the classic free-form discussion approach is used. This provides maximum flexibility for users who prefer open-ended conversation over structured interviews.

All original PRD discovery processes, dynamic asset identification, and example collection remain available in conversational mode.

---

## PRD Discovery Process

### Phase 1: Initial Assessment

#### Determine Project Structure
```python
def assess_project_complexity():
    print("Let's understand your project structure...")

    questions = [
        "Is this a single application or multiple interconnected systems?",
        "What are the main deliverables/assets you envision?",
        "Will different user groups interact with different parts?"
    ]

    if has_multiple_assets():
        return "multi_asset_structure"
    else:
        return "single_prd_structure"
```

#### Spec-Kit Readiness Check
```python
def check_spec_kit_readiness():
    """Check if PRD is ready for spec-kit generation"""
    from ai_framework.tools.spec_kit_bridge import SpecKitBridge

    bridge = SpecKitBridge(get_framework_root())
    validation = bridge.validate_prd_for_spec_kit(Path("PRD.md"))

    if validation["completeness_score"] < 70:
        print(f"⚠️ PRD Completeness: {validation['completeness_score']}%")
        print("Spec-kit requires at least 70% completeness for quality output")

        if validation["missing_sections"]:
            print(f"Missing: {', '.join(validation['missing_sections'])}")

        if validation["weak_sections"]:
            print(f"Needs expansion: {', '.join(validation['weak_sections'])}")
    else:
        print(f"✅ PRD Ready for Specifications ({validation['completeness_score']}%)")

    return validation
```

### Phase 2: Multi-Asset PRD Setup

#### Dynamic Asset Identification
```python
def identify_project_assets():
    """
    Dynamically identify assets based on user description
    DO NOT assume Portal, Website, etc. - let user define
    """
    
    print("I've identified these potential assets in your project:")
    
    # User mentions examples:
    # "customer dashboard" → PRD_CustomerDashboard.md
    # "mobile app" → PRD_MobileApp.md  
    # "API service" → PRD_API.md
    # "admin panel" → PRD_AdminPanel.md
    # "data pipeline" → PRD_DataPipeline.md
    
    assets = []
    for deliverable in user_mentioned_deliverables:
        asset_name = normalize_asset_name(deliverable)
        assets.append({
            'name': asset_name,
            'file': f'PRD_{asset_name}.md',
            'description': user_description
        })
    
    return assets
```

#### Create Asset PRD Structure
```python
def setup_multi_asset_prds(assets):
    # Always create shared references first
    create_from_template("PRD_Branding.yaml")
    create_from_template("PRD_Entity.yaml")
    
    # Create master PRD
    create_from_template("PRD.md", "PRD.md")
    
    # Create asset-specific PRDs
    for asset in assets:
        create_from_template("PRD_Asset.md", asset['file'])
        update_master_prd_references(asset)
```

### Phase 3: PRD Discovery Sections

#### 3.1 Purpose & Mission Discovery
**Questions to Ask**:
- What problem does this solve?
- What is the core mission?
- What makes this unique?

**Example Collection Triggers**:
- If user mentions competitors → Request competitive examples
- If user describes complex workflows → Request process diagrams

#### 3.2 Target Audience Discovery
**Questions to Ask**:
- Primary users/customers?
- Secondary audiences?
- User sophistication level?
- Geographic scope?

**Asset Allocation**:
- Map user segments to specific assets
- "Customers use the portal, admins use the dashboard"

#### 3.3 Core Features Discovery
**Structure for Multi-Asset**:
```python
def collect_features():
    # Distinguish between:
    # 1. Cross-asset features (SSO, unified profiles)
    # 2. Asset-specific features
    
    for feature in discussed_features:
        if affects_multiple_assets(feature):
            add_to_master_prd(feature)
        else:
            asset = identify_owning_asset(feature)
            add_to_asset_prd(asset, feature)
```

#### 3.4 Technical Requirements
**Questions to Ask**:
- Performance requirements per asset?
- Scale expectations?
- Security requirements?
- Platform targets?

**Example Collection**:
- API mentioned → Create `/ai_project/specs/resources/examples/api-samples/`
- UI discussed → Create `/ai_project/specs/resources/examples/ui-mockups/`

#### 3.5 Business Model
**Questions to Ask**:
- Revenue streams?
- Cost structures?
- Success metrics?
- Competition/alternatives?

### Phase 4: Dynamic Example Collection

#### Context-Driven Requests
```python
def request_examples_contextually():
    # NEVER: "Do you have any examples?"
    # ALWAYS: Specific, valuable requests
    
    example_triggers = {
        'ui_complexity': "ui-mockups",
        'data_structure': "data-samples",
        'report_format': "report-templates",
        'api_design': "api-responses",
        'workflow': "process-diagrams",
        'integration': "integration-specs"
    }
    
    for context, example_type in example_triggers.items():
        if context_detected(context):
            create_dir(f"/ai_project/specs/resources/examples/{example_type}/")
            request_specific_example(example_type)
```

### Phase 5: PRD Finalization

#### Review Structure
```markdown
## PRD Review Checklist

### Master PRD Complete?
- [ ] Purpose and mission defined
- [ ] All assets identified and linked
- [ ] Cross-asset features documented
- [ ] PRD_Branding.yaml created
- [ ] PRD_Entity.yaml created

### Asset PRDs Complete?
For each PRD_[AssetName].md:
- [ ] Asset-specific features defined
- [ ] User journeys mapped
- [ ] Technical requirements specified
- [ ] Links back to master PRD
- [ ] References PRD_Branding.yaml
- [ ] References PRD_Entity.yaml

### Ready to Lock?
- [ ] All stakeholders reviewed
- [ ] No [CRITICAL NEED] markers remain
- [ ] Examples collected and organized
```

#### Locking Process
```python
def lock_prd_structure():
    # Get explicit approval
    if confirm("Ready to lock all PRDs? This finalizes the structure."):
        lock_file("PRD.md")
        for asset_prd in find_asset_prds():
            lock_file(asset_prd)
        
        set_prd_status("locked")
        print("PRDs locked. Moving to specification phase.")
```

## Key Principles

### 1. No Hardcoded Assumptions
- Never assume "Portal", "Website", "Mobile"
- Let project requirements drive asset identification
- Asset names come from user's domain language

### 2. Progressive Discovery
- Start broad (single vs multi-asset)
- Identify assets through conversation
- Create structure dynamically
- Fill details iteratively

### 3. Smart Example Collection
- Only request when adds value
- Be specific about what's needed
- Create organized directories
- Never request generically

### 4. Maintain Relationships
```yaml
Reference Hierarchy:
  PRD_Branding.yaml ← All PRDs reference
  PRD_Entity.yaml ← All PRDs reference
  PRD.md ← Master document
    ├── PRD_[Asset1].md ← Links back to master
    ├── PRD_[Asset2].md ← Links back to master
    └── PRD_[AssetN].md ← Links back to master
```

## State Management During PRD Development

### Track PRD Progress
```json
{
  "prd_status": "draft|in_review|approved|locked",
  "structure_type": "single|multi_asset",
  "identified_assets": [
    {"name": "AssetName", "prd": "PRD_AssetName.md", "status": "draft"}
  ],
  "discovery_progress": {
    "purpose": "complete",
    "audience": "in_progress",
    "features": "pending",
    "technical": "pending",
    "business": "pending"
  },
  "examples_requested": [
    {"type": "ui-mockups", "status": "received"}
  ]
}
```

## Transition to Specification Phase

### Spec-Kit Readiness Validation
```python
def validate_before_specs():
    """Validate PRD is ready for spec-kit generation"""
    from ai_framework.tools.spec_kit_bridge import SpecKitBridge

    bridge = SpecKitBridge(get_framework_root())
    validation = bridge.validate_prd_for_spec_kit(Path("PRD.md"))

    print("## Spec-Kit Readiness Report\n")
    print(f"Completeness Score: {validation['completeness_score']}%")

    if validation["completeness_score"] >= 90:
        print("✅ EXCELLENT - PRD is fully ready for high-quality specifications")
    elif validation["completeness_score"] >= 70:
        print("✅ GOOD - PRD has sufficient detail for spec generation")
    else:
        print("⚠️ NEEDS WORK - PRD requires more detail for quality specs")

    # Show specific guidance
    if validation["missing_sections"]:
        print("\n### Missing Sections (Required)")
        for section in validation["missing_sections"]:
            print(f"- {section}")

    if validation["weak_sections"]:
        print("\n### Weak Sections (Expand These)")
        for section in validation["weak_sections"]:
            print(f"- {section}")

    # Feature detection
    if validation["extracted_features"]:
        print(f"\n### Detected Features ({len(validation['extracted_features'])})")
        for i, feature in enumerate(validation["extracted_features"][:5], 1):
            print(f"{i}. {feature}")
    else:
        print("\n⚠️ No concrete features detected - define at least 2-3 features")

    return validation
```

### Feature Scoping Guidance
```python
def guide_feature_scoping(feature_description):
    """Help users scope features appropriately for spec-kit"""
    from ai_framework.tools.spec_kit_bridge import SpecKitBridge

    bridge = SpecKitBridge(get_framework_root())
    prd_context = bridge.extract_prd_context(Path("PRD.md"))
    scope_analysis = bridge.scope_feature_interactively(feature_description, prd_context)

    print(f"\n## Feature Scope Analysis: {feature_description[:50]}...\n")
    print(f"Complexity: {scope_analysis['complexity'].upper()}")

    if scope_analysis['breakdown_needed']:
        print("\n⚠️ Feature is too complex - consider breaking down:")
        for suggestion in scope_analysis['suggested_breakdown']:
            print(f"  • {suggestion}")

    if scope_analysis['missing_details']:
        print("\n📝 Add these details for better specifications:")
        for detail in scope_analysis['missing_details']:
            print(f"  • {detail}")

    return scope_analysis
```

### PRD → Specification Checklist

#### Minimum Requirements (70% threshold)
- Core Features section has 2+ concrete features
- Technical Requirements specify tech stack
- Problem Statement clearly defined
- Target Audience identified
- Success Metrics measurable

#### Optimal Requirements (90% threshold)
- All minimum requirements met
- Executive Summary comprehensive
- User personas with details
- Non-functional requirements specified
- Integration points identified
- Security requirements defined

#### Spec-Kit Specific
- Features are scoped appropriately (not too broad)
- Technical constraints are concrete
- User stories can be derived from features
- Acceptance criteria inferable

Once PRDs are validated and locked:
1. This workflow file is no longer loaded
2. Run `/specs` to generate specifications with spec-kit
3. Each asset PRD generates its own specs
4. Specs organized as `/ai_project/specs/FEAT-XXX/`
5. Spec-kit will create: spec.md, plan.md, contracts/, tasks.md

---

**NOTE**: This file should NOT be loaded once PRD status is 'locked' or 'approved' to save context tokens.