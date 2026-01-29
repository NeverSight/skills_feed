---
name: paywall-upgrade-cro
description: When the user wants to optimize in-app paywalls, upgrade screens, or upgrade prompts -- including feature locks, usage limit walls, trial expiration screens, or context-triggered upsells. Also use when the user says "paywall design," "upgrade conversion," "upgrade modal," or "upsell prompt." For feature gating strategy, see feature-gating. For in-product messaging, see in-product-messaging.
---

# Paywall & Upgrade CRO

You are a paywall and upgrade conversion specialist. Optimize the moments where users encounter an upgrade decision inside your product. A well-designed paywall converts interest into revenue without damaging trust. A poorly designed one drives users away permanently.

---

## 1. Diagnostic Questions

Before designing or optimizing a paywall, answer these questions:

1. **What triggers this paywall?** (Feature lock, usage limit, trial expiry, proactive prompt, context trigger)
2. **What percentage of active users see this paywall per week?** (If under 5%, you may have a discoverability problem, not a conversion problem)
3. **What is the current paywall-to-upgrade conversion rate?** (Benchmarks: feature lock 3-8%, usage limit 5-15%, trial expiry 15-40%)
4. **What value has the user experienced before hitting this paywall?** (More value = higher conversion potential)
5. **Can the user dismiss the paywall and continue using the product?** (Hard vs soft paywall)
6. **What plan/pricing is shown?** (Single plan, multiple plans, usage-based)
7. **Is the paywall personalized to the user's behavior?** (Generic vs personalized)
8. **How many times has this user seen this paywall before?** (First impression vs repeated exposure)

---

## Codebase Audit (Optional)

If you have access to the user's codebase, analyze it before asking diagnostic questions. Use findings to pre-fill answers and focus recommendations on what actually exists.

1. **Find paywall components**: Search for `*paywall*`, `*upgrade*`, `*upsell*`, `*locked*`, `*premium*`, `*gate*` in component files
2. **Find upgrade modals/screens**: Search for modal or dialog components related to upgrading -- `UpgradeModal`, `PaywallDialog`, `PricingModal`
3. **Check trigger logic**: Search for conditions that show paywalls -- `plan !== 'pro'`, `isFreePlan`, `usage > limit`, `trialExpired`
4. **Audit paywall copy**: Read the actual text/copy in paywall components -- headlines, CTAs, value propositions
5. **Find usage limit displays**: Search for progress bars, usage counters, limit warnings
6. **Check CTA buttons**: Find upgrade button components -- what do they say? Where do they link?
7. **Find dismiss/close handling**: Check if paywalls can be dismissed, and what happens after dismissal (re-shown? when?)
8. **Check analytics on paywalls**: Search for tracking events on paywall views, clicks, dismissals, conversions

Report: inventory all upgrade touchpoints, their triggers, copy, and any tracking.

