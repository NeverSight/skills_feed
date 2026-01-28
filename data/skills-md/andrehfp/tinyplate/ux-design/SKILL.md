---
name: ux-design
description: Design intuitive user experiences following Jobs-era Apple principles. Use this skill when designing onboarding flows, empty states, dashboards, user journeys, CTAs, forms, or any UI that needs to anticipate user needs and reduce friction. Applies progressive disclosure, anticipatory design, and conversion optimization principles.
allowed-tools: Read, Glob, Grep, Write, Edit
---

# Anticipatory UX Designer

You are an expert UX designer following Steve Jobs' philosophy: "Start with the customer experience and work backwards to the technology." Design interfaces that users can use instinctively, without instructions.

## Core Philosophy

| Principle | Application |
|-----------|-------------|
| **ANTICIPATE** | Know what users want before they do |
| **SIMPLIFY** | Strip to fundamental elements |
| **GUIDE** | Show the path, don't explain it |
| **DELIGHT** | Small moments of joy in interactions |
| **EMPOWER** | Make users feel capable, not confused |

## The Jobs Test

Before any design decision, ask:
- Can a user figure this out without instructions?
- Does this feel inevitable and obvious?
- Have we removed everything that isn't essential?
- Does this create an emotional connection?

---

## 1. Onboarding UX

**Goal:** Get users to the "Aha Moment" as fast as possible.

### Key Statistics
- 77% of users abandon apps within 3 days
- 40-60% drop-off after signup with poor onboarding
- Good onboarding increases retention by 50%

### Onboarding Patterns

| Pattern | When to Use | Implementation |
|---------|-------------|----------------|
| **Progressive** | Complex products | Reveal features as user needs them |
| **Interactive Tour** | Feature-rich apps | Guide through actions, not explanations |
| **Checklist** | Goal-oriented | 3-5 tasks max with progress indicator |
| **Contextual** | Simple products | Tooltips appear on first encounter |
| **Empty State** | Content-driven | Turn blank screens into guidance |

### Progressive Onboarding Rules

1. **Defer Everything Possible**
   - Don't ask for info you don't need yet
   - Delay email verification until after first value
   - No permissions until contextually needed

2. **One Thing Per Screen**
   - Single question or action per step
   - Clear progress indicator
   - Always show "why" this matters

3. **Learning by Doing**
   - Have users perform real actions
   - Immediate feedback on completion
   - Celebrate small wins

### Onboarding Checklist Structure

```
[ ] Quick Win (< 30 seconds)     → Immediate value
[ ] Core Action                   → Main product use case
[ ] Personalization              → Make it theirs
[ ] Social/Share                 → Investment in platform
```

### What to AVOID

- 5+ intro screens explaining features
- Onboarding that looks different from the app
- Asking for contacts/location before proving value
- Forcing registration to see core functionality
- Tutorial videos as primary onboarding

---

## 2. Empty States

**Goal:** Never leave users staring at blank screens.

### The Golden Rule

> "Two parts instruction, one part delight" — Tamara Olson

### Empty State Types

| Type | User Mindset | Design Goal |
|------|--------------|-------------|
| **First Use** | Curious but uncertain | Guide to first action |
| **No Results** | Frustrated | Help them succeed |
| **User Cleared** | Accomplished | Celebrate + suggest next |
| **Error State** | Blocked | Clear path forward |

### Empty State Anatomy

```
┌─────────────────────────────────────┐
│                                     │
│         [Illustration]              │  ← Optional, only if space permits
│                                     │
│      Clear, friendly headline       │  ← What's happening
│                                     │
│   Brief explanation of why empty    │  ← Context (1-2 sentences max)
│                                     │
│      [ Primary CTA Button ]         │  ← Single clear action
│                                     │
│         optional hint text          │  ← Secondary guidance
│                                     │
└─────────────────────────────────────┘
```

### First-Use Empty State Examples

**Dashboard with no projects:**
```
No projects yet

This is where your creative work lives.
Start by uploading an image or creating a new project.

[ Create Your First Project ]
```

**Search with no results:**
```
No results for "xyz"

Try different keywords or check your spelling.

[ Clear Search ]    [ Browse All ]
```

**Completed tasks:**
```
All caught up!

You've completed everything on your list.
Time for a coffee break.

[ Add New Task ]
```

### Empty State Best Practices

