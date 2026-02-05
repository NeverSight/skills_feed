---
name: devtu-optimize-skills
description: Optimize ToolUniverse skills for better report quality, evidence handling, and user experience. Apply patterns like tool verification, foundation data layers, disambiguation-first, evidence grading, quantified completeness, and report-only output. Use when reviewing skills, improving existing skills, or creating new ToolUniverse research skills.
---

# Optimizing ToolUniverse Skills

Best practices for creating high-quality ToolUniverse research skills that produce detailed, evidence-graded reports with proper source attribution.

## When to Use This Skill

Apply when:
- Creating new ToolUniverse research skills
- Reviewing/improving existing skills
- User complains about missing details, noisy results, or unclear reports
- Skill produces process-heavy instead of content-heavy output
- Tools are failing silently or returning empty results

## Core Optimization Principles

### 1. Tool Interface Verification (Pre-flight Check)

**Problem**: Tool APIs change parameter names over time, or skills are written with incorrect parameter assumptions. This causes silent failures - tools return empty results without errors.

**Solution**: Verify tool parameters before calling unfamiliar tools:

```python
# Always check tool params to prevent silent failures
tool_info = tu.tools.get_tool_info(tool_name="Reactome_map_uniprot_to_pathways")
# Reveals: takes `id` not `uniprot_id`
```

**Maintain a known corrections table** in skills that use many tools:

| Tool | WRONG Parameter | CORRECT Parameter |
|------|-----------------|-------------------|
| `Reactome_map_uniprot_to_pathways` | `uniprot_id` | `id` |
| `ensembl_get_xrefs` | `gene_id` | `id` |
| `GTEx_get_median_gene_expression` | `gencode_id` only | `gencode_id` + `operation="median"` |
| `OpenTargets_*` | `ensemblID` | `ensemblId` (camelCase) |

**Rule**: Before calling any tool for the first time in a skill, confirm params via `get_tool_info()` once per tool family, or maintain a vetted param map in the skill.

**Why this matters**: Retry logic won't help if you're calling a tool with wrong parameter names - it will consistently return empty. This is different from API flakiness.

### 2. Foundation Data Layer (Path 0)

**Problem**: Skills query specialized tools for each section independently, missing data that a comprehensive aggregator already has. Results are inconsistent when specialized tools fail.

**Solution**: Identify if your domain has a **comprehensive aggregator** and query it FIRST before specialized tools.

**Examples by domain**:

| Domain | Foundation Source | What It Provides |
|--------|-------------------|------------------|
| Drug targets | Open Targets | Diseases, tractability, safety, drugs, GO, publications, mouse models |
| Chemicals | PubChem | Properties, bioactivity, patents, literature |
| Diseases | Open Targets / OMIM | Genes, drugs, phenotypes, literature |
| Genes | MyGene / Ensembl | Annotations, cross-refs, GO, pathways |

**Pattern**:
```markdown
## Workflow
Phase 0: Foundation Data (aggregator query)
Phase 1: Disambiguation (ID resolution, collision detection)
Phase 2: Specialized Queries (fill gaps from Phase 0)
Phase 3: Report Synthesis
```

**Why this works**: The aggregator provides reliable baseline data across multiple sections. Specialized tools then add depth or fill gaps, rather than being the sole source.

### 3. Versioned Identifier Handling

**Problem**: Some APIs require versioned identifiers (e.g., GTEx needs `ENSG00000123456.12`), while others reject them. Skills fail silently when using the wrong format.

**Solution**: During ID resolution, capture BOTH versioned and unversioned forms:

```python
ids = {
    'ensembl': 'ENSG00000123456',           # Unversioned (most APIs)
    'ensembl_versioned': 'ENSG00000123456.12'  # Versioned (GTEx, some others)
}

# Get version from Ensembl lookup
gene_info = tu.tools.ensembl_lookup_gene(id=ensembl_id, species="human")
if gene_info and gene_info.get('version'):
    ids['ensembl_versioned'] = f"{ensembl_id}.{gene_info['version']}"
```

**Fallback strategy**:
1. Try unversioned first (more portable)
2. If empty, try versioned
3. Document which format worked

