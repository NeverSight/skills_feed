---
name: code-review
description: Review code for quality, security vulnerabilities, and best practices compliance
---

# Code Review

Review code for quality, security issues, and best practices.

## Capabilities

- Identify bugs and potential issues
- Check for security vulnerabilities (OWASP top 10)
- Suggest performance improvements
- Verify coding standards compliance

## Checklist

1. Error handling - proper try/catch, edge cases
2. Security - input validation, injection prevention
3. Performance - unnecessary loops, memory leaks
4. Readability - naming, comments, structure

## Output Format

Returns structured feedback with:
- severity: critical | warning | info
- location: file:line
- message: description of the issue
- suggestion: how to fix
