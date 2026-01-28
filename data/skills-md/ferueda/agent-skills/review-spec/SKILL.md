---
name: review-spec
description: Review a spec document against codebase reality, identifying gaps and ensuring sound, robust implementations.
---

Review the given spec document by analyzing both the spec AND the referenced codebase.

## Process

1. **Read the spec** - Understand goals, phases, and proposed changes
2. **Explore the codebase** - Read files and code mentioned in the spec
3. **Analyze patterns** - Identify existing patterns, conventions, and architecture
4. **Validate the plan** - Ensure proposals align with codebase reality
5. **Identify issues** - Find gaps, risks, and improvement opportunities

## Review Dimensions

Evaluate across these areas (focus on what's relevant):

- **Architecture**: Component boundaries, data flow, API contracts, separation of concerns
- **Feasibility**: Implementation complexity, technology trade-offs, effort estimation
- **Reliability**: Error handling, retries, idempotency, graceful degradation
- **Performance**: Bottlenecks, caching, query patterns, scaling approach
- **Security**: Auth, data protection, input validation, audit logging
- **Edge Cases**: Null handling, limits, timeouts, race conditions, partial failures
- **Testing**: Testability, integration strategy, rollback considerations

## Output Format

For each finding:

```
### [Finding Title]

**Category**: Architecture | Feasibility | Reliability | Performance | Security | Edge Case | Testing
**Severity**: Critical | High | Medium | Low
**Section**: [Spec section or phase]

**Issue**: [Clear problem description]
**Recommendation**: [Specific, actionable change]
**Rationale**: [Technical justification]
```

## Guidelines

- **Verify against code** - Don't trust the spec blindly; check actual implementations
- **Follow existing patterns** - Recommendations should align with codebase conventions
- **Be specific** - Reference exact files, functions, and line numbers
- **Prioritize** - Order findings by severity and impact
- **Challenge assumptions** - Question decisions that lack justification
