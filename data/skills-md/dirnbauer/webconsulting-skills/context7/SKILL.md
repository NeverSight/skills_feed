---
name: context7
description: Fetch up-to-date library documentation via Context7 REST API. Use when needing current API docs, framework patterns, or code examples for any library.
version: 1.0.0
triggers:
  - documentation
  - api
  - libraries
  - docs
  - context7
---

# Context7 Documentation Lookup Skill

Fetch current library documentation, API references, and code examples via the Context7 REST API.

## When to Use

Activate this skill when:
- User asks about library APIs or framework patterns
- Import statements suggest documentation needs: `import`, `require`, `from`
- Questions about specific library versions or migration
- Need for official documentation patterns vs generic solutions
- "How do I use X library?", "What's the API for Y?"

## Workflow

### Step 1: Search for Library ID

Always search first to get the correct library ID:

```bash
curl -s "https://context7.com/api/v1/search?q=library-name" | jq
```

Example output shows library IDs you can use:

```json
{
  "id": "/facebook/react",
  "name": "React",
  "snippets": 2135,
  "score": 79.4
}
```

### Step 2: Fetch Documentation

```bash
curl -s "https://context7.com/api/v1/docs?library=<library-id>&topic=<topic>&mode=<mode>" | jq
```

**Parameters:**
- `library`: Library ID from search results (e.g., `/facebook/react`)
- `topic`: Optional focus area (e.g., `hooks`, `routing`)
- `mode`: `code` (default) for API/examples, `info` for guides

**Examples:**

```bash
# Get React hooks documentation
curl -s "https://context7.com/api/v1/docs?library=/facebook/react&topic=hooks" | jq

# Get Next.js routing docs
curl -s "https://context7.com/api/v1/docs?library=/vercel/next.js&topic=routing" | jq

# Get conceptual guide (info mode)
curl -s "https://context7.com/api/v1/docs?library=/vercel/next.js&topic=app%20router&mode=info" | jq
```

### Step 3: Apply to User's Question

Use the returned documentation to:
1. Provide accurate, version-specific answers
2. Show official code patterns and examples
3. Reference correct API signatures
4. Include relevant caveats or deprecations

## Common Library IDs

| Library | ID |
|---------|-----|
| React | `/facebook/react` |
| Next.js | `/vercel/next.js` |
| Vue.js | `/vuejs/vue` |
| Prisma | `/prisma/prisma` |
| Laravel | `/laravel/laravel` |
| Symfony | `/symfony/symfony` |
| TYPO3 | `/typo3/typo3` |
| Tailwind CSS | `/tailwindlabs/tailwindcss` |
| TypeScript | `/microsoft/typescript` |

## Documentation Modes

| Mode | Use For |
|------|---------|
| `code` | API references, code examples, function signatures (default) |
| `info` | Conceptual guides, tutorials, architecture docs |

## Example Workflow

```bash
# User asks: "How do I use React hooks?"

# Step 1: Search for React
curl -s "https://context7.com/api/v1/search?q=react" | jq '.results[0]'
# Output shows: id: /facebook/react

# Step 2: Fetch hooks docs
curl -s "https://context7.com/api/v1/docs?library=/facebook/react&topic=hooks" | jq

# Step 3: Use the returned documentation to answer
```

## TYPO3 Documentation Lookup

For TYPO3-specific documentation:

```bash
# Search for TYPO3
curl -s "https://context7.com/api/v1/search?q=typo3" | jq

# Get DataHandler docs
curl -s "https://context7.com/api/v1/docs?library=/typo3/typo3&topic=DataHandler" | jq

# Get Fluid ViewHelper docs
curl -s "https://context7.com/api/v1/docs?library=/typo3/typo3&topic=ViewHelper" | jq
```

## Error Handling

If requests fail:
1. Verify `jq` and `curl` are installed
2. Check the library ID format (`/org/project`)
3. Try a broader topic or no topic filter
4. Try `info` mode if `code` returns nothing
5. Check network connectivity

## MCP Alternative

If you have the Context7 MCP server configured, you can use it directly:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@context7/mcp-server"]
    }
  }
}
```

## Notes

- **No persistent context overhead**: Uses REST API directly
- **API key optional**: Works without key, but rate-limited
- **Topic filtering**: Use specific topics for focused results
- **Search first**: Always search to find the correct library ID
- **Fresh data**: Results are not cached; each call fetches fresh data

---

## Credits & Attribution

This skill is based on the excellent work by
**[Netresearch DTT GmbH](https://www.netresearch.de/)**.

Original repository: https://github.com/netresearch/context7-skill

**Copyright (c) Netresearch DTT GmbH** - Methodology and best practices  
Adapted by webconsulting.at for this skill collection
