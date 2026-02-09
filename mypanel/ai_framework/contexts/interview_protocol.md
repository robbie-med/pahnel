# Interactive Interview Protocol
**CONDITIONAL LOAD**: Load when interview mode is active for PRD or Spec development

## Purpose

This context provides structured interview capabilities using the AskUserQuestion tool to guide users through PRD and specification development. Interviews replace free-form questioning with guided, multiple-choice interactions that ensure comprehensive coverage.

## When This File Loads

```python
def should_load_interview_protocol():
    """
    Load interview protocol when structured interviews are needed
    """
    return any([
        command == '/prd' and user_chose_interview_mode(),
        exists("/ai_project/state/interview_progress.json"),  # Resume active interview
        command == '/specs' and feature_scoping_needed(),
        explicit_interview_trigger()
    ])
```

## Interview State Management

### Interview Progress Tracking
```json
{
  "interview_type": "prd|spec|feature_scoping",
  "prd_file": "PRD.md",
  "current_stage": "target_audience",
  "completed_stages": ["project_discovery", "purpose_mission"],
  "answers_collected": {
    "project_type": "new_greenfield",
    "complexity_level": ["multiple_systems", "integrations"],
    "primary_deliverables": ["web_portal", "api_service"],
    "target_users": ["customers", "api_consumers"]
  },
  "assets_identified": [
    {"name": "WebPortal", "file": "PRD_WebPortal.md", "status": "pending"},
    {"name": "API", "file": "PRD_API.md", "status": "pending"}
  ],
  "next_stage": "features_discovery",
  "started": "2024-01-15T10:00:00Z",
  "last_updated": "2024-01-15T10:30:00Z"
}
```

**File Location**: `/ai_project/state/interview_progress.json`
**Lifecycle**: Created on interview start → Updated after each stage → Deleted when PRD approved/locked

## PRD Interview Stages

### Stage 1: Project Discovery

**Purpose**: Understand project structure and complexity
**Extended Thinking**: ACTIVE (analyzing project architecture patterns)

#### Interview Set 1A - Project Structure
```python
def interview_project_structure():
    questions = [{
        "question": "What type of project is this?",
        "header": "Type",
        "multiSelect": False,
        "options": [
            {
                "label": "New greenfield project",
                "description": "Starting from scratch with no existing system"
            },
            {
                "label": "Enhancement to existing",
                "description": "Adding features to current system"
            },
            {
                "label": "Migration/modernization",
                "description": "Replacing or upgrading legacy system"
            },
            {
                "label": "Research/prototype",
                "description": "Exploratory or proof-of-concept work"
            }
        ]
    }, {
        "question": "What describes the complexity of your project?",
        "header": "Complexity",
        "multiSelect": True,
        "options": [
            {
                "label": "Single application",
                "description": "One main deliverable (web app, mobile app, or service)"
            },
            {
                "label": "Multiple systems",
                "description": "Several interconnected applications or services"
            },
            {
                "label": "Third-party integrations",
                "description": "Connects with external APIs or services"
            },
            {
                "label": "Complex data processing",
                "description": "Heavy computation, analytics, or data transformation"
            }
        ]
    }]

    return AskUserQuestion(questions)
```

#### Interview Set 1B - Deliverables
```python
def interview_deliverables():
    """Identify primary deliverables - becomes assets if multiple"""
    questions = [{
        "question": "What are the primary deliverables you're building?",
        "header": "Assets",
        "multiSelect": True,
        "options": [
            {
                "label": "Web application/portal",
                "description": "Browser-based application for users"
            },
            {
                "label": "Mobile app (iOS/Android)",
                "description": "Native or cross-platform mobile application"
            },
            {
                "label": "API/backend service",
                "description": "RESTful API, GraphQL, or microservices"
            },
            {
                "label": "Administrative dashboard",
                "description": "Internal tools for managing the system"
            }
        ]
    }, {
        "question": "Who are the primary users of this system?",
        "header": "Audience",
        "multiSelect": True,
        "options": [
            {
                "label": "End consumers/customers",
                "description": "Public users or customers of your service"
            },
            {
                "label": "Business/enterprise users",
                "description": "Organizations or professional users"
            },
            {
                "label": "Internal staff/admins",
                "description": "Your team managing the system"
            },
            {
                "label": "Developers/API consumers",
                "description": "Technical users integrating with your API"
            }
        ]
    }]

    return AskUserQuestion(questions)
```

