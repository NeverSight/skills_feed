---
name: textbook-grounding
description: "Orthogonally-integrated Hegelian syntopical analysis for SAQ/VIVA/concept grounding with systematic textbook citations. Implements thesis extraction → antithesis identification → abductive synthesis across multiple authoritative sources. Tensor-integrated with /m command: activates S×T×L synergies (textbook-grounding × pdf-search × qmd = 0.95). Triggers on requests for model SAQ responses, VIVA preparation, concept explanations requiring textbook evidence, or any PEX exam content needing systematic cross-reference validation."
version: "2.0.0"
triggers:
  - "SAQ model response"
  - "VIVA preparation"
  - "textbook grounding"
  - "cross-reference"
  - "syntopical analysis"
  - "PEX exam"
  - "CICM primary"
  - "ANZCA primary"
  - "medical textbook search"
  - "evidence synthesis"
  - "multi-source citation"
  - "academic grounding"
tensor_integration:
  dimension: S (Skills)
  synergies:
    S×T: [pdf-search, perplexity, deepgraph]
    S×L: [pdf-brain, docling, qmd, nu]
    S×S: [saq, dialectical, critique, constraints, deep-research]
    S×A: [researcher, gemini]
  cross_dimensional_score: 0.95
---

# Textbook Grounding v2.0

> **λ**: Query → Tensor Activation → Syntopical Analysis → Grounded Response with Citations

Generate examination-optimized responses grounded in systematic cross-textbook analysis using Hegelian dialectical synthesis with orthogonal tensor integration.

## Core Philosophy

### Syntopical Reading (Mortimer Adler)
The highest level of reading—comparing multiple authoritative sources on the same topic to synthesize understanding unavailable from any single source.

