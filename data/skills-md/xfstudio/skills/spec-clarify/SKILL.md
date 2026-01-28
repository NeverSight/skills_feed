---
name: spec-clarify
description: Identify underspecified areas in a feature spec by asking up to 5 targeted clarification questions and encoding answers into the spec. Use when user says "/spec-clarify", "clarify the spec", or after /spec-specify to reduce ambiguity before /spec-plan.
---

# Spec-Clarify

Reduce ambiguity in specifications through targeted questioning.

**Prerequisites**: Feature spec must exist (run `/spec-specify` first).

## Workflow

1. **Initialize** - Run `.specify/scripts/bash/check-prerequisites.sh --json --paths-only`
2. **Load spec** - Read spec.md
3. **Scan ambiguity** - Analyze coverage taxonomy
4. **Generate questions** - Max 5, prioritized by impact
5. **Question loop** - Present ONE at a time with recommendation
6. **Integrate answers** - Update spec after each answer
7. **Report** - Output summary and next steps

## Ambiguity Taxonomy

Categories to scan (mark Clear/Partial/Missing):

| Category | Check For |
|----------|-----------|
| Functional Scope | User goals, out-of-scope, personas |
| Data Model | Entities, relationships, constraints |
| UX Flow | Journeys, error states, accessibility |
| Non-Functional | Performance, security, observability |
| Integration | External APIs, formats, versioning |
| Edge Cases | Negative scenarios, rate limits |

## Question Format

**Multiple Choice:**
```markdown
**Recommended:** Option A - <reasoning>

| Option | Description |
|--------|-------------|
| A | Option A |
| B | Option B |
| Short | Custom answer (<=5 words) |
```

**Short Answer:**
```markdown
**Suggested:** <answer> - <reasoning>
Format: <=5 words. Say "yes" or provide your own.
```

## Integration Rules

After each answer:
1. Add `## Clarifications` section if missing
2. Add `### Session YYYY-MM-DD` subheading
3. Append: `- Q: <question> → A: <answer>`
4. Update relevant spec section
5. Save immediately

## Constraints

- Max 5 questions asked
- Max 10 questions total across session
- Respect "done", "stop", "proceed" signals

## Next Steps

After `/spec-clarify`:
- `/spec-plan` - Create technical plan
