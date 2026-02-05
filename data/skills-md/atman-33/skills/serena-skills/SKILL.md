---
name: serena-skills
description: Standalone Serena MCP tools for code intelligence - symbol search, file ops, memory, editing, config, workflow helpers, and shell execution without MCP server
---

# Serena Skills

Standalone Serena MCP tools for code intelligence without requiring MCP server.

## Quick Start

When running from project root, use full path to scripts:

1. (Optional) Register project:
   ```bash
   python .claude/skills/serena-skills/scripts/project-config/activate_project.py --project-path .
   ```

2. Get structure:
   ```bash
   # get_symbols_overview.py: Use --file parameter (not --path)
   python .claude/skills/serena-skills/scripts/symbol-search/get_symbols_overview.py --project-root . --file src/main.ts
   ```

3. Locate target:
   ```bash
   # find_symbol.py: Use --pattern parameter (not --symbol)
   python .claude/skills/serena-skills/scripts/symbol-search/find_symbol.py --project-root . --pattern "MyClass"
   ```

4. Edit:
   ```bash
   python .claude/skills/serena-skills/scripts/code-editor/replace_content.py --project-root . --file src/main.ts --old-string "old" --new-string "new"
   ```

All scripts support `--project-root` parameter (use `.` for current directory when running from project root).

## Tool Categories

Maps Serena MCP tools to standalone scripts organized by category.

When running from project root, use path: `.claude/skills/serena-skills/scripts/<category>/<script>.py`

### Symbol Search (`.claude/skills/serena-skills/scripts/symbol-search/`)
LSP-based code analysis - maps to Serena MCP symbol tools:
- **get_symbols_overview.py** (`--file`) - File structure overview (classes, functions, methods)
- **find_symbol.py** (`--pattern`) - Search by name path pattern (`Class/method`, `/absolute/path`)
- **find_referencing_symbols.py** (`--symbol-name`) - Find all usages of a symbol
- **insert_after_symbol.py** / **insert_before_symbol.py** (`--symbol-path`) - Insert code around symbols
- **rename_symbol.py** (`--old-name`, `--new-name`) - Safe refactoring with automatic reference updates

### Memory Management (`.claude/skills/serena-skills/scripts/memory-manager/`)
Persistent project knowledge - maps to Serena MCP memory tools:
- **write_memory.py** (`--name`, `--content`) / **read_memory.py** (`--name`) - Store/retrieve project knowledge
- **list_memories.py** / **delete_memory.py** (`--name`) / **edit_memory.py** (`--name`, `--content`) - Manage memories

Storage: `.tmp/.serena-skills/memories/`

### File Operations (`.claude/skills/serena-skills/scripts/file-ops/`)
File system operations - maps to Serena MCP file tools:
- **read_file.py** (`--file`) - Read file contents or line ranges
- **list_dir.py** (`--path`) - List directories (with recursion support)
- **find_file.py** (`--pattern`) - Find files by name pattern (wildcards)
- **search_for_pattern.py** (`--pattern`) - Regex search with context (grep-like)

### Code Editor (`.claude/skills/serena-skills/scripts/code-editor/`)
Code modification - maps to Serena MCP editing tools:
- **replace_symbol_body.py** (`--symbol-path`, `--new-body`) - Symbol-level replacement (LSP-aware)
- **replace_content.py** (`--file`, `--old-string`, `--new-string`) - Text-based find/replace (literal or regex)
- **create_text_file.py** (`--file`, `--content`) - Create new file
- **delete_lines.py** / **replace_lines.py** / **insert_at_line.py** (`--file`, `--line`) - Line-based edits

### Project Config (`.claude/skills/serena-skills/scripts/project-config/`)
Project setup and configuration - maps to Serena MCP config tools:
- **activate_project.py** (`--project-path`) - Register and configure project (creates `.tmp/.serena-skills/`)
- **list_projects.py** - Show all registered projects
- **get_config.py** (`--project-root`) - Display current configuration
- **get_project_config.py** / **update_project_config.py** (`--project-root`) - Manage project.yml
- **remove_project.py** (`--project-root`) - Unregister project

### Workflow Assistant (`.claude/skills/serena-skills/scripts/workflow-assistant/`)
Workflow helpers - maps to Serena MCP workflow tools:
- **check_onboarding.py** / **create_onboarding.py** / **get_onboarding.py** / **update_onboarding.py** - Onboarding docs
- **think_collected_info.py** - Reflect on information completeness
- **think_task_adherence.py** - Verify task alignment before code changes
- **think_are_done.py** - Check completion before finalizing

### Shell Executor (`.claude/skills/serena-skills/scripts/shell-executor/`)
Command execution - maps to Serena MCP command tool:
- **execute_shell_command.py** (`--command`) - Safe shell execution with timeout protection

