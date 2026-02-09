# Expert Review System
**CONDITIONAL LOAD**: Loaded during task completion, quality reviews, or when expert analysis is needed

## Available Experts

### Agent-Based Expert System
Our experts are our specialized agents. Each agent serves as an expert in their domain.
Full definitions are in `/ai_framework/agents/*.md`

### Technical Experts

**Architect** → `/ai_framework/agents/architect.md`
- System design, API contracts, integrations, data architecture
- **Command**: `/expert architect` or `/agent architect`

**Dev** → `/ai_framework/agents/dev.md`
- Implementation, DevOps, security, database, performance
- **Command**: `/expert dev` or `/agent dev`

**QA** → `/ai_framework/agents/qa.md`
- Testing strategies, quality standards, compliance testing
- **Command**: `/expert qa` or `/agent qa`

### Business Experts

**CEO** → `/ai_framework/agents/ceo.md`
- Strategic vision, product direction, high-level decisions
- **Command**: `/expert ceo` or `/agent ceo`

**CFO** → `/ai_framework/agents/cfo.md`
- Financial modeling, pricing, unit economics
- **Command**: `/expert cfo` or `/agent cfo`

**Marketing** → `/ai_framework/agents/marketing.md`
- Positioning, go-to-market, growth strategies
- **Command**: `/expert marketing` or `/agent marketing`

**Legal** → `/ai_framework/agents/legal.md`
- Contracts, compliance, IP, privacy
- **Command**: `/expert legal` or `/agent legal`

### Content Experts

**Writer** → `/ai_framework/agents/writer.md`
- Technical writing, books, documentation
- **Command**: `/expert writer` or `/agent writer`

**Editor** → `/ai_framework/agents/editor.md`
- Review, style consistency, publication standards
- **Command**: `/expert editor` or `/agent editor`

**Researcher** → `/ai_framework/agents/researcher.md`
- Deep research, fact-checking, validation
- **Command**: `/expert researcher` or `/agent researcher`

## Expert Review Integration

### Automatic Suggestion at Task Completion
```python
def suggest_expert_review(task):
    """
    Intelligently suggest relevant agents as experts based on task content
    """
    experts_needed = []
    
    # Dev agent for security/performance/database review
    if involves_authentication(task) or handles_user_data(task):
        experts_needed.append(("dev", "Security implementation review"))
    if involves_heavy_processing(task) or has_database_operations(task):
        experts_needed.append(("dev", "Performance/database review"))
    
    # Architect for API and system changes
    if creates_new_endpoints(task) or changes_architecture(task):
        experts_needed.append(("architect", "API/architecture review"))
    
    # QA for testing coverage
    if lacks_tests(task) or has_complex_logic(task):
        experts_needed.append(("qa", "Test coverage review"))
    
    # Legal for compliance
    if handles_user_data(task) or has_terms_changes(task):
        experts_needed.append(("legal", "Compliance review"))
    
    # CFO for pricing/billing
    if involves_pricing(task) or affects_revenue(task):
        experts_needed.append(("cfo", "Financial impact review"))
    
    if experts_needed:
        print(f"✅ Task {task.id} implementation appears complete.")
        print("")
        print("Recommended expert reviews before marking complete:")
        for expert, reason in experts_needed:
            print(f"  • {expert.title()} Expert - {reason}")
        print("")
        print("Options:")
        print("1. Run all recommended reviews")
        print("2. Select specific experts")
        print("3. Mark complete without review")
        print("4. Continue working on task")
        
        return handle_expert_review_choice(experts_needed)
```

### Manual Expert Invocation
```python
def invoke_expert(expert_type, context=None):
    """
    Manually call an expert for review or guidance
    """
    expert = load_expert(expert_type)
    
    print(f"🎓 {expert.name} Expert Activated")
    print(f"Specialization: {expert.domain}")
    print("")
    
    if context:
        # Review specific code/task
        review_results = expert.review(context)
        print_review_results(review_results)
    else:
        # Provide guidance
        print("How can I help with {expert.domain}?")
        print("Available actions:")
        for action in expert.available_actions:
            print(f"  • {action}")
```

## Expert Review Process

### 1. Code Analysis
```python
def expert_code_review(expert_type, task_id):
    expert = load_expert(expert_type)
    task_files = get_modified_files(task_id)
    
    findings = {
        "critical": [],    # Must fix before complete
        "important": [],   # Should fix soon
        "suggestions": [], # Nice to have improvements
        "approved": []     # What looks good
    }
    
    for file in task_files:
        result = expert.analyze(file)
        categorize_findings(result, findings)
    
    return findings
```

### 2. Review Output Format
```
🎓 Security Expert Review - Task T055

✅ APPROVED:
• Input validation properly implemented
• SQL injection prevention in place
• Error messages don't leak sensitive info

⚠️ IMPORTANT:
• Add rate limiting to authentication endpoint
• Implement CSRF token validation
• Add security headers to responses

🔴 CRITICAL:
• Password stored in plain text (line 45)
• API key exposed in client code (line 78)

Recommendation: Fix critical issues before marking complete
```

### 3. Expert Recommendations
Experts provide actionable recommendations:
- Specific code changes
- Best practice patterns
- Library suggestions
- Configuration improvements
- Testing strategies

## Expert Knowledge by Agent

Each agent brings specific expertise. See full definitions:

### Technical Expertise
- **Architect** (`/ai_framework/agents/architect.md`): System design, APIs, integrations
- **Dev** (`/ai_framework/agents/dev.md`): Full-stack, DevOps, security, databases
- **QA** (`/ai_framework/agents/qa.md`): Testing, quality, compliance
- **PM** (`/ai_framework/agents/pm.md`): Project management, agile, planning

### Business Expertise  
- **CEO** (`/ai_framework/agents/ceo.md`): Vision, strategy, decisions
- **CFO** (`/ai_framework/agents/cfo.md`): Finance, pricing, metrics
- **Marketing** (`/ai_framework/agents/marketing.md`): Positioning, growth, go-to-market
- **Legal** (`/ai_framework/agents/legal.md`): Contracts, compliance, IP
- **Support** (`/ai_framework/agents/support.md`): Customer success, operations

### Content Expertise
- **Writer** (`/ai_framework/agents/writer.md`): Books, technical writing
- **Editor** (`/ai_framework/agents/editor.md`): Review, style, standards
- **Researcher** (`/ai_framework/agents/researcher.md`): Research, validation

## When This Context Loads
- Task appears complete
- User requests expert review via `/expert [type]`
- Quality review needed
- Complex implementation requiring specialized knowledge
- Before marking critical tasks complete
- Keywords: "review", "expert", "quality", "check"