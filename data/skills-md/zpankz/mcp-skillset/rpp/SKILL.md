---
name: rpp
description: |
  Generates hierarchical knowledge graphs via Recursive Pareto Principle for optimised 
  schema construction. Produces four-level structures (L0 meta-graph through L3 detail-graph) 
  where each level contains 80% fewer nodes while grounding 80% of its derivative, achieving 
  51% coverage from 0.8% of nodes via Pareto³ compression. Use when creating domain ontologies 
  or knowledge architectures requiring: (1) Atomic first principles with emergent composites, 
  (2) Pareto-optimised information density, (3) Small-world topology with validated node 
  ratios (L1:L2 2-3:1), or (4) Bidirectional construction. Integrates with graph (η≥4 
  validation), abduct (refactoring), mega (SuperHyperGraphs), infranodus (gap detection). 
  Triggers: 'schema generation', 'ontology creation', 'Pareto hierarchy', 'recursive graph', 
  'first principles decomposition'.
---

# Recursive Pareto Principle (RPP)

> **λL.τ** : Domain → OptimisedSchema via recursive Pareto compression

## Purpose

Generate hierarchical knowledge structures where each level achieves maximum explanatory power with minimum nodes through recursive application of the Pareto principle.

## Core Model

```
L0 (Meta-graph/Schema)    ← 0.8% nodes → 51% coverage (Pareto³)
      │ abductive generalisation
      ▼
L1 (Logic-graph/Atomic)   ← 4% nodes → 64% coverage (Pareto²)
      │ Pareto extraction
      ▼
L2 (Concept-graph)        ← 20% nodes → 80% coverage (Pareto¹)
      │ emergent clustering
      ▼
L3 (Detail-graph)         ← 100% nodes → ground truth
```

### Level Specifications

| Level | Role | Node % | Coverage | Ratio to L3 |
|-------|------|--------|----------|-------------|
| L0 | Meta-graph/Schema | 0.8% | 51% | 6-9:1 to L1 |
| L1 | Logic-graph/Atomic | 4% | 64% | 2-3:1 to L2 |
| L2 | Concept-graph/Composite | 20% | 80% | — |
| L3 | Detail-graph/Ground-truth | 100% | 100% | — |

### Node Ratio Constraints

- **L1:L2** = 2-3:1 (atomic to composite)
- **L1:L2** = 9-12:1 (logic to concept)
- **L1:L3** = 6-9:1 (atomic to detail)
- **Generation constraint**: 2-3 children per node at any level

## Quick Start

### 1. Domain Analysis

```python
from rpp import RPPGenerator

# Initialize with domain text
rpp = RPPGenerator(domain="pharmacology")

# Extract ground truth (L3)
l3_graph = rpp.extract_details(corpus)
```

### 2. Hierarchical Construction

```python
# Bottom-up: L3 → L2 → L1 → L0
l2_graph = rpp.cluster_concepts(l3_graph, pareto_threshold=0.8)
l1_graph = rpp.extract_atomics(l2_graph, pareto_threshold=0.8)
l0_schema = rpp.generalise_schema(l1_graph, pareto_threshold=0.8)

# Validate ratios
rpp.validate_ratios(l0_schema, l1_graph, l2_graph, l3_graph)
```

### 3. Topology Validation

```python
# Ensure small-world properties
metrics = rpp.validate_topology(
    target_eta=4.0,        # Edge density
    target_ratio_l1_l2=(2, 3),
    target_ratio_l1_l3=(6, 9)
)
```

## Construction Methods

### Bottom-Up (Reconstruction)

Start from first principles, build emergent complexity:

```
L3 details → cluster → L2 concepts → extract → L1 atomics → generalise → L0 schema
```

Use when: Ground truth is well-defined, deriving principles from evidence.

### Top-Down (Decomposition)

Start from control systems, decompose to details:

```
L0 schema → derive → L1 atomics → expand → L2 concepts → ground → L3 details
```

Use when: Schema exists, validating against domain specifics.

### Bidirectional (Recommended)

Simultaneous construction with convergence:

```
┌─────────────────────────────────────────┐
│ Bottom-Up          ⊗          Top-Down │
│ L3→L2→L1→L0       merge        L0→L1→L2→L3 │
│         └───────→ L2 ←───────┘         │
│              convergence               │
└─────────────────────────────────────────┘
```

Use when: Iterative refinement needed, validating both directions.

## Graph Topology

### Small-World Properties

The RPP graph exhibits:
- **High clustering** — Related concepts form dense clusters
- **Short path length** — Any two nodes connected via few hops
- **Core-peripheral structure** — L0/L1 form core, L2/L3 form periphery
- **Orthogonal bridges** — Unexpected cross-hierarchical connections

