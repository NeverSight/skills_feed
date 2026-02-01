---
name: logic
description: "Master formal and informal logic - valid reasoning, fallacies, paradoxes. Use for: argument analysis, validity, soundness, logical form, fallacies, paradoxes. Triggers: 'valid', 'validity', 'fallacy', 'premise', 'conclusion', 'modus ponens', 'modus tollens', 'paradox', 'logical', 'syllogism', 'deduction', 'induction', 'inference', 'argument form', 'soundness', 'entailment', 'contradiction'."
---

# Logic Skill

Master the principles of valid reasoning: formal logic, informal logic, fallacy detection, and paradox analysis.

## Fundamentals

### Basic Concepts

| Term | Definition |
|------|------------|
| Argument | Premises + Conclusion |
| Premise | Statement offered as support |
| Conclusion | Statement being supported |
| Valid | Conclusion follows from premises |
| Sound | Valid + true premises |
| Cogent | Strong inductive + true premises |

### Validity vs. Soundness

```
VALIDITY: If premises true, conclusion must be true
          (Logical form preserves truth)

SOUNDNESS: Valid + Actually true premises
           (Guarantees true conclusion)

EXAMPLE:
All cats are mammals.     (True)
All mammals are animals.  (True)
∴ All cats are animals.   (True) → SOUND

All fish are mammals.     (False)
All mammals can fly.      (False)
∴ All fish can fly.       (False) → VALID but not SOUND
```

---

## Propositional Logic

### Connectives

| Symbol | Name | Meaning |
|--------|------|---------|
| ¬ | Negation | Not P |
| ∧ | Conjunction | P and Q |
| ∨ | Disjunction | P or Q |
| → | Conditional | If P then Q |
| ↔ | Biconditional | P iff Q |

### Valid Argument Forms

```
MODUS PONENS               MODUS TOLLENS
P → Q                      P → Q
P                          ¬Q
─────                      ─────
∴ Q                        ∴ ¬P

HYPOTHETICAL SYLLOGISM     DISJUNCTIVE SYLLOGISM
P → Q                      P ∨ Q
Q → R                      ¬P
─────                      ─────
∴ P → R                    ∴ Q

CONSTRUCTIVE DILEMMA       REDUCTIO AD ABSURDUM
P → Q                      Assume P
R → S                      ...
P ∨ R                      Derive contradiction
─────                      ─────
∴ Q ∨ S                    ∴ ¬P
```

### Invalid Forms (Fallacies)

```
AFFIRMING THE CONSEQUENT   DENYING THE ANTECEDENT
P → Q                      P → Q
Q                          ¬P
─────                      ─────
∴ P ✗ INVALID              ∴ ¬Q ✗ INVALID
```

---

## Predicate Logic

### Quantifiers

| Symbol | Name | Meaning |
|--------|------|---------|
| ∀x | Universal | For all x |
| ∃x | Existential | There exists x |

### Valid Inferences

```
UNIVERSAL INSTANTIATION    EXISTENTIAL GENERALIZATION
∀x(Fx)                     Fa
─────                      ─────
∴ Fa                       ∴ ∃x(Fx)

UNIVERSAL GENERALIZATION   EXISTENTIAL INSTANTIATION
(arbitrary a) Fa           ∃x(Fx)
─────                      ─────
∴ ∀x(Fx)                   ∴ Fa (for new constant a)
```

---

## Informal Fallacies

### Fallacies of Relevance

| Fallacy | Description | Example |
|---------|-------------|---------|
| Ad hominem | Attack the person | "You're wrong because you're stupid" |
| Appeal to authority | Irrelevant authority | "A celebrity says X" |
| Appeal to emotion | Manipulate feelings | Fear-mongering |
| Red herring | Change subject | Diverting attention |
| Straw man | Misrepresent argument | Attack weaker version |

### Fallacies of Presumption

| Fallacy | Description | Example |
|---------|-------------|---------|
| Begging the question | Assume conclusion | Circular reasoning |
| False dilemma | Only two options | "With us or against us" |
| Hasty generalization | Small sample | "Two Xs did Y, so all Xs" |
| Slippery slope | Unsupported chain | "A leads to Z inevitably" |

### Fallacies of Ambiguity

| Fallacy | Description | Example |
|---------|-------------|---------|
| Equivocation | Shifting meaning | "Light" (weight/illumination) |
| Amphiboly | Grammatical ambiguity | Headlines |
| Composition | Parts → whole | "Atoms invisible ∴ tables invisible" |
| Division | Whole → parts | "Team good ∴ each player good" |

---

## Paradoxes

### Liar Paradox

```
"This sentence is false"

If true → It says it's false → False
If false → It says it's false, which is true → True

RESPONSES:
├── Tarskian hierarchy: No self-reference
├── Paraconsistent logic: Accept contradiction
├── Gapping: Sentence is neither true nor false
└── Contextualism: Truth conditions shift
```

### Sorites Paradox (Heap)

```
1 grain is not a heap.
If n grains is not a heap, n+1 grains is not a heap.
∴ 1,000,000 grains is not a heap. ✗

RESPONSES:
├── Epistemicism: Sharp boundary, we don't know where
├── Supervaluationism: True under all precisifications
├── Degree theory: "Heap" admits degrees
└── Contextualism: Boundary shifts with context
```

### Russell's Paradox

```
R = {x : x ∉ x} (Set of all sets not members of themselves)

Is R ∈ R?
If yes → By definition, R ∉ R
If no → By definition, R ∈ R

RESPONSE: Type theory, set-theoretic axioms preventing
          unrestricted comprehension
```

---

## Modal Logic

### Basic Modal Operators

| Symbol | Meaning |
|--------|---------|
| □P | Necessarily P |
| ◊P | Possibly P |

### Relations

```
□P ↔ ¬◊¬P   (Necessary = not possibly not)
◊P ↔ ¬□¬P   (Possible = not necessarily not)
```

### Systems

| System | Characteristic Axiom |
|--------|---------------------|
| K | Basic modal logic |
| T | □P → P (Necessity implies truth) |
| S4 | □P → □□P (Iterated necessity) |
| S5 | ◊P → □◊P (Possibility is necessary) |

---

## Argument Analysis Protocol

```
ANALYZING ARGUMENTS
═══════════════════

1. IDENTIFY CONCLUSION
   What is being argued for?

2. IDENTIFY PREMISES
   What reasons are given?

3. SUPPLY HIDDEN PREMISES
   What's assumed but not stated?

4. EVALUATE VALIDITY
   Does conclusion follow?

5. EVALUATE SOUNDNESS
   Are premises true?

6. CHECK FOR FALLACIES
   Any reasoning errors?
```

---

## Key Vocabulary

| Term | Meaning |
|------|---------|
| Entailment | P logically implies Q |
| Tautology | True under all interpretations |
| Contradiction | False under all interpretations |
| Contingent | Neither tautology nor contradiction |
| Consistent | Can all be true together |
| Inference | Moving from premises to conclusion |
| Deduction | Conclusion follows necessarily |
| Induction | Conclusion follows probably |

---

## Integration with Repository

### Related Skills
- `argument-mapping`: Visualizing argument structure
- `thought-experiments`: Logical analysis of scenarios
