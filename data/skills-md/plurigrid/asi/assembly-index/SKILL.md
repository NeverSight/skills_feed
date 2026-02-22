---
name: assembly-index
description: Lee Cronin's Assembly Theory for molecular complexity measurement and
  life detection via assembly index computation.
license: UNLICENSED
metadata:
  trit: 1
  source: local
---

# Assembly Index Skill: Molecular Complexity Validation

**Status**: ✅ Production Ready
**Trit**: -1 (MINUS - validator/constraint)
**Color**: #2626D8 (Blue)
**Principle**: Complexity threshold → Life signature
**Frame**: Assembly pathways with minimal step counting

---

## Overview

**Assembly Index** measures molecular complexity by counting the minimum number of joining operations needed to construct a molecule from basic building blocks. Molecules with assembly index > 15 are biosignatures—too complex for random chemistry.

1. **Assembly pathway**: Shortest construction sequence
2. **Copy number threshold**: Abundance × complexity = life signal
3. **Molecular DAG**: Directed acyclic graph of substructures
4. **Mass spectrometry integration**: MA(m/z) measurement

## Core Formula

```
MA(molecule) = min |steps| to construct from primitives
Life threshold: MA > 15 with copy_number > 1
```

```python
def assembly_index(molecule: Molecule) -> int:
    """Compute minimum assembly steps via dynamic programming."""
    substructures = enumerate_substructures(molecule)
    dag = build_assembly_dag(substructures)
    return shortest_path_length(dag, source="primitives", target=molecule)
```

## Key Concepts

### 1. Assembly Pathway Enumeration

```python
class AssemblyPathway:
    def __init__(self, molecule):
        self.mol = molecule
        self.fragments = self.decompose()
    
    def decompose(self) -> list[Fragment]:
        """Find all valid bond-breaking decompositions."""
        return [split for split in self.mol.bonds 
                if split.yields_valid_fragments()]
    
    def minimal_pathway(self) -> list[JoinOperation]:
        """DP over fragment DAG for minimum steps."""
        memo = {}
        return self._dp_assemble(self.mol, memo)
```

### 2. Copy Number Amplification

```python
def is_biosignature(molecule, sample) -> bool:
    ma = assembly_index(molecule)
    copies = sample.count(molecule)
    # Life creates copies of complex molecules
    return ma > 15 and copies > 1
```

### 3. Tandem Mass Spectrometry Integration

```python
def ma_from_ms2(spectrum: MS2Spectrum) -> float:
    """Estimate assembly index from fragmentation pattern."""
    fragments = spectrum.peaks
    dag = reconstruct_assembly_dag(fragments)
    return dag.longest_path()
```

## Commands

```bash
# Compute assembly index
just assembly-index molecule.sdf

# Validate biosignature threshold
just assembly-validate sample.ms2

# Compare assembly pathways
just assembly-compare mol1.sdf mol2.sdf
```

## Integration with GF(3) Triads

```
assembly-index (-1) ⊗ turing-chemputer (0) ⊗ crn-topology (+1) = 0 ✓  [Molecular Complexity]
```

## Related Skills

- **turing-chemputer** (0): Execute chemical synthesis programs
- **crn-topology** (+1): Generate reaction network topologies
- **kolmogorov-compression** (-1): Algorithmic complexity baseline

---

**Skill Name**: assembly-index
**Type**: Complexity Validator
**Trit**: -1 (MINUS)
**Color**: #2626D8 (Blue)
