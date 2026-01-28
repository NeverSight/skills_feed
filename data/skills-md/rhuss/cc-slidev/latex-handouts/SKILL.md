---
name: LaTeX Handouts
description: This skill should be used when the user asks to "create LaTeX handout", "compile handout", "generate presentation handout", "create PDF document from slides", or needs guidance on LaTeX document structure, formatting, embedding images, or creating comprehensive presentation materials.
version: 0.1.0
---

# LaTeX Handouts

LaTeX provides professional typesetting for presentation handouts that combine slide images, presenter notes, and supplementary research into comprehensive reference documents.

## Dependency Checking

Before generating handouts, check dependencies using:
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/check-handout-deps.sh
```

**Exit codes:**
- 0: All dependencies available (full handout with images and rich formatting)
- 1: pdflatex missing (BLOCKER - cannot generate handout)
- 2: LaTeX packages missing (use basic formatting)
- 3: Playwright missing (text-only handout)

## Graceful Degradation Strategies

**When LaTeX packages unavailable (exit code 2):**
- Skip `\usepackage{tcolorbox}` and `\usepackage{enumitem}` in preamble
- Use standard LaTeX boxes instead of tcolorbox
- Use default enumerate/itemize instead of enumitem
- Result: Basic but functional handout

**When Playwright unavailable (exit code 3):**
- Skip slide PNG export entirely
- Omit `\begin{figure}...\end{figure}` blocks for slide images
- Still include all prose paragraphs (Overview, Key Considerations, Technical Details)
- Still include all Further Reading links
- Result: Text-only reference document (still valuable)

**When pdflatex unavailable (exit code 1):**
- Cannot generate PDF handout
- Offer to create .tex file for user to compile later
- Provide installation instructions

## Handout Writing Principles

**Critical:** Handouts should be **comprehensive standalone documents**, not just copies of slides.

### Content Requirements

✅ **DO:**
- Write in **complete prose paragraphs** (2-4 sentences minimum)
- **Expand on slide content** - explain concepts in detail
- **Add context** - WHY things matter, HOW they work
- **Include researched URLs** - 3-5 quality resources per section
- **Provide examples** - real-world applications and use cases
- **Explain trade-offs** - discuss implications and alternatives
- Make it **standalone** - reader understands without attending presentation

❌ **DON'T:**
- Copy bullet points from slides verbatim
- Write generic descriptions
- Use slide content as handout content
- Skip research for further reading
- Assume reader attended presentation

### Writing Style

**For each slide, write:**

1. **Overview paragraph** (2-4 sentences)
   - Transform slide bullets into flowing narrative
   - Explain the concept in complete detail
   - Provide context and connections

2. **Key Considerations paragraph** (2-4 sentences)
   - Discuss implications and trade-offs
   - Explain WHY it matters
   - Provide real-world examples

3. **Technical Details paragraph** (if applicable)
   - Explain HOW things work (not just WHAT)
   - Code explanations in prose
   - Architecture decisions and reasoning

4. **Further Reading list** (3-5 URLs)
   - Official documentation
   - Authoritative articles
   - Tutorials and guides
   - Each with specific description of value

## Document Structure

### Basic Handout Template

```latex
\documentclass[11pt,a4paper]{article}

% Essential packages
\usepackage[utf8]{inputenc}
\usepackage[margin=1in]{geometry}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{fancyhdr}

% Document metadata
\title{Presentation Title}
\author{Author Name}
\date{\today}

% Header/footer setup
\pagestyle{fancy}
\fancyhead[L]{Presentation Title}
\fancyhead[R]{\thepage}
\fancyfoot[C]{}

\begin{document}

\maketitle
\tableofcontents
\newpage

% Content sections
\section{Introduction}
Content here...

