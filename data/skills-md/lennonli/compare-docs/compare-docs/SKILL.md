---
name: compare-docs
description: Compares two documents (docx, md, txt, pdf) to identify substantive differences, focusing on financial data, key clauses, and statistical discrepancies. Generates a formatted comparison report. Use when the user asks to "compare documents", "check differences between files", "find discrepancies", "比对文档", "查看差异", "比较实质性差异", or "核对合同".
---

# Document Comparison Skill

This skill compares two documents to find substantive differences, errors, or inconsistencies. It is particularly useful for legal contracts, financial reports, or revised document versions.

## Usage

```bash
# Compare two specific files
/compare-docs file1.docx file2.docx

# Compare with specific focus
/compare-docs file1.docx file2.docx --focus "financial data"
```

## Workflow

1.  **Input Verification:**
    *   Verify both input files exist.
    *   Determine file type (.docx, .pdf, .md, .txt).

2.  **Content Extraction:**
    *   If files are `.docx`, use `pandoc` to convert them to Markdown for clear text analysis.
        ```bash
        pandoc -t markdown "file1.docx" -o "file1.md"
        pandoc -t markdown "file2.docx" -o "file2.md"
        ```
    *   If files are `.pdf`, use available PDF reading tools.

3.  **Analysis & Comparison:**
    *   Read the extracted content.
    *   Compare the documents section by section or key-value by key-value.
    *   **Focus Areas:**
        *   **Numbers & Dates:** Check for discrepancies in financial figures, dates, percentages, and quantities.
        *   **Key Clauses:** Identify added, removed, or modified clauses (especially in legal/contractual contexts).
        *   **Definitions:** Check for changes in defined terms.
    *   *Note:* Ignore minor formatting changes unless explicitly requested.

4.  **Report Generation:**
    *   Create a Markdown report (`comparison_report.md`) structured as follows:
        *   **Summary:** Brief overview of the comparison result.
        *   **Critical Differences (High Risk):** Data mismatches, missing clauses, conflicting obligations.
        *   **Substantive Changes:** Changes in meaning or scope.
        *   **Stylistic/Format Changes:** (Optional) Brief mention of layout or phrasing changes that don't alter meaning.
        *   **Recommendations:** Actionable advice based on findings.

5.  **Output formatting & Delivery:**
    *   Convert the Markdown report to a professional `.docx` document using `pandoc`.
        ```bash
        pandoc "comparison_report.md" -o "Comparison_Report.docx"
        ```
    *   **Open the file:** Automatically open the generated document so the user can view it immediately.
        *   On macOS: `open "Comparison_Report.docx"`
        *   On Windows: `start "Comparison_Report.docx"`
        *   On Linux: `xdg-open "Comparison_Report.docx"`
    *   Inform the user of the report location.

6.  **Cleanup:**
    *   Remove temporary intermediate files (e.g., converted .md files) to keep the workspace clean.

## Example Output Structure

# Comparison Report

## 1. Executive Summary
...

## 2. Key Discrepancies
| Item | File A Value | File B Value | Impact |
|------|--------------|--------------|--------|
| Revenue | $10M | $12M | Significant |
| ... | ... | ... | ... |

## 3. Detailed Clause Analysis
...
