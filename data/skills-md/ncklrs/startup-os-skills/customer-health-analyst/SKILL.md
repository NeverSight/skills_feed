---
name: customer-health-analyst
description: Expert customer health scoring and analytics guidance. Use when designing health scores, building churn prediction models, analyzing usage metrics, identifying at-risk accounts, creating executive dashboards, or performing cohort analysis. Use for leading indicator development, customer data enrichment, risk escalation frameworks, and retention analytics.
---

# Customer Health Analyst

Expert guidance for customer health scoring, predictive analytics, and data-driven customer success strategies. Transform raw customer data into actionable insights that prevent churn and drive expansion.

## Philosophy

Customer health is not a single metric — it's a predictive system:

1. **Measure what matters** — Health scores should predict outcomes, not just track activity
2. **Lead, don't lag** — Focus on indicators that predict churn before it's too late
3. **Segment for action** — Different customers need different interventions
4. **Automate detection** — Scale health monitoring across your entire customer base
5. **Close the loop** — Analytics without action is just expensive data collection

## How This Skill Works

When invoked, apply the guidelines in `rules/` organized by:

- `health-*` — Health score design, weighting, and calibration
- `indicators-*` — Leading vs lagging indicator analysis
- `churn-*` — Prediction modeling and early warning systems
- `usage-*` — Analytics and adoption metrics
- `risk-*` — Identification, escalation, and intervention
- `data-*` — Enrichment and customer 360 development
- `cohort-*` — Analysis and benchmarking
- `executive-*` — Reporting and dashboards
- `segmentation-*` — Customer tiers and scoring models

## Core Frameworks

### The Health Score Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│                    COMPOSITE HEALTH SCORE                       │
│                         (0-100)                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ PRODUCT  │  │ENGAGEMENT│  │ GROWTH   │  │ SUPPORT  │       │
│  │  USAGE   │  │          │  │ SIGNALS  │  │ HEALTH   │       │
│  │  (35%)   │  │  (25%)   │  │  (20%)   │  │  (20%)   │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                    COMPONENT METRICS                            │
│                                                                 │
│  Usage:        Engagement:    Growth:        Support:          │
│  - DAU/MAU     - NPS score    - Seat trend   - Ticket volume   │
│  - Features    - CSM meetings - Usage trend  - Resolution time │
│  - Depth       - Email opens  - Expansion    - Sentiment       │
│  - Breadth     - Logins       - Contract     - Escalations     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Leading vs Lagging Indicators

| Type | Definition | Examples | Action Window |
|------|------------|----------|---------------|
| **Leading** | Predict future outcomes | Usage decline, engagement drop | 60-90 days |
| **Coincident** | Move with outcomes | Support sentiment, NPS | 30-60 days |
| **Lagging** | Confirm after the fact | Churn, revenue loss | Too late |

### Customer Health States

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  THRIVING ──→ HEALTHY ──→ NEUTRAL ──→ AT-RISK ──→ CRITICAL    │
│    (85+)      (70-84)     (50-69)     (30-49)      (<30)       │
│                                                                 │
│  Expand       Monitor     Engage      Intervene    Escalate    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Health Score Components

| Component | Weight | Key Metrics | Why It Matters |
|-----------|--------|-------------|----------------|
| **Product Usage** | 30-40% | DAU/MAU, feature adoption, depth | Usage predicts value realization |
| **Engagement** | 20-25% | NPS, CSM contact, responsiveness | Relationship strength indicator |
| **Growth Signals** | 15-20% | Seat expansion, usage trend | Investment signals commitment |
| **Support Health** | 15-20% | Ticket volume, sentiment, resolution | Frustration predicts churn |
| **Financial** | 5-10% | Payment history, contract length | Financial commitment level |

### Churn Risk Factors

| Factor | Risk Weight | Detection Method |
|--------|-------------|------------------|
| Champion departure | Critical | Contact tracking, LinkedIn |
| Usage decline >30% | High | Product analytics |
| Negative NPS (0-6) | High | Survey responses |
| Support escalations | High | Ticket analysis |
| Missed renewal meeting | High | CSM activity tracking |
| Contract downgrade | Very High | Billing data |
| Competitor mentions | High | Call transcripts, tickets |
| Budget review mentions | Medium | CSM notes |

### The Analytics Stack

| Layer | Purpose | Tools/Methods |
|-------|---------|---------------|
| **Collection** | Gather raw data | Product events, CRM, support |
| **Processing** | Clean and transform | ETL, data pipelines |
| **Calculation** | Compute scores | Scoring algorithms |
| **Storage** | Historical tracking | Data warehouse |
| **Visualization** | Present insights | Dashboards, reports |
| **Action** | Trigger interventions | Alerting, automation |

### Key Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| **Health Score Accuracy** | Churn predicted / Actual churn | >70% |
| **Leading Indicator Correlation** | Correlation to outcomes | >0.6 |
| **Score Distribution** | % in each health tier | Bell curve |
| **Intervention Success Rate** | Saved / Intervened | >40% |
| **Time to Detection** | Days before risk → action | <14 days |
| **False Positive Rate** | False alerts / Total alerts | <20% |

### Executive Dashboard KPIs

| KPI | Definition | Benchmark |
|-----|------------|-----------|
| **Gross Revenue Retention** | Retained ARR / Starting ARR | 85-95% |
| **Net Revenue Retention** | (Retained + Expansion) / Starting | 100-130% |
| **Logo Retention** | Retained customers / Starting | 90-95% |
| **Health Score Average** | Mean across customer base | 65-75 |
| **At-Risk Revenue** | ARR with health <50 | <15% |
| **Expansion Rate** | Customers expanded / Total | 15-30% |

### Cohort Analysis Framework

| Cohort Type | Segments By | Use Case |
|-------------|-------------|----------|
| **Time-based** | Sign-up month/quarter | Retention trends |
| **Behavioral** | Feature usage patterns | Activation success |
| **Value-based** | ARR tier | Segment economics |
| **Industry** | Vertical | Product-market fit |
| **Acquisition** | Channel/source | Marketing efficiency |

## Anti-Patterns

- **Vanity health scores** — Scores that look good but don't predict outcomes
- **Over-weighted product usage** — Ignoring relationship and sentiment signals
- **Lagging indicator focus** — Measuring what already happened
- **One-size-fits-all thresholds** — Same scores mean different things for different segments
- **Manual-only health tracking** — Can't scale without automation
- **Score without action** — Calculating risk without intervention playbooks
- **Annual calibration only** — Health models need continuous refinement
- **Ignoring data quality** — Garbage in, garbage out
