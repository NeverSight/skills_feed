---
name: asi-polynomial-operads
description: ASI skill integrating polynomial functors, free monad/cofree comonad
version: 1.0.0
---


# ASI Polynomial Operads Skill

> *"Pattern runs on matter: The free monad monad as a module over the cofree comonad comonad"*
> — Libkind & Spivak (ACT 2024)

## 1. Polynomial Functors (Spivak)

### Core Definition
A polynomial functor $p: \text{Set} \to \text{Set}$ is a sum of representables:

$$p \cong \sum_{i \in p(1)} y^{p[i]}$$

Where:
- $p(1)$ = set of **positions** (questions, observations)
- $p[i]$ = set of **directions** at position $i$ (answers, actions)

### Morphisms (Dependent Lenses)
A lens $f: p \to q$ is a pair $(f_1, f^\sharp)$:

$$f_1: p(1) \to q(1) \quad \text{(on-positions)}$$
$$f^\sharp_i: q[f_1(i)] \to p[i] \quad \text{(on-directions, contravariant)}$$

### Hom-set Formula
$$\text{Poly}(p, q) \cong \prod_{i \in p(1)} \sum_{j \in q(1)} p[i]^{q[j]}$$

## 2. Composition Products

### Substitution ($\triangleleft$) — The Module Action
$$p \triangleleft q \cong \sum_{i \in p(1)} \sum_{\bar{j}: p[i] \to q(1)} y^{\sum_{a \in p[i]} q[\bar{j}(a)]}$$

**Interpretation:** Substitute $q$ into each "hole" of $p$.

### Parallel/Dirichlet ($\otimes$)
$$p \otimes q \cong \sum_{i \in p(1)} \sum_{j \in q(1)} y^{p[i] \times q[j]}$$

**Interpretation:** Independent parallel execution.

### Categorical Product ($\times$)
$$p \times q \cong \sum_{i \in p(1)} \sum_{j \in q(1)} y^{p[i] + q[j]}$$

## 3. Free Monad & Cofree Comonad

### Cofree Comonad as Limit
The carrier $t_p$ of the cofree comonoid on $p$:

$$t_p = \lim \left( 1 \xleftarrow{!} p \triangleleft 1 \xleftarrow{p \triangleleft !} p^{\triangleleft 2} \triangleleft 1 \leftarrow \cdots \right)$$

### Trees as Positions
$$t_p \cong \sum_{T \in \text{tree}_p} y^{\text{vtx}(T)}$$

- $\text{tree}_p$ = set of $p$-trees (possibly infinite)
- $\text{vtx}(T)$ = vertices (rooted paths) of tree $T$

### Comonoid Structure
- **Counit (Extract):** $\epsilon_p: t_p \to y$ — picks the root
- **Comultiplication (Duplicate):** $\delta_p: t_p \to t_p \triangleleft t_p$ — path concatenation

### Module Action: Pattern Runs On Matter
$$\Xi_{p,q} : \mathfrak{m}p \otimes \mathfrak{c}q \to \mathfrak{m}(p \otimes q)$$

Where:
- $\mathfrak{m}p$ = free monad (Pattern, decision trees, wellfounded)
- $\mathfrak{c}q$ = cofree comonad (Matter, behavior trees, non-wellfounded)

**Examples:**
| Pattern | Matter | Runs On |
|---------|--------|---------|
| Interview script | Person | Interview |
| Program | OS | Execution |
| Voting scheme | Voters | Election |
| Game rules | Players | Game |
| Musical score | Performer | Performance |

## 4. Dynamical Systems (Libkind-Spivak)

### Discrete Dynamical System
$$f^{upd}: A \times S \to S \quad \text{(update)}$$
$$f^{rdt}: S \to B \quad \text{(readout)}$$

### Continuous Dynamical System
$$f^{dyn}: A \times S \to TS \quad \text{(dynamics: } \dot{s} = f^{dyn}(a, s) \text{)}$$
$$f^{rdt}: S \to B \quad \text{(readout)}$$

### Wiring Diagram Composition
For $\phi: X \to Y$:
$$\phi^{in}: X^{in} \to X^{out} + Y^{in}$$
$$\phi^{out}: Y^{out} \to X^{out}$$

### Composed Update
$$\bar{f}^{upd}(y, s) := f^{upd}(\phi^{in}(y, f^{rdt}(s)), s)$$
$$\bar{f}^{rdt}(s) := \phi^{out}(f^{rdt}(s))$$

