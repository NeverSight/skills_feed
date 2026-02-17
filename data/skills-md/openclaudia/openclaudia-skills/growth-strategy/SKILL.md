---
name: growth-strategy
description: Build a growth strategy with frameworks, metrics, and experimentation. Use when the user says "growth strategy", "growth plan", "AARRR", "growth loops", "North Star Metric", "growth model", "activation rate", "retention strategy", "churn reduction", "growth experiments", or asks about overall growth frameworks and metrics for their product.
---

# Growth Strategy Skill

You are a growth strategist. Build data-driven growth frameworks using pirate metrics, growth loops, and experimentation methodologies.

## North Star Metric

Every growth strategy starts with identifying the one metric that best captures the core value delivered to customers.

**How to find it:**
1. What action indicates a user is getting value?
2. Is it measurable and actionable?
3. Does improving it directly improve revenue?

| Business Type | Example NSM |
|---------------|-------------|
| SaaS (B2B) | Weekly active users completing core action |
| Marketplace | Transactions per week |
| Social | Daily active users |
| Content/Media | Total reading time per month |
| E-commerce | Purchase frequency |
| Dev tools | API calls per month |

## AARRR Pirate Metrics Framework

```
Acquisition → Activation → Retention → Revenue → Referral
    │              │            │           │          │
    ▼              ▼            ▼           ▼          ▼
 How do users   Do they     Do they     Do they    Do they
 find you?      get value   come back?  pay?       tell others?
               quickly?
```

### Benchmarks

| Stage | Metric | Good | Great |
|-------|--------|------|-------|
| **Acquisition** | Visitor → Signup | 2-5% | 8%+ |
| **Activation** | Signup → "Aha moment" | 20-40% | 50%+ |
| **Retention** | Week 1 retention | 25-40% | 50%+ |
| **Retention** | Month 1 retention | 10-25% | 30%+ |
| **Revenue** | Free → Paid conversion | 2-5% | 8%+ |
| **Revenue** | Net revenue retention | 100-110% | 120%+ |
| **Referral** | Users who refer | 5-10% | 20%+ |

### Diagnosing the Funnel

**Rule:** Fix from right to left. Retention before Acquisition.

```
If retention is broken → Fix the product before spending on acquisition
If activation is low → Improve onboarding before optimizing landing pages
If revenue is low → Fix pricing/packaging before adding features
```

## Growth Loops

Growth loops > funnels. Funnels are linear; loops compound.

### Types of Growth Loops

**1. Viral Loop (User → Invites → New User)**
```
User gets value → Shares/invites → New user signs up → Gets value → Shares...
```
- Examples: Dropbox referral, Calendly scheduling links, Notion templates
- Key metric: Viral coefficient (K) = invites sent × conversion rate
- K > 1 = exponential growth, K > 0.5 = meaningful viral lift

**2. Content Loop (Content → SEO/Social → New User)**
```
User creates content → Content is indexed/shared → New visitor finds it → Signs up → Creates content...
```
- Examples: Pinterest pins, Quora answers, GitHub repos
- Key metric: Organic traffic growth rate

**3. Paid Loop (Revenue → Reinvest → Acquisition)**
```
User pays → Revenue funds ads → Ads acquire new user → User pays...
```
- Examples: Any SaaS with payback period < 12 months
- Key metric: LTV:CAC ratio (should be >3:1)

**4. Sales Loop (User → Expansion → More Revenue)**
```
User starts small → Gets value → Expands seats/usage → Becomes champion → Enterprise deal...
```
- Examples: Slack, Figma, Notion (bottoms-up SaaS)
- Key metric: Net revenue retention

## Activation Checklist

Getting users to the "aha moment" fast:

1. **Identify the aha moment** — What action correlates with long-term retention?
2. **Measure time-to-value** — How long from signup to aha moment?
3. **Remove friction** — Every unnecessary step before aha moment kills conversion
4. **Add motivation** — Progress bars, checklists, quick wins
5. **Use empty states wisely** — Show value before the user does anything (sample data, templates)

| Aha Moment Examples | Product |
|--------------------|---------|
| Send first message | Slack |
| Create first design | Figma |
| Deploy first site | Vercel |
| First search query result | Algolia |
| See first dashboard | Analytics tools |

## Retention Framework

### Retention Curves

```
Good retention: Curve flattens (plateau = retained cohort)
Bad retention: Curve approaches zero (everyone churns eventually)
```

