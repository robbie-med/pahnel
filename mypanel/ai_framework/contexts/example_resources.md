# Dynamic Example Collection & Resources
**CONDITIONAL LOAD**: Loaded when discussing examples, mockups, resources, or user-provided materials

## Dynamic Example Collection

### Smart Example Requests
Context-driven requests for specific examples that would add value:

```python
# Context-driven example requests
if discussing_ui_complexity:
    create_dir("/ai_project/resources/examples/ui-mockups/")
    ask("Could you provide mockups of the dashboard you described?")

if discussing_api_structure:
    create_dir("/ai_project/resources/examples/api-samples/")
    ask("Sample API responses would help me understand the data structure")

if discussing_report_formats:
    create_dir("/ai_project/resources/examples/report-templates/")
    ask("Could you provide a sample report in the format you need?")

if discussing_data_processing:
    create_dir("/ai_project/resources/examples/data-samples/")
    ask("Sample data files would help me understand the structure")
```

### Example Request Principles
- **Be Specific**: Request exactly what would help
- **Add Value**: Only request if it clarifies requirements
- **Create Structure**: Make directories for easy user placement
- ✅ "Could you provide a sample report format?"
- ❌ "Do you have any examples?"

## Resources Directory - Read-Only Reference Pool

### Purpose
The `/ai_project/resources/` directory serves as a micro MCP (Model Context Protocol) resource pool - a read-only collection of all reference materials and user-provided content.

### Directory Structure
```
/ai_project/resources/       # READ-ONLY at all times
├── examples/               # User-provided examples
│   ├── ui-mockups/        # UI/UX mockups and wireframes
│   ├── api-samples/       # Sample API requests/responses
│   ├── data-samples/      # Sample data files, CSVs, JSONs
│   ├── report-templates/  # Report format examples
│   └── workflow-diagrams/ # Process and workflow diagrams
├── reference/             # Documentation and guides
│   ├── original-code/     # Preserved original implementations
│   ├── style-guides/      # Coding and design standards
│   ├── external-docs/     # Third-party documentation
│   └── architecture/      # System design references
└── assets/                # Files for project use
    ├── images/           # Logos, icons, graphics
    ├── fonts/            # Typography files
    ├── templates/        # Document templates
    └── config-samples/   # Configuration examples
```

### Usage Guidelines

#### Reading Resources
```python
def use_resource_as_reference(resource_path):
    # Always READ, never modify
    content = read_file(resource_path)
    
    # Treat as reference that may be outdated
    if is_requirement_related:
        check_against_prd()  # PRD is source of truth
    
    # Use for implementation guidance
    if is_style_guide:
        apply_patterns_to_new_code()
    
    if is_original_code:
        preserve_business_logic()
        modernize_implementation()
```

#### When User Provides Resources
1. Create appropriate subdirectory if needed
2. Guide user to place files in correct location
3. Acknowledge receipt and intended use
4. Never modify the provided files
5. Reference them during implementation

### Critical Rules
1. **NEVER modify** any file in `/ai_project/resources/`
2. **ALWAYS treat as reference** - PRD is source of truth for requirements
3. **READ operations only** - use as reference, never edit
4. **User uploads only** - only users add content (unless explicitly asked to copy)
5. **Preserve originals** - when implementing, copy patterns don't move files

### Common Resource Types

#### UI Mockups
- Wireframes (Figma, Sketch, PDF)
- Screenshots of desired functionality
- Style references
- Component examples

#### API Samples
- Example requests/responses
- Postman collections
- OpenAPI specifications
- GraphQL schemas

#### Data Samples
- CSV files showing data structure
- JSON examples
- Database exports
- Excel templates

#### Original Code
- Legacy implementations to modernize
- Business logic to preserve
- Algorithms to port
- Configuration files

## When This Context Loads
- User mentions: "example", "mockup", "sample", "resource", "upload"
- User provides files or asks where to put them
- Discussion involves UI/UX design
- API structure being defined
- Data format discussions
- User has existing materials to share