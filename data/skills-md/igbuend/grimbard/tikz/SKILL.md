---
name: tikz
description: "LaTeX TikZ/PGF package for programmatic vector graphics and diagrams. Use when helping users draw flowcharts, trees, graphs, automata, circuits, geometric figures, or any custom diagram in LaTeX."
---

# TikZ/PGF — Vector Graphics & Diagrams

**CTAN:** https://ctan.org/pkg/pgf  
**Manual:** `texdoc tikz` (~1300 pages)

## Setup

```latex
\usepackage{tikz}
% Load libraries as needed:
\usetikzlibrary{arrows.meta, calc, positioning, decorations.pathmorphing,
  patterns, shapes.geometric, shapes.misc, fit, backgrounds,
  automata, trees, mindmap, circuits.logic.US}
```

## Basic Drawing

### Minimal Example

```latex
\begin{tikzpicture}
  \draw (0,0) -- (2,0) -- (2,2) -- cycle;  % triangle
\end{tikzpicture}
```

### Path Operations

| Operation | Syntax | Example |
|-----------|--------|---------|
| Line | `--` | `(0,0) -- (1,1)` |
| Horizontal-vertical | <code>-\|</code> | `(0,0) -| (1,1)` (go right then up) |
| Vertical-horizontal | <code>\|-</code> | `(0,0) |- (1,1)` (go up then right) |
| Curve | `.. controls .. ..` | `(0,0) .. controls (0.5,1) .. (1,0)` |
| Smooth curve | `to[out=..,in=..]` | `(0,0) to[out=90,in=180] (2,1)` |
| Arc | `arc` | `(0,0) arc (0:90:1cm)` start:end:radius |
| Circle | `circle` | `(0,0) circle[radius=1]` |
| Ellipse | `ellipse` | `(0,0) ellipse[x radius=2, y radius=1]` |
| Rectangle | `rectangle` | `(0,0) rectangle (2,1)` |
| Grid | `grid` | `(0,0) grid (3,3)` |
| Parabola | `parabola` | `(0,0) parabola (2,2)` |
| Sin/Cos | `sin`/`cos` | `(0,0) sin (1,1)` |
| Plot | `plot` | `plot[domain=0:3] (\x, {\x^2})` |
| Cycle | `cycle` | close path back to start |

### Path Actions

| Command | Effect |
|---------|--------|
| `\draw` | Stroke the path |
| `\fill` | Fill the path |
| `\filldraw` | Fill and stroke |
| `\path` | Invisible path (for coordinates, nodes) |
| `\clip` | Clip subsequent drawing to path |
| `\shade` | Gradient fill |
| `\shadedraw` | Gradient fill + stroke |
| `\node` | Shorthand for `\path node` |
| `\coordinate` | Shorthand for `\path coordinate` |

### Common Draw Options

```latex
\draw[
  color=blue,            % or just: blue
  line width=1pt,        % or: thin, thick, very thick, ultra thick
  dashed,                % or: dotted, dash dot, dash dot dot
  dash pattern={on 3pt off 2pt},
  rounded corners=5pt,
  ->                     % arrow tip (see arrows section)
  opacity=0.5,
  double,
  double distance=2pt,
] (0,0) -- (2,2);
```

### Common Fill Options

```latex
\fill[
  fill=blue!20,          % 20% blue
  fill opacity=0.5,
  pattern=north lines,   % requires patterns library
  pattern color=gray,
] (0,0) rectangle (2,1);
```

## Coordinate Systems