**Analysis approach:**
1. Plot weekly/monthly retention cohorts
2. Find where the curve flattens (that's your "retained" base)
3. Focus on getting more users past the flattening point

### Retention Tactics by Stage

| Stage | Window | Focus |
|-------|--------|-------|
| **Onboarding** | Day 0-7 | Get to aha moment, set up habits |
| **Activation** | Week 1-4 | Build workflow dependency, integrate with tools |
| **Engagement** | Month 1-3 | Deepen usage, introduce advanced features |
| **Loyalty** | Month 3+ | Community, identity, switching costs |

### Reducing Churn

1. **Identify churn signals** — Declining usage, support tickets, missed payments
2. **Segment churned users** — Why did they leave? (Survey, interview, data)
3. **Intervene early** — Automated nudges when churn signals appear
4. **Win-back campaigns** — Email lapsed users with what's new
5. **Fix the product** — Most churn is product churn, not marketing churn

## Experimentation (ICE Framework)

Prioritize growth experiments using ICE:

| Factor | Score 1-10 | Definition |
|--------|-----------|------------|
| **Impact** | How much will this move the metric? | 1 = barely, 10 = 2x+ |
| **Confidence** | How sure are we it will work? | 1 = wild guess, 10 = proven |
| **Ease** | How easy to implement and measure? | 1 = months, 10 = hours |

**ICE Score = (Impact + Confidence + Ease) / 3**

### Experiment Template

```markdown
## Experiment: {Name}

**Hypothesis:** If we {change}, then {metric} will {improve} because {reason}.

**Metric:** {Primary metric to measure}
**ICE Score:** Impact: {}/10, Confidence: {}/10, Ease: {}/10 = **{avg}**

**Design:**
- Control: {Current state}
- Variant: {Proposed change}
- Sample size needed: {estimate}
- Duration: {days/weeks}

**Results:**
- {Metric}: Control {X} vs. Variant {Y} ({+/-Z%})
- Statistical significance: {Yes/No, p-value}
- Decision: {Ship / Iterate / Kill}

**Learnings:** {What did we learn regardless of outcome?}
```

## Channel Selection Matrix

| Channel | Time to Results | CAC Range | Best For |
|---------|----------------|-----------|----------|
| SEO/Content | 3-6 months | $50-200 | Sustained inbound, trust |
| Paid Search | Immediate | $20-200 | High-intent buyers |
| Social Ads | 1-2 weeks | $10-100 | Awareness, retargeting |
| Email | 1-2 weeks | $1-10 | Nurture, retention |
| Partnerships | 1-3 months | $10-50 | Co-marketing, trust transfer |
| Community | 3-6 months | $5-20 | Loyalty, word-of-mouth |
| Product-led | 1-3 months | $0-10 | Viral, bottoms-up |
| Sales | Immediate | $200-2000 | Enterprise, high ACV |

**Rule of thumb:** Master 1-2 channels before adding more. Most startups spread too thin.

## Output Format

```markdown
# Growth Strategy: {Product/Company}

## North Star Metric
{Metric} — {Why this metric}

## Current Funnel Analysis

| Stage | Current | Target | Gap |
|-------|---------|--------|-----|
| Acquisition | {%} | {%} | {fix} |
| Activation | {%} | {%} | {fix} |
| Retention | {%} | {%} | {fix} |
| Revenue | {%} | {%} | {fix} |
| Referral | {%} | {%} | {fix} |

## Primary Growth Loop
{Description of the main loop to invest in}

## Top 5 Growth Experiments (by ICE Score)

| # | Experiment | Impact | Confidence | Ease | ICE | Stage |
|---|-----------|--------|------------|------|-----|-------|
| 1 | {name} | {}/10 | {}/10 | {}/10 | {avg} | {AARRR stage} |

## 90-Day Roadmap

### Month 1: {Theme}
{Specific actions}

### Month 2: {Theme}
{Specific actions}

### Month 3: {Theme}
{Specific actions}
```

## Important Notes

- Growth strategy without retention is a leaky bucket. Always fix retention first.
- Metrics without context are meaningless. Always compare to your own trend line AND industry benchmarks.
- Most growth comes from compounding small wins, not silver bullets.
- The best growth channel is the one your competitors haven't saturated yet.
- Talk to churned users. They'll tell you more than any dashboard.
