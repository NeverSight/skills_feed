---
name: scientific-paper-figure-generator
description: Use when asked to create publication-ready scientific figures, charts for research papers, or academic visualizations.
---

# Scientific Paper Figure Generator

Create publication-ready figures for scientific papers with proper formatting, high resolution, and journal-compliant styling.

## Purpose

Scientific figure creation for:
- Research paper submissions
- Conference presentations
- Thesis and dissertation figures
- Grant proposals
- Academic posters

## Features

- **Journal Templates**: Nature, Science, IEEE, ACS styles
- **Multi-Panel Figures**: Subfigures with labels (a, b, c)
- **High Resolution**: 300+ DPI for publication
- **Vector Output**: EPS, PDF for scalability
- **Statistical Annotations**: p-values, error bars, significance
- **Consistent Styling**: Match journal requirements

## Quick Start

```python
from scientific_paper_figure_generator import PaperFigureGenerator

# Create multi-panel figure
fig_gen = PaperFigureGenerator(style='nature')
fig_gen.add_panel(data=df1, plot_type='bar', label='a')
fig_gen.add_panel(data=df2, plot_type='line', label='b')
fig_gen.annotate_significance(panel='a', x1=0, x2=1, p_value=0.001)
fig_gen.save('figure1.pdf', dpi=300)
```

## CLI Usage

```bash
# Create figure from data
python scientific_paper_figure_generator.py --data results.csv --plot bar --style nature --output figure1.pdf

# Multi-panel figure
python scientific_paper_figure_generator.py --panels panel_a.csv,panel_b.csv --layout 1x2 --output figure2.pdf
```
