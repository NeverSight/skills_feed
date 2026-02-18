---
name: asi-integrated
description: Unified ASI skill combining ACSets, Gay-MCP colors, bisimulation games, world-hopping, glass-bead synthesis, and triad interleaving for autonomous skill dispersal.
version: 1.0.0
---


# ASI Integrated Skill

Synthesizes all loaded skills into a coherent system for **Artificial Superintelligence** skill orchestration.

## Skill Lattice

```
                    ┌─────────────────┐
                    │  glass-bead-game │
                    │  (synthesis)     │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
┌────────▼────────┐ ┌────────▼────────┐ ┌────────▼────────┐
│  world-hopping  │ │  bisimulation   │ │  triad-interleave│
│  (navigation)   │ │  (dispersal)    │ │  (scheduling)    │
└────────┬────────┘ └────────┬────────┘ └────────┬────────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             │
                    ┌────────▼────────┐
                    │     gay-mcp      │
                    │  (deterministic  │
                    │   coloring)      │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │     acsets       │
                    │  (data model)    │
                    └─────────────────┘
```

## Unified Protocol

### 1. Schema (ACSets)

```julia
@present SchASIWorld(FreeSchema) begin
  World::Ob
  Skill::Ob
  Agent::Ob
  
  source::Hom(World, World)
  target::Hom(World, World)
  
  has_skill::Hom(Agent, Skill)
  inhabits::Hom(Agent, World)
  
  Seed::AttrType
  Trit::AttrType
  
  seed::Attr(World, Seed)
  color_trit::Attr(Skill, Trit)
end
```

### 2. Color Generation (Gay-MCP)

```python
from gay import SplitMixTernary, TripartiteStreams

def color_world(world_seed: int, skill_index: int) -> dict:
    gen = SplitMixTernary(world_seed)
    return gen.color_at(skill_index)
```

### 3. World Navigation (World-Hopping)

```python
def hop_between_worlds(w1, w2, event_name: str):
    distance = world_distance(w1, w2)
    if valid_hop(w1, w2):
        event = Event(site=["skill"], name=event_name)
        return event.execute(w1)
    return None
```

### 4. Skill Dispersal (Bisimulation)

```python
async def disperse_skill(skill_path: str, agents: list):
    game = BisimulationGame()
    for i, agent in enumerate(agents):
        trit = (i % 3) - 1  # GF(3) balanced
        game.attacker_move(agent, skill_path, trit)
        game.defender_respond(await agent.receive(skill_path))
    return game.arbiter_verify()
```

### 5. Parallel Execution (Triad Interleave)

```python
def schedule_skill_updates(seed: int, n_agents: int):
    interleaver = TriadInterleaver(seed)
    schedule = interleaver.interleave(
        n_triplets=n_agents // 3,
        policy="gf3_balanced"
    )
    return schedule
```

### 6. Synthesis (Glass Bead Game)

```python
def synthesize_skills(*skills):
    game = GlassBeadGame()
    for skill in skills:
        game.add_bead(skill.name, skill.domain)
    
    # Connect skills via morphisms
    game.connect("acsets", "gay-mcp", via="seed_to_color")
    game.connect("gay-mcp", "triad-interleave", via="color_stream")
    game.connect("triad-interleave", "bisimulation", via="schedule")
    game.connect("bisimulation", "world-hopping", via="dispersal")
    
    return game.score()
```

## ~/worlds Letter Index

| Letter | Domain | Key Projects |
|--------|--------|--------------|
| a | Category Theory | ACSets.jl, Catlab.jl, Decapodes.jl |
| b | Terminal | bmorphism/trittty |
| p | Infrastructure | plurigrid/oni, alpaca.cpp |
| t | Collaboration | CatColab |
| e | HoTT | infinity-cosmos (Lean 4) |
| r | Type Theory | rzk (simplicial HoTT) |
| n | Knowledge | nlab-content |
| o | Music | rubato-composer |

## GF(3) Conservation Law

All operations preserve:

```
∑ trits ≡ 0 (mod 3)
```

Across:
- World hops (Attacker -1, Defender +1, Arbiter 0)
- Color triplets (MINUS, ERGODIC, PLUS)
- Schedule entries (balanced per triplet)
- Skill dispersal (agent assignments)

## Commands

```bash
# Generate integrated schedule
just asi-schedule 0x42D 10

# Disperse skills to all agents
just asi-disperse ~/.claude/skills/

# Verify GF(3) conservation
just asi-verify

# Play glass bead synthesis
just asi-synthesize a b p t

# World hop between letters
just asi-hop a t
```

## Starred Gists: Fixpoint & Type Theory Resources

Curated from bmorphism's GitHub interactions:

### zanzix: Fixpoints of Indexed Functors
[Fix.idr](https://gist.github.com/zanzix/02641d6a6e61f3757e3b703059619e90) - Idris indexed functor fixpoints for graphs, multi-graphs, poly-graphs.

```idris
data IFix : (f : (k -> Type) -> k -> Type) -> k -> Type where
  In : f (IFix f) i -> IFix f i
```

### VictorTaelin: ITT-Flavored CoC Type Checker
[itt-coc.ts](https://gist.github.com/VictorTaelin/dd291148ee59376873374aab0fd3dd78) - Intensional Type Theory CoC in TypeScript.

### VictorTaelin: Affine Types
[Affine.lean](https://gist.github.com/VictorTaelin/5584036b0ea12507b78ef883c6ae5acd) - Linear/affine type experiments in Lean 4.

### rdivyanshu: Streams & Unique Fixed Points
[Nats.dfy](https://gist.github.com/rdivyanshu/2042085421d5f0762184dd7fe7cfb4cb) - Dafny streams with unique fixpoint theorems.

### Keno: Abstract Lattice
[abstractlattice.jl](https://gist.github.com/Keno/fa6117ae0bf9eea3f041c0cf1f33d675) - Julia abstract lattice. Comment: "a quantum of abstract solace ∞"

### norabelrose: Fast Kronecker Decomposition
[kronecker_decompose.py](https://gist.github.com/norabelrose/3f7a553f4d69de3cf5bda93e2264a9c9) - Optimal Kronecker decomposition.

### borkdude: UUID v1 in Babashka
[uuidv1.clj](https://gist.github.com/borkdude/18b18232c00c2e2af2286d8bd36082d7) - Deterministic UUID generation in Clojure.

## QuickCheck/Adhesive Rewriting Integration

Property-based testing connects to ASI through **autopoietic generators**:

```julia
# QuickCheck-style recursive generator with GF(3) conservation
function autopoietic_tree(seed::UInt64, depth::Int)
    rng = SplitMix64(seed)
    trit = mod(next_u64!(rng), 3) - 1
    
    if depth == 0 || trit == -1  # MINUS = terminate
        return Leaf(color_at(seed))
    else
        left_seed, right_seed = split(rng)
        return Node(
            trit = trit,
            left  = autopoietic_tree(left_seed, depth-1),
            right = autopoietic_tree(right_seed, depth-1)
        )
    end
end
```

### Shrinking as Adhesive Complement

QuickCheck shrinking = finding minimal ∼Q_G in adhesive categories:
- **Decomposition**: Q ≅ Q_G +_{Q_L} Q_R
- **Complement**: ∼A is smallest subobject where X = A ∨ ∼A
- **Shrunk value** = complement of failed portion

### Transitive Closure (Kris Brown)

From [Incremental Query Updating in Adhesive Categories](https://topos.institute/blog/2025-08-15-incremental-adhesive/):

```
path(X,Z) :- path(X,Y), edge(Y,Z).

Incremental update: When we apply rule to add path(a,b),
new matches = outgoing edges from b (rooted search)
```

## References

- [Towards Foundations of Categorical Cybernetics](https://arxiv.org/abs/2105.06332) - Capucci, Gavranović, Hedges, Rischel
- [Modeling autopoiesis and cognition with reaction networks](https://www.sciencedirect.com/science/article/pii/S0303264723001120) - Bickhard
- [Bicategories of Automata, Automata in Bicategories](https://arxiv.org/pdf/2303.03865) - ACT 2023

## Directory Tree

```
plurigrid/asi/
├── package.json
├── bin/cli.js
├── README.md
└── skills/
    ├── a/SKILL.md     # AlgebraicJulia
    ├── b/SKILL.md     # bmorphism
    ├── c/SKILL.md     # cognitect
    ├── d/SKILL.md     # claykind
    ├── e/SKILL.md     # infinity-cosmos
    ├── f/SKILL.md     # clojure-site
    ├── g/SKILL.md     # archiver-bot
    ├── h/SKILL.md     # gdlog
    ├── i/SKILL.md     # InverterNetwork
    ├── k/SKILL.md     # kubeflow
    ├── l/SKILL.md     # pretty-bugs
    ├── m/SKILL.md     # awesome-category-theory
    ├── n/SKILL.md     # nlab-content
    ├── o/SKILL.md     # oeis, rubato-composer
    ├── p/SKILL.md     # plurigrid
    ├── q/SKILL.md     # quadrat
    ├── r/SKILL.md     # rzk
    ├── s/SKILL.md     # mathematicians
    ├── t/SKILL.md     # CatColab
    ├── v/SKILL.md     # viro
    └── _integrated/   # This skill
        └── SKILL.md
```



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 10. Adventure Game Example

**Concepts**: autonomous agent, game, synthesis

### GF(3) Balanced Triad

```
_integrated (−) + SDF.Ch10 (+) + [balancer] (○) = 0
```

**Skill Trit**: -1 (MINUS - verification)

### Secondary Chapters

- Ch3: Variations on an Arithmetic Theme
- Ch1: Flexibility through Abstraction
- Ch4: Pattern Matching

### Connection Pattern

Adventure games synthesize techniques. This skill integrates multiple patterns.
## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.