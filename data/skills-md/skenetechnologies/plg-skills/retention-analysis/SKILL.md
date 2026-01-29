---
name: retention-analysis
description: When the user wants to analyze, diagnose, or improve user retention -- including cohort analysis, churn prediction, engagement scoring, or resurrection campaigns. Also use when the user says "retention rate," "churn rate," "cohort analysis," "why are users churning," "NRR," or "how to reduce churn." For engagement loops, see engagement-loops. For activation, see activation-metrics.
---

# Retention Analysis

You are a retention analyst. Measure, diagnose, and improve user or customer retention.

## Diagnostic Questions

Before analyzing retention, ask the user:

1. What is your current D1 / D7 / D30 / D90 retention rate? (If unknown, that's step one)
2. Do you have cohort analysis set up?
3. What does your retention curve look like? (Flattening, declining to zero, or smile curve)
4. What is your product's natural usage frequency? (Daily / Weekly / Monthly)
5. What is your current churn rate (monthly or annual)?
6. Do you know why users churn? (Exit surveys, cancellation flow data, support tickets)
7. Have you identified behavioral differences between retained and churned users?
8. What is your current NRR (Net Revenue Retention)?
9. Do you have re-engagement campaigns (emails, push notifications) for inactive users?
10. Is your activation rate strong, or could poor activation be driving churn?

---

## Retention Curve Types

| Curve Shape | Meaning | Action |
|---|---|---|
| **Flattening** | Product-market fit; users who survive initial period stay long-term | Increase the terminal retention rate and move the flattening point earlier |
| **Declining** | No stabilization; product does not deliver recurring value | Urgent: understand WHY users leave (exit surveys, interviews) |
| **Smile** | Users return after initial decline (seasonal, re-engagement, product improvements) | Verify it is real (not measurement artifact); understand resurrection triggers |

---

## How to Build Retention Curves

### Step 1: Choose Your Retention Event

The retention event should be a meaningful action, not just a login.

| Product Type | Retention Event Candidates |
|---|---|
| Analytics platform | Viewed a report or dashboard |
| Collaboration tool | Sent a message or comment |
| Dev tool | Made a commit, deployed, or ran a build |
| Project management | Updated a task or created a task |
| CRM | Logged an activity or updated a record |

**Rule:** The retention event should be the action most closely tied to the product's core value. "Logged in" is almost never the right retention event.

### Step 2: Choose Your Retention Metric Type

| Metric Type | Definition | Best For |
|---|---|---|
| N-day retention | % of users active on exactly day N | Daily-use products (D1, D7, D30) |
| Bounded retention | % of users active within a specific window (e.g., Week 2 = days 8-14) | Weekly-use products |
| Unbounded retention | % of users active on day N OR any day after | Products where any return counts |

**Recommendation by product frequency:**

| Product Frequency | Recommended Metric | Key Timepoints |
|---|---|---|
| Daily-use | N-day retention | D1, D7, D14, D30, D60, D90 |
| Weekly-use | Bounded weekly retention | W1, W2, W4, W8, W12 |
| Monthly-use | Bounded monthly retention | M1, M2, M3, M6, M12 |

### Step 3: Build the Cohort Table

A cohort table groups users by their signup date and tracks their retention over time.

```
                    Week 0  Week 1  Week 2  Week 3  Week 4  Week 5
Jan 1-7 cohort      100%    52%     38%     33%     30%     29%
Jan 8-14 cohort     100%    55%     40%     35%     32%     --
Jan 15-21 cohort    100%    48%     36%     31%     --       --
Jan 22-28 cohort    100%    50%     37%     --       --       --
Feb 1-7 cohort      100%    53%     --       --       --       --
```

### Step 4: Plot and Analyze

- Plot each cohort's retention curve on the same chart
- Look for: Is the curve flattening? At what level? At what timepoint?
- Compare cohorts: Are newer cohorts retaining better than older ones? (This indicates product improvements are working.)

---

## Cohort Analysis Types

| Cohort Type | Grouping | Use When |
|---|---|---|
| **Time-Based** | By signup date (week, month, quarter) | Understanding if retention improves over time or after changes |
| **Behavioral** | By actions taken (invited teammate, connected integration, used Feature X, reached Aha Moment) | Identifying which behaviors predict retention |
| **Acquisition Source** | By channel (organic, paid, referral, direct) | Evaluating acquisition channel quality |
| **Plan/Segment** | By plan tier, company size, industry | Understanding which segments retain best |

---

## Churn Prediction Signals

Identifying users at risk of churning before they leave allows proactive intervention.

### Usage-Based Signals

| Signal | Definition | Risk Level |
|---|---|---|
| Declining login frequency | Sessions per week decreased 50%+ vs prior 4-week average | Medium |
| Declining core action frequency | Core action frequency dropped 40%+ vs prior period | High |
| Feature disengagement | Stopped using a feature they previously used regularly | Medium |
| Decreasing session duration | Sessions are significantly shorter than historical average | Low-Medium |
| No activity in [expected period] | No login for 2x their normal inter-session interval | High |

### Account-Based Signals

| Signal | Definition | Risk Level |
|---|---|---|
| Billing issues | Failed payment, expired card, downgrade request | High |
| Reduced seats | Team removed users from the workspace | High |
| Admin departure | The primary admin/champion left the company (detected via email bounce or role change) | Very High |
| Support escalation | Multiple support tickets, especially about the same issue | Medium |
| Data export | User exported their data | High |
| Competitor mentions | User mentions a competitor in support tickets or surveys | Medium |

### Building an Engagement Score

A composite engagement score combines multiple signals into a single health metric for each user or account.

**Step 1: Identify 4-6 engagement signals**
- Login frequency (sessions per week)
- Core action frequency (core actions per week)
- Feature breadth (number of features used per week)
- Collaboration intensity (team interactions per week, if applicable)
- Recency (days since last activity)

**Step 2: Normalize each signal**
Transform each signal to a 0-100 scale based on your product's distribution.

**Step 3: Weight and combine**
```
Engagement Score = (w1 * Login Frequency Score)
                 + (w2 * Core Action Score)
                 + (w3 * Feature Breadth Score)
                 + (w4 * Collaboration Score)
                 + (w5 * Recency Score)

Where w1 + w2 + w3 + w4 + w5 = 1.0
```

**Step 4: Define risk tiers**
- Score 80-100: Healthy (green)
- Score 50-79: Monitor (yellow)
- Score 20-49: At risk (orange)
- Score 0-19: Critical (red)

**Step 5: Validate against actual churn**
Back-test your scoring model against historical churn data. The score should predict churn: users who churned should have had lower scores in the weeks before churning.

---

## Retention Benchmarks by Product Category

Use these as reference points, not targets. Your own trend matters more than absolute numbers.

### B2B SaaS (Horizontal)

| Timepoint | Below Average | Average | Good | Excellent |
|---|---|---|---|---|
| Week 1 | <40% | 40-55% | 55-65% | >65% |
| Month 1 | <25% | 25-40% | 40-50% | >50% |
| Month 3 | <15% | 15-25% | 25-35% | >35% |
| Month 12 | <5% | 5-15% | 15-25% | >25% |

### B2B SaaS (Vertical / Niche)

| Timepoint | Below Average | Average | Good | Excellent |
|---|---|---|---|---|
| Week 1 | <50% | 50-60% | 60-70% | >70% |
| Month 1 | <35% | 35-50% | 50-60% | >60% |
| Month 3 | <25% | 25-40% | 40-50% | >50% |
| Month 12 | <15% | 15-25% | 25-40% | >40% |

### Developer Tools

| Timepoint | Below Average | Average | Good | Excellent |
|---|---|---|---|---|
| Week 1 | <30% | 30-45% | 45-55% | >55% |
| Month 1 | <20% | 20-35% | 35-45% | >45% |
| Month 3 | <10% | 10-20% | 20-30% | >30% |

### Collaboration Tools

| Timepoint | Below Average | Average | Good | Excellent |
|---|---|---|---|---|
| Week 1 | <40% | 40-55% | 55-65% | >65% |
| Month 1 | <25% | 25-40% | 40-50% | >50% |
| Month 3 | <15% | 15-30% | 30-40% | >40% |

---

## Retention Improvement Framework

Prioritize retention improvement efforts in this order, from highest leverage to lowest.

### 1. Activation Improvements (Highest Leverage)

Per [Shaun Clowes](https://www.intercom.com/blog/podcasts/metromiles-shaun-clowes-on-activating-and-retaining-users/): activation is the single biggest lever for retention. Users who never activate will never retain. Before investing in retention-specific features, ensure your activation rate is strong.

**Actions:**
- Identify and validate your Aha Moment (see `activation-metrics` skill)
- Reduce time-to-value for new users
- Eliminate setup friction
- Ensure new users reach the Aha Moment within their first session

**Expected impact:** Improving activation rate by 10 percentage points typically improves Month 3 retention by 5-15 percentage points.

### 2. Engagement Loop Optimization

Build and strengthen the mechanisms that bring users back at the right frequency.

**Actions:**
- Audit existing triggers (notifications, emails, in-product cues)
- Design engagement loops matched to natural product frequency (see `engagement-loops` skill)
- Implement or improve digest emails with actionable content
- Add environment loops (integrations into existing workflow tools)

**Expected impact:** Well-designed engagement loops can improve Week 4+ retention by 10-20%.

### 3. Feature Stickiness Analysis

Identify which features most strongly correlate with retention, then drive adoption of those features.

**Methodology:**
1. List all significant features in your product
2. For each feature, segment users into "used this feature" vs "did not use this feature"
3. Compare retention rates between the two groups at Day 30, 60, 90
4. Rank features by retention lift

```
Feature                    | D30 Retention (Used) | D30 Retention (Didn't) | Lift
---------------------------|---------------------|------------------------|------
Team collaboration         | 68%                 | 25%                    | +43pp
Custom dashboards          | 62%                 | 30%                    | +32pp
API integrations           | 58%                 | 33%                    | +25pp
Export/download             | 35%                 | 34%                    | +1pp
```

**Actions based on results:**
- Features with high lift: Drive adoption through onboarding, tooltips, and nudges
- Features with low lift: Deprioritize investment
- Features used by retained users but not by churned users: These are your "sticky features" -- make them more discoverable

### 4. Resurrection Campaigns for Dormant Users

Bring back users who have stopped using the product but have not formally cancelled.

**Dormant user definition:** No activity for 2x the user's typical inter-session interval, or no activity for 14+ days for daily-use products, 30+ days for weekly-use products.

**Resurrection strategies:**

#### Email Re-Engagement Sequence

```
Email 1 (Day 7 of inactivity): "We noticed you haven't been in [Product] lately"
- Tone: Helpful, not guilty
- Content: Quick reminder of what they can do
- CTA: Direct link to their most-used feature

Email 2 (Day 14): "Here's what you've missed"
- Tone: Informational
- Content: New features, team activity, or data updates since they left
- CTA: "See what's new →"

Email 3 (Day 21): "Need help?"
- Tone: Supportive
- Content: Offer a 1-on-1 session, video walkthrough, or FAQ
- CTA: "Schedule a quick call" or "Watch a 2-min video"

Email 4 (Day 30): "Your account is still here"
- Tone: Final, no pressure
- Content: Summary of their data/workspace + what they'd lose if they leave
- CTA: "Come back" or "Tell us why you left [survey link]"
```

#### "What You Missed" Digests

For products with team activity or updating data:
- Show a summary of team actions, new data, or product changes that occurred while the user was away
- Create FOMO by showing what colleagues accomplished
- Link directly to the most relevant content

#### Win-Back Offers

For paid products with churned customers:
- Offer a discount on re-subscription (20-50% for 1-3 months)
- Offer an extended free trial to try again
- Offer a free upgrade to a higher tier for a limited time
- Highlight what has improved since they left

---

## Churn Analysis

### Exit Surveys

When a user cancels or downgrades, capture their reason with a structured exit survey.

**Survey design:**

```
"We're sorry to see you go. What's the primary reason you're leaving?"

○ Too expensive / not worth the price
○ Missing features I need
○ Too complicated / hard to use
○ Switched to a different tool
○ My needs changed / no longer need this
○ Poor customer support experience
○ Technical issues / bugs
○ Other: [free text]

[Optional follow-up]: "Is there anything we could have done differently?"
[Free text field]

[Optional]: "Would you consider coming back if we [fixed issue]?"
○ Yes  ○ Maybe  ○ No
```

### Cancellation Flow Optimization

Before completing a cancellation, offer alternatives:

```
Step 1: "Are you sure?" + Reason selection (exit survey above)

Step 2: Based on selected reason, offer targeted retention:
- "Too expensive" → Offer downgrade to a cheaper plan or pause subscription
- "Missing features" → Show roadmap or workaround + offer to log a feature request
- "Too complicated" → Offer a 1-on-1 walkthrough with a CS rep
- "Switching to competitor" → Offer a comparison and any migration assistance
- "Needs changed" → Offer pause instead of cancel

Step 3: If they proceed:
- Confirm what they will lose (data retention policy, team impact)
- Offer a "pause" option (keep account, stop billing for 1-3 months)
- Confirm cancellation with grace period information

Step 4: Post-cancellation:
- Send a confirmation email
- Keep data for 30-90 days (allow easy reactivation)
- Schedule a win-back email sequence starting 30 days after cancellation
```

---

## Dollar Retention (Net Revenue Retention / NRR)

### NRR Calculation

```
NRR = (Starting MRR + Expansion - Contraction - Churn) / Starting MRR * 100%

Where:
- Starting MRR: Revenue from existing customers at period start
- Expansion: Upgrades, additional seats, upsells from existing customers
- Contraction: Downgrades from existing customers
- Churn: Revenue from customers who cancelled
```

### NRR Benchmarks

| Tier | NRR | What It Means |
|---|---|---|
| Elite | >130% | Strong expansion; revenue grows even without new customers |
| Excellent | 115-130% | Healthy expansion offsetting churn |
| Good | 100-115% | Slight expansion, low churn |
| Concerning | 90-100% | Churn slightly exceeds expansion |
| Problem | <90% | Revenue is shrinking from existing customers |

---

## Output Format: Retention Diagnostic Report

When performing a retention analysis, produce a document with these sections:

```
# [Product Name] -- Retention Diagnostic Report

## 1. Executive Summary
- Current retention health: [Healthy / At Risk / Critical]
- Key finding: [One sentence summary of the biggest retention issue]
- Top recommendation: [One sentence summary of the highest-impact action]

## 2. Retention Metrics Snapshot

| Metric | Current | Benchmark | Status |
|---|---|---|---|
| D1/W1 retention | [X%] | [Y%] | [Above/Below] |
| D7/W2 retention | [X%] | [Y%] | [Above/Below] |
| D30/M1 retention | [X%] | [Y%] | [Above/Below] |
| D90/M3 retention | [X%] | [Y%] | [Above/Below] |
| DAU/MAU | [X%] | [Y%] | [Above/Below] |
| NRR (if B2B) | [X%] | [Y%] | [Above/Below] |

## 3. Retention Curve Analysis
- Curve shape: [Flattening / Declining / Smile]
- Terminal retention rate: [X%] (the level at which the curve flattens)
- Flattening point: [Day/Week X] (when the curve stabilizes)
- Cohort trend: [Improving / Stable / Declining] over the last [N] months

## 4. Cohort Analysis
[Cohort table with 6-12 cohorts]
- Key finding from time-based cohorts: [What changed and when]
- Key finding from behavioral cohorts: [Which behaviors predict retention]
- Key finding from acquisition cohorts: [Which channels produce retaining users]

## 5. Churn Diagnosis
- Primary churn reason: [Based on exit surveys and data analysis]
- Secondary churn reason: [Second most common]
- Churn timing: [When do most users churn? D7? D30? Month 3?]
- At-risk user profile: [Description of users most likely to churn]

## 6. Feature Stickiness Analysis
[Table of features ranked by retention lift]
- Stickiest feature: [Feature name] -- users of this feature retain [X]pp better
- Recommendation: [How to drive adoption of sticky features]

## 7. Engagement Score Distribution
- Score 80-100 (Healthy): [X%] of users
- Score 50-79 (Monitor): [X%] of users
- Score 20-49 (At Risk): [X%] of users
- Score 0-19 (Critical): [X%] of users

## 8. Improvement Roadmap (Prioritized)

### Priority 1: [Highest-impact initiative]
- Description: [What to do]
- Expected impact: [Estimated retention improvement]
- Effort: [Low / Medium / High]
- Timeline: [Weeks/months]

### Priority 2: [Second-highest impact]
[Same structure]

### Priority 3: [Third]
[Same structure]

### Priority 4: [Fourth]
[Same structure]

## 9. Resurrection Strategy
- Dormant user count: [N users inactive for 14+ days]
- Re-engagement sequence: [Summary of planned email/notification sequence]
- Win-back offer: [If applicable]

## 10. Measurement Plan
- Dashboard: [Where retention will be monitored]
- Review cadence: [Weekly / Bi-weekly / Monthly]
- Alert thresholds: [When to escalate]
```

---

## Related Skills

- `engagement-loops` -- Designing the mechanisms that drive repeated usage and improve retention
- `activation-metrics` -- Activation is the highest-leverage retention improvement
- `plg-metrics` -- Broader PLG metrics framework that includes retention
- `feature-adoption` -- Driving adoption of features that correlate with retention
