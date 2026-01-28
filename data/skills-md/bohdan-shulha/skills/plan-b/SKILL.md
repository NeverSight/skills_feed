---
name: plan-b
description: Create a concise plan for coding/build tasks, especially when users say "I want to make..." or "I need to do...". Use to generate a final plan by aggregating multiple subagent plan variants, include ASCII diagrams/flows/UI mockups when possible, and follow the create-plan style (read-only scan, minimal questions).
---

# Plan B

## Overview

Produce a strong, concise plan by combining multiple plan variants from subagents, then synthesize a single best plan with an ASCII diagram.

## Workflow (follow in order)

1. **Scan context quickly (read-only)**
   - Read `README.md` and obvious docs (`docs/`, `CONTRIBUTING.md`, `ARCHITECTURE.md`).
   - Skim relevant files (likely touchpoints).
   - Identify constraints (language, frameworks, CI/test commands, deployment shape).

2. **Ask follow-ups only if blocking**
   - Ask **at most 1-2 questions**.
   - Only ask if you cannot responsibly plan without the answer; prefer multiple-choice.
   - If unsure but not blocked, make a reasonable assumption and proceed.

3. **Spawn subagents for plan variants**
   - Spawn **at least 3 subagents** to draft independent plan variants.
   - Give each a different focus, for example:
     - Variant A: architecture/structure emphasis
     - Variant B: testing/risks/edge cases emphasis
     - Variant C: scope trimming/prioritization emphasis
   - Instruct each subagent to use the plan template below and include an ASCII diagram.

4. **Judge and synthesize**
   - Evaluate variants for coverage, risk handling, testability, clarity, and concision.
   - Compose a single best plan by merging the strongest parts.
   - **Do not output** subagent drafts; only output the final plan.

5. **Output the final plan only**
   - Do not preface with meta explanations.
   - Always include an ASCII diagram (flow/architecture/UI mockup).
   - Include test/validation and edge-case/risk items when applicable.

## ASCII diagram guidance

- Always include a diagram, even if simple.
- Use a flow (requirements -> design -> implement -> test) or a box layout.
- For UI work, use a quick ASCII mockup.
- Keep it in a fenced `text` code block.

## Plan template (follow exactly)

```markdown
# Plan

<1-3 sentences: what we are doing, why, and the high-level approach.>

## Diagram (ASCII)
```text
<diagram here>
```

## Scope
- In:
- Out:

## Action items
[ ] <Step 1>
[ ] <Step 2>
[ ] <Step 3>
[ ] <Step 4>
[ ] <Step 5>
[ ] <Step 6>

## Open questions
- <Question 1>
- <Question 2>
- <Question 3>
```

## Checklist item guidance

Good checklist items:
- Point to likely files/modules: `src/...`, `app/...`, `services/...`
- Name concrete validation: "Run npm test", "Add unit tests for X"
- Include safe rollout when relevant: feature flag, migration plan, rollback note

Avoid:
- Vague steps ("handle backend", "do auth")
- Too many micro-steps
- Writing code snippets (keep the plan implementation-agnostic)
