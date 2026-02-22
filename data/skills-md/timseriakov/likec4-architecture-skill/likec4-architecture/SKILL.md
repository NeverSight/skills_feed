---
name: likec4-architecture
description: Builds and maintains software architecture as code with LikeC4 DSL. Use when requests mention architecture diagrams, C4 context/container/component views, system landscapes, dependency maps, integration maps, or architecture generated from code. Applies to creating new `.c4`/`.likec4` models, updating existing models, validating with LikeC4 CLI, and preparing preview/build/export outputs.
---

# LikeC4 Architecture

Creates and updates LikeC4 architecture models that stay executable and reviewable.

## Workflow

1. Scope the model:
- Identify system boundary and audience.
- Start with context and container views unless a different view set is requested.

2. Load DSL guidance before editing:
- If building from scratch or changing notation, read `references/likec4-dsl-quickstart.md` first.
- If choosing architecture shape, read `references/likec4-patterns.md`.
- If feature usage is unclear, check `references/likec4-capabilities-reference.md` and follow official docs links.

3. Locate or bootstrap model files:
- Reuse existing `.c4`/`.likec4` files when present.
- If missing, copy starter from `assets/likec4-starter/docs/architecture/model.c4` to project `docs/architecture/model.c4`.

4. Model structure before visuals:
- Define stable element IDs and meaningful names.
- Add explicit directional relationships with short labels.
- Add technology/description fields where useful.

5. Keep views focused:
- Create small, purposeful views.
- Split crowded diagrams by domain, team, or bounded context.

6. Validate and package:
- Run `npx likec4 validate` and fix all errors.
- Provide `npx likec4 start` preview command.
- If requested, provide build/export commands.

## Quality Gates

- Avoid unlabeled ambiguous relationships.
- Avoid orphan elements that never appear in views.
- Prefer domain names over implementation-noise names.
- Finish only after successful CLI validation.

## Command Set

```sh
npx likec4 validate
npx likec4 start
npx likec4 build -o ./dist
npx likec4 export png -o ./assets/architecture
```

## Output Contract

When architecture files change, return:

1. Changed files.
2. Validation result.
3. One-line purpose for each view.
4. Relevant preview/build/export command(s).

## References

- DSL quickstart: `references/likec4-dsl-quickstart.md`
- Architecture patterns: `references/likec4-patterns.md`
- Capabilities map: `references/likec4-capabilities-reference.md`
- Checklist: `references/likec4-checklist.md`
- Examples: `references/examples.md`
- Starter template: `assets/likec4-starter/docs/architecture/model.c4`
