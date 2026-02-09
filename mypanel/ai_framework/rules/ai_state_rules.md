# State Management - Resumption Only

## Critical Understanding

**State is ONLY for crash/interruption recovery of in-progress work.**

### What State IS:
- Emergency recovery from interruptions
- Context retention between primary and subagent collaborative workflows
- Session crashes
- Context key detail protection during context clear/compression actions by the model or IDE
- API timeouts
- Model swaps

## Key Principle

**This directory should be EMPTY after completion of a task and all active side-work if before commencement of the next task.**

Upon completion of a task:
1. **ALWAYS ASK USER** to confirm if task is complete
2. Update the checkbox in `/ai_framework/tasks/task-list.md` from `[ ]` to `[x]`
3. **DELETE ALL STATE FILES** - they are for resumption only, not records
4. State directory should be **EMPTY** between tasks

State files are created when work begins on a new task. They are deleted when the user confirms task completion to avoid resuming completed work after IDE restart or context rebuild.

## State Files (For Tracking Active Work on Tasks or Side-Work[side-work:non-task work but User directed])

### session_state.json
**Exists**: ONLY when actively working on a task or side-work
**Purpose**: Resume interrupted work
**Contents**:
```json
{
  "task_id": "T042",
  "description": "Implement auth service",
  "started": "2024-01-15T10:30:00Z",
  "progress": "Writing JWT refresh logic",
  "files_modified": ["auth.service.ts"],
  "next_step": "Add refresh token validation",
  "working_directory": "/src/services"
}
```
**Lifecycle**: Created on task/workflow start → Deleted on task/workflow complete
**task_id**: is actual ID if task or if sidework tracking a short name of nature of side-work objective

### interview_progress.json (NEW)
**Exists**: ONLY during active PRD/Spec interview sessions
**Purpose**: Resume interrupted interview workflows
**Contents**:
```json
{
  "interview_type": "prd|spec|feature_scoping",
  "prd_file": "PRD.md",
  "current_stage": "target_audience",
  "completed_stages": ["project_discovery", "purpose_mission"],
  "answers_collected": {
    "project_type": "new_greenfield",
    "complexity_level": ["multiple_systems", "integrations"],
    "primary_deliverables": ["web_portal", "api_service"]
  },
  "assets_identified": [
    {"name": "WebPortal", "file": "PRD_WebPortal.md", "status": "pending"}
  ],
  "next_stage": "features_discovery",
  "started": "2024-01-15T10:00:00Z",
  "last_updated": "2024-01-15T10:30:00Z"
}
```
**Lifecycle**: Created when interview starts → Updated after each stage → Deleted when PRD approved or interview complete
**interview_type**: Type of interview (PRD development, spec generation, or feature scoping) 

### checkpoint.json
**Exists**: ONLY during complex multi-step operations
**Purpose**: Detailed workflow resumption instructions with context regen and objective clarifications.
**Contents**:
```json
{
  "recovery_instructions": "Continue implementing refresh token at line 45",
  "open_files": ["auth.service.ts", "auth.test.ts"],
  "pending_decisions": ["Token expiry duration"],
  "last_command": "npm test",
  "last_output": "3 tests failing"
}
```
**Lifecycle**: Created during complex work → Deleted as part of state clearing when approved by user.

### agent_handoff.json
**Exists**: ONLY during active agent coordination
**Purpose**: Resume multi-agent workflows
**Contents**:
```json
{
  "from_agent": "architect",
  "to_agent": "dev",
  "handoff_time": "2024-01-15T11:00:00Z",
  "task": "Implement the API design from spec",
  "context": {
    "spec_location": "/ai_project/specs/FEAT-001/",
    "critical_notes": ["Rate limiting required"]
  }
}
```
**Lifecycle**: Created during handoff → Deleted as part of state clearing when approved by user.

## Proper Usage

### Starting Work
```python
# Task begins - create minimal state
create_session_state({
  "task_id": "T055",
  "started": now(),
  "description": "Add user profile endpoint"
})
```

### During Work
```python
# Update only if interrupted
if (interrupted || context_limit_approaching):
  update_checkpoint({
    "progress": "Created model, writing controller",
    "user_notes": "Save any specific details that were found in recent prompts from user for model reference.",
    "next_step": "Add validation middleware"
  })
```

### Completing Work

**IMPORTANT**: Task completion is tracked ONLY in `/ai_framework/tasks/task-list.md`

When the framework believes a task is complete:
1. **ASK THE USER** for confirmation:
   - "Task T055 appears complete. Status?"
   - Options: [Mark Complete] [More Work Needed] [Pause Task]

2. **On "Mark Complete"**:
   ```python
   # Update the task list markdown file
   update_task_in_list("T055", "[x]")  # Check the box
   # IMMEDIATELY clear all state files
   delete_session_state()
   delete_checkpoint()
   # State directory should be EMPTY
   ```

