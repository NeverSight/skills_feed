---
name: jetbrains-skill
description: "Use the JetBrains IDE MCP Server (IntelliJ IDEA 2025.2+) to let an external client drive IDE-backed actions: run Run Configurations, execute commands in the IDE terminal, read/create/edit project files, search via IDE indexes (text/regex), retrieve code inspections for a file, fetch symbol info, perform rename refactoring, list modules/dependencies/repos, open files in the editor, and reformat code. Use when you want IDE-grade indexing/refactoring/inspection instead of raw shell scripting."
---

# JetBrains Skill

## Quick start

Goal: use JetBrains IDE features (index, inspections, refactoring, run configurations, integrated terminal) as tools for an external client, while keeping changes auditable and safe.

notes + tool list (condensed): `skills/jetbrains-skill/references/jetbrains-skill.md`.

## Connection & modes

### Client setup (done in the IDE)
- Settings → Tools → MCP Server
- Enable MCP Server
- Use “Auto-configure” for supported clients (updates their JSON config), or copy SSE / Stdio config for manual setup
- Restart the external client to apply changes

### Brave Mode (no confirmations)
The IDE can allow running shell commands / run configurations without per-action confirmation (“Brave mode”).
This increases automation power but also increases risk. Require explicit user confirmation before enabling/disabling it.

## Workflow decision tree

1) Do I need IDE-grade analysis/refactoring?
- File diagnostics: `get_file_problems`
- Symbol semantics / docs: `get_symbol_info`
- Safe rename across project: `rename_refactoring` (prefer over plain text replace)
- Indexed search: `search_in_files_by_text` / `search_in_files_by_regex`
- Find files: `find_files_by_name_keyword` (fast, name-only) or `find_files_by_glob` (path glob)

2) Do I just need file operations in the project?
- Read file text: `get_file_text_by_path`
- Create file: `create_new_file`
- Targeted replace: `replace_text_in_file` (auto-saves)
- Open in editor: `open_file_in_editor`
- Reformat: `reformat_file`

3) Do I need to run something?
- List run configs: `get_run_configurations`
- Run a config (wait for completion): `execute_run_configuration`
- Run a terminal command in IDE: `execute_terminal_command` (may require confirmation; output is capped)

## Constraints (avoid common mistakes)

- Always pass `projectPath` when known to avoid ambiguity.
- Many tools require paths relative to the project root and only operate on project files.
- Line/column positions are 1-based for location-based tools.
- Prefer controlling output with `maxLinesCount` + `truncateMode`; do not rely on defaults for large outputs.
- Terminal commands and running configurations are high-risk; require explicit confirmation for any potentially destructive command. Brave Mode removes guardrails.

## Recommended high-value patterns

### Debug via inspections first
1) `get_file_problems` to find errors/warnings → 2) `get_symbol_info` to understand the code → 3) `rename_refactoring` for renames → 4) `replace_text_in_file` only for truly textual changes.

### Use indexed search for scale
Prefer `search_in_files_by_text` / `search_in_files_by_regex` since it uses IDE search/indexing and highlights matches with `||`.

### Running and output control
Use `execute_run_configuration` with a sane `timeout` (ms). For terminal commands use `execute_terminal_command`, but remember output caps; for huge output, redirect to a file and read it via file tools.

## References
- notes + tool list (condensed): `skills/jetbrains-skill/references/jetbrains-skill.md`
