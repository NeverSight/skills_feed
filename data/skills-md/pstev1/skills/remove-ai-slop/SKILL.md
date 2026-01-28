---
name: remove-ai-slop
description: Check the diff against master and remove all AI generated slop introduced in this branch. This includes extra comments, defensive checks, type casts, and inconsistent code style.
metadata:
  version: 1.0.0
---

# Remove AI Code Slop

## Workflow

1. Run `git diff master --name-only` to list changed files
2. For each file, run `git diff master -- <file>` to see changes
3. Read surrounding context in the original file to understand existing style
4. Remove slop patterns (see below)
5. Report a 1-3 sentence summary

## Slop Patterns to Remove

| Pattern | Example | Fix |
|---------|---------|-----|
| Redundant comments | `// Get the user` above `getUser()` | Delete |
| Obvious inline comments | `const x = 5; // set x to 5` | Delete |
| Defensive null checks | `if (x != null && x.y != null)` when caller already validates | Remove extra checks |
| Unnecessary try/catch | Wrapping code that can't throw or is already handled upstream | Unwrap |
| `as any` casts | `foo as any` to bypass types | Fix the type properly or remove |
| Verbose conditionals | `if (x === true)` | Simplify to `if (x)` |
| Empty catch blocks | `catch (e) {}` | Either handle or remove try/catch |
| Over-documented parameters | JSDoc repeating what types already say | Delete redundant docs |

## Style Consistency Rules

- Match existing brace style, spacing, and naming conventions in the file
- If file has no comments, don't add them
- If file uses terse variable names, don't expand them
- Preserve the file's existing level of defensive coding
