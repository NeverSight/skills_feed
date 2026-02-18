---
name: tooluniverse-epigenomics
description: Comprehensive epigenomics and gene regulation analysis integrating ENCODE functional genomics data, JASPAR transcription factor binding motifs, SCREEN cis-regulatory elements, ReMap TF binding sites, RegulomeDB variant regulatory scoring, 4D Nucleome chromatin conformation, and Ensembl regulatory features. Performs regulatory element cataloging, transcription factor analysis, variant regulatory impact scoring, chromatin conformation mapping, and gene-centric regulatory landscape profiling. Use when asked about gene regulation, enhancers, promoters, transcription factor binding, epigenetic modifications, chromatin structure, regulatory variants, or non-coding genome function.
---

# Epigenomics & Gene Regulation Analysis

Comprehensive analysis of the regulatory genome integrating functional genomics experiments, transcription factor binding data, cis-regulatory element catalogs, chromatin conformation, and variant regulatory scoring. Generates structured regulatory landscape reports with evidence grading.

## When to Use This Skill

**Triggers**:
- "What regulates [gene]?" / "Show the regulatory landscape of [gene]"
- "What transcription factors bind to [gene/region]?"
- "Find enhancers near [gene]"
- "What is the regulatory impact of variant [rsID]?"
- "Find ENCODE experiments for [histone mark/TF] in [cell type]"
- "What is the chromatin structure around [gene/region]?"
- "Analyze the epigenetic regulation of [gene]"
- "Find transcription factor binding motifs for [TF]"
- "Regulatory element analysis for [genomic region]"

**Use Cases**:
1. **Gene Regulatory Landscape**: Comprehensive view of all regulatory elements, TF binding, and chromatin around a gene
2. **Transcription Factor Profiling**: TF binding motifs (JASPAR), binding sites (ReMap), and target gene identification
3. **Regulatory Variant Interpretation**: Assess non-coding variant impact using RegulomeDB, SCREEN, and ENCODE
4. **Functional Genomics Data Discovery**: Find ChIP-seq, ATAC-seq, Hi-C experiments from ENCODE and 4DN
5. **Enhancer/Promoter Cataloging**: Identify and characterize cis-regulatory elements using SCREEN
6. **Chromatin Conformation**: 3D genome organization from 4D Nucleome Hi-C data
7. **Epigenetic Profiling**: Histone modification patterns, DNA methylation, chromatin accessibility

---

## KEY PRINCIPLES

1. **Report-first approach** - Create report file FIRST, then populate progressively
2. **Tool parameter verification** - Verify params via `get_tool_info` before calling unfamiliar tools
3. **Evidence grading** - Grade all regulatory findings by evidence strength (T1-T4)
4. **Citation requirements** - Every finding must have inline source attribution (database, experiment ID)
5. **Mandatory completeness** - All sections must exist with data minimums or explicit "No data" notes
6. **Gene disambiguation first** - Resolve gene symbol/coordinates before analysis
7. **Cell-type context** - Always note cell type specificity of regulatory data
8. **Negative results documented** - "No enhancers found in region" is data; empty sections are failures
9. **English-first queries** - Always use English gene names and standard nomenclature in tool calls

---

## Evidence Grading System (MANDATORY)

Grade every regulatory finding by evidence strength:

| Tier | Symbol | Criteria | Examples |
|------|--------|----------|----------|
| **T1** | [T1] | Direct experimental validation, functional assay | CRISPR-validated enhancer, reporter assay, luciferase |
| **T2** | [T2] | High-quality experimental data, curated | ENCODE ChIP-seq peak, SCREEN cCRE, ReMap binding site |
| **T3** | [T3] | Computational prediction, motif match | JASPAR motif score, RegulomeDB score, Ensembl regulatory prediction |
| **T4** | [T4] | Association, text-mined, low confidence | Literature mention, low-score motif match, inferred regulation |

---

## Core Strategy: 7 Research Dimensions

