---
name: doc-search
description: Automatically activates when documentation lookup is needed. Routes to the optimal source (Sanity MCP, Context7, Ref, or WebSearch) based on the technology being queried.
---

# Smart Documentation Search

## Purpose

This skill automatically activates when you need to look up documentation, API references, or best practices. It intelligently routes to the best available source.

## When to Activate

Invoke this skill when the request involves:
- Looking up how to use a library/framework feature
- Finding API references or function signatures
- Searching for code examples or patterns
- Checking best practices or conventions
- Verifying correct usage before writing code

## Routing Logic (Priority Order)

### 1. Native MCP Tools (if available)

**Always check if a dedicated MCP server exists for the technology.** MCP tools provide the most accurate, integrated results.

| Technology | MCP Tools | Use For |
|------------|-----------|---------|
| Sanity | `mcp__Sanity__search_docs`, `mcp__Sanity__read_docs`, `mcp__Sanity__get_groq_specification`, `mcp__Sanity__get_sanity_rules` | Schemas, GROQ, Studio, Visual Editing |
| GitHub | `mcp__github__*` (if configured) | Repos, issues, PRs |
| Notion | `mcp__notion__*` (if configured) | Workspace docs |
| Other MCPs | Check available tools | Varies |

**How to detect:** If `mcp__[Technology]__` tools are available, use them first.

### 2. Context7 (Popular Libraries)

Use for well-indexed popular libraries. Context7 provides curated, high-quality code snippets.

```
Step 1: mcp__context7__resolve-library-id (get library ID)
Step 2: mcp__context7__get-library-docs (fetch docs)
```

**Pre-resolved Library IDs (skip Step 1 for these):**

| Technology | Context7 ID |
|------------|-------------|
| React Router | `/remix-run/react-router` |
| React | `/websites/react_dev` |
| Next.js | `/vercel/next.js` |
| Tailwind CSS | `/tailwindlabs/tailwindcss` |
| TypeScript | `/microsoft/typescript` |
| Prisma | `/prisma/prisma` |
| Zod | `/colinhacks/zod` |
| Vite | `/vitejs/vite` |
| Astro | `/withastro/astro` |
| tRPC | `/trpc/trpc` |
| Drizzle | `/drizzle-team/drizzle-orm` |
| shadcn/ui | `/shadcn-ui/ui` |

**Parameters:**
- `topic`: Focus the search (e.g., "loaders", "hooks", "validation")
- `mode`: "code" for API/examples, "info" for concepts/architecture

### 3. Ref (Broader Search)

Use for broader searches across multiple sources.

```
Step 1: mcp__Ref__ref_search_documentation (search)
Step 2: mcp__Ref__ref_read_url (read specific URLs)
```

**When to use:**
- Library not found in Context7
- Need to search private repositories (add `ref_src=private`)
- Looking for blog posts, tutorials, or discussions
- Obscure or niche libraries

### 4. WebSearch (Fallback)

Use `WebSearch` as last resort for:
- Very recent information (current year)
- Comparing multiple solutions
- Community discussions or Stack Overflow answers

## Decision Flowchart

```
Is there an MCP for this technology?
├─ YES → Use MCP tools
└─ NO → Is it a popular library?
         ├─ YES → Use Context7
         └─ NO/Not found → Use Ref
                           └─ Still not enough? → WebSearch
```

## Response Format

After retrieving documentation:

1. **Source**: Which tool was used and why
2. **Summary**: Concise answer to the query
3. **Code Examples**: Relevant snippets (if applicable)
4. **Links**: Source URLs for further reading

## Important Rules

- **NEVER guess** - always verify with documentation
- **Check MCP availability first** - most accurate source
- **Use topic parameter** in Context7 to focus results
- **Combine sources** when query spans multiple technologies
- **Cite sources** with URLs in your response
