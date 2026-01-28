---
name: tikz-flowchart
description: "Creates professional TikZ flowcharts with a standardized style (Google Material-like colors, node shapes, and layout)."
---

# TikZ Flowchart Skill

This skill provides a standardized template/style for establishing professional technical diagrams using LaTeX TikZ. It is designed for creating flowcharts, architecture diagrams, and process flows.

## Usage

When asked to "create a flowchart" or "draw a diagram" in this project, use the template below as a starting point. Adjust styles (`dataNode`, `opNode`, etc.) as needed for the specific content.

## Style Guide

### Colors
The template uses a Google Material-like palette:
-   **Green (`greenFill`/`greenStroke`)**: Data, Inputs, Outputs, Tensors.
-   **Orange/Memory (`memFill`/`memStroke`)**: Memory, Weights, Checkpoints.
-   **Blue/Core (`coreFill`/`coreStroke`)**: Operations, Compute Kernels, Processes.
-   **Pink/Optimization (`optFill`/`optStroke`)**: Optimizations, Special Steps.
-   **Yellow/Process (`procFill`/`procStroke`)**: General Processing Steps.

### Standard Nodes
-   `dataNode`: Rectangles for data flow (green).
-   `memNode`: Cylinders for storage/weights (orange).
-   `opNode`: Rectangles for operations (blue).
-   `kernelBox`: Dashed containers for grouping internal kernel logic.
-   `group`: Dashed background containers for logical grouping of phases/stages.

## Template

Use this template as your base:

```latex
\documentclass[tikz,border=10pt]{standalone}
\usepackage{tikz}
\usepackage{amssymb}
\usetikzlibrary{shapes.geometric, arrows.meta, positioning, fit, backgrounds, calc, shadows.blur, decorations.pathreplacing}

% --- Color Definitions ---
\definecolor{greenFill}{HTML}{E8F5E9}
\definecolor{greenStroke}{HTML}{43A047}
\definecolor{memFill}{HTML}{FFF3E0}
\definecolor{memStroke}{HTML}{FFB74D}
\definecolor{coreFill}{HTML}{E1F5FE}
\definecolor{coreStroke}{HTML}{0277BD}
\definecolor{optFill}{HTML}{FCE4EC}
\definecolor{optStroke}{HTML}{E91E63}
\definecolor{procFill}{HTML}{FFF9C4}
\definecolor{procStroke}{HTML}{FBC02D}

\begin{document}

\begin{tikzpicture}[
    node distance=1.2cm and 1.8cm, % Vertical and Horizontal spacing
    font=\sffamily\footnotesize,
    >=Stealth,
    % --- Styles ---
    dataNode/.style={
        rectangle, rounded corners=3pt,
        draw=greenStroke, thick,
        fill=greenFill,
        minimum width=2.4cm, minimum height=1.2cm,
        align=center,
        drop shadow
    },
    memNode/.style={
        cylinder, cylinder uses custom fill,
        cylinder body fill=memFill, cylinder end fill=memFill!90!gray,
        shape border rotate=90,
        aspect=0.25,
        draw=memStroke, thick,
        minimum width=1.8cm, minimum height=1.3cm,
        align=center
    },
    opNode/.style={
        rectangle, rounded corners=3pt,
        draw=coreStroke, thick,
        fill=coreFill,
        minimum width=2.6cm, minimum height=1.2cm,
        align=center,
        drop shadow
    },
    kernelBox/.style={
        rectangle, rounded corners=8pt,
        draw=coreStroke, thick, dashed,
        fill=coreFill!20,
        inner sep=12pt,
        align=center
    },
    group/.style={
        draw=gray!30, dashed, rounded corners=8pt, inner sep=12pt, fill=gray!5
    },
    edgeLabel/.style={
        font=\scriptsize,
        text=black!80,
        align=center,
        inner sep=1pt
    }
]

    % --- Nodes ---
    % Example:
    % \node[dataNode] (Input) {Input Data};
    % \node[opNode, right=of Input] (Process) {Process};

    % --- Layout Containers (Optional) ---
    % \begin{scope}[on background layer]
    %    \node[group, fit=(Input)(Process)] (MainGroup) {};
    % \end{scope}

    % --- Connections ---
    % \draw[->, thick, color=gray!80] (Input) -- (Process);

\end{tikzpicture}
\end{document}
```

## Best Practices

1.  **Relative Positioning**: Use `right=of Node`, `below=of Node` for layout stability. Adjust distances via `node distance` in the `tikzpicture` options.
2.  **Grouping**: Use the `fit` library and `group` style to draw background boxes around related nodes. Always place these in a `\begin{scope}[on background layer]` block.
3.  **Orthogonal Edges**: Use `-|` and `|-` path operations for clean, orthogonal lines (e.g., `(A) -| (B)`).
4.  **Conciseness**: Keep node text short. Use `\\` for line breaks and `\scriptsize` for secondary details.
