# Recovery Protocols
**CONDITIONAL LOAD**: Loaded when state files exist, after crashes, or when resuming work

## Session Recovery

### Automatic Recovery Check
```python
def check_for_recovery_on_start():
    """
    Run this check at the beginning of every session
    """
    if exists("/ai_framework/state/session_state.json"):
        state = load_state("session_state.json")
        
        # Check if state is recent enough to be relevant
        if state.age < 24_hours:
            print("📎 Found active work to resume:")
            print(f"  Task: {state.task_id} - {state.description}")
            print(f"  Progress: {state.progress}")
            print(f"  Next step: {state.next_step}")
            print("")
            print("Resume this work? (Y/n)")
            
            if user_confirms():
                recover_from_state(state)
            else:
                clear_state_with_permission()
        else:
            # State too old, probably not relevant
            print("Found old state files (>24 hours)")
            clear_state_with_permission()
    else:
        # No active work
        print("No active work found. See /tasks for next items.")
```

### Full Context Recovery
```python
def recover_context():
    """
    Restore complete working context from state
    """
    state = load_all_states()
    
    if state.has_checkpoint:
        print(f"🔄 Resuming: {state.project_name}")
        print(f"  Mode: {state.current_workflow_mode}")
        print(f"  Phase: {state.current_phase}")
        print(f"  Last action: {state.last_action}")
        print(f"  Files involved: {state.files_modified}")
        
        # Restore working environment
        restore_working_directory(state.working_directory)
        reopen_files(state.open_files)
        
        # Continue from exact stopping point
        continue_from_checkpoint(state.recovery_instructions)
```

## Recovery Scenarios

### After Context Clear/Compression
When user or system clears context:
1. Load state immediately on next interaction
2. Show: "Resuming [project] in [mode] mode"
3. Continue exact last action
4. No repeated work
5. Maintain continuity

### After IDE Crash
```python
def recover_from_crash():
    # Check all state files
    states = {
        "session": load_if_exists("session_state.json"),
        "checkpoint": load_if_exists("checkpoint.json"),
        "handoff": load_if_exists("agent_handoff.json"),
        "parallel": load_if_exists("agent_processes.json")
    }
    
    # Prioritize recovery
    if states["parallel"] and states["parallel"]["active"]:
        recover_parallel_agents(states["parallel"])
    elif states["checkpoint"]:
        recover_from_checkpoint(states["checkpoint"])
    elif states["session"]:
        recover_session(states["session"])
```

### After Model Swap
When switching between models (Claude → GPT → Claude):
```python
def recover_after_model_swap():
    # State persists in JSON (model-agnostic)
    state = load_state()
    
    # Re-establish context
    print("Loading framework context...")
    load_file("AI_CONTEXT.md")
    
    # Show where we were
    print(f"Previous model was working on: {state.task_id}")
    print(f"Continue from: {state.next_step}")
    
    # Restore agent if needed
    if state.active_agent:
        activate_agent(state.active_agent)
```

### Multi-Agent Recovery
```python
def recover_parallel_agents():
    """
    Recover multiple agents after interruption
    """
    agent_state = load_state("agent_processes.json")
    
    if agent_state["parallel_execution_active"]:
        active = agent_state["active_parallel_agents"]
        print(f"🔄 Recovering {len(active)} parallel agents:")
        
        for agent in active:
            if agent["recovery_checkpoint"]["can_resume"]:
                print(f"  ✅ {agent['agent']}: Resume at {agent['recovery_checkpoint']['progress_percentage']}%")
                resume_agent_work(agent)
            else:
                print(f"  🔁 {agent['agent']}: Restart required")
                restart_agent_work(agent)
```

## State File Locations

### Primary State Files
```
/ai_framework/state/
├── session_state.json      # Current task/work
├── checkpoint.json          # Detailed recovery point
├── agent_handoff.json       # Agent coordination
└── agent_processes.json     # Parallel execution
```

### What Gets Recovered
- Current task ID and description
- Progress within task
- Files being modified
- Open editor tabs
- Working directory
- Next planned action
- Agent assignments
- Parallel work distribution

## Recovery Best Practices

### Creating Recovery Points
```python
def create_recovery_point(reason):
    checkpoint = {
        "timestamp": now(),
        "reason": reason,
        "recovery_instructions": get_next_steps(),
        "open_files": get_open_files(),
        "pending_decisions": get_pending_decisions(),
        "context_summary": summarize_current_work()
    }
    save_checkpoint(checkpoint)
```

### When to Create Checkpoints
- Before long-running operations
- At natural pause points
- When switching between major sections
- Before user decisions needed
- When context is near limit

## Cross-Tool Compatibility

### Model Agnostic Design
- JSON state files work with any model
- Markdown documentation universally readable
- Clear prompt patterns, no model-specific syntax
- @hege commands work across all models

### IDE Flexibility
```yaml
VSCode → Cursor:
  - Same file structure
  - State remains valid
  - Commands work identically
  
Cursor → VSCode:
  - No changes needed
  - Continue from checkpoint
  - Full compatibility
```

## When This Context Loads
- Session start with existing state files
- After crashes or interruptions
- Command: `/prime` with active state
- Context clear/compression recovery
- Model or IDE switches
- Keywords: "resume", "recover", "continue", "checkpoint"