**Common versioned ID APIs**: GTEx, GENCODE, some Ensembl endpoints

### 4. Disambiguation Before Research

**Problem**: Skills that jump straight to literature search often miss target details or retrieve irrelevant papers due to naming collisions.

**Solution**: Add a disambiguation phase before any literature search:

```markdown
## Phase 1: Target Disambiguation (Default ON)

### 1.1 Resolve Official Identifiers
- UniProt accession (canonical protein)
- Ensembl gene ID + version (for expression data)
- NCBI Gene ID (for literature)
- ChEMBL target ID (for drug data)

### 1.2 Gather Synonyms and Aliases
- All known gene symbols
- Protein name variants
- Historical names

### 1.3 Detect Naming Collisions
- Search "[SYMBOL]"[Title] - review top 20 results
- If >20% off-topic → identify collision terms
- Build negative filter: NOT [collision1] NOT [collision2]

### 1.4 Get Baseline Profile (from annotation DBs, not literature)
- Protein domains (InterPro)
- Subcellular location (HPA)
- Tissue expression (GTEx)
- GO terms and pathways
```

**Why this works**: Annotation databases provide reliable baseline data even when literature is sparse or noisy.

### 5. Report-Only Output (Hide Search Process)

**Problem**: Users don't want to see "searched 8 databases, found 1,247 papers, deduplicated to 892..."

**Solution**: Output structure:

| File | Content | When |
|------|---------|------|
| `[topic]_report.md` | Narrative findings only | Always (default) |
| `[topic]_bibliography.json` | Full deduplicated papers | Always |
| `methods_appendix.md` | Search methodology | Only if requested |

**In the report**:
- ✅ DO: "The literature reveals three main therapeutic approaches..."
- ❌ DON'T: "I searched PubMed, OpenAlex, and EuropePMC, finding 342 papers..."

### 6. Evidence Grading

**Problem**: A review article mention is treated the same as a mechanistic study with direct evidence.

**Solution**: Apply evidence tiers to every claim:

| Tier | Symbol | Criteria |
|------|--------|----------|
| T1 | ★★★ | Mechanistic study with direct evidence |
| T2 | ★★☆ | Functional study (knockdown, overexpression) |
| T3 | ★☆☆ | Association (screen hit, GWAS, correlation) |
| T4 | ☆☆☆ | Mention (review, text-mined, peripheral) |

**In report**:
```markdown
ATP6V1A drives lysosomal acidification [★★★: PMID:12345678] and has been 
implicated in cancer progression [★☆☆: PMID:23456789, TCGA expression data].
```

**Required locations for evidence grades**:
1. Executive Summary - key disease claims
2. Disease Associations - every disease link
3. Key Papers table - evidence tier column
4. Recommendations - reference evidence quality

**Per-section summary**:
```markdown
### Theme: Lysosomal Function (47 papers)
**Evidence Quality**: Strong (32 mechanistic, 11 functional, 4 association)
```

### 7. Quantified Completeness (Not Just Categorical)

**Problem**: "Include PPIs" is aspirational; reports pass the checklist but are data-thin.

**Solution**: Define **numeric minimums** for each section:

| Section | Minimum Data | If Not Met |
|---------|--------------|------------|
| PPIs | ≥20 interactors | Explain why fewer + which tools failed |
| Expression | Top 10 tissues with values | Note "limited data" with specific gaps |
| Disease | Top 10 associations with scores | Note if fewer available |
| Variants | All 4 constraint scores (pLI, LOEUF, missense Z, pRec) | Note which unavailable |
| Druggability | All modalities assessed | "No drugs/probes" is valid data |
| Literature | Total + 5-year trend + 3-5 key papers | Note if sparse (<50 papers) |

**Why this matters**: Quantified minimums make completeness auditing objective and mechanical, not subjective.

### 8. Mandatory Completeness Checklist

**Problem**: Reports have inconsistent sections; some topics get skipped entirely.

**Solution**: Define mandatory sections that MUST exist, even if populated with "Limited evidence" or "Unknown":