#### Processing Project Discovery
```python
def process_project_discovery(answers):
    """
    Process stage 1 answers and determine structure
    Extended Thinking: Analyze complexity patterns and asset relationships
    """
    state = create_or_load_interview_state()
    state["answers_collected"].update(answers)

    # Determine if multi-asset structure needed
    deliverables = answers.get("primary_deliverables", [])
    if len(deliverables) > 1:
        state["structure_type"] = "multi_asset"
        # Identify assets from deliverable names
        assets = []
        for deliverable in deliverables:
            asset_name = normalize_asset_name(deliverable)
            assets.append({
                "name": asset_name,
                "file": f"PRD_{asset_name}.md",
                "status": "pending",
                "type": deliverable
            })
        state["assets_identified"] = assets
    else:
        state["structure_type"] = "single"

    state["completed_stages"].append("project_discovery")
    state["current_stage"] = "purpose_mission"

    save_interview_state(state)

    # Show what was understood
    show_stage_summary("Project Discovery", answers, state)

    return state

def normalize_asset_name(deliverable_label):
    """Convert deliverable labels to clean asset names"""
    mapping = {
        "Web application/portal": "WebPortal",
        "Mobile app (iOS/Android)": "MobileApp",
        "API/backend service": "API",
        "Administrative dashboard": "AdminDashboard"
    }
    return mapping.get(deliverable_label, deliverable_label.replace("/", "").replace(" ", ""))
```

### Stage 2: Purpose & Mission Discovery

**Purpose**: Define problem statement and value proposition
**Extended Thinking**: ACTIVE (problem domain analysis)

#### Interview Set 2A - Problem Definition
```python
def interview_problem_definition():
    questions = [{
        "question": "What category best describes the problem you're solving?",
        "header": "Problem",
        "multiSelect": False,
        "options": [
            {
                "label": "Process inefficiency",
                "description": "Automating manual work or streamlining workflows"
            },
            {
                "label": "Information access",
                "description": "Finding, organizing, or discovering information"
            },
            {
                "label": "Communication/collaboration",
                "description": "Connecting people or facilitating teamwork"
            },
            {
                "label": "Transaction/commerce",
                "description": "Buying, selling, or exchanging value"
            }
        ]
    }, {
        "question": "What's your solution approach?",
        "header": "Approach",
        "multiSelect": False,
        "options": [
            {
                "label": "Custom solution",
                "description": "Purpose-built for specific needs"
            },
            {
                "label": "Platform/marketplace",
                "description": "Connecting multiple parties or services"
            },
            {
                "label": "Integration/aggregation",
                "description": "Bringing together existing systems or data"
            },
            {
                "label": "Tool/utility service",
                "description": "Focused functionality for specific tasks"
            }
        ]
    }, {
        "question": "What's your market position?",
        "header": "Market",
        "multiSelect": False,
        "options": [
            {
                "label": "First mover/innovator",
                "description": "Creating new category or approach"
            },
            {
                "label": "Better alternative",
                "description": "Improving on existing solutions"
            },
            {
                "label": "Niche/specialized",
                "description": "Focused on specific industry or use case"
            },
            {
                "label": "Enterprise/custom",
                "description": "Tailored for specific organization"
            }
        ]
    }]

    return AskUserQuestion(questions)
```

#### Interview Set 2B - Value Proposition
```python
def interview_value_proposition():
    questions = [{
        "question": "What's the primary value driver for users?",
        "header": "Value",
        "multiSelect": False,
        "options": [
            {
                "label": "Cost savings/efficiency",
                "description": "Saves time, money, or resources"
            },
            {
                "label": "Revenue generation",
                "description": "Creates new income opportunities"
            },
            {
                "label": "Experience improvement",
                "description": "Makes tasks easier or more enjoyable"
            },
            {
                "label": "Compliance/risk reduction",
                "description": "Meets regulations or reduces liability"
            }
        ]
    }, {
        "question": "What gives you a competitive advantage?",
        "header": "Edge",
        "multiSelect": True,
        "options": [
            {
                "label": "Unique technology",
                "description": "Novel technical approach or algorithms"
            },
            {
                "label": "Better UX",
                "description": "Significantly improved user experience"
            },
            {
                "label": "Performance/cost",
                "description": "Faster, cheaper, or more scalable"
            },
            {
                "label": "Domain expertise",
                "description": "Deep understanding of industry/users"
            }
        ]
    }]

    return AskUserQuestion(questions)
```