```
Gene / Region / Variant Query
|
+-- PHASE 0: Gene/Region Resolution (ALWAYS FIRST)
|   +-- Resolve gene symbol -> Ensembl ID, coordinates, aliases
|   +-- Define genomic region of interest (+/- 500kb flanking)
|
+-- PHASE 1: Cis-Regulatory Elements (SCREEN)
|   +-- Candidate enhancers, promoters, insulators
|   +-- cCRE activity by cell type
|   +-- CTCF binding sites
|
+-- PHASE 2: Transcription Factor Binding
|   +-- JASPAR: TF binding motifs and PWMs
|   +-- ReMap: ChIP-seq validated TF binding sites
|   +-- ENCODE: TF ChIP-seq experiments
|
+-- PHASE 3: Regulatory Variant Scoring
|   +-- RegulomeDB: Variant regulatory evidence score
|   +-- Functional annotations from multiple data types
|
+-- PHASE 4: ENCODE Functional Genomics
|   +-- Histone modification ChIP-seq
|   +-- ATAC-seq / DNase-seq accessibility
|   +-- RNA-seq expression context
|   +-- Available experiments and datasets
|
+-- PHASE 5: Chromatin Conformation (4D Nucleome)
|   +-- Hi-C contact maps
|   +-- TAD boundaries
|   +-- Chromatin loops and compartments
|
+-- PHASE 6: Ensembl Regulatory Annotation
|   +-- Regulatory build features
|   +-- Promoter/enhancer/CTCF site annotations
|   +-- Activity states across cell types
|
+-- SYNTHESIS: Integrated Regulatory Model
    +-- Aggregate regulatory evidence
    +-- Build gene regulation model
    +-- Identify key regulatory elements and TFs
    +-- Data gaps and experimental recommendations
```

---

## Phase 0: Gene/Region Resolution (ALWAYS FIRST)

**CRITICAL**: Resolve gene identity and genomic coordinates before any analysis.

### Input Types Handled

| Input Format | Resolution Strategy |
|-------------|---------------------|
| Gene symbol (e.g., "BRCA1") | Ensembl lookup -> coordinates, Ensembl ID |
| Genomic region (e.g., "chr17:43044295-43170245") | Use directly; identify overlapping genes |
| Ensembl ID (e.g., "ENSG00000012048") | Ensembl lookup -> symbol, coordinates |
| rsID (e.g., "rs12345") | RegulomeDB/Ensembl -> coordinates, nearby genes |

### Resolution Tools

| Tool | Purpose | Parameters |
|------|---------|------------|
| `ensembl_lookup_gene` | Gene symbol to Ensembl ID + coordinates | `id`: str, `species`: str |
| `HGNC_get_gene_info` | Official gene symbol, aliases | `symbol`: str |
| `ensembl_get_xrefs` | Cross-references to external databases | `id`: str |

### Disambiguation Output

```markdown
## Gene Identity

| Property | Value |
|----------|-------|
| **Gene Symbol** | TP53 |
| **Ensembl ID** | ENSG00000141510 |
| **Chromosome** | 17 |
| **Start** | 7661779 |
| **End** | 7687550 |
| **Strand** | - |
| **Region of Interest** | 17:7161779-8187550 (+/- 500kb) |
| **Aliases** | p53, TRP53, LFS1 |
```

---

## Phase 1: Cis-Regulatory Elements (SCREEN)

**When**: Gene name or genomic region available

**Objective**: Catalog candidate cis-regulatory elements (cCREs) from the ENCODE SCREEN database

### Tools Used

| Tool | Function | Parameters |
|------|----------|------------|
| `SCREEN_get_regulatory_elements` | Get cCREs for a gene | `gene_name`: str, `element_type`: str, `limit`: int |

### Workflow

1. Query enhancers: `SCREEN_get_regulatory_elements(gene_name=gene, element_type="enhancer", limit=20)`
2. Query promoters: `SCREEN_get_regulatory_elements(gene_name=gene, element_type="promoter", limit=20)`
3. Query insulators: `SCREEN_get_regulatory_elements(gene_name=gene, element_type="insulator", limit=10)`
4. For each element: extract coordinates, activity scores, cell type specificity

### Decision Logic

