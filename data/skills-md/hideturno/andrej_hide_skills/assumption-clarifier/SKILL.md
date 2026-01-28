---
name: assumption-clarifier
description: Identify hidden assumptions, contradictions, and missing info before coding; use when requirements are vague, ambiguous, or risky, and when a task needs clarification questions or explicit success criteria.
---

# Assumption Clarifier

## Quick start

- Read the request and repo context.
- List assumptions that must be true for the solution to work.
- Ask 2-5 high leverage questions.
- Propose default choices only if the user does not reply quickly.

## Procedure

1) Detect ambiguity, contradictions, or missing constraints.
2) Separate facts (given) from guesses (assumptions).
3) Ask for missing inputs that change architecture, data, or risk.
4) State success criteria in simple, testable terms.
5) If the user wants speed, proceed with safe defaults and say them.

## Output format

- Assumptions: 3-7 bullets.
- Questions: 2-5 bullets.
- Success criteria: 2-4 bullets.
- Defaults (if needed): short list with rationale.

## Guardrails

- Do not over-ask; only ask questions that change the plan.
- Do not invent constraints; label every guess as a guess.
- If the user says "ship", pick conservative defaults and move on.
