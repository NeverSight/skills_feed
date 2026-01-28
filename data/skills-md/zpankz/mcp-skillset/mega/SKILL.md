---
name: mega
description: "Maximally Endowed Graph Architecture — λ-calculus over bounded n-SuperHyperGraphs with grounded uncertainty, conditional self-duality, and autopoietic refinement. Use when (1) simple graphs insufficient (η<2), (2) multi-scale reasoning required, (3) uncertainty is structured not stochastic, (4) knowledge must self-refactor. Pareto-governed: complexity added only when simpler structures fail validation."
---

# MEGA - Maximally Endowed Graph Architecture

> **λΩ.τ**: Query → Bounded n-SuperHyperGraph → Validated Holon

<purpose>

## purpose

- implements structured management for complex knowledge relationships
- achieved by applying the Pareto principle it invokes
- activates only when η≥4 or φ>0.2
- ensures operational tractability while retaining theoretical completeness

## triggers

- "complex adaptive system"
- "graph of graphs"
- "multi-scale reasoning"
- "knowledge architecture"
- "structured uncertainty"
- "self-refactoring"

## anti_triggers

- simple lookup
- single-domain query
- deterministic computation
- η ≥ 4 already satisfied with base graph

## integrates

- graph (γ): compression quotients, η validation
- ontolog (ω): simplicial complex encoding
- hierarchical (η): strategic→tactical→operational levels
- non-linear (ν): uncertainty propagation, convergence
- infranodus (ι): gap detection, bridge suggestions
- abduct (β): refactoring, topology optimization

</purpose>

---

## 1. PARETO-GOVERNED COMPLEXITY

<complexity_escalation>

``` md
ESCALATION LADDER
─────────────────
Level 0: Simple Graph G = (V, E)
  ↓ escalate if: η < 2 OR φ > 0.3
Level 1: Property Graph G = (V, E, Π)
  ↓ escalate if: η < 3 OR requires multi-valued attributes
Level 2: Hypergraph H = (V, E ⊆ P(V))
  ↓ escalate if: η < 4 OR requires hypernodes
Level 3: n-SuperHyperGraph (n ≤ 3)
  ↓ escalate if: fails self-consistency check
Level Ω: Full MEGA (theoretical limit)

PARETO RULE
───────────
complexity_cost(level) = 2^level
utility_gain(level) ≤ 1.5^level for most domains

⟹ Level 2-3 is Pareto-optimal for 80% of use cases
⟹ Level Ω reserved for genuinely pathological structures
```

</complexity_escalation>

<trigger_logic>

```python
def needs_mega(structure: Graph) -> tuple[bool, int]:
    """
    Determine if MEGA is warranted and at what level.
    Returns (should_escalate, recommended_level).
    """
    η = len(structure.edges) / max(len(structure.nodes), 1)
    φ = isolated_ratio(structure)
    κ = clustering_coefficient(structure)

    # Level 0: Simple graph sufficient
    if η >= 4 and φ < 0.2 and κ > 0.3:
        return False, 0

    # Check for multi-valued attributes
    if has_structured_uncertainty(structure):
        if requires_contradiction_logic(structure):
            return True, 2  # Plithogenic needed
        return True, 1  # Property graph sufficient

    # Check for hierarchical nesting
    if requires_hypernodes(structure):
        max_nesting = max_nesting_depth(structure)
        return True, min(max_nesting + 1, 3)

    # Default: try Level 1 refinement
    return True, 1
```

</trigger_logic>

---

## 2. BOUNDED n-SUPERHYPERGRAPH

<formal_definition>

```md
n-SHG (OPERATIONAL FORM)
────────────────────────
For practical n ∈ {1, 2, 3}:

Ω_n = (V_n, E_n, Π, Φ, Ψ) where:
  V_n ⊆ P^n(V_0)      Vertices up to n-th powerset (bounded)
  E_n ⊆ P^n(E_0)      Edges up to n-th powerset (bounded)
  Π : V_n ∪ E_n → A   Attribute function (not tensor)
  Φ : V_n → {1..n}    Level assignment (explicit, not manifold)
  Ψ : V_n × V_n → R   Correlation matrix (sparse, not universal)

COMPUTATIONAL BOUNDS
────────────────────
|V_1| ≤ 2|V_0|        First powerset: at most doubles
|V_2| ≤ |V_1|^1.5     Second: subquadratic in practice
|V_3| ≤ |V_2|log|V_2| Third: polylog growth (pruned)

Total storage: O(|V_0|^2 · n) for n ≤ 3
Query time: O(|E|log|V|) with appropriate indexing
```

