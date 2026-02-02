---
name: mcp-sequential-thinking
description: Use the sequential thinking MCP server (@modelcontextprotocol/server-sequential-thinking) to break down complex problems into ordered, testable steps; use when the task requires careful multi-step reasoning, risk reduction, or dependency-sensitive refactors.
---

# MCP Skill: Sequential Thinking

## Scope
Use the MCP server configured as `sequentialthinking` in `.vscode/mcp.json` to produce step-by-step reasoning artifacts for complex changes.

## Preconditions
- Ensure `.vscode/mcp.json` contains a server entry named `sequentialthinking`.

## Operating Rules
- Prefer short, ordered steps that can be validated locally.
- Call out unknowns explicitly and convert them into concrete discovery steps (search files, read AGENTS, inspect type errors).
- Keep the solution Occam-simple: avoid introducing new abstractions without a demonstrated need.

## When To Use
- Refactors crossing multiple modules (shell/workspace/capability/eventing/integration).
- Any change that might impact DDD boundaries or the append-before-publish contract.
- Debugging nondeterministic behavior (signals/streams, event ordering).

## Output Shape
- A numbered sequence of actions.
- Each action includes: target file(s), expected outcome, and how to verify (command or observation).

## Prompt Templates
- "Think sequentially about implementing <feature>. Identify risks (DDD boundaries, event causality, signals boundary) and produce a minimal step plan with verification per step."
- "Given this error/log: <paste>, produce an ordered debug plan with the smallest set of probes/changes."
