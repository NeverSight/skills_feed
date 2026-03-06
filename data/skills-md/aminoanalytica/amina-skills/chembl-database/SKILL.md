---
name: chembl-database
description: Query the ChEMBL database for bioactive compounds, drug targets, and bioactivity data. Use this skill when searching for small molecules, finding inhibitors for protein targets, or analyzing drug mechanisms of action.
---

# ChEMBL Database

ChEMBL is the European Bioinformatics Institute's repository of bioactive compound data, containing over 2 million compounds, 19 million bioactivity measurements, and 13,000+ drug targets.

## Use Cases

- Find potent inhibitors for a protein target
- Search for compounds similar to a known drug
- Retrieve drug mechanism of action data
- Filter compounds by molecular properties (Lipinski, etc.)
- Export bioactivity data for ML or analysis

## Installation

```bash
uv pip install chembl_webresource_client
```

## Basic Usage

```python
from chembl_webresource_client.new_client import new_client

# Fetch compound by identifier
mol = new_client.molecule.get('CHEMBL192')

# Retrieve target data
tgt = new_client.target.get('CHEMBL203')

# Query activity measurements
acts = new_client.activity.filter(
    target_chembl_id='CHEMBL203',
    standard_type='IC50',
    standard_value__lte=50
)
```

## Available Endpoints

| Resource | Description |
|----------|-------------|
| `molecule` | Compound structures and properties |
| `target` | Biological targets |
| `activity` | Bioassay measurements |
| `assay` | Experimental protocols |
| `drug` | Approved drug data |
| `mechanism` | Drug mechanisms of action |
| `drug_indication` | Therapeutic indications |
| `similarity` | Structure similarity search |
| `substructure` | Substructure search |
| `document` | Literature references |
| `cell_line` | Cell line data |
| `protein_class` | Protein classifications |
| `image` | SVG molecular images |

## Query Operators

The client uses Django-style filtering:

| Operator | Function | Example |
|----------|----------|---------|
| `__exact` | Exact match | `pref_name__exact='Aspirin'` |
| `__icontains` | Case-insensitive substring | `pref_name__icontains='kinase'` |
| `__lte`, `__gte` | Less/greater than or equal | `standard_value__lte=10` |
| `__lt`, `__gt` | Less/greater than | `pchembl_value__gt=7` |
| `__range` | Value within range | `alogp__range=[-1, 5]` |
| `__in` | Value in list | `target_chembl_id__in=['CHEMBL203']` |
| `__isnull` | Null check | `pchembl_value__isnull=False` |
| `__startswith` | Prefix match | `pref_name__startswith='Proto'` |
| `__regex` | Regular expression | `pref_name__regex='^[A-Z]{3}'` |

## Common Workflows

### Find Target Inhibitors

```python
from chembl_webresource_client.new_client import new_client

activity = new_client.activity

# Get potent BRAF inhibitors (IC50 < 100 nM)
braf_hits = activity.filter(
    target_chembl_id='CHEMBL5145',
    standard_type='IC50',
    standard_value__lte=100,
    standard_units='nM'
)

for hit in braf_hits:
    print(f"{hit['molecule_chembl_id']}: {hit['standard_value']} nM")
```

### Search by Target Name

```python
from chembl_webresource_client.new_client import new_client

target = new_client.target
activity = new_client.activity

# Find CDK targets
cdk_targets = target.filter(
    pref_name__icontains='cyclin-dependent kinase',
    target_type='SINGLE PROTEIN'
)

target_ids = [t['target_chembl_id'] for t in cdk_targets]

# Get activities for these targets
cdk_activities = activity.filter(
    target_chembl_id__in=target_ids[:5],
    standard_type='IC50',
    standard_value__lte=100,
    standard_units='nM'
)
```

### Structure Similarity Search

```python
from chembl_webresource_client.new_client import new_client

sim = new_client.similarity

# Find molecules 80% similar to ibuprofen
ibuprofen_smiles = 'CC(C)Cc1ccc(cc1)C(C)C(=O)O'
matches = sim.filter(smiles=ibuprofen_smiles, similarity=80)

for m in matches:
    print(f"{m['molecule_chembl_id']}: {m['similarity']}%")
```

### Substructure Search

```python
from chembl_webresource_client.new_client import new_client

sub = new_client.substructure

# Find compounds with benzimidazole core
benzimidazole = 'c1ccc2[nH]cnc2c1'
compounds = sub.filter(smiles=benzimidazole)
```

### Filter by Molecular Properties

```python
from chembl_webresource_client.new_client import new_client

mol = new_client.molecule

# Lipinski-compliant fragments
fragments = mol.filter(
    molecule_properties__mw_freebase__lte=300,
    molecule_properties__alogp__lte=3,
    molecule_properties__hbd__lte=3,
    molecule_properties__hba__lte=3
)
```

