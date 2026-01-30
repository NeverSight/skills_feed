---
name: desktop-commander
description: "Use Desktop Commander MCP (typically tools like `mcp__desktop-commander__*`) to manage local files and long-running processes: read/write/search files, apply precise edits, work with Excel/PDFs, run terminal commands and interact with REPLs (Python/Node/SSH/DB), inspect/terminate processes, and review tool call history. Use when the task requires doing real work on the machine (editing code/configs, searching a repo, analyzing CSV/Excel, generating/modifying PDFs, running commands with streaming output)."
---

# Desktop Commander

## Quick start

Goal: use Desktop Commander MCP to turn “files / processes / search / edits” into verifiable tool calls (small, safe steps) instead of treating the machine as a black box.

Most common entry points:
- Read content: `mcp__desktop-commander__read_file` (paging, negative offset tail, PDF/image/Excel/URL).
- Small edits: `mcp__desktop-commander__edit_block` (targeted text replace / Excel range update).
- Large edits: `mcp__desktop-commander__write_file` in chunks (respect `fileWriteLineLimit`).
- Interactive work: `mcp__desktop-commander__start_process` + `mcp__desktop-commander__interact_with_process` + `mcp__desktop-commander__read_process_output`.

Official notes + tool list: `skills/desktop-commander/references/desktop-commander.md`.

## Workflow decision tree

1) Do I need to *find* something?
- File names/paths: `mcp__desktop-commander__start_search` (`searchType="files"`) → `mcp__desktop-commander__get_more_search_results`
- File contents: `mcp__desktop-commander__start_search` (`searchType="content"`) → paginate → `mcp__desktop-commander__stop_search` when done

2) Do I need to *read* or *change* content?
- Read: `mcp__desktop-commander__read_file` (use `offset/length`; use `offset=-N` for tail)
- Small change: `mcp__desktop-commander__edit_block` (default replaces 1 occurrence; use `expected_replacements` for multiple)
- Large change: `mcp__desktop-commander__write_file` (`mode="rewrite"` then `mode="append"` chunked)

3) Do I need to run commands / keep sessions?
- One-off commands: `mcp__desktop-commander__start_process` (shell command) + read output
- REPL / SSH / DB / dev server: `start_process` → `interact_with_process` → `read_process_output`

4) Is this a high-risk operation (config changes, killing processes, bulk edits/moves, any data loss)?
- Explain impact + rollback first; require explicit user confirmation before executing.
- Prefer making config changes in a separate chat (official guidance).

## Recipes

### Reading files

- Text/code: `read_file` with pagination; logs: `offset=-200` (tail-like).
- Multiple files: `read_multiple_files` to reduce round trips.
- URLs: `read_file` with `isUrl: true` for web content/images.

### Editing files

- Targeted replace: `edit_block` with minimal unique context; for many occurrences set `expected_replacements`.
- Rewrites: `write_file` in 25–30 line chunks (`rewrite` then `append`).
- Excel: read via `read_file`; edit via `edit_block` with `range` + 2D array.
- PDFs: only via `write_pdf` (do not use `write_file` for PDFs).

### Search

- Prefer `start_search` + `get_more_search_results` for repo exploration; stop searches you no longer need.
- Use `literalSearch: true` for patterns with special characters (parentheses, brackets, dots, etc.).

### Processes & interaction

- Data analysis: run `python3 -i`, then use `interact_with_process` for pandas/numpy workflows.
- Observing long jobs: call `read_process_output` periodically; to stop use `kill_process`/`force_terminate` (high-risk).
- Status: `list_sessions` / `list_processes`.

### Config & audit

- `get_config` / `set_config_value`: use carefully; directory restrictions are not a security boundary for terminal commands.
- `get_recent_tool_calls`: recover context and debug “what happened”.
- `get_usage_stats`: usage/performance insight.

## Guardrails (must follow)

- Prefer absolute paths; don’t assume OS-specific separators.
- For big changes: read first; keep edits small; chunk writes; keep rollback in mind.
- High-risk actions require explicit confirmation: config changes, killing sessions/processes, bulk file edits/moves, any destructive command.
- Security: `allowedDirectories` limits filesystem tools, not terminal commands—don’t treat it as sandboxing.

## References
- Official notes + tool list: `skills/desktop-commander/references/desktop-commander.md`
