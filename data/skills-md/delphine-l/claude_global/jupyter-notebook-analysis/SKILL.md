---
name: jupyter-notebook-analysis
description: Best practices for creating comprehensive Jupyter notebook data analyses with statistical rigor, outlier handling, and publication-quality visualizations
---

# Jupyter Notebook Analysis Patterns

Expert knowledge for creating comprehensive, statistically rigorous Jupyter notebook analyses.

## When to Use This Skill

- Creating multi-cell Jupyter notebooks for data analysis
- Adding correlation analyses with statistical testing
- Implementing outlier removal strategies
- Building series of related visualizations (10+ figures)
- Analyzing large datasets with multiple characteristics

## Common Pitfalls

### Variable Shadowing in Loops

**Problem**: Using common variable names like `data` as loop variables overwrites global variables:

```python
# BAD - Shadows global 'data' variable
for i, (sp, data) in enumerate(species_by_gc_content[:10], 1):
    val = data['gc_content']
    print(f'{sp}: {val}')
```

After this loop, `data` is no longer your dataset list - it's the last species dict!

**Solution**: Use descriptive loop variable names:

```python
# GOOD - Uses specific name
for i, (sp, sp_data) in enumerate(species_by_gc_content[:10], 1):
    val = sp_data['gc_content']
    print(f'{sp}: {val}')
```

**Detection**: If you see errors like "Type: <class 'dict'>" when expecting a list, check for variable shadowing in recent cells.

**Prevention**:
- Never use generic names (`data`, `item`, `value`) as loop variables
- Use prefixed names (`sp_data`, `row_data`, `inv_data`)
- Add validation cells that check variable types
- Run "Restart & Run All" regularly to catch issues early

**Common shadowing patterns to avoid**:
```python
for data in dataset:          # Shadows 'data'
for i, data in enumerate():   # Shadows 'data'
for key, data in dict.items() # Shadows 'data'
```

### Verify Column Names Before Processing

**Problem**: Assuming column names without checking actual DataFrame structure leads to immediate failures. Column names may use different capitalization, spacing, or naming conventions than expected.

**Example error:**
```python
# Assumed column name
df_filtered = df[df['scientific_name'] == target]  # KeyError!

# Actual column name was 'Scientific Name' (capitalized with space)
```

**Solution**: Always check actual columns first:
```python
import pandas as pd
df = pd.read_csv('data.csv')

# ALWAYS print columns before processing
print("Available columns:")
print(df.columns.tolist())

# Then write filtering code with correct names
df_filtered = df[df['Scientific Name'] == target_species]  # Correct
```

**Best practice for data processing scripts:**
```python
# At the start of your script
def verify_required_columns(df, required_cols):
    """Verify DataFrame has required columns."""
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        print(f"ERROR: Missing columns: {missing}")
        print(f"Available columns: {df.columns.tolist()}")
        sys.exit(1)

# Use it
required = ['Scientific Name', 'tolid', 'accession']
verify_required_columns(df, required)
```

**Common column name variations to watch for:**
- `scientific_name` vs `Scientific Name` vs `ScientificName`
- `species_id` vs `species` vs `Species ID`
- `genome_size` vs `Genome size` vs `GenomeSize`

**Debugging tip**: Include column listing in all data processing scripts:
```python
# Add at script start for easy debugging
if '--debug' in sys.argv or len(df.columns) < 10:
    print(f"Columns ({len(df.columns)}): {df.columns.tolist()}")
```

## Outlier Handling Best Practices

### Two-Stage Outlier Removal

For analyses correlating characteristics across aggregated entities (e.g., species-level summaries):

1. **Stage 1: Count-based outliers (IQR method)**
   - Remove entities with abnormally high sample counts
   - Prevents over-represented entities from skewing correlations
   - Apply BEFORE other analyses

   ```python
   import numpy as np
   workflow_counts = [entity_data[id]['workflow_count'] for id in entity_data.keys()]
   q1 = np.percentile(workflow_counts, 25)
   q3 = np.percentile(workflow_counts, 75)
   iqr = q3 - q1
   upper_bound = q3 + 1.5 * iqr

   outliers = [id for id in entity_data.keys()
               if entity_data[id]['workflow_count'] > upper_bound]
   for id in outliers:
       del entity_data[id]
   ```

