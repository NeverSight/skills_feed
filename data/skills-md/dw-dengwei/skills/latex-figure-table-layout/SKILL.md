---
name: latex-figure-table-layout
description: Professional LaTeX figure and table positioning. Handle float placement, subfigure/subtable layouts, side-by-side arrangements, and cross-column figures. Does NOT adjust sizes, widths, or scaling.
version: 1.0.0
author: User
license: Apache-2.0
tags: [LaTeX, Figures, Tables, Positioning, Layout, Float]
---

# LaTeX Figure and Table Layout

Expert guidance for positioning figures and tables in LaTeX documents. This skill handles float placement, subfigure arrangements, side-by-side layouts, and cross-column positioning.

## When to Use This Skill

Use this skill when:
- Adjusting figure/table position parameters (`[h]`, `[t]`, `[b]`, `[p]`)
- Arranging multiple figures/tables in subfigures
- Creating side-by-side figure or figure+table layouts
- Fixing float positioning issues (drifting, page alone)
- Working with cross-column figures (`figure*`, `table*`)

**NOTE**: This skill does NOT modify sizes, column widths, or scaling. Only positioning.

---

## Float Position Parameters

### Position Specifiers

| Parameter | Meaning | Priority |
|-----------|---------|----------|
| `[h]` | Here (exact location) | Highest |
| `[t]` | Top of page | Medium |
| `[b]` | Bottom of page | Medium |
| `[p]` | Separate float page | Lowest |
| `[!]` | Override LaTeX defaults | - |

### Recommended Order

```latex
\begin{figure}[htbp]  % Recommended: try here, then top, bottom, then float page
\end{figure}
```

### Strong Recommendations

```latex
\begin{figure}[!htbp]  % Force LaTeX to respect your order
\end{figure}
```

**Best Practice**: Use `[htbp]` or `[!htbp]` for most cases. Avoid single `[h]` which can cause float to drift.

---

## Subfigure Layout with subcaption

### Basic Subfigures (2 side-by-side)

```latex
\usepackage{subcaption}

\begin{figure}[htbp]
  \centering
  \begin{subfigure}[b]{0.45\textwidth}
    \includegraphics[width=\textwidth]{figure1.pdf}
    \caption{First figure}
    \label{fig:first}
  \end{subfigure}
  \hfill
  \begin{subfigure}[b]{0.45\textwidth}
    \includegraphics[width=\filename]{figure2.pdf}
    \caption{Second figure}
    \label{fig:second}
  \end{subfigure}
  \caption{Main caption for both figures}
  \label{fig:both}
\end{figure}
```

### Subfigures in Grid (2x2)

```latex
\begin{figure}[htbp]
  \centering
  \begin{subfigure}[t]{0.45\textwidth}
    \includegraphics[width=\filename]{fig1.pdf}
    \caption{Caption A}
  \end{subfigure}
  \hfill
  \begin{subfigure}[t]{0.45\textwidth}
    \includegraphics[width=\filename]{fig2.pdf}
    \caption{Caption B}
  \end{bmatrix}
  \\
  \begin{subfigure}[t]{0.45\textwidth}
    \includegraphics[width=\filename]{fig3.pdf}
    \caption{Caption C}
  \end{subfigure}
  \hfill
  \begin{subfigure}[t]{0.45\textwidth}
    \includegraphics[width=\filename]{fig4.pdf}
    \caption{Caption D}
  \end{subfigure}
  \caption{Main caption for all four}
  \label{fig:grid}
\end{figure}
```

### Subtables

```latex
\begin{table}[htbp]
  \centering
  \begin{subtable}[t]{0.45\textwidth}
    \centering
    \begin{tabular}{cc}
      \toprule
      A & B \\
      \midrule
      1 & 2 \\
      \bottomrule
    \end{tabular}
    \caption{First table}
    \label{tab:first}
  \end{subtable}
  \hfill
  \begin{subtable}[t]{0.45\textwidth}
    \centering
    \begin{tabular}{cc}
      \toprule
      C & D \\
      \midrule
      3 & 4 \\
      \bottomrule
    \end{tabular}
    \caption{Second table}
    \label{tab:second}
  \end{subtable}
  \caption{Main caption}
  \label{tab:both}
\end{table}
```

---

## Side-by-Side: Figure + Table

### Using minipage

```latex
\begin{figure}[htbp]
  \centering
  \begin{minipage}[c]{0.45\textwidth}
    \centering
    \includegraphics[width=\filename]{figure.pdf}
    \caption{My figure}
    \label{fig:minipage}
  \end{minipage}
  \hfill
  \begin{minipage}[c]{0.45\textwidth}
    \centering
    \begin{tabular}{lc}
      \toprule
      Method & Acc \\
      \midrule
      A & 85.2 \\
      B & 92.1 \\
      \bottomrule
    \end{tabular}
    \caption{My table}
    \label{tab:minipage}
  \end{minipage}
  \caption{Combined figure and table}
  \label{fig+tab}
\end{figure}
```

