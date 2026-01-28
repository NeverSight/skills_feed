---
name: creativity
description: Generates non-obvious ideas using Verbalized Sampling (VS-CoT). Use when the user needs to brainstorm novel solutions, avoid stereotypical patterns, or write creatively.
---

# Creativity

This skill uses Distribution-level Sampling to bypass "mode collapse" and surface high-quality, non-obvious ideas (p < 0.10). 

State the goal for using this skill, and align the outcome to it.

## Creative Workflow

Follow these phases thoroughly. Show your reasoning to the user.

### Phase 1: Explore semantic space

Conduct a reasoning-first exploration of the semantic space. Identify the most "obvious" or stereotypical answers and explicitly discard them. 

Announce a list of discarded ideas with a super-short rationale.

### Phase 2: Generate

Produce a set of diverse responses:
1. $k$ (default 5) from the tail of the distribution (p < 0.15)
2. $k$ (default 5) from the head of the distribution (p > 0.85)

Use internal chain-of-thought to explore multiple distinct directions before writing outputs. Assign an estimated probability to each.

### Phase 3: Review

- Review the generated set against the broader task user is working on. 
- Eliminate any ideas that are irrelevant, or lack impact.

### Phase 4: Iteration

Decide whether the current set is sufficient:
- **Loop**: If ideas lack impact or relevance, re-run Phase 1.
- **Finalize**: If the set is strong, follow the **output format**.

## Output Format

Present the final set of ideas using Markdown tables. Each idea must have its own table with the following structure:

| Idea {n} | Probability: {P} |
| :--- | :--- |
| Idea | [Generated response] |
| Impact | [Short text on how impactful it is to the broader goal] |
| Rationale | [Short text on why it is relevant for the broader task] |

### Example Output

| **Idea 1** | Probability: 0.04 |
| :--- | :--- |
| Idea | Silent Onboarding: Replace tutorial pop-ups with environmental cues embedded in the UI itself. | 
| Impact | High. Standard onboardings are often skipped. This reframe lets users "learn by doing." |
| Rationale | Most onboarding assumes explicit instruction. This challenges the pattern by treating the interface as a "learning landscape" rather than a "lesson plan." |

## Creative Operators

To ensure non-obvious and creative output, optionally use the methods detailed in [operators.md](./assets/operators.md).