```latex
% Cartesian (default)
(2, 3)

% Polar (angle:radius)
(45:2cm)

% Relative (shift from last point)
++(1,0)    % move reference point
+(1,0)     % don't move reference point

% Named
\coordinate (A) at (1,2);
\draw (A) -- (2,3);

% Intersection (calc library)
\usetikzlibrary{calc}
($(A)!0.5!(B)$)           % midpoint of A and B
($(A)!0.5!90:(B)$)        % midpoint rotated 90°
($(A) + (1,2)$)           % A shifted by (1,2)
($(A)!1cm!(B)$)           % 1cm from A toward B

% Perpendicular coordinates (A -| B) = (x of B, y of A)
(A |- B)                   % (x of A, y of B)

% Barycentric
(barycentric cs:A=1,B=1,C=1)  % centroid
```

## Nodes

### Basic Nodes

```latex
\node (name) at (0,0) {Text};

% Node options
\node[
  draw,                    % draw border
  fill=yellow!20,
  rectangle,               % shape (default)
  circle,
  ellipse,
  rounded corners,
  minimum width=2cm,
  minimum height=1cm,
  inner sep=5pt,           % padding
  outer sep=2pt,           % margin
  text=red,
  font=\bfseries\small,
  align=center,            % for multi-line: use \\ in text
  text width=3cm,
  anchor=north,            % positioning anchor
  rotate=45,
] (mynode) at (1,2) {Hello\\World};
```

### Node Anchors

```
          north west  north  north east
                 ┌──────────┐
            west │  center   │ east
                 └──────────┘
          south west  south  south east
```

Also: `base`, `mid`, `text`, and angle anchors like `45`, `135`.

### Nodes on Paths

```latex
\draw (0,0) -- node[above] {label} (3,0);
\draw (0,0) -- node[midway, sloped, above] {sloped text} (3,2);
\draw (0,0) -- node[pos=0.3, below] {at 30\%} (3,0);
\draw (0,0) to[out=90,in=0] node[near start, left] {A} (2,2);
```

### Common Shapes (requires libraries)

```latex
\usetikzlibrary{shapes.geometric, shapes.misc}

\node[diamond, draw] {D};
\node[star, draw, star points=5] {S};
\node[regular polygon, regular polygon sides=6, draw] {Hex};
\node[trapezium, draw] {T};
\node[cylinder, draw, shape border rotate=90] {DB};
\node[cloud, draw, cloud puffs=10] {Cloud};
\node[cross out, draw] at (0,0) {};
\node[strike out, draw] at (0,0) {};
```

## Arrows

```latex
\usetikzlibrary{arrows.meta}

% Arrow tips (arrows.meta syntax)
\draw[->] (0,0) -- (1,0);              % default
\draw[-Stealth] (0,0) -- (1,0);        % filled triangle
\draw[-Latex] (0,0) -- (1,0);          % larger filled
\draw[-{Stealth[length=5mm]}] (0,0) -- (1,0);
\draw[{Latex[red]}-{Latex[blue]}] (0,0) -- (1,0);  % colored
\draw[-{>[scale=2]}] (0,0) -- (1,0);

% Common tips: >, Stealth, Latex, To, Circle, Square, |, Hooks
% Modifiers: [length=..], [width=..], [open], [fill=..], [scale=..]
```

## Styles

```latex
% Define in preamble or tikzpicture options
\tikzset{
  mybox/.style = {draw, fill=blue!20, rounded corners, minimum width=2cm},
  myarrow/.style = {-Stealth, thick, red},
  highlight/.style = {fill=yellow, draw=orange, line width=2pt},
}

% Use
\node[mybox] {Box};
\draw[myarrow] (0,0) -- (1,1);

% Style with parameters
\tikzset{
  box/.style = {draw, fill=#1!20, minimum width=1.5cm},
  box/.default = blue,
}
\node[box] {Blue};        % default
\node[box=red] {Red};     % override

% every node/.style applies to all nodes
\begin{tikzpicture}[every node/.style={font=\small}]
```

## Foreach Loops

