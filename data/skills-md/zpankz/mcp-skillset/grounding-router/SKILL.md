---
name: grounding-router
description: |
  Routes medical education grounding requests through atomic primitive composition.
  Four primitives (Σ Source, Τ Textbook, Δ Dialectical, Ρ Response) combine via
  operators (∘ ⊗ * |) for SAQ/VIVA/Academic response generation.
  Integrates: limitless, research, pieces, pdf-search, pdf-brain CLIs.
---

# Grounding Router

**Version**: 3.0.0
**Architecture**: atomic-permutation-router
**Trigger Keywords**: grounding, saq, viva, textbook, pex, medical, citations, synthesis, sc:grounding

**Progressive Loading**:
- Level 0: Frontmatter (~100 tokens) - trigger detection only
- Level 1: Core SKILL.md (~2500 tokens) - primitives + routing
- Level 2: references/*.md - on-demand deep specifications
- Level 3: scripts/*.py - execute without loading context

**Integrations**:
- Skills: dialectical, critique, mega, textbook-grounding, saq, qp
- CLIs: limitless, research, pieces, pdf-search, pdf-brain, pex
- Commands: sc:grounding
- Routers: context-router

> **λΩ.τ**: Query(ο) → Atomic-Composition(λ) → Grounded-Response(τ)

Routes grounding requests through minimal atomic primitives for maximal emergent function.

## Trigger Conditions

Activate when:
- Explicit: `/grounding`, `/saq`, `/viva`, `sc:grounding`
- Implicit: SAQ, VIVA, medical exam, textbook citations, PEX sources
- Hook signal: `need_grounding=true` from intent detection

## Routing Decision Tree

```
Request Received
    │
    ├── Mode Detection
    │   ├── "SAQ" or ~200 words → SAQ Mode
    │   ├── "VIVA" or examiner → VIVA Mode
    │   ├── "academic" or paper → Academic Mode
    │   └── Default → SAQ Mode
    │
    ├── Composition Selection
    │   ├── SAQ: (Σ ⊗ Τ) ∘ Δ ∘ Ρₛ
    │   ├── VIVA: Σ* ∘ (Τ ⊗ Δ) ∘ Ρᵥ*
    │   └── Academic: Σ* ∘ Τ* ∘ Δ* ∘ Ρₐ
    │
    └── Pipeline Execution
        ├── G₀: Preflight (CLI health)
        ├── Σ: Source extraction
        ├── Τ: Textbook grounding
        ├── Δ: Dialectical synthesis
        ├── G₄: Hallucination check
        └── Ρ: Response generation
```

## The Four Atomic Primitives

| Symbol | Name | λο.τ Form | CLI Sources |
|:-------|:-----|:----------|:------------|
| **Σ** | SOURCE | Context(ο) → Extraction(λ) → Evidence(τ) | limitless, pieces, pdf-search, research |
| **Τ** | TEXTBOOK | Evidence(ο) → Grounding(λ) → Citation(τ) | pdf-search, pdf-brain |
| **Δ** | DIALECTICAL | Claims(ο) → Synthesis(λ) → Universal(τ) | Thesis→Antithesis→Synthesis |
| **Ρ** | RESPONSE | Synthesis(ο) → Formatting(λ) → Output(τ) | SAQ/VIVA/Academic modes |

## Composition Operators

| Operator | Notation | Function | Pattern |
|:---------|:---------|:---------|:--------|
| Sequential | ∘ | Apply in order | `Σ ∘ Τ` (extract then ground) |
| Parallel | ⊗ | Concurrent | `Σₚ ⊗ Σₜ` (parallel sources) |
| Recursive | * | Until convergence | `Δ*` (resolve all antitheses) |
| Conditional | \| | Activate on condition | `Σ \| has_cache` |

## Source Sub-Primitives (Σ)

| Symbol | CLI | Triggers | Output |
|:-------|:----|:---------|:-------|
| Σₚ | limitless | personal, lifelog, recall | personal_context[] |
| Σₗ | pieces | ltm, snippet, history | local_context[] |
| Σₜ | pdf-search | textbook, book, page | textbook_chunks[] |
| Σₐ | research | pex, guidelines, evidence | authoritative_sources[] |
| Σₚₑₓ | pex | exam, lo, saq, curriculum | exam_context[] |

### CLI Commands

```bash
# Σₚ — Personal Context
limitless lifelogs search "{topic}" --limit 10 --json

# Σₗ — Local Context
echo "" | pieces ask "{topic}" --ltm

# Σₜ — Textbook Context
pdf-search "{topic}" --limit 10 --tags {tags}
pdf-brain search "{topic}" --limit 10

# Σₐ — Authoritative Context
research pex-grounding -t "{topic}" --specialty {specialty} --format json

# Σₚₑₓ — PEX Exam Context
pex search "{topic}" --limit 10
pex prereq "LO:{id}" --model fast
pex path "{topic}" --max 10
```

## Mode Compositions

### SAQ Mode: `(Σ ⊗ Τ) ∘ Δ ∘ Ρₛ`

```
Parallel source + textbook → Sequential synthesis → SAQ output
Word count: 180-220 | Citations: 5-10 | Tables: max 1
```

### VIVA Mode: `Σ* ∘ (Τ ⊗ Δ) ∘ Ρᵥ*`

```
Recursive sources → Parallel ground+synthesize → Recursive expand
Word count: 500-800 | Citations: 15-25 | Examiner probes: 3-5
```

### Academic Mode: `Σ* ∘ Τ* ∘ Δ* ∘ Ρₐ`

```
All recursive → Maximum depth → Full scholarly
Word count: 1000-2000 | Citations: 30-50 | Full bibliography
```

## Quality Gates

| Gate | Check | Pass Criteria |
|:-----|:------|:--------------|
| G₀ | Preflight | ≥3/5 CLIs available |
| G₁ | Sources | ≥2 sources, ≥2 types |
| G₂ | Textbook | ≥50% claims grounded |
| G₃ | Synthesis | All theses subsumed |
| G₄ | Hallucination | <20% flagged claims |
| G₅ | Output | Word count compliant |

## Confidence Calculation

```python
confidence = (
    0.30 * source_authority +
    0.25 * textbook_coverage +
    0.20 * synthesis_parsimony +
    0.15 * citation_density +
    0.10 * hallucination_pass_rate
)
```

| Confidence | Action |
|:-----------|:-------|
| ≥ 0.85 | Emit response |
| 0.70-0.84 | Warn, emit |
| 0.50-0.69 | Load references/, retry |
| < 0.50 | Execute scripts/, escalate |

## Progressive Loading Protocol

### Level 0: Trigger (Always Active)
- Frontmatter triggers in hook
- ~100 tokens loaded

### Level 1: Core (On Trigger Match)
- This SKILL.md body
- Routing + primitive specs

### Level 2: References (On Demand)
Load when confidence < 0.7 or customization needed:
- `references/atomic-primitives.md` — Full sub-primitive specs
- `references/composition-patterns.md` — Advanced compositions
- `references/quality-gates.md` — Detailed validation
- `references/cli-integration.md` — CLI command patterns

### Level 3: Scripts (Execute Only)
Invoke without loading context:
- `scripts/preflight.py --format json` — CLI health
- `scripts/extract.py "{query}"` — Parallel extraction
- `scripts/validate.py -r response.md` — Hallucination check

## Integration Points

### Context Router Handoff
```yaml
when: Σ primitives activated
action: Delegate to context-router for CLI orchestration
return: Aggregated sources to Τ primitive
```

### Skill Integration
```yaml
dialectical: Δ uses dialectical.atomic-composition
critique: G₄ uses critique.multi-lens
saq: Ρₛ uses saq.template
mega: Δ* escalates to mega when depth > 3
```

### Command Integration
```yaml
sc:grounding:
  invokes: grounding-router with mode detection
  flags: --mode, --sources, --specialty
```

## Example Invocations

### Basic SAQ
```
/grounding "Describe labetalol pharmacology" --mode=saq

Composition: (Σₗ ⊗ Σₜ ⊗ Σₐ) ∘ Δ ∘ Ρₛ
Output: 195-word SAQ with 7 citations
Confidence: 0.89
```

### Extended VIVA
```
/grounding "Pre-eclampsia management" --mode=viva --sources=all

Composition: Σ* ∘ (Τ ⊗ Δ*) ∘ Ρᵥ*
Output: 650-word VIVA with 22 citations + 5 probes
Confidence: 0.92
```

## Anti-Patterns

| Pattern | Why Harmful | Fix |
|:--------|:------------|:----|
| Σ without Τ | Ungrounded claims | Always include Τ |
| Δ without Σₜ | No textbook basis | Require textbook source |
| Ρ without Δ | No synthesis | Dialectical before response |
| Skip G₄ | Hallucination risk | Always validate |

---

**Recursion**: `grounding-router(grounding-router)` → meta-grounding for skill improvement.
