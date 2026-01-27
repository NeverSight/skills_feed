---
name: atomise
description: "Atom of Thoughts (AoT) reasoning - decompose complex problems into atomic units with confidence tracking and backtracking. For genuinely complex reasoning, not everyday questions. Triggers on: atomise, complex reasoning, decompose problem, structured thinking, verify hypothesis."
allowed-tools: "Read"
compatibility: "Pure reasoning framework, no external dependencies."
depends-on: []
related-skills: []
---

# Atomise - Atom of Thoughts Reasoning

Decompose complex problems into minimal, verifiable "atoms" of thought. Unlike chain-of-thought (linear, error-accumulating), AoT treats each step as independently verifiable and backtracks when confidence drops.

**Use for:** Security analysis, architectural decisions, complex debugging, multi-step proofs.
**Don't use for:** Simple questions, trivial calculations, information lookup.

```
/atomise "<problem>" [--light | --deep] [--math | --code | --security | --design]
```

---

## The Core Loop

```
1. DECOMPOSE -> Break into atomic subquestions (1-2 sentences each)
2. SOLVE     -> Answer leaf nodes first, propagate up
3. VERIFY    -> Test each hypothesis (counterexample, consistency, domain check)
4. CONTRACT  -> Summarize verified state in 2 sentences (drop history)
5. EVALUATE  -> Confident enough? Done. Too uncertain? Backtrack and try another path.
```

Repeat until confident or all paths exhausted.

---

## Atoms

Each atom is a minimal unit:

```
{id, type, content, depends_on[], confidence, verified}
```

| Type | Purpose | Starting Confidence |
|------|---------|---------------------|
| **premise** | Given facts | 1.0 |
| **reasoning** | Logical inference | Inherited from parents |
| **hypothesis** | Claim to test | Max 0.7 until verified |
| **verification** | Test result | Based on test outcome |
| **conclusion** | Final answer | Propagated from chain |

**Confidence propagates:** A child can't be more confident than its least-confident parent.

---

## Confidence (Honest Caveat)

These numbers are *heuristic*, not calibrated probabilities. They're useful for tracking relative certainty, not for actual risk assessment.

| Threshold | Meaning |
|-----------|---------|
| **> 0.85** | Confident enough to conclude |
| **0.6 - 0.85** | Needs more verification |
| **< 0.6** | Decompose further or backtrack |
| **< 0.5** | Backtrack - this path isn't working |

**Verification adjusts confidence:**
- Confirmed -> maintain or slight boost
- Partial -> reduce ~15%
- Refuted -> major reduction, likely backtrack

---

## Modes

**Depth:**
- `--light` - Fast: max 3 levels, 0.70 confidence threshold
- *(default)* - Standard: max 5 levels, 0.85 threshold
- `--deep` - Exhaustive: max 7 levels, 0.90 threshold

**Domain** (adjusts verification style):
- `--math` - Arithmetic checks, proof validation, boundary tests
- `--code` - Type checking, invariant verification, test generation
- `--security` - Threat modeling, attack surface, adversarial thinking
- `--design` - Tradeoff analysis, constraint satisfaction, feasibility

---

## Output

```
ANSWER: {result}
CONFIDENCE: {0.0-1.0} - {why}

KEY CHAIN: P1 -> R1 -> H1 -> V1 -> C1

ATOMS:
| id | type | content | conf | verified |
|----|------|---------|------|----------|
| P1 | premise | Given: ... | 1.0 | Y |
| R1 | reasoning | Therefore: ... | 0.95 | Y |
| ... | ... | ... | ... | ... |

RISKS: {what could change this}
```

Add `--verbose` for full trace, `--quiet` for just the answer.

---

## Execution Guide

### Phase 0: Setup

1. **Restate** the problem in one sentence
2. **Extract premises** as atoms (given facts = 1.0, assumptions = 0.6)
3. **Sketch approaches:** Direct solve? Decompose? Reframe? Pick best.

### Phase 1+: Iterate

1. **Atomicity gate:** Can you answer from verified atoms? Yes -> solve. No -> decompose.
2. **Decompose:** Build dependency tree of atomic subquestions
3. **Solve + Verify:** Leaves first, propagate up. Every hypothesis needs verification.
4. **Contract:** Summarize in <=2 sentences. Drop everything else.
5. **Evaluate:**
   - Confident? -> Terminate
   - Uncertain but viable? -> Continue
   - Low confidence? -> Backtrack, try alternative

### Backtracking

When a path yields confidence < 0.5 after verification:
1. Prune that branch
2. Restore to last contracted state
3. Try alternative from initial sketch

---

## Examples

```bash
# Complex debugging
/atomise "Why does this function return null on the second call?" --code

# Security review
/atomise "Is this authentication flow vulnerable to session fixation?" --security

# Architecture decision
/atomise "Should we use event sourcing for this domain?" --deep --design

# Quick decision (light mode)
/atomise "Redis vs Memcached for this cache layer?" --light
```

---

## Anti-Patterns

```
BAD:  /atomise "What's 2+2?"           -> Just answer it
BAD:  /atomise "Rewrite this function" -> That's implementation, not reasoning
BAD:  Forcing conclusion despite low confidence -> Let it backtrack
GOOD: /atomise for genuine uncertainty requiring structured decomposition
```

---

## Remember

1. **Atomic = minimal.** 1-2 sentences per atom.
2. **Verify everything.** Hypotheses need tests.
3. **Contract aggressively.** Keep only what's needed for next step.
4. **Backtrack freely.** Low confidence means try another path.
5. **Confidence is heuristic.** Useful for structure, not actual probabilities.
