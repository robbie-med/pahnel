# Multi-Agent Parallel Orchestration Rules
**CONDITIONAL LOAD**: This file loads when parallel execution is triggered

## Activation Conditions
This file loads when:
- User explicitly requests parallel work ("work on these in parallel", "simultaneously")
- Multiple independent tasks are identified
- User lists multiple deliverables that could be done concurrently
- AI suggests and user approves parallel execution

## Parallel Execution Framework

### Core Orchestration Rules
```python
def orchestrate_parallel_agents():
    """
    Primary agent orchestrates parallel execution
    """
    # Maximum concurrent agents
    MAX_PARALLEL_AGENTS = 5
    
    # Identify parallelizable work
    tasks = identify_independent_tasks()
    
    # Validate CASCADE integrity for each
    for task in tasks:
        if not validate_cascade_compliance(task):
            mark_as_sequential(task)
    
    # Deploy agents in waves if > 5 tasks
    if len(tasks) > MAX_PARALLEL_AGENTS:
        create_execution_waves(tasks, MAX_PARALLEL_AGENTS)
    
    # Launch agents and track in state
    launch_parallel_agents(tasks)
    update_agent_state_tracking()
```

### Parallel Agent Deployment

#### Using the /agent Command
```python
def deploy_specialist_agent(agent_name, task_description):
    """
    Deploy agent as autonomous subagent via Task tool
    """
    # Build comprehensive context for agent
    context = {
        "framework_state": load_state(),
        "prd_status": get_prd_status(),
        "available_specs": list_specs(),
        "cascade_hash": get_current_cascade_hash(),
        "task_details": task_description,
        "dependencies": identify_dependencies(task_description)
    }
    
    # Launch via /agent command
    execute_command(f"/agent {agent_name} {task_description}")
    
    # Track in state for recovery
    add_to_parallel_tracking(agent_name, task_description)
```

### Task Processing Patterns

#### Sequential Execution (Default)
```python
for task in tasks_by_priority:
    load_state()
    mark_in_progress(task)
    execute_task(task)
    save_output()
    mark_complete(task)
    save_state()
```

#### Parallel Batch Processing (When Triggered)
```python
def execute_parallel_batch():
    # Get parallelizable tasks
    batch = get_parallelizable_tasks(max=5)
    
    # Deploy agents for each task
    for task in batch:
        agent = determine_best_agent(task)
        deploy_specialist_agent(agent, task)
    
    # Monitor and collect results
    while agents_working():
        monitor_agent_progress()
        handle_agent_completions()
    
    # Validate all results
    verify_quality()
    update_cascade_hash()
    save_all_states()
```

#### Multi-Stage Review Process
```python
def multi_stage_review(deliverable):
    """
    Sequential quality gates after parallel creation
    """
    review_stages = [
        ("Initial Creation", "specialist_agent"),
        ("Architecture Review", "architect"),
        ("Standards Review", "analyst"),
        ("Security Review", "qa"),
        ("Production Ready", "primary")
    ]
    
    for stage_name, reviewing_agent in review_stages:
        result = execute_review(deliverable, reviewing_agent)
        if result.needs_revision:
            return_to_specialist(deliverable, result.feedback)
        save_review_checkpoint(stage_name, result)
```

### Agent Communication Protocol

#### Parallel Agent State Tracking
Save to `/ai_framework/state/agent_processes.json`:
```json
{
  "parallel_execution_active": true,
  "orchestrator": "primary",
  "active_parallel_agents": [
    {
      "agent": "analyst",
      "task": "complete PRD sections 3-5",
      "status": "working",
      "started": "2024-01-15T10:00:00Z",
      "expected_completion": "2024-01-15T10:30:00Z",
      "output_location": "/ai_framework/working/prd_sections_3-5.md",
      "cascade_validation": "pending",
      "recovery_checkpoint": {
        "last_action": "writing section 4",
        "progress_percentage": 67,
        "can_resume": true
      }
    },
    {
      "agent": "architect",
      "task": "design API structure",
      "status": "working",
      "started": "2024-01-15T10:00:00Z",
      "expected_completion": "2024-01-15T10:45:00Z",
      "output_location": "/ai_framework/specs/api_structure.md",
      "cascade_validation": "pending",
      "recovery_checkpoint": {
        "last_action": "defining endpoints",
        "progress_percentage": 45,
        "can_resume": true
      }
    }
  ],
  "completed_parallel_tasks": [],
  "failed_tasks_for_retry": [],
  "agent_utilization": {
    "current": 2,
    "maximum": 5,
    "available": 3
  },
  "wave_execution": {
    "current_wave": 1,
    "total_waves": 1,
    "tasks_per_wave": 2
  }
}
```

### Recovery and Resumption

