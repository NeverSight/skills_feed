---
name: critique
description: Multi-perspective dialectical reasoning with cross-evaluative synthesis. Spawns parallel evaluative lenses (STRUCTURAL, EVIDENTIAL, SCOPE, ADVERSARIAL, PRAGMATIC) that critique thesis AND critique each other's critiques, producing N-squared evaluation matrix before recursive aggregation. Triggers on /critique, /dialectic, /crosseval, requests for thorough analysis, stress-testing arguments, or finding weaknesses. Implements Hegelian refinement enhanced with interleaved multi-domain evaluation and convergent synthesis.
---

# Critique: Multi-Lens Dialectical Refinement

Execute adversarial self-refinement through parallel evaluative lenses with cross-evaluation and recursive aggregation.

## Architecture

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                         DIALECTIC ENGINE v3                                  │
├──────────────────────────────────────────────────────────────────────────────┤
│  Φ0: CLASSIFY    → complexity assessment, mode selection, lens allocation    │
│  Φ1: THESIS      → committed position with claim DAG                         │
│  Φ2: MULTI-LENS  → N lenses evaluate thesis (N critiques)                    │
│      ANTITHESIS    + each lens evaluates others (N×(N-1) cross-evals)        │
│                    = N² total evaluation cells                               │
│  Φ3: AGGREGATE   → consensus/contested/unique extraction                     │
│      SYNTHESIS     + recursive compression passes → single output            │
│  Φ4: CONVERGE    → stability check, iterate or finalize                      │
└──────────────────────────────────────────────────────────────────────────────┘

PHASE DEPENDENCIES:
  Φ0 ──► Φ1 ──► Φ2a ──► Φ2b ──► Φ3 ──► Φ4
              (initial)  (cross)      │
                                      └──► Φ1 (if ITERATE)
```

## Mode Selection

### Automatic Mode Detection

```python
def select_mode(query: str) -> Mode:
    """
    Select critique depth based on query characteristics.
    
    QUICK:  Simple claims, factual questions, narrow scope
    STANDARD: Moderate complexity, clear domain, some nuance
    FULL:   Complex arguments, multiple stakeholders, high stakes
    """
    indicators = {
        "quick": [
            len(query) < 200,
            single_claim(query),
            factual_verifiable(query),
            low_controversy(query)
        ],
        "full": [
            len(query) > 1000,
            multi_stakeholder(query),
            ethical_implications(query),
            policy_recommendation(query),
            high_stakes_decision(query)
        ]
    }
    
    if sum(indicators["quick"]) >= 3:
        return Mode.QUICK
    elif sum(indicators["full"]) >= 2:
        return Mode.FULL
    else:
        return Mode.STANDARD
```

### Mode Specifications

| Mode | Lenses | Cross-Eval | Cycles | Threshold | Token Budget |
|------|--------|------------|--------|-----------|--------------|
| QUICK | 3 (S,E,A) | None | 1 | 0.85 | ~800 |
| STANDARD | 5 (all) | Selective (10 cells) | 2 | 0.92 | ~2000 |
| FULL | 5 (all) | Complete (25 cells) | 3 | 0.96 | ~4000 |

### Manual Triggers

| Trigger | Mode | Description |
|---------|------|-------------|
| `/critique` | Auto-detect | Intelligent mode selection |
| `/critique-quick` | QUICK | Fast, 3-lens, no cross-eval |
| `/critique-standard` | STANDARD | Balanced, selective cross-eval |
| `/critique-full` | FULL | Complete N² analysis |
| `/crosseval` | FULL | Emphasis on Φ2b matrix |
| `/aggregate` | FULL | Emphasis on Φ3 synthesis |

## Evaluative Lenses

Five orthogonal perspectives designed for comprehensive coverage with minimal overlap:

| Lens | Code | Domain | Core Question | Orthogonality Rationale |
|------|------|--------|---------------|-------------------------|
| STRUCTURAL | S | Logic & coherence | Is reasoning valid? | Form vs content |
| EVIDENTIAL | E | Evidence & epistemology | What justifies belief? | Justification type |
| SCOPE | O | Boundaries & generality | Where does this apply? | Domain limits |
| ADVERSARIAL | A | Opposition & alternatives | What's the best counter? | External challenge |
| PRAGMATIC | P | Application & consequence | Does this work? | Theory vs practice |

### Lens Independence Validation

Lenses target distinct failure modes:
- **S** catches: invalid inference, circular reasoning, equivocation
- **E** catches: weak evidence, unfalsifiable claims, cherry-picking
- **O** catches: overgeneralization, edge cases, context dependence
- **A** catches: stronger alternatives, unconsidered objections
- **P** catches: implementation barriers, unintended consequences

Overlap detection: If two lenses identify the same issue, it's either a genuine high-priority concern (reinforce) or a lens calibration problem (investigate).

## Execution Protocol

### Φ0: Classification & Mode Selection

```python
def classify_and_configure(query: str) -> Config:
    mode = select_mode(query)
    
    configs = {
        Mode.QUICK: {
            "lenses": ["S", "E", "A"],
            "cross_eval": False,
            "cycles": 1,
            "threshold": 0.85,
            "token_budget": 800
        },
        Mode.STANDARD: {
            "lenses": ["S", "E", "O", "A", "P"],
            "cross_eval": "selective",  # 10 highest-value cells
            "cycles": 2,
            "threshold": 0.92,
            "token_budget": 2000
        },
        Mode.FULL: {
            "lenses": ["S", "E", "O", "A", "P"],
            "cross_eval": "complete",   # All 25 cells
            "cycles": 3,
            "threshold": 0.96,
            "token_budget": 4000
        }
    }
    
    return Config(**configs[mode], mode=mode)
