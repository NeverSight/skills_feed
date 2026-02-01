---
name: project-understanding
description: Use when you need a fast, reliable architecture or impact view in a large unfamiliar repo, especially under time pressure or tight context budgets where manual grep or folder inference would be risky.
---

# Project Understanding

## Overview
Automated repository intelligence via Tree-sitter indexing and PUI commands. Core principle: index once, then use focused packs (repomap/find/zoom/impact) instead of manual grep.

## When to Use
- **Entering new codebase:** Rapidly map structure and entry points
- **Planning refactors or hotfixes:** Find callers and assess blast radius
- **Budgeting context:** Fit repository summaries into LLM token limits
- **Time pressure:** Reduce risk of missing indirect dependencies
- **Verification:** Ensure changes don't violate architectural boundaries

**When NOT to Use**
- **Tiny repos:** Manual reading is faster than indexing
- **Unsupported languages:** Avoid relying on symbol graphs (see `skills/project-understanding/references/LANG_SUPPORT.md`)

## Language Support (Read This Early)
- **Full symbol/call graph support:** Python, JavaScript, TypeScript, Go, Rust
- **C/C++:** Expect mostly file-level results; `zoom`/`graph` may show "Symbol not found"
- **Reference:** `skills/project-understanding/references/LANG_SUPPORT.md`

## Command Guardrails (No Exceptions)
- **Repo selection is the working directory.** There is no `--repo` flag.
- **Always call `"$PUI"` from the target repo.** Do not run `./scripts/pui.sh` inside the target repo.
- **`zoom` target is positional.** There is no `--target` or `--file` flag.
- **`zoom` does not accept file paths.** Use a symbol id/name or `file:line`.

## Core Workflow
1. **Set tool path once:** `PUI="/path/to/skills/project-understanding/scripts/pui.sh"` (use `pui.ps1` on Windows). Do NOT run `./scripts/pui.sh` from the target repo.
2. **From the repo root (no `--repo` flag):**
   - `"$PUI" index` (or `"$PUI" index build` after big changes)
   - `"$PUI" repomap --depth 2 --max-tokens auto`
3. **Locate symbols:**
   - `"$PUI" find "SymbolName"` to get a symbol id (avoid guessing generic names)
   - `"$PUI" zoom <symbol-id|name|file:line>` (file paths alone will fail)
   - `"$PUI" graph --symbol <symbol-id|name> --depth 2`
4. **Assess impact:**
   - `"$PUI" impact --files path/to/file --include-tests`
   - `"$PUI" impact --git-diff HEAD~1..HEAD`

## Example (Lean Boost)
From the `project-understanding-skill` repo root:

```bash
PUI="$(pwd)/skills/project-understanding/scripts/pui.sh"
cd ./codebases/lean-boost

"$PUI" index
"$PUI" repomap --depth 3 --max-tokens 1200
"$PUI" find "services_manager"
"$PUI" graph --symbol 70 --depth 1 --format mermaid
"$PUI" impact --files src/uninstall/leftovers_scanner.cpp --max-tokens 800
```

## Installation
The skill works out of the box. On first run it bootstraps a shared virtual environment in `~/.local/share/pui/venv` (or a local fallback). Repository indexes are stored in `.pui/` under the project root.

## Quick Reference

| Command | Purpose | Key Flag |
|---------|---------|----------|
| `index` | Build/update index | `build`, `--force` |
| `repomap` | Directory + top files | `--depth`, `--max-tokens` |
| `find` | Symbol search | `--limit`, `--format` |
| `zoom` | Symbol detail | `--max-tokens` |
| `graph` | Call/dependency graph | `--symbol`, `--depth` |
| `impact` | Blast radius analysis | `--files`, `--git-diff`, `--include-tests` |
| `architecture` | High-level architecture summary | `--format` |
| `depgraph` | Module dependency graph | `--scope`, `--format` |

Usage notes:
- `zoom` target is positional; there is no `--target` flag.
- `zoom` does not accept file paths; use a symbol id/name or `file:line`.
- Use `find` first if you are unsure of symbol ids.

## Impact Analysis Confidence
| Score | Meaning | Action |
|-------|---------|--------|
| **0.9+** | Definite match | Trust & proceed |
| **0.7-0.9** | Likely (imports) | Verify manually |
| **<0.7** | Heuristic/dynamic | Treat as hints |

Confidence signals are meaningful only for supported languages with symbol extraction.

## Common Mistakes
- **Wrong script path:** Running `./scripts/pui.sh` from the repo root fails. Use an absolute path or `PUI=...`.
- **Skipping index:** Commands will fail or show stale data. Use `index` regularly; use `index build` for full rebuilds.
- **Wrong zoom target:** `zoom` needs a symbol id/name or `file:line`. There is no `--target` flag.
- **Guessing symbols:** Run `find` before `zoom`/`graph`, especially in large repos.
- **Inventing flags:** There is no `--repo` flag; set the repo by `cd` into it.
- **Assuming C/C++ symbol graphs:** Check `skills/project-understanding/references/LANG_SUPPORT.md` first.
- **Ignoring budget:** Large repo-maps can burn 20k+ tokens. Use `--depth` or `--max-tokens`.

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "I can just grep for imports" | Grep misses indirect dependencies. `impact` is more accurate after indexing. |
| "Structure is obvious from folder names" | Folder names are not dependency graphs. Use `repomap` and `graph`. |
| "Indexing takes too long" | Indexing is incremental; manual tracing is slower and riskier. |
| "I haven't used the tool, so I'll skip it" | First run cost is one-time; `find` + `impact` save time after. |
| "I'll just read the big files" | Reading 600+ line files burns tokens and focus. `zoom` isolates the essential logic. |
| "The tool should be in ./scripts here" | The script lives in the skill directory. Set `PUI` first. |
| "I can zoom a file path" | `zoom` needs a symbol id/name or `file:line`. File paths alone fail. |

## Red Flags - STOP and Index
- You are about to publish an impact summary from manual grep alone.
- You are guessing architecture based on folder names.
- You see "Symbol not found" and keep going without checking language support or `find`.
- You are about to run `./scripts/pui.sh` inside the target repo.
- You are about to pass a file path to `zoom`.
- You are manually following imports through more than 2 files.
- You are hitting context window limits with large code blocks.

**All of these mean: run `index`, use `repomap`/`find`/`impact`, or verify language support first.**