2. **Stage 2: Value-based outliers (percentile)**
   - Remove extreme values for visualization clarity
   - Apply ONLY to visualization data, not statistics
   - Typically top 5% for highly skewed distributions

   ```python
   values = [entity_data[id]['metric'] for id in entity_data.keys()]
   threshold = np.percentile(values, 95)
   viz_entities = [id for id in entity_data.keys()
                   if entity_data[id]['metric'] <= threshold]

   # Use viz_entities for plotting
   # Use full entity_data.keys() for statistics
   ```

### Characteristic-Specific Outlier Removal

When analyzing genome characteristics vs metrics, remove outliers for the characteristic being analyzed:

```python
# After removing workflow count outliers, also remove heterozygosity outliers
heterozygosity_values = [species_data[sp]['heterozygosity'] for sp in species_data.keys()]

het_q1 = np.percentile(heterozygosity_values, 25)
het_q3 = np.percentile(heterozygosity_values, 75)
het_iqr = het_q3 - het_q1
het_upper_bound = het_q3 + 1.5 * het_iqr

het_outliers = [sp for sp in species_data.keys()
                if species_data[sp]['heterozygosity'] > het_upper_bound]

for sp in het_outliers:
    del species_data[sp]

print(f'Removed {len(het_outliers)} heterozygosity outliers (>{het_upper_bound:.2f}%)')
print(f'New heterozygosity range: {min(vals):.2f}% - {max(vals):.2f}%')
```

**Apply separately for each characteristic**:
- Genome size outliers for genome size analysis
- Heterozygosity outliers for heterozygosity analysis
- Repeat content outliers for repeat content analysis

### When to Skip Outlier Removal

- Memory usage plots when investigating over-allocation patterns
- Comparison plots (allocated vs used) where outliers reveal problems
- User explicitly requests to see all data
- Data is already limited (< 10 points)

**Document clearly** in plot titles and code comments which outlier removal is applied.


###IQR-Based Outlier Removal for Visualization

**Standard Method**: 1.5×IQR (Interquartile Range)

**Implementation**:
```python
# Calculate IQR
Q1 = data.quantile(0.25)
Q3 = data.quantile(0.75)
IQR = Q3 - Q1

# Define outlier boundaries (standard: 1.5×IQR)
lower_bound = Q1 - 1.5*IQR
upper_bound = Q3 + 1.5*IQR

# Filter outliers
outlier_mask = (data >= lower_bound) & (data <= upper_bound)
data_filtered = data[outlier_mask]
n_outliers = (~outlier_mask).sum()

# IMPORTANT: Report outliers removed
print(f"Removed {n_outliers} outliers for visualization")
# Add to figure: f"({n_outliers} outliers removed)"
```

**Multi-dimensional Outlier Removal**:
```python
# For scatter plots with two dimensions (e.g., size ratio AND absolute size)
outlier_mask = (
    (ratio >= Q1_ratio - 1.5*IQR_ratio) &
    (ratio <= Q3_ratio + 1.5*IQR_ratio) &
    (size >= Q1_size - 1.5*IQR_size) &
    (size <= Q3_size + 1.5*IQR_size)
)
```

**Best Practice**: Always report number of outliers removed in figure statistics or caption.

**When to Use**: For visualization clarity when extreme values compress the main distribution. Not for removing "bad" data - use for display only.

## Statistical Rigor

### Required for Correlation Analyses

1. **Pearson correlation with p-values**:
   ```python
   from scipy import stats
   correlation, p_value = stats.pearsonr(x_values, y_values)
   sig_text = 'significant' if p_value < 0.05 else 'not significant'
   ```

2. **Report both metrics**:
   - Correlation coefficient (r) - strength and direction
   - P-value - statistical significance (α=0.05)
   - Sample size (n)

3. **Display on plots**:
   ```python
   ax.text(0.98, 0.02,
           f'r = {correlation:.3f}\np = {p_value:.2e}\n({sig_text})\nn = {len(data)} species',
           transform=ax.transAxes, ...)
   ```


### Adding Mann-Whitney U Tests to Figures

**When to Use**: Comparing continuous metrics between two groups (e.g., Dual vs Pri/alt curation)

