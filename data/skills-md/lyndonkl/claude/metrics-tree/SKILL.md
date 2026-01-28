---
name: metrics-tree
description: Use when setting product North Star metrics, decomposing high-level business metrics into actionable sub-metrics and leading indicators, mapping strategy to measurable outcomes, identifying which metrics to move through experimentation, understanding causal relationships between metrics (leading vs lagging), prioritizing metric improvement opportunities, or when user mentions metric tree, metric decomposition, North Star metric, leading indicators, KPI breakdown, metric drivers, or how metrics connect.
---

# Metrics Tree

## Table of Contents
- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [What Is It](#what-is-it)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Purpose

Decompose high-level "North Star" metrics into actionable sub-metrics, identify leading indicators, understand causal relationships, and select high-impact experiments to move metrics.

## When to Use

Use metrics-tree when you need to:

**Define Strategy:**
- Setting a North Star metric for product/business
- Aligning teams around single most important metric
- Clarifying what success looks like quantitatively
- Connecting strategic goals to measurable outcomes

**Understand Metrics:**
- Decomposing complex metrics into component drivers
- Identifying what actually moves a high-level metric
- Understanding causal relationships between metrics
- Distinguishing leading vs lagging indicators
- Mapping metric interdependencies

**Prioritize Actions:**
- Deciding which sub-metrics to focus on
- Identifying highest-leverage improvement opportunities
- Selecting experiments that will move North Star
- Allocating resources across metric improvement efforts
- Understanding tradeoffs between metric drivers

**Diagnose Issues:**
- Investigating why a metric is declining
- Finding root causes of metric changes
- Identifying bottlenecks in metric funnels
- Troubleshooting unexpected metric behavior

## What Is It

A metrics tree decomposes a North Star metric (the single most important product/business metric) into its component drivers, creating a hierarchy of related metrics with clear causal relationships.

**Key Concepts:**

**North Star Metric:** Single metric that best captures core value delivered to customers and predicts long-term business success. Examples:
- Airbnb: Nights booked
- Netflix: Hours watched
- Slack: Messages sent by teams
- Uber: Rides completed
- Stripe: Payment volume

**Metric Levels:**
1. **North Star** (top): Ultimate measure of success
2. **Input Metrics** (L2): Direct drivers of North Star (what you can control)
3. **Action Metrics** (L3): Specific user behaviors that drive inputs
4. **Output Metrics** (L4): Results of actions (often leading indicators)

**Leading vs Lagging:**
- **Leading indicators**: Predict future North Star movement (early signals)
- **Lagging indicators**: Measure past performance (delayed feedback)

**Quick Example:**

```
North Star: Weekly Active Users (WAU)

Input Metrics (L2):
├─ New User Acquisition
├─ Retained Users (week-over-week)
└─ Resurrected Users (inactive → active)

Action Metrics (L3) for Retention:
├─ Users completing onboarding
├─ Users creating content
├─ Users engaging with others
└─ Users receiving notifications

Leading Indicators:
- Day 1 activation rate (predicts 7-day retention)
- 3 key actions in first session (predicts long-term engagement)
```

## Workflow

Copy this checklist and track your progress:

```
Metrics Tree Progress:
- [ ] Step 1: Define North Star metric
- [ ] Step 2: Identify input metrics (L2)
- [ ] Step 3: Map action metrics (L3)
- [ ] Step 4: Select leading indicators
- [ ] Step 5: Prioritize and experiment
- [ ] Step 6: Validate and refine
```

**Step 1: Define North Star metric**

Ask user for context if not provided:
- **Product/business**: What are we measuring?
- **Current metrics**: Any existing key metrics?
- **Goals**: What does success look like?

Choose North Star using criteria:
- Captures value delivered to customers
- Reflects business model (how you make money)
- Measurable and trackable
- Actionable (teams can influence it)
- Not a vanity metric

See [Common Patterns](#common-patterns) for North Star examples by type.

**Step 2: Identify input metrics (L2)**

Decompose North Star into 3-5 direct drivers:
- What directly causes North Star to increase?
- Use addition or multiplication decomposition
- Ensure components are mutually exclusive where possible
- Each input should be controllable by a team

See [resources/template.md](resources/template.md) for decomposition frameworks.

**Step 3: Map action metrics (L3)**

For each input metric, identify specific user behaviors:
- What actions drive this input?
- Focus on measurable, observable behaviors
- Limit to 3-5 actions per input
- Actions should be within user control

If complex, see [resources/methodology.md](resources/methodology.md) for multi-level hierarchies.

**Step 4: Select leading indicators**

Identify early signals that predict North Star movement:
- Which metrics change before North Star changes?
- Look for early-funnel behaviors (onboarding, activation)
- Find patterns in high-retention cohorts
- Test correlation with future North Star values

**Step 5: Prioritize and experiment**

Rank opportunities by:
- **Impact**: How much will moving this metric affect North Star?
- **Confidence**: How certain are we about the relationship?
- **Ease**: How hard is it to move this metric?

Select 1-3 experiments to test highest-priority hypotheses.

See [resources/evaluators/rubric_metrics_tree.json](resources/evaluators/rubric_metrics_tree.json) for quality criteria.

**Step 6: Validate and refine**

Verify metric relationships:
- Check correlation strength between metrics
- Validate causal direction (does A cause B or vice versa?)
- Test leading indicator timing (how early does it predict?)
- Refine based on data and experiments

## Common Patterns

**North Star Metrics by Business Model:**

**Subscription/SaaS:**
- Monthly Recurring Revenue (MRR)
- Weekly Active Users (WAU)
- Net Revenue Retention (NRR)
- Paid user growth

**Marketplace:**
- Gross Merchandise Value (GMV)
- Successful transactions
- Completed bookings
- Platform take rate × volume

**E-commerce:**
- Revenue per visitor
- Order frequency × AOV
- Customer lifetime value (LTV)

**Social/Content:**
- Time spent on platform
- Content created/consumed
- Engaged users (not just active)
- Network density

**Decomposition Patterns:**

**Additive Decomposition:**
```
North Star = Component A + Component B + Component C

Example: WAU = New Users + Retained Users + Resurrected Users
```
- Use when: Components are independent segments
- Benefit: Teams can own individual components

**Multiplicative Decomposition:**
```
North Star = Factor A × Factor B × Factor C

Example: Revenue = Users × Conversion Rate × Average Order Value
```
- Use when: Components multiply together
- Benefit: Shows leverage points clearly

**Funnel Decomposition:**
```
North Star = Step 1 → Step 2 → Step 3 → Final Conversion

Example: Paid Users = Signups × Activation × Trial Start × Trial Convert
```
- Use when: Sequential conversion process
- Benefit: Identifies bottlenecks

**Cohort Decomposition:**
```
North Star = Σ (Cohort Size × Retention Rate) across all cohorts

Example: MAU = Sum of retained users from each signup cohort
```
- Use when: Retention is key driver
- Benefit: Separates acquisition from retention

## Guardrails

**Avoid Vanity Metrics:**
- ❌ Total registered users (doesn't reflect value)
- ❌ Page views (doesn't indicate engagement)
- ❌ App downloads (doesn't mean active usage)
- ✓ Active users, engagement time, completed transactions

**Ensure Causal Clarity:**
- Don't confuse correlation with causation
- Test whether A causes B or B causes A
- Consider confounding variables
- Validate relationships with experiments

**Limit Tree Depth:**
- Keep to 3-4 levels max (North Star → L2 → L3 → L4)
- Too deep = analysis paralysis
- Too shallow = not actionable
- Focus on highest-leverage levels

**Balance Leading and Lagging:**
- Need both for complete picture
- Leading indicators for early action
- Lagging indicators for validation
- Don't optimize leading indicators that hurt lagging ones

**Avoid Gaming:**
- Consider unintended consequences
- What behaviors might teams game?
- Add guardrail metrics (quality, trust, safety)
- Balance growth with retention/satisfaction

## Quick Reference

**Resources:**
- `resources/template.md` - Metrics tree structure with decomposition frameworks
- `resources/methodology.md` - Advanced techniques for complex metric systems
- `resources/evaluators/rubric_metrics_tree.json` - Quality criteria for metric trees

**Output:**
- File: `metrics-tree.md` in current directory
- Contains: North Star definition, input metrics (L2), action metrics (L3), leading indicators, prioritized experiments, metric relationships diagram

**Success Criteria:**
- North Star clearly defined with rationale
- 3-5 input metrics that fully decompose North Star
- Action metrics are specific, measurable behaviors
- Leading indicators identified with timing estimates
- Top 1-3 experiments prioritized with ICE scores
- Validated against rubric (score ≥ 3.5)

**Quick Decision Framework:**
- **Simple product?** → Use [template.md](resources/template.md) with 2-3 levels
- **Complex multi-sided?** → Use [methodology.md](resources/methodology.md) for separate trees per side
- **Unsure about North Star?** → Review common patterns above, test with "captures value + predicts revenue" criteria
- **Too many metrics?** → Limit to 3-5 per level, focus on highest impact

**Common Mistakes:**
1. **Choosing wrong North Star**: Pick vanity metric or one team can't influence
2. **Too many levels**: Analysis paralysis, lose actionability
3. **Weak causal links**: Metrics correlated but not causally related
4. **Ignoring tradeoffs**: Optimizing one metric hurts another
5. **No experiments**: Build tree but don't test hypotheses
