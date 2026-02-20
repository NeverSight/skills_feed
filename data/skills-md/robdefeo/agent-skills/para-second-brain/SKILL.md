---
name: para-second-brain
description: Use this skill when the user wants to organize, classify, or maintain a PARA-method second brain. Triggers include asking where to file something, distinguishing projects from areas, processing an inbox, setting up a new project, completing or archiving a project, running a monthly review, validating system structure, or finding stale/orphaned content.
---

# PARA Method

Use this skill to help users organize and maintain a second brain using the PARA system (Projects, Areas, Resources, Archives).

## Routing

Pick the entry point based on user intent:

- Classification and "where does this go?" questions: read `references/decision-trees.md`
- Example requests and edge-case comparisons: read `references/examples.md`
- Operational process requests (inbox, review, setup, close-out, archive): read `references/workflows.md`
- Troubleshooting pain points and validation guidance: read `references/common-problems.md`

If the request is broad or does not clearly match one route, default to `references/decision-trees.md`.

## Output Convention

- Classification guidance and Q&A: answer in chat
- Validation workflows: run `scripts/validate.sh` and write report output to `PARA-validation-YYYY-MM-DD.md` in the current working directory
- Installation location: out of scope for this skill; installation is handled by separate tooling

## Terminology

- Use "second brain" for the user's vault/folder structure
- Use "PARA system" only for the method/framework

## Validation Workflow

When the user asks to validate structure or project health:

1. Read `references/common-problems.md` for interpretation guidance.
2. Run `scripts/validate.sh <path>` (or omit path to use current directory).
3. Save report output to `PARA-validation-YYYY-MM-DD.md` if user wants a file.
4. Summarize critical findings and recommended next actions.