</formal_definition>

<level_semantics>

``` md
LEVEL INTERPRETATION
────────────────────
n=1: ENTITIES
  Concrete objects, concepts, terms
  Example: "thermodilution", "cardiac_output", "Stewart-Hamilton"

n=2: GROUPINGS (meta-entities)
  Sets of entities that form coherent units
  Example: {"Stewart-Hamilton", "indicator_mass", "flow_rate"} = CO_measurement

n=3: SCHEMAS (meta-meta-entities)
  Patterns across groupings, organizing principles
  Example: {"CO_measurement", "Fick_principle", "bioimpedance"} = hemodynamic_monitoring

n>3: THEORETICAL LIMIT
  Rarely needed; signals over-abstraction
  If required: split domain, don't increase n
```

</level_semantics>

---

## 3. GROUNDED UNCERTAINTY (Plithogenic-Lite)

<uncertainty_model>

``` md
OPERATIONAL PLITHOGENIC ATTRIBUTES
──────────────────────────────────
For element x and attribute a:

Π(x, a) = (confidence, coverage, source_quality)

confidence ∈ [0,1]    How certain (not T/F/I split)
coverage ∈ [0,1]      What fraction of attribute space covered
source_quality ∈ [0,1] Reliability of evidence

COMPOSITION RULES
─────────────────
conjunction: min(conf₁, conf₂), min(cov₁, cov₂), min(sq₁, sq₂)
disjunction: max(conf₁, conf₂), max(cov₁, cov₂), max(sq₁, sq₂)
negation: 1-conf, cov, sq

GROUNDING HEURISTICS
────────────────────
confidence = 0.9  if peer-reviewed source
confidence = 0.7  if expert consensus
confidence = 0.5  if single expert opinion
confidence = 0.3  if plausible inference
confidence = 0.1  if speculation

source_quality derived from:
  - Examiner reports (CICM/ANZCA): 0.95
  - Textbooks: 0.85
  - Review articles: 0.80
  - Primary research: 0.75 (varies)
  - Web search: 0.50 (requires triangulation)
```

</uncertainty_model>

<contradiction_handling>

``` md
DETECTING CONTRADICTION
───────────────────────
Two claims C₁, C₂ contradict if:
  subject(C₁) ≅ subject(C₂) AND
  predicate(C₁) ⊗ predicate(C₂) = ⊥

RESOLUTION STRATEGIES (ordered)
───────────────────────────────
1. AUTHORITY: Higher source_quality wins
2. RECENCY: More recent evidence wins
3. SPECIFICITY: More specific claim wins
4. CONSENSUS: More sources wins
5. ESCALATE: Flag for human review

OPERATIONAL PATTERN
───────────────────
def resolve_contradiction(c1, c2):
    if source_quality(c1) - source_quality(c2) > 0.2:
        return c1
    if timestamp(c1) - timestamp(c2) > 1_year:
        return c1
    if specificity(c1) > specificity(c2):
        return c1
    return Both(c1, c2, confidence=0.5)  # Escalate
```

</contradiction_handling>

---

## 4. CONDITIONAL SELF-DUALITY

<matroid_when_applicable>

``` md
SELF-DUALITY IS CONDITIONAL
───────────────────────────
Not all graphs admit self-dual matroids.
MEGA applies self-duality only when structure permits.

CHECK FOR SELF-DUAL ELIGIBILITY
───────────────────────────────
def is_self_dual_eligible(G: Graph) -> bool:
    M = graphic_matroid(G)
    M_dual = dual_matroid(M)
    return is_isomorphic(M, M_dual)

COMMON SELF-DUAL STRUCTURES
───────────────────────────
✓ Trees (always self-dual)
✓ Complete graphs K_n for n ≤ 4
✓ Wheel graphs W_n for certain n
✓ Planar graphs with planar duals ≅ self
✗ Most random graphs
✗ Dense networks with asymmetric structure

OPERATIONAL CONSEQUENCE
───────────────────────
If self-dual:
  Node↔Edge flip preserves query semantics
  Can answer "what connects X and Y" via dual query

If not self-dual:
  Restrict to explicit graph structure
  No automatic role reversal
```

