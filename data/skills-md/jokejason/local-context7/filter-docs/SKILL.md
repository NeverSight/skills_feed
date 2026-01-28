---
name: filter-docs
description: AI-assisted filtering to identify and remove non-useful documentation files. Generates review manifests and applies deletion lists.
user-invocable: false
---

# Filter Docs

AI-assisted documentation filtering to keep only files useful for developers.

## Quick Start

Generate review file for a manifest:
```bash
.claude/skills/filter-docs/scripts/filter-docs.sh {manifest-name}
```

Apply deletions (after creating `._delete.txt`):
```bash
.claude/skills/filter-docs/scripts/filter-docs.sh {manifest-name}
```

## Workflow

### Step 1: Generate Review

Run the filter script to create `output/{manifest}/._review.json` containing:
- File paths and names
- File sizes and line counts
- First 10 lines as preview

### Step 2: AI Evaluation

Read the review JSON and evaluate each file against these criteria:

**KEEP** - Files that help developers USE the library:
- API reference documentation
- Usage guides and tutorials
- Configuration and setup docs
- Code examples and patterns
- Integration guides
- Troubleshooting guides

**DELETE** - Files NOT useful for using the library:
- Internal development docs
- Contribution guidelines (CONTRIBUTING.md)
- Release notes and changelogs
- Meeting notes, RFCs, proposals
- Marketing and landing pages
- Duplicate or stub files
- Auto-generated index files with no content
- License files (already excluded by default)

### Step 3: Create Delete List

Write paths of files to delete to `output/{manifest}/._delete.txt`:
- One relative path per line (relative to output/{manifest}/)
- Lines starting with `#` are ignored as comments

Example:
```
# Internal docs
internal/architecture.md
internal/roadmap.md
# Marketing
landing-page.md
```

### Step 4: Apply Deletions

Run the filter script again. It will:
1. Delete all files listed in `._delete.txt`
2. Remove empty directories
3. Delete the `._delete.txt` file

## Output Files

| File | Purpose |
|------|---------|
| `._review.json` | File metadata and previews for AI review |
| `._delete.txt` | List of files to delete (you create this) |
