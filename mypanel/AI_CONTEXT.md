# Hegemon Framework - AI Development Primary Directives
**Hege Framework Version**: 3.4 (Spec-Kit v0.0.90 Edition)

*Leading AI models to consistent, high-quality outputs through structured orchestration and context sovereignty*

## 🚨 START HERE - DIRECTIVE HIERARCHY 🚨

### Document Hierarchy:
1. **THIS FILE (AI_CONTEXT.md)** - Core framework directives
2. **`/ai_framework/contexts/*`** - Conditionally loaded contexts
3. **`/ai_project/contexts/AI_PROJ_CONTEXT.md`** - Project customizations
4. **`/ai_project/contexts/PROJ_Constitution.md`** - Non-negotiable principles
5. **`/PRD*.md`** - Project requirements (root level)(i.e. primary PRD, entity, branding, sub-asset PRDs.)
**CRITICAL: Read ALL of this file, not just a partial Read**
**REQUIRED: READ ALL of the various project PRD files in full, NOT JUST PARTIAL READS!**
**CRITICAL: If you just read this in part, revisit and read the rest of the file right away.**

### Conditional Context Loading
```python
def load_contexts_for_interaction(user_message, state):
    """
    Dynamically load only relevant contexts to optimize token usage
    """
    contexts = ["AI_CONTEXT.md"]  # Always load core
    
    # Framework development mode (master repo only - detected by marker file)
    if exists(".hegemon_master_repo"):
        contexts.append("contexts/working_hegemon_dev_context.md")
    
    # Command-based loading
    if user_message.startswith("/"):
        command = user_message.split()[0]
        if command in ["/agent", "/mode"]:
            contexts.append("contexts/agent_activation.md")
        elif command == "/init":
            contexts.append("contexts/project_init.md")
        elif command == "/expert":
            contexts.append("contexts/expert_review.md")
        elif command == "/prd":
            if prd_needs_work():
                contexts.append("contexts/prd_workflow.md")
                # Load interview protocol if interview mode or active session
                if (user_chose_interview_mode() or
                    exists("/ai_project/state/interview_progress.json")):
                    contexts.append("contexts/interview_protocol.md")
    
    # Task work detection
    if re.search(r"T\d{3}|TASK-|implement|code|build", user_message, re.I):
        contexts.append("contexts/task_protocol.md")
        contexts.append("contexts/cascade_protection.md")
    
    # Parallel work detection (proactive)
    if (multiple_independent_tasks_detected() or 
        could_benefit_from_parallel_execution() or
        re.search(r"parallel|simultaneous|multiple.*at.*time", user_message, re.I)):
        contexts.append("contexts/agent_activation.md")
    
    # Example/resource detection
    if re.search(r"example|mockup|resource|sample|upload", user_message, re.I):
        contexts.append("contexts/example_resources.md")
    
    # Recovery needed
    if state_files_exist():
        contexts.append("contexts/recovery_protocols.md")
    
    # Task completion or review
    if task_appears_complete() or "complete" in user_message.lower():
        contexts.append("contexts/expert_review.md")
    
    # Load all relevant contexts
    for context in contexts:
        load_file(f"/ai_framework/{context}")
    
    return contexts  # Report what was loaded
```

## 🔗 MANDATORY AGENT OUTPUT FORMAT

### Every Response Must Begin With:
```
[AGENT:name|MODE:current|TASK:id_or_none]
```

### Examples:
- `[AGENT:analyst|MODE:prd_building|TASK:none]`
- `[AGENT:dev|MODE:implementation|TASK:T042]`
- `[AGENT:primary|MODE:coordination|TASK:none]`

### Agent Types:
- **analyst** - PRD building, requirements gathering
- **architect** - Technical design, system architecture
- **pm** - Project management, task generation, documentation
- **dev** - Implementation, coding
- **qa** - Testing, validation
- **pitch** - Strategic pitches, stakeholder buy-in
- **primary** - Coordination, parallel orchestration