</matroid_when_applicable>

<dual_operations>

``` md
LINE GRAPH TRANSFORM (always available)
───────────────────────────────────────
L(G): edges become nodes, adjacency via shared endpoint
  - Useful for "relationship-centric" queries
  - O(|E|²) worst case, often much smaller

QUOTIENT TRANSFORM (compression)
────────────────────────────────
G/~ : Collapse equivalence classes
  - Preserves η ≥ 4 if class sizes bounded
  - Primary tool for managing complexity

COVER TRANSFORM (expansion)
───────────────────────────
Ĝ: Lift to covering space
  - Useful for resolving ambiguity
  - Inverse of quotient
```

</dual_operations>

---

## 5. OPERATIONAL ENTANGLEMENT

<correlation_semantics>

``` md
"ENTANGLEMENT" OPERATIONALIZED
──────────────────────────────
NOT quantum superposition
IS: strong structural correlation requiring co-update

Ψ(v_i, v_j) = pearson_correlation(history(v_i), history(v_j))

COMPUTATION
───────────
Sparse matrix (most pairs uncorrelated)
Store only |Ψ(i,j)| > 0.5 (significant correlation)

Update rule:
  When v_i modified: propagate to all j where |Ψ(i,j)| > 0.7
  Propagation: notification, not automatic change
  Human/agent decides actual update

PRACTICAL EXAMPLE
─────────────────
In medical knowledge graph:
  Ψ(CO, SVR) = -0.8  (inverse relationship)
  Ψ(HR, CO) = +0.6   (positive correlation if SV constant)

When CO↑ noted:
  Flag SVR for potential decrease
  Flag HR for potential cause/effect review
```

</correlation_semantics>

<decoherence_as_query>

``` md
"DECOHERENCE" OPERATIONALIZED
─────────────────────────────
NOT quantum measurement collapse
IS: query-time materialization of lazy evaluation

Before query: Graph may have multiple valid interpretations
  (e.g., "CO" could mean cardiac output or carbon monoxide)

Query provides context → resolve ambiguity
  "CO in hemodynamic monitoring" → cardiac output
  "CO in toxicology" → carbon monoxide

IMPLEMENTATION
──────────────
def decohere(graph: Graph, query: Query) -> ResolvedGraph:
    context = extract_context(query)

    for node in graph.ambiguous_nodes:
        candidates = node.interpretations
        best = argmax(candidates, key=lambda c:
                      semantic_similarity(c, context))
        node.resolve_to(best)

    for edge in graph.conditional_edges:
        if edge.condition.satisfied_by(context):
            edge.activate()

    return graph.materialized_view()
```

</decoherence_as_query>

---

## 6. AUTOPOIESIS AS INCREMENTAL REFINEMENT

<autopoiesis_grounded>

``` md
NOT: mystical self-creation from void
IS: systematic pattern recognition → structure update

TRIGGER CONDITIONS
──────────────────
1. η drops below 4 after insertion
2. New cluster detected (modularity increase > 0.05)
3. Orphan nodes created (φ increases)
4. Contradiction detected (plithogenic conflict)

REFINEMENT ACTIONS
──────────────────
R1: BRIDGE GAPS
    When: structural gap detected (InfraNodus)
    Action: generate research questions, seek bridging concepts

R2: COMPRESS REDUNDANCY
    When: bisimulation quotient non-trivial
    Action: merge structurally equivalent nodes

R3: EXPAND ABSTRACTION
    When: cluster size > threshold, internal η > 6
    Action: create meta-node at level n+1

R4: REPAIR VIOLATIONS
    When: axiom check fails
    Action: local restructuring, escalate if persistent
```