```latex
% Basic
\foreach \x in {0,1,2,3}
  \draw (\x, 0) circle (0.3);

% With step
\foreach \x in {0,0.5,...,3}
  \fill (\x,0) circle (1pt);

% Multiple variables
\foreach \x/\y in {0/A, 1/B, 2/C}
  \node at (\x, 0) {\y};

% Counter
\foreach \x [count=\i] in {a,b,c,d}
  \node at (\i, 0) {\x};

% Evaluate
\foreach \x [evaluate=\x as \y using \x*\x] in {1,...,5}
  \fill (\x, \y/5) circle (2pt);

% Remember
\foreach \x [remember=\x as \lastx (initially 0)] in {1,...,5}
  \draw (\lastx, 0) -- (\x, 0);
```

## Scopes and Transformations

```latex
\begin{tikzpicture}
  \draw (0,0) -- (1,0);
  
  \begin{scope}[shift={(2,0)}, rotate=45, scale=0.5, red, thick]
    \draw (0,0) -- (1,0) -- (1,1) -- cycle;
  \end{scope}
  
  % Transformations
  % shift={(x,y)}, xshift=1cm, yshift=2cm
  % rotate=45, rotate around={45:(1,1)}
  % scale=2, xscale=2, yscale=0.5
  % xslant=0.5, yslant=0.5
\end{tikzpicture}
```

## Clipping

```latex
\begin{tikzpicture}
  \clip (0,0) circle (1.5cm);
  % Everything below is clipped to the circle
  \fill[blue!30] (-2,-2) rectangle (2,2);
  \draw[step=0.5, gray] (-2,-2) grid (2,2);
\end{tikzpicture}
```

## Layers (backgrounds library)

```latex
\usetikzlibrary{backgrounds}

\begin{tikzpicture}
  \node[draw, fill=white] (A) {Foreground};
  
  \begin{pgfonlayer}{background}
    \fill[yellow!30] (A.south west) rectangle (A.north east);
  \end{pgfonlayer}
\end{tikzpicture}
```

## Pics

```latex
\tikzset{
  myshape/.pic = {
    \draw (-0.5,-0.5) rectangle (0.5,0.5);
    \draw (0,0) circle (0.3);
  }
}

\begin{tikzpicture}
  \pic at (0,0) {myshape};
  \pic[rotate=45, scale=1.5] at (2,0) {myshape};
\end{tikzpicture}
```

## Decorations

```latex
\usetikzlibrary{decorations.pathmorphing, decorations.markings, decorations.text}

% Wavy/zigzag lines
\draw[decorate, decoration={zigzag, amplitude=2mm, segment length=5mm}]
  (0,0) -- (4,0);
\draw[decorate, decoration={snake, amplitude=1mm}]
  (0,0) -- (4,0);
\draw[decorate, decoration={coil, aspect=0.5}]
  (0,0) -- (4,0);
\draw[decorate, decoration={random steps, segment length=3mm}]
  (0,0) -- (4,0);

% Brace
\draw[decorate, decoration={brace, amplitude=5pt}]
  (0,0) -- (3,0) node[midway, above=5pt] {label};

% Text along path
\draw[decorate, decoration={text along path, text={Hello World}}]
  (0,0) .. controls (1,1) .. (3,0);

% Markings (arrows along path)
\draw[decoration={markings, mark=at position 0.5 with {\arrow{>}}},
  postaction={decorate}]
  (0,0) -- (3,0);
```

## Patterns

```latex
\usetikzlibrary{patterns}

\fill[pattern=north east lines] (0,0) rectangle (2,1);
\fill[pattern=crosshatch dots, pattern color=blue] (0,0) circle (1);

% Available: north east lines, north west lines, horizontal lines,
% vertical lines, crosshatch, dots, crosshatch dots,
% fivepointed stars, sixpointed stars, bricks, checkerboard
```

---

## Common Diagram Patterns

### Flowchart

