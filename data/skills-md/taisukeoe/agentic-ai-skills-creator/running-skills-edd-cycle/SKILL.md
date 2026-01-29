---
name: running-skills-edd-cycle
description: Guides evaluation-driven development (EDD) process for agent skills. Use when setting up skill testing workflows, creating skill evaluation scenarios, or establishing Claude A/B feedback loops for skill validation. Provides development methodology, not content guidance.
license: Apache-2.0
allowed-tools: "Skill(creating-effective-skills) Skill(improving-skills) Skill(reviewing-skills) Skill(evaluating-skills-with-models)"
metadata:
  author: Softgraphy GK
  version: "0.2.0"
---

# Running Skills EDD Cycle

Run evaluation-driven development cycle for agent skills.

## Workflow

### Step 1: Build Evaluations First

Create evaluations BEFORE writing documentation. This ensures skills solve real problems.

1. Run Claude on representative tasks WITHOUT the skill
2. Document specific failures or missing context
3. Create 3+ evaluation scenarios that test these gaps

Evaluation scenarios are saved to `tests/scenarios.md` as the final step of `/creating-effective-skills` workflow.

### Step 2: Establish Baseline

Measure Claude's performance WITHOUT the skill:

1. Run each evaluation scenario
2. Record: success/failure, missing context, wrong approaches
3. This becomes comparison baseline

### Step 3: Write Minimal Instructions

Create just enough content to address the gaps:

- Start with core workflow only
- Add detail only when tests fail
- Avoid over-explaining

**REQUIRED:** Use the Skill tool to invoke `creating-effective-skills` before writing any skill content. This ensures proper naming, description format, and structure from the start.

### Step 4: Evaluate with Multiple Models

> **Note:** This step requires Claude Code CLI. Skip if using Claude.ai.

**REQUIRED:** Use the Skill tool to invoke `evaluating-skills-with-models` with the skill path.

This will:
1. Auto-load scenarios from `tests/scenarios.md`
2. Execute with sub-agents across models (sonnet, opus, haiku)
3. Evaluate against expected behaviors
4. Determine recommended model (least capable with full compatibility)

**After evaluation:** Document recommended model in skill's metadata.

**REQUIRED:** Use the Skill tool to invoke `improving-skills` when observations reveal issues.

### Step 5: Final Review

Before considering the skill complete:

**REQUIRED:** Use the Skill tool to invoke `reviewing-skills` to verify compliance with best practices.

1. Address all compliance issues identified
2. Re-run evaluations after fixes
3. Repeat until skill passes review

### Step 6: User Validation Guide

After all reviews pass, output instructions for user to validate in a fresh session:

```
## Test Your Skill

Run this command in a new terminal to test with a fresh Claude session:

claude --model {recommended_model} "{evaluation_query}"

After testing, paste the output file or result back to this session for final confirmation.
```

Replace:
- `{recommended_model}`: Model determined in Step 4 (e.g., `sonnet`)
- `{evaluation_query}`: A representative query from your evaluations

## Quick Reference

### Cycle

```
Identify gaps -> Create evaluations -> Baseline -> Write minimal -> Model eval (sub-agents) -> Review -> User validation
```

### What Observations Indicate

| Observation | Indicates |
|-------------|-----------|
| Unexpected file reading order | Structure not intuitive |
| Missed references | Links need to be explicit |
| Repeated reads of same file | Move content to SKILL.md |
| Never accessed file | Unnecessary or poorly signaled |
