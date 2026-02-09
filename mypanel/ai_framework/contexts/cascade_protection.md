# CASCADE Protection Protocol
**CONDITIONAL LOAD**: Loaded during task implementation, spec validation, or when working on numbered tasks

## CASCADE Integrity System

### What is CASCADE?
CASCADE ensures alignment between:
- **PRD** (Product Requirements) → 
- **Specifications** (Technical Design) → 
- **Tasks** (Implementation Work)

When any upstream document changes, downstream work becomes stale and must be reviewed.

### Validation Process
```python
def validate_cascade_integrity(task_id):
    """
    Check if task is still aligned with its source spec
    and if spec is aligned with PRD
    """
    # Get task's spec hash from when it was generated
    task_spec_hash = get_task_metadata(task_id)["spec_hash"]
    
    # Get current spec hash
    current_spec_hash = calculate_hash(spec_file)
    
    # Get spec's PRD hash from when it was generated  
    spec_prd_hash = get_spec_metadata(spec_id)["prd_hash"]
    
    # Get current PRD hash
    current_prd_hash = calculate_hash(prd_file)
    
    # Check alignment
    if task_spec_hash != current_spec_hash:
        return CASCADE_BROKEN("task_stale")
    
    if spec_prd_hash != current_prd_hash:
        return CASCADE_BROKEN("spec_stale")
    
    return CASCADE_VALID
```

## When CASCADE Breaks

### Required Model Behavior
1. **DETECT** - Automatically check hashes before any implementation
2. **BLOCK** - Stop all work immediately
3. **ALERT** - Clearly inform user of the mismatch
4. **SUGGEST** - Provide specific commands to resolve
5. **WAIT** - Require explicit user decision

### Example Response
```python
# When cascade violation detected:
print("⚠️ CASCADE VIOLATION DETECTED")
print("")
print("Task T042 was generated from an older version of FEAT-001 spec")
print("The spec has been updated since this task was created")
print("")
print("Your options:")
print("1. Review changes: /specs diff FEAT-001")
print("2. Update tasks: /tasks update (shows changes before applying)")
print("3. Continue anyway: Type 'override' to proceed with caution")
print("")
print("What would you like to do?")

# Wait for user response
user_decision = wait_for_user_input()

# Only proceed based on explicit user instruction
if user_decision == "override":
    log_cascade_override(task_id, "user_override")
    proceed_with_caution()
elif user_decision == "update":
    show_task_updates_preview()
    # Still require confirmation before applying
else:
    remain_blocked()
```

## User Retains Control

### The Framework NEVER:
- Auto-regenerates tasks without showing changes
- Auto-updates specifications
- Auto-fixes misalignments
- Proceeds with stale data
- Makes assumptions about intended changes

### The Framework ALWAYS:
- Shows what changed
- Explains the impact
- Provides clear options
- Waits for explicit approval
- Logs override decisions

## CASCADE Hash Tracking

### In Specifications
```yaml
# At top of each spec file
_prd_hash: abc123  # Hash of PRD when spec was created
_spec_hash: def456  # Hash of this spec content
```

### In Tasks
```yaml
# In task metadata
_spec_hash: def456  # Hash of spec when task was created
_spec_file: /ai_framework/specs/FEAT-001/spec.md
```

### Hash Calculation
```python
def calculate_cascade_hash(content):
    # Remove hash lines before calculating
    clean_content = remove_hash_metadata(content)
    # Generate consistent hash
    return hashlib.sha256(clean_content.encode()).hexdigest()[:8]
```

## When This Context Loads
- Working on numbered tasks (T001, TASK-XXX)
- During implementation phase
- Spec or task validation
- Commands: `/tasks`, `/specs`
- CASCADE validation needed