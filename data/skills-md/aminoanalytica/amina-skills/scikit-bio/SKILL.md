---
name: scikit-bio
description: Python bioinformatics library for sequence manipulation, alignments, phylogenetics, diversity metrics (Shannon, UniFrac), ordination (PCoA, CCA), statistical tests (PERMANOVA, Mantel), and biological file format I/O.
---

# scikit-bio

A Python library for biological data analysis spanning sequence handling, phylogenetics, microbial ecology, and multivariate statistics.

## When to Apply

Use this skill when users need to:

| Task Category | Examples |
|--------------|----------|
| Sequence work | DNA/RNA/protein manipulation, motif finding, translation |
| File handling | FASTA, FASTQ, GenBank, Newick, BIOM I/O |
| Alignments | Pairwise or multiple sequence alignment |
| Phylogenetics | Tree construction, manipulation, distance calculations |
| Diversity metrics | Alpha diversity (Shannon, Faith's PD), beta diversity (Bray-Curtis, UniFrac) |
| Ordination | PCoA, CCA, RDA for dimensionality reduction |
| Statistical tests | PERMANOVA, ANOSIM, Mantel tests |
| Microbiome analysis | Feature tables, rarefaction, community comparisons |

## Installation

```bash
uv pip install scikit-bio
```

## Sequences

Work with biological sequences through specialized `DNA`, `RNA`, and `Protein` classes.

```python
import skbio

# Load from file
seq = skbio.DNA.read('gene.fasta')

# Common operations
complement = seq.reverse_complement()
messenger = seq.transcribe()
peptide = messenger.translate()

# Pattern search
hits = seq.find_with_regex('ATG[ACGT]{6}TAA')

# Properties
contains_ambiguous = seq.has_degenerates()
clean_seq = seq.degap()
```

**Metadata types:**
- Sequence-level: ID, description, source organism
- Positional: Per-base quality scores (from FASTQ)
- Interval: Feature annotations, gene boundaries

## Sequence Alignment

Pairwise and multiple alignment using dynamic programming.

```python
from skbio.alignment import local_pairwise_align_ssw, TabularMSA

# Local alignment (Smith-Waterman)
result = local_pairwise_align_ssw(query_seq, target_seq)

# Load existing alignment
alignment = TabularMSA.read('msa.fasta', constructor=skbio.DNA)

# Derive consensus
consensus_seq = alignment.consensus()
```

**Notes:**
- `local_pairwise_align_ssw` provides fast SSW-based local alignment
- `StripedSmithWaterman` handles protein sequences with substitution matrices
- Affine gap penalties suit biological sequences best

## Phylogenetic Trees

Construct and analyze evolutionary trees.

```python
from skbio import TreeNode
from skbio.tree import nj, upgma

# Build from distances
phylogeny = nj(distance_matrix)

# Load existing tree
phylogeny = TreeNode.read('species.nwk')

# Extract subset
clade = phylogeny.shear(['mouse', 'rat', 'human'])

# Enumerate leaf nodes
leaves = list(phylogeny.tips())

# Common ancestor
ancestor = phylogeny.lowest_common_ancestor(['mouse', 'rat'])

# Branch length between taxa
branch_dist = phylogeny.find('mouse').distance(phylogeny.find('rat'))

# Pairwise distances for all tips
pairwise_dm = phylogeny.cophenetic_matrix()

# Topology comparison
rf_diff = phylogeny.robinson_foulds(other_tree)
```

**Tree construction methods:**

| Method | Use case |
|--------|----------|
| `nj()` | Standard neighbor-joining |
| `upgma()` | Assumes molecular clock |
| `bme()` | Scalable for large datasets |

## Diversity Analysis

Calculate ecological diversity metrics.

### Alpha Diversity (within-sample)

```python
from skbio.diversity import alpha_diversity

# Sample abundance matrix
abundances = np.array([
    [45, 12, 0, 8],
    [5, 0, 33, 17],
    [20, 20, 15, 10]
])
samples = ['gut_1', 'gut_2', 'gut_3']

# Richness and evenness metrics
shannon_vals = alpha_diversity('shannon', abundances, ids=samples)
simpson_vals = alpha_diversity('simpson', abundances, ids=samples)

# Phylogenetic diversity (requires tree)
faith_vals = alpha_diversity('faith_pd', abundances, ids=samples,
                             tree=phylogeny, otu_ids=feature_names)
```

### Beta Diversity (between-sample)

```python
from skbio.diversity import beta_diversity

# Distance matrices
bray_dm = beta_diversity('braycurtis', abundances, ids=samples)
unifrac_dm = beta_diversity('weighted_unifrac', abundances, ids=samples,
                            tree=phylogeny, otu_ids=feature_names)
```

**Key points:**
- Input must be integer counts, not proportions
- Phylogenetic metrics require a tree matching feature IDs
- `partial_beta_diversity()` computes specific sample pairs efficiently

## Ordination

Project high-dimensional data to visualizable spaces.

```python
from skbio.stats.ordination import pcoa, cca

# PCoA from distance matrix
coords = pcoa(bray_dm)
axis1 = coords.samples['PC1']
axis2 = coords.samples['PC2']
variance_explained = coords.proportion_explained

# CCA with environmental predictors
constrained = cca(species_abundances, environmental_vars)
```

**Methods:**

| Function | Input | Purpose |
|----------|-------|---------|
| `pcoa()` | Distance matrix | Unconstrained ordination |
| `cca()` | Abundance + environment | Constrained ordination (unimodal) |
| `rda()` | Abundance + environment | Constrained ordination (linear) |

## Statistical Tests

Hypothesis testing for ecological data.

```python
from skbio.stats.distance import permanova, anosim, mantel

# Group comparison
treatment_groups = ['control', 'control', 'treated', 'treated']
perm_result = permanova(bray_dm, treatment_groups, permutations=999)
print(f"F = {perm_result['test statistic']:.3f}, p = {perm_result['p-value']:.4f}")

# Alternative group test
anos_result = anosim(bray_dm, treatment_groups, permutations=999)

# Matrix correlation
r, pval, n = mantel(genetic_dm, geographic_dm, method='spearman', permutations=999)
print(f"r = {r:.3f}, p = {pval:.4f}")
```

**Test overview:**

| Test | Purpose | Key output |
|------|---------|------------|
| PERMANOVA | Group differences | F-statistic, p-value |
| ANOSIM | Group differences (alternative) | R-statistic, p-value |
| PERMDISP | Dispersion homogeneity | Tests PERMANOVA assumption |
| Mantel | Matrix correlation | Correlation coefficient, p-value |

## File I/O

Read and write 19+ biological formats.

```python
import skbio

# Automatic format detection
tree = skbio.TreeNode.read('phylogeny.nwk')

# Memory-efficient iteration
for record in skbio.io.read('reads.fastq', format='fastq', constructor=skbio.DNA):
    if record.positional_metadata['quality'].mean() > 30:
        process(record)

# Format conversion
records = skbio.io.read('sequences.fastq', format='fastq', constructor=skbio.DNA)
skbio.io.write(records, format='fasta', into='sequences.fasta')
```

**Supported formats:**

| Category | Formats |
|----------|---------|
| Sequences | FASTA, FASTQ, GenBank, EMBL, QSeq |
| Alignments | Clustal, PHYLIP, Stockholm |
| Trees | Newick |
| Tables | BIOM (HDF5/JSON) |
| Distances | Delimited matrices |

## Distance Matrices

Store and manipulate pairwise distances.

```python
from skbio import DistanceMatrix
import numpy as np

# Create from array
distances = np.array([
    [0.0, 0.3, 0.7],
    [0.3, 0.0, 0.5],
    [0.7, 0.5, 0.0]
])
dm = DistanceMatrix(distances, ids=['sp_A', 'sp_B', 'sp_C'])

# Access elements
pair_dist = dm['sp_A', 'sp_B']
all_from_a = dm['sp_A']

# Subset
subset_dm = dm.filter(['sp_A', 'sp_C'])
```

## Feature Tables (BIOM)

Handle OTU/ASV abundance tables.

```python
from skbio import Table

# Load table
tbl = Table.read('features.biom')

# Inspect structure
sample_names = tbl.ids(axis='sample')
feature_names = tbl.ids(axis='observation')

# Filter by abundance
filtered = tbl.filter(lambda row, id_, md: row.sum() > 500, axis='sample')

# Convert to pandas
df = tbl.to_dataframe()
```

## Protein Embeddings

Bridge language model outputs with scikit-bio analysis.

```python
from skbio.embedding import ProteinEmbedding

# Load embeddings (from ESM, ProtTrans, etc.)
emb = ProteinEmbedding(embedding_matrix, protein_ids)

# Create distance matrix for downstream analysis
emb_dm = emb.to_distances(metric='cosine')

# Ordination visualization
emb_pcoa = emb.to_ordination(metric='euclidean', method='pcoa')
```

## Typical Workflows

**Microbiome diversity study:**
1. Load BIOM table and phylogenetic tree
2. Calculate alpha diversity per sample
3. Compute beta diversity (UniFrac)
4. Ordinate with PCoA
5. Test group differences with PERMANOVA

**Phylogenetic inference:**
1. Read sequences from FASTA
2. Perform multiple alignment
3. Calculate pairwise distances
4. Construct tree with neighbor-joining
5. Analyze clade relationships

**Sequence processing:**
1. Read FASTQ with quality scores
2. Filter low-quality reads
3. Search for motifs
4. Translate to protein
5. Export as FASTA

## Performance Tips

- Use generators for large sequence files
- Prefer BIOM HDF5 over JSON for big tables
- Apply `partial_beta_diversity()` when computing only specific pairs
- Choose BME for very large phylogenies

## Ecosystem Integration

| Library | Integration |
|---------|-------------|
| pandas | DataFrames from distance matrices, diversity results |
| numpy | Array conversions throughout |
| matplotlib/seaborn | Plot ordination results, heatmaps |
| scikit-learn | Distance matrices as input |
| QIIME 2 | Native BIOM, tree, distance matrix compatibility |

## Reference Files

| File | Contents |
|------|----------|
| [references/api-reference.md](references/api-reference.md) | Complete method signatures, parameters, extended examples, and troubleshooting |
