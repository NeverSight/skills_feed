---
name: parallel-debug-orchestrator
description: |
  Orchestrate parallel debugging agents with root-cause tracing for multi-failure scenarios
version: "1.0.0"
category: Debugging
tags:
  - parallel
  - debugging
  - orchestration
  - agents
  - root-cause
author: mcp-skillset
license: MIT
created: 2026-01-01
last_updated: 2026-01-01
---

# Parallel Debug Orchestrator

## Overview

This skill provides guidance for debugging tasks using modern best practices and proven patterns.

## When to Use This Skill

Use this skill when:
- Working with debugging projects
- Implementing debugging-related features
- Following best practices for debugging

## Core Principles

### 1. Follow Industry Standards

**Always adhere to established conventions and best practices**

```
# Example: Follow naming conventions and structure
# Adapt this to your specific domain and language
```

### 2. Prioritize Code Quality

**Write clean, maintainable, and well-documented code**

- Use consistent formatting and style
- Add meaningful comments for complex logic
- Follow SOLID principles where applicable

### 3. Test-Driven Approach

**Write tests to validate functionality**

- Unit tests for individual components
- Integration tests for system interactions
- End-to-end tests for critical workflows

## Best Practices

### Structure and Organization

- Organize code into logical modules and components
- Use clear and descriptive naming conventions
- Keep files focused on single responsibilities
- Limit file size to maintain readability (< 500 lines)

### Error Handling

- Implement comprehensive error handling
- Use specific exception types
- Provide actionable error messages
- Log errors with appropriate context

### Performance Considerations

- Optimize for readability first, performance second
- Profile before optimizing
- Use appropriate data structures and algorithms
- Consider memory usage for large datasets

### Security

- Validate all inputs
- Sanitize outputs to prevent injection
- Use secure defaults
- Keep dependencies updated

## Common Patterns

### Pattern 1: Configuration Management

```
# Separate configuration from code
# Use environment variables for sensitive data
# Provide sensible defaults
```

### Pattern 2: Dependency Injection

```
# Inject dependencies rather than hardcoding
# Makes code testable and flexible
# Reduces coupling between components
```

### Pattern 3: Error Recovery

```
# Implement graceful degradation
# Use retry logic with exponential backoff
# Provide fallback mechanisms where appropriate
```

## Anti-Patterns

### ❌ Avoid: Hardcoded Values

**Don't hardcode configuration, credentials, or magic numbers**

```
# BAD: Hardcoded values
API_TOKEN = "hardcoded-value-bad"  # Never do this!
max_retries = 3
```

✅ **Instead: Use configuration management**

```
# GOOD: Configuration-driven
API_TOKEN = os.getenv("API_TOKEN")  # Get from environment
max_retries = config.get("max_retries", 3)
```

### ❌ Avoid: Silent Failures

**Don't catch exceptions without logging or handling**

```
# BAD: Silent failure
try:
    risky_operation()
except Exception:
    pass
```

✅ **Instead: Explicit error handling**

```
# GOOD: Explicit handling
try:
    risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    raise
```

### ❌ Avoid: Premature Optimization

**Don't optimize without measurements**

✅ **Instead: Profile first, then optimize**

- Measure performance with realistic workloads
- Identify actual bottlenecks
- Optimize the critical paths only
- Validate improvements with benchmarks

## Testing Strategy

### Unit Tests

- Test individual functions and classes
- Mock external dependencies
- Cover edge cases and error conditions
- Aim for >80% code coverage

### Integration Tests

- Test component interactions
- Use test databases or services
- Validate data flow across boundaries
- Test error propagation

### Best Practices for Tests

- Make tests independent and repeatable
- Use descriptive test names
- Follow AAA pattern: Arrange, Act, Assert
- Keep tests simple and focused

## Debugging Techniques

### Common Issues and Solutions

**Issue**: Unexpected behavior in production

**Solution**:
1. Enable detailed logging
2. Reproduce in staging environment
3. Use debugger to inspect state
4. Add assertions to catch assumptions

**Issue**: Performance degradation

**Solution**:
1. Profile the application
2. Identify bottlenecks with metrics
3. Optimize critical paths
4. Monitor improvements with benchmarks

## Related Skills
- **test-driven-development**: Write tests before implementation
- **systematic-debugging**: Debug issues methodically
- **code-review**: Review code for quality and correctness

## References

- Industry documentation and best practices
- Official framework/library documentation
- Community resources and guides
- Code examples and patterns

## Version History

- **1.0.0** (2026-01-01): Initial version
