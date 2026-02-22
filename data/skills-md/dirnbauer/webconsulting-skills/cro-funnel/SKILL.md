---
name: cro-funnel
description: >-
  Full-funnel Conversion Rate Optimization (CRO) for SaaS and web apps. Covers page CRO,
  form optimization, signup flow, onboarding activation, popup/modal design, and
  paywall/upgrade screens. Use when optimizing any part of the conversion funnel.
license: MIT
metadata:
  version: "1.0.0"
---

# CRO Funnel Optimization

> **Source:** This skill is adapted from **[AgentKits Marketing](https://github.com/aitytech/agentkits-marketing)** 
> by AITYTech. Enterprise-grade AI marketing automation (MIT License).

Full-funnel Conversion Rate Optimization covering every stage from page visit to paid conversion:

```
Visitor → Page CRO → Form CRO → Signup CRO
     ↓
  Popup CRO (capture abandoners)
     ↓
New User → Onboarding CRO → Activation
     ↓
Free User → Paywall CRO → Paid Customer
```

---

## 1. Form CRO

Optimize lead capture forms, contact forms, demo requests, and quote forms (not signup/registration).

### Core Principles

1. **Every Field Has a Cost** - Each field reduces completion by 10-25%
2. **Value Must Exceed Effort** - Clear value proposition above form
3. **Reduce Cognitive Load** - One question per field, logical grouping

### The 5-Field Rule

| Fields | Typical Impact |
|--------|---------------|
| 3 fields | Baseline |
| 4-6 fields | 10-25% reduction |
| 7+ fields | 25-50%+ reduction |

For each field, ask:
- Is this absolutely necessary before we can help them?
- Can we get this information another way?
- Can we ask this later?

### Field Optimization

**Email**: Single field, inline validation, typo detection

**Name**: Test single "Name" vs. First/Last split

**Phone**: Make optional if possible, explain why if required

**Message**: Make optional, expand on focus

### Multi-Step Forms

Use when:
- More than 5-6 fields needed
- Logically distinct sections
- Conditional paths based on answers

Best practices:
- Progress indicator (step X of Y)
- Start with easy, end with sensitive
- Allow back navigation
- Save progress

### Submit Button Copy

**Weak**: "Submit", "Send"

**Strong**: "[Action] + [What they get]"
- "Get My Free Quote"
- "Download the Guide"
- "Request Demo"

---

## 2. Signup Flow CRO

Optimize registration, account creation, and trial activation flows.

### Core Principles

1. **Minimize Required Fields** - Email + Password minimum
2. **Show Value Before Asking** - Can they experience product first?
3. **Reduce Perceived Effort** - "Takes 30 seconds"

### Field Priority

| Priority | Fields |
|----------|--------|
| Essential | Email, Password |
| Often needed | Name |
| Usually deferrable | Company, Role, Team size, Phone |

### Social Auth Options

- B2C: Google, Apple, Facebook
- B2B: Google, Microsoft, SSO
- Consider "Sign up with Google" as primary

### Single-Step vs. Multi-Step

**Single-step works**: 3 or fewer fields, simple B2C, high-intent visitors

**Multi-step works**: More than 3-4 fields, B2B needing segmentation

**Progressive commitment pattern**:
1. Email only (lowest barrier)
2. Password + name
3. Customization questions (optional)

### Trust Elements

- "No credit card required" (if true)
- "Free forever" or "14-day free trial"
- Privacy note: "We'll never share your email"
- Testimonial near signup form

---

## 3. Onboarding CRO

Optimize post-signup user activation and time-to-value.

### Core Principles

1. **Time-to-Value Is Everything** - How quickly can someone experience core value?
2. **One Goal Per Session** - Don't teach everything at once
3. **Do, Don't Show** - Interactive > Tutorial
4. **Progress Creates Motivation** - Show advancement, celebrate completions

### Define Your Aha Moment

The action that correlates most strongly with retention:

| Product Type | Aha Moment |
|-------------|------------|
| Project management | Create first project + add team member |
| Analytics | Install tracking + see first report |
| Design tool | Create first design + export/share |
| Collaboration | Invite first teammate |
| Marketplace | Complete first transaction |

### Onboarding Checklist Pattern

Best practices:
- 3-7 items (not overwhelming)
- Order by value (most impactful first)
- Start with quick wins
- Progress bar/completion %
- Celebration on completion

Example item:
```
☐ Connect your first data source (2 min)
  Get real-time insights from your existing tools
  [Connect Now]
```

### Empty States

Empty states are onboarding opportunities:
- Explain what this area is for
- Show what it looks like with data
- Clear primary action to add first item
- Optional: Pre-populate with example data

### Handling Stalled Users

1. **Detection**: Define "stalled" criteria (X days inactive)
2. **Email sequence**: Reminder of value, address blockers, offer help
3. **In-app recovery**: Welcome back message, pick up where left off
4. **Human touch**: Personal outreach for high-value accounts

---

## 4. Popup CRO

Optimize popups, modals, overlays, slide-ins, and banners.

### Core Principles

1. **Timing Is Everything** - Too early = annoying, too late = missed opportunity
2. **Value Must Be Obvious** - Clear, immediate benefit
3. **Respect the User** - Easy to dismiss, remember preferences

### Trigger Strategies

| Trigger | When to Use | Example |
|---------|-------------|---------|
| Scroll-based (25-50%) | Blog posts, long-form content | "You're halfway through—get more" |
| Exit intent | E-commerce, lead gen | "Wait! Before you go..." |
| Click-triggered | Lead magnets, demos | Zero annoyance |
| Time-based (30-60s) | Proven engagement | General site visitors |

### Popup Types

**Email Capture**: Newsletter subscription
- Clear value prop (not just "Subscribe")
- Single field (email only)
- Consider incentive

**Lead Magnet**: Exchange content for email
- Show what they get (cover image)
- Minimal fields

**Exit Intent**: Last-chance conversion
- Acknowledge they're leaving
- Different offer than entry popup

**Announcement Banner**: Site-wide communication
- Top of page, dismissable
- Time-limited

### Headline Formulas

- Benefit: "Get [result] in [timeframe]"
- Question: "Want [desired outcome]?"
- Social proof: "Join [X] people who..."
- Curiosity: "The one thing [audience] always get wrong"

### Decline Options

**Good**: "No thanks", "Maybe later"

**Avoid**: "No, I don't want to save money" (manipulative)

### Frequency Rules

- Show maximum once per session
- Remember dismissals (7-30 days before showing again)
- Exclude converted users
- Exclude checkout/conversion flows

---

## 5. Paywall & Upgrade CRO

Optimize in-app paywalls, upgrade screens, and freemium conversion.

### Core Principles

1. **Value Before Ask** - User should have experienced value first
2. **Show, Don't Just Tell** - Demonstrate the value of paid features
3. **Friction-Free Path** - Easy to upgrade when ready
4. **Respect the No** - Don't trap or pressure

### Paywall Trigger Points

| Trigger | Example |
|---------|---------|
| Feature gates | Click paid-only feature |
| Usage limits | Hit storage/project limit |
| Trial expiration | 7, 3, 1 day warnings |
| Context-triggered | Power user behavior |

### Paywall Screen Components

1. **Headline**: Focus on benefit, not price
   - "Unlock [Feature] to [Benefit]"
   - NOT: "Upgrade to Pro for $X/month"

2. **Value Demonstration**: Preview the feature in action

3. **Social Proof**: "X teams use this feature"

4. **CTA**: "Upgrade to Pro" (specific)

5. **Escape Hatch**: "Continue with Free" (respectful)

### Feature Lock Paywall Template

```
[Lock Icon]
This feature is available on Pro

[Feature preview/screenshot]

[Feature name] helps you [benefit]:
• [Specific capability]
• [Specific capability]

[Upgrade to Pro - $X/mo]
[Maybe Later]
```

### Trial Expiration Template

```
Your trial ends in 3 days

What you'll lose:
• [Feature they've used]
• [Data they've created]

What you've accomplished:
• Created X projects

[Continue with Pro - $X/mo]
[Remind me later] [Downgrade to Free]
```

### Anti-Patterns to Avoid

- Hiding the close button
- Confusing plan selection
- Guilt-trip copy
- Asking before value delivered
- Too frequent prompts
- Surprise charges

---

## Quick Reference: CRO by Funnel Stage

| Stage | Key Metric | Primary Focus |
|-------|-----------|---------------|
| Page | Bounce rate, CTA clicks | Value prop clarity, visual hierarchy |
| Form | Completion rate | Reduce fields, clear labels |
| Signup | Signup completion | Minimize friction, social auth |
| Onboarding | Activation rate | Time to aha moment |
| Popup | Conversion rate | Timing, value exchange |
| Paywall | Upgrade rate | Value demonstration |

---

## Measurement

### Key Metrics by Stage

- **Form start rate**: Page views → Started form
- **Completion rate**: Started → Submitted
- **Field drop-off**: Which fields lose people
- **Activation rate**: % reaching aha moment
- **Time to activation**: Days to first value
- **Upgrade rate**: Free → Paid conversion

---

## Credits & Attribution

This skill is adapted from **[AgentKits Marketing](https://github.com/aitytech/agentkits-marketing)** by AITYTech.

**Copyright (c) AITYTech** - MIT License  
Adapted by webconsulting.at for this skill collection