**Standard Implementation**:
```python
from scipy import stats

# Calculate test
data_group1 = df[df['group'] == 'Group1']['metric']
data_group2 = df[df['group'] == 'Group2']['metric']

if len(data_group1) > 0 and len(data_group2) > 0:
    stat, pval = stats.mannwhitneyu(data_group1, data_group2, alternative='two-sided')
else:
    pval = np.nan

# Add to stats text
if not np.isnan(pval):
    stats_text += f"\nMann-Whitney p: {pval:.2e}"
```

**Display in Figures**: Include p-value in statistics box with format `Mann-Whitney p: 1.23e-04`

**Consistency**: Ensure all quantitative comparison figures include this test for statistical rigor.

## Large-Scale Analysis Structure

### Control Analyses: Checking for Confounding

When comparing methods (e.g., Method A vs Method B), always check if observed differences could be explained by characteristics of the samples rather than the methods themselves.

**Critical control analysis**:
```python
import pandas as pd
from scipy import stats

def check_confounding(df, method_col, characteristics):
    """
    Compare sample characteristics between methods to check for confounding.
    
    Args:
        df: DataFrame with samples
        method_col: Column indicating method ('Method_A', 'Method_B')
        characteristics: List of column names to compare
    
    Returns:
        DataFrame with statistical comparison
    """
    results = []
    
    for char in characteristics:
        # Get data for each method
        method_a = df[df[method_col] == 'Method_A'][char].dropna()
        method_b = df[df[method_col] == 'Method_B'][char].dropna()
        
        if len(method_a) < 5 or len(method_b) < 5:
            continue
        
        # Statistical test
        stat, pval = stats.mannwhitneyu(method_a, method_b, alternative='two-sided')
        
        # Calculate effect size (% difference in medians)
        pooled_median = pd.concat([method_a, method_b]).median()
        effect_pct = (method_a.median() - method_b.median()) / pooled_median * 100
        
        results.append({
            'Characteristic': char,
            'Method_A_median': method_a.median(),
            'Method_A_n': len(method_a),
            'Method_B_median': method_b.median(),
            'Method_B_n': len(method_b),
            'p_value': pval,
            'effect_pct': effect_pct,
            'significant': pval < 0.05
        })
    
    return pd.DataFrame(results)

# Example usage
characteristics = ['genome_size', 'gc_content', 'heterozygosity', 
                  'repeat_content', 'sequencing_coverage']

confounding_check = check_confounding(df, 'curation_method', characteristics)
print(confounding_check)
```

**Interpretation guide**:
- **No significant differences**: Methods compared equivalent samples → valid comparison
- **Method A has "easier" samples** (smaller genomes, lower complexity): Quality differences may be due to sample properties, not method
- **Method A has "harder" samples** (larger genomes, higher complexity): Strengthens conclusion that Method A is better despite challenges
- **Limited data** (n<10): Cannot rule out confounding, note as limitation

**Present in notebook**:
```markdown
## Genome Characteristics Comparison

**Control Analysis**: Are quality differences due to method or sample properties?

[Table comparing characteristics]

**Conclusion**: 
- If no differences → Valid method comparison
- If Method A works with harder samples → Strengthens conclusions
- If Method A works with easier samples → Potential confounding
```

**Why critical**: Reviewers will ask this question. Preemptive control analysis demonstrates scientific rigor and prevents major revisions.


### Organizing 60+ Cell Notebooks

1. **Section headers** (markdown cells):
   - Main sections: "## CPU Runtime Analysis", "## Memory Analysis"
   - Subsections: "### Genome Size vs CPU Runtime"

2. **Cell pairing pattern**:
   - Markdown header + code cell for each analysis
   - Keeps related content together
   - Easier to navigate and debug

3. **Consistent naming**:
   - Figure files: `fig18_genome_size_vs_cpu_hours.png`
   - Variables: `species_data`, `genome_sizes_full`, `genome_sizes_viz`
   - Functions: `safe_float_convert()` defined consistently

4. **Progressive enhancement**:
   - Start with basic analyses
   - Add enriched data (Cell 7 pattern)
   - Build increasingly complex correlations
   - End with multivariate analyses (PCA)

