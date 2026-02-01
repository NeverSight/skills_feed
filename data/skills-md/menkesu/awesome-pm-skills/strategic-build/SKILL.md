---
name: strategic-build
description: Distinguishes strategic vs tactical work during development using Shreyas Doshi's frameworks and Marty Cagan's empowered teams principles. Use when making architectural decisions, choosing what to build, preventing "product theater", or applying the LNO framework (Leverage, Neutral, Overhead). Helps avoid feature factory and build work that compounds.
---

# Strategic Prototyping: Build What Matters

## When This Skill Activates

Claude uses this skill when:
- User asks "should I build this?" or "is this worth it?"
- Making architectural decisions (reusable component, abstraction, etc.)
- Evaluating feature requests
- Distinguishing busy-work from high-impact work
- Preventing premature optimization or "product theater"

## Core Frameworks

### 1. The LNO Framework (Source: Shreyas Doshi, ex-Stripe/Twitter/Google PM)

**Leverage, Neutral, Overhead:**
> "Not all tasks are created equal. Some tasks compound (Leverage), some maintain (Neutral), and some drain without return (Overhead)."

**Use when:** Prioritizing what to build or evaluating if work is strategic

**The Three Categories:**

**🚀 Leverage Work (10x multipliers)**
- Compounds over time
- Enables future work
- Used repeatedly
- *Examples:* Design systems, core infrastructure, strategic features

**➡️ Neutral Work (1x necessary)**
- Maintains current state
- Necessary but doesn't compound
- One-time impact
- *Examples:* Bug fixes, minor UX tweaks, maintenance

**⚓ Overhead Work (0x drain)**
- Busy-work that doesn't move needle
- "Product theater" - looks like PM work but isn't
- Process for process's sake
- *Examples:* Excessive docs, meetings about meetings, vanity features

**How to Apply:**
```
For any work request, ask:
1. Will this be used 10+ times? (Leverage candidate)
2. Does this unblock future work? (Leverage candidate)
3. Is this maintaining vs building? (Likely Neutral)
4. Is this just "looking busy"? (Overhead - avoid)

BUILD: Leverage > Neutral > Overhead
RATIO: Aim for 70% Leverage, 20% Neutral, 10% Overhead max
```

**Example:**
```
Request: "Make this component reusable across the app"

LNO Analysis:
- Will we reuse it 10+ times? 
  YES → Leverage work, do it
  NO (only 2-3 uses) → Neutral/Overhead, build specific first

- Does it unblock future teams?
  YES → Leverage (design system contribution)
  NO → Wait until 3rd use case, then refactor
```

---

### 2. The Three Levels of Product Work (Source: Shreyas Doshi)

**Impact, Execution, Optics:**
> "Most execution problems are actually strategy problems. Most failed launches had unclear strategy, not bad execution."

**The Hierarchy:**

**Level 1: IMPACT (Why)**
- What outcome matters?
- Why does this move the business?
- What problem are we solving?
- **Failure mode:** Building without clear success criteria

**Level 2: EXECUTION (How)**
- How do we build this well?
- Technical decisions
- Quality standards
- **Failure mode:** Great execution on wrong problem

**Level 3: OPTICS (Perception)**
- How does this look to stakeholders?
- Updating status, demos, comms
- **Failure mode:** Theater - looks good but no impact

**Critical Insight:**
> "Teams often confuse Level 2 (execution) for Level 1 (impact). You ship fast but to nowhere. Always validate Level 1 before optimizing Level 2."

**How to Apply:**
```
Before building anything:
1. Level 1: What's the outcome? (Impact)
   - Define success metric
   - Know why this matters
   
2. Level 2: How to build it? (Execution)
   - Technical approach
   - Quality bar
   
3. Level 3: How to communicate? (Optics)
   - Stakeholder updates
   - Launch narrative

Most teams skip Level 1 and jump to Level 2.
```

---

### 3. Pre-Mortems for Strategic Decisions (Source: Shreyas Doshi)

**Imagine Failure Before Building:**
> "Six months from now, this failed completely. Why did it fail?"

**Use when:** Making big architectural decisions or starting major features

