---
name: skill-innovation-retrospective
description: Detect improvement opportunities after task completion, blockers, or quality feedback; produce an Innovation Retrospective and always ask for confirmation before running $skill-creator. Apply across all tasks and conversations.
---

# Skill Innovation Retrospective

## Purpose
- Detect skill gaps, quality issues, user suggestions, or repeated friction.
- Recommend updating an existing skill or creating a new one.
- Never modify or create skills automatically.

## Triggers
- Task finished (final output delivered or conversation clearly done).
- Task blocked or issues encountered (errors, tool failure, uncertainty, partial completion, or multiple clarification loops).
- Quality feedback (user dissatisfaction, redo/refactor request, "wrong/missed/didn't follow").

## Signals to Look For
- Quality: negative sentiment, format mismatch, missing constraints, incorrect facts/outdated info,
  missing citations where required, hallucination risk.
- Process: too many clarifying questions, forgot constraints, no plan/options when needed.
- Tooling: tool errors, wrong tool usage, missing troubleshooting steps.
- User contribution: suggested better workflow/template/tone.
- Additional must-include cases: unclear skill steps, insufficient edge cases, cross-skill conflict,
  recurring task type, domain nuance, delivery-model nuance.

## Output (Innovation Retrospective)
- Observed Signals (bulleted, brief paraphrase).
- Root Cause Hypothesis (1-3 bullets).
- Recommendation: update existing skill or create new skill.
- Proposed Change Summary: additions/removals/clarifications; checklist/guardrails/examples;
  new skill scope/triggers/standardization.
- Ask for Confirmation (mandatory): "Do you want me to run $skill-creator to (create/update)
  the skill now?"
- Keep concise (8-20 lines unless user asks for more).

## Decide Update vs Create
- Update if within scope of existing skill and needs clarity/guardrails/examples/edge cases.
- Create if no existing skill fits or pattern recurs and needs standardized structure.

## If User Confirms: Use $skill-creator Workflow
1) Identify target: existing skill name/path or proposed new skill name/path (e.g.,
   `.codex/skills/<name>.md`).
2) Prepare change package: title, problem statement, triggers, inputs/outputs, step-by-step
   algorithm, guardrails/anti-patterns, at least one positive and one negative example, and a
   Definition of Done checklist.
3) Confirm again if scope is large or impacts many conversations.
4) Execute $skill-creator; summarize changes and improvements.
- Never run $skill-creator without explicit confirmation.
- Never include sensitive or personal data in examples.

## Anti-patterns
- Don't derail the main answer; run only at end or on issue/feedback.
- Don't produce long essays or blame the user.
- Don't propose changes without evidence.
- Don't auto-edit skills without approval.
