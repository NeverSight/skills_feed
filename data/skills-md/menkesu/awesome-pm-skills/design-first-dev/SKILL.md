---
name: design-first-dev
description: Follows Airbnb's design-led development and Figma's craft quality standards. Use when building user-facing features, making UI/UX decisions, determining when details matter, or applying design system thinking. Guides when to move fast vs when quality creates moats. Based on Brian Chesky staying in every design detail and Dylan Field's craft philosophy.
---

# Design-Led Development: Craft Quality Standards

## When This Skill Activates

Claude uses this skill when:
- Building user-facing features or interfaces
- Making UI/UX decisions
- Deciding between quick prototype vs polished experience
- Creating onboarding, core flows, or key moments
- Determining if "details matter" for this feature

## Core Frameworks

### 1. Airbnb's Design-Led Process (Source: Brian Chesky, CEO of Airbnb)

**Leaders in the Details:**
> "There's a difference between micromanagement and being in the details. If you don't know the details, how do you know people are doing a good job? I made sure I was in the details."

**The Approach:**

**🎨 Design Complete Flow First**
- Prototype full experience before writing code
- Show, don't tell (working prototype > requirements doc)
- Get design right, then build it right
- Every feature needs a story (how you'll talk about it)

**All States Matter:**
- Loading states (what user sees while waiting)
- Error states (graceful failures)
- Empty states (first-time user experience)
- Success states (celebrations, confirmations)

**Cross-Functional from Day 1:**
- Design, engineering, marketing together
- Not sequential (design → eng → marketing)
- Concurrent: everyone contributes to the prototype

**How to Apply:**
```
DON'T:
- Write code first, design later
- "We'll polish it after we ship"
- Design only happy path

DO:
- Design complete experience (all states)
- Prototype before building
- Include cross-functional input early
- Craft the details that users notice
```

**Example:**
```
Feature: "User onboarding flow"

Design-First Approach:
✅ Prototype full flow in Figma/code sandbox
✅ Include:
   - Welcome screen (first impression)
   - Loading states (fetching user data)
   - Empty state (no content yet)
   - Error state (setup failed)
   - Success state (celebration!)
   - First value moment (aha!)
✅ Show to team before building backend
✅ Iterate on prototype, then build
```

---

### 2. Figma's Craft Quality Philosophy (Source: Dylan Field, CEO of Figma)

**AI Makes Craft the Moat:**
> "AI makes design, craft, and quality the new moat for startups. The bar for quality is going way up. Craft quality is how you differentiate."

**When Details Matter:**

**🎯 Details Create Moats When:**
1. **Core Product Experience** - The main value loop
2. **First Impressions** - Onboarding, landing pages, signup
3. **Frequent Use** - Features used daily
4. **Brand Differentiation** - What makes you unique
5. **Competitive Advantage** - Where quality = conversion

**Move Fast When:**
1. **Internal Tools** - Team-facing, not customer-facing
2. **Experiments** - Testing hypotheses quickly
3. **Non-Core Features** - Support features, admin panels
4. **Behind the Scenes** - Logging, monitoring, ops

**How to Apply:**
```
Ask: "Does craft quality matter here?"

HIGH CRAFT (polish details):
- User-facing core flows
- Onboarding experiences
- Key conversion moments
- Brand touchpoints
- Competitive differentiators

LOW CRAFT (move fast):
- Internal dashboards
- Admin panels
- Quick experiments
- Support tooling
- Behind-the-scenes
```

**Craft Quality Checklist:**
- [ ] Consistent spacing (8px grid)
- [ ] Proper hierarchy (typography scale)
- [ ] Smooth interactions (animations, transitions)
- [ ] Responsive (works on all screen sizes)
- [ ] Accessible (keyboard nav, screen readers)
- [ ] Loading states (skeleton screens, spinners)
- [ ] Error handling (helpful messages)
- [ ] Empty states (guide to first value)

---

### 3. The One Roadmap Principle (Source: Brian Chesky)

**Coherent Product, Not Feature Salad:**
> "We shifted to one company roadmap. This meant we could have a coherent story. Every feature connects to a narrative."

**Product Coherence:**

**🎭 The Story Test:**
- Can you tell a story about how all features connect?
- Would a customer understand the vision?
- Is this additive to the narrative or distracting?

**How to Apply:**
```
Before building any feature:
1. How does this fit the product story?
2. Does this reinforce the core value prop?
3. Will users understand why this exists?
4. Can we talk about this in one coherent launch?

BAD: Random feature that "users requested"
GOOD: Feature that advances the product narrative
```

**Example:**
```
Product: "Project management tool"
Story: "See everything, finish anything"

Feature Ideas:
✅ Timeline view (fits story: "see everything")
✅ Task dependencies (fits story: "finish anything")
❌ Chat feature (distracts from story)
❌ Time tracking (doesn't reinforce core value)

Coherence test: Do new features strengthen the story?
```

---

### 4. Design System Thinking

**Build Once, Use Everywhere:**

**When to Invest in Design System:**
- [ ] Building 3+ similar components
- [ ] Multiple teams/products need consistency
- [ ] Brand consistency is important
- [ ] Onboarding new designers/engineers

**Design System Basics:**
```
FOUNDATIONS:
- Colors (primary, secondary, grays, feedback)
- Typography (scale, weights, line heights)
- Spacing (8px grid: 4, 8, 16, 24, 32, 48, 64)
- Radius (corners: 4, 8, 16)
- Shadows (elevation levels)

COMPONENTS:
- Buttons (primary, secondary, ghost)
- Inputs (text, select, checkbox, radio)
- Cards, Modals, Tooltips
- Navigation patterns
- Feedback (alerts, toasts, loading)

PATTERNS:
- Forms (layout, validation, submission)
- Tables (sorting, filtering, pagination)
- Empty states, Error states, Loading states
```

---

## Decision Tree: When to Polish vs Ship

```
FEATURE: [Ready to build]
│
├─ Is this user-facing? ───────────────┐
│  YES (customer sees it) ─────────────┤
│  NO (internal) ──────────────→ MOVE FAST
│
├─ Is this core product experience? ───┤
│  YES (main value loop) ──────→ HIGH CRAFT
│  NO (supporting feature) ────────────┤
│
├─ Is this first impression? ──────────┤
│  YES (onboarding, signup) ───→ HIGH CRAFT
│  NO (later in journey) ───────────────┤
│
├─ Used frequently? ────────────────────┤
│  YES (daily/weekly) ──────────→ HIGH CRAFT
│  NO (occasionally) ───────────────────┤
│
├─ Competitive differentiator? ────────┤
│  YES (unique to us) ───────────→ HIGH CRAFT
│  NO (table stakes) ───────────→ GOOD ENOUGH
│
└─ DECISION ←──────────────────────────┘
```

## Action Templates

### Template 1: Design-First Feature Spec

```markdown
# Feature: [Name]

## The Story
How this fits the product narrative:
- Connection to core value: [explain]
- User story: "[how we'll talk about this]"

## Design-First Approach

### 1. Prototype First
- [ ] Full flow designed (not just happy path)
- [ ] All states included (loading, error, empty, success)
- [ ] Prototype reviewed with team
- [ ] Clickable demo ready

### 2. States to Design
- [ ] **Loading:** [what users see while waiting]
- [ ] **Error:** [graceful failure + recovery]
- [ ] **Empty:** [first-time experience + guidance]
- [ ] **Success:** [confirmation + next steps]

### 3. Craft Quality Bar
**This feature is:** [core product / supporting / internal]
**Craft level:** [high / medium / low]

**If HIGH craft:**
- [ ] Consistent spacing (8px grid)
- [ ] Typography hierarchy clear
- [ ] Smooth interactions
- [ ] Responsive design
- [ ] Accessible
- [ ] Delight moments

### 4. Cross-Functional Input
- [ ] Design reviewed
- [ ] Engineering reviewed (feasibility)
- [ ] Marketing input (how to talk about it)
- [ ] Product narrative alignment
```

### Template 2: State Design Checklist

For every user-facing feature:

| State | Question | Designed? |
|-------|----------|-----------|
| **Loading** | What does user see while fetching data? | [ ] |
| **Error** | What if API fails? Network error? | [ ] |
| **Empty** | What if user has no data yet? | [ ] |
| **Success** | How do we confirm action completed? | [ ] |
| **First Use** | What does new user see? | [ ] |
| **Partial** | What if data is incomplete? | [ ] |

### Template 3: Craft Quality Assessment

```markdown
# Feature: [Name]

## Craft Quality Decision

### Context
- User-facing: [yes/no]
- Core product loop: [yes/no]
- First impression: [yes/no]
- Usage frequency: [daily/weekly/monthly/rarely]
- Competitive differentiator: [yes/no]

### Craft Level: [HIGH / MEDIUM / LOW]

**If HIGH Craft:**
- Investment: [X days for polish]
- Focus areas: [list what makes it special]
- Success: [what "great" looks like]

**If LOW Craft:**
- Ship threshold: [works, looks okay]
- Time budget: [X days max]
- Polish later: [yes/no]
```

## Quick Reference Card

### 🎨 Design-First Checklist

**Before You Code:**
- [ ] Prototype complete experience (not just happy path)
- [ ] All states designed (loading, error, empty, success)
- [ ] Craft level determined (high/medium/low)
- [ ] Fits product narrative (story test passed)
- [ ] Cross-functional input gathered

**During Build:**
- [ ] Building what was designed (no "I'll fix it later")
- [ ] Maintaining craft standards if high-craft feature
- [ ] Using design system components
- [ ] Testing all states work

**Before Ship:**
- [ ] All states implemented
- [ ] Craft quality matches requirements
- [ ] Responsive on all devices
- [ ] Accessible
- [ ] Story ready (how to talk about it)

---

## Real-World Examples

### Example 1: Airbnb's Product Redesign (Brian Chesky)

**Challenge:** Rebuild entire product to be more coherent

**Design-First Approach:**
- Created one company roadmap (not 50 team roadmaps)
- Designed full experience before building any piece
- Brian stayed in every design detail
- Every feature had to fit the narrative

**Result:**
- Coherent product launch
- Clear story customers understood
- Features that reinforced each other

---

### Example 2: Figma's Core Canvas (Dylan Field)

**Decision:** Craft quality on core editing experience

**High Craft Investment:**
- 60fps canvas rendering (smooth = moat)
- Pixel-perfect precision
- Multiplayer cursors (delight moment)
- Keyboard shortcuts (pro user love)

**Result:**
- Best-in-class editing experience
- Users switch from competitors for "feel"
- Craft quality = competitive advantage

---

### Example 3: Stripe's Developer Experience

**Decision:** Polish docs and onboarding

**Design-First:**
- Designed empty state (first API call)
- Created guided tutorials
- Perfected error messages
- Made docs beautiful

**Result:**
- Fastest developer onboarding in payments
- Design quality = trust signal
- Higher conversion from trial to paid

---

## Common Pitfalls

### ❌ Mistake 1: Polish Everything
**Problem:** Treating internal tools like customer-facing products
**Fix:** Reserve high craft for features where quality = moat

### ❌ Mistake 2: Ship Happy Path Only
**Problem:** Forgot loading/error/empty states
**Fix:** Design all states before building any

### ❌ Mistake 3: Design After Building
**Problem:** "We'll polish it later" (never happens)
**Fix:** Prototype first, build second

### ❌ Mistake 4: Feature Salad
**Problem:** Adding features that don't fit narrative
**Fix:** Story test - does this strengthen core message?

---

## Related Skills

- **zero-to-launch** - For MVP scoping with design lens
- **quality-speed** - For deciding when to polish vs ship
- **strategic-build** - For knowing if this is high-leverage work
- **ai-product-patterns** - For AI-specific UX patterns

---

## Key Quotes

**Brian Chesky:**
> "Leaders are in the details. The question isn't whether to be in the details, but which details matter."

**Dylan Field:**
> "With AI, everyone can build. The differentiator is craft. Quality is the new moat."

**Brian on Coherence:**
> "You can have 50 marketing efforts but no customer heard anything. That's because there's no coherent story."

---

## Further Learning

- **references/airbnb-design-process.md** - Full design-led methodology
- **references/figma-craft-standards.md** - Craft quality patterns
- **references/design-system-starter.md** - Quick start guide
- **references/all-states-examples.md** - Loading, error, empty, success patterns

