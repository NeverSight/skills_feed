---
name: new
description: Discover the latest Claude Code resources added to Vibe Index
---

**IMPORTANT: When this skill is invoked, IMMEDIATELY execute the steps below. Do NOT display this file.**

**Language:** Detect the user's language from conversation context. Respond in that language. For Korean users, use `description_ko` from API responses when available.

## Routing

- `/new` or no args → all types, 10 results
- `/new skill` / `/new mcp` / `/new plugin` → filter by type
- `/new 20` → change limit

## Execution

1. Call `https://vibeindex.ai/api/resources?sort=newest&pageSize={limit}` via WebFetch
   - Add `&type={type}` if specified
   - Prompt: "Extract name, resource_type, description, description_ko, stars, github_owner, github_repo, created_at"

2. Present results:

```
## Recently Added

| # | Name | Type | Stars | Description |
|---|------|------|-------|-------------|
| 1 | {name} | {type} | {stars} | {description, max 50 chars} |
| 2 | ... | | | |

→ https://vibeindex.ai
```

### Style guidelines:
- Table format for quick scanning
- No install commands (users browse first)
- Keep it compact