### Using subcaptionbox

```latex
\begin{figure}[htbp]
  \centering
  \subcaptionbox{Figure label\label{fig:subcap}}
    {\includegraphics[width=0.45\textwidth]{figure.pdf}}
  \qquad
  \subcaptionbox{Table label\label{tab:subcap}}
    {\begin{tabular}{lc}
      \toprule
      A & B \\
      \midrule
      1 & 2 \\
      \bottomrule
    \end{tabular}}
  \caption{Combined caption}
  \label{fig:subcap:combined}
\end{figure}
```

---

## Cross-Column Figures (twocolumn)

### Cross-Column Figure

```latex
\begin{figure*}[htbp]
  \centering
  \includegraphics[width=0.8\textwidth]{wide-figure.pdf}
  \caption{Wide figure spanning both columns}
  \label{fig:wide}
\end{figure*}
```

### Cross-Column Table

```latex
\begin{table*}[htbp]
  \centering
  \begin{tabular}{lcccc}
    \toprule
    Method & A & B & C & D \\
    \midrule
    Baseline & 85.2 & 86.1 & 87.3 & 88.0 \\
    Ours & \textbf{92.1} & \textbf{91.5} & \textbf{93.2} & \textbf{94.1} \\
    \bottomrule
  \end{tabular}
  \caption{Wide table spanning both columns}
  \label{tab:wide}
\end{table*}
```

---

## Common Float Issues and Solutions

### Issue: Figure drifts to end of document

**Cause**: Using `[h]` alone or figure is too large

**Solution**:
```latex
% Before (problematic)
\begin{figure}[h]

% After (recommended)
\begin{figure}[htbp]
% Or force placement
\begin{figure}[!htbp]
```

### Issue: Figure takes entire page alone

**Cause**: `[p]` triggers float page, or figure is large

**Solution**:
```latex
% Add stretch to push other content
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.7\textwidth]{figure.pdf}
  \caption{Caption}
  % Add space to encourage text to flow around
\end{figure}
```

### Issue: Figure separated from text reference

**Cause**: Float placement rules

**Solution**:
1. Use `[!htbp]` to force earlier placement
2. Place figure closer to its reference in source
3. Use `\FloatBarrier` from `placeins` package:
```latex
\usepackage{placeins}
\section{My Section}
Text reference to \figurename~\ref{fig:myfig}.

\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\textwidth]{figure.pdf}
  \caption{My figure}
  \label{fig:myfig}
\end{figure}
\FloatBarrier  % Prevents floats from crossing this barrier
```

### Issue: Subfigures not aligned

**Cause**: Different heights, missing alignment option

**Solution**:
```latex
% Use [t], [b], or [c] for vertical alignment
\begin{subfigure}[t]{0.45\textwidth}  % [t] = top alignment
\begin{subfigure}[b]{0.45\textwidth}  % [b] = bottom alignment
```

### Issue: Captions not centered under subfigures

**Cause**: Missing width specification

**Solution**:
```latex
\begin{subfigure}[t]{0.45\textwidth}
  \centering
  \includegraphics[width=\filename]{fig.pdf}
  \caption{Caption text}
\end{subfigure}
```

---

## Best Practices

1. **Use `[htbp]` by default** - gives LaTeX flexibility while respecting order
2. **Use `[!htbp]` for important figures** - overrides some float constraints
3. **Place floats near their reference** - in source order, not necessarily final position
4. **Use `booktabs` for tables** - professional look, but this skill doesn't handle formatting
5. **Use `subcaption` package** - modern replacement for `subfig`
6. **Consider `\FloatBarrier`** - for strict float control in sensitive locations

---

## Required Packages

The following packages are referenced in the examples above:

```latex
\usepackage{subcaption}  % For subfigure/subtable
\usepackage{booktabs}    % For professional tables (not positioning)
\usepackage{placeins}    % For \FloatBarrier
```

---

## Example Tasks

| Request | Approach |
|---------|----------|
| "Figure 1 always goes to next page" | Change `[h]` to `[htbp]` or `[!htbp]` |
| "Arrange 4 figures in 2x2 grid" | Use subfigure with line break `\\` |
| "Put figure and table side by side" | Use minipage or subcaptionbox |
| "Figure 2 is far from Section 2.2" | Use `[!htbp]` or add `\FloatBarrier` |
| "Wide table spans both columns" | Use `table*` instead of `table` |
