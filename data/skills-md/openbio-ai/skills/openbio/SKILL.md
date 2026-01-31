---
name: openbio
description: >
  OpenBio API for biological data access and computational biology tools.
  Use when: (1) Querying biological databases (PDB, UniProt, ChEMBL, etc.),
  (2) Searching scientific literature (PubMed, bioRxiv, arXiv),
  (3) Running structure prediction (Boltz, Chai, ProteinMPNN),
  (4) Performing pathway/enrichment analysis,
  (5) Designing molecular biology experiments (primers, cloning),
  (6) Analyzing variants and clinical data.
metadata:
  tags: [biology, protein, genomics, chemistry, bioinformatics, drug-discovery]
---

## Installation

```bash
bunx skills add https://github.com/openbio-ai/skills --skill openbio
```

## Authentication

**Required**: `OPENBIO_API_KEY` environment variable.

```bash
export OPENBIO_API_KEY=your_key_here
```

**Base URL**: `https://openbio-api.fly.dev/`

## Quick Start

```bash
# List available tools
curl -X GET "https://openbio-api.fly.dev/api/v1/tools" \
  -H "X-API-Key: $OPENBIO_API_KEY"

# Get tool schema (always do this first!)
curl -X GET "https://openbio-api.fly.dev/api/v1/tools/{tool_name}" \
  -H "X-API-Key: $OPENBIO_API_KEY"

# Invoke tool
curl -X POST "https://openbio-api.fly.dev/api/v1/tools" \
  -H "X-API-Key: $OPENBIO_API_KEY" \
  -F "tool_name=search_pubmed" \
  -F 'params={"query": "CRISPR", "max_results": 5}'
```

## Decision Tree: Which Tools to Use

```
What do you need?
│
├─ Protein/structure data?
│   └─ Read rules/protein-structure.md
│       → PDB, AlphaFold, UniProt tools
│
├─ Literature search?
│   └─ Read rules/literature.md
│       → PubMed, arXiv, bioRxiv, OpenAlex
│
├─ Genomics/variants?
│   └─ Read rules/genomics.md
│       → Ensembl, GWAS, VEP, GEO
│
├─ Small molecule analysis?
│   └─ Read rules/cheminformatics.md
│       → RDKit, PubChem, ChEMBL
│
├─ Cloning/PCR/assembly?
│   └─ Read rules/molecular-biology.md
│       → Primers, restriction, Gibson, Golden Gate
│
├─ Structure prediction/design?
│   └─ Read rules/structure-prediction.md
│       → Boltz, Chai, ProteinMPNN, LigandMPNN
│
├─ Pathway analysis?
│   └─ Read rules/pathway-analysis.md
│       → KEGG, Reactome, STRING
│
└─ Clinical/drug data?
    └─ Read rules/clinical-data.md
        → ClinicalTrials, ClinVar, FDA, Open Targets
```

## Critical Rules

### 1. Always Check Tool Schema First
```bash
# Before invoking ANY tool:
curl -X GET "https://openbio-api.fly.dev/api/v1/tools/{tool_name}" \
  -H "X-API-Key: $OPENBIO_API_KEY"
```
Parameter names vary (e.g., `pdb_ids` not `pdb_id`). Check schema to avoid errors.

### 2. Long-Running Jobs (submit_* tools)
Prediction tools return a `job_id`. Poll for completion:
```bash
# Check status
curl -X GET "https://openbio-api.fly.dev/api/v1/jobs/{job_id}/status" \
  -H "X-API-Key: $OPENBIO_API_KEY"

# Get results with download URLs
curl -X GET "https://openbio-api.fly.dev/api/v1/jobs/{job_id}" \
  -H "X-API-Key: $OPENBIO_API_KEY"
```

### 3. Quality Thresholds
Don't just retrieve data—interpret it:

**AlphaFold pLDDT**: > 70 = confident, < 50 = disordered
**Experimental resolution**: < 2.5 Å for binding sites
**GWAS p-value**: < 5×10⁻⁸ = genome-wide significant
**Tanimoto similarity**: > 0.7 = similar compounds

See individual rule files for detailed thresholds.

## Rule Files

Read these for domain-specific knowledge:

### Core API
| File | Description |
|------|-------------|
| [rules/api.md](rules/api.md) | Core endpoints, authentication, job management |

### Data Access Tools
| File | Tools Covered |
|------|---------------|
| [rules/protein-structure.md](rules/protein-structure.md) | PDB, PDBe, AlphaFold, UniProt |
| [rules/literature.md](rules/literature.md) | PubMed, arXiv, bioRxiv, OpenAlex |
| [rules/genomics.md](rules/genomics.md) | Ensembl, ENA, Gene, GWAS, GEO |
| [rules/cheminformatics.md](rules/cheminformatics.md) | RDKit, PubChem, ChEMBL |
| [rules/molecular-biology.md](rules/molecular-biology.md) | Primers, PCR, restriction, assembly |
| [rules/pathway-analysis.md](rules/pathway-analysis.md) | KEGG, Reactome, STRING |
| [rules/clinical-data.md](rules/clinical-data.md) | ClinicalTrials, ClinVar, FDA |

### ML Prediction Tools (Detailed)
| File | Tool | Use Case |
|------|------|----------|
| [rules/structure-prediction.md](rules/structure-prediction.md) | **Index** | Decision tree for all prediction tools |
| [rules/boltz.md](rules/boltz.md) | Boltz-2 | Structure + binding affinity |
| [rules/chai.md](rules/chai.md) | Chai-1 | Multi-modal (protein+ligand+RNA+glycan) |
| [rules/simplefold.md](rules/simplefold.md) | SimpleFold | Quick single-protein folding |
| [rules/proteinmpnn.md](rules/proteinmpnn.md) | ProteinMPNN | Fixed-backbone sequence design |
| [rules/ligandmpnn.md](rules/ligandmpnn.md) | LigandMPNN | Ligand-aware sequence design |
| [rules/thermompnn.md](rules/thermompnn.md) | ThermoMPNN | Stability (ΔΔG) prediction |
| [rules/geodock.md](rules/geodock.md) | GeoDock | Protein-protein docking |
| [rules/pinal.md](rules/pinal.md) | Pinal | De novo design from text |
| [rules/boltzgen.md](rules/boltzgen.md) | BoltzGen | End-to-end binder design |

## Tool Categories Summary

| Category | Count | Examples |
|----------|-------|----------|
| Protein structure | 23 | fetch_pdb_metadata, get_alphafold_prediction |
| Literature | 14 | search_pubmed, arxiv_search, biorxiv_search_keywords |
| Genomics | 27 | lookup_gene, vep_predict, search_gwas_associations_by_trait |
| Cheminformatics | 20+ | calculate_molecular_properties, chembl_similarity_search |
| Molecular biology | 15 | design_primers, restriction_digest, assemble_gibson |
| Structure prediction | 15+ | submit_boltz_prediction, submit_proteinmpnn_prediction |
| Pathway analysis | 24 | analyze_gene_list, get_string_network |
| Clinical data | 22 | search_clinical_trials, search_clinvar |

## Common Mistakes

1. **Not checking schemas** → Parameter errors
2. **Ignoring quality metrics** → Using unreliable data
3. **Wrong tool for task** → Check decision trees in rule files
4. **Not polling jobs** → Missing prediction results

---

**Tip**: When in doubt, search for tools: `GET /api/v1/tools/search?q=your_query`
