---
name: argument-mapping
description: "Reconstruct, visualize, and analyze argument structure. Use for: argument reconstruction, premise identification, inference evaluation, finding hidden assumptions, visualizing debates, Toulmin model analysis. Triggers: 'argument structure', 'premises', 'conclusion', 'inference', 'reconstruct', 'map the argument', 'Toulmin', 'argument diagram', 'validity', 'soundness', 'implicit premise', 'hidden assumption', 'logical structure'."
---

# Argument Mapping Skill

Master the art of reconstructing, visualizing, and evaluating the logical structure of arguments.

## Why Map Arguments?

Argument mapping serves several purposes:
1. **Clarify**: Make implicit structure explicit
2. **Evaluate**: Assess validity and soundness systematically
3. **Communicate**: Present complex arguments visually
4. **Critique**: Identify weaknesses and hidden assumptions
5. **Steelman**: Ensure fair representation of opposing views

## Basic Argument Structure

### Components of an Argument

| Component | Definition | Example |
|-----------|------------|---------|
| **Conclusion** | The claim being argued for | "Socrates is mortal" |
| **Premise** | A reason supporting the conclusion | "All men are mortal" |
| **Inference** | The logical move from premises to conclusion | "Therefore..." |
| **Assumption** | Unstated premise needed for validity | (Often hidden) |

### Simple Argument Form

```
P1: [Premise 1]
P2: [Premise 2]
-------------------
C: [Conclusion]
```

**Example**:
```
P1: All men are mortal
P2: Socrates is a man
-------------------
C: Socrates is mortal
```

## The Toulmin Model

Stephen Toulmin's model captures the nuanced structure of real-world arguments.

### Six Components

```
                        QUALIFIER
                            │
                            ▼
  GROUNDS ──────────► CLAIM ◄─────────── REBUTTAL
      │                  ▲                    │
      │                  │                    │
      ▼                  │                    ▼
  WARRANT ◄──────── BACKING               (Unless...)
```

| Component | Definition | Example |
|-----------|------------|---------|
| **Claim** | The conclusion/assertion | "We should ban smoking in restaurants" |
| **Grounds** | Evidence/data supporting claim | "Secondhand smoke causes cancer" |
| **Warrant** | Principle connecting grounds to claim | "We should prevent cancer-causing exposures" |
| **Backing** | Support for the warrant itself | "Preventing harm is a core purpose of public policy" |
| **Qualifier** | Degree of certainty | "Probably," "Certainly," "Presumably" |
| **Rebuttal** | Conditions where claim fails | "Unless economic harm outweighs health benefits" |

### Toulmin Diagram Template

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  CLAIM: [Central thesis/conclusion]                                 │
│         Qualifier: [Certainly/Probably/Possibly]                    │
│                                                                     │
│  ────────────────────────────────────────────────────────────────   │
│                                                                     │
│  GROUNDS:                          │  REBUTTAL:                     │
│  [Evidence/facts/data]             │  Unless [exception conditions] │
│                                    │                                │
│  ────────────────────────────────────────────────────────────────   │
│                                                                     │
│  WARRANT:                                                           │
│  [Principle that licenses inference from grounds to claim]          │
│                                                                     │
│  ────────────────────────────────────────────────────────────────   │
│                                                                     │
│  BACKING:                                                           │
│  [Support for the warrant]                                          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Argument Reconstruction Protocol

### Step 1: Identify the Conclusion
What is the main claim being defended?

**Indicator words**: therefore, thus, hence, so, consequently, it follows that, we can conclude

**If not explicit**: What would the speaker want you to believe/do?

### Step 2: Find the Premises
What reasons are given for the conclusion?

**Indicator words**: because, since, for, given that, as shown by, the reason is

**List them**: Number each premise explicitly (P1, P2, P3...)

### Step 3: Make Implicit Premises Explicit
What unstated assumptions are needed for the argument to work?

**Test**: If we add this premise, does the argument become valid?

**Charity**: Choose the most reasonable implicit premises

### Step 4: Analyze the Structure
How do the premises relate?

**Linked premises**: Work together (all needed)
```
    P1 + P2
       │
       ▼
       C
```

**Convergent premises**: Independent support (each sufficient)
```
    P1     P2
     \    /
      \  /
       C
```

**Serial/Chain arguments**: One supports another
```
    P1
     │
    P2
     │
     C
```

### Step 5: Evaluate
- **Validity**: Does conclusion follow from premises?
- **Soundness**: Are premises actually true?
- **Strength** (inductive): How probable is conclusion given premises?

## Diagramming Conventions

### Standard Notation

```
┌─────┐
│ P1  │  ← Premise (box)
└──┬──┘
   │
   ▼
┌─────┐
│  C  │  ← Conclusion (box)
└─────┘
```

### Linked vs. Convergent

**Linked** (all premises needed together):
```
┌─────┐   ┌─────┐
│ P1  │───│ P2  │
└──┬──┘   └──┬──┘
   └────┬────┘
        ▼
    ┌─────┐
    │  C  │
    └─────┘
```

**Convergent** (independent support):
```
┌─────┐         ┌─────┐
│ P1  │         │ P2  │
└──┬──┘         └──┬──┘
   │             │
   └─────┬───────┘
         ▼
     ┌─────┐
     │  C  │
     └─────┘
```

### Sub-Arguments

When a premise is itself supported:
```
┌─────┐
│ P1a │  ← Sub-premise
└──┬──┘
   ▼
┌─────┐
│ P1  │  ← Intermediate conclusion / Premise for main argument
└──┬──┘
   │
┌──┴──┐
│ P2  │
└──┬──┘
   ▼
┌─────┐
│  C  │  ← Main conclusion
└─────┘
```

