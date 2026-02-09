# Master Task List Template

## Project Information
- **Project ID**: [project_name_here]
- **Generated From**: PRD and Specifications
- **Generation Date**: [YYYY-MM-DD]
- **Total Tasks**: 0
- **Estimated Effort**: 0 hours

## Task Structure

### Task Template
```
TASK-XXX: [Task Title]
Category: [feature|technical|documentation|testing|deployment]
Priority: [critical|high|medium|low]
Status: [ ] pending | [ ] in_progress | [ ] blocked | [x] completed

Description:
[Detailed description of what needs to be done]

Dependencies:
- Requires: TASK-001, TASK-002 (must complete before this)
- Enables: TASK-003, TASK-004 (unlocked by this)

Assignment:
- Primary Agent: [agent_name]
- Review Agents: [agent1, agent2]
- Human Review Required: [Yes/No]

Estimation:
- Effort Hours: [X]
- Complexity: [trivial|simple|moderate|complex|very_complex]
- Risk Level: [low|medium|high]

Acceptance Criteria:
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

Deliverables:
- Type: [code|document|configuration|test]
- Path: /path/to/output
- Description: [What will be produced]

Quality Gates:
- Test Coverage: ≥80%
- Documentation: Complete
- Review Approval: 2 reviewers required
```

## Phase-Based Task Organization

### Phase 1: Foundation
**Description**: Core infrastructure and setup

#### Tasks:
- [ ] TASK-001: [Task title]
- [ ] TASK-002: [Task title]

---

### Phase 2: Core Features
**Description**: MVP functionality

#### Tasks:
- [ ] TASK-010: [Task title]
- [ ] TASK-011: [Task title]

---

### Phase 3: Enhancement
**Description**: Additional features

#### Tasks:
- [ ] TASK-020: [Task title]
- [ ] TASK-021: [Task title]

---

### Phase 4: Polish
**Description**: Quality and optimization

#### Tasks:
- [ ] TASK-030: [Task title]
- [ ] TASK-031: [Task title]

---

### Phase 5: Deployment
**Description**: Production readiness

#### Tasks:
- [ ] TASK-040: [Task title]
- [ ] TASK-041: [Task title]

## Parallel Execution Opportunities

### Batch 1: Independent Foundation Tasks
**Max Parallel**: 5 agents
**Description**: Tasks that can run simultaneously without dependencies

Tasks eligible for parallel execution:
- [ ] TASK-001 [P]
- [ ] TASK-002 [P]
- [ ] TASK-003 [P]

### Batch 2: Feature Development
**Max Parallel**: 5 agents
**Description**: Independent feature implementations

Tasks eligible for parallel execution:
- [ ] TASK-010 [P]
- [ ] TASK-011 [P]
- [ ] TASK-012 [P]

## Multi-Stage Review Workflows

### Standard Review Workflow
1. **Initial Creation** → specialist agent
2. **Technical Review** → architecture_reviewer agent
3. **Quality Review** → standards_reviewer agent
4. **Security Review** → security_reviewer agent
5. **Final Approval** → project_manager agent

### Documentation Review Workflow
1. **Content Creation** → documentation_specialist agent
2. **Technical Accuracy** → technical_reviewer agent
3. **Readability Check** → documentation_reviewer agent
4. **Final Polish** → editor agent

## Agent Specializations Required

| Agent Name | Tasks Assigned | Specialization | Status |
|------------|---------------|----------------|---------|
| technical_specialist | 0 | Implementation | Ready |
| documentation_specialist | 0 | Documentation | Ready |
| test_specialist | 0 | Testing | Ready |
| architecture_reviewer | 0 | Review | Ready |
| security_reviewer | 0 | Security | Ready |

## Risk Register

### RISK-001: [Risk Description]
- **Probability**: [low|medium|high]
- **Impact**: [low|medium|high]
- **Mitigation**: [Mitigation strategy]
- **Contingency**: [Fallback plan]
- **Affected Tasks**: TASK-001, TASK-002

## Metrics and Tracking

### Velocity Metrics
- **Tasks per Day**: 0
- **Story Points per Sprint**: 0

### Quality Metrics
- **Defect Rate**: 0%
- **Rework Percentage**: 0%
- **First-Time Pass Rate**: 0%

### Efficiency Metrics
- **Actual vs Estimated**: 0%
- **Automation Percentage**: 0%
- **Parallel Execution Rate**: 0%

## TDD Task Structure (from Spec-Kit Integration)

### Test-First Development Tasks
**CRITICAL**: Tests MUST be written and MUST FAIL before implementation

#### Phase A: Contract Tests (MUST COMPLETE FIRST)
- [ ] T001 [P] Contract test POST /api/resource
- [ ] T002 [P] Contract test GET /api/resource/{id}
- [ ] T003 [P] Contract test PUT /api/resource/{id}
- [ ] T004 [P] Contract test DELETE /api/resource/{id}

#### Phase B: Integration Tests
- [ ] T010 [P] Integration test for user workflow
- [ ] T011 [P] Integration test for data persistence
- [ ] T012 [P] Integration test for external services

#### Phase C: Implementation (ONLY after tests fail)
- [ ] T020 Create resource model
- [ ] T021 Implement service layer
- [ ] T022 Create API endpoints
- [ ] T023 Add validation logic

#### Phase D: Unit Tests (Last)
- [ ] T030 [P] Unit tests for validators
- [ ] T031 [P] Unit tests for utilities
- [ ] T032 [P] Unit tests for helpers

## Task Generation Metadata

### Generation Information
- **Generation Method**: automated_from_specs
- **Human Review Status**: pending
- **Last Updated**: [YYYY-MM-DD]
- **Version**: 1.0.0
- **Approved By**: pending
- **Locked**: false

### CASCADE Tracking
- **PRD Hash**: [generated]
- **Spec Hash**: [generated]
- **Task List Hash**: [generated]

---

## Notes

### Parallel Execution Markers
- **[P]** = Can run in parallel (different files, no dependencies)
- Tasks without [P] must run sequentially

### Task ID Format
- TASK-XXX for general tasks
- T-XXX for TDD test tasks
- FEAT-XXX-T-XXX for feature-specific tasks

### Status Tracking
- Use checkboxes for completion tracking
- Update status field when task state changes
- Document blockers in task description

---

*This template is used by the /tasks command to generate project task lists from specifications.*