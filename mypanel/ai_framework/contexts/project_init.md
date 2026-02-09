# Project Initialization Workflow
**CONDITIONAL LOAD**: Loaded during project setup, initialization, or when starting new projects

## Project Initialization Phases

### Phase 1: PRD Discovery
Interactive conversation systematically covering:

#### 1. Purpose & Mission
- What problem does this solve?
- What makes this solution unique?
- What is the core mission?

#### 2. Target Audience  
- Who are the primary users?
- What is their technical sophistication?
- What geographic regions?
- What devices/platforms?

#### 3. Core Features
- **MVP Features** (must-have for launch)
- **Phase 2 Features** (nice-to-have)
- **Future Vision** (long-term possibilities)
- **Non-Goals** (what we explicitly won't build)

#### 4. Technical Requirements
- Technology stack preferences
- Performance requirements
- Security requirements  
- Platform targets
- Scale expectations

#### 5. Business Model
- Revenue streams
- Competition/alternatives
- Success metrics
- Cost structures

### Phase 2: Specification Development
Once PRD is locked, generate comprehensive specs:

1. **Technical Architecture**
   - System design
   - Database schema
   - API structure
   - Security architecture

2. **User Personas & Journeys**
   - Detailed user profiles
   - User journey maps
   - Pain points & solutions

3. **Detailed Workflows**
   - Core use cases
   - Edge cases
   - Error scenarios
   - Integration points

4. **API Contracts**
   - Endpoint definitions
   - Request/response formats
   - Authentication flows
   - Rate limiting

5. **Testing Requirements**
   - Test strategies
   - Coverage requirements
   - Performance benchmarks
   - Acceptance criteria

### Phase 3: Task Generation
Create structured, prioritized task list:

1. **Setup Tasks**
   - Project structure
   - Development environment
   - CI/CD pipeline
   - Documentation setup

2. **Feature Tasks**
   - User stories
   - Dependencies mapped
   - Acceptance criteria
   - Story points

3. **Technical Tasks**
   - Infrastructure setup
   - Database migrations
   - API implementation
   - Integration work

4. **Quality Tasks**
   - Unit tests
   - Integration tests
   - E2E tests
   - Performance tests

5. **Documentation Tasks**
   - API documentation
   - User guides
   - Developer docs
   - Deployment guides

### Phase 4: Implementation
Execute approved tasks systematically:

1. **Pre-Implementation**
   - Verify task dependencies
   - Check CASCADE alignment
   - Review acceptance criteria
   - Set up working environment

2. **During Implementation**
   - Follow test-first approach
   - Track progress in state
   - Apply quality standards
   - Create checkpoints

3. **Post-Implementation**
   - Run all tests
   - Validate acceptance criteria
   - Update documentation
   - Mark task complete

## Initialization Commands

### Starting Fresh
```bash
/init          # Start new project from templates
/prd           # Begin PRD development
/prime         # Analyze existing project
```

### Project Structure Creation
```python
def initialize_project_structure():
    create_directories([
        "/ai_framework/",
        "/ai_framework/templates/",
        "/ai_framework/specs/",
        "/ai_framework/tasks/",
        "/ai_framework/state/",
        "/ai_framework/resources/",
        "/ai_project/",
        "/.claude/agents/",
        "/.claude/commands/",
        "/.claude/hooks/"
    ])
    
    copy_templates_to_project()
    initialize_empty_state()
    create_readme()
```

## When This Context Loads
- Command: `/init`
- Keywords: "new project", "start project", "initialize", "begin"
- First time setup detected
- No PRD exists yet
- User asks about project structure or setup