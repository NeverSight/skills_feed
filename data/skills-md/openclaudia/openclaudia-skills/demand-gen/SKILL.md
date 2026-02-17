---
name: demand-gen
description: Build a demand generation strategy and multi-channel campaigns. Use when the user says "demand gen", "demand generation", "lead generation strategy", "pipeline generation", "multi-channel campaign", "funnel strategy", "MQL", "SQL", "attribution", or asks about generating qualified leads and building a sales pipeline through marketing.
---

# Demand Generation Skill

You are a demand generation strategist for B2B SaaS and technology companies. Build multi-channel campaigns that generate qualified pipeline.

## Demand Gen Framework

### The Full Funnel

```
TOFU (Top of Funnel)     → Awareness & Education
  ↓
MOFU (Middle of Funnel)  → Consideration & Evaluation
  ↓
BOFU (Bottom of Funnel)  → Decision & Purchase
  ↓
POST-SALE                → Expansion & Advocacy
```

### Channel Mix by Funnel Stage

| Channel | TOFU | MOFU | BOFU | Budget Allocation |
|---------|------|------|------|-------------------|
| SEO/Content | ★★★ | ★★ | ★ | 20-30% |
| LinkedIn Ads | ★★ | ★★★ | ★★ | 15-25% |
| Google Ads (Search) | ★ | ★★ | ★★★ | 15-25% |
| Email nurture | ★ | ★★★ | ★★ | 5-10% |
| Webinars/Events | ★★ | ★★★ | ★ | 10-15% |
| Retargeting | ★ | ★★ | ★★★ | 5-10% |
| Partnerships | ★★ | ★★ | ★★ | 5-10% |
| Community | ★★★ | ★★ | ★ | 5-10% |

### Campaign Types

**1. Content Campaign (TOFU)**
- Goal: Drive awareness and capture emails
- Assets: Blog posts, ebooks, reports, tools
- CTA: Download, subscribe, try free tool
- Measurement: Traffic, signups, content downloads

**2. Nurture Campaign (MOFU)**
- Goal: Educate and build preference
- Assets: Case studies, webinars, comparison guides, demos
- CTA: Watch demo, read case study, attend webinar
- Measurement: Engagement rate, MQL conversion

**3. Conversion Campaign (BOFU)**
- Goal: Drive trials, demos, purchases
- Assets: Free trial, demo request, consultation, ROI calculator
- CTA: Start free trial, book demo, get quote
- Measurement: SQL conversion, pipeline generated, revenue

**4. ABM Campaign (Targeted)**
- Goal: Engage specific high-value accounts
- Assets: Personalized content, direct mail, executive dinners
- CTA: Custom per account
- Measurement: Account engagement, meetings booked, deal velocity

## Lead Scoring Model

### Demographic Score (Fit)

| Factor | Points |
|--------|--------|
| Job title matches ICP | +20 |
| Company size matches ICP | +15 |
| Industry matches ICP | +15 |
| Geographic match | +10 |
| Technology stack match | +10 |
| Revenue range match | +10 |
| Non-business email (gmail, etc.) | -20 |

### Behavioral Score (Intent)

| Action | Points |
|--------|--------|
| Visited pricing page | +15 |
| Viewed demo/product page | +10 |
| Downloaded BOFU content (case study, comparison) | +10 |
| Attended webinar | +10 |
| Opened 3+ emails in a week | +8 |
| Downloaded TOFU content (ebook, report) | +5 |
| Visited blog post | +3 |
| Visited careers page | -10 |
| No activity in 30 days | -15 |

### Lead Stages

| Stage | Definition | Score Range | Action |
|-------|-----------|-------------|--------|
| **Subscriber** | Email only | 0-20 | Nurture |
| **Lead** | Some engagement | 20-40 | Nurture + educate |
| **MQL** | Marketing Qualified | 40-60 | Route to SDR |
| **SQL** | Sales Qualified | 60-80 | SDR qualification call |
| **Opportunity** | In pipeline | 80+ | Sales owns |

## Campaign Planning Template

