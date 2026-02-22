---
name: code-review
description: Code review checklists, PR review patterns, and feedback templates. Use when user asks to "review this code", "code review checklist", "PR review template", "review best practices", "write review feedback", or any code review tasks.
---

# Code Review

Checklists, patterns, and feedback templates for effective code reviews.

## Quick Review Checklist

```
Correctness
[ ] Does the code do what it's supposed to?
[ ] Are edge cases handled?
[ ] Are error conditions handled gracefully?
[ ] Are there any off-by-one errors?
[ ] Are null/undefined cases handled?

Security
[ ] No hardcoded secrets, keys, or passwords
[ ] Input validation on all user data
[ ] No SQL injection, XSS, or command injection
[ ] Authentication/authorization checks in place
[ ] Sensitive data not logged or exposed

Performance
[ ] No unnecessary database queries (N+1)
[ ] No memory leaks (event listeners, timers)
[ ] Large lists paginated, not loaded entirely
[ ] Expensive operations cached when appropriate
[ ] No blocking operations on main thread

Maintainability
[ ] Code is readable without extensive comments
[ ] Functions do one thing (single responsibility)
[ ] No duplicated logic (DRY where it makes sense)
[ ] Consistent naming conventions
[ ] No dead code or unused imports

Testing
[ ] Tests cover the main scenarios
[ ] Edge cases tested
[ ] Error paths tested
[ ] Tests are readable and maintainable
[ ] No flaky tests introduced
```

## PR Review Template

```markdown
## Review Summary

**Status**: Approve / Request Changes / Comment

### What I Reviewed
- [Brief description of what you looked at]

### Feedback

#### Must Fix
- [ ] Item 1 (link to code)
- [ ] Item 2 (link to code)

#### Suggestions
- [ ] Consider extracting X into a helper
- [ ] Could simplify with Y pattern

#### Praise
- Great error handling in the auth module
- Nice test coverage for edge cases
```

## Feedback Patterns

### Constructive Feedback

```
Instead of: "This is wrong"
Say: "This might cause issues when X because Y. Consider Z instead."

Instead of: "Why did you do it this way?"
Say: "I'm curious about the reasoning for this approach. Have you considered X?"

Instead of: "This is bad code"
Say: "This could be simplified by [specific suggestion]"
```

### Prefixed Comments

```
[nit] Minor style issue, take or leave
[suggestion] Optional improvement idea
[question] Seeking understanding, not necessarily a change
[issue] Must be addressed before merge
[praise] Something done well
[thought] Just sharing a perspective
```

### Common Review Comments

```markdown
**Missing error handling**
> What happens if `fetchUser()` throws? Consider wrapping in try/catch
> or adding `.catch()` to handle the error case.

**Potential null reference**
> `user.name` could throw if `user` is null. Consider optional chaining:
> `user?.name` or add a null check.

**N+1 query**
> This queries the database inside a loop. Consider using a batch query
> or `WHERE IN` clause to fetch all records at once.

**Race condition**
> If two requests hit this endpoint simultaneously, they could both
> read the same value before either writes. Consider using a transaction
> or optimistic locking.

**Security concern**
> User input is passed directly to the SQL query. Use parameterized
> queries to prevent SQL injection.

**Test coverage gap**
> The error path isn't tested. Consider adding a test for when
> the API returns a 500 error.
```

## Review by Language

### JavaScript/TypeScript

```
[ ] Using === not == for comparisons
[ ] Promises properly awaited (no floating promises)
[ ] Types are specific (not `any`)
[ ] useEffect dependencies correct (React)
[ ] No unnecessary re-renders (React)
[ ] Event listeners cleaned up
[ ] Error boundaries for UI components
```

### Python

```
[ ] Type hints on public functions
[ ] Context managers for resources (with statement)
[ ] No mutable default arguments
[ ] Exception handling is specific (not bare except)
[ ] f-strings used consistently
[ ] Generator used for large sequences
[ ] __init__.py exports are intentional
```

### SQL

```
[ ] Parameterized queries (no string interpolation)
[ ] Indexes exist for WHERE/JOIN columns
[ ] Migrations are reversible
[ ] No SELECT * in production queries
[ ] Transactions used for multi-statement operations
[ ] LIMIT on queries that could return many rows
```

## PR Size Guidelines

```
Small PR (< 200 lines)  → Review in 15-30 min
Medium PR (200-500)      → Review in 30-60 min
Large PR (500-1000)      → Consider splitting
Very Large PR (> 1000)   → Should almost always be split

Tips for smaller PRs:
- Separate refactoring from feature changes
- Split infrastructure from business logic
- Extract migrations into their own PR
- Send tests in same PR as code (not separate)
```

## Review Workflow

```
1. Read the PR description and linked issue
2. Understand the context (what problem does this solve?)
3. Review the test files first (understand expected behavior)
4. Review the main changes
5. Check for:
   - Correctness
   - Edge cases
   - Security
   - Performance
   - Readability
6. Run the code locally if needed
7. Leave feedback using prefixed comments
8. Summarize with overall assessment
```

## Reference

For language-specific checklists: `references/checklists.md`