```

**Output**: `[CRITIQUE:Φ0|mode={m}|lenses={n}|cross={type}|budget={t}]`

### Φ1: Thesis Generation

Generate committed response with explicit claim DAG.

**Requirements**:
1. State positions with **falsifiable specificity**
2. Build claim graph with stability ordering:
   - `F` (FOUNDATIONAL) — axioms, definitions (immutable after Φ1)
   - `S` (STRUCTURAL) — derived claims (attackable)
   - `P` (PERIPHERAL) — applications (most vulnerable)
3. Verify acyclicity (DAG enforcement)
4. Compute initial topology metrics

**Schema**:
```yaml
thesis:
  response: "{Complete committed response}"
  claims:
    - id: C1
      content: "{Specific falsifiable claim}"
      stability: F|S|P
      supports: [C2, C3]
      depends_on: []
      confidence: 0.0-1.0
      evidence_type: empirical|logical|definitional|analogical
  topology:
    nodes: {n}
    edges: {e}
    density: {e/n}  # Target ≥2.0
    cycles: 0       # Must be 0 (enforced)
  aggregate_confidence: 0.0-1.0
  completion_marker: "Φ1_COMPLETE"  # Required for Φ2 to proceed
```

**Output**: `[CRITIQUE:Φ1|claims={n}|edges={e}|η={density}|conf={c}|✓]`

### Φ2: Multi-Lens Antithesis

#### Φ2a: Initial Lens Evaluations

**Prerequisite**: `Φ1.completion_marker == "Φ1_COMPLETE"`

Each lens independently evaluates thesis using attack vectors:

```yaml
# STRUCTURAL lens attacks
structural:
  - non_sequitur: "Conclusion does not follow from premises"
  - circular_reasoning: "Conclusion presupposed in premises"
  - false_dichotomy: "Excluded middle options"
  - equivocation: "Term shifts meaning mid-argument"

# EVIDENTIAL lens attacks  
evidential:
  - insufficient_evidence: "Claim exceeds evidential support"
  - cherry_picking: "Counter-evidence unaddressed"
  - unfalsifiable: "No possible disconfirming evidence"
  - correlation_causation: "Causal claim from correlational data"

# SCOPE lens attacks
scope:
  - overgeneralization: "Specific case → universal claim"
  - edge_case: "Valid boundary defeats universal"
  - context_dependence: "Unstated contextual requirements"

# ADVERSARIAL lens attacks
adversarial:
  - steel_man: "Strongest form of opposition"
  - alternative_explanation: "Competing hypothesis equally plausible"
  - precedent_contradiction: "Accepted instance defeats thesis"

# PRAGMATIC lens attacks
pragmatic:
  - implementation_barrier: "Cannot be executed as stated"
  - unintended_consequence: "Second-order effects harmful"
  - scaling_failure: "Works small, fails large"
