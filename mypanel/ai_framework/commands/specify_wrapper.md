# Spec-Kit Specify Wrapper

Wrapper for spec-kit's specification generation capability within Hegemon Framework.

## Purpose

Generates comprehensive specifications using GitHub's spec-kit tool while maintaining Hegemon's CASCADE integrity and directory structure.

## Workflow

1. **Input Preparation**
   - Extract context from PRD or user description
   - Create isolated temp workspace
   - Prepare formatted input for spec-kit

2. **Spec-Kit Execution**
   ```bash
   uvx --from ./ai_framework/tools/spec-kit specify init
   ```

3. **Output Capture**
   - Scan generated artifacts:
     - spec.md (main specification)
     - plan.md (implementation plan)
     - research.md (research findings)
     - data-model.md (data structures)
     - contracts/ (API contracts)
     - quickstart.md (quick start guide)
     - tasks.md (task breakdown)

4. **Hegemon Integration**
   - Port artifacts to `/ai_project/specs/FEAT-XXX/`
   - Add CASCADE metadata (_cascade_meta.json)
   - Update project state

## Usage

### From PRD
```python
def generate_spec_from_prd(feat_id: str):
    bridge = SpecKitBridge(framework_root)
    
    # Extract PRD context
    prd_context = bridge.extract_prd_context(Path("PRD.md"))
    
    # Create workspace
    workspace = bridge.create_spec_kit_workspace()
    
    try:
        # Prepare input
        bridge.prepare_spec_kit_input(
            prd_context["description"],
            feat_id,
            workspace
        )
        
        # Run spec-kit
        code, stdout, stderr = bridge.run_spec_kit_command(
            "init",
            [],
            workspace
        )
        
        if code == 0:
            # Capture and port output
            artifacts = bridge.scan_spec_kit_output(workspace)
            spec_dir = bridge.port_to_hegemon(artifacts, feat_id)
            
            # Validate
            if bridge.validate_spec_kit_output(spec_dir):
                return spec_dir
        
    finally:
        bridge.cleanup_workspace(workspace)
```

### From Description
```python
def generate_spec_from_description(feat_id: str, description: str):
    bridge = SpecKitBridge(framework_root)
    workspace = bridge.create_spec_kit_workspace()
    
    try:
        # Direct description input
        bridge.prepare_spec_kit_input(description, feat_id, workspace)
        
        # Run spec-kit
        code, stdout, stderr = bridge.run_spec_kit_command(
            "init",
            ["--description", str(workspace / "description.md")],
            workspace
        )
        
        # ... rest of workflow
    finally:
        bridge.cleanup_workspace(workspace)
```

## Error Handling

- **Missing uv**: Prompt to install uv
- **spec-kit failure**: Fall back to native Hegemon spec generation
- **Invalid output**: Report missing required artifacts
- **CASCADE break**: Block and request PRD update

## Output Structure

```
/ai_project/specs/FEAT-001-feature/
├── spec.md              # Main specification
├── plan.md              # Implementation plan
├── research.md          # Research notes
├── data-model.md        # Data structures
├── contracts/           # API contracts
│   ├── api.yaml
│   └── schemas/
├── quickstart.md        # Quick start guide
├── tasks.md             # Task breakdown
└── _cascade_meta.json   # Hegemon CASCADE tracking
```

## Integration Points

- Called by `/specs` command when spec-kit available
- Updates CASCADE hash chain
- Triggers agent assignment for generated tasks
- Maintains state in `/ai_project/state/`