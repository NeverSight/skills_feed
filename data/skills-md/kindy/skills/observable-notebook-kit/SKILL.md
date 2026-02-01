---
name: observable-notebook-kit
description: Create, edit, and build Observable Notebooks using Notebook Kit. Use when working with .html notebook files, generating static sites from notebooks, querying databases from notebooks, or using data loaders (Node.js/Python/R) in notebooks. Covers notebook file format, cell types, CLI commands, database connectors, and JavaScript API.
---

# Observable Notebook Kit

Observable Notebook Kit is an open-source CLI and Vite plugin for building static sites from Observable Notebooks.

## File Format

Notebooks are `.html` files with this structure:

```html
<!doctype html>
<notebook theme="air">
  <title>My Notebook</title>
  <script type="text/markdown">
    # Hello
  </script>
  <script type="module" pinned>
    1 + 2
  </script>
</notebook>
```

### `<notebook>` Attributes

- `theme` - colorway: `air` (default), `coffee`, `cotton`, `deep-space`, `glacier`, `ink`, `midnight`, `near-midnight`, `ocean-floor`, `parchment`, `slate`, `stark`, `sun-faded`
- `readonly` - disallow editing

### `<script>` (Cell) Attributes

- `type` - cell language (required)
- `pinned` - show source code
- `hidden` - suppress display
- `output` - variable name to expose (for non-JS cells)
- `database` - database name (SQL cells)
- `format` - output format (data loader cells)
- `id` - cell identifier

### Cell Types (`type` values)

| Type | Language |
|------|----------|
| `module` | JavaScript |
| `text/x-typescript` | TypeScript |
| `text/markdown` | Markdown |
| `text/html` | HTML |
| `application/sql` | SQL |
| `application/x-tex` | TeX/LaTeX |
| `text/vnd.graphviz` | DOT (Graphviz) |
| `application/vnd.node.javascript` | Node.js data loader |
| `text/x-python` | Python data loader |
| `text/x-r` | R data loader |

Use 4 spaces indentation inside `<script>` (auto-trimmed). Escape `</script>` as `<\/script>`.

## CLI Commands

Install: `npm add @observablehq/notebook-kit`

### Preview

```sh
notebooks preview --root docs
notebooks preview --root docs --template docs/custom.tmpl
```

### Build

```sh
notebooks build --root docs -- docs/*.html
```

Output goes to `.observable/dist`.

### Download

Convert Observable notebook URL to local HTML:

```sh
notebooks download https://observablehq.com/@d3/bar-chart > bar-chart.html
```

### Query

Run database query manually:

```sh
notebooks query --database duckdb 'SELECT 1 + 2'
```

## JavaScript in Notebooks

### Expression vs Program Cells

Expression cell (implicit display):
```js
1 + 2
```

Program cell (explicit display):
```js
const foo = 1 + 2;
display(foo);
```

### Key Built-ins

- `display(value)` - render value to cell output
- `view(input)` - display input, return value generator
- `FileAttachment("path")` - load local files (same/sub directory only)
- `invalidation` - promise for cleanup on re-run
- `visibility` - promise when cell visible
- `width` - current page width
- `now` - current time

### Standard Library

- `Inputs` - Observable Inputs
- `Plot` - Observable Plot
- `d3` - D3.js
- `htl`, `html`, `svg` - Hypertext Literal
- `tex`, `md` - tagged template literals

### Imports

```js
import lib from "npm:package-name";
import {fn} from "jsr:@scope/package";
```

### Reactivity

Top-level variables trigger re-runs. Promises auto-await; generators yield latest value.

```js
const x = view(Inputs.range([0, 100]));
```
```js
x ** 2  // re-runs when x changes
```

### Interpolation

Use `${...}` in Markdown/HTML cells:
```md
The answer is ${x * 2}.
```

## Database Connectors

See [references/databases.md](references/databases.md) for full configuration.

### Quick Setup

SQL cells use `database` attribute. Default is `duckdb` (in-memory).

```html
<script type="application/sql" database="duckdb" output="results">
  SELECT * FROM 'data.parquet'
</script>
```

### Supported Databases

- DuckDB (`@duckdb/node-api`)
- SQLite (Node.js 24+ built-in)
- Postgres (`postgres`)
- Snowflake (`snowflake-sdk`)
- BigQuery (`@google-cloud/bigquery`)
- Databricks (`@databricks/sql`)

Install drivers separately: `npm add @duckdb/node-api`

### Query Results

- Auto-cached in `.observable/cache`
- Re-run via Play button or Shift+Enter in Desktop
- Delete cache file to refresh in Notebook Kit

### Dynamic Queries

```js
const db = DatabaseClient("duckdb");
const data = await db.sql`SELECT * FROM t WHERE x = ${value}`;
```

## Data Loaders

Cells that run at build time via interpreter. Output cached in `.observable/cache`.

### Formats

Text: `text`, `json`, `csv`, `tsv`, `xml`
Binary: `arrow`, `parquet`, `blob`, `buffer`
Image: `png`, `jpeg`, `gif`, `webp`, `svg`
Other: `html`

### Node.js

```html
<script type="application/vnd.node.javascript" format="json" output="data">
  process.stdout.write(JSON.stringify({hello: "world"}));
</script>
```

Requires Node.js 22.12+. Sandboxed with read-only access to notebook directory.

### Python

```html
<script type="text/x-python" format="text" output="result">
  print("hello", end="")
</script>
```

Requires Python 3.12+. Uses `.venv` if present.

### R

```html
<script type="text/x-r" format="json" output="data">
  cat(jsonlite::toJSON(list(x = 1:3)))
</script>
```

## Page Templates

Custom templates wrap built notebooks:

```html
<!doctype html>
<html>
  <head>
    <style>@import url("observable:styles/index.css");</style>
  </head>
  <body>
    <main></main>  <!-- notebook renders here -->
  </body>
</html>
```

Use `--template path.tmpl` with CLI.

## Project Setup

Typical `package.json`:

```json
{
  "dependencies": {
    "@observablehq/notebook-kit": "^"
  },
  "scripts": {
    "docs:preview": "notebooks preview --root docs",
    "docs:build": "notebooks build --root docs -- docs/*.html"
  }
}
```

## Configuration Files

- `.observable/databases.json` - database configs (keep out of git)
- `.observable/cache/` - query/data loader results
- `.observable/dist/` - built site

Recommended `.gitignore`:
```
.observable
```