## Usage Patterns

**Note:** When running from project root, prefix all script paths with `.claude/skills/serena-skills/scripts/`

### Understanding New Codebase
1. `python .claude/skills/serena-skills/scripts/file-ops/list_dir.py --project-root . --path . --recursive` - Get structure
2. `python .claude/skills/serena-skills/scripts/symbol-search/get_symbols_overview.py --project-root . --file src/main.ts` - Overview key files
3. `python .claude/skills/serena-skills/scripts/symbol-search/find_symbol.py --project-root . --pattern "Class" --include-body` - Explore implementations
4. `python .claude/skills/serena-skills/scripts/memory-manager/write_memory.py --project-root . --name "findings" --content "..."` - Document findings

### Making Code Changes
1. `python .claude/skills/serena-skills/scripts/symbol-search/find_symbol.py --project-root . --pattern "target"` - Locate target
2. `python .claude/skills/serena-skills/scripts/symbol-search/find_referencing_symbols.py --project-root . --symbol "target"` - Check impact
3. `python .claude/skills/serena-skills/scripts/code-editor/replace_content.py --project-root . --file src/file.ts --old-string "old" --new-string "new"` - Edit
4. `python .claude/skills/serena-skills/scripts/shell-executor/execute_shell_command.py --project-root . --command "npm test"` - Run tests

### Refactoring
1. `python .claude/skills/serena-skills/scripts/symbol-search/find_symbol.py --project-root . --pattern "target"` - Understand structure
2. `python .claude/skills/serena-skills/scripts/symbol-search/find_referencing_symbols.py --project-root . --symbol "target"` - Map dependencies
3. `python .claude/skills/serena-skills/scripts/symbol-search/rename_symbol.py --project-root . --old-name "OldName" --new-name "NewName"` - Safe rename across codebase
4. `python .claude/skills/serena-skills/scripts/code-editor/replace_symbol_body.py --project-root . --symbol "target" --new-body "..."` - Modify implementations

## When to Use What

**Understanding code?** → `symbol-search/get_symbols_overview.py` → `symbol-search/find_symbol.py`

**Modifying code?** → `code-editor/replace_symbol_body.py` (symbol-level) or `code-editor/replace_content.py` (text-level)

**Searching?** → `file-ops/search_for_pattern.py` (text) or `symbol-search/find_symbol.py` (symbols)

**Widespread changes?** → `symbol-search/rename_symbol.py` (names) or `code-editor/replace_content.py` (patterns)

**Track findings?** → `memory-manager/write_memory.py` (session) or `workflow-assistant/update_onboarding.py` (permanent)

All paths relative to `.claude/skills/serena-skills/scripts/` when running from project root.

## Symbol vs Text Editing

**Symbol-level (LSP-aware):**
- Entire functions/methods/classes
- Type-aware, reference-aware
- Tools: `code-editor/replace_symbol_body.py`, `symbol-search/insert_*_symbol.py`, `symbol-search/rename_symbol.py`

**Text-level (pattern matching):**
- Small targeted changes, comments, strings
- Regex support, multi-location edits
- Tools: `code-editor/replace_content.py`, `code-editor/*_lines.py`, `code-editor/insert_at_line.py`

All paths relative to `.claude/skills/serena-skills/scripts/` when running from project root.

## Technical Notes

**Requirements:**
- Python 3.8+
- Language servers for LSP tools (e.g., `pyright` for Python)
- Auto-detects `.venv` when present

**Storage:**
- Project data: `{project}/.tmp/.serena-skills/`
- Memories: `{project}/.tmp/.serena-skills/memories/`
- Config: `{project}/.tmp/.serena-skills/project.yml`

**Troubleshooting:**
- **LSP timeout** → Language mismatch or large project
  - Cause: Wrong language server (e.g., Pyright for TypeScript)
  - Fix: Specify `--language typescript` or run `activate_project.py --project-path . --language typescript`
  - Or: Increase timeout with `--lsp-timeout 20` for large projects
- **LSP fails** → Install language server
- **Module not found** → Install deps (see SETUP.md)
- **No `python3`** → Use `python`
- **`lib` import errors** → Set PYTHONPATH:
  - Windows PowerShell: `$env:PYTHONPATH = ".claude/skills/serena-skills"`
  - Linux/macOS/WSL: `export PYTHONPATH=.claude/skills/serena-skills`
  - Or run: `cd .claude/skills/serena-skills && python scripts/...`

## Setup and Installation

See [SETUP.md](SETUP.md) for complete installation guide, including:
- System requirements
- Installation methods (system-wide or virtual environment)
- Language server setup
- Verification steps
- Usage examples and troubleshooting
