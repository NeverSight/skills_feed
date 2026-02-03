---
name: mcp-software-planning
description: Use the Software-planning-mcp MCP server (github:NightTrek/Software-planning-mcp) to generate requirements, designs, task breakdowns, and execution plans for changes in this repo; use when you need structured planning artifacts (requirements/design/tasks) before implementation.
---

# MCP Skill: Software Planning

## Scope
Use the MCP server configured as `Software-planning-mcp` in `.vscode/mcp.json` to produce planning artifacts that align with Black-Tortoise governance (DDD boundaries, append-before-publish, minimalism).

## Preconditions
- Ensure `.vscode/mcp.json` contains a server entry named `Software-planning-mcp`.
- Planning output must be compatible with the repo workflow (requirements/design/tasks + audit notes when needed).

## Operating Rules
- Keep plans minimal and verifiable (Occam's Razor): only create artifacts that will be used.
- Tie every plan step to a concrete file/command in this repo (e.g., `pnpm run architecture:gate`).
- Do not invent APIs or layers; follow existing module boundaries.

## Typical Workflows
1. Requirements drafting
- Input: feature goal, constraints, affected bounded context/capability.
- Output: acceptance criteria + non-functional constraints.

2. Design outline
- Input: existing module location + eventing/state constraints.
- Output: dependency direction, events, store changes, UI signals, persistence.

3. Task breakdown
- Output: ordered tasks with explicit validation steps (lint/build/gate/tests).

## Prompt Templates
- "Create a requirements.md and tasks.md plan for: <goal>. Constraints: Angular 20 zoneless, signals-first, event-first flow, DDD boundaries. List files to touch and commands to run."
- "Draft a design.md for capability <name> using append-before-publish, include event schema and causality IDs. Keep it minimal."

## Validation Checklist
- Architecture direction preserved (Presentation -> Application -> Domain; Infrastructure implements ports).
- Append -> Publish -> React ordering explicit.
- Testing/gates listed when the change touches architecture, eventing, or integration.
