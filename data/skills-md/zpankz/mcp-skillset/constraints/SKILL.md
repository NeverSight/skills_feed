---
name: constraints
description: "Formal constraint theory unifying deontic logic (P/O/F/I operators), Juarrero's trichotomy (enabling/governing/constitutive), Hohfeldian rights (claim-duty, privilege-noright, power-liability, immunity-disability), and category-theoretic composition. Use when modelling permissions, obligations, prohibitions, rights structures, agent authority, governance systems, ontology validation, or any domain requiring formal constraint specification. Integrates with ontolog via λ-calculus mapping."
---

# Constraints

*Formal theory of constraints as structure-preserving functors over deontic modalities*

## Core Definition

A constraint is a **functor** mapping structural contexts to deontic outcomes:

```
C : (Σ × A) → Δ

Where:
  Σ = Simplicial complex (structural context from ontolog)
  A = Action/state space
  Δ = Deontic modality {P, O, F, I, ?}
```

Constraints shape **possibility spaces** without adding energy—they are **rate-independent** causes that determine what can happen without forcing any particular outcome.

## The Constraint Equation

```
C(σ, a) = δ ⟺ Within context σ, action a has deontic status δ
```

**Composition**: Constraints form a category with:
- Objects: Deontic positions
- Morphisms: Constraint transformations
- Identity: Trivial permission (P by default)
- Composition: Sequential constraint application

## Deontic Modalities (Δ)

Four fundamental operators from modal deontic logic:

| Operator | Symbol | Semantics | Dual |
|----------|--------|-----------|------|
| **Permitted** | P(a) | a is allowed | ¬F(a) |
| **Obligated** | O(a) | a is required | ¬P(¬a) |
| **Forbidden** | F(a) | a is prohibited | ¬P(a) |
| **Impossible** | I(a) | a cannot occur | ¬◇a |

**Axioms** (Standard Deontic Logic):
```
D: O(a) → P(a)           — Ought implies may
K: O(a→b) → (O(a)→O(b))  — Distribution
N: If ⊢a then ⊢O(a)      — Necessitation for tautologies

Interdefinitions:
P(a) ≡ ¬O(¬a)            — Permission as non-obligatory negation
F(a) ≡ O(¬a)             — Prohibition as obligated negation
```

## Constraint Trichotomy (Juarrero)

Constraints differ by **how they shape possibility**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONSTRAINT TRICHOTOMY                        │
├──────────────┬──────────────────────────────────────────────────┤
│   ENABLING   │ Creates new possibilities, opens pathways        │
│              │ Examples: catalysts, bridges, APIs, permissions   │
│              │ Effect: Expands action space                      │
│              │ Hohfeldian: Privilege, Power                      │
├──────────────┼──────────────────────────────────────────────────┤
│  GOVERNING   │ Regulates without participating, modulates rate  │
│              │ Examples: thermostats, regulatory genes, duties   │
│              │ Effect: Channels existing possibilities          │
│              │ Hohfeldian: Claim-Duty                            │
├──────────────┼──────────────────────────────────────────────────┤
│ CONSTITUTIVE │ Defines identity, creates closure                │
│              │ Examples: rules of chess, cell membranes, types  │
│              │ Effect: Determines what something IS             │
│              │ Hohfeldian: Immunity-Disability                   │
└──────────────┴──────────────────────────────────────────────────┘
```

**Causal flow**: Enabling → Constitutive → Governing
- Enabling constraints **induce** coherence
- Constitutive constraints **maintain** coherence  
- Governing constraints **regulate** coherent behaviour

## Hohfeldian Rights Structure

Eight fundamental jural positions in two squares:

### First-Order (Conduct)
```
    Claim ←─correlative─→ Duty
      ↕                     ↕
   opposite             opposite
      ↕                     ↕
  No-Right ←─correlative─→ Privilege
```

### Second-Order (Normative Change)
```
    Power ←─correlative─→ Liability
      ↕                     ↕
   opposite             opposite
      ↕                     ↕
 Disability ←─correlative─→ Immunity
```

**Position semantics**:

| Position | Definition | Constraint Type |
|----------|------------|-----------------|
| Claim | X has claim that Y φ | Governing |
| Duty | Y must φ toward X | Governing |
| Privilege | X may φ (no duty not to) | Enabling |
| No-Right | Y cannot demand X not φ | Enabling |
| Power | X can change Y's positions | Enabling |
| Liability | Y's positions changeable by X | Governing |
| Immunity | X's positions unchangeable by Y | Constitutive |
| Disability | Y cannot change X's positions | Constitutive |

**Correlative inference**: If X has Claim against Y, then Y has Duty to X (and vice versa).

## The KROG Theorem

Valid actions satisfy all constraint layers within governance:

```
Valid(a) ⟺ K(a) ∧ R(a) ∧ O(a) ∧ (a ∈ G)

Where:
  K(a) = Knowledge constraint (a is knowable/queryable)
  R(a) = Rights constraint (agent has right to a)
  O(a) = Obligation constraint (a satisfies duties)
  G    = Governance boundary (meta-rules)
