---
name: alphafold-database
description: Query and retrieve AI-predicted protein structures from DeepMind's AlphaFold database. Fetch structures via UniProt accession, interpret pLDDT/PAE confidence scores, and access bulk proteome data for structural biology workflows.
---

# AlphaFold Database

Programmatic access to DeepMind's AlphaFold Protein Structure Database (200M+ predicted structures).

## Quick Reference

```python
# Fetch structure via Biopython
from Bio.PDB import alphafold_db
predictions = list(alphafold_db.get_predictions("P00520"))
alphafold_db.download_cif_for(predictions[0], directory="./output")

# Direct API call
import requests
resp = requests.get("https://alphafold.ebi.ac.uk/api/prediction/P00520")
entry_id = resp.json()[0]['entryId']  # AF-P00520-F1

# Download structure file
structure_url = f"https://alphafold.ebi.ac.uk/files/{entry_id}-model_v4.cif"
```

## When to Use

- Obtain 3D coordinates for proteins without experimental structures
- Assess prediction quality via pLDDT and PAE metrics
- Download structure files (mmCIF, PDB) for visualization or docking
- Retrieve proteome-scale datasets for computational analysis

## Key Concepts

| Term | Description |
|------|-------------|
| **UniProt Accession** | Protein identifier (e.g., `P00520`) used to query |
| **AlphaFold ID** | Format: `AF-{UniProt}-F{fragment}` (e.g., `AF-P00520-F1`) |
| **pLDDT** | Per-residue confidence (0-100); >90 = reliable, <50 = disordered |
| **PAE** | Predicted Aligned Error; <5A = high confidence domain positions |

See `references/confidence-scores.md` for detailed interpretation guidance.

## File Types

| File | URL Pattern | Contents |
|------|-------------|----------|
| Coordinates | `{id}-model_v4.cif` | Atomic positions (mmCIF) |
| Confidence | `{id}-confidence_v4.json` | Per-residue pLDDT array |
| PAE Matrix | `{id}-predicted_aligned_error_v4.json` | Inter-residue error |

Base URL: `https://alphafold.ebi.ac.uk/files/`

## Core Operations

### Fetch Structure Metadata
```python
import requests
resp = requests.get(f"https://alphafold.ebi.ac.uk/api/prediction/{uniprot_id}")
metadata = resp.json()[0]
af_id = metadata['entryId']
```

### Download All Files
Use `scripts/alphafold_utils.py`:
```python
from scripts.alphafold_utils import download_alphafold_files
paths = download_alphafold_files("AF-P04637-F1", output_dir="./data")
```

### Analyze Confidence
```python
from scripts.alphafold_utils import get_plddt_scores
stats = get_plddt_scores("AF-P04637-F1")
print(f"Average pLDDT: {stats['mean']:.1f}")
```

### Bulk Proteome Access
```bash
# Google Cloud Storage
gsutil ls gs://public-datasets-deepmind-alphafold-v4/
gsutil -m cp "gs://public-datasets-deepmind-alphafold-v4/proteomes/proteome-tax_id-9606-*.tar" ./
```

See `references/bulk-access.md` for BigQuery queries and batch processing.

## Caveats

- **Predictions, not experiments**: Verify critical findings experimentally
- **Confidence matters**: Always check pLDDT before using regions
- **Single chains only**: No multimers or complexes
- **No ligands**: Missing cofactors, ions, PTMs

## Setup

```bash
pip install biopython requests numpy matplotlib pandas scipy
# Optional: pip install google-cloud-bigquery gsutil
```

## Links

- Database: https://alphafold.ebi.ac.uk/
- API Docs: https://alphafold.ebi.ac.uk/api-docs
- Biopython: https://biopython.org/docs/dev/api/Bio.PDB.alphafold_db.html
