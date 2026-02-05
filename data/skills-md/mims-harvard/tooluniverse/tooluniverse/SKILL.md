---
name: tooluniverse
description: General strategies for using ToolUniverse effectively with 10000+ scientific tools. Covers tool discovery, multi-hop queries, comprehensive research workflows, disambiguation, evidence grading, and report generation. Use when users need to research any scientific topic, find biological data, explore drug/target/disease relationships, or need guidance on how to use ToolUniverse tools wisely.
---

# ToolUniverse General Usage Strategies

Master strategies for using ToolUniverse's 10000+ scientific tools effectively. These principles apply regardless of how you access ToolUniverse (MCP server, SDK, or direct tool calls).

## Core Philosophy

**ToolUniverse has MANY tools** - the challenge is discovering and using them effectively:

1. **Search widely** - Don't assume you know all relevant tools; always search for more
2. **Query multiple databases** - Cross-reference data across sources
3. **Multi-hop persistence** - Many answers require 3-5 tool calls in sequence
4. **Never give up easily** - If one tool fails, try alternatives
5. **Comprehensive reports** - Use all available data; detail is valuable

---

## Strategy 1: Exhaustive Tool Discovery

**CRITICAL**: ToolUniverse has 10000+ tools. Before any research task, search for ALL relevant tools.

### Tool Discovery Methods

Use the tool finder tools to discover what's available:

| Method | Tool | Best For |
|--------|------|----------|
| **Keyword** | `Tool_Finder_Keyword` | Fast search by terms |
| **LLM-based** | `Tool_Finder_LLM` | Intelligent matching by description |
| **Embedding** | `Tool_Finder` | Semantic similarity search |

### Discovery Best Practices

| Practice | Why | Example |
|----------|-----|---------|
| **Search with multiple terms** | Same data from different angles | "protein expression", "gene expression", "tissue expression" |
| **Search by database name** | Find all tools for a source | "UniProt", "ChEMBL", "OpenTargets" |
| **Search by data type** | Comprehensive coverage | "variant", "mutation", "SNP", "polymorphism" |
| **Search by use case** | Task-oriented discovery | "druggability", "target validation" |

### Minimum Discovery Queries

Before any research task, run at least these searches:

1. **Main topic query**: `[your topic]`
2. **Related terms**: `[synonym1]`, `[synonym2]`  
3. **Database-specific**: `[relevant database names]`
4. **Data type specific**: `[required data types]`

**Example for target research**:
- "protein information"
- "gene expression" 
- "drug target"
- "UniProt", "OpenTargets"
- "protein interaction"
- "variant mutation"

---

## Strategy 2: Multi-Hop Tool Chains

**CRITICAL**: Most scientific questions require multiple tool calls. A single tool rarely gives the complete answer.

### Why Multi-Hop Matters

| Question Type | Single Tool Answer | Multi-Hop Answer |
|---------------|-------------------|------------------|
| "Tell me about EGFR" | Basic protein info | Full profile with structure, expression, drugs, variants, literature |
| "What drugs target TP53?" | List of drug names | Drug details, mechanisms, clinical trials, bioactivity data |
| "Research Alzheimer's" | Disease definition | Genes, pathways, drugs, trials, phenotypes, GWAS, literature |

### Common Multi-Hop Patterns

#### Pattern A: ID Resolution Chain
```
Name → ID → Data → Related Data

Example: Gene name to complete profile
1. gene_name → Ensembl ID
2. Ensembl ID → UniProt accession  
3. UniProt accession → Protein entry
4. UniProt accession → Domains
5. UniProt accession → Structure
```

#### Pattern B: Cross-Database Enrichment
```
Primary Data → Cross-reference → Enriched View

Example: Drug compound enrichment
1. drug_name → PubChem CID
2. drug_name → ChEMBL ID
3. CID → properties
4. ChEMBL ID → bioactivity
5. ChEMBL ID → targets
6. SMILES → ADMET predictions
```

#### Pattern C: Network Expansion
```
Seed Entity → Connected Entities → Entity Details

Example: Target interaction network
1. gene → protein interactions
2. For each interactor → gene info
3. Interactor → disease associations
```

