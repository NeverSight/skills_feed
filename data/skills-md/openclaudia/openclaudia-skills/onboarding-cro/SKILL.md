---
name: onboarding-cro
description: >
  Improve user onboarding flows to increase activation and retention. Use when
  asked to design welcome screens, setup wizards, product tours, onboarding
  checklists, or activation sequences. Trigger phrases: "onboarding flow",
  "user activation", "welcome screen", "product tour", "onboarding checklist",
  "first-run experience", "setup wizard", "aha moment", "time to value",
  "user onboarding", "activation rate".
---

# Onboarding CRO

Design and optimize user onboarding flows that drive activation and long-term retention.

---

## 1. Onboarding Frameworks

### Jobs-To-Be-Done (JTBD) Onboarding

The best onboarding flows are organized around the user's job, not the product's features.

**Process:**
1. Identify the user's primary job-to-be-done
2. Map the minimum steps to complete that job in your product
3. Guide the user through those steps, removing all distractions
4. Celebrate completion (aha moment)

**Example (Notion):**
- Job: "I need to organize my team's projects"
- Steps: Create workspace > Invite team > Create first page > Use a template
- The onboarding flow guides exactly this path, nothing more

**Anti-pattern:** Feature tours that show every feature. Users do not care about features during onboarding; they care about solving their problem.

### Progressive Disclosure

Reveal functionality gradually as users demonstrate readiness.

**Levels:**
1. **First session:** Only show core functionality needed for primary job
2. **After first success:** Introduce secondary features that enhance the core workflow
3. **After repeated use:** Surface power features, integrations, customization
4. **After mastery:** Invite to advanced features, API, automation

**Implementation:**
- Use feature flags or user state to control what's visible
- Track user actions to determine when to advance disclosure level
- Never show everything at once

### Activation Metrics

Define your activation metric before designing onboarding. The activation metric is the action most correlated with long-term retention.

**Examples:**

| Product | Activation Metric | Timeframe |
|---------|------------------|-----------|
| Slack | Send 2,000 messages (team) | First 30 days |
| Dropbox | Upload 1 file from 2 devices | First 7 days |
| Facebook | Add 7 friends | First 10 days |
| Zoom | Host first meeting | First 7 days |
| Notion | Create 3 pages | First 7 days |
| Figma | Create first design | First 3 days |
| HubSpot | Import contacts + send first email | First 14 days |

**How to find your activation metric:**
1. Cohort analysis: Compare retained vs churned users
2. Identify actions that retained users took that churned users did not
3. Find the action with strongest correlation to 30-day retention
4. Validate by testing whether guiding users to that action improves retention

### Aha Moment Identification

The aha moment is when a user first experiences the core value of your product.

**Framework for identifying it:**
1. What do users say when they recommend your product? ("It's amazing because...")
2. When during their journey do users typically say "wow" or "this is cool"?
3. What single action separates users who stay from those who leave?

**The aha moment is NOT:**
- Signing up
- Completing onboarding
- Seeing a feature demo

**The aha moment IS:**
- Getting their first result
- Experiencing time saved
- Seeing their data visualized for the first time
- Completing their first task successfully

---

## 2. Onboarding Components

### Welcome Screens

The first screen after signup. Serves two purposes: make the user feel welcomed and collect information for personalization.

**Best Practices:**
- Use the user's name ("Welcome, Sarah!")
- Keep it to 1-3 questions maximum
- Use visual selectors (cards with icons) instead of dropdowns
- Every question should directly affect their experience
- Always allow skipping

**Template:**
```
Welcome to [Product], [Name]!

Let's personalize your experience.

What's your primary goal?
[ ] [Goal 1 -- with icon]
[ ] [Goal 2 -- with icon]
[ ] [Goal 3 -- with icon]
[ ] Something else

[Continue]  [Skip for now]
```

**Example (Notion):**
```
What will you use Notion for?
[Personal] [Team] [School]

How big is your team?
[Just me] [2-10] [11-50] [50+]
```

### Setup Wizards

Guided multi-step flows that set up the product for use.

**When to use:** When the product requires configuration before it can deliver value (CRM, analytics, marketing automation).

**Best Practices:**
- Maximum 3-5 steps
- Show progress indicator
- Pre-fill defaults where possible
- Allow skipping non-essential steps
- Provide "try it with sample data" option
- End with a clear next action, not a blank screen

**Template:**
```
Step 1: Connect your [data source]
  [Connect Google] [Connect manually] [Use sample data]

Step 2: Configure your [workspace/project]
  [Pre-filled sensible defaults with edit option]

Step 3: Invite your team (optional)
  [Email input] [Copy invite link] [Skip]

You're all set!
  [Go to your dashboard]
```

