---
name: agent-estimation
description: Accurately estimate AI agent work effort using the agent's own operational units (tool-call rounds) instead of human time. Use when asked to estimate, scope, plan, or evaluate how long a coding task will take. Prevents the common failure mode where agents anchor to human developer timelines and massively overestimate. Outputs a structured breakdown with round counts, risk factors, and a final wallclock conversion.
---

# Agent Work Estimation Skill

## Problem

AI coding agents systematically overestimate task duration because they anchor to human developer timelines absorbed from training data. A task an agent can complete in 30 minutes gets estimated as "2-3 days" because that's what a human developer forum post would say.

## Solution

Force the agent to estimate from its own operational units — **tool-call rounds** — and only convert to human wallclock time at the very end.

## Core Units

| Unit | Definition | Scale |
|------|-----------|-------|
| **Round** | One tool-call cycle: think → write code → execute → verify → fix | ~2-4 min wallclock |
| **Module** | A functional unit built from multiple rounds until usable | 2-15 rounds |
| **Project** | All modules + integration + debugging | Sum of modules × integration factor |

A **Round** is the atomic unit. It maps directly to one iteration of:
1. Agent reasons about what to do
2. Agent writes/edits code
3. Agent runs the code or a test
4. Agent reads the output
5. Agent decides if it needs to fix something (if yes → next round)

## Estimation Procedure

When asked to estimate a task, follow these steps in order:

### Step 1: Decompose into Modules

Break the task into functional modules. Each module should be independently buildable and testable. Ask yourself: "What are the distinct pieces I would build one at a time?"

### Step 2: Estimate Rounds per Module

For each module, estimate the number of rounds using these anchors:

| Pattern | Typical Rounds | Examples |
|---------|---------------|----------|
| **Boilerplate / known pattern** | 1-2 | CRUD endpoint, config file, standard API client |
| **Moderate complexity** | 3-5 | Custom UI layout, state management, data pipeline |
| **Exploratory / under-documented** | 5-10 | Unfamiliar framework, platform-specific APIs, complex integrations |
| **High uncertainty** | 8-15 | Undocumented behavior, novel algorithms, multi-system debugging |

Key calibration rules:
- If you can generate the code in one shot and it will likely run → **1 round**
- If you'll need to generate, run, see an error, and fix → **2-3 rounds**
- If the library/framework has sparse docs and you'll be guessing → **5+ rounds**
- If it involves platform permissions, OS-level APIs, or environment-specific behavior the user must manually verify → add **2-3 rounds**

### Step 3: Assign Risk Coefficients

Each module gets a risk coefficient that inflates its round count:

| Risk Level | Coefficient | When to Apply |
|------------|------------|---------------|
| **Low** | 1.0 | Mature ecosystem, clear docs, agent has strong pattern match |
| **Medium** | 1.3 | Minor unknowns, may need 1-2 extra debug rounds |
| **High** | 1.5 | Sparse docs, platform quirks, integration unknowns |
| **Very High** | 2.0 | Possible dead ends, may need to change approach entirely |

### Step 4: Calculate Totals

```
Module effective rounds = base rounds × risk coefficient
Project rounds = Σ(module effective rounds) + integration rounds
Integration rounds = 10-20% of base total (for wiring modules together)
```

### Step 5: Convert to Wallclock Time

Only at the very end, convert to human time:

```
Wallclock time = project rounds × minutes_per_round
```

Default `minutes_per_round` = **3 minutes** (includes agent generation time + user review time).

Adjust this parameter based on context:
- Fast iteration, user barely reviews → 2 min/round
- Complex domain, user carefully reviews each step → 4 min/round
- User needs to manually test (mobile, hardware, permissions) → 5 min/round

## Output Format

Always output the estimation in this exact structure:

```markdown
### Task: [task name]

#### Module Breakdown

| # | Module | Base Rounds | Risk | Effective Rounds | Notes |
|---|--------|------------|------|-----------------|-------|
| 1 | ...    | N          | 1.x  | M               | why   |
| 2 | ...    | N          | 1.x  | M               | why   |

#### Summary

- **Base rounds**: X
- **Integration**: +Y rounds
- **Risk-adjusted total**: Z rounds
- **Estimated wallclock**: A – B minutes (at N min/round)

#### Biggest Risks
1. [specific risk and what could blow up the estimate]
2. [...]
```

## Anti-Patterns to Avoid

These are the failure modes this skill exists to prevent:

1. **Human-time anchoring**: "A developer would take about 2 weeks..." → NO. Start from rounds.
2. **Padding by vibes**: Adding time "just to be safe" without specific risk rationale → NO. Use risk coefficients.
3. **Confusing complexity with volume**: 500 lines of boilerplate ≠ hard. One line of CGEvent API ≠ easy. Estimate by uncertainty, not line count.
4. **Forgetting integration cost**: Modules work alone but break together. Always add integration rounds.
5. **Ignoring user-side bottlenecks**: If the user must manually grant permissions, restart an app, or test on a device, that's extra round time. Adjust `minutes_per_round`, don't add phantom rounds.

## Calibration Reference

Here are example projects with known round counts to help calibrate:

See `references/calibration-examples.md` for detailed examples across project types.

## Eval Prompts

See `evals/evals.json` for test cases to validate estimation accuracy.
