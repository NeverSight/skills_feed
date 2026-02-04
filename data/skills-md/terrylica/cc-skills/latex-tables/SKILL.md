---
name: latex-tables
description: LaTeX tables with tabularray package. TRIGGERS - LaTeX table, tabularray, fixed-width columns, table alignment.
allowed-tools: Read, Edit, Bash
---

# LaTeX Tables with tabularray

## When to Use This Skill

Use this skill when:

- Creating tables with fixed-width columns
- Formatting complex table layouts
- Need precise column alignment
- Migrating from tabular/tabularx/longtable/booktabs
- Troubleshooting table overflow issues

## Quick Reference

## Why tabularray?

Modern LaTeX3 package (replaces old solutions):

- Fixed-width columns with proper alignment
- Clean, consistent syntax
- Replaces: `tabular`, `tabularx`, `longtable`, `booktabs`
- Better performance than legacy packages
- Part of TeX Live 2025

---

## Installation

```bash
# Check if installed
kpsewhich tabularray.sty

# If not found, install:
sudo tlmgr install tabularray
```

## Basic Usage

```latex
\documentclass{article}
\usepackage{tabularray}  % Modern table package

\begin{document}
% Simple table
\begin{tblr}{colspec={ccc}, hlines, vlines}
  Header 1 & Header 2 & Header 3 \\
  Data 1   & Data 2   & Data 3   \\
\end{tblr}
\end{document}
```

---

## Quick Reference Card

```latex
% Minimal table
\begin{tblr}{colspec={ccc}}
  A & B & C \\
\end{tblr}

% With all lines
\begin{tblr}{colspec={ccc}, hlines, vlines}
  A & B & C \\
\end{tblr}

% Fixed widths
\begin{tblr}{colspec={Q[2cm] Q[3cm] Q[2cm]}, hlines}
  A & B & C \\
\end{tblr}

% Bold header
\begin{tblr}{
  colspec={ccc},
  row{1}={font=\bfseries}
}
  Header & Header & Header \\
  Data   & Data   & Data   \\
\end{tblr}
```

---

## Best Practices

1. Use Q[width] for fixed columns instead of p{width}
2. Specify widths explicitly when text might overflow
3. Use X for flexible columns that should expand
4. Style headers with row{1} instead of manual formatting
5. Use colspec for column properties, not inline commands
6. Check package version: `kpsewhich tabularray.sty` (should be recent)

---

## Reference Documentation

For detailed information, see:

- [Table Patterns](./references/table-patterns.md) - 5 common table patterns with examples
- [Column Specification](./references/column-spec.md) - Alignment options and width control
- [Lines and Borders](./references/lines-borders.md) - All lines, selective lines, thick lines
- [Troubleshooting](./references/troubleshooting.md) - Table too wide, text not wrapping, alignment issues
- [Migration](./references/migration.md) - Migrating from tabular and tabularx

**Official Docs**: Run `texdoc tabularray` for complete package documentation

**See Also**:

- Use `latex/setup` skill for installing tabularray package
- Use `latex/build` skill for compilation workflows

---

## Troubleshooting

| Issue                    | Cause                     | Solution                                            |
| ------------------------ | ------------------------- | --------------------------------------------------- |
| Package not found        | tabularray not installed  | `sudo tlmgr install tabularray`                     |
| Table too wide           | Fixed widths exceed page  | Use smaller Q[width] values or X for flexible       |
| Text not wrapping        | Column spec missing width | Use Q[width] instead of c/l/r for wrapping          |
| Alignment issues         | Mixed column types        | Ensure all columns have consistent spec             |
| Compile error on colspec | Invalid syntax            | Check for missing commas or typos in column spec    |
| hlines not appearing     | Missing from spec         | Add `hlines` to the spec: `{colspec={...}, hlines}` |
| Row style not applied    | Wrong row index           | Remember row{1} is first row (1-indexed)            |
| Package version too old  | TeX Live outdated         | `sudo tlmgr update --self --all`                    |
