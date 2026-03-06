---
name: sc-troubleshoot
description: Diagnose and resolve issues in code, builds, or system behavior. Use when debugging errors, investigating build failures, or resolving deployment issues.
---

# Issue Diagnosis and Resolution

Systematically diagnose and resolve issues in code, builds, deployments, or system behavior.

## When to use

- Debugging errors and exceptions
- Investigating build failures
- Diagnosing performance issues
- Resolving deployment problems
- Tracing issues to root cause

## Instructions

### Usage

```
/sc:troubleshoot [issue] [--type bug|build|performance|deployment] [--trace]
```

### Arguments

- `issue` - Description of the problem or error message
- `--type` - Issue category (bug, build, performance, deployment)
- `--trace` - Enable detailed tracing and logging
- `--fix` - Automatically apply fixes when safe

### Execution

1. Analyze issue description and gather initial context
2. Identify potential root causes and investigation paths
3. Execute systematic debugging and diagnosis
4. Propose and validate solution approaches
5. Apply fixes and verify resolution

### Claude Code Integration

- Uses Read for error log analysis
- Leverages Bash for runtime diagnostics
- Applies Grep for pattern-based issue detection
- Maintains structured troubleshooting documentation
