# MCP Server Integration Guide

**Model Context Protocol (MCP)** extends Claude's capabilities with external tools and data sources.

## Quick Setup

1. **Copy the template**:
   ```bash
   cp ai_framework/templates/mcp.json.template .claude/mcp.json
   ```

2. **Edit `.claude/mcp.json`** to add servers for your project

3. **Restart Claude Code** to load the new servers

## Common MCP Servers

### Filesystem Access
```json
{
  "filesystem": {
    "command": "npx",
    "args": ["-y", "@anthropic/mcp-filesystem@latest", "/path/to/directory"]
  }
}
```

### GitHub Integration
```json
{
  "github": {
    "command": "npx",
    "args": ["-y", "@anthropic/mcp-github@latest"],
    "env": {
      "GITHUB_TOKEN": "${GITHUB_TOKEN}"
    }
  }
}
```

### PostgreSQL Database
```json
{
  "postgres": {
    "command": "npx",
    "args": ["-y", "@anthropic/mcp-postgres@latest"],
    "env": {
      "DATABASE_URL": "${DATABASE_URL}"
    }
  }
}
```

### SQLite Database
```json
{
  "sqlite": {
    "command": "npx",
    "args": ["-y", "@anthropic/mcp-sqlite@latest", "/path/to/database.db"]
  }
}
```

### Web Search (Brave)
```json
{
  "brave-search": {
    "command": "npx",
    "args": ["-y", "@anthropic/mcp-brave-search@latest"],
    "env": {
      "BRAVE_API_KEY": "${BRAVE_API_KEY}"
    }
  }
}
```

### Memory/Notes
```json
{
  "memory": {
    "command": "npx",
    "args": ["-y", "@anthropic/mcp-memory@latest"]
  }
}
```

## Environment Variables

MCP servers can use environment variables for sensitive data:

```json
{
  "env": {
    "API_KEY": "${API_KEY}"
  }
}
```

Set these in your shell or `.env` file (not committed to git).

## Hegemon Integration

### Recommended Servers for Development

| Server | Use Case |
|--------|----------|
| `filesystem` | Access project specs, PRDs, and docs |
| `github` | PR reviews, issue tracking |
| `postgres/sqlite` | Database schema exploration |
| `memory` | Persistent context between sessions |

### Example: Full Stack Project

```json
{
  "mcpServers": {
    "project-docs": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-filesystem@latest", "./ai_project"],
      "description": "Access to project specs and requirements"
    },
    "database": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-postgres@latest"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      },
      "description": "Database schema access"
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-github@latest"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      },
      "description": "GitHub integration for PRs and issues"
    }
  }
}
```

## Security Considerations

1. **Review permissions** - MCP servers have access to external resources
2. **Use environment variables** - Never hardcode API keys or secrets
3. **Limit filesystem access** - Only expose directories that are needed
4. **Audit server sources** - Only use trusted MCP server packages

## Troubleshooting

### Server not loading
- Check that the server is installed: `npx -y @anthropic/mcp-<name>@latest --help`
- Verify JSON syntax in `.claude/mcp.json`
- Restart Claude Code after changes

### Environment variables not working
- Ensure variables are exported in your shell
- Check variable names match exactly (case-sensitive)

### Permission errors
- Verify paths are accessible
- Check file/directory permissions

## Resources

- [MCP Documentation](https://modelcontextprotocol.io)
- [Available MCP Servers](https://github.com/modelcontextprotocol/servers)
- [Claude Code MCP Guide](https://docs.anthropic.com/claude-code/mcp)