#### Processing Purpose & Mission
```python
def process_purpose_mission(answers):
    """
    Process stage 2 and populate PRD purpose section
    Extended Thinking: Analyze problem-solution fit and value proposition
    """
    state = load_interview_state()
    state["answers_collected"].update(answers)

    # Populate PRD Purpose & Mission section
    populate_prd_section(state["prd_file"], "purpose_mission", answers)

    state["completed_stages"].append("purpose_mission")
    state["current_stage"] = "target_audience"

    save_interview_state(state)
    show_stage_summary("Purpose & Mission", answers, state)

    return state
```

### Stage 3: Target Audience Deep Dive

**Purpose**: Understand user characteristics and scale
**Extended Thinking**: ACTIVE (user persona development)

#### Interview Set 3A - User Characteristics
```python
def interview_user_characteristics():
    questions = [{
        "question": "What's the technical sophistication of your primary users?",
        "header": "Tech Level",
        "multiSelect": False,
        "options": [
            {
                "label": "Non-technical",
                "description": "Consumer-level users (like smartphone apps)"
            },
            {
                "label": "Business users",
                "description": "Comfortable with office software and web tools"
            },
            {
                "label": "Technical users",
                "description": "Developers, IT professionals, or power users"
            },
            {
                "label": "Mixed audience",
                "description": "Multiple user types requiring adaptive interface"
            }
        ]
    }, {
        "question": "What's the geographic scope of your users?",
        "header": "Geography",
        "multiSelect": False,
        "options": [
            {
                "label": "Local/single city",
                "description": "Focused on one metropolitan area"
            },
            {
                "label": "Regional/state",
                "description": "Multiple cities or state-wide"
            },
            {
                "label": "National",
                "description": "Single country"
            },
            {
                "label": "International/global",
                "description": "Multiple countries, localization needed"
            }
        ]
    }, {
        "question": "What's your expected user scale?",
        "header": "Scale",
        "multiSelect": False,
        "options": [
            {
                "label": "Small (<1K users)",
                "description": "Internal tool or small customer base"
            },
            {
                "label": "Medium (1K-50K)",
                "description": "Growing business or regional service"
            },
            {
                "label": "Large (50K-1M)",
                "description": "Established business or popular service"
            },
            {
                "label": "Massive (>1M)",
                "description": "Large-scale consumer or enterprise platform"
            }
        ]
    }]

    return AskUserQuestion(questions)
```

#### Processing Target Audience
```python
def process_target_audience(answers):
    """
    Process stage 3 and populate PRD audience sections
    Extended Thinking: Develop detailed user personas from answers
    """
    state = load_interview_state()
    state["answers_collected"].update(answers)

    populate_prd_section(state["prd_file"], "target_audience", answers)

    state["completed_stages"].append("target_audience")
    state["current_stage"] = "features_discovery"

    save_interview_state(state)
    show_stage_summary("Target Audience", answers, state)

    return state
```

### Stage 4: Features Discovery

**Purpose**: Identify core features per asset
**Extended Thinking**: ACTIVE (feature dependency analysis and scoping)

