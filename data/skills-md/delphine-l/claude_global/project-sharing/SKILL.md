---
name: project-sharing
description: Prepare organized packages of project files for sharing at different levels - from summary PDFs to fully reproducible archives. Creates copies with cleaned notebooks, documentation, and appropriate file selection. After creating sharing package, all work continues in the main project directory.
version: 1.1.0
---

# Project Sharing and Output Preparation

Expert guidance for preparing project outputs for sharing with collaborators, reviewers, or repositories. Creates organized packages at different sharing levels while preserving your working directory.

## When to Use This Skill

- Sharing analysis results with collaborators
- Preparing supplementary materials for publications
- Creating reproducible research packages
- Archiving completed projects
- Handoff to other researchers
- Submitting to data repositories

## Core Principles

1. **Work on copies** - Never modify the working directory
2. **Choose appropriate level** - Match sharing depth to audience needs
3. **Document everything** - Include clear guides and metadata
4. **Clean before sharing** - Remove debug code, clear outputs, anonymize if needed
5. **Make it reproducible** - Include dependencies and instructions
6. **⚠️ CRITICAL: After creating sharing folder, all future work happens in the main project directory, NOT in the sharing folder** - Sharing folders are read-only snapshots

---

## Three Sharing Levels

### Level 1: Summary Only

**Purpose:** Quick sharing for presentations, reports, or high-level review

**What to include:**
- PDF export of final notebook(s)
- Final data/results (CSV, Excel, figures) - optional
- Brief README

**Use when:**
- Sharing results with non-technical stakeholders
- Presentations or talks
- Quick review without reproduction needs
- Space/time constraints

**Structure:**
```
shared-summary/
├── README.md                          # Brief overview
├── analysis-YYYY-MM-DD.pdf           # Notebook as PDF
└── results/
    ├── figures/
    │   ├── fig1-main-result.png
    │   └── fig2-comparison.png
    └── tables/
        └── summary-statistics.csv
```

---

### Level 2: Reproducible

**Purpose:** Enable others to reproduce your analysis from processed data

**What to include:**
- Analysis notebooks (.ipynb) - cleaned
- Scripts for figure generation
- Processed/analysis-ready data
- Requirements file (requirements.txt or environment.yml)
- Detailed README with instructions

**Use when:**
- Sharing with collaborating researchers
- Peer review / manuscript supplementary materials
- Teaching or tutorials
- Standard collaboration needs

**Structure:**
```
shared-reproducible/
├── README.md                          # Setup and reproduction instructions
├── MANIFEST.md                        # File descriptions
├── environment.yml                    # Conda environment OR requirements.txt
├── notebooks/
│   ├── 01-data-processing.ipynb      # Cleaned, outputs cleared
│   ├── 02-analysis.ipynb
│   └── 03-visualization.ipynb
├── scripts/
│   ├── generate_figures.py           # Standalone scripts
│   └── utils.py
└── data/
    ├── processed/
    │   ├── cleaned_data.csv
    │   └── processed_results.tsv
    └── README.md                      # Data provenance
```

---

### Level 3: Full Traceability

**Purpose:** Complete transparency from raw data through all processing steps

**What to include:**
- Starting/raw data
- All processing scripts and notebooks
- All intermediate files
- Final results
- Complete documentation
- Full dependency specification

**Use when:**
- Archiving for future reference
- Regulatory compliance
- High-stakes reproducibility (clinical, policy)
- Data repository submission (Zenodo, Dryad, etc.)
- Complete project handoff

