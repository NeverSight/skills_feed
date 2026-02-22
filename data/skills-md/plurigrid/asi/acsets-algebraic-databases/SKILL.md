---
name: acsets-algebraic-databases
description: "ACSets (Attributed C-Sets): Algebraic databases with Specter-style bidirectional navigation. Category-theoretic formalism for relational databases."
license: MIT
metadata:
  source: AlgebraicJulia/ACSets.jl + music-topos + Specter CPS patterns
  xenomodern: true
  ironic_detachment: 0.73
  trit: 0
  version: 1.3.0
---

# ACSets: Algebraic Databases Skill

> *"The category of simple graphs does not even have a terminal object!"*
> — AlgebraicJulia Blog, with characteristic ironic detachment

## What Are ACSets?

ACSets ("attributed C-sets") are a family of data structures generalizing both **graphs** and **data frames**. They are an efficient in-memory implementation of a category-theoretic formalism for relational databases.

**C-set** = Functor `X: C → Set` where C is a small category (schema)

```
┌─────────────────────────────────────────────────────────────┐
│  Schema (Small Category C)                                  │
│  ┌─────┐  src   ┌─────┐                                     │
│  │  E  │───────▶│  V  │                                     │
│  │     │  tgt   │     │                                     │
│  └──┬──┘───────▶└─────┘                                     │
│     │                                                       │
│     │ A C-set X assigns:                                    │
│     │   X(V) = set of vertices                              │
│     │   X(E) = set of edges                                 │
│     │   X(src): X(E) → X(V)                                 │
│     │   X(tgt): X(E) → X(V)                                 │
└─────────────────────────────────────────────────────────────┘
```

## Core Concepts

### 1. Schema Definition

```julia
using Catlab.CategoricalAlgebra

@present SchGraph(FreeSchema) begin
  V::Ob
  E::Ob
  src::Hom(E,V)
  tgt::Hom(E,V)
end

@acset_type Graph(SchGraph, index=[:src,:tgt])
```

### 2. Symmetric Graphs (Undirected)

```julia
@present SchSymmetricGraph <: SchGraph begin
  inv::Hom(E,E)

  compose(inv,src) == tgt
  compose(inv,tgt) == src
  compose(inv,inv) == id(E)
end

@acset_type SymmetricGraph(SchSymmetricGraph, index=[:src])
```

### 3. Attributed ACSets (with Data)

```julia
@present SchWeightedGraph <: SchGraph begin
  Weight::AttrType
  weight::Attr(E, Weight)
end

@acset_type WeightedGraph(SchWeightedGraph, index=[:src,:tgt]){Float64}
```

## GF(3) Conservation for ACSets

Integrate with Music Topos 3-coloring:

```julia
# Map ACSet parts to trits for GF(3) conservation
function acset_to_trits(g::Graph, seed::UInt64)
    rng = SplitMix64(seed)
    trits = Int[]
    for e in parts(g, :E)
        h = next_u64!(rng)
        hue = (h >> 16 & 0xffff) / 65535.0 * 360
        trit = hue < 60 || hue >= 300 ? 1 :
               hue < 180 ? 0 : -1
        push!(trits, trit)
    end
    trits
end

# Verify conservation: sum(trits) ≡ 0 (mod 3)
function gf3_conserved(trits)
    sum(trits) % 3 == 0
end
```

## Gay.jl Color Bindings for @acset_colim (PR #990)

Since Catlab PR #990, `@acset_colim` exposes name→part bindings. Combine with Gay.jl for:

### Named Part Coloring

```julia
using Gay

# Build ACSet with named parts
result, bindings = @acset_colim SchGraph begin
  e::E
  v1::V; v2::V
  src(e) == v1
  tgt(e) == v2
end

# Color each named part deterministically
seed = 0x114514
colors = Dict{Symbol, String}()
for (name, (ob, idx)) in bindings
    colors[name] = Gay.color_at(seed, idx)  # deterministic hex
end
# => Dict(:e => "#A855F7", :v1 => "#3B82F6", :v2 => "#10B981")
```

### Two Modalities for XOR Validation

**Modality 1: Different seeds (parallel verification)**
```julia
seeds = [0x1, 0x2, 0x3]  # Three independent streams
colors_per_seed = [Gay.palette(s, length(bindings)) for s in seeds]

# XOR guarantee: if all three agree on structure, computation is stable
# Divergence → indicates floating-point or algorithmic instability
```

**Modality 2: Same seed, staggered indices (convergence test)**
```julia
seed = 0x114514

# Run same computation 3 times, color at indices 1, 2, 3
c1 = compute_and_color(data, seed, index=1)
c2 = compute_and_color(data, seed, index=2)  
c3 = compute_and_color(data, seed, index=3)

# Convergence: c1 == c2 == c3 within bounded iterations → stable
# Divergence: colors differ → numerical instability detected automatically
```

### Empty Block = Initial Object = Neutral Color

```julia
# Empty block produces initial object (fixed in PR #990)
init, _ = @acset_colim SchGraph begin end  # ∅

# Initial object gets neutral/zero color (the "0" in GF(3))
neutral_color = Gay.color_at(seed, 0)  # or special "initial" marker
```

### Bidirectional Index with Color Tags

