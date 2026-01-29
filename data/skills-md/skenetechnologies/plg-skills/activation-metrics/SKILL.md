---
name: activation-metrics
description: When the user wants to define, measure, or optimize user activation -- including identifying the aha moment, measuring time-to-value, or building an activation funnel. Also use when the user says "activation rate," "aha moment," "setup moment," "habit moment," "time to value," or "how do I measure activation." For onboarding design, see product-onboarding. For retention, see retention-analysis.
---

# Activation Metrics

You are an activation metrics strategist. Use this skill when helping teams define, measure, and optimize user activation. Activation is the single most impactful lever in PLG growth -- [Shaun Clowes](https://www.intercom.com/blog/podcasts/metromiles-shaun-clowes-on-activating-and-retaining-users/) (former VP Growth at Atlassian) famously stated: **"Spend 80% of your resources on activation."** A user who never activates never retains, never expands, and never refers.

This skill is built on [Shaun Clowes' **Three Moments of Activation** framework](https://www.intercom.com/blog/podcasts/metromiles-shaun-clowes-on-activating-and-retaining-users/) and covers how to identify, define, measure, and improve each moment.

---

## The Three Moments of Activation

Activation is not a single event. It is a progression through three distinct moments, each of which must be achieved before the next becomes possible.

```
Signup ──► [Setup Moment] ──► [Aha Moment] ──► [Habit Moment] ──► Retained User
              │                    │                   │
              ▼                    ▼                   ▼
         "I can use this"    "This is valuable"   "This is part of
                                                   my workflow"
```

### Moment 1: Setup Moment

The Setup Moment is the set of actions a user must complete before they can experience the product's core value. These are prerequisite steps -- necessary but not sufficient for activation.

**Common Setup Actions by Product Type:**

| Product Type | Typical Setup Actions |
|---|---|
| B2B SaaS | Create workspace, invite team members, connect integrations |
| Dev Tools | Install CLI/SDK, configure project, connect repository |
| Analytics | Add tracking snippet, verify data flowing, import historical data |
| Collaboration | Create first project/channel, invite collaborators |
| Productivity | Import data, configure preferences, connect calendar |

**Diagnostic Questions for Setup Moment:**
1. What is the absolute minimum a user must do before they can experience core value?
2. Which setup steps can be deferred to after the Aha Moment?
3. Which steps can be automated or pre-filled?
4. What is the current completion rate for each setup step?
5. Where is the biggest drop-off in the setup flow?

**Setup Moment Optimization Principles:**
- Remove every field and step that is not strictly required for first value
- Auto-detect and pre-fill wherever possible (e.g., company name from email domain)
- Allow skipping with sensible defaults
- Show progress indicators so users know how close they are
- Provide sample/demo data so users can skip data import initially

### Moment 2: Aha Moment

The Aha Moment is the first time a user experiences the product's core value proposition. It is the emotional "this is what I came for" moment. It is NOT the same as understanding what the product does -- it is *experiencing* the value firsthand.

**Examples of Aha Moments:**

| Product | Aha Moment |
|---|---|
| Slack | Receiving your first message from a teammate |
| Dropbox | Seeing a file sync across devices for the first time |
| Figma | Getting real-time feedback from a collaborator on a design |
| Amplitude | Seeing your first retention curve with real user data |
| Notion | Creating a page that replaces a clunky spreadsheet/doc |

#### How to Find Your Aha Moment: Correlation Analysis

Your Aha Moment is not something you decide in a brainstorm. You discover it through data analysis. Here is the methodology:

**Step 1: Hypothesize candidate Aha Moment actions**
List 5-15 early actions users can take within their first 7 days. Examples:
- Created first [object]
- Invited first team member
- Connected first integration
- Completed first [workflow]
- Shared first [output]
- Viewed first [report/insight]

**Step 2: Segment users by whether they performed each action**
For each candidate action, split users into two groups:
- Group A: Users who performed the action within their first [7/14/30] days
- Group B: Users who did NOT perform the action in that window

**Step 3: Compare long-term retention curves**
For each candidate action, compare the Day 30 / Day 60 / Day 90 retention rate of Group A vs Group B.

**Step 4: Rank by retention lift**
The action with the largest gap in long-term retention between the two groups is your strongest Aha Moment candidate.

```
Candidate Action              | D30 Retention (Did) | D30 Retention (Didn't) | Lift
------------------------------|---------------------|------------------------|------
Invited 1+ team member        | 72%                 | 23%                    | +49pp
Created 3+ projects           | 68%                 | 31%                    | +37pp
Connected integration         | 65%                 | 35%                    | +30pp
Completed profile             | 45%                 | 38%                    | +7pp
```

**Step 5: Validate causality (not just correlation)**
- Run an experiment: actively push users toward the candidate action and measure if retention improves
- Control for selection bias: users who invite teammates may be more committed regardless
- Look for dose-response: does performing the action MORE strongly correlate with even better retention?

**Step 6: Define the Aha Moment metric**
Format: `[X]% of new users [perform specific action] within [timeframe] of signing up`

Example: "65% of new users create and share at least one report within 7 days of signing up"

### Moment 3: Habit Moment

The Habit Moment is when a user establishes the core behavior at the product's natural frequency. The user has moved from "I tried it and liked it" to "I use this regularly as part of my workflow."

**How to Define the Habit Moment:**

1. **Determine your product's natural frequency:**
   - Daily-use products (Slack, email, dev tools): habit = daily usage
   - Weekly-use products (analytics, project management): habit = weekly usage
   - Monthly-use products (billing, reporting): habit = monthly usage

2. **Frequency analysis methodology:**
   - Take your retained users (users active at Day 90+)
   - Plot their usage frequency distribution (sessions per week/month)
   - Identify the natural clustering -- this is your target frequency
   - The Habit Moment occurs when a new user matches this frequency for 2+ consecutive periods

3. **Habit Moment definition format:**
   `User performs [core action] at least [N] times per [period] for [M] consecutive [periods]`

   Examples:
   - "User sends messages at least 3 days per week for 2 consecutive weeks"
   - "User runs at least 2 analyses per week for 3 consecutive weeks"
   - "User logs in at least 3 times per month for 2 consecutive months"

---

## Activation Funnel Design

Map the three moments as measurable funnel steps. Each step should have a clear, binary definition.

### Activation Funnel Template

```
Step 0: Signed Up
  ↓  [Conversion Rate: ___%]
Step 1: Setup Complete
  Definition: [User has completed: ____________]
  Target timeframe: Within [___] of signup
  ↓  [Conversion Rate: ___%]
Step 2: Aha Moment Reached
  Definition: [User has performed: ____________]
  Target timeframe: Within [___] of signup
  ↓  [Conversion Rate: ___%]
Step 3: Habit Established
  Definition: [User performs _____ at least ___ times per _____ for ___ consecutive _____]
  Target timeframe: Within [___] of signup
  ↓
Activated User ✓
```

### Measuring the Funnel

For each step, track:
- **Conversion rate**: % of users reaching this step
- **Median time**: How long it takes the median user to reach this step
- **Drop-off reasons**: Why users fail to advance (qualitative + quantitative)
- **Segment breakdown**: Conversion rates by acquisition channel, user type, plan tier

---

## Time-to-Value (TTV) Optimization

Time-to-value is the elapsed time from signup to the user's first experience of core value (the Aha Moment). Shorter TTV correlates directly with higher activation and retention.

### How to Measure TTV

```
TTV = Timestamp(Aha Moment action) - Timestamp(Signup)
```

Track:
- **Median TTV**: The typical user's time to value
- **P90 TTV**: The slowest 10% of users -- these are at high risk of churning
- **TTV by segment**: Compare across user types, acquisition channels, and plan tiers

### TTV Reduction Strategies

1. **Eliminate unnecessary setup steps** -- Move non-essential configuration to after the Aha Moment
2. **Pre-populate with sample data** -- Let users experience value before importing their own data
3. **Auto-detect context** -- Use email domain, browser locale, referral source to skip questions
4. **Offer templates** -- Pre-built configurations for common use cases
5. **Guided quick-start** -- A focused 3-5 minute path to first value
6. **Defer account verification** -- Let users into the product before verifying email
7. **Smart defaults** -- Choose the most common configuration as default for every setting
8. **Parallel setup** -- Let users start using the product while background tasks complete (data import, etc.)

---

## Activation Rate Benchmarks

Use these as rough reference points, not hard targets. Your own historical trend and improvement rate matter more than absolute benchmarks.

| Product Category | Signup → Setup | Setup → Aha | Aha → Habit | Overall Activation |
|---|---|---|---|---|
| B2B SaaS (horizontal) | 60-75% | 40-55% | 30-50% | 15-25% |
| B2B SaaS (vertical) | 65-80% | 50-65% | 35-55% | 20-30% |
| Dev Tools | 50-65% | 35-50% | 25-40% | 10-18% |
| Collaboration Tools | 55-70% | 45-60% | 30-45% | 15-22% |
| Productivity (individual) | 70-85% | 50-65% | 20-35% | 12-20% |
| Analytics / Data Tools | 45-60% | 35-50% | 30-45% | 8-15% |

**Note:** These ranges represent median performers. Top-quartile PLG companies achieve 1.5-2x these rates.

---

## Activation Metric Definition Template

Use this template to create a precise, measurable activation metric definition.

```
ACTIVATION METRIC DEFINITION
=============================

Product: [Product Name]
Date Defined: [Date]
Owner: [Team/Person]

SETUP MOMENT
  Definition: User has completed ALL of the following:
    1. [Action 1, e.g., "Created workspace"]
    2. [Action 2, e.g., "Invited at least 1 team member"]
    3. [Action 3, e.g., "Connected at least 1 data source"]
  Target: [X]% of signups within [timeframe]
  Current: [Y]% (as of [date])

AHA MOMENT
  Definition: User has [specific action with quantitative threshold]
  Example: "Created and viewed at least 1 dashboard with live data"
  Target: [X]% of signups within [timeframe]
  Current: [Y]% (as of [date])
  Evidence: [Link to correlation analysis showing this action
             predicts D30+ retention with lift of +[N]pp]

HABIT MOMENT
  Definition: User [core action] at least [N] times per [period]
              for [M] consecutive [periods]
  Example: "Logs in and views dashboards at least 3x/week for 2 weeks"
  Target: [X]% of signups within [timeframe]
  Current: [Y]% (as of [date])

COMPOSITE ACTIVATION RATE
  Definition: % of signups reaching Habit Moment within [timeframe]
  Target: [X]%
  Current: [Y]%
```

---

## Cohort Analysis for Activation

Comparing activated vs non-activated user retention curves is the most powerful way to demonstrate the value of activation investments to stakeholders.

### How to Build the Analysis

1. **Define your activation criteria** (use the Aha Moment or Habit Moment definition)
2. **Split each signup cohort** into Activated and Non-Activated groups
3. **Plot retention curves** for both groups on the same chart
4. **Calculate the retention gap** at Day 30, 60, 90, 180

### Expected Pattern

```
Retention
100% |*
     | * *
     |  *   *  ← Activated users (flattening curve)
     |   *     * * * * * *
     |    *
     |     *
     |      *   ← Non-activated users (declining to zero)
     |        *
     |          *  *
  0% |________________*___*___
     D1  D7  D14  D30  D60  D90
```

### How to Use This Analysis

- **Justify investment**: "Activated users retain at 55% at D90 vs 8% for non-activated -- a 7x difference"
- **Size the opportunity**: "If we improve activation rate by 10pp, that translates to [X] additional retained users per month, worth $[Y] ARR"
- **Prioritize initiatives**: Compare the retention lift from different activation criteria to find the highest-impact actions to drive

---

## Shaun Clowes Principle: "Spend 80% on Activation"

The rationale: activation is the **highest-leverage** point in the user lifecycle.

- Users who don't activate will never retain, expand, or refer -- they are permanently lost
- Activation improvements compound: every additional activated user flows through to retention, revenue, and referral
- Acquisition without activation is waste -- you are filling a leaky bucket
- Retention improvements only apply to users who already activated
- Monetization improvements only apply to users who already retained

**Implication for resource allocation:**
- Prioritize activation over acquisition when activation rate is below benchmarks
- Prioritize activation over retention when activation-to-retention correlation is strong
- Only shift focus to later stages when activation rate is at or above top-quartile benchmarks

---

## Diagnostic Questions to Identify Activation Blockers

Use these questions in a structured diagnostic session to identify what is preventing users from activating.

### Setup Moment Blockers
1. What percentage of signups complete each setup step?
2. Where is the largest single drop-off in the setup flow?
3. How long does the setup process take? What is the P90 time?
4. Are there setup steps that could be automated, deferred, or eliminated?
5. Do users understand WHY each setup step is necessary?
6. Is there a "blank slate" problem -- do users face empty states with no guidance?

### Aha Moment Blockers
7. Have you identified and validated your Aha Moment through data analysis?
8. What percentage of users who complete setup reach the Aha Moment?
9. What is the median time from setup completion to Aha Moment?
10. Are there users who complete setup but never take the key Aha Moment action? Why?
11. Is the Aha Moment achievable solo, or does it require others (team members, customers, etc.)?
12. Can you create a "synthetic" Aha Moment using sample data or simulations?

### Habit Moment Blockers
13. Do users who reach the Aha Moment return the next day/week?
14. What is the natural usage frequency for your retained users?
15. What triggers bring users back? Are they internal (need) or external (notification)?
16. Is there a competing workflow or tool that users default back to?
17. Does the product integrate into existing workflows (calendar, Slack, email) or require a separate visit?

---

## Codebase Audit (Optional)

If you have access to the user's codebase, analyze it before asking diagnostic questions. Use findings to pre-fill answers and focus recommendations on what actually exists.

1. **Find activation-related events**: Search for tracking calls with event names like `activated`, `onboarding_complete`, `first_action`, `aha_moment`, `setup_complete`
2. **Find setup flow**: Trace the post-signup flow -- what steps must a user complete before they can use the product?
3. **Check for activation flags**: Search for `is_activated`, `has_completed_setup`, `onboarding_status` in user models or state
4. **Find core value action**: Identify the product's main action -- the thing users came to do. Search for the primary create/submit/complete action
5. **Check for habit tracking**: Search for usage frequency tracking, session counts, DAU/WAU/MAU calculations
6. **Find onboarding completion**: Search for checklist completion, setup wizard completion, required-steps tracking
7. **Check time-to-value tracking**: Search for timestamp differences between signup and first key action
8. **Find cohort/retention queries**: Search for retention calculations, cohort grouping, or analytics dashboard queries

Report: describe what activation tracking exists, what the likely aha moment action is based on the product, and what tracking gaps exist.

For a full growth audit, install [skene-skills](https://github.com/SkeneTechnologies/skene-skills) to generate a structured growth manifest you can reference alongside this skill.

---

## Output Format: Activation Metrics Definition Document

When helping a team define their activation metrics, produce a document with these sections:

```
# [Product Name] -- Activation Metrics Definition

## 1. Product Context
- Core value proposition: [What problem does this solve?]
- Target user: [Who is the primary user?]
- Natural usage frequency: [Daily / Weekly / Monthly]
- Current overall activation rate: [X%] (if known)

## 2. The Three Moments

### Setup Moment
- Required actions: [Numbered list]
- Current completion rate: [X%]
- Median completion time: [X hours/days]
- Key bottleneck: [Specific step with highest drop-off]
- Optimization priority: [Specific recommendation]

### Aha Moment
- Candidate actions analyzed: [List of 5-15 actions tested]
- Winning action: [The action with highest retention correlation]
- Retention lift: [+Xpp at Day 30/60/90]
- Metric definition: "[X]% of users [action] within [timeframe]"
- Current rate: [X%]

### Habit Moment
- Core repeated action: [What action defines regular use]
- Target frequency: [N times per period]
- Habit threshold: [N times per period for M consecutive periods]
- Current rate: [X%]
- Key driver of habit formation: [What makes users come back]

## 3. Activation Funnel
[Funnel diagram with conversion rates between each step]

## 4. Measurement Plan
- Data sources: [Product analytics tool, data warehouse, etc.]
- Tracking events required: [List of events to instrument]
- Dashboard: [Where the funnel will be monitored]
- Review cadence: [Weekly / Bi-weekly]

## 5. Improvement Roadmap
- Priority 1: [Highest-impact activation improvement]
- Priority 2: [Second-highest impact]
- Priority 3: [Third]
- Expected impact: [If activation improves by Xpp, Y additional retained users/month]

## 6. Activated vs Non-Activated Retention Comparison
[Cohort analysis showing retention curves for both groups]
```

---

## Related Skills

- `product-onboarding` -- Designing the first-run experience that drives users through setup to aha moment
- `plg-metrics` -- Broader PLG metrics framework that includes activation as a key stage
- `retention-analysis` -- Measuring and improving retention for activated users
