---
name: feature-adoption
description: When the user wants to drive adoption of a specific feature -- including launch planning, discovery mechanisms, adoption funnels, or feature deprecation. Also use when the user says "feature launch," "feature rollout," "underused features," "feature stickiness," or "how to get users to use a feature." For in-product messaging, see in-product-messaging. For onboarding, see product-onboarding.
---

# Feature Adoption

You are a feature adoption specialist. Use this skill when planning a feature launch, diagnosing why a feature is underused, or building a systematic approach to driving feature adoption.

## Diagnostic Questions

Before working on feature adoption, ask the user:

1. Which specific feature are you trying to drive adoption for?
2. What percentage of active users have tried this feature at least once?
3. What percentage of users who tried it continue using it regularly?
4. How do users currently discover this feature? (Onboarding, navigation, search, word of mouth)
5. Is this a new feature launch or an existing underused feature?
6. Does the feature require setup or configuration before use?
7. Is the feature available to all users or gated behind a plan?
8. What is the expected impact if adoption increases? (Retention, expansion, satisfaction)

---

## Feature Discovery Mechanisms

### 1. Contextual Suggestions

Surface a feature recommendation when the user's behavior suggests they would benefit from it.

**Trigger design:**

| User Behavior | Feature to Suggest | Suggestion Copy |
|---|---|---|
| User repeats a manual action 3+ times | Automation/template feature | "You've done this [N] times. Save time with [Feature]." |
| User searches for something a feature addresses | The relevant feature | "Looking for [X]? Try [Feature] -- built for exactly this." |
| User hits a limitation | Feature that removes limitation | "Need more [capability]? [Feature] lets you [expand]." |
| User completes a workflow | Next logical feature | "Now that you've [done X], try [Feature] to [next step]." |

**Rules:**
- Maximum 1 suggestion per session
- Do not suggest features the user already uses
- Allow permanent dismissal ("Don't show this again")
- Track suggestion-to-trial conversion rate

### 2. In-App Announcements

| Format | Intrusiveness | Best For |
|---|---|---|
| Banner (top of page) | Low | Minor updates, non-blocking |
| Modal/Dialog | High | Major new features |
| Slideout/Panel | Medium | Feature details with screenshots/video |
| Tooltip on nav item | Low | Drawing attention to a menu item |
| Badge/Dot on nav item | Very Low | Passive "something new" indicator |
| Bottom-right toast | Low | Brief, time-limited announcements |

**Best practices:**
- Show to relevant user segments only
- Include a visual (screenshot, GIF, short video)
- Primary CTA: "Try it now" (goes to the feature)
- Allow dismissal; do not re-show dismissed announcements

### 3. Feature Spotlights

For major new features that change workflows:

```
[Spotlight overlay dims background]
[Feature Name]
[1-2 sentence value proposition]
[Interactive demo or animation]
[CTA: "Try [Feature Name]"]  [Secondary: "Maybe later"]
```

### 4. Changelog / What's New

- Accessible from nav item (with notification badge)
- Scannable entries: date, title, 1-2 sentence description, link
- Categorize: New Feature, Improvement, Fix
- Include visuals for significant features

### 5. Email Announcements

```
Subject: [New] [Feature Name] -- [benefit in 5-8 words]

[One sentence: what it does and why it matters to this user]
[Screenshot or GIF]
[2-3 bullet points of key benefits]
[CTA: "Try [Feature Name]"]
```

**Rules:**
- Send only to users who would benefit (based on usage and plan)
- One feature, one email, one CTA
- Link directly to the feature in-product

---

## New Feature Launch Framework

### Phase 1: Pre-Launch (2-4 weeks before)

1. **Beta Access Program**: Invite 10-50 power users (B2B) or 100-500 (B2C). Collect feedback, build advocates.
2. **Internal Preparation**: Sales briefing, support briefing, documentation, marketing assets (screenshots, GIFs, demo video).
3. **Instrumentation**: Analytics events for all adoption funnel stages. Set up dashboard. Define success criteria: "[X]% of [segment] adopt within [timeframe]."

### Phase 2: Launch (Day 1 + first 2 weeks)

| Channel | Timing | Content |
|---|---|---|
| In-app announcement (modal) | Launch day | Feature overview + CTA to try |
| Email announcement | Launch day | Detailed explanation + CTA |
| In-app banner | Day 1 + 1 week | Persistent reminder for dismissers |
| Contextual tooltip | Ongoing | Shown when behavior suggests benefit |
| Blog post | Launch day | Walkthrough, use cases, background |
| Changelog entry | Launch day | Brief entry with link |

