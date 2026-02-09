# Tasks Directory - Implementation Tracking

## Purpose
Central location for task lists and progress tracking.

## Task Format
```
T001 [P] Task description
T002     Sequential task (depends on T001)
T003 [P] Parallel task
```
- **[P]** = Parallel execution allowed
- See `/.claude/commands/tasks.md` for full format specification

## Governance
Task management is governed by:
- **Generation**: `/.claude/agents/pm.md` - PM agent creates tasks from specs
- **Test-First**: `/ai_framework/CONSTITUTION.md` - Enforces RED-GREEN-Refactor
- **Commands**: `/.claude/commands/tasks.md` - Task manipulation
- **Validation**: `/.claude/hooks/parallel-task-validator.sh` - Conflict detection
- **Workflow**: `/AI_CONTEXT.md` → "Task-Based Implementation Protocol"

## Quick Reference
- `/tasks` - Show progress
- `/tasks init` - Generate from specs
- `/tasks update` - Refresh from changes
- Tasks require approved specs (see `/ai_framework/specs/`)
- Active work tracked in `/ai_framework/state/` (resumption only)

## Files Here
- `task-list.md` - Current tasks
- `Template_Task.md` - Task structure template
- Completions tracked by checkboxes in `task-list.md` ([ ] = pending, [x] = complete)