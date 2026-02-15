---
name: sheet-model
description: "Headless spreadsheet engine for financial modeling, data analysis, and scenario comparison. Use when: building financial models with ratios and what-if scenarios, computing derived values from tabular data with formulas, producing .xlsx files with live formulas (not static values) for human review, any task where the agent would otherwise write imperative code to manipulate numbers that a spreadsheet does naturally. Triggers: financial model, scenario analysis, ratio computation, balance sheet, P&L, what-if, sensitivity analysis, banking ratios, spreadsheet model, build a model, projection, forecast. Do NOT use for: simple CSV/Excel read/write (use the xlsx skill), chart-only tasks, or data volumes exceeding ~5000 rows."
---

# Sheet Model — Headless Spreadsheet for Agents

Build spreadsheet models programmatically using HyperFormula (headless computation engine) + ExcelJS (xlsx export). The spreadsheet IS both the computation and the deliverable.

## When to Use This vs the `xlsx` Skill

| Task | Use |
|------|-----|
| Read/write/edit existing .xlsx files | `xlsx` skill |
| Clean messy CSV data into a spreadsheet | `xlsx` skill |
| Build a financial model with formulas and scenarios | **this skill** |
| Produce a .xlsx where formulas are live and editable | **this skill** |
| Compute ratios, projections, what-if analysis | **this skill** |

## Setup

Install dependencies (run once):

```bash
cd {baseDir}
npm install
```

## Architecture

```text
Agent code (declarative)          SheetModel wrapper          Output
────────────────────────    ──────────────────────────    ──────────────
addRow('Revenue', 701384)   → HyperFormula (compute)     → Console table
addRow('EBITDA', formula)   → Named ranges auto-tracked  → .xlsx with live
addScenarioSheet(config)    → {Name} refs resolved       →   formulas +
getValue('EBITDA')          → Dependency graph updates    →   styling +
exportXlsx('model.xlsx')    → ExcelJS (export)           →   cond. format
```

## Core API

All code is ESM (`.mjs`). Import the wrapper:

```javascript
import { SheetModel } from '{baseDir}/lib/sheet-model.mjs';
const M = new SheetModel();
```

### Creating Sheets and Adding Data

```javascript
M.addSheet('Data');

// Section headers (bold, no value)
M.addSection('Data', 'BALANCE SHEET');
M.addBlank('Data');

// Data rows — addRow returns the A1 row number (use it in SUM ranges)
const r_first = M.addRow('Data', '  Revenue',    701384, { name: 'Revenue' });
const r_costs = M.addRow('Data', '  Costs',     -450000, { name: 'Costs' });
const r_other = M.addRow('Data', '  Other',        5000);

// Formula rows — use returned row numbers for SUM ranges
M.addRow('Data', '  EBITDA', `=SUM(B${r_first}:B${r_other})`, { name: 'EBITDA' });

// Formula rows using named references (auto-resolved by HyperFormula)
M.addRow('Data', '  Margin', '=EBITDA/Revenue', { name: 'Margin' });
```

> **Build top-to-bottom**: Names must be defined before any formula that references them. Define data rows first, then formulas.
>
> `addBlank()` and `addSection()` also return the A1 row number (useful for SUM range boundaries).

**When to use which formula style:**

| Need | Use | Why |
|------|-----|-----|
| `SUM`, `AVERAGE` over a range of rows | Row numbers: `` `=SUM(B${r_first}:B${r_last})` `` | Ranges need cell references; named expressions resolve to single cells |
| Arithmetic between specific cells | Named expressions: `'=EBITDA/Revenue'` | Cleaner, self-documenting |
| Mixed | Both: `` `=SUM(B${r1}:B${r5}) + Revenue` `` | Combine as needed |

**Never use named expressions as range endpoints**: `=SUM(Revenue:OtherIncome)` is undefined behavior.

### Named References

The `{ name: 'Revenue' }` option on `addRow`:

1. Registers a HyperFormula named expression (usable in any formula as `Revenue`)
2. Tracks the A1 row for internal cross-referencing
3. Exports as a proper Excel named range in .xlsx (via `cell.names`)

> ⚠️ **Names are global** across all sheets. Using `{ name: 'Revenue' }` in two different sheets overwrites the first. Use unique, prefixed names for multi-sheet models: `{ name: 'Rev2024' }`, `{ name: 'Rev2025' }`.

