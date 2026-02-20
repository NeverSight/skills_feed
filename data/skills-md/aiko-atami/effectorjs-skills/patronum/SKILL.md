---
name: patronum
description: Select and apply Patronum operators for Effector code with minimal, practical v2.x examples. Use when tasks involve choosing between Patronum operators, composing reactive state flows, replacing manual sample/combine boilerplate with Patronum utilities, explaining operator signatures and return types, or adapting legacy Patronum usage to modern v2 shorthand and import patterns.
---

# Patronum Skill

Use this skill to solve Patronum usage questions quickly and consistently.
Target Patronum v2.x by default.

## Workflow

1. Classify request:
- `operator-choice`: choose one or several operators for a task.
- `api-explain`: explain signature, overloads, and return value.
- `compose`: combine multiple operators into one flow.
- `debug`: use `debug` and scope-aware debugging notes.
- `migration`: map legacy forms to modern usage.

2. Load references progressively:
- Start with `references/operator-matrix.md`.
- Add `references/recipes.md` for task-to-solution mapping.
- Add `references/pitfalls.md` for caveats and anti-patterns.
- Add `references/migration-notes.md` when legacy forms appear.

3. Build answer contract:
- Start with decision: selected operator(s) and why.
- Provide minimal practical snippet.
- Add caveats (imports, overload differences, behavior traps).
- For uncertain versions, explicitly state v2 assumption and show migration note.

## Defaults

- Prefer Patronum v2.x shorthand where available.
- Prefer concise examples with explicit imports.
- Keep examples deterministic and composable with Effector primitives.
- Prefer `patronum/<operator-kebab-name>` imports when clarity matters.

## Guardrails

- Do not suggest outdated signatures as default.
- Do not invent operators outside the official list.
- Do not hide behavior differences between overloads.
- Do not skip edge cases for `pending`, `condition`, `interval`, `time`, and `debug`.

## Output Template

Use this structure in answers:

1. `Use <operator>`: one-line reason.
2. `Example`: minimal code block.
3. `Caveats`: version or overload notes.
