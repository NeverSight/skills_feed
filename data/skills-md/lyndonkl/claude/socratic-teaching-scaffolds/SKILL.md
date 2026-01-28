---
name: socratic-teaching-scaffolds
description: Use when teaching complex concepts (technical, scientific, philosophical), helping learners discover insights through guided questioning rather than direct explanation, correcting misconceptions by revealing contradictions, onboarding new team members through scaffolded learning, mentoring through problem-solving question frameworks, designing self-paced learning materials, or when user mentions "teach me", "help me understand", "explain like I'm", "learning path", "guided discovery", or "Socratic method".
---

# Socratic Teaching Scaffolds

## Table of Contents
1. [Purpose](#purpose)
2. [When to Use](#when-to-use)
3. [What Is It](#what-is-it)
4. [Workflow](#workflow)
5. [Socratic Question Types](#socratic-question-types)
6. [Scaffolding Levels](#scaffolding-levels)
7. [Common Patterns](#common-patterns)
8. [Guardrails](#guardrails)
9. [Quick Reference](#quick-reference)

## Purpose

Socratic Teaching Scaffolds guide learners to discover knowledge through strategic questioning and progressive support removal. This skill transforms passive explanation into active discovery, corrects misconceptions by revealing contradictions, and builds durable understanding through self-generated insights.

## When to Use

**Invoke this skill when you need to:**
- Teach complex concepts where understanding beats memorization (algorithms, scientific theories, philosophical ideas)
- Correct deep misconceptions that resist direct explanation (statistical fallacies, physics intuitions, programming mental models)
- Help learners develop problem-solving skills, not just solutions
- Design learning experiences that build from concrete to abstract understanding
- Onboard professionals through guided discovery rather than documentation dumps
- Create self-paced learning materials with built-in feedback loops
- Mentor through questions that develop independent thinking
- Bridge expertise gaps across different knowledge levels

**User phrases that trigger this skill:**
- "Teach me [concept]"
- "Help me understand [topic]"
- "Explain like I'm [expertise level]"
- "I don't get why [misconception]"
- "What's the best way to learn [skill]?"
- "How should I think about [concept]?"

## What Is It

A teaching framework combining **Socratic questioning** (strategic questions that guide discovery) with **instructional scaffolding** (temporary support that fades as competence grows).

**Core components:**
1. **Question Ladders**: Sequences from simple to complex that build understanding incrementally
2. **Misconception Detectors**: Questions that reveal faulty mental models through contradiction
3. **Feynman Explanations**: Build-up from simple analogies to technical precision
4. **Worked Examples with Fading**: Full solutions → partial solutions → independent practice
5. **Cognitive Apprenticeship**: Model thinking process explicitly, then transfer to learner

**Quick example (Teaching Recursion):**

**Question Ladder:**
1. "Can you break this problem into a smaller version of itself?" (problem decomposition)
2. "What would happen if we had only one item?" (base case discovery)
3. "If we could solve the small version, how would we use it for the big version?" (recursive case)
4. "What prevents this from running forever?" (termination reasoning)

**Misconception Detector:**
- "Will this recursion ever stop? Trace it with 3 items." (reveals infinite recursion misunderstanding)

**Feynman Progression:**
- Level 1: "Like Russian nesting dolls—each contains a smaller version"
- Level 2: "Function calls itself with simpler input until base case"
- Level 3: "Recursive definition: f(n) = g(f(n-1), n) with f(0) = base"

## Workflow

Copy this checklist and track your progress:

```
Socratic Teaching Progress:
- [ ] Step 1: Diagnose learner's current understanding
- [ ] Step 2: Design question ladder and scaffolding plan
- [ ] Step 3: Guide discovery through questioning
- [ ] Step 4: Fade scaffolding as competence grows
- [ ] Step 5: Validate understanding and transfer
```

**Step 1: Diagnose learner's current understanding**

Ask probing questions to identify current knowledge level, misconceptions, and learning goals. See [Socratic Question Types](#socratic-question-types) for diagnostic question categories.

**Step 2: Design question ladder and scaffolding plan**

Build progression from learner's current state to target understanding. For straightforward teaching → Use [resources/template.md](resources/template.md). For complex topics with multiple misconceptions → Study [resources/methodology.md](resources/methodology.md).

**Step 3: Guide discovery through questioning**

Ask questions in sequence, provide scaffolding (hints, worked examples, analogies) as needed. See [Scaffolding Levels](#scaffolding-levels) for support gradations. Adjust based on learner responses.

**Step 4: Fade scaffolding as competence grows**

Progressively remove hints, provide less complete examples, ask more open-ended questions. Monitor for struggle (optimal challenge) vs frustration (too hard). See [resources/methodology.md](resources/methodology.md) for fading strategies.

**Step 5: Validate understanding and transfer**

Test with novel problems, ask for explanations in learner's words, check for misconception elimination. Self-check using [resources/evaluators/rubric_socratic_teaching_scaffolds.json](resources/evaluators/rubric_socratic_teaching_scaffolds.json). Minimum standard: Average score ≥ 3.5.

## Socratic Question Types

**1. Clarifying Questions** (Understand current thinking)
- "What do you mean by [term]?"
- "Can you give me an example?"
- "How does this relate to [known concept]?"

**2. Probing Assumptions** (Surface hidden beliefs)
- "What are we assuming here?"
- "Why would that be true?"
- "Is that always the case?"

**3. Probing Reasons/Evidence** (Justify claims)
- "Why do you think that?"
- "What evidence supports that?"
- "How would we test that?"

**4. Exploring Implications** (Think through consequences)
- "What would happen if [change]?"
- "What follows from that?"
- "What are the edge cases?"

**5. Questioning the Question** (Meta-cognition)
- "Why is this question important?"
- "What are we really trying to understand?"
- "How would we know if we understood?"

**6. Revealing Contradictions** (Bust misconceptions)
- "Earlier you said [X], but now [Y]. How do these fit?"
- "If that's true, why does [counterexample] happen?"
- "What would this predict for [test case]?"

## Scaffolding Levels

Provide support that matches current need, then fade:

**Level 5: Full Modeling** (I do, you watch)
- Complete worked example with thinking aloud
- Explicit strategy articulation
- All steps shown with rationale

**Level 4: Guided Practice** (I do, you help)
- Partial worked example
- Ask learner to complete steps
- Provide hints before errors

**Level 3: Coached Practice** (You do, I help)
- Learner attempts independently
- Intervene with questions when stuck
- Guide without giving answers

**Level 2: Independent with Feedback** (You do, I watch)
- Learner solves alone
- Review and discuss afterwards
- Identify gaps for next iteration

**Level 1: Transfer** (You teach someone else)
- Learner explains to others
- Learner creates examples
- Learner identifies misconceptions in others

**Fading strategy:** Start at level matching current competence (not Level 5 by default). Move down one level when learner demonstrates success. Move up one level if learner struggles repeatedly.

## Common Patterns

**Pattern 1: Concept Introduction (Concrete → Abstract)**
- Start: Real-world analogy or example
- Middle: Formalize with terminology
- End: Abstract definition with edge cases
- Example: Teaching pointers (address on envelope → memory location → pointer arithmetic)

**Pattern 2: Misconception Correction (Prediction → Surprise → Explanation)**
- Ask learner to predict outcome
- Show actual result (contradicts misconception)
- Guide discovery of correct mental model
- Example: "Will this float? [test with 0.1 + 0.2 in programming] Why not exactly 0.3?"

**Pattern 3: Problem-Solving Strategy (Model → Practice → Reflect)**
- Model strategy on simple problem (think aloud)
- Learner applies to similar problem (with coaching)
- Reflect on when strategy applies/fails
- Example: Teaching debugging (print statements → breakpoints → hypothesis testing)

**Pattern 4: Depth Ladder (ELI5 → Undergraduate → Expert)**
- Build multiple explanations at different depths
- Let learner choose starting point
- Provide "go deeper" option at each level
- Example: Teaching neural networks (pattern matching → weighted sums → backpropagation → optimization theory)

**Pattern 5: Discovery Learning (Puzzle → Hints → Insight)**
- Present puzzling phenomenon or problem
- Provide graduated hints if stuck
- Guide to "aha" moment of discovery
- Example: Teaching recursion (Towers of Hanoi → break into subproblems → recursive solution)

## Guardrails

**Zone of proximal development:**
- Too easy = boredom, too hard = frustration
- Optimal: Can't do alone, but can with guidance
- Adjust scaffolding level based on struggle signals

**Don't fish for specific answers:**
- Socratic questioning isn't a guessing game
- If learner's reasoning is sound but reaches different conclusion, explore their path
- Multiple valid approaches often exist

**Avoid pseudo-teaching:**
- Don't just ask questions without purpose
- Each question should advance understanding or reveal misconception
- If question doesn't help, provide direct explanation

**Misconception resistance:**
- Deep misconceptions resist single corrections
- Need multiple exposures to contradictions
- May require building correct model from scratch before dismantling wrong one

**Expertise blind spots:**
- Experts forget what was hard as beginners
- Make implicit knowledge explicit
- Slow down automated processes to show thinking

**Individual differences:**
- Some learners prefer exploration, others prefer structure
- Adjust scaffolding style to learner preferences
- Monitor for frustration vs productive struggle

## Quick Reference

**Resources:**
- **Quick teaching session**: [resources/template.md](resources/template.md)
- **Complex topics/misconceptions**: [resources/methodology.md](resources/methodology.md)
- **Quality rubric**: [resources/evaluators/rubric_socratic_teaching_scaffolds.json](resources/evaluators/rubric_socratic_teaching_scaffolds.json)

**5-Step Process**: Diagnose → Design Ladder → Guide Discovery → Fade Scaffolding → Validate Transfer

**Question Types**: Clarifying, Probing Assumptions, Probing Evidence, Exploring Implications, Meta-cognition, Revealing Contradictions

**Scaffolding Levels**: Full Modeling → Guided Practice → Coached Practice → Independent Feedback → Transfer (fade progressively)

**Patterns**: Concrete→Abstract, Prediction→Surprise→Explanation, Model→Practice→Reflect, ELI5→Expert, Puzzle→Hints→Insight

**Guardrails**: Zone of proximal development, purposeful questions, avoid pseudo-teaching, resist misconceptions, make implicit explicit