**Structure:**
```
shared-complete/
├── README.md                          # Complete project guide
├── MANIFEST.md                        # Comprehensive file listing
├── environment.yml
├── data/
│   ├── raw/                          # Original, unmodified data
│   │   ├── sample_A_reads.fastq.gz
│   │   └── README.md                 # Data source, download date
│   ├── intermediate/                 # Processing steps
│   │   ├── 01-filtered/
│   │   ├── 02-aligned/
│   │   └── README.md
│   └── processed/                    # Final analysis-ready
│       └── final_dataset.csv
├── scripts/
│   ├── 01-download-data.sh
│   ├── 02-quality-control.py
│   ├── 03-filtering.py
│   ├── 04-analysis.py
│   └── utils/
├── notebooks/
│   ├── exploratory/                  # Early exploration
│   └── final/                        # Publication analyses
├── results/
│   ├── figures/
│   ├── tables/
│   └── supplementary/
└── documentation/
    ├── methods.md                    # Detailed methodology
    ├── changelog.md                  # Processing decisions
    └── data-dictionary.md            # Variable definitions
```

---

## Preparation Workflow

### Step 1: Ask User for Sharing Level

**Questions to determine level:**

```
Which sharing level do you need?

1. Summary Only - PDF + final results (quick sharing)
2. Reproducible - Notebooks + scripts + data (standard sharing)
3. Full Traceability - Everything from raw data (archival/compliance)

Additional questions:
- Who is the audience? (colleagues, reviewers, public)
- Are there size constraints?
- Any sensitive data to handle?
- Timeline for sharing?
```

### Step 2: Identify Files to Include

**For each level, identify:**

**Level 1 - Summary:**
- Main analysis notebook(s)
- Key figures (publication-quality)
- Summary tables/statistics
- Optional: Final processed dataset

**Level 2 - Reproducible:**
- All analysis notebooks (not exploratory)
- Figure generation scripts
- Processed/cleaned data
- Environment specification
- Any utility functions/modules

**Level 3 - Full:**
- Raw data (or links if too large)
- All processing scripts
- All notebooks (including exploratory)
- All intermediate files
- Complete documentation

### Step 3: Create Sharing Directory

```bash
# Create dated directory
SHARE_DIR="shared-$(date +%Y%m%d)-[level]"
mkdir -p "$SHARE_DIR"

# Create subdirectories based on level
# ... appropriate structure from above
```

### Step 4: Copy and Clean Files

**For notebooks (.ipynb):**

```python
import nbformat
from nbconvert.preprocessors import ClearOutputPreprocessor

def clean_notebook(input_path, output_path):
    """Clean notebook: clear outputs, remove debug cells."""

    # Read notebook
    with open(input_path, 'r') as f:
        nb = nbformat.read(f, as_version=4)

    # Clear outputs
    clear_output = ClearOutputPreprocessor()
    nb, _ = clear_output.preprocess(nb, {})

    # Remove cells tagged as 'debug' or 'remove'
    nb.cells = [cell for cell in nb.cells
                if 'debug' not in cell.metadata.get('tags', [])
                and 'remove' not in cell.metadata.get('tags', [])]

    # Write cleaned notebook
    with open(output_path, 'w') as f:
        nbformat.write(nb, f)
```

**For data files:**
- Copy as-is for small files
- Consider compression for large files
- Check for sensitive information

**For scripts:**
- Remove debugging code
- Add docstrings if missing
- Ensure paths are relative

### Step 5: Generate Documentation

#### README.md Template

```markdown
# Project: [Project Name]

**Date:** YYYY-MM-DD
**Author:** [Your Name]
**Sharing Level:** [Summary/Reproducible/Full]

## Overview

Brief description of the project and analysis.

## Contents

See MANIFEST.md for detailed file descriptions.

## Requirements

[For Reproducible/Full levels]
- Python 3.X
- See environment.yml for dependencies

## Setup

\`\`\`bash
# Create environment
conda env create -f environment.yml
conda activate project-name
\`\`\`

## Reproduction Steps

[For Reproducible/Full levels]

1. [Description of first step]
   \`\`\`bash
   jupyter notebook notebooks/01-analysis.ipynb
   \`\`\`

2. [Description of second step]

## Data Sources

[For Full level]
- Dataset A: [Source, download date, version]
- Dataset B: [Source, download date, version]

## Contact

[Your email or preferred contact]

## License

[If applicable - e.g., CC BY 4.0, MIT]
```