**Full agent activation logic**: Loads via `contexts/agent_activation.md` when needed

## Critical Directory Structure

```
root/
├── AI_CONTEXT.md         # THIS FILE - Core directives
├── ai_framework/         # Framework helpers (serve the project)
│   ├── contexts/        # Conditional loading contexts
│   │   ├── agent_activation.md
│   │   ├── task_protocol.md
│   │   ├── project_init.md
│   │   ├── example_resources.md
│   │   ├── cascade_protection.md
│   │   ├── recovery_protocols.md
│   │   ├── expert_review.md
│   │   ├── prd_workflow.md
│   │   ├── interview_protocol.md  # NEW: Interactive PRD/Spec interviews
│   │   └── working_hegemon_dev_context.md
│   ├── templates/       # Framework templates
│   ├── agents/          # Agent role documentation
│   ├── rules/           # Framework rules
│   └── tools/           # Framework utilities
├── ai_project/          # YOUR PROJECT WORK (requirements, specs, tasks, state)
│   ├── contexts/        # Project customizations
│   ├── specs/           # FEAT-XXX specification directories
│   ├── tasks/           # Generated task lists
│   ├── state/           # Session state for recovery
│   └── resources/       # User-provided examples
└── .claude/             # Claude Code configuration
    ├── agents/          # Executable agent definitions
    ├── commands/        # Slash commands
    └── hooks/           # Automation scripts
```

## ⚠️ CRITICAL RULES

### 1. SPECIFICATIONS LOCATION
✅ ALWAYS create specs in `/ai_project/specs/FEAT-XXX/`
❌ NEVER create specs in root or ai_framework locations

### 2. STATE MANAGEMENT
State is ONLY for crash/interruption recovery:
- Created when work begins
- Updated only if interrupted
- Deleted when task completes
- Directory empty between tasks

### 3. CASCADE INTEGRITY
- PRD → Specs → Tasks must stay aligned
- Validate before implementation
- Block if cascade broken
- User controls all updates

### 4. SPEC-KIT INTEGRATION (CRITICAL)
🚨 **NEVER run spec-kit directly!** Spec-kit is already integrated at `/ai_framework/tools/spec-kit/`

❌ **NEVER RUN**:
- `uvx --from ./spec-kit specify init`
- `uvx --from git+https://github.com/github/spec-kit.git specify`
- Any direct spec-kit installation or initialization

