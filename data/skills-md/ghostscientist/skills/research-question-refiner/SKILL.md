---
name: research-question-refiner
description: Helps transform a vague research interest into a concrete, tractable research question. Use when asked to refine a research idea, develop a research question, scope a research project, or figure out what to work on. Walks through systematic refinement with feasibility analysis.
---

# Research Question Refiner

Transform "I'm interested in X" into "I will investigate whether Y under conditions Z, measuring W."

## The Problem

Most research ideas fail not because they're bad, but because they're:
- Too vague to act on
- Too ambitious to complete
- Too incremental to matter
- Missing a clear success criterion

This skill fixes that.

## Process

### Stage 1: Excavate the Interest

Start by understanding what's actually pulling at you:

**Questions to ask:**
1. What sparked this interest? (Paper, conversation, problem you encountered?)
2. What's the version that excites you most?
3. What would be cool if it worked?
4. Who would care about the answer?

**Output:** A paragraph capturing the raw interest, unfiltered.

### Stage 2: Map the Territory

Before scoping, understand the landscape:

**What's Known:**
- What's the current state-of-the-art?
- What are the established approaches?
- What have people tried that didn't work?

**What's Unknown:**
- What are the acknowledged open problems?
- What assumptions does current work make?
- Where do methods fail?

**What's Controversial:**
- Where do researchers disagree?
- What's claimed but not convincingly shown?
- What's believed but not rigorously tested?

**Output:** A structured map with citations/references for each area.

### Stage 3: Find the Gap

A good research question lives in a gap that is:

| Property | Too Little | Just Right | Too Much |
|----------|-----------|------------|----------|
| **Novelty** | Redoing existing work | New angle or combination | No foundation to build on |
| **Difficulty** | Trivial to answer | Challenging but doable | Requires breakthroughs |
| **Impact** | No one cares | Community would update beliefs | Nobel prize (unrealistic) |
| **Scope** | One experiment | Thesis chapter / paper | Multiple PhDs |

**Gap-finding questions:**
- What would change if we relaxed assumption X?
- What if we applied method A to domain B?
- What's between approach X and approach Y?
- What fails in setting Z that works elsewhere?

**Output:** 3-5 candidate gaps, each as one sentence.

### Stage 4: Refine to Concrete Question

For each candidate gap, sharpen into a question:

**The Formula:**
```
[Action verb] + [specific phenomenon] + [under conditions] + [measurable outcome]
```

**Examples of refinement:**

❌ Vague: "How can we make transformers more efficient?"
✅ Concrete: "Does structured sparsity in attention patterns preserve performance on long-context tasks while reducing compute by >50%?"

❌ Vague: "Can robots learn from humans better?"
✅ Concrete: "Does incorporating gaze direction in demonstrations improve sample efficiency for manipulation tasks compared to kinesthetic teaching alone?"

❌ Vague: "What makes language models hallucinate?"
✅ Concrete: "Do retrieval-augmented models hallucinate less on factual questions when retrieval confidence is used to modulate generation temperature?"

### Stage 5: Feasibility Check

For each refined question, assess:

**Resources Required:**
- Compute: GPU-hours estimate
- Data: Available or needs collection?
- Time: Weeks/months realistically
- Expertise: What skills are needed?

**Risk Assessment:**
- What's the probability this works at all?
- What if the hypothesis is wrong? (Is negative result publishable?)
- What could go wrong technically?
- What could invalidate the whole direction?

**Dependencies:**
- Does this require other work to finish first?
- Are there rate-limiting steps?
- What can be parallelized?

### Stage 6: The Litmus Tests

A good research question passes all of these:

**The Advisor Test:**
> "If I pitched this in 2 minutes, would a busy professor say 'yes, go do that' rather than 'hmm, let's talk more'?"

**The Paper Test:**
> "Can I envision the title, abstract, and figure 1 of the resulting paper?"

**The Null Result Test:**
> "If my hypothesis is wrong, would that still be interesting to report?"

**The Motivation Test:**
> "Am I actually excited to work on this for 6+ months?"

**The Explanation Test:**
> "Can I explain why this matters to a smart non-expert in 60 seconds?"

## Output Format

Deliver a Research Question Brief:

```markdown
# Research Question Brief

## The Interest (Raw)
[Original unfiltered interest]

## Territory Map

### What's Known
- [Point 1] ([citation])
- [Point 2] ([citation])

### What's Unknown
- [Open question 1]
- [Open question 2]

### What's Controversial
- [Debate 1]

## Candidate Gaps
1. [Gap 1]
2. [Gap 2]
3. [Gap 3]

## Refined Questions

### Question 1: [Title]
**Statement:** [Precise question]
**Hypothesis:** [What you expect to find]
**Feasibility:** [Brief assessment]
**If it works:** [Impact]
**If it doesn't:** [What we still learn]

### Question 2: [Title]
[Same structure]

## Recommendation
[Which question to pursue and why]

## Immediate Next Steps
1. [Concrete action 1]
2. [Concrete action 2]
3. [Concrete action 3]
```

## Common Failure Modes

**The Kitchen Sink:** Trying to answer too many questions at once
→ Fix: Ruthlessly cut until there's ONE core question

**The Solution in Search of a Problem:** Starting with a method, not a question
→ Fix: Ask "Who has this problem? Why hasn't it been solved?"

**The Incremental Trap:** Small delta on existing work
→ Fix: Ask "Would this change how people think?"

**The Impossible Dream:** Beautiful question, can't be answered
→ Fix: Ask "What's the minimal version that's still interesting?"

**The Boring Sure Thing:** Will definitely work, nobody cares
→ Fix: Add ambition until there's meaningful risk
