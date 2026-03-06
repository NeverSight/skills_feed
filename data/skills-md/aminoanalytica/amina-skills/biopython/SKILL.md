---
name: biopython
description: Python toolkit for computational biology. Use when asked to "parse FASTA", "read GenBank", "query NCBI", "run BLAST", "analyze protein structure", "build phylogenetic tree", or work with biological sequences. Handles sequence I/O, database access, alignments, structure analysis, and phylogenetics.
---

# Biopython: Python Tools for Computational Biology

## Summary

Biopython (v1.85+) delivers a comprehensive Python library for biological data analysis. It requires Python 3 and NumPy, providing modular components for sequences, alignments, database access, BLAST, structures, and phylogenetics.

## Applicable Scenarios

This skill applies when you need to:

| Task Category | Examples |
|---------------|----------|
| Sequence Operations | Create, modify, translate DNA/RNA/protein sequences |
| File Format Handling | Parse or convert FASTA, GenBank, FASTQ, PDB, mmCIF |
| NCBI Database Access | Query GenBank, PubMed, Protein, Gene, Taxonomy |
| Similarity Searches | Execute BLAST locally or via NCBI, parse results |
| Alignment Work | Pairwise or multiple sequence alignments |
| Structural Analysis | Parse PDB files, compute distances, DSSP assignment |
| Tree Construction | Build, manipulate, visualize phylogenetic trees |
| Motif Discovery | Find and score sequence patterns |
| Sequence Statistics | GC content, molecular weight, melting temperature |

## Module Organization

| Module | Purpose | Reference |
|--------|---------|-----------|
| Bio.Seq / Bio.SeqIO | Sequence objects and file I/O | `references/sequence-io.md` |
| Bio.Align / Bio.AlignIO | Pairwise and multiple alignments | `references/alignment.md` |
| Bio.Entrez | NCBI database programmatic access | `references/databases.md` |
| Bio.Blast | BLAST execution and result parsing | `references/blast.md` |
| Bio.PDB | 3D structure manipulation | `references/structure.md` |
| Bio.Phylo | Phylogenetic tree operations | `references/phylogenetics.md` |
| Bio.motifs, Bio.SeqUtils, etc. | Motifs, utilities, restriction sites | `references/advanced.md` |

## Setup

Install via pip:

```python
uv pip install biopython
```

Configure NCBI access (mandatory for Entrez operations):

```python
from Bio import Entrez

Entrez.email = "researcher@institution.edu"
Entrez.api_key = "your_ncbi_api_key"  # Optional: increases rate limit to 10 req/s
```

## Quick Reference

### Parse Sequences

```python
from Bio import SeqIO

records = SeqIO.parse("data.fasta", "fasta")
for rec in records:
    print(f"{rec.id}: {len(rec)} bp")
```

### Translate DNA

```python
from Bio.Seq import Seq

dna = Seq("ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG")
protein = dna.translate()
```

### Query NCBI

```python
from Bio import Entrez

Entrez.email = "researcher@institution.edu"
handle = Entrez.esearch(db="nucleotide", term="insulin[Gene] AND human[Organism]")
results = Entrez.read(handle)
handle.close()
```

### Run BLAST

```python
from Bio.Blast import NCBIWWW, NCBIXML

result = NCBIWWW.qblast("blastp", "swissprot", "MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNLSGAEKAVQVKVKALPDAQFEVVHSLAKWKRQQIAAALEHHHHHH")
record = NCBIXML.read(result)
```

### Parse Protein Structure

```python
from Bio.PDB import PDBParser

parser = PDBParser(QUIET=True)
structure = parser.get_structure("protein", "structure.pdb")
for atom in structure.get_atoms():
    print(atom.name, atom.coord)
```

### Build Phylogenetic Tree

```python
from Bio import AlignIO, Phylo
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor

alignment = AlignIO.read("aligned.fasta", "fasta")
calc = DistanceCalculator("identity")
dm = calc.get_distance(alignment)
tree = DistanceTreeConstructor().nj(dm)
Phylo.draw_ascii(tree)
```

## Reference Files

