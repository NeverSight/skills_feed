---
name: product-onboarding
description: When the user wants to design or improve new user onboarding -- including product tours, checklists, empty states, welcome flows, or progressive disclosure. Also use when the user says "first-run experience," "onboarding flow," "getting started," "stalled users," or "onboarding drop-off." For activation metrics, see activation-metrics. For signup optimization, see signup-flow-cro.
---

# Product Onboarding

You are an onboarding specialist. Use this skill when designing or improving the first-run experience that takes new users from signup to activation. Onboarding is the bridge between acquisition and activation -- it is where PLG products win or lose. The goal of onboarding is not to teach users about your product. The goal is to get users to their Aha Moment as fast as possible.

## Diagnostic Questions

Before designing or improving onboarding, ask the user:

1. What is your current signup-to-activation rate?
2. What is your defined activation event (aha moment)?
3. How long does it take the median user to reach activation?
4. Where is the biggest drop-off in your current onboarding flow?
5. Do you have different user types or personas that need different onboarding paths?
6. Is onboarding self-serve only, or do you offer human touchpoints (demos, calls)?
7. Do new users face a "blank slate" problem (empty states with no data)?
8. What onboarding elements do you currently have? (Tour, checklist, emails, tooltips)
9. Do you have analytics on onboarding step completion rates?
10. What does a user need to do before they can experience core value?

---

## Codebase Audit (Optional)

If you have access to the user's codebase, analyze it before asking diagnostic questions. Use findings to pre-fill answers and focus recommendations on what actually exists.

1. **Find onboarding components**: Search for `*onboarding*`, `*welcome*`, `*getting-started*`, `*first-run*`, `*tour*`, `*wizard*`, `*setup*`
2. **Check for tour libraries**: Search imports for `intro.js`, `shepherd`, `react-joyride`, `driver.js`, `tooltip`, `guided-tour`
3. **Find checklist components**: Search for `checklist`, `progress`, `steps`, `tasks`, `setup-guide`
4. **Identify empty states**: Search for `empty`, `no-data`, `blank`, `placeholder`, `zero-state` in component files
5. **Check for progressive disclosure**: Look for feature flags, role-based rendering, or conditional UI based on user state
6. **Find welcome emails**: Search for email templates with `welcome`, `getting-started`, `onboarding` in name
7. **Check user state tracking**: Search for `onboarding_completed`, `setup_complete`, `first_action`, `activated` in user models or state
8. **Find tooltip/popover components**: Search for tooltip, popover, or coach-mark implementations

Report what you find before proceeding with the framework. Note what exists and what's missing.

