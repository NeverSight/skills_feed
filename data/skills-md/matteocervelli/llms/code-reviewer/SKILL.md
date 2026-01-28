---
name: code-reviewer
description: Review code for quality, security, and performance with comprehensive
  feedback.
allowed-tools: Read, Bash, Grep
---

# Code Reviewer Skill

## Purpose

This skill provides comprehensive code review guidance covering quality, security, performance, and style. It helps identify issues, suggest improvements, and ensure code meets project standards before committing.

## Activation

**On-demand via command:** `/review-code <file-path>`

Example:
```bash
/review-code src/tools/example/core.py
```

## When to Use

- Self-review before committing
- Refactoring existing code
- Security concerns arise
- Performance optimization needed
- Ensuring style guide compliance
- Code quality improvement
- Pre-pull request review

## Resources

### review-checklist.md
Comprehensive code review checklist covering:
- **Code Quality:** File organization, naming, type hints, docstrings, error handling
- **Testing:** Coverage, quality, edge cases
- **Performance:** Algorithm efficiency, memory usage, I/O optimization
- **Security:** Input validation, authentication, authorization, data protection
- **Style:** PEP 8 compliance, import organization, formatting

### security-patterns.md
Security best practices including:
- **OWASP Top 10:** Injection, authentication, XSS, etc.
- **Python-Specific Security:** eval() usage, pickle security, SQL injection
- **Best Practices:** Input validation patterns, secure authentication, data protection

## Provides

### Code Quality Feedback
- File size enforcement (500-line limit)
- Single responsibility principle adherence
- Type hint completeness
- Docstring quality (Google-style)
- Error handling patterns
- Naming convention compliance

### Security Vulnerability Detection
- Input validation issues
- SQL injection vulnerabilities
- XSS vulnerabilities
- Authentication/authorization flaws
- Sensitive data exposure
- Insecure dependencies

### Performance Optimization Suggestions
- Algorithm efficiency improvements
- Memory usage optimization
- I/O operation optimization
- Caching opportunities
- Database query optimization

### Refactoring Recommendations
- Code duplication removal
- Complexity reduction
- Design pattern applications
- Dependency injection improvements
- Interface clarity

### Style Guide Compliance Checks
- PEP 8 for Python
- Import organization
- Code formatting
- Comment quality
- Documentation completeness

## Usage Examples

### Example 1: Review Python Module

```bash
/review-code src/tools/doc_fetcher/core.py
```

**Provides feedback on:**
- Function complexity and size
- Type hints and docstrings
- Error handling
- Security concerns (if any)
- Performance bottlenecks
- Style violations

### Example 2: Security-Focused Review

```bash
/review-code src/api/authentication.py
```

**Focuses on:**
- Authentication patterns
- Password handling
- Session management
- Input validation
- Authorization checks
- Token security

### Example 3: Performance Review

```bash
/review-code src/processors/data_processor.py
```

**Analyzes:**
- Algorithm complexity
- Memory allocation
- I/O operations
- Caching strategy
- Database queries
- Batch processing opportunities

## Review Categories

### 1. Code Quality (⭐⭐⭐⭐⭐ Essential)

#### File Organization
- ✓ File size ≤ 500 lines
- ✓ Logical module structure
- ✓ Clear separation of concerns
- ✓ Appropriate file naming

#### Naming Conventions
- ✓ Descriptive variable names
- ✓ Clear function names (verb_noun pattern)
- ✓ Class names (PascalCase)
- ✓ Constants (UPPER_CASE)
- ✓ Private members (_prefix)

#### Type Hints
- ✓ All function parameters typed
- ✓ All return types specified
- ✓ Complex types properly annotated
- ✓ Optional types used correctly

#### Docstrings
- ✓ Google-style format
- ✓ Clear description
- ✓ Args documented
- ✓ Returns documented
- ✓ Raises documented

#### Error Handling
- ✓ Appropriate exception types
- ✓ Error messages clear
- ✓ No bare except clauses
- ✓ Cleanup in finally blocks

### 2. Testing (⭐⭐⭐⭐ Important)

#### Test Coverage
- ✓ 80%+ code coverage
- ✓ All public functions tested
- ✓ Edge cases covered
- ✓ Error paths tested

#### Test Quality
- ✓ Clear test names
- ✓ Arrange-Act-Assert pattern
- ✓ Independent tests
- ✓ Appropriate fixtures

### 3. Performance (⭐⭐⭐ Moderate)

#### Efficiency
- ✓ Optimal algorithm complexity
- ✓ No unnecessary loops
- ✓ Efficient data structures
- ✓ Batch operations where possible

