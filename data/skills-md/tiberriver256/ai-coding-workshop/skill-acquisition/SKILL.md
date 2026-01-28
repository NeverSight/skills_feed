---
name: skill-acquisition
description: Create, document, or revise Codex skills, including deciding when to add scripts/references/assets, structuring SKILL.md content, enforcing the 500-line rule, and updating repo references (AGENTS.md, kanban evidence).
---

# Skill Acquisition

## Scope

- Document or update a skill in this repo.
- Keep skill guidance concise while covering structure, resources, and validation.

## Workflow

1. Confirm the skill goal, triggers, and expected outputs.
2. Pick a short, hyphenated skill name (folder name and frontmatter `name` match).
3. Create `skills/<skill-name>/SKILL.md` with YAML frontmatter:
   - `name`: skill name.
   - `description`: when to use the skill and what it enables.
4. Draft the SKILL.md body in imperative form:
   - Keep to actionable steps, not general explanations.
   - Prefer short checklists and decision points.
5. Decide on bundled resources:
   - `scripts/` for repeated deterministic steps.
   - `references/` for long or variant-specific guidance.
   - `assets/` for templates or files used in outputs.
6. Enforce the 500-line rule:
   - Keep SKILL.md under 500 lines.
   - Split large guidance into `references/` and link it from SKILL.md.
   - Optionally run `scripts/check-file-lengths.sh`.
7. Update repo references:
   - Add the skill path to `AGENTS.md` (skills block).
   - Update the relevant kanban card with summary and evidence link.

## Structure Checklist

- `skills/<skill-name>/SKILL.md` exists and uses required frontmatter only.
- SKILL.md includes: scope, workflow, resource guidance, and 500-line rule.
- Resources exist only when needed; avoid unused folders.
- References are linked directly from SKILL.md (one level deep).

## Troubleshooting

- Missing init script: create the folder and SKILL.md manually.
- SKILL.md too long: move detailed sections into `references/` and link them.
- Evidence missing: add direct paths in the kanban card links section.
