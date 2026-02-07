---
name: report
description: Create Investigation/Analysis Report. This skill should be used when summarizing investigation or analysis work into a structured GitHub Flavored Markdown report. Use it after completing research, debugging, security audits, or other analytical tasks.
---

# Create Investigation/Analysis Report

## Overview

This skill creates a structured report summarizing investigation and analysis work in GitHub Flavored Markdown (GFM) format. It follows a consistent template that organizes findings, recommendations, and conclusions in a professional format.

## Workflow

### 1. Confirm Report Details (Claude Code only)

When running in Claude Code, use AskUserQuestion tool to confirm the following before creating the report:

**Report Type**:
- Question: "What type of report are you creating?"
- Header: "Type"
- Options:
  - "Investigation" - Error investigation, debugging session documentation
  - "Analysis" - Performance analysis, code analysis, data analysis
  - "Audit" - Security audit, compliance review
  - "Review" - Code review summary, architecture review
- The selected type will be used in the report metadata

**Save Location**:
- Question: "Where should the report be saved?"
- Header: "Location"
- Options:
  - "docs/reports/ (Recommended)" - Standard location for reports
  - "docs/" - General documentation directory
  - "Project root" - Save in the root directory

### 2. Determine File Location and Name

Based on the confirmed details, determine the file name and save location following these conventions:

**File name format:**
```
{topic}-{YYYY-MM-DD}-{HHmm}.md
```

**Save location priority:**
1. `docs/reports/` directory (recommended)
2. `docs/` directory
3. Project root

**Naming conventions:**
- Topic part should concisely represent the investigation/analysis content
  - Examples: `error-investigation`, `performance-analysis`, `security-audit`
- Date format: YYYY-MM-DD (e.g., 2025-11-13)
- Time format: HHmm in 24-hour notation (e.g., 1430)
- All lowercase, words separated by hyphens

**Examples:**
```
docs/reports/api-error-investigation-2025-11-13-1430.md
docs/reports/database-performance-analysis-2025-11-13-0915.md
docs/reports/security-vulnerability-audit-2025-11-13-1620.md
```

### 3. Verify and Create Directory

If the save destination directory does not exist, create it:
```bash
mkdir -p docs/reports
```

### 4. Create Report

Create the report following this standard structure:

**Required section structure:**
```markdown
# {Report Title}

**Created**: YYYY-MM-DD HH:mm
**Author**: Claude Code
**Type**: {Investigation/Analysis/Audit/Review}

## Summary

{Brief explanation of the report's purpose and investigation content}

## Background

{Why this investigation/analysis was performed}

## Investigation/Analysis Details

{Detailed content}

## Findings

{Important discoveries or issues}

## Recommendations

{Future actions, proposed fixes, etc.}

## Conclusion

{Summary}

## Additional Information

{Referenced files, related documents, etc.}
```

**Formatting requirements:**
- Write in GitHub Flavored Markdown format
- Add appropriate language specification to code blocks
- Use ```diff for diff displays
- Actively use tables
- Write file paths as links: `[filename.ts](path/to/filename.ts)`
- Use ## or ### to create section hierarchy

### 5. Save File and Confirm

1. Save the report with the determined file name
2. After saving, explicitly display the file path
3. Display report summary (number of sections, character count, etc.)

## Output Example

```
📝 Report created

Location: docs/reports/api-error-investigation-2025-11-13-1430.md
Size: 3,245 characters
Sections: 7
Created: 2025-11-13 14:30
```

## Use Cases

- Error investigation reports
- Performance analysis documentation
- Security audit findings
- Code review summaries
- Architecture decision records
- Debugging session documentation
