---
name: hooked-ux
description: 'Hook Model framework for building habit-forming products based on Nir Eyal''s "Hooked". Use when you need to: (1) increase user engagement and retention, (2) design habit loops in your product, (3) audit why users aren''t returning, (4) create effective triggers and notifications, (5) design variable reward systems, (6) increase investment and switching costs, (7) evaluate the ethics of your engagement tactics, (8) optimize onboarding for habit formation.'
---

# Hook Model Framework

Framework for building habit-forming products. Based on a fundamental truth: habits are not created—they are built through successive cycles through the Hook.

## Core Principle

**The Hook Model** = a four-phase process that connects the user's problem to your solution frequently enough to form a habit.

```
Trigger → Action → Variable Reward → Investment
    ↑                                      │
    └──────────────────────────────────────┘
```

**Habit Zone:** Products enter the "habit zone" when used frequently enough and with enough perceived value. The goal is to move users from deliberate usage to automatic, habitual behavior.

## Scoring

**Goal: 10/10.** When reviewing or creating product engagement mechanics, rate them 0-10 based on adherence to the principles below. A 10/10 means full alignment with all guidelines; lower scores indicate gaps to address. Always provide the current score and specific improvements needed to reach 10/10.

## The Four Phases

### 1. Trigger

The actuator of behavior. What prompts the user to take action?

**Two types of triggers:**

| Type | Definition | Examples |
|------|------------|----------|
| **External** | Sensory stimuli in the environment | Push notification, email, button, ad, word of mouth |
| **Internal** | Internal cue, emotion, or routine | Boredom, loneliness, uncertainty, fear of missing out |

**The goal:** Move users from external triggers (you prompt them) to internal triggers (they prompt themselves).

**Mapping triggers to emotions:**

| Internal Trigger (Emotion) | Example Product |
|---------------------------|-----------------|
| Boredom | Instagram, TikTok, YouTube |
| Loneliness | Facebook, Messaging apps |
| Uncertainty/FOMO | Twitter, News apps |
| Confusion | Google, Stack Overflow |
| Stress/Anxiety | Games, Meditation apps |

See: [references/triggers.md](references/triggers.md) for detailed trigger design.

### 2. Action

The simplest behavior done in anticipation of a reward.

**Fogg Behavior Model:** `B = MAT`
- **M**otivation: User wants to do it
- **A**bility: User can easily do it
- **T**rigger: User is prompted to do it

**Six elements of simplicity (ability):**

| Element | Question | Example |
|---------|----------|---------|
| Time | How long does it take? | Infinite scroll vs. page load |
| Money | What's the financial cost? | Free tier vs. paywall |
| Physical effort | How much work? | Voice input vs. typing |
| Brain cycles | How much thinking? | Autocomplete vs. blank field |
| Social deviance | Is it socially acceptable? | Anonymous vs. public |
| Non-routine | How unfamiliar? | Familiar patterns vs. new UI |

**Key insight:** Increasing motivation is hard. Reducing friction is easier and often more effective.

**Action formula:**
```
Ease of action > User's motivation threshold
```

### 3. Variable Reward

The phase that keeps users coming back. The anticipation of reward (not the reward itself) creates dopamine.

**Three types of variable rewards:**

| Type | Definition | Examples |
|------|------------|----------|
| **Tribe** | Social rewards from others | Likes, comments, followers, status |
| **Hunt** | Search for resources/information | Scrolling feeds, search results, deals |
| **Self** | Personal accomplishment | Leveling up, completion, mastery |

**Critical:** Rewards must be **variable**. Predictable rewards lose power. The slot machine effect: uncertainty is addictive.

**Autonomy:** Users must feel in control. Forced engagement backfires.

See: [references/rewards.md](references/rewards.md) for reward design patterns.

### 4. Investment

The phase that increases the likelihood of another pass through the Hook.

**Principle:** Users value what they put effort into (IKEA effect). Investment creates switching costs.

**Types of investment:**

| Investment | Example | Switching Cost |
|------------|---------|----------------|
| **Data** | Preferences, history, uploads | Loss of personalization |
| **Content** | Posts, playlists, documents | Loss of created work |
| **Reputation** | Reviews, ratings, followers | Loss of social proof |
| **Skill** | Learning the interface | Learning curve for alternatives |
| **Social** | Connections, groups | Losing relationships |

**Investment loads the next trigger:**
- Creating content → Notification when someone responds
- Following users → Feed updates
- Setting preferences → Personalized recommendations

## The Habit Zone

Two axes determine if a product can become a habit:

| | Low Frequency | High Frequency |
|--|---------------|----------------|
| **High Perceived Value** | Viable product (needs ads/marketing) | **HABIT ZONE** |
| **Low Perceived Value** | Failure | Failure |

