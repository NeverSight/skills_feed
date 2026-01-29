---
name: user-segmentation
description: When the user wants to segment users for personalized experiences -- including behavioral cohorts, engagement scoring, churn risk scoring, or ICP refinement. Also use when the user says "user segments," "cohort analysis," "power users," "at-risk users," "RFM analysis," or "user scoring." For product-led sales, see product-led-sales. For retention, see retention-analysis.
---

# User Segmentation

You are a user segmentation specialist. Divide your user base into meaningful groups so you can deliver the right experience, messaging, and upgrade path to each user. In PLG, segmentation is the difference between a generic product that sort of works for everyone and a personalized experience that converts each user type optimally.

---

## 1. Diagnostic Questions

Before building your segmentation strategy, answer these:

1. **What data do you collect about users?** (Profile data, usage events, billing data, firmographic data)
2. **How many active users do you have?** (Segments need sufficient sample sizes -- at least 100-200 users per segment)
3. **Do you have a way to act on segments?** (Can you target messages, emails, features, or experiences by segment?)
4. **What decisions are you trying to inform?** (Onboarding, messaging, pricing, sales outreach, feature development)
5. **Do you already have implicit segments?** (Different plans, roles, use cases that naturally separate users)
6. **What is your activation metric?** (Needed to segment by lifecycle stage)
7. **What engagement data do you track?** (Feature usage, session frequency, depth of usage)
8. **Do you have churn prediction signals?** (Declining usage, support tickets, failed payments)

---

## 2. Segmentation Dimensions

### 2.1 Behavioral Segmentation

| Dimension | How to Measure | Use Case |
|---|---|---|
| Usage frequency | Sessions per week, DAU/WAU/MAU ratios | Identify power users vs casual |
| Feature usage patterns | Features used, feature breadth, feature depth | Recommend features, personalize onboarding |
| Engagement depth | Time in product, actions per session, content created | Measure value received |
| Collaboration activity | Invites sent, shared content, team interactions | Identify expansion potential |
| Growth signals | Increasing usage, new feature adoption, team growth | Identify upgrade candidates |
| Decline signals | Decreasing frequency, fewer features used, shorter sessions | Identify churn risk |

**Example behavioral segments:**
```
Segment: Power Users
  Criteria: Sessions/week >= 5, Feature breadth >= 70%, Active 30+ days
  Size: ~10% | Action: Expansion offers, beta access, advocacy program

Segment: Regular Users
  Criteria: Sessions/week 2-4, Feature breadth 30-69%, Active 14+ days
  Size: ~30% | Action: Feature adoption campaigns, engagement deepening

Segment: Casual Users
  Criteria: Sessions/week 0.5-1, Feature breadth <30%, Active 7+ days
  Size: ~35% | Action: Activation nudges, value demonstration, use case guidance

Segment: At-Risk Users
  Criteria: 50%+ session drop week-over-week OR no sessions in 7+ days
  Size: ~15% | Action: Re-engagement campaigns, feedback requests, support outreach

Segment: Dormant Users
  Criteria: No activity in 30+ days, previously had 3+ sessions
  Size: ~10% | Action: Win-back campaigns, sunset communications
```

### 2.2 Firmographic Segmentation

| Dimension | Sources | Use Case |
|---|---|---|
| Company size | Signup form, enrichment (Clearbit, ZoomInfo) | Pricing, features, sales motion |
| Industry | Signup form, enrichment, email domain | Use case messaging, templates |
| Role/title | Signup form, enrichment | Onboarding path, feature emphasis |
| Geography | IP, signup form, billing | Compliance, localization, pricing |
| Tech stack | Enrichment, integrations used | Integration recommendations |

### 2.3 Lifecycle Segmentation

```
1. New User (Day 0-3): Hasn't completed activation. Goal: activation.
2. Activated (Day 1-14): Completed activation, not yet habitual. Goal: build habit.
3. Engaged (Day 7-90): Regular usage, multiple sessions/week. Goal: expand value, prepare upgrade.
4. Power User (Day 30+): Top 10% usage, broad feature adoption. Goal: expand seats, upgrade, advocacy.
5. At-Risk (Any time): Usage declining from personal baseline. Goal: re-engage before churn.
6. Churned (After inactivity threshold): No activity beyond threshold. Goal: win-back, learn from churn.
```

### 2.4 Intent Segmentation

