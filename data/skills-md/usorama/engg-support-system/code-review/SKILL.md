---
name: code-review
description: Review code for quality, security, and best practices. Use for PR reviews, code quality checks, security audits, and pre-merge reviews.
allowed-tools: Read, Grep, Glob, Bash
---

# Code Review Skill

Systematic code review for quality, security, and maintainability.

## Review Checklist

### 1. Correctness

- [ ] Logic is correct
- [ ] Edge cases handled
- [ ] Error handling appropriate
- [ ] No obvious bugs

### 2. Security (OWASP Top 10)

- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] Input validation present
- [ ] No hardcoded secrets
- [ ] Authentication/authorization correct
- [ ] Sensitive data protected

### 3. Code Quality

- [ ] Code is readable
- [ ] Functions are focused (single responsibility)
- [ ] No code duplication (DRY)
- [ ] Naming is clear and consistent
- [ ] No magic numbers/strings
- [ ] Appropriate comments where needed

### 4. TypeScript Specifics

- [ ] No `any` types
- [ ] Proper type annotations
- [ ] Null/undefined handled
- [ ] Generics used appropriately

### 5. Performance

- [ ] No obvious performance issues
- [ ] No N+1 queries
- [ ] Appropriate caching
- [ ] Memory leaks avoided

### 6. Testing

- [ ] Tests exist for new code
- [ ] Tests are meaningful
- [ ] Edge cases tested
- [ ] Coverage maintained

## Output Format

### Critical (Must Fix)

Issues that must be fixed before merge.

```
CRITICAL: [file:line] - [Issue description]
  Code: `problematic code`
  Fix: [Suggested fix]
```

### Warnings (Should Fix)

Issues that should be addressed but don't block merge.

```
WARNING: [file:line] - [Issue description]
  Suggestion: [Improvement]
```

### Suggestions (Consider)

Nice-to-have improvements.

```
SUGGESTION: [file:line] - [Improvement idea]
```

### Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CODE REVIEW SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Files reviewed: X
Critical issues: X
Warnings: X
Suggestions: X

Verdict: [APPROVED / CHANGES REQUESTED]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
