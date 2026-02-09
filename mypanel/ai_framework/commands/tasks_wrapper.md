# Spec-Kit Tasks Wrapper

Wrapper for spec-kit's task generation with Hegemon agent assignment and parallel execution markers.

## Purpose

Generates test-driven development tasks from specifications using spec-kit, then enhances them with Hegemon's agent assignments and parallel execution capabilities.

## Workflow

1. **Input Validation**
   - Verify spec and plan exist in `/ai_project/specs/FEAT-XXX/`
   - Check CASCADE integrity
   - Ensure PRD is MAINTAINED status

2. **Task Generation**
   ```bash
   uvx --from ./ai_framework/tools/spec-kit specify tasks
   ```

3. **Hegemon Enhancement**
   - Parse generated tasks.md
   - Assign agents based on task type:
     - `qa:` Test-related tasks
     - `dev:` Implementation tasks
     - `architect:` Design/contract tasks
     - `scrum:` Documentation tasks
   - Add `[P]` markers for parallelizable tasks
   - Generate task IDs (T001, T002, etc.)

4. **Output Structure**
   - Port to `/ai_project/tasks/FEAT-XXX-tasks.md`
   - Create task tracking JSON
   - Update CASCADE metadata

## Usage

```python
def generate_tasks_with_agents(feat_id: str):
    bridge = SpecKitBridge(framework_root)
    spec_dir = bridge.project_specs_dir / feat_id
    
    # Verify prerequisites
    if not (spec_dir / "spec.md").exists():
        raise ValueError(f"Specification required for {feat_id}")
    
    if not (spec_dir / "plan.md").exists():
        raise ValueError(f"Plan required for {feat_id}")
    
    workspace = bridge.create_spec_kit_workspace()
    
    try:
        # Copy spec and plan to workspace
        workspace_spec_dir = workspace / "specs" / feat_id
        workspace_spec_dir.mkdir(parents=True)
        
        for artifact in ["spec.md", "plan.md", "data-model.md"]:
            source = spec_dir / artifact
            if source.exists():
                shutil.copy2(source, workspace_spec_dir / artifact)
        
        # Generate tasks
        code, stdout, stderr = bridge.run_spec_kit_command(
            "tasks",
            ["--spec", str(workspace_spec_dir)],
            workspace
        )
        
        if code == 0:
            # Get generated tasks
            tasks_file = workspace_spec_dir / "tasks.md"
            if tasks_file.exists():
                # Enhance with agents
                enhanced_tasks = assign_agents_to_tasks(
                    tasks_file.read_text()
                )
                
                # Add parallel markers
                enhanced_tasks = mark_parallel_tasks(enhanced_tasks)
                
                # Save to project
                tasks_path = Path(f"ai_project/tasks/{feat_id}-tasks.md")
                tasks_path.write_text(enhanced_tasks)
                
                # Create tracking JSON
                create_task_tracking(tasks_path, feat_id)
                
                return tasks_path
                
    finally:
        bridge.cleanup_workspace(workspace)
```

## Agent Assignment Logic

```python
def assign_agents_to_tasks(tasks_content: str) -> str:
    """Assign agents based on task patterns"""
    
    patterns = {
        'qa': [
            r'test', r'verify', r'validate', r'check',
            r'assertion', r'coverage', r'e2e', r'unit test'
        ],
        'architect': [
            r'design', r'architect', r'contract', r'schema',
            r'api', r'interface', r'structure'
        ],
        'dev': [
            r'implement', r'create', r'build', r'add',
            r'integrate', r'connect', r'setup'
        ],
        'scrum': [
            r'document', r'readme', r'guide', r'tutorial',
            r'example', r'sample'
        ]
    }
    
    # Parse and assign agents
    enhanced_lines = []
    for line in tasks_content.split('\n'):
        if line.startswith('- [ ]'):
            agent = determine_agent(line, patterns)
            task_id = generate_task_id()
            
            # Format: - [ ] [qa:T001] Task description
            enhanced_line = line.replace(
                '- [ ]',
                f'- [ ] [{agent}:{task_id}]'
            )
            enhanced_lines.append(enhanced_line)
        else:
            enhanced_lines.append(line)
    
    return '\n'.join(enhanced_lines)
```

## Parallel Execution Markers

```python
def mark_parallel_tasks(tasks_content: str) -> str:
    """Add [P] markers for parallelizable tasks"""
    
    # Tasks that can run in parallel:
    # - Independent test creation
    # - Multiple component implementations
    # - Documentation tasks
    
    parallel_patterns = [
        r'Create.*test',
        r'Implement.*component',
        r'Add.*documentation',
        r'Setup.*independent'
    ]
    
    # Add [P] markers where appropriate
    # Format: - [ ] [qa:T001][P] Task description
```

## Output Format

### Enhanced Tasks File
```markdown
# Tasks for FEAT-001-feature

## Phase 1: Test Setup
- [ ] [qa:T001][P] Create unit tests for user model
- [ ] [qa:T002][P] Create integration tests for auth flow
- [ ] [architect:T003] Design API contract for user endpoints

## Phase 2: Implementation
- [ ] [dev:T004] Implement user model with validations
- [ ] [dev:T005][P] Create user service layer
- [ ] [dev:T006][P] Add user controller endpoints

## Phase 3: Integration
- [ ] [dev:T007] Connect user service to database
- [ ] [qa:T008] Run integration test suite
- [ ] [scrum:T009] Update API documentation
```

### Task Tracking JSON
```json
{
  "feat_id": "FEAT-001-feature",
  "total_tasks": 9,
  "by_agent": {
    "qa": 3,
    "dev": 4,
    "architect": 1,
    "scrum": 1
  },
  "parallel_capable": 5,
  "phases": 3,
  "status": "ready",
  "generated_at": "2024-XX-XX",
  "spec_kit_version": "v0.0.30"
}
```

## Error Handling

- **Missing prerequisites**: Require spec.md and plan.md
- **Task generation failure**: Report spec-kit errors
- **Agent assignment conflicts**: Default to 'dev' agent
- **CASCADE validation**: Ensure spec hasn't changed

## Integration Points

- Called by `/tasks` command when spec-kit available
- Feeds into agent orchestration system
- Enables parallel execution via Task tool
- Maintains state tracking per task