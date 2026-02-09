# Task-Based Implementation Protocol
**CONDITIONAL LOAD**: Loaded when working on tasks, implementation, or coding activities

## Before ANY Code Changes

### Mandatory Validation
```python
def validate_implementation(action):
    # MANDATORY CHECKS
    current_mode = get_current_mode()
    
    if current_mode == "PLANNING_MODE":
        print("❌ Cannot modify code in Planning Mode")
        print("💡 Switch to Task Mode or get user override")
        return False
    
    if current_mode == "TASK_MODE":
        task = find_matching_task(action)
        if not task:
            print("❌ No approved task for this action")
            print("📋 Check task list or request task creation")
            return False
        
        # CASCADE VALIDATION - CRITICAL POLICY
        if not validate_cascade_integrity(task):
            print("❌ CASCADE VIOLATION DETECTED")
            print("Task is out of sync with specs/PRD")
            print("SUGGESTED commands (user must run):")
            print("  /tasks update - Review changes first")
            print("  /specs review - Check spec alignment")
            # Require explicit user action and approval
            return False  # BLOCK - no auto-fixes
        
        if not dependencies_met(task):
            print("❌ Task dependencies not met")
            return False
    
    return True
```

## Task Implementation Workflow

### 1. Task Selection
- Verify task exists in `/ai_framework/tasks/task-list.md`
- Check task status (must be pending `[ ]`)
- Validate dependencies are complete

### 2. Pre-Implementation Checks
- Confirm CASCADE integrity (PRD → Spec → Task alignment)
- Verify test-first approach if applicable
- Check for blocking dependencies
- Validate working directory

### 3. During Implementation
- Update session state with progress
- Track files modified
- Follow quality standards (loaded in core)
- Create checkpoints for complex work

### 4. Task Completion Flow
```python
def handle_task_completion(task_id):
    # Check if work appears complete
    if implementation_complete(task_id):
        print(f"Task {task_id} appears complete.")
        
        # Get user confirmation
        response = prompt_user([
            "1. Mark Complete",
            "2. More Work Needed", 
            "3. Pause Task"
        ])
        
        if response == "Mark Complete":
            # Update checkbox in task-list.md
            mark_task_complete_in_list(task_id)
            # Clear state files
            clear_session_state()
            print(f"✅ Task {task_id} marked complete")
            
            # Suggest expert review if needed
            if needs_expert_review(task_id):
                load_context("expert_review.md")
                suggest_expert_review(task_id)
        
        elif response == "More Work Needed":
            # Continue with current task
            maintain_session_state()
        
        elif response == "Pause Task":
            # Save progress for later resumption
            save_checkpoint()
```

## Task Tracking Format

Tasks in `/ai_framework/tasks/task-list.md` use this format:
```markdown
## Phase 3.2: Implementation
- [ ] T001 Create user authentication service
- [x] T002 Set up database connection
- [ ] T003 [P] Implement user profile endpoints
```

- `[ ]` = Pending task
- `[x]` = Completed task
- `[P]` = Can be done in parallel

## When This Context Loads
- User mentions task IDs (T001, TASK-XXX, STORY-XXX)
- Implementation or coding keywords detected
- Commands: `/tasks`
- Working in TASK_MODE
- Keywords: "implement", "code", "develop", "build"