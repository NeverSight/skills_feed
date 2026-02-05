---
name: tooluniverse-target-research
description: Gather comprehensive biological target intelligence from 9 parallel research paths covering protein info, structure, interactions, pathways, expression, variants, drug interactions, and literature. Features collision-aware searches, evidence grading (T1-T4), explicit Open Targets coverage, and mandatory completeness auditing. Use when users ask about drug targets, proteins, genes, or need target validation, druggability assessment, or comprehensive target profiling.
---

# Comprehensive Target Intelligence Gatherer

Gather complete target intelligence by exploring 9 parallel research paths. Supports targets identified by gene symbol, UniProt accession, Ensembl ID, or gene name.

**KEY PRINCIPLES**:
1. **Report-first approach** - Create report file FIRST, then populate progressively
2. **Tool parameter verification** - Verify params via `get_tool_info` before calling unfamiliar tools
3. **Evidence grading** - Grade all claims by evidence strength (T1-T4)
4. **Citation requirements** - Every fact must have inline source attribution
5. **Mandatory completeness** - All sections must exist with data minimums or explicit "No data" notes
6. **Disambiguation first** - Resolve all identifiers before research
7. **Negative results documented** - "No drugs found" is data; empty sections are failures
8. **Collision-aware literature search** - Detect and filter naming collisions

---

## Phase 0: Tool Parameter Verification (CRITICAL)

**BEFORE calling ANY tool for the first time**, verify its parameters:

```python
# Always check tool params to prevent silent failures
tool_info = tu.tools.get_tool_info(tool_name="Reactome_map_uniprot_to_pathways")
# Reveals: takes `id` not `uniprot_id`
```

### Known Parameter Corrections (Updated)

| Tool | WRONG Parameter | CORRECT Parameter |
|------|-----------------|-------------------|
| `Reactome_map_uniprot_to_pathways` | `uniprot_id` | `id` |
| `ensembl_get_xrefs` | `gene_id` | `id` |
| `GTEx_get_median_gene_expression` | `gencode_id` only | `gencode_id` + `operation="median"` |
| `OpenTargets_*` | `ensemblID` | `ensemblId` (camelCase) |

### GTEx Versioned ID Fallback (CRITICAL)

GTEx often requires versioned Ensembl IDs. If `ENSG00000123456` returns empty:

```python
# Step 1: Get gene info with version
gene_info = tu.tools.ensembl_lookup_gene(id=ensembl_id, species="human")
version = gene_info.get('version', 1)

# Step 2: Try versioned ID
versioned_id = f"{ensembl_id}.{version}"  # e.g., "ENSG00000123456.12"
result = tu.tools.GTEx_get_median_gene_expression(
    gencode_id=versioned_id,
    operation="median"
)
```

---

## When to Use This Skill

Apply when users:
- Ask about a drug target, protein, or gene
- Need target validation or assessment
- Request druggability analysis
- Want comprehensive target profiling
- Ask "what do we know about [target]?"
- Need target-disease associations
- Request safety profile for a target

---

## Critical Workflow Requirements

### 1. Report-First Approach (MANDATORY)

**DO NOT** show the search process or tool outputs to the user. Instead:

1. **Create the report file FIRST** - Before any data collection:
   - File name: `[TARGET]_target_report.md`
   - Initialize with all 14 section headers
   - Add placeholder: `[Researching...]` in each section

2. **Progressively update the report** - As you gather data:
   - Update each section immediately after retrieving data
   - Replace `[Researching...]` with actual content
   - Include "No data returned" when tools return empty results

3. **Methodology in appendix only** - If user requests methodology details, create separate `[TARGET]_methods_appendix.md`

### 2. Evidence Grading System (MANDATORY)

**CRITICAL**: Grade every claim by evidence strength.

#### Evidence Tiers

| Tier | Symbol | Criteria | Examples |
|------|--------|----------|----------|
| **T1** | ★★★ | Direct mechanistic evidence, human genetic proof | CRISPR KO, patient mutations, crystal structure with mechanism |
| **T2** | ★★☆ | Functional studies, model organism validation | siRNA phenotype, mouse KO, biochemical assay |
| **T3** | ★☆☆ | Association, screen hits, computational | GWAS hit, DepMap essentiality, expression correlation |
| **T4** | ☆☆☆ | Mention, review, text-mined, predicted | Review article, database annotation, computational prediction |

