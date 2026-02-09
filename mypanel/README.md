# Hegemon Framework - AI Development Orchestration System
**Version**: 3.4 (Spec-Kit v0.0.90 Edition)

*Leading AI models to consistent, high-quality outputs through structured orchestration and context sovereignty*

A comprehensive spec-driven development framework that transforms how AI assists in software development. Through intelligent agent orchestration, workflow modes, and automatic state persistence, Hegemon ensures every project follows best practices from requirements to production.

## Prerequisites

**Required:**
- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) - The AI assistant that runs Hegemon

**Recommended (for full functionality):**
- **Python 3.8+** - Powers workflow hooks and automation
- **git** - Version control and submodule management

**Optional (for advanced features):**
- **uv** - Isolated Python tool execution for `/specs` command
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- **ffmpeg** - Audio processing for `/tts` voice features
  ```bash
  brew install ffmpeg  # macOS
  ```

> **Note:** Hegemon works without optional dependencies. Features gracefully disable when dependencies are unavailable. Run `.claude/hooks/check_dependencies.sh` to verify your setup.

### Model Configuration

Hegemon defaults to Claude Opus for best results. If you don't have Opus access, update `.claude/settings.json`:

```json
{
  "model": "sonnet"
}
```

Or override per-session with: `claude --model sonnet`

## 🚀 Quick Command Reference

Start here - these commands guide your entire development workflow:

| Command | Purpose | When to Use |
|---------|---------|------------|
| `/init` | Initialize new project | First time setup from template |
| `/prime` | Load project & continue | Start any work session |
| `/prd` | Develop requirements | Define what you're building |
| `/specs` or `/specify` | Generate specifications | After PRD is complete |
| `/clarify` | Refine specifications | After initial spec, before plan |
| `/plan` | Create implementation plan | After specs ready |
| `/tasks` | Create task list | After plan is ready |
| `/analyze` | Cross-artifact check | Before implementation |
| `/state` | Check progress | Anytime to see status |
| `/save` | Save your work | Before breaks or context switches |

### Typical Workflow

```bash
# First time - new project
/init "My SaaS Project"     # Sets up everything
/prime                      # Loads context, ready to work
/prd                        # Start requirements gathering

# Continuing work
/prime                      # Resumes where you left off
/prd "add payment feature"  # Update requirements
/specs                      # Generate specifications
/clarify                    # Refine with targeted questions
/plan                       # Create implementation plan
/tasks init                 # Create implementation tasks
/analyze                    # Validate consistency

# During development
/state                      # Check current progress
/tasks                      # See what's next
/save "milestone reached"   # Checkpoint your work
```

## Installation & Migration

### Option 1: Fresh Project (New Development)
1. **Clone the framework**
   ```bash
   git clone <hegemon-repo> my-project
   cd my-project
   rm -rf .git  # Remove framework git history
   git init     # Start your own repository
   ```

2. **Launch your AI assistant**
   ```bash
   claude  # Claude Code CLI (recommended)
   # or
   cursor  # Cursor IDE
   # or  
   code .  # VSCode with Continue/Copilot
   ```

3. **Initialize the project**
   ```
   /init "Your project description"   # Sets up everything
   ```

### Option 2: Add to Existing Project (Migration)

#### For Non-Framework Projects
**Your project has no AI framework:**

1. **Get the migration tool**
   ```bash
   cd /your/existing/project
   
   # Download migration tool
   curl -o MIGRATION.md https://raw.githubusercontent.com/<hegemon-repo>/main/ai_framework/tools/MIGRATION.md
   ```

2. **Run migration**
   ```bash
   claude  # Start AI in your project
   ```
   Then tell the AI:
   ```
   "Read MIGRATION.md and migrate this project to Hegemon Framework v3.3"
   ```

#### For Projects with CLAUDE.md or AI Instructions
**Your project already has some AI guidance:**