\end{document}
```

### Document Classes

**article** - Standard documents
- Best for: Short handouts (1-20 pages)
- Features: Simple structure, no chapters
- Use when: Single presentation handout

**report** - Longer documents
- Best for: Extended handouts (20+ pages)
- Features: Chapters supported, more structure
- Use when: Multi-session course materials

**scrartcl/scrreprt** - KOMA-Script alternatives
- Best for: Modern, customizable layouts
- Features: Better typography, more options
- Use when: Advanced formatting needed

## Essential Packages

### Graphics and Images

```latex
\usepackage{graphicx}  % Include images
\usepackage{float}     % Better float positioning

% Usage
\begin{figure}[H]
  \centering
  \includegraphics[width=0.8\textwidth]{slide-01.pdf}
  \caption{Introduction Slide}
  \label{fig:intro}
\end{figure}
```

### Layout and Formatting

```latex
\usepackage[margin=1in]{geometry}  % Page margins
\usepackage{multicol}              % Multiple columns
\usepackage{parskip}               % Paragraph spacing
\usepackage{setspace}              % Line spacing

% Multi-column sections
\begin{multicols}{2}
  Content in two columns
\end{multicols}
```

### Hyperlinks and References

```latex
\usepackage{hyperref}

% Configuration
\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    filecolor=magenta,
    urlcolor=cyan,
    citecolor=green
}

