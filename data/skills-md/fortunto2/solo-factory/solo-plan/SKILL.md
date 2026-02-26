---
name: solo-plan
description: Explore codebase and create spec + phased implementation plan with file-level task breakdown. Use when user says "plan this feature", "create implementation plan", "write a spec", "battle plan", or describes a feature/bug/refactor. Zero questions — researches code instead. Do NOT use for idea validation (use /validate) or execution (use /build).
license: MIT
metadata:
  author: fortunto2
  version: "2.2.1"
  openclaw:
    emoji: "📋"
allowed-tools: Read, Grep, Bash, Glob, Write, Edit, AskUserQuestion, mcp__solograph__session_search, mcp__solograph__project_code_search, mcp__solograph__codegraph_query, mcp__solograph__codegraph_explain, mcp__solograph__kb_search, mcp__solograph__web_search, mcp__context7__resolve-library-id, mcp__context7__query-docs
argument-hint: "<task description>"
---

# /plan

This skill is self-contained — follow the steps below instead of delegating to external planning skills (superpowers, etc.).

Research the codebase and create a spec + phased implementation plan. Zero interactive questions — explores the code instead.

## When to use

Creates a track for any feature, bug fix, or refactor with a concrete, file-level implementation plan. Works with or without `/setup`.

## MCP Tools (use if available)

- `session_search(query)` — find similar past work in Claude Code chat history
- `project_code_search(query, project)` — find reusable code across projects
- `codegraph_query(query)` — check dependencies of affected files
- `codegraph_explain(project)` — architecture overview: stack, languages, directory layers, key patterns, top dependencies, hub files
- `kb_search(query)` — search knowledge base for relevant methodology

If MCP tools are not available, fall back to Glob + Grep + Read.

## Steps

1. **Parse task description** from `$ARGUMENTS`.
   - If empty, ask via AskUserQuestion: "What feature, bug, or refactor do you want to plan?"
   - This is the ONE question maximum.

2. **Detect context** — determine where plan files should be stored:

   **Project context** (normal project with code):
   - Detected by: `package.json`, `pyproject.toml`, `Cargo.toml`, `*.xcodeproj`, or `build.gradle.kts` exists in working directory
   - Plan path: `docs/plan/{trackId}/`

   **Knowledge base context** (documentation-centric project):
   - Detected by: NO package manifest found, BUT directories like `docs/`, `notes/`, or structured numbered directories exist
   - Plan path: `docs/plan/{shortname}/`
   - Note: the shortname is derived from the task (kebab-case, no date suffix for the directory)

   Set `$PLAN_ROOT` based on detected context. All subsequent file paths use `$PLAN_ROOT`.

3. **Load project context** (parallel reads):
   - `CLAUDE.md` — architecture, constraints, Do/Don't
   - `docs/prd.md` — what the product does (if exists)
   - `docs/workflow.md` — TDD policy, commit strategy (if exists)
   - `package.json` or `pyproject.toml` — stack, versions, deps

3. **Auto-classify track type** from keywords in task description:
   - Contains "fix", "bug", "broken", "error", "crash" → `bug`
   - Contains "refactor", "cleanup", "reorganize", "migrate" → `refactor`
   - Contains "update", "upgrade", "bump" → `chore`
   - Default → `feature`