Name validation rules:

- Must be valid Excel names: start with a letter or underscore, no spaces
- **Cannot collide with Excel cell references**: names like `AC`, `PC`, `R1C1`, `A1` are rejected with a clear error
- Use descriptive names: `AdjPC`, `TotalAC`, `CurrentAssets` (not `AC`, `PC`, `CA`)

#### Cross-Sheet References (Data Sheets Only)

In `addRow` formulas, reference named cells on other data sheets with dot notation:

```javascript
M.addRow('CashFlow', '  From Operations', '={PnL.NetIncome} + {PnL.Depreciation}');
```

> This `{Sheet.Name}` syntax only works in `addRow` formulas, NOT in scenario output formulas. For scenarios, use named expressions (bare names) — they are global across sheets.

### Scenario Sheets

The core feature — define inputs, scenarios, and output formulas declaratively:

```javascript
M.addScenarioSheet('Scenarios', {
  inputs: [
    { name: 'GrowthRate', label: 'Revenue Growth %' },
    { name: 'CostCut',    label: 'Cost Reduction' },
  ],

  scenarios: [
    { label: 'Base Case',    values: {} },                              // all inputs = 0
    { label: 'Optimistic',   values: { GrowthRate: 0.10, CostCut: 50000 } },
    { label: 'Conservative', values: { GrowthRate: 0.03, CostCut: 20000 } },
  ],

  outputs: [
    // {InputName} → column-relative (B2, C2, D2...)
    // DataSheetName → named expression from Data sheet (fixed)
    // {PriorOutput} → column-relative ref to earlier output in this sheet
    { name: 'AdjRev',  label: 'Adj. Revenue',  format: 'number',
      formula: 'Revenue * (1 + {GrowthRate})' },
    { name: 'AdjCost', label: 'Adj. Costs',    format: 'number',
      formula: 'Costs + {CostCut}' },
    { name: 'AdjEBITDA', label: 'EBITDA',      format: 'number',
      formula: '{AdjRev} + {AdjCost}' },

    // Section separator
    { section: true, label: 'RATIOS' },

    // Ratio with conditional formatting thresholds
    { name: 'EBITDAm', label: 'EBITDA Margin', format: 'percent',
      formula: '{AdjEBITDA} / {AdjRev}',
      thresholds: { good: 0.15, bad: 0.08 } },

    // Inverted threshold (lower = better)
    { name: 'DebtEBITDA', label: 'Debt/EBITDA', format: 'ratio',
      formula: 'TotalDebt / {AdjEBITDA}',
      thresholds: { good: 2.5, bad: 4.0, invert: true } },
  ],
});
```

> **Do NOT call `addSheet()` before `addScenarioSheet()`** — it creates the sheet internally. Only use `addSheet()` for data sheets.
>
> **`addScenarioSheet` is a one-shot call.** You cannot add rows to a scenario sheet after creation. Include all inputs, outputs, and sections in the config object.
>
> **Every output you want to reference later MUST have a `name` property.** Without it, `{ThatOutput}` in a subsequent formula will throw an error.

#### Formula Reference Resolution in Scenarios

Inside `outputs[].formula`, references are resolved as follows:

| Syntax | Resolves to | Example |
|--------|-------------|---------|
| `{InputName}` | Column-relative cell ref to scenario input row | `{GrowthRate}` → `B2`, `C2`, `D2`... |
| `{OutputName}` | Column-relative cell ref to prior output in same sheet | `{AdjRev}` → `B7`, `C7`, `D7`... |
| `NamedExpr` | HyperFormula named expression (global, from any sheet) | `Revenue` → the named cell (fixed) |

**Important**: Bare names (no `{}`) are HyperFormula named expressions — they resolve to a **fixed** cell. `{Wrapped}` names resolve to **column-relative** cells within the Scenarios sheet.

> ⚠️ **Name collision rule**: If a scenario output `{name}` matches a Data sheet named expression, `{OutputName}` will resolve to the **Data sheet's fixed cell**, not the scenario output's column-relative cell. Always use **unique names** for scenario outputs. Example: Data sheet has `{ name: 'EBITDA' }`, scenario should use `{ name: 'AdjEBITDA' }` — never both `EBITDA`.