| Intent Segment | Signals | Experience |
|---|---|---|
| **Evaluator** | Short sessions, viewing pricing/docs, comparing features | Clear value prop, competitor comparison, trial extension |
| **Individual User** | Using product alone, personal use case | Individual plans, personal templates, solo workflows |
| **Team Champion** | Inviting team members, sharing content, admin actions | Team features, collaboration tools, team pricing |
| **Buyer** | Visiting pricing page, contacting sales, requesting quotes | Sales handoff, custom pricing, security docs |
| **Admin/IT** | Configuring SSO, reviewing security, managing seats | Admin tools, compliance info, enterprise features |

### 2.5 Plan/Tier Segmentation

| Plan Segment | Focus |
|---|---|
| **Free plan** | Demonstrate value, encourage activation, show upgrade path |
| **Trial** | Maximize trial activation, guide toward key value, conversion prompts |
| **Basic/Starter** | Deepen engagement, show value of higher tier features |
| **Pro/Business** | Team expansion, advanced feature adoption, retention |
| **Enterprise** | Account health, expansion, executive engagement |

---

## 3. Behavioral Cohort Creation

### 3.1 Power Users

**Identification criteria (use 2-3):**
- Top 10% by session frequency, feature breadth, or content created
- Consistent usage for 30+ consecutive days
- Using advanced/premium features regularly

**Actions:** Beta access, advisory board, referral prompts, expansion paths, study behavior to improve onboarding for others.

### 3.2 Champions

Power users who also exhibit expansion and advocacy signals:
- Invited 2+ team members
- Share content externally
- NPS 9-10
- Engage with community positively

### 3.3 At-Risk Users

**Detection signals:**
```
Signal: Usage frequency decline
  Rule: Current week sessions < 50% of 4-week trailing average

Signal: Feature breadth contraction
  Rule: Features used this week < 50% of peak week

Signal: Login gap
  Rule: Days since last login > 2x typical inter-session gap

Signal: Support escalation
  Rule: 2+ support tickets in 7 days, or negative sentiment

Composite at-risk score: Each signal = 1 point. 2+ signals = at-risk.
```

### 3.4 Dormant Users

