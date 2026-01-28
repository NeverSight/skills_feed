---
name: product-analyst
description: Expert product analytics strategist for SaaS and digital products. Use when designing product metrics frameworks, funnel analysis, cohort retention, feature adoption tracking, A/B testing, experimentation design, data instrumentation, or product dashboards. Covers AARRR, HEART, behavioral analytics, and impact measurement.
---

# Product Analyst

Strategic product analytics expertise for data-driven product decisions — from metrics framework selection to experimentation design and impact measurement.

## Philosophy

Great product analytics isn't about tracking everything. It's about **measuring what matters** to drive better product decisions.

The best product analytics:
1. **Start with decisions, not data** — What will you do differently based on this metric?
2. **Instrument once, measure forever** — Invest in solid event tracking upfront
3. **Balance leading and lagging** — Predict outcomes, don't just report them
4. **Make data accessible** — Self-serve dashboards beat SQL queues
5. **Experiment before you ship** — Validate hypotheses with real users

## How This Skill Works

When invoked, apply the guidelines in `rules/` organized by:

- `metrics-*` — Frameworks (AARRR, HEART), KPI selection, metric hierarchies
- `funnel-*` — Conversion analysis, drop-off diagnosis, optimization
- `cohort-*` — Retention analysis, segmentation, lifecycle tracking
- `feature-*` — Adoption tracking, usage patterns, feature success
- `experiment-*` — A/B testing, hypothesis design, statistical rigor
- `instrumentation-*` — Event tracking, data modeling, collection best practices
- `dashboard-*` — Visualization, stakeholder reporting, self-serve analytics

## Core Frameworks

### AARRR (Pirate Metrics)

| Stage | Question | Key Metrics |
|-------|----------|-------------|
| **Acquisition** | Where do users come from? | Traffic sources, CAC, signup rate |
| **Activation** | Do they have a great first experience? | Time-to-value, setup completion, aha moment |
| **Retention** | Do they come back? | DAU/MAU, D1/D7/D30 retention, churn |
| **Revenue** | Do they pay? | Conversion rate, ARPU, LTV |
| **Referral** | Do they tell others? | NPS, referral rate, viral coefficient |

### HEART Framework (Google)

| Dimension | Definition | Signal Types |
|-----------|------------|--------------|
| **Happiness** | User attitudes, satisfaction | NPS, CSAT, surveys |
| **Engagement** | Depth of involvement | Sessions, time-in-app, actions/session |
| **Adoption** | New users/features uptake | New users, feature adoption % |
| **Retention** | Continued usage over time | Retention curves, churn rate |
| **Task Success** | Efficiency and completion | Task completion, error rate, time-on-task |

### The Metrics Hierarchy

```
                    ┌─────────────────┐
                    │   North Star    │  ← Single metric that matters most
                    │     Metric      │
                    ├─────────────────┤
                    │    Primary      │  ← 3-5 key performance indicators
                    │      KPIs       │
                    ├─────────────────┤
                    │   Supporting    │  ← Diagnostic and health metrics
                    │    Metrics      │
                    ├─────────────────┤
                    │   Operational   │  ← Day-to-day tracking
                    │    Metrics      │
                    └─────────────────┘
```

### Retention Analysis Types

```
┌───────────────────────────────────────────────────────────┐
│                    RETENTION VIEWS                        │
├───────────────────────────────────────────────────────────┤
│  N-Day Retention    │  % who return on exactly day N      │
│  Unbounded          │  % who return on or after day N     │
│  Bracket Retention  │  % who return within a time window  │
│  Rolling Retention  │  % still active after N days        │
└───────────────────────────────────────────────────────────┘
```

### Experimentation Rigor Ladder

| Level | Approach | When to Use |
|-------|----------|-------------|
| **1. Gut** | Ship and hope | Never for important features |
| **2. Qualitative** | User research, feedback | Early exploration |
| **3. Observational** | Pre/post analysis | Low-risk changes |
| **4. Quasi-experiment** | Cohort comparison | When randomization hard |
| **5. A/B Test** | Randomized control | Optimization, validation |
| **6. Multi-arm Bandit** | Adaptive allocation | When speed > precision |

## Metric Selection Criteria

| Criterion | Question | Good Sign |
|-----------|----------|-----------|
| **Actionable** | Can we influence this? | Direct lever exists |
| **Accessible** | Can we measure it reliably? | <5% missing data |
| **Auditable** | Can we debug anomalies? | Clear calculation logic |
| **Aligned** | Does it tie to business value? | Executive cares |
| **Attributable** | Can we trace changes to causes? | A/B testable |

## Anti-Patterns

- **Vanity metrics** — Tracking what looks good, not what drives decisions
- **Metric overload** — 50 dashboards, zero insights
- **Lagging only** — Measuring outcomes without predictive indicators
- **Silent failures** — No alerting on data quality issues
- **HiPPO-driven** — Highest-paid person's opinion beats data
- **P-hacking** — Running tests until you get significance
- **Ship and forget** — Launching features without success criteria
- **Segment blindness** — Looking only at averages, missing cohort differences
