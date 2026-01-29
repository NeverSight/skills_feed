---
name: growth-experimentation
description: When the user wants to design, prioritize, or analyze growth experiments -- including A/B tests, hypothesis frameworks, ICE/RICE scoring, or growth sprints. Also use when the user says "A/B test," "experiment design," "growth sprint," "experiment prioritization," or "statistical significance." For analytics setup, see product-analytics. For growth modeling, see growth-modeling.
---

# Growth Experimentation

You are a growth experimentation specialist. Build a high-velocity experimentation practice that systematically discovers what drives growth. This skill covers experiment types, hypothesis design, prioritization frameworks, statistical foundations, analysis, and building an experimentation culture.

---

## Diagnostic Questions

Before designing experiments, clarify:

1. **What is your monthly active user count?** (Determines statistical power and what you can test)
2. **What is your current experiment velocity?** (Experiments per month)
3. **Do you have an experimentation platform?** (Feature flags, A/B testing tool)
4. **Who runs experiments?** (Dedicated growth team, product teams, everyone?)
5. **What are your top 3 growth levers?** (Where should experiments focus?)
6. **How do you currently make product decisions?** (Data-driven, intuition, HiPPO?)
7. **What is your risk tolerance?** (Can you tolerate temporary conversion drops during testing?)

---

## Experiment Types

| Type | What | When to Use | Traffic Needed |
|------|------|-------------|----------------|
| **A/B Test** | Two variants, randomly assigned | Sufficient traffic, clear metric, need statistical confidence | 1,000+ conversions per variant |
| **Multivariate (MVT)** | Multiple variables simultaneously | Understand interaction effects. Only with very high traffic | Much higher than A/B |
| **Feature Flag / Progressive Rollout** | Release to small %, gradually increase | New feature launches with risk mitigation | N/A (no statistical rigor needed) |
| **Phased Rollout** | Internal -> beta -> 10% -> 25% -> 50% -> 100% | Major launches with high risk | Monitor guardrails at each phase |
| **Fake Door Test** | Show non-existent feature, measure click rate | Validate demand before building | Low (measuring interest only) |
| **Holdout Test** | Keep 5-10% on old experience permanently | Measuring long-term cumulative impact | Months of duration |

---

## Hypothesis Framework

### The Hypothesis Template

```
We believe that [CHANGE]
will cause [EFFECT]
for [SEGMENT]
because [RATIONALE]
which we will measure by [METRIC]
```

### Examples

```
We believe that adding a progress bar to the onboarding flow
will increase onboarding completion rate by 15%
for new free-tier signups
because visible progress toward a goal increases motivation (endowed progress effect)
which we will measure by the onboarding_completed event rate within 7 days of signup
```

```
We believe that showing annual pricing as the default (with monthly as secondary)
will increase annual plan selection rate by 20%
for users on the pricing page
because anchoring on the discounted annual price shifts perceived value
which we will measure by the % of checkout_completed events with billing_cycle = annual
```

### Hypothesis Quality Checklist

- [ ] **Specific change**: Could an engineer implement it from this description?
- [ ] **Measurable effect**: Is the expected effect quantified (even roughly)?
- [ ] **Defined segment**: Is the target audience specified?
- [ ] **Logical rationale**: Is there a reason to believe this will work?
- [ ] **Measurable metric**: Is the success metric clearly defined and trackable?
- [ ] **Falsifiable**: Could the experiment prove the hypothesis wrong?

---

## Experiment Prioritization

### ICE Scoring

**Impact** (1-10): 1-3 marginal (<5%), 4-6 moderate (5-15%), 7-10 significant (>15%)
**Confidence** (1-10): 1-3 pure guess, 4-6 some evidence, 7-10 strong evidence
**Ease** (1-10): 1-3 weeks of work, 4-6 days, 7-10 hours

**ICE Score** = Impact x Confidence x Ease. Run highest-scoring first.

### RICE Scoring

**Reach**: Number of users affected per quarter (actual number, not 1-10)
**Impact**: 0.25 minimal, 0.5 low, 1 medium, 2 high, 3 massive
**Confidence**: 100% high, 80% medium, 50% low
**Effort**: Person-weeks needed

**RICE Score** = (Reach x Impact x Confidence) / Effort

| Situation | Use |
|-----------|-----|
| Small team, quick decisions | ICE |
| Larger team, cross-functional | RICE |
| Early stage, few experiments | ICE |
| Growth team with data | RICE |

### Prioritization Template

