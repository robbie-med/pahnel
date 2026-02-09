# Feature Specification: [FEATURE NAME]

**Feature ID**: FEAT-[XXX]-[feature-name]  
**Created**: [DATE]  
**Status**: Draft  
**From PRD Section**: [Reference to PRD section]

## Execution Flow (main)
```
1. Parse requirements from PRD
   → If incomplete: ERROR "Missing PRD requirements"
2. Extract key concepts
   → Identify: actors, actions, data, constraints
3. For each unclear aspect:
   → Mark with [NEEDS CLARIFICATION: specific question]
4. Generate user scenarios
   → If no clear flow: ERROR "Cannot determine user scenarios"
5. Create functional requirements
   → Each must be testable
   → Mark ambiguous requirements
6. Define key entities (if data involved)
7. Run validation checks
   → If any [NEEDS CLARIFICATION]: WARN "Spec has uncertainties"
   → If implementation details found: ERROR "Remove tech details"
8. Check constitution compliance
   → If violations: ERROR "Constitution violation: [principle]"
9. Return: SUCCESS (spec ready for planning)
```

---

## ⚡ Quick Guidelines
- ✅ Focus on WHAT users need and WHY
- ❌ Avoid HOW to implement (no tech stack, APIs, code structure)
- 👥 Written for business stakeholders, not developers
- 🔒 Must comply with CONSTITUTION.md principles

---

## User Scenarios & Testing

### Primary User Story
As a [user type], I want to [action] so that [benefit].

**Given**: [initial state]  
**When**: [user action]  
**Then**: [expected outcome]

### Acceptance Scenarios
1. **Scenario: [Name]**
   - **Given**: [precondition]
   - **When**: [action taken]
   - **Then**: [expected result]
   - **And**: [additional outcomes]

2. **Scenario: [Error Case]**
   - **Given**: [precondition]
   - **When**: [invalid action]
   - **Then**: [error handling]

### Edge Cases
- What happens when [boundary condition]?
- How does system handle [error scenario]?
- What if [concurrent action]?

## Requirements

### Functional Requirements
- **FR-001**: System MUST [specific capability]
  - Testable: [how to verify]
  - Priority: [High/Medium/Low]
  
- **FR-002**: Users MUST be able to [action]
  - Testable: [verification method]
  - Priority: [High/Medium/Low]

- **FR-003**: System MUST [behavior] [NEEDS CLARIFICATION: specify exact behavior]
  - Testable: [pending clarification]
  - Priority: [High/Medium/Low]

### Non-Functional Requirements
- **Performance**: [specific metrics or NEEDS CLARIFICATION]
- **Security**: [specific requirements or NEEDS CLARIFICATION]
- **Scalability**: [specific targets or NEEDS CLARIFICATION]
- **Availability**: [uptime requirements]

### Key Entities
- **[Entity 1]**: 
  - Purpose: [what it represents]
  - Attributes: [key properties without implementation]
  - Relationships: [connections to other entities]

- **[Entity 2]**:
  - Purpose: [what it represents]
  - Attributes: [key properties]
  - Relationships: [connections]

## API Contracts (High-Level)

### Endpoint: [Resource Name]
- **Purpose**: [what this API does]
- **Operations**: 
  - CREATE: [description]
  - READ: [description]
  - UPDATE: [description]
  - DELETE: [description]
- **Business Rules**: [validation, constraints]

*Note: Detailed contracts in `/contracts/` directory*

## Test Strategy

### Test Pyramid (Enforced Order)
1. **Contract Tests** (API boundaries)
   - Verify API contracts
   - Request/response validation
   - Error scenarios

2. **Integration Tests** (Component interaction)
   - Service communication
   - Database operations
   - External integrations

3. **E2E Tests** (User workflows)
   - Complete user journeys
   - Cross-system flows
   - UI interactions

4. **Unit Tests** (Individual functions)
   - Business logic
   - Utility functions
   - Edge cases

**⚠️ CRITICAL**: Tests MUST be written and MUST FAIL before implementation

## Constitution Compliance Checklist

- [ ] Follows simplicity principle
- [ ] Respects test-first development
- [ ] Maintains library-first architecture (if applicable)
- [ ] Adheres to project constraints
- [ ] No unnecessary complexity

## Dependencies & Assumptions

### Dependencies
- Depends on: [other features/systems]
- Required by: [dependent features]
- External: [third-party services]

### Assumptions
- [Assumption 1 about user behavior]
- [Assumption 2 about system state]
- [NEEDS CLARIFICATION: unclear assumption]

## Success Metrics

- **Acceptance**: [how to know feature is complete]
- **Performance**: [measurable targets]
- **User Satisfaction**: [how to measure]
- **Business Value**: [expected impact]

---

## Review & Acceptance Checklist

### Content Quality
- [ ] No implementation details (languages, frameworks, APIs)
- [ ] Focused on user value and business needs
- [ ] Written for non-technical stakeholders
- [ ] All sections completed or marked NEEDS CLARIFICATION

### Requirement Completeness
- [ ] All requirements are testable
- [ ] Success criteria are measurable
- [ ] Scope is clearly bounded
- [ ] Dependencies identified

### Constitution Compliance
- [ ] Checked against all principles
- [ ] No violations or justified exceptions
- [ ] Approved by: [stakeholder]

---

## Execution Status
*Updated during specification generation*

- [ ] PRD requirements parsed
- [ ] Key concepts extracted
- [ ] Ambiguities marked
- [ ] User scenarios defined
- [ ] Requirements generated
- [ ] Entities identified
- [ ] Constitution checked
- [ ] Review checklist passed

---

## Approval

**Status**: [Draft/Review/Approved]  
**Last Updated**: [Date]  
**Approved By**: [Pending]  
**Lock Date**: [When approved]