#### MANIFEST.md Template

```markdown
# File Manifest

Generated: YYYY-MM-DD

## Directory Structure

\`\`\`
shared-YYYYMMDD/
├── README.md                  - Project overview and setup
├── MANIFEST.md               - This file
[... complete tree ...]
\`\`\`

## File Descriptions

### Notebooks

- \`notebooks/01-data-processing.ipynb\` - Initial data loading and cleaning
- \`notebooks/02-analysis.ipynb\` - Main statistical analysis
- \`notebooks/03-visualization.ipynb\` - Figure generation for publication

### Data

- \`data/processed/cleaned_data.csv\` - Quality-controlled dataset (N=XXX samples)
  - Columns: [list key columns]
  - Missing values handled by [method]

### Scripts

- \`scripts/generate_figures.py\` - Automated figure generation
  - Usage: \`python generate_figures.py --input data/processed/cleaned_data.csv\`

### Results

- \`results/figures/fig1-main.png\` - Main result showing [description]
- \`results/tables/summary_stats.csv\` - Descriptive statistics

[Continue for all files...]
```

### Step 6: Handle Sensitive Data

**Check for sensitive information:**
- Personal identifiable information (PII)
- Access credentials (API keys, passwords)
- Proprietary data
- Institutional data with sharing restrictions
- Patient/subject identifiers

**Strategies:**
1. **Anonymize** - Remove or hash identifiers
2. **Exclude** - Don't include sensitive files
3. **Aggregate** - Share summary statistics only
4. **Document restrictions** - Note what's excluded and why

**Example anonymization:**
```python
import hashlib

def anonymize_ids(df, id_column='subject_id'):
    """Replace IDs with hashed values."""
    df[id_column] = df[id_column].apply(
        lambda x: hashlib.sha256(str(x).encode()).hexdigest()[:8]
    )
    return df
```

### Step 7: Package and Compress

**For smaller packages (<100MB):**
```bash
# Create zip archive
zip -r shared-YYYYMMDD.zip shared-YYYYMMDD/
```

**For larger packages:**
```bash
# Create tar.gz (better compression)
tar -czf shared-YYYYMMDD.tar.gz shared-YYYYMMDD/

# Or split into parts if very large
tar -czf - shared-YYYYMMDD/ | split -b 1G - shared-YYYYMMDD.tar.gz.part
```

**Document package contents:**
- Total size
- Number of files
- Compression method
- How to extract

### Step 8: Return to Working Directory

**⚠️ IMPORTANT: After creating the sharing package, always work in the main project directory.**

The sharing folder is a **snapshot for distribution only**. Any future development, analysis, or modifications should happen in your original working directory, not in the `shared-*/` folder.

**Claude should:**
- Change directory back to main project: `cd ..` (if needed)
- Confirm working directory: `pwd`
- Continue all work in the original project location
- Treat sharing folders as read-only archives

**Example:**
```bash
# After creating sharing package
cd /path/to/main/project  # Return to working directory
pwd                        # Verify location
# Continue work here, NOT in shared-YYYYMMDD/
```

---

## Best Practices

### Notebook Cleaning

**Before sharing notebooks:**

1. **Clear all outputs**
   ```bash
   jupyter nbconvert --clear-output --inplace notebook.ipynb
   ```

2. **Remove debug cells**
   - Tag cells for removal: Cell → Cell Tags → add "remove"
   - Filter during copy

3. **Add markdown explanations**
   - Ensure each code cell has context
   - Add section headers
   - Document assumptions

4. **Check cell execution order**
   - Run "Restart & Run All" to verify
   - Fix any out-of-order dependencies