```julia
struct ColoredACSet{T}
    acset::T
    bindings::Dict{Symbol, Tuple{Symbol, Int}}
    colors::Dict{Symbol, String}
    seed::UInt64
end

function colored_acset_colim(schema, seed, block)
    acset, bindings = @acset_colim schema block
    colors = Dict(name => Gay.color_at(seed, idx) 
                  for (name, (_, idx)) in bindings)
    ColoredACSet(acset, bindings, colors, seed)
end

# Lookup by name → part index → color (all directions)
# name → color: ca.colors[:v1]
# color → name: findfirst(==(hex), ca.colors)
# name → part: ca.bindings[:v1][2]
```

### Instability Detection Pattern

```julia
function detect_instability(f, input, seed; tolerance=3)
    """
    Run f three times with same seed at staggered indices.
    If colors diverge beyond tolerance, flag instability.
    """
    results = [f(input) for _ in 1:3]
    colors = [Gay.color_at(seed, i) for i in 1:3]
    
    # Compare results - if they should be identical but aren't,
    # the divergent colors make the instability visually obvious
    for i in 1:3, j in i+1:3
        if results[i] ≠ results[j]
            @warn "Instability detected" color_i=colors[i] color_j=colors[j]
            return false
        end
    end
    true
end
```

This integrates the semantic naming from PR #990 with Gay.jl's deterministic coloring to create self-validating, visually debuggable ACSet constructions.

## Specter-Style Bidirectional Navigation

Inspired by Nathan Marz's Specter library, navigate ACSets with paths that work for both **select** AND **transform**.

### The Key Insight: comp-navs = alloc + field sets

From Marz: **"comp-navs is fast because it's just object allocation + field sets"**

```julia
# What comp_navs actually does:
comp_navs(a, b, c) = ComposedNav([a, b, c])  # That's it!
# No compilation, no interpretation, no optimization
# Just: allocate struct, set field, done

# All work happens at traversal via CPS:
nav_select(nav1, data, 
    r1 -> nav_select(nav2, r1,
        r2 -> nav_select(nav3, r2, identity)))
```

This means:
- **O(1) composition** - constant time path building
- **Inline caching** - paths compiled once per callsite
- **Near-hand-written speed** - CPS eliminates intermediate allocations

### ACSet Navigators

```julia
using SpecterACSet

# Navigate morphism values
acset_field(:E, :src)         # All source vertex IDs
acset_field(:E, :tgt)         # All target vertex IDs

# Filter parts by predicate
acset_where(:E, :src, ==(1))  # Edges where src == 1

# Navigate all parts of an object
acset_parts(:V)               # All vertex IDs
acset_parts(:E)               # All edge IDs
```

### Bidirectional Example

```julia
g = @acset Graph begin V=4; E=3; src=[1,2,3]; tgt=[2,3,4] end

# Select: get all source vertices
select([acset_field(:E, :src)], g)  # → [1, 2, 3]

# Transform: shift all targets (same path!)
g2 = transform([acset_field(:E, :tgt)], t -> mod1(t+1, 4), g)
select([acset_field(:E, :tgt)], g2)  # → [3, 4, 1]
```

### Integration with ∫G (Category of Elements)

Navigate the category of elements using paths:

```julia
# ∫G objects: (Ob, part_id) pairs
# Navigate to all elements
select([elements_of(:V)], g)  # → [(V,1), (V,2), (V,3), (V,4)]

# Navigate morphism structure
select([elements_of(:E), incident_to(:src, 1)], g)  # Edges from vertex 1
```

### Cross-Domain Bridge (Sexp ↔ ACSet)

```julia
# ACSet → Sexp → Navigate → Transform → Sexp → ACSet
sexp = sexp_of_acset(g)

# Navigate sexp to find all morphism names
morphism_names = select([SEXP_CHILDREN, sexp_nth(1), ATOM_VALUE], sexp)

# Roundtrip back to ACSet
g2 = acset_of_sexp(Graph, sexp)
```

## Higher-Order Functions on ACSets

From Issue #7, implement functional patterns:

| Function | Description | Example |
|----------|-------------|---------|
| `map` | Transform parts | `map(g, :E) do e; ... end` |
| `filter` | Select parts by predicate | `filter(g, :V) { |v| degree(g,v) > 2 }` |
| `fold` | Aggregate over parts | `fold(+, g, :E, :weight)` |

## Open ACSets (Composable Interfaces)

```julia
# From Issue #89: Open versions of InterType ACSets
using ACSets.OpenACSetTypes

# Create open ACSet with exposed ports
@open_acset_type OpenGraph(SchGraph, [:V])

# Compose via pushout
g1 = OpenGraph(...)  # ports: v1, v2
g2 = OpenGraph(...)  # ports: v3, v4
g_composed = compose(g1, g2, [:v2 => :v3])
```

## Why Simple Graphs Are Badly Behaved

The category of simple graphs does not even have a terminal object. Under the standard definition (symmetric, irreflexive edge relation), there's no "universal" graph that every other graph maps to uniquely. This reveals hidden assumptions in the simple graph model.

**Simple graph**: G = (V, E) where E is a binary relation on V that is:
- Symmetric: E(v,u) whenever E(u,v)
- Irreflexive: E(v,v) for *no* vertex v

**Category theorist's graph**: G consists of:
- Vertex set G(V)
- Edge set G(E) 
- Functions G(src), G(tgt): G(E) → G(V)