- **Multiple element types**: Always query enhancers AND promoters (insulators optional)
- **Empty results**: Some genes have fewer regulatory elements; note counts
- **Cell type specificity**: SCREEN data is cell-type annotated; report top active cell types
- **All findings graded [T2]**: SCREEN cCREs are experimentally derived from ENCODE data

### Output Format

```markdown
### Cis-Regulatory Elements (SCREEN) [T2]

#### Enhancers (15 found)
| Element ID | Coordinates | Activity Score | Top Cell Types |
|-----------|-------------|---------------|----------------|
| EH38E1234567 | chr17:7650000-7651000 | 0.95 | HepG2, K562 |
| ... | ... | ... | ... |

#### Promoters (3 found)
| Element ID | Coordinates | Activity Score | Top Cell Types |
|-----------|-------------|---------------|----------------|
| EH38E9876543 | chr17:7687000-7688000 | 0.99 | Ubiquitous |
| ... | ... | ... | ... |

#### Insulators (2 found)
| Element ID | Coordinates | CTCF Binding |
|-----------|-------------|-------------|
| EH38E5555555 | chr17:7700000-7701000 | Yes |
```

---

## Phase 2: Transcription Factor Binding

**When**: Gene symbol available

**Objective**: Identify transcription factors that regulate the gene through motif analysis and ChIP-seq binding data

### Tools Used

#### JASPAR - TF Binding Motifs
| Tool | Function | Parameters |
|------|----------|------------|
| `jaspar_search_matrices` | Search TF binding motifs | `search`: str, `collection`: str, `tax_group`: str, `species`: str |
| `jaspar_get_matrix` | Get PWM for specific TF | `matrix_id`: str |
| `JASPAR_get_transcription_factors` | List TFs in collection | `collection`: str, `page`: int, `page_size`: int |

#### ReMap - Validated TF Binding Sites
| Tool | Function | Parameters |
|------|----------|------------|
| `ReMap_get_transcription_factor_binding` | Get TF binding sites near gene | `gene_name`: str, `cell_type`: str, `limit`: int |

#### ENCODE - ChIP-seq Experiments
| Tool | Function | Parameters |
|------|----------|------------|
| `ENCODE_search_experiments` | Search TF ChIP-seq experiments | `assay_title`: str, `target`: str, `organism`: str, `limit`: int |

### Workflow

1. **JASPAR motif search**: Search for known TF binding motifs
   - `jaspar_search_matrices(search=gene_symbol, collection="CORE", species="9606")`
   - If gene IS a TF: get its PWM binding motif
   - If gene is NOT a TF: identify TFs known to bind its promoter
2. **ReMap binding data**: Get experimentally validated TF binding sites
   - `ReMap_get_transcription_factor_binding(gene_name=gene, cell_type="HepG2", limit=20)`
   - Try multiple cell types: "HepG2", "K562", "MCF-7", "GM12878"
3. **ENCODE ChIP-seq**: Find available ChIP-seq experiments for key TFs
   - `ENCODE_search_experiments(assay_title="ChIP-seq", target=top_tf, organism="Homo sapiens", limit=5)`

### Decision Logic

- **Gene is a TF**: Show its binding motif (JASPAR PWM) + target genes + ENCODE ChIP-seq experiments
- **Gene is NOT a TF**: Show TFs that bind its promoter/enhancers (ReMap) + relevant motifs
- **Multiple cell types for ReMap**: Query at least 2-3 common cell types
- **JASPAR grades [T3]**: Motif predictions are computational
- **ReMap grades [T2]**: Based on experimental ChIP-seq data
- **ENCODE grades [T2]**: Direct experimental data

### Output Format

```markdown
### Transcription Factor Binding

#### JASPAR Binding Motifs [T3]
| Matrix ID | TF Name | Score | Sequence Logo |
|-----------|---------|-------|---------------|
| MA0106.3 | TP53 | 0.92 | RRRCWWGYYY |
| ... | ... | ... | ... |

#### ReMap ChIP-seq Validated Binding [T2]
| Transcription Factor | Cell Type | Binding Score | Coordinates |
|---------------------|-----------|--------------|-------------|
| SP1 | HepG2 | 850 | chr17:7687200-7687500 |
| CTCF | K562 | 920 | chr17:7700100-7700400 |
| ... | ... | ... | ... |

#### ENCODE ChIP-seq Experiments Available [T2]
| Experiment | Target | Cell Type | Files | Status |
|-----------|--------|-----------|-------|--------|
| ENCSR000BNT | TP53 | HepG2 | 12 | released |
| ... | ... | ... | ... | ... |
```

