---
name: deep-analyse
description: Thorough code analysis without polluting main context
---

# Deep Analysis

Perform thorough analysis of the specified code area: $ARGUMENTS

## Analysis Steps

1. **Trace all code paths**: Follow execution from entry points through to completion
2. **Map dependencies**: Identify all imports, interfaces, and external dependencies
3. **Identify side effects**: Document state changes, I/O operations, and mutations
4. **List callers and callees**: Build a call graph for the target code
5. **Check test coverage**: Identify which paths have test coverage and which lack it

## Deliverables

Provide a structured report with:
- Architecture overview
- Key abstractions and their purposes
- Critical code paths
- Potential issues or improvement opportunities
- Test coverage assessment
