---
name: lang-typescript
description: TypeScript language patterns and type safety rules — strict mode, no
  any, discriminated unions. Use when writing TypeScript code, reviewing types, or
  enforcing type safety.
metadata:
  category: universal
  extends: core-coding-standards
  tags:
  - typescript
  - type-safety
  - language
  status: ready
  version: 2
---

# Principles

- Enable strict mode — no implicit any, strict null checks
- Prefer discriminated unions over type assertions
- Use `unknown` over `any` — narrow with type guards

# Rules

See [rules index](rules/_sections.md) for detailed patterns.

## Examples

### Positive Trigger

User: "Replace unsafe any usage with discriminated unions in this module."

Expected behavior: Use `lang-typescript` guidance, follow its workflow, and return actionable output.

### Non-Trigger

User: "Design REST route naming conventions for a new backend."

Expected behavior: Do not prioritize `lang-typescript`; choose a more relevant skill or proceed without it.

## Troubleshooting

### Skill Does Not Trigger

- Error: The skill is not selected when expected.
- Cause: Request wording does not clearly match the description trigger conditions.
- Solution: Rephrase with explicit domain/task keywords from the description and retry.

### Guidance Conflicts With Another Skill

- Error: Instructions from multiple skills conflict in one task.
- Cause: Overlapping scope across loaded skills.
- Solution: State which skill is authoritative for the current step and apply that workflow first.

### Output Is Too Generic

- Error: Result lacks concrete, actionable detail.
- Cause: Task input omitted context, constraints, or target format.
- Solution: Add specific constraints (environment, scope, format, success criteria) and rerun.

## Workflow

1. Identify whether the request clearly matches `lang-typescript` scope and triggers.
2. Apply the skill rules and referenced guidance to produce a concrete result.
3. Validate output quality against constraints; if gaps remain, refine once with explicit assumptions.