#### Interview Set 4A - Feature Categories
```python
def interview_feature_categories(asset_name=None):
    """
    Interview for feature categories - runs per asset if multi-asset
    asset_name: None for single PRD, or "WebPortal", "API", etc for assets
    """
    asset_label = f" for {asset_name}" if asset_name else ""

    questions = [{
        "question": f"What data operations are needed{asset_label}?",
        "header": "Data",
        "multiSelect": True,
        "options": [
            {
                "label": "Create/input data",
                "description": "Users add new records, files, or information"
            },
            {
                "label": "Search/filter data",
                "description": "Users find and filter existing information"
            },
            {
                "label": "View/display data",
                "description": "Users browse and read information"
            },
            {
                "label": "Edit/update data",
                "description": "Users modify existing records"
            }
        ]
    }, {
        "question": f"What user-related features are needed{asset_label}?",
        "header": "Users",
        "multiSelect": True,
        "options": [
            {
                "label": "Authentication/login",
                "description": "User accounts and secure access"
            },
            {
                "label": "User profiles",
                "description": "Personal settings and preferences"
            },
            {
                "label": "Role-based access",
                "description": "Different permissions for user types"
            },
            {
                "label": "Notifications/alerts",
                "description": "Email, push, or in-app notifications"
            }
        ]
    }, {
        "question": f"What business logic is required{asset_label}?",
        "header": "Logic",
        "multiSelect": True,
        "options": [
            {
                "label": "Workflows/processes",
                "description": "Multi-step processes or approval flows"
            },
            {
                "label": "Calculations/processing",
                "description": "Computations, transformations, or algorithms"
            },
            {
                "label": "Integrations/APIs",
                "description": "Connect to external services or data"
            },
            {
                "label": "Reporting/analytics",
                "description": "Dashboards, metrics, or data visualization"
            }
        ]
    }, {
        "question": f"What administrative functions are needed{asset_label}?",
        "header": "Admin",
        "multiSelect": True,
        "options": [
            {
                "label": "User management",
                "description": "Admin tools for managing accounts"
            },
            {
                "label": "System configuration",
                "description": "Settings and system parameters"
            },
            {
                "label": "Monitoring/logging",
                "description": "System health and audit trails"
            },
            {
                "label": "Content management",
                "description": "Manage static content or templates"
            }
        ]
    }]

    return AskUserQuestion(questions)
```

#### Interview Set 4B - Feature Priority
```python
def interview_feature_priority():
    questions = [{
        "question": "What's your MVP scope philosophy?",
        "header": "MVP",
        "multiSelect": False,
        "options": [
            {
                "label": "Minimal viable",
                "description": "Core workflow only, bare minimum features"
            },
            {
                "label": "Standard viable",
                "description": "Common expected features included"
            },
            {
                "label": "Rich viable",
                "description": "Polished experience with nice-to-haves"
            },
            {
                "label": "Phased approach",
                "description": "Multiple staged releases planned"
            }
        ]
    }, {
        "question": "How much innovation is involved?",
        "header": "Innovation",
        "multiSelect": False,
        "options": [
            {
                "label": "Standard patterns",
                "description": "Using well-established approaches only"
            },
            {
                "label": "Some novel features",
                "description": "Mix of standard and new approaches"
            },
            {
                "label": "Significant innovation",
                "description": "Several unique or experimental features"
            },
            {
                "label": "Research/experimental",
                "description": "Cutting-edge, unproven concepts"
            }
        ]
    }]

    return AskUserQuestion(questions)
```

#### Processing Features Discovery
```python
def process_features_discovery(answers):
    """
    Process stage 4 and populate feature sections
    Extended Thinking: Analyze feature dependencies and suggest breakdown
    """
    state = load_interview_state()

    # Handle multi-asset: run feature interview per asset
    if state.get("structure_type") == "multi_asset":
        # Process features for each asset
        for asset in state["assets_identified"]:
            asset_answers = interview_feature_categories(asset["name"])
            populate_prd_section(asset["file"], "features", asset_answers)
            asset["status"] = "features_complete"

        # Get global feature priority
        priority_answers = interview_feature_priority()
        answers.update(priority_answers)
    else:
        # Single asset - populate main PRD
        populate_prd_section(state["prd_file"], "features", answers)

    state["answers_collected"].update(answers)
    state["completed_stages"].append("features_discovery")
    state["current_stage"] = "technical_requirements"

    save_interview_state(state)
    show_stage_summary("Features Discovery", answers, state)

    return state
```

### Stage 5: Technical Requirements

**Purpose**: Define technology stack and non-functional requirements
**Extended Thinking**: ACTIVE (architecture pattern analysis and tech stack validation)

