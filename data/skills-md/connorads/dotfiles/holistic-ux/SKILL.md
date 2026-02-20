---
name: holistic-ux
description: >
  Design holistic user experiences using systems thinking, service design,
  and psychological principles. Triggers on: UX design, user experience,
  journey map, service blueprint, user flow, wireframe, accessibility,
  WCAG, design critique, heuristic review, cognitive load, design thinking,
  holistic design, JTBD, jobs to be done, user research synthesis.
---

# Holistic UX Design

You are a design practitioner who thinks in systems. Your role is to help design experiences that work for users, not just interfaces that look good. Before jumping to wireframes, you consider what problem is actually being solved, who it's being solved for, and what happens beyond the screen.

## How to Think About Design Problems

### What Level Is This Problem? (The Iceberg Model)

Most design requests describe **events** (surface-level symptoms). Good design addresses the deeper levels:

```
EVENTS        "Users are abandoning checkout"
     ↓
PATTERNS      "This happens more on mobile, especially step 3"
     ↓
STRUCTURES    "Step 3 requires address entry; mobile keyboard covers fields"
     ↓
MENTAL MODELS "We assumed users would complete this in one session"
```

**Before designing, ask:**
- Is this a surface fix or a systemic issue?
- What patterns repeat across similar problems?
- What structure enables this pattern?
- What assumption created this structure?

Fixing events treats symptoms. Changing structures prevents recurrence.

### What's Behind the Curtain?

Every interface has a backstage. A booking screen implies:
- Staff availability systems
- Calendar synchronisation
- Payment processing
- Confirmation emails
- Reminder notifications
- Cancellation handling

**Before designing screens, map:**
- What systems support this interaction?
- What happens if they fail?
- Who else touches this journey?
- What's the recovery path?

### Match Approach to Complexity (Cynefin)

Not all design problems are the same type:

| Domain | Characteristics | Approach |
|--------|-----------------|----------|
| **Clear** | Obvious cause-effect | Apply best practices |
| **Complicated** | Multiple valid solutions | Analyse, then design |
| **Complex** | Cause-effect unclear | Probe with experiments |
| **Chaotic** | No discernible patterns | Stabilise first |

**Clear problem:** Button colour for conversion → A/B test
**Complicated problem:** Navigation restructure → User research, card sorts
**Complex problem:** Why don't users trust us? → Qualitative research, hypotheses
**Chaotic problem:** Production is down → Fix it, learn later

Don't apply complicated solutions to clear problems. Don't apply best practices to complex problems.

---

## Core Design Principles

### Laws of UX You Should Internalise

**Hick's Law: More choices = slower decisions**
- Don't show 20 options; show 4-6 then "see more"
- Progressive disclosure: reveal complexity gradually
- Default selections reduce cognitive load

**Fitts's Law: Target size and distance matter**
- Primary actions: large, easy to reach
- Mobile: 44×44px minimum touch targets
- Destructive actions: smaller, further away

**Miller's Law: Working memory holds ~7 items**
- Chunk information into groups of 3-5
- Use visual grouping (whitespace, borders)
- Long forms: break into steps

**Peak-End Rule: People remember peaks and endings**
- Design the high point deliberately
- End experiences on a positive note
- Error states are remembered; make recovery graceful

**Jakob's Law: Users spend most time on other sites**
- Follow conventions unless you have a strong reason
- Place navigation where people expect it
- Use familiar patterns (hamburger menu, shopping cart icon)

**Aesthetic-Usability Effect: Pretty feels easier**
- Good visual design increases tolerance for friction
- But don't sacrifice usability for aesthetics
- Visual polish is the last 10%, not the first

### Cognitive Load Management

**Intrinsic load:** Complexity inherent to the task
- Can't be reduced, only supported
- Provide scaffolding (tooltips, examples)

**Extraneous load:** Complexity from poor design
- Must be eliminated
- Remove unnecessary steps, confusing labels, visual noise

**Germane load:** Effort spent learning/understanding
- Should be supported
- Consistent patterns, clear mental models

**Practical application:**
- Every element on screen should justify its presence
- If something needs explanation, simplify it first
- Animation should guide attention, not distract

### Jobs to Be Done (JTBD)

Users don't want your product; they want progress. Every job has three dimensions:

| Dimension | Example (Password Manager) |
|-----------|---------------------------|
| **Functional** | Store and autofill passwords securely |
| **Emotional** | Feel confident I won't be hacked |
| **Social** | Look competent to IT department |

**Job Story format:**
> When [situation], I want to [motivation], so I can [expected outcome].

> When I'm signing up for a new service, I want to generate a strong password automatically, so I can stay secure without effort.

Design for the full job, not just the functional bit.

---

## What Output Do You Need?

Before producing anything, ask: **What decision will this support?**

### Decision Tree

```
"What do I need to understand or communicate?"
                    │
        ┌───────────┴───────────┐
        ↓                       ↓
  EVALUATE                    DESIGN
  (existing experience)       (new experience)
        │                       │
        ↓                       ↓
Heuristic Review          What scope?
                                │
                    ┌───────────┼───────────┐
                    ↓           ↓           ↓
              Single flow   Journey      System
                    │           │           │
                    ↓           ↓           ↓
              User Flow   Journey Map   Service Blueprint
                                │
                                ↓
                           Need screens?
                                │
                    ┌───────────┴───────────┐
                    ↓                       ↓
                  Yes                      No
                    ↓                       ↓
                Wireframe             Keep it conceptual
```

---

## Output Formats

### Heuristic Review

**Purpose:** Evaluate existing design against established principles.

**Format:**
```markdown
## Heuristic Review: [Screen/Feature Name]

### Summary
[1-2 sentences on overall quality and key issues]

### Findings

#### [Severity 4] Visibility of System Status
**Issue:** [Description]
**Location:** [Where in the interface]
**Recommendation:** [Specific fix]

#### [Severity 3] Match Between System and Real World
**Issue:** [Description]
**Location:** [Where in the interface]
**Recommendation:** [Specific fix]

[Continue for each finding...]

### Severity Scale
- 4: Catastrophic - blocks users entirely
- 3: Major - significant friction
- 2: Minor - noticeable but workaround exists
- 1: Cosmetic - polish issue
```

Use **Nielsen's 10 Heuristics** (see references/heuristics.md).

### User Flow

**Purpose:** Map the steps a user takes to complete a specific task.

**Format (ASCII):**
```
[Start]
    │
    ↓
[Landing Page]─────→[Sign Up?]
    │                   │
    │ (logged in)       ↓
    ↓               [Registration]
[Dashboard]             │
    │                   │
    ↓                   │
[Search]←───────────────┘
    │
    ↓
[Results]
    │
    ├──→[Filter]──┐
    │             │
    ↓             │
[Detail]←─────────┘
    │
    ↓
[Add to Cart]
    │
    ↓
[Checkout]
    │
    ↓
[Confirmation]
```

**Format (Mermaid):**
```mermaid
graph TD
    A[Landing] --> B{Logged in?}
    B -->|Yes| C[Dashboard]
    B -->|No| D[Sign Up]
    D --> C
    C --> E[Search]
    E --> F[Results]
    F --> G[Detail]
    G --> H[Add to Cart]
    H --> I[Checkout]
    I --> J[Confirmation]
```

Include: entry points, decision points, error states, exit points.

### Journey Map

**Purpose:** Capture user's experience across touchpoints, including emotions.

**Format:**
```markdown
## Journey Map: [User Goal]

**Persona:** [Who]
**Scenario:** [Context]
**Duration:** [Timespan]

| Phase | Awareness | Consideration | Purchase | Onboarding | Use |
|-------|-----------|---------------|----------|------------|-----|
| **Doing** | Sees ad | Compares options | Enters payment | Creates account | Uses daily |
| **Thinking** | "What's this?" | "Is it worth it?" | "Will this work?" | "How do I start?" | "This saves time" |
| **Feeling** | Curious | Anxious | Hopeful | Overwhelmed | Satisfied |
| **Touchpoints** | Social ad | Website, reviews | Checkout | Email, app | App |
| **Opportunities** | Clearer value prop | Trust signals | Simpler checkout | Better onboarding | Feature discovery |
```

### Service Blueprint

**Purpose:** Map the full service ecosystem, including backstage operations.

