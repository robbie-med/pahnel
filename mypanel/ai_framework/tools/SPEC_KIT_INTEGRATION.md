# Spec-Kit Integration Guide

## Overview

GitHub's spec-kit v0.0.90 has been integrated into the Hegemon Framework as a vendored tool, providing enhanced specification generation while maintaining framework integrity.

## Architecture

```
Hegemon Commands (/specs, /plan, /tasks, /clarify, /analyze)
         ↓
    Bridge Layer (spec_kit_bridge.py)
         ↓
    spec-kit (vendored at /ai_framework/tools/spec-kit/)
         ↓
    Output Capture & Enhancement
         ↓
    /ai_project/specs/ (final location)
```

## Quick Start

### Prerequisites
1. Install `uv` globally (one-time setup):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   source ~/.bashrc  # or ~/.zshrc
   ```

2. Verify installation:
   ```bash
   .claude/hooks/check_dependencies.sh
   ```

### Usage Flow

1. **Complete PRD** (status: MAINTAINED)
   ```
   /prd
   ```

2. **Generate Specifications with spec-kit**
   ```
   /specs "User authentication system"
   ```
   Creates: `/ai_project/specs/FEAT-001-user-authentication/`

3. **Clarify Specifications** (NEW in v0.0.90)
   ```
   /clarify
   ```
   Interactive clarification of up to 5 targeted questions

4. **Enhance with Implementation Plan**
   ```
   /plan FEAT-001-user-authentication
   ```
   Adds: `plan.md` to specification directory

5. **Generate Tasks**
   ```
   /tasks init
   ```
   Creates: `/ai_project/tasks/FEAT-001-tasks.md` with agent assignments

6. **Analyze for Consistency** (NEW in v0.0.90)
   ```
   /analyze
   ```
   Cross-artifact consistency and quality analysis

## New in spec-kit v0.0.90

### New Commands
- **`/clarify`** - Interactive clarification workflow (up to 5 targeted questions)
- **`/analyze`** - Cross-artifact consistency analysis (read-only)
- **`/implement`** - Execute implementation with checklist validation
- **`/checklist`** - Generate domain-specific quality checklists

### Enhanced Features
- **Handoffs**: Commands can suggest next steps (e.g., specify → clarify → plan)
- **Quality Checklists**: Automatic validation before proceeding
- **Branch Naming**: Intelligent short-name generation for git branches
- **Constitution Support**: Project principles validation

### Supported AI Agents
Claude Code, Gemini CLI, GitHub Copilot, Cursor, Qwen Code, opencode,
Codex CLI, Windsurf, Kilo Code, Auggie CLI, Roo Code, CodeBuddy CLI,
Amazon Q Developer CLI, Amp, and more.

## Key Differences from Native spec-kit

### 1. Directory Structure
- **Native spec-kit**: Creates in current directory
- **Hegemon Integration**: Outputs to `/ai_project/specs/FEAT-XXX/`

### 2. Execution Method
- **Native spec-kit**: Direct CLI usage with `speckit.` prefix
- **Hegemon Integration**: Via Hegemon wrapper commands

### 3. Task Enhancement
- **Native spec-kit**: Plain task list organized by user story
- **Hegemon Integration**:
  - Agent assignments `[qa:T001]`
  - Parallel markers `[P]`
  - CASCADE tracking
  - Story labels `[US1]`, `[US2]`

### 4. State Management
- **Native spec-kit**: No state tracking
- **Hegemon Integration**: Full state preservation and recovery

## Troubleshooting

### "uv not found"
**Solution**: Install uv globally
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# Add to PATH if needed
export PATH="$HOME/.local/bin:$PATH"
```

### "spec-kit submodule not initialized"
**Solution**: Initialize git submodule
```bash
git submodule update --init --recursive
```

### "spec-kit command fails"
**Check**:
1. Test spec-kit directly:
   ```bash
   ~/.local/bin/uvx --from ./ai_framework/tools/spec-kit specify --help
   ```

2. Check Python availability:
   ```bash
   uv python list
   ```

3. View bridge logs:
   ```bash
   python ai_framework/tools/spec_kit_bridge.py test
   ```

### "CASCADE validation fails"
**Cause**: PRD changed after spec generation
**Solution**: 
1. Review PRD changes
2. Regenerate specs if needed: `/specs`
3. Or force update: `/specs --force`

### "Tasks not generating"
**Requirements**:
- spec.md must exist
- plan.md should exist (auto-generated if missing)
- PRD must be MAINTAINED status

### "Parallel tasks not working"
**Check**: Task format must be:
```markdown
- [ ] [agent:T###][P] Task description
```

## Fallback Behavior

If spec-kit is unavailable, Hegemon automatically falls back to native generation:
- `/specs` → Native Hegemon specification generation
- `/plan` → Basic plan from templates
- `/tasks` → Standard task list generation

## Performance Tips

1. **Temp Directory Cleanup**: Automatic after each operation
2. **Parallel Execution**: Use `[P]` marked tasks with Task tool
3. **Caching**: spec-kit results cached in CASCADE metadata

## Updating spec-kit

To update to latest spec-kit version:
```bash
cd ai_framework/tools/spec-kit
git fetch origin
git pull origin main

# Update version tracking
echo "Updated to $(git describe --tags)" >> ../TOOL_VERSIONS.md
```

## Integration Status

✅ **Completed**:
- spec-kit v0.0.90 vendored (no submodule)
- Input/output bridge (`spec_kit_bridge.py`)
- Command wrappers (/specs, /plan, /tasks)
- Agent assignment logic
- Parallel task marking
- CASCADE integration
- Fallback mechanisms
- Quality checklist support
- Cross-artifact analysis

🔄 **Future Enhancements**:
- Custom spec-kit templates
- Multi-language support
- Real-time progress tracking
- GitHub Issues export via `/taskstoissues`

## Support

For issues:
1. Check this guide first
2. Run dependency check: `.claude/hooks/check_dependencies.sh`
3. Test bridge directly: `python ai_framework/tools/spec_kit_bridge.py test`
4. Review logs in temp directories (if preserved)

---

*Integration Version: 2.0*
*spec-kit Version: v0.0.90*
*Last Updated: 2025-12*