---
name: stock-qualitative-analysis
description: Create comprehensive and deeply analyzed buy-side style qualitative stock analysis reports from filings and public sources with strict citations, chapter-by-chapter workflow, and placeholders for missing evidence. Emphasizes active extraction and detailed analysis of SEC information. Use for Chinese qualitative analysis of listed companies.
compatibility: Requires Python 3. Network access needed for SEC EDGAR fetches.
metadata:
  author: sysyphus
  version: "0.1"
---

# Stock Qualitative Analysis Skill

## When to use
Use this skill when a user asks for a qualitative stock analysis report (定性分析) that must be evidence-based and formatted as a structured report. This skill emphasizes strict citations and non-hallucination behavior.

## Inputs
- Company name (required)
- Ticker / exchange (optional but recommended)
- Market context (US / HK / CN / other)
- Time window (e.g., FY2015–FY2024; latest quarterly)
- Language preference (Chinese default; English if requested)
- Sources:
  - User-provided filings (PDF or HTML)
  - SEC EDGAR fetch (optional, if allowed)
  - Other public sources (only if cited)

## Outputs
- A Markdown report following the template structure in `assets/report-template.md`
- Each section contains: `结论要点 / 详细情况 / 证据与出处` (or English equivalents when English output is requested)
- Final `来源清单` with SEC filings and other sources in reverse-chronological order

## Core rules (non-negotiable)
- Do not state facts without a source.
- Any factual claim MUST include a source string; otherwise use a placeholder in `【...】` describing what is needed.
- **Actively analyze sources**: Go beyond surface-level summaries. Extract specific details, quantitative data, and contextual insights relevant to each section of the report template.
- **Comprehensive filling**: Make the best effort to fill all sections of the report template. If information is truly missing from the provided sources, use a specific placeholder indicating what is missing.
- If real-time data is required, explicitly state that the user must verify freshness.
- No investment advice, price targets, or trading recommendations.
- Default output language: Chinese. If the user query is in English, respond in English.

## Execution
- Intake: confirm company name, ticker/exchange, market, time window, and allowed data sources.
- Pre-check local data: before any remote fetching, verify whether local filings are sufficient; only fetch remotely if local data is insufficient.
- Acquire sources: use `scripts/build_source_manifest.py` to pull SEC filings and ingest local PDFs.
- Extract key 10-K sections (HTML): use `scripts/extract_sec_html_sections.py` to produce per-item text files (e.g., Item 1/1A/7/8) before analysis.
- Section-by-section generation (Agent-driven): for each section in `assets/report-template.md`, the Agent expands the section in sequence, producing `结论要点 / 详细情况 / 证据与出处` based on the available sources and citing evidence.
- Progressive write-back: before starting summaries, determine whether a local report file exists; after completing each section, write the content into that file.
- Finalization: rewrite `投资要点概览` after all sections are complete, then update `来源清单`.

## Usage
- The Agent executes the section loop at runtime based on the template headings.
- The Agent MUST attempt to fill every section using provided sources and mark missing facts with explicit placeholders.
- If the user asks for English output, the Agent translates the template headings and section labels consistently (e.g., Conclusion / Details / Evidence) while preserving the report structure.

## Data acquisition
- SEC EDGAR fetch: `scripts/fetch_sec_edgar.py`
- Local PDF ingestion: `scripts/ingest_local_pdfs.py`
- Source manifest: `scripts/build_source_manifest.py`
- HTML section extractor: `scripts/extract_sec_html_sections.py`

## Citation format
- SEC filings: `Form 10-K/10-Q/20-F/6-K + 年度/日期 + 章节/标题`
- Web sources: `机构/网站 + 发布日期 + 标题`

## Examples
### Example request
“参考 SEC filings，帮我做 AAPL 的定性分析，按模板输出。”

### Example output shape
Use `assets/report-template.md` and fill each section with facts + citations. Unknowns become placeholders.

## References
- Guardrails and writing style: `references/prompt-guardrails.md`
- Report template: `assets/report-template.md`
- Validation checklist: `references/validation-checklist.md`
- Goldenset examples: `references/goldenset.md`