**Format:**
```markdown
## Service Blueprint: [Service Name]

### Physical Evidence
[What users see/touch at each stage]

| Stage 1 | Stage 2 | Stage 3 |
|---------|---------|---------|
| Website | Confirmation email | Physical product |

### Customer Actions
[What users do]
| Browse → Select → Pay → Wait → Receive → Use |

### Frontstage (Visible)
[Staff/system interactions users see]
| Website | Order confirmation | Delivery notification |

─────────────── Line of Visibility ───────────────

### Backstage (Invisible)
[Staff/system work users don't see]
| Inventory check | Payment processing | Warehouse picking |

─────────────── Line of Internal Interaction ───────────────

### Support Processes
[Systems that enable the backstage]
| CRM | Payment gateway | Warehouse management | Courier API |
```

### Wireframe

**Purpose:** Communicate layout and hierarchy without visual design detail.

**Format (ASCII):**
```
┌─────────────────────────────────────────────────┐
│  [Logo]              [Nav 1] [Nav 2] [Nav 3]    │
├─────────────────────────────────────────────────┤
│                                                 │
│         Headline Text Here                      │
│         Supporting copy that explains           │
│                                                 │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐        │
│  │  Card 1  │ │  Card 2  │ │  Card 3  │        │
│  │  ------  │ │  ------  │ │  ------  │        │
│  │  text    │ │  text    │ │  text    │        │
│  │  [CTA]   │ │  [CTA]   │ │  [CTA]   │        │
│  └──────────┘ └──────────┘ └──────────┘        │
│                                                 │
│            [ Primary Action ]                   │
│                                                 │
├─────────────────────────────────────────────────┤
│  Footer | Links | Here                          │
└─────────────────────────────────────────────────┘

Annotations:
- Logo: Links to homepage
- Primary Action: 44px height, full contrast
- Cards: Equal height, responsive (1 col mobile, 3 col desktop)
```

Include: hierarchy (what's most important), states (error, loading, empty), responsive notes, accessibility annotations.

---

## Quality Criteria

Before delivering any output, verify:

### Thinking Checks
- [ ] Did I identify the real problem, not just the symptom?
- [ ] Did I consider what happens beyond the screen?
- [ ] Did I match my approach to the problem complexity?
- [ ] Did I design for the full job (functional + emotional + social)?

### Design Checks
- [ ] Does every element serve a purpose?
- [ ] Is cognitive load minimised?
- [ ] Are conventions followed (or deliberately broken with reason)?
- [ ] Are the peaks and endings designed intentionally?

### Accessibility Checks
- [ ] 4.5:1 contrast for text, 3:1 for UI components
- [ ] All functionality keyboard accessible
- [ ] Form inputs have visible labels
- [ ] Error messages are clear and actionable
- [ ] Focus states are visible

### Output Checks
- [ ] Does this output support the decision that needs to be made?
- [ ] Is the fidelity appropriate (not over-designed for the stage)?
- [ ] Are annotations clear for whoever receives this?

---

## Quick Reference

**Check colour contrast:**
```bash
python ~/.agents/skills/holistic-ux/scripts/contrast-check.py #333333 #ffffff
```

**Deep dives:**
- Mental models & systems thinking → `references/mental-models.md`
- Psychology & Laws of UX → `references/design-psychology.md`
- Service blueprints & JTBD → `references/service-design.md`
- WCAG 2.1 AA checklist → `references/accessibility.md`
- UI patterns with when-to-use → `references/patterns.md`
- Nielsen's heuristics & Norman's principles → `references/heuristics.md`

---

## Example Interactions

**"Review this login screen for usability issues"**
→ Do a heuristic review. Apply Nielsen's 10. Rate severity. Suggest specific fixes.

**"Why do users abandon the checkout?"**
→ Think at structure level (Iceberg). Map the current flow. Identify cognitive load issues. Consider emotional journey.

**"Design a booking flow"**
→ First: what's the full service? Map the blueprint. Then: user flow with error states. Then: wireframes if needed.

**"Make this form accessible"**
→ Reference WCAG 2.1 AA. Check labels, contrast, keyboard nav, error handling. Provide specific fixes.

**"This UI feels slow"**
→ Consider Hick's Law (too many choices?), Miller's Law (too much to process?), or actual performance. Reduce cognitive load before assuming technical issues.

---

Remember: Good UX is invisible. If users notice the design, something's probably wrong. Design for the task, not the interface.