## Template Generation Pattern

For creating multiple similar analysis cells:

```python
# Create template with placeholder variables
template = '''
if len(data_with_species) > 0:
    print('Analyzing {display} vs {metric}...\\n')

    # Aggregate data per species
    species_data = {{}}

    for inv in data_with_species:
        {name} = safe_float_convert(inv.get('{name}'))
        if {name} is None:
            continue
        # ... analysis code
'''

# Generate multiple cells from characteristics list
characteristics = [
    {'name': 'genome_size', 'display': 'Genome Size', 'unit': 'Gb'},
    {'name': 'heterozygosity', 'display': 'Heterozygosity', 'unit': '%'},
    # ...
]

for char in characteristics:
    code = template.format(**char)
    # Write to notebook or temp file
```

## Helper Function Pattern

Define once, reuse throughout:

```python
def safe_float_convert(value):
    """Convert string to float, handling comma separators"""
    if not value or not str(value).strip():
        return None
    try:
        return float(str(value).replace(',', ''))
    except (ValueError, TypeError):
        return None
```

Include in Cell 7 (enrichment) and reference: "# Helper function (same as Cell 7)"

## Publication-Quality Figures

Standard settings:
- DPI: 300
- Figure size: (12, 8) for single plots, (16, 7) for side-by-side
- Grid: `alpha=0.3, linestyle='--'`
- Point size: Proportional to sample count (`s=[50 + count*20 for count in counts]`)
- Colormap: 'viridis' for workflow counts


### Publication-Ready Font Sizes

**Problem**: Default matplotlib fonts are designed for screen viewing, not print publication.

**Solution**: Use larger, bold fonts for print readability.

**Recommended sizes** (for standard 10-12 cm wide figures):

| Element | Default | Publication | Code |
|---------|---------|-------------|------|
| **Title** | 11-12pt | **18pt** (bold) | `fontsize=18, fontweight='bold'` |
| **Axis labels** | 10-11pt | **16pt** (bold) | `fontsize=16, fontweight='bold'` |
| **Tick labels** | 9-10pt | **14pt** | `tick_params(labelsize=14)` |
| **Legend** | 8-10pt | **12pt** | `legend(fontsize=12)` |
| **Annotations** | 8-10pt | **11-13pt** | `fontsize=12` |
| **Data points** | 20-36 | **60-100** | `s=80` (scatter) |

**Implementation example**:
```python
fig, ax = plt.subplots(figsize=(10, 8))

# Plot data
ax.scatter(x, y, s=80, alpha=0.6)  # Larger points

# Titles and labels - BOLD
ax.set_title('Your Title Here', fontsize=18, fontweight='bold')
ax.set_xlabel('X Axis Label', fontsize=16, fontweight='bold')
ax.set_ylabel('Y Axis Label', fontsize=16, fontweight='bold')

# Tick labels
ax.tick_params(axis='both', which='major', labelsize=14)

# Legend
ax.legend(fontsize=12, loc='best')

# Stats box
stats_text = "Statistics:\nMean: 42.5"
ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
       fontsize=13, family='monospace',
       bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))

# Reference lines - thicker
ax.axhline(y=1.0, linewidth=2.5, linestyle='--', alpha=0.6)
```

**Quick check**: If you have to squint to read the figure on screen at 100% zoom, fonts are too small for print.

**Special cases**:
- Multi-panel figures: Increase 10-15% more
- Posters: Increase 50-100% more
- Presentations: Increase 30-50% more

### Accessibility: Colorblind-Safe Palettes

**Problem**: Standard color schemes (green vs blue, red vs green) are difficult or impossible to distinguish for people with color vision deficiencies, affecting ~8% of males and ~0.5% of females.

**Solution**: Use colorblind-safe palettes from validated sources.

**IBM Color Blind Safe Palette (Recommended)**:
```python
# For comparing two groups/conditions
colors = {
    'Group_A': '#0173B2',  # Blue
    'Group_B': '#DE8F05'   # Orange
}
```

**Why this works**:
- ✅ Maximum contrast for all color vision types (deuteranopia, protanopia, tritanopia, achromatopsia)
- ✅ Professional appearance for scientific publications
- ✅ Clear distinction even in grayscale printing
- ✅ Cultural neutrality (no red/green traffic light associations)