#### Pattern D: Literature + Data Integration
```
Database Annotations → Literature Evidence → Synthesis

Example: Disease mechanism research
1. disease → associated genes
2. disease → phenotypes
3. disease → drugs
4. disease → literature
5. key papers → citations
```

### Multi-Hop Persistence Rules

1. **Don't stop at first result** - One tool gives partial data; keep going
2. **Follow cross-references** - Use IDs from one tool to query others
3. **Chain until complete** - 5-10 tool calls for comprehensive answers is normal
4. **Track all IDs** - Save every identifier for potential future use

---

## Strategy 3: Query Multiple Databases for Same Data

**CRITICAL**: Different databases have different coverage. Query ALL relevant sources.

### Database Redundancy Principle

For any data type, query multiple sources:

| Data Type | Primary | Secondary | Tertiary |
|-----------|---------|-----------|----------|
| **Protein info** | UniProt | Proteins API | NCBI Protein |
| **Gene expression** | GTEx | Human Protein Atlas | ArrayExpress |
| **Drug targets** | ChEMBL | DGIdb | OpenTargets |
| **Variants** | gnomAD | ClinVar | OpenTargets |
| **Literature** | PubMed | Europe PMC | OpenAlex |
| **Pathways** | Reactome | KEGG | WikiPathways |
| **Structures** | RCSB PDB | PDBe | AlphaFold |
| **Disease associations** | OpenTargets | ClinVar | GWAS Catalog |

### Merge Results Strategy

When querying multiple databases:
1. **Collect all results** - Don't stop at first success
2. **Note data source** - Track where each datum came from
3. **Handle conflicts** - Document when sources disagree
4. **Prefer curated** - Weight RefSeq over GenBank, UniProt over predictions

---

## Strategy 4: Disambiguation First

**CRITICAL**: Before any research, resolve entity identity to avoid wrong data and missed results.

### Why Disambiguation Matters

| Problem | Example | Consequence |
|---------|---------|-------------|
| **Naming collision** | "JAK" = Janus kinase OR "just another kinase" | Wrong papers retrieved |
| **Multiple IDs** | Gene has symbol, Ensembl, Entrez, UniProt IDs | Miss data in some databases |
| **Salt forms** | Metformin vs metformin HCl (different CIDs) | Incomplete compound data |
| **Species ambiguity** | BRCA1 in human vs mouse | Wrong expression/function data |

### Disambiguation Workflow

```
Step 1: Establish Canonical IDs
    gene_name → UniProt, Ensembl, NCBI Gene, ChEMBL target
    compound_name → PubChem CID, ChEMBL ID, SMILES
    disease_name → EFO ID, ICD-10, UMLS CUI

Step 2: Gather Synonyms
    All aliases, alternative names, historical names
    
Step 3: Detect Naming Collisions
    Search "[TERM]"[Title] → check if results are on-topic
    Build negative filters: NOT [collision_term]
    
Step 4: Species Confirmation
    Verify organism is correct (default: Homo sapiens)
```

### ID Types by Entity

**Genes/Proteins:**
- Gene Symbol (EGFR, TP53)
- UniProt accession (P00533)
- Ensembl ID (ENSG00000146648)
- NCBI Gene ID (1956)
- ChEMBL Target ID (CHEMBL203)

**Compounds:**
- PubChem CID (2244)
- ChEMBL ID (CHEMBL25)
- SMILES string
- InChI/InChIKey

**Diseases:**
- EFO ID (EFO_0000249)
- ICD-10 code (G30)
- UMLS CUI (C0002395)
- SNOMED CT

---

## Strategy 5: Never Give Up on Search

**CRITICAL**: When a tool fails or returns empty, don't give up. Try alternatives.

### Failure Handling Protocol

```
Attempt 1: Primary tool
    ↓ fails
Wait briefly, then retry
    ↓ fails
Try fallback tool #1
    ↓ fails
Try fallback tool #2
    ↓ fails
Document as "unavailable" with reason
```

### Common Fallback Chains