### Product Tours

Interactive walkthroughs of the product interface.

**Types:**
1. **Tooltip tour:** Highlights UI elements with explanatory tooltips (Intercom, Appcues)
2. **Video walkthrough:** Short video showing key workflows
3. **Interactive tutorial:** User performs real actions with guidance
4. **Sandbox mode:** Pre-populated environment for safe exploration

**Best Practices:**
- Keep tours under 5 steps (3 is ideal)
- Focus on ONE workflow per tour
- Let users exit at any point
- Make the user DO something, not just read
- Trigger contextually (first time visiting a feature), not globally
- Never replay completed tours unless user requests it

**Anti-patterns:**
- 15-step tours that show every button
- Forced tours that cannot be dismissed
- Tours that explain obvious UI elements
- Tours that trigger repeatedly

**Template (per step):**
```
Step [X] of [Y]:

[Pointer to UI element]

"[Action verb] here to [achieve result]."

[Try it now] / [Next] / [Skip tour]
```

### Onboarding Checklists

Persistent task lists that guide users through activation.

**Why they work:**
- Zeigarnik effect: People feel compelled to complete unfinished tasks
- Clear progress visualization
- Users self-pace through the list
- Can be dismissed and revisited

**Template:**
```
Get started with [Product]  [3/5 complete]

[x] Create your account
[x] Set up your profile
[x] [First key action]
[ ] [Second key action] <-- "Do this next"
[ ] [Third key action]

[Dismiss checklist]
```

**Best Practices:**
- 4-6 items maximum
- Pre-check easy items (account creation) for momentum
- Order by dependency and importance
- Highlight the next recommended step
- Celebrate completion (confetti, badge, reward)
- Include at least one "aha moment" action
- Show percentage complete or progress bar

**Example (Slack):**
```
Getting started  [2/4]
[x] Set your profile photo
[x] Join a channel
[ ] Send your first message
[ ] Invite a teammate
```

**Example (Figma):**
```
Welcome to Figma  [1/5]
[x] Create your account
[ ] Create a design file
[ ] Add a frame
[ ] Use a component
[ ] Share with your team
```

### Email Onboarding Sequences

Drip emails that complement the in-app experience.

**Sequence structure:**

| Day | Email | Purpose |
|-----|-------|---------|
| 0 | Welcome + quick start | Immediate value, link to first action |
| 1 | Tip: [Core feature] | Teach one key feature |
| 3 | Social proof | Show what others achieve with the product |
| 5 | "Need help?" | Address common obstacles, offer support |
| 7 | Feature highlight | Introduce a secondary feature |
| 10 | Activation reminder | If not activated, nudge toward key action |
| 14 | Upgrade prompt | If activated, pitch premium features |

**Day 0 Welcome Email Template:**
```
Subject: Welcome to [Product] -- here's your quick start

Hi [Name],

You're in! Here's how to get the most out of [Product] in the next 5 minutes:

1. [First action] -- [link directly to it]
2. [Second action] -- [link]
3. [Third action] -- [link]

[Primary CTA: "Go to your dashboard"]

Need help? Reply to this email or check our [getting started guide].

[Signature]
```

**Day 3 Social Proof Email Template:**
```
Subject: How [Customer] uses [Product] to [Result]

Hi [Name],

Did you know that [Customer/Company] uses [Product] to [specific result with metric]?

Here's what they did:
1. [Step they took]
2. [Step they took]
3. [Result they achieved]

You can do the same:
[CTA: "Try it now"]
```

---

## 3. Onboarding Examples from Top Products

### Notion

**What they do well:**
- Welcome screen asks role + use case (2 questions)
- Offers templates based on selection
- Pre-populates workspace with starter content
- Progressive disclosure: basic blocks first, databases later
- Checklist in sidebar tracks setup progress
- Empty states have clear CTAs

**Activation metric:** Create 3+ pages in first 7 days

### Slack

**What they do well:**
- Workspace setup wizard is 3 steps (name, invite, channel)
- Slackbot guides first interactions conversationally
- Pre-created #general and #random channels with welcome messages
- Teaches features by having users use them (send a message, react with emoji)
- Onboarding checklist in sidebar

**Activation metric:** Team sends 2,000 messages in first 30 days

### Figma

**What they do well:**
- Minimal signup (Google OAuth one-click)
- Immediately drops user into a canvas with interactive tutorial
- Tutorial teaches by doing (create shape, move it, style it)
- Sample files available to explore
- Team collaboration demonstrated early (cursor presence)

**Activation metric:** Create first design file in first 3 days

### Canva

