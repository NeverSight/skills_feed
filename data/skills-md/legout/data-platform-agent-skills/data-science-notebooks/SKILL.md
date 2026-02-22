---
name: data-science-notebooks
description: "Interactive notebooks for data science: Jupyter, JupyterLab, and marimo. Use for exploratory analysis, reproducible research, documentation, and sharing insights with stakeholders."
dependsOn: ["@data-science-eda", "@data-engineering-core"]
---

# Interactive Notebooks

Use this skill for creating reproducible, well-structured notebooks for data exploration, analysis, and communication.

## When to use this skill

- **Exploratory analysis** — interactively investigate data
- **Reproducible research** — document methodology with code and results
- **Teaching/demos** — explain concepts with executable examples
- **Stakeholder communication** — share insights with narrative + visuals
- **Prototyping** — quickly iterate on data transformations or models

## Tool selection

| Tool | Best For | Key Feature |
|---|---|---|
| **JupyterLab** | Traditional data science, extensions ecosystem | Full IDE experience |
| **marimo** | Reproducible notebooks, reactive execution | Python-native, version-control friendly |
| **VS Code + Jupyter** | IDE-native notebook experience | Intellisense, debugging, git integration |
| **Google Colab** | Cloud GPUs, sharing, collaboration | Free TPU/GPU, easy sharing |

## Core principles

### 1) Structure for readability

```markdown
# Title: Clear project/question description

## Setup
Imports and configuration

## Data Loading
Load and validate data

## Analysis
- Subsection per question/hypothesis
- Clear markdown explanations
- Visualizations with interpretations

## Conclusions
Key findings and next steps
```

### 2) Ensure reproducibility

```python
# Set random seeds
import numpy as np
import random

np.random.seed(42)
random.seed(42)

# Pin versions in requirements.txt or environment.yml
# requirements.txt example:
# pandas==2.1.0
# scikit-learn==1.3.0
```

### 3) Keep cells focused

- One concept per cell
- Avoid cells with >50 lines
- Refactor helper functions to `.py` files

### 4) Never hardcode secrets

```python
# ✅ Use environment variables
import os

api_key = os.environ.get("OPENAI_API_KEY")

# ❌ Never do this
api_key = "sk-abc123..."
```

## Jupyter best practices

### Magic commands (Jupyter/IPython)

```python
# In a Jupyter cell (these are IPython magics, not standard Python)
# Auto-reload modules during development
# %load_ext autoreload
# %autoreload 2

# Timing
# %timeit function_call()

# Debugging
# %debug

# Environment info (requires watermark package)
# %watermark -v -m -p numpy,pandas,sklearn
```

### Clean outputs before git

```bash
# Using nbstripout
pip install nbstripout
nbstripout --install

# Or pre-commit hook
pip install pre-commit
pre-commit install
```

## marimo advantages

### Reactive execution

```python
# marimo notebook - cells auto-recompute when dependencies change
import marimo as mo

slider = mo.ui.slider(1, 100, value=50)
slider  # Display the slider

# This cell re-runs automatically when slider changes
df_filtered = df[df['value'] > slider.value]
```

### Version control friendly

- Pure Python (`.py` files)
- No output blobs in git
- Readable diffs

### Convert Jupyter to marimo

```bash
marimo convert notebook.ipynb -o notebook.py
```

## Common anti-patterns

- ❌ Running cells out of order (Jupyter)
- ❌ Giant cells with mixed concerns
- ❌ Hardcoded file paths
- ❌ No markdown explanations
- ❌ Committing large output files
- ❌ Inline data (use data/ folder)

## Progressive disclosure

- `../references/jupyter-advanced.md` — Widgets, extensions, debugging
- `../references/marimo-guide.md` — Reactive patterns, UI components
- `../references/notebook-testing.md` — Unit tests for notebook code
- `../references/sharing-publishing.md` — nbconvert, Quarto, Voilà

## Related skills

- `@data-science-eda` — Exploration patterns for notebooks
- `@data-science-interactive-apps` — Convert notebooks to apps
- `@data-engineering-core` — Production-ready code patterns

## References

- [Jupyter Documentation](https://docs.jupyter.org/)
- [marimo Documentation](https://docs.marimo.io/)
- [nbstripout](https://github.com/kynan/nbstripout)
- [Quarto](https://quarto.org/) (publishing)