#### Required Evidence Grading Locations

Evidence grades MUST appear in:
1. **Executive Summary** - Key disease claims graded
2. **Section 8.2 Disease Associations** - Every disease link graded with source type
3. **Section 11 Literature** - Key papers table with evidence tier
4. **Section 13 Recommendations** - Scorecard items reference evidence quality

#### Per-Section Evidence Summary

```markdown
---
**Evidence Quality for this Section**: Strong
- Mechanistic (T1): 12 papers
- Functional (T2): 8 papers
- Association (T3): 15 papers
- Mention (T4): 23 papers
**Data Gaps**: No CRISPR data; mouse KO phenotypes limited
---
```

### 3. Citation Requirements (MANDATORY)

Every piece of information MUST include its source:

```markdown
EGFR mutations cause lung adenocarcinoma [★★★: PMID:15118125, activating mutations 
in patients]. *Source: ClinVar, CIViC*
```

---

## Core Strategy: 9 Research Paths

Execute 9 research paths (Path 0 is always first):

```
Target Query (e.g., "EGFR" or "P00533")
│
├─ PATH 0: Open Targets Foundation (ALWAYS FIRST - fills gaps in all other paths)
│
├─ PATH 1: Core Identity (names, IDs, sequence, organism)
├─ PATH 2: Structure & Domains (3D structure, domains, binding sites)
├─ PATH 3: Function & Pathways (GO terms, pathways, biological role)
├─ PATH 4: Protein Interactions (PPI network, complexes)
├─ PATH 5: Expression Profile (tissue expression, single-cell)
├─ PATH 6: Variants & Disease (mutations, clinical significance)
├─ PATH 7: Drug Interactions (known drugs, druggability, safety)
└─ PATH 8: Literature & Research (publications, trends)
```

---

## Identifier Resolution (Phase 1)

**CRITICAL**: Resolve ALL identifiers before any research path.

```python
def resolve_target_ids(tu, query):
    """
    Resolve target query to ALL needed identifiers.
    Returns dict with: query, uniprot, ensembl, ensembl_version, symbol, 
    entrez, chembl_target, hgnc
    """
    ids = {
        'query': query, 
        'uniprot': None, 
        'ensembl': None, 
        'ensembl_versioned': None,  # For GTEx
        'symbol': None,
        'entrez': None,
        'chembl_target': None,
        'hgnc': None,
        'full_name': None,
        'synonyms': []
    }
    
    # [Resolution logic based on input type]
    # ... (see current implementation)
    
    # CRITICAL: Get versioned Ensembl ID for GTEx
    if ids['ensembl']:
        gene_info = tu.tools.ensembl_lookup_gene(id=ids['ensembl'], species="human")
        if gene_info and gene_info.get('version'):
            ids['ensembl_versioned'] = f"{ids['ensembl']}.{gene_info['version']}"
        
        # Also get synonyms for literature collision detection
        ids['full_name'] = gene_info.get('description', '').split(' [')[0]
    
    # Get UniProt alternative names for synonyms
    if ids['uniprot']:
        alt_names = tu.tools.UniProt_get_alternative_names_by_accession(accession=ids['uniprot'])
        if alt_names:
            ids['synonyms'].extend(alt_names)
    
    return ids
```

### Collision Detection for Literature Search

Before literature search, detect naming collisions:

```python
def detect_collisions(tu, symbol, full_name):
    """
    Detect if gene symbol has naming collisions in literature.
    Returns negative filter terms if collisions found.
    """
    # Search by symbol in title
    results = tu.tools.PubMed_search_articles(
        query=f'"{symbol}"[Title]',
        limit=20
    )
    
    # Check if >20% are off-topic
    off_topic_terms = []
    for paper in results.get('articles', []):
        title = paper.get('title', '').lower()
        # Check if title mentions biology/protein/gene context
        bio_terms = ['protein', 'gene', 'cell', 'expression', 'mutation', 'kinase', 'receptor']
        if not any(term in title for term in bio_terms):
            # Extract potential collision terms
            # e.g., "JAK" might collide with "Just Another Kinase" jokes
            # e.g., "WDR7" might collide with other WDR family members in certain contexts
            pass
    
    # Build negative filter
    collision_filter = ""
    if off_topic_terms:
        collision_filter = " NOT " + " NOT ".join(off_topic_terms)
    
    return collision_filter
```

---

