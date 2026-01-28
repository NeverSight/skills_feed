---
name: learn
description: |
  Recursive self-improving holon λ(ο,Κ,Σ).τ' for knowledge compounding and schema evolution.
  USE WHEN learning, improving, optimizing, assessing, reflecting, debugging, synthesizing,
  or refining—whether human, AI, or organizational. Triggers on /learn, /compound, /improve,
  /refine, /optimize, /assess, /reflect, "lessons learned", "best practices", "continuous improvement".
  Preserves Κ-monotonicity, η≥4, homoiconicity.
allowed-tools: Read, Write, Edit, Grep, Glob, WebSearch, WebFetch
model: sonnet
context: fork
agent: knowledge-domain-agent
user-invocable: true
---

<!-- Extended Metadata (non-official, preserved for framework compatibility) -->
<!-- ο.class: "occurrent" | ο.mode: "independent" -->
<!-- λ.in: lambda-skill | λ.out: 1-parse, INDEX | λ.kin: schema, lambda-compound -->
<!-- τ.goal: compound knowledge; preserve η≥4, Κ-monotonicity -->

# Learn

> λ(ο,Κ,Σ).τ' — Knowledge compounds, schema evolves.

## Navigation

[INDEX](INDEX.md) | [schema](schema.yaml)

**Concepts**: [homoiconicity](concepts/homoiconicity.md), [compound-interest](concepts/compound-interest.md), [topology](concepts/topology-invariants.md), [vertex-sharing](concepts/vertex-sharing.md), [convergence](concepts/convergence.md), [fixed-point](concepts/fixed-point.md)

**Phases**: [1-parse](phases/1-parse.md) → [2-route](phases/2-route.md) → [3-execute](phases/3-execute.md) → [4-assess](phases/4-assess.md) → [5-refactor](phases/5-refactor.md) → [6-compound](phases/6-compound.md) → [7-renormalize](phases/7-renormalize.md)

**Domains**: [learning](domains/learning.md), [coding](domains/coding.md), [research](domains/research.md), [writing](domains/writing.md), [meta](domains/meta.md)

**Related Skills**: [λ (lambda-skill)](../lambda-skill/SKILL.md) — shares compound loop, topology validation, vertex-sharing

## Pipeline

```
ο → PARSE → ROUTE → EXECUTE → ASSESS → REFACTOR → COMPOUND → RENORMALIZE → τ'
```

[PARSE](phases/1-parse.md) → [ROUTE](phases/2-route.md) → [EXECUTE](phases/3-execute.md) → [ASSESS](phases/4-assess.md) → [REFACTOR](phases/5-refactor.md) → [COMPOUND](phases/6-compound.md) → [RENORMALIZE](phases/7-renormalize.md)

## Invariants

| Invariant | Expression | Reference |
|-----------|------------|-----------|
| Κ-monotonicity | `len(Κ') ≥ len(Κ)` | [knowledge-monotonicity](concepts/knowledge-monotonicity.md) |
| Topology | `η ≥ 4` | [topology-invariants](concepts/topology-invariants.md) |
| Homoiconicity | `Σ.can_process(Σ)` | [homoiconicity](concepts/homoiconicity.md) |
| Integration | `shared_vertices ≠ ∅` | [vertex-sharing](concepts/vertex-sharing.md) |

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **Parse** | "extract intent", "understand request" | `phases/1-parse.md` |
| **Route** | "classify complexity", "select pipeline" | `phases/2-route.md` |
| **Execute** | "apply skills", "run pipeline" | `phases/3-execute.md` |
| **Assess** | "evaluate outcome", "measure quality" | `phases/4-assess.md` |
| **Refactor** | "improve structure", "optimize" | `phases/5-refactor.md` |
| **Compound** | "extract learnings", "crystallize" | `phases/6-compound.md` |
| **Renormalize** | "prune noise", "compress" | `phases/7-renormalize.md` |

## Examples

**Example 1: After debugging session**
```
User: "That fixed the auth bug. Let's capture what we learned."
→ Invokes Compound phase
→ Extracts: symptom, root cause, solution, prevention
→ Crystallizes learning with vertex-sharing to PKM
→ Returns: Learning artifact saved to K
```

**Example 2: Skill improvement**
```
User: "/learn improve the grounding-router skill"
→ Invokes full pipeline: Parse → Route (R2) → Execute → Assess → Refactor
→ Applies topology validation (η≥4)
→ Returns: Improved skill with preserved invariants
```

**Example 3: Reflection on session**
```
User: "/reflect on this coding session"
→ Invokes Assess → Compound → Renormalize
→ Extracts patterns, antipatterns, principles
→ Returns: Session learnings integrated into K
```

## Integration with λ (lambda-skill)

This skill extends [lambda-skill](../lambda-skill/SKILL.md) with:
- **Additional phases**: Assess, Refactor, Renormalize (beyond λ's 6 stages)
- **Schema evolution**: Σ→Σ' (λ only evolves K)
- **Shared invariants**: η≥4, KROG, vertex-sharing

```haskell
-- λ (lambda) core
λ(ο,K).τ = emit ∘ validate ∘ compose ∘ execute(K) ∘ route ∘ parse

-- Learn extends with schema evolution
λ(ο,Κ,Σ).τ' = renormalize ∘ compound ∘ refactor ∘ assess ∘ execute ∘ route ∘ parse
```

## Quick Reference

```haskell
λ(ο,Κ,Σ).τ'    Parse→Route→Execute→Assess→Refactor→Compound→Renormalize
Κ grows        Σ evolves        η≥4 preserved        vertex-sharing enforced
```

