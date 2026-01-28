---
name: oracle
description: "This skill should be used when the user asks to 'ask the oracle', 'use the oracle', 'get a second opinion', 'consult oracle', 'deep analysis', or when facing difficult bugs, reviewing critical code, designing complex refactors, or needing architectural analysis. Invokes a powerful reasoning model via Codex MCP for complex analysis tasks."
---

# Oracle - Second Opinion Model

## Overview

The oracle invokes a powerful reasoning model (OpenAI's gpt-5.2) via Codex MCP, optimized for complex analysis tasks. It excels at debugging, code review, architecture analysis, and finding better solutions.

**Trade-offs:** Slower and more expensive than the main agent, but significantly better at complex reasoning. Use deliberately, not for every task.

## When to Use

**Good use cases:**

- Debugging complex or elusive bugs
- Reviewing critical code changes for correctness
- Analyzing architecture and suggesting improvements
- Refactoring planning with backward compatibility
- Finding better solutions to hard problems
- Verifying logic hasn't changed after modifications
- Understanding complex codebases or algorithms

**Poor use cases (use main agent instead):**

- Simple edits or typo fixes
- Straightforward feature implementation
- File operations and basic searches
- Tasks where speed matters more than depth

## Codex Instructions

Prefix every prompt with these instructions to enable Codex's full capabilities:

```text
Instructions: You have access to powerful tools to help with analysis. Read additional files from the codebase as needed to understand context. Use web search to look up documentation, best practices, or solutions when helpful. Proactively use these tools to provide thorough, well-informed analysis.

```

## Invocation Pattern

```yaml
mcp__codex__codex with:
  prompt: |
    Instructions: You have access to powerful tools to help with analysis. Read additional files from the codebase as needed to understand context. Use web search to look up documentation, best practices, or solutions when helpful. Proactively use these tools to provide thorough, well-informed analysis.

    <task with optional @file references>
  profile: "oracle"
```

Use `@` syntax to include specific files directly in prompts (e.g., `@src/auth/login.ts`).

## Example Prompts

### Code Review

```text
Review @src/auth/jwt.ts for security vulnerabilities.
Provide specific fixes for any issues found.
```

### Debugging

```text
Analyze @src/components/DataFetcher.tsx to find why the memory leak occurs.
The component fetches data but doesn't clean up properly on unmount.
```

### Architecture Analysis

```text
Analyze how @src/services/payment.ts and @src/services/order.ts interact.
Propose a refactoring plan that maintains backward compatibility.
```

### Complex Bug Investigation

```text
Bug: Users intermittently see stale data after updates.
Related files: @src/api/update.ts @src/cache/invalidation.ts @src/hooks/useData.ts

1. Trace the data flow through these files
2. Identify race conditions or cache invalidation issues
3. Provide a fix with explanation
```

## Workflow

1. **Gather context first**: Identify relevant files and the specific problem
2. **Formulate a focused prompt**: Include file references with `@`
3. **Invoke the oracle**: Use Codex MCP with appropriate sandbox settings
4. **Act on the analysis**: Implement recommendations from the oracle's response

## Best Practices

- **Use `@` syntax for files**: Include relevant files directly in the prompt
- **Provide full context**: Include error messages, reproduction steps, and constraints
- **Ask specific questions**: "Does this handle null edge cases?" beats "Is this correct?"
- **Request actionable output**: Ask for specific recommendations, not just analysis
- **Chain with main agent**: Use oracle for analysis, main agent for implementation

## Integration Reference

| Parameter | Description                                         | Default           |
| --------- | --------------------------------------------------- | ----------------- |
| `prompt`  | The analysis request (required). Use `@file` syntax | -                 |
| `profile` | Configuration profile from config.toml              | `oracle`          |
| `cwd`     | Working directory for the session                   | Current directory |

For continued conversations, use `mcp__codex__codex-reply` with the `threadId` from the initial response.