---

## Phase 3: Regulatory Variant Scoring

**When**: rsID or variant provided, OR gene has known regulatory variants

**Objective**: Assess the regulatory impact of genetic variants in the region

### Tools Used

| Tool | Function | Parameters |
|------|----------|------------|
| `RegulomeDB_query_variant` | Get regulatory evidence score for variant | `rsid`: str |

### Workflow

1. If rsID provided: Query RegulomeDB directly
   - `RegulomeDB_query_variant(rsid=rsid)`
2. Parse RegulomeDB score (1a-7): lower = more regulatory evidence
3. Extract supporting evidence types (eQTL, TF binding, chromatin state, etc.)
4. Cross-reference with SCREEN and ENCODE data from other phases

### RegulomeDB Score Interpretation

| Score | Meaning | Evidence Level |
|-------|---------|---------------|
| 1a | eQTL + TF binding + DNase + motif | Very likely regulatory [T2] |
| 1b | eQTL + TF binding + DNase | Likely regulatory [T2] |
| 1c | eQTL + TF binding + motif | Likely regulatory [T2] |
| 1d | eQTL + TF binding | Likely regulatory [T2] |
| 1e | eQTL + DNase | Likely regulatory [T3] |
| 1f | eQTL only | Possible regulatory [T3] |
| 2a-2c | TF binding + DNase/motif | Likely affects TF binding [T3] |
| 3a-3b | DNase or ChIP-seq evidence | Some evidence [T3] |
| 4-7 | Minimal or no evidence | Limited evidence [T4] |

### Decision Logic

- **Score 1a-1d**: Flag as likely functional regulatory variant; high confidence
- **Score 2a-3b**: Moderate evidence; recommend experimental validation
- **Score 4-7**: Low regulatory evidence; likely benign regulatory impact
- **No rsID provided**: Skip this phase gracefully; note "no variant specified"

### Output Format

```markdown
### Regulatory Variant Impact [T2/T3]

| Variant | RegulomeDB Score | Interpretation | Evidence Types |
|---------|-----------------|---------------|----------------|
| rs12345 | 1b | Likely regulatory | eQTL, TF binding, DNase |
| rs67890 | 3a | Some evidence | DNase peak |
```

---

## Phase 4: ENCODE Functional Genomics

**When**: Gene or region available

**Objective**: Discover functional genomics experiments and datasets from ENCODE

### Tools Used

| Tool | Function | Parameters |
|------|----------|------------|
| `ENCODE_search_experiments` | Search experiments by assay/target | `assay_title`, `target`, `organism`, `status`, `limit` |
| `ENCODE_get_experiment` | Get detailed experiment metadata | `accession`: str |
| `ENCODE_list_files` | List available data files | `file_type`, `assay_title`, `limit` |
| `ENCODE_search_biosamples` | Search available cell types | `organism`, `biosample_type`, `treatment`, `limit` |

### Workflow

1. **Histone marks**: Search for H3K4me3 (promoter), H3K27ac (enhancer), H3K4me1 (enhancer), H3K27me3 (repressive)
   - `ENCODE_search_experiments(assay_title="ChIP-seq", target="H3K27ac", organism="Homo sapiens", limit=5)`
2. **Chromatin accessibility**: Search ATAC-seq and DNase-seq
   - `ENCODE_search_experiments(assay_title="ATAC-seq", organism="Homo sapiens", limit=5)`
3. **If gene is a TF**: Search for ChIP-seq of that TF
   - `ENCODE_search_experiments(assay_title="ChIP-seq", target=gene, organism="Homo sapiens", limit=5)`
