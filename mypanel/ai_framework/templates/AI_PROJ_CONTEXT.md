# Project-Specific AI Directives

## Purpose of This Document
This file contains AI-specific behavioral instructions for THIS project. These directives tell AI models HOW to work on this specific project, while PROJ_Constitution.md defines WHAT principles must be followed.

**This is different from PROJ_Constitution.md:**
- AI_PROJ_CONTEXT = AI behavior customizations for this project
- PROJ_Constitution = Non-negotiable project principles

## Project Overview
<!-- Customize this section with your project details -->
- **Project Name**: [Your Project Name]
- **Project Type**: [Web App / CLI Tool / Library / etc.]
- **Primary Goal**: [Main objective]
- **Target Completion**: [Timeline]

## Technology Stack
<!-- Define your project's tech stack -->
- **Language**: [Primary language]
- **Framework**: [Main framework if applicable]
- **Database**: [Database choice if applicable]
- **Testing**: [Testing framework]
- **Deployment**: [Deployment target]

## Project-Specific Rules

### 1. Code Style & Standards
<!-- Define project-specific coding standards -->
- **Style Guide**: [Which style guide to follow]
- **Naming Conventions**: [Specific naming patterns]
- **File Organization**: [How to organize project files]
- **Comment Style**: [Documentation standards]

### 2. Development Constraints
<!-- List any specific constraints or requirements -->
- **Performance Targets**: [Specific metrics]
- **Browser/Platform Support**: [Minimum versions]
- **Security Requirements**: [Specific security needs]
- **Accessibility Standards**: [WCAG level, etc.]

### 3. Integration Requirements
<!-- Define external integrations -->
- **APIs**: [External services to integrate]
- **Authentication**: [Auth approach]
- **Third-party Libraries**: [Approved libraries]
- **Data Sources**: [External data requirements]

## Project-Specific Workflows

### Development Process
<!-- Customize the development workflow for this project -->
1. **Local Development**:
   - Commands to run
   - Environment setup
   - Hot reload configuration

2. **Testing Requirements**:
   - Unit test coverage targets
   - Integration test requirements
   - E2E test scenarios

3. **Build & Deployment**:
   - Build commands
   - Deployment process
   - Environment configurations

### Git Workflow
<!-- Define git conventions for this project -->
- **Branch Naming**: [Pattern for branch names]
- **Commit Messages**: [Commit message format]
- **PR Process**: [Pull request requirements]
- **Code Review**: [Review requirements]

## Content Guidelines
<!-- Project-specific content rules -->
- **Tone & Voice**: [How to communicate in the app]
- **Terminology**: [Specific terms to use/avoid]
- **Localization**: [Language requirements]
- **Error Messages**: [Error message style]

## File Organization Rules
<!-- How files should be organized in this project -->
```
/src/                    # Source code structure
  /components/           # [Component organization]
  /utils/               # [Utility organization]
  /services/            # [Service organization]
  /types/               # [Type definitions]
  
/tests/                 # Test organization
/docs/                  # Documentation
/scripts/               # Build/deploy scripts
```

## Testing Requirements
<!-- Specific testing requirements for this project -->
- **Unit Tests**: [Coverage requirements]
- **Integration Tests**: [What to test]
- **Performance Tests**: [Performance criteria]
- **Security Tests**: [Security testing needs]

## Documentation Standards
<!-- How documentation should be maintained -->
- **Code Documentation**: [Inline doc requirements]
- **API Documentation**: [API doc format]
- **User Documentation**: [End-user doc needs]
- **Developer Guide**: [Developer doc requirements]

## Deployment Configuration
<!-- Deployment-specific configuration -->
- **Environments**: [Dev/Staging/Prod setup]
- **CI/CD Pipeline**: [Automation requirements]
- **Monitoring**: [What to monitor]
- **Rollback Process**: [How to handle rollbacks]

## Performance Targets
<!-- Specific performance requirements -->
- **Load Time**: [Target metrics]
- **Response Time**: [API response targets]
- **Concurrent Users**: [Scalability targets]
- **Resource Usage**: [Memory/CPU limits]

## Security Requirements
<!-- Project-specific security needs -->
- **Authentication**: [Auth requirements]
- **Authorization**: [Permission model]
- **Data Protection**: [Encryption needs]
- **Compliance**: [Regulatory requirements]

## Known Decisions
<!-- Document important decisions made for this project -->
- **Decision 1**: [What and why]
- **Decision 2**: [What and why]
- **Decision 3**: [What and why]

## Project-Specific State
<!-- Track project-specific state information -->
- **Current Phase**: [Where we are]
- **Completed Milestones**: [What's done]
- **Pending Items**: [What's remaining]
- **Blockers**: [Current blockers]

## Custom Agent Configuration
<!-- If using specialized agents for this project -->
- **Agent Roles**: [Specific agent assignments]
- **Review Process**: [Multi-stage review needs]
- **Quality Gates**: [Quality checkpoints]

## Notes for Future Development
<!-- Important notes for future work -->
- **Phase 2 Features**: [Planned enhancements]
- **Technical Debt**: [Known issues to address]
- **Optimization Opportunities**: [Performance improvements]
- **Refactoring Needs**: [Code improvement areas]

---

**Document Status**: Template
**Last Updated**: [Update date]
**Project Phase**: [Current phase]
**Review Schedule**: [When to review]

<!-- 
CUSTOMIZATION GUIDE:
1. Replace all bracketed placeholders with project-specific information
2. Remove sections that don't apply to your project
3. Add new sections as needed for your specific requirements
4. Keep this document updated as the project evolves
5. Use this to override or extend framework defaults in CLAUDE.md
-->