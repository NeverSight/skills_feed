---
name: vibe
description: Analyze your project and get personalized recommendations for Claude Code skills, MCP servers, and plugins
---

# vibe

Analyze your project and get personalized recommendations for Claude Code skills, MCP servers, and plugins from [Vibe Index](https://vibeindex.ai).

**No setup required!** Just install and use.

## Commands

### /vibe
Analyze your project and recommend matching resources.

```
/vibe
```

### /vibe search <query>
Search for resources by keyword.

```
/vibe search git
/vibe search database mcp
```

### /vibe top [type]
Show top resources by stars.

```
/vibe top
/vibe top skill
/vibe top mcp
```

### /vibe trending
Show trending resources this week.

```
/vibe trending
```

---

## How It Works

When the user runs `/vibe`, follow these steps:

### Step 1: Analyze Project Context

Read the following files to understand the project:

1. **package.json** - Extract dependencies
2. **File structure** (use Glob)
   - `*.py` → Python
   - `*.go` → Go
   - `*.tsx/*.jsx` → React
   - `Dockerfile` → Docker
   - `supabase/` → Supabase
   - `prisma/` → Prisma
3. **Configuration files**
   - `tsconfig.json` → TypeScript
   - `tailwind.config.*` → Tailwind
   - `next.config.*` → Next.js
   - `.github/workflows/` → GitHub Actions

### Step 2: Search for Matching Resources

**Use WebFetch to call Vibe Index API directly:**

```
WebFetch({
  url: "https://vibeindex.ai/api/resources?search=supabase&pageSize=5",
  prompt: "Extract resource names, types, descriptions, stars, and install commands"
})
```

| Detected | Search URL |
|----------|------------|
| React | `https://vibeindex.ai/api/resources?search=react&pageSize=5` |
| TypeScript | `https://vibeindex.ai/api/resources?search=typescript&pageSize=5` |
| Supabase | `https://vibeindex.ai/api/resources?search=supabase&pageSize=5` |
| Docker | `https://vibeindex.ai/api/resources?search=docker&pageSize=5` |
| Next.js | `https://vibeindex.ai/api/resources?search=nextjs&pageSize=5` |
| Python | `https://vibeindex.ai/api/resources?search=python&pageSize=5` |

### Step 3: Calculate Match Probability

```
Base Score:
- Direct dependency match: +40%
- File type match: +25%
- Config file match: +20%
- Tag overlap: +15%

Bonuses:
- High stars (>10k): +5%
- Multiple matches: +5% per additional

Maximum: 99%
```

### Step 4: Present Results

```markdown
## Suggested for Your Project

Based on analysis:
- Framework: Next.js + React + TypeScript
- Database: Supabase

---

### 1. supabase-mcp (mcp)
**Match: 95%** - @supabase/supabase-js detected

Supabase MCP server for database operations with Row Level Security support.

Stars: 6,616 | Install: See https://vibeindex.ai/mcp/supabase/supabase-community/supabase-mcp

---

### 2. react-best-practices (skill)
**Match: 88%** - react detected in dependencies

Best practices for React development.

Stars: 12,345 | Install: `npx skills add owner/repo --skill react-best-practices`
```

---

## API Reference

All endpoints are public and require no authentication:

| Command | API Endpoint |
|---------|-------------|
| `/vibe search <query>` | `https://vibeindex.ai/api/resources?search={query}&pageSize=10` |
| `/vibe top` | `https://vibeindex.ai/api/resources?sort=stars&pageSize=10` |
| `/vibe top skill` | `https://vibeindex.ai/api/resources?sort=stars&type=skill&pageSize=10` |
| `/vibe trending` | `https://vibeindex.ai/api/rising-stars?period=week&limit=10` |
| `/vibe stats` | `https://vibeindex.ai/api/stats` |

### Response Format

The API returns JSON with this structure:
```json
{
  "data": [
    {
      "name": "resource-name",
      "resource_type": "skill|mcp|plugin|marketplace",
      "description": "...",
      "description_ko": "...",
      "stars": 12345,
      "github_owner": "owner",
      "github_repo": "repo",
      "tags": ["tag1", "tag2"]
    }
  ],
  "total": 100
}
```

### Install Commands by Type

Generate install commands based on resource type:

- **skill**: `npx skills add {github_owner}/{github_repo} --skill {name}`
- **plugin**: Link to `https://vibeindex.ai/plugins/{github_owner}/{github_repo}/{name}`
- **mcp**: Link to `https://vibeindex.ai/mcp/{github_owner}/{github_repo}/{name}`
- **marketplace**: Link to `https://vibeindex.ai/marketplaces/{github_owner}/{github_repo}`

---

## Examples

### /vibe search git
```
WebFetch({
  url: "https://vibeindex.ai/api/resources?search=git&pageSize=10",
  prompt: "List the resources with name, type, description, stars. Format as markdown list."
})
```

### /vibe top mcp
```
WebFetch({
  url: "https://vibeindex.ai/api/resources?sort=stars&type=mcp&pageSize=10",
  prompt: "List top MCP servers with name, description, stars. Format as numbered list."
})
```

### /vibe trending
```
WebFetch({
  url: "https://vibeindex.ai/api/rising-stars?period=week&limit=10",
  prompt: "Show trending resources with star growth this week."
})
```

---

Built by [Vibe Index](https://vibeindex.ai) - The Claude Code Ecosystem Directory