4. **RNA-seq context**: Search for expression experiments
   - `ENCODE_search_experiments(assay_title="RNA-seq", organism="Homo sapiens", limit=5)`

### Decision Logic

- **Prioritize by relevance**: Histone marks and accessibility most informative for regulatory analysis
- **Cell type matching**: When possible, focus on cell types relevant to user's question
- **Experiment quality**: Prefer "released" status and recent experiments
- **Data volume**: ENCODE has thousands of experiments; limit results and highlight most relevant
- **All ENCODE data graded [T2]**: High-quality experimental data

### Output Format

```markdown
### ENCODE Functional Genomics [T2]

#### Histone Modification Experiments
| Experiment | Mark | Cell Type | Status | Files |
|-----------|------|-----------|--------|-------|
| ENCSR000AKP | H3K27ac | HepG2 | released | 8 |
| ENCSR000ALA | H3K4me3 | K562 | released | 6 |

#### Chromatin Accessibility
| Experiment | Assay | Cell Type | Status |
|-----------|-------|-----------|--------|
| ENCSR889WQX | ATAC-seq | GM12878 | released |

#### TF ChIP-seq (for [gene] if TF)
| Experiment | Target | Cell Type | Status |
|-----------|--------|-----------|--------|
| ENCSR000BNT | TP53 | HepG2 | released |
```

---

## Phase 5: Chromatin Conformation (4D Nucleome)

**When**: Gene or region available

**Objective**: Explore 3D genome organization data from the 4D Nucleome project

### Tools Used

| Tool | Function | Parameters |
|------|----------|------------|
| `FourDN_search_data` | Search Hi-C data | `operation`: "search_data", `assay_title`, `biosource_name`, `limit` |
| `FourDN_get_experiment_metadata` | Get experiment details | `operation`: "get_experiment_metadata", `experiment_accession`: str |

### Workflow

1. Search Hi-C experiments: `FourDN_search_data(operation="search_data", assay_title="Hi-C", limit=10)`
2. Search Micro-C data: `FourDN_search_data(operation="search_data", assay_title="Micro-C", limit=5)`
3. For relevant experiments: get metadata for top results
4. Note available cell types and data types

### Decision Logic

- **IMPORTANT: 4DN tools require `operation` parameter** - This is a SOAP-style tool
- **Hi-C vs Micro-C**: Micro-C has higher resolution for local interactions
- **Cell type matching**: Note which cell types have chromatin data
- **Data availability**: 4DN may not cover all cell types of interest
- **Grade [T2]**: High-quality experimental chromatin conformation data

### Output Format

```markdown
### Chromatin Conformation (4D Nucleome) [T2]

#### Available Hi-C Datasets
| Experiment | Cell Type | Assay | Resolution | Status |
|-----------|-----------|-------|-----------|--------|
| 4DNESXXXXXXX | H1-hESC | Hi-C | 10kb | released |
| 4DNESYYYYYYY | GM12878 | Micro-C | 1kb | released |

#### Chromatin Organization Context
- **TAD**: Gene located within TAD spanning chr17:7.1-8.2Mb
- **Compartment**: A compartment (active)
- **Nearby CTCF sites**: 3 CTCF sites within 100kb (from SCREEN Phase 1)
```

---

## Phase 6: Ensembl Regulatory Annotation

**When**: Genomic region coordinates available

**Objective**: Get regulatory feature annotations from the Ensembl Regulatory Build

### Tools Used

| Tool | Function | Parameters |
|------|----------|------------|
| `ensembl_get_regulatory_features` | Get regulatory features in region | `region`: str (chr:start-end), `feature`: str, `species`: str |

### Workflow

1. Get regulatory features: `ensembl_get_regulatory_features(region="17:7661779-7687550", feature="regulatory", species="human")`
2. Parse feature types: promoter, enhancer, CTCF_binding_site, TF_binding_site, open_chromatin_region
3. Note activity states across cell types when available

### Decision Logic

- **Region format**: Use chromosome:start-end without "chr" prefix
- **Feature parameter**: Must be "regulatory" for this endpoint
- **Cross-reference with SCREEN**: Compare Ensembl regulatory build with SCREEN cCREs
- **Grade [T3]**: Ensembl regulatory build is computationally derived

