---
name: rdkit
description: Python cheminformatics library for molecular manipulation and analysis. Parse SMILES/SDF/MOL formats, compute descriptors (MW, LogP, TPSA), generate fingerprints (Morgan, MACCS), perform substructure queries with SMARTS, create 2D/3D geometries, calculate similarity, and run chemical reactions.
---

# RDKit: Python Cheminformatics Library

## Summary

RDKit (v2023+) provides comprehensive Python APIs for molecular structure manipulation, property calculation, and chemical informatics. It requires Python 3 and NumPy, offering modular components for molecule parsing, descriptors, fingerprints, substructure search, conformer generation, and reaction processing.

## Applicable Scenarios

This skill applies when you need to:

| Task Category | Examples |
|---------------|----------|
| Molecule I/O | Parse SMILES, MOL, SDF, InChI; write structures |
| Property Calculation | Molecular weight, LogP, TPSA, H-bond donors/acceptors |
| Fingerprinting | Morgan (ECFP), MACCS keys, atom pairs, topological |
| Similarity Analysis | Tanimoto, Dice, clustering compounds |
| Substructure Search | SMARTS patterns, functional group detection |
| 3D Conformers | Generate, optimize, align molecular geometries |
| Chemical Reactions | Define and execute transformations |
| Drug-Likeness | Lipinski rules, QED, lead-likeness filters |
| Visualization | 2D depictions, highlighting, grid images |

## Module Organization

| Module | Purpose | Reference |
|--------|---------|-----------|
| rdkit.Chem | Core molecule parsing, serialization, substructure | `references/api-reference.md` |
| rdkit.Chem.Descriptors | Property calculations | `references/descriptors-reference.md` |
| rdkit.Chem.rdFingerprintGenerator | Modern fingerprint API | `references/api-reference.md` |
| rdkit.DataStructs | Similarity metrics, bulk operations | `references/api-reference.md` |
| rdkit.Chem.AllChem | 3D coordinates, reactions, optimization | `references/api-reference.md` |
| rdkit.Chem.Draw | Visualization and depiction | `references/api-reference.md` |
| SMARTS patterns | Substructure query language | `references/smarts-patterns.md` |

## Setup

Install via pip or conda:

```bash
# Conda (recommended)
conda install -c conda-forge rdkit

# Pip
pip install rdkit-pypi
```

Standard imports:

```python
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors, Draw
from rdkit import DataStructs
```

## Quick Reference

### Parse and Validate Molecules

```python
from rdkit import Chem

mol = Chem.MolFromSmiles('c1ccc(O)cc1')
if mol is None:
    print("Invalid SMILES")
```

### Compute Properties

```python
from rdkit.Chem import Descriptors

mw = Descriptors.MolWt(mol)
logp = Descriptors.MolLogP(mol)
tpsa = Descriptors.TPSA(mol)
```

### Generate Fingerprints

```python
from rdkit.Chem import rdFingerprintGenerator

gen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
fp = gen.GetFingerprint(mol)
```

### Similarity Search

```python
from rdkit import DataStructs

similarity = DataStructs.TanimotoSimilarity(fp1, fp2)
```

### Substructure Match

```python
pattern = Chem.MolFromSmarts('[OH1][C]')  # Alcohol
has_alcohol = mol.HasSubstructMatch(pattern)
```

### Generate 3D Conformer

```python
from rdkit.Chem import AllChem

mol = Chem.AddHs(mol)
AllChem.EmbedMolecule(mol, randomSeed=42)
AllChem.MMFFOptimizeMolecule(mol)
```

## Implementation Patterns

### Drug-Likeness Assessment

```python
from rdkit import Chem
from rdkit.Chem import Descriptors

def assess_druglikeness(smiles: str) -> dict | None:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None

    mw = Descriptors.MolWt(mol)
    logp = Descriptors.MolLogP(mol)
    hbd = Descriptors.NumHDonors(mol)
    hba = Descriptors.NumHAcceptors(mol)

    return {
        'MW': mw,
        'LogP': logp,
        'HBD': hbd,
        'HBA': hba,
        'TPSA': Descriptors.TPSA(mol),
        'RotBonds': Descriptors.NumRotatableBonds(mol),
        'Lipinski': mw <= 500 and logp <= 5 and hbd <= 5 and hba <= 10,
        'QED': Descriptors.qed(mol)
    }
```

### Batch Similarity Search

```python
from rdkit import Chem, DataStructs
from rdkit.Chem import rdFingerprintGenerator

def find_similar(query_smiles: str, database: list[str], threshold: float = 0.7) -> list:
    query = Chem.MolFromSmiles(query_smiles)
    if query is None:
        return []

    gen = rdFingerprintGenerator.GetMorganGenerator(radius=2)
    query_fp = gen.GetFingerprint(query)

    hits = []
    for idx, smi in enumerate(database):
        mol = Chem.MolFromSmiles(smi)
        if mol:
            fp = gen.GetFingerprint(mol)
            sim = DataStructs.TanimotoSimilarity(query_fp, fp)
            if sim >= threshold:
                hits.append((idx, smi, sim))

    return sorted(hits, key=lambda x: x[2], reverse=True)
```

