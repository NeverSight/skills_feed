---
name: arxiv-paper-writer
description: >
  Write LaTeX ML/AI review articles for arXiv using the IEEEtran template
  and verified BibTeX citations.
compatibility: >
  Python 3.8+ for scripts. Web browsing/search for citation verification.
  LaTeX is required (pdflatex + bibtex or latexmk).
metadata:
  short-description: ML/AI review papers (IEEEtran template) with verified citations
---

# ML/AI Review Paper Workflow (IEEEtran template)

## When to Use
- ML/AI review papers for arXiv (main text ~6-10 pages; references excluded)
- LaTeX + BibTeX workflow with verified citations
- Citation validation/repair on existing LaTeX projects

## When NOT to Use
- Novel experimental research papers (this is a review workflow)
- Non-academic documents

## Inputs
- Topic description (required)
- Constraints: venue, page limit, author/affiliations (optional)
- Existing project path for citation validation (optional)

## Outputs
- `main.tex` (LaTeX source)
- `ref.bib` (verified BibTeX entries)
- `IEEEtran.cls`
- `plan/<timestamp>-<slug>.md`, `issues/<timestamp>-<slug>.csv`
- Figures/tables; `main.pdf`
- `notes/literature-notes.md` (optional per-citation notes)
- `notes/arxiv-registry.sqlite3` (arXiv metadata/BibTeX cache)

**Conventions**: run `python3 scripts/...` from this skill folder (where `scripts/` lives); `<paper_dir>` is the paper/project root (contains `main.tex`, `ref.bib`, `plan/`, `issues/`, `notes/`). Paths like `plan/...` are under `<paper_dir>`. For arXiv discovery/metadata/BibTeX, use `scripts/arxiv_registry.py` (no ad-hoc curl/wget).

---

## Gated Workflow

> Tip: Run `python3 scripts/<script>.py --help` before use.
> Open reference files only when a step calls them out.

### Non-Negotiable Rules
1. **No prose in `main.tex`** until plan approved AND issues CSV exists.
2. First deliverable: research snapshot + outline + clarification questions + draft plan.
3. **Use plan + issues tracking for all new papers; do not opt out.**
4. Issues CSV is the execution contract; update `Status` and `Verified_Citations` per issue, and add/split/insert issue rows when scope grows (do not do untracked work).
5. **Template is fixed**: use IEEEtran two-column layout (`assets/template/IEEEtran.cls`).
   Treat two-column width as a layout constraint (use two-column floats when needed).

### Gate 0: Research Snapshot + Draft Plan
1. Confirm constraints (venue, page limit, author block, date range).
2. Translate the topic into search keywords and run a light discovery pass:
   10-20 key papers (see `references/research-workflow.md`). After step 4 (once `<paper_dir>` exists), cache arXiv discovery with `arxiv_registry.py search`.
3. Propose 2-4 candidate titles aligned to the topic.
4. Scaffold the project folder and draft plan:
   ```bash
   python3 scripts/bootstrap_ieee_review_paper.py --stage kickoff --topic "<topic>"
   ```
   This copies LaTeX templates from `assets/template/`; plan/issues are generated from templates in `assets/`.
   Initialize arXiv registry (once): `python3 scripts/arxiv_registry.py --project-dir <paper_dir> init`.
5. Create a **framework skeleton** in `main.tex`
   (section headings + 2-4 bullets per section + seed citations; **no prose**).
6. Update the plan file to reflect the framework, proposed titles, and section/subsection plan.
7. Compile early: `python3 scripts/compile_paper.py --project-dir <paper_dir>`
   Fix any `Overfull \hbox` warnings (see Layout Hygiene below).
8. Return to user:
    - Proposed outline (5-8 sections, 2-4 bullets each)
    - Planned visualizations (5+) mapped to sections (see `references/visual-templates.md`)
    - Clarification questions
9. **STOP** until user approves.

### Gate 1: Create Issues CSV (after approval)
1. Check kickoff gate in plan: `- [x] User confirmed scope + outline in chat`.
2. Create issues CSV (script refuses if gate unchecked):
   ```bash
   python3 scripts/bootstrap_ieee_review_paper.py --stage issues --topic "<topic>" --with-literature-notes
   ```
3. Validate:
   ```bash
   python3 scripts/validate_paper_issues.py <paper_dir>/issues/<timestamp>-<slug>.csv
   ```