**Other colorblind-safe combinations**:
- Blue + Orange (best overall)
- Blue + Red (good for most types)
- Blue + Yellow (good but lower contrast)

**Avoid**:
- ❌ Green + Red (most common color blindness)
- ❌ Green + Blue (confusing for many)
- ❌ Blue + Purple (too similar)

**Implementation in matplotlib**:
```python
import matplotlib.pyplot as plt

# Define colorblind-safe palette
CB_COLORS = {
    'blue': '#0173B2',
    'orange': '#DE8F05',
    'green': '#029E73',
    'red': '#D55E00',
    'purple': '#CC78BC',
    'brown': '#CA9161'
}

# Use in plots
plt.scatter(x, y, color=CB_COLORS['blue'], label='Treatment')
plt.scatter(x2, y2, color=CB_COLORS['orange'], label='Control')
```

**Testing your colors**:
- Use online simulators: https://www.color-blindness.com/coblis-color-blindness-simulator/
- Check in grayscale: Convert figure to grayscale to ensure distinguishability

### Handling Severe Data Imbalance in Comparisons

**Problem**: Comparing groups with very different sample sizes (e.g., 84 vs 10) can lead to misleading conclusions.

**Solution**: Add prominent warnings both visually and in documentation.

**Visual warning on figure**:
```python
import matplotlib.pyplot as plt

# After creating your plot
n_group_a = len(df[df['group'] == 'A'])
n_group_b = len(df[df['group'] == 'B'])
total_a = 200
total_b = 350

warning_text = f"⚠️  DATA LIMITATION\n"
warning_text += f"Data availability:\n"
warning_text += f"  Group A: {n_group_a}/{total_a} ({n_group_a/total_a*100:.1f}%)\n"
warning_text += f"  Group B: {n_group_b}/{total_b} ({n_group_b/total_b*100:.1f}%)\n"
warning_text += f"Severe imbalance limits\nstatistical comparability"

ax.text(0.98, 0.02, warning_text, transform=ax.transAxes,
       fontsize=11, verticalalignment='bottom', horizontalalignment='right',
       bbox=dict(boxstyle='round', facecolor='red', alpha=0.2, 
                edgecolor='red', linewidth=2),
       family='monospace', color='darkred', fontweight='bold')

# Update title to indicate limitation
ax.set_title('Your Title\n(SUPPLEMENTARY - Limited Data Availability)', 
            fontsize=14, fontweight='bold')
```

**Text warning in notebook/paper**:
```markdown
**⚠️ CRITICAL DATA LIMITATION**: This figure suffers from severe data availability bias:
- Group A: 84/200 (42%)
- Group B: 10/350 (3%)

This **8-fold imbalance** severely limits statistical comparability. The 10 Group B 
samples are unlikely to be representative of all 350. 

**Interpretation**: Comparisons should be interpreted with extreme caution. This 
figure is provided for completeness but should be considered **supplementary**.
```

**Guidelines for sample size imbalance**:
- **< 2× imbalance**: Generally acceptable, note in caption
- **2-5× imbalance**: Add note about limitations
- **> 5× imbalance**: Add prominent warnings (visual + text)
- **> 10× imbalance**: Consider excluding figure or supplementary-only

**Alternative**: If possible, subset the larger group to match sample size:
```python
# Random subset to balance groups
if n_group_a > n_group_b * 2:
    group_a_subset = df[df['group'] == 'A'].sample(n=n_group_b * 2, random_state=42)
    # Use subset for balanced comparison
```

## Creating Analysis Notebooks for Scientific Publications

When creating Jupyter notebooks to accompany manuscript figures:

### Structure Pattern
1. **Title and metadata** - Date, dataset info, sample sizes
2. **Overview** - Context from paper abstract/intro
3. **Figure-by-figure analysis**:
   - Code cell to display image
   - Detailed figure legend (publication-ready)
   - Comprehensive analysis paragraph explaining:
     - What the metric measures
     - Statistical results
     - Mechanistic explanation
     - Biological/technical implications
4. **Methods section** - Complete reproducibility information
5. **Conclusions** - Summary of findings

### Table of Contents

For analysis notebooks >10 cells, add a navigable table of contents at the top:

