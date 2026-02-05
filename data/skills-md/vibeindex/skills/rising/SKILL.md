---
name: rising
description: Discover trending Claude Code resources that are rising on GitHub right now
---

# rising

Discover trending Claude Code resources from [Vibe Index](https://vibeindex.ai).

**No setup required!** Just install and use.

## Commands

### /rising
Show resources trending this week.

```
/rising
```

### /rising day
Show resources trending today.

```
/rising day
```

### /rising month
Show resources trending this month.

```
/rising month
```

---

## Implementation

When the user runs `/rising [period]`:

### Fetch Trending Data

Use WebFetch to get trending resources:

```
WebFetch({
  url: "https://vibeindex.ai/api/rising-stars?period=week&limit=10",
  prompt: "List trending resources with name, type, star growth, total stars, and description"
})
```

### API Parameters

| Parameter | Values | Default |
|-----------|--------|---------|
| period | day, week, month | week |
| limit | 1-20 | 10 |

### Output Format

```markdown
## Trending This Week

Resources from Vibe Index currently rising on GitHub:

### #1 claude-code-toolkit (skill)
**+523 stars this week** | Total: 4,521 ⭐
Comprehensive toolkit for Claude Code development
→ `npx skills add owner/repo --skill claude-code-toolkit`

---

### #2 supabase-mcp (mcp)
**+312 stars this week** | Total: 6,616 ⭐
Supabase MCP server with RLS support
→ See https://vibeindex.ai/mcp/supabase/supabase-community/supabase-mcp

---

See full rankings: https://vibeindex.ai
```

---

## API Reference

| Command | API Endpoint |
|---------|-------------|
| `/rising` | `https://vibeindex.ai/api/rising-stars?period=week&limit=10` |
| `/rising day` | `https://vibeindex.ai/api/rising-stars?period=day&limit=10` |
| `/rising month` | `https://vibeindex.ai/api/rising-stars?period=month&limit=10` |

---

Built by [Vibe Index](https://vibeindex.ai)