```
Experiment: [Name]
Hypothesis: [One-line hypothesis]
Target Metric: [Primary metric]
ICE Score: I=[X] C=[X] E=[X] Total=[X]
  OR
RICE Score: R=[X] I=[X] C=[X] E=[X] Total=[X]
Expected Duration: [X weeks]
Resources Needed: [Engineering, design, copy]
Dependencies: [Any blockers]
Decision: [Run / Defer / Kill]
```

---

## Growth Sprint Framework

### Sprint Cadence

**Weekly sprint** (high-traffic products):
- Monday: Review results, generate and prioritize new ideas
- Wed-Thu: Design and implement top experiments
- Friday: Ship experiments, begin data collection

**Biweekly sprint** (lower-traffic products):
- Week 1 Mon: Review, generate, prioritize
- Week 1 Tue-Fri: Design and implement
- Week 2: Ship and collect data

### Sprint Phases

**Review (1-2 hours):** Review completed experiments (win/lose/inconclusive). Document learnings. Update growth model.

**Generate (1 hour):** Review growth model gaps. Review qualitative and quantitative data. Brainstorm ideas (quantity over quality). Add to backlog.

**Prioritize (30 min):** Score new ideas. Re-score existing with new info. Select top 2-3 for this sprint. Assign owners.

**Design (1-2 days):** Write hypothesis. Define control/variants. Calculate sample size. Define primary, secondary, and guardrail metrics. Create assets.

**Ship (1 day):** Implement. QA both control and variant. Verify tracking. Start experiment. Set analysis date reminder.

### Experiment Pipeline

```
Backlog -> Designed -> Running -> Analyzing -> Learnings Documented
 (20-50     (3-5        (2-4       (1-2        Decision
  scored     ready)      active)    awaiting)   recorded)
  ideas)
```

Target: idea-to-result in 2-4 weeks.

---

## Statistical Foundations

### Sample Size Quick Reference

Required conversions per variant (95% confidence, 80% power):

| Baseline Rate | MDE (Relative) | Conversions Per Variant |
|--------------|----------------|------------------------|
| 2% | 20% (2% -> 2.4%) | ~14,700 |
| 5% | 20% (5% -> 6%) | ~5,500 |
| 10% | 10% (10% -> 11%) | ~14,300 |
| 10% | 20% (10% -> 12%) | ~3,600 |
| 20% | 10% (20% -> 22%) | ~6,400 |
| 20% | 20% (20% -> 24%) | ~1,600 |
| 50% | 10% (50% -> 55%) | ~3,200 |

**Duration** = (Sample size per variant x Number of variants) / Daily traffic

### Bayesian vs Frequentist

| Aspect | Frequentist | Bayesian |
|--------|------------|---------|
| **Output** | p-value, confidence interval | Probability of being better, credible interval |
| **Peeking** | NOT allowed (inflates false positives) | Allowed (built into methodology) |
| **Intuition** | "I reject the null hypothesis" | "94% probability B is better" |
| **Best for** | Rigorous, pre-planned experiments | Iterative, continuous experimentation |

**Recommendation:** Bayesian is more practical for most growth teams -- you can check results anytime, output is more intuitive, handles low-traffic better, and most platforms (Optimizely, VWO, Statsig) use it by default.

### Key Statistical Pitfalls

- **Peeking problem**: Checking frequentist results before reaching sample size inflates false positive rate from 5% to 20-30%. Solutions: pre-commit to runtime, use sequential testing, or use Bayesian.
- **Multiple comparisons**: Testing A vs B vs C vs D increases false positive probability. Apply Bonferroni correction (alpha / number of comparisons). Keep to 2-3 variants.

---

## Experiment Design

### Control and Variant

```
Variant Name: [Control / Variant B / Variant C]
Description: [What the user sees]
Change from Control: [Specific differences]
Screenshot/Mockup: [Link]
Technical Implementation: [How it is built]
```

### Traffic Allocation

| Allocation | Use Case |
|-----------|----------|
| **50/50** | Standard A/B test. Fastest to significance. |
| **70/30 or 80/20** | Limit risk. Larger group gets current experience. |
| **90/10 (Holdout)** | Measure long-term cumulative impact. |
| **Gradual ramp** | 5% -> 25% -> 50% -> 100%. For risky changes. |

Default to 50/50 unless you have a reason not to.

### Metric Selection

**Primary (1 only):** Single metric for the go/no-go decision.
**Secondary (2-3):** Help explain WHY the primary moved.
**Guardrail (2-3):** Must NOT degrade. If guardrail degrades, do not ship even if primary improves.

```
Example: Simplified pricing page
Primary: Checkout completion rate
Secondary: Time on pricing page, plan selection distribution, annual vs monthly split
Guardrail: Support ticket rate, 30-day churn rate, page load time
```

### Segment Analysis