```latex
\usetikzlibrary{arrows.meta, shapes.geometric, positioning}

\tikzset{
  startstop/.style = {rectangle, rounded corners, draw, fill=red!20,
    minimum width=3cm, minimum height=1cm},
  process/.style = {rectangle, draw, fill=blue!20,
    minimum width=3cm, minimum height=1cm},
  decision/.style = {diamond, draw, fill=green!20,
    minimum width=3cm, minimum height=1cm, aspect=1.5},
  io/.style = {trapezium, trapezium left angle=70, trapezium right angle=110,
    draw, fill=orange!20, minimum width=3cm, minimum height=1cm},
  arrow/.style = {thick, -Stealth},
}

\begin{tikzpicture}[node distance=1.5cm]
  \node[startstop] (start) {Start};
  \node[io, below=of start] (input) {Input $x$};
  \node[decision, below=of input] (decide) {$x > 0$?};
  \node[process, below left=of decide] (neg) {$y = -x$};
  \node[process, below right=of decide] (pos) {$y = x$};
  \node[io, below=2cm of decide] (output) {Output $y$};
  \node[startstop, below=of output] (stop) {Stop};

  \draw[arrow] (start) -- (input);
  \draw[arrow] (input) -- (decide);
  \draw[arrow] (decide) -| node[near start, above] {No} (neg);
  \draw[arrow] (decide) -| node[near start, above] {Yes} (pos);
  \draw[arrow] (neg) |- (output);
  \draw[arrow] (pos) |- (output);
  \draw[arrow] (output) -- (stop);
\end{tikzpicture}
```

### Tree

```latex
\begin{tikzpicture}[
  level 1/.style={sibling distance=4cm},
  level 2/.style={sibling distance=2cm},
  every node/.style={draw, circle, minimum size=8mm},
  edge from parent/.style={draw, -Stealth},
]
  \node {1}
    child { node {2}
      child { node {4} }
      child { node {5} }
    }
    child { node {3}
      child { node {6} }
      child { node {7} }
    };
\end{tikzpicture}
```

### Graph / Network

```latex
\usetikzlibrary{positioning}

\begin{tikzpicture}[
  vertex/.style={draw, circle, fill=blue!20, minimum size=8mm},
  edge/.style={thick},
  >=Stealth,
]
  \node[vertex] (a) at (0,2)  {A};
  \node[vertex] (b) at (2,3)  {B};
  \node[vertex] (c) at (4,2)  {C};
  \node[vertex] (d) at (2,0)  {D};

  \draw[edge] (a) -- node[above left]  {3} (b);
  \draw[edge] (b) -- node[above right] {2} (c);
  \draw[edge] (a) -- node[below left]  {7} (d);
  \draw[edge] (c) -- node[below right] {1} (d);
  \draw[edge] (b) -- node[right]       {4} (d);
\end{tikzpicture}
```

### Finite Automaton / State Machine

```latex
\usetikzlibrary{automata, positioning}

\begin{tikzpicture}[shorten >=1pt, node distance=2.5cm, on grid, auto,
  every state/.style={draw, minimum size=1cm}]

  \node[state, initial]           (q0) {$q_0$};
  \node[state, right=of q0]      (q1) {$q_1$};
  \node[state, accepting, right=of q1] (q2) {$q_2$};

  \path[->]
    (q0) edge              node {a}   (q1)
    (q0) edge [loop above] node {b}   ()
    (q1) edge              node {a,b} (q2)
    (q1) edge [bend left]  node {b}   (q0)
    (q2) edge [loop above] node {a}   ();
\end{tikzpicture}
```

### Mind Map

```latex
\usetikzlibrary{mindmap}

\begin{tikzpicture}[mindmap, grow cyclic,
  every node/.style={concept, execute at begin node=\hskip0pt},
  concept color=blue!40,
  level 1/.append style={level distance=4cm, sibling angle=90},
  level 2/.append style={level distance=2.5cm, sibling angle=45},
]
  \node {Main Topic}
    child[concept color=red!40] { node {Sub 1}
      child { node {Detail A} }
      child { node {Detail B} }
    }
    child[concept color=green!40] { node {Sub 2}
      child { node {Detail C} }
    }
    child[concept color=orange!40] { node {Sub 3} }
    child[concept color=purple!40] { node {Sub 4} };
\end{tikzpicture}
```

