---
name: spreadjs
description: "Creating & editing Excel workbooks via CLI — powered by SpreadJS"
---

# hsx CLI

## Setup

Before using `hsx`, check it's available. If not, install the package and its system dependencies (Cairo/Pango for `canvas`):

```bash
which hsx 2>/dev/null || npm install -g @hewliyang/headless-spreadjs
```

## Commands

All operations are bash calls. Formulas recalculate instantly (no sync step needed).

Global options:

- `--timeout <seconds>` (default: `30`)
- `--no-daemon` (run command directly bypassing daemon)

```bash
hsx create file.xlsx                                   # new workbook
hsx info file.xlsx                                     # workbook metadata
hsx get file.xlsx "Sheet1!A1:C10"                      # read cells → JSON
hsx csv file.xlsx "Sheet1!A1:C10" [--mode value|formula|both] [--formulas]
hsx set file.xlsx "Sheet1!A1:C3" '<json>'              # write cells
hsx clear file.xlsx "A1:C10" [--type all|styles]       # clear values (default), all, or styles
hsx search file.xlsx "term" [--sheet S] [--regex]      # find values
hsx copy file.xlsx "A1:C1" "A10:C10"                   # copy range (formulas + styles)
hsx diff left.xlsx right.xlsx [--inline-limit N] [--preview-limit N] # compare value + formula changes
hsx deps file.xlsx "Sheet1!A1" [--depth N|--recursive] # precedents (upstream)
hsx refs file.xlsx "Sheet1!A1" [--depth N|--recursive] [--max-formulas N] # dependents (downstream)
hsx sheet file.xlsx list|create|delete|rename          # manage sheets
hsx rc file.xlsx insert|delete|hide|freeze rows|columns [--ref R] [--count N]
hsx resize file.xlsx [--columns A:D] [--width N] [--rows 1:10] [--height N]
hsx objects file.xlsx [--sheet Name]                   # list charts, tables, pivots
hsx screenshot file.xlsx [ref] [-o out.png]            # screenshot workbook or range as PNG
hsx eval file.xlsx "code"                              # arbitrary JS
hsx daemon start|stop|status|flush                     # daemon lifecycle
```

References use A1 notation: `Sheet1!A1:C10`, `A1:C10` (active sheet), or `A1` (single cell).

Dependency tracing defaults to one-hop (`--depth 1`). Use `--depth N` for bounded multi-hop traversal or `--recursive` (shorthand for `--depth 50`).

## Write

```bash
hsx set file.xlsx "A1:B3" '[
  [{"value":"Name","style":{"fontStyle":{"bold":true}}}, {"value":"Qty","style":{"fontStyle":{"bold":true}}}],
  [{"value":"Alice"}, {"value":4}],
  [{"value":"Bob"}, {"formula":"=B2+1"}]
]'
```

Each cell: `{"value": ...}`, `{"formula": "=..."}`, optional `"style": {...}`.

`style` (SpreadJS-style):
- `fontStyle`: `{ bold?: boolean, italic?: boolean, underline?: boolean }`
- `fontSize`: CSS size string (e.g. `"12px"`)
- `fontFamily`
- `foreColor`
- `backColor`
- `hAlign`: SpreadJS `HorizontalAlign` enum value
- `formatter`

## Read

```bash
hsx get file.xlsx "A1:B3"
# → {"cells":{"A1":{"value":"Name","style":{"fontStyle":{"bold":true}}},"B3":{"value":5,"formula":"B2+1"}}, ...}

hsx csv file.xlsx "A1:B3"
# → Name,Qty
#    Alice,4
#    Bob,5

hsx csv file.xlsx "A1:B3" --mode formula
hsx csv file.xlsx "A1:B3" --mode both
```

## Screenshot

```bash
hsx screenshot file.xlsx
hsx screenshot file.xlsx "Sheet1!A1:F20"
hsx screenshot file.xlsx "Summary!A1:H30" -o summary.png
```

Screenshots render the full workbook (default) or a specific range to PNG.

## Search

```bash
hsx search file.xlsx "Alice"                     # case-insensitive across all sheets
hsx search file.xlsx "^Q[1-4]$" --regex          # regex
hsx search file.xlsx "Revenue" --sheet Summary    # single sheet
```

## Copy / Diff

```bash
hsx copy file.xlsx "A1:C1" "A1:C10"              # repeat header pattern down
hsx copy file.xlsx "Sheet1!A1:B5" "Sheet2!A1:B5"  # cross-sheet

hsx diff old.xlsx new.xlsx
hsx diff old.xlsx new.xlsx --inline-limit 1000 --preview-limit 50
```

