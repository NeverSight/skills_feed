---
name: fogg-behavior-model
description:
  Design behavior change using the B=MAP framework. Use when designing
  onboarding flows, improving conversion, building habits, increasing feature
  adoption, or understanding why users don't take desired actions.
---

# Fogg Behavior Model - B = MAP

The Fogg Behavior Model explains that three elements must converge at the same
moment for a behavior to occur: **Motivation**, **Ability**, and a **Prompt**.
When a behavior does not occur, at least one of these elements is missing.

## When to Use This Skill

- Designing onboarding and activation flows
- Improving conversion rates
- Building habit-forming products
- Increasing feature adoption
- Understanding why users drop off
- Planning behavior change interventions

## The B = MAP Formula

```
┌─────────────────────────────────────────────────────────────────┐
│                    BEHAVIOR = MAP                                │
│                                                                  │
│    Behavior happens when Motivation, Ability, and Prompt        │
│    come together at the SAME MOMENT.                            │
│                                                                  │
│    When behavior doesn't happen → at least one is missing.      │
└─────────────────────────────────────────────────────────────────┘

    High  │                    ·····
    M     │              ·····     Behavior
    o     │        ·····           Happens
    t     │   ·····                Here
    i     │····─────────────────────────────
    v     │   Action Line
    a     │
    t     │        Behavior
    i     │        Fails
    o     │        Here
    n     │
    Low   └─────────────────────────────────────
              Hard ←── Ability ──→ Easy

    Prompts only work above the Action Line.
```

## The Three Elements

### 1. Motivation

**What drives the user to act?**

```
Motivation Sources:

Core Motivators (Fogg):
├── Pleasure / Pain
├── Hope / Fear
└── Social Acceptance / Rejection

Additional Drivers:
├── Intrinsic interest
├── Personal goals
├── External rewards
└── Social pressure
```

| Motivator     | Low                 | High                     |
| ------------- | ------------------- | ------------------------ |
| Pleasure/Pain | "I should exercise" | "I want to feel great"   |
| Hope/Fear     | "Might be useful"   | "Don't want to miss out" |
| Social        | "No one cares"      | "Everyone's doing it"    |

### 2. Ability

**How easy is it to do?**

```
Ability Factors (Fogg):

Simplicity Chain (weakest link determines ability):
├── Time: How long does it take?
├── Money: How much does it cost?
├── Physical effort: How hard physically?
├── Mental effort: How much thinking?
├── Social deviance: How weird is it?
└── Non-routine: How different from habits?

Ability = Inverse of the HARDEST factor
```

| Factor   | Low Ability       | High Ability        |
| -------- | ----------------- | ------------------- |
| Time     | 30-minute signup  | 2-click signup      |
| Money    | $99/month         | Free trial          |
| Physical | Visit store       | Click button        |
| Mental   | Complex form      | Smart defaults      |
| Social   | Public commitment | Private action      |
| Routine  | New behavior      | Fits existing habit |

### 3. Prompt

**What triggers action at the right moment?**

```
Prompt Types:

Spark (High Ability, Low Motivation):
├── Inspires and motivates
├── Appeals to emotions
└── Example: "Your friends are waiting"

Facilitator (High Motivation, Low Ability):
├── Makes action easier
├── Reduces friction
└── Example: "One-click purchase"

Signal (High Motivation, High Ability):
├── Simple reminder
├── Just needs timing
└── Example: "Time to check in"
```

## Behavior Diagnosis Framework

### Step 1: Define Target Behavior

Be specific about what you want users to do:

```
Behavior Definition:

❌ Vague: "Use the app more"
✅ Specific: "Complete a 5-minute workout daily"

Components:
├── Who: [Target user segment]
├── What: [Specific action]
├── When: [Timing/context]
└── How often: [Frequency]
```

### Step 2: Diagnose Missing Element

```
Diagnosis Tree:

Is the user doing the behavior?
│
├── NO → Diagnose which element is missing:
│   │
│   ├── Do they WANT to do it?
│   │   ├── NO → Motivation problem
│   │   └── YES → Continue
│   │
│   ├── CAN they easily do it?
│   │   ├── NO → Ability problem
│   │   └── YES → Continue
│   │
│   └── Are they PROMPTED at the right moment?
│       ├── NO → Prompt problem
│       └── YES → Re-examine all three
│
└── YES → Behavior successful
```

### Step 3: Design Intervention

| Problem         | Solution Approach                      |
| --------------- | -------------------------------------- |
| Low Motivation  | Increase desire (spark prompt)         |
| Low Ability     | Reduce friction (facilitator prompt)   |
| No Prompt       | Add well-timed trigger (signal prompt) |
| Multiple issues | Start with Ability (easiest to change) |

## Output Template

After completing analysis, document as:

```markdown
## Behavior Design Analysis

**Target Behavior:** [Specific behavior]

**User Segment:** [Who]

**Date:** [Date]

### Current State

| Element    | Score (1-5) | Evidence              |
| ---------- | ----------- | --------------------- |
| Motivation | [Score]     | [What indicates this] |
| Ability    | [Score]     | [What indicates this] |
| Prompt     | [Score]     | [What indicates this] |

### Ability Breakdown

| Factor   | Current State | Bottleneck? |
| -------- | ------------- | ----------- |
| Time     | [Assessment]  | Yes/No      |
| Money    | [Assessment]  | Yes/No      |
| Physical | [Assessment]  | Yes/No      |
| Mental   | [Assessment]  | Yes/No      |
| Social   | [Assessment]  | Yes/No      |
| Routine  | [Assessment]  | Yes/No      |

### Diagnosis

**Primary Issue:** [Motivation/Ability/Prompt]

**Root Cause:** [Specific reason]

### Intervention Design

| Priority | Change            | Element | Expected Impact      |
| -------- | ----------------- | ------- | -------------------- |
| 1        | [Specific change] | [M/A/P] | [Measurable outcome] |
| 2        | [Specific change] | [M/A/P] | [Measurable outcome] |

### Success Metrics

| Metric          | Current | Target | Timeline |
| --------------- | ------- | ------ | -------- |
| [Behavior rate] | X%      | Y%     | [Time]   |
```

## Real-World Examples

### Example 1: Daily Exercise Habit

```
Target Behavior: Do a 20-minute workout daily

Motivation:
├── Want to get fit ✓
├── Feel better ✓
└── Score: 4/5 (High)

Ability:
├── Time: 20 min → Could be less
├── Physical: Moderate effort
├── Mental: Need to decide what to do
├── Routine: Not part of current habits
└── Score: 2/5 (Low - bottleneck)

Prompt:
├── No consistent trigger
└── Score: 2/5 (Low)

Interventions:
├── Ability: Reduce to 5-minute starter routine
├── Ability: Pre-select workout (no decisions)
├── Prompt: Phone alarm + clothes laid out
└── Routine: Anchor to morning coffee
```

### Example 2: Feature Adoption (SaaS)

```
Target Behavior: Use new collaboration feature

Motivation:
├── Users don't see value yet
└── Score: 2/5 (Low - problem)

Ability:
├── Feature is buried in menu
├── Requires 4 clicks to access
└── Score: 2/5 (Low - problem)

Prompt:
├── One email announcement sent
└── Score: 1/5 (Very low)

Interventions:
├── Motivation: Show social proof ("Teams save 2hrs/week")
├── Ability: Add one-click access from dashboard
├── Ability: Pre-configure with defaults
├── Prompt: In-app tooltip at relevant moment
└── Prompt: Contextual suggestion during related tasks
```

### Example 3: Newsletter Signup

```
Target Behavior: Subscribe to weekly newsletter

Motivation:
├── Valuable content promised
├── Social proof: "10,000 subscribers"
└── Score: 3/5 (Medium)

Ability:
├── Email only (simple)
├── One field
└── Score: 5/5 (High)

Prompt:
├── Popup after 30 seconds
├── User often not ready yet
└── Score: 2/5 (Wrong timing)

Intervention:
├── Prompt: Move to end of valuable article
├── Prompt: "Want more like this?"
└── Context: After user received value
```

## Design Principles

### Start with Ability

```
Why Ability First:

Motivation:
├── Hard to change
├── Often outside your control
└── Fluctuates over time

Ability:
├── Directly designable
├── Permanent once improved
└── Helps when motivation dips

"Make it so easy they can't say no."
```

### Right Prompt, Right Moment

```
Prompt Timing:

Too Early:
├── User not ready
├── Creates annoyance
└── Wasted impression

Too Late:
├── Moment passed
├── Motivation cooled
└── Friction accumulated

Just Right:
├── High motivation moment
├── Ability is present
└── Action is natural next step
```

### Tiny Habits Approach

```
BJ Fogg's Tiny Habits:

1. Make it TINY
   └── Smallest possible version of behavior

2. Find the right ANCHOR
   └── Existing habit to attach to

3. Celebrate IMMEDIATELY
   └── Positive emotion reinforces

Formula: "After I [ANCHOR], I will [TINY BEHAVIOR]"

Example: "After I pour my coffee, I will do 2 pushups"
```

## Behavior Types

| Type       | Motivation | Ability | Focus                 |
| ---------- | ---------- | ------- | --------------------- |
| **Green**  | High       | High    | Just add prompt       |
| **Blue**   | High       | Low     | Increase ability      |
| **Purple** | Low        | High    | Increase motivation   |
| **Gray**   | Low        | Low     | Major redesign needed |

## Integration with Other Methods

| Method             | Combined Use                           |
| ------------------ | -------------------------------------- |
| **Hooked Model**   | Fogg explains the trigger/action phase |
| **Cognitive Load** | Ability = inverse of cognitive load    |
| **Loss Aversion**  | Powerful motivation lever              |
| **Curiosity Gap**  | Motivation through information gaps    |
| **Five Whys**      | Why isn't behavior happening?          |

## Quick Reference

```
B = MAP CHECKLIST

Motivation Boosters:
□ Clear value proposition
□ Social proof present
□ Loss framing considered
□ Personalized relevance
□ Emotional connection

Ability Enhancers:
□ Minimum steps possible
□ Smart defaults set
□ No unnecessary fields
□ Mobile-friendly
□ Fits existing routines

Prompt Optimization:
□ Right type for situation
□ Appears at right moment
□ Clear call to action
□ Not interruptive
□ Contextually relevant
```

## Resources

- [BJ Fogg's Behavior Model](https://behaviormodel.org/)
- [Tiny Habits - BJ Fogg](https://tinyhabits.com/)
- [Hooked - Nir Eyal](https://www.nirandfar.com/hooked/)
- [Atomic Habits - James Clear](https://jamesclear.com/atomic-habits)
