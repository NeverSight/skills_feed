---
name: code-review
description: >-
  Perform structured code reviews focusing on correctness, readability,
  security, and maintainability. Use this skill when reviewing pull requests,
  evaluating code changes, or establishing review standards for a team.
---

# Code Review

Perform structured, actionable code reviews.

## When to Use

- Reviewing a pull request or set of changes
- Evaluating code quality before merging
- Auditing a module for technical debt
- Establishing review standards or checklists

## Review Dimensions

Review code across these dimensions, in priority order:

### 1. Correctness

- Does the code do what it claims?
- Are edge cases handled? (null, empty, overflow, concurrency)
- Are error paths tested?
- Do tests cover the changed behavior?

### 2. Security

- Input validation at system boundaries
- No secrets in code (API keys, passwords, tokens)
- SQL/command injection prevention
- Proper authentication and authorization checks
- See `security-audit` skill for deeper analysis

### 3. Readability

- Clear naming (variables, functions, classes)
- Functions do one thing
- No deep nesting (max 3 levels)
- Comments explain "why", not "what"
- Consistent style with the surrounding codebase

### 4. Maintainability

- No unnecessary abstractions
- DRY without over-abstraction (rule of three)
- Dependencies are justified
- Breaking changes are flagged

### 5. Performance

- Only flag when there is a real concern (hot path, large data, N+1 queries)
- Do not micro-optimize unless the context demands it

## Review Output Format

Structure feedback as:

```markdown
## Review: <PR title or file>

### Must Fix
- [ ] **file.py:42** — [Correctness] Description of the issue and suggested fix

### Should Fix
- [ ] **file.py:78** — [Readability] Description and suggestion

### Consider
- [ ] **file.py:100** — [Performance] Optional improvement

### Positive
- file.py:15 — Good use of context manager for resource cleanup
```

**Severity levels:**

| Level | Meaning | Merge? |
|-------|---------|--------|
| Must Fix | Bug, security issue, or broken contract | Block |
| Should Fix | Significant readability/maintainability concern | Request changes |
| Consider | Optional improvement, style preference | Approve with comment |
| Positive | Good patterns worth highlighting | - |

## Guidelines

1. **Be specific** - Point to exact lines, suggest concrete alternatives
2. **Explain why** - "This could cause X because Y", not just "change this"
3. **Separate style from substance** - Automate style (linters); review logic manually
4. **Limit scope** - Review what changed, not the entire file (unless asked)
5. **Acknowledge good work** - Include at least one positive observation
6. **Propose, don't impose** - "Consider using X" not "You must use X" (unless it's a Must Fix)
