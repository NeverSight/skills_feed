---
name: hypothesis-tree
description:
  Structure complex questions into testable hypotheses. Use when validating
  product ideas, debugging problems, planning experiments, or breaking down
  ambiguous challenges into actionable research.
---

# Hypothesis Tree - Structured Problem Decomposition

A Hypothesis Tree is a structured approach to breaking down complex questions
into testable hypotheses. Originally from management consulting (McKinsey), it
ensures MECE (Mutually Exclusive, Collectively Exhaustive) coverage of a problem
space.

## When to Use This Skill

- Validating new product or feature ideas
- Investigating why metrics are underperforming
- Planning user research or experiments
- Breaking down ambiguous strategic questions
- Prioritizing what to test first
- Communicating analysis structure to stakeholders

## Core Concepts

### Structure of a Hypothesis Tree

```
                    Main Question
                    "Why is X happening?"
                          |
          +---------------+---------------+
          |               |               |
     Hypothesis A    Hypothesis B    Hypothesis C
          |               |               |
       +--+--+         +--+--+         +--+--+
       |     |         |     |         |     |
     Sub-   Sub-     Sub-   Sub-     Sub-   Sub-
     hyp    hyp      hyp    hyp      hyp    hyp
```

### MECE Principle

**Mutually Exclusive**: No overlap between branches **Collectively Exhaustive**:
All possibilities covered

```
Good MECE:                    Bad (not MECE):
+----------------+            +----------------+
| New users      |            | Mobile users   | <- Overlap
|----------------|            |----------------|
| Returning      |            | New users      | <- Overlap
| users          |            |----------------|
+----------------+            | Some users     | <- Vague
                              +----------------+
```

### Hypothesis Format

Strong hypotheses are:

| Element         | Description             | Example                                  |
| --------------- | ----------------------- | ---------------------------------------- |
| **Specific**    | Clear, measurable       | "Checkout abandonment is >70% on mobile" |
| **Testable**    | Can be proven/disproven | Not "users don't like it"                |
| **Falsifiable** | Could be wrong          | Has clear failure criteria               |
| **Actionable**  | Leads to decision       | If true → do X, if false → do Y          |

## Analysis Framework

### Step 1: Frame the Question

Convert vague concerns into structured questions:

| Vague                   | Structured                        |
| ----------------------- | --------------------------------- |
| "Growth is slow"        | "Why is our MoM user growth <5%?" |
| "Users aren't engaged"  | "Why is D7 retention below 20%?"  |
| "Feature isn't working" | "Why is feature X adoption <10%?" |

### Step 2: Generate First-Level Hypotheses

Brainstorm potential explanations, then organize MECE:

```
Question: "Why is signup conversion <30%?"

Level 1 Hypotheses:
├── Awareness: Users don't understand the value proposition
├── Ability: The signup process is too difficult
├── Motivation: The perceived benefit isn't worth the effort
└── Technical: Bugs/errors prevent completion
```

### Step 3: Decompose to Testable Level

Keep breaking down until hypotheses are directly testable:

```
Ability: The signup process is too difficult
├── Too many fields required
├── Password requirements unclear
├── Form validation confusing
└── Mobile experience broken
```

### Step 4: Prioritize and Test

| Hypothesis | Evidence Available | Test Effort | Impact if True |
| ---------- | ------------------ | ----------- | -------------- |
| [Hyp 1]    | [None/Some/Strong] | [L/M/H]     | [L/M/H]        |
| [Hyp 2]    | [None/Some/Strong] | [L/M/H]     | [L/M/H]        |

Priority = High Impact + Low Effort + Little Existing Evidence

## Output Template

```markdown
## Hypothesis Tree Analysis

**Central Question:** [Clear, specific question] **Date:** [Date] **Owner:**
[Name]

### Hypothesis Tree Structure

[Main Question] ├── H1: [First major hypothesis] │ ├── H1.1: [Sub-hypothesis] │
└── H1.2: [Sub-hypothesis] ├── H2: [Second major hypothesis] │ ├── H2.1:
[Sub-hypothesis] │ └── H2.2: [Sub-hypothesis] └── H3: [Third major hypothesis]
└── H3.1: [Sub-hypothesis]

### Prioritized Testing Plan

| Priority | Hypothesis | Test Method | Timeline | Owner |
| -------- | ---------- | ----------- | -------- | ----- |
| 1        | [H1.2]     | [Method]    | [Time]   | [Who] |
| 2        | [H2.1]     | [Method]    | [Time]   | [Who] |

### Current Evidence Summary

| Hypothesis | Status                       | Evidence  |
| ---------- | ---------------------------- | --------- |
| [H1]       | [Confirmed/Rejected/Testing] | [Summary] |
```

## Real-World Examples

### Example 1: Low Feature Adoption

**Question**: "Why is our new reporting feature only used by 8% of users?"

```
Low Feature Adoption
├── Awareness
│   ├── Users don't know it exists
│   └── Announcement wasn't clear
├── Value
│   ├── Feature doesn't solve their problem
│   └── Existing workarounds are "good enough"
├── Ability
│   ├── Feature is hard to find
│   └── Feature is hard to use
└── Timing
    └── Users don't need reports frequently
```

### Example 2: Churn Investigation

**Question**: "Why did monthly churn increase from 5% to 8%?"

```
Increased Churn
├── Product Changes
│   ├── Recent feature change caused issues
│   └── Performance degradation
├── Market Changes
│   ├── Competitor launched better alternative
│   └── Economic conditions changed
├── Customer Mix
│   ├── Acquired lower-quality leads
│   └── Channel mix shifted
└── Service Issues
    └── Support quality declined
```

## Best Practices

### Do

- Start with clear, specific question
- Check MECE at each level
- Get to testable hypotheses quickly (3 levels usually enough)
- Update tree as evidence comes in
- Share tree with stakeholders for alignment

### Avoid

- Overlapping hypotheses (not mutually exclusive)
- Hypotheses that can't be tested
- Going too deep without testing
- Confirmation bias (seeking to prove favorite hypothesis)

## Integration with Other Methods

| Method                  | Combined Use                      |
| ----------------------- | --------------------------------- |
| **Five Whys**           | Go deep on confirmed hypotheses   |
| **Jobs-to-be-Done**     | Frame hypotheses around user jobs |
| **Fogg Behavior Model** | Structure behavioral hypotheses   |

## Resources

- [The Pyramid Principle - Barbara Minto](https://www.amazon.com/Pyramid-Principle-Logic-Writing-Thinking/dp/0273710516)
- [Bulletproof Problem Solving - Charles Conn](https://www.amazon.com/Bulletproof-Problem-Solving-Changes-Everything/dp/1119553024)
