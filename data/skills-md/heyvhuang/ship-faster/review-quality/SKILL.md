---
name: review-quality
description: "Unified codebase quality review: merge readiness verdict + maintainability (Clean Code) + docs-vs-code consistency. Use for code review, quality check, refactor check, outdated docs check, or merge/production readiness."
---

# Quality Review (Unified)

Goal: turn “is this change good?” into a **repeatable review** with a clear **merge/production readiness** verdict.

This skill intentionally merges three review lenses:

1) **Merge readiness** (requirements alignment + risk + verification)
2) **Code maintainability** (Clean Code-style review)
3) **Documentation consistency** (README/docs vs implementation)

This is the **single entry point** for Ship Faster reviews. It includes an internal auto-triage:
- Always run the unified review (this skill).
- If React/Next.js performance risk is detected, also run `review-react-best-practices` and include its findings.
- If UI surface changes are detected, also run a Web Interface Guidelines audit (a11y/focus/forms/motion/content overflow) and include terse `file:line` findings.

## Inputs (recommended)

- `BASE_SHA` and `HEAD_SHA` for diff-based reviews
- Optional: `PLAN_OR_REQUIREMENTS` path (e.g. `run_dir/evidence/features/<feature_slug>-plan.md`)
- Optional: docs scope (`README.md`, `docs/**`, API contracts)
- Optional: `run_dir` (Ship Faster run directory, if available)

### Suggested scope commands

```bash
# Baseline: main/master merge-base
BASE_SHA=$(git merge-base HEAD main 2>/dev/null || git merge-base HEAD master)
HEAD_SHA=$(git rev-parse HEAD)

git diff --stat "$BASE_SHA..$HEAD_SHA"
git diff "$BASE_SHA..$HEAD_SHA"
```

## Process

### 0) Auto-triage (Built-in Router)

Goal: reduce user choice. The reviewer decides which specialized review lens to apply, deterministically, based on the diff.

Collect signals (minimum):

```bash
git diff --name-only "$BASE_SHA..$HEAD_SHA"
git diff --stat "$BASE_SHA..$HEAD_SHA"
git diff "$BASE_SHA..$HEAD_SHA"
```

Routing rules (apply in order):

1) **Docs-only change** (fast path):
   - If every changed file is in `docs/**` or ends with `.md|.txt|.rst`
   - Then run the unified review, but focus on **Docs ↔ Code consistency** + **release risk** (skip deep code maintainability unless docs reference code changes).

2) **React/Next.js performance-sensitive change**:
   - If any changed file matches:
     - `**/*.tsx`, `**/*.jsx`
     - `next.config.*`, `app/**`, `pages/**`, `src/app/**`, `src/pages/**`
     - React/Next entrypoints (`layout.tsx`, `page.tsx`, `middleware.ts`, `route.ts`, `loading.tsx`)
   - Or the diff contains performance-sensitive keywords (spot check via `git diff`):
     - `use client`, `Suspense`, `dynamic(`, `next/dynamic`, `next/navigation`, `React.cache`, `revalidate`, `fetch(`, `headers()`, `cookies()`
   - Then: run `review-react-best-practices` and include its output (or link to its artifact) in the final report.

3) **UI Web Interface Guidelines audit** (a11y/UX rules, terse output):
   - If any changed file matches:
     - UI code: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.html`, `**/*.css`, `**/*.scss`
     - Common UI dirs: `app/**`, `pages/**`, `src/app/**`, `src/pages/**`, `components/**`, `src/components/**`
   - Then: fetch the latest Web Interface Guidelines and audit only the changed UI files first.
     - Source: `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`
     - Fetch method: WebFetch (if available) or `curl -fsSL <url>`
   - Output findings in **terse `file:line` format**, grouped by file (high signal, low prose). Treat a11y + focus issues as higher severity than cosmetic issues.

Output requirement (at top of your report):

```md
## Triage
- Docs-only: yes|no
- React/Next perf review: yes|no
- UI guidelines audit: yes|no
- Reason: <1-3 bullets based on file paths / patterns>
```

### 1) Merge readiness (verdict review)

Use the template: `references/code-reviewer.md`.

Minimum checks:
- Requirements alignment (acceptance criteria hit, non-goals respected)
- Side effects are gated (deploy/payments/DB writes require explicit approval)
- Error handling is explicit (no silent failures)
- Verification evidence exists (tests/build/typecheck/lint/manual steps)

### 2) Clean Code maintainability scan

Review the diff (and nearby touched code) across these dimensions:

1. **Meaningful naming** (avoid `data1`, `tmp`, mixed naming for same concept)
2. **Small functions / SRP** (very long functions, too many params, mixed responsibilities)
3. **Duplication (DRY)** (copy/paste logic, repeated transformations/validation)
4. **Over-engineering (YAGNI)** (unused branches, unnecessary abstractions)
5. **Magic numbers / strings** (hardcoded values without semantic constants)
6. **Structural clarity** (deep nesting, unreadable one-liners, nested ternaries)
7. **Project conventions** (imports/order/style consistency)

### 3) Docs ↔ code consistency scan

Check that docs do not lie:
- Enumerate: `README.md`, `docs/**/*.md`, config examples, env keys, API contracts
- For each claim/config/example: locate the authoritative code/config/contracts
- Record mismatches with evidence (doc location + code location)

## Output (required)

Produce a structured report:

- `quality-review.md`
- `quality-review.json` (optional but recommended)

If you are working inside a Ship Faster run directory, write to:
- `run_dir/evidence/quality-review.md`
- `run_dir/evidence/quality-review.json`

If triage selects React/Next performance review and a Ship Faster `run_dir` is available, also persist:
- `run_dir/evidence/react-best-practices-review.md`

If triage selects UI guidelines audit and a Ship Faster `run_dir` is available, also persist:
- `run_dir/evidence/ui-guidelines-review.md` (terse `file:line` findings, grouped by file)

## Output format (recommended)

```md
## Summary
- Verdict: Ready / With fixes / Not ready
- Scope: BASE_SHA..HEAD_SHA (or file list)

## Triage
- Docs-only: yes|no
- React/Next perf review: yes|no
- UI guidelines audit: yes|no
- Reason: ...

## Strengths
- ...

## Issues
### Critical (Must Fix)
- Location: path:line
  - What
  - Why it matters
  - Minimal fix

### Important (Should Fix)
...

### Minor (Nice to Have)
...

## UI Guidelines (terse, only if audit=yes)
- path:line <finding>
- path:line <finding>
```
