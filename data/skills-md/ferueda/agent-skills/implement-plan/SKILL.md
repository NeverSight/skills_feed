---
name: implement-plan
description: Implement a spec document phase-by-phase, writing robust idiomatic code that follows codebase patterns.
---

Implement the given spec document. Work phase-by-phase, writing robust code that follows codebase patterns, and industry best practices and patterns.

## Process

1. **Read the spec** - Understand phases, success criteria, and scope boundaries
2. **Explore the codebase** - Read files mentioned in the spec and related code
3. **Analyze patterns** - Identify existing conventions, architecture, and idioms to follow
4. **Implement phase-by-phase** - Complete each phase fully before proceeding
5. **Verify your work** - Run `make check` after code changes (skip for docs-only)

## Implementation Rules

- **Follow the plan** - The spec is your contract; implement what's specified
- **Match codebase patterns** - Use existing conventions, not new ones
- **Write robust code** - Handle errors, edge cases, and failure modes
- **Be idiomatic** - Use language best practices and established patterns
- **No shortcuts** - Implement fully, don't stub or placeholder

## Per-Phase Workflow

For each phase:

1. **Read** - Understand what the phase requires
2. **Explore** - Read existing code that will be modified or extended
3. **Implement** - Write code matching codebase style and patterns
4. **Test** - Run `make check` to verify (for code changes)
5. **Update** - Check off completed items in the spec file

## Verification

- **Code changes**: Run `make check` before proceeding to next phase
- **On failure**: Run `make fix` first, then re-run `make check`
- **Documentation-only**: Skip verification

## Communication

- If the plan doesn't match codebase reality, explain the discrepancy
- If you need to deviate, explain why before making changes
- Update checkboxes in the spec as you complete each section