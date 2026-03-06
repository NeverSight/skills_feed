---
name: sc-test
description: Execute tests, generate test reports, and maintain test coverage. Use when running tests, checking coverage, or setting up test infrastructure.
---

# Testing and Quality Assurance

Execute tests, generate comprehensive test reports, and maintain test coverage standards.

## When to use

- Running unit, integration, or e2e tests
- Generating coverage reports
- Setting up test infrastructure
- Monitoring test results
- Fixing failing tests

## Instructions

### Usage

```
/sc:test [target] [--type unit|integration|e2e|all] [--coverage] [--watch]
```

### Arguments

- `target` - Specific tests, files, or entire test suite
- `--type` - Test type (unit, integration, e2e, all)
- `--coverage` - Generate coverage reports
- `--watch` - Run tests in watch mode
- `--fix` - Automatically fix failing tests when possible

### Execution

1. Discover and categorize available tests
2. Execute tests with appropriate configuration
3. Monitor test results and collect metrics
4. Generate comprehensive test reports
5. Provide recommendations for test improvements

### Claude Code Integration

- Uses Bash for test execution and monitoring
- Leverages Glob for test discovery
- Applies TodoWrite for test result tracking
- Maintains structured test reporting and coverage analysis
