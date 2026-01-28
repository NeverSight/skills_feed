---
name: code-review
description: Performs comprehensive code reviews following industry best practices. Use when reviewing pull requests, code changes, or when asked to analyze code quality, security, performance, or maintainability. Checks for common bugs, security vulnerabilities, code smells, and adherence to coding standards.
license: MIT
metadata:
  author: agent-skills-demo
  version: "1.0"
  category: development
---

# Code Review Skill

## When to Use This Skill

Use this skill when:
- The user requests a code review or asks to review code
- A pull request needs to be examined
- Code quality, security, or performance analysis is needed
- The user mentions terms like "review", "check my code", "code quality", or "find bugs"

## Review Process

Follow this systematic approach for code reviews:

### 1. Initial Assessment
- Read through the entire code change to understand the intent
- Identify the type of change (bug fix, feature, refactor, etc.)
- Note the programming language and framework being used

### 2. Functionality Review
- Verify the code does what it's supposed to do
- Check for logical errors or edge cases
- Ensure error handling is appropriate
- Validate input/output handling

### 3. Security Analysis
Use the security checklist in [references/CHECKLIST.md](references/CHECKLIST.md):
- SQL injection vulnerabilities
- XSS (Cross-Site Scripting) risks
- Authentication and authorization issues
- Sensitive data exposure
- Insecure dependencies
- Command injection risks

### 4. Performance Review
- Identify potential bottlenecks
- Check for inefficient algorithms (O(n²) where O(n) is possible)
- Look for unnecessary database queries or API calls
- Review memory usage patterns
- Check for resource leaks

### 5. Code Quality
- Readability: Is the code easy to understand?
- Maintainability: Can it be easily modified?
- DRY principle: Avoid code duplication
- SOLID principles adherence
- Appropriate use of design patterns
- Proper naming conventions

### 6. Testing
- Are there adequate unit tests?
- Do tests cover edge cases?
- Are integration tests needed?
- Is test coverage sufficient?

## Output Format

Structure your review using the template in [assets/review-template.md](assets/review-template.md):

### Summary
Brief overview of the changes and overall assessment.

### Critical Issues 🔴
Issues that must be fixed (security vulnerabilities, breaking bugs).

### Important Issues 🟡
Significant concerns (performance problems, poor error handling).

### Suggestions 🟢
Nice-to-have improvements (refactoring opportunities, better naming).

### Positive Notes ✅
Call out well-written code and good practices.

## Common Patterns to Check

### Anti-patterns
- God classes (classes doing too much)
- Magic numbers (unexplained constants)
- Deep nesting (more than 3 levels)
- Long functions (more than 50 lines)
- Catch and ignore exceptions
- Hard-coded credentials or secrets

### Best Practices
- Single Responsibility Principle
- Meaningful variable names
- Consistent formatting
- Appropriate comments
- Proper error messages
- Logging important events

## Language-Specific Considerations

### Python
- PEP 8 compliance
- Type hints usage
- Context managers for resources
- List comprehensions vs loops
- Async/await usage

### JavaScript/TypeScript
- Const/let over var
- Async/await over callbacks
- Type safety (TypeScript)
- Proper promise handling
- Memory leak prevention

### Java
- Exception handling patterns
- Resource management (try-with-resources)
- Thread safety
- Collection usage
- Null safety

## Example Review

For code like this:
```python
def process_users(users):
    result = []
    for user in users:
        if user['active']:
            result.append(user['name'].upper())
    return result
```

Review output:
**🟡 Suggestions:**
- Use list comprehension for better readability and performance
- Add type hints for better code documentation
- Consider KeyError handling if 'active' or 'name' might be missing

**Improved version:**
```python
from typing import List, Dict, Any

def process_users(users: List[Dict[str, Any]]) -> List[str]:
    """Extract and uppercase names of active users."""
    return [
        user['name'].upper() 
        for user in users 
        if user.get('active', False)
    ]
```

## Tips for Effective Reviews

1. **Be constructive**: Frame feedback positively
2. **Be specific**: Point to exact lines and explain why
3. **Prioritize**: Distinguish between critical issues and suggestions
4. **Educate**: Explain the reasoning behind recommendations
5. **Acknowledge good work**: Highlight excellent code
6. **Be consistent**: Apply the same standards throughout

## When to Request Human Review

Some situations require human judgment:
- Major architectural decisions
- Trade-offs between conflicting requirements
- Business logic validation
- Regulatory compliance questions
- Significant performance optimizations
