---
name: markdown-optimization
description: |
  Analyze and optimize markdown documents for size, structure, and maintainability.
  Use when: (1) markdown files are too large or verbose, (2) documentation needs
  restructuring, (3) checking docs for quality issues, (4) converting prose to tables.
tech_stack: [markdown, agnostic]
---

# Markdown Optimization

Patterns and techniques for analyzing and optimizing markdown documentation.

## Quick Start

### Size Check

```bash
# Check single file
wc -l docs/README.md

# Check all markdown in folder
find docs -name "*.md" -exec wc -l {} \; | sort -n

# Find files over 500 lines
find . -name "*.md" -exec sh -c \
  'lines=$(wc -l < "$1"); [ "$lines" -gt 500 ] && echo "$1: $lines"' _ {} \;
```

### Structure Validation

Check for common issues:
- Missing TOC (files > 100 lines)
- Heading hierarchy violations (h1 → h3, skipping h2)
- Sections over 200 lines

## Document Profiles

Different document types have different optimization rules.

> **Authoritative limits**: For Claude Code artifacts (`agent`, `skill`, `command`, `guidelines`), size limits are defined in [GUIDELINES.md](../../GUIDELINES.md#size-limits). This skill enforces those limits.

| Profile | Target | Key Focus |
|---------|--------|-----------|
| `claude-md` | Project context | Concise, table-heavy |
| `architecture` | System design | Diagrams external, decisions linked |
| `domain` | Business docs | Entity tables, numbered rules |
| `feature-spec` | Feature docs | Separated concerns |
| `readme` | Entry points | Quick start, links |
| `agent` | Agent prompts | Lean, reference skills |
| `skill` | Skill docs | Progressive disclosure |
| `command` | Slash commands | Focused action |
| `guidelines` | Meta-knowledge | Modular structure |

**Full profile definitions**: See [profiles.md](references/profiles.md)

## Core Analysis Patterns

### 1. Size Analysis

```markdown
## Size Metrics
| File | Lines | Limit | Status |
|------|-------|-------|--------|
| README.md | 180 | 200 | ✅ OK |
| business-rules.md | 620 | 400 | ❌ OVER (+220) |
```

**Actions for oversized files**:
- Split by topic/domain
- Extract examples to separate files
- Convert prose to tables
- Move detailed content to references

### 2. Duplication Detection

Look for:
- Identical paragraphs across files
- Same concepts explained differently
- Copy-pasted code blocks
- Repeated tables/lists

```markdown
## Duplication Findings
| Concept | Found In | Action |
|---------|----------|--------|
| "Entity base classes" | patterns.md:45, entities.md:12 | Consolidate to entities.md |
| "Build commands" | README.md:30, CLAUDE.md:15 | Single source in CLAUDE.md |
```

### 3. Structure Assessment

**Heading Hierarchy**:
```markdown
# Title (h1) - Only one per file
## Section (h2)
### Subsection (h3)
#### Detail (h4) - Use sparingly
```

**Issues to flag**:
- Multiple h1 headings
- Skipped levels (h1 → h3)
- Sections > 200 lines without subsections
- Missing TOC for files > 100 lines

### 4. Link Validation

```bash
# Find all markdown links
grep -oP '\[.*?\]\(.*?\)' file.md

# Check if targets exist
# Internal: [text](path.md) or [text](#anchor)
# External: [text](https://...)
```

**Common issues**:
- Broken relative paths
- Missing anchor targets
- Orphaned files (not linked anywhere)

### 5. Compaction Opportunities

Identify verbose patterns that can be condensed.

**Full techniques**: See [compaction-patterns.md](references/compaction-patterns.md)

Quick reference:
| Pattern | Before | After | Savings |
|---------|--------|-------|---------|
| Prose list | Paragraph with items | Bullet list | 40-60% |
| Explanation table | Multi-paragraph | Table | 50-70% |
| Code comments | Heavily commented | Self-documenting | 30-50% |
| Repeated structure | Copy-paste sections | Template + instances | 60-80% |

## Optimization Techniques

### Convert Prose to Tables

**Before** (12 lines):
```markdown
The system supports three user roles. Administrators have full access
to all features including user management, system configuration, and
reporting. Managers can access reports and manage their team members
but cannot modify system settings. Regular users can only access their
own data and perform basic operations within their assigned scope.
```

**After** (6 lines):
```markdown
| Role | Access |
|------|--------|
| Admin | Full access: user management, config, reporting |
| Manager | Reports, team management (no system settings) |
| User | Own data, basic operations |
```

### Extract Examples

**Before** (inline, 50 lines):
```markdown
## API Usage

Here's how to use the API:

```python
# 40 lines of code
```
```

**After** (referenced, 5 lines):
```markdown
## API Usage

See [examples/api-usage.md](examples/api-usage.md) for complete examples.

Quick start:
```python
client.get("/api/resource")
```
```

### Use Progressive Disclosure

**Before** (everything inline):
```markdown
## Feature X
[200 lines of content]
```

**After** (layered):
```markdown
## Feature X

[Core concept - 30 lines]

**Advanced configuration**: See [feature-x-advanced.md](references/feature-x-advanced.md)
**API reference**: See [feature-x-api.md](references/feature-x-api.md)
```

## Custom Profiles

Define custom profiles in `.claude/config/md-profiles.yaml`:

```yaml
profiles:
  # Custom profile for API docs
  api-docs:
    patterns:
      - "docs/api/**"
      - "**/api-*.md"
    max_lines: 400
    rules:
      - require_toc: true
      - require_examples: true
      - max_section_lines: 150
    compaction:
      - prose_to_table: true
      - extract_examples: true

  # Custom profile for internal docs
  internal:
    patterns:
      - "internal/**"
    max_lines: 800  # More lenient
    rules:
      - require_toc: false
```

## Report Templates

### Audit Report Structure

```markdown
# Markdown Optimization Report

## Target: {path}
## Profile: {profile}
## Generated: {timestamp}

## Executive Summary
- Files analyzed: N
- Issues found: N (X critical, Y warnings)
- Estimated optimization potential: N lines (X%)

## Detailed Findings

### Size Issues
[Table of oversized files]

### Structure Issues
[Table of structural problems]

### Duplication
[Table of duplicated content]

### Broken Links
[Table of link issues]

## Recommendations
[Prioritized action items]
```

## Integration with Commands

This skill supports:
- `/docs:optimize-md` - Primary command (use `--profile guidelines` for GUIDELINES.md ecosystem)

## Related

- [GUIDELINES.md](../../GUIDELINES.md) - **Authoritative source** for artifact size limits and quality standards
- [Profile Definitions](references/profiles.md) - Detection patterns and optimization rules per profile
- [Compaction Patterns](references/compaction-patterns.md) - Techniques for reducing verbosity
