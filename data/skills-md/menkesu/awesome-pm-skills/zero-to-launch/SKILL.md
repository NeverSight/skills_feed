---
name: zero-to-launch
description: Guides Claude from idea to working prototype using frameworks from OpenAI, Figma, and Airbnb. Use when starting new product features, planning MVP scope, making build-vs-buy decisions, or guiding users from concept to shippable prototype. Applies AI-first thinking (Kevin Weil), simplicity forcing functions (Dylan Field), and complete experience design (Brian Chesky).
---

# Zero to Launch: Idea → Prototype Playbook

## When This Skill Activates

Claude uses this skill when:
- User asks to "build", "create", or "prototype" a new feature
- Starting from a product idea or user need
- Planning MVP or initial scope
- Making "what to build first" decisions
- Guiding from concept to code

## Core Frameworks

### 1. OpenAI's AI-First Product Development (Source: Kevin Weil, CPO of OpenAI)

**The Model Improvement Mindset:**
> "The AI models you're using today is the worst AI model you will ever use for the rest of your life. Every two months, computers can do something they've never been able to do before."

**Use when:** Building any product that could benefit from AI capabilities

**How:**
1. **Design for Future Models:** Build assuming models will get 10x better in 2 months
2. **Edge Cases Today = Core Cases Tomorrow:** If it barely works now, it'll sing soon
3. **Evals as Product Specs:** Write test cases that measure quality, not just functionality
4. **Hybrid Approach:** Combine AI + traditional code based on task suitability

**Example:**
```
User request: "Build a search feature"

Apply AI-First Thinking:
✅ Could AI understand intent better than keyword matching?
✅ Design for streaming results (models will get faster)
✅ Add eval: "Does search return relevant results for ambiguous queries?"
✅ Hybrid: Use AI for intent, traditional for exact matches
```

---

### 2. Figma's Simplicity Forcing Function (Source: Dylan Field, CEO of Figma)

**The Core Question:**
> "The hardest thing is saying no. We operationalize simplicity by constantly asking: What's the ONE thing that matters here?"

**Use when:** Feature scope is unclear or growing too large

**How:**
1. **Identify the Core Job:** What's the ONE outcome users need?
2. **Remove Until It Breaks:** Strip features until core value disappears
3. **Craft Quality Threshold:** Details matter when they create moats
4. **Progressive Disclosure:** Hide complexity, reveal when needed

**Example:**
```
User request: "Build a dashboard with 15 metrics"

Apply Simplicity Test:
❌ 15 metrics = paralysis
✅ What's the ONE metric that drives action?
✅ Show that metric prominently
✅ Hide other 14 behind "View Details"
✅ Polish the main metric display (craft quality)
```

---

### 3. Airbnb's Complete Experience Design (Source: Brian Chesky, CEO of Airbnb)

**The One Roadmap Philosophy:**
> "We shifted to one company roadmap. Leaders are in the details. If you don't know the details, how do you know people are doing a good job?"

**Use when:** Building features that touch multiple parts of the product

**How:**
1. **Design Complete Flow:** Map entire user journey before coding
2. **Consider All States:** Loading, error, empty, success states
3. **Cross-Functional From Start:** Design, eng, marketing together
4. **Story Over Features:** How would you talk about this to customers?

**Example:**
```
User request: "Build user onboarding"

Apply Complete Experience:
✅ Map full journey: Signup → Setup → First Value → Habit
✅ Design all states: Loading screens, errors, empty states
✅ Include: Welcome email, in-app guidance, success celebration
✅ Story: "Get your first [outcome] in under 2 minutes"
```

---

## Decision Tree: What to Build First

```
START: New Feature Idea
│
├─ Can AI 10x this? ─────────────────┐
│  YES: Apply AI-First Framework     │
│  NO: Continue                       ↓
│                                Use OpenAI Patterns
├─ What's the ONE core job? ─────────┤
│  Apply Simplicity Test              │
│  Define: Must-have vs nice-to-have  │
│                                     │
├─ Map complete experience ───────────┤
│  All states, full journey           │
│  Cross-functional considerations    │
│                                     │
└─ BUILD MVP ←───────────────────────┘
   Start with core job
   Add details that create moats
   Ship to small group first
```

## Action Templates

### Template 1: MVP Scope Definition

