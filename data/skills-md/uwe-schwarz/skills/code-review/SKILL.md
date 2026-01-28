---
name: code-review
description: Comprehensive code review guidelines for ensuring code quality, security, and maintainability. Use when reviewing pull requests, refactoring code, or ensuring best practices.
license: MIT
metadata:
  author: your-name
  version: "1.0.0"
---

# Code Review Skill

Guidelines for thorough and effective code reviews.

## When to Apply

Use these guidelines when:
- Reviewing pull requests
- Refactoring existing code
- Conducting code audits
- Ensuring code quality standards

## Review Categories

### 1. Code Quality

- Check for consistent code style
- Ensure proper error handling
- Verify meaningful variable and function names
- Look for code duplication

### 2. Security

- Check for SQL injection vulnerabilities
- Verify input validation and sanitization
- Review authentication and authorization logic
- Check for sensitive data exposure

### 3. Performance

- Identify potential performance bottlenecks
- Check for unnecessary database queries
- Review algorithm efficiency
- Look for memory leaks

### 4. Testing

- Verify test coverage
- Check test quality and relevance
- Ensure edge cases are covered
- Review mocking and fixtures

### 5. Documentation

- Check for code comments
- Verify README updates
- Review API documentation
- Ensure changelog is updated

## Review Process

1. **Initial Review**
   - Read through the changes
   - Understand the purpose
   - Identify major issues first

2. **Detailed Review**
   - Check each file
   - Verify logic and implementation
   - Test if necessary

3. **Final Review**
   - Summarize findings
   - Provide actionable feedback
   - Verify fixes if needed

## Best Practices

- Be constructive and respectful
- Explain the "why" behind comments
- Suggest improvements, not just problems
- Acknowledge good work
- Keep reviews timely