| Primary Tool | Fallback Options |
|--------------|------------------|
| PubMed citations | EuropePMC citations → OpenAlex citations |
| GTEx expression | Human Protein Atlas expression |
| PubChem compound lookup | ChEMBL search → SMILES-based lookup |
| ChEMBL bioactivity | PubChem bioactivity summary |
| DailyMed drug labels | PubChem drug label info |
| UniProt protein entry | Proteins API |

### Alternative Search Strategies

**If keyword search fails:**
- Try synonyms and aliases
- Use broader/narrower terms
- Try different databases

**If database is empty:**
- Query related databases
- Use literature to find mentions
- Check if entity exists under different name

**If API rate-limited:**
- Wait and retry
- Try same query on different database
- Use cached results if available

---

## Strategy 6: Generate Comprehensive Reports

**CRITICAL**: With access to many tools, reports should be detailed and thorough.

### Report-First Approach

1. **Create report structure FIRST** - Define all sections before gathering data
2. **Progressively update** - Fill sections as data is gathered
3. **Show findings, not process** - Report results, not search methodology

### Citation Requirements

**Every fact must have a source:**

```
## Protein Function

EGFR is a receptor tyrosine kinase that regulates cell growth.
*Source: UniProt (P00533)*

### Expression Profile
| Tissue | TPM | Source |
|--------|-----|--------|
| Skin | 156.3 | GTEx |
| Lung | 98.4 | GTEx |
```

### Evidence Grading

Grade claims by evidence strength:

| Tier | Symbol | Description | Example |
|------|--------|-------------|---------|
| **T1** | ★★★ | Mechanistic with direct evidence | CRISPR KO study |
| **T2** | ★★☆ | Functional study | siRNA knockdown |
| **T3** | ★☆☆ | Association/screen hit | GWAS, high-throughput screen |
| **T4** | ☆☆☆ | Review mention, text-mined | Review article |

**In report:**
```
ATP6V1A drives lysosomal acidification [★★★: PMID:12345678].
It has been implicated in cancer metabolism [★☆☆: TCGA data].
```

### Mandatory Completeness

All sections must exist, even if "data unavailable":

```
## Pathogen Involvement
No pathogen interactions identified in literature or databases.
*Source: Literature search, UniProt annotations*
```

### Report Quality Metrics

| Quality | Description | Tool Calls | Sections |
|---------|-------------|------------|----------|
| **Excellent** | Multi-database, evidence-graded | 30+ | All mandatory, detailed |
| **Good** | Cross-referenced, sourced | 15-30 | All mandatory, adequate |
| **Adequate** | Single-database focus | 5-15 | Core sections only |
| **Poor** | Single tool, no sources | <5 | Incomplete |

---

## Strategy 7: Use Specialized Skills for Specific Tasks

**CRITICAL**: For specific research tasks, use specialized skills (not this general skill).

### Task-Specific Skill Selection

| Task | Recommended Skill |
|------|-------------------|
| **Drug profiling** | `tooluniverse-drug-research` |
| **Target analysis** | `tooluniverse-target-research` |
| **Disease research** | `tooluniverse-disease-research` |
| **Literature review** | `tooluniverse-literature-deep-research` |
| **Protein structure** | `tooluniverse-protein-structure-retrieval` |
| **Sequence retrieval** | `tooluniverse-sequence-retrieval` |
| **Chemical compounds** | `tooluniverse-chemical-compound-retrieval` |
| **Expression data** | `tooluniverse-expression-data-retrieval` |

### When to Use This General Skill

Use this skill when:
- Need general guidance on ToolUniverse usage
- Task doesn't fit a specialized skill
- Need to combine multiple specialized workflows
- Exploring what's possible with ToolUniverse
- Learning ToolUniverse best practices

---

## Strategy 8: Parallel Execution for Speed

**CRITICAL**: Run independent queries simultaneously for faster research.

### When to Parallelize

| Parallel | Sequential |
|----------|------------|
| Different databases for same entity | Tool B needs output from Tool A |
| Multiple entities, same data type | Building an ID → using the ID |
| Independent research paths | Iterating through a list of results |

### Parallel Research Paths Example

For target research, run these 8 paths simultaneously:
1. **Identity** - Names, IDs, sequence
2. **Structure** - 3D structure, domains
3. **Function** - GO terms, pathways
4. **Interactions** - PPI network
5. **Expression** - Tissue expression
6. **Variants** - Genetic variation
7. **Drugs** - Known drugs, druggability
8. **Literature** - Publications, trends

