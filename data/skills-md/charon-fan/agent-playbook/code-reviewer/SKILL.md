---
name: code-reviewer
description: Reviews pull requests and code changes for quality, security, and best practices. Use when user asks for code review, PR review, or mentions reviewing changes.
allowed-tools: Read, Grep, Glob, Bash, WebFetch, WebSearch
metadata:
  hooks:
    after_complete:
      - trigger: self-improving-agent
        mode: background
        reason: "Learn from review patterns"
      - trigger: session-logger
        mode: auto
        reason: "Log review activity"
---

# Code Reviewer

A comprehensive code review skill that analyzes pull requests and code changes for quality, security, maintainability, and best practices.

## When This Skill Activates

This skill activates when you:
- Ask for a code review
- Request a PR review
- Mention reviewing changes
- Say "review this" or "check this code"

## Review Process

### Phase 1: Context Gathering

1. **Get changed files**
   ```bash
   git diff main...HEAD --name-only
   git log main...HEAD --oneline
   ```

2. **Get the diff**
   ```bash
   git diff main...HEAD
   ```

3. **Understand project context**
   - Read relevant documentation
   - Check existing patterns in similar files
   - Identify project-specific conventions

### Phase 2: Analysis Categories

#### 1. Correctness
- [ ] Logic is sound and matches requirements
- [ ] Edge cases are handled
- [ ] Error handling is appropriate
- [ ] No obvious bugs or typos

#### 2. Security
- [ ] No hardcoded secrets or credentials
- [ ] Input validation and sanitization
- [ ] SQL injection prevention
- [ ] XSS prevention (for frontend)
- [ ] Authentication/authorization checks
- [ ] Safe handling of user data

#### 3. Performance
- [ ] No N+1 queries
- [ ] Appropriate caching
- [ ] Efficient algorithms
- [ ] No unnecessary computations
- [ ] Memory efficiency

#### 4. Code Quality
- [ ] Follows DRY principle
- [ ] Follows KISS principle
- [ ] Appropriate abstractions
- [ ] Clear naming conventions
- [ ] Proper typing (if TypeScript)
- [ ] No commented-out code

#### 5. Testing
- [ ] Tests cover new functionality
- [ ] Tests cover edge cases
- [ ] Test assertions are meaningful
- [ ] No brittle tests

#### 6. Documentation
- [ ] Complex logic is explained
- [ ] Public APIs have documentation
- [ ] JSDoc/TSDoc for functions
- [ ] README updated if needed

#### 7. Maintainability
- [ ] Code is readable
- [ ] Consistent style
- [ ] Modular design
- [ ] Separation of concerns

### Phase 3: Output Format

Use this structured format for review feedback:

```markdown
# Code Review

## Summary
Brief overview of the changes (2-3 sentences).

## Issues by Severity

### Critical
Must fix before merge.

- [ ] **Issue Title**: Description with file:line reference

### High
Should fix before merge unless there's a good reason.

- [ ] **Issue Title**: Description with file:line reference

### Medium
Consider fixing, can be done in follow-up.

- [ ] **Issue Title**: Description with file:line reference

### Low
Nice to have improvements.

- [ ] **Issue Title**: Description with file:line reference

## Positive Highlights
What was done well in this PR.

## Suggestions
Optional improvements that don't require immediate action.

## Approval Status
- [ ] Approved
- [ ] Approved with suggestions
- [ ] Request changes
```

## Common Issues to Check

### Security Issues

| Issue | Pattern | Recommendation |
|-------|----------|----------------|
| Hardcoded secrets | `const API_KEY = "sk-"` | Use environment variables |
| SQL injection | `\"SELECT * FROM...\" + user_input` | Use parameterized queries |
| XSS vulnerability | `innerHTML = user_input` | Sanitize or use textContent |
| Missing auth check | New endpoint without `@RequireAuth` | Add authentication middleware |

### Performance Issues

| Issue | Pattern | Recommendation |
|-------|----------|----------------|
| N+1 query | Loop with database call | Use eager loading or batch queries |
| Unnecessary re-render | Missing dependencies in `useEffect` | Fix dependency array |
| Memory leak | Event listener not removed | Add cleanup in useEffect return |
| Inefficient loop | Nested loops O(n²) | Consider hash map or different algorithm |

### Code Quality Issues

| Issue | Pattern | Recommendation |
|-------|----------|----------------|
| Duplicate code | Similar blocks repeated | Extract to function |
| Magic number | `if (status === 5)` | Use named constant |
| Long function | Function >50 lines | Split into smaller functions |
| Complex condition | `a && b || c && d` | Extract to variable with descriptive name |

### Testing Issues

| Issue | Pattern | Recommendation |
|-------|----------|----------------|
| No tests | New feature without test file | Add unit tests |
| Untested edge case | Test only covers happy path | Add edge case tests |
| Brittle test | Test relies on implementation details | Test behavior, not implementation |
| Missing assertion | Test doesn't assert anything | Add proper assertions |

## Language-Specific Guidelines

### TypeScript
- Use `unknown` instead of `any` for untyped values
- Prefer `interface` for public APIs, `type` for unions
- Use strict mode settings
- Avoid `as` assertions when possible

### React
- Follow Hooks rules
- Use `useCallback`/`useMemo` appropriately (not prematurely)
- Prefer function components
- Use proper key props in lists
- Avoid prop drilling with Context

### Python
- Follow PEP 8 style guide
- Use type hints
- Use f-strings for formatting
- Prefer list comprehensions over map/filter
- Use context managers for resources

### Go
- Handle errors explicitly
- Use named returns for clarity
- Keep goroutines simple
- Use channels for communication
- Avoid package-level state

## Before Approving

Confirm the following:
- [ ] All critical issues are addressed
- [ ] Tests pass locally
- [ ] No merge conflicts
- [ ] Commit messages are clear
- [ ] Documentation is updated
- [ ] Breaking changes are documented

## Scripts

Run the review checklist script:
```bash
python scripts/review_checklist.py <pr-number>
```

## References

- `references/checklist.md` - Complete review checklist
- `references/security.md` - Security review guidelines
- `references/patterns.md` - Common patterns and anti-patterns