4. **Research phase** — explore the codebase to understand what needs to change:

   a. **Get architecture overview** (if MCP available — do this FIRST):
      ```
      codegraph_explain(project="{project name from CLAUDE.md or directory name}")
      ```
      Gives you: stack, languages, directory layers, key patterns, top dependencies, hub files.

   b. **Find relevant files** — Glob + Grep for patterns related to the task:
      - Search for keywords from the task description
      - Look at directory structure to understand architecture
      - Identify files that will need modification

   c. **Precedent retrieval** (context graph pattern — search past solutions BEFORE planning):
      - Search past sessions (if MCP available):
        ```
        session_search(query="{task description keywords}")
        ```
        Look for: how similar tasks were solved, what went wrong, what patterns worked.
      - Search KB for relevant methodology:
        ```
        kb_search(query="{task type}: {keywords}")
        ```
        Check for: harness patterns, architectural constraints, quality scores.

   d. **Search code across projects** (if MCP available):
      ```
      project_code_search(query="{relevant pattern}")
      ```

   e. **Check dependencies** of affected files (if MCP available):
      ```
      codegraph_query(query="MATCH (f:File {path: '{file}'})-[:IMPORTS]->(dep) RETURN dep.path")
      ```

   f. **Read existing tests** in the affected area — understand testing patterns used.

   g. **Read CLAUDE.md** architecture constraints — understand boundaries and conventions.
      - Check for harness section: module boundaries, data validation rules, lint configs.
      - Read `docs/ARCHITECTURE.md` and `docs/QUALITY_SCORE.md` if they exist.

   h. **Detect deploy infrastructure** — search for deploy scripts/configs to include deploy phase in plan:
      ```bash
      find . -maxdepth 3 \( -name 'deploy.sh' -o -name 'Dockerfile' -o -name 'docker-compose.yml' -o -name 'fly.toml' -o -name 'wrangler.toml' \) -type f 2>/dev/null
      ```
      If found, read them to understand deploy targets. Include a deploy phase in the plan with concrete commands.

5. **Generate track ID:**
   - Extract a short name (2-3 words, kebab-case) from task description.
   - Format: `{shortname}_{YYYYMMDD}` (e.g., `user-auth_20260209`).

6. **Create track directory:**
   ```bash
   mkdir -p $PLAN_ROOT
   ```
   - Project context: `docs/plan/{trackId}/`
   - KB context: `docs/plan/{shortname}/`

7. **Generate `$PLAN_ROOT/spec.md`:**
   Based on research findings, NOT generic questions.
   ```markdown
   # Specification: {Title}

   **Track ID:** {trackId}
   **Type:** {Feature|Bug|Refactor|Chore}
   **Created:** {YYYY-MM-DD}
   **Status:** Draft

   ## Summary
   {1-2 paragraph description based on research}

   ## Acceptance Criteria
   - [ ] {concrete, testable criterion}
   - [ ] {concrete, testable criterion}
   {3-8 criteria based on research findings}

   ## Dependencies
   - {external deps, packages, other tracks}

   ## Out of Scope
   - {what this track does NOT cover}

   ## Technical Notes
   - {architecture decisions from research}
   - {relevant patterns found in codebase}
   - {reusable code from other projects}
   ```

8. **Generate `$PLAN_ROOT/plan.md`:**
   Concrete, file-level plan from research. Keep it tight: 2-4 phases, 5-15 tasks total.

   **Critical format rules** (parsed by `/build`):
   - Phase headers: `## Phase N: Name`
   - Tasks: `- [ ] Task N.Y: Description` (with period or detailed text)
   - Subtasks: indented `  - [ ] Subtask description`
   - All tasks use `[ ]` (unchecked), `[~]` (in progress), `[x]` (done)

   ```markdown
   # Implementation Plan: {Title}

   **Track ID:** {trackId}
   **Spec:** [spec.md](./spec.md)
   **Created:** {YYYY-MM-DD}
   **Status:** [ ] Not Started

   ## Overview
   {1-2 sentences on approach}

   ## Phase 1: {Name}
   {brief description of phase goal}

   ### Tasks
   - [ ] Task 1.1: {description with concrete file paths}
   - [ ] Task 1.2: {description}

   ### Verification
   - [ ] {what to check after this phase}

   ## Phase 2: {Name}
   ### Tasks
   - [ ] Task 2.1: {description}
   - [ ] Task 2.2: {description}

   ### Verification
   - [ ] {verification steps}

   {2-4 phases total}

   ## Phase {N-1}: Deploy (if deploy infrastructure exists)
   _Include this phase ONLY if the project has deploy scripts/configs (deploy.sh, Dockerfile, docker-compose.yml, fly.toml, wrangler.toml, vercel.json). Skip if no deploy infra found._

   ### Tasks
   - [ ] Task {N-1}.1: {concrete deploy step — e.g. "Run python/deploy.sh to push Docker image to VPS", "wrangler deploy", etc.}
   - [ ] Task {N-1}.2: Verify deployment — health check, logs, HTTP status

   ### Verification
   - [ ] Service is live and healthy
   - [ ] No runtime errors in production logs

   ## Phase {N}: Docs & Cleanup
   ### Tasks
   - [ ] Task {N}.1: Update CLAUDE.md with any new commands, architecture changes, or key files
   - [ ] Task {N}.2: Update README.md if public API or setup steps changed
   - [ ] Task {N}.3: Remove dead code — unused imports, orphaned files, stale exports

   ### Verification
   - [ ] CLAUDE.md reflects current project state
   - [ ] Linter clean, tests pass

   ## Final Verification
   - [ ] All acceptance criteria from spec met
   - [ ] Tests pass
   - [ ] Linter clean
   - [ ] Build succeeds
   - [ ] Documentation up to date

   ---
   _Generated by /plan. Tasks marked [~] in progress and [x] complete by /build._
   ```

   **Plan quality rules:**
   - Every task mentions specific file paths (from research).
   - Tasks are atomic — one commit each.
   - Phases are independently verifiable.
   - Total: 5-15 tasks (not 70).
   - **Last phase is always "Docs & Cleanup"**.
   - **Harness-aware:** if the task introduces new patterns, include a task to update lint rules or CLAUDE.md constraints. If it touches module boundaries, include verification of dependency direction. Think: "what harness change prevents future agents from breaking this?"

