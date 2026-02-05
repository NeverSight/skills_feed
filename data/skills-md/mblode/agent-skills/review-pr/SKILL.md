---
name: review-pr
description: High-signal PR review for bugs and CLAUDE.md compliance. Use before creating PRs or when reviewing changes.
---

# PR Review

Systematic PR review with actionable, validated feedback only.

## Scope
- Use before creating PRs or when reviewing existing PRs
- Skip trivial changes, drafts, and bot PRs

## Workflow

1. **Validate**: Skip if closed, already reviewed, or trivial
2. **Context**: Get PR intent, changed files, and relevant CLAUDE.md files
3. **Review** (4 parallel agents):
   - 2 agents: CLAUDE.md compliance (in-scope rules only, unambiguous violations)
   - 2 agents: Bugs (compile errors, logic errors, security issues)
4. **Validate issues**: Secondary agent verifies each flagged issue
5. **Post**: Inline comments with reasoning, or "No issues found" summary

## High signal only

Flag only when certain:
- Code will fail to compile (syntax, types, imports)
- Code will produce wrong results (clear logic errors)
- Unambiguous CLAUDE.md violation (quote rule, verify scope)

Never flag:
- Style, quality, or subjective preferences
- Pre-existing issues or linter-catchable problems
- Potential issues dependent on inputs
- Explicitly silenced violations

## Output format

**Inline comments** (use `mcp__github_inline_comment__create_inline_comment`):
- Issue description with reasoning
- Link to rule (CLAUDE.md) or code with full SHA: `https://github.com/owner/repo/blob/[40-char-sha]/file.ts#L4-L7`
- Committable suggestion for small fixes (< 6 lines); description for larger changes
- One comment per unique issue

**Summary** (if no issues):
```
## Code review
No issues found. Checked for bugs and CLAUDE.md compliance.
```

## Anti-patterns
- ❌ "This might cause issues" → ✅ "Variable `x` undefined at line 45, will throw ReferenceError"
- ❌ "Consider refactoring" → ✅ "Violates CLAUDE.md: 'Max 50 lines' (currently 67)"
- ❌ Multiple comments for same issue → ✅ One comment linking all locations

Every flagged issue should be something a senior engineer would catch.