```markdown
# Feature: [Name]

## The ONE Job (Figma Simplicity Test)
What outcome must this deliver?
- Core job: [describe]
- Success = when user can [achieve outcome]

## AI-First Considerations (OpenAI Thinking)
- Could AI help? [yes/no + how]
- Designed for future models? [yes/no]
- Evals needed: [list test cases]

## Complete Experience (Airbnb Approach)
- User journey: [list steps]
- States to design: [loading, error, empty, success]
- Story to tell: "[how we'll talk about this]"

## MVP Scope
**Must Have (Week 1):**
- [feature]
- [feature]

**Should Have (Week 2):**
- [feature]

**Nice to Have (Later):**
- [feature]
```

### Template 2: Build Decision Framework

When deciding what to build:

| Question | Framework | Action |
|----------|-----------|--------|
| Is this AI-suitable? | OpenAI | Build with AI if: repetitive, pattern-matching, improves over time |
| What's essential? | Figma | Strip to ONE core job, build that first |
| Is experience complete? | Airbnb | Design all states before building any |
| Can we ship in 1 week? | All | If no, scope is too big - simplify |

## Quick Reference Card

### 🏗️ Zero to Launch Checklist

**Before You Code:**
- [ ] Defined the ONE core job (Figma Test)
- [ ] Considered AI-first approach (OpenAI Lens)
- [ ] Mapped complete user experience (Airbnb Standard)
- [ ] Identified must-have vs nice-to-have
- [ ] Designed all states (loading, error, empty, success)

**During Build:**
- [ ] Building for future model improvements (if AI)
- [ ] Maintaining simplicity (saying no to scope creep)
- [ ] Including cross-functional perspectives
- [ ] Crafting details that matter

**Before Ship:**
- [ ] Core job works end-to-end
- [ ] All states handled
- [ ] Story ready (how to talk about it)
- [ ] Ship to small group first

---

## Real-World Examples from Episodes

### Example 1: OpenAI's ChatGPT Features (Kevin Weil)

**Challenge:** Users wanted ChatGPT to remember context across conversations

**AI-First Approach:**
- Built knowing models would improve memory capabilities
- Started with basic context, designed for future sophistication
- Created evals: "Does it remember key facts across sessions?"
- Hybrid: Explicit memory + AI interpretation

**Result:** Feature that gets better as models improve

---

### Example 2: Figma's Feature Development (Dylan Field)

**Challenge:** Users requested 50+ features

**Simplicity Test Applied:**
- Asked: "What's the ONE thing designers need most?"
- Answer: Collaboration in real-time
- Shipped: Multiplayer editing (core job)
- Deferred: 45+ other requests

**Result:** Killer feature that defined the product

---

### Example 3: Airbnb's Product Redesign (Brian Chesky)

**Challenge:** Rebuilding entire product experience

**Complete Experience Approach:**
- One roadmap across all teams
- Designed full booking journey before building any piece
- Every feature needed a story (how to talk about it)
- Leaders stayed in design details

**Result:** Coherent product, not disconnected features

---

## Common Pitfalls to Avoid

### ❌ Mistake 1: Building Without the AI Lens
**Problem:** Missing 10x opportunities by defaulting to traditional approaches
**Fix:** Always ask: "Could AI make this 10x better?"

### ❌ Mistake 2: Scope Creep
**Problem:** "Just one more feature" → bloated MVP that never ships
**Fix:** Ruthlessly apply Figma simplicity test - ONE core job

### ❌ Mistake 3: Incomplete States
**Problem:** Shipping without error/empty/loading states
**Fix:** Use Airbnb complete experience checklist

### ❌ Mistake 4: Feature Factory Mentality
**Problem:** Building what's requested vs solving jobs
**Fix:** Start with user job, not feature request

---

## Related Skills

- **strategic-build** - For deciding if this is strategic vs tactical work
- **design-first-dev** - For detailed craft and quality standards
- **ai-product-patterns** - For deep AI implementation patterns
- **ship-decisions** - For when to ship vs iterate more
- **jtbd-building** - For understanding underlying user jobs

---

## Key Quotes from Episodes

**Kevin Weil (OpenAI):**
> "Our general mindset is in two months, there's going to be a better model. If you're building and the product is right on the edge of capabilities, keep going. You're doing something right."

**Dylan Field (Figma):**
> "AI makes design, craft, and quality the new moat for startups. The bar for quality is going to go way up."

**Brian Chesky (Airbnb):**
> "Way too many founders apologize for how they want to run the company. What everyone really wants is clarity and to row in the same direction."

---

## Further Learning

For deeper dives on specific topics, see:
- **references/kevin-weil-openai.md** - Full AI-first product philosophy
- **references/dylan-field-figma.md** - Simplicity and craft standards
- **references/brian-chesky-airbnb.md** - Complete experience design methodology

