# Agent Activation System
**CONDITIONAL LOAD**: Loaded when agents are mentioned, parallel work detected, or optimization opportunities identified

## 🤖 Agent Determination Logic

### Check Every Interaction
```python
def determine_active_agent(user_message, project_state):
    # @hege commands are processed first by all models
    if user_message.strip().startswith("@hege"):
        return execute_hege_command(user_message)
    
    # Slash commands are handled by Claude Code CLI
    # This function determines agent for regular messages
    
    # Check PRD status for workflow decisions
    prd_status = get_prd_status()
    
    # PRD-based agent activation
    if prd_status in ["TEMPLATE", "BUILDING"]:
        return activate_agent("analyst", "prd_building")
    
    if prd_status == "MAINTAINED":
        if not specs_exist():
            return activate_agent("architect", "design")
        if specs_exist() and not stories_exist():
            return activate_agent("pm", "planning")
    
    # Message pattern-based activation
    if "STORY-" in user_message or "T0" in user_message:
        story_id = extract_story_id(user_message)
        return activate_agent("dev", "implementation", story_id)
    
    if any(keyword in user_message.lower() for keyword in 
           ["test", "validate", "qa", "quality"]):
        return activate_agent("qa", "testing")
    
    if any(keyword in user_message.lower() for keyword in 
           ["document", "story", "context"]):
        return activate_agent("scrum", "documentation")
    
    # Check for parallel execution triggers
    if any(phrase in user_message.lower() for phrase in 
           ["in parallel", "simultaneously", "at the same time", 
            "multiple agents", "work on both", "work on all"]):
        load_file("/ai_framework/rules/ai_agent_rules.md")
        return activate_agent("primary", "parallel_orchestration")
    
    # PROACTIVE: Check if multiple independent tasks could benefit from parallelization
    if (multiple_independent_tasks_detected() or 
        user_has_listed_multiple_deliverables() or
        could_benefit_from_parallel_execution()):
        suggest_parallel = True
        print("I notice multiple independent items that could be handled in parallel.")
        print("Would you like me to work on these simultaneously for faster completion?")
    
    # Default coordination
    return activate_agent("primary", "coordination")
```

## 🧠 Extended Thinking Activation (NEW)

### Automatic Extended Thinking Triggers

Extended Thinking is AUTOMATICALLY activated for the following scenarios:

```python
def should_activate_extended_thinking(context):
    """
    Determine if Extended Thinking should be automatically activated
    Extended Thinking provides deeper analysis and reasoning for complex tasks
    """
    triggers = {
        # PRD Development (ALWAYS)
        'prd_active': context.prd_status in ['TEMPLATE', 'BUILDING', 'EDITING'],
        'prd_command': context.command == '/prd',
        'prd_interview': exists("/ai_project/state/interview_progress.json"),
        'agent_is_analyst': context.agent == 'analyst',

        # Specification Development (ALWAYS)
        'spec_generation': context.command in ['/specs', '/specify'],
        'agent_is_architect': context.agent == 'architect',
        'architecture_decisions': 'architecture' in context.mode.lower(),

        # Complex Analysis Tasks
        'feature_scoping': 'scope' in context.task_description.lower(),
        'interview_active': context.interview_stage is not None,
        'multi_asset_complexity': context.structure_type == 'multi_asset',

        # Strategic Planning
        'task_planning': context.command == '/tasks',
        'complex_requirements': len(context.requirements) > 5
    }

    return any(triggers.values())
```

### Extended Thinking Benefits by Agent

| Agent | When Active | Benefit |
|-------|-------------|---------|
| **analyst** | ALL PRD work | Deep problem domain analysis, unstated assumption identification |
| **architect** | ALL spec generation | Architecture pattern matching, technology trade-off analysis |
| **pm** | Task generation | Dependency analysis, optimal task sequencing |
| **dev** | Complex features | Algorithm optimization, error handling strategies |
| **qa** | Test planning | Edge case identification, comprehensive test coverage |

### Visual Indicators

When Extended Thinking is active, show user:
```
[🧠 Extended Thinking Active - Deep Analysis Mode]
```

This indicator should be shown at the start of PRD/Spec work and interview sessions.

## Agent Capabilities Summary

### Core Agents
- **analyst**: PRD development and requirements gathering (Extended Thinking: ALWAYS)
- **architect**: Technical specifications and system design (Extended Thinking: ALWAYS)
- **pm**: Task generation and project management (Extended Thinking: When complex)
- **dev**: Implementation with CASCADE validation
- **qa**: Testing and validation
- **scrum**: Documentation and story context
- **primary**: Coordination and framework management (includes parallel orchestration)

### Parallel Execution Optimization
When the model detects opportunities for speed/outcome optimization through parallel agents:
1. Identify independent work items
2. Assess available agent capacity (max 5 concurrent)
3. Suggest parallel approach to user
4. Deploy agents upon approval
5. Coordinate results through primary agent

### Agent Handoff Protocol
```python
def handoff_between_agents(from_agent, to_agent, context):
    handoff = {
        "from": from_agent,
        "to": to_agent,
        "timestamp": now(),
        "context": context,
        "work_completed": summarize_completed_work(),
        "next_steps": identify_next_steps()
    }
    save_to_state("agent_handoff.json", handoff)
    activate_agent(to_agent, inherit_context=True)
```

## When This Context Loads
- User mentions specific agents or agent-related commands
- User requests parallel work or mentions multiple tasks
- Model detects opportunity for parallel optimization
- Commands: `/agent`, `/mode`
- Keywords: "parallel", "simultaneously", "multiple", "agents"

**Full Agent Details**: See `/.claude/agents/` for complete specifications
**Parallel Rules**: Loads `/ai_framework/rules/ai_agent_rules.md` when parallel execution triggered