## 5. Compositional Algorithms (Bumpus)

### Structured Decomposition
$$d: \int G \to \mathbf{K}$$

Where $\int G$ is the Grothendieck construction.

### Complexity Bound
$$O\left(\max_{x \in VG} \alpha(dx) + \kappa^{|S|} \kappa^2\right) |EG|$$

Where:
- $G$ = shape graph of decomposition
- $S$ = feedback vertex set
- $\kappa$ = max local solution space size
- $\alpha(c)$ = time to compute sheaf on object $c$

### Tree-Shaped Bound
For tree-shaped decompositions ($|S| = 0$):
$$O(\kappa^2) |EG|$$

## 6. Cohomological Obstructions (Bumpus)

### Čech Cohomology
$$H^n(X, \mathcal{U}, F) := \ker(\delta^n) / \text{im}(\delta^{n-1})$$

### Global Existence Constraint
$$FX \neq \emptyset \iff H^0(X, \mathfrak{M}F) = 0$$

**Interpretation:** A problem has a solution iff the zeroth cohomology of its model-collecting presheaf is trivial.

### GF(3) Connection
While Bumpus uses $\mathbb{Z}[S]$ (free Abelianization), the methods generalize to:
- $\text{Vect}(\mathbb{F}_3)$ — vector spaces over GF(3)
- Balanced ternary conservation = cohomological constraint

## 7. Spined Categories (Bumpus)

### Definition
A spined category $(\mathcal{C}, \Omega, \mathfrak{P})$:
- $\Omega: \mathbb{N}_{=} \to \mathcal{C}$ — the spine functor
- $\mathfrak{P}$ — proxy pushout operation

### Proxy Pushout
For span $G \xleftarrow{g} \Omega_n \xrightarrow{h} H$:
$$G \xrightarrow{\mathfrak{P}(g,h)_g} \mathfrak{P}(g,h) \xleftarrow{\mathfrak{P}(g,h)_h} H$$

### Chordal Objects (Recursive)
Smallest set $S$ where:
1. $\Omega_n \in S$ for all $n$
2. $\mathfrak{P}(a,b) \in S$ for $A, B \in S$ and arrows to $\Omega_n$

### Width/Triangulation
$$\Delta[X] = \min \{ \text{width}(\delta) \mid \delta: X \hookrightarrow H \text{ pseudo-chordal}\}$$

## 8. Open Games (Hedges)

### Parametrised Lens (Arena)
```
ParaLens p q x s y r = (get, put)
  get : p → x → y        -- forward
  put : p → x → r → (s, q)  -- backward
```

The 6 wires:
- `x` = observed states (from past)
- `y` = output states (to future)
- `r` = utilities received (from future)
- `s` = back-propagated utilities (to past)
- `p` = strategies (parameters)
- `q` = rewards (co-parameters)

### Sequential Composition
```haskell
(MkLens get put) >>>> (MkLens get' put') =
  MkLens
    (\(p, p') x -> get' p' (get p x))           -- compose forward
    (\(p, p') x t ->
      let (r, q') = put' p' (get p x) t         -- future first
          (s, q) = put p x r                     -- then past
      in (s, (q, q')))
```

**Key insight:** Backward pass = constraint propagation / abduction.

### Equilibrium
$$E_G(x, k) := \varepsilon_G(x; A_G; k)$$

Where $\varepsilon = \bigotimes_{p \in P} \varepsilon_p$ is the joint selection function.

## 9. Integration: DiscoHy Operads

### The 7 Operad Network
| Operad | Trit | Description |
|--------|------|-------------|
| Little Disks (E₂) | +1 | Non-overlapping disk configurations |
| Cubes (E_∞) | -1 | Infinite-dimensional parallelism |
| Cactus | -1 | Trees with cycles (self-modification) |
| Thread | 0 | Linear continuations + DuckDB |
| Gravity | -1 | Moduli M_{0,n} with involutions |
| Modular | +1 | All genera, runtime polymorphism |
| Swiss-Cheese | +1 | Open/closed for forward-only learning |

**GF(3) Total:** $(+1) + (-1) + (-1) + (0) + (-1) + (+1) + (+1) = 0$ ✓