**Questions:**
- How often do users need to engage? (Daily, weekly, monthly?)
- What's the perceived value of each engagement?
- Is frequency high enough to form automatic behavior?

## Habit Testing

The 5% rule: A product has formed a habit when at least 5% of users show unprompted, habitual usage.

**Three questions for habit testing:**

1. **Who are the habitual users?**
   - Which users engage most frequently?
   - What do they have in common?

2. **What are they doing?**
   - What's the "Habit Path" (common sequence of actions)?
   - What differentiates power users from casual users?

3. **Why are they doing it?**
   - What internal trigger drives the behavior?
   - What emotion precedes usage?

See: [references/habit-testing.md](references/habit-testing.md) for testing methodology.

## The Manipulation Matrix

Framework for evaluating the ethics of habit-forming products.

|  | **Maker Uses Product** | **Maker Doesn't Use** |
|--|------------------------|----------------------|
| **Materially Improves User's Life** | **Facilitator** ✓ | **Peddler** ⚠️ |
| **Doesn't Improve Life** | **Entertainer** | **Dealer** ✗ |

**Questions to ask:**
1. Would I use this product myself?
2. Does it genuinely help users achieve their goals?
3. Am I exploiting vulnerabilities or serving needs?

### When NOT to Use the Hook Model

The Hook Model is inappropriate when:
- Your product doesn't genuinely improve lives
- You're targeting vulnerable populations (children, addiction-prone users)
- Business model depends on user regret
- Engagement conflicts with user wellbeing

See [ethical-boundaries.md](references/ethical-boundaries.md) for comprehensive ethics guidance.

### Regulatory Context

Be aware of emerging regulations around:
- **Children's apps:** COPPA, GDPR-K restrictions
- **Dark patterns:** FTC enforcement increasing
- **Notification practices:** Some jurisdictions regulating "addictive" features
- **Loot boxes:** Gaming regulations expanding

## Onboarding Audit Checklist

Optimizing onboarding for habit formation:

### First Trigger
- [ ] Is the first action obvious and easy?
- [ ] Is the value proposition clear before asking for investment?
- [ ] Are we using the right external trigger for this user?

### First Action
- [ ] Can the user complete the core action in under 60 seconds?
- [ ] Have we removed all unnecessary friction?
- [ ] Is the UI familiar (not requiring new learning)?

### First Reward
- [ ] Does the user get immediate feedback?
- [ ] Is there a variable element (surprise, delight)?
- [ ] Does the reward connect to an internal trigger?

### First Investment
- [ ] Do we ask for investment after reward (not before)?
- [ ] Is the investment small but meaningful?
- [ ] Does the investment load the next trigger?

### Loop Completion
- [ ] Is there a clear path back to the trigger?
- [ ] Do we send external triggers at appropriate times?
- [ ] Are we measuring progression through the Hook?

## Quick Diagnostic

Audit any product feature:

| Question | If No | Action |
|----------|-------|--------|
| What's the internal trigger? | Users need reminders to use it | Research user emotions |
| Is the action dead simple? | Users start but don't complete | Remove friction |
| Is the reward variable? | Users get bored | Add unpredictability |
| Does investment load next trigger? | Users don't return | Connect investment to triggers |

## Warning Signs

Your habit loop is broken if:

- Users need constant external triggers (they're not forming habits)
- Engagement drops after novelty wears off (weak reward)
- Users don't increase usage over time (no investment)
- High churn despite initial engagement (wrong internal trigger)
- Users describe product as "useful but forgettable"

## Reference Files

- [triggers.md](references/triggers.md): External and internal trigger design, emotion mapping
- [rewards.md](references/rewards.md): Variable reward types, reinforcement schedules, reward timing
- [habit-testing.md](references/habit-testing.md): Testing methodology, habit zone identification
- [case-studies.md](references/case-studies.md): Instagram, Slack, Duolingo, Pinterest, and failed products analysis
- [ethical-boundaries.md](references/ethical-boundaries.md): Dark patterns vs. ethical engagement, protecting vulnerable users
- [neuroscience-foundations.md](references/neuroscience-foundations.md): Dopamine, variable reinforcement schedules, habit loop neuroscience
- [product-applications.md](references/product-applications.md): B2B SaaS, e-commerce, health apps, productivity tools patterns

## Further Reading

This skill is based on the Hook Model developed by Nir Eyal. For the complete methodology, research, and case studies, read the original book:

- [*"Hooked: How to Build Habit-Forming Products"*](https://www.amazon.com/Hooked-How-Build-Habit-Forming-Products/dp/1591847788?tag=wondelai00-20) by Nir Eyal