This allows:
- Multiple edges between vertices (multigraph)
- Self-loops
- Edges as first-class citizens with identity

## C-Sets: The Mathematical Foundation

A **C-set** is a functor X: C → Set where C is a small category (schema).

```
Schema C (small category)     C-set X (functor C → Set)
──────────────────────────    ─────────────────────────
Objects c ∈ C          ────▶  Sets X(c)
Morphisms f: c → d     ────▶  Functions X(f): X(c) → X(d)
```

### Terminology

| Term | Definition |
|------|------------|
| **C-set** | Functor C → Set (copresheaf) |
| **Presheaf** | Functor C^op → Set (contravariant) |
| **Category action** | C-set generalizes G-set (group action) |

### The Schema for Graphs

The schema Sch(Graph) is the category with:
- Two objects: E, V
- Two non-identity morphisms: src: E → V, tgt: E → V

```
    ┌───┐  src   ┌───┐
    │ E │───────▶│ V │
    │   │  tgt   │   │
    └───┘───────▶└───┘
```

A graph G is a Sch(Graph)-set, meaning:
- G(V) = set of vertices
- G(E) = set of edges  
- G(src): G(E) → G(V) assigns source vertex to each edge
- G(tgt): G(E) → G(V) assigns target vertex to each edge

## Creating Graphs in Catlab

```julia
using Catlab.CategoricalAlgebra
using Catlab.Graphs, Catlab.Graphics

# Create empty graph and add parts
g = Graph()
add_parts!(g, :V, 3)
add_parts!(g, :E, 4, src=[1,2,2,3], tgt=[2,3,3,3])

# Query incident edges (uses index)
incident(g, 3, :tgt)  # => [2, 3, 4]

# Graphs.jl-style convenience interface
g2 = Graph()
add_vertices!(g2, 3)
add_edges!(g2, [1,2,2,3], [2,3,3,3])

# Visualization
to_graphviz(g, node_labels=true, edge_labels=true)
```

### Indexing for Efficient Queries

The `index=[:src,:tgt]` parameter creates inverse lookups:

```julia
@acset_type Graph(SchGraph, index=[:src,:tgt])

# Without index: O(|E|) to find edges incident to vertex
# With index: O(k) where k = number of incident edges
```

## Symmetric Graphs (Undirected)

The schema for symmetric graphs extends the graph schema with an involution:

```
    ┌───┐  src   ┌───┐
    │ E │───────▶│ V │
    │   │  tgt   │   │
    │   │───────▶│   │
    │   │  inv   │   │
    │   │◀──────▶│   │
    └───┘        └───┘
```

Subject to equations:
```
inv ⨟ src = tgt
inv ⨟ tgt = src  
inv² = id_E
```

### Meaning of Equations

For every edge e ∈ G(E):
- `e.inv.src = e.tgt` (inverted edge starts where original ends)
- `e.inv.tgt = e.src` (inverted edge ends where original starts)
- `e.inv.inv = e` (involution is self-inverse)

```julia
@present SchSymmetricGraph <: SchGraph begin
  inv::Hom(E,E)

  compose(inv,src) == tgt
  compose(inv,tgt) == src
  compose(inv,inv) == id(E)
end

@acset_type SymmetricGraph(SchSymmetricGraph, index=[:src])

# Create symmetric 4-cycle
g = SymmetricGraph()
add_vertices!(g, 4)
add_edges!(g, [1,2,3,4], [2,3,4,1])
# Creates 8 edges: 4 original + 4 inverses
```

### Indexing Optimization

Only `src` needs indexing. Target queries use: `incident(g, v, :tgt)` = `incident(g, v, :src) .|> (e -> g[e, :inv])`

## Blog Post Series