% Usage
\href{https://example.com}{Link text}
\url{https://example.com}
```

### Code Listings

```latex
\usepackage{listings}
\usepackage{xcolor}

% Configuration
\lstset{
    basicstyle=\ttfamily\small,
    keywordstyle=\color{blue},
    commentstyle=\color{green},
    stringstyle=\color{red},
    frame=single,
    breaklines=true
}

% Usage
\begin{lstlisting}[language=Python]
def hello():
    print("Hello, World!")
\end{lstlisting}
```

### Bibliography

```latex
\usepackage[backend=biber,style=apa]{biblatex}
\addbibresource{references.bib}

% In document
\cite{key}

% At end
\printbibliography
```

## Heading Hierarchy

**Use semantic heading levels rigorously and consistently:**

- `\section{}` - Major document divisions (Introduction, Presentation Content, Summary, Additional Resources)
- `\subsection{}` - Topic sections within presentation (matches slide deck sections/chapters)
- `\subsubsection{}` - Individual slide titles (each slide gets its own subsubsection heading)
- `\paragraph{}` - Content subdivisions within slides (Overview, Key Considerations, Technical Details, Further Reading)

**Rules:**
- Never skip heading levels (don't go from `\section{}` to `\subsubsection{}`)
- Use headings for semantic structure, not just visual formatting
- Keep heading text descriptive and assertion-based
- Each slide must have its own `\subsubsection{}` heading

## Handout Patterns

### Comprehensive Slide Documentation (RECOMMENDED)

Modern handout format with PNG slides and prose explanations:

```latex
\section{Topic Name}

\subsubsection{Specific Slide Title (Assertion Form)}

\begin{figure}[H]
  \centering
  \fbox{\includegraphics[width=0.72\textwidth]{exports/slide-005.png}}
  \caption{Specific Slide Title}
\end{figure}

\paragraph{Overview:}
This section introduces the core concept of container orchestration in distributed systems.
Kubernetes provides declarative configuration management, allowing operators to specify desired
state rather than imperative commands. The reconciliation loop continuously monitors actual
state and makes adjustments to match the declared configuration, providing self-healing
capabilities automatically.

\paragraph{Key Considerations:}
The declarative approach fundamentally changes operational practices compared to traditional
imperative automation. When configuration drift occurs, the system automatically corrects it
without human intervention. This is particularly valuable in large-scale deployments where
manual intervention becomes impractical. However, it requires careful design of resource
specifications and understanding of reconciliation behavior during failures.

\paragraph{Technical Details:}
The control loop pattern uses three key components: controllers watch the API server for
changes, compare current state to desired state, and issue commands to reconcile differences.
Each controller operates independently, managing specific resource types. This distributed
control model provides scalability and fault tolerance, as controller failures don't cascade
across the system.

\paragraph{Further Reading:}
\begin{itemize}
  \item \href{https://kubernetes.io/docs/concepts/architecture/controller/}{Kubernetes Controllers} -
        Official documentation explaining control loop patterns and reconciliation
  \item \href{https://www.oreilly.com/library/view/programming-kubernetes/9781492047094/}{Programming Kubernetes} -
        In-depth guide to writing custom controllers and operators
  \item \href{https://speakerdeck.com/thockin/kubernetes-what-is-reconciliation}{What is Reconciliation?} -
        Tim Hockin's presentation on reconciliation patterns
\end{itemize}

\vspace{0.5cm}

\newpage
```

### WRONG: Bullet Point Copy (DON'T DO THIS)

❌ **Bad handout - just copies slide bullets:**

```latex
\subsection{Slide Content}
\begin{figure}[H]
  \includegraphics[width=0.9\textwidth]{slide.png}
\end{figure}

\subsection{Notes}
Key points:
\begin{itemize}
  \item Declarative configuration
  \item Reconciliation loops
  \item Self-healing
\end{itemize}

Additional info:
\begin{itemize}
  \item Useful for large deployments
  \item See Kubernetes docs
\end{itemize}
```

**Why this is bad:**
- Just copies bullets from slide (no value added)
- Generic descriptions ("useful", "see docs")
- No explanation of HOW or WHY
- Not standalone (requires attending presentation)
- Links without context

### Multi-Slide Grid

Show multiple slides per page:

```latex
\begin{figure}[H]
  \centering
  \begin{minipage}{0.45\textwidth}
    \centering
    \includegraphics[width=\textwidth]{slide-01.pdf}
    \caption{Slide 1}
  \end{minipage}
  \hfill
  \begin{minipage}{0.45\textwidth}
    \centering
    \includegraphics[width=\textwidth]{slide-02.pdf}
    \caption{Slide 2}
  \end{minipage}
\end{figure}
```

### Two-Column Layout

Content alongside images:

```latex
\begin{multicols}{2}
  \noindent
  \textbf{Key Concepts:}
  \begin{itemize}
    \item Concept 1
    \item Concept 2
  \end{itemize}

  \columnbreak

  \begin{figure}[H]
    \centering
    \includegraphics[width=\linewidth]{diagram.pdf}
  \end{figure}
\end{multicols}
```

## Image Embedding

### Slide Images

**IMPORTANT:** All slide images in handouts should have black borders using `\fbox{}` to clearly delineate the slide boundaries.

Export slides as PNG for handouts:

```latex
% Single slide
\includegraphics[width=0.8\textwidth]{exports/slides.pdf}

% Specific page from multi-page PDF
\includegraphics[page=5,width=0.8\textwidth]{exports/slides.pdf}

% With black border (recommended for handouts)
\fbox{\includegraphics[width=0.72\textwidth]{slide.png}}
```

### Size Control

```latex
% By width (maintains aspect ratio)
\includegraphics[width=0.8\textwidth]{image.pdf}

% By height
\includegraphics[height=6cm]{image.pdf}

% Scale factor
\includegraphics[scale=0.5]{image.pdf}

% Exact dimensions (distorts if wrong ratio)
\includegraphics[width=10cm,height=6cm]{image.pdf}
```

### Positioning

```latex
% Centered
\begin{center}
  \includegraphics[width=0.7\textwidth]{image.pdf}
\end{center}

% In figure environment (with caption)
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.7\textwidth]{image.pdf}
  \caption{Descriptive caption}
  \label{fig:label}
\end{figure}

% Position codes:
% h - here
% t - top of page
% b - bottom of page
% p - separate page
% ! - override restrictions
% H - HERE (requires float package)
```

## Document Formatting

### Title Page

```latex
\begin{titlepage}
  \centering
  \vspace*{2cm}

  {\Huge\bfseries Presentation Title\par}
  \vspace{1cm}
  {\Large Subtitle or Topic\par}
  \vspace{2cm}
  {\Large\itshape Author Name\par}
  \vspace{1cm}
  {\large\today\par}

  \vfill
  {\large Organization Name\par}
  \vspace{0.5cm}
  \includegraphics[width=0.3\textwidth]{logo.pdf}
\end{titlepage}
```

### Table of Contents

```latex
\tableofcontents
\newpage

% Depth control (default 3)
\setcounter{tocdepth}{2}  % Show up to subsections
```

### Headers and Footers

```latex
\usepackage{fancyhdr}
\pagestyle{fancy}

% Clear defaults
\fancyhf{}

% Left header
\fancyhead[L]{Presentation Title}

% Right header
\fancyhead[R]{Author Name}

% Center footer
\fancyfoot[C]{\thepage}

% Right footer
\fancyfoot[R]{\today}

% Line width
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0.4pt}
```

### Section Formatting

```latex
\usepackage{titlesec}

% Customize section appearance
\titleformat{\section}
  {\Large\bfseries\color{blue}}
  {\thesection}
  {1em}
  {}

% Spacing around sections
\titlespacing*{\section}{0pt}{2ex}{1ex}
```

## Advanced Features

### Boxes and Highlighting

```latex
\usepackage{tcolorbox}

% Simple box
\begin{tcolorbox}[colback=blue!5,colframe=blue!40!black,title=Key Point]
  Important information here
\end{tcolorbox}

% Warning box
\begin{tcolorbox}[colback=yellow!10,colframe=orange!80!black,title=Note]
  Something to remember
\end{tcolorbox}
```

### Tables

```latex
\begin{table}[H]
  \centering
  \begin{tabular}{|l|c|r|}
    \hline
    \textbf{Header 1} & \textbf{Header 2} & \textbf{Header 3} \\
    \hline
    Row 1 & Data & 123 \\
    Row 2 & More data & 456 \\
    \hline
  \end{tabular}
  \caption{Table caption}
  \label{tab:example}
\end{table}
```

### Footnotes and Margin Notes

```latex
% Footnote
This is important\footnote{Additional details in footnote}.

% Margin note
\marginpar{Side note}
```

### Page Breaks

```latex
\newpage          % Start new page
\clearpage        % Start new page, flush floats
\pagebreak        % Break page (if possible)
\nopagebreak      % Prevent page break
```

## Handout Organization

### Section Structure

```latex
\section{Introduction}
% Overview and objectives

\section{Main Content}
\subsection{Topic 1}
% Slide + notes + context

\subsection{Topic 2}
% Slide + notes + context

\section{Conclusion}
% Summary and takeaways

\section{Additional Resources}
% References, links, further reading

\section{Appendix}
% Extra materials, code samples
```

### Reference Lists

```latex
\section{References and Resources}

\subsection{Key Papers}
\begin{itemize}
  \item Smith, J. (2023). \textit{Important Paper}. Journal Name.
  \item Jones, A. (2022). \textit{Another Study}. Conference Proceedings.
\end{itemize}

\subsection{Online Resources}
\begin{itemize}
  \item \href{https://example.com}{Resource Name} - Description
  \item \href{https://tutorial.com}{Tutorial Site} - Learning materials
\end{itemize}

\subsection{Tools and Software}
\begin{itemize}
  \item Tool Name - \url{https://tool.com}
  \item Library Name - \url{https://github.com/user/repo}
\end{itemize}
```

## Compilation

### Basic Compilation

```bash
pdflatex handout.tex
```

### With Bibliography

```bash
pdflatex handout.tex
bibtex handout
pdflatex handout.tex
pdflatex handout.tex
```

### Modern Toolchain

```bash
# Using latexmk (automatic)
latexmk -pdf handout.tex

# Clean auxiliary files
latexmk -c
```

## Common Issues

### Image Not Found

Ensure correct path:
```latex
% Relative to .tex file
\includegraphics{./images/slide.pdf}

% Tell LaTeX where to look
\graphicspath{{./images/}{./exports/}}
```

### Float Positioning

Images not appearing where expected:

```latex
% Force HERE
\usepackage{float}
\begin{figure}[H]  % Capital H
  ...
\end{figure}

% Or allow more flexibility
\begin{figure}[htbp!]
  ...
\end{figure}
```

### Text Overflow

Long URLs or code breaking margins:

```latex
% For URLs
\usepackage{url}
\url{https://very-long-url.com}

% For code
\begin{lstlisting}[breaklines=true]
  long code here
\end{lstlisting}
```

### Special Characters

LaTeX special characters need escaping:

```latex
% These need backslash
\$ \% \& \# \_ \{ \}

% Or use verb
\verb|$special_chars|

% For code, use lstlisting
```

## Best Practices

### Slide Image Formatting

**REQUIRED:**
- All slide images MUST use `\fbox{}` for black borders
- Use width of 0.72\textwidth to account for border width
- Center slides with `\centering` in figure environment
- Always include descriptive captions

**Example:**
```latex
\begin{figure}[H]
  \centering
  \fbox{\includegraphics[width=0.72\textwidth]{exports/slide-001.png}}
  \caption{Descriptive Slide Title}
  \label{fig:slide1}
\end{figure}
```

### Heading Structure

**REQUIRED:**
- Use semantic heading hierarchy rigorously
- Never skip heading levels
- Each slide gets its own `\subsubsection{}` heading
- Use `\paragraph{}` for content subdivisions within slides
- Keep heading text assertion-based and descriptive

### File Organization

```
presentation/
├── handout.tex         # Main document
├── handout.pdf         # Compiled output
├── references.bib      # Bibliography
├── images/             # Diagrams, logos
├── slides/             # Individual slide PDFs
└── exports/            # Slide deck exports
```

### Template Reuse

Create reusable section templates:

```latex
% template.tex
\newcommand{\slideandnotes}[4]{
  \subsection{#1}

  \begin{figure}[H]
    \centering
    \includegraphics[width=0.9\textwidth]{#2}
    \caption{#3}
  \end{figure}

  \subsubsection{Notes}
  #4

  \newpage
}

% Usage
\slideandnotes{Topic Name}{slides/slide-05.pdf}{Caption}{
  Notes and additional context here.
}
```

### Version Control

Comment versions in document:

```latex
% Version 1.0 - 2024-01-15 - Initial draft
% Version 1.1 - 2024-01-20 - Added section 3
% Version 2.0 - 2024-01-25 - Final revision

% Or use git info
\usepackage{gitinfo2}
```

### Accessibility

```latex
% PDF metadata
\hypersetup{
    pdftitle={Presentation Handout},
    pdfauthor={Author Name},
    pdfsubject={Topic},
    pdfkeywords={keyword1, keyword2},
    pdfproducer={LaTeX},
    pdfcreator={pdflatex}
}

% Alt text for images
\includegraphics{image.pdf}
% Described in caption or surrounding text
```

## Quick Reference

### Minimal Handout

```latex
\documentclass{article}
\usepackage{graphicx}
\usepackage{hyperref}
\title{Handout Title}
\author{Author}
\date{\today}

\begin{document}
\maketitle

\section{Introduction}
Content...

\end{document}
```

### Common Commands

```latex
\section{Title}          % Section
\subsection{Title}       % Subsection
\textbf{bold}           % Bold
\textit{italic}         % Italic
\underline{text}        % Underline
\newpage                % Page break
\vspace{1cm}            % Vertical space
\hspace{1cm}            % Horizontal space
```

---

For comprehensive LaTeX documentation, consult The LaTeX Project (https://www.latex-project.org/) and Overleaf documentation (https://www.overleaf.com/learn).
