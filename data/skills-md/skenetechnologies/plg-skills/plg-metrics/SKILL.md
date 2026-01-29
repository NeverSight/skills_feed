---
name: plg-metrics
description: When the user wants to define PLG metrics, build a growth dashboard, or set KPI targets -- including activation rate, free-to-paid conversion, NRR, or North Star metric. Also use when the user says "PLG dashboard," "growth KPIs," "metric definitions," or "PLG benchmarks." For activation-specific metrics, see activation-metrics. For analytics setup, see product-analytics.
---

# PLG Metrics

You are a PLG metrics specialist. Build the definitive metrics framework for a product-led growth business. This skill helps you define, measure, and act on the KPIs that matter for PLG -- from acquisition through monetization and retention.

---

## Diagnostic Questions

Before building your metrics framework, answer these questions:

1. **What is your business model?** (freemium, free trial, open-source, reverse trial, usage-based)
2. **What is your primary growth loop?** (viral, content-led, sales-assisted, product-led)
3. **What is your product's core value action?** (the thing users do that delivers value)
4. **Who is your ideal user vs. buyer?** (same person or different?)
5. **What is your current stage?** (pre-PMF, early growth, scaling, mature)
6. **Do you have a sales team layered on top of PLG?** (pure PLG vs. product-led sales)
7. **What analytics tools do you currently use?**
8. **What metrics do you currently track, and what gaps exist?**

---

## The PLG Metrics Stack

### 1. Acquisition Metrics

These measure how effectively you attract new users into your product.

| Metric | Formula | Benchmark | Cadence |
|--------|---------|-----------|---------|
| **Signups** | Count of new account creations per period | Varies by stage | Daily/Weekly |
| **Signup-to-Activation Rate** | (Activated users / Total signups) x 100 | 20-40% | Weekly |
| **Organic vs. Paid Split** | % of signups from organic channels | >60% organic is healthy for PLG | Monthly |
| **Viral Coefficient (K-factor)** | Invites sent per user x invite acceptance rate | K > 1 = viral growth | Monthly |
| **CAC by Channel** | Total channel spend / New customers from channel | Varies; PLG should have low blended CAC | Monthly |
| **Signup Completion Rate** | (Completed signups / Started signups) x 100 | 70-90% | Weekly |

**Key insight**: In PLG, your product IS your acquisition channel. Track what percentage of new signups come from product-driven sources (referrals, shared content, embeds, word-of-mouth) vs. traditional marketing.

### 2. Activation Metrics

These measure whether new users experience your product's core value.

| Metric | Formula | Benchmark | Cadence |
|--------|---------|-----------|---------|
| **Activation Rate** | (Users reaching aha moment / Total signups) x 100 | 20-40% typical; top PLG companies 40-60% | Weekly |
| **Time-to-Value (TTV)** | Median time from signup to first value moment | Shorter is better; <5 min ideal for simple products | Weekly |
| **Setup Completion Rate** | (Users completing setup / Users starting setup) x 100 | 60-80% | Weekly |
| **Aha Moment Reach Rate** | (Users experiencing aha moment / Users completing setup) x 100 | 40-70% | Weekly |
| **Habit Formation Rate** | (Users who perform core action 3+ times in first week / Activated users) x 100 | 30-50% | Monthly |
| **Onboarding Funnel Completion** | Step-by-step drop-off through onboarding flow | Track each step independently | Weekly |

**Defining your Aha Moment**: The aha moment is when a user first experiences the core value of your product. It is NOT a feature -- it is an outcome. Examples:
- Slack: Sending 2,000+ messages as a team
- Dropbox: Putting a file in a Dropbox folder on one device and seeing it appear on another
- Zoom: Hosting a meeting with 3+ participants
- Figma: Creating a design and sharing it with a collaborator

### 3. Engagement Metrics

These measure ongoing product usage intensity and breadth.

| Metric | Formula | Benchmark | Cadence |
|--------|---------|-----------|---------|
| **DAU / WAU / MAU** | Count of unique users active in day/week/month | Absolute numbers; track growth rate | Daily |
| **DAU/MAU Ratio (Stickiness)** | DAU / MAU | SaaS: 10-25% typical, >25% excellent; Social: >50% | Weekly |
| **Session Frequency** | Average sessions per user per week | 3-5x/week for daily-use products | Weekly |
| **Feature Usage Breadth** | Average number of distinct features used per user | Varies; track trend over time | Monthly |
| **Feature Usage Depth** | Frequency of usage of core features | Track for top 5-10 features | Monthly |
| **Engagement Score** | Composite score based on weighted feature usage | Custom; normalize to 0-100 scale | Weekly |

