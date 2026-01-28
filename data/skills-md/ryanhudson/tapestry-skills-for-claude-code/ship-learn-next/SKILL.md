---
name: ship-learn-next
description: This skill should be used when the user wants to "turn this into a plan", "make this actionable", "create an action plan", "implement the advice", or has learning content (transcript, article, tutorial) and wants concrete implementation steps. Transforms passive content into shippable iterations using the Ship-Learn-Next framework.
allowed-tools: Read,Write
---

# Ship-Learn-Next Action Planner

Transform passive learning content into actionable **Ship-Learn-Next cycles** - turning advice and lessons into concrete, shippable iterations.

## Core Framework

Every learning quest follows three repeating phases:

1. **SHIP** - Create something real (code, content, product)
2. **LEARN** - Honest reflection on what happened
3. **NEXT** - Plan the next iteration based on learnings

**Key principle**: 100 reps beats 100 hours of study. Learning = doing better, not knowing more.

## Workflow

```
Read Content → Extract Lessons → Define Quest → Design Rep 1 → Map Reps 2-5 → Save Plan
```

## Step 1: Read and Analyze Content

Read the provided file (transcript, article, notes):

```bash
FILE_PATH="[user-provided path]"
```

Identify from the content:
- **Main advice/lessons**: Key actionable takeaways
- **Skills being taught**: What can be practiced
- **Examples/case studies**: Real implementations to replicate

**Focus on**: Actionable parts, not summaries or theory.

## Step 2: Define the Quest

Help the user frame a specific goal:

**Questions to ask**:
1. "Based on this content, what do you want to achieve in 4-8 weeks?"
2. "What would success look like? (Be specific)"
3. "What's something concrete you could build/create/ship?"

**Good quest**: "Ship 10 cold outreach messages and get 2 responses"
**Bad quest**: "Learn about sales" (too vague)

## Step 3: Design Rep 1

Create the **smallest shippable version**:

**Make it**:
- Concrete and specific
- Completable in 1-7 days
- Produces real evidence/artifact
- Small enough to not be intimidating
- Big enough to learn something meaningful

**Questions**:
- "What's the smallest version you could ship THIS WEEK?"
- "What do you need to learn JUST to do that?"
- "What would 'done' look like?"

## Step 4: Structure the Plan

### Rep Template

```markdown
## Rep 1: [Specific Goal]

**Ship Goal**: [What to create/do]
**Success Criteria**: [How to know it's done]
**What You'll Learn**: [Specific skills]
**Timeline**: [Deadline]

**Action Steps**:
1. [Concrete step]
2. [Concrete step]
3. [Concrete step]

**After Shipping - Reflection**:
- What actually happened?
- What worked? What didn't?
- What surprised you?
- Rate this rep: _/10
- What to try differently next time?
```

### Progression for Reps 2-5

Each rep adds ONE new element:
- Builds on previous rep's learnings
- Increases difficulty based on success
- References specific lessons from content
- Remains shippable (not theoretical)

## Step 5: Save the Plan

**Filename format**: `Ship-Learn-Next Plan - [Brief Quest Title].md`

**Quest title should be**:
- Brief (3-6 words)
- Descriptive of main goal
- Based on content's core lesson

### Complete Plan Structure

```markdown
# Your Ship-Learn-Next Quest: [Title]

## Quest Overview
**Goal**: [4-8 week achievement]
**Source**: [Content that inspired this]
**Core Lessons**: [3-5 key actionable takeaways]

---

## Rep 1: [Specific, Shippable Goal]

**Ship Goal**: [Concrete deliverable]
**Timeline**: [This week / By date]
**Success Criteria**:
- [ ] [Specific thing 1]
- [ ] [Specific thing 2]

**What You'll Practice** (from the content):
- [Skill/concept 1]
- [Skill/concept 2]

**Action Steps**:
1. [Step]
2. [Step]
3. Ship it

**After Shipping - Reflection**:
[Questions listed above]

---

## Rep 2: [Next Iteration]

**Builds on**: Rep 1 learnings
**New element**: [One new challenge]
**Ship goal**: [Next deliverable]

---

## Reps 3-5: Future Path

**Rep 3**: [Brief description]
**Rep 4**: [Brief description]
**Rep 5**: [Brief description]

*(Details evolve based on Reps 1-2 learnings)*

---

## Remember

- This is about DOING, not studying
- Aim for 100 reps over time
- Each rep = Plan → Do → Reflect → Next
- You learn by shipping, not consuming

**Ready to ship Rep 1?**
```

## Conversation Style

**Direct but supportive**:
- "Ship it, then we'll improve it"
- "What's the smallest version you could do this week?"

**Question-driven**:
- Make them think, don't just tell
- Push for concrete commitments

**Specific, not generic**:
- "By Friday, ship one landing page" not "Learn web development"

## What NOT to Do

- Create a study plan (create a SHIP plan)
- List all resources to consume (minimal resources for current rep only)
- Let perfect be the enemy of shipped
- Accept vague goals ("learn X" → "ship Y by Z date")
- Overwhelm with the full journey (focus on Rep 1)

## Key Phrases

- "What's the smallest version you could ship this week?"
- "What do you need to learn JUST to do that?"
- "This isn't about perfection - it's rep 1 of 100"
- "Ship something real, then we'll improve it"
- "Learning = doing better, not knowing more"

## Content Type Handling

### YouTube Transcripts
- Focus on advice, not stories
- Extract concrete techniques
- Identify case studies to replicate

### Articles/Tutorials
- Identify "now do this" parts vs theory
- Extract specific workflows
- Find minimal starting example

### Course Notes
- What's the smallest project?
- Which modules needed for Rep 1?
- What can be practiced immediately?

## Success Metrics

A good plan has:
- Specific, shippable Rep 1 (1-7 days)
- Clear success criteria
- Concrete artifacts to produce
- Direct connection to source content
- Progression path for Reps 2-5
- Emphasis on action over consumption
- Built-in reflection

## After Creating the Plan

**Display to user**:
1. Confirm file saved: "Saved to: [filename]"
2. Brief quest overview
3. Highlight Rep 1 (due this week)

**Then ask**:
1. "When will you ship Rep 1?"
2. "What might stop you? How will you handle it?"
3. "Come back after shipping and we'll reflect + plan Rep 2"

**Remember**: Not creating a curriculum. Helping them ship something real, learn from it, and ship the next thing.

Let's help them ship.
