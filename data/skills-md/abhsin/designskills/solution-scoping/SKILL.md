---
name: solution-scoping
description: Prioritize features and define MVP boundaries based on problem framing and user models. Use when a user has validated their problem and understands their users but needs to decide what to build first. Outputs feature priorities, MVP scope, and explicit cuts that feed into PRD generation.
---

# Solution Scoping

Decide what to build first—and what to cut.

## Why This Exists

Forces hard prioritization decisions before development starts, when cutting features is cheap.

## Input Requirements

This skill works best with:
- `problem-framing` output (problem statement, JTBD, assumptions)
- `user-modeling` output (personas, scenarios, insights)

Can also work with a raw feature list if the user has one.

## Workflow

### Step 1: Gather Context

Ingest upstream artifacts or ask:
- What problem are you solving?
- Who are you solving it for?
- What features are you considering?
- Any constraints—time, budget, skills?

### Step 2: Generate Feature List

If not provided, brainstorm features based on:
- User jobs-to-be-done
- Persona pain points
- Scenarios from user modeling
- Competitor features (if known)

Keep it exhaustive initially—we'll cut later.

### Step 3: Apply Prioritization

Use one or more frameworks to force ranking:

**Impact vs Effort Matrix**
- High impact, low effort → Do first
- High impact, high effort → Plan carefully
- Low impact, low effort → Maybe later
- Low impact, high effort → Cut

**MoSCoW Method**
- Must have — Product doesn't work without it
- Should have — Important but not critical
- Could have — Nice to have
- Won't have — Explicitly out

**User Value Filter**
For each feature, ask:
- Does it solve the core problem?
- Which persona needs it most?
- What happens if we ship without it?

### Step 4: Define MVP Boundary

Draw a hard line:
- What's in the first release?
- What's deferred to v1.1?
- What's cut entirely?

The MVP should be the *smallest thing that tests your core assumption*.

### Step 5: Validate Cuts

For each cut, confirm:
- Can the product still solve the core problem?
- Will users still get value?
- Are we cutting for good reasons or fear?

## Output Format

**Automatically save the output to `design/04-solution-scoping.md` using the Write tool** while presenting it to the user.

```markdown
# Solution Scoping: [Project Name]

## Context
[Brief summary of the problem and target user]

**Core assumption to test:**
[The main bet this MVP validates]

**Constraints:**
- Timeline: [If any]
- Budget: [If any]
- Skills: [Technical limitations]
- Other: [Platform, dependencies, etc.]

---

## Feature Inventory

### All Considered Features
| # | Feature | User Value | Effort | Notes |
|---|---------|------------|--------|-------|
| 1 | [Feature] | [High/Med/Low] | [High/Med/Low] | [Context] |
| 2 | [Feature] | [High/Med/Low] | [High/Med/Low] | [Context] |
| 3 | [Feature] | [High/Med/Low] | [High/Med/Low] | [Context] |
| 4 | [Feature] | [High/Med/Low] | [High/Med/Low] | [Context] |
| 5 | [Feature] | [High/Med/Low] | [High/Med/Low] | [Context] |

---

## Prioritization

### Must Have (MVP)
*Product doesn't work without these*

| Feature | Rationale |
|---------|-----------|
| [Feature] | [Why it's essential] |
| [Feature] | [Why it's essential] |
| [Feature] | [Why it's essential] |

### Should Have (v1.1)
*Important, but MVP can ship without them*

| Feature | Rationale | Dependency |
|---------|-----------|------------|
| [Feature] | [Why it's important] | [What it needs first] |
| [Feature] | [Why it's important] | [What it needs first] |

### Could Have (Future)
*Nice to have, low priority*

| Feature | Rationale |
|---------|-----------|
| [Feature] | [Why it's deferred] |
| [Feature] | [Why it's deferred] |

### Won't Have (Cut)
*Explicitly out of scope*

| Feature | Reason for Cut |
|---------|----------------|
| [Feature] | [Why we're not building this] |
| [Feature] | [Why we're not building this] |

---

## MVP Definition

### What We're Building
[2-3 sentence description of the MVP]

### Core User Flow
[The one primary flow the MVP enables]
1. User [action]
2. System [response]
3. User [achieves goal]

### What Success Looks Like
- [Metric or outcome 1]
- [Metric or outcome 2]

### What We're NOT Building (Yet)
- [Explicit cut 1]
- [Explicit cut 2]
- [Explicit cut 3]

---

## Risk Check

### Cuts That Might Hurt
| Cut | Risk | Mitigation |
|-----|------|------------|
| [Feature we cut] | [What could go wrong] | [How we'll handle it] |

### Scope Creep Triggers
*Watch out for these during development*
- [Temptation 1]
- [Temptation 2]

---

## Open Questions
- [Decision still needed]
- [Assumption to validate before committing]
```

## Prioritization Tips

**When everything feels "Must Have":**
- Ask: "Would users pay for this feature alone?"
- Ask: "Can users accomplish their goal without it?"
- Ask: "What's the workaround if we don't build it?"

**When you can't decide:**
- Default to smaller scope
- Ship, learn, then add
- A shipped MVP beats a perfect spec

**When stakeholders push back on cuts:**
- Frame as "not yet" not "never"
- Show the dependency chain
- Remind: we can add, but we can't un-ship

## Anti-Patterns to Avoid

- **The Feature Buffet** — "Let's just add one more thing"
- **The Safety Blanket** — Keeping features because cutting feels scary
- **The Competitor Copy** — Including features just because others have them
- **The Premature Scale** — Building for 10,000 users when you have 10

## Handoff

After presenting the scoped MVP, ask:
> "Ready to generate the PRD with `/prd-generation`, or want to adjust priorities first?"

**Note:** File is automatically saved to `design/04-solution-scoping.md`. This feeds into PRD generation (Must Have → MVP features, Should Have → v1.1 roadmap, Won't Have → Out of Scope).