### Block Diagram / System Diagram

```latex
\usetikzlibrary{positioning, arrows.meta, fit}

\begin{tikzpicture}[
  block/.style={draw, rectangle, fill=blue!10, minimum height=1cm,
    minimum width=2cm, align=center},
  sum/.style={draw, circle, minimum size=6mm},
  >=Stealth, thick,
]
  \node[sum] (sum) {};
  \node[block, right=1.5cm of sum] (ctrl) {Controller\\$G_c(s)$};
  \node[block, right=1.5cm of ctrl] (plant) {Plant\\$G(s)$};
  \node[block, below=1cm of plant] (fb) {Sensor\\$H(s)$};

  \draw[->] ++(-1.5,0) -- node[above] {$R(s)$} (sum);
  \draw[->] (sum) -- node[above] {$E(s)$} (ctrl);
  \draw[->] (ctrl) -- (plant);
  \draw[->] (plant) -- ++(2,0) node[above left] {$Y(s)$};
  \draw[->] (plant.east) ++(1,0) |- (fb);
  \draw[->] (fb) -| (sum) node[near end, left] {$-$};

  \node at (sum) {$\Sigma$};
\end{tikzpicture>
```

### Venn Diagram

```latex
\begin{tikzpicture}
  \fill[red!20]  (0,0)   circle (1.5cm);
  \fill[blue!20] (1.5,0) circle (1.5cm);
  
  \begin{scope}
    \clip (0,0) circle (1.5cm);
    \fill[purple!30] (1.5,0) circle (1.5cm);
  \end{scope}
  
  \draw (0,0) circle (1.5cm) node[left=1cm]  {$A$};
  \draw (1.5,0) circle (1.5cm) node[right=1cm] {$B$};
  \node at (0.75, 0) {$A \cap B$};
\end{tikzpicture}
```

### Timeline

```latex
\begin{tikzpicture}
  \draw[thick, -Stealth] (0,0) -- (10,0);
  
  \foreach \x/\year/\event in {
    1/2020/Founded,
    3/2021/v1.0,
    5.5/2022/IPO,
    8/2023/Global%
  }{
    \draw (\x, -0.15) -- (\x, 0.15);
    \node[above=3pt] at (\x, 0.15) {\footnotesize \year};
    \node[below=3pt, align=center, text width=1.5cm] at (\x, -0.15) {\footnotesize \event};
  }
\end{tikzpicture}
```

### Circuit (Logic Gates)

```latex
\usetikzlibrary{circuits.logic.US}

\begin{tikzpicture}[circuit logic US, every circuit symbol/.style={thick}]
  \node[and gate] (and1) at (2,1) {};
  \node[or gate]  (or1)  at (4,0.5) {};

  \draw (0,1.25) node[left] {$A$} -- (and1.input 1);
  \draw (0,0.75) node[left] {$B$} -- (and1.input 2);
  \draw (and1.output) -- (or1.input 1);
  \draw (0,0)    node[left] {$C$} -- (or1.input 2);
  \draw (or1.output) -- ++(1,0) node[right] {$Y$};
\end{tikzpicture}
```

### Commutative Diagram (Math)

```latex
\usetikzlibrary{positioning}

\begin{tikzpicture}[>=Stealth, node distance=2cm]
  \node (A)              {$A$};
  \node (B) [right=of A] {$B$};
  \node (C) [below=of A] {$C$};
  \node (D) [right=of C] {$D$};

  \draw[->] (A) -- node[above] {$f$} (B);
  \draw[->] (A) -- node[left]  {$g$} (C);
  \draw[->] (B) -- node[right] {$h$} (D);
  \draw[->] (C) -- node[below] {$k$} (D);
\end{tikzpicture}
```