## PATH 0: Open Targets Foundation (ALWAYS FIRST)

**Objective**: Populate baseline data for Sections 5, 8, 9, 10, 11 before specialized queries.

**CRITICAL**: Open Targets provides the most comprehensive aggregated data. Query ALL these endpoints:

| Endpoint | Section | Data Type |
|----------|---------|-----------|
| `OpenTargets_get_diseases_phenotypes_by_target_ensemblId` | 8 | Diseases/phenotypes |
| `OpenTargets_get_target_tractability_by_ensemblId` | 9 | Druggability assessment |
| `OpenTargets_get_target_safety_profile_by_ensemblId` | 10 | Safety liabilities |
| `OpenTargets_get_target_interactions_by_ensemblId` | 6 | PPI network |
| `OpenTargets_get_target_gene_ontology_by_ensemblId` | 5 | GO annotations |
| `OpenTargets_get_publications_by_target_ensemblId` | 11 | Literature |
| `OpenTargets_get_biological_mouse_models_by_ensemblId` | 8/10 | Mouse KO phenotypes |
| `OpenTargets_get_chemical_probes_by_target_ensemblId` | 9 | Chemical probes |
| `OpenTargets_get_associated_drugs_by_target_ensemblId` | 9 | Known drugs |

### Path 0 Implementation

```python
def path_0_open_targets(tu, ids):
    """
    Open Targets foundation data - fills gaps for sections 5, 6, 8, 9, 10, 11.
    ALWAYS run this first.
    """
    ensembl_id = ids['ensembl']
    if not ensembl_id:
        return {'status': 'skipped', 'reason': 'No Ensembl ID'}
    
    results = {}
    
    # 1. Diseases & Phenotypes (Section 8)
    diseases = tu.tools.OpenTargets_get_diseases_phenotypes_by_target_ensemblId(
        ensemblId=ensembl_id
    )
    results['diseases'] = diseases if diseases else {'note': 'No disease associations returned'}
    
    # 2. Tractability (Section 9)
    tractability = tu.tools.OpenTargets_get_target_tractability_by_ensemblId(
        ensemblId=ensembl_id
    )
    results['tractability'] = tractability if tractability else {'note': 'No tractability data returned'}
    
    # 3. Safety Profile (Section 10)
    safety = tu.tools.OpenTargets_get_target_safety_profile_by_ensemblId(
        ensemblId=ensembl_id
    )
    results['safety'] = safety if safety else {'note': 'No safety liabilities identified'}
    
    # 4. Interactions (Section 6)
    interactions = tu.tools.OpenTargets_get_target_interactions_by_ensemblId(
        ensemblId=ensembl_id
    )
    results['interactions'] = interactions if interactions else {'note': 'No interactions returned'}
    
    # 5. GO Annotations (Section 5)
    go_terms = tu.tools.OpenTargets_get_target_gene_ontology_by_ensemblId(
        ensemblId=ensembl_id
    )
    results['go_terms'] = go_terms if go_terms else {'note': 'No GO annotations returned'}
    
    # 6. Publications (Section 11)
    publications = tu.tools.OpenTargets_get_publications_by_target_ensemblId(
        ensemblId=ensembl_id
    )
    results['publications'] = publications if publications else {'note': 'No publications returned'}
    
    # 7. Mouse Models (Section 8/10)
    mouse_models = tu.tools.OpenTargets_get_biological_mouse_models_by_ensemblId(
        ensemblId=ensembl_id
    )
    results['mouse_models'] = mouse_models if mouse_models else {'note': 'No mouse model data returned'}
    
    # 8. Chemical Probes (Section 9)
    probes = tu.tools.OpenTargets_get_chemical_probes_by_target_ensemblId(
        ensemblId=ensembl_id
    )
    results['chemical_probes'] = probes if probes else {'note': 'No chemical probes available'}
    
    # 9. Associated Drugs (Section 9)
    drugs = tu.tools.OpenTargets_get_associated_drugs_by_target_ensemblId(
        ensemblId=ensembl_id
    )
    results['drugs'] = drugs if drugs else {'note': 'No approved/trial drugs found'}
    
    return results
```

### Negative Results Are Data

**CRITICAL**: Always document when a query returns empty:

```markdown
### 9.3 Chemical Probes

**Status**: No validated chemical probes available for this target.
*Source: OpenTargets_get_chemical_probes_by_target_ensemblId returned empty*

**Implication**: Tool compound development would be needed for chemical biology studies.
```