1. **Same as above, but the migration will**:
   - Preserve your existing CLAUDE.md content
   - Port instructions to AI_PROJ_CONTEXT.md
   - Maintain all your custom directives

#### For Old Hegemon Versions (1.0, 2.0, 3.0, 3.1, 3.2)
**Upgrading from previous Hegemon:**

1. **Get migration tool and run**:
   ```bash
   cd /your/hegemon/project
   curl -o MIGRATION.md https://raw.githubusercontent.com/<hegemon-repo>/main/ai_framework/tools/MIGRATION.md
   claude
   ```

2. **Tell the AI**:
   ```
   "This is a Hegemon [version] project. Read MIGRATION.md and upgrade to v3.3"
   ```

### Migration Safety Features
- **Zero Deletions**: Nothing is ever deleted, only archived
- **Full Backup**: Everything backed up to `MIGRATION_ARCHIVE/`
- **Interactive Process**: Asks permission for every change
- **Detailed Report**: Complete log in `MIGRATION_ARCHIVE/MIGRATION_REPORT.md`
- **Rollback Available**: Instructions provided if needed

### What Gets Migrated
```
MIGRATION_ARCHIVE/
├── MIGRATION_REPORT.md       # What was done
├── original_structure/       # Complete backup
├── replaced_files/          # Updated files
└── deprecated_templates/    # Old framework files

Your Project/
├── AI_CONTEXT.md           # Added (framework directives)
├── ai_project/             # Added (YOUR project work - tracked in git)
│   ├── specs/              # YOUR specifications
│   ├── tasks/              # YOUR task lists
│   ├── state/              # YOUR session state
│   ├── contexts/           # YOUR project customizations
│   └── resources/          # YOUR examples and assets
├── ai_framework/           # Added (framework helpers)
│   ├── templates/          # Framework templates
│   ├── contexts/           # Conditional contexts
│   ├── rules/              # Framework rules
│   └── tools/              # Framework utilities
├── .claude/                # Added (AI configuration)
├── PRD.md                  # YOUR requirements (tracked in git)
├── PRD_*.md                # YOUR requirement docs (tracked in git)
└── [YOUR CODE]             # Untouched - never modified
```

## Quick Start After Installation

### Resuming Work
When returning to an existing project:
```
/prime          # Smart resume - picks up where you left off
/state          # Check current status and next steps
/tasks          # See task progress

# Or use @hege commands (any AI model)
@hege resume    # Continue from checkpoint
@hege context   # Display current work
```

## Key Features

### 🤖 Intelligent Agent System with Parallel Execution
Hegemon includes 15 specialized agents that activate automatically based on context:

**Core Development:**
- **Analyst Agent**: PRD building and requirements gathering
- **Architect Agent**: System design and technical specifications
- **PM Agent**: Project management, task generation, documentation
- **Dev Agent**: Implementation of approved stories
- **QA Agent**: Testing and validation

**Executive & Support:** CEO, CFO, Legal, Marketing, Editor, Researcher, Support, Writer
**Design:** UI, UX

Plus **Primary Agent** for framework coordination and parallel orchestration

#### Multi-Agent Parallel Execution (NEW)
Launch up to 5 agents simultaneously for independent tasks:
```bash
# Work on multiple tasks in parallel
/agent analyst "complete market analysis"
/agent architect "design system architecture" 
/agent dev "prototype authentication"

# Monitor all agents
/agent

# Automatic recovery after crashes
/state  # Resumes all parallel agents
```

Every response includes an agent header:
```
[AGENT:dev|MODE:implementation|TASK:STORY-042]
```

### 🧠 Interactive Interview Mode with Extended Thinking (NEW in v3.2)

**Revolutionize PRD and Spec Development** with guided interviews and deep analysis:

#### Interactive PRD Development
Choose between two modes when building requirements:

**Interview Mode** (Recommended):
- Guided multi-choice questions ensure completeness
- 6 structured stages covering all aspects:
  1. Project Discovery (structure and complexity)
  2. Purpose & Mission (problem and value prop)
  3. Target Audience (users and scale)
  4. Features Discovery (capabilities per asset)
  5. Technical Requirements (stack and infrastructure)
  6. Business Model (revenue and metrics)
- Automatic PRD population from answers
- Resume capability for interrupted sessions
- Consistently achieves 85%+ PRD completeness

**Conversational Mode** (Classic):
- Free-form discussion for maximum flexibility
- Full backward compatibility maintained

```bash
/prd  # Choose your mode on first run

# Interview mode presents structured questions:
[🧠 Extended Thinking Active - Deep Analysis Mode]

Question 1 of 3: What type of project is this?
○ New greenfield project
○ Enhancement to existing system
○ Migration/modernization effort
○ Research/prototype phase
```

#### Extended Thinking Everywhere
**Automatic activation** for deep analysis during:
- ALL PRD development work
- ALL specification generation
- Feature scoping and breakdown
- Architecture decisions
- Complex requirements analysis

Benefits:
- Identifies unstated assumptions
- Validates architecture patterns
- Analyzes technology trade-offs
- Discovers edge cases proactively
- Ensures business model viability

Visual indicator shows when active:
```
[🧠 Extended Thinking Active - Deep Analysis Mode]
```

#### Feature Scoping Interviews
When generating specs, interactive interviews help scope features properly:
```bash
/specs "user authentication system"

# Automatically asks:
- User goal (create/find/process/communicate)
- Complexity level (simple/moderate/complex/advanced)
- Required interactions (forms/lists/details/real-time)
- Backend operations (CRUD/logic/integrations/jobs)

# Extended Thinking analyzes answers and suggests optimal breakdown
```

#### State Management for Interviews
Interviews can be interrupted and resumed seamlessly:
- Progress saved after each stage
- Resume from last completed section
- 24-hour session validity
- Clean state on completion

```bash
# Start interview
/prd
# Complete 2 of 6 stages, then stop

# Later - automatic resume
/prd  # Continues from stage 3
```

### 🎯 Spec-Driven Development
- **PRD-First Approach**: Interactive discovery builds comprehensive requirements
- **Smart Examples**: Framework requests specific examples when needed
- **Specification Generation**: Automatic tech specs from approved PRD
- **Context-Rich Stories**: Every task includes full requirements context
- **Locked Documents**: Approved docs become immutable truth source

### 🔄 Automatic State Management
- **Never Lose Work**: State saved after every action
- **Seamless Recovery**: Resume exactly where you left off
- **Survives Everything**: Model swaps, crashes, clear commands
- **Multi-Session Support**: Perfect continuity across sessions
- **Agent Communication**: Agents pass context between handoffs

### 🎮 Workflow Mode Enforcement
Three distinct modes prevent inappropriate actions:
- **Planning Mode**: Design and specifications only (no code changes)
- **Task Mode**: Implementation of approved tasks only
- **Direct Mode**: Explicit override for urgent requests

### 🔀 Universal Compatibility
- **Model Agnostic**: Works with Claude, GPT, Gemini, any LLM
- **IDE Flexible**: VSCode, Cursor, Claude Code CLI, any editor
- **Command Systems**: Native slash commands + universal @hege commands
- **State Portability**: JSON format works everywhere

