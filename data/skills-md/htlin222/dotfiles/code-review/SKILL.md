---
name: code-review
description: Expert code review for quality, security, and maintainability. Use after writing or modifying code, or when user asks for review.
---

# Code Review

Review code for quality, security, and maintainability with prioritized feedback.

## When to Use

- After writing or modifying code
- User asks "review this code" or "check my changes"
- Before committing significant changes
- When code quality concerns arise

## Review Process

1. Run `git diff` to see recent changes
2. Read modified files to understand context
3. Analyze against checklist below
4. Provide prioritized feedback

## Review Checklist

### Critical (Must Fix)

- Security vulnerabilities (exposed secrets, injection risks)
- Logic errors that cause incorrect behavior
- Missing error handling for critical paths
- Race conditions or data corruption risks

### Warnings (Should Fix)

- Code duplication that harms maintainability
- Missing input validation
- Poor error messages
- Performance issues in hot paths
- Missing or inadequate tests

### Suggestions (Consider)

- Naming improvements for clarity
- Simplification opportunities
- Better abstractions
- Documentation gaps

## Output Format

```markdown
## Code Review Summary

**Files Reviewed:** [list files]
**Overall Assessment:** [Good/Needs Work/Critical Issues]

### Critical Issues

- [file:line] Issue description → Fix suggestion

### Warnings

- [file:line] Issue description → Recommendation

### Suggestions

- [file:line] Improvement opportunity
```

## Examples

**Input:** "Review my changes"
**Action:** Run git diff, analyze changes, provide structured feedback

**Input:** "Check this function for issues"
**Action:** Read the function, check for bugs/security/quality, report findings