```markdown
## Completeness Checklist (ALL Required)

### Identity & Context
- [ ] Official identifiers resolved (all 6 types)
- [ ] Synonyms/aliases documented
- [ ] Naming collisions handled (or "none detected")

### Biology
- [ ] Protein architecture (or "N/A for non-protein")
- [ ] Subcellular localization
- [ ] Expression profile (≥10 tissues with values)
- [ ] Pathway involvement (≥10 pathways)

### Mechanism
- [ ] Core function with evidence grades
- [ ] Model organism data (or "none found")
- [ ] Key assays described

### Disease & Clinical
- [ ] Genetic variants (SNVs and CNVs separated)
- [ ] Constraint scores (all 4, with interpretations)
- [ ] Disease links with evidence grades (≥10 or "limited")

### Druggability
- [ ] Tractability for all modalities
- [ ] Known drugs (or "none")
- [ ] Chemical probes (or "none available")
- [ ] Clinical pipeline (or "none")

### Synthesis (CRITICAL)
- [ ] Research themes (≥3 papers each, or "limited")
- [ ] Open questions/gaps
- [ ] Biological model synthesized
- [ ] Testable hypotheses (≥3)
```

### 9. Aggregated Data Gaps Section

**Problem**: "No data" notes scattered across 14 sections; users can't quickly see what's missing.

**Solution**: Add a dedicated **Data Gaps & Limitations** section that consolidates all gaps:

```markdown
## 15. Data Gaps & Limitations

| Section | Expected Data | Actual | Reason | Alternative Source |
|---------|---------------|--------|--------|-------------------|
| 6. PPIs | ≥20 interactors | 8 | Novel target, limited studies | Literature review needed |
| 7. Expression | GTEx TPM | None | Versioned ID not recognized | See HPA data |
| 9. Probes | Chemical probes | None | No validated probes exist | Consider tool compound dev |

**Recommendations for Data Gaps**:
1. For PPIs: Query BioGRID with broader parameters; check yeast-2-hybrid studies
2. For Expression: Query GEO directly for tissue-specific datasets
```

**Why this matters**: Users can quickly assess data quality and know where to look for more information.

### 10. Query Strategy Optimization

**Problem**: Simple keyword searches retrieve too much noise or miss relevant papers.

**Solution**: Three-step collision-aware query strategy:

```markdown
## Query Strategy

### Step 1: High-Precision Seeds
Build a mechanistic core set (15-30 papers):
- "[GENE_SYMBOL]"[Title] AND mechanism
- "[FULL_PROTEIN_NAME]"[Title]
- "UniProt:ACCESSION"

### Step 2: Citation Network Expansion
From seeds, expand via citations:
- Forward: PubMed_get_cited_by, EuropePMC_get_citations
- Related: PubMed_get_related
- Backward: EuropePMC_get_references

### Step 3: Collision-Filtered Broad
Apply negative filters for known collisions:
- "TRAG" AND immune NOT plasmid NOT conjugation
- "JAK" AND kinase NOT "just another"
```

**Citation-first for sparse targets**: When keyword search returns <30 papers, prioritize citation expansion from the few good seeds.

### 11. Tool Failure Handling

**Problem**: NCBI elink and other APIs can be flaky; skills fail silently.

**Solution**: Automatic retry with fallback chains:

```markdown
## Failure Handling

### Retry Protocol
Attempt 1 → fails → wait 2s → Attempt 2 → fails → wait 5s → Fallback

### Fallback Chains
| Primary | Fallback 1 | Fallback 2 |
|---------|------------|------------|
| PubMed_get_cited_by | EuropePMC_get_citations | OpenAlex citations |
| PubMed_get_related | SemanticScholar | Keyword search |
| GTEx_* | HPA_* | Note as unavailable |
| Unpaywall | EuropePMC OA flag | OpenAlex is_oa |
| ChEMBL_get_target_activities | GtoPdb_get_target_ligands | OpenTargets drugs |
| intact_get_interactions | STRING_get_protein_interactions | OpenTargets interactions |

### Document Failures
In report: "Expression data unavailable (GTEx API timeout after 3 attempts)"
```

**Rule**: NEVER silently skip failed tools. Always document in the Data Gaps section.

### 12. Scalable Output Structure

**Problem**: Reports with 500+ papers become unreadable; users can't find what they need.

