---
name: mcp-context7
description: Use the Context7 MCP server (@upstash/context7-mcp) to fetch authoritative, version-appropriate library documentation snippets (Angular, NgRx Signals, Firebase, RxJS, Playwright); use when you must confirm API usage, signatures, or best practices without relying on memory.
---

# MCP Skill: Context7 (Docs Lookup)

## Scope

Use the MCP server configured as `context7` in `.vscode/mcp.json` to retrieve documentation context for libraries used in this repo.

## Preconditions

- Ensure `.vscode/mcp.json` contains the `context7` server.
- Ensure the `CONTEXT7_API_KEY` input is available (the VS Code MCP input prompt will request it).

## Operating Rules

- Use Context7 for API correctness when there is a meaningful chance memory is wrong (new Angular versions, new NgRx Signals APIs, Firebase SDK changes).
- Prefer primary documentation references; do not quote large blocks.

## Typical Uses In This Repo

- Angular 20 control flow and signals interop APIs.
- NgRx Signals (`signalStore`, `withState`, `withMethods`, `rxMethod`, `tapResponse`).
- AngularFire / Firebase modular APIs.
- Playwright test APIs.

## Prompt Templates

- "Look up the correct API/signature for <symbol> in <library> (target versions: Angular ~20, @ngrx/signals ~20). Provide minimal usage example."
- "Confirm best practice for converting Observable to Signal in Angular 20, including cleanup semantics."

## Output Requirements

- Provide the minimal snippet needed to implement correctly.
- Call out version assumptions explicitly (match `package.json` versions).
