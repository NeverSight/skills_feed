---
name: us-stock-researcher
description: US Stock Investment Research Assistant. Supports Gemini Deep Research or Claude Native Deep Research (7-Phase + GoT). Use when analyzing 10-K/10-Q reports or generating investment research reports.
allowed-tools: Read, Write, WebSearch, Bash(python3.11:*)
---

# US Stock Researcher

Institutional-grade deep analysis of US stock SEC filings, outputting professional investment reports.

## Research Mode Selection

| Mode | When to Use | Requirements |
|------|-------------|--------------|
| **Gemini Mode** | Default when GEMINI_API_KEY is configured | GEMINI_API_KEY environment variable |
| **Claude Native Mode** | When no Gemini API or user requests | WebSearch tool access |

---

## Quick Start Workflow

### Step 1: Determine Filing Period

**If user did NOT specify a period**, use WebSearch to find the latest filing:
```
WebSearch: "{company_name} latest 10-K 10-Q SEC filing"
```

**IMPORTANT: Always analyze the MOST RECENT filing by date, regardless of type (10-K or 10-Q).**

Example decision logic:
- If latest 10-K is 2024-12-31 and latest 10-Q is 2025-09-30 → Use 10-Q (more recent)
- If latest 10-K is 2025-01-15 and latest 10-Q is 2024-09-30 → Use 10-K (more recent)

Inform user: "根据搜索，{TICKER} 最新的财报是 {10-K/10-Q}（截至 {period}），将分析该期财报"

### Step 2: Download Filing

```bash
python3.11 scripts/download_sec_filings.py --ticker <TICKER> --type <10-K|10-Q|6-K> --limit 1
```

Output: `<project_root>/investment-research/{TICKER}/tmp/sec_filings/cleaned.txt`

### Step 3: Dynamic Framework Generation

1. Read first 5000 characters of filing
2. Identify company industry
3. Select modules from `industry-analysis-modules.md`
4. Merge with `financial-analysis-framework.md`
5. Save to `tmp/analysis-framework-YYYY-MM-DD.md`

### Step 4: Execute Deep Research

**Gemini Mode:**
```bash
python3.11 scripts/gemini_deep_research.py \
  --input <cleaned.txt path> \
  --prompt <analysis framework path> \
  --output-dir <project_root>/investment-research/<TICKER> \
  --ticker <TICKER> \
  --company <Company Name> \
  --phase all
```

**Claude Native Mode:**
Follow `prompts/claude-deep-research-protocol.md` for complete 7-phase execution.

### Step 5: Format and Save

Format per `markdown-formatter-rules.md`, save to `investment-research/{TICKER}/`

---

## Mode 1: Gemini Deep Research

```
User Input → Download Filing → Framework Generation → Phase 1 Filing Analysis → Phase 2 Web Research → Integration → Final Report
                                                              ↓                         ↓
                                                      (Gemini Deep Research)    (Gemini Deep Research)
```

- **Phase 1**: Upload filing via Files API, Gemini analyzes comprehensively
- **Phase 2**: Web search for competitors, trends, management verification
- **Integration**: Claude merges Phase 1 + Phase 2 per `prompts/report-merge-prompt.md`

---

## Mode 2: Claude Native Deep Research

Uses **7-Phase Deep Research + Graph of Thoughts (GoT)** methodology.

**For complete execution details, see:** `prompts/claude-deep-research-protocol.md`

### 7-Phase Overview

| Phase | Name | Description |
|-------|------|-------------|
| 1 | Question Scoping | Define goals, download filing |
| 2 | Retrieval Planning | Identify industry, create research plan |
| 3 | Iterative Querying | GoT branches: Financial, Competitive, Industry, Management, Risk |
| 4 | Source Triangulation | Cross-validate findings |
| 5 | Knowledge Synthesis | Structure report per framework |
| 6 | Quality Assurance | Chain-of-Verification |
| 7 | Output Packaging | Format and save |

### GoT Research Branches

| Branch | Method | Focus |
|--------|--------|-------|
| A | Read filing | Financial data analysis |
| B | WebSearch | Competitive landscape |
| C | WebSearch | Industry trends |
| D | WebSearch | Management verification |
| E | WebSearch | Risk factors |

---

## Reference Documents

| Document | Purpose |
|----------|---------|
| [financial-analysis-framework.md](financial-analysis-framework.md) | Base analysis framework |
| [industry-analysis-modules.md](industry-analysis-modules.md) | Industry-specific modules |
| [markdown-formatter-rules.md](markdown-formatter-rules.md) | Report formatting rules |
| [prompts/claude-deep-research-protocol.md](prompts/claude-deep-research-protocol.md) | Claude Native 7-phase guide |
| [prompts/report-merge-prompt.md](prompts/report-merge-prompt.md) | Gemini mode report integration |

---

## Output Location

```
<project_root>/investment-research/{TICKER}/
├── tmp/
│   ├── sec_filings/cleaned.txt
│   ├── analysis-framework-YYYY-MM-DD.md
│   ├── phase1-YYYY-MM-DD.md
│   └── phase2-YYYY-MM-DD.md
└── {TICKER}-Investment-Report-YYYY-MM-DD.md
```

---

## Usage Examples

- "Analyze AAPL's latest 10-K annual report"
- "Deep research MSFT's 10-K filing"
- "Analyze JPM's latest annual report" (auto-selects Financial module)
- "Research PFE's financial report" (auto-selects Pharma module)
