# Project-Specific Agents

This directory is for custom agents specific to your project.

## Purpose

While the framework provides 16 standard agents in `.claude/agents/`, you may need:
- Project-specific expertise
- Custom workflows
- Domain-specific agents
- Modified versions of framework agents

## Usage

### Creating a Project Agent
1. Create a new `.md` file in this directory
2. Follow the same format as framework agents
3. Include activation, authority, and integration sections

### Overriding Framework Agents
To override a framework agent for this project:
1. Copy the agent from `.claude/agents/`
2. Modify as needed
3. The project version takes precedence

### Custom Workflows
Create workflow files here:
- `custom_workflow.md` - Define multi-agent patterns
- `project_rules.md` - Project-specific agent rules

## Example Structure

```
ai_project/agents/
├── README.md           (this file)
├── data_scientist.md   (custom agent)
├── ml_engineer.md      (custom agent)
├── dev.md             (override of framework dev)
└── ml_workflow.md     (custom workflow)
```

## Integration

Project agents integrate with:
- Framework agents (can call them)
- CASCADE validation system
- State management
- All framework tools

## Best Practices

1. Only create project agents when framework agents insufficient
2. Document why the agent is needed
3. Follow framework conventions
4. Maintain compatibility with CASCADE
5. Test agent interactions

## Current Project Agents

*No project-specific agents defined yet.*

When you add agents, list them here with their purpose.