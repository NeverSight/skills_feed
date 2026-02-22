---
name: get-commits
description: Extract and parse local git commit history into structured JSON format with custom tags ([Why], [What], [Impact]). Use when generating changelogs, creating PR summaries, updating CHANGELOG.md files, or analyzing recent code changes. Parses conventional commits, extracts technical details and business impact, and returns flat JSON to save context tokens and reduce hallucinations during documentation generation.
license: MIT
metadata:
  author: aroldolanderos
  version: "1.0.0"
---

# Git Changelog Parser

Parse local git commit history into clean, structured JSON.
Extracts conventional commit metadata, custom tags
([Why], [What], [Impact]), and returns a token-efficient flat
structure ready for documentation workflows.

## Quick Start

```bash
python3 scripts/get_commits.py 20
```

Returns JSON with last 20 commits:

```json
[
  {
    "hash": "abc1234",
    "date": "2026-02-09",
    "type": "feat",
    "scope": "auth",
    "title": "Add JWT authentication",
    "what": "Implemented JWT tokens with refresh mechanism",
    "impact": "Breaking change: auth endpoints require tokens"
  }
]
```

### Use in your workflow

1. **Changelog**: Run script, extract [What] fields, format as
   Markdown
2. **PR Summary**: Run script, extract [Impact] fields, create
   executive summary
3. **Change Analysis**: Run script, filter by type/scope,
   generate reports

## Commit Message Format

The script expects commits following this structure:

```
feat(scope): Brief description

[Why] Reason for this change
[What] Technical implementation details
[Impact] Business impact or breaking changes
```

- First line: `type(scope): title` or `type: title`
- Tags on separate lines: `[Why]: ...`, `[What]: ...`,
  `[Impact]: ...`
- All tags are optional; missing tags return empty strings
- Merge commits are filtered out automatically

## Script Parameters

```bash
python3 scripts/get_commits.py [limit]
```

- `limit` (optional): Number of commits to retrieve
  (default: 50)

## JSON Output Structure

Flat, token-efficient structure (no nesting):

| Field   | Description                                  |
|---------|----------------------------------------------|
| `hash`  | Short commit hash (7 chars)                  |
| `date`  | ISO date formatted as YYYY-MM-DD             |
| `type`  | Conventional commit type (feat, fix, etc.)   |
| `scope` | Component/area affected (empty if missing)   |
| `title` | Description with type/scope prefix removed   |
| `what`  | Technical details from [What] tag            |
| `impact`| Business impact from [Impact] tag            |