</autopoiesis_grounded>

<refinement_loop>

```python
def autopoietic_cycle(omega: MEGA, environment: Stream) -> MEGA:
    """
    One cycle of self-refinement.
    Bounded: max 10 refinements per cycle.
    """
    refinements = 0
    max_refinements = 10

    while refinements < max_refinements:
        # Check invariants
        violations = validate_all(omega)
        if not violations:
            break

        # Prioritize by severity
        violations.sort(key=lambda v: v.severity, reverse=True)

        # Apply most critical fix
        fix = select_fix(violations[0])
        omega = apply_fix(omega, fix)
        refinements += 1

        # Log for observability
        log(f"Refinement {refinements}: {fix.description}")

    # Observe environment for new patterns
    if environment.has_new():
        patterns = detect_patterns(environment.recent())
        for pattern in patterns:
            if not already_encoded(omega, pattern):
                omega = integrate_pattern(omega, pattern)

    return omega
```

</refinement_loop>

---

## 7. INTEGRATION WITH SKILLS/TOOLS

<skill_composition>

``` md
MEGA AS ORCHESTRATOR
────────────────────
MEGA provides the structural backbone; other skills provide operations.

graph (γ):
  - Input: raw extractions
  - MEGA adds: level assignment, uncertainty attributes
  - Invariant: η ≥ 4 preserved

ontolog (ω):
  - Provides: simplicial complex encoding
  - MEGA adds: n-level nesting, chrono-indexing
  - Integration: Σ_k face structure maps to level k

hierarchical (η):
  - Provides: strategic/tactical/operational decomposition
  - MEGA adds: cross-level correlation (Ψ)
  - Integration: S↔T↔O levels become n=1,2,3

non-linear (ν):
  - Provides: uncertainty propagation, convergence detection
  - MEGA adds: structured uncertainty (not just variance)
  - Integration: ν handles dynamics, MEGA handles structure

infranodus (ι):
  - Provides: gap detection, research question generation
  - MEGA adds: gap severity via η impact analysis
  - Integration: ι.gaps → R1 bridge refinement

abduct (β):
  - Provides: schema refactoring
  - MEGA adds: level-preserving constraint
  - Integration: β operates within level, MEGA handles cross-level
```

</skill_composition>

<tool_integration>

```python
# InfraNodus integration for gap analysis
async def mega_gap_analysis(omega: MEGA, text: str) -> GapReport:
    """
    Use InfraNodus to find structural gaps in MEGA instance.
    """
    # Extract text representation
    text_repr = omega_to_text(omega)

    # Call InfraNodus
    result = await infranodus.getGraphAndAdvice(
        name="mega_analysis",
        text=text_repr,
        optimize="gaps",
        extendedGraphSummary=True,
        gapDepth=2
    )

    # Map gaps to MEGA structure
    gaps = []
    for gap in result.gaps:
        mega_gap = MegaGap(
            clusters=map_to_mega_nodes(gap.clusters, omega),
            severity=compute_eta_impact(gap, omega),
            suggested_bridges=gap.bridging_concepts
        )
        gaps.append(mega_gap)

    return GapReport(gaps=gaps, suggested_refinements=generate_R1_actions(gaps))

# Obsidian integration for PKM
def mega_to_obsidian(omega: MEGA, vault_path: str) -> None:
    """
    Export MEGA structure to Obsidian vault.
    """
    for level in range(omega.max_level + 1):
        nodes = omega.nodes_at_level(level)
        for node in nodes:
            path = f"{vault_path}/L{level}/{node.slug}.md"
            content = generate_obsidian_note(node, omega)
            write_file(path, content)

    # Generate MOC (Map of Content) at each level
    for level in range(omega.max_level + 1):
        moc_path = f"{vault_path}/L{level}/_MOC.md"
        moc_content = generate_level_moc(omega, level)
        write_file(moc_path, moc_content)
```

</tool_integration>

---

## 8. VALIDATION

<invariants>

