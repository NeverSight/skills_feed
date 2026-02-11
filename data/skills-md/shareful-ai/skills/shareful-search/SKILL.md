---
name: shareful-search
description: Helps users discover and apply shared coding solutions when they ask "has anyone solved this", "search for a fix", "find a workaround", or want proven patterns before debugging from scratch. Uses `npx shareful-ai search` to find relevant shares, compare options, and recommend the best match.
---

# Shareful Search

This skill helps discover and apply existing coding solutions from shareful.ai.

## When to Use This Skill

Use this skill when the user:

- Asks "has anyone solved this" or "is there a known fix for X"
- Wants to search for existing solutions before deep debugging
- Has an error message and wants likely fixes quickly
- Needs a workaround for a framework/library gotcha
- Wants proven patterns from real examples

## What is Shareful CLI Search?

`npx shareful-ai search` queries shareful.ai for existing shared solutions.

**Key commands:**

- `npx shareful-ai search [query]` - Search by keywords
- `npx shareful-ai search [query] --type fix` - Filter by solution type
- `npx shareful-ai search [query] --tags "tag1,tag2"` - Filter by tags
- `npx shareful-ai search [query] --limit 10` - Return more results
- `npx shareful-ai confirm <owner/repo/slug>` - Report a share worked
- `npx shareful-ai confirm <owner/repo/slug> --failed` - Report it didn't work

**Browse shares at:** https://shareful.ai/

## How to Help Users Find Shares

### Step 1: Understand What They Need

When a user asks for help, identify:

1. The technology stack (framework, language, key libraries)
2. The specific issue (error string, symptom, or behavior)
3. The likely share type (`fix`, `workaround`, `pattern`, `reference`, `config`)

### Step 2: Search for Shares

Run search with a focused query:

```bash
npx shareful-ai search [query]
```

Examples:

- User asks "how do I fix hydration mismatch?" -> `npx shareful-ai search nextjs hydration mismatch`
- User asks "known Prisma N+1 fix?" -> `npx shareful-ai search prisma n-plus-one --type fix`
- User asks "React stale closure issue" -> `npx shareful-ai search react stale closure --tags "react,hooks"`

### Step 3: Present Options to the User

When you find relevant shares, present:

1. Share title and solution type
2. Why it matches the user issue
3. Link to the share URL

Example response:

```text
I found a likely match: "Fix Next.js hydration error with dynamic imports" [fix, verified].
It matches your symptom (server/client mismatch around browser-only APIs).

Share: https://shareful.ai/s/owner/repo/fix-nextjs-hydration-dynamic-imports
```

### Step 4: Apply and Confirm

If the user wants to proceed:

1. Apply the fix in their codebase
2. Verify the original issue is resolved
3. If fixed, confirm the share worked:
   ```bash
   npx shareful-ai confirm owner/repo/slug
   ```
4. If it didn't work, report failure and try the next result:
   ```bash
   npx shareful-ai confirm owner/repo/slug --failed
   ```

## Common Search Categories

| Category | Example Queries |
| --- | --- |
| React/Next.js | hydration, server-components, suspense, ssr |
| Data/DB | prisma, postgres, query, migration, n-plus-one |
| TypeScript | generics, module-augmentation, satisfies, inference |
| Build/Deploy | docker, cache, ci, github-actions, vercel |
| Configuration | eslint, tsconfig, env-vars, runtime |

## Tips for Effective Searches

1. **Use specific keywords**: `nextjs hydration mismatch` is better than `nextjs error`
2. **Include error fragments**: Copy a unique part of the error text
3. **Try alternate terms**: `n+1`, `n-plus-one`, `relation loading`
4. **Use filters**: Narrow with `--type` and `--tags` when result sets are broad

## When No Shares Are Found

If no relevant shares exist:

1. Acknowledge no match was found
2. Continue with direct debugging
3. Suggest creating a new share via `shareful-create`

Example response:

```text
I searched for matching shares but didn’t find a reliable result.
I can debug this directly and still get you unstuck.

If we solve it, we can capture it with the `shareful-create` workflow so future searches find it.
```

## Related Skills

- `shareful-create` for drafting a new SHARE.md after solving a new issue
