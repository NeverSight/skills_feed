---
name: code-reviewer
description: Review code for best practices, security issues, and potential bugs. Use when reviewing code changes, checking PRs, analyzing code quality, or performing security audits.
allowed-tools: Read, Grep, Glob
---

# Code Reviewer

Perform comprehensive code reviews focusing on quality, security, and maintainability.

## Instructions

1. Read the target files using the Read tool
2. Search for patterns and related code using Grep
3. Find related files using Glob
4. Analyze code against the review checklist
5. Provide structured feedback with severity levels

## Review Checklist

### Code Quality
- [ ] Code is simple and readable
- [ ] Functions and variables are well-named
- [ ] No duplicated code (DRY principle)
- [ ] Appropriate comments for complex logic
- [ ] Consistent code style

### Security
- [ ] No exposed secrets or API keys
- [ ] Input validation implemented
- [ ] SQL injection prevention
- [ ] XSS prevention for web code
- [ ] Proper authentication/authorization checks

### Error Handling
- [ ] Errors are caught and handled appropriately
- [ ] Meaningful error messages
- [ ] No silent failures
- [ ] Proper logging for debugging

### Performance
- [ ] No obvious performance bottlenecks
- [ ] Efficient algorithms and data structures
- [ ] Appropriate caching where needed
- [ ] Database queries are optimized

### Testing
- [ ] Adequate test coverage
- [ ] Edge cases are tested
- [ ] Tests are readable and maintainable

## Output Format

Organize feedback by severity:

### Critical (Must Fix)
Issues that could cause security vulnerabilities, data loss, or crashes.

### Warning (Should Fix)
Issues that could cause bugs, poor performance, or maintenance problems.

### Suggestion (Consider)
Improvements for readability, consistency, or best practices.

## Example Feedback

```markdown
### Critical
- **SQL Injection vulnerability** in `user_service.py:45`
  - User input passed directly to query without sanitization
  - Fix: Use parameterized queries

### Warning
- **Missing error handling** in `api_client.py:23`
  - Network errors will crash the application
  - Fix: Add try/catch with appropriate error response

### Suggestion
- Consider extracting the validation logic in `validators.py:78-95` into a separate function for reusability
```
