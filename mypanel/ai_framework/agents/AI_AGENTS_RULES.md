# Framework Agent Usage Rules

## Agent System Architecture

This document guides AI models on proper agent usage within the Hegemon Framework.

## Agent Locations

### Primary Agent Definitions
**Location**: `.claude/agents/*.md`
- Complete agent definitions with full capabilities
- 16 specialized agents covering all aspects of development
- Each agent includes CASCADE validation and state management

### Framework Rules and Workflows
**Location**: `ai_framework/agents/`
- This file (usage rules)
- Future workflow definitions (*_workflow.md)
- Multi-agent orchestration patterns

### Project-Specific Agents
**Location**: `ai_project/agents/`
- Custom agents for specific projects
- Overrides or extensions of framework agents
- Project-unique workflows

## Available Agents

### Core Development Team
- **analyst**: Requirements gathering, PRD development
- **architect**: Technical design, specifications
- **dev**: Implementation, coding, testing
- **pm**: Project management, task generation, agile facilitation
- **qa**: Testing, quality assurance

### Executive Team
- **ceo**: Strategic vision, high-level decisions
- **cfo**: Financial modeling, pricing strategy
- **legal**: Compliance, contracts, privacy
- **marketing**: Go-to-market, positioning

### Business Development Team
- **pitch**: Strategic pitches, funding requests, stakeholder buy-in (YC-logic)

### Support Team
- **editor**: Content review, style consistency
- **researcher**: Deep research, fact-checking
- **support**: Customer success, operations
- **writer**: Content creation, technical writing

### Design Team
- **ui**: User interface design
- **ux**: User experience research

## Agent Activation Rules

### Automatic Agent Selection
The framework automatically selects agents based on:
1. Current PRD status
2. Available specifications
3. Task requirements
4. User message patterns

### Manual Agent Activation
Users can explicitly activate agents:
```
/agent [agent_name] [task_description]
```

### CASCADE Validation
ALL agents must respect CASCADE integrity:
- PRD → Specifications → Tasks → Implementation
- Each level must validate against its parent
- Stale dependencies block progress

## Workflow Patterns

### Sequential Workflow
```
analyst → architect → pm → dev → qa
```

### Parallel Execution
When multiple independent tasks exist:
- Maximum 5 concurrent agents
- Track in `/ai_framework/state/agent_processes.json`
- See `/ai_framework/rules/ai_agent_rules.md` for orchestration

### Multi-Stage Review
Critical deliverables undergo:
1. Initial creation (specialist agent)
2. Architecture review (architect)
3. Standards review (analyst)
4. Security review (qa)
5. Final approval (primary)

## State Management

### Agent State Tracking
Each agent maintains state in:
- `/ai_framework/state/[agent]_state.json`
- Includes current task, progress, blockers

### Recovery Protocol
On interruption:
1. Check `/ai_framework/state/agent_processes.json`
2. Resume or restart based on checkpoint
3. Validate CASCADE before continuing

## Integration Points

### With Commands
- `/agent` - Activate specific agent
- `/mode` - Set agent mode
- `/state` - Check agent status

### With Contexts
Agent activation triggers loading of:
- `ai_framework/contexts/agent_activation.md`
- Relevant domain contexts

### With Tools
Agents use standard tools:
- Read/Write for file operations
- Task tool for parallel execution
- State management utilities

## Best Practices

### Agent Selection
1. Let framework auto-select when possible
2. Use explicit activation for specific expertise
3. Respect agent authority boundaries
4. Maintain agent continuity during tasks

### Communication
1. Always use agent output format
2. Track handoffs between agents
3. Document decisions in state
4. Maintain CASCADE validation

### Quality
1. Each agent validates their domain
2. No agent skips their checks
3. Quality gates must pass
4. Documentation is mandatory

## Common Patterns

### PRD Development
```
User: "Help me create a PRD"
→ analyst agent activates
→ Guides through template
→ Validates completeness
→ Marks MAINTAINED when ready
```

### Specification Creation
```
PRD Status: MAINTAINED
→ architect agent activates
→ Creates technical specs
→ Updates CASCADE hash
→ Hands off to pm
```

### Task Implementation
```
Task: T001
→ dev agent activates
→ CASCADE validation
→ Implementation
→ Tests
→ Handoff to qa
```

## Important Notes

1. **Single Source of Truth**: Agent definitions in `.claude/agents/`
2. **CASCADE is Mandatory**: Never skip validation
3. **State Persistence**: Always save progress
4. **Clean Handoffs**: Document agent transitions
5. **Parallel Limits**: Maximum 5 concurrent agents

For parallel orchestration rules, see: `/ai_framework/rules/ai_agent_rules.md`
For agent definitions, see: `.claude/agents/`
For project customizations, see: `ai_project/agents/`