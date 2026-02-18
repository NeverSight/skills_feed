---
name: ab-test-designer
description: Design robust A/B test experiments. Use when testing a new feature, validating a hypothesis, or optimizing conversion rates.
argument-hint: [feature/change to test]
---

# A/B Test Designer

## When to Use
- Testing a new feature or design variation
- Validating a hypothesis before full rollout
- Optimizing conversion rates or key metrics
- Choosing between multiple design approaches
- Need to make a data-driven decision on a change

## What This Skill Does
Helps you design rigorous A/B tests with clear hypotheses, success metrics, sample size calculations, and analysis plans.

## Instructions
Help me design an A/B test for [feature/change]. Include:

1. Hypothesis
   - Current situation and metrics
   - Proposed change
   - Expected impact and why

2. Test Design
   - Primary success metric
   - Secondary metrics
   - Sample size needed
   - Test duration
   - User segments to include/exclude

3. Variants
   - Control (A): current experience
   - Variant (B): new experience
   - Any additional variants (C, D, etc.)

4. Risks and Controls
   - Potential negative impacts
   - Guardrail metrics
   - When to stop the test early

5. Analysis Plan
   - Statistical significance threshold
   - How to handle edge cases
   - Decision criteria

Feature context:
[Add context about the change you want to test]

## Best Practices
- Start with a clear, falsifiable hypothesis
- Choose one primary metric to avoid multiple comparison issues
- Calculate sample size upfront based on expected effect size
- Run tests for full weekly cycles to account for day-of-week effects
- Set a minimum test duration (usually 1-2 weeks)
- Define success criteria before running the test
- Monitor guardrail metrics (revenue, errors, performance)

## Example
**Input:** Testing new onboarding flow vs current 3-step process
**Output:** Hypothesis (new 1-step flow will increase co...