#### Output Formats

| Format | Excel numFmt | Display |
|--------|-------------|---------|
| `'number'` | `#,##0` | `1,234` |
| `'percent'` | `0.0%` | `12.5%` |
| `'ratio'` | `0.00"x"` | `3.14x` |
| `'decimal'` | `#,##0.00` | `1,234.56` |

#### Thresholds (Conditional Formatting)

```javascript
thresholds: { good: 0.15, bad: 0.08 }             // Higher is better (green >= 0.15, red < 0.08)
thresholds: { good: 2.5, bad: 4.0, invert: true }  // Lower is better (green <= 2.5, red > 4.0)
```

Colors: green (#E2EFDA), amber (#FFF2CC), red (#FCE4EC).

### Reading Computed Values

```javascript
// From Data sheet (by named ref)
const ebitda = M.getValue('Data', 'EBITDA');

// From Scenarios (by scenario index, 0-based)
const baseEBITDA = M.getScenarioValue('Scenarios', 0, 'AdjEBITDA');
const optEBITDA  = M.getScenarioValue('Scenarios', 1, 'AdjEBITDA');

// Raw cell access (sheet, col 0-indexed, a1Row 1-indexed)
const val = M.getCellValue('Data', 1, 5); // col B, row 5
```

> Use `getValue()` for data sheets, `getScenarioValue()` for scenario sheets. `getValue()` on a scenario sheet returns the first scenario's value (column B).

### Error Handling

```javascript
// Formula errors (division by zero, etc.) return CellError objects, not exceptions
const val = M.getValue('Data', 'Margin');
if (typeof val !== 'number' || !isFinite(val)) {
  console.error('Formula error:', val);
  // val might be: { type: 'DIV_BY_ZERO' }, { type: 'REF' }, { type: 'NAME' }, etc.
}

// To prevent #DIV/0! in formulas, guard with IF:
M.addRow('Data', '  Margin', '=IF(Revenue=0, 0, EBITDA/Revenue)', { name: 'Margin' });

// Reference errors throw immediately during addRow/addScenarioSheet
// → Always define named rows BEFORE formulas that reference them
// → Error messages include the row label and cell reference for easy debugging
```

Common causes of formula errors:

- Division by zero in ratios → guard with `IF(denominator=0, 0, numerator/denominator)`
- Misspelled named expression → throws immediately with clear error message
- Circular reference → throws immediately with row context

### Console Output

```javascript
M.printScenarios('Scenarios');
```

Prints a formatted table with emoji flags for threshold-based RAG status (🟢🟡🔴).

### Export to .xlsx

```javascript
await M.exportXlsx('output.xlsx', {
  creator: 'Agent Name',
  headerColor: '1B3A5C',  // Dark blue header background (ARGB hex, no #)
});
```

The exported file contains:

- **Live formulas** (not static values) — user can change inputs and see results update
- **Named ranges** on all named cells (visible in Excel's Name Manager)
- **Conditional formatting** on cells with thresholds (green/amber/red)
- **Frozen panes** — first column frozen on all sheets; header row also frozen on scenario sheets
- **Input cells** highlighted in light blue (#DAEEF3)
- **Section headers** in bold

> **Named ranges on scenario sheets** point to the **first scenario column** (column B). They exist for cross-sheet references in Excel, not for selecting all scenarios.

### Advanced Styling

For styling beyond what SheetModel provides, modify the file after export with ExcelJS:

```javascript
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const ExcelJS = require('exceljs');

await M.exportXlsx('model.xlsx');

const wb = new ExcelJS.Workbook();
await wb.xlsx.readFile('model.xlsx');
const ws = wb.getWorksheet('Data');
// Custom column widths, borders, fills, page setup, etc.
ws.pageSetup = { orientation: 'landscape', fitToPage: true, fitToWidth: 1 };
ws.getColumn(2).numFmt = '$#,##0';
await wb.xlsx.writeFile('model.xlsx');
```

## Complete Example: Financial Model with Scenarios

```javascript
import { SheetModel } from '{baseDir}/lib/sheet-model.mjs';

const M = new SheetModel();
M.addSheet('Data');

// ── Balance Sheet ──
M.addSection('Data', 'BALANCE SHEET');
M.addBlank('Data');
const r1 = M.addRow('Data', '  Cash',           50000, { name: 'Cash' });
const r2 = M.addRow('Data', '  Receivables',   120000, { name: 'Receivables' });
const r3 = M.addRow('Data', '  Inventory',      30000);
M.addRow('Data', '  Current Assets', `=SUM(B${r1}:B${r3})`, { name: 'CurrentAssets' });

M.addBlank('Data');
const r4 = M.addRow('Data', '  Payables',       80000, { name: 'Payables' });
const r5 = M.addRow('Data', '  Short-term Debt', 40000, { name: 'STDebt' });
M.addRow('Data', '  Current Liabilities', `=SUM(B${r4}:B${r5})`, { name: 'CurrentLiab' });

M.addBlank('Data');
M.addRow('Data', '  Equity', 200000, { name: 'Equity' });
M.addRow('Data', '  Long-term Debt', 150000, { name: 'LTDebt' });

// ── P&L ──
M.addBlank('Data');
M.addSection('Data', 'INCOME STATEMENT');
M.addBlank('Data');
const p1 = M.addRow('Data', '  Revenue',         500000, { name: 'Revenue' });
const p2 = M.addRow('Data', '  COGS',           -200000);
const p3 = M.addRow('Data', '  Operating Exp',  -150000);
const p4 = M.addRow('Data', '  Depreciation',    -30000, { name: 'Depreciation' });
M.addRow('Data', '  Operating Income', `=SUM(B${p1}:B${p4})`, { name: 'OpIncome' });
M.addRow('Data', '  Interest Expense',  -15000, { name: 'IntExp' });
M.addRow('Data', '  Net Income', '=OpIncome+IntExp', { name: 'NetIncome' });

// ── Scenarios ──
M.addScenarioSheet('Analysis', {
  inputs: [
    { name: 'RevGrowth',  label: 'Revenue Growth' },
    { name: 'DebtPaydown', label: 'Debt Paydown' },
  ],
  scenarios: [
    { label: 'As-Is',       values: {} },
    { label: 'Growth 10%',  values: { RevGrowth: 0.10 } },
    { label: 'Deleverage',  values: { RevGrowth: 0.05, DebtPaydown: 50000 } },
  ],
  outputs: [
    { name: 'AdjRev',   label: 'Adj. Revenue',      format: 'number',
      formula: 'Revenue * (1 + {RevGrowth})' },
    { name: 'AdjEBITDA', label: 'EBITDA',            format: 'number',
      formula: '{AdjRev} + (Revenue - OpIncome + Depreciation) / Revenue * {AdjRev} * -1 + ABS(Depreciation)' },
    { name: 'TotalDebt', label: 'Total Debt',        format: 'number',
      formula: 'LTDebt + STDebt - {DebtPaydown}' },
    { name: 'NetDebt',   label: 'Net Debt',          format: 'number',
      formula: '{TotalDebt} - Cash' },

    { section: true, label: 'KEY RATIOS' },
    { name: 'CurrRatio', label: 'Current Ratio',     format: 'ratio',
      formula: 'CurrentAssets / CurrentLiab',
      thresholds: { good: 1.5, bad: 1.0 } },
    { name: 'DebtEBITDA', label: 'Debt/EBITDA',      format: 'ratio',
      formula: '{TotalDebt} / {AdjEBITDA}',
      thresholds: { good: 2.5, bad: 4.0, invert: true } },
    { name: 'ICR',  label: 'Interest Coverage',      format: 'ratio',
      formula: '{AdjEBITDA} / ABS(IntExp)',
      thresholds: { good: 3.0, bad: 1.5 } },
    { name: 'EBITDAm', label: 'EBITDA Margin',       format: 'percent',
      formula: '{AdjEBITDA} / {AdjRev}',
      thresholds: { good: 0.20, bad: 0.10 } },
    { name: 'ROE',  label: 'Return on Equity',       format: 'percent',
      formula: 'NetIncome / Equity',
      thresholds: { good: 0.12, bad: 0.05 } },
  ],
});

// Use
M.printScenarios('Analysis');
console.log('EBITDA (Growth):', M.getScenarioValue('Analysis', 1, 'AdjEBITDA'));
await M.exportXlsx('financial-model.xlsx');
```

## Recipe: Loan Amortization

```javascript
const M = new SheetModel();
M.addSheet('Loan');

M.addSection('Loan', 'LOAN PARAMETERS');
M.addBlank('Loan');
M.addRow('Loan', 'Principal',    500000, { name: 'Principal' });
M.addRow('Loan', 'Annual Rate',  0.05,   { name: 'AnnualRate' });
M.addRow('Loan', 'Years',        20,     { name: 'Years' });
M.addRow('Loan', 'Monthly Rate', '=AnnualRate/12', { name: 'MonthlyRate' });
M.addRow('Loan', 'Periods',      '=Years*12',      { name: 'Periods' });
M.addBlank('Loan');
// PMT returns negative (cash outflow) — negate for display
M.addRow('Loan', 'Monthly Payment', '=-PMT(MonthlyRate, Periods, Principal)', { name: 'Payment' });
M.addRow('Loan', 'Total Interest',  '=Payment*Periods - Principal', { name: 'TotalInterest' });

await M.exportXlsx('loan-model.xlsx');
```

## Available Formulas

HyperFormula supports **395 built-in functions** including:

- **Math**: SUM, AVERAGE, MIN, MAX, ABS, ROUND, CEILING, FLOOR, MOD, POWER, SQRT, LOG
- **Financial**: PMT, FV, NPER, PV, RATE, NPV, XNPV
- **Logical**: IF, IFS, AND, OR, NOT, SWITCH, IFERROR
- **Lookup**: VLOOKUP, HLOOKUP, INDEX, MATCH
- **Statistical**: COUNT, COUNTA, COUNTIF, SUMIF, SUMIFS, AVERAGEIF
- **Text**: CONCATENATE, LEFT, RIGHT, MID, LEN, TRIM, UPPER, LOWER, TEXT
- **Date**: DATE, YEAR, MONTH, DAY, TODAY, DATEDIF, EOMONTH

Full list: https://hyperformula.handsontable.com/guide/built-in-functions.html

## ExcelJS Gotchas (Critical)

These bugs were discovered empirically and MUST be followed:

1. **Named ranges**: Use `cell.names = ['Name']`, NEVER `definedNames.add()` or `addEx()`.
   - `add()` tries to parse the name as a cell ref → crashes on names like `InvFinCP`
   - `addEx()` silently doesn't persist to the .xlsx file
   - SheetModel handles this automatically — don't use ExcelJS definedNames directly

2. **Formula prefix**: HyperFormula `getCellFormula()` returns `"=SUM(...)"` with leading `=`.
   ExcelJS expects `{ formula: 'SUM(...)' }` without `=`. Double `=` causes `#NAME?` errors.
   SheetModel handles this automatically.

3. **Formula language**: .xlsx always stores formulas in English (`SUM`, `ABS`, `IF`).
   Excel translates to locale on display. Always write English function names.

## Limitations

- **Row limit**: Practical limit ~5,000 rows. For larger datasets, use pandas/openpyxl via the `xlsx` skill.
- **Single value column on data sheets**: `addRow` writes to columns A (label) and B (value) only. For multi-period models (Year 1, Year 2, Year 3), use a scenario sheet where each "scenario" is a period, or use direct HyperFormula API (`M.hf.setCellContents(...)`) for additional columns.
- **Data sheet formatting**: All values in data sheets are formatted as integers (`#,##0`). For percentages, ratios, or decimals, compute them in a scenario sheet output with the appropriate `format` option, or post-process with ExcelJS (see Advanced Styling).
- **No charts**: HyperFormula/ExcelJS can't create Excel charts. Add charts manually or use a separate tool.
- **No pivot tables**: Use pandas for pivot-style analysis.
- **Scenario columns**: Maximum **25** scenarios per sheet (columns B–Z). For readability, keep to 10 or fewer.
- **Named range naming**: Names that match Excel cell/column references (e.g., `AC`, `R1C1`, `A1`) are rejected automatically. Use descriptive names.
- **Data sheet formulas in .xlsx**: The exported Excel formula is the original text, not extracted from HyperFormula. Stick to bare named expressions (e.g., `Revenue`, `OpIncome`) and A1 refs via template literals (e.g., `` `=SUM(B${r1}:B${r3})` ``).
