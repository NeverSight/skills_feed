---
name: versus
description: Compare two Claude Code resources side-by-side with objective data and recommendations
---

# versus

Compare two Claude Code resources side-by-side from [Vibe Index](https://vibeindex.ai).

**No setup required!** Just install and use.

## Commands

### /versus <resource1> <resource2>
Compare two resources by name.

```
/versus postgres-mcp supabase-mcp
/versus react-best-practices nextjs-best-practices
```

---

## Implementation

When the user runs `/versus A B`:

### Step 1: Search for Both Resources

Use WebFetch to find each resource:

```
WebFetch({
  url: "https://vibeindex.ai/api/resources?search=postgres-mcp&pageSize=3",
  prompt: "Find the resource named postgres-mcp and extract name, type, description, stars, github_owner, github_repo"
})

WebFetch({
  url: "https://vibeindex.ai/api/resources?search=supabase-mcp&pageSize=3",
  prompt: "Find the resource named supabase-mcp and extract name, type, description, stars, github_owner, github_repo"
})
```

### Step 2: Analyze Project Context (Optional)

Read `package.json` and project structure to determine which resource fits better.

### Step 3: Generate Comparison

```markdown
## ⚔️ postgres-mcp vs supabase-mcp

|                | postgres-mcp | supabase-mcp |
|----------------|--------------|--------------|
| **Type**       | mcp          | mcp          |
| **Stars**      | 2,341 ⭐     | 6,616 ⭐     |
| **Focus**      | Raw SQL      | Supabase API |

### postgres-mcp
Direct PostgreSQL access with raw SQL execution. Best for:
- Custom PostgreSQL setups
- Complex SQL queries
- No ORM overhead

### supabase-mcp
Supabase-native with RLS, Auth, and Realtime. Best for:
- Supabase projects
- Row Level Security
- Auth integration

---

## 🎯 Recommendation for Your Project

**Detected:** `supabase/` directory, `@supabase/supabase-js` in package.json

→ **supabase-mcp** is the better fit for your project.

---

**More info:**
- https://vibeindex.ai/mcp/crystaldba/postgres-mcp/postgres-mcp
- https://vibeindex.ai/mcp/supabase/supabase-community/supabase-mcp
```

---

## API Reference

| Action | API Endpoint |
|--------|-------------|
| Search resource | `https://vibeindex.ai/api/resources?search={name}&pageSize=3` |

---

## Edge Cases

### No Match Found
```
Could not find "xyz" in Vibe Index.
Try searching: /vibe search xyz
Or browse: https://vibeindex.ai/browse
```

### Same Resource
```
Both names refer to the same resource!
Nothing to compare.
```

---

Built by [Vibe Index](https://vibeindex.ai)