```

**Implication**: No valid action can violate knowledge transparency, rights structure, obligation compliance, OR governance bounds.

## ontolog Integration

Constraints map to λ-calculus primitives:

| ontolog | Constraint Role | Mapping |
|---------|-----------------|---------|
| ο (base) | Constraint domain | Agents, states subject to C |
| λ (operation) | Constrained action | Actions C evaluates |
| τ (terminal) | Satisfied state | C(σ,a) = P ∨ O fulfilled |
| Σ (complex) | Context | Structural scope of C |
| H (holon) | Authority scope | Nested jurisdiction |

**Constraint as λ-abstraction**:
```
C = λσ.λa.δ    — Constraint abstracts context and action to modality
```

**Reduction**:
```
(C σ₀) a₀ →β δ₀    — Applying C to specific context and action yields modality
```

## Constraint Composition

### Logical Operations
```
C₁ ∧ C₂ : Both constraints must permit
C₁ ∨ C₂ : Either constraint permits
C₁ → C₂ : If C₁ permits, C₂ must permit
¬C      : Opposite constraint (correlative)
```

### Category-Theoretic Operations
```
C₁ ∘ C₂ : Sequential (C₂ then C₁)
C₁ ⊗ C₂ : Parallel independent
C₁ + C₂ : Coproduct (choice)
```

### Functor Laws
```
C(id) = id                    — Identity preservation
C(f ∘ g) = C(f) ∘ C(g)       — Composition preservation
```

## Temporal Extension

Constraints over time using temporal operators:

```
□C     : C holds always (invariant)
◇C     : C holds eventually
C U C' : C until C' (deadline)
○C     : C holds next (sequence)
```

**Common patterns**:
```
O(a) U t        — Obligated to do a before time t
□P(a)           — Always permitted to do a
F(a) U C(b)     — Forbidden until condition b claimed
```

## Rigidity Classification

| Rigidity | Can Change? | Ontological Type | Example |
|----------|-------------|------------------|---------|
| Constitutional | Never | Fundamental identity | "Persons have rights" |
| Static | By governance only | Kind, Category | Type definitions |
| Dynamic | By power holders | Role, Phase | Employment status |
| Contextual | By situation | Circumstantial | Weather-dependent rules |

## Validation Protocol

```python
def validate_constraint(C, σ, a):
    """Validate constraint application."""
    
    # 1. Scope check
    if not in_scope(a.agent, C.holon):
        return Invalid("Agent outside constraint scope")
    
    # 2. Context check
    if not C.domain.contains(σ):
        return Invalid("Context outside constraint domain")
    
    # 3. Modality check
    δ = C(σ, a)
    
    # 4. Correlative consistency
    for correlative in C.correlatives:
        if not consistent(δ, correlative(σ, a)):
            return Invalid("Correlative inconsistency")
    
    # 5. KROG theorem
    if not (K(a) and R(a) and O(a) and in_governance(a)):
        return Invalid("KROG violation")
    
    return Valid(δ)
```

## Inference Rules

### Correlative Inference
```
Claim(X, Y, φ)  ⊢  Duty(Y, X, φ)
Power(X, Y, φ)  ⊢  Liability(Y, X, φ)
```

### Transitivity (where applicable)
```
C(a, b) ∧ C(b, c) ∧ C.transitive  ⊢  C(a, c)
```

### Governing Propagation
```
Governing(C) ∧ C(parent, child) ∧ scope(H)  ⊢  C(parent, descendants(H))
```

### Constitutional Immutability
```
Constitutive(C)  ⊢  ¬◇modify(C)   — Constitutive constraints cannot be modified
```

## Quick Reference

### Constraint Declaration
```yaml
constraint:
  id: "hiring_authority"
  type: enabling
  modality: P
  domain: [Manager]
  action: hire
  scope: department_holon
  correlative: liability_to_be_hired
  rigidity: dynamic
```

### Hohfeldian Position Check
```
has_position(agent, position, target, action) → Boolean
correlative_of(position) → Position
opposite_of(position) → Position
```

### KROG Compliance
```
krog_valid(action) := K(action) ∧ R(action) ∧ O(action) ∧ G(action)
```

## File Structure

```
constraints/
├── SKILL.md              # This file
├── references/
│   ├── deontic.md        # Full deontic logic reference
│   ├── hohfeld.md        # Complete Hohfeldian analysis
│   └── composition.md    # Category-theoretic details
└── scripts/
    └── validate.py       # Constraint validation
```

## Integration Points

| Skill | Integration |
|-------|-------------|
| ontolog | ο/λ/τ mapping, Σ context, H scope |
| graph | Constraint edges, validation rules |
| reason | Constraint-guided branching bounds |
| agency | Agent authority via Hohfeldian positions |

---

**Core insight**: Constraints are not limitations imposed from outside but **structure-preserving functors** that shape possibility spaces. The trichotomy (enabling/governing/constitutive) combined with deontic modality (P/O/F/I) and Hohfeldian relational structure provides complete formal vocabulary for any rule-based system.