**Building an Engagement Score**: Create a composite metric that combines multiple usage signals into a single score (0-100). Steps:

1. List the 5-10 most important actions in your product
2. Assign weights based on correlation with retention (use regression analysis)
3. Define thresholds for each action (e.g., "3+ projects created = 10 points")
4. Sum weighted scores and normalize to 0-100
5. Validate by checking if high-engagement-score users retain better

Example engagement score formula:
```
Engagement Score = (
  login_frequency_score x 0.15 +
  core_action_frequency x 0.30 +
  feature_breadth_score x 0.15 +
  collaboration_score x 0.25 +
  content_creation_score x 0.15
) x 100
```

### 4. Monetization Metrics

These measure how effectively you convert free users to paying customers and grow revenue.

| Metric | Formula | Benchmark | Cadence |
|--------|---------|-----------|---------|
| **Free-to-Paid Conversion Rate** | (New paying users / Total free users) x 100 | Freemium: 2-5%; Free trial: 10-25% | Monthly |
| **Natural Rate of Conversion** | (Users converting without sales touch / Total conversions) x 100 | >50% is strong PLG | Monthly |
| **Trial-to-Paid Rate** | (Users converting before trial end / Total trial starts) x 100 | 15-25% is good; >30% is excellent | Monthly |
| **ARPU** | Total revenue / Total users (including free) | Varies by segment | Monthly |
| **ARPPU** | Total revenue / Paying users only | Varies; track growth over time | Monthly |
| **Expansion MRR** | Additional MRR from existing customers (upgrades + add-ons) | >30% of new MRR should come from expansion | Monthly |
| **Net Revenue Retention (NRR)** | (Starting MRR + expansion - contraction - churn) / Starting MRR x 100 | 100-120% good; >130% excellent | Monthly/Quarterly |
| **LTV** | ARPU x Gross margin % / Monthly churn rate | LTV:CAC > 3:1 | Quarterly |

**Natural Rate of Conversion**: This is a uniquely PLG metric. It measures what percentage of your paid conversions happen without any sales intervention. A high natural rate (>60%) indicates your product is effectively selling itself. Track this separately from sales-assisted conversions.

### 5. Retention Metrics

These measure whether users continue to find value over time.

| Metric | Formula | Benchmark | Cadence |
|--------|---------|-----------|---------|
| **Logo Retention** | (Customers at end - New customers) / Customers at start x 100 | >85% monthly; >95% annual for enterprise | Monthly |
| **Dollar Retention (NRR)** | See monetization section | >100% means expansion exceeds churn | Monthly |
| **D1 / D7 / D30 Retention** | % of users returning on day 1, 7, 30 after signup | D1: 40-60%, D7: 25-40%, D30: 15-25% (varies widely) | Weekly |
| **Cohort Retention Curves** | Retention by signup cohort over time | Curves should flatten (not continue declining) | Monthly |
| **Resurrection Rate** | (Returning churned users / Total churned users) x 100 | 5-15% | Monthly |

**Reading Cohort Retention Curves**: The most important pattern to look for is whether the curve flattens. If your retention curve continues to decline month over month without leveling off, you have a product-market fit problem, not a retention problem.

```
Healthy curve:
Month 0: 100%
Month 1:  60%
Month 2:  45%
Month 3:  38%
Month 4:  35%  <-- flattening
Month 5:  34%
Month 6:  33%

Unhealthy curve:
Month 0: 100%
Month 1:  50%
Month 2:  30%
Month 3:  18%
Month 4:  11%  <-- still declining
Month 5:   7%
Month 6:   4%
```

### 6. PQL Metrics (Product-Led Sales)

If you layer sales on top of PLG, track Product Qualified Leads.

| Metric | Formula | Benchmark | Cadence |
|--------|---------|-----------|---------|
| **PQL Rate** | (Users qualifying as PQLs / Total active users) x 100 | 5-15% of active users | Weekly |
| **PQL-to-SQL Conversion** | (PQLs accepted by sales / Total PQLs) x 100 | 30-50% | Weekly |
| **PQL-to-Closed-Won Rate** | (PQLs that become customers / Total PQLs) x 100 | 15-30% (much higher than MQL rates) | Monthly |
| **PQL Velocity** | Number of new PQLs generated per week | Track growth rate | Weekly |
| **Time-to-PQL** | Median time from signup to PQL qualification | Varies; shorter is better | Monthly |

---

## North Star Metric

### Framework: Value x Frequency x Breadth

Your North Star Metric should capture the core value your product delivers, measured at a frequency that allows you to act on it, across the broadest relevant user base.

**Formula**: North Star = Value Delivered x Frequency of Delivery x Breadth of Users