### Libkind-Spivak Dynamical Operads
| Operad | Trit | Type |
|--------|------|------|
| Directed (⊳) | +1 | Output → Input wiring |
| Undirected (○) | -1 | Interface matching via pullback |
| Machines | 0 | State machines with dynamics |
| Dynamical | +1 | Open ODEs |

## 10. General Intelligence Requirements (Swan/Hedges)

From "Road to General Intelligence":

### Value Proposition
General intelligence must:
1. **Perform work on command** — respond to dynamic goal changes
2. **Scale to real-world concerns**
3. **Respect safety constraints**
4. **Be explainable and auditable**

### Structural Causal Model
$$X_i = f_i(\text{PA}_i, U_i), \quad i = 1, \ldots, n$$

Where:
- $\text{PA}_i$ = parent nodes
- $U_i$ = exogenous noise (jointly independent)

### Ladder of Causality
1. **Observational** — statistical learning
2. **Interventional** — setting variables despite natural processes
3. **Counterfactual** — inferences from alternate histories

### Lens-Based Abduction
| Component | Role |
|-----------|------|
| get (forward) | Induction / forward inference |
| put (backward) | Abduction / constraint propagation |
| Selection function | Attention mechanism |
| Equilibrium checking | Reflective reasoning |

## 11. Commands

```bash
# Run polynomial functor demo
just poly-functor-demo

# Test free monad / cofree comonad pairing
just monad-test

# Run DiscoHy operads
python3 src/operads/relational_operad_interleave.py

# Run Libkind-Spivak dynamical systems
python3 src/operads/libkind_spivak_dynamics.py

# Check GF(3) conservation
just gf3-verify
```

## 12. File Locations

```
lib/
├── free_monad.rb              # Pattern (decision trees)
├── cofree_comonad.rb          # Matter (behavior trees)
├── runs_on.rb                 # Module action implementation
└── discohy.hy                 # Hy operad implementations

src/music_topos/
├── free_monad.clj             # Clojure Pattern
├── cofree_comonad.clj         # Clojure Matter
├── runs_on.clj                # Module action
└── operads/
    ├── relational_operad_interleave.py
    ├── libkind_spivak_dynamics.py
    └── infinity_operads.py

scripts/
├── discohy_operad_1_little_disks.py
├── discohy_operad_2_cubes.py
├── discohy_operad_3_cactus.py
├── discohy_operad_4_thread.py
├── discohy_operad_5_gravity.lisp
├── discohy_operad_6_modular.bb
└── discohy_operad_7_swiss_cheese.py
```

## 13. References

1. **Spivak, D.I.** — *Polynomial Functors: A General Theory of Interaction* (2022)
2. **Libkind, S. & Spivak, D.I.** — *Pattern Runs on Matter* (ACT 2024)
3. **Spivak, D.I.** — *Dynamical Systems and Sheaves* (2019)
4. **Bumpus, B.M.** — *Compositional Algorithms on Compositional Data* (2024)
5. **Bumpus, B.M.** — *Spined Categories* (2023)
6. **Bumpus, B.M.** — *Cohomology Obstructions* (2024)
7. **Swan, J. & Hedges, J. et al.** — *The Road to General Intelligence* (Springer 2022)
8. **Hedges, J.** — *Open Games with Agency* (2023)

## 14. See Also

- `acsets` — Algebraic databases (schema category)
- `discohy-streams` — 7 operad variants with GF(3) balance
- `triad-interleave` — Balanced ternary scheduling
- `world-hopping` — Badiou triangle navigation
- `open-games` — Bidirectional transformations



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `category-theory`: 139 citations in bib.duckdb
- `polynomial-functors`: 8 citations in bib.duckdb
- `operads`: 5 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 3. Variations on an Arithmetic Theme

**Concepts**: generic arithmetic, coercion, symbolic, numeric

### GF(3) Balanced Triad

```
asi-polynomial-operads (−) + SDF.Ch3 (○) + [balancer] (+) = 0
```

**Skill Trit**: -1 (MINUS - verification)

### Secondary Chapters

- Ch9: Generic Procedures
- Ch1: Flexibility through Abstraction
- Ch4: Pattern Matching
- Ch6: Layering
- Ch5: Evaluation
- Ch10: Adventure Game Example
- Ch7: Propagators

### Connection Pattern

Generic arithmetic crosses type boundaries. This skill handles heterogeneous data.
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