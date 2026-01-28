---
name: graph
description: "Use when extracting entities and relationships, building ontologies, compressing large graphs, or analyzing knowledge structures - provides structural equivalence-based compression achieving 57-95% size reduction, k-bisimulation summarization, categorical quotient constructions, and metagraph hierarchical modeling with scale-invariant properties. Supports recursive refinement through graph topology metrics including |R|/|E| ratios and automorphism analysis."
---

# Graph: Extraction, Analysis & Categorical Compression

Systematic extraction and analysis of entities, relationships, and ontological structures from unstructured text—enhanced with categorical metagraph compression enabling scale-invariant representation through structural equivalence, k-bisimulation summarization, and quotient constructions that preserve query-answering capabilities while achieving dramatic size reductions.

## Quick Start

### Basic Extraction

1. **Load schema**: Read `/mnt/skills/user/knowledge-graph/schemas/core_ontology.md` for entity/relationship types
2. **Extract entities and relationships** using the schema as a guide
3. **Format as JSON** following `/mnt/skills/user/knowledge-graph/templates/extraction_template.md`
4. **Validate**: Run validation script on extracted graph

### Compression Workflow

```bash
# 1. Extract → validate → analyze topology
python scripts/validate_graph.py graph.json
python scripts/analyze_graph.py graph.json --topology

# 2. Compute structural equivalence and compress
python scripts/compress_graph.py graph.json --method k-bisim --k 5

# 3. Verify query preservation
python scripts/verify_compression.py original.json compressed.json --queries reachability,pattern
```

## Theoretical Foundation

### The Compression Mechanism

Structural equivalence enables compression through a precise mechanistic chain:

**Equivalence → Redundancy → Quotient → Preservation**

1. **Equivalence relations partition structures**: Graph automorphisms and categorical isomorphisms identify structurally interchangeable elements—vertices with identical connection patterns to equivalent neighbors belong to the same automorphism orbit

2. **Orbits represent information redundancy**: For *k* vertices in one orbit, *(k-1)* are informationally redundant since they encode the same structural relationships

3. **Quotient constructions eliminate redundancy**: Categorical quotients collapse equivalence classes to single representatives while the **universal property** guarantees any construction respecting the equivalence factors uniquely through the compressed representation

4. **Functors preserve structure across scales**: The quotient functor Q: C → C/R is full and bijective on objects—no essential categorical information is lost

### Quantitative Foundation

The connection between automorphisms and Kolmogorov complexity:

```
K(G) ≤ K(G/Aut(G)) + log|Aut(G)| + O(1)
```

Graphs with large automorphism groups have lower complexity because only one representative from each orbit needs encoding. For highly symmetric structures, compression can reach **n/log n** factor.

### Why This Matters for Knowledge Graphs

Knowledge graphs exhibit natural structural regularities:

| Pattern | Compression Mechanism | Typical Reduction |
|---------|----------------------|-------------------|
| Type hierarchies | Automorphism orbits | 40-60% |
| Repeated subgraphs | k-bisimulation equivalence | 50-80% |
| Community structure | Block quotients | 30-50% |
| Self-similar patterns | Scale-invariant quotients | 60-95% |

## Core Capabilities

### 1. Structured Entity Extraction

Extract entities with confidence scores, provenance tracking, and property attribution:

- **Entity types**: Person, Organization, Concept, Event, Document, Technology, Location
- **Confidence scoring**: 0.0-1.0 scale based on evidence clarity
- **Provenance metadata**: Source document, location, timestamp
- **Alias tracking**: Capture all name variations

**Key principle**: Every extraction must include confidence score and source tracking for auditability.

### 2. Relationship Mapping

Identify and classify relationships between entities:

- **Core relationships**: WORKS_FOR, AFFILIATED_WITH, RELATED_TO, AUTHORED, CITES, USES, LOCATED_IN, IMPLEMENTS
- **Domain-specific relationships**: Load schemas from `/mnt/skills/user/knowledge-graph/schemas/`
- **Bidirectional awareness**: Track relationship directionality
- **Property attribution**: Capture relationship metadata (dates, roles, contexts)

### 3. Domain-Specific Schemas

**General domains** use `core_ontology.md`

**Coding/software** domains additionally use `coding_domain.md` which adds:
- CodeEntity, Repository, API, Library, Architecture, Bug types
- DEPENDS_ON, CALLS, INHERITS_FROM, FIXES, DEPLOYED_ON relationships
- Language-specific extraction patterns