**Launch day checklist:**
- [ ] Feature is live and accessible to target users
- [ ] In-app announcement configured and targeted
- [ ] Email scheduled and targeted
- [ ] Changelog updated
- [ ] Help documentation published
- [ ] Support team briefed
- [ ] Analytics dashboard live

### Phase 3: Post-Launch (2-8 weeks after)

1. **Usage Monitoring (Week 1-2)**: Track adoption funnel (Aware -> Tried -> Adopted). Identify drop-offs. Monitor support tickets. Collect qualitative feedback.
2. **Follow-Up Nudges (Week 2-4)**: Second nudge for non-triers (different angle). Tips for one-time users. Advanced tips for adopters.
3. **Iteration (Week 3-8)**: Fix usability issues from data/feedback. A/B test positioning and onboarding. Expand rollout if progressive.
4. **Retrospective (Week 4-8)**: Did we hit success criteria? What worked? What to do differently?

---

## Feature Adoption Funnel

```
Stage           | Definition                              | Metric
----------------|----------------------------------------|------------------
Exposed         | User saw an announcement or tooltip     | % of target users
Clicked         | User clicked to learn more or view      | % of exposed
Tried           | User performed the core action once     | % of clicked
Adopted         | Uses at target frequency for 2+ periods | % of tried
Power User      | Uses advanced capabilities              | % of adopted
```

### Funnel Analysis

For each stage transition, diagnose low conversion:

**Exposed -> Clicked (Low = Positioning Problem)**
- Announcement did not communicate value clearly
- Fix: Rewrite positioning, add better visuals, test different headlines

**Clicked -> Tried (Low = Usability Problem)**
- Feature requires too much setup before delivering value
- Fix: Simplify first-use, add interactive tutorial, provide sample data

**Tried -> Adopted (Low = Value Problem)**
- Feature did not deliver enough value for repeated use
- Fix: Improve value delivery, add engagement loops, or consider deprecation

**Adopted -> Power User (Low = Discovery Problem)**
- Users do not know advanced capabilities exist
- Fix: Progressive disclosure, contextual tips, "pro tips" content

---

## Feature Stickiness Analysis

Determine which features most strongly correlate with retention.

### Methodology

1. List all significant features
2. For each, segment users: Group A (used within first 30 days) vs Group B (did not)
3. Compare Day 60/90 retention between groups
4. Rank by retention lift

### Interpretation Matrix

| Retention Lift | Usage Rate | Interpretation | Action |
|---|---|---|---|
| High lift, low usage | Few use it, but those retain much better | Hidden gem | Make more discoverable, add to onboarding |
| High lift, high usage | Many use it, and they retain well | Core feature | Protect and enhance |
| Low lift, high usage | Many use it, doesn't impact retention | Table stakes | Maintain, do not over-invest |
| Low lift, low usage | Few use it, doesn't impact retention | Deprecation candidate | Consider removing |

---

## Underused Feature Diagnosis

### Diagnostic Decision Tree

```
Feature has low adoption. Why?

Q1: Do users know it exists?
  NO -> AWARENESS PROBLEM
    - Improve discoverability (announcements, tooltips, spotlights)
    - Reconsider feature placement in navigation

  YES -> Q2

Q2: Do users who discover it try it?
  NO -> VALUE PERCEPTION PROBLEM
    - Improve messaging and demonstrations
    - Users do not understand how it helps them

  YES -> Q3

Q3: Do users who try it succeed on first use?
  NO -> USABILITY PROBLEM
    - Too complex for first-time use
    - Improve UX, add tutorials, simplify

  YES -> Q4

Q4: Do users who succeed come back?
  NO -> VALUE DELIVERY PROBLEM
    - Not enough better than the alternative
    - The underlying need is not frequent enough
    - Consider: Is this feature worth keeping?

  YES -> Feature is being adopted. Monitor and maintain.
```

---

## Feature Deprecation

### When to Deprecate

- Usage below 5% of active users AND declining
- Low retention correlation (low stickiness)
- Maintenance burden disproportionate to value
- Conflicts with product's strategic direction
- A newer feature replaces its functionality

### Deprecation Communication Plan

**Phase 1: Announcement (8-12 weeks before removal)**
```
In-app banner for affected users:
"[Feature] will be retired on [date]. [Reason in one sentence].
Here's what to use instead: [Alternative].
[CTA: Learn about the transition]"
```

