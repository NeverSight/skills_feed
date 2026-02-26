---
name: solo-setup
description: Auto-generate project workflow config (docs/workflow.md) from existing PRD and CLAUDE.md with zero questions. Use when user says "set up workflow", "configure TDD", "wire up dev workflow", or after running /scaffold before /plan. Do NOT use for founder setup (use /init) or project scaffolding (use /scaffold).
license: MIT
metadata:
  author: fortunto2
  version: "2.1.1"
  openclaw:
    emoji: "⚙️"
allowed-tools: Read, Grep, Bash, Glob, Write, Edit, AskUserQuestion, mcp__solograph__project_info, mcp__solograph__codegraph_query, mcp__solograph__kb_search
argument-hint: "[project-name]"
---

# /setup

Auto-generate project workflow config from existing PRD and CLAUDE.md. Zero interactive questions — all answers extracted from project data that already exists after `/scaffold`.

## When to use

After `/scaffold` creates a project, before `/plan`. Creates `docs/workflow.md` so `/plan` and `/build` can work.

## MCP Tools (use if available)

- `project_info(name)` — get project details, detected stack
- `kb_search(query)` — search for dev principles, manifest, stack templates
- `codegraph_query(query)` — check project dependencies in code graph

If MCP tools are not available, fall back to reading local files only.

## Steps

1. **Detect project root:**
   - If `$ARGUMENTS` is provided, look for a project with that name in the current directory or `projects_dir` from `~/.solo-factory/defaults.yaml`.
   - Otherwise use current working directory.
   - Verify the directory exists and has `CLAUDE.md`.
   - If not found, ask via AskUserQuestion.

2. **Check if already initialized:**
   - If `docs/workflow.md` exists, warn and ask whether to regenerate.

3. **Read project data** (parallel — all reads at once):
   - `CLAUDE.md` — tech stack, architecture, commands, Do/Don't
   - `docs/prd.md` — problem, users, solution, features, metrics, pricing
   - `package.json` or `pyproject.toml` — exact dependency versions
   - `Makefile` — available commands
   - Linter configs (`.eslintrc*`, `eslint.config.*`, `.swiftlint.yml`, `ruff.toml`, `detekt.yml`)

4. **Read ecosystem sources** (optional — enhances quality):
   - Detect stack name from CLAUDE.md (look for "Stack:" or the stack name in tech section).
   - If MCP `kb_search` available: search for stack template and dev-principles.
   - Otherwise: look for `stacks/<stack>.yaml` and `dev-principles.md` in `.solo/` or plugin templates directory (if accessible).
   - If neither available: derive all info from CLAUDE.md + package manifest (sufficient).

5. **Detect languages** from package manifest:
   - `package.json` → TypeScript
   - `pyproject.toml` → Python
   - `*.xcodeproj` or `Package.swift` → Swift
   - `build.gradle.kts` → Kotlin

6. **Create docs directory if needed:**
   ```bash
   mkdir -p docs
   ```

7. **Generate `docs/workflow.md`:**
   Based on dev-principles (from MCP/KB or built-in defaults):
   ```markdown
   # Workflow — {ProjectName}

   ## TDD Policy
   **Moderate** — Tests encouraged but not blocking. Write tests for:
   - Business logic and validation
   - API route handlers
   - Complex algorithms
   Tests optional for: UI components, one-off scripts, prototypes.

   ## Test Framework
   {from package manifest devDeps: vitest/jest/pytest/xctest}

   ## Commit Strategy
   **Conventional Commits**
   Format: `<type>(<scope>): <description>`
   Types: feat, fix, refactor, test, docs, chore, perf, style

   ## Verification Checkpoints
   **After each phase completion:**
   1. Run tests — all pass
   2. Run linter — no errors
   3. Run build — successful (if applicable)
   4. Manual smoke test

   ## Branch Strategy
   - `main` — production-ready
   - `feat/<track-id>` — feature branches
   - `fix/<description>` — hotfixes
   ```

8. **Update `CLAUDE.md`** — add workflow reference to Key Documents section if not present.

9. **Show summary and suggest next step:**
   ```
   Setup complete for {ProjectName}!

   Created:
     docs/workflow.md — TDD moderate, conventional commits

   Next: /plan "Your first feature"
   ```

## Common Issues

### CLAUDE.md not found
**Cause:** Project not scaffolded or running from wrong directory.
**Fix:** Run `/scaffold` first, or ensure you're in the project root with CLAUDE.md.

### workflow.md already exists
**Cause:** Previously set up.
**Fix:** Skill warns and asks whether to regenerate. Existing file is preserved unless you confirm overwrite.

### Wrong test framework detected
**Cause:** Multiple test frameworks in devDependencies.
**Fix:** Skill picks the first found. Edit `docs/workflow.md` manually to specify the correct framework.
