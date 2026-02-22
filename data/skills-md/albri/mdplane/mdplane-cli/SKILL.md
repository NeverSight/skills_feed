---
name: mdplane-cli
description: Use the mdplane CLI for workspace operations from a shell (init, read/cat, append, write, search, export, login, claim). Trigger when users ask for mdplane command usage or command-line automation. For HTTP-first usage, use mdplane.
---

# mdplane CLI

Use this skill when shell access is available and the task should be solved with `mdplane` commands.

## Operating Rules

1. OpenAPI and server behavior are the source of truth.
2. Do not invent commands, flags, or response fields.
3. Prefer least privilege:
   - read key for read/search (scoped)
   - append key for appends
   - write key only for mutating file/folder state
   - API key for `/api/v1/*` control endpoints (workspace-wide search, exports, deleted, agents)
4. Never print capability URLs, API keys, or session tokens.

## Standard Workflow

1. Confirm deployment target (`https://api.mdplane.dev`, self-host, or local).
2. Resolve auth mode from profile/env/flags.
3. Execute command(s) with minimal required capability.
4. Validate outcomes (`status`, `files`, `read`, `check-keys` as needed).
5. Summarize results and any follow-up action.

## Command Surface

The canonical command inventory and auth expectations are in:

- `./references/command-surface.md`

Use it before giving command guidance.

## Canonical References

- `./references/canonical-links.md`

Read these references when the request touches new endpoints, auth edge cases, orchestration, webhooks, export, or folder operations.

## Quick Checks

```bash
mdplane --help
mdplane <command> --help
```

If CLI behavior appears to drift from docs, trust source and OpenAPI links in references and flag the drift.