### Objections and Rebuttals

```
┌─────┐
│ P1  │
└──┬──┘
   ▼
┌─────┐         ┌─────────┐
│  C  │ ◄─ ✗ ───│Objection│
└─────┘         └────┬────┘
                     │
                ┌────▼────┐
                │ Rebuttal│
                └─────────┘
```

## Dialectical Tree Format

For multi-position debates:

```
THESIS: [Main Position A]
│
├── Support 1: [Argument for A]
│   ├── Evidence 1a
│   └── Evidence 1b
│
├── Support 2: [Another argument for A]
│
└── ANTITHESIS: [Opposing Position B]
    │
    ├── Objection to Support 1: [Why it fails]
    │
    ├── Objection to Support 2: [Why it fails]
    │
    └── Positive argument for B
        │
        └── SYNTHESIS: [Higher-level resolution]
            │
            ├── What's preserved from A
            ├── What's preserved from B
            └── What's new
```

## Common Argument Patterns

### Deductive Patterns

**Modus Ponens**:
```
P1: If A, then B
P2: A
---------------
C: B
```

**Modus Tollens**:
```
P1: If A, then B
P2: Not B
---------------
C: Not A
```

**Disjunctive Syllogism**:
```
P1: A or B
P2: Not A
---------------
C: B
```

**Hypothetical Syllogism**:
```
P1: If A, then B
P2: If B, then C
---------------
C: If A, then C
```

**Reductio ad Absurdum**:
```
P1: Assume A (for contradiction)
P2: A leads to contradiction B & not-B
---------------
C: Not A
```

### Inductive Patterns

**Generalization**:
```
P1: Sample S has property P
P2: Sample S is representative of population X
---------------
C: (Probably) All X have property P
```

**Analogy**:
```
P1: A has properties F, G, H
P2: B has properties F, G
P3: A has property X
---------------
C: (Probably) B has property X
```

**Inference to Best Explanation**:
```
P1: Phenomenon P is observed
P2: Hypothesis H would explain P
P3: H is the best available explanation
---------------
C: (Probably) H is true
```

### Philosophical Argument Patterns

**Conceivability Argument**:
```
P1: X is conceivable
P2: If conceivable, then possible
---------------
C: X is possible
```

**Counterexample**:
```
P1: Thesis T claims all X are Y
P2: Case C is X but not Y
---------------
C: Thesis T is false
```

**Thought Experiment**:
```
P1: In scenario S, intuition I is strong
P2: If I is correct, then principle P
---------------
C: Principle P
```

## Hidden Assumption Detection

### Method 1: Gap Analysis
1. State the premises
2. State the conclusion
3. Ask: What must be true for this inference to work?
4. The answer is the hidden assumption

### Method 2: Negation Test
1. Negate a potential assumption
2. If the argument fails, the assumption was needed

### Method 3: Charity + Validity
1. Assume the argument is intended to be valid
2. What premise would make it valid?
3. That's the most charitable hidden assumption

### Common Hidden Assumptions

| Type | Example |
|------|---------|
| **Empirical** | Facts about the world assumed without evidence |
| **Normative** | Value judgments assumed without defense |
| **Conceptual** | Definitions assumed without clarification |
| **Background** | Shared context assumed without statement |
| **Scope** | Universality assumed without justification |

## Evaluation Criteria

### For Deductive Arguments

| Criterion | Question | Assessment |
|-----------|----------|------------|
| **Validity** | Does conclusion follow necessarily? | Yes/No |
| **Soundness** | Are all premises true? | Yes/No/Unknown |
| **Completeness** | Are hidden premises stated? | Yes/Partially/No |

### For Inductive Arguments

| Criterion | Question | Assessment |
|-----------|----------|------------|
| **Strength** | How probable is conclusion given premises? | Strong/Moderate/Weak |
| **Cogency** | Are premises true AND argument strong? | Yes/No |
| **Sample quality** | Is evidence representative? | Yes/No |

## Output Templates

### Standard Reconstruction

```markdown
## Argument Reconstruction: [Topic/Source]

### Conclusion
[State the main claim being argued for]

### Explicit Premises
P1: [First stated premise]
P2: [Second stated premise]
P3: [Third stated premise]

### Hidden Premises
H1: [First unstated assumption needed for validity]
H2: [Second unstated assumption]

### Argument Structure
[Diagram showing how premises relate to conclusion]

### Evaluation
- **Validity**: [Valid/Invalid—explain]
- **Soundness**: [Sound/Unsound/Unknown—explain]
- **Key weakness**: [Most vulnerable point]

### Dialectical Context
[How this argument relates to the broader debate]
```

### Debate Map

```markdown
## Debate Map: [Topic]

### Question at Issue
[The central question being debated]

### Position A: [Label]
**Thesis**: [Main claim]

**Arguments**:
1. [Argument 1]
   - Objection: [Counter]
   - Reply: [Response]
2. [Argument 2]

### Position B: [Label]
**Thesis**: [Main claim]

**Arguments**:
1. [Argument 1]
2. [Argument 2]

### Points of Agreement
- [Shared premise 1]
- [Shared premise 2]

### Core Disagreement
[What the debate ultimately turns on]

### Assessment
[Which position is stronger and why]
```

## Integration with Other Skills

- **philosophical-analyst**: Use mapping in step 2 (argument reconstruction)
- **symposiarch**: Map arguments during debate management
- **thought-experiments**: Map the argument structure of thought experiment cases
- **devils-advocate**: Identify weak premises in argument maps

## Reference Files

- `patterns.md`: Comprehensive catalog of argument patterns
- `diagramming.md`: Extended diagramming conventions and tools