### Topology Targets

| Metric | Target | Validation |
|--------|--------|------------|
| η (density) | ≥ 4.0 | `graph.validate_topology()` |
| κ (clustering) | > 0.3 | Small-world coefficient |
| φ (isolation) | < 0.2 | No orphan nodes |
| Bridge edges | Present | Cross-level connections |

### Edge Types

1. **Vertical edges** — Parent-child across levels (L0↔L1↔L2↔L3)
2. **Horizontal edges** — Sibling relations within level
3. **Hyperedges** — Multi-node interactions (weighted by semantic importance)
4. **Bridge edges** — Orthogonal cross-hierarchical connections

## Pareto Extraction Algorithm

```python
def pareto_extract(source_graph, target_ratio=0.2):
    """
    Extract Pareto-optimal nodes from source graph.
    
    Args:
        source_graph: Input graph (e.g., L3 for extracting L2)
        target_ratio: Target node reduction (default 20% = 0.2)
    
    Returns:
        Reduced graph with target_ratio * |source| nodes
        grounding (1 - target_ratio) of semantic coverage
    """
    # 1. Compute node importance (PageRank + semantic weight)
    importance = compute_importance(source_graph)
    
    # 2. Select top nodes by cumulative coverage
    selected = []
    coverage = 0.0
    for node in sorted(importance, reverse=True):
        selected.append(node)
        coverage += node.coverage_contribution
        if coverage >= (1 - target_ratio):
            break
    
    # 3. Verify Pareto constraint
    assert len(selected) / len(source_graph) <= target_ratio
    assert coverage >= (1 - target_ratio)
    
    # 4. Build reduced graph preserving topology
    return build_subgraph(selected, preserve_bridges=True)
```

## Integration Points

### With graph skill

```python
# Validate RPP topology
from graph import validate_topology
metrics = validate_topology(rpp_graph, require_eta=4.0)
```

### With abduct skill

```python
# Refactor schema for optimisation
from abduct import refactor_schema
l0_optimised = refactor_schema(l0_schema, target_compression=0.8)
```

### With mega skill

```python
# Extend to n-SuperHyperGraphs for complex domains
from mega import extend_to_superhypergraph
shg = extend_to_superhypergraph(rpp_graph, max_hyperedge_arity=5)
```

### With infranodus MCP

```python
# Detect structural gaps
gaps = mcp__infranodus__generateContentGaps(rpp_graph.to_text())
bridges = mcp__infranodus__getGraphAndAdvice(optimize="gaps")
```

## Scale Invariance Principles

The RPP framework embodies scale-invariant patterns:

| Principle | Application in RPP |
|-----------|-------------------|
| Fractal self-similarity | Each level mirrors whole structure |
| Pareto distribution | 80/20 at each level compounds |
| Neuroplasticity | Pruning weak, amplifying strong connections |
| Free energy principle | Minimising surprise through compression |
| Critical phase transitions | Level boundaries as phase transitions |
| Power-law distribution | Node importance follows power law |

## References

For detailed implementation, see:

| Need | File |
|------|------|
| Level-specific construction | [references/level-construction.md](references/level-construction.md) |
| Topology validation | [references/topology-validation.md](references/topology-validation.md) |
| Pareto algorithms | [references/pareto-algorithms.md](references/pareto-algorithms.md) |
| Scale invariance theory | [references/scale-invariance.md](references/scale-invariance.md) |
| Integration patterns | [references/integration-patterns.md](references/integration-patterns.md) |
| Examples and templates | [references/examples.md](references/examples.md) |

## Scripts

| Script | Purpose |
|--------|---------|
| [scripts/rpp_generator.py](scripts/rpp_generator.py) | Core RPP graph generation |
| [scripts/pareto_extract.py](scripts/pareto_extract.py) | Level extraction algorithm |
| [scripts/validate_ratios.py](scripts/validate_ratios.py) | Node ratio validation |
| [scripts/topology_check.py](scripts/topology_check.py) | Small-world validation |

## Checklist

### Before Generation
- [ ] Domain corpus available
- [ ] Target level count defined (typically 4)
- [ ] Integration skills accessible (graph, abduct)

### During Generation
- [ ] L3 ground truth extracted
- [ ] Each level achieves 80% coverage with 20% nodes
- [ ] Node ratios within constraints
- [ ] Hyperedge weights computed

### After Generation
- [ ] Topology validated (η≥4)
- [ ] Small-world coefficient verified
- [ ] Bridge edges present
- [ ] Schema exported in required format

---

```
λL.τ                     L3→L2→L1→L0 via Pareto extraction
80/20 → 64/4 → 51/0.8   recursive compression chain
rpp                      hierarchical knowledge architecture
```