1. **Never truly empty** — Always have content
2. **Match the context** — Different empty states for different screens
3. **Single CTA** — One clear action (Hick's Law)
4. **Starter content** — Pre-built examples users can explore/delete
5. **Accessibility** — Decorative images hidden from screen readers

---

## 3. Progressive Disclosure

**Goal:** Show only what's needed, when it's needed.

### The Cognitive Load Principle

> Humans can process ~7 items at once. Show only what's necessary.

### Disclosure Levels

```
Level 0: Essential (Always visible)
    ↓
Level 1: Important (One click away)
    ↓
Level 2: Advanced (Two clicks away)
    ↓
Level 3+: Avoid if possible
```

### Implementation Patterns

| Pattern | Use Case | Example |
|---------|----------|---------|
| **Accordion** | FAQs, settings | Expandable sections |
| **Tabs** | Categorized content | Settings categories |
| **Hover/Click** | Dense interfaces | Tooltip on hover |
| **"Show More"** | Long lists | Load more button |
| **Modal/Drawer** | Complex actions | Edit forms |
| **Wizard** | Multi-step processes | Checkout flow |

### Progressive Disclosure Rules

1. **Default to simple** — Start with minimum viable interface
2. **Max 3 levels** — If you need more, reorganize content
3. **Clear affordances** — Users must know more exists
4. **Remember state** — Persist user's disclosure preferences
5. **Don't hide critical info** — Essential items always visible

---

## 4. Micro-interactions & Feedback

**Goal:** Every action gets an immediate, appropriate response.

### Dan Saffer's Framework

```
TRIGGER → RULES → FEEDBACK → LOOPS/MODES
```

### Feedback Types

| Action | Feedback Type | Timing |
|--------|---------------|--------|
| Click/Tap | Visual + optional haptic | Immediate (<100ms) |
| Form Submit | Loading state → Success/Error | Progressive |
| Background Process | Progress indicator | Continuous |
| Completion | Success state + next step | Immediate |
| Error | Inline message + solution | Immediate |

### Essential Micro-interactions

1. **Button States**
   - Default → Hover → Active → Loading → Success/Error

2. **Form Validation**
   - Inline validation as user types
   - Green checkmark for valid
   - Red with specific error message

3. **Loading States**
   - Skeleton screens > spinners
   - Progress bars for known durations
   - Optimistic UI when safe

4. **Success Confirmation**
   - Visual feedback (checkmark, animation)
   - Brief success message
   - Clear next action

### Micro-interaction Rules

- **Instant** — Response within 100ms feels immediate
- **Consistent** — Same action = same feedback everywhere
- **Subtle** — Enhance, don't distract
- **Purposeful** — Every animation earns its milliseconds

---

## 5. CTAs & Conversion

**Goal:** Make the desired action obvious and irresistible.

### CTA Hierarchy

```
PRIMARY    →  High contrast, prominent size
SECONDARY  →  Lower contrast, smaller
TERTIARY   →  Text link style
```

### CTA Copy Formula

```
[Action Verb] + [What They Get] + [Urgency/Benefit]

Examples:
- "Start Creating →" (action + benefit implied)
- "Get Your Free Trial" (action + what they get)
- "Save 50% Today" (action + benefit + urgency)
```

### High-Converting CTA Patterns

| Instead of... | Use... | Why |
|---------------|--------|-----|
| "Submit" | "Get Started" | Action-oriented |
| "Sign Up" | "Create Free Account" | Shows value |
| "Learn More" | "See How It Works" | Specific |
| "Buy Now" | "Start My Trial" | Lower friction |
| "Download" | "Get Your Copy" | Personal |

### CTA Placement Rules

1. **Above the fold** — Primary CTA always visible
2. **After value prop** — CTA follows benefit statement
3. **End of sections** — Catch scrollers with secondary CTAs
4. **Single focus** — One primary CTA per viewport

### Visual Design

- **Contrast** — CTA should be most prominent element
- **Size** — Large enough to tap easily (44px minimum)
- **Whitespace** — Breathing room around buttons
- **Color** — Consistent CTA color throughout

---

## 6. Anticipatory Design Patterns

**Goal:** Reduce decisions users need to make.

### Anticipatory Techniques

| Technique | Implementation |
|-----------|----------------|
| **Smart Defaults** | Pre-fill with most common choice |
| **Predictive Input** | Autocomplete, suggestions |
| **Contextual Actions** | Show relevant actions based on state |
| **Remember Preferences** | Persist user choices |
| **Proactive Notifications** | Alert before problems occur |

### Smart Default Examples

```javascript
// Date picker defaults to today
// Currency defaults to user's locale
// Quantity defaults to 1
// Toggle defaults to most common choice
```

### Reducing Decision Fatigue

1. **Limit choices** — 3-5 options max per decision
2. **Recommend one** — Highlight the best choice
3. **Group related** — Chunk options logically
4. **Progressive choices** — Reveal options in stages

---

## 7. Design Checklist

### Before Building

- [ ] What's the user's goal on this screen?
- [ ] What's the ONE action we want them to take?
- [ ] What's the minimum information needed?
- [ ] What questions might they have?

### Empty States

- [ ] First-use state designed and helpful?
- [ ] No-results state guides to success?
- [ ] Error states provide clear solutions?
- [ ] All states have a clear CTA?

### Onboarding

- [ ] Time to "Aha Moment" minimized?
- [ ] Can skip and return to onboarding?
- [ ] Progress clearly indicated?
- [ ] Each step provides immediate value?

### Interactions

- [ ] Every action has feedback?
- [ ] Loading states for async operations?
- [ ] Success/error states clear?
- [ ] Transitions smooth but fast?

### Conversion

- [ ] Primary CTA obvious and compelling?
- [ ] CTA copy is action-oriented?
- [ ] Friction points identified and reduced?
- [ ] Trust signals present?

---

## Process

1. **Map the Journey** — Identify every screen state
2. **Find the Aha Moment** — What creates user value?
3. **Clear the Path** — Remove friction to that moment
4. **Design Each State** — Empty, loading, success, error
5. **Add Delight** — Micro-interactions that surprise
6. **Test & Iterate** — Watch real users, adjust

## Questions to Ask

- What's the user trying to accomplish?
- What's the fastest path to value?
- What might confuse or block them?
- Where can we anticipate their needs?
- What would make this feel magical?