**Benefits**:
- Quick navigation to specific analyses
- Clear overview of notebook structure
- Professional presentation
- Easier for collaborators

**Implementation** (Markdown cell):
```markdown
# Analysis Name

## Table of Contents

1. [Data Loading](#data-loading)
2. [Data Quality Metrics](#data-quality-metrics)
3. [Figure 1: Completeness](#figure-1-completeness)
4. [Figure 2: Contiguity](#figure-2-contiguity)
5. [Figure 3: Scaffold Validation](#figure-3-scaffold-validation)
...
10. [Methods](#methods)
11. [References](#references)

---
```

**Section Headers** (Markdown cells):
```markdown
## Data Loading

[Your code/analysis]

---

## Data Quality Metrics

[Your code/analysis]
```

**Auto-generation**: For large notebooks, consider generating TOC programmatically:
```python
from IPython.display import Markdown

sections = ['Introduction', 'Data Loading', 'Analysis', ...]
toc = "## Table of Contents\n\n"
for i, section in enumerate(sections, 1):
    anchor = section.lower().replace(' ', '-')
    toc += f"{i}. [{section}](#{anchor})\n"

display(Markdown(toc))
```

### Methods Documentation

Always include a Methods section documenting:
- Data sources with accession numbers
- Key algorithms and formulas
- Statistical approaches
- Software versions
- Special adjustments (e.g., sex chromosome correction)
- Literature citations

**Example**:
```markdown
## Methods

### Karyotype Data

Karyotype data (diploid 2n and haploid n chromosome numbers) was manually curated from peer-reviewed literature for 97 species representing 17.8% of the VGP Phase 1 dataset (n = 545 assemblies).

#### Sex Chromosome Adjustment

When both sex chromosomes are present in the main haplotype, the expected number of chromosome-level scaffolds is:

**expected_scaffolds = n + 1**

For example:
- Asian elephant: 2n=56, n=28, has X+Y → expected 29 scaffolds
- White-throated sparrow: 2n=82, n=41, has Z+W → expected 42 scaffolds

This adjustment accounts for the biological reality that X and Y (or Z and W) are distinct chromosomes.
```

### Writing Style Matching
To match manuscript style:
- Read draft paper PDF to extract tone and terminology
- Use same technical vocabulary
- Match paragraph structure (observation → mechanism → implication)
- Include specific details (tool names, file formats, software versions)
- Use first-person plural ("we") if paper does
- Maintain consistent bullet point/list formatting

### Example Code Pattern
```python
# Display figure
from IPython.display import Image, display
from pathlib import Path

FIG_DIR = Path('figures/analysis_name')
display(Image(filename=str(FIG_DIR / 'figure_01.png')))
```