### 📁 Framework Structure (v3.2)
```
root/
├── AI_CONTEXT.md         # Framework directives
├── CLAUDE.md             # Lightweight pointer to AI_CONTEXT
├── PRD.md                # YOUR project requirements (TRACKED IN GIT)
├── PRD_*.md              # Additional requirement docs (TRACKED IN GIT)
│
├── ai_project/           # YOUR PROJECT WORK (ALL tracked in git)
│   ├── specs/            # YOUR specifications
│   │   └── FEAT-001-name/  # Feature directories
│   │       ├── spec.md     # Feature specification
│   │       ├── plan.md     # Implementation plan
│   │       └── contracts/  # API contracts
│   ├── tasks/            # YOUR task lists
│   │   └── task-list.md  # T001, T002 format
│   ├── state/            # YOUR session state (for recovery)
│   │   ├── session_state.json
│   │   ├── checkpoint.json
│   │   └── agent_handoff.json
│   ├── contexts/         # YOUR project customizations
│   │   ├── AI_PROJ_CONTEXT.md     # Project-specific directives
│   │   └── PROJ_Constitution.md   # Project principles
│   └── resources/        # YOUR examples and assets
│       ├── examples/     # Mockups, data samples
│       ├── reference/    # Guides, docs
│       └── assets/       # Images and files
│
├── ai_framework/         # Framework helpers (serve your project)
│   ├── templates/        # Starting templates (PRD, Spec, etc.)
│   ├── contexts/         # Conditional loading contexts
│   ├── rules/            # Framework operation rules
│   ├── agents/           # Agent documentation
│   └── tools/            # Framework utilities (spec-kit, migration)
│
├── .claude/              # Claude Code configuration
│   ├── agents/           # 15 agent definitions
│   ├── commands/         # Slash commands (/prime, /prd, /specs, etc.)
│   └── hooks/            # Event automation
│
└── [Your Source Code]    # Your actual application code
    ├── src/              # Source files (your structure)
    ├── tests/            # Test files (your structure)
    └── ...               # Whatever structure your project needs
```

**⚠️ CRITICAL - PROJECT-FIRST PHILOSOPHY**:
- **YOUR project work** (PRDs, specs, tasks, state) **MUST be tracked in git**
- Specs go in `/ai_project/specs/FEAT-XXX/` directories
- Framework files in `/ai_framework/` are helpers that serve your project
- The framework exists to support YOUR project, not the other way around

## Development Workflow

### Phase 1: PRD Discovery (Analyst Agent)
The framework guides you through structured discovery:
1. **Purpose & Mission** - What problem are you solving?
2. **Target Audience** - Who will use this?
3. **Core Features** - MVP, future features, non-goals
4. **Technical Requirements** - Performance, scale, security
5. **Business Model** - Revenue, competition, metrics

**Smart Examples**: The framework identifies when examples would help and creates specific directories:
```
"I see you're describing complex UI workflows. 
Creating /ai_framework/resources/examples/ui-mockups/
Could you provide mockups of the dashboard?"
```

### Phase 2: Specification Generation (Architect Agent)
Once PRD is approved and locked, specs are auto-generated:
- Technical architecture and stack selection
- Database design and API contracts  
- User personas and journey maps
- Security and scaling patterns
- Testing requirements

All specs go in `/ai_framework/specs/` with clear naming.

### Phase 3: Story Engineering (PM Agent)
Specs transform into context-rich stories:
- Each story includes full PRD/spec context
- Dependencies mapped automatically
- Effort estimates and priorities
- Acceptance criteria embedded
- Cross-references to requirements

Example story header:
```markdown
# STORY-042: Implement User Authentication
**Context**: PRD Section 3.1, Spec: auth-flow.md
**Dependencies**: STORY-038, STORY-040
**Estimate**: 8 points
```

### Phase 4: Implementation (Dev Agent)
Only approved stories can be implemented:
```
[AGENT:dev|MODE:task|TASK:STORY-042]
✅ Task STORY-042 approved and dependencies met
🔨 Beginning implementation of user authentication...
```

If you try to code without a task:
```
❌ Cannot modify code without approved task
💡 Current mode: PLANNING - Switch to TASK mode
📋 Or create a task first: @hege mode task
```

## Expected Behaviors

### Agent Headers in Every Response
```
[AGENT:analyst|MODE:prd_building|TASK:none]
Let's continue building your PRD. You mentioned the target 
audience includes enterprise clients. Could you elaborate on 
their typical size and industry?
```

