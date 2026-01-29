---
name: behaviour-surprisal-analysis
description: Behaviour Surprisal Analysis
version: 1.0.0
---

# Behaviour Surprisal Analysis

**Status**: Production Ready (v3.0 - Cat# Integration)
**Trit**: 0 (ERGODIC - measurement/observation)
**Principle**: S(x) = -log₂(P(x|attention_mode))
**Frame**: Tri-channel prediction evaluation with AGM belief revision + Cat# bicomodule structure

---

## Overview

**Behaviour Surprisal Analysis** calculates information-theoretic surprise between predictions and observed outcomes using three complementary attention channels mapped to Cat# = Comod(P) structure:

| Channel | Trit | Home | Poly Op | Kan Role | Description |
|---------|------|------|---------|----------|-------------|
| **Direct** (α) | −1 | Span | × (product) | Ran_K | Exact artifact matching |
| **Diffuse** (β) | 0 | Prof | ⊗ (parallel) | Adj | Thematic/structural matching |
| **Meta** (γ) | +1 | Presheaves | ◁ (substitution) | Lan_K | Capability/infrastructure tracking |

```
Total Surprisal = α·S_direct + β·S_diffuse + γ·S_meta
where α + β + γ = 1 and typically α=0.3, β=0.5, γ=0.2
```



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 5. Evaluation

**Concepts**: eval, apply, interpreter, environment

### GF(3) Balanced Triad

```
behaviour-surprisal-analysis (−) + SDF.Ch5 (−) + [balancer] (−) = 0
```

**Skill Trit**: -1 (MINUS - verification)

### Secondary Chapters

- Ch1: Flexibility through Abstraction
- Ch4: Pattern Matching
- Ch6: Layering
- Ch10: Adventure Game Example

### Connection Pattern

Evaluation interprets expressions. This skill processes or generates evaluable forms.
## Cat# Integration (v3.0)

### Galois Adjunction α ⊣ γ

The Direct and Meta channels form a Galois adjunction through the Diffuse bridge:

```
         α (abstract)
  Direct ─────────────→ Diffuse
    ↑                      │
    │        CatSharp      │ γ (concretize)
    │         Scale        │
    └──────────────────────┘
           Meta

  GF(3): (−1) + (0) + (+1) = 0 ✓
```

- **α (abstraction)**: Direct predictions → Diffuse patterns
- **γ (concretization)**: Diffuse patterns → Direct predictions
- **Unit η**: id → γ∘α verifies coherence

### Three Homes (Spivak ACT 2023)

Each channel lives in a specific Cat# home:

```
┌────────────┬─────────────┬──────────┬───────────────┬────────────┐
│  Channel   │  Poly Op    │ Kan Role │   Structure   │   Home     │
├────────────┼─────────────┼──────────┼───────────────┼────────────┤
│  Direct    │  × (prod)   │  Ran_K   │ cofree t_p    │   Span     │
│  Diffuse   │  ⊗ (para)   │  Adj     │ bicomodule    │   Prof     │
│  Meta      │  ◁ (subst)  │  Lan_K   │ free m_p      │ Presheaves │
└────────────┴─────────────┴──────────┴───────────────┴────────────┘
```

### Bicomodule Coherence

Predictions and observations form bicomodule pairs. Coherence is verified by:

1. **Galois unit check**: η: id → γ∘α preserves trits
2. **Bicomodule compatibility**: pred_trit ↔ obs_trit compatible homes

## CatSharp Scale Sonification

Surprisal values map to pitch classes via the CatSharp scale:

| Trit | Pitch Classes | Chord Type | Hz Range |
|------|---------------|------------|----------|
| +1 (PLUS) | {0, 4, 8} | Augmented triad | C-E-G# |
| 0 (ERGODIC) | {3, 6, 9} | Diminished 7th | D#-F#-A-C |
| −1 (MINUS) | {1,2,5,7,10,11} | Fifths cycle | C#,D,F,G,A#,B |

```clojure
;; Surprisal → Pitch class → Frequency
(defn surprisal->pitch-class [surp]
  (mod (Math/round (* (min surp 10.0) 1.2)) 12))

(defn pitch-class->freq [pc]
  (* 261.63 (Math/pow 2 (/ pc 12.0))))  ;; C4 = 261.63 Hz
```

Enable with `--sonify` flag to hear the surprisal as tones via sox.

## AGM Belief Revision (Levi Identity)

Based on [Baker 2023](https://ijcai.org/proceedings/2023/811):

```
K * φ = (K − ¬φ) + φ   (Levi Identity)
```

- **Contraction (K − ¬φ)**: Remove predictions contradicted by observations
- **Expansion (+ φ)**: Add new beliefs from observed data
- **Revision (K * φ)**: Combined operation via Levi identity

### Spohn κ-Ranking

Predictions ranked by entrenchment:

```clojure
(defn kappa-rank [belief]
  (- (Math/log (/ 1 (max 0.01 (:confidence belief))))))
```

Lower κ = more entrenched = harder to revise.

## Usage

```bash
# Full Cat# analysis with sonification
bb ~/.claude/skills/behaviour-surprisal-analysis/analyse.bb \
  --predictions predictions.json \
  --observed observed.json \
  --alpha 0.3 --beta 0.5 --gamma 0.2 \
  --sonify

# With capability tracking
bb analyse.bb \
  --predictions predictions.json \
  --observed observed.json \
  --skills-before skills_t0.txt \
  --skills-after skills_t30.txt

# Direct-heavy (Span home focus)
bb analyse.bb --alpha 0.7 --beta 0.2 --gamma 0.1

# Meta-heavy (Presheaves home focus)
bb analyse.bb --alpha 0.1 --beta 0.3 --gamma 0.6 --sonify
```

## Input Format

```json
{
  "predictions": {
    "direct": [
      {"content": "Ruby MCP SDK for skill markets", "confidence": 0.8},
      {"content": "VirtualizationBridge sandbox test", "confidence": 0.7}
    ],
    "diffuse": [
      {"theme": "GF(3) conservation", "keywords": ["trit", "lattice", "conservation"]},
      {"theme": "skill markets", "keywords": ["confidential", "commitment", "beacon"]}
    ],
    "meta": {
      "skills_before": 45,
      "mcp_servers_before": 12,
      "config_hash": "a3f2c1"
    }
  },
  "observed": {
    "threads": [
      "Ruby MCP SDK for confidential skill markets",
      "GF(3) skill composition and Galois connection verification",
      "Derangement operators and GF(3) entropy management"
    ],
    "capability_events": [
      {"type": "skill_install", "count": 373, "source": "plurigrid/asi"},
      {"type": "mcp_addition", "server": "world_a_aptos"}
    ]
  }
}
```

## Output Format

```
╔══════════════════════════════════════════════════════════════════╗
║  BEHAVIOUR SURPRISAL ANALYSIS v3.0 (Cat# + AGM)                  ║
║  α=0.30 (Span/Ran) β=0.50 (Prof/Adj) γ=0.20 (Presh/Lan)          ║
╚══════════════════════════════════════════════════════════════════╝

  DIRECT ATTENTION (Home: Span, Kan: Ran_K)
  ───────────────────────────────────────────────────────────────
  Prediction                      │ Match │ S_dir │ Trit │ PC │ Home
  ────────────────────────────────┼───────┼───────┼──────┼────┼─────
  VirtualizationBridge sandbox    │  34.9% │  1.52 │  +   │  2 │ Span
  ...

  CAT# COHERENCE
  ───────────────────────────────────────────────────────────────
  Galois adjunction α ⊣ γ:    ✓ coherent
  Bicomodule compatibility:   85.0% (✓)

  CATSHARP SONIFICATION
  ───────────────────────────────────────────────────────────────
  ♪ Direct (Ran_K): 293.7 Hz
  ♪ Diffuse (Adj): 329.6 Hz
  ♪ Meta (Lan_K): 261.6 Hz
```

## GF(3) Triads

The skill participates in balanced triads:

```
behaviour-surprisal-analysis (0) ⊗ catsharp-galois (0) ⊗ gay-mcp (-1) + operad-compose (+1) = 0 ✓

# Internal channel triad
Direct (−1) + Diffuse (0) + Meta (+1) = 0 ✓
```

## Attention Calibration

| Prediction Style | Recommended (α,β,γ) | Cat# Focus |
|-----------------|---------------------|------------|
| Specific artifacts | (0.6, 0.3, 0.1) | Span heavy |
| Thematic directions | (0.2, 0.6, 0.2) | Prof heavy |
| Capability exploration | (0.2, 0.3, 0.5) | Presheaves heavy |
| Mixed/balanced | (0.3, 0.5, 0.2) | Bicomodule equilibrium |

## API

```clojure
(require '[behaviour-surprisal-analysis :as bsa])

;; Full Cat# analysis
(bsa/combined-analysis
  predictions observed
  0.3 0.5 0.2          ;; α β γ
  before-state after-state
  capability-events
  true)                ;; sonify?

;; Galois adjunction verification
(bsa/verify-galois-unit direct-result)

;; Bicomodule coherence check
(bsa/check-bicomodule-coherence direct diffuse meta)

;; Sonify channel
(bsa/sonify-channel results "Direct" 0.3)
```

## Philosophical Foundation

The tri-channel Cat# model reflects:

1. **Cat# Three Homes**: Span (comodules), Prof (bimodules), Presheaves (right modules)
2. **Kan Extensions**: Ran_K (limit/consume), Lan_K (colimit/generate), Adj (bridge)
3. **Galois Adjunction**: α ⊣ γ for abstraction/concretization
4. **AGM Epistemology**: Contraction, Expansion, Revision via Levi identity
5. **CatSharp Scale**: Mazzola's categorical music theory for sonification

### Key Insight: GF(3) = Naturality

GF(3) conservation IS the naturality condition of Cat# equipment:

```
For a triad (s₋₁, s₀, s₊₁):
  Ran_K(s₋₁) →[bicomodule]→ s₀ →[bicomodule]→ Lan_K(s₊₁)
  
  The commuting square:
    G(f) ∘ η_A = η_B ∘ F(f)
    
  Becomes the GF(3) equation:
    (−1) + (0) + (+1) ≡ 0 (mod 3)
```

---

**Skill Name**: behaviour-surprisal-analysis
**Version**: 3.0.0 (Cat# Integration)
**Type**: Prediction Evaluation / Information Theory / Belief Revision / Category Theory
**Trit**: 0 (ERGODIC)
**GF(3)**: Conserved via Cat# bicomodule structure
**Dependencies**: sox (optional, for sonification)
**Sources**: 
- [Spivak "All Concepts are Cat#" (ACT 2023)](https://topos.site/p/2023-act-tutorial)
- [Baker 2023 - AGM for Human Reasoning](https://ijcai.org/proceedings/2023/811)
- [Mazzola "The Topos of Music" (2002)](https://www.springer.com/gp/book/9783764357313)
- [arxiv:2505.13763 - LLM Metacognition](https://arxiv.org/abs/2505.13763)