``` md
TOPOLOGY INVARIANTS
───────────────────
η = |E|/|V| ≥ 4         Edge density (mandatory)
φ = |isolated|/|V| < 0.2 Isolation ratio (mandatory)
κ > 0.3                  Clustering (recommended)
ζ = 0                    Acyclicity (for DAG mode only)

STRUCTURAL INVARIANTS
─────────────────────
levels_well_founded:     ∀v. level(v) = 0 ∨ ∃u. level(u) < level(v) ∧ (u,v) ∈ E
uncertainty_bounded:     ∀v,a. Π(v,a) ∈ [0,1]³
correlation_symmetric:   Ψ = Ψᵀ
correlation_bounded:     ∀i,j. |Ψ(i,j)| ≤ 1

OPERATIONAL INVARIANTS
──────────────────────
query_terminates:        All decoherence operations halt
refinement_bounded:      Autopoietic cycles ≤ 10 per trigger
storage_polynomial:      |structure| = O(|V_0|² · n) for n ≤ 3
```

</invariants>

<validation_procedure>

```python
def validate_mega(omega: MEGA) -> ValidationResult:
    """
    Comprehensive validation with remediation suggestions.
    """
    violations = []

    # Topology
    eta = len(omega.edges) / max(len(omega.nodes), 1)
    if eta < 4:
        violations.append(Violation(
            type="TOPOLOGY",
            metric="η",
            value=eta,
            threshold=4,
            severity="CRITICAL",
            remediation="Apply γ.triangulate() or ι.bridge_gaps()"
        ))

    phi = omega.isolated_ratio()
    if phi > 0.2:
        violations.append(Violation(
            type="TOPOLOGY",
            metric="φ",
            value=phi,
            threshold=0.2,
            severity="MAJOR",
            remediation="Connect orphans via ι.suggested_bridges()"
        ))

    # Structural
    for node in omega.nodes:
        if node.level > 0:
            if not any(omega.has_edge(u, node) for u in omega.nodes
                      if u.level < node.level):
                violations.append(Violation(
                    type="STRUCTURAL",
                    metric="level_grounding",
                    value=f"Node {node.id} at level {node.level} ungrounded",
                    severity="MAJOR",
                    remediation="Add cross-level edge or demote node"
                ))

    # Uncertainty bounds
    for node in omega.nodes:
        for attr, val in node.attributes.items():
            if not (0 <= val.confidence <= 1):
                violations.append(Violation(
                    type="UNCERTAINTY",
                    metric="confidence_bound",
                    value=f"{node.id}.{attr}.confidence = {val.confidence}",
                    severity="CRITICAL",
                    remediation="Clamp to [0,1]"
                ))

    return ValidationResult(
        valid=len(violations) == 0,
        violations=violations,
        summary=summarize_violations(violations)
    )
```

</validation_procedure>

---

## 9. WORKFLOW

<process>

```python
def mega_process(query: str, context: Context) -> MEGAHolon:
    """
    Main MEGA workflow: Query → Validated Holon
    """

    # Φ1: PARSE — Extract structure from query
    components = parse_query(query)
    initial_graph = extract_graph(components, context)

    # Φ2: ASSESS — Determine if MEGA needed
    needs_escalation, level = needs_mega(initial_graph)
    if not needs_escalation:
        return simple_graph_response(initial_graph, query)

    # Φ3: BUILD — Construct n-SHG at appropriate level
    omega = build_n_shg(initial_graph, n=level)

    # Φ4: ENDOW — Add uncertainty and correlation
    omega = add_uncertainty_attributes(omega, context)
    omega = compute_correlations(omega)

    # Φ5: INTEGRATE — Connect to existing PKM
    if context.pkm_available:
        omega = vertex_share(omega, context.pkm)

    # Φ6: VALIDATE — Check invariants
    validation = validate_mega(omega)
    if not validation.valid:
        # Apply remediations
        for v in validation.violations:
            omega = apply_remediation(omega, v.remediation)
        # Re-validate
        validation = validate_mega(omega)
        assert validation.valid, f"Remediation failed: {validation.summary}"

    # Φ7: DECOHERE — Resolve ambiguities for this query
    resolved = decohere(omega, query)

    # Φ8: REASON — Hierarchical processing
    strategic = strategic_level(resolved, query)   # Why
    tactical = tactical_level(strategic)           # How
    operational = operational_level(tactical)      # What

    # Φ9: SYNTHESIZE — Generate output holon
    holon = synthesize_holon(operational, level)

    # Φ10: REFINE — Autopoietic update for future
    if should_refine(holon, omega):
        schedule_refinement(omega, holon)

    return holon
```