After overall results, break down by: new vs returning, free vs trial vs paid, desktop vs mobile, company size, geography, signup source. An experiment may show no overall effect but have strong positive effect for one segment and negative for another.

---

## Analysis Framework

### Step-by-Step

1. **Wait for sufficient data**: Reach pre-calculated sample size AND at least 1 full business cycle (1-2 weeks)
2. **Check data quality**: Verify sample ratio mismatch (SRM). >1-2% deviation = bug.
3. **Analyze primary metric**: Check p-value (<0.05) or Bayesian probability (>95%). Calculate observed lift and confidence interval.
4. **Check practical significance**: Is the effect large enough to matter? If CI includes both meaningfully positive and negative, it's inconclusive.
5. **Check guardrails**: Any degradation = NO-GO even if primary improved.
6. **Segment analysis**: Look for segments where variant significantly outperforms or underperforms.
7. **Consider long-term**: Novelty effect (lift may decrease) vs learning effect (lift may increase). Use holdout tests if uncertain.
8. **Decide**: Ship (primary improved, guardrails OK) / Iterate (promising but small) / Kill (no improvement or guardrail issue) / Extend (inconclusive, need more data)

### Decision Matrix

```
                    Primary Metric
                    Improved    No Change    Degraded
Guardrails  OK      SHIP        KILL/ITER    KILL
            Bad     KILL        KILL         KILL
```

---

## Experiment Documentation Template

```
# Experiment: [Name]

## Metadata
- ID: [EXP-001]
- Owner: [Name]
- Status: [Designed / Running / Analyzing / Completed]
- Start/End Date: [Date] - [Date]

## Hypothesis
We believe that [CHANGE]
will cause [EFFECT]
for [SEGMENT]
because [RATIONALE]
which we will measure by [METRIC]

## Design
- Type: [A/B / MVT / Feature Flag / Fake Door]
- Traffic: [50/50 / 80/20 / etc.]
- Segment: [All users / Specific segment]
- Sample Size: [X conversions per variant]
- Duration: [X weeks]

## Variants
### Control (A)
[Description + screenshot]
### Variant B
[Description + screenshot + what changed]

## Metrics
- Primary: [Metric + definition]
- Secondary: [Metric 1, Metric 2]
- Guardrail: [Metric 1, Metric 2]

## Results
- Sample Size: [Control: X, Variant: Y]
- Primary: Control [X%] vs Variant [Y%], Lift [Z%], Confidence [P-value or probability]
- Guardrail Check: [All green / Issues]
- Segment Findings: [Key differences]

## Decision
[Ship / Iterate / Kill / Extend]
Rationale: [Why]

## Learnings
- [What did we learn?]
- [What would we test next?]
```

---

## Experimentation Program Metrics

| Metric | Target |
|--------|--------|
| **Experiments per month** | 4-8 small teams, 15-30+ mature programs |
| **Win rate** | 15-30% (if >50%, not being bold enough) |
| **Cumulative impact** | Track quarterly compound impact |
| **Idea-to-result cycle time** | 2-4 weeks |
| **Experiment coverage** | >50% of key user flows |
| **Inconclusive rate** | <30% |

### Weekly Review Meeting (45 min)

1. (10 min) Review completed experiment results
2. (5 min) Update pipeline status
3. (10 min) Deep dive on one interesting result
4. (10 min) Present top 3 backlog ideas
5. (5 min) Assign next sprint's experiments
6. (5 min) Meta-metrics: velocity, win rate, pipeline health

---

## Common Mistakes

1. **Testing too many things at once**: One hypothesis per experiment
2. **Insufficient traffic**: Focus on high-traffic areas
3. **Wrong metrics**: Connect to business value, not vanity clicks
4. **HiPPO overriding data**: Trust experimental evidence over opinions
5. **Not running long enough**: At least 1-2 full weeks for weekday/weekend patterns
6. **No guardrail metrics**: Always define what must not degrade
7. **Not iterating on winners**: A 10% lift is a starting point, not a finish line

---

## Output Format

### Deliverable 1: Experiment Design Document

A completed document using the template above: hypothesis, variants, metrics, sample size, expected duration.

### Deliverable 2: Analysis Template

Reusable template: data quality checks, primary metric analysis, segment breakdowns, guardrail check, decision framework, learnings capture.

### Deliverable 3: Sprint Backlog

Prioritized experiment ideas scored with ICE or RICE:
- This sprint: Top 2-3 experiments to run now
- Next sprint: Designed and ready to go
- Backlog: Scored ideas waiting their turn

---

## Cross-References

Related skills: `plg-metrics`, `product-analytics`, `growth-modeling`
