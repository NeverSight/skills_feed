---
name: code-quality
description: >-
  Set up formatting, linting, import sorting, type checking, and pre-commit
  hooks when scaffolding or starting a new project. Use this skill whenever
  creating a new project, initializing a repo, scaffolding an app, or when
  the user asks to add linting/formatting to an existing project. Triggers
  on: "new project", "scaffold", "init", "set up linting", "add formatter",
  "add pre-commit hooks", "configure biome", "configure ruff". The goal is
  to establish code quality tooling from day one so issues are caught
  incrementally, not in a painful bulk-fix later.
---

# Code Quality Setup

When starting or scaffolding any project, set up formatting, linting, import
sorting, type checking, and pre-commit hooks **before writing application code**.
This prevents the painful scenario of adding these tools later and facing
thousands of lines of formatting changes in a single commit.

## Detect the ecosystem

Determine the project type from existing files or the scaffolding context:

| Signal | Ecosystem |
|--------|-----------|
| `pyproject.toml`, `setup.py`, `requirements.txt`, `.py` files | Python |
| `package.json`, `tsconfig.json`, `.ts`/`.js`/`.tsx` files | JavaScript/TypeScript |
| Both present | Monorepo — configure each ecosystem separately |

Also check for existing quality tooling configs (`.eslintrc`, `.prettierrc`, `biome.json`, `[tool.black]` or `[tool.ruff]` in `pyproject.toml`, `.pre-commit-config.yaml`, `lefthook.yml`). If present, preserve them — only migrate to different tools if the user explicitly requests it (see Guardrails).

## Set up tooling

After detecting the ecosystem, follow the appropriate guide:

- **Python projects** — see [python.md](references/python.md) for Ruff + pre-commit setup
- **JS/TS projects** — see [javascript.md](references/javascript.md) for Biome + Knip + lefthook + tsc setup

## Standard command contract

Every project must expose these five commands (via `package.json` scripts or `Makefile`):

| Command | What it does |
|---------|-------------|
| `format` | Auto-format and sort imports |
| `lint` | Lint without writing (report only) |
| `typecheck` | Run type checker (`tsc --noEmit`, `mypy`, or `pyright`) |
| `check` | All non-writing checks: lint + typecheck + unused-code detection |
| `check:fix` | Run autofixers (format + lint fix), then run `check` |

Pre-commit hooks should run `check:fix` so that commits are always clean.

## Workflow

1. Install and configure the tools (formatter, linter, type checker)
2. Add pre-commit hook infrastructure (lefthook or pre-commit)
3. Run the full suite once to establish a clean baseline
4. Fix any initial issues so the first "real" commit starts clean
5. Commit the configuration files as the first or second commit in the project

## When working on existing projects

If a project already has code but no quality tooling:

1. Add and configure the tools
2. Run the formatter first — commit the formatting changes in a single dedicated commit with a message like `chore: apply initial formatting`
3. Run the linter — fix issues and commit separately: `chore: fix initial lint issues`
4. Wire up pre-commit hooks last so all future commits are clean

## Guardrails

- **Don't replace existing mature tooling.** If a project already uses ESLint/Prettier, Black, or other established tools, keep them. Only migrate to Biome/Ruff if the user explicitly asks.
- **Don't broadly disable rules to force a green baseline.** Use narrow, targeted exceptions (`// biome-ignore`, `# noqa: XX`) with comments explaining why — never bulk-suppress to make errors disappear.
- **If tooling binaries aren't available, scaffold configs anyway.** Write the configuration files and report the install commands the user needs to run.

## Completion checklist

Before considering the setup done, verify:

1. Formatter, linter, and type checker installed and configured for the project's ecosystem
2. Import sorting enabled (Ruff's `I` rules or Biome's `organizeImports`)
3. All five standard commands work: `format`, `lint`, `typecheck`, `check`, `check:fix`
4. Pre-commit hooks configured and executable (`pre-commit run --all-files` or `npx lefthook run pre-commit`)
5. Baseline autofix applied and a clean check passes with no errors
