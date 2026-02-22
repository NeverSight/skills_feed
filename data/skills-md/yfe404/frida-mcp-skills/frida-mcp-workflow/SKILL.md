---
name: frida-mcp-workflow
description: "Enforce safe Frida 17 MCP operations with strict phase gating. Use when attaching/spawning sessions, writing or loading scripts, applying Java/native hooks, troubleshooting instrumentation failures, or interpreting Frida MCP output. Require docs-first usage and run the mandatory workflow: Idea -> Scripting -> Execution -> Notes."
---

# Frida MCP Workflow

Run these phases in order. Do not skip phases.

## Phase 1: Idea

- Define target: process/app identifier, platform, and session type.
- Define objective: what signal/result must be observed.
- Query docs before function use: call `search_frida_docs` for each non-trivial API/runtime assumption.
- Record 2-5 `Doc facts used` bullets before scripting.
- Assume Frida 17 semantics only. Do not use Frida 16 assumptions.

Hard stop:
- If docs are missing or ambiguous, narrow the query and retry before scripting.

## Phase 2: Scripting

- Prefer saved files over inline scripts.
- Allow inline only for short, read-only probes.
- For hook scripts, require file-based scripts and `load_script`.
- Declare `script_id`, purpose, and explicit target list (module/symbol or class/method).
- Add idempotence guard to prevent duplicate install.
- Define teardown path (`uninstall` RPC export or equivalent).

Script policy:
- If script is more than 25 lines or writes hooks, save it to a file.
- If modifying existing behavior, include rollback logic in the script.

## Phase 3: Execution

- Preflight checks before load/execute:
  - session exists and is alive
  - loaded scripts are listed
  - target overlap is checked
- If overlap exists, unload/replace old script before loading new one.
- Do not attach multiple scripts to the same target unless explicitly intentional.
- Prefer one script per purpose (probe, hook, tracer).

Failure handling:
- On `Java is not defined`, stop retries and re-check docs/runtime assumptions.
- On attach/spawn failures, run diagnostics before retrying instrumentation.
- On oversized docs output, reduce query scope or paginate; do not guess.

## Phase 4: Notes

- Persist notes to file after each execution cycle.
- Record:
  - doc facts used
  - script ledger (loaded/unloaded/current active)
  - observed output and verification status
  - errors and root cause
  - cleanup status and next action
- Confirm teardown is complete when ending work.

## Required Response Shape

For each task, output four sections in this order:

1. `Idea`
2. `Scripting`
3. `Execution`
4. `Notes`

Do not run tool calls in `Execution` before `Idea` and `Scripting` are present.
