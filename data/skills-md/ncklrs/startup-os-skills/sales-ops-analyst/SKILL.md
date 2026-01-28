---
name: sales-ops-analyst
description: Expert sales operations and analytics guidance for revenue teams. Use when designing CRM workflows, building sales dashboards, optimizing pipeline analytics, creating lead routing rules, designing territories, calculating commissions, managing data quality, building forecasting models, or integrating sales tech stack. Covers Salesforce, HubSpot, Outreach, Gong, and RevOps best practices.
---

# Sales Ops Analyst

Strategic sales operations expertise for revenue teams — from CRM architecture and pipeline analytics to territory design and commission automation.

## Philosophy

Great sales ops isn't about more data. It's about **actionable insights** that accelerate revenue.

The best sales operations teams:
1. **Enable, don't police** — Make it easier for reps to do the right thing
2. **Measure what matters** — Vanity metrics create vanity pipeline
3. **Automate the mundane** — Free reps to sell, not update fields
4. **Build for scale** — Today's workaround is tomorrow's technical debt

## How This Skill Works

When invoked, apply the guidelines in `rules/` organized by:

- `crm-*` — CRM architecture, data models, hygiene practices
- `pipeline-*` — Pipeline analytics, stage definitions, velocity metrics
- `dashboard-*` — Sales reporting, metrics, visualizations
- `process-*` — Automation, workflows, approval chains
- `routing-*` — Lead routing, assignment rules, territory design
- `commission-*` — Comp plans, calculation logic, tracking
- `data-*` — Data quality, deduplication, enrichment
- `forecast-*` — Forecasting methodologies, models, accuracy

## Core Frameworks

### The RevOps Data Hierarchy

| Level | What It Measures | Used By | Update Frequency |
|-------|------------------|---------|------------------|
| **Activity** | Calls, emails, meetings | Reps, managers | Real-time |
| **Opportunity** | Deal progress, value | Reps, managers | Daily |
| **Pipeline** | Forecast, velocity | Directors, execs | Weekly |
| **Revenue** | Bookings, ARR, churn | C-suite, board | Monthly/Quarterly |

### Pipeline Velocity Formula

```
Pipeline Velocity = (# Opportunities × Win Rate × Avg Deal Size) / Sales Cycle Length

Example:
(100 opps × 25% × $50K) / 90 days = $13,889/day potential revenue
```

### The Sales Tech Stack

```
┌─────────────────────────────────────────────────────────────┐
│                      ANALYTICS LAYER                         │
│   (BI Tools: Tableau, Looker, Power BI, Salesforce Reports) │
├─────────────────────────────────────────────────────────────┤
│                      CRM LAYER                               │
│           (Salesforce, HubSpot, Dynamics 365)               │
├──────────────────┬──────────────────┬───────────────────────┤
│   ENGAGEMENT     │   INTELLIGENCE    │     ENRICHMENT       │
│ Outreach, Salesloft│  Gong, Chorus   │   ZoomInfo, Clearbit │
├──────────────────┴──────────────────┴───────────────────────┤
│                      DATA LAYER                              │
│     (Integrations, ETL, Data Warehouse, CDP)                │
└─────────────────────────────────────────────────────────────┘
```

### Lead Scoring Matrix

| Signal Type | Examples | Weight |
|-------------|----------|--------|
| **Fit** (firmographic) | Industry, company size, tech stack | 40% |
| **Engagement** (behavioral) | Website visits, content downloads, email opens | 35% |
| **Intent** (buying signals) | Pricing page views, demo requests, competitor research | 25% |

### Territory Design Principles

```
                    ┌─────────────────┐
                    │   BALANCED      │
                    │  OPPORTUNITY    │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
    ┌─────────┐        ┌─────────┐        ┌─────────┐
    │ Account │        │ Revenue │        │ Travel  │
    │ Volume  │        │Potential│        │ Load    │
    └─────────┘        └─────────┘        └─────────┘
```

## Key Metrics Overview

| Category | Metric | Target Range | Red Flag |
|----------|--------|--------------|----------|
| **Activity** | Meetings/week/rep | 10-15 | <5 |
| **Pipeline** | Coverage ratio | 3-4x | <2x |
| **Velocity** | Avg sales cycle | Industry dependent | Growing |
| **Quality** | Win rate | 20-30% | <15% or >50% |
| **Forecast** | Accuracy | ±10% | >25% variance |
| **Data** | Duplicate rate | <5% | >10% |

## Anti-Patterns

- **Field proliferation** — Adding fields without removing unused ones
- **Report graveyard** — Dashboards no one looks at
- **Process theater** — Mandatory updates that don't drive action
- **Excel dependency** — Critical processes outside the CRM
- **Garbage in, garbage out** — No data quality governance
- **Over-automation** — Automating bad processes faster
- **Single point of failure** — Tribal knowledge in one person's head
- **Metric gaming** — Optimizing for the number, not the outcome