### Hegelian Dialectic
> "A higher level of understanding and insight could be achieved by creating the two most diametrically opposed viewpoints, the mutual contradiction being reconciled on a higher level of truth."
> — [Model of Dialectical Learning](https://link.springer.com/rwe/10.1007/978-1-4614-3858-8_493)

- **Thesis**: Each textbook's interpretation/claim
- **Antithesis**: Contradictions, variations, nuances across sources
- **Synthesis**: Universal principles emerging from resolved tensions

### Orthogonal Tensor Integration
This skill participates in the 5D tensor routing space:
- **S dimension**: Activates [saq, dialectical, critique, constraints]
- **T dimension**: Integrates [pdf-search, perplexity, relate]
- **L dimension**: Leverages [pdf-brain, docling, qmd]
- **Cross-dimensional synergy**: S×T×L = 0.95

## Architecture v2.0

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                  ORTHOGONAL TEXTBOOK GROUNDING PIPELINE                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Φ0: TENSOR ACTIVATE ─────────────────────────────────────────────────────  │
│      └─ Score dimensions, detect synergies, compose execution plan          │
│                                                                             │
│  Φ1: QUERY DECOMPOSE ─────────────────────────────────────────────────────  │
│      └─ Parse topic, domains, complexity; route to skill stack              │
│                                                                             │
│  Φ2: PARALLEL SEARCH ─────────────────────────────────────────────────────  │
│      └─ Multi-query semantic search across pdf-embeddings + web             │
│      └─ Execute via T×L synergy: pdf-search × pdf-brain × docling           │
│                                                                             │
│  Φ3: THESIS EXTRACTION ───────────────────────────────────────────────────  │
│      └─ Extract T_i from each source with page-level citations              │
│      └─ Classify: definitional | mechanistic | quantitative | clinical      │
│                                                                             │
│  Φ4: ANTITHESIS DETECTION ────────────────────────────────────────────────  │
│      └─ Compare thesis pairs for tensions A_ij                              │
│      └─ Classify: contradiction | refinement | extension | context_dependent│
│                                                                             │
│  Φ5: DIALECTICAL SYNTHESIS ───────────────────────────────────────────────  │
│      └─ Invoke dialectical skill for α-β-γ structure                        │
│      └─ Apply constraints skill for deontic obligations                     │
│                                                                             │
│  Φ6: MULTI-LENS CRITIQUE ─────────────────────────────────────────────────  │
│      └─ STRUCTURAL × EVIDENTIAL × SCOPE × ADVERSARIAL × PRAGMATIC           │
│      └─ Per-thesis evaluation with aggregate scoring                        │
│                                                                             │
│  Φ7: ABDUCTIVE SYNTHESIS ─────────────────────────────────────────────────  │
│      └─ Abduce minimal universal principles S resolving tensions            │
│      └─ Validate: ∀T_i. ∃s ∈ S. subsumes(s, T_i)                            │
│                                                                             │
│  Φ8: RESPONSE GENERATION ─────────────────────────────────────────────────  │
│      └─ Invoke saq skill for template routing                               │
│      └─ Apply symbol lexicon, word count constraints                        │
│                                                                             │
│  Φ9: CITATION WEAVING ────────────────────────────────────────────────────  │
│      └─ Systematic footnote generation with page references                 │
│      └─ Apply deontic constraints: O(cite), O(page), F(uncited)             │
│                                                                             │
│  Φ10: VALIDATION & QA ────────────────────────────────────────────────────  │
│       └─ Coverage, parsimony, confidence floor checks                       │
│       └─ Examiner expectation alignment                                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Phase Execution Details

### Φ0: Tensor Activation

When invoked via `/m`, this skill receives tensor context:

```yaml
tensor_context:
  prompt: "{original_query}"
  activated_dimensions:
    C: sc:document (0.70)
    A: researcher (0.75)
    S: textbook-grounding (0.95), saq (0.90), dialectical (0.80), critique (0.75)
    T: perplexity (0.65), pdf-search (0.90)
    L: pdf-brain (0.90), docling (0.75), qmd (0.70)
  synergies:
    S×T×L: textbook-grounding × pdf-search × qmd = 0.95
    S×S×S: saq × dialectical × critique = 0.90
  execution_mode: sequential
```

**Synergy Exploitation:**
```
IF synergy(S×T×L) > 0.9:
    activate_parallel_search()  # pdf-brain + pdf-search + perplexity
IF synergy(S×S×S) > 0.85:
    chain_skill_stack()  # dialectical → critique → saq
```

### Φ1: Query Decomposition

```yaml
inputs:
  query: "Describe the pharmacology of propofol with textbook citations"
  context: ANZCA_primary | CICM_primary | VIVA | concept | academic

outputs:
  topic: "propofol pharmacology"
  domains: [pharmacology, anaesthetics, sedation, critical_care]
  question_verb: describe
  estimated_sources: 8-12
  complexity: standard | deep | comprehensive
  skill_stack: [textbook-grounding, dialectical, saq, critique]
  tool_stack: [pdf-search, pdf-brain, perplexity]
  cli_stack: [docling, qmd]
```

**Complexity Routing:**
```
IF context = VIVA OR context = comprehensive:
    complexity = deep
    search_depth = 25
    skill_chain = [dialectical, critique, constraints, saq]
ELIF context ∈ {ANZCA_primary, CICM_primary}:
    complexity = standard
    search_depth = 15
    skill_chain = [dialectical, saq]
ELIF context = academic:
    complexity = comprehensive
    search_depth = 30
    skill_chain = [dialectical, critique, deep-research]
ELSE:
    complexity = standard
    search_depth = 10
    skill_chain = [saq]
```

### Φ2: Parallel Search (T×L Synergy)

Execute multi-query semantic search across sources:

```bash
# Primary searches (parallel via T×L synergy)
pdf-search "{topic} {key_terms}" --limit {search_depth} &
pdf-brain search "{topic}" --semantic --top-k 10 &
docling convert *.pdf --extract-sections "{topic}" &

# Secondary enrichment (sequential)
perplexity search "{topic} latest research 2024 2025"
```

**Search Strategy Matrix:**

| Query Type | Tool | Purpose | Weight |
|:-----------|:-----|:--------|:-------|
| Core topic | pdf-search | Textbook passages | 0.40 |
| Mechanism | pdf-brain | Mechanistic detail | 0.25 |
| Clinical | perplexity | Current practice | 0.20 |
| Comparison | docling | Cross-source compare | 0.15 |

**Multi-Query Expansion:**
```
Primary: "{topic} {domain_terms}"
Mechanism: "how {topic} works mechanism"
Clinical: "{topic} clinical application"
Comparison: "{topic} vs alternatives"
Exceptions: "{topic} exceptions limitations"
```

### Φ3: Thesis Extraction

For each unique source, extract claims with full provenance:

```yaml
thesis:
  id: T_01
  source: "Middleton B et al. Physics in Anaesthesia. 3rd ed."
  page: 115
  chapter: "Fluid Dynamics"
  claim: "Reynolds number is dimensionless"
  claim_type: definitional | mechanistic | quantitative | clinical
  confidence: 0.95
  context: "The Reynolds number is a dimensionless quantity, i.e. it has no units."
  quote: true
  extraction_method: pdf-search | manual | perplexity

classification:
  definitional:
    description: "What something IS"
    priority: HIGH
    focus: "examine consensus across sources"
  mechanistic:
    description: "How something WORKS"
    priority: HIGH
    focus: "examine completeness of explanation"
  quantitative:
    description: "Numeric values/thresholds"
    priority: CRITICAL
    focus: "examine variation, cite ranges"
  clinical:
    description: "Application/relevance"
    priority: MEDIUM
    focus: "context-dependent, may vary by source"
```

### Φ4: Antithesis Detection

Compare all thesis pairs for tensions:

```yaml
antithesis:
  id: A_01_02
  thesis_1: T_01  # "Re < 2000 = laminar"
  thesis_2: T_02  # "Re < 1000 = laminar"
  tension_type: contradiction | refinement | extension | context_dependent
  description: "Threshold for laminar flow varies: 2000 vs 1000"
  resolution_candidates:
    - "2000 is generally accepted; 1000 is conservative"
    - "Context matters: ideal vs physiological conditions"
  evidence_weight:
    T_01: 0.85  # More sources agree
    T_02: 0.70  # Single source

tension_types:
  contradiction:
    definition: "Mutually exclusive claims"
    resolution: "Authority + recency + specificity + consensus"
  refinement:
    definition: "One claim more precise than other"
    resolution: "Accept refined version with acknowledgment"
  extension:
    definition: "One claim adds to another"
    resolution: "Merge with attribution to both"
  context_dependent:
    definition: "Both true in different contexts"
    resolution: "State conditions explicitly"
```

### Φ5: Dialectical Synthesis (S×S Synergy)

Invoke dialectical skill for structured synthesis:

```yaml
dialectical_structure:
  α_AGONAL:
    purpose: "Establish consensus with paradox awareness"
    content: "Synthesized universal principles from majority sources"
    citations: [highest_authority_sources]

  β_MAIEUTIC:
    purpose: "Guide through mechanisms with Socratic clarity"
    content: "Resolved tensions with evidence-weighted decisions"
    method: "Show reasoning process, not just conclusions"

  γ_APOPHATIC:
    purpose: "Acknowledge limitations with academic humility"
    content: "Noted variations, exceptions, context dependencies"
    tone: "Scholarship, not overconfidence"
```

**Integration with Constraints Skill:**
```yaml
deontic_obligations:
  O(cite): "All claims MUST have at least one citation"
  O(page): "Page numbers OBLIGATORY for all citations"
  O(synthesis): "Must produce synthesis, not mere aggregation"
  P(multi_cite): "Multiple citations PERMITTED for consensus"
  P(quote): "Direct quotes PERMITTED for key definitions"
  F(uncited): "Uncited claims are FORBIDDEN"
  F(single_source): "Single-source claims FORBIDDEN for consensus"
```

### Φ6: Multi-Lens Critique (S Synergy)

Apply critique skill's five lenses:

```yaml
lenses:
  STRUCTURAL:
    question: "Are theses logically coherent?"
    weight: 0.20
    validation: [internal_consistency, logical_flow]

  EVIDENTIAL:
    question: "What's the evidence quality?"
    weight: 0.25
    validation: [source_authority, peer_review, recency]

  SCOPE:
    question: "Do claims overgeneralize?"
    weight: 0.20
    validation: [boundary_conditions, exceptions_noted]

  ADVERSARIAL:
    question: "What would examiners challenge?"
    weight: 0.20
    validation: [anticipate_objections, prepare_defenses]

  PRAGMATIC:
    question: "Does this work clinically?"
    weight: 0.15
    validation: [clinical_utility, practical_application]

per_thesis_evaluation:
  thesis: T_01
  lens_scores:
    S: 0.90  # Clear logical structure
    E: 0.95  # Peer-reviewed source
    O: 0.75  # May not apply to all fluids
    A: 0.80  # Standard examiner expectation
    P: 0.85  # Clinically applicable
  aggregate: 0.85
  issues:
    - "Scope: Applies to Newtonian fluids; blood is non-Newtonian"
```

### Φ7: Abductive Synthesis

Generate minimal set of universal principles:

```
ABDUCTION PROTOCOL
──────────────────
1. Cluster theses by claim_type
2. For each cluster:
   a. Identify consensus claims (≥80% agreement)
   b. Resolve contested claims (40-79%) via critique lens priority
   c. Flag unique claims with high individual confidence (>0.8)
3. Compose synthesis S that:
   a. Subsumes all consensus claims
   b. Includes resolved contested claims with caveats
   c. Optionally includes unique claims as extensions
4. Validate: ∀T_i. ∃s ∈ S. subsumes(s, T_i)
5. Check parsimony: |S| ≤ min(|T|/2, 10)
6. Verify confidence floor: ∀s ∈ S. confidence(s) ≥ 0.60
```

**Synthesis Schema:**
```yaml
synthesis:
  universal_principles:
    - id: S_01
      claim: "Reynolds number predicts flow type (laminar vs turbulent)"
      type: universal
      supporting_theses: [T_01, T_02, T_03, T_05, T_08]
      confidence: 0.95

  resolved_tensions:
    - antithesis: A_01_02
      resolution: "Re < 2000 generally indicates laminar; stricter thresholds exist"
      resolution_type: context_dependent
      caveats: ["ideal conditions", "physiological variation"]

  acknowledged_variations:
    - topic: "Critical threshold"
      range: "1000-4000 depending on source"
      recommendation: "Use Re < 2000 = laminar, Re > 3000 = turbulent"
```

### Φ8: Response Generation (S Synergy with SAQ)

Route to saq skill for template-based generation:

```yaml
template_routing:
  IF question_verb = describe AND domain = pharmacology:
    template = saq/references/pharmacology-template.md
  ELIF question_verb = describe AND domain = physiology:
    template = saq/references/physiology-template.md
  ELIF question_verb ∈ {compare, contrast}:
    template = saq/references/comparison-template.md
  ELIF context = VIVA:
    template = viva-extended-template.md
  ELSE:
    template = saq/references/physiology-template.md

generation_constraints:
  SAQ_mode:
    word_count: 180-220
    structure: 2-3 A4 pages handwritten
    time: 8 minutes
    format: dot points, symbols, minimal prose
  VIVA_mode:
    word_count: 500-800
    structure: extended mechanistic detail
    includes: [examiner_anticipation, deep_dive, edge_cases, clinical_vignettes]
  Academic_mode:
    word_count: 1000-2000
    structure: full scholarly format
    includes: [literature_review, methodology, discussion]
```

### Φ9: Citation Weaving

**Footnote Format:**
```markdown
[^n]: Author(s). *Title*. Edition. Publisher, Year; p. page. "Verbatim quote."
```

**Citation Priority Weights:**
| Source Type | Weight | Usage |
|:------------|:-------|:------|
| Examiner reports (CICM/ANZCA) | 0.95 | Gold standard |
| Core textbooks | 0.85 | Primary evidence |
| Review articles | 0.80 | Synthesis support |
| Primary research | 0.75 | Novel findings |
| Clinical guidelines | 0.85 | Practice standards |
| Web sources | 0.50 | Triangulation required |

**Citation Density Requirements:**
```yaml
SAQ: 5-10 citations (1 per major claim)
VIVA: 15-25 citations (comprehensive)
Academic: 30-50 citations (scholarly)
```

### Φ10: Validation & QA

```python
def validate_grounded_response(response, theses, synthesis):
    checks = {
        # Coverage checks
        "citation_coverage": all_claims_cited(response),
        "synthesis_reflected": synthesis_in_response(response, synthesis),
        "thesis_coverage": all_theses_subsumed(theses, synthesis),

        # Format checks
        "word_count": word_count_in_range(response, mode),
        "cascade_preserved": no_decomposed_cascades(response),
        "values_contextualized": all_values_have_context(response),

        # Quality checks
        "tensions_acknowledged": variations_noted(response),
        "deontic_compliance": deontic_constraints_met(response),
        "examiner_optimized": meets_examiner_expectations(response),

        # Parsimony checks
        "synthesis_minimal": len(synthesis) <= len(theses) / 2,
        "confidence_floor": all(s.confidence >= 0.60 for s in synthesis)
    }
    return ValidationResult(
        valid=all(checks.values()),
        issues=[k for k, v in checks.items() if not v],
        score=sum(checks.values()) / len(checks)
    )
```

## Output Structures

### SAQ Mode Output
```markdown
---
topic: "{topic}"
type: saq-model-response
textbooks-analyzed: {n}
theses-extracted: {m}
antitheses-identified: {k}
citations: {c}
confidence: {0.85}
---

# {Topic}

> [!abstract] Definition
> {Core definition with citation}[^1]

## {Domain Heading 1}
- {Cascade with context}[^2]
- {Value with clinical relevance}[^3]

## {Domain Heading 2}
...

## Syntopical Analysis

> [!warning] Key Variation
> {Identified discrepancy with resolution}[^4][^5]

## References

[^1]: {Full citation with page}
```

### VIVA Mode Output

Extends SAQ mode with:
- **Examiner Anticipation**: Likely follow-up questions with prepared responses
- **Deep Dive**: Extended mechanistic detail on key points
- **Edge Cases**: Acknowledged limitations and exceptions
- **Clinical Vignettes**: Application scenarios
- **Recovery Strategies**: If caught off-guard

### Academic Mode Output

Full scholarly structure:
- **Abstract**: Synthesis summary
- **Introduction**: Context and scope
- **Literature Review**: Organized theses with critical analysis
- **Methodology**: Syntopical approach description
- **Results**: Synthesis with tension resolution
- **Discussion**: Implications and limitations
- **Conclusion**: Universal principles
- **References**: Complete bibliography

## Integration Points

### With /m Universal Meta-Router

```yaml
tensor_activation:
  on_prompt: "Generate SAQ on propofol pharmacology with citations"

  decomposition:
    C: sc:document (0.70)
    A: researcher (0.75)
    S: textbook-grounding (0.95)
    T: pdf-search (0.90)
    L: pdf-brain (0.90)

  synergies_activated:
    S×T×L: 0.95 → parallel_search_mode
    S×S×S: 0.90 → skill_chain_mode

  execution_plan:
    mode: sequential
    steps:
      1: T×L → parallel search (pdf-brain + pdf-search + perplexity)
      2: S → textbook-grounding (thesis extraction + antithesis detection)
      3: S×S → dialectical → critique (synthesis + validation)
      4: S → saq (template + formatting)
```

### With pdf-search / pdf-brain (Primary T×L)
```bash
# Parallel search execution
pdf-search "{query}" --limit 15 &
pdf-brain search "{query}" --semantic --top-k 10 &
wait

# Merge and deduplicate results
# Weight by source quality
```

### With SAQ Skill (S Synergy)
```yaml
handoff:
  from: textbook-grounding
  to: saq
  data:
    synthesis: universal_principles
    citations: formatted_footnotes
    constraints: word_count, symbol_lexicon
```

### With Critique Skill (S Synergy)
```yaml
invocation:
  purpose: "Multi-lens thesis evaluation"
  lenses: [STRUCTURAL, EVIDENTIAL, SCOPE, ADVERSARIAL, PRAGMATIC]
  output: per_thesis_scores, aggregate_confidence
```

### With Dialectical Skill (S Synergy)
```yaml
structure:
  α_AGONAL: consensus_with_paradox
  β_MAIEUTIC: mechanism_through_questioning
  γ_APOPHATIC: limitations_with_humility
```

### With Constraints Skill (S Synergy)
```yaml
deontic_framework:
  O: [cite, page, synthesis]
  P: [multi_cite, quote]
  F: [uncited, single_source_consensus]
```

### With knowledge-orchestrator (Meta-S)
```yaml
delegation:
  IF task.requires_multi_skill:
    delegate_to: knowledge-orchestrator
    skills: [textbook-grounding, dialectical, critique, saq]
    coordination: confidence-weighted
```

## Extended Examples

### Example 1: Reynolds Number SAQ

**Input:** "Describe the Reynolds number and factors affecting flow type"

**Φ2 Search Results:**
- Physics in Anaesthesia (Middleton) p.115
- Ganong's Review of Medical Physiology p.567
- West's Respiratory Physiology p.112
- Nunn's Applied Respiratory Physiology p.89
- Power & Kam Physiology p.203

**Φ3 Theses Extracted:** 25 from 12 sources

**Φ4 Antitheses Identified:** 5 (threshold variations, equation forms)

**Φ7 Synthesis:** 6 universal principles + 2 resolved tensions

**Φ8 Response (198 words):**
```
## Definition
- Dimensionless ratio of inertial/viscous forces[^1]
- Re = ρvd/μ = vd/ν (kinematic form)[^2]

## Factors
- ↑ρ (density) → ↑Re → ↑turbulence[^3]
- ↑v (velocity) → ↑Re → most significant clinically[^4]
- ↑d (diameter) → ↑Re → larger airways turbulent[^5]
- ↓μ (viscosity) → ↑Re → ↑turbulence[^6]

## Critical Values
- Re < 2000 → laminar (generally)[^7]
- 2000 < Re < 4000 → transitional[^8]
- Re > 4000 → turbulent[^9]

> [!warning] Variation
> Some sources cite Re < 1000 for laminar (conservative)[^10]

## Clinical Integration
- Heliox: ↓density → ↓Re → ↓turbulence → ↓WOB in UAO[^11]
- ETT: ↓diameter → ↓Re → more laminar despite ↑velocity[^12]
- Blood: non-Newtonian → Re applicability limited[^13]

## References
[^1]: Middleton B. *Physics in Anaesthesia*. 3e. Scion; 2021. p.115.
[^2]: Ganong WF. *Review of Medical Physiology*. 26e. McGraw-Hill; 2019. p.567.
...
```

### Example 2: VIVA Depth Response

**Input:** "VIVA preparation on propofol including pharmacokinetics and clinical applications"

**Execution:** Full Φ0-Φ10 with VIVA mode

**Output includes:**
- Extended mechanistic cascades (800 words)
- Anticipated examiner questions with prepared answers
- Edge cases (propofol infusion syndrome, allergies)
- Clinical vignettes (TCI, sedation, induction)
- 25 citations with page references

## Anti-Patterns

| Pattern | Why Harmful | Fix |
|:--------|:------------|:----|
| Single-source claims | Fails syntopical requirement | Multi-source validation |
| Uncited variations | Undermines credibility | Always cite discrepancies |
| Ignored tensions | Appears superficial | Acknowledge and resolve |
| Over-complex synthesis | Violates Pareto parsimony | Minimal principle set |
| Generic citations | Loses precision | Page-level references |
| Decomposed cascades | Loses mechanistic flow | Preserve as single chains |
| Values without context | Appears rote | Same-line clinical meaning |

## File Reference

| Purpose | Location |
|:--------|:---------|
| Synthesis protocol | `references/synthesis-protocol.md` |
| Citation formats | `references/citation-formats.md` |
| Examiner expectations | `references/examiner-expectations.md` |
| Validation script | `scripts/grounding_validator.py` |
| VIVA template | `references/viva-template.md` |
| Academic template | `references/academic-template.md` |

## Quality Metrics

```yaml
grounding_quality:
  citation_density: citations_per_claim >= 1.0
  source_diversity: unique_sources >= 5
  synthesis_ratio: |synthesis| / |theses| <= 0.5
  confidence_floor: all_confidence >= 0.60
  tension_coverage: all_antitheses_resolved
  examiner_alignment: meets_expectations >= 0.85
```

---

**Core Insight**: Orthogonal tensor integration transforms textbook grounding from isolated skill to synergistic capability. Cross-dimensional activation (S×T×L) enables parallel search, skill chaining, and optimal composition. The Hegelian dialectic ensures tensions are not hidden but resolved through evidence-weighted abduction, producing responses that withstand examiner scrutiny.

**Research Sources:**
- [Self-reflecting LLMs: A Hegelian Dialectical Approach](https://www.microsoft.com/en-us/research/wp-content/uploads/2025/06/Hegelian_Dialectic_ICML_Version-18.pdf)
- [Model of Dialectical Learning](https://link.springer.com/rwe/10.1007/978-1-4614-3858-8_493)
- [Hegel's Dialectics (Stanford Encyclopedia)](https://plato.stanford.edu/entries/hegel-dialectics/)