### Functional Group Screening

```python
from rdkit import Chem

FUNCTIONAL_GROUPS = {
    'alcohol': '[OH1][C]',
    'amine': '[NH2,NH1][C]',
    'carboxylic_acid': 'C(=O)[OH1]',
    'amide': 'C(=O)N',
    'ester': 'C(=O)O[C]',
    'nitro': '[N+](=O)[O-]'
}

def detect_functional_groups(smiles: str) -> list[str]:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return []

    found = []
    for name, smarts in FUNCTIONAL_GROUPS.items():
        pattern = Chem.MolFromSmarts(smarts)
        if mol.HasSubstructMatch(pattern):
            found.append(name)
    return found
```

### Conformer Generation with Clustering

```python
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.ML.Cluster import Butina

def generate_diverse_conformers(smiles: str, n_confs: int = 50, rmsd_thresh: float = 0.5) -> list:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return []

    mol = Chem.AddHs(mol)
    conf_ids = AllChem.EmbedMultipleConfs(mol, numConfs=n_confs, randomSeed=42)

    # Optimize all conformers
    for cid in conf_ids:
        AllChem.MMFFOptimizeMolecule(mol, confId=cid)

    # Cluster by RMSD to get diverse set
    if len(conf_ids) < 2:
        return list(conf_ids)

    dists = []
    for i in range(len(conf_ids)):
        for j in range(i):
            rmsd = AllChem.GetConformerRMS(mol, conf_ids[j], conf_ids[i])
            dists.append(rmsd)

    clusters = Butina.ClusterData(dists, len(conf_ids), rmsd_thresh, isDistData=True)
    return [conf_ids[c[0]] for c in clusters]  # Cluster centroids
```

### Batch Processing SDF Files

```python
from rdkit import Chem
from rdkit.Chem import Descriptors

def process_sdf(input_path: str, output_path: str, min_mw: float = 200, max_mw: float = 500):
    """Filter compounds by molecular weight and add property columns."""
    supplier = Chem.SDMolSupplier(input_path)
    writer = Chem.SDWriter(output_path)

    for mol in supplier:
        if mol is None:
            continue

        mw = Descriptors.MolWt(mol)
        if not (min_mw <= mw <= max_mw):
            continue

        # Add computed properties
        mol.SetProp('MW', f'{mw:.2f}')
        mol.SetProp('LogP', f'{Descriptors.MolLogP(mol):.2f}')
        mol.SetProp('TPSA', f'{Descriptors.TPSA(mol):.2f}')

        writer.write(mol)

    writer.close()
```

## Guidelines

**Always validate parsed molecules:**

```python
mol = Chem.MolFromSmiles(smiles)
if mol is None:
    print(f"Parse failed: {smiles}")
    continue
```

**Use bulk operations for performance:**

```python
fps = [gen.GetFingerprint(m) for m in mols]
sims = DataStructs.BulkTanimotoSimilarity(fps[0], fps[1:])
```

**Add hydrogens for 3D work:**

```python
mol = Chem.AddHs(mol)  # Required before EmbedMolecule
AllChem.EmbedMolecule(mol)
```

**Stream large files:**

```python
# Memory-efficient: process one at a time
for mol in Chem.ForwardSDMolSupplier(file_handle):
    if mol:
        process(mol)

# Avoid: loading entire file
all_mols = list(Chem.SDMolSupplier('huge.sdf'))
```

**Thread safety:** Most operations are thread-safe except for concurrent access to MolSupplier objects.

## Troubleshooting

| Issue | Resolution |
|-------|------------|
| `MolFromSmiles` returns `None` | Invalid SMILES syntax; check input |
| Sanitization error | Use `Chem.DetectChemistryProblems(mol)` to diagnose |
| Wrong 3D geometry | Call `AddHs(mol)` before embedding |
| Fingerprint size mismatch | Use same `fpSize` parameter for all comparisons |
| SMARTS not matching | Check aromatic vs aliphatic atoms (`c` vs `C`) |
| Slow SDF processing | Use `ForwardSDMolSupplier` or `MultithreadedSDMolSupplier` |
| Memory issues with large files | Stream with `ForwardSDMolSupplier`, don't load all |

## Reference Documentation

Each reference file contains detailed API documentation:

| File | Contents |
|------|----------|
| `references/api-reference.md` | Complete function/class listings by module |
| `references/descriptors-reference.md` | All molecular descriptors with examples |
| `references/smarts-patterns.md` | Common SMARTS patterns for substructure search |

## External Resources

- RDKit Documentation: https://www.rdkit.org/docs/
- Getting Started Guide: https://www.rdkit.org/docs/GettingStartedInPython.html
- GitHub Repository: https://github.com/rdkit/rdkit
- Cookbook: https://www.rdkit.org/docs/Cookbook.html