---

## PATH 2: Structure & Domains (Enhanced)

**Objective**: Robust structure coverage using 3-step chain.

### 3-Step Structure Search Chain

**Do NOT rely solely on PDB text search.** Use this chain:

```python
def path_structure_robust(tu, ids):
    """
    Robust structure search using 3-step chain.
    """
    structures = {'pdb': [], 'alphafold': None, 'domains': [], 'method_notes': []}
    
    # STEP 1: UniProt PDB Cross-References (most reliable)
    if ids['uniprot']:
        entry = tu.tools.UniProt_get_entry_by_accession(accession=ids['uniprot'])
        pdb_xrefs = [x for x in entry.get('uniProtKBCrossReferences', []) 
                    if x.get('database') == 'PDB']
        for xref in pdb_xrefs:
            pdb_id = xref.get('id')
            # Get details for each PDB
            pdb_info = tu.tools.get_protein_metadata_by_pdb_id(pdb_id=pdb_id)
            if pdb_info:
                structures['pdb'].append(pdb_info)
        structures['method_notes'].append(f"Step 1: {len(pdb_xrefs)} PDB cross-refs from UniProt")
    
    # STEP 2: Sequence-based PDB Search (catches missing annotations)
    if ids['uniprot'] and len(structures['pdb']) < 5:
        sequence = tu.tools.UniProt_get_sequence_by_accession(accession=ids['uniprot'])
        if sequence and len(sequence) < 1000:  # Reasonable length for search
            similar = tu.tools.PDB_search_similar_structures(
                sequence=sequence[:500],  # Use first 500 AA if long
                identity_cutoff=0.7
            )
            if similar:
                for hit in similar[:10]:  # Top 10 similar
                    if hit['pdb_id'] not in [s.get('pdb_id') for s in structures['pdb']]:
                        structures['pdb'].append(hit)
        structures['method_notes'].append(f"Step 2: Sequence search (identity ≥70%)")
    
    # STEP 3: Domain-based Search (for multi-domain proteins)
    if ids['uniprot']:
        domains = tu.tools.InterPro_get_protein_domains(uniprot_accession=ids['uniprot'])
        structures['domains'] = domains if domains else []
        
        # For large proteins with domains, search by domain sequence windows
        if len(structures['pdb']) < 3 and domains:
            for domain in domains[:3]:  # Top 3 domains
                domain_name = domain.get('name', '')
                # Could search PDB by domain name
                domain_hits = tu.tools.PDB_search_by_keyword(query=domain_name, limit=5)
                if domain_hits:
                    structures['method_notes'].append(f"Step 3: Domain '{domain_name}' search")
    
    # AlphaFold (always check)
    alphafold = tu.tools.alphafold_get_prediction(uniprot_accession=ids['uniprot'])
    structures['alphafold'] = alphafold if alphafold else {'note': 'No AlphaFold prediction'}
    
    # IMPORTANT: Document limitations
    if not structures['pdb']:
        structures['limitation'] = "No direct PDB hit does NOT mean no structure exists. Check: (1) structures under different UniProt entries, (2) homolog structures, (3) domain-only structures."
    
    return structures
```

### Structure Section Output Format

```markdown
### 4.1 Experimental Structures (PDB)

**Total PDB Entries**: 23 structures *(Source: UniProt cross-references)*
**Search Method**: 3-step chain (UniProt xrefs → sequence search → domain search)

| PDB ID | Resolution | Method | Ligand | Coverage | Year |
|--------|------------|--------|--------|----------|------|
| 1M17 | 2.6Å | X-ray | Erlotinib | 672-998 | 2002 |
| 3POZ | 2.8Å | X-ray | Gefitinib | 696-1022 | 2010 |

**Note**: "No direct PDB hit" ≠ "no structure exists". Check homologs and domain structures.
```

---

## PATH 5: Expression Profile (Enhanced)

### GTEx with Versioned ID Fallback

