---
name: user-modeling
description: Create lightweight user personas and usage scenarios from problem framing or raw research. Use when a user needs to clarify who they're building for beyond a basic target user description. Outputs practical personas and scenarios that inform feature priorities and UX decisions—not marketing fluff.
---

# User Modeling

Build just enough understanding of your users to make better product decisions.

## Why This Exists

Creates behavior-based user models that reveal what users need and how they'll behave, not marketing personas with stock photos.

## Input Requirements

This skill works best with:
- `problem-framing` output (problem statement, target user, JTBD)
- Any existing research (interviews, surveys, support tickets, Reddit threads, reviews)

Can also work from assumptions if no research exists—but flags that these need validation.

## Workflow

### Step 1: Gather Context

Ingest upstream artifacts or ask:
- Who are you building this for?
- What do you know about them already?
- Have you talked to any potential users?
- Any data sources—reviews, forums, support tickets?

### Step 2: Identify User Segments

Look for meaningful differences in:
- **Goals** — What are they trying to accomplish?
- **Context** — When/where do they encounter the problem?
- **Constraints** — What limits their options?
- **Skill level** — How sophisticated are they?
- **Frequency** — How often do they face this problem?

Not every difference matters. Focus on differences that change *what you'd build*.

### Step 3: Build Personas

For each meaningful segment, create a lightweight persona. Limit to 2-3 personas max—more than that dilutes focus.

### Step 4: Define Scenarios

For each persona, define 2-3 concrete scenarios where they'd use the product. These become the basis for user stories and flows.

### Step 5: Identify Insights

Surface patterns that inform product decisions:
- What do all personas have in common?
- Where do they diverge?
- What would you build differently for each?

**Automatically save the output to `design/02-user-modeling.md` using the Write tool** while presenting it to the user.

## Output Format

```markdown
# User Modeling: [Project Name]

## Context
[Brief summary of the problem space and what we know]

**Research basis:**
- [Source 1: what it told us]
- [Source 2: what it told us]
- [Or: "Based on assumptions—needs validation"]

---

## Personas

### Persona 1: [Name/Label]
*[One-line description of who they are]*

**Goals:**
- [Primary goal]
- [Secondary goal]

**Context:**
- [When they encounter the problem]
- [Where they encounter it]
- [What else is going on]

**Pain points:**
- [Frustration 1]
- [Frustration 2]

**Current behavior:**
- [How they solve this today]
- [Tools they use]
- [Workarounds they've developed]

**Constraints:**
- [Time/budget/skill/access limitations]

**What success looks like:**
- [How they'd know the problem is solved]

**Quote:** *"[Something they might say that captures their mindset]"*

---

### Persona 2: [Name/Label]
*[One-line description]*

[Same structure]

---

### Persona 3: [Name/Label]
*[One-line description]*

[Same structure]

---

## Scenarios

### Persona 1 Scenarios

**Scenario 1.1: [Name]**
- **Situation:** [Context—what's happening]
- **Trigger:** [What prompts them to act]
- **Goal:** [What they're trying to accomplish]
- **Current approach:** [How they handle it today]
- **Frustration:** [What's broken about current approach]

**Scenario 1.2: [Name]**
[Same structure]

### Persona 2 Scenarios

**Scenario 2.1: [Name]**
[Same structure]

---

## Key Insights

### Commonalities
[What all personas share—these are table-stakes features]
- [Insight 1]
- [Insight 2]

### Divergences
[Where personas differ—these inform prioritization]
- [Persona 1] needs [X], while [Persona 2] needs [Y]
- [Persona 1] is [context], while [Persona 2] is [different context]

### Design Implications
[How this should influence what you build]
- [Implication 1]
- [Implication 2]
- [Implication 3]

---

## Validation Needed
[What assumptions need testing]
- [ ] [Assumption to validate]
- [ ] [Assumption to validate]
```

## Adaptation Guidelines

**Minimal (single obvious user type):**
- One persona, 2-3 scenarios
- Skip Divergences section
- 1 page total

**Standard (2-3 user types):**
- Full structure as shown
- 2-3 pages total

**Research-heavy (actual user data):**
- Include research summary
- Add quotes from real users
- Link to source data in appendix

## What Makes a Good Persona

**Good persona:**
- Defined by *goals and behaviors*, not demographics
- Reveals something that changes what you'd build
- Based on patterns, not individuals
- Specific enough to make decisions against

**Bad persona:**
- Stock photo + age + job title + hobbies
- So generic it could be anyone
- Based on one interview or pure assumption
- Doesn't inform any product decisions

## Anti-Patterns to Avoid

- **The Kitchen Sink** — Don't add demographics unless they matter
- **The Clone Army** — If personas don't differ meaningfully, merge them
- **The Wishful Thinker** — Model who users *are*, not who you wish they were
- **The Edge Case Collector** — Focus on primary users, not every possible user

## Handoff

After presenting the personas, ask:
> "Want to move to `/solution-scoping` to prioritize features, or straight to `/prd-generation`?"

**Note:** File is automatically saved to `design/02-user-modeling.md` for context preservation.