#### On IDE Crash or Interruption
```python
def recover_parallel_execution():
    """
    Resume parallel agent work after interruption
    """
    state = load_state("/ai_framework/state/agent_processes.json")
    
    if state["parallel_execution_active"]:
        print("[AGENT:primary|MODE:recovery|TASK:parallel_resume]")
        print(f"Recovering {len(state['active_parallel_agents'])} parallel agents...")
        
        for agent_process in state["active_parallel_agents"]:
            if agent_process["status"] == "working":
                if agent_process["recovery_checkpoint"]["can_resume"]:
                    # Resume from checkpoint
                    resume_agent_task(
                        agent_process["agent"],
                        agent_process["task"],
                        agent_process["recovery_checkpoint"]
                    )
                else:
                    # Restart task
                    restart_agent_task(
                        agent_process["agent"],
                        agent_process["task"]
                    )
```

#### State Cleanup Protocol
```python
def cleanup_parallel_state():
    """
    Clean up after parallel execution completes
    """
    # Only clean up when user confirms completion
    if user_confirms("Are all parallel tasks complete and approved?"):
        state = load_state("/ai_framework/state/agent_processes.json")
        
        # Mark tasks complete in task-list.md
        for task_id in state["completed_parallel_tasks"]:
            mark_task_complete_in_list(task_id)
        
        # Reset parallel execution state
        state["parallel_execution_active"] = False
        state["active_parallel_agents"] = []
        state["completed_parallel_tasks"] = []
        state["agent_utilization"]["current"] = 0
        
        save_state(state)
        print("Parallel execution state cleaned up")
```

## Orchestration Scenarios

### Scenario 1: Multiple Independent PRD Sections
```
User: "Complete the technical requirements, business model, and compliance sections in parallel"

Primary Agent:
1. Identifies 3 independent PRD sections
2. Validates no dependencies between them
3. Deploys 3 analyst agents:
   - /agent analyst "complete technical requirements section"
   - /agent analyst "complete business model section"
   - /agent analyst "complete compliance section"
4. Monitors progress via /agent status
5. Collects and integrates results
6. Updates PRD and CASCADE hash
```

### Scenario 2: Multi-Asset Project Setup
```
User: "Set up the API, frontend, and documentation simultaneously"

Primary Agent:
1. Identifies 3 independent deliverables
2. Assigns to specialist agents:
   - /agent architect "design API structure and contracts"
   - /agent dev "scaffold frontend application"
   - /agent scrum "create initial documentation structure"
3. Tracks in agent_processes.json
4. Handles any interdependencies as they emerge
5. Runs multi-stage review on each deliverable
```

### Scenario 3: Wave-Based Execution (>5 Tasks)
```
User: "Generate all 12 feature specifications in parallel"

Primary Agent:
1. Identifies 12 spec generation tasks
2. Creates 3 waves (5 + 5 + 2)
3. Wave 1: Deploys 5 architect agents
4. Monitors and collects Wave 1 results
5. Wave 2: Deploys next 5 architect agents
6. Continues until all complete
7. Validates CASCADE integrity across all specs
```

## Best Practices

### When to Use Parallel Execution
 **Good Candidates**:
- Independent PRD sections
- Multiple feature specifications
- Separate deliverables (docs, tests, code)
- Different asset PRDs in multi-asset projects
- Non-overlapping code modules

L **Keep Sequential**:
- Tasks with dependencies
- CASCADE validation critical paths
- Shared resource modifications
- Complex integrations
- Ordered workflows

### Monitoring Parallel Agents
```bash
# Check all agent status
/agent

# Monitor specific agent output
# Agents write progress to their output locations
tail -f /ai_framework/working/[agent_output_file]

# Check state for recovery info
cat /ai_framework/state/agent_processes.json
```

### Coordination Best Practices
1. **Stay as Primary**: Don't switch agents when orchestrating
2. **Clear Task Definitions**: Provide specific, bounded tasks
3. **Monitor Regularly**: Check /agent status periodically
4. **Handle Failures**: Retry failed tasks with same or different agent
5. **Validate Results**: Run CASCADE validation after parallel completion
6. **Clean State**: Clear parallel tracking after user approval

## Integration Points

### With CASCADE System
- Each parallel agent validates CASCADE before starting
- Results must maintain hash integrity
- Conflicts trigger sequential resolution

### With State Management
- All parallel work tracked in agent_processes.json
- Recovery checkpoints for each agent
- Cleanup only after user confirmation

### With Task System
- Tasks marked [P] are parallelizable
- Dependencies prevent parallelization
- Task status updates in real-time

## Commands Summary

### Parallel Execution Commands
```bash
# Launch parallel agents
/agent analyst "task 1"
/agent architect "task 2"
/agent dev "task 3"

# Monitor all agents
/agent

# Check parallel state
cat /ai_framework/state/agent_processes.json

# Resume after crash
/state  # Automatically detects and resumes parallel work
```

## Important Notes

1. **Maximum 5 Concurrent Agents**: Hardware and API limits
2. **State Tracking Mandatory**: Every agent must update state
3. **CASCADE Validation Required**: Maintain integrity
4. **User Approval for Cleanup**: Never auto-clear parallel state
5. **Recovery Always Available**: Can resume from any interruption

---

**Remember**: Parallel execution is powerful but requires careful orchestration. When in doubt, validate CASCADE integrity and maintain comprehensive state for recovery.