### Automatic Agent Switching
```
User: "Let's design the authentication system"
[AGENT:architect|MODE:design|TASK:none]
I'll create the authentication architecture spec. Based on your 
PRD's security requirements, I recommend OAuth 2.0 with JWT...

User: "Can we test the login flow?"
[AGENT:qa|MODE:testing|TASK:none]
I'll create a test plan for the authentication system. First, 
let me review the implementation in STORY-042...
```

### State Recovery After Interruption
```
# After system crash or context clear:
User: "continue" 
[AGENT:primary|MODE:coordination|TASK:none]
Resuming YourProject - Phase: Implementation
Mode: TASK_MODE
Active: STORY-042 (Authentication) - 67% complete
Last action: Created JWT token service

Continuing with refresh token implementation...
```

### Mode Violation Prevention
```
User: "Add a caching layer to improve performance"
[AGENT:dev|MODE:planning|TASK:none]
⚠️ Currently in PLANNING mode - cannot modify code
Options:
1. Create a task for this enhancement
2. Switch to TASK mode: @hege mode task
3. Override with acknowledgment: @hege mode direct

Shall I create STORY-089 for the caching layer?
```

## Command Reference

### Claude Code CLI Slash Commands
- `/prime` - Full framework initialization and analysis
- `/state` - Current status, agent, mode, and tasks
- `/agent [name]` - View or switch agents
- `/mode [mode]` - Switch workflow modes
- `/save` - Force state persistence

### Universal @hege Commands (All Models)
- `@hege status` - Report current state
- `@hege reset` - Return to framework root
- `@hege agent <name>` - Force agent switch
- `@hege mode <mode>` - Change workflow mode
- `@hege resume` - Load last checkpoint
- `@hege validate` - Run framework checks
- `@hege context` - Display understanding

### Usage Examples
```
# Check where you are
/state
@hege status

# Switch to implementation
/agent dev "implement STORY-042"
@hege agent dev

# Change workflow mode
/mode task
@hege mode planning
```

## Best Practices

### Starting a New Project
1. **Use `/prime` or `@hege reset`** to initialize properly
2. **Complete PRD thoughtfully** - it drives everything
3. **Provide examples when asked** - but only specific ones
4. **Trust agent assignments** - they know their domains
5. **Review and lock PRD** before moving to specs

### During Development  
1. **Watch agent headers** - know who's responding
2. **Respect workflow modes** - they prevent mistakes
3. **Use story IDs** - reference STORY-XXX for implementation
4. **Let state management work** - it saves constantly
5. **Check dependencies** - framework tracks them

### Maintaining Progress
1. **Regular `/state` checks** - see where you are
2. **Use `@hege resume`** after breaks
3. **Review generated specs** - they're in `/ai_framework/specs/`
4. **Track story completion** - in `/ai_framework/tasks/`
5. **Trust the recovery** - checkpoint.json has everything

## Why Hegemon Works

### Intelligent Design Decisions
- **Agent Specialization**: Each agent is an expert in their domain
- **Mandatory Headers**: Always know who's acting and why
- **PRD Lock**: Prevents scope creep after approval
- **Mode Enforcement**: Can't accidentally code during planning
- **Story Context**: Every task includes full requirements
- **State Persistence**: Survives any interruption
- **Example Collection**: Only requests what's actually needed
- **Spec Organization**: Always in `/ai_framework/specs/` - never scattered

### Framework Benefits
- **Consistency**: Same quality regardless of AI model
- **Predictability**: Know exactly what will happen
- **Recoverability**: Never lose work or context
- **Traceability**: Every decision tracks to requirements
- **Quality**: Multi-stage validation ensures excellence
- **Efficiency**: No repeated work or lost progress

## Customization & Extension

### Project-Specific Rules
Add your own rules in `/ai_framework/PROJECT_DIRECTIVES.md`:
```markdown
# Project-Specific Directives

## Code Standards
- Use TypeScript with strict mode
- Follow team's ESLint configuration
- All components must have tests

## Custom Workflow
- Require security review for auth changes
- Deploy to staging before production
```