**How:**
1. **Assume Failure:** Imagine it's 6 months later, project failed
2. **Work Backwards:** List all reasons it could have failed
3. **Address Top Risks:** Mitigate the most likely failure modes
4. **Decide:** Build with eyes open or don't build at all

**Example:**
```
Feature: "Build AI-powered recommendations"

Pre-Mortem (Imagine it failed):
- Model wasn't accurate enough (users ignored recommendations)
- Too slow (users left before results loaded)
- Cold start problem (no data for new users)
- Team underestimated ML expertise needed

Mitigations:
✅ Start with hybrid: AI + rule-based fallback
✅ Set latency budget: <500ms or use cached results
✅ Plan cold start: Popular items + collaborative filtering
✅ Hire ML advisor or partner with ML team
```

---

### 4. Empowered vs Feature Teams (Source: Marty Cagan)

**Product Theater Warning:**
> "Too many companies overhired. Product owners, product ops, agile coaches - dramatically overpaid for value they provide. It's project management, not product management."

**Feature Team (Avoid This):**
- Given features to build
- Success = shipped on time
- PM is project manager
- **Result:** Feature factory, no ownership

**Empowered Team (Aim for This):**
- Given problems to solve
- Success = business outcome
- PM discovers solutions
- **Result:** Innovation, ownership

**How to Identify:**
```
Feature Team Signs:
❌ "We need to ship X by Q2"
❌ Roadmap is list of features
❌ Success = velocity, not outcomes
❌ PM writes tickets, not strategies

Empowered Team Signs:
✅ "We need to increase retention by 20%"
✅ Roadmap is list of outcomes
✅ Success = metrics moved
✅ PM discovers solutions
```

**Action:**
If you're in a feature team, shift your framing:
- Feature request → User problem
- Ship date → Outcome timeline
- Velocity → Impact

---

## Decision Tree: Strategic vs Tactical

```
DECISION: Should I build this?
│
├─ LNO Check ──────────────────────────┐
│  Is this Leverage work? ──YES──────→ PRIORITIZE
│  Is this Overhead? ───YES──────────→ SKIP
│  Is this Neutral? ────YES──────────↓
│
├─ Three Levels Check ─────────────────┤
│  Clear Level 1 (Impact)? ──NO──────→ PAUSE & DEFINE
│  Clear Level 2 (How)? ─────YES─────↓
│
├─ Pre-Mortem ─────────────────────────┤
│  Top failure risks mitigated? NO───→ REDESIGN
│  Confident in approach? ────YES────↓
│
├─ Feature vs Empowered ───────────────┤
│  Solving problem or building feature?
│  Problem-focused ──────────────────→ BUILD
│  Feature-focused ──────────────────→ REFRAME AS PROBLEM
│
└─ BUILD WITH STRATEGY ←──────────────┘
```

## Action Templates

### Template 1: LNO Assessment

```markdown
# Work Item: [Name]

## LNO Classification
- [ ] **Leverage** - Compounds over time, enables future work
- [ ] **Neutral** - Maintains, necessary but doesn't compound
- [ ] **Overhead** - Busy-work, no meaningful impact

## Evidence
- Times this will be used: [number]
- Future work it enables: [list]
- Business impact if skipped: [high/medium/low]

## Decision
- Priority: [High/Medium/Low]
- Rationale: [explain using LNO framework]
```

### Template 2: Three Levels Check

```markdown
# Feature: [Name]

## Level 1: IMPACT (Why)
- Problem we're solving: [describe]
- Success metric: [specific number]
- Business outcome: [revenue/retention/acquisition/etc.]
- **✓ Clear?** [yes/no - if no, stop and define]

## Level 2: EXECUTION (How)
- Technical approach: [describe]
- Quality bar: [standards]
- Timeline: [estimate]
- **Only proceed if Level 1 is clear**

## Level 3: OPTICS (Communication)
- Stakeholders: [list]
- Update cadence: [frequency]
- Launch story: [how we'll talk about it]
```

### Template 3: Pre-Mortem

