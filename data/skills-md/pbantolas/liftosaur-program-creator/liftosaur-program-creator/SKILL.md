---
name: liftosaur-program-creator
description: Creates and edits Liftosaur workout programs using Liftoscript. Use for program authoring, exercise/set changes, progression setup (lp/dp/sum/custom), advanced custom progression logic, custom progress/update script debugging, and reuse/template refactors.
---

# Liftoscript Program Authoring

## Output contract

- Default to slash-style format for new lines: `Exercise Name / set expressions / section: value / section: value`.
- Keep one separator style per line; do not mix slash and freeform section placement.
- Preserve existing local style when editing unless the user asks to normalize.
- Use explicit section names for non-set data (`progress:`, `update:`, `warmup:`, `superset:`, `used:`, `id:`).

## Operating rules

- Keep terminology consistent: use "exercise line", "set", "progress", "update", "state variable", "set variation".
- Prefer built-in progression (`lp`, `dp`, `sum`) before custom scripts.
- For scripting tasks, identify execution context first: `progress: custom()` vs `update: custom()`.
- Use timer literals by context: `45s`/`120s` in exercise-line sets, numeric timers in scripts (`timers[5] = 20`).
- Reject timed rep tokens in set syntax (`3x60s`); use numeric reps (`3x60`) when needed.
- Resolve units deterministically: nearby program text -> explicit user preference -> default `kg`.
- Do not silently mix `kg` and `lb` in one generated snippet.
- In exercise-line set syntax, `%` load tokens are percentages of `1RM` (not training max).
- Resolve exercise naming from `references/exercise-name-resolution.md` against `references/exercise-list.md`.
- In full mode, place template lines (`used: none`) inside a day block; for week-level templates, anchor after `## Day 1`, not directly after `# Week N`.
- Apply a validation loop: draft -> verify writable variables/scope/indexing -> correct -> finalize.
- Preserve user intent and existing structure; change only what is required.

## Routing by task

- Basic syntax and set notation -> `references/language-core.md`
- Weeks, days, comments, labels, warmups, supersets, tags -> `references/program-structure.md`
- Built-in progression choice and arguments -> `references/progression-builtins.md`
- Reuse, repeat, templates, overrides -> `references/reuse-and-templates.md`
- `progress: custom()` authoring -> `references/custom-progress-scripts.md`
- `update: custom()` authoring -> `references/update-scripts.md`
- Read/write variables and indexing rules -> `references/runtime-reference.md`
- Liftoscript built-in functions -> `references/builtins-reference.md`
- End-to-end examples and fix patterns -> `references/recipes.md`
- Exercise name resolution -> `references/exercise-name-resolution.md`
- Known pitfalls and quick fixes -> `references/common-failure-modes.md`

## Minimal workflow

1. Classify request: syntax, progression, reuse, custom script, or debug.
2. Identify mode before drafting: edit existing text vs generate new text; for scripts, choose `progress` vs `update` context.
3. Resolve units before drafting: nearby text -> user preference -> `kg`.
4. Read only the minimum references required (target 1-2 files from routing list).
5. Produce the smallest correct change.
6. Validate constraints (especially writable variables and index scope).
7. Return final program/script text and a short rationale.

## Preflight validator (must pass before final output)

- Section separators are correct and consistent for each exercise line.
- Set and set-variation syntax is structurally valid (including grouped load/timer behavior when used).
- Script assignments target writable variables for the selected context.
- Script assignment literals use valid types for the target variable.
- Timer literals follow context rules (`45s` in exercise text, numeric in scripts).
- Rep tokens are numeric counts (no `s` suffix on reps; use `3x60`, not `3x60s`).
- Percent load tokens in exercise-line set syntax are interpreted as `% of 1RM`.
- Units are resolved from context/user preference or defaulted to `kg`.
- No forbidden unit mismatches in generated output.
- Exercise naming resolves against `references/exercise-list.md` (bare `Exercise Name` or explicit `Exercise Name, Equipment`).
- When user intent specifies equipment/variant, explicit `Exercise Name, Equipment` is an exact match in `references/exercise-list.md`.
- When user intent does not specify equipment, alias-only `Exercise Name` is an exact bare-name match in `references/exercise-list.md`.
- If exercise is not in built-in list, output remains valid and mentions manual add path in Liftosaur.
- In full mode output, template lines (`used: none`) are placed after `## Day 1` (or another explicit day), never directly under `# Week N`.
