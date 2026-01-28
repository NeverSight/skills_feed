---
name: advanced-evaluation
description: Master LLM-as-a-Judge evaluation techniques including direct scoring, pairwise comparison, rubric generation, and bias mitigation. Use when building evaluation systems, comparing model outputs, or establishing quality standards for AI-generated content.
version: 1.0.0
tags:
  - evaluation
  - llm-as-judge
  - quality
  - bias-mitigation
---

# Advanced Evaluation

LLM-as-a-Judge techniques for evaluating AI outputs. Not a single technique but a family of approaches - choosing the right one and mitigating biases is the core competency.

## When to Activate

- Building automated evaluation pipelines for LLM outputs
- Comparing multiple model responses to select the best one
- Establishing consistent quality standards
- Debugging inconsistent evaluation results
- Designing A/B tests for prompt or model changes
- Creating rubrics for human or automated evaluation

## Core Concepts

### Evaluation Taxonomy

**Direct Scoring**: Single LLM rates one response on a defined scale.

- Best for: Objective criteria (factual accuracy, instruction following, toxicity)
- Reliability: Moderate to high for well-defined criteria

**Pairwise Comparison**: LLM compares two responses and selects better one.

- Best for: Subjective preferences (tone, style, persuasiveness)
- Reliability: Higher than direct scoring for preferences

### Known Biases

| Bias | Description | Mitigation |
|------|-------------|------------|
| Position | First-position preference | Swap positions, check consistency |
| Length | Longer = higher scores | Explicit prompting, length-normalized scoring |
| Self-Enhancement | Models rate own outputs higher | Use different model for evaluation |
| Verbosity | Unnecessary detail rated higher | Criteria-specific rubrics |
| Authority | Confident tone rated higher | Require evidence citation |

### Decision Framework

```
Is there an objective ground truth?
├── Yes → Direct Scoring (factual accuracy, format compliance)
└── No → Pairwise Comparison (tone, style, creativity)
```

## Quick Reference

### Direct Scoring Requirements

1. Clear criteria definitions
2. Calibrated scale (1-5 recommended)
3. Chain-of-thought: justification BEFORE score (improves reliability 15-25%)

### Pairwise Comparison Protocol

1. First pass: A in first position
2. Second pass: B in first position (swap)
3. Consistency check: If passes disagree → TIE
4. Final verdict: Consistent winner with averaged confidence

### Rubric Components

- Level descriptions with clear boundaries
- Observable characteristics per level
- Edge case guidance
- Strictness calibration (lenient/balanced/strict)

## Integration

Works with:

- **context-fundamentals** - Effective context structure
- **tool-design** - Evaluation tool schemas
- **evaluation** (foundational) - Core evaluation concepts

---

**For detailed implementation patterns, prompt templates, examples, and metrics:** `references/full-guide.md`

See also: `references/implementation-patterns.md`, `references/bias-mitigation.md`, `references/metrics-guide.md`