**What they do well:**
- Asks "What will you design today?" with visual categories
- Immediately shows templates relevant to selection
- First design experience uses pre-made template (user edits, not creates from scratch)
- Celebrates first download with sharing prompt

### Linear

**What they do well:**
- Import from existing tools (Jira, Asana) as first step
- Pre-configured with sensible defaults (workflow states, labels)
- Keyboard shortcuts taught in context
- Empty states show exactly what to do next

---

## 4. Measuring Onboarding Success

### Key Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| Onboarding completion rate | Users who complete onboarding / signups | 60-80% |
| Time to first key action | Time from signup to first meaningful action | Under 5 min |
| Activation rate | Users hitting activation metric / signups | 20-40% |
| Day 1 retention | Users returning day after signup / signups | 40-60% |
| Day 7 retention | Users returning 7 days after signup / signups | 20-35% |
| Day 30 retention | Users active 30 days after signup / signups | 10-25% |
| Onboarding step drop-off | Users completing step N / users starting step N | Track per step |
| Time to value (TTV) | Median time from signup to aha moment | As low as possible |

### Funnel Analysis

Build an onboarding funnel in your analytics tool:

```
Signup completed
  -> Welcome screen completed
    -> First key action
      -> Second key action (aha moment)
        -> Activation metric reached
          -> Day 7 return
```

Track conversion rate between each step. The biggest drop-off is your biggest opportunity.

---

## 5. A/B Test Ideas for Onboarding

### Welcome Screen
1. 1 question vs 3 questions on welcome screen
2. Visual card selection vs dropdown
3. Personalized template suggestions vs generic

### Setup Flow
4. Guided setup vs "explore on your own"
5. Pre-populated sample data vs empty state
6. Setup wizard vs onboarding checklist

### Product Tour
7. Tooltip tour vs video walkthrough
8. 3-step tour vs 5-step tour
9. Auto-triggered tour vs user-initiated

### Activation
10. Email nudge on day 1 vs day 3 for inactive users
11. In-app prompt for next action vs no prompt
12. Celebrating milestones (confetti, badge) vs no celebration
13. Showing progress ("You're 60% set up") vs not showing

### Engagement
14. Daily tip emails vs weekly digest
15. Push notifications for incomplete onboarding vs email only
16. Peer comparison ("Teams like yours usually...") vs no comparison

---

## 6. Onboarding Audit Template

When auditing an existing onboarding flow:

```
## Onboarding Audit: [Product Name]
### Date: [Date]

### Current Flow Map
[Step-by-step flow with screenshots]

### Time to Complete
- Minimum path: [X] minutes
- Average path: [X] minutes

### Drop-off Analysis
| Step | Users Entering | Completion Rate | Drop-off |
|------|---------------|-----------------|----------|
| Signup | 100% | X% | X% |
| Welcome screen | X% | X% | X% |
| Setup step 1 | X% | X% | X% |
| Setup step 2 | X% | X% | X% |
| First key action | X% | X% | X% |
| Activation | X% | -- | -- |

### Scores (1-10)
| Dimension | Score | Notes |
|-----------|-------|-------|
| Time to value | X | |
| Clarity of next step | X | |
| Progressive disclosure | X | |
| Error recovery | X | |
| Mobile experience | X | |
| Personalization | X | |
| **Overall** | **X** | |

### Issues Found
1. **[Critical]** [Issue] -- Impact: [X]% activation loss
2. **[High]** [Issue]
3. **[Medium]** [Issue]

### Recommendations (Priority Order)
1. [Recommendation] -- Expected lift: X% on [metric]
2. [Recommendation] -- Expected lift: X%
3. [Recommendation] -- Expected lift: X%

### Quick Wins
- [ ] [Immediate fix]
- [ ] [Immediate fix]

### Long-term Improvements
- [ ] [Bigger initiative]
- [ ] [Bigger initiative]
```

---

## 7. Common Onboarding Mistakes

1. **Showing everything at once** -- Overwhelms users. Use progressive disclosure.
2. **Explaining features, not outcomes** -- "This is our dashboard" vs "See your results here."
3. **Forcing completion before value** -- Let users explore, then guide.
4. **No empty state strategy** -- Blank screens kill activation. Use templates, samples, or guided prompts.
5. **One-size-fits-all flow** -- Different user types need different onboarding paths.
6. **Ignoring mobile** -- Mobile onboarding needs its own design (not a shrunk desktop flow).
7. **No re-engagement for drop-offs** -- Users who abandon onboarding need targeted email nudges.
8. **Celebrating signup, not activation** -- "Welcome!" is not the goal. The first success moment is.
9. **Too many tooltips** -- If you need 10 tooltips, your UI is too complex.
10. **No measurement** -- If you are not tracking step-by-step drop-offs, you are guessing.