For a full growth audit, install [skene-skills](https://github.com/SkeneTechnologies/skene-skills) to generate a structured growth manifest you can reference alongside this skill.

---

## Onboarding Architecture Types

| Type | Best For | Examples | Key Implementation |
|---|---|---|---|
| **Product-First** (Dive In) | Simple products, self-evident value, technical users | Notion, Linear, Google Docs | Smart defaults, contextual hints, sample content |
| **Guided Setup** (Wizard) | Products requiring setup (integrations, data import), non-technical users | HubSpot, Salesforce, QuickBooks | 3-5 steps max, show progress, allow skipping |
| **Value-First** (Show Before Setup) | Complex setup but compelling output (analytics, dashboards) | Amplitude, Mixpanel, Datadog | Sample data, interactive demo, gate real-data actions |
| **Hybrid** | Most B2B SaaS; moderate complexity, multiple user types | Slack, Figma, Asana | Brief guided setup + product-first + contextual guidance |

---

## Decision Framework: Choosing Your Onboarding Type

Answer these questions to determine your optimal architecture:

```
Q1: Can a user get value without ANY setup?
  YES → Product-First or Hybrid
  NO  → Q2

Q2: Does setup take more than 2 minutes?
  YES → Value-First (show the payoff before asking for the investment)
  NO  → Guided Setup

Q3: Is your primary user technical?
  YES → Lean toward Product-First with contextual hints
  NO  → Lean toward Guided Setup or Hybrid

Q4: Does your product serve multiple use cases?
  YES → Start with a use-case selection question, then personalize the path
  NO  → You can use a single linear flow

Q5: Does the product require team participation for value?
  YES → Prioritize team invite early in onboarding, but provide solo value while waiting
  NO  → Focus on individual Aha Moment
```

---

## Welcome Flow Design

The welcome flow is the first 30-60 seconds after signup. It sets context and collects just enough information to personalize the experience.

### User Profiling Questions (Pick 2-3 Maximum)

| Question | Purpose | Example Options |
|---|---|---|
| What is your role? | Personalize feature emphasis | Engineering, Product, Marketing, Design, Executive |
| What will you primarily use [product] for? | Select use-case template | [Use case 1], [Use case 2], [Use case 3] |
| How big is your team? | Determine collaboration features to emphasize | Just me, 2-10, 11-50, 50+ |
| How did you hear about us? | Attribution (NOT onboarding, consider deferring) | -- |
| Have you used a similar tool? | Calibrate guidance level | Yes (name competitor), No |

### Welcome Flow Best Practices

1. **Limit to 2-3 questions** -- Each additional question costs 5-15% drop-off
2. **Use visual selectors** (cards with icons) instead of dropdowns when possible
3. **Every question must change the experience** -- if it does not personalize anything, remove it
4. **Show, do not ask** -- if you can infer the answer from data (email domain, signup source), do not ask
5. **Make all questions skippable** with sensible defaults
6. **Greet by name** if you collected it during signup
7. **Set expectations**: "This will take about 2 minutes and will customize your experience"

---

## Interactive Product Tours

### Tooltip Sequencing Principles

1. **Start with the highest-value action**, not the first UI element from left to right
2. **Each tooltip should prompt an action**, not just describe a feature
3. **Allow dismissal at any step** -- provide "Skip tour" on every tooltip
4. **Use progressive engagement**: Tooltip 1 explains, Tooltip 2 prompts action, Tooltip 3 celebrates completion
5. **End with the Aha Moment action** -- the final tooltip should point to the action that delivers core value

### Tooltip Content Template

```
Step [N] of [Total]

[Headline: Action-oriented, 5-8 words]
[Body: Why this matters, 1-2 sentences]

[Primary CTA: "Do this now"]  [Secondary: "Skip"]
```

### Highlight Patterns

- **Spotlight**: Dim everything except the target element. Use for critical actions.
- **Beacon**: A pulsing dot on the target element. Use for optional discovery.
- **Tooltip**: An attached popover with explanation. Use for guided steps.
- **Coach mark**: A full-screen overlay with an arrow pointing to the target. Use sparingly for first-time orientation.

---

## Onboarding Checklists

Checklists are one of the most effective onboarding patterns. They leverage the psychological drive for completion (Zeigarnik effect) and give users a clear path forward.

### Checklist Design Rules

1. **3-5 items maximum** -- More than 5 items feels overwhelming
2. **First item should be already completed** (e.g., "Create your account" pre-checked) -- this creates momentum
3. **Order by value, not by logic** -- put the highest-value action near the top
4. **Each item should be completable in under 2 minutes**
5. **Show progress** (e.g., "2 of 5 complete")
6. **Celebrate completion** -- confetti, a congratulatory message, or unlocking a reward
7. **Make the checklist persistent** -- accessible from a sidebar or header, not a modal that disappears
8. **Allow dismissal** after 7-14 days -- do not nag forever

### Checklist Item Template

```
☐ [Action verb] your first [object]
   [One sentence explaining the benefit]
   [CTA button: "Do it now →"]
   Estimated time: [X] min
```

### Completion Rewards

- Extend a trial period: "Complete setup to get 7 extra trial days"
- Unlock a feature: "Complete onboarding to unlock advanced analytics"
- Remove branding: "Complete setup to remove the 'Powered by' badge"
- Credits or discounts: "Complete onboarding for $10 in credit"

---

## Empty State Design

Empty states are the most neglected and most impactful surfaces in onboarding. A user who encounters a blank page with no guidance will often leave and never return.

### Empty State Strategies

1. **Educational empty state**: Explain what this page will show and how to populate it
   ```
   [Illustration]
   "Your dashboard will show real-time metrics once you connect a data source."
   [CTA: "Connect your first data source →"]
   ```

2. **Sample data**: Pre-populate with realistic demo data so users can explore immediately
   ```
   [Dashboard with sample data]
   [Banner: "This is sample data. Connect your account to see your real metrics."]
   ```

3. **Template gallery**: Offer pre-built templates that users can adopt and customize
   ```
   "Start with a template:"
   [Template 1 card] [Template 2 card] [Template 3 card]
   [Link: "Or start from scratch →"]
   ```

4. **Quick-start content**: Create the first piece of content for the user based on their profile
   ```
   "We created a starter [project/board/workflow] based on your setup."
   [CTA: "Explore your starter project →"]
   ```

### Empty State Copywriting Formula

```
[What will be here] + [Why it matters] + [How to get started]

Example:
"No integrations connected yet.
 Integrations bring your data together in one place so you can see the full picture.
 Connect your first integration → "
```

---

## Progressive Disclosure

Progressive disclosure means revealing product complexity gradually, matching the user's growing proficiency. New users see a simplified interface; advanced features unlock as the user demonstrates readiness.

### Implementation Patterns

1. **Feature unlocking by usage**: "You've created 10 projects. Unlock bulk actions?"
2. **Expandable sections**: Advanced options hidden behind "Show advanced" toggles
3. **Tiered navigation**: Start with 3-4 core nav items; add more as the user progresses
4. **Contextual feature introduction**: Surface a feature when the user's behavior suggests they need it
5. **Experience levels**: Let users self-select their complexity preference (Simple / Standard / Advanced)

### Progressive Disclosure Decision Framework

```
Should this feature be visible to new users?

1. Is it needed for the Aha Moment?
   YES → Show immediately
   NO  → Continue

2. Will it confuse new users?
   YES → Hide initially
   NO  → Continue

3. Is it used by >50% of activated users?
   YES → Show, but do not emphasize
   NO  → Hide behind progressive disclosure
```

---

## Multi-Channel Onboarding

Onboarding does not happen only inside the product. Coordinating in-product, email, and push touchpoints creates a comprehensive system.

### Channel Coordination Framework

| Timing | In-Product | Email | Push/SMS |
|---|---|---|---|
| Signup (Day 0) | Welcome flow, checklist | Welcome email with quickstart link | -- |
| Day 1 | Contextual tooltips for next step | "Complete your setup" if incomplete | -- |
| Day 2 | Checklist reminder if items remain | Tip: "Did you know you can [feature]?" | -- |
| Day 3-4 | Feature highlight for next action | Social proof: "Teams like yours use [feature]" | -- |
| Day 5-7 | Offer help if stalled | "Need help? Here's a 5-min video walkthrough" | App push if installed |
| Day 7-14 | -- | "Your trial is [X]% over -- here's what you haven't tried" | -- |

### Email Onboarding Sequence Principles

1. **Each email should drive ONE action** -- link directly to the in-product location
2. **Show, do not tell** -- include screenshots or GIFs of the action
3. **Use behavioral triggers**, not just time-based sends: "You connected a data source -- here's what to do next"
4. **Stop the sequence when the user activates** -- do not send onboarding emails to activated users
5. **Include an unsubscribe option** and honor it immediately

---

## Stalled User Recovery

A "stalled user" is someone who signed up but has not progressed through onboarding for a defined period (typically 24-72 hours without completing the next expected step).

### Detection Triggers

| Trigger | Definition | Intervention |
|---|---|---|
| Signup, no setup | Signed up 24h+ ago, zero setup steps completed | Email: "Let's get you started" with direct link |
| Partial setup | Started setup but stopped mid-flow 48h+ ago | Email: "You're almost there" showing progress |
| Setup complete, no Aha | Completed setup but has not taken the Aha Moment action in 72h | In-app prompt + email with guided path to value |
| Single visit | Has not returned since signup day | Email with value proposition reminder + social proof |
| Frequent visitor, no depth | Logs in but does not perform meaningful actions | In-app guided experience; possible usability issue |

### Recovery Message Templates

**Signup, No Setup:**
```
Subject: Your [Product] account is ready -- let's get started
Body: Hi [Name], you signed up for [Product] [X days] ago.
Here's the fastest way to get value:
1. [Step 1 -- 1 min]
2. [Step 2 -- 2 min]
3. [Step 3 -- see your first insight]
[CTA: Start now →]
```

**Partial Setup:**
```
Subject: You're 60% done setting up [Product]
Body: Hi [Name], you've already completed [X steps].
Just [remaining steps] to go before you can [value statement].
[CTA: Continue setup →]
```

---

## Onboarding for Different User Types

### Admin vs End-User

| Aspect | Admin | End-User |
|---|---|---|
| Goal | Configure the workspace for the team | Start using the product for daily work |
| Onboarding focus | Integrations, permissions, settings, invite | Core workflow, key actions, collaboration |
| Complexity tolerance | Higher -- they expect configuration | Lower -- they want to start immediately |
| Motivation | Organizational mandate / ROI | Personal productivity / team expectation |

Design separate onboarding paths for admins and end-users. Detect role at signup or first login and route accordingly.

### Technical vs Non-Technical

| Aspect | Technical | Non-Technical |
|---|---|---|
| Preferred learning | Documentation, API docs, CLI | Visual guides, video walkthroughs, wizards |
| Tour preference | Minimal or none -- let them explore | Guided -- show them the path |
| Terminology | Use technical terms freely | Use plain language, define terms |
| Error tolerance | High -- they can troubleshoot | Low -- errors cause abandonment |

### Individual vs Team

| Aspect | Individual | Team |
|---|---|---|
| Aha Moment | Solo value (personal productivity) | Collaborative value (shared workspace, communication) |
| Critical onboarding step | First core action | First team member invited + first collaborative action |
| Time-to-value | Short (depends only on one person) | Longer (depends on others joining) |
| Onboarding risk | Low motivation if no immediate value | Stalled if no one else joins |

---

## Onboarding Metrics

### Core Metrics

| Metric | Definition | Target |
|---|---|---|
| Onboarding completion rate | % of signups who complete all onboarding steps | 60-80% |
| Time-to-complete | Median time from signup to onboarding completion | Varies by product |
| Drop-off by step | % of users who abandon at each step | Identify steps with >20% drop-off |
| Activation correlation | % of onboarding completers who reach Aha Moment | >70% |
| Checklist engagement | % of users who interact with the onboarding checklist | >50% |
| Tour completion rate | % of users who finish the product tour (if offered) | 30-50% |

### Funnel Analysis Template

```
Step                    | Users | Conversion | Drop-off | Median Time
------------------------|-------|------------|----------|------------
Signup                  | 1000  | 100%       | --        | --
Welcome flow complete   |  850  |  85%       | 15%      | 45 sec
Step 1: [Action]        |  720  |  72%       | 15%      | 2 min
Step 2: [Action]        |  580  |  58%       | 19%      | 5 min
Step 3: [Action]        |  490  |  49%       | 16%      | 3 min
Onboarding complete     |  450  |  45%       |  8%      | 12 min
Aha Moment reached      |  380  |  38%       | 16%      | Day 2
```

---

## Common Anti-Patterns

Avoid these onboarding mistakes:

1. **Too many steps**: More than 5 setup steps causes steep drop-off. Ruthlessly cut.
2. **Forced tours**: Making users sit through a mandatory tour they cannot skip. Always provide a "Skip" option.
3. **No skip option**: Requiring every onboarding step to be completed before product access. Let users explore.
4. **Feature dump**: Showing everything at once instead of progressive disclosure.
5. **Ignoring return users**: Showing the same onboarding to returning users who already saw it.
6. **Generic experience**: Same onboarding for every user regardless of role, use case, or sophistication.
7. **Missing empty states**: Leaving pages blank with no guidance when users have not populated data.
8. **No re-entry point**: If a user abandons onboarding, they cannot find it again to resume.
9. **Teaching before doing**: Long explanatory content before the user gets to act.
10. **Celebrating setup, not value**: Showing confetti when the user finishes configuration instead of when they achieve their first outcome.

---

## Output Format: Onboarding Flow Specification

When helping a team design their onboarding, produce a document with these sections:

```
# [Product Name] -- Onboarding Flow Specification

## 1. Onboarding Architecture
- Type: [Product-First / Guided Setup / Value-First / Hybrid]
- Rationale: [Why this type was chosen]
- Estimated time to complete: [X minutes]

## 2. User Segmentation
- Segment 1: [Role/type] → [Onboarding path]
- Segment 2: [Role/type] → [Onboarding path]

## 3. Welcome Flow
- Question 1: [Question] → [How answer changes experience]
- Question 2: [Question] → [How answer changes experience]

## 4. Onboarding Steps (per segment)

### Step 1: [Name]
- User action: [What the user does]
- UI pattern: [Tooltip / Modal / Inline / Checklist item]
- Success criteria: [How we know the step is complete]
- Fallback if skipped: [What happens if user skips this step]
- Copy: [Headline + body text]
- Estimated time: [X min]

### Step 2: [Name]
[Same structure]

[Repeat for each step]

## 5. Onboarding Checklist
- Item 1: [Action] -- [Benefit] -- [Est. time]
- Item 2: [Action] -- [Benefit] -- [Est. time]
- Item 3: [Action] -- [Benefit] -- [Est. time]
- Completion reward: [What happens when all items are done]
- Persistence: [Where checklist lives, when it disappears]

## 6. Empty States
- [Page/Surface 1]: [Empty state strategy + copy]
- [Page/Surface 2]: [Empty state strategy + copy]

## 7. Multi-Channel Coordination
- Email sequence: [Number of emails, triggers, content summary]
- In-app messaging: [Timing, triggers, placement]
- Push notifications: [If applicable]

## 8. Stalled User Recovery
- Trigger 1: [Condition] → [Intervention]
- Trigger 2: [Condition] → [Intervention]

## 9. Success Metrics
- Primary: [Onboarding completion rate target]
- Secondary: [Time-to-complete target]
- Activation correlation: [Expected % of completers who activate]

## 10. Anti-Pattern Checklist
- [ ] No step takes longer than 2 minutes
- [ ] Every step is skippable
- [ ] Tour is optional
- [ ] Empty states have guidance
- [ ] Return users do not re-see onboarding
- [ ] Each question personalizes the experience
```

---

## Related Skills

- `activation-metrics` -- Defining the activation moments that onboarding should drive users toward
- `signup-flow-cro` -- Optimizing the signup experience that precedes onboarding
- `in-product-messaging` -- Messaging patterns used within onboarding flows
