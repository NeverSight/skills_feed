---
name: latex-document
description: >
  Universal LaTeX document skill: create, compile, and convert any document to
  professional PDF with PNG previews. Supports resumes, reports, cover letters,
  invoices, academic papers, theses/dissertations, academic CVs, presentations
  (Beamer), scientific posters, formal letters, exams/quizzes, books,
  cheat sheets, reference cards, exam formula sheets,
  fillable PDF forms (hyperref form fields), conditional content (etoolbox toggles),
  mail merge from CSV/JSON (Jinja2 templates), version diffing (latexdiff),
  charts (pgfplots + matplotlib), tables (booktabs + CSV import), images (TikZ),
  Mermaid diagrams, AI-generated images, watermarks, landscape pages,
  bibliography/citations (BibTeX/biblatex), multi-language/CJK (auto XeLaTeX),
  algorithms/pseudocode, colored boxes (tcolorbox), SI units (siunitx),
  Pandoc format conversion (Markdown/DOCX/HTML ↔ LaTeX),
  and PDF-to-LaTeX conversion of handwritten or printed documents (math, business,
  legal, general). Compile script supports pdflatex, xelatex, lualatex with
  auto-detection, latexmk backend, texfot log filtering, PDF/A output, and
  verbosity control (--verbose/--quiet). Empirically optimized scaling: single agent 1-10 pages, split
  11-20, batch-7 pipeline 21+. Use when user asks to: (1) create a resume/CV/cover
  letter, (2) write a LaTeX document, (3) create PDF with tables/charts/images,
  (4) compile a .tex file, (5) make a report/invoice/presentation, (6) anything
  involving LaTeX or pdflatex, (7) convert/OCR a PDF to LaTeX, (8) convert
  handwritten notes, (9) create charts/graphs/diagrams, (10) create slides,
  (11) write a thesis or dissertation, (12) create an academic CV, (13) create
  a poster, (14) create an exam/quiz, (15) create a book, (16) convert between
  document formats (Markdown, DOCX, HTML to/from LaTeX), (17) generate Mermaid
  diagrams for LaTeX, (18) create a formal business letter, (19) create a cheat
  sheet or reference card, (20) create an exam formula sheet or crib sheet,
  (21) condense lecture notes/PDFs into a cheat sheet,
  (22) create a fillable PDF form with text fields/checkboxes/dropdowns,
  (23) create a document with conditional content/toggles (show/hide sections),
  (24) generate batch/mail-merge documents from CSV/JSON data,
  (25) create a version diff PDF (latexdiff) highlighting changes between documents,
  (26) create a homework or assignment submission with problems and solutions,
  (27) create a lab report with data tables, graphs, and error analysis,
  (28) encrypt or password-protect a PDF,
  (29) merge multiple PDFs into one,
  (30) optimize/compress a PDF for web or email,
  (31) lint or check a LaTeX document for common issues,
  (32) count words in a LaTeX document,
  (33) analyze document statistics (figures, tables, citations),
  (34) fetch BibTeX from a DOI,
  (35) convert a Graphviz .dot file to PDF/PNG,
  (36) convert a PlantUML .puml file to PDF/PNG,
  (37) create a one-pager/fact sheet/executive summary,
  (38) create a datasheet or product specification sheet,
  (39) extract pages from a PDF (page ranges, odd/even),
  (40) check LaTeX package availability before compiling,
  (41) analyze citations and cross-reference with .bib files,
  (42) debug LaTeX compilation errors,
  (43) make a document accessible (PDF/A, tagged PDF),
  (44) create lecture notes or course handouts,
  (45) fill an existing PDF form (fillable fields or non-fillable with annotations),
  (46) extract text or tables from a PDF (pdfplumber, pypdf),
  (47) OCR a scanned PDF to text (pytesseract),
  (48) create a PDF programmatically with reportlab (Canvas, Platypus),
  (49) rotate or crop PDF pages (pypdf),
  (50) add a watermark to an existing PDF,
  (51) extract metadata from a PDF (title, author, subject).
---

# LaTeX Document Skill

Create any LaTeX document, compile to PDF, and generate PNG previews. Convert PDFs of any type to LaTeX.

