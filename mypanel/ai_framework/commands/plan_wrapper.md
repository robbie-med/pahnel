# Spec-Kit Plan Wrapper

Wrapper for spec-kit's planning capability to enhance existing specifications.

## Purpose

Generates detailed implementation plans from existing specifications using spec-kit's planning engine.

## Workflow

1. **Locate Existing Spec**
   - Find spec in `/ai_project/specs/FEAT-XXX/`
   - Verify spec.md exists
   - Check CASCADE metadata

2. **Workspace Setup**
   - Copy spec to temp workspace
   - Maintain spec-kit expected structure

3. **Plan Generation**
   ```bash
   uvx --from ./ai_framework/tools/spec-kit specify plan
   ```

4. **Output Integration**
   - Capture enhanced plan.md
   - Update existing spec directory
   - Maintain CASCADE integrity

## Usage

```python
def enhance_spec_with_plan(feat_id: str):
    bridge = SpecKitBridge(framework_root)
    spec_dir = bridge.project_specs_dir / feat_id
    
    if not spec_dir.exists():
        raise ValueError(f"Specification {feat_id} not found")
    
    workspace = bridge.create_spec_kit_workspace()
    
    try:
        # Copy existing spec to workspace
        workspace_spec_dir = workspace / "specs" / feat_id
        workspace_spec_dir.mkdir(parents=True)
        
        # Copy spec.md (minimum requirement for plan)
        shutil.copy2(
            spec_dir / "spec.md",
            workspace_spec_dir / "spec.md"
        )
        
        # Run plan generation
        code, stdout, stderr = bridge.run_spec_kit_command(
            "plan",
            ["--spec", str(workspace_spec_dir)],
            workspace
        )
        
        if code == 0:
            # Port enhanced artifacts back
            artifacts = bridge.scan_spec_kit_output(workspace)
            
            # Selectively update plan-related files
            if "plan.md" in artifacts:
                shutil.copy2(
                    artifacts["plan.md"],
                    spec_dir / "plan.md"
                )
                
            # Update CASCADE metadata
            bridge._add_cascade_metadata(spec_dir, feat_id)
            
            return spec_dir
            
    finally:
        bridge.cleanup_workspace(workspace)
```

## Plan Components

The generated plan.md typically includes:

- **Architecture Overview**: System design decisions
- **Implementation Phases**: Ordered development stages
- **Component Breakdown**: Detailed module descriptions
- **Integration Points**: How components connect
- **Testing Strategy**: Test-first approach
- **Deployment Considerations**: Production readiness

## Error Handling

- **Missing spec**: Cannot generate plan without base specification
- **Invalid spec format**: Ensure spec.md follows expected structure
- **Plan generation failure**: Report spec-kit errors, maintain existing files

## CASCADE Maintenance

Plan generation updates:
1. Spec hash (if spec modified)
2. Plan timestamp
3. Artifact inventory
4. Version tracking

## Integration Points

- Triggered by `/plan` command
- Can be run after `/specs` to enhance
- Feeds into `/tasks` generation
- Updates agent assignments based on plan complexity