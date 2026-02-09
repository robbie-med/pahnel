# Framework Contradiction Analysis

## Core Problem Identified

The framework has contradictory directives about project files:
1. **Says**: Track project work in git (PRDs, specs, tasks, state)
2. **But also says**: Delete state when complete, keep directories empty
3. **Result**: Confusion about what's permanent vs temporary

## Files with Contradictions

### 1. `.gitignore` (FIXED)
**Was**: Ignoring `/PRD.md`, `/ai_project/specs/`, `/ai_project/tasks/`, `/ai_project/state/`
**Now**: Only ignores framework dev files (WORKING_*.md)
**Status**: ✅ Fixed

### 2. `AI_CONTEXT.md`
**Line 105**: Changed "pure, no project pollution" → "serve the project" ✅
**Line 121**: Changed "all project files here" → "YOUR PROJECT WORK" ✅
**Lines 135-153**: Added verbose "PROJECT-FIRST" section ⚠️ REDUNDANT
**Lines 163-164**: Still says "Deleted when task completes / Directory empty between tasks" ❌ CONTRADICTS
**Line 250**: Still says "clear_all_state_files()" ❌ CONTRADICTS

### 3. `ai_framework/rules/ai_state_rules.md`
**Line 5**: "State is ONLY for crash/interruption recovery"
**Line 17**: "Directory should be EMPTY after completion"
**Lines 22-23**: "DELETE ALL STATE FILES - they are for resumption only"
**Entire file philosophy**: Treats state as temporary runtime data, not project artifacts

## What Should Actually Happen

### Clear Categories

**A. Permanent Project Artifacts** (NEVER delete, ALWAYS track in git):
- `/PRD.md`, `/PRD_*.md` - Requirements
- `/ai_project/specs/` - Specifications
- `/ai_project/tasks/` - Task lists
- `/ai_project/resources/` - Examples and assets
- `/ai_project/contexts/` - Project customizations

**B. Project Progress Tracking** (Keep and track):
- `/ai_project/state/project_progress.json` - Overall progress
- Task completion checkboxes in task lists

**C. Session Recovery** (Could be local/ephemeral, team decides):
- `/ai_project/state/session_state.json` - Current editing context
- `/ai_project/state/checkpoint.json` - Recovery instructions
- These could be gitignored like `.vscode/workspace` OR tracked for team collaboration

## Minimal Fix Needed

### 1. Remove Verbose Counter-Directives
Delete the "PROJECT-FIRST: GIT TRACKING (PARAMOUNT)" section I added to AI_CONTEXT.md.
If we don't tell people to ignore files, we don't need verbose instructions to track them.

### 2. Fix State Philosophy
In `ai_state_rules.md` and `AI_CONTEXT.md`:

**Change from**:
- "State is ONLY for recovery"
- "Delete when complete"
- "Directory empty between tasks"

**Change to**:
- State includes project progress (permanent) and session recovery (ephemeral)
- Never delete project artifacts
- Session recovery files can be cleared, project progress cannot

### 3. Update Examples
Change code examples from:
```python
if task_complete:
    clear_all_state_files()  # ❌ Wrong - deletes project work
```

To:
```python
if task_complete:
    # Update task list (permanent record)
    update_task_list(task_id, completed=True)
    # Clear session recovery (optional, if user prefers)
    clear_session_recovery()  # Only session_state.json, checkpoint.json
    # NEVER clear project_progress.json or task lists!
```

## Recommendation

**Make these surgical changes:**
1. Remove lines 135-153 from AI_CONTEXT.md (verbose section I added)
2. Rewrite lines 159-164 to clarify permanent vs ephemeral
3. Rewrite ai_state_rules.md with correct philosophy
4. Update code examples to never delete project artifacts

**Don't add:**
- Verbose "track everything!" instructions
- Redundant explanations
- Counter-directives

**Just remove the contradictions and let natural behavior emerge.**