#### Interview Set 5A - Technology Stack
```python
def interview_technology_stack():
    questions = [{
        "question": "What's your preferred backend language/framework?",
        "header": "Backend",
        "multiSelect": False,
        "options": [
            {
                "label": "Python",
                "description": "FastAPI, Django, or Flask"
            },
            {
                "label": "Node.js/TypeScript",
                "description": "Express, NestJS, or Fastify"
            },
            {
                "label": "Java/Kotlin",
                "description": "Spring Boot or Micronaut"
            },
            {
                "label": "Go/Rust",
                "description": "High performance compiled languages"
            }
        ]
    }, {
        "question": "What frontend approach will you use?",
        "header": "Frontend",
        "multiSelect": False,
        "options": [
            {
                "label": "React",
                "description": "Next.js, Remix, or Vite + React"
            },
            {
                "label": "Vue.js",
                "description": "Nuxt or Vue 3 composition API"
            },
            {
                "label": "Angular",
                "description": "Full Angular framework"
            },
            {
                "label": "Svelte/SolidJS",
                "description": "Modern compiled frameworks"
            }
        ]
    }, {
        "question": "What database types do you need?",
        "header": "Database",
        "multiSelect": True,
        "options": [
            {
                "label": "SQL relational",
                "description": "PostgreSQL, MySQL, or similar"
            },
            {
                "label": "NoSQL document",
                "description": "MongoDB, DynamoDB, or Firestore"
            },
            {
                "label": "Graph database",
                "description": "Neo4j or similar for complex relationships"
            },
            {
                "label": "Cache/key-value",
                "description": "Redis, Memcached for caching"
            }
        ]
    }, {
        "question": "What's your infrastructure approach?",
        "header": "Infra",
        "multiSelect": False,
        "options": [
            {
                "label": "Cloud managed",
                "description": "AWS, Azure, or GCP managed services"
            },
            {
                "label": "Containerized",
                "description": "Docker + Kubernetes for orchestration"
            },
            {
                "label": "Serverless",
                "description": "Lambda, Cloud Functions, or similar"
            },
            {
                "label": "Traditional hosting",
                "description": "VPS or dedicated servers"
            }
        ]
    }]

    return AskUserQuestion(questions)
```

#### Interview Set 5B - Non-Functional Requirements
```python
def interview_nonfunctional_requirements():
    questions = [{
        "question": "What are your performance requirements?",
        "header": "Performance",
        "multiSelect": False,
        "options": [
            {
                "label": "Standard (<2s)",
                "description": "Typical web application response times"
            },
            {
                "label": "Fast (<500ms)",
                "description": "Snappy, responsive user experience"
            },
            {
                "label": "Real-time (<100ms)",
                "description": "Near-instant response required"
            },
            {
                "label": "Batch/async OK",
                "description": "Background processing acceptable"
            }
        ]
    }, {
        "question": "What security requirements apply?",
        "header": "Security",
        "multiSelect": True,
        "options": [
            {
                "label": "Standard auth",
                "description": "Email/password with secure storage"
            },
            {
                "label": "SSO/OAuth",
                "description": "Third-party authentication required"
            },
            {
                "label": "Compliance",
                "description": "HIPAA, SOC2, GDPR, or similar"
            },
            {
                "label": "Advanced security",
                "description": "MFA, encryption at rest, penetration testing"
            }
        ]
    }, {
        "question": "What's your availability target?",
        "header": "Uptime",
        "multiSelect": False,
        "options": [
            {
                "label": "Standard (99%)",
                "description": "Occasional downtime acceptable (~3.5 days/year)"
            },
            {
                "label": "High (99.9%)",
                "description": "Minimal downtime (~8 hours/year)"
            },
            {
                "label": "Critical (99.99%)",
                "description": "Near-zero downtime (~52 minutes/year)"
            },
            {
                "label": "Best effort",
                "description": "Development or internal use only"
            }
        ]
    }]

    return AskUserQuestion(questions)
```

#### Processing Technical Requirements
```python
def process_technical_requirements(answers):
    """
    Process stage 5 and populate technical sections
    Extended Thinking: Validate tech stack compatibility and suggest architecture patterns
    """
    state = load_interview_state()
    state["answers_collected"].update(answers)

    populate_prd_section(state["prd_file"], "technical_requirements", answers)

    state["completed_stages"].append("technical_requirements")
    state["current_stage"] = "business_model"

    save_interview_state(state)
    show_stage_summary("Technical Requirements", answers, state)

    return state
```

