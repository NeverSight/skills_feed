---
name: documentation-structure
description: Documentation architecture for this repository. Use when creating, updating, or reviewing README.md, CONTRIBUTING.md, or docs/ files. Covers separation of concerns, vendor documentation standards, cross-references, and validation.
---

# Documentation Structure

This skill defines how documentation is organized and maintained in this repository.

## Core Principles

| Principle | Description |
|-----------|-------------|
| **Separation of Concerns** | README (landing), docs/ (reference), CONTRIBUTING (dev workflow) |
| **Single Source of Truth** | Define once, link everywhere. Never duplicate content. |
| **Hub-and-Spoke** | `docs/README.md` is the central navigation hub |
| **Vendor Isolation** | Each AI platform gets its own directory in docs/ |

## Document Responsibilities

### README.md (Landing Page)

**Purpose:** First impression. Get users started quickly.

**Must include:**
- One-line description
- Quick Start (4 steps: Choose → Install → Authenticate → Try)
- Capability tables (what users can do)
- Links to docs/ for details

**Must NOT include:**
- Full API reference (→ docs/mcp/)
- Development workflows (→ CONTRIBUTING.md)
- Detailed architecture (→ docs/)

### docs/ (Reference Documentation)

**Purpose:** Complete reference for users and developers.

**Structure:**
```
docs/
├── README.md              # Navigation hub
├── troubleshooting.md     # Cross-platform issues
├── getting-started/       # Entry points
│   ├── mcp-setup.md       # Generic MCP config
│   └── enterprise.md      # Admin requirements
├── claude-code/           # Vendor: Claude Code
├── kiro/                  # Vendor: Kiro
├── gemini-cli/            # Vendor: Gemini CLI
└── mcp/                   # Protocol reference
    ├── tools-reference.md
    └── tutorials.md
```

### CONTRIBUTING.md (Development Workflow)

**Purpose:** How to modify THIS repository.

**Must include:**
- Clone and local dev setup
- How to test changes locally (`--plugin-dir`, etc.)
- Validation checklists
- PR process

**Must NOT include:**
- Full plugin/power architecture (→ docs/)
- User-facing tutorials (→ docs/)

## Vendor Documentation Standards

Each vendor directory in `docs/` follows this pattern:

### Required Files

| File | Purpose |
|------|---------|
| `overview.md` | What is this integration, why use it, installation |
| `*-development.md` | How to build new plugins/powers/extensions |
| Individual component docs | One file per plugin/power |

### Standard Sections in overview.md

```markdown
## What are [Plugins/Powers/Extensions]?
## Why Use [Plugins/Powers] vs Direct MCP?
## Available [Plugins/Powers]
## Installation
## Authentication
## Related
```

### Vendor-Specific Metadata

| Vendor | Config Format | Location |
|--------|--------------|----------|
| Claude Code | `plugin.json` | `.claude-plugin/plugin.json` |
| Kiro | POWER.md frontmatter | `POWER.md` |
| Gemini CLI | JSON extension | `gemini-extension.json` |

## Cross-Reference Patterns

### Link Format

- **Within docs/**: Use relative paths `[text](../mcp/tools-reference.md)`
- **From README to docs/**: Use `docs/` prefix `[text](docs/claude-code/overview.md)`
- **External links**: Full URLs `[text](https://developers.miro.com)`

### Required "Related" Section

Every doc file should end with a Related section:

```markdown
## Related

- [Overview](overview.md) - Introduction to this integration
- [Tools Reference](../mcp/tools-reference.md) - MCP tool documentation
```

### Reciprocal Links

If doc A links to doc B, doc B should link back to doc A in its Related section.

## Validation Guidelines

Before committing documentation changes:

### Content Checks
- [ ] No duplicated content (link instead)
- [ ] Correct document owns the content (README vs docs/ vs CONTRIBUTING)
- [ ] All sections present per vendor standards

### Link Checks
- [ ] All internal links resolve
- [ ] Related sections have reciprocal links
- [ ] External links use HTTPS

### Format Checks
- [ ] Code blocks have language specified
- [ ] Tables have consistent formatting
- [ ] Collapsibles have matching tags

## See Also

- `references/patterns.md` - Formatting patterns (tables, collapsibles, code blocks)
