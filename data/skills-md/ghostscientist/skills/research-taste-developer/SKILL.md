---
name: research-taste-developer
description: Develops intuition for what makes research "good" versus "incremental." Use when asked about research taste, how to identify good research, what makes a paper impactful, how to develop research intuition, or how to pick important problems. Analyzes patterns in highly-cited work and what top researchers do differently.
---

# Research Taste Developer

Research taste is the ability to distinguish work that matters from work that doesn't - before the community tells you. This skill helps you develop that instinct.

## What is Research Taste?

It's the intuition that lets experienced researchers:
- Pick problems that turn out to be important
- Know when an idea is "close" vs. "far" from working
- Recognize a good result even with imperfect execution
- Predict which papers will be remembered in 5 years

Taste isn't magic - it's pattern recognition from deep exposure. This skill accelerates that exposure.

## Process

### Phase 1: Analyze the Field

Pick a specific subfield. We'll study what "good" looks like there.

**Questions to investigate:**
1. What are the 10 most-cited papers of the last 5 years?
2. What are the 5 papers experts say "changed how we think"?
3. What are the best papers from top venues (NeurIPS, ICML, CVPR, etc.)?
4. What got awards? What got invited talks?

**For each landmark paper, analyze:**
- What was the state before this paper?
- What's the single core insight?
- What specifically made people cite it?
- Was it obvious in hindsight?

### Phase 2: Pattern Recognition

Look for what the great papers have in common:

**The Patterns of Impact:**

#### 1. The New Primitive
Papers that introduce a building block others build on.
- Examples: Attention mechanism, ResNet skip connections, Dropout
- Pattern: Simple idea, surprisingly general applicability
- Why it works: Reduces friction for future work

#### 2. The Surprising Connection
Papers that link two previously separate areas.
- Examples: VAE (variational inference + neural nets), NeRF (neural nets + ray marching)
- Pattern: "X, but for Y" where the combination is non-obvious
- Why it works: Cross-pollinates communities

#### 3. The Scaling Insight
Papers showing that scale changes qualitative behavior.
- Examples: GPT-3, Chinchilla
- Pattern: What everyone "knew" was wrong at sufficient scale
- Why it works: Forces field to update beliefs

#### 4. The Rigorous Foundation
Papers that formalize what was previously folklore.
- Examples: Theoretical convergence proofs, generalization bounds
- Pattern: Makes hand-wavy intuitions precise
- Why it works: Enables confident building

#### 5. The Elegant Solution
Papers that solve a problem far more simply than expected.
- Examples: Simple baseline papers, "X is all you need"
- Pattern: Previous solutions were overcomplicated
- Why it works: Shifts field's complexity assumptions

### Phase 3: Anti-Patterns

Learn to recognize work that won't age well:

**The Incremental Treadmill:**
- Pattern: +0.5% on benchmark with architectural tweak
- Why it fails: No one remembers or uses it
- Exception: When it reveals something fundamental

**The Method Mashing:**
- Pattern: "We combine A, B, C, and D"
- Why it fails: No insight about why the combination works
- Exception: When combination reveals unexpected interaction

**The Benchmark Overfitter:**
- Pattern: Method that works only on specific benchmarks
- Why it fails: Doesn't transfer, forgotten when benchmarks change
- Exception: When it exposes benchmark weaknesses

**The Complexity Monster:**
- Pattern: Works but requires 47 hyperparameters and 3 loss terms
- Why it fails: No one can reproduce or build on it
- Exception: Rarely

**The Solution Without a Problem:**
- Pattern: Novel method without compelling use case
- Why it fails: "Interesting but why?"
- Exception: When use case emerges later (rare)

### Phase 4: Develop Your Own Taste

**Exercise 1: Prediction Game**
Before reading a paper, predict based on title/abstract:
- Will this paper be cited >100 times in 5 years?
- Write down your prediction and reasoning
- Track your accuracy over time
- Analyze where your predictions went wrong

**Exercise 2: Explain the Gap**
For any two papers in citation count:
- Paper A: 2000 citations
- Paper B: 50 citations (same venue, same year)
- What explains the difference?
- Write a paragraph explanation

**Exercise 3: The Time Machine**
Pick a highly-cited paper. Go back to when it was published:
- What was the state of the field?
- Would you have recognized its importance?
- What signals would you have looked for?

**Exercise 4: Design a Hit**
Given current state of a field:
- What's the most important open problem?
- What would a "great paper" on this look like?
- What would make people cite it?

### Phase 5: Meta-Principles

What top researchers seem to do differently:

**Problem Selection:**
- Work on problems that are "ready" (pieces exist, no one assembled them)
- Avoid problems that are stuck for fundamental reasons
- Pick problems where you have unfair advantages

**Execution Taste:**
- Know when to stop polishing (diminishing returns)
- Know when result is "strong enough" to share
- Prefer simple-that-works over complex-that-works-slightly-better

**Communication Taste:**
- Lead with the insight, not the method
- Make contribution obvious in first 2 minutes
- Anticipate and address likely objections

**Portfolio Taste:**
- Mix safe and risky projects
- Build a coherent research identity
- Create compound interest (each paper enables the next)

## Output: Taste Development Report

```markdown
# Research Taste Analysis: [Field/Subfield]

## Landmark Paper Analysis

### [Paper 1 Title] ([Year])
- **Pre-existing state:** [What was true before]
- **Core insight:** [One sentence]
- **Why it's cited:** [Specific reason]
- **Pattern type:** [New Primitive / Connection / etc.]

### [Paper 2 Title]
[Same structure]

## Pattern Distribution
In this subfield, highly-cited papers tend to be:
- [X]% New Primitives
- [Y]% Surprising Connections
- [Z]% Other

## Anti-Pattern Warnings
The following patterns are common but don't lead to impact:
1. [Anti-pattern common in this field]
2. [Another one]

## Taste Heuristics for [Field]
When evaluating a paper in this field, ask:
1. [Field-specific question that distinguishes good from meh]
2. [Another one]
3. [Another one]

## Current Opportunities
Based on this analysis, promising directions seem to be:
1. [Direction 1]: [Why it's ripe]
2. [Direction 2]: [Why it's ripe]

## Your Taste Development Exercises
1. [Specific exercise for this field]
2. [Another one]
```

## The Ultimate Test

You have good taste when:
- You're bored by work others find impressive (correctly predicting it won't matter)
- You're excited by work others overlook (correctly predicting it will matter)
- Your intuitions about importance are calibrated with reality
- You can articulate *why* something is good, not just that it is

This takes years. But deliberate practice - not just reading, but *analyzing* - accelerates it dramatically.