5. **Remove absolute paths**
   ```python
   # ❌ Bad
   data = pd.read_csv('/Users/yourname/project/data.csv')

   # ✅ Good
   data = pd.read_csv('../data/data.csv')
   # or
   from pathlib import Path
   data_dir = Path(__file__).parent / 'data'
   ```

### File Organization

**Naming conventions for shared files:**
- Use descriptive names: `telomere_analysis_results.csv` not `results.csv`
- Include dates for time-sensitive data: `data_2024-01-15.csv`
- Version if applicable: `analysis_v2.ipynb`
- No spaces: use `-` or `_`

**Size considerations:**
- Document large files in README
- Consider hosting large data separately (institutional storage, Zenodo)
- Provide download links instead of including in package
- Use `.gitattributes` for large file tracking if using Git

### Documentation Requirements

**Minimum documentation for each level:**

**Level 1 - Summary:**
- What the results show
- Key findings
- Date and author

**Level 2 - Reproducible:**
- Setup instructions
- How to run the analysis
- Software dependencies
- Expected runtime
- Data source information

**Level 3 - Full:**
- Complete methodology
- All data sources with versions
- Processing decisions and rationale
- Known issues or limitations
- Contact information

### Dependency Management

**Create requirements file:**

**For pip:**
```bash
# From active environment
pip freeze > requirements.txt

# Or manually curated (better)
cat > requirements.txt << EOF
pandas>=1.5.0
numpy>=1.23.0
matplotlib>=3.6.0
scipy>=1.9.0
EOF
```

**For conda:**
```bash
# Export current environment
conda env export > environment.yml

# Or minimal (recommended)
conda env export --from-history > environment.yml

# Then edit to remove build-specific details
```

---

## Common Scenarios

### Scenario 1: Sharing with Lab Collaborators

**Level:** Reproducible

**Include:**
- Cleaned analysis notebooks
- Processed data
- Figure generation scripts
- environment.yml
- README with reproduction steps

**Don't include:**
- Exploratory notebooks
- Failed analysis attempts
- Debug outputs
- Personal notes

### Scenario 2: Manuscript Supplementary Material

**Level:** Reproducible or Full (depending on journal)

**Include:**
- All notebooks used for figures in paper
- Scripts for each figure panel
- Processed data (or instructions to obtain)
- Complete environment specification
- Detailed methods document

**Best practices:**
- Number notebooks to match paper sections
- Export key figures in publication formats (PDF, high-res PNG)
- Include data dictionary for all variables
- Test reproduction on clean environment

### Scenario 3: Project Archival

**Level:** Full Traceability

**Include:**
- Complete data pipeline from raw to processed
- All versions of analysis
- Meeting notes or decision logs
- External tool versions
- System information

**Organization tips:**
- Use dates in directory names
- Keep chronological changelog
- Document all external dependencies
- Include contact info for questions

### Scenario 4: Data Repository Submission (Zenodo, Figshare)

**Level:** Full Traceability

**Additional considerations:**
- Add LICENSE file (CC BY 4.0, MIT, etc.)
- Include CITATION.cff or CITATION.txt
- Comprehensive metadata
- README with DOI/reference instructions
- Consider maximum file sizes
- Review repository-specific guidelines

---

## Quality Checklist

Before finalizing the sharing package:

### File Quality
- [ ] All notebooks run without errors
- [ ] Notebook outputs cleared
- [ ] No absolute paths in code
- [ ] No hardcoded credentials or API keys
- [ ] File sizes documented
- [ ] Large files compressed or linked

### Documentation
- [ ] README explains setup and usage
- [ ] MANIFEST describes all files
- [ ] Data sources documented
- [ ] Dependencies specified
- [ ] Contact information included
- [ ] License specified (if applicable)

### Reproducibility
- [ ] Requirements file tested in clean environment
- [ ] All data accessible (included or linked)
- [ ] Scripts run in documented order
- [ ] Expected outputs match actual outputs
- [ ] Processing time documented