### Output Format

```markdown
### Ensembl Regulatory Build [T3]

| Feature ID | Type | Coordinates | Activity State |
|-----------|------|-------------|----------------|
| ENSR00000123456 | Promoter | 17:7687200-7688000 | Active (most cell types) |
| ENSR00000789012 | Enhancer | 17:7650000-7651500 | Active (liver, lung) |
| ENSR00000345678 | CTCF_binding_site | 17:7700000-7700500 | Active |
```

---

## Synthesis: Integrated Regulatory Model (MANDATORY)

**Always the final section**. Integrates all evidence into a coherent regulatory model.

### Synthesis Template

```markdown
## Integrated Regulatory Model

### Regulatory Architecture Summary

**Gene**: [GENE] ([Ensembl ID])
**Region analyzed**: [coordinates] ([size]kb)

### Key Regulatory Elements
1. **Proximal promoter** [T2/T3]: Located at [coords], active in [cell types]
   - TFs binding: SP1, CTCF, [others from ReMap]
   - Histone marks: H3K4me3 (ENCODE), H3K27ac (ENCODE)
   - SCREEN cCRE: [element ID]

2. **Distal enhancer 1** [T2]: Located at [coords], [distance] from TSS
   - Active in [cell types] (SCREEN)
   - TF binding: [TFs from ReMap/ENCODE]
   - Hi-C contact with promoter: [Yes/No/Unknown]

3. **CTCF insulator** [T2]: Located at [coords]
   - Defines TAD boundary
   - CTCF motif score: [from JASPAR]

### Transcription Factor Regulatory Network
| TF | Binding Evidence | Motif Match | Cell Types | Role |
|----|-----------------|-------------|-----------|------|
| SP1 | ReMap ChIP-seq [T2] | JASPAR 0.92 [T3] | HepG2, K562 | Activator |
| CTCF | ENCODE ChIP-seq [T2] | JASPAR 0.98 [T3] | Ubiquitous | Insulator |

### Regulatory Variants (if applicable)
| Variant | RegulomeDB Score | Regulatory Impact | Affected Element |
|---------|-----------------|-------------------|-----------------|
| rs12345 | 1b | Disrupts SP1 binding | Proximal promoter |

### Evidence Quality Assessment
| Dimension | Data Available | Evidence Tier | Confidence |
|-----------|---------------|--------------|------------|
| cCREs (SCREEN) | 15 enhancers, 3 promoters | [T2] | High |
| TF Binding (ReMap) | 8 TFs validated | [T2] | High |
| Motifs (JASPAR) | 12 motif matches | [T3] | Medium |
| ENCODE experiments | 25 relevant datasets | [T2] | High |
| Chromatin (4DN) | Hi-C in 3 cell types | [T2] | Medium |
| Regulatory Build | 5 features annotated | [T3] | Medium |

### Data Gaps
- [ ] No single-cell ATAC-seq data available for this region
- [ ] Chromatin conformation data limited to 3 cell types
- [ ] No CRISPR-validated enhancers (would be needed for [T1])
- [ ] Regulatory variant impact is predictive (needs experimental validation)

### Experimental Recommendations
1. **Validate key enhancers**: CRISPR deletion or reporter assays for top 3 enhancers
2. **Confirm TF binding**: ChIP-qPCR for SP1, CTCF at predicted sites
3. **Test regulatory variants**: Allele-specific reporter assays for rs12345
```

---

## Mandatory Completeness Checklist

Before finalizing any report, verify:

- [ ] **Phase 0**: Gene/region fully resolved (symbol, Ensembl ID, coordinates)
- [ ] **Phase 1**: SCREEN queried for enhancers AND promoters (counts reported)
- [ ] **Phase 2**: At least 2 TF data sources queried (JASPAR + ReMap or ENCODE)
- [ ] **Phase 3**: RegulomeDB queried for variants OR "no variant specified" noted
- [ ] **Phase 4**: At least 2 ENCODE assay types searched (histone marks + accessibility)
- [ ] **Phase 5**: 4DN queried for Hi-C/Micro-C data OR "no chromatin data" noted
- [ ] **Phase 6**: Ensembl regulatory build queried OR "no regulatory features" noted
- [ ] **Synthesis**: Regulatory model provided with element catalog and TF network
- [ ] **Evidence Grading**: All findings have [T1]-[T4] annotations
- [ ] **Cell-type context**: Cell type specificity noted for all binding/activity data
- [ ] **Data gaps**: Explicitly listed in synthesis section