### How to Define Your North Star

1. **Identify your core value proposition**: What outcome does your product enable?
2. **Find the proxy action**: What user action best represents value delivery?
3. **Add frequency**: How often should this action happen?
4. **Add breadth**: Should you measure per user, per team, or total?
5. **Validate**: Does this metric correlate with revenue and retention?

### North Star Examples by Product Type

| Product Type | North Star Metric | Why It Works |
|-------------|-------------------|--------------|
| **Collaboration tool** | Weekly active teams with 3+ active members | Captures value (collaboration), frequency (weekly), breadth (teams) |
| **Analytics platform** | Weekly queries run by activated accounts | Measures value extraction from data |
| **Design tool** | Weekly designs shared with collaborators | Captures creation + collaboration |
| **Developer tool** | Weekly API calls by integrated accounts | Measures actual product usage in production |
| **Project management** | Weekly tasks completed per active team | Captures productivity value delivered |
| **Communication tool** | Daily messages sent per active workspace | Measures communication value at daily frequency |
| **E-signature** | Monthly documents signed | Captures core transaction value |
| **Payments** | Weekly transaction volume processed | Directly tied to value and revenue |

### North Star Anti-patterns

- **Revenue as North Star**: Revenue is an output, not an input you can directly improve
- **Signups as North Star**: Measures top-of-funnel only, not value delivery
- **DAU as North Star**: Activity without value -- users can be active but not getting value
- **NPS as North Star**: Lagging indicator, hard to act on, survey-dependent

---

## Metric Definitions Template

For each metric in your framework, create a definition card:

```
### [Metric Name]

**Category**: [Acquisition / Activation / Engagement / Monetization / Retention / PQL]
**Formula**: [Exact calculation with numerator and denominator]
**Data Source**: [Which system/tool provides this data]
**Owner**: [Team or person responsible]
**Current Value**: [Baseline as of date]
**Target**: [Goal for this quarter/period]
**Benchmark**: [Industry benchmark range]
**Review Cadence**: [Daily / Weekly / Monthly / Quarterly]
**Leading or Lagging**: [Leading = predictive / Lagging = measures outcome]
**Segments to Break Down By**: [e.g., plan type, signup source, company size]
**Alert Thresholds**: [When to trigger alerts -- e.g., drops >10% week-over-week]
**Dependencies**: [Other metrics this influences or is influenced by]
**Notes**: [Any caveats, known data quality issues, or context]
```

---

## PLG Dashboard Design

### Executive Dashboard (Weekly/Monthly Review)

The executive dashboard answers: "Is the business healthy and growing?"

**Section 1 -- Headlines**
- North Star Metric (current + trend)
- MRR / ARR (current + growth rate)
- Active users (DAU/WAU/MAU + growth rate)

**Section 2 -- Funnel Health**
- Signups (volume + trend)
- Activation Rate (% + trend)
- Free-to-Paid Conversion Rate (% + trend)
- NRR (% + trend)

**Section 3 -- Unit Economics**
- Blended CAC
- LTV
- LTV:CAC ratio
- Payback period

**Section 4 -- Leading Indicators**
- PQL pipeline (volume + conversion)
- Engagement score distribution
- Expansion signals

### Team-Level Dashboards

**Growth Team Dashboard**:
- Signup volume by source, signup completion rate, activation rate by cohort, experiment results, viral coefficient

**Product Team Dashboard**:
- Feature adoption rates, feature usage depth, engagement score distribution, session metrics, feature-retention correlation

**Revenue Team Dashboard**:
- Free-to-paid conversion by segment, ARPU/ARPPU trends, expansion MRR, NRR by cohort, PQL pipeline

**Customer Success Dashboard**:
- Health scores, retention by cohort, churn risk signals, expansion opportunities, NPS/CSAT

---

## Leading vs. Lagging Indicators

| Leading Indicators (Predictive) | Lagging Indicators (Outcome) |
|--------------------------------|------------------------------|
| Activation rate | Revenue / MRR |
| Engagement score | Churn rate |
| Feature adoption velocity | NRR |
| PQL generation rate | LTV |
| Invite/sharing activity | Logo retention |
| Setup completion rate | Annual contract value |
| Time-to-value | Customer count |
| Session frequency trend | Market share |

**Key principle**: Manage by leading indicators, report on lagging indicators. Your team should focus their daily/weekly efforts on moving leading indicators, which will eventually move lagging indicators.

---

## Metric Anti-patterns

### 1. Vanity Metrics
Metrics that look impressive but do not drive decisions.
- **Total signups** (ever): Always goes up; tells you nothing about health
- **Page views**: Activity without value signal
- **Total registered users**: Includes churned/dead accounts
- **App downloads**: Does not mean usage

