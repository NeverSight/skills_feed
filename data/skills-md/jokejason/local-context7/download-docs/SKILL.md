---
name: download-docs
description: Download documentation from GitHub repos or URLs. Supports manifest-based batch downloads with configurable exclude patterns.
user-invocable: false
---

# Download Docs

Download documentation files from various sources using manifest configurations.

## Quick Start

Download from a specific manifest:
```bash
.claude/skills/download-docs/scripts/download.sh {manifest-name}
```

Download from all manifests:
```bash
.claude/skills/download-docs/scripts/download.sh
```

Output location: `output/{manifest-name}/`

## Manifest Format

Manifests are JSON files in `scripts/manifests/`. Use `$schema` for IDE validation. Two source types are supported:

### GitHub Source (for large doc sets)

Clones repository and extracts markdown files:

```json
{
  "$schema": "./manifest.schema.json",
  "_source": {
    "type": "github",
    "repo": "owner/repo-name",
    "branch": "main",
    "path": "docs",
    "extensions": [".md", ".mdx"],
    "exclude": ["**/internal/**"],
    "noDefaultExcludes": false
  }
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `repo` | Yes | GitHub repository (owner/name) |
| `branch` | No | Branch to clone (default: "main") |
| `path` | No | Directory path within repo (default: ".") |
| `extensions` | No | File extensions to include (default: [".md", ".mdx"]) |
| `exclude` | No | Additional glob patterns to exclude |
| `noDefaultExcludes` | No | Set true to disable default excludes |

**Default exclude patterns:**
- CHANGELOG*, CONTRIBUTING*, LICENSE*, SECURITY*, CODE_OF_CONDUCT*
- .github/**, **/test/**, **/tests/**, **/__tests__/**
- **/spec/**, **/fixtures/**, **/examples/**, **/node_modules/**

### URL Source (for individual files)

Downloads specific files from URLs:

```json
{
  "$schema": "./manifest.schema.json",
  "_source": { "type": "url" },
  "files": {
    "category-name": {
      "doc-name": "https://example.com/path/to/doc.md"
    }
  }
}
```

### URL Source with HTML Conversion

Downloads HTML and converts to markdown (requires pandoc):

```json
{
  "$schema": "./manifest.schema.json",
  "_source": {
    "type": "url",
    "convert": "html"
  },
  "files": {
    "category-name": {
      "doc-name": "https://example.com/docs/page.html"
    }
  }
}
```

> **Note:** HTML conversion only works for static HTML. SPA sites (React, Angular, etc.) will produce empty output.

### Disabling a Manifest

Add `_disabled` to skip processing:

```json
{
  "$schema": "./manifest.schema.json",
  "_source": {
    "type": "url",
    "_disabled": true,
    "_reason": "SPA site - requires Playwright handler"
  },
  "files": { ... }
}
```

## Requirements

- `jq` - JSON parsing
- `git` - GitHub source cloning
- `curl` - URL downloads
- `pandoc` - HTML conversion (optional)

## Adding New Manifests

Create a JSON file in `scripts/manifests/` following the format above. The manifest filename (without .json) becomes the output directory name.
