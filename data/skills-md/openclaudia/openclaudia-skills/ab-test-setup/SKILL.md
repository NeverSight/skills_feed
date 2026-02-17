---
name: ab-test-setup
description: Design, plan, and analyze A/B tests with statistical rigor. Use when the user asks about A/B testing, split testing, experiment design, statistical significance, sample size calculation, test duration, multivariate testing, or conversion experiments. Trigger phrases include "A/B test", "split test", "experiment", "statistical significance", "sample size", "test duration", "which version wins", "conversion experiment", "hypothesis test", "variant testing".
---

# A/B Test Design and Analysis

You are an expert in experimentation and A/B testing. When the user asks you to design a test, calculate sample sizes, analyze results, or plan an experimentation roadmap, follow this framework.

## Step 1: Gather Test Context

Establish: page/feature being tested, current conversion rate, monthly traffic, primary metric, secondary metrics, guardrail metrics, duration constraints, testing platform (Optimizely, VWO, custom).

## Step 2: Hypothesis Framework

### Hypothesis Template

```
OBSERVATION: [What we noticed in data/research/feedback]
HYPOTHESIS: If we [specific change], then [metric] will [change] by [amount],
            because [behavioral/psychological reasoning].
CONTROL (A): [Current state]
VARIANT (B): [Proposed change]
PRIMARY METRIC: [Single metric that determines winner]
GUARDRAILS: [Metrics that must not degrade]
```

### Hypothesis Categories

- **Clarity**: "Users don't understand what we offer" -- test headline, value prop
- **Motivation**: "Users aren't motivated to act" -- test social proof, urgency, benefits
- **Friction**: "Process is too difficult" -- test form length, step count, layout
- **Trust**: "Users don't trust us" -- test testimonials, guarantees, badges
- **Relevance**: "Content doesn't match intent" -- test personalization, segmentation

## Step 3: Sample Size and Duration

### Sample Size Formula

```
n = (Z_alpha/2 + Z_beta)^2 * (p1*(1-p1) + p2*(1-p2)) / (p2 - p1)^2
Where: Z_alpha/2 = 1.96 (95%), Z_beta = 0.84 (80% power), p2 = p1 * (1 + MDE)
```

### Quick Reference (per variant, 95% significance, 80% power)

| Baseline CR | 10% MDE | 15% MDE | 20% MDE | 25% MDE |
|---|---|---|---|---|
| 2% | 385,040 | 173,470 | 98,740 | 63,850 |
| 3% | 253,670 | 114,300 | 65,080 | 42,110 |
| 5% | 148,640 | 67,040 | 38,200 | 24,730 |
| 10% | 70,420 | 31,780 | 18,120 | 11,740 |
| 15% | 44,310 | 20,010 | 11,420 | 7,400 |
| 20% | 31,310 | 14,140 | 8,070 | 5,230 |

**Duration** = (Sample size per variant x Number of variants) / Daily traffic. Minimum 7 days, maximum 8 weeks.

If duration exceeds 8 weeks: increase MDE, reduce variants, test a higher-traffic page, use a micro-conversion metric, or accept lower power.

## Step 4: Test Types

| Type | What | When | Caution |
|---|---|---|---|
| A/B | Two versions, 50/50 split | One specific change, sufficient traffic | Minimum 7 days |
| A/B/n | Control + 2-4 variants | Multiple approaches to same element | Needs proportionally more traffic |
| MVT | Multiple element combinations | High traffic (100K+/month) | Combinations multiply fast |
| Bandit | Dynamic traffic allocation | High opportunity cost | Harder to reach significance |
| Pre/Post | Before vs. after (no split) | Cannot split traffic | Weakest causal evidence |

## Step 5: Test Design by Element

### Headline Tests
Test: value prop angle, specificity, social proof integration, question vs. statement, length. Measure: conversion rate, bounce rate, scroll depth.

### CTA Tests
Test: button copy (action vs. benefit), color (contrast), size, placement, surrounding copy. Measure: click-through rate, conversion rate.

### Layout Tests
Test: single vs. two column, long vs. short form, section order, video vs. static hero, with vs. without nav. Measure: conversion rate, scroll depth. Guardrail: page load time.

### Pricing Tests
Test: price point, billing display, tier count, feature allocation, default plan, anchoring, decoy pricing. Measure: **revenue per visitor** (not just CR). Guardrail: support tickets, refund rate.

### Copy Tests
Test: tone, length, format (paragraphs vs. bullets), emotional angle, proof type. Measure: conversion rate, read depth.

## Step 6: Running the Test

### Pre-Launch Checklist

- [ ] Hypothesis documented with primary metric defined
- [ ] Sample size calculated, traffic sufficient
- [ ] QA on both variants across devices and browsers
- [ ] Tracking verified -- conversions fire correctly for both variants
- [ ] No other tests on same page/funnel
- [ ] Traffic allocation set (50/50)
- [ ] Exclusion criteria defined (bots, internal IPs)
- [ ] Stakeholders aligned on decision criteria before launch

### During the Test

- Do not peek for first 3-5 days (early results are misleading)
- Do not stop early unless guardrail metrics violated
- Monitor for technical issues and tracking accuracy
- Watch for sample ratio mismatch (SRM): >1% deviation means setup problem
- Do not add variants mid-test

### Post-Test Analysis

```
TEST RESULTS
============
Test: [name] | Duration: [days] | Sample: [n] | Split: [%/%]
SRM Check: [Pass/Fail]

| Variant | Visitors | Conversions | CR | vs Control | p-value | Significant? |
|---------|----------|-------------|-----|------------|---------|--------------|
| Control | X,XXX | XXX | X.XX% | -- | -- | -- |
| Var B | X,XXX | XXX | X.XX% | +X.X% | 0.XXX | Yes/No |

DECISION: [Implement / Keep Control / Iterate]
REASONING: [Data-based rationale]
NEXT TEST: [What to test next]
```

## Step 7: Common Pitfalls

1. **Peeking**: Checking daily inflates false positives to 25-30%. Commit to sample size upfront.
2. **Underpowered tests**: "No result" often means "not enough data."
3. **Too many variables**: Isolate one variable per test.
4. **Ignoring segments**: Overall flat, but mobile wins / desktop loses. Always segment.
5. **Novelty effect**: Run 2+ weeks to account for novelty wearing off.
6. **Multiple comparisons**: One primary metric. Bonferroni correction for extras.
7. **Practical significance**: A significant 0.1% lift may not be worth implementing.

## Step 8: Test Prioritization (ICE Scoring)

```
Impact (1-10): How much will this move the metric?
Confidence (1-10): How likely to produce a result?
Ease (1-10): How easy to implement?
ICE Score = (Impact + Confidence + Ease) / 3
```

### Roadmap Template

```
EXPERIMENTATION ROADMAP
Quarter: [Q] | Page: [target] | Traffic: [volume] | Current CR: [X%]

| Priority | Test | ICE | Duration | Status |
|----------|------|-----|----------|--------|
| 1 | ... | 8.3 | 14 days | Ready |
| 2 | ... | 7.7 | 21 days | Ready |
| 3 | ... | 7.0 | 14 days | Idea |
```

Run tests sequentially on the same page to avoid interaction effects. Provide a backlog ranked by ICE score.
