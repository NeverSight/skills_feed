---
name: dbs-report
description: Generate a DBS Group Research US Equity Research report in HTML format. Use this skill when the user asks to create, generate, or produce a DBS-style equity research report for a company. The skill produces a pixel-perfect reproduction of the DBS report format including cover page, financial tables, ratings history, and disclaimer pages.
argument-hint: <company-name>
user-invocable: true
---

# DBS Group Research -- US Equity Research Report Generator

You are generating a **DBS Group Research US Equity Research report** in HTML format. The output must be a single self-contained HTML file that, when opened in a browser and printed to PDF, is visually indistinguishable from the original DBS reports.

The user will provide a company name (and optionally a ticker). You must gather the required financial data using available tools (financial datasets MCP, web search, etc.) and produce the full report.

For the complete formatting specification, see [report-spec.md](report-spec.md).
For the HTML/CSS template, see [template.html](template.html).

---

## REPORT GENERATION WORKFLOW

### Step 1: Gather Data

Use available tools to collect:

1. **Company facts**: Sector, market cap, share price, volume, free float, dividend yield, Bloomberg ticker
2. **Financial statements**: 3 years of actuals + 2 years of consensus estimates for income statement, balance sheet, cash flow
3. **Valuation metrics**: P/E, P/B, EV/EBITDA, dividend yield, FCF yield
4. **Credit metrics**: Debt/Equity, Net Debt/Equity, Debt/Assets, EBITDA/Interest, Debt/EBITDA, receivable days, payable days, inventory days
5. **Stock price history**: ~4 years of monthly prices for the indexed performance chart
6. **S&P 500 history**: Same period for the benchmark comparison
7. **Recent news and filings**: For writing the investment overview narrative

### Step 2: Write Narrative Content

Generate the following sections using the voice and style rules from the spec:

1. **Company Overview** (1 paragraph, ~100-150 words): Factual description of what the company does, key products/segments with revenue percentage breakdowns.
2. **Investment Overview** (2-4 paragraphs, each starting with a **bold lead-in sentence**):
   - Each paragraph covers one investment thesis point
   - The final paragraph is always the rating/valuation call
   - Use specific data points, percentages, and figures inline
3. **Risks** (1-2 short paragraphs, bold lead-in sentence): Key downside risks

### Step 3: Determine Rating and Target Price

Based on the analysis:
- Apply the DBS Absolute Total Return rating system:
  - **STRONG BUY**: >20% total return over 3 months
  - **BUY**: >15% (small caps) / >10% (large caps) over 12 months
  - **HOLD**: -10% to +15% (small caps) / -10% to +10% (large caps) over 12 months
  - **FULLY VALUED**: negative total return >-10% over 12 months
  - **SELL**: negative total return >-20% over 3 months
- State the valuation methodology (e.g., "based on Xx forward PE, +Y SD above peers' average")

### Step 4: Build the HTML Report

Use the template from [template.html](template.html) and populate all sections. The HTML must be self-contained with inline CSS and embedded SVG charts.

---

## CRITICAL FORMATTING RULES

These rules must be followed exactly. Deviations will make the report look non-authentic.

### Font & Typography

- **Font family**: Sans-serif throughout: `Calibri, 'Segoe UI', Arial, Helvetica, sans-serif` -- this applies to body text, tables, headers, everything. Do NOT use serif fonts (Georgia, Times, etc.)
- **Banner**: `US EQUITY RESEARCH` banner must span **100% full page width**, not just the left column
- **Lead-in sentences**: Must be both **bold AND underlined** (`font-weight: bold; text-decoration: underline;`)
- **Rating names** in the rating definitions box: Must be **bold AND underlined**
- **Source attributions** below financial tables: Regular weight, NOT italic
- **DBS logo star**: Use ❖ (`&#10070;`), not ✶ (`&#10038;`)
- **SVG chart text**: Must also use the same sans-serif font family

### Writing Style

- **Justified text alignment** for all body paragraphs
- **Bold + underlined lead-in sentences**: Every paragraph in Investment Overview and Risks starts with a **bold and underlined** first sentence (`.lead-in { font-weight: bold; text-decoration: underline; }`), ending with a period, then continues in regular weight with no underline
- Currency: Always "USD" prefix (e.g., "USD210", "USD1.2 trillion"), never "$" in body text ($ is acceptable in tables)
- Percentages: Use `%` symbol inline (e.g., "17% y/y", "51% of FY24 revenue")
- Year-over-year: Write as "y/y"
- Fiscal year: Format as "FY24", "FY9/25F", "FY2025F" -- "F" suffix for forecasts
- Tone: Institutional, analytical, third-person. No first-person ("I/we think"), instead use "We expect", "We believe", "We are [RATING] on [TICKER]"
- No bullet points in body text -- everything in paragraph form
- Company name used in full on first reference, then ticker or shortened name thereafter

### Page Layout

- **Page 1**: Two-column (60% left narrative / 40% right data sidebar)
- **Page 2**: Full-width financial tables (3 tables stacked)
- **Page 3**: Target Price & Ratings History chart + Rating definitions box + start of disclaimer
- **Pages 4-7**: Boilerplate legal disclaimer (use the standard text from the spec)

### Numbers in Tables

- Right-aligned
- Comma-separated thousands (e.g., "394,328")
- Negative values in parentheses: `(2.8)`, `(10.6)` for percentage rows
- y/y percentage sub-rows: italicized, indented
- Missing data: show as "-"
- Not meaningful: show as "nm"

### Every Page Must Have

1. "DBS Group Research" -- top-right corner, small font
2. 3-line disclaimer footer at bottom
3. DBS logo (red diamond ❖ `&#10070;` + "DBS" text) -- bottom-right corner

---

## OUTPUT FORMAT

Produce a single HTML file named `{CompanyName}_DBS_Report.html`. The file must:

1. Be completely self-contained (inline CSS, embedded SVG charts, no external dependencies)
2. Use `@media print` CSS for proper PDF generation
3. Use `@page` rules for A4 sizing and margins
4. Render charts as inline SVG elements
5. Include page breaks at the correct locations

When generating charts as SVGs:

**Indexed Performance Chart (Page 1):**
- Two-line chart: Company (orange/gold `#D4A843`) vs S&P 500 (dark gray `#333`)
- Both indexed to 100 at the start date
- ~4 year window
- X-axis labels: "Mon-YY" format at ~6-month intervals
- Y-axis: indexed values
- Horizontal gridlines only, light gray
- Legend at top: horizontal, with colored line samples

**Target Price & Ratings History Chart (Page 3):**
- Dual series: share price (red line `#CC3333`) and target price (black step-line)
- Numbered circle markers at each report date
- ~12-month window
- Y-axis: Stock Price (USD)

$ARGUMENTS
