---
name: codebase-singularity
description: "Apply the codebase singularity approach: reliable codebase understanding and change with a repeatable workflow, guardrails, and verification gates. Use for repo work (feature, bugfix, refactor, migration) when you need high trust, minimal diffs, and explicit validation and exit criteria."
---

# Codebase Singularity

## Quick start
1. Collect inputs: repo path, goal, constraints, risk tolerance, and validation commands.
2. Prime: list files, read README, and inspect entry points.
3. Summarize: explain repo shape and where the change belongs; ask questions if ambiguous.
4. Plan: write a short plan with success criteria and validation steps.
5. Change: implement the smallest viable patch; avoid unrelated refactors.
6. Validate: run the requested command(s) or the closest available; record results.
7. Wrap up: report changes, evidence, risks, and next steps.

## Inputs
- Repo path and task goal.
- Constraints (files to avoid, time or risk limits, API stability).
- Validation commands (tests, lint, build, or targeted checks).

## Outputs
- Short plan with success criteria.
- Minimal patch.
- Evidence: commands run and results.
- Wrap-up: what changed, why, risks, and next steps.

## Grades (maturity ladder)

### Grade 1: Prime only
- Prime, summarize, and stop on ambiguity.

### Grade 2: Specialized roles + verification
- Add role prompts (e.g., test_writer, docs_fetcher, reviewer).
- Require a verification step for each role.

### Grade 3: Tooling expansion
- Declare required tools or services and expected outputs.
- Prefer tools over guessing (e.g., query schema instead of inferring).

### Grade 4: Closed-loop autonomy
- Run cycles: request -> validate -> resolve.
- Add hard exits: max iterations, evidence of progress, stop after repeated failures.

## Guardrails
- Keep diffs small.
- Always validate; if you cannot, say so and propose a safe next step.
- Ask before broad refactors or scope expansion.

## Templates

### Safe bugfix
```
Goal: Fix <bug> with minimal change.
Constraints: Do not modify public API; avoid touching <paths>.
Validation: Run `...` and paste output.
Exit conditions: Stop after 2 failed attempts; summarize hypotheses and logs.
Deliverables: Patch + explanation + risks.
```

### Add a feature
```
Goal: Add <feature>.
Constraints: Keep scope to <module>; no new dependencies.
Validation: Run `...`.
Deliverables: Patch + tests + short doc update.
```

## References
- Read `references/video.md` for a concise source summary.
- Read `references/transcript.md` for full context.
- Read `references/visual-notes.md` for a visual outline.