**Solution**: Separate narrative from data:

**Narrative report** (~20-50 pages max):
- Executive summary
- Key findings by theme
- Top 20-50 papers highlighted
- Conclusions and hypotheses

**Bibliography files** (unlimited):
- `[topic]_bibliography.json` - Full structured data
- `[topic]_bibliography.csv` - Tabular for filtering

**JSON structure**:
```json
{
  "pmid": "12345678",
  "doi": "10.1038/xxx",
  "title": "...",
  "evidence_tier": "T1",
  "themes": ["lysosomal_function", "autophagy"],
  "is_core_seed": true,
  "oa_status": "gold"
}
```

### 13. Synthesis Sections

**Problem**: Reports describe what was found but don't synthesize into actionable insights.

**Solution**: Require synthesis sections:

```markdown
## Required Synthesis Sections

### Biological Model (3-5 paragraphs)
Integrate all evidence into a coherent model:
- What does the target do?
- How does it connect to disease?
- What's the key uncertainty?

### Testable Hypotheses (≥3)
| # | Hypothesis | Perturbation | Readout | Expected |
|---|------------|--------------|---------|----------|
| 1 | [Hypothesis] | [Experiment] | [Measure] | [Prediction] |

### Suggested Experiments
Brief description of how to test each hypothesis.
```

---

## Skill Review Checklist

When reviewing a ToolUniverse skill, check:

### Tool Contract
- [ ] Tool parameters verified via `get_tool_info()` or documented corrections
- [ ] Versioned vs unversioned ID handling specified
- [ ] Foundation data source identified (if available for domain)

### Report Quality
- [ ] Report focuses on content, not search process
- [ ] Methodology in separate appendix (optional)
- [ ] Evidence grades applied to claims (T1-T4)
- [ ] Source attribution on every fact
- [ ] Sections exist even if "limited evidence"

### Query Strategy
- [ ] Disambiguation phase before search
- [ ] Collision detection for ambiguous names
- [ ] High-precision seeds before broad search
- [ ] Citation expansion option for sparse topics
- [ ] Negative filters documented

### Tool Usage
- [ ] Annotation tools used (not just literature)
- [ ] Fallback chains defined
- [ ] Failure handling with retry
- [ ] OA handling (full or best-effort)

### Completeness
- [ ] Quantified minimums defined per section
- [ ] Completeness checklist with checkboxes
- [ ] Data Gaps section aggregates all missing data
- [ ] "Negative results" explicitly documented ("no probes" not blank)

### Output Structure
- [ ] Main report is narrative-focused
- [ ] Bibliography in separate JSON/CSV
- [ ] Synthesis sections required

### User Experience
- [ ] Progress updates are brief
- [ ] No raw tool outputs shown
- [ ] Final report is the deliverable

---

## Common Anti-Patterns to Fix

### 1. "Search Log" Reports
**Bad**: "Round 1: Searched PubMed (234 papers), OpenAlex (456 papers)..."
**Fix**: Keep methodology internal; report findings only

### 2. Missing Disambiguation
**Bad**: Search "JAK" and get kinase + "just another kinase" papers mixed
**Fix**: Add collision detection; build negative filters

### 3. No Evidence Grading
**Bad**: "Multiple studies show..." (which studies? what quality?)
**Fix**: Apply T1-T4 grades; label each claim

### 4. Empty Sections Omitted
**Bad**: Skip "Pathogen Involvement" because nothing found
**Fix**: Include section with "None identified in literature search"

### 5. No Synthesis
**Bad**: Long list of papers organized by theme
**Fix**: Add biological model + testable hypotheses

### 6. Monolithic Bibliography
**Bad**: 200 papers embedded in report narrative
**Fix**: Top 20-50 in report; full list in JSON/CSV

