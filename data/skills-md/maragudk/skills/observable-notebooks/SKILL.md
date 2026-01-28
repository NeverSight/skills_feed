---
name: observable-notebooks
description: Guide for creating Observable Notebooks 2.0, the open-source notebook system for interactive data visualization and exploration. Use this skill when creating, editing, or building Observable notebooks.
license: MIT
---

# Observable Notebooks 2.0

## Overview

Observable Notebooks 2.0 is an open-source notebook system for creating interactive documents that combine code, data, and visualization. It features an HTML-based file format, vanilla JavaScript (no more Observable-specific dialect), and a CLI for building static sites.

## When to Use This Skill

Use this skill when:
- Creating new Observable notebooks
- Editing existing notebook files
- Building and previewing notebooks locally
- Working with Observable's standard library (Plot, Inputs, D3)

## Installation

Install Notebook Kit as a local dependency:

```bash
npm add @observablehq/notebook-kit
```

## CLI Commands

### Preview (Development Server)

```bash
notebooks preview notebook.html
notebooks preview --root ./notebooks
notebooks preview --template template.tmpl notebook.html
```

Starts a development server with live reload for editing notebooks.

### Build (Static Site Generation)

```bash
notebooks build notebook.html
notebooks build --root ./notebooks -- *.html
```

Generates static HTML in `.observablehq/dist/` by default.

### Download (Convert Existing Notebooks)

```bash
notebooks download https://observablehq.com/@d3/bar-chart > bar-chart.html
```

Downloads an existing Observable notebook to the local HTML format.

### Query (Database Queries)

```bash
notebooks query --database duckdb 'SELECT * FROM data'
```

Execute and cache database query results.

## File Format

Notebooks are HTML files with a `<notebook>` root element:

```html
<notebook>
  <title>My Notebook</title>

  <script type="text/markdown">
    # Introduction

    This is a markdown cell with interpolation: ${1 + 1}
  </script>

  <script type="module">
    const data = [1, 2, 3, 4, 5];
    display(data);
  </script>

  <script type="module">
    import * as Plot from "npm:@observablehq/plot";
    display(Plot.barY(data).plot());
  </script>

</notebook>
```

Use four-space indentation inside `<script>` tags (trimmed during parsing).

## Cell Types

| Type | Script Attribute | Description |
|------|------------------|-------------|
| JavaScript | `type="module"` | Standard ES modules, `display()` for output |
| TypeScript | `type="text/x-typescript"` | TypeScript with type checking |
| Markdown | `type="text/markdown"` | CommonMark with `${...}` interpolation |
| HTML | `type="text/html"` | HTML with auto-escaped interpolation |
| SQL | `type="application/sql"` | Database queries |
| TeX | `type="application/x-tex"` | LaTeX equations |
| Graphviz | `type="text/vnd.graphviz"` | DOT diagram notation |
| Python | `type="text/x-python"` | Python code (data loaders) |
| R | `type="text/x-r"` | R code (data loaders) |
| Node.js | `type="application/vnd.node.javascript"` | Node.js data loaders |

## Cell Attributes

- `pinned` - Displays the cell's source code alongside output
- `hidden` - Suppresses implicit display (cell still runs)
- `id="123"` - Unique positive integer for stable editing
- `database="mydb"` - Specifies database for SQL cells
- `format="json"` - Output format for data loaders
- `output="varname"` - Exposes values from non-JavaScript cells

Example:

```html
<script type="module" pinned>
  const x = 42;
  display(x);
</script>

<script type="application/sql" database="duckdb" output="results">
  select * from data limit 10
</script>
```

## Reactivity

Cells run automatically when referenced variables change, like a spreadsheet:

```html
<script type="module">
  const a = 10;
</script>

<script type="module">
  const b = 20;
</script>

<script type="module">
  // This cell re-runs whenever a or b changes
  display(a + b);
</script>
```

Top-level variables declared in one cell are accessible throughout the notebook.

## Standard Library

### Core Functions

- `display(value)` - Render values to the page
- `view(input)` - Display inputs and return value generators
- `FileAttachment(path)` - Reference local files
- `invalidation` - Promise for cleanup on cell re-run
- `visibility` - Wait for cell to become visible
- `width` - Current page width (reactive)
- `now` - Current timestamp (reactive)

### Preloaded Libraries

All available without explicit imports:

- **Inputs** - Form controls (`Inputs.range()`, `Inputs.select()`, etc.)
- **Plot** - Charting library (`Plot.barY()`, `Plot.line()`, etc.)
- **D3** - Data visualization utilities
- **htl** - Hypertext Literal for safe DOM creation
- **tex** - LaTeX rendering

### Using npm Packages