```python
def path_expression(tu, ids):
    """
    Expression data with GTEx versioned ID fallback.
    """
    results = {'gtex': None, 'hpa': None, 'failed_tools': []}
    
    # GTEx with fallback
    ensembl_id = ids['ensembl']
    versioned_id = ids.get('ensembl_versioned')
    
    # Try unversioned first
    gtex_result = tu.tools.GTEx_get_median_gene_expression(
        gencode_id=ensembl_id,
        operation="median"
    )
    
    # Fallback to versioned if empty
    if not gtex_result or gtex_result.get('data') == []:
        if versioned_id:
            gtex_result = tu.tools.GTEx_get_median_gene_expression(
                gencode_id=versioned_id,
                operation="median"
            )
            if gtex_result and gtex_result.get('data'):
                results['gtex'] = gtex_result
                results['gtex_note'] = f"Used versioned ID: {versioned_id}"
        
        if not results.get('gtex'):
            results['failed_tools'].append({
                'tool': 'GTEx_get_median_gene_expression',
                'tried': [ensembl_id, versioned_id],
                'fallback': 'See HPA data below'
            })
    else:
        results['gtex'] = gtex_result
    
    # HPA (always query as backup)
    hpa_result = tu.tools.HPA_get_rna_expression_by_source(ensembl_id=ensembl_id)
    results['hpa'] = hpa_result if hpa_result else {'note': 'No HPA RNA data'}
    
    return results
```

---

## PATH 6: Variants & Disease (Enhanced)

### ClinVar SNV vs CNV Separation

```markdown
### 8.3 Clinical Variants (ClinVar)

#### Single Nucleotide Variants (SNVs)
| Variant | Clinical Significance | Condition | Review Status | PMID |
|---------|----------------------|-----------|---------------|------|
| p.L858R | Pathogenic | Lung cancer | 4 stars | 15118125 |
| p.T790M | Pathogenic | Drug resistance | 4 stars | 15737014 |

**Total Pathogenic SNVs**: 47

#### Copy Number Variants (CNVs) - Reported Separately
| Type | Region | Clinical Significance | Frequency |
|------|--------|----------------------|-----------|
| Amplification | 7p11.2 | Pathogenic | Common in cancer |

*Note: CNV data separated as it represents different mutation mechanism*
```

---

## PATH 8: Literature & Research (Collision-Aware)

### Collision-Aware Query Strategy

```python
def path_literature_collision_aware(tu, ids):
    """
    Literature search with collision detection and filtering.
    """
    symbol = ids['symbol']
    full_name = ids.get('full_name', '')
    uniprot = ids['uniprot']
    synonyms = ids.get('synonyms', [])
    
    # Step 1: Detect collisions
    collision_filter = detect_collisions(tu, symbol, full_name)
    
    # Step 2: Build high-precision seed queries
    seed_queries = [
        f'"{symbol}"[Title] AND (protein OR gene OR expression)',  # Symbol in title
        f'"{full_name}"[Title]' if full_name else None,  # Full name in title
        f'"UniProt:{uniprot}"' if uniprot else None,  # UniProt accession
    ]
    seed_queries = [q for q in seed_queries if q]
    
    # Add key synonyms
    for syn in synonyms[:3]:
        seed_queries.append(f'"{syn}"[Title]')
    
    # Step 3: Execute seed queries and collect PMIDs
    seed_pmids = set()
    for query in seed_queries:
        if collision_filter:
            query = f"({query}){collision_filter}"
        results = tu.tools.PubMed_search_articles(query=query, limit=30)
        for article in results.get('articles', []):
            seed_pmids.add(article.get('pmid'))
    
    # Step 4: Expand via citation network (for sparse targets)
    if len(seed_pmids) < 30:
        expanded_pmids = set()
        for pmid in list(seed_pmids)[:10]:  # Top 10 seeds
            # Get related articles
            related = tu.tools.PubMed_get_related(pmid=pmid, limit=20)
            for r in related.get('articles', []):
                expanded_pmids.add(r.get('pmid'))
            
            # Get citing articles
            citing = tu.tools.EuropePMC_get_citations(pmid=pmid, limit=20)
            for c in citing.get('citations', []):
                expanded_pmids.add(c.get('pmid'))
        
        seed_pmids.update(expanded_pmids)
    
    # Step 5: Classify papers by evidence tier
    papers_by_tier = {'T1': [], 'T2': [], 'T3': [], 'T4': []}
    # ... classification logic based on title/abstract keywords
    
    return {
        'total_papers': len(seed_pmids),
        'collision_filter_applied': collision_filter if collision_filter else 'None needed',
        'seed_queries': seed_queries,
        'papers_by_tier': papers_by_tier
    }
```

---

## Retry Logic & Fallback Chains

### Retry Policy

