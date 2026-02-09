# Implementation Plan: [FEATURE NAME]

**Feature ID**: FEAT-[XXX]-[feature-name]  
**Date**: [DATE]  
**Specification**: [link to spec.md]

## Execution Flow (/specs command scope)
```
1. Load feature spec from specification
   → If not found: ERROR "No feature spec found"
2. Analyze technical context
   → Detect project type (web/mobile/cli)
   → Identify technology stack
3. Check Constitution compliance
   → If violations: Document and justify
   → If unjustifiable: ERROR "Simplify approach"
4. Generate technical architecture
   → Define components and boundaries
   → Create API contracts
   → Design data models
5. Plan test implementation (RED phase)
   → Contract tests first
   → Then integration tests
   → Then E2E tests
   → Finally unit tests
6. Define implementation sequence
   → Dependencies first
   → Core features next
   → Polish last
7. Identify parallel opportunities
   → Mark tasks that can run concurrently
8. Validate completeness
   → All requirements covered?
   → All tests defined?
9. Return: SUCCESS (ready for task generation)
```

## Summary
[One paragraph: primary requirement + technical approach]

## Technical Context

### Stack & Environment
**Language/Version**: [e.g., Python 3.11, TypeScript 5.0]  
**Framework**: [e.g., FastAPI, Next.js, or NEEDS CLARIFICATION]  
**Database**: [e.g., PostgreSQL 15, MongoDB, or N/A]  
**Testing**: [e.g., pytest, Jest, or NEEDS CLARIFICATION]  
**Deployment**: [e.g., Docker, Kubernetes, AWS Lambda]  
**CI/CD**: [e.g., GitHub Actions, Jenkins]

### Performance Requirements
**Response Time**: [< Xms p95 or NEEDS CLARIFICATION]  
**Throughput**: [X requests/sec or NEEDS CLARIFICATION]  
**Concurrent Users**: [X users or NEEDS CLARIFICATION]  
**Data Volume**: [X GB or NEEDS CLARIFICATION]

### Constraints
**Budget**: [infrastructure costs]  
**Timeline**: [delivery date]  
**Team Size**: [available developers]  
**Compatibility**: [browser, OS, device requirements]

## Constitution Compliance Check

### Principle Validation
**Test-First Development**:
- ✅ Tests defined before implementation
- ✅ RED-GREEN-Refactor cycle planned
- ⚠️ [Any concerns or adjustments]

**Simplicity**:
- Projects count: [X] (max 3 recommended)
- Using frameworks directly? [Yes/No]
- Single data model? [Yes/No]
- Avoiding unnecessary patterns? [Yes/No]

**[Other Constitution Principles]**:
- Status: [✅/⚠️/❌]
- Notes: [compliance details]

### Justified Violations
*If any principles must be violated, document why:*
- **Principle**: [which one]
- **Reason**: [why violation necessary]
- **Mitigation**: [how to minimize impact]
- **Approval**: [who approved]

## Architecture Design

### Component Architecture
```
┌─────────────────┐     ┌─────────────────┐
│   Frontend      │────▶│   API Gateway   │
└─────────────────┘     └─────────────────┘
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
            ┌─────────────┐      ┌─────────────┐
            │   Service A  │      │   Service B  │
            └─────────────┘      └─────────────┘
                    │                     │
                    └──────────┬──────────┘
                               ▼
                        ┌─────────────┐
                        │   Database   │
                        └─────────────┘
```

### API Contracts

#### Contract: [API Name]
**Endpoint**: `[METHOD] /api/[resource]`  
**Purpose**: [what this does]

**Request**:
```json
{
  "field1": "type",
  "field2": "type"
}
```

**Response (Success)**:
```json
{
  "status": "success",
  "data": {
    "field1": "value",
    "field2": "value"
  }
}
```

**Response (Error)**:
```json
{
  "status": "error",
  "code": "ERROR_CODE",
  "message": "Human readable message"
}
```

**Validation Rules**:
- field1: [validation rules]
- field2: [validation rules]

### Data Model

#### Entity: [Name]
```yaml
attributes:
  - id: UUID (primary key)
  - name: String (required, max 255)
  - created_at: Timestamp
  - updated_at: Timestamp

relationships:
  - belongs_to: User
  - has_many: Items

validations:
  - name must be unique per user
  - created_at <= updated_at

indexes:
  - (user_id, name) - unique
  - created_at - for sorting
```

## Test Implementation Plan

### Phase 1: Contract Tests (MUST FAIL FIRST)
```
tests/contract/
├── test_[api]_create.py    # POST endpoint contract
├── test_[api]_read.py      # GET endpoint contract
├── test_[api]_update.py    # PUT endpoint contract
└── test_[api]_delete.py    # DELETE endpoint contract
```

**Key Scenarios**:
- Valid request/response format
- Error response format
- Required field validation
- Authorization checks

### Phase 2: Integration Tests
```
tests/integration/
├── test_[feature]_workflow.py    # Complete feature flow
├── test_database_operations.py   # DB interactions
└── test_service_communication.py # Service integration
```

**Key Scenarios**:
- Component interaction
- Database transactions
- External service calls
- Error propagation

### Phase 3: E2E Tests
```
tests/e2e/
├── test_user_journey_[scenario].py
└── test_cross_system_flow.py
```

**Key Scenarios**:
- Complete user workflows
- Multi-step processes
- UI interactions (if applicable)

### Phase 4: Unit Tests (LAST)
```
tests/unit/
├── test_business_logic.py
├── test_validators.py
└── test_utilities.py
```

## Implementation Sequence

### Setup Phase
1. Project structure creation
2. Dependency installation
3. Configuration setup
4. Database schema

### Test Phase (RED)
1. Write contract tests → Run → Verify failure
2. Write integration tests → Run → Verify failure
3. Write E2E tests → Run → Verify failure

### Implementation Phase (GREEN)
1. Implement data models
2. Implement API endpoints
3. Implement business logic
4. Connect components

### Refactor Phase
1. Remove duplication
2. Optimize performance
3. Improve readability
4. Add documentation

## Parallel Execution Opportunities

Tasks that can run simultaneously:
- Different API endpoints (separate files)
- Different test files
- Independent services
- Separate frontend components

Tasks that must be sequential:
- Database schema → Models → Services
- Tests → Implementation
- Core features → Extensions

## Risk Analysis

### Technical Risks
- **Risk**: [description]
  - **Impact**: [High/Medium/Low]
  - **Mitigation**: [strategy]

### Schedule Risks
- **Risk**: [description]
  - **Impact**: [High/Medium/Low]
  - **Mitigation**: [strategy]

## Dependencies

### External Dependencies
- [Service/Library]: [purpose, version]
- [API]: [purpose, SLA]

### Internal Dependencies
- Feature depends on: [other features]
- Required before: [dependent features]

## Success Criteria

### Technical Success
- [ ] All tests passing
- [ ] Performance targets met
- [ ] Security requirements satisfied
- [ ] Code coverage > X%

### Business Success
- [ ] User stories completed
- [ ] Acceptance criteria met
- [ ] Stakeholder approval
- [ ] Metrics tracking enabled

---

## Review Checklist

- [ ] Architecture follows best practices
- [ ] API contracts are complete
- [ ] Test strategy covers all scenarios
- [ ] Constitution compliance verified
- [ ] Dependencies identified
- [ ] Risks assessed and mitigated

---

## Approval

**Status**: [Draft/Reviewed/Approved]  
**Technical Review**: [Pending]  
**Architecture Review**: [Pending]  
**Final Approval**: [Pending]