#### Resource Usage
- ✓ Memory-efficient
- ✓ File handles closed
- ✓ Database connections managed
- ✓ No resource leaks

#### Optimization
- ✓ Caching implemented
- ✓ Lazy loading used
- ✓ Async for I/O operations
- ✓ Query optimization

### 4. Security (⭐⭐⭐⭐⭐ Critical)

#### Input Validation
- ✓ All inputs validated
- ✓ Type checking
- ✓ Range checking
- ✓ Sanitization

#### Authentication & Authorization
- ✓ Strong authentication
- ✓ Proper authorization
- ✓ Session management
- ✓ Token validation

#### Data Protection
- ✓ No secrets in code
- ✓ Sensitive data encrypted
- ✓ SQL parameterized
- ✓ Output encoding

#### OWASP Top 10
- ✓ Injection prevention
- ✓ Broken auth prevention
- ✓ XSS prevention
- ✓ Access control
- ✓ Security misconfiguration

### 5. Style (⭐⭐⭐ Moderate)

#### PEP 8 Compliance
- ✓ Line length ≤ 88 characters
- ✓ Indentation (4 spaces)
- ✓ Blank line usage
- ✓ Whitespace around operators

#### Import Organization
- ✓ Grouped (stdlib, third-party, local)
- ✓ Alphabetically sorted
- ✓ No unused imports
- ✓ Absolute imports preferred

#### Code Formatting
- ✓ Black-formatted
- ✓ Consistent style
- ✓ Readable layout
- ✓ Appropriate comments

## Review Output Format

```markdown
# Code Review: <file-path>

## Summary
[Brief overview of file purpose and key findings]

## Quality Score: X/10
[Overall quality score with justification]

## Critical Issues (Must Fix)
- [Issue 1 with location and recommendation]
- [Issue 2 with location and recommendation]

## Important Issues (Should Fix)
- [Issue 1 with location and recommendation]
- [Issue 2 with location and recommendation]

## Suggestions (Consider)
- [Suggestion 1 with rationale]
- [Suggestion 2 with rationale]

## Strengths
- [Positive aspect 1]
- [Positive aspect 2]

## Detailed Analysis

### Code Quality
[Detailed quality assessment]

### Security
[Security assessment and concerns]

### Performance
[Performance analysis]

### Testing
[Test coverage and quality]

### Style
[Style guide compliance]

## Recommendations
1. [Priority 1 recommendation]
2. [Priority 2 recommendation]
3. [Priority 3 recommendation]

## Next Steps
[Suggested actions for improvement]
```

## Best Practices

### Constructive Feedback
- Focus on code, not person
- Explain "why" behind suggestions
- Provide specific examples
- Offer alternative solutions
- Acknowledge good practices

### Priority Levels
- **Critical:** Security vulnerabilities, bugs, data loss
- **Important:** Poor performance, missing tests, unclear code
- **Suggestions:** Style improvements, refactoring opportunities

### Context Awareness
- Consider project stage (prototype vs. production)
- Respect project conventions
- Balance perfection with pragmatism
- Focus on impactful improvements

## Common Issues to Check

### Python-Specific
- [ ] Using eval() or exec() unsafely
- [ ] Mutable default arguments
- [ ] Catching Exception too broadly
- [ ] Not using context managers for resources
- [ ] String concatenation in loops
- [ ] Missing __init__.py in packages
- [ ] Incorrect use of class variables
- [ ] Not using generators for large datasets

### General Issues
- [ ] Magic numbers (use constants)
- [ ] Deeply nested code (>3 levels)
- [ ] Long functions (>50 lines)
- [ ] Duplicate code
- [ ] Unclear variable names
- [ ] Missing error handling
- [ ] No input validation
- [ ] Hard-coded credentials

## Integration with Development Workflow

### Pre-Commit Review
Use this skill before committing:
```bash
/review-code <file-you-modified>
```

### Pre-Pull Request Review
Review all changed files:
```bash
git diff --name-only main | xargs -I {} /review-code {}
```

### Refactoring Review
After refactoring, verify improvements:
```bash
/review-code <refactored-file>
```

## Notes

- **Guidance Only:** This skill provides review feedback and guidance. It does not automatically fix issues.
- **Comprehensive:** Reviews cover multiple dimensions (quality, security, performance, style).
- **Actionable:** Feedback includes specific recommendations and examples.
- **Project-Aware:** Considers project-specific standards and conventions.

## Used When

- Before committing changes
- During code refactoring
- When security review is needed
- For performance optimization
- To ensure style compliance
- Pre-pull request submission
- Learning best practices
- Mentoring code quality