**Fix**: Replace with rate-based or active-user-based metrics.

### 2. Over-indexing on One Metric
Optimizing a single metric at the expense of the whole system.
- Maximizing signups by reducing friction, leading to low-quality users and poor activation
- Maximizing free-to-paid conversion by restricting the free tier, killing viral growth
- Maximizing engagement by adding notifications that annoy users

**Fix**: Use guardrail metrics -- secondary metrics that must not degrade while you optimize the primary.

### 3. Metric Gaming
When the measure becomes the target, it ceases to be a good measure (Goodhart's Law).
- Sales team cherry-picking PQLs to inflate conversion rates
- Product team redefining "active" to include trivial actions
- Marketing inflating signup numbers with low-intent channels

**Fix**: Audit metric definitions regularly. Use composite metrics that are harder to game. Separate the metric from incentive structures.

### 4. Measuring Too Late
Only tracking lagging indicators means you discover problems after the damage is done.

**Fix**: For every lagging indicator, identify 2-3 leading indicators that predict it.

---

## Benchmarks Reference

### Activation Rate
- **Below 15%**: Significant onboarding or PMF issues
- **15-25%**: Below average; room for improvement
- **25-40%**: Average for most PLG products
- **40-60%**: Strong; typical of top-performing PLG companies
- **60%+**: Exceptional; usually simple products with clear value props

### Free-to-Paid Conversion
- **Freemium model**: 2-5% of all free users (measured over lifetime)
- **Free trial (14-day)**: 10-20%
- **Free trial (30-day)**: 8-15%
- **Reverse trial**: 15-30% (higher because users experience premium first)
- **Usage-based / metered**: 5-10% (conversion triggered by usage limits)

### Net Revenue Retention (NRR)
- **Below 90%**: Serious churn problem
- **90-100%**: Acceptable but no expansion to offset churn
- **100-110%**: Good; expansion slightly exceeds churn
- **110-130%**: Strong; healthy expansion revenue
- **130%+**: Exceptional (e.g., Snowflake, Twilio, Datadog)

### DAU/MAU Ratio
- **Below 10%**: Monthly-use product or engagement problem
- **10-20%**: Typical for most B2B SaaS
- **20-30%**: Strong daily engagement
- **30-50%**: Very sticky (e.g., Slack, core workflow tools)
- **50%+**: Social media territory; rare for B2B

### D1/D7/D30 Retention
- Highly variable by product type. Use your own cohort data as the primary benchmark.
- Consumer apps: D1 40%, D7 20%, D30 10%
- B2B SaaS: D1 50-70%, D7 30-50%, D30 20-35%

---

## Setting Targets

### Step-by-Step Target-Setting Process

1. **Establish baselines**: Measure current state for at least 4-8 weeks to establish stable baselines
2. **Benchmark comparison**: Compare your metrics against the benchmarks above and category-specific data
3. **Gap analysis**: Identify your largest gaps between current state and benchmarks
4. **Prioritize**: Focus on the 2-3 metrics with the largest gap AND the highest impact on your North Star
5. **Set improvement goals**: Use the following framework:
   - **Conservative**: 10-15% improvement per quarter
   - **Moderate**: 15-30% improvement per quarter
   - **Aggressive**: 30-50% improvement per quarter (only if you have a clear lever to pull)
6. **Decompose**: Break the target into weekly milestones so you can track progress
7. **Review and adjust**: Re-evaluate targets monthly; adjust if assumptions change

### Target-Setting Template

```
Metric: [Name]
Current Baseline: [Value as of date, based on N weeks of data]
Industry Benchmark: [Range]
Gap: [Baseline vs. benchmark]
Q[X] Target: [Specific number]
Weekly Milestone: [Incremental target]
Key Lever: [What initiative will move this metric]
Owner: [Person/team]
Guardrail Metrics: [What must not degrade]
```

---

## Output Format

When using this skill, produce two deliverables:

### Deliverable 1: PLG Metrics Definition Document

A comprehensive document defining every metric the company tracks, using the metric definition template above. Organize by category (Acquisition, Activation, Engagement, Monetization, Retention, PQL).

### Deliverable 2: Dashboard Specification

A specification for building dashboards, including:
- Dashboard name and audience
- Metrics included with exact definitions
- Visualization type for each metric (line chart, bar chart, big number, table)
- Time range and granularity
- Filters and breakdowns available
- Alert/threshold configurations
- Data source and refresh cadence

---

## Cross-References

Related skills: `activation-metrics`, `retention-analysis`, `growth-modeling`, `product-analytics`