```

**Per-lens output**:
```yaml
lens_evaluation:
  lens: S|E|O|A|P
  attacks:
    - target: C{id}
      type: "{attack_vector}"
      content: "{Specific critique}"
      severity: fatal|major|minor|cosmetic
      confidence_impact: -0.0 to -1.0
  summary_score: 0.0-1.0
  completion_marker: "Φ2a_{lens}_COMPLETE"
```

**Completion Gate**: All lenses must have `completion_marker` before Φ2b proceeds.

#### Φ2b: Cross-Lens Evaluation

**Prerequisite**: All `Φ2a_{lens}_COMPLETE` markers present

**QUICK mode**: Skip Φ2b entirely

**STANDARD mode**: Evaluate 10 highest-value cells:
- High-severity attacks from each lens (5 cells)
- Highest-confidence attacks cross-checked by adjacent lens (5 cells)

**FULL mode**: Complete 5×5 matrix (25 cells, minus 5 diagonal = 20 evaluations)

```
Cross-evaluation matrix:
    │  S eval │  E eval │  O eval │  A eval │  P eval │
────┼─────────┼─────────┼─────────┼─────────┼─────────┤
S → │    —    │   S→E   │   S→O   │   S→A   │   S→P   │
E → │   E→S   │    —    │   E→O   │   E→A   │   E→P   │
O → │   O→S   │   O→E   │    —    │   O→A   │   O→P   │
A → │   A→S   │   A→E   │   A→O   │    —    │   A→P   │
P → │   P→S   │   P→E   │   P→O   │   P→A   │    —    │
```

**Cross-eval output**:
```yaml
cross_evaluation:
  evaluator: S|E|O|A|P
  evaluated: S|E|O|A|P
  verdict: endorse|partial|reject
  agreements: ["{attack_ids}"]
  disagreements:
    - attack: "{attack_id}"
      objection: "{Why evaluator disagrees}"
  missed: ["{What evaluator would add}"]
  calibration: "{Over/under severity assessment}"
```

**Output**: `[CRITIQUE:Φ2|mode={m}|attacks={n}|cross={cells}|✓]`

### Φ3: Aggregation & Synthesis

#### Phase 3a: Matrix Analysis

```python
def analyze_matrix(all_attacks: list, cross_evals: Matrix) -> Analysis:
    # Consensus: ≥80% lenses agree
    consensus = [a for a in all_attacks if agreement_rate(a) >= 0.80]
    
    # Contested: 40-79% agreement
    contested = [a for a in all_attacks if 0.40 <= agreement_rate(a) < 0.80]
    
    # Unique: Single lens, but cross-eval endorsed
    unique = [a for a in all_attacks 
              if source_count(a) == 1 and cross_endorsed(a)]
    
    # Rejected: <40% agreement AND cross-eval rejection
    rejected = [a for a in all_attacks 
                if agreement_rate(a) < 0.40 and cross_rejected(a)]
    
    return Analysis(consensus, contested, unique, rejected)
```

#### Phase 3b: Conflict Resolution

For contested items:

```python
def resolve_contested(contested: list, matrix: Matrix) -> list:
    resolutions = []
    for attack in contested:
        support_weight = sum(credibility(s) for s in supporters(attack))
        oppose_weight = sum(credibility(o) for o in opposers(attack))
        
        if support_weight > oppose_weight * 1.5:
            resolution = "ADOPT"
        elif oppose_weight > support_weight * 1.5:
            resolution = "REJECT"
        else:
            resolution = "CONDITIONAL"
        
        resolutions.append(Resolution(attack, resolution, rationale(attack)))
    return resolutions
```

#### Phase 3c: Recursive Compression

```
Pass 1: Apply consensus → Core modifications (mandatory)
Pass 2: Apply contested → Conditional modifications (with qualifications)
Pass 3: Apply unique → Enhancement layer (optional enrichment)
Pass 4: Validate coherence → If failed, re-compress with tighter constraints
```

**Maximum compression passes**: 4 (prevent infinite recursion)

**Synthesis output**:
```yaml
synthesis:
  response: "{Refined response}"
  modifications:
    from_consensus: [{claim, action, rationale}]
    from_contested: [{claim, action, condition}]
    from_unique: [{claim, enhancement}]
  rejected_attacks: [{attack, rejection_rationale}]
  residual_uncertainties: [{uncertainty, disagreeing_lenses, impact}]
  confidence:
    initial: {Φ1}
    final: {post-synthesis}