</process>

---

## 10. LOGOS / TELOS / ONTOS MAPPING

<triadic_grounding>

``` md
LOGOS (How) — The Calculus
────────────────────────────
Blueprint:   Bounded n-SHG with explicit level assignment
Compass:     η ≥ 4 (density), φ < 0.2 (connectivity)
Grammar:     λ-composition: ∘ ⊗ * |
Instantiation: skill composition over simplicial complex

TELOS (Why) — The Attractor
─────────────────────────────
Driver:      PSR — every edge has sufficient reason
Optimizer:   Pareto governance — complexity earned not assumed
Minima:      FEP-like — minimize structural surprise (gaps, orphans)
Schema:      80/20 distribution of truth-weight across meta-nodes

ONTOS (What) — The Substance
─────────────────────────────
Being:       Grounded uncertainty (confidence, coverage, quality)
Presence:    Query-time materialization (lazy → resolved)
Anatomy:     Bounded fractal: L0 → L1 → L2 (rarely L3)
Holonic:     Parts contain projections (InfraNodus cluster views)

SYNTHESIS
─────────
Valid(MEGA) ⟺ LOGOS(η≥4) ∧ TELOS(Pareto) ∧ ONTOS(bounded)
```

</triadic_grounding>

---

## 11. QUICK REFERENCE

``` md
MEGA v2.0 — Operationally Grounded λΩ.τ
═══════════════════════════════════════

CORE PRINCIPLE
  Complexity is earned through validation failure
  Pareto governs: 80% of utility from Level ≤ 2

ESCALATION LADDER
  L0: Simple Graph    (η<2 OR φ>0.3 → L1)
  L1: Property Graph  (structured uncertainty → L2)
  L2: Hypergraph      (hypernodes required → L3)
  L3: 3-SHG           (max practical depth)
  LΩ: Full MEGA       (theoretical limit only)

INVARIANTS (mandatory)
  η = |E|/|V| ≥ 4     Edge density
  φ < 0.2             Isolation ratio
  n ≤ 3               Bounded depth

UNCERTAINTY (grounded)
  Π(x,a) = (confidence, coverage, source_quality) ∈ [0,1]³
  Contradiction → resolution by authority/recency/specificity

SELF-DUALITY (conditional)
  Only when matroid M ≅ M*
  Otherwise: explicit structure, no role flip

ENTANGLEMENT (operational)
  Ψ(i,j) = correlation requiring co-update notification
  Sparse matrix, threshold |Ψ| > 0.5 for storage

DECOHERENCE (query-time)
  Ambiguous → context-resolved materialization
  Lazy evaluation until query commits

AUTOPOIESIS (incremental)
  R1: Bridge gaps (ι integration)
  R2: Compress redundancy (γ quotient)
  R3: Expand abstraction (level creation)
  R4: Repair violations (local restructure)

INTEGRATION
  γ: compression     ω: encoding      η: levels
  ν: uncertainty     ι: gaps          β: refactoring

λ-OPERATORS
  ∘  sequential      (β → τ) → (α → β) → (α → τ)
  ⊗  parallel        (α → β) → (α → γ) → (α → (β,γ))
  *  recursive       ((α→α) → α) fixpoint
  |  conditional     (α → β) | (α → Bool) → (α → Maybe β)
```

<routing>

| Need | Reference | Description |
|------|-----------|-------------|
| Full endowment specs | [references/endowments.md](references/endowments.md) | Detailed component behavior |
| λ-operations | [references/operations.md](references/operations.md) | Composition algebra |
| Validation details | [references/validation.md](references/validation.md) | Invariant enforcement |
| Skill integration | [references/integration.md](references/integration.md) | Cross-skill composition |
| Python implementation | [scripts/mega_core.py](scripts/mega_core.py) | Executable patterns |

</routing>
