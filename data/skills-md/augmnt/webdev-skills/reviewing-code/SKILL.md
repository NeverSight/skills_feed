---
name: reviewing-code
description: Provides structured code review with prioritized feedback. Use when reviewing PRs, analyzing code quality, checking for bugs, or auditing changes. Triggers on "review this", "check this code", PR reviews, or code quality questions.
allowed-tools: Read, Grep, Glob
---

# Reviewing Code

Prioritized, actionable feedback. Assume good intent.

## Priority Levels

| Level | Prefix | Meaning |
|-------|--------|---------|
| Blocker | 🚨 | Must fix before merge |
| Suggestion | ⚠️ | Should consider |
| Nit | 💭 | Optional polish |
| Question | ❓ | Need clarification |
| Praise | ✨ | Done well |

## Checklist

### Blockers (Security & Correctness)
- [ ] No secrets/credentials in code
- [ ] User input validated/sanitized
- [ ] Auth checks present where needed
- [ ] Edge cases handled (null, empty, errors)
- [ ] No race conditions in async code

### High Priority (Performance & Logic)
- [ ] No N+1 queries
- [ ] Large lists paginated
- [ ] Expensive ops not in render loops
- [ ] Error handling appropriate

### Medium Priority (Maintainability)
- [ ] Functions have single responsibility
- [ ] No copy-paste duplication
- [ ] Naming is clear

## Output Format

```markdown
## Summary
[Approve / Request Changes / Discuss]

## 🚨 Blockers
- `file:line` - Issue and fix

## ⚠️ Suggestions
- `file:line` - Suggestion and why

## 💭 Nits
- `file:line` - Minor improvement

## ✨ Good Stuff
- What was done well
```

## Common Issues

**React**: Missing useEffect deps, state that should be derived, prop drilling
**TypeScript**: `any` types, missing null checks
**API**: Missing loading/error states, unbounded queries

For detailed React/hooks patterns and accessibility checks, see [REACT-PATTERNS.md](REACT-PATTERNS.md).