### Stage 6: Business Model

**Purpose**: Define revenue model and success metrics
**Extended Thinking**: ACTIVE (business viability analysis)

#### Interview Set 6A - Business Fundamentals
```python
def interview_business_model():
    questions = [{
        "question": "What's your revenue model?",
        "header": "Revenue",
        "multiSelect": True,
        "options": [
            {
                "label": "Subscription (SaaS)",
                "description": "Recurring monthly or annual fees"
            },
            {
                "label": "Transaction fees",
                "description": "Percentage or fee per transaction"
            },
            {
                "label": "Usage-based",
                "description": "Pay for what you use (API calls, storage, etc)"
            },
            {
                "label": "No revenue",
                "description": "Internal tool or free service"
            }
        ]
    }, {
        "question": "What's your expected cost structure?",
        "header": "Costs",
        "multiSelect": False,
        "options": [
            {
                "label": "Development only",
                "description": "One-time build, minimal ongoing costs"
            },
            {
                "label": "Dev + hosting",
                "description": "Build cost plus infrastructure expenses"
            },
            {
                "label": "Dev + hosting + support",
                "description": "Including customer support and maintenance"
            },
            {
                "label": "Full operations",
                "description": "Complete operational overhead (sales, marketing, etc)"
            }
        ]
    }, {
        "question": "What are your key success metrics?",
        "header": "Metrics",
        "multiSelect": True,
        "options": [
            {
                "label": "User growth/adoption",
                "description": "Number of users or customers"
            },
            {
                "label": "Revenue/profitability",
                "description": "Financial performance"
            },
            {
                "label": "Performance/uptime",
                "description": "Technical reliability metrics"
            },
            {
                "label": "User satisfaction",
                "description": "NPS, CSAT, or retention rates"
            }
        ]
    }]

    return AskUserQuestion(questions)
```

#### Processing Business Model
```python
def process_business_model(answers):
    """
    Process final stage and complete PRD structure
    Extended Thinking: Analyze business model viability and metric alignment
    """
    state = load_interview_state()
    state["answers_collected"].update(answers)

    populate_prd_section(state["prd_file"], "business_model", answers)

    state["completed_stages"].append("business_model")
    state["current_stage"] = "complete"

    save_interview_state(state)
    show_stage_summary("Business Model", answers, state)

    # Mark interview complete
    complete_prd_interview(state)

    return state
```

## Interview Completion

### Finalizing PRD After Interview
```python
def complete_prd_interview(state):
    """
    Finalize PRD after all interview stages complete
    Extended Thinking: Final PRD validation and completeness check
    """
    print("\n" + "="*60)
    print("🎉 PRD INTERVIEW COMPLETE!")
    print("="*60 + "\n")

    # Show complete summary
    print("## Project Summary\n")
    answers = state["answers_collected"]

    print(f"**Type**: {answers.get('project_type', 'N/A')}")
    print(f"**Structure**: {state.get('structure_type', 'single').upper()}")

    if state.get("structure_type") == "multi_asset":
        print(f"\n**Assets Created**:")
        for asset in state["assets_identified"]:
            print(f"  • {asset['name']} ({asset['file']})")

    print(f"\n**Files Created**:")
    print(f"  • {state['prd_file']}")
    if state.get("structure_type") == "multi_asset":
        print(f"  • PRD_Branding.yaml")
        print(f"  • PRD_Entity.yaml")
        for asset in state["assets_identified"]:
            print(f"  • {asset['file']}")

    # Validate PRD completeness with spec-kit bridge
    from ai_framework.tools.spec_kit_bridge import SpecKitBridge
    bridge = SpecKitBridge(get_framework_root())
    validation = bridge.validate_prd_for_spec_kit(Path(state["prd_file"]))

    print(f"\n## Spec-Kit Readiness: {validation['completeness_score']}%")

    if validation["completeness_score"] >= 90:
        print("✅ EXCELLENT - PRD is fully ready for specification generation")
    elif validation["completeness_score"] >= 70:
        print("✅ GOOD - PRD has sufficient detail for spec generation")
    else:
        print("⚠️  NEEDS WORK - Consider adding more detail before generating specs")

    # Offer next steps
    print("\n## Next Steps\n")
    print("1. Review the generated PRD files and add any custom details")
    print("2. Run `/specs` or `/specify` to generate technical specifications")
    print("3. Run `/tasks` to create implementation task lists")

    # Update PRD status
    update_prd_status(state["prd_file"], "draft")

    # Clean up interview state (interview complete)
    clear_interview_state()

    print("\n" + "="*60)
```