### Plot (built-in, no pgfplots)

```latex
\begin{tikzpicture}[scale=0.8]
  \draw[->] (-0.5,0) -- (4.5,0) node[right] {$x$};
  \draw[->] (0,-0.5) -- (0,3.5) node[above] {$y$};
  
  \draw[blue, thick, domain=0:4, samples=100]
    plot (\x, {sqrt(\x)});
  
  \foreach \x in {1,...,4}
    \draw (\x, 0.1) -- (\x, -0.1) node[below] {\x};
  \foreach \y in {1,2,3}
    \draw (0.1, \y) -- (-0.1, \y) node[left] {\y};
\end{tikzpicture}
```

## Positioning Library

```latex
\usetikzlibrary{positioning}

% Relative positioning (preferred over manual coordinates)
\node[right=of A] (B) {B};       % default separation
\node[right=1.5cm of A] (B) {B}; % custom distance
\node[above right=1cm and 2cm of A] (B) {B};  % separate x/y

% Available: above, below, left, right,
% above left, above right, below left, below right
```

## Fit Library

```latex
\usetikzlibrary{fit}

% Draw a box around multiple nodes
\node[draw, dashed, fit=(A) (B) (C), inner sep=5pt, label=above:Group] {};
```

## Calc Library Key Operations

```latex
\usetikzlibrary{calc}

% Midpoint
($(A)!0.5!(B)$)

% Point 1cm from A toward B
($(A)!1cm!(B)$)

% Projection of C onto line AB
($(A)!(C)!(B)$)

% Rotated point: midpoint of AB rotated 90° around A
($(A)!0.5!90:(B)$)

% Vector addition
($(A) + (1,2)$)

% Scalar multiply
($2*(A) - (B)$)

% let syntax for complex calculations
\draw let \p1 = ($(B)-(A)$),
          \n1 = {veclen(\x1,\y1)}
      in (A) circle (\n1);
```

## Externalizing (Caching) Figures

```latex
% In preamble — compiles each tikzpicture once, reuses PDF
\usetikzlibrary{external}
\tikzexternalize[prefix=tikz-cache/]

% To skip a figure:
\tikzexternaldisable
\begin{tikzpicture} ... \end{tikzpicture}
\tikzexternalenable
```

Requires `--shell-escape` flag: `pdflatex --shell-escape main.tex`

## Common Pitfalls

| Problem | Cause | Fix |
|---------|-------|-----|
| "Dimension too large" | Coordinates too big | Use `scale` or smaller coords |
| Missing arrow tips | Forgot `arrows.meta` library | `\usetikzlibrary{arrows.meta}` |
| Node text cut off | Node too small | Add `minimum width`, `text width` |
| `positioning` not working | Forgot library | `\usetikzlibrary{positioning}` |
| Nodes overlap | Using `at` instead of relative | Use `right=of` with positioning lib |
| `foreach` errors | Special chars in body | Wrap body in `{}` |
| Path not closing | Forgot `cycle` | End path with `-- cycle` |
| Slow compilation | Complex figures | Use `external` library for caching |
| Math in nodes | `$` conflicts | Use `$...$` inside node text normally |
| Colors not found | Missing xcolor | TikZ loads xcolor; use `\usepackage[dvipsnames]{xcolor}` before tikz for extra colors |

## Tips

- Use `positioning` library — never hardcode coordinates for node layouts
- `\tikzset` in preamble for reusable styles across figures
- `every node/.style`, `every path/.style` for consistent appearance
- Use `\begin{scope}` to limit option scope
- `name path=X` + `name intersections` (intersections library) to find crossing points
- For standalone figures: `\documentclass[tikz]{standalone}`
- `spy` library for magnification insets
- `pgfplotstable` for data-driven diagrams (see pgfplots skill)
