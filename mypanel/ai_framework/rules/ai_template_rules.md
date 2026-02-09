# Template Processing Guide

## Section Priority Markers

Templates use these markers to guide intelligent generation:

### Priority Levels

1. **[CRITICAL NEED]** - Must be completed before proceeding
   - Blocks downstream work if missing
   - Framework will persistently ask for this
   - Examples: Problem statement, core features

2. **[NEEDS ATTENTION]** - Should be completed soon
   - Important but not blocking
   - Framework will periodically remind
   - Examples: Success metrics, team composition

3. **[OPTIONAL]** - Nice to have
   - Can be left empty without issues
   - Framework mentions once then ignores
   - Examples: Future vision features, some compliance items

4. **[AUTO-GENERATED]** - Framework will fill this
   - Based on other inputs
   - User can override if desired
   - Examples: Document status, timestamps

## Progressive Disclosure Strategy

### Phase 1: Initial (/init)
Ask only for:
- Project name
- Brief description
- Primary goal

Generate files with:
- CRITICAL NEED sections highlighted
- Other sections present but marked
- Smart defaults where possible

### Phase 2: PRD Development (/prd)
Guided conversation to fill:
1. CRITICAL NEED sections first
2. NEEDS ATTENTION sections next
3. OPTIONAL sections if user engaged

### Phase 3: Ongoing Refinement
- Check for [NEEDS ATTENTION] during /prime
- Suggest completing sections based on context
- Remove markers as sections completed

## Template Processing Rules

### When generating from template:

```python
def process_template(template, user_context):
    # Remove sections marked [OPTIONAL] if no data
    if section.is_optional and not user_has_data:
        remove_section()
    
    # Keep [CRITICAL NEED] visible
    if section.is_critical and not completed:
        keep_marker_visible()
        add_to_reminders()
    
    # Convert [NEEDS ATTENTION] based on project phase
    if section.needs_attention:
        if project.phase == "early":
            mark_as_todo_later()
        else:
            prompt_for_completion()
```

## Section Dependencies

Some sections depend on others:

```yaml
Technical Requirements:
  depends_on: [Core Features]
  
Success Metrics:
  depends_on: [Purpose & Mission, Core Features]
  
Team Composition:
  depends_on: [Technical Requirements]
```

## Smart Defaults

When possible, provide intelligent defaults:

```yaml
Performance Requirements:
  if web_app:
    default: "< 3s page load, < 200ms API response"
  if cli_tool:
    default: "< 100ms command execution"
    
Security Requirements:
  if has_users:
    default: "JWT auth, HTTPS only, bcrypt passwords"
```

## Example Processing

### Input (Template):
```markdown
### Problem Statement
[CRITICAL NEED: What problem does this solve?]

### Future Vision
[OPTIONAL: Long-term goals]
```

### Output (Generated PRD):
```markdown
### Problem Statement
[CRITICAL NEED: What problem does this solve?]
<!-- Framework will ask about this immediately -->

<!-- Future Vision section removed as optional and empty -->
```

## Guided Questions

For each section, the framework should have intelligent questions:

### Problem Statement Questions:
1. "What specific pain point does this address?"
2. "Who experiences this problem most?"
3. "What happens if this isn't solved?"

### Target Audience Questions:
1. "Describe your ideal first user"
2. "What's their technical skill level?"
3. "How many users do you expect initially?"

## Progressive Enhancement

As project matures, upgrade markers:

```
Early Stage:
[OPTIONAL: Compliance requirements]

After discussing enterprise customers:
[NEEDS ATTENTION: Compliance requirements - mentioned enterprise needs]

After securing enterprise deal:
[CRITICAL NEED: Compliance requirements - contract requires SOC2]
```