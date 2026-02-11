---
name: planning
description: Guidelines for planning code implementations - invoke when entering plan mode or before implementing a complex feature
---

# Code Implementation Planning Guidelines

Use these guidelines when in plan mode or planning any non-trivial code implementation.

## Leveraging Skills

- **Check available skills before planning**: Review available skills to identify which could assist with the task
- Reference relevant skills in the plan, including specific files and line numbers (e.g., `google-adk` skill's `docs/streaming.md:42-87` for streaming patterns)
- Skills provide specialized context, documentation, and workflows that improve implementation quality

## Clarifying Requirements

- **Interview the user in depth** before finalizing any plan (use `AskUserQuestion` tool if available, otherwise ask directly)
- Ask about: technical implementation details, UI/UX preferences, concerns, tradeoffs, edge cases, error handling strategies, integration points, performance requirements, and future extensibility
- **Legacy code handling**: When changes affect existing APIs or endpoints, ask whether to deprecate (keep with warnings) or remove entirely
- **Questions must not be obvious** - avoid questions answerable by reading the requirements; instead ask about ambiguities, implicit assumptions, and decisions that could go multiple ways
- **Continue interviewing iteratively** until all critical unknowns are resolved - don't stop after one round of questions

## Autonomous Implementation Readiness

- Before concluding planning, **evaluate whether the plan enables fully autonomous implementation**
- Ask yourself: "Can I implement this without needing to ask any more questions?"
- If the answer is no, identify the gaps and continue the interview
- The plan should be detailed enough that implementation becomes mechanical execution of well-defined steps
- **Permissions for uninterrupted execution**: Anticipate which actions will need permission during implementation and check if they're already allowed. If not, include them in the plan so the user can pre-approve. Categories to consider:
  - Bash commands (e.g., `npm test`, `docker build`, `git push`)
  - File modifications outside typical source directories
  - Network requests / WebFetch to external domains
  - MCP tool usage
  - Subagent/Task delegation
  - Access to directories beyond the working directory
- **Verification strategy**: The plan must specify how to confirm success:
  - **Basic verification**: Tests pass, types check, linting passes
  - **End-to-end verification**: Test as a human user would - agents tend to skip this without explicit instructions

## Proving Completion

The coding agent must **prove** to the user that all requirements were fulfilled—not just claim it.

- **Plan for proof**: During planning, think about how each requirement can be demonstrated as complete (test output, screenshots, logs, behavioral evidence)
- **Execute verification**: After implementation, actively verify each requirement through concrete actions
- **Completion report**: Write a brief report at the end that:
  - Lists each original requirement
  - States what was implemented to fulfill it
  - Provides evidence (e.g., "tests pass", "endpoint returns expected response", "UI renders correctly")
  - Flags any requirements that were partially met or descoped

## Plan Output Style

- **Sketch, don't implement**: Describe the approach at a high level rather than writing out actual implementation code
- Explain *what* will be done and *why*, not the literal code that will do it
- Only include specific code snippets when:
  - The user explicitly requests them
  - A particular syntax or pattern is non-obvious and benefits from illustration
  - The implementation detail is critical to understanding the approach
- Focus on: file changes, architectural decisions, data flow, key integration points, and sequencing of steps