### Privacy & Sensitivity
- [ ] No sensitive data included
- [ ] Identifiers anonymized if needed
- [ ] Institutional policies checked
- [ ] Collaborator permissions obtained

### Organization
- [ ] Clear directory structure
- [ ] Consistent naming conventions
- [ ] Files logically grouped
- [ ] No duplicate files
- [ ] No unnecessary files (cache, .DS_Store, etc.)

---

## Integration with Other Skills

**Works well with:**
- **folder-organization** - Ensures source project is well-organized before sharing
- **jupyter-notebook-analysis** - Creates notebooks that are share-ready
- **managing-environments** - Documents dependencies properly

**Before using this skill:**
1. Organize working directory (folder-organization)
2. Finalize analysis (jupyter-notebook-analysis)
3. Document environment (managing-environments)

**After using this skill:**
1. Test package in clean environment
2. Share via appropriate channel (email, repository, cloud storage)
3. Keep archived copy for reference

---

## Example Scripts

### Create Sharing Package Script

```python
#!/usr/bin/env python3
"""Create sharing package for project."""

import shutil
from pathlib import Path
from datetime import date
import nbformat
from nbconvert.preprocessors import ClearOutputPreprocessor

def create_sharing_package(level='reproducible', output_dir=None):
    """
    Create sharing package.

    Args:
        level: 'summary', 'reproducible', or 'full'
        output_dir: Output directory name (auto-generated if None)
    """

    # Create output directory
    if output_dir is None:
        output_dir = f"shared-{date.today():%Y%m%d}-{level}"

    share_path = Path(output_dir)
    share_path.mkdir(exist_ok=True)

    print(f"Creating {level} sharing package in {share_path}")

    # Create structure based on level
    if level == 'summary':
        create_summary_package(share_path)
    elif level == 'reproducible':
        create_reproducible_package(share_path)
    elif level == 'full':
        create_full_package(share_path)

    print(f"✓ Package created: {share_path}")
    print(f"  Review and compress: tar -czf {share_path}.tar.gz {share_path}")

def clean_notebook(input_path, output_path):
    """Clean notebook outputs and debug cells."""
    with open(input_path) as f:
        nb = nbformat.read(f, as_version=4)

    # Clear outputs
    clear = ClearOutputPreprocessor()
    nb, _ = clear.preprocess(nb, {})

    # Remove debug cells
    nb.cells = [c for c in nb.cells
                if 'debug' not in c.metadata.get('tags', [])]

    with open(output_path, 'w') as f:
        nbformat.write(nb, f)

# ... implement level-specific functions ...

if __name__ == '__main__':
    import sys
    level = sys.argv[1] if len(sys.argv) > 1 else 'reproducible'
    create_sharing_package(level)
```

---

## Summary

**Key principles for project sharing:**

1. 🎯 **Choose the right level** - Match sharing depth to audience needs
2. 📋 **Copy, don't move** - Preserve your working directory
3. 🧹 **Clean thoroughly** - Remove debug code, clear outputs
4. 📝 **Document everything** - README + MANIFEST minimum
5. 🔒 **Check sensitivity** - Anonymize or exclude as needed
6. ✅ **Test before sharing** - Run in clean environment
7. 📦 **Package properly** - Compress and document contents
8. ⚠️ **Work in main directory** - After creating sharing package, ALL future work happens in the original project directory, NOT in the sharing folder

**Remember:** Good sharing practices benefit both collaborators and your future self!

---

## ⚠️ Critical Reminder for Claude

**After creating any sharing package:**

1. **Always return to the main project directory**
2. **Never work in `shared-*/` directories** - These are read-only snapshots
3. **All future edits, analysis, and development happen in the original working directory**
4. **Sharing folders are for distribution only, not active development**

If the user asks to modify files, always check the current directory and ensure you're working in the main project location, not in a sharing package.
