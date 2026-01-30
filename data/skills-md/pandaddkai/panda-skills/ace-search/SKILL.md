---
name: ace-search
description: 'Use when the task is read-only codebase discovery/search (查找/搜索/定位): find files, functions, classes, call sites, tests, or "where is X implemented" questions; prefer Augment Context Engine MCP (augment-context-engine) codebase retrieval over grep/rg.'
---

# Ace Search

## Overview

Use Augment Context Engine (ACE) semantic retrieval to quickly locate where things live in a codebase and explain how code is organized, without making edits.

Core principle: search semantically first; cite concrete file paths + symbols; iterate queries; stay read-only.

## Workflow

1. Restate the search goal in one sentence (what you’re looking for + the expected shape: file, symbol, call site, test, config).
2. Decide tool:
   - Use `mcp__augment-context-engine__codebase-retrieval` for semantic questions: “where is X implemented?”, “how does Y work?”, “what calls Z?”
   - Use `rg`/`grep` only for exact, non-semantic string needs (e.g., an error message, a literal config key) where “ALL occurrences” matters.
3. Run ACE retrieval with a specific query that names:
   - the concept (feature/domain),
   - the likely artifact type (handler, CLI command, API route, config loader, test),
   - any known identifiers (function/class/module names).
4. Summarize results anchored to facts:
   - List key files (`path/to/file.ext`) and the relevant symbols/functions/classes.
   - Describe relationships (caller/callee, entrypoints, config flow) at a high level.
5. If results are weak, refine once:
   - add constraints (language/framework, directory, module name),
   - ask a single clarifying question if needed (e.g., product name, endpoint name, exact error text).
6. Stop before editing:
   - If the user asks to modify code, ask whether they want a separate edit-focused pass; do not call `apply_patch` in this skill.

## Query Patterns (Copy/Paste)

- “Where is `{feature}` implemented? List entrypoints and main modules.”
- “Find the CLI command / subcommand handling `{name}` and its code path.”
- “How is `{concept}` configured? Identify config loading + env var parsing + defaults.”
- “Where are the tests for `{feature}`? List unit/integration/e2e tests and helpers.”
- “Trace the call path from `{entrypoint}` to `{target}` (functions/classes/modules).”
- “Find all call sites / usages of `{identifier}` and summarize patterns.”

## Output Standard

- Prefer file paths + symbol names over generalities.
- If you reference a file, include enough context in words so the user can open it and confirm quickly.
- If you are unsure, say what’s missing and ask one targeted question.

## Quick Reference

| Need | Do |
|---|---|
| “Where is X implemented?” / “How does X work?” | Use `mcp__augment-context-engine__codebase-retrieval` |
| “Show me every occurrence of this exact string” | Use `rg`/`grep` (exact match) |
| “Find definition/constructor of Foo” (exact symbol) | Use `mcp__augment-context-engine__codebase-retrieval` first; use `rg` only if you truly need exact-match enumeration |
| “And now change it” | Stop; ask to switch to an edit-focused workflow |

## Example

User: “在这个仓库里，`rollback` 是在哪里实现的？列出入口和主要调用路径。”

ACE query to run:
- “Find where rollback is implemented. Identify the CLI entrypoint/command, the function(s) performing rollback, and any backup/restore modules. Return key files and symbols.”

Then respond with:
- Key files + symbols (entrypoint + implementation + helpers)
- High-level call flow (who calls what)
- Any relevant tests

## Common Mistakes

- Using `rg`/`grep` for semantic discovery (“where is X implemented?”) instead of ACE.
- Writing an overly vague ACE query (“find auth”) and not refining it.
- Reporting conclusions without anchoring them to file paths + symbols.
- Making edits “while you’re here” when the task is explicitly search-only.

## Rationalization Table

| Rationalization | Counter |
|---|---|
| “`rg` is faster; I’ll just grep quickly.” | Speed is irrelevant if the query is semantic; use ACE to avoid missing the right entrypoint/symbols. |
| “I already know where it is.” | Prove it with a retrieval-backed file + symbol list; don’t guess. |
| “I might as well fix it now.” | This skill is read-only; stop and ask to switch workflows before editing. |

## Red Flags (Stop)

- Reaching for `rg`/`grep` before attempting ACE retrieval
- Not listing file paths/symbols in the answer
- Editing files (or proposing patches) during a search-only request
- “I’m sure it’s in `src/` somewhere” (guessing without retrieval evidence)
