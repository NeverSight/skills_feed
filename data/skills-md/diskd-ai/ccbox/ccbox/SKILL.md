---
name: ccbox
description: Inspect and summarize local Codex/Claude session logs using the ccbox CLI (projects, sessions, history). Use when asked to list discovered projects, find sessions for the current repo/folder, print a session timeline, or produce an evidence-based “what happened” report from a session .jsonl log under CODEX_SESSIONS_DIR.
---

# ccbox

Inspect local agent session logs via `ccbox` CLI and produce quick, evidence-based insights.

## Quick start

- List discovered projects:

```bash
ccbox projects
```

- List sessions for the current folder (auto-detect project):

```bash
ccbox sessions
ccbox sessions --limit 50 --offset 0 --size
```

- Inspect the latest session for the current folder:

```bash
ccbox history
ccbox history --full
ccbox history --limit 200 --offset 0 --full --size
```

- Inspect a specific project or log file:

```bash
ccbox sessions "/abs/path/to/project"
ccbox history "/abs/path/to/project" --full
ccbox history "/abs/path/to/session.jsonl" --full
```

## Workflow (recommended)

1. Confirm `ccbox` is available and up to date:
   - `ccbox --help`
   - `ccbox update` (prints `up-to-date:` or `updated:`; self-update is supported on macOS/Linux)
2. Gather facts first (do not guess):
   - Use `ccbox sessions` to select the latest session for the current folder, or `ccbox sessions "/abs/project/path"` for an explicit project.
   - Copy the `log_path` from the first line.
   - Run `ccbox history "/abs/log.jsonl" --full` to capture evidence (tool calls, tool outputs, errors).
3. Produce an insights report:
   - What the user wanted (first USER prompt).
   - What the agent did (sequence of tool calls + key outputs).
   - What changed (files/commands visible in tool outputs).
   - What failed or is risky (warnings, truncated timelines, panics/errors in outputs).
   - Next steps (concrete verification commands and follow-ups).

## References

- CLI commands + output formats: `references/cli.md`
- Insights checklist + report template: `references/insights.md`