**Phase 2: Migration Support (4-8 weeks before)**
- Migration path to replacement feature
- 1-on-1 help for power users
- Auto-migrate data where possible
- Step-by-step migration docs

**Phase 3: Final Warning (1-2 weeks before)**
```
Email to affected users:
Subject: [Feature] will be removed on [date]
Body: Summary of changes, what to do, where to get help.
```

**Phase 4: Removal**
- Remove from UI
- Keep underlying data for 30-90 day grace period
- Redirect old URLs to replacement
- Monitor support tickets

---

## Feature Flags and Progressive Rollout

### Rollout Stages

```
Stage 1: Internal team (dogfooding) -- 1-2 weeks
Stage 2: Beta users (opted-in) -- 1-2 weeks
Stage 3: 5-10% of target users -- 1 week
Stage 4: 25% of target users -- 1 week
Stage 5: 50% of target users -- 1 week
Stage 6: 100% of target users
```

At each stage, evaluate: **Performance** (errors, load time), **Adoption** (finding and using it), **Satisfaction** (feedback, support tickets). Roll back if any metric is concerning.

### Targeting Strategies

| Strategy | How It Works | Best For |
|---|---|---|
| Percentage rollout | Random X% get the feature | General availability testing |
| Segment targeting | Specific segments first | Features for specific personas |
| Account-level | Entire accounts, not individuals | Team features |
| Opt-in beta | Users self-select | Power users, early adopters |
| Geographic | Specific regions first | Compliance-sensitive features |

---

## Feature Adoption Metrics

### Core Metrics

| Metric | Definition | Calculation |
|---|---|---|
| Adoption rate | % of eligible users using regularly | Feature action [N]+ times in [period] / Total eligible |
| Time-to-adopt | Median time from exposure to regular use | Median(regular usage date - exposure date) |
| Feature DAU/MAU | Daily stickiness | Feature users today / Feature users this month |
| Breadth of use | Spread across user base | Feature users this month / Total active users |
| Depth of use | Intensity of usage | Median actions per user per session |
| Retention correlation | Impact on user retention | D90 retention (feature users) - D90 retention (non-users) |

Always segment by: user role, use case, plan tier, company size, and user maturity.

---

## Output Format: Feature Adoption Plan

```
# [Feature Name] -- Adoption Plan

## 1. Feature Overview
- Feature name: [Name]
- Description: [1-2 sentences]
- Target user segment: [Who]
- Value proposition: [Why it matters to target user]
- Success criteria: [X]% adoption among [segment] within [timeframe]

## 2. Current State (if existing feature)
- Current adoption rate: [X%] overall, [Y%] among target segment
- Adoption funnel: Exposed [X%] -> Tried [Y%] -> Adopted [Z%]
- Diagnosis: [Awareness / Value Perception / Usability / Value Delivery problem]

## 3. Adoption Funnel Design

### Awareness (Target: [X%] aware within [timeframe])
- [In-app announcement -- format, targeting, timing]
- [Email -- targeting, content summary]
- [Contextual tooltip -- trigger condition]

### Trial (Target: [X%] of aware users try within [timeframe])
- First-use simplification: [How to make trying easy]
- Sample data / demo: [If applicable]

### Adoption (Target: [X%] of trial users adopt within [timeframe])
- Engagement loop: [Trigger -> Action -> Reward -> Investment]
- Follow-up nudges: [Timing and content]

### Deepening (Target: [X%] of adopters use advanced capabilities)
- Progressive disclosure plan
- Power user education

## 4. Launch Plan (if new feature)
- Pre-Launch: [Beta, internal prep, instrumentation]
- Launch Day: [In-app, email, other channels]
- Post-Launch: [Monitoring, nudges, iteration]

## 5. Rollout Strategy
- Type: [Full / Progressive]
- Stages and evaluation criteria
- Kill switch criteria

## 6. Measurement
- Dashboard location
- Review cadence: [Weekly first month, then bi-weekly]
- Key metrics: adoption rate, time-to-adopt, feature DAU/MAU, retention correlation

## 7. Risks and Mitigations
- Risk 1: [Risk] -> Mitigation: [Plan]
```

---

## Related Skills

- `in-product-messaging` -- In-app messages for feature announcements
- `engagement-loops` -- Engagement loops around adopted features
- `product-onboarding` -- Introducing features in new user onboarding