### Drug Mechanisms of Action

```python
from chembl_webresource_client.new_client import new_client

mech = new_client.mechanism
drug_ind = new_client.drug_indication

# Get mechanism of metformin
metformin_id = 'CHEMBL1431'
mechanisms = mech.filter(molecule_chembl_id=metformin_id)

for m in mechanisms:
    print(f"Target: {m['target_chembl_id']}")
    print(f"Action: {m['action_type']}")

# Get approved indications
indications = drug_ind.filter(molecule_chembl_id=metformin_id)
```

### Generate Molecule Images

```python
from chembl_webresource_client.new_client import new_client

img = new_client.image

# Get SVG of caffeine
caffeine_svg = img.get('CHEMBL113')

with open('caffeine.svg', 'w') as f:
    f.write(caffeine_svg)
```

## Key Response Fields

### Molecule Properties

| Field | Description |
|-------|-------------|
| `molecule_chembl_id` | ChEMBL identifier |
| `pref_name` | Preferred name |
| `molecule_structures.canonical_smiles` | SMILES string |
| `molecule_structures.standard_inchi_key` | InChI key |
| `molecule_properties.mw_freebase` | Molecular weight |
| `molecule_properties.alogp` | Calculated LogP |
| `molecule_properties.hba` / `hbd` | H-bond acceptors/donors |
| `molecule_properties.psa` | Polar surface area |
| `molecule_properties.rtb` | Rotatable bonds |
| `molecule_properties.num_ro5_violations` | Lipinski violations |
| `molecule_properties.qed_weighted` | QED drug-likeness |

### Activity Fields

| Field | Description |
|-------|-------------|
| `molecule_chembl_id` | Compound ID |
| `target_chembl_id` | Target ID |
| `standard_type` | Measurement type (IC50, Ki, EC50) |
| `standard_value` | Numeric value |
| `standard_units` | Units (nM, uM) |
| `pchembl_value` | Normalized -log10 value |
| `data_validity_comment` | Quality flag |
| `potential_duplicate` | Duplicate indicator |

### Target Fields

| Field | Description |
|-------|-------------|
| `target_chembl_id` | ChEMBL target ID |
| `pref_name` | Preferred name |
| `target_type` | SINGLE PROTEIN, PROTEIN COMPLEX, etc. |
| `organism` | Species |

### Mechanism Fields

| Field | Description |
|-------|-------------|
| `molecule_chembl_id` | Drug ID |
| `target_chembl_id` | Target ID |
| `mechanism_of_action` | Description |
| `action_type` | INHIBITOR, AGONIST, ANTAGONIST, etc. |

## Export to DataFrame

```python
import pandas as pd
from chembl_webresource_client.new_client import new_client

activity = new_client.activity

results = activity.filter(
    target_chembl_id='CHEMBL279',
    standard_type='Ki',
    pchembl_value__isnull=False
)

df = pd.DataFrame(list(results))
df.to_csv('dopamine_d2_ligands.csv', index=False)
```

## Configuration

```python
from chembl_webresource_client.settings import Settings

cfg = Settings.Instance()

cfg.CACHING = True           # Enable response caching
cfg.CACHE_EXPIRE = 43200     # Cache TTL (12 hours)
cfg.TIMEOUT = 60             # Request timeout
cfg.TOTAL_RETRIES = 5        # Retry attempts
```

## Data Quality Notes

- ChEMBL data is manually curated but verify `data_validity_comment` fields
- Check `potential_duplicate` flags when aggregating results
- Use `pchembl_value` for normalized comparisons across assay types
- Activity values without `standard_units` should be used cautiously

## Best Practices

1. **Use caching** - Reduces API load and improves performance
2. **Filter early** - Apply filters to reduce data transfer
3. **Limit results** - Use `[:n]` slicing for testing
4. **Check validity** - Inspect `data_validity_comment` fields
5. **Use pchembl_value** - Normalized values enable cross-assay comparison
6. **Batch queries** - Use `__in` operator for multiple IDs

## Error Handling

```python
from chembl_webresource_client.new_client import new_client

mol = new_client.molecule

try:
    result = mol.get('INVALID_ID')
except Exception as e:
    if '404' in str(e):
        print("Compound not found")
    elif '503' in str(e):
        print("Service unavailable - retry later")
    else:
        raise
```

## External Links

- ChEMBL: https://www.ebi.ac.uk/chembl/
- API Documentation: https://chembl.gitbook.io/chembl-interface-documentation
- Python Client: https://github.com/chembl/chembl_webresource_client
