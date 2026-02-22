---
name: experiment-design
description: >
  Design hypothesis-driven experiments and A/B tests with proper
  methodology. Use when asked to design an A/B test, validate a
  hypothesis, plan an experiment, or set up a test for a product
  change. Covers hypothesis writing, sample size, and common mistakes.
---

Design experiments that actually prove something. Most A/B tests fail because they test vague ideas, run too short, or peek at results. A well-designed experiment has a clear hypothesis, adequate power, and a pre-committed analysis plan.

## Hypothesis Template

Every experiment starts with a written hypothesis before any work begins:

**"If we [make this specific change] for [this audience], then [this metric] will [change in this direction] by [this amount], because [this reason based on evidence]."**

Example:
> "If we replace the 5-step onboarding wizard with a single guided first-project flow for new signups, then 7-day activation rate will increase from 23% to 35%, because 4/6 interviewed users said they wanted to 'just start using it' not 'set everything up first.'"

Every part matters:
- **Specific change:** Not "improve onboarding" — the exact change
- **Audience:** Who sees this? New users only? Free tier only?
- **Metric + direction + amount:** A number you'll measure
- **Because:** The evidence-based reason. No evidence = no experiment.

## Experiment Design

### 1. Primary Metric
One metric the experiment is designed to move. Not three. One. Additional metrics are guardrails.

### 2. Guardrail Metrics
Metrics that must NOT degrade. These prevent "winning" by breaking something else.

### 3. Sample Size
Calculate BEFORE running. Use a sample size calculator with:
- Baseline conversion rate (current number)
- Minimum detectable effect (smallest change worth caring about)
- Statistical significance (95% is standard)
- Power (80% minimum)

If you need 50,000 users and you get 500/week, the experiment will take 100 weeks. Either increase the MDE or don't run the experiment.

### 4. Duration
Run for at least one full business cycle (usually 1-2 weeks minimum) to capture day-of-week effects. NEVER run less than 7 days.

### 5. Analysis Plan
Write BEFORE launching: what metric, what threshold, what you'll do if it wins/loses/is inconclusive. Pre-commit to avoid post-hoc storytelling.

## Common Mistakes

- **Peeking:** Checking results daily and stopping when you see significance. This inflates false positive rates. Set a duration and don't peek until it's done.
- **Underpowered tests:** Running a test with too few users to detect a meaningful effect. The result is "inconclusive" which teaches you nothing.
- **Testing too many things:** Changing 5 things at once means you don't know what worked. One change per experiment.
- **No guardrails:** Increasing signups by removing the password field "works" but breaks everything else.
- **Post-hoc storytelling:** The test was inconclusive but "we noticed an interesting trend in the 25-34 age group." That's noise, not signal.

## Guidelines

- CRITICAL: Write the hypothesis and analysis plan BEFORE building anything. If you can't state what you're testing and how you'll decide, you're not ready.
- NEVER peek at results before the pre-determined end date. Statistical significance at day 3 of a 14-day test is meaningless.
- NEVER run an experiment without calculating required sample size first.
- ALWAYS include guardrail metrics. Winning the primary metric while tanking retention is not a win.
- NEVER test more than one major change per experiment. Isolate variables.
- ALWAYS document learnings from inconclusive tests. "We couldn't detect an effect with N=5,000 users" is still useful information — it suggests the effect is small or nonexistent.

---

*Built on controlled experimentation methodology (Kohavi, Tang, Xu). Skills from [productskills](https://github.com/assimovt/productskills).*
