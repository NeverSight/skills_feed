---
name: datasheet-intelligence
description: "This skill is triggered when a request needs datasheet/TRM-grounded hardware facts or firmware init code with page/section citations. Keywords: datasheet, TRM, register map, base address, bitfield, reset value, pin mux, clock divider, init code, 데이터시트, 레지스터, 초기화 코드."
argument-hint: "[document-path] [task-or-keywords]"
---

# Datasheet Intelligence

## Objective

- Produce evidence-grounded hardware answers and code from `PDF`/`DOCX`/`XLSX` datasheets.
- Prefer fast mode by default; use `--structured` only when table/header fidelity is required.

## Context Policy

- Keep `SKILL.md` minimal and procedural.
- Run `scripts/toc.py`, `scripts/search.py`, `scripts/read.py` directly before loading extra references.
- Load `references/usage.md` only for detailed flags or format-specific examples.

## Prerequisites

Use `uv` with this skill's `pyproject.toml` and `uv.lock`.
Do not rely on PEP 723 inline script metadata.

```bash
# Install uv if needed
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Use one of these execution contexts:

- Recommended (works from any directory): `uv run --project skills/datasheet-intelligence ...`
- Alternative: `cd skills/datasheet-intelligence && uv run ...`

All command examples below use the recommended `--project` style.

## Mandatory Execution Loop

1. MUST identify candidate pages first with `scripts/toc.py` or `scripts/search.py` before large reads.
2. MUST read targeted ranges with `scripts/read.py --pages` and expand iteratively.
3. MUST verify every critical claim (address, bit position, reset value, formula) with `source file + page/section`.
4. MUST rerun extraction on mismatch or ambiguity (`search -> read -> search`).
5. MUST follow `Tip:` / `Try:` guidance from script errors, then rerun.
6. MUST not finalize the answer until critical code settings are mapped to citations.

## Workflow

### PDF Datasheets

Choose the strategy by document size.

#### Small (< 50 pages)

1. Run `scripts/toc.py` (use `--structured` if bookmarks are missing).
2. Run `scripts/read.py --pages` for relevant sections.
3. Add `--structured` if tables are broken.

#### Medium (50-150 pages)

1. Run `scripts/toc.py --filter` to narrow sections.
2. Run `scripts/search.py` to locate exact pages.
3. Run `scripts/read.py --pages` for focused ranges (use `--structured` for table-heavy ranges).

#### Large (>= 150 pages)

Never read the whole document at once.

1. Run `scripts/toc.py` to map sections and page ranges.
2. If `scripts/toc.py` reports no bookmarks, switch immediately to `scripts/search.py` (search-first) instead of full `--structured` TOC.
3. Skip low-value sections (Legal, Revision History, Ordering Info, Package Drawing).
4. Run `scripts/search.py` for exact keyword locations (`--unique-pages` recommended for long documents).
5. Run `scripts/read.py --pages` in 10-30 page chunks.
6. Iterate: read -> discover new keywords -> search again -> read again.

High-priority large-PDF sections:

| Priority | Section | Why |
| --- | --- | --- |
| High | Register Map / List | Addresses, bit fields, reset values |
| High | Address Map | Base addresses, memory map |
| Medium | Pin Description / GPIO | Pin functions, function select |
| Medium | Electrical Characteristics | Voltage/current constraints |
| Medium | Clock / Timing | Timing formulas, divider rules |
| Low | Reset Controller | Reset release sequence |
| Lowest | Legal / Ordering / Revision | Usually not needed |

### DOCX / XLSX

1. Run `scripts/search.py` first to find candidate paragraphs/rows.
2. Run `scripts/read.py` for targeted reading.
3. Use `scripts/read.py --structured` when layout/table structure is critical.
4. If no hits, expand keywords and retry search before full reading.

## Quick Commands

Use `--structured` only when table/header fidelity is required.

```bash
SKILL_DIR="skills/datasheet-intelligence"

# 1) Find candidate pages first
uv run --project "$SKILL_DIR" "$SKILL_DIR/scripts/search.py" docs/rp2040.pdf "IC_CON" "I2C0_BASE" --unique-pages

# 2) Read only selected ranges
uv run --project "$SKILL_DIR" "$SKILL_DIR/scripts/read.py" docs/rp2040.pdf --pages 464-470

# 3) Switch to structured mode only if layout fidelity is critical
uv run --project "$SKILL_DIR" --with docling "$SKILL_DIR/scripts/read.py" docs/rp2040.pdf --pages 464-470 --structured
```

For full flags and format-specific examples, read `references/usage.md`.

## Operational Rules

1. Start with TOC for PDF workflows.
2. If bookmarks are missing, switch to search-first flow and avoid full structured TOC for very large PDFs.
3. Keep explicit project context in every command (`uv run --project ...`).
4. Read enough neighboring context to avoid missing table headers/footnotes.
5. Cross-check register values against Address Map / Register List sections.

## Output Contract

1. MUST provide evidence for each critical claim (address, bit position, reset value, formula): `source file + page/section`.
2. MUST map important code settings to evidence locations.
3. MUST mark unverifiable values as unverified.
4. MUST report table/prose conflicts and separate uncertain items.

## Resources

| Script | Role | Formats | `--structured` |
| --- | --- | --- | --- |
| `scripts/toc.py` | TOC extraction | PDF, DOCX | Yes |
| `scripts/read.py` | Targeted reading | PDF, DOCX, XLSX | Yes |
| `scripts/search.py` | Keyword search | PDF, DOCX, XLSX | Yes |

See [usage.md](references/usage.md) for detailed examples.