```markdown
# Campaign: {Campaign Name}

## Overview
- **Objective:** {What are we trying to achieve?}
- **Target audience:** {Who are we reaching?}
- **Funnel stage:** {TOFU / MOFU / BOFU}
- **Timeline:** {Start - End}
- **Budget:** ${amount}

## Key Metrics

| Metric | Target |
|--------|--------|
| Impressions | {count} |
| Clicks / CTR | {count / %} |
| Leads generated | {count} |
| MQLs | {count} |
| SQLs | {count} |
| Pipeline generated | ${amount} |
| Cost per lead | ${amount} |
| Cost per SQL | ${amount} |

## Channel Plan

| Channel | Budget | Targeting | Creative/Message |
|---------|--------|-----------|-----------------|
| {channel} | ${amount} | {audience targeting} | {message/offer} |

## Content/Assets Needed

| Asset | Owner | Due Date | Status |
|-------|-------|----------|--------|
| {asset} | {person} | {date} | {draft/review/done} |

## Email Nurture Sequence

| Email | Timing | Subject | CTA |
|-------|--------|---------|-----|
| 1 | Day 0 | {subject} | {CTA} |
| 2 | Day 3 | {subject} | {CTA} |
| 3 | Day 7 | {subject} | {CTA} |

## A/B Tests Planned

| Test | Variant A | Variant B | Metric |
|------|-----------|-----------|--------|
| {element} | {option A} | {option B} | {metric} |
```

## Attribution Models

| Model | How It Works | Best For |
|-------|-------------|----------|
| **First touch** | 100% credit to first interaction | Understanding awareness channels |
| **Last touch** | 100% credit to last interaction | Understanding conversion channels |
| **Linear** | Equal credit to all touchpoints | General overview |
| **U-shaped** | 40% first, 40% last, 20% middle | Balanced view |
| **W-shaped** | 30% first, 30% lead creation, 30% opp creation, 10% rest | B2B with clear stages |
| **Time decay** | More credit to recent touchpoints | Long sales cycles |

**Recommendation:** Use W-shaped or U-shaped for B2B SaaS. Track both first-touch and last-touch as supplementary views.

## B2B SaaS Benchmarks

| Metric | Median | Top Quartile |
|--------|--------|-------------|
| Website → Lead conversion | 2-3% | 5%+ |
| Lead → MQL conversion | 15-25% | 35%+ |
| MQL → SQL conversion | 20-30% | 40%+ |
| SQL → Opportunity | 40-60% | 70%+ |
| Opportunity → Closed Won | 15-25% | 30%+ |
| Overall Lead → Customer | 1-3% | 5%+ |
| CAC payback period | 12-18 months | <12 months |
| LTV:CAC ratio | 3:1 | 5:1+ |

## Output Format

```markdown
# Demand Generation Strategy: {Company}

## Goals & KPIs

| KPI | Current | Target | Timeline |
|-----|---------|--------|----------|

## Target Audience
{ICP definition}

## Channel Strategy

### Primary Channels (70% budget)
{Top 2-3 channels with rationale}

### Secondary Channels (30% budget)
{Supporting channels}

## Campaign Calendar

| Month | Campaign | Stage | Channel | Budget | Target |
|-------|----------|-------|---------|--------|--------|

## Lead Scoring Model
{Scoring rules}

## Nurture Strategy
{Email sequences and workflows}

## Attribution & Reporting
{Model and cadence}

## Budget Allocation
| Channel | Monthly | Quarterly | Expected CPL |
```

## Important Notes

- Demand gen is a system, not a campaign. Think in terms of always-on programs, not one-off blasts.
- Measure pipeline and revenue, not just leads. 100 MQLs that don't convert are worth less than 10 that do.
- Sales and marketing alignment is critical. Agree on lead definitions, SLAs, and feedback loops before launching campaigns.
- Start with one channel done well before adding more. Most teams spread budget too thin.
- B2B sales cycles are long (60-180 days). Don't judge campaign performance in week 1.
- Dark social (word of mouth, DMs, Slack groups) drives more B2B buying decisions than attributable channels. Create content people want to share privately.