4. If literature notes are enabled, keep short summaries and (optional) abstract snippets to avoid re-search.
5. The plan may evolve; add/split/insert issues as needed, re‑validate after edits, and keep going until all issues (including inserted ones) are `DONE` or `SKIP` (when feasible, in the same run).

### Phase 2: Per-Issue Writing Loop
For each writing issue in the CSV:
- If an issue balloons (new figure, new subsection, new benchmark set, or a large QA fix), split/insert new issue row(s) (e.g., `W6a`, `Q5`) before proceeding; re-run `python3 scripts/validate_paper_issues.py <issues.csv>`; keep going until all issues are `DONE`/`SKIP`.
1. **Research**: 8-12 section-specific papers.
2. **Write**: Never 3 sentences without citations; varied paragraph rhythm
   (see `references/writing-style.md`).
   For section intent and structure, use `references/template-usage.md`.
3. **Visualize**: Match content triggers (see `references/visual-templates.md`).
   Prioritize single-column sizing; use double-column spans only when necessary (see Layout Hygiene).
   Cite externally sourced figure content.
4. **Verify**: Web search + open source page (and PDF if available) before adding to `ref.bib`.
   For arXiv entries, append BibTeX via `python3 scripts/arxiv_registry.py --project-dir <paper_dir> export-bibtex <arxiv_id> --out-bib <paper_dir>/ref.bib`.
5. **Update**: Mark issue `DONE` with `Verified_Citations` count.
6. Compile after meaningful changes; fix `Overfull \hbox` before marking `DONE`.

### Phase 2.5: Rhythm Refinement
After all writing issues are `DONE`, refine prose section-by-section using the `latex-rhythm-refiner` skill. This step varies sentence/paragraph lengths and removes filler phrases while preserving all citations.

### Phase 3: QA Gate
1. Run internal QA checklist (see `references/quality-report.md`).
2. Compile; ensure no `Overfull \hbox` warnings in `main.log`.
3. Deliver `main.tex`, `ref.bib`, figures, and `main.pdf`.

---

## Existing Paper Workflow (No Re-Scaffold)
If a paper folder already exists, do NOT rerun scaffold:
```bash
# Create plan
python3 scripts/create_paper_plan.py --topic "<topic>" --stage plan --output-dir <paper_dir>
# STOP for approval, then check kickoff gate box
# Create issues (use timestamp/slug from plan filename/frontmatter)
python3 scripts/create_paper_plan.py --topic "<topic>" --stage issues --timestamp "<TS>" --slug "<slug>" --output-dir <paper_dir> --with-literature-notes
```

## Citation-Validation Variant
1. Treat provided path as LaTeX project root.
2. Follow `references/citation-workflow.md`.
3. Use `references/bibtex-guide.md` for BibTeX rules if entries need repair.
4. Deliver validation report and corrected `ref.bib` if requested.

---

## Success Criteria

**Compilation**: `python3 scripts/compile_paper.py --project-dir <paper_dir>` (exit 0, no "Citation undefined" warnings). Use `--report-page-counts` for main-text page count.

**Quality Metrics**:
- 6-10 pages of main text (references excluded)
- 60-80 total citations (8+ per section)
- 100% citation verification rate
- 70%+ citations from last 3 years
- 5+ visualization types
- All issues `DONE` or `SKIP`

---

## Safety & Guardrails
- **Never fabricate** citations or results; add TODO and ask user if evidence missing.
- **Verify every citation** via web search + source page (and PDF if available) before adding to `ref.bib`.
- **Confirm before** large literature searches.
- **Do not overwrite** user files without confirmation.
- **Issues CSV** is the contract; mark `DONE` only when criteria met.
- **No submission bundles** unless user requests.

## Layout Hygiene
Fix `Overfull \hbox` warnings before marking issues `DONE`:
- Figures: start with `figure` + `\columnwidth`; switch to `figure*` + `\textwidth` if needed
- Tables: prefer `p{...}` column widths / `\tabcolsep` over `\resizebox`
- Equations: use `split`, `multline`, `aligned`, or `IEEEeqnarray` for line-breaking

---

## Issues CSV Schema
| Phase | Issues |
|-------|--------|
| Research | Rx: discovery, scaffolding, framework, viz planning |
| Writing | Wx: each section with target citations and visualization |
| Refinement | RFx: apply `latex-rhythm-refiner` skill (after all Wx DONE) |
| QA | Qx: citation verification, QA checklist, compilation, final review |

Status: `TODO` → `DOING` → `DONE`. Schema validated by `validate_paper_issues.py`.
