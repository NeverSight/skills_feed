---
name: urf
description: "Universal Reasoning Framework implementing λο.τ calculus over holarchic structures. Provides severity-based routing (R0-R3 pipelines), modular cognitive architecture (DEC, EVL, PAT, SYN, MEA, HYP, INT), fractal execution patterns, multi-level validation (η≥4, KROG), and adaptive learning. Triggers on: (1) complex multi-step reasoning, (2) high-stakes decisions requiring validation, (3) research synthesis across domains, (4) system design and architecture, (5) crisis management, (6) performance optimization. Implements scale-invariant reasoning from micro (tool calls) through meso (skill composition) to macro (orchestrated workflows)."
---

# Universal Reasoning Framework (URF)

## λο.τ Universal Form

```
λ : Operation     — The transformation
ο : Base          — Input entity  
τ : Terminal      — Target output

λο.τ : Base → Terminal via Operation
```

**Composition Operators:**
```haskell
(∘) : sequential   — (λ₁ ∘ λ₂)ο = λ₁(λ₂(ο))
(⊗) : parallel     — (λ₁ ⊗ λ₂)ο = (λ₁(ο), λ₂(ο))
(*) : recursive    — fix(λ) = λ(fix(λ))
(|) : conditional  — (λ | c)ο = Just(λ(ο)) if c(ο) else Nothing
```

## Π-Classification

Classify every query before execution:

| Score | Pipeline | Holons | Tools | Validation | τ-Form |
|-------|----------|--------|-------|------------|--------|
| <2 | **R0** | ∅ | ∅ | ∅ | ≤2 sentences |
| 2-4 | **R1** | `{ρ}∨{θ}` | optional | implicit | 1-2¶ |
| 4-8 | **R2** | `{γ,η}∪{ρ,θ}` | infranodus | `η≥4` | mechanistic |
| ≥8 | **R3** | `Σ` (all) | all | `KROG∧η≥4∧PSR` | comprehensive |

**Score Calculation:**
```python
score = (
    len(domains) * 2 +          # Multi-domain bonus
    reasoning_depth * 3 +       # Deep reasoning weight
    (1.5 if high_stakes else 1.0) +  # Safety multiplier
    (2 if requires_verification else 0)  # Recency/fact-check
)
```

**Auto-Escalation Triggers:**
- Verification requests (`"latest"`, `"current"`, `"2025"`) → **R3**
- Trivial factual (`"What is..."`, `"Define..."`) → **R0**
- Medical/legal stakes → score × 1.5

## Σ-Complex (Module Registry)

| Symbol | Module | Signature | When to Use |
|--------|--------|-----------|-------------|
| `ρ` | reason | `parse→branch→reduce→ground→emit` | Any reasoning |
| `θ` | think | `thoughtbox ⊗ mental_models ⊗ notebook` | Cognitive enhancement |
| `ω` | ontolog | `simplices→homology→sheaves` | Formal structures |
| `γ` | graph | `extract→compress→validate(η≥4)` | Knowledge graphs |
| `η` | hierarchical | `strategic→tactical→operational` | Multi-scale problems |
| `κ` | critique | `thesis→antithesis→synthesis` | Dialectical refinement |
| `α` | agency | `observe→reason→plan→act→reflect` | Task execution |
| `ν` | non-linear | `orchestrator⊗workers→checkpoint` | Uncertainty handling |
| `β` | abduct | `detect→infer→refactor→validate` | Schema optimization |
| `χ` | constraints | `KROG: K∧R∧O∧G` | Governance validation |

**Edge Registry (Composition Patterns):**
```
(ρ, θ): ∘   # reason feeds think
(θ, ω): ∘   # think grounds in ontolog
(ω, ρ): ∘   # ontolog constrains reason
(γ, η): ⊗   # graph parallel hierarchical
(κ, β): ∘   # critique feeds abduct
(β, κ): *   # recursive refinement
(α, ν): ∘   # agency orchestrates non-linear
(ν, χ): |   # non-linear conditional on constraints
```

## Ψ-Execution Patterns

### R0: Direct Response
```python
λR0 = id  # Identity transformation, <100ms
```

### R1: Single Skill
```python
λR1 = ρ.emit ∘ ρ.ground ∘ ρ.reduce ∘ ρ.parse
# parse→branch→reduce→ground→emit
```

### R2: Skill Composition
```python
λR2 = (
    validate(η≥4) ∘ 
    γ.compress ∘ 
    (γ.extract ⊗ η.decompose) ∘ 
    ρ.parse
)
```

### R3: Full Orchestration
```python
λR3 = (
    χ.validate(KROG) ∘
    β.refactor ∘
    κ.synthesize ∘
    (ρ ⊗ θ ⊗ ω).parallel ∘
    κ.thesis ∘
    ν.orchestrate ∘
    α.observe
)
```

## Γ-Topology Invariants

**Required Metrics:**
```python
TARGETS = {
    "η": ("|E|/|V|", "≥", 4.0),      # Density ratio
    "ζ": ("cycles", "=", 0),         # Acyclicity
    "κ": ("clustering", ">", 0.3),   # Small-world
    "φ": ("isolated", "<", 0.2),     # Connectivity
}
```