### 7. Silent Failures
**Bad**: "Expression data: [blank]" (tool failed, user doesn't know)
**Fix**: "Expression data unavailable (API timeout); see HPA directly"

### 8. Wrong Tool Parameters (NEW)
**Bad**: `Reactome_map_uniprot_to_pathways(uniprot_id=...)` returns empty
**Fix**: Verify params via `get_tool_info()`; use correct param `id`

### 9. Missing Versioned IDs (NEW)
**Bad**: GTEx returns empty for `ENSG00000123456`
**Fix**: Try versioned ID `ENSG00000123456.12`; document which worked

### 10. No Foundation Layer (NEW)
**Bad**: Query 15 specialized tools independently, miss data when some fail
**Fix**: Query comprehensive aggregator (e.g., Open Targets) first

### 11. Scattered "No Data" Notes (NEW)
**Bad**: "No data" in 5 different sections; user doesn't know overall gaps
**Fix**: Aggregate all gaps in dedicated Data Gaps section with recommendations

### 12. Aspirational Completeness (NEW)
**Bad**: "Include PPIs" ✓ (but only 3 interactors listed)
**Fix**: "≥20 PPIs OR explanation why fewer"

---

## Template: Optimized Skill Structure

```markdown
---
name: [domain]-research
description: [What it does]. Creates detailed report with evidence grading 
and mandatory completeness. [When to use triggers].
---

# [Domain] Research Strategy

## When to Use
[Trigger scenarios]

## Workflow
Phase -1: Tool Verification → Phase 0: Foundation Data → Phase 1: Disambiguate → Phase 2: Search → Phase 3: Report

## Phase -1: Tool Verification
[Parameter corrections table for tools used in this skill]

## Phase 0: Foundation Data
[Comprehensive aggregator query - e.g., Open Targets for targets]

## Phase 1: Disambiguation (Default ON)
[ID resolution (versioned + unversioned), collision detection, baseline profile]

## Phase 2: Specialized Queries (Internal)
[Query strategy with collision filters, citation expansion, tool fallbacks]

## Phase 3: Report Synthesis
[Progressive writing, evidence grading, mandatory sections]

## Output Files
- `[topic]_report.md` (narrative, always)
- `[topic]_bibliography.json` (data, always)
- `methods_appendix.md` (only if requested)

## Quantified Minimums
[Specific numbers per section - e.g., ≥20 PPIs, top 10 tissues]

## Completeness Checklist
[ALL required sections with checkboxes]

## Data Gaps Section
[Template for aggregating missing data with recommendations]

## Evidence Grading
[T1-T4 definitions with required locations]

## Tool Reference
[Tools by category with fallback chains and parameter notes]
```

---

## Quick Fixes for Common Complaints

| User Complaint | Root Cause | Fix |
|----------------|------------|-----|
| "Report is too short" | Missing annotation data | Add Phase 1 disambiguation + Phase 0 foundation |
| "Too much noise" | No collision filtering | Add negative query filters |
| "Can't tell what's important" | No evidence grading | Add T1-T4 tiers |
| "Missing sections" | No completeness checklist | Add mandatory sections with minimums |
| "Too long/unreadable" | Monolithic output | Separate narrative from JSON |
| "Just a list of papers" | No synthesis | Add biological model + hypotheses |
| "Shows search process" | Wrong output focus | Report-only; methodology in appendix |
| "Tool failed, no data" | No fallback handling | Add retry + fallback chains |
| "Empty results, no error" | Wrong tool parameters | Add Phase -1 param verification |
| "GTEx returns nothing" | Versioned ID needed | Try `ENSG*.version` format |
| "Data seems incomplete" | No foundation layer | Add Phase 0 with aggregator |
| "Can't tell what's missing" | Scattered gaps | Add Data Gaps section |

---

## Summary

**Seven pillars of optimized ToolUniverse skills**:

1. **Verify tool contracts** - Check params via `get_tool_info()`; maintain corrections table
2. **Foundation first** - Query comprehensive aggregators before specialized tools
3. **Disambiguate carefully** - Resolve IDs (versioned + unversioned), detect collisions, get baseline from annotation DBs
4. **Grade evidence** - T1-T4 tiers on all claims; summarize quality per section
5. **Require quantified completeness** - Numeric minimums, not just "include X"
6. **Report content, not process** - Methodology in appendix only if asked; aggregate gaps in one section
7. **Synthesize** - Biological models and testable hypotheses, not just paper lists

Apply these principles to any ToolUniverse research skill for better user experience and actionable output.
