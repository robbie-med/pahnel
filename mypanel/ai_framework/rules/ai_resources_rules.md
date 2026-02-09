# Resources Directory - READ-ONLY Reference Pool

## CRITICAL RULE
**This entire directory is READ-ONLY. Never modify any files here. Only add to this dir if User asks you to explicitly, then upon success revoke your permission to avoid mistakes.**

## Purpose
Micro MCP resource pool containing all user-provided reference materials for the project.

## Directory Structure
```
/resources/
├── examples/        # Mockups, data samples, user-provided examples
│   ├── ui-mockups/
│   ├── api-samples/
│   ├── data-samples/
│   └── workflow-diagrams/
├── reference/       # Guides, docs, original code preservations
│   ├── original-code/
│   ├── style-guides/
│   ├── external-docs/
│   └── architecture/
└── assets/         # Images and files for use in project
    ├── images/
    ├── fonts/
    ├── templates/
    └── config-samples/
```

## Usage Rules
1. **READ ONLY** - Never edit, move, or delete
2. **Source of Truth** - Treat all content here as resources, but the PRD is your source of truth.
3. **User Uploads** - Only users add content here, or a model can add if specifically directed to add explicitly by the user.
4. **Copy Don't Move** - When implementing, copy from here to project directories for later revisit references
5. **Reference When Helpful** - Check here to see if materials will aid with user collaborations if the user doesn't reference it directly initially.

## During Development
- Check `/examples/` for user-provided mockups and samples, but check with user before acceptance as current
- Use `/reference/` for style guides and documentation, or if in need of docs ask user to add them here
- See if user wants you to pull from `/assets/` for project resources (logos, configs, etc.)
- Always preserve originals - work with copies in project directories