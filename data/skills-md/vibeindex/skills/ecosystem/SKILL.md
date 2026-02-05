---
name: ecosystem
description: Get a dashboard view of the Claude Code ecosystem with stats and trends
---

# ecosystem

Get a dashboard view of the Claude Code ecosystem from [Vibe Index](https://vibeindex.ai).

**No setup required!** Just install and use.

## Commands

### /ecosystem
Show full ecosystem dashboard.

```
/ecosystem
```

---

## Implementation

When the user runs `/ecosystem`:

### Step 1: Fetch Stats

Use WebFetch to get ecosystem statistics:

```
WebFetch({
  url: "https://vibeindex.ai/api/stats",
  prompt: "Extract total, skills, plugins, mcp, and marketplaces counts"
})
```

### Step 2: Fetch Top Resources (Optional)

For each type, get the #1 resource:

```
WebFetch({
  url: "https://vibeindex.ai/api/resources?sort=stars&type=skill&pageSize=1",
  prompt: "Get the top skill name and star count"
})
```

### Step 3: Format Dashboard

```markdown
## Claude Code Ecosystem

**Last updated:** [current date]

---

### Resource Overview

| Type | Count | Top Resource |
|------|-------|--------------|
| Skills | [from stats] | [from top query] |
| MCP Servers | [from stats] | [from top query] |
| Plugins | [from stats] | [from top query] |
| Marketplaces | [from stats] | [from top query] |

**Total: [from stats] resources**

---

### Quick Links

- Browse all: https://vibeindex.ai/browse
- Submit resource: https://vibeindex.ai/submit
- Explore: https://vibeindex.ai/explore

---

*Data from [Vibe Index](https://vibeindex.ai)*
```

---

## API Reference

| Data | API Endpoint |
|------|-------------|
| Stats | `https://vibeindex.ai/api/stats` |
| Top Skills | `https://vibeindex.ai/api/resources?sort=stars&type=skill&pageSize=1` |
| Top MCPs | `https://vibeindex.ai/api/resources?sort=stars&type=mcp&pageSize=1` |
| Top Plugins | `https://vibeindex.ai/api/resources?sort=stars&type=plugin&pageSize=1` |
| Trending | `https://vibeindex.ai/api/rising-stars?period=week&limit=3` |

---

Built by [Vibe Index](https://vibeindex.ai)