9. **Create progress task list** for pipeline visibility:

   After writing plan.md, create TaskCreate entries so progress is trackable:
   - One task per phase: "Phase 1: {name}" with task list as description.
   - This gives the user and pipeline real-time visibility into what's planned.
   - `/build` will update these tasks as it works through them.

   If `superpowers:writing-plans` skill is available, follow its granularity format: bite-sized tasks (2-5 minutes each), complete code in task descriptions, exact file paths, verification steps per task. This enhances the built-in format above.

10. **Show plan for approval** via AskUserQuestion:
   Present the spec summary + plan overview. Options:
   - "Approve and start" — ready for `/build`
   - "Edit plan" — user wants to modify before implementing
   - "Cancel" — discard the track

   If "Edit plan": tell user to edit `$PLAN_ROOT/plan.md` manually, then run `/build`.

## Output

```
Track created: {trackId}

  Type:   {Feature|Bug|Refactor|Chore}
  Phases: {N}
  Tasks:  {N}
  Spec:   $PLAN_ROOT/spec.md
  Plan:   $PLAN_ROOT/plan.md

Research findings:
  - {key finding 1}
  - {key finding 2}
  - {reusable code found, if any}

Next: /build {trackId}
```

## Rationalizations Catalog

These thoughts mean STOP — you're skipping research:

| Thought | Reality |
|---------|---------|
| "I know this codebase" | You know what you've seen. Search for what you haven't. |
| "The plan is obvious" | Obvious plans miss edge cases. Research first. |
| "Let me just start coding" | 10 minutes of research prevents 2 hours of rework. |
| "This is a small feature" | Small features touch many files. Map the blast radius. |
| "I'll figure it out as I go" | That's not a plan. Write the file paths first. |
| "70 tasks should cover it" | 5-15 tasks. If you need more, split into tracks. |

## Compatibility Notes

- Plan format must match what `/build` parses: `## Phase N:`, `- [ ] Task N.Y:`.
- `/build` reads `docs/workflow.md` for TDD policy and commit strategy (if exists).
- If `docs/workflow.md` missing, `/build` uses sensible defaults (moderate TDD, conventional commits).

## Common Issues

### Plan has too many tasks
**Cause:** Feature scope too broad or tasks not atomic enough.
**Fix:** Target 5-15 tasks across 2-4 phases. Split large features into multiple tracks.

### Context detection wrong (project vs KB)
**Cause:** Directory has both code manifests and KB-style directories.
**Fix:** Project context takes priority if `package.json`/`pyproject.toml` exists.

### Research phase finds no relevant code
**Cause:** New project with minimal codebase or MCP tools unavailable.
**Fix:** Skill falls back to Glob + Grep. For new projects, the plan will rely more on CLAUDE.md architecture and stack conventions.
