---
name: vibe-coding-setup
description: Set up a complete vibe coding workflow with Claude Code after migrating from a platform. Covers Supabase MCP, Netlify MCP, Vercel, API keys, GitHub, and decision framework for when to stay vs migrate. Use when users want to set up MCPs, connect hosting/database, or start a new project with the "all-in-one" experience in Claude Code.
license: MIT
metadata:
  author: CarolMonroe22
  version: "1.0.0"
  tags:
    - claude-code
    - mcp
    - netlify
    - supabase
    - vibe-coding
---

# Vibe Coding Setup with Claude Code

Set up a complete vibe coding workflow with Claude Code after migrating from an all-in-one platform (Lovable, Replit, Bolt, etc.).

## When to Use This Skill

- User is migrating from a platform to Claude Code
- User wants to set up MCPs for their project
- User needs to connect hosting, database, and API keys
- User is starting a new project and wants the "all-in-one" experience with Claude Code

## Setup Checklist

### 1. Supabase MCP (Database + Auth + Storage)

Add to your Claude Code MCP config (`~/.claude/mcp.json` or project `.mcp.json`):

```json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": ["-y", "@supabase/mcp-server-supabase@latest", "--project-ref", "YOUR-PROJECT-ID"]
    }
  }
}
```

This gives Claude Code access to:
- List and query tables
- Run SQL and migrations
- Manage edge functions
- Generate TypeScript types

Note: It doesn't have to be Supabase — Claude Code can connect to any Postgres database via the generic Postgres MCP.

### 2. Netlify MCP (Hosting + Deploys)

```json
{
  "mcpServers": {
    "netlify": {
      "command": "npx",
      "args": ["-y", "@netlify/mcp"],
      "env": {
        "NETLIFY_PERSONAL_ACCESS_TOKEN": "your-token"
      }
    }
  }
}
```

Get your token at: https://app.netlify.com/user/applications#personal-access-tokens

This gives Claude Code access to:
- Create and deploy sites
- Check build logs
- Manage environment variables
- Preview deploys

### 3. Vercel MCP (Alternative Hosting)

Vercel uses a remote MCP endpoint with OAuth:

```json
{
  "mcpServers": {
    "vercel": {
      "url": "https://mcp.vercel.com"
    }
  }
}
```

Currently read-only: logs, docs, project metadata. Useful for debugging.

### 4. API Keys

Add to your shell config (`~/.zshrc` or `~/.bashrc`):

```bash
export OPENAI_API_KEY="sk-..."
export GOOGLE_AI_API_KEY="..."
export ANTHROPIC_API_KEY="..."
```

Or use a `.env` file in your project (add to `.gitignore`).

### 5. GitHub

```bash
git clone your-repo
cd your-repo
claude
```

Claude Code works directly with your local files and can use git commands.

### 6. Additional MCPs (Optional)

| MCP | Purpose | Package |
|-----|---------|---------|
| Postgres | Direct DB access | `@modelcontextprotocol/server-postgres` |
| GitHub | Issues, PRs, repos | `@modelcontextprotocol/server-github` |
| Filesystem | File operations | `@modelcontextprotocol/server-filesystem` |
| Brave Search | Web search | `@modelcontextprotocol/server-brave-search` |

## Decision Framework

### Stay on the platform when:
- Just starting to vibe code or won't do it regularly
- Building something simple or prototyping
- Not comfortable with terminals
- Non-technical team needs to collaborate
- Need to ship fast without setup

### Migrate to Claude Code when:
- You hit platform limitations (auth, SQL, RLS)
- You need staging/production environments
- You want to combine multiple tools
- Your project outgrew the prototype phase

### The combo approach:
- Use a platform (Lovable) for UI and team collaboration
- Use Claude Code for backend, migrations, edge functions, precision work
- Best of both worlds

## Platform Equivalents

| Platform Feature | Claude Code Equivalent |
|-----------------|----------------------|
| One-click deploy | Netlify MCP |
| Database dashboard | Supabase MCP |
| Environment variables | `.env` + hosting MCP |
| Preview URLs | Netlify/Vercel deploys |
| AI chat | Claude Code itself |
| Auth setup | Supabase Auth |
| File storage | Supabase Storage |

## References

- [mcp-connections.md](references/mcp-connections.md) - Full MCP config examples
- [migration-checklist.md](references/migration-checklist.md) - Step-by-step migration guide