---

## Tool Parameter Reference

**Critical Parameter Notes** (verified from source code):

| Tool | Parameter Name | Type | Notes |
|------|---------------|------|-------|
| `SCREEN_get_regulatory_elements` | `gene_name`, `element_type`, `limit` | str, str, int | element_type: "enhancer", "promoter", "insulator" |
| `ReMap_get_transcription_factor_binding` | `gene_name`, `cell_type`, `limit` | str, str, int | cell_type default: "HepG2" |
| `RegulomeDB_query_variant` | `rsid` | str | rsID format (e.g., "rs12345") |
| `jaspar_search_matrices` | `search`, `name`, `collection`, `tax_group`, `species` | str (all optional) | species="9606" for human |
| `jaspar_get_matrix` | `matrix_id` | str | JASPAR matrix ID (e.g., "MA0106.3") |
| `JASPAR_get_transcription_factors` | `collection`, `page`, `page_size` | str, int, int | collection="CORE" default |
| `ENCODE_search_experiments` | `assay_title`, `target`, `organism`, `status`, `limit` | str (all optional) | status="released" default |
| `ENCODE_get_experiment` | `accession` | str | ENCODE accession (e.g., "ENCSR000BNT") |
| `ENCODE_list_files` | `file_type`, `assay_title`, `limit` | str, str, int | All optional |
| `ENCODE_search_biosamples` | `organism`, `biosample_type`, `treatment`, `limit` | str (all optional) | |
| `FourDN_search_data` | `operation`, `query`, `item_type`, `assay_title`, `biosource_name`, `limit` | **operation REQUIRED** | operation="search_data" |
| `FourDN_get_experiment_metadata` | `operation`, `experiment_accession` | **operation REQUIRED** | operation="get_experiment_metadata" |
| `ensembl_get_regulatory_features` | `region`, `feature`, `species` | str, str, str | feature="regulatory", region="17:start-end" |

### CRITICAL: SOAP-style Tools

The following tools require an `operation` parameter:
- **FourDN_search_data**: `operation="search_data"`
- **FourDN_get_experiment_metadata**: `operation="get_experiment_metadata"`
- **FourDN_get_file_metadata**: `operation="get_file_metadata"`
- **FourDN_get_download_url**: `operation="get_download_url"`

### Response Format Notes (verified from testing)

- **SCREEN**: Returns dict with `@context`, `@graph`, `@id`, `@type`, `all` keys (JSON-LD format)
- **ReMap**: Returns dict with TF binding records
- **RegulomeDB**: Returns `{status, data, url}` with regulatory score and evidence in `data`
- **JASPAR search**: Returns `{count, next, previous, results}` with matrix objects in `results`
- **JASPAR get_matrix**: Returns dict with matrix details (name, PFM, sequence logo)
- **ENCODE**: Returns dict with experiment/file objects (structure varies by endpoint)
- **4DN**: Returns dict with search results
- **Ensembl**: Returns `{status, data, url, content_type}` with regulatory features in `data`

---

## Fallback Strategies

### Regulatory Elements
- **Primary**: SCREEN cCREs by gene name
- **Fallback**: Ensembl Regulatory Build by coordinates
- **If both empty**: Note "limited regulatory annotation in this region"

### TF Binding
- **Primary**: ReMap binding sites + JASPAR motifs
- **Fallback**: ENCODE ChIP-seq experiments
- **If all empty**: Gene may have limited TF binding data; note and continue

### Chromatin Data
- **Primary**: 4DN Hi-C experiments
- **Fallback**: ENCODE Hi-C experiments
- **If empty**: Note "no chromatin conformation data available for this region"