### Adding Custom Agents
Define new agents based on your needs:
```python
# In AI_CONTEXT.md agent section
Agent: SecurityExpert
Activation: Security-critical story
Responsibilities:
- Threat modeling
- Vulnerability assessment  
- Security pattern implementation
Authority:
- ✅ Review security implications
- ✅ Suggest security improvements
- ❌ Modify business logic
```

### Extending State Management
State files are JSON - add custom fields:
```json
// project_progress.json
{
  "custom_metrics": {
    "code_coverage": 0.85,
    "performance_score": 98,
    "tech_debt_items": 12
  },
  "team_assignments": {
    "STORY-042": "backend_team",
    "STORY-043": "frontend_team"
  }
}
```

## Multi-Agent Parallel Execution

### Activation
The framework automatically detects opportunities for parallel execution when:
- User says "in parallel", "simultaneously", "at the same time"
- Multiple independent tasks are identified
- User lists multiple deliverables
- Different PRD sections can be completed independently

### Usage Examples

#### Parallel PRD Development
```bash
User: "Complete the technical requirements, business model, and compliance sections in parallel"

# Framework automatically:
1. Launches 3 analyst agents
2. Each works on their section independently
3. Results integrate automatically
4. CASCADE validation maintained
```

#### Multi-Asset Development
```bash
User: "Set up the API, frontend, and documentation simultaneously"

# Framework response:
/agent architect "design API structure"
/agent dev "scaffold frontend application"
/agent pm "create documentation structure"

# Monitor progress
/agent  # Shows all active agents and their progress
```

#### Wave-Based Execution (>5 tasks)
```bash
User: "Generate all 12 feature specifications in parallel"

# Framework handles in waves:
- Wave 1: 5 architect agents
- Wave 2: 5 architect agents  
- Wave 3: 2 architect agents
- Automatic coordination between waves
```

### Recovery After Interruption
```bash
# After crash/restart
/state

## 🔄 Recovering Parallel Execution
### Active Parallel Agents (3)
1. analyst - 67% complete - Resuming...
2. architect - 45% complete - Resuming...
3. dev - 12% complete - Restarting...
```

### Best Practices
- **Stay as Primary**: Don't switch agents when orchestrating
- **Clear Tasks**: Provide specific, bounded work items
- **Monitor Progress**: Check `/agent` status regularly
- **Trust Recovery**: State tracking enables full resumption
- **Clean When Done**: Approve completion to clear parallel state

## Multi-Model Support

### Getting Any AI Model Started

#### First Message to Any Model
```
"Read AI_CONTEXT.md to understand the Hegemon framework, 
then @hege status to check current state"
```

The AI will:
1. Load framework directives from AI_CONTEXT.md
2. Check project state in `/ai_framework/state/`
3. Identify active agent and mode
4. Resume from last checkpoint

### Model-Specific Setup

#### Claude (via Claude Code CLI)
- CLAUDE.md auto-loads
- Slash commands available immediately
- Use `/prime` for full initialization

#### GPT-4 (via API or ChatGPT)
- Paste: "Follow AI_CONTEXT.md as primary directive"
- Use @hege commands for control
- State persists identically

#### Gemini/Other Models
- Start with: "Load AI_CONTEXT.md as system prompt"
- All @hege commands work
- Same state format

### Switching Between Models Mid-Project
```
# Leaving Claude for GPT:
Claude: [AGENT:dev|MODE:task|TASK:STORY-042]
        Saved state at 67% completion of auth module

# Starting with GPT:
User: "Read AI_CONTEXT.md and @hege resume"
GPT:  [AGENT:dev|MODE:task|TASK:STORY-042]
      Resuming authentication module at 67%...
```

## Troubleshooting

### Common Issues

#### "AI isn't following the framework"
- Ensure AI read AI_CONTEXT.md first
- Check for agent header in responses
- Use `@hege validate` to verify setup