**Thresholds (adjust for your product's usage cadence):**
- Daily-use product: No login for 7+ days
- Weekly-use product: No login for 21+ days
- Monthly-use product: No login for 60+ days

**Sub-segments:** Lapsed after activation (higher win-back potential), never activated (diagnose why), churned after paying (highest value to win back).

---

## 4. User Scoring Models

### 4.1 Engagement Score

```
Engagement Score Components (0-100):

Usage frequency (0-30 points):
  7+ sessions/week: 30 | 4-6: 20 | 2-3: 12 | 1: 5 | <1: 0

Feature breadth (0-25 points):
  80%+ features: 25 | 50-79%: 18 | 25-49%: 10 | <25%: 3

Engagement depth (0-25 points):
  Avg session > 30 min: 25 | 15-30: 18 | 5-15: 10 | <5: 3

Recency (0-20 points):
  Today: 20 | 1-3 days: 15 | 4-7 days: 8 | 8-14 days: 3 | 14+: 0

Tiers:
  80-100: Highly engaged (power user)
  60-79: Engaged (regular)
  40-59: Moderate (casual)
  20-39: Low (at risk)
  0-19: Disengaged (dormant/churning)
```

### 4.2 Activation Score

```
Activation Score (customize milestones per product):

Example for a project management tool:
  Created first project: 20 pts | Added first task: 15 pts
  Invited team member: 25 pts | Completed first task: 15 pts
  Used template: 10 pts | Connected integration: 15 pts

Tiers:
  80-100: Fully activated
  50-79: Partially activated (nudge remaining steps)
  20-49: Early activation (guide next steps)
  0-19: Not activated (immediate onboarding attention)
```

### 4.3 Expansion Readiness Score

```
Expansion Readiness Score (0-100):

Usage approaching limits (0-25): 80%+ of limits: 25 | 60-79%: 15 | 40-59%: 5
Team growth signals (0-25): Added members recently: 15 | Using collab features: 10
Feature interest signals (0-25): Clicked locked features: 15 | Viewed pricing: 10
Engagement level (0-25): Score >70: 25 | 50-70: 15 | 30-50: 5

Tiers:
  75-100: High readiness (proactive outreach, upgrade prompts)
  50-74: Moderate (nurture, show higher-tier value)
  25-49: Low (deepen current engagement first)
  0-24: Not ready (focus on activation and value delivery)
```

### 4.4 Churn Risk Score

```
Churn Risk Score (0-100):

Usage decline (0-30): 70%+ decline: 30 | 50-69%: 20 | 30-49%: 10
Recency gap (0-25): 2x typical gap: 25 | 1.5x: 15 | 1x: 5
Support signals (0-20): Negative interactions: 20 | Multiple tickets: 10
Billing signals (0-15): Failed payment: 15 | Downgraded: 10 | Viewed cancel page: 10
Engagement trend (0-10): Declining: 10 | Stable/increasing: 0

Tiers:
  70-100: High risk (immediate intervention)
  40-69: Moderate risk (proactive outreach)
  20-39: Low risk (monitor)
  0-19: Healthy
```

---

## 5. Segmentation for Personalization

### 5.1 Onboarding Paths by Segment

```
IF user.role == "designer":
  Flow: Design templates, design tool integrations, visual workspace
  First action: "Create your first design project"

IF user.role == "developer":
  Flow: API docs, code integration, developer workspace
  First action: "Connect your first repository"

IF user.role == "manager":
  Flow: Team setup, reporting, collaboration features
  First action: "Invite your team"

IF user.role == "unknown":
  Flow: General flow with role selection step
```

### 5.2 Feature Recommendations by Usage Pattern

```
IF user uses feature A frequently AND has never used feature B:
  AND feature A users who also use B have 30% higher retention:
  THEN recommend B: "Users who use [A] love [B] because [benefit]"

Implementation:
  1. Build feature affinity matrix (which features power users combine)
  2. For each user, find gaps vs similar power users
  3. Surface top 1-2 recommendations via in-product messaging
```

### 5.3 Upgrade Messaging by Engagement Level

| Engagement Level | Upgrade Strategy | Message Tone |
|---|---|---|
| Power user (80-100) | Aggressive upgrade prompts, usage-limit nudges | "You're getting incredible value. Unlock even more with [Plan]." |
| Engaged (60-79) | Feature-based upgrade prompts | "You might like [premium feature] based on how you use [Product]." |
| Moderate (40-59) | Value demonstration before upgrade ask | "Here are 3 things you haven't tried yet." |
| Low (20-39) | Focus on engagement, not upgrades | "We noticed you haven't been back. Here's what's new." |
| Disengaged (0-19) | Re-engagement, not upgrade | "We miss you. Come back and see [new feature]." |

---

## 6. Implementing Segmentation

### 6.1 Event-Based Rules

```
segment "Power Users" {
  conditions {
    events.session_count(last_7_days) >= 5
    AND events.unique_features_used(last_30_days) >= 0.7 * total_features
    AND user.days_since_signup >= 30
  }
  refresh: daily
}

segment "At Risk" {
  conditions {
    events.session_count(last_7_days) < 0.5 * events.avg_weekly_sessions(last_28_days)
    AND events.avg_weekly_sessions(last_28_days) >= 2
  }
  refresh: daily
}

segment "Expansion Ready" {
  conditions {
    scores.engagement >= 60
    AND (
      usage.percentage_of_limit >= 0.7
      OR events.pricing_page_view(last_14_days) >= 1
      OR events.locked_feature_click(last_14_days) >= 1
    )
  }
  refresh: daily
}
```

### 6.2 ML-Based vs Rule-Based

**Use ML clustering when:** You suspect undiscovered user groups, have 10,000+ users with rich behavioral data, have data science resources.

**Use rule-based segments when:** You know your segments (lifecycle, plan, role), have <10,000 users, need easy-to-explain segments.

### 6.3 RFM Analysis

```
RFM Scoring (1-5 each):

Recency: 5=Today, 4=1-3 days, 3=4-7 days, 2=8-14 days, 1=15+ days
Frequency: 5=Daily, 4=4-6x/week, 3=2-3x/week, 2=Weekly, 1=<Weekly
Monetary (plan value, seat count, or usage volume):
  5=Enterprise/highest, 4=Pro/high usage, 3=Basic paid, 2=Active free, 1=Inactive free

RFM Segments:
  555, 554, 545: Champions -- nurture, upsell, advocacy
  444, 445, 455: Loyal -- deepen engagement, expand
  334, 343, 344: Promising -- increase frequency, feature adoption
  233, 234, 244: Need attention -- re-engage, show value
  111, 112, 121: Lost -- win-back campaign or sunset
```

---

## 7. Segmentation in Practice

### 7.1 Email Campaigns by Segment

| Segment | Campaign | Frequency | Content |
|---|---|---|---|
| New (not activated) | Onboarding drip | Daily x 7 days | Step-by-step activation guidance |
| Activated (not engaged) | Feature discovery | 2x/week x 2 weeks | Highlight unused features |
| Engaged (free) | Upgrade nurture | 1x/week | Paid plan value, success stories |
| At-risk (any plan) | Re-engagement | 1x immediate, then 1x/week | Value reminder, feedback ask |
| Churned | Win-back | At churn, 30 days, 90 days | What's new, special offer, survey |

### 7.2 Sales Prioritization (PLS)

```
Tier 1 (Hot -- sales-assist immediately):
  Expansion readiness > 75, 5+ active users, pricing page 2x in last week, enterprise signals

Tier 2 (Warm -- outreach within 1 week):
  Expansion readiness 50-75, 3+ active users, using team/collab features

Tier 3 (Nurture -- marketing-led):
  Expansion readiness 25-49, individual user, no team signals

Tier 4 (No action):
  Expansion readiness < 25, not activated or disengaged
```

---

## 8. ICP Refinement

```
Step 1: Identify best customers (top 20% by retention + revenue + engagement)
Step 2: Find common attributes (firmographic, behavioral, channel)
Step 3: Compare to worst customers (bottom 20% by retention)
Step 4: Refine ICP -- current vs data-informed, document delta
Step 5: Action -- update targeting, adjust messaging, deprioritize churning segments, inform roadmap
```

---

## 9. Segment Analysis

### 9.1 Cross-Segment Comparison Dashboard

```
| Metric | Power Users | Regular | Casual | At-Risk | Dormant |
|---|---|---|---|---|---|
| Segment size | [N] ([%]) | [N] ([%]) | [N] ([%]) | [N] ([%]) | [N] ([%]) |
| 30-day retention | [%] | [%] | [%] | [%] | [%] |
| Paid conversion | [%] | [%] | [%] | [%] | [%] |
| Avg revenue | [$] | [$] | [$] | [$] | [$] |
| LTV | [$] | [$] | [$] | [$] | [$] |
```

### 9.2 Movement Analysis

```
Segment transition matrix (monthly):

From \ To    | Power | Regular | Casual | At-Risk | Dormant | Churned
Power        | 85%   | 10%     | 2%     | 2%      | 1%      | 0%
Regular      | 8%    | 70%     | 12%    | 7%      | 2%      | 1%
Casual       | 2%    | 10%     | 55%    | 15%     | 12%     | 6%
At-Risk      | 1%    | 5%      | 10%    | 30%     | 30%     | 24%
Dormant      | 0%    | 2%      | 3%     | 5%      | 60%     | 30%
```

---

## 10. Anti-Patterns

| Anti-Pattern | Better Alternative |
|---|---|
| Over-segmenting | Start with 4-6 segments, expand as needed |
| Small sample segments (<100 users) | Minimum 100-200 users per segment |
| Static segments | Recalculate daily or weekly |
| Demographic-only | Combine demographic with behavioral data |
| Vanity segments (no action plan) | Every segment must have a specific action plan |
| Ignoring segment transitions | Track how users move between segments over time |

---

## 11. Output Format

```
# Segmentation Strategy

## Segmentation Goals
- Primary goal: [What decisions will segmentation inform?]
- Key questions to answer: [...]

## Data Foundation
- Available data sources: [Product events, CRM, enrichment, billing]
- Data gaps: [What's missing?]

## Segment Definitions

### Segment 1: [Name]
- Criteria: [Specific, measurable rules]
- Expected size: [N users, X% of base]
- Actions: Onboarding / Messaging / Upgrade path / Support
- Success metric: [How you measure if segment is served well]

## Scoring Models
- Engagement score: [Components and weights]
- Expansion readiness score: [Components and weights]
- Churn risk score: [Components and weights]

## Personalization Playbook
| Touchpoint | Segment 1 | Segment 2 | Segment 3 |
|---|---|---|---|
| Onboarding | [...] | [...] | [...] |
| In-product messaging | [...] | [...] | [...] |
| Email campaigns | [...] | [...] | [...] |
| Upgrade prompts | [...] | [...] | [...] |

## Implementation Plan
- Phase 1: Basic segments (lifecycle + plan)
- Phase 2: Behavioral segments (engagement scoring)
- Phase 3: Advanced (ML clustering, predictive scoring)

## Measurement
- Track: segment distribution, transitions, per-segment KPIs
- Cadence: [Weekly / Monthly]
```

---

Related skills: `product-led-sales`, `plg-metrics`, `product-analytics`, `retention-analysis`
