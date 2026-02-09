# [PROJECT NAME] Constitution

*Non-negotiable principles that guide all development decisions*

## Core Development Principles

### I. Test-First Development (NON-NEGOTIABLE)
**Principle**: No implementation without failing tests  
**Enforcement**: 
- Tests must be written before any implementation code
- Tests must fail initially (RED phase)
- Implementation makes tests pass (GREEN phase)
- Then refactor while keeping tests green (REFACTOR phase)

**AI Check**: Before generating implementation code, verify test file exists and is failing

### II. Simplicity First
**Principle**: Start simple, add complexity only when proven necessary  
**Rules**:
- Maximum 3 active projects/services initially
- Use frameworks directly without wrapper classes
- Single data model (no DTOs unless serialization differs)
- No patterns (Repository/UoW) without demonstrated need
- YAGNI (You Aren't Gonna Need It) by default

**AI Check**: Challenge any complexity additions with "Is this needed now?"

### III. Contract-First Development
**Principle**: Define interfaces before implementation  
**Rules**:
- API contracts defined before endpoints
- Data schemas defined before models
- Integration points specified before coding
- Error responses planned upfront

**AI Check**: Verify contracts exist in `/specs/FEAT-XXX/contracts/` before implementation

## Technical Standards

### Code Quality
- **Test Coverage**: Minimum 80% for critical paths
- **Documentation**: Every public API must have docstrings
- **Linting**: Zero errors, minimal warnings
- **Type Safety**: Full typing in TypeScript/Python (if applicable)

### Performance Requirements
- **Response Time**: 95th percentile < [X]ms
- **Throughput**: Minimum [X] requests/second
- **Memory**: Maximum [X]GB per service
- **Startup Time**: < [X] seconds

### Security Requirements
- **Authentication**: [Method - JWT/OAuth/etc]
- **Authorization**: [Model - RBAC/ABAC/etc]
- **Data Protection**: [Encryption requirements]
- **Audit Logging**: All state changes logged
- **Input Validation**: All inputs sanitized

## Architecture Constraints

### Technology Choices
- **Language**: [Primary language and version]
- **Framework**: [Approved framework(s)]
- **Database**: [Approved database(s)]
- **Message Queue**: [If applicable]
- **Cache**: [If applicable]

### Deployment Constraints
- **Environment**: [Cloud provider/On-premise]
- **Containerization**: [Docker/Kubernetes requirements]
- **Scaling**: [Horizontal/Vertical approach]
- **Monitoring**: [Required metrics and tools]

## Development Workflow

### Version Control
- **Branching**: [Strategy - GitFlow/GitHub Flow/etc]
- **Commit Messages**: [Format requirements]
- **PR Requirements**: 
  - Tests must pass
  - Code review required
  - Documentation updated

### Review Process
- **Code Review**: Required for all changes
- **Architecture Review**: Required for new components
- **Security Review**: Required for auth/data changes

## Operational Requirements

### Observability
- **Logging**: Structured JSON logging required
- **Metrics**: Key metrics must be exposed
- **Tracing**: Distributed tracing for all services
- **Alerting**: Critical paths must have alerts

### Reliability
- **Availability**: [Target - 99.9%/99.99%]
- **Recovery Time**: Maximum [X] minutes
- **Data Backup**: [Frequency and retention]
- **Disaster Recovery**: [RTO/RPO requirements]

## Forbidden Practices

**Never Do These**:
1. ❌ Implement without tests
2. ❌ Skip the RED phase (tests must fail first)
3. ❌ Commit secrets or keys
4. ❌ Use `any` type (TypeScript) or skip typing (Python)
5. ❌ Create abstraction layers "for future use"
6. ❌ Ignore linting errors
7. ❌ Skip code review
8. ❌ Deploy without monitoring

## Exception Process

If a principle must be violated:
1. Document the reason in code comments
2. Create a ticket to fix later
3. Get explicit approval from: [Technical Lead/Architect]
4. Update this constitution if pattern emerges

## Constitution Amendments

### Amendment Process
1. Propose change with justification
2. Document impact on existing code/processes
3. Trial period (if applicable)
4. Vote or consensus decision
5. Update constitution with version increment
6. Create migration plan if breaking changes
7. Update all dependent documentation

### Version History
<!-- Version format: MAJOR.MINOR.PATCH
     MAJOR: Breaking changes to core principles
     MINOR: New principles or significant clarifications
     PATCH: Minor clarifications or typo fixes
-->
- **v1.0.0** - [Date] - Initial constitution ratified
<!-- Example amendments:
- **v1.1.0** - [Date] - Added distributed tracing requirement
- **v1.2.0** - [Date] - Clarified test coverage exceptions
- **v2.0.0** - [Date] - Changed from monolith to microservices principles
-->

---

## Governance

**This Constitution supersedes all other practices and preferences.**

- All code generation must comply with these principles
- All PRs must verify constitutional compliance
- Violations must be justified and documented
- Regular audits ensure ongoing compliance

**For AI Models**: 
- Check this document before ANY code generation
- Enforce these principles in all suggestions
- Flag violations to user immediately
- Refuse to generate non-compliant code without explicit override

---

**Constitution Version**: 1.0.0  
**Ratified**: [Date]  
**Last Amended**: [Date]  
**Next Review**: [Date - typically quarterly or semi-annually]

**Amendment Log**:
<!-- Track all amendments with version, date, and brief description
| Version | Date | Amendment | Approved By |
|---------|------|-----------|-------------|
| 1.0.0   | YYYY-MM-DD | Initial constitution | Team |
| 1.1.0   | YYYY-MM-DD | Added X requirement | Team |
-->

**Signatories**:
- [Project Lead] - [Date]
- [Technical Lead] - [Date]
- [Team Members] - [Date]