```markdown
# Pre-Mortem: [Feature Name]

**Scenario:** It's 6 months from now. This completely failed.

## Why It Failed (Brainstorm)
1. [failure reason]
2. [failure reason]
3. [failure reason]
4. [failure reason]
5. [failure reason]

## Top 3 Risks
1. **Risk:** [most likely failure]
   **Mitigation:** [how to prevent]

2. **Risk:** [second most likely]
   **Mitigation:** [how to prevent]

3. **Risk:** [third most likely]
   **Mitigation:** [how to prevent]

## Go/No-Go Decision
- [ ] Risks acceptable and mitigated
- [ ] Still believe in the approach
- [ ] **Decision:** [Build / Redesign / Skip]
```

## Quick Reference Card

### 🎯 Strategic Build Checklist

**Before Committing:**
- [ ] Classified as Leverage/Neutral/Overhead (LNO)
- [ ] If not Leverage, questioning if worth building
- [ ] Level 1 (Impact) crystal clear
- [ ] Success metric defined
- [ ] Pre-mortem completed
- [ ] Top risks mitigated

**During Build:**
- [ ] Avoiding "product theater" - building real value
- [ ] Focusing on outcomes, not just output
- [ ] Making decisions with strategy in mind
- [ ] Building for reuse only when justified (3+ use cases)

**Red Flags (Stop & Reassess):**
- [ ] Can't articulate the "why" (Level 1 unclear)
- [ ] Building because "stakeholder wants it"
- [ ] No clear success metric
- [ ] Feels like busy-work

---

## Real-World Examples

### Example 1: Stripe's API Design (Shreyas Doshi at Stripe)

**Challenge:** Should we build this new API endpoint?

**LNO Analysis:**
- Used by 1000+ developers → Leverage
- Enables ecosystem growth → High leverage
- Alternative: Developers build workarounds → Tech debt

**Decision:** Build (high Leverage work)

---

### Example 2: Feature Factory Trap (Marty Cagan)

**Challenge:** Product team shipping fast but metrics flat

**Diagnosis:** Feature Team, not Empowered Team
- Roadmap = list of features
- PM = project manager
- No ownership of outcomes

**Fix:**
- Shifted to outcome-based roadmap
- PM discovers solutions, not just builds features
- Measured impact, not velocity

**Result:** Fewer features, better outcomes

---

### Example 3: Premature Abstraction

**Request:** "Make this component super reusable"

**LNO Assessment:**
- Currently used: 2 times
- Abstraction adds complexity
- Not clear if we'll need it again

**Decision:** Build specific, wait for 3rd use case
- First 2 uses: Copy-paste (acceptable tech debt)
- 3rd use: Refactor into shared component (data-driven)

---

## Common Pitfalls

### ❌ Mistake 1: Optimizing Execution Without Strategy
**Problem:** Building fast but in wrong direction
**Fix:** Always validate Level 1 (Impact) before Level 2 (Execution)

### ❌ Mistake 2: Overhead Disguised as Work
**Problem:** Updating stakeholders, writing docs, tweaking process
**Fix:** Audit your week - what % was Leverage vs Overhead?

### ❌ Mistake 3: Building for "Someday"
**Problem:** "We might need this later" → premature abstraction
**Fix:** YAGNI (You Aren't Gonna Need It) - build when needed

### ❌ Mistake 4: Feature Team Mentality
**Problem:** Success = shipped, not impact
**Fix:** Reframe every feature as a problem to solve

---

## Related Skills

- **zero-to-launch** - For scoping MVP strategically
- **decision-frameworks** - For structured decision-making
- **prioritization-craft** - For choosing between options
- **strategic-pm** - For moving from tactical to strategic thinking
- **ship-decisions** - For when to ship vs iterate

---

## Key Quotes

**Shreyas Doshi:**
> "The hardest thing about product management isn't the frameworks - it's distinguishing Leverage work from Overhead disguised as work."

**Marty Cagan:**
> "If you're just delivering output, you're a project manager. Product managers deliver outcomes."

**Shreyas on Pre-Mortems:**
> "Most teams do post-mortems when it's too late. Do pre-mortems when you can still change course."

---

## Further Learning

- **references/shreyas-doshi-frameworks.md** - Deep dive on LNO and Three Levels
- **references/marty-cagan-empowered.md** - Feature teams vs empowered teams
- **references/strategic-vs-tactical.md** - Case studies and examples