#### "Lost context after interruption"  
- Use `@hege resume` or `/state`
- Check `/ai_framework/state/checkpoint.json`
- State auto-saves every action

#### "Can't modify code"
- Check current mode with `@hege status`
- Verify you have an approved task
- Switch modes if needed: `@hege mode task`

#### "Specs created in wrong location"
- MUST be in `/ai_framework/specs/`
- Never in `/ai_framework/` root
- Framework enforces this strictly

### Recovery Commands
```bash
# Check everything
@hege validate

# Reset to known state  
@hege reset

# Force state save
@hege save
/save

# See all agents
/agent
@hege status
```

## Quick Reference Card

### Workflow Phases
```
1. PRD Discovery    → Analyst Agent    → Planning Mode
2. Spec Generation  → Architect Agent  → Planning Mode  
3. Story Creation   → PM Agent         → Planning Mode
4. Implementation   → Dev Agent        → Task Mode
5. Testing          → QA Agent         → Task Mode
```

### Mode Rules
| Mode | Can Do | Cannot Do |
|------|--------|----------|
| PLANNING | Create specs, design architecture | Modify code |
| TASK | Implement approved stories | Create new features |
| DIRECT | Override with acknowledgment | Skip approval |

### Essential Files
| File | Purpose |
|------|------|
| `/AI_CONTEXT.md` | Complete framework rules |
| `/ai_framework/PRD.md` | Project requirements |
| `/ai_framework/specs/` | All specifications |
| `/ai_framework/tasks/` | Stories and backlog |
| `/ai_framework/state/` | Automatic saves |

## Recent Updates

### Conditional Context Loading System (v3.1)
The framework now uses intelligent context loading to optimize token usage by ~50%:

#### How It Works
- **Core Context**: AI_CONTEXT.md (~3,200 tokens) always loads with essential directives
- **Conditional Contexts**: Additional contexts load only when relevant to the current interaction
- **Dynamic Detection**: Framework analyzes user messages and state to determine what's needed

#### Context Loading Triggers
| Context File | Loads When | Contains |
|-------------|------------|----------|
| `agent_activation.md` | `/agent`, `/mode`, parallel work detected | Full agent system, parallel execution |
| `task_protocol.md` | Task IDs mentioned, implementation work | Task workflow, implementation rules |
| `project_init.md` | `/init` command | Project initialization workflow |
| `example_resources.md` | Examples/mockups discussed | Resource handling guidelines |
| `cascade_protection.md` | Working on tasks | CASCADE validation system |
| `recovery_protocols.md` | State files exist | Session recovery procedures |
| `expert_review.md` | Task completion, `/expert` | Expert review system |
| `prd_workflow.md` | PRD work needed | PRD development process |
| `working_hegemon_dev_context.md` | Framework development only | Hegemon development rules |

#### Token Optimization Results
- **Before**: ~6,400 tokens (single monolithic file)
- **After**: ~3,200 tokens base + 500-1,500 conditional
- **Typical Load**: 3,700-4,700 tokens (42-27% reduction)
- **Best Case**: 3,200 tokens (50% reduction)

#### Proactive Detection
The framework proactively loads contexts when it detects opportunities:
- Multiple independent tasks → Loads agent system for parallel execution
- Complex implementation → Loads expert review for quality checks
- State files present → Loads recovery protocols automatically

### Context Optimization (Previous)
- **20% reduction** in context load on `/prime` command
- Eliminated duplication between AI_CONTEXT.md and other files
- Moved detailed rules to referenced files (AI_STATE_RULES.md)
- Preserved all critical functionality while reducing token usage

### Framework Improvements
- Enhanced state management with atomic writes
- Improved agent switching and mode enforcement
- Better recovery from interruptions
- Clearer separation of concerns in directory structure
- Conditional context loading for optimal token usage

## License

MIT License - Use freely for your projects

---

**Ready to build something amazing?** 
- Claude Code: Type `/prime` to begin
- Any AI Model: Type `@hege reset` to begin