For each critical tool, implement retry with exponential backoff:

```python
def call_with_retry(tu, tool_name, params, max_retries=3):
    """
    Call tool with retry logic.
    """
    for attempt in range(max_retries):
        try:
            result = getattr(tu.tools, tool_name)(**params)
            if result and not result.get('error'):
                return result
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                return {'error': str(e), 'tool': tool_name, 'attempts': max_retries}
    return None
```

### Fallback Chains (CRITICAL)

| Primary Tool | Fallback 1 | Fallback 2 | Failure Action |
|--------------|------------|------------|----------------|
| `ChEMBL_get_target_activities` | `GtoPdb_get_target_ligands` | `OpenTargets drugs` | Note in report |
| `intact_get_interactions` | `STRING_get_protein_interactions` | `OpenTargets interactions` | Note in report |
| `GO_get_annotations_for_gene` | `OpenTargets GO` | `MyGene GO` | Note in report |
| `GTEx_get_median_gene_expression` | `HPA_get_rna_expression` | Note as unavailable | Document in report |
| `gnomad_get_gene_constraints` | `OpenTargets constraint` | - | Note in report |
| `DGIdb_get_drug_gene_interactions` | `OpenTargets drugs` | `GtoPdb` | Note in report |

### Failure Surfacing Rule

**NEVER silently skip failed tools.** Always document:

```markdown
### 7.1 Tissue Expression

**GTEx Data**: Unavailable (API timeout after 3 attempts)
**Fallback Data (HPA)**:
| Tissue | Expression Level | Specificity |
|--------|-----------------|-------------|
| Liver | High | Enhanced |
| Kidney | Medium | - |

*Note: For complete GTEx data, query directly at gtexportal.org*
```

---

## Per-Section Data Minimums & Completeness Audit

### Minimum Data Requirements (Enforced)

| Section | Minimum Data | If Not Met |
|---------|--------------|------------|
| **6. PPIs** | ≥20 interactors | Document which tools failed + why |
| **7. Expression** | Top 10 tissues with TPM + HPA RNA summary | Note "limited data" with specific gaps |
| **8. Disease** | Top 10 OT diseases + gnomAD constraints + ClinVar summary | Separate SNV/CNV; note if constraint unavailable |
| **9. Druggability** | OT tractability + probes + drugs + DGIdb + GtoPdb fallback | "No drugs/probes" is valid data |
| **11. Literature** | Total count + 5-year trend + 3-5 key papers with evidence tiers | Note if sparse (<50 papers) |

### Post-Run Completeness Audit

Before finalizing the report, run this checklist:

```markdown
## Completeness Audit (REQUIRED)

### Data Minimums Check
- [ ] PPIs: ≥20 interactors OR explanation why fewer
- [ ] Expression: Top 10 tissues with values OR explicit "unavailable"
- [ ] Diseases: Top 10 associations with scores OR "no associations"
- [ ] Constraints: All 4 scores (pLI, LOEUF, missense Z, pRec) OR "unavailable"
- [ ] Druggability: All modalities assessed; probes + drugs listed OR "none"

### Negative Results Documented
- [ ] Empty tool results noted explicitly (not left blank)
- [ ] Failed tools with fallbacks documented
- [ ] "No data" sections have implications noted

### Evidence Quality
- [ ] T1-T4 grades in Executive Summary disease claims
- [ ] T1-T4 grades in Disease Associations table
- [ ] Key papers table has evidence tiers
- [ ] Per-section evidence summaries included

### Source Attribution
- [ ] Every data point has source tool/database cited
- [ ] Section-end source summaries present
```

### Data Gap Table (Required if minimums not met)

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

---

## Report Template (Initial File)

**File**: `[TARGET]_target_report.md`

