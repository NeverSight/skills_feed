---
name: marimo
description: Guide for creating and working with marimo notebooks, the reactive Python notebook that stores as pure .py files. This skill should be used when creating, editing, running, or deploying marimo notebooks.
license: MIT
---

# marimo

## Overview

marimo is an open-source reactive Python notebook that reinvents notebooks as reproducible, interactive, and shareable Python programs. Unlike traditional Jupyter notebooks, marimo notebooks:

- Store as pure `.py` files (Git-friendly, no JSON)
- Execute reactively (like a spreadsheet)
- Run as scripts or deploy as web apps
- Prevent bugs through automatic dependency tracking

## Installation

```bash
pip install marimo                    # Basic
pip install marimo[recommended]       # With extras
pip install marimo[sql]               # With SQL support

marimo tutorial intro                 # Start tutorial
```

## CLI Commands

```bash
# Edit
marimo edit                           # New notebook
marimo edit notebook.py               # Edit existing
marimo edit --watch --sandbox         # Watch files, isolate deps

# Run as app
marimo run notebook.py                # Read-only app
marimo run notebook.py --watch        # Auto-reload on changes

# Run as script
python notebook.py

# Create from prompt
marimo new "analyze sales data"

# Convert
marimo convert notebook.ipynb -o notebook.py

# Export
marimo export html notebook.py -o output.html
marimo export html-wasm notebook.py -o output.html  # Browser-executable
```

## Key Concepts

### Reactivity

Running a cell automatically runs all cells that depend on it. Execution order is determined by variable dependencies (DAG), not cell position.

### Cell Rules

1. Each global variable must be defined in exactly one cell
2. Mutations like `list.append()` aren't tracked; reassign instead
3. If mutating is needed, do it in the same cell as the declaration

### File Format

Notebooks are pure Python files with marimo decorators:

```python
import marimo
app = marimo.App()

@app.cell
def _():
    import marimo as mo
    return (mo,)

@app.cell
def _(mo):
    mo.md("# My Notebook")
    return ()
```

## API Reference

Detailed documentation for each API is available in the `references/` directory. Consult these files for comprehensive examples and parameters.

### Core

| API | Reference File | Description |
|-----|----------------|-------------|
| Markdown | `references/markdown.md` | `mo.md()` for rich text, LaTeX, icons |
| HTML | `references/html.md` | `mo.Html`, `mo.as_html()`, styling |
| Outputs | `references/outputs.md` | `mo.output.append()`, console redirection |

### UI Elements

| API | Reference File | Description |
|-----|----------------|-------------|
| Inputs | `references/inputs.md` | Sliders, text, dropdowns, tables, forms, etc. |
| Layouts | `references/layouts.md` | `mo.hstack`, `mo.vstack`, tabs, accordion, etc. |
| Media | `references/media.md` | Images, audio, video, PDF, downloads |
| Plotting | `references/plotting.md` | Altair, Plotly, matplotlib integration |
| Diagrams | `references/diagrams.md` | Mermaid diagrams |
| Status | `references/status.md` | Progress bars, spinners |

### Data

| API | Reference File | Description |
|-----|----------------|-------------|
| SQL | `references/sql.md` | `mo.sql()` for database and DataFrame queries |

### Advanced

| API | Reference File | Description |
|-----|----------------|-------------|
| Control Flow | `references/control-flow.md` | `mo.stop()`, conditional execution |
| State | `references/state.md` | `mo.state()` for UI synchronization |
| Caching | `references/caching.md` | `@mo.cache`, `@mo.persistent_cache` |
| Query Params | `references/query-params.md` | `mo.query_params()` for URL state |
| CLI Args | `references/cli-args.md` | `mo.cli_args()` for script arguments |
| Watch | `references/watch.md` | `mo.watch.file()` for reactive file monitoring |
| App | `references/app.md` | Embedding notebooks, `mo.app_meta()` |
| Cell | `references/cell.md` | Cross-notebook execution, testing |

## Quick Examples

### Basic UI

```python
import marimo as mo

slider = mo.ui.slider(0, 100, value=50, label="Threshold")
slider

# In another cell
mo.md(f"Selected value: **{slider.value}**")
```

### Interactive Table

```python
table = mo.ui.table(df, selection="multi")
table

# In another cell
selected = table.value  # Selected rows as DataFrame
```

### SQL Query

```python
result = mo.sql(f"SELECT * FROM {df} WHERE value > {threshold.value}")
```

### Conditional Execution

```python
mo.stop(form.value is None, mo.md("Submit the form to continue"))
# Rest of cell runs only after form submission
```

## Running as Apps

```bash
marimo run notebook.py                    # Local app
marimo export html-wasm notebook.py       # Static WASM app
```

Layout options: Vertical (default), Grid (drag-drop in editor), Slides.

## Best Practices

- **Reactivity**: Declare and mutate variables in the same cell
- **Performance**: Use `@mo.cache` for expensive computations
- **UI Gating**: Use `mo.stop()` to prevent expensive ops until ready
- **State**: Avoid `mo.state()` unless synchronizing multiple UI elements
- **Organization**: Cell position doesn't matter; organize for readability

## Resources

- [Documentation](https://docs.marimo.io/)
- [GitHub](https://github.com/marimo-team/marimo)
- [Examples Gallery](https://marimo.io/gallery)