```html
<script type="module">
  import confetti from "npm:canvas-confetti";
  confetti();
</script>
```

## Observable Inputs

Create interactive controls that automatically update dependent cells:

```html
<script type="module">
  const gain = view(Inputs.range([0, 11], {
    value: 5,
    step: 0.1,
    label: "Gain"
  }));
</script>

<script type="module">
  // This cell re-runs when the slider changes
  display(`Current gain: ${gain}`);
</script>
```

Available inputs:
- `Inputs.button(label)` - Click trigger
- `Inputs.toggle({label, value})` - Boolean switch
- `Inputs.checkbox(options, {label})` - Multi-select
- `Inputs.radio(options, {label})` - Single select
- `Inputs.range([min, max], {value, step, label})` - Numeric slider
- `Inputs.select(options, {label, multiple})` - Dropdown
- `Inputs.text({label, placeholder})` - Text input
- `Inputs.textarea({label, rows})` - Multi-line text
- `Inputs.date({label, value})` - Date picker
- `Inputs.color({label, value})` - Color picker
- `Inputs.file({label, accept})` - File upload
- `Inputs.search(data, {label})` - Search/filter data
- `Inputs.table(data, {columns})` - Interactive data table

## Observable Plot

Create charts with the grammar of graphics:

```html
<script type="module">
  const data = [
    {year: 2020, value: 10},
    {year: 2021, value: 20},
    {year: 2022, value: 15}
  ];

  display(Plot.plot({
    marks: [
      Plot.barY(data, {x: "year", y: "value"})
    ]
  }));
</script>
```

Common marks:
- `Plot.dot()` - Scatter plots
- `Plot.line()` - Line charts
- `Plot.barX()`, `Plot.barY()` - Bar charts
- `Plot.areaY()` - Area charts
- `Plot.rectY()` - Histograms
- `Plot.text()` - Labels
- `Plot.ruleX()`, `Plot.ruleY()` - Reference lines

## Loading Data

### Local Files

```html
<script type="module">
  const data = await FileAttachment("data.csv").csv({typed: true});
  display(Inputs.table(data));
</script>
```

Supported formats: `.csv()`, `.json()`, `.tsv()`, `.text()`, `.blob()`, `.arrayBuffer()`, `.image()`, `.xlsx()`, `.zip()`.

### Remote Data

```html
<script type="module">
  const response = await fetch("https://api.example.com/data");
  const data = await response.json();
  display(data);
</script>
```

### Database Queries

```html
<script type="application/sql" database="duckdb" output="results">
  select * from "data.parquet" limit 100
</script>

<script type="module">
  display(Inputs.table(results));
</script>
```

## Themes

Set a theme on the notebook element:

```html
<notebook theme="dark">
  ...
</notebook>
```

Built-in themes: `air`, `coffee`, `cotton`, `deep-space`, `glacier`, `ink`, `midnight`, `near-midnight`, `ocean-floor`, `parchment`, `slate`, `stark`, `sun-faded`.

## Page Templates

Create custom templates for consistent layouts:

```html
<!-- template.tmpl -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="generator" content="Observable Notebook Kit">
  <title>My Site</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header>My Site Header</header>
  <main></main>
  <footer>My Site Footer</footer>
</body>
</html>
```

Use with: `notebooks build --template template.tmpl -- *.html`

The `<main>` element receives the rendered notebook cells.

## Example: Complete Notebook

```html
<notebook theme="slate">
  <title>Sales Dashboard</title>

  <script type="text/markdown">
    # Sales Dashboard

    Interactive visualization of quarterly sales data.
  </script>

  <script type="module">
    const sales = await FileAttachment("sales.csv").csv({typed: true});
  </script>

  <script type="module">
    const quarter = view(Inputs.select(
      ["Q1", "Q2", "Q3", "Q4"],
      {label: "Quarter", value: "Q1"}
    ));
  </script>

  <script type="module">
    const filtered = sales.filter(d => d.quarter === quarter);

    display(Plot.plot({
      title: `Sales for ${quarter}`,
      marks: [
        Plot.barY(filtered, {
          x: "product",
          y: "revenue",
          fill: "category"
        }),
        Plot.ruleY([0])
      ]
    }));
  </script>

  <script type="module" pinned>
    display(Inputs.table(filtered, {
      columns: ["product", "category", "revenue", "units"]
    }));
  </script>

</notebook>
```

## Resources

- [Notebook Kit Documentation](https://observablehq.com/notebook-kit/)
- [System Guide](https://observablehq.com/notebook-kit/system-guide)
- [Observable Plot](https://observablehq.com/plot/)
- [GitHub Repository](https://github.com/observablehq/notebook-kit)
