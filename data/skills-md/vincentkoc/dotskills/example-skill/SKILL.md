---
name: example-skill
description: Template skill for repository authors; excluded from public publishing.
license: Proprietary
metadata:
  internal: true
  version: "1.0.0"
---

# Example Skill

## Purpose

Provide a spec-aligned template for creating consistent, reusable skills.

## When to use

- You are adding a new skill to this repository.
- You want a starter structure with required sections.

## Workflow

1. State the objective in one sentence.
2. Collect only required inputs.
3. Execute deterministic steps.
4. Load deeper context only when needed:
   - `references/REFERENCE.md`
   - `assets/output-template.md`
   - `agents/openai.yaml`
5. Return output in a stable format.
6. Use `scripts/example-check.sh` for a deterministic preflight check.

## Inputs

- Task objective
- Constraints
- Output destination

## Outputs

- Primary deliverable
- Follow-up checks

## Examples

- Build a new skill skeleton with required sections and valid frontmatter.
- Refactor an existing skill to move deep details into `references/`.
- Add deterministic checks under `scripts/` for repeatable verification.

## Edge cases

- Missing frontmatter fields: stop and add required fields first.
- Invalid `name` format: normalize to lowercase-hyphen and match directory name.
- Broken resource paths: fix links so all referenced files exist.

## Guardrails

- Keep instructions concrete and testable.
- Avoid unnecessary context loading.
- Prefer deterministic commands over manual steps.
- Keep file references one level deep from `SKILL.md`.