3. **On "More Work Needed"**:
   ```python
   # Continue with current task
   # Keep state files active
   ```

4. **On "Pause Task"**:
   ```python
   # Save current progress to state
   # But do NOT mark task complete
   # Can resume later
   ```

## Recovery Flow

### Check on Session Start
```python
if exists("session_state.json"):
  state = load_state()
  if state.age > 24_hours:
    # Too old, probably not relevant
    delete_state()
    print("No active work to resume")
  else:
    print(f"Resume task {state.task_id}? (y/n)")
else:
  print("No active work. See /tasks for next items")

# Check for parallel agent recovery
if exists("agent_processes.json"):
  agent_state = load_state("agent_processes.json")
  if agent_state["parallel_execution_active"]:
    active_count = len(agent_state["active_parallel_agents"])
    print(f"Recovering {active_count} parallel agents...")
    for agent in agent_state["active_parallel_agents"]:
      if agent["recovery_checkpoint"]["can_resume"]:
        print(f"  - {agent['agent']}: Resume {agent['task']} at {agent['recovery_checkpoint']['progress_percentage']}%")
      else:
        print(f"  - {agent['agent']}: Restart {agent['task']}")
```

### Parallel Agent State Management
```python
# When launching parallel agents
def track_parallel_agent(agent_name, task, output_location):
  agent_state = load_or_create("agent_processes.json")
  agent_state["parallel_execution_active"] = True
  agent_state["active_parallel_agents"].append({
    "agent": agent_name,
    "task": task,
    "status": "working",
    "started": now(),
    "output_location": output_location,
    "recovery_checkpoint": {
      "last_action": "starting",
      "progress_percentage": 0,
      "can_resume": False
    }
  })
  save_state(agent_state)

# When agent makes progress
def update_agent_checkpoint(agent_name, progress, last_action):
  agent_state = load_state("agent_processes.json")
  for agent in agent_state["active_parallel_agents"]:
    if agent["agent"] == agent_name:
      agent["recovery_checkpoint"] = {
        "last_action": last_action,
        "progress_percentage": progress,
        "can_resume": True
      }
  save_state(agent_state)

# When parallel execution completes
def cleanup_parallel_agents():
  if user_confirms("All parallel tasks complete and approved?"):
    agent_state = load_state("agent_processes.json")
    agent_state["parallel_execution_active"] = False
    agent_state["active_parallel_agents"] = []
    agent_state["completed_parallel_tasks"] = []
    save_state(agent_state)
```

### agent_processes.json Structure
```json
{
  "parallel_execution_active": false,
  "orchestrator": "primary",
  "active_parallel_agents": [],
  "completed_parallel_tasks": [],
  "failed_tasks_for_retry": [],
  "agent_utilization": {
    "current": 0,
    "maximum": 5,
    "available": 5
  },
  "wave_execution": {
    "current_wave": 0,
    "total_waves": 0,
    "tasks_per_wave": 0
  },
  "last_cleanup": null,
  "recovery_available": false
}
```

## Commands

### /state Command Behavior
- If state files exist: "Resuming T055: Add user profile endpoint"
- If no state files: "No active work. See /tasks for next items"

### /tasks Command Behavior
- Shows overall progress: "15 of 45 tasks complete"
- Shows next tasks: "Next: T056, T057, T058"
- This is your roadmap, NOT state

## State Lifecycle

### When to Create State
```python
def should_save_state():
    return any([
        task_in_progress(),
        awaiting_user_input(), 
        long_running_operation(),
        context_near_limit()
    ])
```

### Recovery Process
```python
def on_session_start():
    if exists("session_state.json"):
        state = load_state()
        if state.timestamp < 24_hours_ago:
            clear_state()  # Too old to be relevant
        else:
            resume_from_state()
```

### Cleanup Rules
```python
def on_task_complete():
    # Task done, no need to resume it
    save_checkpoint("task_completed")
    if user_approves("Clear state for completed task?"):
        clear_state()
```

## Clean State Directory

A properly functioning state directory looks like this between task or user-objective targeted workflows:

```
/ai_project/state/
├── README.md
└── (empty - no other files)
```

During active work we'll have:
```
/ai_project/state/
├── README.md
├── session_state.json (current task and any side-workflow only)
└── checkpoint.json (if complex operation)
```

## Migration Note

If you have existing state files with historical data:
1. Move task history to `/ai_project/tasks/completed/`
2. Move project progress to `/ai_project/tasks/metrics.json`
3. Delete all other files
4. Keep this directory empty unless actively working

Remember: **State = "What was I doing?" (resumption only)**
Not: "What have I done?" (that's what /tasks is for)