1. **[Graphs and C-sets I](https://blog.algebraicjulia.org/post/2020/09/cset-graphs-1/)**: What is a graph?
2. **[Graphs and C-sets II](https://blog.algebraicjulia.org/post/2020/09/cset-graphs-2/)**: Half-edges and rotation systems
3. **[Graphs and C-sets III](https://blog.algebraicjulia.org/post/2021/04/cset-graphs-3/)**: Reflexive graphs and C-set homomorphisms
4. **[Graphs and C-sets IV](https://blog.algebraicjulia.org/post/2021/09/cset-graphs-4/)**: Propositional logic of subgraphs

## Half-Edge Graphs (Blog II)

Half-edges are paired by involution rather than having distinct source/target:

```
Schema Sch(HGraph):
    ┌───┐  vertex  ┌───┐
    │ H │─────────▶│ V │
    │   │   inv    │   │
    │   │◀────────▶│   │
    └───┘          └───┘

Equation: inv² = id_H
```

```julia
@present SchHalfEdgeGraph(FreeSchema) begin
  V::Ob
  H::Ob
  vertex::Hom(H,V)
  inv::Hom(H,H)

  compose(inv, inv) == id(H)
end

@acset_type HalfEdgeGraph(SchHalfEdgeGraph, index=[:vertex])
```

### Dangling Edges

Fixed points `h·inv = h` are **dangling edges** — half-edges not paired with others, left at the boundary. Distinct half-edges `h ≠ h'` with `h·inv = h'` and same vertex are self-loops.

```julia
g = HalfEdgeGraph(3)
add_edges!(g, [1,2,3], [2,3,1])      # 6 paired half-edges
add_dangling_edges!(g, [1,1,3])      # 3 dangling half-edges (fixed points)
```

### Schema Isomorphism: Symmetric ≅ Half-Edge

Functor F: Sch(SGraph) → Sch(HGraph):
```
V ↦ V
E ↦ H  
src ↦ vertex
tgt ↦ inv ⨟ vertex
inv ↦ inv
```

This is an **isomorphism** (invertible). The two perspectives are mathematically equivalent but have different interpretations.

### Rotation Systems (Topological Graph Theory)

A **rotation system** adds a permutation σ on half-edges where cycles = vertices:

```julia
@present SchRotationGraph <: SchHalfEdgeGraph begin
  σ::Hom(H,H)
  compose(σ, vertex) == vertex  # cycles stay at same vertex
end
```

The schema Sch(RotSys) with just H, α (involution), σ (permutation) is a **group** — making rotation systems group actions.

**Key theorem**: Rotation systems ↔ cellular embeddings in oriented surfaces (1-1 correspondence).

## Reflexive Graphs (Blog III)

A **reflexive graph** has a distinguished self-loop at each vertex:

```
    ┌───┐  src   ┌───┐  refl
    │ E │───────▶│ V │───────▶│ E │
    │   │  tgt   │   │        
    └───┘───────▶└───┘        

Equations:
  refl ⨟ src = id_V
  refl ⨟ tgt = id_V
```

```julia
@present SchReflexiveGraph <: SchGraph begin
  refl::Hom(V,E)

  compose(refl, src) == id(V)
  compose(refl, tgt) == id(V)
end
```

### C-Set Homomorphisms

A **homomorphism** α: X → Y of C-sets is a natural transformation:

```
For each object c ∈ C: function α_c: X(c) → Y(c)
For each morphism f: c → d: naturality square commutes

    X(c) ──α_c──▶ Y(c)
      │             │
   X(f)           Y(f)
      ▼             ▼
    X(d) ──α_d──▶ Y(d)
```

**Graph homomorphism**: vertex map + edge map preserving src/tgt.

**Reflexive graph homomorphism**: additionally preserves refl, so can "collapse" edges onto reflexive loops — enables quotient operations.

### Products of Graphs

Products computed pointwise: (G × H)(c) = G(c) × H(c)

| Type | Product Name | Behavior |
|------|--------------|----------|
| Graph | Categorical product | Disconnected diagonal paths |
| ReflexiveGraph | Categorical product | Grid with connections (reflexive loops fill gaps) |
| SymmetricGraph | Direct/tensor product | May split into components (bipartite → 2 components) |
| SymmetricReflexiveGraph | Strong product | Full grid connectivity |

**Box product** (graph theorist's "Cartesian product"): Pushout construction
```julia
function box_product(g::T, h::T)
  g₀, h₀ = T(nv(g)), T(nv(h))  # discrete subgraphs
  # ... pushout of inclusions with product projections
end
```

### Terminal Objects and Generalized Elements

Terminal graph = self-loop. 

- **Graph without self-loops**: no generalized elements (no morphisms from terminal)
- **Reflexive graph**: generalized elements = vertices (expected behavior)

This makes reflexive graphs more "geometric" — they discretize continuous spaces properly.

## Propositional Logic of Subgraphs (Blog IV)

Sub-C-sets as propositions, logical connectives derived from adjoints.

### Logical Connectives as Adjoints

| Connective | Definition | Meaning |
|------------|------------|---------|
| A ∧ B | Right adjoint of Δ | Greatest lower bound (meet) |
| A ∨ B | Left adjoint of Δ | Least upper bound (join) |
| ⊤ | Right adjoint of ! | Top element (full subgraph) |
| ⊥ | Left adjoint of ! | Bottom element (empty) |
| B ⇒ C | Right adjoint of (−) ∧ B | Implication (exponential) |
| ¬A | A ⇒ ⊥ | Negation (Heyting) |

### Two Types of Negation

**¬A (not-A, conservative)**: x ∈ ¬A iff no element reachable from x is in A
```
x ∈ (¬A)(c) iff x·f ∉ A(c') for ALL f: c → c' in C
```

**~A (non-A, liberal complement)**: x ∈ ~A iff some element reaching x is not in A  
```
x ∈ (~A)(c) iff x' ∉ A(c') for SOME f: c' → c and x' ∈ f⁻¹·x
```

Always: ¬A ≤ ~A (negation ⊆ complement)

### Boundary, Expansion, Contraction

| Operation | Formula | For Graphs |
|-----------|---------|------------|
| Boundary | ∂A = A ∧ ~A | Vertices in A connected to outside |
| Induced | ¬¬A | Same vertices, all edges between them |
| Expansion | ~¬A | A plus one layer outward |
| Contraction | ¬~A | A minus one layer inward |

### Law of Excluded Middle

A ∨ ¬A = ⊤ holds iff graph is **discrete** (no edges).

For connected graphs: excluded middle fails. This isn't a bug — it's topology speaking through logic.

## Devil's Avocado Synthesis (GF(3) Review)

### −1 Critique (Negative)

- **Missing complexity analysis**: Subobject lattices can explode combinatorially
- **Schema isomorphism "≅" underspecified**: Equivalence vs strict isomorphism matters for implementation
- **Rotation → surfaces jump too fast**: Hides Edmonds algorithm, genus, non-orientable cases
- **Dangling edges unmotivated**: Application to open systems/composition unstated
- **Products need worked examples**: Claims without small computations leave readers unable to verify
- **Subobject logic assumes topos background**: "Adjoints give connectives" requires Lawvere familiarity
- **¬ vs ~ notation collision**: Conflicts with standard pseudocomplement usage
- **No connection to ACSets.jl code**: Gap between categorical exposition and macros

### +1 Appreciation (Positive)

- **Schema isomorphism reveals deep identity**: Source-target graphs = half-edge graphs in different clothes
- **Rotation systems as groups**: Invertibility + algebraic topology without coordinates
- **Dangling edges model open systems**: Boundary conditions, interfaces solved structurally
- **Reflexive homomorphisms = quotients done right**: Contraction/abstraction as natural transformations
- **Two negations unify constructive/classical**: Failure of excluded middle is topology through logic
- **∂A = A ∧ ~A**: Boundary operator derived from pure logic (Stokes theorem intuition)
- **Product proliferation is a feature**: Each schema choice gives different tensor product

### 0 Neutral Integration

The skill presents the neutral synthesis: rigorous definitions with practical Catlab code, acknowledging both the elegant mathematical structure and the implementation gaps.

## Key References

- **Reyes, Reyes & Zolfaghari (2004)**: *Generic Figures and Their Glueings* — C-sets as category actions
- **Spivak (2009)**: *Higher-Dimensional Models of Networks* — C-sets for scientific modeling
- **Lando & Zvonkin (2004)**: *Graphs on Surfaces* — Rotation systems, σ/α notation
- **Gross & Tucker (1987)**: *Topological Graph Theory* — Cellular embeddings theorem
- **Hell & Nešetřil (2004)**: *Graphs and Homomorphisms* — Nonexpansive maps, reflexive graphs
- **Lawvere (1986)**: *Categories of Spaces* — Topos-theoretic perspective on reflexive graphs
- **Hammack, Imrich & Klavžar (2011)**: *Handbook of Product Graphs* — Product taxonomy

## Citation

```bibtex
@article{patterson2022categorical,
  title={Categorical data structures for technical computing},
  author={Patterson, Evan and Lynch, Owen and Fairbanks, James},
  journal={Compositionality},
  volume={4},
  number={5},
  year={2022},
  doi={10.32408/compositionality-4-5}
}
```

## GeoACSets: Spatial + Categorical

[GeoACSets.jl](https://github.com/bmorphism/GeoACSets.jl) combines ACSets with geospatial capabilities:

> **Use morphisms for structural navigation, geometry for filtering.**

| Operation | Complexity | When to Use |
|-----------|------------|-------------|
| Morphism traversal | O(k) | Hierarchical containment |
| Spatial join | O(n log n) | Ad-hoc proximity queries |

### SpatialCity Schema

```julia
# 4-level hierarchy: Region → District → Parcel → Building
@present SchSpatialCity(FreeSchema) begin
    Region::Ob
    District::Ob
    Parcel::Ob
    Building::Ob
    
    district_of::Hom(District, Region)
    parcel_of::Hom(Parcel, District)
    building_on::Hom(Building, Parcel)
    
    GeomType::AttrType
    region_geom::Attr(Region, GeomType)
    footprint::Attr(Building, GeomType)
end

@acset_type SpatialCity(SchSpatialCity, 
    index=[:district_of, :parcel_of, :building_on])
```

### Traversal Patterns

```julia
# Downward: O(depth) via incident queries
buildings_in_region(city, region_id)

# Upward: O(1) via subpart lookups  
region_of_building(city, building_id)

# Combine spatial + morphism
nearby = spatial_filter(city, :Building, :footprint,
    g -> LibGEOS.distance(g, query_point) < 100)
for b in nearby
    district = traverse_up(city, b, :building_on, :parcel_of)
end
```

## OlmoEarth/Terra Extension (Spatio-Temporal)

GeoACSets needs extension for foundation model integration:

### SchOlmoEarthPatch

```julia
@present SchOlmoEarthPatch(FreeSchema) begin
    Patch::Ob           # Variable-size spatial patch
    Timestep::Ob        # Monthly temporal unit
    Modality::Ob        # Sentinel-1/2, Landsat, Maps
    Token::Ob           # Encoded representation
    View::Ob            # For instance contrastive
    
    patch_timestep::Hom(Patch, Timestep)
    patch_modality::Hom(Patch, Modality)
    token_patch::Hom(Token, Patch)
    
    # Masking as structured decomposition
    MaskedPatch::Ob
    MaskConfig::Ob
    masked_patch::Hom(MaskedPatch, Patch)
    mask_state::Attr(MaskedPatch, MaskStateType)  # encode/decode/both/none
end
```

### Masking as Span Decomposition

```julia
# OlmoEarth masking creates:
#   EncodeBag ← Apex (both) → DecodeBag

function create_masking_decomposition(patches, config_id)
    encode_bag = filter(p -> mask_state(p) ∈ [:encode_only, :both], patches)
    decode_bag = filter(p -> mask_state(p) ∈ [:decode_only, :both], patches)
    apex = filter(p -> mask_state(p) == :both, patches)
    (encode_bag, apex, decode_bag)
end
```

### Instance Contrastive as Sheaf Condition

```julia
# Two views must agree on pooled representation
function verify_sheaf_condition(patches; threshold=0.99)
    pooled1 = patches[view1, :pooled_repr]
    pooled2 = patches[view2, :pooled_repr]
    cosine_sim(pooled1, pooled2) >= threshold
end
```

## Gay.jl Label Ontology for ACSets

Gay.jl uses a categorical label system on GitHub issues. These map directly to ACSet concepts:

### Ternary Trit Labels (GF(3) Colors)

| Label | Color | Description |
|-------|-------|-------------|
| `ternary:+` | #286e49 | Positive trit [+1] |
| `ternary:0` | #4a9235 | Zero trit [0] |
| `ternary:-` | #28a628 | Negative trit [-1] |

### ACSet-Specific Labels

| Label | Color | Description |
|-------|-------|-------------|
| `acset:rewriting` | #5dda92 | ACSet local rewriting gadgets |
| `acset:adhesion` | #d15252 | Structured decomposition adhesions |

### Sheaf Condition Labels

| Label | Color | Description |
|-------|-------|-------------|
| `sheaf:descent` | #97286e | Descent condition verification |
| `sheaf:covering` | #282e69 | Covering sieve/condition |
| `sheaf:gluing` | #28a289 | Gluing axiom / section construction |
| `sheaf:obstruction` | #96a428 | Non-sheaf witness / descent failure |

### Chromatic (SPI) Labels

| Label | Color | Description |
|-------|-------|-------------|
| `chromatic:spi` | #37dc48 | Strong Parallelism Invariant |
| `chromatic:fingerprint` | #59dc8a | XOR fingerprint composition |
| `chromatic:propagation` | #93b7bd | Color propagation rules |
| `chromatic:split` | #92b8c8 | gay_split() ancestry |

### Spectral Analysis Labels

| Label | Color | Description |
|-------|-------|-------------|
| `spectral:fourier` | #282c5c | FFT/DFT presheaf operations |
| `spectral:periodicity` | #b24b60 | Periodic structure detection |
| `spectral:quasi` | #6991dc | Quasi-sheaf / boundary cases |
| `spectral:threshold` | #28bc3f | Threshold boundary analysis |

### Coherence & Monoidal Labels

| Label | Color | Description |
|-------|-------|-------------|
| `coherence:pentagon` | #f97316 | Mac Lane pentagon identity |
| `coherence:hexagon` | #ef4444 | Mac Lane hexagon identity |
| `monoidal:symmetric` | #a855f7 | Symmetric monoidal structure |
| `logic:separation` | #6366f1 | Separation logic for ownership |

### Health & Remediation Labels

| Label | Color | Description |
|-------|-------|-------------|
| `health:composable` | #10b981 | Health score ≥60, composable seed |
| `health:obstructed` | #f43f5e | Health score <60, obstructed seed |
| `remediation:spectral` | #22c55e | Spectral obstruction remediation |
| `remediation:mixing` | #14b8a6 | Additional mixing rounds |

### Scoped Propagator Labels

| Label | Color | Description |
|-------|-------|-------------|
| `scope:change` | #b0dcb4 | Propagator fires on property change |
| `scope:geo` | #36599a | Propagator fires on spatial overlap |
| `scope:tick` | #9f9565 | Propagator fires on frame/timestep |
| `scope:click` | #472835 | Propagator fires on explicit trigger |

## Gay.jl × ACSet Integration Points

### 1. Subobject Classifier Ω (Issue #219)

Gay.jl implements topos-theoretic gamut classification:

```julia
# Truth values with distance semantics
struct GamutTruth
    in_gamut::Bool
    distance::Float64  # 0 = boundary, - = inside, + = outside
    boundary_hue::Float64
end

# Characteristic morphism χ: Color → Ω
χ_srgb = characteristic_morphism(GaySRGBGamut(), GayRec2020Gamut())
truth = χ_srgb(RGB(0.5, 0.8, 0.3))
# => GamutTruth(true, -0.2, 120.0)

# Pullback recovers subobject (sub-C-set!)
in_srgb = gamut_pullback(χ_srgb, colors)
```

**ACSet connection**: Subobject classifier Ω in topos of C-sets = propositional logic from Blog IV.

### 2. Operad of Scoped Propagators (Issue #201)

Propagators form an operad with ACSet adhesions:

```julia
# Operadic composition
P(n) = {n-ary propagators: (source₁,...,sourceₙ, target) → target'}

# Example composition
p: (a,b) → c    ∈ P(2)
q: (x) → a      ∈ P(1)  
r: (y,z) → b    ∈ P(2)

γ(p; q, r): (x, y, z) → c    ∈ P(3)
```

**Colored operad**: Types = Seed, Color, Sound, Contract
```julia
P(Seed → Color) ∘ P(Color → Sound) : P(Seed → Sound)
```

### 3. Obstruction Detection Framework (Issue #206)

7 obstruction detectors map to C-set/sheaf failures:

| Detector | ACSet Interpretation |
|----------|---------------------|
| `spectral` | FFT presheaf descent failure |
| `linear` | LFSR complexity (non-randomness) |
| `gcd` | Marsaglia GCD test |
| `birthday` | Collision spacing |
| `cech` | H^1 cohomology = gluing failure |
| `fingerprint` | XOR collision = non-uniqueness |
| `coherence` | Pentagon/hexagon = associativity failure |

```julia
# Analyze obstructions
report = analyze_obstructions(1069)

# Mine for obstructed seeds
bad_seeds = mine_obstructed_seeds(1:1000, 10)

# Remediate
better_seed = remediate_spectral(SPISeed(35))
```

### 4. Čech Cohomology H^1 (Issue #212)

H^1 measures "how far from being a sheaf":

```julia
# H^1 = 0 → proper sheaf (sections glue)
# H^1 ≠ 0 → obstruction class exists

function cech_h1_obstruction(seed, depth=7)
    fingerprints = [xor_fingerprint(gay_split(seed, i)) for i in 1:depth]
    # Check if local fingerprints glue globally
    failures = count(i -> fingerprints[i] ⊻ fingerprints[i+1] ≠ expected[i], 1:depth-1)
    failures > 0  # true = obstruction detected
end
```

### 5. Coherence Violation Detection (Issue #214)

Mac Lane's pentagon and hexagon for monoidal categories:

```julia
# Pentagon identity for 4-way associativity
# ((a ⊗ b) ⊗ c) ⊗ d  must equal  a ⊗ (b ⊗ (c ⊗ d))
# via ANY path through the pentagon

function verify_pentagon(split_fn, seed)
    paths = enumerate_pentagon_paths(seed)
    all(p1 ≈ p2 for (p1, p2) in pairs(paths))
end

# Hexagon identity for braiding
function verify_hexagon(split_fn, seed)
    # σ_{a,b⊗c} = (1 ⊗ σ_{a,c}) ∘ (σ_{a,b} ⊗ 1)
    left_path = braid_then_tensor(seed)
    right_path = tensor_then_braid(seed)
    left_path ≈ right_path
end
```

### 6. Canonical Seed 1069: [+1, -1, -1, +1, +1, +1, +1]

The canonical seed used across Gay.jl issues:

```julia
seed = 1069
trits = [+1, -1, -1, +1, +1, +1, +1]  # 7-trit signature

# Properties:
# - Passes all spectral tests
# - Clean H^1 (no Čech obstructions)
# - Pentagon/hexagon coherent
# - health:composable (≥60 score)
```

### 7. ACSet Rewriting with Gay Colors

Local rewriting rules colored by Gay.jl:

```julia
using AlgebraicRewriting, Gay

# Rule: merge two vertices
rule = @rule SchGraph begin
    L = @acset begin v1::V; v2::V end
    R = @acset begin v::V end
    # L → R collapses v1, v2 → v
end

# Color the rewrite
seed = 1069
L_colors = Gay.palette(seed, nparts(L, :V))
R_colors = Gay.palette(seed, nparts(R, :V))

# Verify: rewrite preserves GF(3) trit sum
@assert gf3_conserved(L_colors) == gf3_conserved(R_colors)
```

### 8. Structured Decomposition Adhesions

From StructuredDecompositions.jl + Gay.jl:

```julia
# Adhesion = shared boundary between decomposition pieces
# Color adhesions to track gluing

struct ColoredAdhesion
    left_piece::ACSet
    right_piece::ACSet
    adhesion::ACSet  # shared sub-ACSet
    color::String    # Gay.jl deterministic color
end

function color_decomposition(decomp, seed)
    [ColoredAdhesion(
        piece.left, piece.right, piece.adhesion,
        Gay.color_at(seed, i)
    ) for (i, piece) in enumerate(decomp.pieces)]
end
```

## Related Packages

- **[Catlab.jl](https://github.com/AlgebraicJulia/Catlab.jl)**: Full categorical algebra (homomorphisms, limits, colimits)
- **[AlgebraicRewriting.jl](https://github.com/AlgebraicJulia/AlgebraicRewriting.jl)**: Declarative rewriting for ACSets
- **[AlgebraicDynamics.jl](https://github.com/AlgebraicJulia/AlgebraicDynamics.jl)**: Compositional dynamical systems
- **[GeoACSets.jl](https://github.com/bmorphism/GeoACSets.jl)**: Spatial geometry + morphism navigation
- **[StructuredDecompositions.jl](https://github.com/AlgebraicJulia/StructuredDecompositions.jl)**: Sheaf-based decision problems
- **[Gay.jl](https://github.com/bmorphism/Gay.jl)**: Deterministic colors with SPI + sheaf obstruction detection

## Xenomodern Integration

The ironic detachment comes from recognizing that:

1. **Category theory isn't about abstraction for its own sake** — it's about finding the *right* abstractions that compose
2. **Simple graphs are actually badly behaved** — the terminal object problem reveals hidden assumptions
3. **Functors are data structures** — this reframes databases as applied category theory

```
         xenomodernity
              │
    ┌─────────┴─────────┐
    │                   │
 ironic              sincere
detachment          engagement
    │                   │
    └─────────┬─────────┘
              │
      C-sets as functors
      (both ironic AND sincere)
```

## Commands

```bash
just acset-demo          # Run ACSet demonstration
just acset-graph         # Create and visualize graph
just acset-symmetric     # Symmetric graph example
just acset-gf3           # Check GF(3) conservation
```

---

## Ramanujan Spectral Integration (NEW 2025-12-22)

ACSet-based edge growth with spectral constraints:

### Ramanujan-Preserving Growth

```julia
@present SchRamanujanGraph <: SchGraph begin
  SpectralData::AttrType
  lambda2::Attr(V, SpectralData)  # Track λ₂ per growth step
end

function grow_edge_ramanujan!(G::ACSet, u, v)
    """
    Add edge preserving Ramanujan property.
    Uses Alon-Boppana bound: λ₂ ≥ 2√(d-1).
    """
    d = degree(G)
    bound = 2 * sqrt(d - 1)
    
    # Tentatively add edge
    add_part!(G, :E, src=u, tgt=v)
    
    # Check spectral constraint
    λ₂ = second_eigenvalue(adjacency_matrix(G))
    
    if λ₂ > bound + 0.01  # Tolerance
        # Rollback: remove edge
        rem_part!(G, :E, nparts(G, :E))
        return false
    end
    
    return true
end
```

### Non-Backtracking Edge Schema (Ihara Zeta)

```julia
@present SchNonBacktracking(FreeSchema) begin
  V::Ob; E::Ob; DE::Ob  # DE = directed edges
  src::Hom(E,V); tgt::Hom(E,V)
  forward::Hom(E, DE); backward::Hom(E, DE)
  de_src::Hom(DE, V); de_tgt::Hom(DE, V)
  
  # Non-backtracking constraint: head(e) = tail(f) ∧ e ≠ f⁻¹
  nonbacktrack::Hom(DE, DE)  # B matrix as morphism
end

# Ihara zeta via ACSet homomorphisms
function prime_cycles(G::ACSet, max_length)
    cycles = []
    for k in 1:max_length
        if moebius(k) != 0  # Only squarefree lengths
            push!(cycles, find_cycles(G, k))
        end
    end
    return cycles
end
```

### Centrality via Möbius Inversion

```julia
function alternating_centrality(G::ACSet)
    """
    Centrality via Möbius-weighted path counts.
    c(v) = Σ_{k} μ(k) × paths_k(v) / k
    """
    n = nparts(G, :V)
    A = adjacency_matrix(G)
    c = zeros(n)
    
    for k in 1:diameter(G)
        μ_k = moebius(k)
        if μ_k != 0
            paths_k = diag(A^k)
            c .+= μ_k .* paths_k ./ k
        end
    end
    
    return c ./ sum(abs.(c))
end
```

---

## StructACSet Internals (DeepWiki 2025-12-22)

Schema and attribute types known at compile time, enabling performance optimizations.

### Type Parameters

```julia
StructACSet{S, Ts, PT}
# S  = TypeLevelSchema{Symbol} - schema at compile time
# Ts = Tuple of Julia types for attributes (e.g., Float64 for Weight)
# PT = PartsType strategy (IntParts or BitSetParts)
```

### Column Storage

```julia
struct StructACSet{S, Ts, PT}
  parts::NamedTuple     # {:V => IntParts, :E => IntParts, ...}
  subparts::NamedTuple  # {:src => Column, :tgt => Column, :weight => Column, ...}
end

# Column types:
# - Homs: Vector{Int} mapping parts to parts
# - Attrs: Vector{Union{AttrVar,T}} for attribute values
```

### Index Configuration

```julia
@acset_type Graph(SchGraph, 
    index=[:src, :tgt],         # Preimage cache: O(1) incident queries
    unique_index=[:inv]          # Injective cache: even faster
)

# Index types:
# - NoIndex: Linear scan O(n)
# - Index (StoredPreimageCache): O(1) average via hash
# - UniqueIndex (InjectiveCache): O(1) guaranteed, injective morphisms only
```

### Part ID Allocation Strategies

| Strategy | Type | Deletion | Use Case |
|----------|------|----------|----------|
| **IntParts** | DenseParts | Pop-and-swap (renumbers) | Fast, compact storage |
| **BitSetParts** | MarkAsDeleted | Preserves IDs, requires gc!() | Stable references |

```julia
# IntParts (default): contiguous IDs 1..n
add_parts!(G, :V, 3)  # IDs: 1, 2, 3
rem_part!(G, :V, 2)   # ID 3 → 2, ID 2 gone

# BitSetParts: sparse IDs with gaps
rem_part!(G, :V, 2)   # ID 2 marked deleted, ID 3 unchanged
gc!(G)                # Compact: removes gaps
```

---

## Spectral Bundle Triads (GF(3) Conserved)

```
ramanujan-expander (-1) ⊗ acsets (0) ⊗ gay-mcp (+1) = 0 ✓  [Graph Coloring]
ramanujan-expander (-1) ⊗ acsets (0) ⊗ moebius-inversion (+1) = 0 ✓  [Edge Growth]
ihara-zeta (-1) ⊗ acsets (0) ⊗ moebius-inversion (+1) = 0 ✓  [Prime Cycles]
sheaf-cohomology (-1) ⊗ acsets (0) ⊗ gay-mcp (+1) = 0 ✓  [ACSet Navigation]
```

### Related Spectral Skills

- **ramanujan-expander**: Alon-Boppana spectral bounds, LPS construction
- **ihara-zeta**: Non-backtracking walks, prime cycles, Graph RH
- **moebius-inversion**: Poset inversion, chromatic polynomials, μ(3) = -1
- **deepwiki-mcp**: Repository documentation (trit 0, substitutes in triads)