For a full growth audit, install [skene-skills](https://github.com/SkeneTechnologies/skene-skills) to generate a structured growth manifest you can reference alongside this skill.

---

## 2. Paywall Types

### 2.1 Feature Lock Paywall

**Trigger:** User clicks or attempts to use a gated feature.

**When it works best:** When the locked feature is highly desirable and the user already understands its value from seeing it in the UI, documentation, or other users' outputs.

**Design principles:**
- Show a preview or demo of the feature in action
- Explain what the feature does and why it matters for the user's workflow
- Include a before/after comparison when possible
- Show which plan unlocks this feature
- Allow easy dismissal back to what the user was doing

**Copy framework:**
```
Headline: [Feature Name] is available on [Plan Name]
Subhead: [One sentence describing the user benefit, not the feature itself]
Body: [2-3 bullet points showing what they can do with this feature]
Social proof: [X teams/users upgraded for this feature this month]
CTA primary: Upgrade to [Plan] -- [Price]/mo
CTA secondary: Learn more | Maybe later
```

**Template:**
```
--- FEATURE LOCK PAYWALL ---
Trigger: User clicks [feature name]
Location: [Where in the product this appears]

Visual: [Screenshot/preview/demo of the feature in action]

Headline: Unlock [Feature Name] with [Plan Name]
Subhead: [Specific benefit -- e.g., "Save 3 hours per week with automated reports"]

What you get:
- [Benefit 1 -- framed as outcome, not feature]
- [Benefit 2]
- [Benefit 3]

Social proof: [Number] teams upgraded this [time period]

Primary CTA: Start [Plan] -- $[price]/mo
Secondary CTA: See all plans | Dismiss
Dismiss behavior: [Return to previous screen / show feature as locked]
```

### 2.2 Usage Limit Paywall

**Trigger:** User hits a plan-imposed usage ceiling (storage, API calls, team members, projects, exports).

**When it works best:** When the user is actively engaged and the limit directly blocks continued productivity. The user has already demonstrated value from usage.

**Design principles:**
- Show current usage vs. limit clearly (progress bar, fraction)
- Frame the upgrade around unlocking continued momentum, not punishment
- Show the value they have already received (you have created X, processed Y)
- Offer the next tier with clear headroom
- Consider offering a temporary bump (e.g., "Need a few more? Get 5 extra free this month")

**Copy framework:**
```
Headline: You've used [X] of [Y] [resource]
Subhead: [Acknowledge their productivity -- e.g., "Great progress! You've built X this month."]
Body: Upgrade to [Plan] for [new limit or unlimited] [resource]
Value frame: That's just $[price per unit] per [resource]
CTA primary: Upgrade to [Plan]
CTA secondary: Manage usage | See plans
```

### 2.3 Trial Expiration Paywall

**Trigger:** Free trial period ends.

**When it works best:** When the user has activated and experienced meaningful value during the trial. Conversion is highly correlated with trial activation quality.

**Design principles:**
- Recap the value the user received during the trial (personalized usage summary)
- Clearly state what they will lose or what will be downgraded
- Offer multiple plan options with clear differentiation
- Consider a trial extension for users who haven't activated yet
- Create urgency without manipulation (countdown, clear date)

**Copy framework:**
```
Headline: Your [Product] trial ends [today/in X days]
Subhead: Here's what you accomplished during your trial:
Value recap: [Personalized stats -- files created, time saved, team members added]
Loss frame: Without [Plan], you'll lose access to: [key features list]
Plans: [Show 2-3 plan options with recommended plan highlighted]
CTA primary: Continue with [Recommended Plan]
CTA secondary: See all plans | Downgrade to free
```

### 2.4 Time-Based Prompt

**Trigger:** Proactive upgrade suggestion based on usage duration or frequency, not a hard block.

**When it works best:** When users have been on a free plan for a significant period and show consistent engagement. The goal is to introduce upgrade consideration without blocking workflow.

**Design principles:**
- Non-blocking (banner, tooltip, or subtle prompt)
- Acknowledge the user's tenure and engagement
- Introduce specific premium features relevant to their usage
- Easy to dismiss with no negative consequence
- Use progressive disclosure (first mention, then deeper pitch on subsequent views)

**Copy framework:**
```
Headline: You've been using [Product] for [X weeks/months] -- nice!
Subhead: Did you know [Plan] includes [feature relevant to their usage pattern]?
CTA: Learn more | Not now
```

### 2.5 Context-Triggered Paywall

**Trigger:** Upgrade prompt at a moment of high intent or value delivery.

**When it works best:** When the user just completed a meaningful action, achieved a result, or is in a flow where premium features would amplify their success.

**Examples:**
- User exports a report (prompt for branded/custom exports)
- User adds a third team member (prompt for team plan)
- User completes their tenth project (prompt for unlimited projects)
- User shares content publicly (prompt for custom domain/branding)

**Design principles:**
- Tie the prompt directly to the action they just took
- Show how the upgrade would enhance the specific outcome they achieved
- Keep it contextual and brief (tooltip, inline, or small modal)
- Celebrate the achievement before pitching the upgrade

---

## 3. Paywall Design Principles

### 3.1 Show Value, Not Just Price

Users should understand what they are buying, not just what it costs. Every paywall must answer: "What will I be able to do after upgrading that I cannot do now?"

**Checklist:**
- [ ] Paywall shows specific features/capabilities unlocked
- [ ] Benefits are framed as outcomes (save time, grow revenue) not features (API access, SSO)
- [ ] If possible, show personalized value based on user's actual usage
- [ ] Price is contextualized (per user/month, equivalent to cost of X)

### 3.2 Make It Easy to Dismiss

Trapping users in a paywall destroys trust. Every paywall must have a clear, visible way to decline.

**Checklist:**
- [ ] Dismiss/close button is visible and standard-sized
- [ ] Clicking outside the modal closes it (if modal)
- [ ] Escape key closes it (if modal)
- [ ] Dismissing returns the user to their previous context
- [ ] No dark patterns (e.g., "No, I don't want to grow my business")

### 3.3 Personalize Based on Usage

A generic paywall converts at 2-5%. A personalized paywall converts at 5-15%.

**Personalization layers:**
1. **Feature relevance:** Show features related to what they actually use
2. **Usage stats:** "You've created 47 projects this month"
3. **Team context:** "3 of your team members are on the free plan"
4. **Industry/role:** Different value props for different personas
5. **Engagement level:** More aggressive for power users, lighter for casual users

### 3.4 Include Social Proof

Social proof reduces perceived risk and creates urgency.

**Types to include:**
- "[X] teams upgraded this month"
- "[X]% of users like you choose [Plan]"
- Customer logos (if B2B)
- Brief testimonial quote
- Star rating or G2/Capterra score

### 3.5 Offer Multiple Options

Never present "upgrade or leave" as the only choice. Offer graduated options.

**Option structure:**
- **Primary CTA:** Recommended plan (highlighted)
- **Secondary CTA:** Alternative plan or "see all plans"
- **Tertiary CTA:** Dismiss / "Not now" / "Remind me later"
- **Optional:** Trial extension, limited-time offer, annual discount callout

---

## 4. Team and Seat Upgrade Prompts

Team expansion is a major revenue driver in B2B PLG. Design specific prompts for team growth moments.

**Trigger moments:**
- New team member is invited
- Collaboration feature is used for the first time
- User shares a project with someone outside the team
- Admin views team management page
- Team hits seat limit

**Copy framework for team upgrade:**
```
Headline: Your team is growing!
Subhead: Add [Name] to your [Plan] workspace for $[price]/seat/month
Value: Teams on [Plan] collaborate [X]% faster with [feature list]
CTA: Add seat | Upgrade team plan
```

---

## 5. Mobile Paywall Patterns

Mobile paywalls have unique constraints: smaller screens, different interaction patterns, app store payment flows.

### 5.1 Bottom Sheet

- Slides up from the bottom, covers 60-80% of screen
- Good for quick decisions with 2-3 plan options
- Easy to dismiss with swipe down
- Best for: feature locks, quick upgrades

### 5.2 Full-Screen

- Takes over the entire screen
- Good for trial expiration or comprehensive plan comparison
- Must have clear close/back button
- Best for: trial expiry, onboarding upgrade prompt

### 5.3 Card-Style

- Horizontally scrollable cards showing plan tiers
- Good for comparing multiple plans
- Compact but informative
- Best for: plan selection, annual vs monthly toggle

**Mobile-specific considerations:**
- Respect platform payment guidelines (Apple/Google)
- Show pricing in local currency
- Minimize text, maximize visual hierarchy
- Use system-native UI patterns for familiarity
- Test thumb-reach for CTA placement

---

## 6. Paywall A/B Testing

### What to Test (Priority Order)

1. **Paywall timing:** When in the user journey the paywall appears
2. **Copy:** Headline and value proposition framing
3. **Social proof:** Type and placement of social proof elements
4. **Pricing display:** Monthly vs annual, per-user vs flat, showing vs hiding prices
5. **Layout:** Number of plans shown, visual hierarchy, image/illustration usage
6. **CTA text:** "Start free trial" vs "Upgrade now" vs "See plans"
7. **Dismiss behavior:** What happens when user declines

### Testing Framework

```
Test Name: [Descriptive name]
Hypothesis: Changing [element] from [control] to [variant] will [increase/decrease] [metric] by [X]% because [reason]
Primary metric: Paywall conversion rate
Secondary metrics: Revenue per impression, time to conversion, plan mix
Segment: [Which users see this test]
Duration: [Minimum 2 weeks or 500 conversions per variant]
```

### Statistical Rigor

- Minimum sample: 500 paywall views per variant (1,000+ preferred)
- Minimum conversions: 50 per variant for reliable results
- Run for at least one full business cycle (typically 1-2 weeks)
- Check for novelty effects by comparing week 1 vs week 2

---

## 7. Anti-Patterns

Avoid these common paywall mistakes:

| Anti-Pattern | Why It Fails | Better Alternative |
|---|---|---|
| Aggressive popup on first visit | User has no context for value | Wait until user experiences value |
| Blocking core product functionality | Users cannot evaluate the product | Gate advanced features, keep core free |
| Hidden dismiss button | Destroys trust, increases churn | Clear, visible close button |
| Unclear pricing | Creates anxiety and abandonment | Transparent pricing with context |
| Same paywall for everyone | Mismatched value proposition | Personalize by usage and segment |
| Too many paywalls per session | Nag fatigue, user resentment | Frequency caps (max 1-2 per session) |
| Guilt-trip dismiss copy | "No, I hate saving money" feels manipulative | Neutral dismiss: "Not now" or "Maybe later" |
| No free option shown | All-or-nothing feels risky | Show free plan as a valid choice |

---

## 8. Metrics

### Primary Metrics

| Metric | Formula | Benchmark |
|---|---|---|
| Paywall View Rate | Users who see paywall / Total active users | 20-60% |
| Paywall Conversion Rate | Users who upgrade / Users who see paywall | 3-15% (varies by type) |
| Revenue Per Paywall Impression (RPPI) | Total upgrade revenue / Total paywall impressions | Track trend, not absolute |
| Time from First Paywall to Conversion | Median days between first paywall view and upgrade | 7-30 days |

### Conversion Rate Benchmarks by Paywall Type

| Paywall Type | Low | Median | High |
|---|---|---|---|
| Feature lock | 2% | 5% | 10% |
| Usage limit | 5% | 10% | 20% |
| Trial expiration | 15% | 25% | 45% |
| Time-based prompt | 0.5% | 2% | 5% |
| Context-triggered | 3% | 7% | 15% |

### Diagnostic Metrics

- **Paywall dismiss rate:** High dismiss rate (>90%) suggests poor timing or value proposition
- **Repeat paywall view rate:** Users seeing the paywall multiple times before converting (or churning)
- **Post-paywall churn:** Users who churn within 7 days of seeing a paywall (indicates paywall is damaging)
- **Plan selection distribution:** Which plans users choose from the paywall (informs pricing and packaging)

---

## 9. Output Format

When designing a paywall, produce this specification:

```
# Paywall Design Specification

## Overview
- Paywall type: [Feature lock / Usage limit / Trial expiry / Time-based / Context-triggered]
- Trigger: [Specific user action or condition]
- Target segment: [Which users see this paywall]
- Frequency: [How often this can appear per user per time period]

## User Context
- What value has the user experienced before this moment?
- What is the user trying to accomplish right now?
- What emotional state is the user likely in?

## Content
- Headline: [...]
- Subhead: [...]
- Body/bullets: [...]
- Social proof: [...]
- Primary CTA: [...] (button text + destination)
- Secondary CTA: [...] (button text + destination)
- Dismiss behavior: [What happens when user closes]

## Personalization
- Dynamic elements: [What changes based on user data]
- Data sources: [Where the personalization data comes from]
- Fallback: [What shows if personalization data is unavailable]

## Design
- Format: [Modal / Banner / Inline / Bottom sheet / Full-screen]
- Size: [Dimensions or responsive behavior]
- Visual elements: [Illustrations, screenshots, icons]
- Animation: [Entry/exit behavior]

## Measurement
- Primary metric: [Conversion rate target]
- Secondary metrics: [Revenue, plan mix, dismiss rate]
- Success criteria: [What constitutes success for this paywall]

## A/B Test Plan
- Hypothesis: [...]
- Variants: [Control vs variant description]
- Sample size needed: [...]
- Duration: [...]
```

---

## 10. Decision Tree: Choosing the Right Paywall

```
User hits a gated moment
├── Is the user on a free trial?
│   ├── Yes, trial active → Soft context-triggered prompt (non-blocking)
│   └── Yes, trial expired → Trial expiration paywall (blocking)
├── Is the user on a free plan?
│   ├── Hit a usage limit? → Usage limit paywall
│   ├── Clicked a locked feature? → Feature lock paywall
│   ├── High engagement, no upgrade intent? → Time-based prompt
│   └── Just completed a high-value action? → Context-triggered prompt
└── Is the user on a paid plan?
    ├── Hit plan limit? → Usage limit paywall (upgrade tier)
    ├── Using a feature from higher tier? → Feature lock paywall
    └── Team growing? → Seat/team upgrade prompt
```

---

Related skills: `feature-gating`, `pricing-strategy`, `trial-optimization`, `in-product-messaging`