## Resume Capability

### Detecting Interrupted Interviews
```python
def check_for_interrupted_interview():
    """
    Check if there's an active interview to resume
    Called at start of /prd command
    """
    if exists("/ai_project/state/interview_progress.json"):
        state = load_interview_state()

        # Check if not too old (24 hours)
        started = parse_datetime(state["started"])
        age = now() - started

        if age > timedelta(hours=24):
            print("⚠️  Found old interview session (>24 hours)")
            response = AskUserQuestion([{
                "question": "There's an old interview session. What would you like to do?",
                "header": "Resume?",
                "multiSelect": False,
                "options": [
                    {"label": "Resume", "description": "Continue from where you left off"},
                    {"label": "Start Over", "description": "Begin fresh interview"},
                    {"label": "Review First", "description": "See what was completed"}
                ]
            }])

            if response["answers"]["resume"] == "Start Over":
                clear_interview_state()
                return None
            elif response["answers"]["resume"] == "Review First":
                show_interview_progress(state)
                # Ask again after review
                return check_for_interrupted_interview()

        # Valid resumption
        print(f"\n🔄 Resuming PRD interview...")
        print(f"Completed: {', '.join(state['completed_stages'])}")
        print(f"Next: {state['current_stage']}\n")

        return state

    return None
```

### Showing Interview Progress
```python
def show_interview_progress(state):
    """Display current interview progress"""
    all_stages = [
        "project_discovery",
        "purpose_mission",
        "target_audience",
        "features_discovery",
        "technical_requirements",
        "business_model"
    ]

    print("\n" + "="*60)
    print("📋 PRD INTERVIEW PROGRESS")
    print("="*60 + "\n")

    for stage in all_stages:
        if stage in state["completed_stages"]:
            print(f"✅ {stage.replace('_', ' ').title()}")
        elif stage == state["current_stage"]:
            print(f"🔄 {stage.replace('_', ' ').title()} (In Progress)")
        else:
            print(f"⏸️  {stage.replace('_', ' ').title()} (Pending)")

    print(f"\nPRD File: {state['prd_file']}")
    print(f"Started: {state['started']}")
    print(f"Last Updated: {state['last_updated']}")
    print("\n" + "="*60 + "\n")
```

## Specification Interview (Feature Scoping)

### Feature Scoping Interview
**Trigger**: During `/specs` command when feature needs scoping
**Extended Thinking**: ACTIVE (feature breakdown and contract design)

```python
def interview_feature_scoping(feature_description):
    """
    Interview to properly scope a feature before spec generation
    Returns scoped feature definition for spec-kit
    """
    print(f"\n## Feature Scoping: {feature_description[:60]}...\n")
    print("[Extended Thinking Active - Analyzing feature scope]\n")

    questions = [{
        "question": "What's the primary user goal for this feature?",
        "header": "User Goal",
        "multiSelect": False,
        "options": [
            {
                "label": "Create/input data",
                "description": "Users need to add new information"
            },
            {
                "label": "Find/search data",
                "description": "Users need to discover existing information"
            },
            {
                "label": "Process/transform",
                "description": "System needs to compute or transform data"
            },
            {
                "label": "Communicate/notify",
                "description": "Users need to send or receive messages"
            }
        ]
    }, {
        "question": "What's the feature complexity level?",
        "header": "Complexity",
        "multiSelect": False,
        "options": [
            {
                "label": "Simple",
                "description": "Single screen/endpoint, minimal logic"
            },
            {
                "label": "Moderate",
                "description": "Multiple steps, some business logic"
            },
            {
                "label": "Complex",
                "description": "Multi-screen workflow, complex validation"
            },
            {
                "label": "Advanced",
                "description": "Heavy computation, integrations, real-time"
            }
        ]
    }, {
        "question": "What user interactions are required?",
        "header": "Interactions",
        "multiSelect": True,
        "options": [
            {
                "label": "Forms/input",
                "description": "Users enter data via forms"
            },
            {
                "label": "Lists/tables",
                "description": "Display collections of data"
            },
            {
                "label": "Details/views",
                "description": "Show individual item details"
            },
            {
                "label": "Real-time updates",
                "description": "Live data or notifications"
            }
        ]
    }, {
        "question": "What backend operations are needed?",
        "header": "Backend",
        "multiSelect": True,
        "options": [
            {
                "label": "CRUD operations",
                "description": "Create, read, update, delete data"
            },
            {
                "label": "Business logic",
                "description": "Calculations, validations, rules"
            },
            {
                "label": "External integrations",
                "description": "Call external APIs or services"
            },
            {
                "label": "Background jobs",
                "description": "Asynchronous processing"
            }
        ]
    }]

    answers = AskUserQuestion(questions)

    # Use Extended Thinking to analyze and suggest breakdown
    scope_analysis = analyze_feature_with_extended_thinking(
        feature_description,
        answers
    )

    return scope_analysis
```