**Validation:**
```python
def validate(graph) -> bool:
    return (
        graph.edges / graph.nodes >= 4.0 and  # η ≥ 4
        not has_cycles(graph) and              # ζ = 0
        clustering_coefficient(graph) > 0.3 and  # κ > 0.3
        isolated_ratio(graph) < 0.2            # φ < 0.2
    )
```

**Remediation Actions:**
- `η < 4`: invoke `infranodus:getGraphAndAdvice` with `optimize="gaps"`
- `ζ > 0`: invoke `abduct.refactor` with `cycle_breaking=True`
- `κ < 0.3`: invoke `graph.add_triangulation`
- `φ > 0.2`: invoke `graph.connect_orphans`

## χ-Constraints (KROG Theorem)

```
Valid(λ) ⟺ K(λ) ∧ R(λ) ∧ O(λ) ∧ G(λ)

K (Knowable):    Effects transparent, auditable
R (Rights):      Agent has authority over domain
O (Obligations): All duties satisfied
G (Governance):  Within meta-bounds
```

**Constraint Trichotomy:**

| Type | Effect | Rigidity |
|------|--------|----------|
| **Enabling** | Expands action space | Dynamic |
| **Governing** | Channels possibilities | Static |
| **Constitutive** | Defines identity | Immutable |

## Execution Lifecycle

```
1. RECEIVE    → Parse query components
2. CLASSIFY   → Score → Pipeline selection
3. LOAD       → Memories + PKM + Context
4. ROUTE      → Activate appropriate holons
5. REASON     → Strategic→Tactical→Operational
6. GROUND     → Gather evidence, verify premises
7. COMPOSE    → Synthesize outputs from holons
8. VALIDATE   → Check invariants (η≥4, KROG)
9. SYNTHESIZE → Format per pipeline τ-form
10. PERSIST   → Update memories if new facts
11. EMIT      → Deliver response
```

**Convergence Detection:**
```python
def converged(state, previous, pipeline) -> bool:
    similarity = (
        0.5 * cosine(state.strategic, previous.strategic) +
        0.3 * cosine(state.tactical, previous.tactical) +
        0.2 * cosine(state.operational, previous.operational)
    )
    thresholds = {R1: 0.85, R2: 0.92, R3: 0.96}
    return similarity > thresholds[pipeline]
```

## Φ-Formatting Axioms

1. **PROSE_PRIMACY**: Organic paragraphs; lists only when requested
2. **TELEOLOGY_FIRST**: Why → How → What
3. **MECHANISTIC_TRACE**: Explicit causal chains `A → B → C`
4. **UNCERTAINTY_HONEST**: State confidence, acknowledge gaps
5. **MINIMAL_FORMATTING**: Headers/bullets only when structurally necessary

**Token Scaling:**

| Pipeline | Tokens | Form |
|----------|--------|------|
| R0 | ≤50 | 1-2 sentences |
| R1 | 100-300 | 1-2 paragraphs |
| R2 | 300-800 | Mechanistic explanation |
| R3 | 500-2000 | Comprehensive synthesis |

## Integration Points

**Tool Selection:**
```python
TOOL_MAP = {
    "current_info": ["exa:web_search", "scholar-gateway"],
    "graph_analysis": ["infranodus:getGraphAndAdvice"],
    "extended_reasoning": ["clear-thought", "atom-of-thoughts"],
    "workflow": ["rube", "n8n"],
    "memory": ["supermemory", "limitless"],
}
```

**Skill Composition:**
```
urf → hierarchical-reasoning   # Multi-level reasoning
urf → knowledge-graph          # Graph operations
urf → ontolog                  # Formal structures
urf → abduct                   # Schema optimization
urf → critique                 # Dialectical synthesis
```

## Emergency Protocols

**Severity Escalation:**
```
DEFCON_5 (Normal):   All systems nominal
DEFCON_4 (Elevated): Minor anomalies, increased monitoring
DEFCON_3 (High):     Multiple anomalies, active mitigation
DEFCON_2 (Severe):   System-wide issues, emergency protocols
DEFCON_1 (Critical): Total failure imminent, crisis mode
```

**Override Codes:**
- `HALT`: Immediate stop → Recovery procedures
- `ROLLBACK`: Undo to last safe state
- `ESCALATE`: Bump severity + external help
- `BYPASS`: Skip validation (CRITICAL only, requires KROG override)

## References

- [references/modules.md](references/modules.md) - Full module specifications
- [references/validation.md](references/validation.md) - QA systems and invariants
- [references/emergency.md](references/emergency.md) - Crisis protocols
- [references/performance.md](references/performance.md) - Optimization strategies
- [references/meta.md](references/meta.md) - Meta-framework governance

## Quick Reference

```
λο.τ                    Universal form
η = |E|/|V| ≥ 4         Topology target
KROG = K∧R∧O∧G          Constraint validation
R0 < R1 < R2 < R3       Pipeline escalation

∘ sequential | ⊗ parallel | * recursive | | conditional

parse→branch→reduce→ground→emit     (reason)
strategic→tactical→operational       (hierarchical)
thesis→antithesis→synthesis          (critique)
observe→reason→plan→act→reflect      (agency)
```