### Variant Scoring
- **Primary**: RegulomeDB for rsID
- **Fallback**: SCREEN + ENCODE overlap analysis at variant position
- **If no variant**: Skip gracefully

---

## Common Use Patterns

### Pattern 1: Gene-Centric Regulatory Landscape
```
Input: Gene symbol (e.g., "TP53")
Workflow: All phases (0-6 + Synthesis)
Output: Complete regulatory atlas for the gene locus
```

### Pattern 2: Transcription Factor Target Analysis
```
Input: TF name (e.g., "CTCF")
Workflow: Phase 0 -> Phase 2 (JASPAR motif + ENCODE ChIP-seq) -> Phase 1 (target gene cCREs)
Output: TF binding motif, genome-wide binding data, target gene catalog
```

### Pattern 3: Non-Coding Variant Interpretation
```
Input: rsID (e.g., "rs6983267")
Workflow: Phase 0 -> Phase 3 (RegulomeDB) -> Phase 1 (nearby cCREs) -> Phase 2 (TF binding) -> Synthesis
Output: Regulatory impact assessment with functional context
```

### Pattern 4: Cell-Type Specific Regulation
```
Input: Gene + cell type (e.g., "MYC in HepG2")
Workflow: Phase 0 -> Phase 1 (SCREEN) -> Phase 2 (ReMap in HepG2) -> Phase 4 (ENCODE in HepG2)
Output: Cell-type specific regulatory landscape
```

### Pattern 5: Epigenetic Data Discovery
```
Input: Histone mark or assay type (e.g., "H3K27ac ChIP-seq in liver")
Workflow: Phase 4 (ENCODE search) -> Phase 5 (4DN chromatin) -> Summary
Output: Available datasets and download information
```

---

## Limitations & Known Issues

### Database-Specific
- **SCREEN**: Limited to ENCODE-defined cCREs; may miss tissue-specific regulatory elements
- **JASPAR**: Motif predictions have false positive rate; binding =/= function
- **ReMap**: Coverage varies by TF and cell type; ~1000 TFs covered
- **RegulomeDB**: Scoring based on available data; novel variants may lack evidence
- **ENCODE**: Primarily human and mouse; limited other organisms
- **4DN**: Focused on chromatin conformation; limited cell type coverage
- **Ensembl**: Regulatory build is computationally predicted; may miss novel elements

### Analysis
- **Cell-type specificity**: Regulatory elements are highly cell-type specific; data from one cell type may not generalize
- **Functional validation gap**: Most findings are [T2]-[T3]; [T1] validation requires experimental follow-up
- **Non-coding complexity**: Regulatory mechanisms are complex; catalog does not capture all interactions
- **3D genome**: TAD and loop data available for limited cell types

### Technical
- **4DN operation parameter**: Must include `operation` for all 4DN tools (SOAP-style)
- **Region format**: Ensembl uses "17:start-end" (no "chr" prefix); SCREEN/ENCODE may use "chr17:start-end"
- **Large gene loci**: Genes spanning >1Mb may require multiple queries

---

## Summary

**Epigenomics & Gene Regulation Skill** provides comprehensive regulatory landscape analysis by integrating:

1. **Cis-regulatory elements** (SCREEN) - Enhancers, promoters, insulators from ENCODE cCRE catalog
2. **Transcription factor binding** (JASPAR + ReMap + ENCODE) - Motifs, validated binding sites, ChIP-seq data
3. **Regulatory variant scoring** (RegulomeDB) - Evidence-based variant regulatory impact
4. **Functional genomics** (ENCODE) - Histone marks, chromatin accessibility, expression
5. **Chromatin conformation** (4D Nucleome) - Hi-C, TADs, chromatin loops
6. **Regulatory annotation** (Ensembl) - Computational regulatory build features

**Outputs**: Structured markdown report with regulatory element catalog, TF network, variant scoring, and integrated regulatory model

**Best for**: Gene regulation analysis, non-coding variant interpretation, enhancer/promoter identification, TF binding profiling, epigenetic data discovery

**Total tools integrated**: 21 tools across 7 databases
