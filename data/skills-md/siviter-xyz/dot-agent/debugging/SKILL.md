---
name: debugging
description: Root cause analysis and debugging protocols. Use when encountering errors, test failures, unexpected behavior, stack traces, or when code behaves differently than expected.
---

# Debugging

Systematic approach to root cause analysis and debugging.

## When to Use

- Encountering errors or exceptions
- Test failures that need investigation
- Unexpected behavior in code
- Stack traces or error messages
- Code behaving differently than expected
- Performance issues or bugs

## Core Principles

- **Evidence-based**: Base diagnosis on error messages, logs, and reproducible steps
- **Systematic**: Follow structured debugging process
- **Minimal fixes**: Implement smallest change that resolves issue
- **Verify solutions**: Confirm fix works and doesn't introduce regressions

## Debugging Process

Follow systematic debugging process:
1. Capture error information (message, stack trace, logs, environment)
2. Identify reproduction steps (minimal steps, conditions, edge cases)
3. Isolate failure location (function/module, recent changes, dependencies)
4. Form and test hypotheses (evidence-based, systematic testing, debug logging)
5. Implement minimal fix (smallest change, preserve behavior, follow patterns)
6. Verify solution (issue resolved, no regressions, tests pass)

See `references/root-cause-analysis.md` for detailed methods.

## Strategic Debug Logging

Add debug logging to entry/exit points, state transitions, conditional branches, external API calls, and data transformations. Remove after issue resolved unless it provides ongoing value.

## Error Pattern Recognition

Common patterns: null/undefined errors, type errors, timing issues, state corruption, configuration issues. See `references/error-patterns.md` for detailed patterns and solutions.

## Integration

After fixing:
- Verify CI passes (types, tests, lint)
- Stage atomic changes (fix + tests)
- Suggest semantic commit message
- Confirm with user before committing

## References

For detailed guidance, see:
- `references/root-cause-analysis.md` - Systematic analysis methods
- `references/error-patterns.md` - Common error patterns and solutions
- `references/debugging-tools.md` - Debugging tools and techniques
