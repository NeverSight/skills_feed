---
name: metrics-framework
description: >
  Define product metrics with a North Star, input/output tree, and
  counter-metrics. Use when asked to define metrics, set up measurement,
  choose KPIs, pick a north star metric, or build a metrics framework.
  Prevents vanity metrics and gaming.
---

Define metrics that drive decisions, not dashboards that collect dust. Every metric must answer: "If this number changes, what will we do differently?" If nothing changes, it's a vanity metric.

## North Star Metric

One metric that captures the core value your product delivers to customers. Not revenue (that's an output). Not signups (that's vanity). The North Star reflects the moment customers get value.

Examples:
- Slack: Messages sent in channels with 3+ members
- Spotify: Time spent listening
- Airbnb: Nights booked

**Test:** If this metric goes up, does the company sustainably grow? If yes, it's your North Star.

## Input/Output Tree

Build a tree connecting your North Star to actionable inputs:

```
North Star: Weekly active teams with 3+ collaborators
  |
  +-- Acquisition: New signups/week
  |     +-- Website visitors
  |     +-- Signup conversion rate
  |
  +-- Activation: % who invite a teammate in 7 days
  |     +-- Onboarding completion rate
  |     +-- Time to first shared project
  |
  +-- Engagement: Documents edited per active team/week
  |     +-- Feature adoption (comments, mentions, sharing)
  |     +-- Return frequency
  |
  +-- Retention: % active at day 30
        +-- Weekly return rate
        +-- Feature breadth used
```

Each leaf is a metric a team can directly influence. The tree shows HOW inputs drive the North Star.

## Counter-Metrics

EVERY metric gets a counter-metric. This prevents gaming and ensures you're not optimizing one thing at the expense of another.

| Metric | Counter-Metric |
|--------|---------------|
| Signup conversion rate | Activation rate (don't lower the bar to get signups) |
| Time to first value | 30-day retention (don't rush users past learning) |
| Feature adoption | Task completion rate (don't push features that confuse) |
| Revenue per user | Churn rate (don't squeeze users into leaving) |

If the metric improves but the counter-metric degrades, you've optimized the wrong thing.

## Guidelines

- CRITICAL: ALWAYS pair every metric with a counter-metric. No exceptions.
- NEVER use vanity metrics: total signups, page views, total users, app downloads. These only go up and tell you nothing.
- NEVER track more than 5-7 metrics actively. If your dashboard has 20 charts, nobody looks at any of them.
- ALWAYS define metrics with exact formulas. "Activation rate" means nothing. "Percentage of new signups who invite at least one teammate within 7 days of account creation" is a metric.
- ALWAYS set a baseline before setting a target. You can't improve what you haven't measured.
- NEVER set targets without understanding the current number and why it's where it is.
- ALWAYS measure outcomes (user behavior) over outputs (features shipped).

---

*Built on Amplitude's North Star framework and the Linear Method. Skills from [productskills](https://github.com/assimovt/productskills).*