```markdown
# Target Intelligence Report: [TARGET NAME]

**Generated**: [Date] | **Query**: [Original query] | **Status**: In Progress

---

## 1. Executive Summary
[Researching...]
<!-- REQUIRED: 2-3 sentences, disease claims must have T1-T4 grades -->

## 2. Target Identifiers
[Researching...]
<!-- REQUIRED: UniProt, Ensembl (versioned), Entrez, ChEMBL, HGNC, Symbol -->

## 3. Basic Information
### 3.1 Protein Description
[Researching...]
### 3.2 Protein Function
[Researching...]
### 3.3 Subcellular Localization
[Researching...]

## 4. Structural Biology
### 4.1 Experimental Structures (PDB)
[Researching...]
<!-- METHOD: 3-step chain (UniProt xrefs → sequence search → domain search) -->
### 4.2 AlphaFold Prediction
[Researching...]
### 4.3 Domain Architecture
[Researching...]
### 4.4 Key Structural Features
[Researching...]

## 5. Function & Pathways
### 5.1 Gene Ontology Annotations
[Researching...]
<!-- REQUIRED: Evidence codes mapped to T1-T4 -->
### 5.2 Pathway Involvement
[Researching...]

## 6. Protein-Protein Interactions
[Researching...]
<!-- MINIMUM: ≥20 interactors OR explanation -->

## 7. Expression Profile
### 7.1 Tissue Expression (GTEx/HPA)
[Researching...]
<!-- NOTE: Use versioned Ensembl ID for GTEx if needed -->
### 7.2 Tissue Specificity
[Researching...]
<!-- MINIMUM: Top 10 tissues with TPM values -->

## 8. Genetic Variation & Disease
### 8.1 Constraint Scores
[Researching...]
<!-- REQUIRED: pLI, LOEUF, missense Z, pRec with interpretations -->
### 8.2 Disease Associations
[Researching...]
<!-- REQUIRED: Top 10 with OT scores; T1-T4 evidence grades -->
### 8.3 Clinical Variants (ClinVar)
[Researching...]
<!-- REQUIRED: Separate SNV and CNV tables -->
### 8.4 Mouse Model Phenotypes
[Researching...]

## 9. Druggability & Pharmacology
### 9.1 Tractability Assessment
[Researching...]
<!-- REQUIRED: All modalities (SM, Ab, PROTAC, other) -->
### 9.2 Known Drugs
[Researching...]
### 9.3 Chemical Probes
[Researching...]
<!-- NOTE: "No probes" is valid data - document explicitly -->
### 9.4 Clinical Pipeline
[Researching...]
### 9.5 ChEMBL Bioactivity
[Researching...]

## 10. Safety Profile
### 10.1 Safety Liabilities
[Researching...]
### 10.2 Expression-Based Toxicity Risk
[Researching...]
### 10.3 Mouse KO Phenotypes
[Researching...]

## 11. Literature & Research Landscape
### 11.1 Publication Metrics
[Researching...]
<!-- REQUIRED: Total, 5y, 1y, drug-related, clinical -->
### 11.2 Research Trend
[Researching...]
### 11.3 Key Publications
[Researching...]
<!-- REQUIRED: Table with PMID, title, year, evidence tier -->
### 11.4 Evidence Summary by Theme
[Researching...]
<!-- REQUIRED: T1-T4 breakdown per research theme -->

## 12. Competitive Landscape
[Researching...]

## 13. Summary & Recommendations
### 13.1 Target Validation Scorecard
[Researching...]
<!-- REQUIRED: 6 criteria, 1-5 scores, evidence quality noted -->
### 13.2 Strengths
[Researching...]
### 13.3 Challenges & Risks
[Researching...]
### 13.4 Recommendations
[Researching...]
<!-- REQUIRED: ≥3 prioritized (HIGH/MEDIUM/LOW) -->

## 14. Data Sources & Methodology
[Will be populated as research progresses...]

## 15. Data Gaps & Limitations
[To be populated post-audit...]
```

---

## Quick Reference: Tool Parameters

| Tool | Parameter | Notes |
|------|-----------|-------|
| `Reactome_map_uniprot_to_pathways` | `id` | NOT `uniprot_id` |
| `ensembl_get_xrefs` | `id` | NOT `gene_id` |
| `GTEx_get_median_gene_expression` | `gencode_id`, `operation` | Try versioned ID if empty |
| `OpenTargets_*` | `ensemblId` | camelCase, not `ensemblID` |
| `STRING_get_protein_interactions` | `protein_ids`, `species` | List format for IDs |
| `intact_get_interactions` | `identifier` | UniProt accession |

---

## When NOT to Use This Skill

- Simple protein lookup → Use `UniProt_get_entry_by_accession` directly
- Drug information only → Use drug-focused tools
- Disease-centric query → Use disease-intelligence-gatherer skill
- Sequence retrieval → Use sequence-retrieval skill
- Structure download → Use protein-structure-retrieval skill

Use this skill for comprehensive, multi-angle target analysis with guaranteed data completeness.