---

## Strategy 9: Iterative Completeness Check

**CRITICAL**: After gathering data, always ask "What else is missing?" to ensure comprehensive coverage.

### The Completeness Loop

```
Gather initial data
    ↓
Review what you have
    ↓
Ask: "What aspects are still missing?"
    ↓
Identify gaps
    ↓
Search for tools to fill gaps
    ↓
Gather additional data
    ↓
Repeat until comprehensive
```

### Universal Completeness Questions

After each research phase, ask:

1. **Identity**: Do I have all relevant identifiers and names?
2. **Core data**: Do I have the fundamental information for this entity type?
3. **Context**: Do I have surrounding/related information?
4. **Relationships**: Do I know what this connects to?
5. **Variations**: Do I know about variants, forms, or subtypes?
6. **Evidence**: Do I have supporting data from multiple sources?
7. **Literature**: Do I have recent publications on this topic?
8. **Gaps**: Have I documented what's unavailable?

### Gap-Filling Strategies

| Gap Identified | Strategy |
|----------------|----------|
| Missing data type | Search for tools with that data type |
| Single source only | Query additional databases |
| Outdated information | Check literature for recent updates |
| No experimental data | Look for predictions/computational data |
| Conflicting data | Find authoritative/curated sources |
| Shallow coverage | Dive deeper with specialized tools |

### When to Stop

Stop the completeness loop when:
- All relevant aspects have been addressed (even if "not found")
- Multiple sources queried for key data
- Gaps are documented, not ignored
- No obvious missing pieces remain

### Self-Review Questions

Before finalizing any research:

- Have I searched for ALL relevant tools?
- Have I queried multiple databases?
- Have I followed cross-references?
- Have I checked recent literature?
- Have I documented what's unavailable?
- Is there any obvious gap I haven't addressed?
- Would someone reading this ask "but what about X?"

---

## Quick Reference: Tool Categories

### Protein & Gene Tools
UniProt, Proteins API, MyGene, Ensembl tools

### Structure Tools
RCSB PDB, PDBe, AlphaFold, InterPro tools

### Drug & Compound Tools
ChEMBL, PubChem, DGIdb, ADMET-AI, DrugBank tools

### Disease & Phenotype Tools
OpenTargets, ClinVar, GWAS, HPO tools

### Expression Tools
GTEx, Human Protein Atlas, CELLxGENE tools

### Variant Tools
gnomAD, ClinVar, dbSNP tools

### Pathway Tools
Reactome, KEGG, WikiPathways, GO tools

### Literature Tools
PubMed, EuropePMC, OpenAlex, SemanticScholar tools

### Clinical Tools
ClinicalTrials.gov, FAERS, PharmGKB, DailyMed tools

---

## Troubleshooting Common Issues

### "Tool not found"
- Search for similar tools using Tool_Finder
- Check spelling of tool name
- Try alternative tools for same data type

### "Empty results"
- Check spelling of query terms
- Try synonyms/aliases
- Try alternative databases
- Verify IDs are correct type

### "Conflicting data"
- Note all sources
- Prefer curated databases
- Document the conflict in report
- Use evidence grading

### "Incomplete picture"
- Search for more tools
- Query additional databases
- Follow cross-references
- Expand via literature

---

## Summary: The ToolUniverse Mindset

| Principle | Action |
|-----------|--------|
| **Search widely** | 10000+ tools; always discover more |
| **Multi-hop persistence** | 5-10 tool calls per question is normal |
| **Cross-reference** | Query multiple databases for same data |
| **Disambiguate first** | Resolve IDs before research |
| **Never give up** | Fallbacks for every failure |
| **Report comprehensively** | Detail with sources and evidence grades |
| **Use specialized skills** | Apply domain-specific skills for focused tasks |
| **Execute in parallel** | Speed through concurrent execution |
| **Check completeness** | Ask "what's missing?" and fill gaps iteratively |

**The goal: Transform 10000+ tools into comprehensive, reliable scientific intelligence.**
