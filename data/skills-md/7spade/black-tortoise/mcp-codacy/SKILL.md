---
name: mcp-codacy
description: Use the Codacy MCP server (@codacy/codacy-mcp) to run static analysis, retrieve findings, and focus remediation on high-signal issues; use when you need code quality feedback aligned with repo gates (lint, build, architecture:gate).
---

# MCP Skill: Codacy

## Scope
Use the MCP server configured as `codacy` in `.vscode/mcp.json` to pull static analysis findings and prioritize fixes that reduce risk without adding unnecessary abstraction.

## Preconditions
- Ensure `.vscode/mcp.json` contains a server entry named `codacy`.
- Ensure the `CODACY_ACCOUNT_TOKEN` input is available (the VS Code MCP input prompt will request it).

## Operating Rules
- Treat findings as a prioritization signal, not an excuse to refactor broadly.
- Fix issues at the source with minimal changes; do not suppress unless explicitly approved.
- Align with existing gates: ESLint, TypeScript type-check, dependency/architecture gate.

## Typical Workflows
1. Focused scan for touched files
- Query findings for files changed in the current task.

2. Prioritized remediation
- Address correctness/security first, then maintainability.

3. Evidence for PR
- Summarize top findings and which commits/changes resolved them.

## Prompt Templates
- "Run Codacy analysis and list the top issues in <path>. Propose minimal fixes that preserve DDD boundaries."
- "Given these Codacy findings: <paste>, group by severity and map to concrete code edits."