| File | Contents |
|------|----------|
| `references/sequence-io.md` | Bio.Seq objects, SeqIO parsing/writing, large file handling, format conversion |
| `references/alignment.md` | Pairwise alignment, BLOSUM matrices, AlignIO, external aligners |
| `references/databases.md` | NCBI Entrez API, esearch/efetch/elink, batch downloads, search syntax |
| `references/blast.md` | Remote/local BLAST, XML parsing, result filtering, batch queries |
| `references/structure.md` | Bio.PDB, SMCRA hierarchy, DSSP, superimposition, spatial queries |
| `references/phylogenetics.md` | Tree I/O, distance matrices, tree construction, consensus, visualization |
| `references/advanced.md` | Motifs, SeqUtils, restriction enzymes, population genetics, GenomeDiagram |

## Implementation Patterns

### Retrieve and Analyze GenBank Record

```python
from Bio import Entrez, SeqIO
from Bio.SeqUtils import gc_fraction

Entrez.email = "researcher@institution.edu"

handle = Entrez.efetch(db="nucleotide", id="NM_001301717", rettype="gb", retmode="text")
record = SeqIO.read(handle, "genbank")
handle.close()

print(f"Organism: {record.annotations['organism']}")
print(f"Length: {len(record)} bp")
print(f"GC: {gc_fraction(record.seq):.1%}")
```

### Batch Sequence Processing

```python
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction

output_records = []
for record in SeqIO.parse("input.fasta", "fasta"):
    if len(record) >= 200 and gc_fraction(record.seq) > 0.4:
        output_records.append(record)

SeqIO.write(output_records, "filtered.fasta", "fasta")
```

### BLAST with Result Filtering

```python
from Bio.Blast import NCBIWWW, NCBIXML

query = "MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSH"
result_handle = NCBIWWW.qblast("blastp", "nr", query, hitlist_size=20)
record = NCBIXML.read(result_handle)

for alignment in record.alignments:
    for hsp in alignment.hsps:
        if hsp.expect < 1e-10:
            identity_pct = (hsp.identities / hsp.align_length) * 100
            print(f"{alignment.accession}: {identity_pct:.1f}% identity, E={hsp.expect:.2e}")
```

### Phylogeny from Alignment

```python
from Bio import AlignIO, Phylo
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
import matplotlib.pyplot as plt

alignment = AlignIO.read("sequences.aln", "clustal")
calculator = DistanceCalculator("blosum62")
dm = calculator.get_distance(alignment)

constructor = DistanceTreeConstructor()
tree = constructor.nj(dm)
tree.root_at_midpoint()
tree.ladderize()

fig, ax = plt.subplots(figsize=(12, 8))
Phylo.draw(tree, axes=ax)
fig.savefig("phylogeny.png", dpi=150)
```

## Guidelines

**Imports**: Use explicit imports
```python
from Bio import SeqIO, Entrez
from Bio.Seq import Seq
```

**File Handling**: Always close handles or use context managers
```python
with open("sequences.fasta") as f:
    for record in SeqIO.parse(f, "fasta"):
        process(record)
```

**Memory Efficiency**: Use iterators for large datasets
```python
# Correct: iterate without loading all
for record in SeqIO.parse("huge.fasta", "fasta"):
    if meets_criteria(record):
        yield record

# Avoid: loading entire file
all_records = list(SeqIO.parse("huge.fasta", "fasta"))
```

**Error Handling**: Wrap network operations
```python
from urllib.error import HTTPError

try:
    handle = Entrez.efetch(db="nucleotide", id=accession)
    record = SeqIO.read(handle, "genbank")
except HTTPError as e:
    print(f"Fetch failed: {e.code}")
```

**NCBI Compliance**: Set email, respect rate limits, cache downloads locally

## Troubleshooting

| Issue | Resolution |
|-------|------------|
| "No handlers could be found for logger 'Bio.Entrez'" | Set `Entrez.email` before any queries |
| HTTP 400 from NCBI | Verify accession/ID format is correct |
| "ValueError: EOF" during parse | Confirm file format matches format string |
| Alignment length mismatch | Sequences must be pre-aligned for AlignIO |
| Slow BLAST queries | Use local BLAST for large-scale searches |
| PDB parser warnings | Use `PDBParser(QUIET=True)` or check structure quality |

## External Resources

- Biopython Documentation: https://biopython.org/docs/latest/
- Biopython Tutorial: https://biopython.org/docs/latest/Tutorial/
- GitHub Repository: https://github.com/biopython/biopython