### Figure Legend Format
**Figure N. [Short title].** [Complete description of panels and what's shown]. [Statistical tests used]. [Sample sizes]. [Scale information]. [Color coding].

### Analysis Paragraph Structure
1. **What it measures** - Define the metric/comparison
2. **Statistical result** - Quantitative findings with p-values
3. **Mechanistic explanation** - Why this result occurs
4. **Implications** - What this means for conclusions

### Methods Section Must Include
- Dataset source and filtering criteria
- Metric definitions
- Outlier handling approach
- Statistical methods with justification
- Software versions and tools
- Reproducibility information
- Known limitations

This approach creates notebooks that serve both as analysis documentation and as supplementary material for publications.

### Environment Setup

For CLI-based workflows (Claude Code, SSH sessions):

```bash
# Run in background with token authentication
/path/to/conda/envs/ENV_NAME/bin/jupyter lab --no-browser --port=8888
```

**Parameters**:
- `--no-browser`: Don't auto-open browser (for remote sessions)
- `--port=8888`: Specify port (default, can change if occupied)
- Run in background: Use `run_in_background=true` in Bash tool

**Access URL format**:
```
http://localhost:8888/lab?token=TOKEN_STRING
```

**To stop later**:
- Find shell ID from BashOutput tool
- Use KillShell with that ID

**Installation if missing**:
```bash
/path/to/conda/envs/ENV_NAME/bin/pip install jupyterlab
```

## Notebook Size Management

For notebooks > 256 KB:
- Use `jq` to read specific cells: `cat notebook.ipynb | jq '.cells[10:20]'`
- Count cells: `cat notebook.ipynb | jq '.cells | length'`
- Check sections: `cat notebook.ipynb | jq '.cells[75:81] | .[].source[:2]'`

## Data Enrichment Pattern

When linking external metadata with analysis data:

```python
# Cell 6: Load genome metadata
import csv
genome_data = []
with open('genome_metadata.tsv') as f:
    reader = csv.DictReader(f, delimiter='\t')
    genome_data = list(reader)

genome_lookup = {}
for row in genome_data:
    species_id = row['species_id']
    if species_id not in genome_lookup:
        genome_lookup[species_id] = []
    genome_lookup[species_id].append(row)

# Cell 7: Enrich workflow data with genome characteristics
for inv in data:
    species_id = inv.get('species_id')

    if species_id and species_id in genome_lookup:
        genome_info = genome_lookup[species_id][0]

        # Add genome characteristics
        inv['genome_size'] = genome_info.get('Genome size', '')
        inv['heterozygosity'] = genome_info.get('Heterozygosity', '')
        # ... other characteristics
    else:
        # Set to None for missing data
        inv['genome_size'] = None
        inv['heterozygosity'] = None

# Create filtered dataset
data_with_species = [inv for inv in data if inv.get('species_id') and inv.get('genome_size')]
```

## Data Backup Strategy

### The Problem
Long-running data enrichment projects risk:
- Losing days of work from accidental overwrites
- Unable to revert to previous data states
- No documentation of what changed when
- Running out of disk space from manual backups

### Solution: Automated Two-Tier Backup System

**Architecture:**
1. **Daily backups** - Rolling 7-day window (auto-cleanup)
2. **Milestone backups** - Permanent, compressed (gzip ~80% reduction)
3. **CHANGELOG** - Automatic documentation of all changes

**Implementation:**
```bash
# Daily backup (start of each work session)
./backup_table.sh

# Milestone backup (after major changes)
./backup_table.sh milestone "added genomescope data for 21 species"

# List all backups
./backup_table.sh list

# Restore from backup (with safety backup)
./backup_table.sh restore 2026-01-23
```

**Directory structure:**
```
backups/
├── daily/              # Rolling 7-day backups (~770KB each)
│   ├── backup_2026-01-17.csv
│   └── backup_2026-01-23.csv
├── milestones/         # Permanent compressed backups (~200KB each)
│   ├── milestone_2026-01-20_initial_enrichment.csv.gz
│   └── milestone_2026-01-23_recovered_accessions.csv.gz
├── CHANGELOG.md        # Auto-generated change log
└── README.md           # User documentation
```

**Storage efficiency:**
- Daily backups: ~5.4 MB (7 days × 770KB)
- Milestone backups: ~200KB each compressed (80% size reduction)
- Total: <10 MB for complete project history
- Old daily backups auto-delete after 7 days

**When to create milestones:**
- After adding new data sources (GenomeScope, karyotypes, etc.)
- Before major data transformations
- When completing analysis sections
- Before submitting/publishing

**Global installer available:**
```bash
# Install backup system in any repository
install-backup-system -f your_data_file.csv
```

**Key features:**
- Never overwrites without confirmation
- Creates safety backup before restore
- Complete audit trail in CHANGELOG
- Color-coded terminal output
- Handles both CSV and TSV files

**Benefits for data analysis:**
- **Data provenance** - CHANGELOG documents every modification
- **Confidence to experiment** - Easy rollback encourages trying approaches
- **Professional workflow** - Matches publication standards
- **Collaboration-ready** - Team members can understand data history

## Debugging Data Availability

Before creating correlation plots, verify data overlap:

```python
# Check how many entities have both metrics
species_with_metric_a = set(inv.get('species_id') for inv in data
                            if inv.get('metric_a'))
species_with_metric_b = set(inv.get('species_id') for inv in data
                            if inv.get('metric_b'))

overlap = species_with_metric_a.intersection(species_with_metric_b)
print(f"Species with both metrics: {len(overlap)}")

if len(overlap) < 10:
    print("⚠️ Warning: Limited data for correlation analysis")
    print(f"  Metric A: {len(species_with_metric_a)} species")
    print(f"  Metric B: {len(species_with_metric_b)} species")
    print(f"  Overlap: {len(overlap)} species")
```

### Variable State Validation

When debugging notebook errors, add validation cells to check variable integrity:

```python
# Validation cell - place before error-prone sections
print('=== VARIABLE VALIDATION ===')
print(f'Type of data: {type(data)}')
print(f'Is data a list? {isinstance(data, list)}')

if isinstance(data, list):
    print(f'Length: {len(data)}')
    if len(data) > 0:
        print(f'First item type: {type(data[0])}')
        print(f'First item keys: {list(data[0].keys())[:10]}')
elif isinstance(data, dict):
    print(f'⚠️  WARNING: data is a dict, not a list!')
    print(f'Dict keys: {list(data.keys())[:10]}')
    print(f'This suggests variable shadowing occurred.')
```

**When to use**:
- After "Restart & Run All" produces errors
- When error messages suggest wrong variable type
- Before cells that fail intermittently
- In notebooks with 50+ cells

**Best practice**: Include automatic validation in cells that depend on critical global variables.

## Programmatic Notebook Manipulation

When inserting cells into large notebooks:

```python
import json

# Read notebook
with open('notebook.ipynb', 'r') as f:
    notebook = json.load(f)

# Create new cell
new_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [line + '\n' for line in code.split('\n')]
}

# Insert at position
insert_position = 50
notebook['cells'] = (notebook['cells'][:insert_position] +
                     [new_cell] +
                     notebook['cells'][insert_position:])

# Write back
with open('notebook.ipynb', 'w') as f:
    json.dump(notebook, f, indent=1)
```


### Synchronizing Figure Code and Notebook Documentation

**Pattern**: Code changes to figure generation → Must update notebook text

**Common Scenario**: Updated figure filtering/outlier removal/statistical tests

**Workflow**:
1. Update figure generation Python script
2. Regenerate figures
3. **CRITICAL**: Update Jupyter notebook markdown cells documenting the figure
4. Use `NotebookEdit` tool (NOT `Edit` tool) for `.ipynb` files

**Example**:
```python
# After adding Mann-Whitney test to figure generation:
NotebookEdit(
    notebook_path="/path/to/notebook.ipynb",
    cell_id="cell-14",  # Found via grep or Read
    cell_type="markdown",
    new_source="Updated description mentioning Mann-Whitney test..."
)
```

**Finding Figure Cells**:
```bash
# Locate figure references
grep -n "figure_name.png" notebook.ipynb

# Or use Glob + Grep
grep -n "Figure 4" notebook.ipynb
```

**Why Critical**: Outdated documentation causes confusion. Notebook text saying "Limited data" when data is now complete, or not mentioning new statistical tests, misleads readers.

## Best Practices Summary

1. **Always check data availability** before creating analyses
2. **Document outlier removal** clearly in titles and comments
3. **Use consistent naming** for variables and figures
4. **Include statistical testing** for all correlations
5. **Separate visualization from statistics** when filtering outliers
6. **Create templates** for repetitive analyses
7. **Use helper functions** consistently across cells
8. **Organize with markdown headers** for navigation
9. **Test with small datasets** before running full analyses
10. **Save intermediate results** for expensive computations

## Common Tasks

### Removing Panels from Multi-Panel Figures

**Scenario**: Convert 2-panel figure to 1-panel after removing unavailable data.

**Steps**:
1. **Update subplot layout**:
   ```python
   # Before: 2 panels
   fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
   
   # After: 1 panel
   fig, ax = plt.subplots(1, 1, figsize=(10, 6))
   ```

2. **Remove panel code**: Delete all code for removed panel (ax2)

3. **Update figure filename**:
   ```python
   # Before
   plt.savefig('06_scaffold_l50_l90_comparison.png')
   
   # After
   plt.savefig('06_scaffold_l50_comparison.png')
   ```

4. **Update notebook references**:
   - Image display: `display(Image(...'06_scaffold_l50_comparison.png'))`
   - Title: Remove references to removed data
   - Description: Add note about why panel is excluded

5. **Clean up old files**:
   ```bash
   rm figures/*_l50_l90_*.png
   ```

