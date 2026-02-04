---
name: reviewing-code
description: Get code review from Codex AI for implementation quality, bug detection, and best practices. Use when asked to review code, check for bugs, find security issues, or get feedback on implementation patterns.
allowed-tools: Read, Grep, Glob, mcp__codex__spawn_agent
---

# Code Review with Codex

Use `mcp__codex__spawn_agent` for code review.

## When to Use

- Review code quality and patterns
- Find potential bugs or edge cases
- Validate against best practices
- Check for security issues

## Usage

```json
{
  "prompt": "Review this code for [quality/bugs/security]: [code or file]"
}
```

## Prompt Examples

- "Review for code quality and Go best practices: [code]"
- "Analyze for security vulnerabilities: [code]"
- "Review for performance issues: [code]"
- "Does this follow idiomatic patterns? [code]"
