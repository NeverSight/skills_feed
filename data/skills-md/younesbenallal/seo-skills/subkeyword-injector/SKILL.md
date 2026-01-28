---
name: subkeyword-injector
description: For a given URL, pull Search Console queries it already ranks for and propose (or apply) content edits to capture more long-tail traffic.
---

# Subkeyword injector (GSC-driven refresh)

You update an existing piece of content to better capture the long-tail queries it already ranks for.

## Inputs to collect

- Page URL
- Editing access:
  - local file path (if the user has the content in the repo), OR
  - “no local access” (you’ll provide a patch plan)
- Constraints: “don’t change meaning”, “keep tone”, “keep sections”, etc.

## Page content access (for planning edits)

Use a Browser MCP if available. If not, use the `agent-browser` CLI (install if needed).

Agent-browser commands to capture current headings/sections:
```bash
agent-browser open <url>
agent-browser snapshot --json > /tmp/page.json
jq -r '.. | objects | select(.role=="heading") | (.name // "")' /tmp/page.json
```

If extraction is blocked or incomplete, ask the user to paste the current article content.

## Required tool

This skill requires **Google Search Console data**.

Use a **GSC MCP** (required) so you can query by page/URL and date range.

If no GSC MCP is available:
- stop and ask the user to install one, OR
- ask them for a manual export (CSV) and proceed with the export.

## Workflow

### 1) Pull queries for this page

Collect page-level queries and metrics:
- impressions, clicks, CTR, avg position
- date range: default 28 days (ask if they want 3 months / 12 months)

### 2) Select subkeywords (no fluff)

Prioritize queries that are:
- **Position 6–25** with meaningful impressions (easy uplift)
- **High impressions + low CTR** (snippet/title mismatch)
- **Query variants** (plural/singular, “best”, “examples”, “template”, “pricing”, “vs”)

Avoid:
- unrelated queries (accidental rankings)
- adding 30 synonyms (keyword stuffing)

### 3) Decide insertion strategy per query cluster

Pick one per cluster:
- Add/rename an H2/H3
- Add a short paragraph in an existing section
- Add a mini-FAQ block
- Add a comparison subsection (“X vs Y”)
- Add a definition snippet (AEO/GEO friendly)

Use the readability rules from `obsidian/Article writing playbook.md`.

### 4) Produce edits

If you have local file access:
- apply edits directly (minimal diff, no refactors)

If you do NOT have access:
- output a “patch plan” with:
  - exact headings to add
  - copy blocks to paste
  - where to place them (anchors)

### 5) Output

- A table of chosen subkeywords + where they were integrated
- Updated title/H1/meta suggestions (only if CTR issue)