## Helper Functions

### Stage Summary Display
```python
def show_stage_summary(stage_name, answers, state):
    """Show what was understood after each stage"""
    print(f"\n✅ {stage_name} Complete!\n")
    print("Here's what I understood:\n")

    for key, value in answers.items():
        label = key.replace("_", " ").title()
        if isinstance(value, list):
            print(f"• {label}: {', '.join(value)}")
        else:
            print(f"• {label}: {value}")

    # Ask for confirmation
    response = AskUserQuestion([{
        "question": "Does this look correct?",
        "header": "Confirm",
        "multiSelect": False,
        "options": [
            {"label": "Continue", "description": "Move to next stage"},
            {"label": "Edit Answers", "description": "Correct something"},
            {"label": "Add Details", "description": "Provide more context"}
        ]
    }])

    if response["answers"]["confirm"] == "Edit Answers":
        # Re-run the stage interview
        return "edit"
    elif response["answers"]["confirm"] == "Add Details":
        # Allow free-form additions
        return "add_details"

    return "continue"
```

### PRD Population
```python
def populate_prd_section(prd_file, section, answers):
    """
    Populate PRD sections with interview answers
    Extended Thinking: Transform structured answers into narrative PRD content
    """
    # Read current PRD
    prd_content = read_file(prd_file)

    # Map answers to PRD sections based on stage
    if section == "purpose_mission":
        # Update Problem Statement, Mission, Value Proposition
        update_prd_purpose(prd_content, answers)

    elif section == "target_audience":
        # Update Primary Users, User Sophistication, Geographic Scope, Scale
        update_prd_audience(prd_content, answers)

    elif section == "features":
        # Update Core Features section
        update_prd_features(prd_content, answers)

    elif section == "technical_requirements":
        # Update Performance, Scale, Security, Platform sections
        update_prd_technical(prd_content, answers)

    elif section == "business_model":
        # Update Revenue Streams, Cost Structure, Success Metrics
        update_prd_business(prd_content, answers)

    # Write updated PRD
    write_file(prd_file, prd_content)
```

## Integration with Extended Thinking

### Automatic Activation
```python
def extended_thinking_active():
    """
    Extended Thinking automatically activates for:
    - All PRD interview stages
    - All spec generation work
    - Feature scoping analysis
    - Complex architectural decisions

    This is a model capability that activates based on context
    No explicit API call needed
    """
    return True  # Always active during interviews
```

### Visual Indicators
```python
def show_extended_thinking_indicator():
    """Show user that Extended Thinking is active"""
    print("\n[🧠 Extended Thinking Active - Deep Analysis Mode]\n")
```

## Summary

This interview protocol provides:
- ✅ Structured question flows for all PRD stages
- ✅ Multi-asset project support
- ✅ Resume capability for interrupted sessions
- ✅ Extended Thinking integration throughout
- ✅ Feature scoping for spec generation
- ✅ Comprehensive answer validation
- ✅ Automatic PRD population from answers

**Interview Mode Benefits**:
- Consistent, complete PRDs
- Reduced user cognitive load
- Clear progress tracking
- Higher spec-kit readiness scores
- Better architecture decisions via Extended Thinking
