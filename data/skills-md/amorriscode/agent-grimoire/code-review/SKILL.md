---
name: code-review
description: Perform thorough code reviews on pull requests, diffs, or code changes. Use when asked to review code, check a PR, or provide feedback on changes.
---

# Code Review

A structured approach to reviewing code changes.

## Instructions

When reviewing code, follow this process:

### 1. Understand the Context

Before diving into the code:
- Read the PR description or commit message
- Understand what problem is being solved
- Note any linked issues or requirements

### 2. Review in Passes

Make multiple passes through the code:

**First pass — Correctness**
- Does the code do what it claims to do?
- Are there logic errors or edge cases missed?
- Could this break existing functionality?

**Second pass — Security**
- Input validation present where needed?
- No hardcoded secrets or credentials?
- SQL injection, XSS, or other OWASP top 10 risks?

**Third pass — Maintainability**
- Is the code readable and well-organized?
- Are names clear and consistent?
- Is complexity justified?

**Fourth pass — Performance**
- Any obvious inefficiencies (N+1 queries, unnecessary loops)?
- Appropriate data structures used?
- Resource cleanup handled?

### 3. Provide Feedback

Structure your review:

```markdown
## Summary
[One sentence overall assessment]

## What's Good
- [Positive observations]

## Suggestions
- [Actionable improvements, ordered by importance]

## Questions
- [Clarifying questions if any]
```

### 4. Severity Levels

Categorize issues:
- **Blocker** — Must fix before merge (bugs, security issues)
- **Should fix** — Important but not blocking
- **Nitpick** — Style preferences, minor suggestions

## Examples

### Example Review Output

```markdown
## Summary
Solid implementation of user authentication. One security issue needs addressing before merge.

## What's Good
- Clean separation of auth logic from route handlers
- Good use of bcrypt for password hashing
- Comprehensive error handling

## Suggestions
1. **[Blocker]** Line 45: Password reset token should use `crypto.randomBytes(32)` instead of `Math.random()` — predictable tokens are a security risk
2. **[Should fix]** Line 78: Consider adding rate limiting to prevent brute force attempts
3. **[Nitpick]** Line 12: Typo in variable name `authetication` → `authentication`

## Questions
- Is there a reason we're storing sessions in memory rather than Redis? This won't scale across multiple instances.
```