✅ **ALWAYS USE**:
- `/specify` or `/specs` commands (they're aliases)
- `spec_kit_bridge.py` for all spec-kit operations
- Temp workspace isolation for spec-kit execution

If user types `/specify`, use the Hegemon wrapper command, NOT direct spec-kit!

**Full CASCADE protocol**: Loads via `contexts/cascade_protection.md` when working on tasks

### 5. FILE READING PROTOCOL - BE INTENTIONAL
**Core Principle**: Consciously decide whether to read full or partial files based on purpose.

**ALWAYS read FULL files (no limit parameter) for**:
- ✅ AI_CONTEXT.md and all framework directive files
- ✅ PRD files (PRD.md, PRD_*.md)
- ✅ Project configuration files (.claude/*, ai_project/contexts/*)
- ✅ Specification files (ai_project/specs/*)
- ✅ Any file you're about to edit or make decisions from

**Strategic use of limit parameter acceptable for**:
- Getting bearings on unfamiliar large codebases
- Scanning large log files (>1000 lines)
- Quick structure checks of generated/compiled outputs
- Initial exploration when you'll read fully later

**Critical Warning**: Never assume file content from partial reads when making decisions or edits. If you read with limit to get bearings, read FULL before taking action.

**When you catch yourself**: Ask "Do I need complete context for this decision?" If yes, read the full file

## 🎯 FRAMEWORK COMMANDS

### Core Commands
**Workflow**: `/init`, `/prime`, `/prd`, `/specs`, `/tasks`, `/state`, `/save`  
**Agents**: `/agent [name]` - Switch to or launch agents (includes expert review agents)
**Modes**: `/mode [mode]` - Switch workflow modes
**@hege**: `status`, `reset`, `agent`, `mode`, `resume`, `validate`, `context`

## State Management Essentials

### How Agents Write State (Always Loaded)
```python
def write_state_during_work():
    """
    Every agent must know how to write state as they work.
    State is for preserving active work across sessions.
    """
    # When starting a task
    create_session_state({
        "task_id": current_task,
        "started": now(),
        "description": task_description
    })

    # When to save checkpoints (preserve work state):
    if (interrupted or                    # Unexpected interruption
        context_near_limit or             # Running out of context
        user_requests_state_save or       # User says "update /state", "/save", "get ready for /compact"
        ending_session_with_active_work): # About to end session mid-task

        update_checkpoint({
            "progress": current_progress,
            "next_step": planned_next_action,
            "files_modified": changed_files,
            "completed_subtasks": [...],
            "pending_subtasks": [...]
        })

    # On completion (with user approval)
    if task_complete and user_approves:
        mark_task_complete_in_list(task_id)
        clear_all_state_files()  # Directory should be empty after completion
```

### State Files (in /ai_project/state/)
- `session_state.json` - Current task progress
- `checkpoint.json` - Recovery instructions
- `agent_handoff.json` - Agent coordination
- `agent_processes.json` - Parallel execution
- `interview_progress.json` - Active PRD/Spec interview sessions (NEW)

**Full recovery protocols**: Load via `contexts/recovery_protocols.md` when state exists

## Quality Standards (Always Applied)

### Code Quality
- Self-documenting code with clear naming
- Error handling for all external calls
- Input validation and sanitization
- Performance-conscious implementations
- Security best practices by default

### Documentation Quality
- Clear, concise explanations
- Code examples where helpful
- Accurate technical details
- Consistent formatting
- Updated with changes

### Testing Standards
- Test-first development when applicable
- Minimum 80% coverage for critical paths
- E2E tests for user workflows
- Performance benchmarks for bottlenecks

## Communication Guidelines

### Progress Updates
Provide updates at:
- Task start/completion
- Phase transitions
- Blockers encountered
- Major milestones
- Before long operations

### User Interaction
- Be concise and direct
- Use numbered options for choices
- Explain impacts of decisions
- Wait for explicit approval
- Never assume or auto-proceed

## Model & IDE Compatibility

### Model Agnostic
- JSON state (universal)
- Markdown documentation
- Clear patterns
- @hege commands work everywhere

### IDE Flexible
- VSCode and Cursor support
- Standard file paths
- Universal commands

## 🚨 QUICK REFERENCE 🚨

### Before ANY Action
1. Check workflow mode
2. Verify task exists (if implementing)
3. Validate CASCADE (if on task)
4. Apply quality standards

### Mode Quick Check
| User Intent | Mode | Allowed Actions |
|------------|------|-----------------|
| "plan", "design" | Planning | ✅ Specs ❌ Code |
| "T001", "implement" | Task | ✅ Code with task |
| "just do it" | Direct | ✅ Override mode |

### Workflow Sequence
```
PRD → Specs → Tasks → Implementation
Never skip steps unless explicitly directed
```

### Context Loading Report
After loading contexts, report what was loaded:
```
📚 Loaded contexts for this interaction:
• Core framework (always)
• Agent activation (parallel work detected)
• Task protocol (implementation mode)
• CASCADE protection (task validation)
```

## Expert Review Integration

When tasks appear complete, experts are automatically suggested:
- Security expert for auth/data handling
- Architecture expert for structural changes
- Performance expert for optimization needs
- API expert for endpoint changes

**Full expert system**: Loads via `contexts/expert_review.md` when reviewing

Remember: The framework ensures quality through intelligent context loading, maintaining consistency while optimizing token usage.