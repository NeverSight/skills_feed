---
name: offer-validator
description: Validate existing offers using Hormozi's Value Equation. Scores offers, exposes weaknesses, and provides actionable fixes. Activates for "validate my offer," "rate my offer," or "is my offer good."
version: 1.0.0
tags:
  - business
  - hormozi
  - validation
  - offers
  - value-equation
  - pricing
auto_activate: true
---

# Offer Validator - Hormozi Value Equation Scorecard

Ruthlessly assess existing offers against Hormozi's Value Equation. Score them, expose weaknesses, and provide actionable fixes.

**Hormozi's Principle:** "Your offer should be so good people feel stupid saying no."

**Your Role:** Score the offer. Find the gaps. Prescribe the fixes.

## When This Activates

- User says "validate my offer"
- User says "rate my offer"
- User asks "is my offer good"
- User wants to check offer quality before launch
- User mentions low conversions on an existing offer

## Key Difference from offer-architect

- **offer-architect** = Create offers from scratch
- **offer-validator** = Assess and score existing offers

## The Value Equation

```
Value = (Dream Outcome × Perceived Likelihood) / (Time Delay × Effort Required)
```

## Scoring Dimensions

| Dimension | Weight | What It Measures |
|-----------|--------|------------------|
| Dream Outcome | 2x | How desirable is the promised result? |
| Perceived Likelihood | 2x | How believable is it they'll achieve it? |
| Time to Results | 1.5x | How fast will they see results? |
| Effort Required | 1.5x | How much work do they have to do? |
| Bonus Stack | 1x | Does value stack overwhelm with extras? |
| Guarantee Strength | 1x | Is the risk completely removed? |

**Max Score:** 100 points

## Rating Scale

| Score | Rating | Verdict |
|-------|--------|---------|
| 85-100 | Grand Slam | Ready to scale. Minor optimizations only. |
| 70-84 | Strong | Good foundation. Fix weak points, then launch. |
| 55-69 | Decent | Significant gaps. Improve before scaling. |
| 40-54 | Weak | Major issues. Rebuild key components. |
| 0-39 | Broken | Start over. Fundamental problems. |

## Quick Gather Questions

Ask:

1. What exactly are you selling?
2. What do you promise they'll get?
3. What's included? (Deliverables, features, bonuses)
4. What's the price?
5. What's the guarantee?
6. Who is this for?

## Integration

| Skill | When to Use |
|-------|-------------|
| `offer-architect` | Rebuild weak components |
| `copy-validator` | Validate sales copy |
| `funnel-validator` | Validate entire funnel |
| `pricing-strategist` | Fix pricing issues |

---

**For detailed scoring criteria, examples, and output templates:** `references/full-guide.md`
