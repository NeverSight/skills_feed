---
name: brainstorming
description: Use when starting any feature, project, or design work. Guides collaborative design refinement through incremental questioning before any code is written.
---

# Brainstorming

## Core Principle

**Design before code. Always.**

Don't jump into implementation. Tease out the spec through conversation first.

## The Brainstorming Process

### Step 1: Understand the Goal
Ask clarifying questions:
- What problem are we solving?
- Who is the user?
- What does success look like?
- What are the constraints?

**One question at a time** - Don't overwhelm with multiple questions.

### Step 2: Explore the Space
- What are the possible approaches?
- What are the trade-offs?
- What similar problems exist?
- What patterns apply?

### Step 3: Propose Alternatives
Always present **2-3 approaches** before settling:

```markdown
## Option A: [Name]
- Pros: ...
- Cons: ...
- Best when: ...

## Option B: [Name]
- Pros: ...
- Cons: ...
- Best when: ...

## Option C: [Name]
- Pros: ...
- Cons: ...
- Best when: ...

**Recommendation:** Option [X] because...
```

### Step 4: Incremental Validation
Present design in digestible chunks:
- Show one section at a time
- Get sign-off before moving on
- Allow for course corrections

### Step 5: Document the Design
Save to: `docs/plans/YYYY-MM-DD-<topic>-design.md`

## YAGNI Ruthlessly

During brainstorming, actively remove:
- Features that "might be nice"
- Edge cases that "could happen"
- Abstractions for "future flexibility"
- Optimizations for "scale we might need"

Ask: **"Do we need this for the MVP?"**

## Question Techniques

### Multiple Choice Preferred
Instead of: "How should we handle errors?"
Ask: "For error handling, should we: A) Return error codes, B) Throw exceptions, C) Use Result types?"

### Constrained Questions
Instead of: "What should the API look like?"
Ask: "Should this be REST, GraphQL, or RPC?"

### Assumption Surfacing
- "I'm assuming X. Is that correct?"
- "This depends on Y. Is that available?"
- "The constraint seems to be Z. Agreed?"

## Output: Design Document

```markdown
# [Feature Name] Design

## Problem Statement
What problem are we solving?

## Goals
- Goal 1
- Goal 2

## Non-Goals
- Explicitly out of scope item 1
- Explicitly out of scope item 2

## Proposed Solution
Overview of the approach

## Alternatives Considered
Why we didn't choose other approaches

## Technical Design
### Component A
...
### Component B
...

## Open Questions
- Question 1
- Question 2

## Next Steps
1. Step 1
2. Step 2
```

## Transition to Implementation

After design is approved:
1. Ask: "Ready to set up for implementation?"
2. Use `using-git-worktrees` skill to create isolated workspace
3. Use `writing-plans` skill to create detailed implementation plan

## Anti-Patterns

### Don't Do This
- Start coding before design is clear
- Present only one option
- Ask open-ended questions when specific ones work
- Skip validation of each section
- Assume requirements are complete
- Over-engineer the initial design