```

**Output**: `[CRITIQUE:Φ3|consensus={n}|contested={n}|unique={n}|rejected={n}|conf={f}]`

### Φ4: Convergence Check

**Convergence Formula**:
```python
convergence = (
    0.30 * semantic_similarity(Φ1, Φ3) +
    0.25 * graph_similarity(Φ1.claims, Φ3.claims) +
    0.25 * confidence_stability(Φ1.conf, Φ3.conf) +
    0.20 * consensus_rate(Φ3.consensus / total_attacks)
)
```

**Threshold Justification**:
- 0.85 (QUICK): Acceptable for low-stakes, rapid iteration
- 0.92 (STANDARD): Balances thoroughness with efficiency
- 0.96 (FULL): High confidence required for complex/high-stakes

**Outcomes**:
- `CONVERGED`: Score ≥ threshold → output Φ3 synthesis
- `ITERATE`: Score < threshold AND cycles < max → Φ3 becomes new Φ1
- `EXHAUSTED`: Cycles exhausted → output Φ3 with uncertainty report

**Output**: `[CRITIQUE:Φ4|conv={score}|{STATUS}|iter={n}/{max}]`

## Graceful Degradation

When resources constrained (token budget, time pressure):

```
FULL → interrupt → Continue as STANDARD
STANDARD → interrupt → Continue as QUICK
QUICK → interrupt → Output best available synthesis with uncertainty flag
```

**Degradation markers**:
```yaml
degraded_output:
  original_mode: FULL
  actual_mode: STANDARD
  skipped_phases: [Φ2b_partial]
  confidence_penalty: -0.1
  recommendation: "Re-run in FULL mode for complete analysis"
```

## Compact Output Mode

```
[CRITIQUE|mode={m}|L={lenses}|c={cycle}/{max}]
[Φ1|n{claims}|e{edges}|η{density}|conf{c}|✓]
[Φ2|attacks{n}|cross{cells}|S:{s}|E:{e}|O:{o}|A:{a}|P:{p}|✓]
[Φ3|consensus{n}|contested{n}|unique{n}|rejected{n}|✓]
[Φ4|conv{score}|{STATUS}|conf{initial}→{final}]

SYNTHESIS: {2-3 sentence refined conclusion}
KEY_CHANGES: {Most significant modifications from Φ1}
RESIDUAL: {Primary unresolved uncertainty, if any}
```

## Meta-Cognitive Markers

```
[CLASSIFYING]  — Φ0: determining mode and resources
[COMMITTING]   — Φ1: stating without hedge
[LENS:X]       — Φ2a: evaluating from lens X perspective
[CROSS:X→Y]    — Φ2b: lens X evaluating lens Y's critique
[CONSENSUS]    — Φ3a: noting cross-lens agreement
[CONTESTED]    — Φ3a: noting genuine disagreement
[RESOLVING]    — Φ3b: applying resolution protocol
[COMPRESSING]  — Φ3c: recursive synthesis pass
[CONVERGING]   — Φ4: stability detected
[DEGRADING]    — Resource constraint, reducing scope
```

## Constraints

1. **Phase Dependencies**: Each phase requires predecessor completion marker
2. **DAG Enforcement**: Claim graph must remain acyclic; circular reasoning = fatal
3. **Stability Ordering**: FOUNDATIONAL claims immutable after Φ1
4. **Genuine Critique**: Softball attacks detected via cross-eval and rejected
5. **Compression Termination**: Max 4 recursive passes in Φ3c
6. **Convergence Cap**: Max cycles from config; output uncertainty if exhausted
7. **Token Budget**: Respect mode-specific limits; degrade gracefully if exceeded

## Integration

- **hierarchical-reasoning**: Map lenses to strategic/tactical/operational
- **graph**: Claim topology analysis, k-bisimulation on evaluation matrix
- **think**: Mental models power individual lens templates
- **non-linear**: Subagent spawning for parallel lens execution
- **infranodus**: Graph gap detection enhances STRUCTURAL lens
- **component**: Structure critique outputs as validatable configuration

## References

- `references/lens-specifications.md` — Complete lens templates and attack vectors
- `references/cross-evaluation-protocol.md` — Matrix construction and analysis
- `references/aggregation-algorithms.md` — Consensus extraction and compression