## Workflow: Create Documents

1. Determine document type (resume, report, letter, invoice, article, thesis, academic CV, presentation, poster, exam, book, cheat sheet)
2. **If poster:** Run the poster sub-workflow (see [Poster Sub-Workflow](#poster-sub-workflow) below), then skip to step 5.
3. **If cheat sheet / reference card:** Run the cheat sheet sub-workflow (see [Cheat Sheet / Reference Card Sub-Workflow](#cheat-sheet--reference-card-sub-workflow) below), then skip to step 5.
4. **Ask the user which enrichment elements they want** (use AskUserQuestion tool with multiSelect). Offer relevant options based on document type:
   - **AI-generated images** -- custom illustrations, diagrams, photos (uses generate-image skill)
   - **Charts/graphs** -- bar, line, pie, scatter, heatmap (pgfplots or matplotlib)
   - **Flowcharts/diagrams** -- process flows, architecture, decision trees (TikZ or Mermaid)
   - **Citations/bibliography** -- academic references, footnotes, works cited (BibTeX/biblatex)
   - **Tables with data** -- comparison matrices, financial data, statistics (booktabs)
   - **Watermarks** -- DRAFT, CONFIDENTIAL, or company logo background
   - Skip this step for simple documents (cover letters, invoices) or when the user has already specified exactly what they want.
5. Copy the appropriate template from `assets/templates/` or write from scratch
6. Customize content based on user requirements
7. Generate external assets based on user's element choices:
   - AI images: `python3 <skill_path>/../generate-image/scripts/generate_image.py "prompt" --output ./outputs/figure.png`
   - matplotlib charts: `python3 <skill_path>/scripts/generate_chart.py <type> --data '<json>' --output chart.png`
   - Mermaid diagrams: `bash <skill_path>/scripts/mermaid_to_image.sh diagram.mmd output.png`
8. **For documents 5+ pages:** Review the [Long-Form Document Anti-Patterns](#long-form-document-anti-patterns-must-read-for-reports-theses-books) section and run the Content Generation Checklist before compiling. Key rules: prefer prose over bullets, include global list compaction, escape `<`/`>` in text mode, vary section formats, limit `\newpage`, size images at 0.75-0.85 textwidth.
9. Compile with `scripts/compile_latex.sh` (auto-detects XeLaTeX for CJK/RTL, glossaries, bibliography)
10. Show PNG preview to user, deliver PDF

### Poster Sub-Workflow

When the user requests a poster: read [references/poster-design-guide.md](references/poster-design-guide.md) for the complete workflow including conference size presets (NeurIPS/ICML/CVPR/ICLR dimensions), layout archetypes (Traditional/BetterPoster/Visual-Heavy), color schemes, and typography standards. Use `poster.tex` (portrait) or `poster-landscape.tex` (landscape). Ask the user for conference/orientation, layout style, and color scheme using AskUserQuestion, then proceed to step 5.

### Cheat Sheet / Reference Card Sub-Workflow

When the user requests a cheat sheet, reference card, or formula sheet:

1. Read [references/cheatsheet-guide.md](references/cheatsheet-guide.md) for the complete workflow including template selection, content budgets, typography rules, and the PDF-to-cheatsheet pipeline.
2. Select template: `cheatsheet.tex` (general, 3-col landscape), `cheatsheet-exam.tex` (exam formula, 2-col portrait), or `cheatsheet-code.tex` (programming, 4-col landscape).
3. Follow the guide's workflow steps, then return to main workflow step 5.

## Workflow: Mail Merge (Batch Personalized Documents)

Generate N personalized documents from a LaTeX template + CSV/JSON data source using `scripts/mail_merge.py`. Template syntax: `{{variable}}` for simple substitution, Jinja2 (`<< >>`, `<% %>`) for conditionals/loops. See `assets/templates/mail-merge-letter.tex` for an example. Full guide: [references/interactive-features.md](references/interactive-features.md).

## Workflow: Version Diffing (latexdiff)

Generate highlighted change-tracked PDFs using `scripts/latex_diff.sh`. Supports file-to-file diff, git revision diff, multi-file flatten, and custom markup styles. Full guide: [references/interactive-features.md](references/interactive-features.md).

## Workflow: Convert Document Formats

Convert between Markdown, DOCX, HTML, and LaTeX using `scripts/convert_document.sh`. Full guide: [references/format-conversion.md](references/format-conversion.md).

## Workflow: Convert PDF to LaTeX

Convert existing PDFs (handwritten notes, printed reports, legal docs) to LaTeX. Full pipeline: [references/pdf-conversion.md](references/pdf-conversion.md).

**Quick steps**: Split PDF into page images (`scripts/pdf_to_images.sh`), select a conversion profile, create shared preamble, apply scaling strategy, validate with `scripts/validate_latex.py`, concatenate, compile.

**Scaling strategy**: 1-10 pages = single agent; 11-20 pages = split in half (2 agents); 21+ pages = batch-7 pipeline (ceil(N/7) agents with `run_in_background: true`).

**Conversion profiles** (in `references/profiles/`): `math-notes.md` (equations, theorems -- has beautiful mode), `business-document.md` (reports, memos), `legal-document.md` (contracts, statutes), `general-notes.md` (handwritten, mixed content).

## Workflow: Fill PDF Forms

Fill existing PDF forms -- both fillable (with form fields) and non-fillable (image-based). Full guide: [references/pdf-operations.md](references/pdf-operations.md).

**Step 1: Check form type:**
```bash
python3 <skill_path>/scripts/pdf_check_form.py form.pdf
```

**If fillable** (has form fields):
```bash
# Extract field metadata
python3 <skill_path>/scripts/pdf_extract_fields.py form.pdf field_info.json
# Create field_values.json with values for each field, then fill
python3 <skill_path>/scripts/pdf_fill_form.py form.pdf field_values.json output.pdf
```

**If non-fillable** (no form fields):
```bash
# Convert to images for visual analysis
bash <skill_path>/scripts/pdf_to_images.sh form.pdf ./tmp/pages
# Visually identify fields, create fields.json with bounding boxes
# Validate bounding boxes (+ optional validation image)
python3 <skill_path>/scripts/pdf_validate_boxes.py fields.json --image page_1.png --output validation.png --page 1
# Fill with text annotations
python3 <skill_path>/scripts/pdf_fill_annotations.py form.pdf fields.json output.pdf
```

## Workflow: Advanced PDF Operations

For text/table extraction (pdfplumber), OCR (pytesseract), programmatic PDF creation (reportlab), watermarking, page rotation/cropping, metadata extraction, JavaScript libraries (pdf-lib, pdfjs-dist), and batch processing, see [references/pdf-operations.md](references/pdf-operations.md).

## Compile Script

```bash
# Basic compile (auto-detects engine)
bash <skill_path>/scripts/compile_latex.sh document.tex

# Compile + generate PNG previews
bash <skill_path>/scripts/compile_latex.sh document.tex --preview

# Compile + PNG in specific directory
bash <skill_path>/scripts/compile_latex.sh document.tex --preview --preview-dir ./outputs

# Force a specific engine
bash <skill_path>/scripts/compile_latex.sh document.tex --engine xelatex
bash <skill_path>/scripts/compile_latex.sh document.tex --engine lualatex

# Use latexmk for automatic multi-pass (recommended for complex documents)
bash <skill_path>/scripts/compile_latex.sh document.tex --use-latexmk --preview

# PDF/A output for thesis submissions and archival compliance
bash <skill_path>/scripts/compile_latex.sh document.tex --pdfa

# Verbose output for debugging compilation issues
bash <skill_path>/scripts/compile_latex.sh document.tex --verbose

# Quiet mode for batch/CI jobs (only errors shown)
bash <skill_path>/scripts/compile_latex.sh document.tex --quiet

# Clean auxiliary files only (no compilation)
bash <skill_path>/scripts/compile_latex.sh document.tex --clean
```

### Compilation Flags

| Flag | Description |
|---|---|
| `--preview` | Generate PNG previews of each page after compilation |
| `--preview-dir DIR` | Directory for PNG output (default: same as .tex file) |
| `--engine ENGINE` | Force engine: `pdflatex`, `xelatex`, or `lualatex` |
| `--use-latexmk` | Use `latexmk` as compilation backend (auto multi-pass, bibliography, index) |
| `--verbose` | Show full compilation output (all engine logs) |
| `--quiet` | Suppress all non-error output |
| `--clean` | Remove auxiliary files (.aux, .log, .bbl, .fdb_latexmk, etc.) and exit |
| `--pdfa` | Produce PDF/A-2b compliant output (auto-injects `pdfx` package) |
| `--auto-fix` | Auto-fix common compilation errors (float placement, encoding) |

### Compilation Backends

**Manual multi-pass (default):** Runs the engine multiple times with bibliography/index/glossary passes as needed. This is the traditional approach and works without `latexmk` installed.

**latexmk (`--use-latexmk`):** Uses `latexmk` for automatic dependency-driven compilation. Recommended for complex documents with bibliographies, indexes, glossaries, or cross-references -- latexmk determines the correct number of passes automatically. Requires `latexmk` (included with TeX Live).

### Log Filtering (texfot)

When `texfot` is installed (included with TeX Live), compilation output is automatically filtered to show only relevant warnings and errors, suppressing noisy package loading messages. This applies in the default verbosity mode. Use `--verbose` to see unfiltered output, or `--quiet` to suppress all non-error output.

**Engine auto-detection**: If the .tex file uses `fontspec`, `xeCJK`, or `polyglossia`, the script automatically uses `xelatex`. If it uses `luacode` or `luatextra`, it uses `lualatex`. Otherwise defaults to `pdflatex`. Override with `--engine`.

The script auto-installs `texlive` (including `texlive-science`, `texlive-xetex`, `texlive-luatex`, `biber`) and `poppler-utils` if missing. It auto-detects `\bibliography{}` (runs bibtex), `\addbibresource{}` (runs biber), `\makeindex` (runs makeindex), `\makeglossaries` (runs makeglossaries), runs the correct number of passes, generates PNG previews with `pdftoppm`, and cleans auxiliary files.

## Script & Tool Reference

For PDF utilities (encrypt, merge, optimize, extract pages, pdf-to-images), LaTeX quality tools (lint, word count, analysis, package check, citations), compilation auto-fix, bibliography fetching, and diagram scripts (Mermaid, Graphviz, PlantUML), see [references/script-tools.md](references/script-tools.md).

## Templates

Copy from `assets/templates/` and customize.

### Resume Templates (5 ATS-Compatible Options)

Select based on experience level, industry, and ATS requirements. See [references/resume-ats-guide.md](references/resume-ats-guide.md) for full ATS guidance.

| Template | Best For | Key Feature | ATS Score |
|---|---|---|---|
| **`resume-classic-ats.tex`** | Finance, law, government, any ATS portal | Zero graphics, plain text only, maximum parse safety | 10/10 |
| **`resume-modern-professional.tex`** | Tech, corporate, general professional | Subtle color accents, clean design, good ATS + human appeal | 9/10 |
| **`resume-executive.tex`** | VP, Director, C-suite (5-15+ years) | Two-page, executive summary, board roles, P&L focus | 9/10 |
| **`resume-technical.tex`** | Software, data, engineering roles | Skills-first hybrid, projects section, tech stack emphasis | 9/10 |
| **`resume-entry-level.tex`** | New graduates, career starters | Education-first, one page, coursework, activities | 9/10 |

All 5 templates follow ATS rules: single-column, no graphics/images, no tables for layout, standard section headings, contact info in body (not header/footer).

### STEM Student Templates

- **`homework.tex`** -- Homework/assignment submission template (`article` class, 11pt) with toggle-able solutions (`\showsolutionstrue`/`\showsolutionsfalse`), custom problem/solution environments, honor code section, `fancyhdr` headers, `amsmath`+`amssymb`+`amsthm` math, `listings` code highlighting (Python, Java, C++, Matlab styles), `enumitem` for (a), (b), (c) sub-parts, `hyperref`. Customization via `\coursename`, `\assignmentnumber`, `\studentname`, `\studentid`, `\duedate`. Example problems: calculus, proof by induction, Python coding, matrix algebra, kinematics, Java OOP.
- **`lab-report.tex`** -- STEM lab report template (`article` class, 11pt) with `siunitx` for uncertainties and SI units, `pgfplots` for data visualization, `booktabs` for professional tables, `amsmath` for equations, `fancyhdr` headers, `caption`+`subcaption` for figures. Structured sections: abstract, theory, procedure, data/results (with uncertainty tables), analysis (pgfplots graphs), discussion (error analysis), conclusion, references, appendix. Example: pendulum period measurement with error propagation.

### Other Templates

- **`lecture-notes.tex`** -- Beautiful lecture notes (`scrartcl` KOMA-Script class) with Palatino font, `microtype` typography, color-coded `tcolorbox` theorem environments (blue theorems, green definitions, orange examples, purple remarks), TikZ graph theory diagram styles and macros (`\CompleteGraph`, `\CycleGraph`, `\PathGraph`), styled section headings with `titlesec`, `fancyhdr` headers, `hyperref` + `cleveref` navigation. Ideal for converting handwritten math/science notes to beautiful PDFs. Includes graph theory custom commands (`\V`, `\E`, `\deg`, `\chr`). Used by the math-notes conversion profile in beautiful mode.
- **`thesis.tex`** -- Thesis/dissertation (`book` class) with title page, declaration, abstract, acknowledgments, TOC, list of figures/tables, chapters, appendices, bibliography. Front matter uses roman numerals, main matter uses arabic. Includes theorem environments.
- **`academic-cv.tex`** -- Multi-page academic CV with publications (journal/conference/preprint sections), grants and funding, teaching, advising (current/graduated students), awards, professional service, invited talks. ORCID and Google Scholar links.
- **`book.tex`** -- Full book (`book` class) with half-title, title page, copyright page, dedication, preface, acknowledgments, TOC, list of figures/tables, parts, chapters, appendix, bibliography, index. Custom chapter headings, epigraphs, fancyhdr, microtype.
- **`poster.tex`** -- Conference poster (`tikzposter` class, A0 portrait) with 2-column layout, QR code, 5 color schemes, tikzfigure charts, tables, coloredbox highlights. Includes commented **#BetterPoster** layout variant (central billboard + sidebars). Portrait is standard for most conferences. See poster design guide for conference size presets.
- **`poster-landscape.tex`** -- Landscape conference poster (`tikzposter` class, A0 landscape) with 3-column (30/40/30) layout, QR code, tech purple color scheme. For CS/ML conferences (NeurIPS, ICML, CVPR, ICLR). Includes commented `\geometry{}` presets for CVPR/NeurIPS custom sizes.
- **`cheatsheet.tex`** -- General reference card (`extarticle` class, landscape A4, 7pt base font) with 3-column `multicols` layout, `tcolorbox` colored section boxes, tight spacing. For command references, concept summaries, quick-reference guides. Supports front+back printing.
- **`cheatsheet-exam.tex`** -- Exam formula sheet (`extarticle` class, portrait A4, 6pt base font) with 2-column layout, maximum content density, black-and-white printer-safe. For university exam "allowed cheat sheets" with formulas, theorems, definitions. Optimized for single-sided printing.
- **`cheatsheet-code.tex`** -- Programming reference card (`extarticle` class, landscape A4, 7pt base font) with 4-column layout, `minted` syntax highlighting, monospace font emphasis. For language syntax, API reference, CLI commands, keyboard shortcuts.
- **`letter.tex`** -- Formal business letter with colored letterhead bar, TikZ logo placeholder, company info, recipient block, date, subject line, signature. Professional corporate appearance.
- **`exam.tex`** -- Exam/quiz (`exam` class) with grading table, multiple question types (multiple choice, true/false, fill-in-blank, matching, short answer, essay), point values, solution toggle via `\printanswers`.
- **`report.tex`** -- Business report with TOC, headers/footers, data tables, bar chart (pgfplots), process flowchart (TikZ), recommendations
- **`cover-letter.tex`** -- Professional cover letter with sender/recipient blocks
- **`invoice.tex`** -- Invoice with company header, line items table, subtotal/tax/total
- **`academic-paper.tex`** -- Research paper with abstract, sections, bibliography, figures. Includes example `.bib` file (`references.bib`) for BibTeX citations.
- **`presentation.tex`** -- Beamer presentation with title slide, content frames, columns
- **`fillable-form.tex`** -- Fillable PDF form (`article` class) with hyperref form fields: text inputs, checkboxes, radio buttons, dropdowns, push buttons. Two-column layout with `tabularx`. Custom `\FormField`, `\FormCheck`, `\FormDropdown` helper commands. Requires Adobe Reader for full form support (browser PDF viewers have limited form capabilities).
- **`conditional-document.tex`** -- Configurable document (`article` class) with etoolbox toggle system: show/hide TOC, appendix, watermark, draft mode, confidential marking, abstract. Template variables via `\providecommand` (title, author, org, version). Three visual profiles (corporate, academic, minimal). Supports command-line variable passing for CI/CD.
- **`mail-merge-letter.tex`** -- Mail merge letter template with `{{variable}}` placeholders for use with `scripts/mail_merge.py`. Company-branded letterhead, recipient address block, body text with data-driven personalization. Pair with CSV/JSON data source.
- **`resume.tex`** -- Legacy resume template (has photo area and tables -- not ATS-optimized)

Usage:
```bash
cp <skill_path>/assets/templates/resume-classic-ats.tex ./outputs/my_resume.tex
# Edit content, then compile
bash <skill_path>/scripts/compile_latex.sh ./outputs/my_resume.tex --preview --preview-dir ./outputs
```

## Document Type Selection

| User Request | Template | Document Class |
|---|---|---|
| Resume, CV (ATS-safe) | `resume-classic-ats.tex` | `article` |
| Resume (modern look) | `resume-modern-professional.tex` | `article` |
| Resume (senior/executive) | `resume-executive.tex` | `article` |
| Resume (technical/engineering) | `resume-technical.tex` | `article` |
| Resume (new graduate) | `resume-entry-level.tex` | `article` |
| Homework, assignment, problem set | `homework.tex` | `article` |
| Lab report, experiment writeup | `lab-report.tex` | `article` |
| Lecture notes, math notes (beautiful) | `lecture-notes.tex` | `scrartcl` |
| Thesis, dissertation | `thesis.tex` | `book` |
| Academic CV (publications, grants) | `academic-cv.tex` | `article` |
| Report, analysis | `report.tex` | `article` |
| Cover letter | `cover-letter.tex` | `article` |
| Invoice | `invoice.tex` | `article` |
| Academic paper | `academic-paper.tex` + `references.bib` | `article` |
| Book | `book.tex` | `book` |
| Scientific poster (portrait) | `poster.tex` | `tikzposter` |
| Scientific poster (landscape) | `poster-landscape.tex` | `tikzposter` |
| Cheat sheet, reference card | `cheatsheet.tex` | `extarticle` |
| Exam formula sheet, crib sheet | `cheatsheet-exam.tex` | `extarticle` |
| Programming reference card | `cheatsheet-code.tex` | `extarticle` |
| Formal business letter | `letter.tex` | `article` |
| Exam, quiz, test | `exam.tex` | `exam` |
| Slides, presentation | `presentation.tex` | `beamer` |
| Fillable PDF form | `fillable-form.tex` | `article` |
| Conditional/configurable document | `conditional-document.tex` | `article` |
| Mail merge, batch letters | `mail-merge-letter.tex` + `scripts/mail_merge.py` | `article` |
| **Version diff (latexdiff)** | Use `scripts/latex_diff.sh` + see [interactive-features.md](references/interactive-features.md) | varies |
| **Convert PDF to LaTeX** | Select profile + see [pdf-conversion.md](references/pdf-conversion.md) | varies |
| **Convert formats** | Use `scripts/convert_document.sh` + see [format-conversion.md](references/format-conversion.md) | varies |
| **Mail merge from CSV/JSON** | Use `scripts/mail_merge.py` + see [interactive-features.md](references/interactive-features.md) | varies |

## Key LaTeX Patterns

### Escaping Special Characters

Always escape: `%` → `\%`, `$` → `\$`, `&` → `\&`, `#` → `\#`, `_` → `\_`

**Angle brackets in text mode:** `<` and `>` are NOT valid in LaTeX text mode with T1 encoding. They render as inverted question marks (¡ or ¿). Always use math mode or text commands:
- `<5%` → `$<$5\%` or `\textless 5\%`
- `>50` → `$>$50` or `\textgreater 50`
- `<$300` → `$<$\$300`
- `>=` → `$\geq$`, `<=` → `$\leq$`

This is one of the most common silent errors in generated LaTeX — the document compiles without errors but the PDF shows garbage characters.

Date ranges use en-dash: `2019--2025` (double hyphen).

### Standard Preamble

```latex
\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{geometry}
\usepackage{hyperref}
\usepackage{xcolor}
\usepackage{graphicx}
\usepackage{tabularx}
\usepackage{colortbl}
\usepackage{enumitem}
\usepackage{titlesec}
```

### Code Patterns (load as needed)

For ready-to-use LaTeX code snippets (tables, charts, flowcharts, bibliography, watermarks, landscape pages, multi-language, images, Mermaid diagrams, matplotlib charts, CSV tables, AI images, fillable forms, conditional content, mail merge, version diff), read [references/code-patterns.md](references/code-patterns.md).

## Visual Elements in Reports

When creating reports, use the enrichment elements the user selected in step 4. For the quick reference table of visual element tools (charts, flowcharts, AI images, tables, timelines) and sizing guidelines, see [references/advanced-features.md](references/advanced-features.md). Use `\begin{figure}[H]` (from `float` package) to prevent figures from floating. Size TikZ diagrams with `width=0.8\textwidth` or smaller.

## Reference Guides (load as needed)

When uncertain about LaTeX patterns, compilation issues, or document quality, consult this table and load relevant files.

| Topic | File | When to Read |
|---|---|---|
| Long-Form Best Practices | [long-form-best-practices.md](references/long-form-best-practices.md) | **MUST READ for 5+ page documents**: 9 anti-patterns, report preamble, content generation checklist |
| Code Patterns (LaTeX snippets) | [code-patterns.md](references/code-patterns.md) | Ready-to-use LaTeX code: tables, charts, flowcharts, bibliography, watermarks, landscape, multi-lang, images, forms, mail merge, diffs |
| Script & Tool Reference | [script-tools.md](references/script-tools.md) | PDF utilities (encrypt, merge, optimize, extract), LaTeX quality tools (lint, wordcount, analysis), compilation auto-fix, bibliography, diagrams |
| Bibliography/Citations | [bibliography-guide.md](references/bibliography-guide.md) | BibTeX/biblatex, citation styles, .bib format |
| Advanced Features & Visual Elements | [advanced-features.md](references/advanced-features.md) | Watermarks, landscape, multi-lang, code, algorithms, tcolorbox, siunitx, advanced charts, AI images, visual elements reference table |
| Mermaid Diagrams | [mermaid-diagrams.md](references/mermaid-diagrams.md) | Flowcharts, sequence, class, ER, Gantt, pie, mindmap |
| Python Charts (matplotlib) | [python-charts.md](references/python-charts.md) | Bar, line, scatter, pie, heatmap, box, histogram, area, radar |
| Format Conversion (Pandoc) | [format-conversion.md](references/format-conversion.md) | Markdown/DOCX/HTML to/from LaTeX |
| Tables and Images | [tables-and-images.md](references/tables-and-images.md) | Colored rows, multi-row/column, booktabs, long tables, images, TikZ |
| Charts and Graphs (pgfplots) | [charts-and-graphs.md](references/charts-and-graphs.md) | Line plots, bar charts, scatter plots, pie charts in pgfplots |
| LaTeX Packages | [packages.md](references/packages.md) | Common packages reference |
| Poster Design Guide | [poster-design-guide.md](references/poster-design-guide.md) | Conference size presets, typography, color schemes, layout archetypes, content guidelines |
| Resume ATS Guide | [resume-ats-guide.md](references/resume-ats-guide.md) | ATS rules, LaTeX pitfalls, keywords |
| PDF-to-LaTeX Pipeline | [pdf-conversion.md](references/pdf-conversion.md) | Full conversion pipeline, scaling strategy, worker agents, validation |
| Interactive Features | [interactive-features.md](references/interactive-features.md) | Fillable PDF forms, conditional content, mail merge from CSV/JSON, latexdiff version tracking |
| Cheat Sheet Design | [cheatsheet-guide.md](references/cheatsheet-guide.md) | Template selection, typography, density optimization, PDF-to-cheatsheet pipeline |
| PDF-to-Cheatsheet Prompts | [pdf-extraction-prompts.md](references/pdf-extraction-prompts.md) | LLM prompts for extraction stages: structure analysis, subject-specific extraction, compression, formatting |
| Visual Packages (TikZ) | [visual-packages.md](references/visual-packages.md) | 24 installed TikZ/visualization packages with working examples |
| Graphviz & PlantUML | [graphviz-plantuml.md](references/graphviz-plantuml.md) | .dot to PDF/PNG, .puml to PDF/PNG, LaTeX integration |
| Debugging & Errors | [debugging-guide.md](references/debugging-guide.md) | Reading LaTeX errors, 20 common errors, .log analysis, silent failures |
| Accessibility & PDF/A | [accessibility-guide.md](references/accessibility-guide.md) | PDF/A for thesis, PDF/UA for screen readers, tagged PDFs, alt text |
| Beamer Presentations | [beamer-guide.md](references/beamer-guide.md) | Themes, overlays/animations, code slides, handouts, presenter notes |
| Font Selection | [font-guide.md](references/font-guide.md) | Font families, fontspec, mathematical fonts, fontawesome5, microtype, CJK |
| Collaboration & CI/CD | [collaboration-guide.md](references/collaboration-guide.md) | Git for LaTeX, GitHub Actions, Docker, multi-author workflows |
| PDF Operations | [pdf-operations.md](references/pdf-operations.md) | Form filling (fillable + non-fillable), text/table extraction (pdfplumber), OCR (pytesseract), programmatic PDF creation (reportlab), watermarking, rotation/cropping, metadata, JavaScript (pdf-lib, pdfjs-dist), batch processing, performance tips |

## Critical Notes and Common Mistakes

### Compile & Output
- Run compile script from the directory containing the .tex file, or use absolute paths
- Place output .tex files in `./outputs/` for user visibility
- After compilation, read the PNG preview files to show the user how the document looks
- PNG previews require `poppler-utils` (auto-installed by script)

### Package Dependency Errors (MUST READ)
These cause `Undefined control sequence` -- always include the required package:

| If you use... | You MUST include | Error without it |
|---|---|---|
| `\rowcolor{}` | `\usepackage{colortbl}` | Undefined control sequence `\rowcolor` |
| `\url{}` in .bib with natbib | `\usepackage{url}` | Undefined control sequence `\url` |
| `\checkmark` | `\usepackage{amssymb}` | Undefined control sequence `\checkmark` |
| `\begin{figure}[H]` | `\usepackage{float}` | Unknown float option `H` |
| `\rowcolors{}{}{}` | `\usepackage[table]{xcolor}` or `\usepackage{colortbl}` | Undefined control sequence |

### hyperref Package
- `hyperref` is fine for normal documents (most templates use it).
- Only avoid it in **PDF-to-LaTeX converted documents** with theorem environments, where it causes `\set@color` errors.

### Compilation Environment
- If texlive is not installed, the compile script auto-installs it. Do NOT run multiple compile commands in parallel before texlive is installed -- they will all try to install simultaneously, causing dpkg lock contention. Install once first or run compiles sequentially.
- The compile script uses `-interaction=nonstopmode` (not `-halt-on-error`) to ensure PDFs are produced even with warnings. This is intentional -- many documents produce warnings on first pass that resolve on subsequent passes.
- **latexmk** and **texfot** are included with TeX Live. The setup script (`setup.sh`) verifies their availability. latexmk is used when `--use-latexmk` is passed; texfot is used automatically when available (default verbosity mode).
- A `.chktexrc` configuration file is included at the skill root to suppress common false positives when linting generated LaTeX documents. The `latex_lint.sh` script uses it automatically.

## Long-Form Document Anti-Patterns

For documents 5+ pages (reports, theses, books), read [references/long-form-best-practices.md](references/long-form-best-practices.md) for 9 critical anti-patterns, the report preamble best practices, and the content generation checklist. **This is MUST-READ material before generating any long document.**