### 4. Structural Equivalence Analysis

Identify and exploit structural redundancy through automorphism detection:

**Automorphism-Based Compression**:
```python
# Compute automorphism group
aut_group = compute_automorphisms(graph)
orbits = partition_by_orbits(graph.nodes, aut_group)

# Each orbit → single representative
compressed_nodes = [orbit.canonical_representative() for orbit in orbits]
compression_ratio = len(graph.nodes) / len(compressed_nodes)
```

**Equivalence Types**:
- **Structural equivalence**: Identical connection patterns (strictest)
- **Regular equivalence**: Same relationship *types* to equivalent alters
- **Automorphic equivalence**: Permutable without changing structure

### 5. k-Bisimulation Summarization

Compress graphs while preserving query semantics using k-bisimulation:

**Definition**: Two nodes are k-bisimilar if they have:
1. Same labels
2. Same edge types to k-bisimilar neighbors
3. This property holds recursively to depth k

**Implementation**:
```bash
python scripts/compress_graph.py graph.json \
  --method k-bisim \
  --k 5 \                    # k=5 sufficient for most graphs
  --preserve-queries reachability,pattern
```

**Empirical Results**:
- k > 5 yields minimal additional partition refinement
- Achieves **95% reduction for reachability queries**
- Achieves **57% reduction for pattern matching**
- Incremental update cost: O(Δ·d^k) where Δ is changes, d is max degree

### 6. Categorical Quotient Construction

Apply category-theoretic compression with provable structure preservation:

**The Universal Property Guarantee**:

For any quotient Q: C → C/R, if H: C → D is any functor such that H(f) = H(g) whenever f ~ g in R, then H factors uniquely as H = H' ∘ Q.

This **unique factorization** means the quotient is the "freest" (most compressed) object respecting the equivalence—any construction built on the original that respects the equivalence can be equivalently built on the quotient.

**Skeleton Construction**:
```python
# Every category is equivalent to its skeleton
skeleton = compute_skeleton(category)
# skeleton contains exactly one representative per isomorphism class
# All categorical properties preserved (limits, colimits, exactness)
```

### 7. Metagraph Hierarchical Modeling

Support edge-of-edge structures for multi-scale representation:

**Metagraph Definition**: MG = ⟨V, MV, E, ME⟩
- V: vertices
- MV: metavertices (each containing an embedded metagraph fragment)
- E: edges connecting sets of vertices
- ME: metaedges connecting vertices, edges, or both

**Why Metagraphs Enable Scale Invariance**:

The edge-of-edge capability creates **holonic structure**—self-similar patterns where the relationship between a metavertex and its contents mirrors the relationship between the entire metagraph and its top-level components. Automorphisms operate at multiple levels simultaneously, creating compression opportunities at each scale when these automorphism structures are isomorphic across levels.

**2-Category Interpretation**:
- 0-cells: vertices/elements
- 1-morphisms: edges connecting sets
- 2-morphisms: metaedges relating edges

The **interchange law** ensures scale-independent composition.

### 8. Topology Metrics & Quality Validation

**Graph Quality Metrics**:

| Metric | Formula | Target | Significance |
|--------|---------|--------|--------------|
| Edge-to-Node Ratio | \|E\|/\|V\| | ≥4:1 | Enables emergence through dense connectivity |
| Isolation Rate | \|V_isolated\|/\|V\| | <20% | Measures integration completeness |
| Clustering Coefficient | Local triangles/possible triangles | >0.3 | Small-world property indicator |
| Fractal Dimension | d_B from box-covering | Finite | Self-similarity/compressibility |
| Average Path Length | Mean geodesic distance | Low | Information flow efficiency |

**Scale-Invariance Indicators**:
```
N_B(l_B) ~ l_B^(-d_B)
```
Networks with finite fractal dimension d_B are self-similar and can be compressed at multiple resolutions with compression ratio scaling as l^(d_B).

**Validation Script**:
```bash
python scripts/validate_graph.py graph.json --topology --compression-potential
```

### 9. Information-Theoretic Analysis

**Structural Entropy**:
```
H_s(G) = (n choose 2)h(p) - n·log(n) + O(n)
```
The term -n·log(n) represents compression gain from removing label information.

**Minimum Description Length (MDL)**:

For graph G and model M:
```
L(G,M) = L(M) + L(G|M)
```
Optimal compression minimizes this total description length. Community structure reduces entropy by ~k·log(n) bits for k communities.

**Compressibility Predictors**:
- High transitivity → higher compressibility
- Degree heterogeneity → higher compressibility
- Hierarchical structure → enables predictable transitions, lower entropy rates

## Extraction Guidelines

### Confidence Scoring Rules

| Score | Criteria | Example |
|-------|----------|---------|
| 0.9-1.0 | Explicitly stated with clear evidence | "Dr. Jane Smith works for MIT" |
| 0.7-0.89 | Strongly implied by context | Person with @mit.edu email |
| 0.5-0.69 | Reasonably inferred but ambiguous | Co-authorship implies collaboration |
| 0.3-0.49 | Weak inference, requires validation | Similar domain suggests relationship |
| 0.0-0.29 | Speculative, likely incorrect | Pure assumption |

### ID Generation Strategy

Create stable, meaningful identifiers:

- **Format**: `{type}_{normalized_name}` (e.g., `person_jane_smith`, `org_mit`)
- **Normalization**: Lowercase, replace spaces with underscores, remove special chars
- **Uniqueness**: Add numeric suffix if collision occurs
- **Stability**: Same entity in different documents should generate same ID

### Provenance Best Practices

Always include:
- `source_document`: Document ID or filename
- `source_location`: Page number, section, line range
- `extraction_timestamp`: ISO 8601 format
- `extractor_version`: Skill version identifier

## Advanced Workflows

### Compression Pipeline

```bash
# 1. Initial extraction
# (Extract to graph.json)

# 2. Validate and analyze
python scripts/validate_graph.py graph.json
python scripts/analyze_graph.py graph.json --full

# 3. Compute structural equivalence
python scripts/structural_equivalence.py graph.json \
  --output equivalence_classes.json \
  --method automorphism

# 4. Apply k-bisimulation compression
python scripts/compress_graph.py graph.json \
  --equivalence equivalence_classes.json \
  --method k-bisim --k 5 \
  --output compressed.json

# 5. Verify preservation
python scripts/verify_compression.py graph.json compressed.json \
  --queries reachability,pattern,neighborhood

# 6. Generate topology report
python scripts/topology_metrics.py compressed.json --report
```

### Iterative Refinement with Compression

1. **Initial extraction**: Broad pass capturing entities/relationships
2. **Topology analysis**: Compute |E|/|V| ratio, isolation rate, clustering
3. **Compression analysis**: Identify automorphism orbits, k-bisimilar classes
4. **Strategic refinement**: Focus on:
   - Central concepts with weak connections
   - Isolated high-confidence entities
   - Low-compression-potential regions (may need restructuring)
5. **Compress and validate**: Apply quotient construction, verify query preservation
6. **Repeat**: Continue until quality thresholds met AND compression ratio stabilizes

**Termination criteria**:
- Isolation rate < 20%
- |E|/|V| ratio ≥ 4:1
- Compression ratio improvement < 5% between iterations
- Query preservation verified

### Multi-Scale Metagraph Construction

For complex domains requiring hierarchical representation:

```bash
# 1. Extract at multiple granularities
python scripts/extract_hierarchical.py source.txt \
  --levels strategic,tactical,operational \
  --output metagraph.json

# 2. Compute cross-level automorphisms
python scripts/metagraph_automorphisms.py metagraph.json

# 3. Apply scale-invariant compression
python scripts/compress_metagraph.py metagraph.json \
  --preserve-hierarchy \
  --output compressed_metagraph.json
```

## Common Patterns

### Pattern: Query-Preserving Compression

Compress while guaranteeing specific query types remain answerable:

```python
# Define query preservation requirements
queries = {
    "reachability": True,      # 95% reduction possible
    "pattern_match": True,     # 57% reduction possible  
    "neighborhood_k": 3,       # Preserve 3-hop neighborhoods
}

# Compress with guarantees
compressed = compress_with_guarantees(
    graph, 
    method="k-bisimulation",
    k=max(5, queries["neighborhood_k"]),
    preserve=queries
)
```

### Pattern: Incremental Compression Maintenance

Maintain compression as graph evolves:

```python
# Update cost: O(Δ·d^k)
# Δ = number of changes
# d = maximum degree
# k = bisimulation depth

def update_compression(compressed_graph, changes):
    affected_classes = identify_affected_equivalence_classes(changes)
    recompute_local_bisimulation(affected_classes, k=5)
    return updated_compressed_graph
```

### Pattern: Categorical Ontology Integration

Use ologs (ontology logs) for categorical knowledge representation:

```python
# Olog: category where objects = noun phrases, morphisms = verb phrases
olog = {
    "objects": ["a person", "an organization", "a concept"],
    "morphisms": [
        {"source": "a person", "target": "an organization", "label": "works for"},
        {"source": "a concept", "target": "a concept", "label": "relates to"}
    ]
}

# Yoneda embedding: object determined by morphisms into it
# Compression: store relationships, not internal structure
```

## Error Handling

### Compression Quality Issues

When compression produces unexpected results:

1. **Over-compression**: Raise k value in k-bisimulation (default k=5)
2. **Under-compression**: Check for missing type labels, inconsistent schemas
3. **Query degradation**: Verify query type is in preservation set
4. **Scale-invariance failure**: Check for unbalanced hierarchical structure

### Topology Violations

When graph metrics fall outside targets:

1. **|E|/|V| < 4**: Graph too sparse—identify disconnected concepts, add bridging relationships
2. **Isolation > 20%**: Too many orphan nodes—run connectivity analysis
3. **Clustering < 0.3**: Lacks small-world property—add local triangulation

## File Structure

```
/mnt/skills/user/knowledge-graph/
├── SKILL.md                    # This file
├── schemas/
│   ├── core_ontology.md        # Universal entity/relationship types
│   ├── coding_domain.md        # Software development extension
│   └── categorical_ontology.md # Category-theoretic type system
├── templates/
│   ├── extraction_template.md  # JSON format specification
│   └── metagraph_template.md   # Hierarchical metagraph format
└── scripts/
    ├── validate_graph.py       # Quality validation
    ├── merge_graphs.py         # Deduplication and merging
    ├── analyze_graph.py        # Refinement strategy generation
    ├── compress_graph.py       # k-bisimulation compression
    ├── structural_equivalence.py # Automorphism computation
    ├── topology_metrics.py     # Graph topology analysis
    └── verify_compression.py   # Query preservation verification
```

## Dependencies

All scripts require Python 3.7+ with standard library only (no external packages for core functionality). Optional NetworkX for advanced topology metrics.

## Best Practices Summary

1. **Always start with schema**: Load appropriate ontology before extraction
2. **Include confidence scores**: Never omit—use 0.5 if uncertain
3. **Track provenance**: Every entity/relationship needs source metadata
4. **Validate early**: Run validation after each extraction
5. **Analyze topology**: Check |E|/|V| ratio before refinement
6. **Compress strategically**: Use k=5 for k-bisimulation (sufficient for most graphs)
7. **Preserve queries**: Specify which query types must remain answerable
8. **Iterate with metrics**: Let topology and compression metrics guide improvement

## Integration with Other Skills

This skill composes naturally with:

- **hierarchical-reasoning**: Strategic→tactical→operational maps to metagraph levels
- **obsidian-markdown**: Compressed graphs export as linked note structures
- **knowledge-orchestrator**: Automatic routing for extraction→compression→documentation workflows
- **infranodus-orchestrator**: Text network analysis → k-bisimulation compression

### Hierarchical Reasoning Integration

```yaml
mapping:
  strategic_level: metagraph_level_0
  tactical_level: metagraph_level_1  
  operational_level: metagraph_level_2
  convergence_metrics: compression_ratio, query_preservation
```

## Evaluation Criteria

A high-quality extraction with compression demonstrates:

- **Completeness**: Major entities and relationships captured
- **Accuracy**: High confidence scores (avg >0.7) and validated
- **Connectivity**: |E|/|V| ≥ 4:1, isolation <20%
- **Compressibility**: Achieves ≥50% reduction via k-bisimulation
- **Preservation**: Specified queries remain answerable post-compression
- **Scale-invariance**: Finite fractal dimension for hierarchical structures

---

**Core Philosophy**: Knowledge graphs emerge through iterative refinement—initial extraction establishes structure, topology analysis reveals density gaps, structural equivalence enables compression, and categorical quotients preserve essential relationships while eliminating redundancy. The compression is "lossy but structure-preserving" because categorical equivalence guarantees that compressed representations support all the same inferences as their originals.