`hsx diff` output is JSON with a top-level `summary` string plus counts (`changedCells`, `comparedCells`).

- `outputMode: "inline"` → full diff rows in `diffs`
- `outputMode: "tmpfile"` → preview rows in `diffs`, full NDJSON at `diffFile` (grep-friendly)

```bash
# inspect spilled diff
jq -r '.diffFile' diff-output.json
rg '"sheet":"Sheet1"' "$(jq -r '.diffFile' diff-output.json)"
```

## Dependency tracing (deps / refs)

```bash
# Direct precedents (what Sheet3!A1 reads)
hsx deps model.xlsx "Sheet3!A1"

# Multi-hop precedents
hsx deps model.xlsx "Sheet3!A1" --depth 2

# Direct dependents (what reads Sheet1!A1)
hsx refs model.xlsx "Sheet1!A1"

# Recursive dependents with a safety cap for large files
hsx refs model.xlsx "Sheet1!A1" --recursive --max-formulas 300000
```

Output is JSON and includes hop counts plus stats. This is best-effort for dynamic formulas (e.g. `INDIRECT`, `OFFSET`).

## Sheets

```bash
hsx sheet file.xlsx list
hsx sheet file.xlsx create "Revenue"
hsx sheet file.xlsx rename "Sheet1" "Data"
hsx sheet file.xlsx delete "OldSheet"
```

## Rows & Columns

```bash
hsx rc file.xlsx insert rows --ref 5 --count 3     # insert 3 rows at row 5
hsx rc file.xlsx delete columns --ref B --count 2  # delete columns B-C
hsx rc file.xlsx hide rows --ref 10                # hide row 10
hsx rc file.xlsx freeze rows --ref 1               # freeze top row
hsx rc file.xlsx unfreeze rows                     # unfreeze
```

## Resize

```bash
hsx resize file.xlsx --columns A:D --width 120
hsx resize file.xlsx --rows 1:1 --height 30
hsx resize file.xlsx --columns A --width 200 --sheet Revenue
```

## Eval (escape hatch)

For charts, sparklines, pivot tables, conditional formatting — anything the structured commands don't cover.

```bash
hsx eval file.xlsx "
  // Globals: workbook, sheet (active), GC, file, range(ref)
  sheet.charts.add('Revenue', GC.Spread.Sheets.Charts.ChartType.line,
    0, 120, 500, 300, 'A1:E6');
"
```

```bash
# A1 notation helper: range(ref) returns native SpreadJS Range
hsx eval file.xlsx "
  range('B2').value(96);                 // active sheet
  range("'Data Sheet'!C5").formula('B2*2'); // quoted sheet names supported
"
```

```bash
hsx eval file.xlsx "
  const data = workbook.getSheetFromName('Data');
  data.tables.add('SalesTable', 0, 0, 10, 4,
    GC.Spread.Sheets.Tables.TableThemes.medium2);
"
```

```bash
# Read values back
hsx eval file.xlsx "
  console.log('Sheets:', workbook.getSheetCount());
  return sheet.getValue(0, 0);
"
```

Stdin also works: `echo "return sheet.getValue(0,0)" | hsx eval file.xlsx`

## SpreadJS API Reference

When using `hsx eval`, you have access to the full SpreadJS API via the `GC` namespace. If you need to look up a specific API (enum values, method signatures, class properties), grep the type definitions:

```bash
# Find an enum or class
grep -n "enum ChartType" ./spreadjs.d.ts
grep -n "class Worksheet" ./spreadjs.d.ts

# Find methods on a class (read nearby lines for signatures)
grep -n "addRows\|deleteRows\|addColumns" ./spreadjs.d.ts

# Find available style properties
grep -n "fontWeight:\|foreColor:\|backColor:\|formatter:" ./spreadjs.d.ts

# Find conditional formatting APIs
grep -n "conditionalFormats\|ConditionalFormatting" ./spreadjs.d.ts
```

The file is at `./spreadjs.d.ts`. Use `grep -n` to find what you need, then `read` with offset to see full signatures and JSDoc examples.

## Best Practices

- Use formulas, not hardcoded computed values: `{"formula":"=SUM(A1:A9)"}` not `{"value":45}`
- Keep each `set` call focused; build incrementally across multiple calls
- Use `hsx get` or `hsx csv` to verify after writes
- Use `hsx deps` / `hsx refs` for repeatable lineage checks; use `eval` for custom one-offs
- Prefer uniform column widths; use empty columns for indentation
- Always specify units in headers: `Revenue ($mm)`, `Growth (%)`
