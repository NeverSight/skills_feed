---
name: docs-sync
description: >
  Synchronizes documentation (README.md, CHANGELOG.md, API docs) with implementation.
  Preserves user content outside speckit markers. Updates are non-destructive and
  clearly delineated. Always run after /speckit.implement completes.
version: 0.0.1
license: MIT
compatibility: Requires spec kit artifacts
metadata:
  author: drillan
  category: automation
  repository: https://github.com/drillan/speckit-gates
---

# docs-sync

Synchronizes documentation with implementation after `/speckit.implement` completes.

## Purpose

This skill automatically updates documentation to reflect the implemented features. It:

- **Updates README.md**: Adds/updates usage section with implementation details
- **Updates CHANGELOG.md**: Adds entries for new features and changes
- **Updates API docs**: Synchronizes API documentation with contracts
- **Preserves user content**: Content outside speckit markers is never modified

## Marker System

docs-sync uses HTML comment markers to delineate auto-generated sections:

```markdown
<!-- speckit:start:section-name -->
Auto-generated content here
<!-- speckit:end:section-name -->
```

Content outside these markers is preserved exactly as-is.

## Output

The skill outputs a **DocsSyncResult** showing:

- Files created, updated, or unchanged
- Sections modified within each file
- Diff summary (lines added/removed/changed)
- Any errors encountered

## Usage

This skill runs automatically after `/speckit.implement`. You can also run it manually:

```bash
npx skills run docs-sync
```

## Exit Codes

| Code | Status | Meaning |
|------|--------|---------|
| 0 | Success | All updates successful |
| 1 | Partial | Some updates failed |
| 3 | Error | Required files missing |

## Sections Updated

### README.md

| Section | Marker | Content Source |
|---------|--------|----------------|
| Usage | `<!-- speckit:start:usage -->` | spec.md user stories |
| Installation | `<!-- speckit:start:installation -->` | plan.md dependencies |
| Features | `<!-- speckit:start:features -->` | spec.md functional requirements |

### CHANGELOG.md

| Section | Marker | Content Source |
|---------|--------|----------------|
| Unreleased | `<!-- speckit:start:unreleased -->` | tasks.md completed tasks |

## Preservation Rules

1. Content before the first marker is always preserved
2. Content after the last marker is always preserved
3. Content between different marker pairs is always preserved
4. Only content within matching marker pairs is updated
5. If no markers exist, content is appended with new markers

## Error Handling

- **Missing markers**: Creates new markers and adds content
- **Malformed markers**: Reports error, skips that section
- **File permissions**: Reports error, continues with other files
- **Missing source files**: Reports which sources are unavailable
