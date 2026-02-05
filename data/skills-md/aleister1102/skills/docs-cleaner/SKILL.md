---
name: docs-cleaner
description: Use when cleaning up redundant documentation, merging duplicates, or consolidating sprawling guides while preserving all valuable content.
---

# Documentation Cleaner

Consolidate redundant documentation while preserving 100% of valuable content.

## When to Use
- You need to merge overlapping docs that currently span several files or exceed 500 lines.
- Multiple materials cover the same topic and reviewers are confused about the canonical source.
- Documentation editors request a value-preserving consolidation before publishing or sharing the guidance.

## When NOT to Use
- The docs are short, focused, and already reference each other intentionally.
- You are performing unrelated documentation like simple typo fixes or formatting tweaks.
- The goal is to keep historical drafts or archives rather than remove redundancy.

## Core Principle

**Critical evaluation before deletion.** Never blindly delete. Analyze each section's unique value before proposing removal. The goal is reduction without information loss.

## Workflow

### Phase 1: Discovery

1. Identify all documentation files covering the topic
2. Count total lines across files
3. Map content overlap between documents

### Phase 2: Value Analysis

For each document, create a section-by-section analysis table:

| Section | Lines | Value | Reason |
|---------|-------|-------|--------|
| API Reference | 25 | Keep | Unique endpoint documentation |
| Setup Steps | 40 | Condense | Verbose but essential |
| Test Results | 30 | Delete | One-time record, not reference |

Value categories:
- **Keep**: Unique, essential, frequently referenced
- **Condense**: Valuable but verbose
- **Delete**: Duplicate, one-time, self-evident, outdated

See `references/value_analysis_template.md` for detailed criteria.

### Phase 3: Consolidation Plan

Propose target structure:

```
Before: 726 lines (3 files, high redundancy)
After:  ~100 lines (1 file + reference in CLAUDE.md)
Reduction: 86%
Value preserved: 100%
```

### Phase 4: Execution

1. Create consolidated document with all valuable content
2. Delete redundant source files
3. Update references (CLAUDE.md, README, imports)
4. Verify no broken links

## Value Preservation Checklist

Before finalizing, confirm preservation of:

- [ ] Essential procedures (setup, configuration)
- [ ] Key constraints and gotchas
- [ ] Troubleshooting guides
- [ ] Technical debt / roadmap items
- [ ] External links and references
- [ ] Debug tips and code snippets

## Anti-Patterns

| Pattern | Problem | Solution |
|---------|---------|----------|
| Blind deletion | Loses valuable information | Section-by-section analysis first |
| Keeping everything | No reduction achieved | Apply value criteria strictly |
| Multiple sources of truth | Future divergence | Single authoritative location |
| Orphaned references | Broken links | Update all references after consolidation |

## Output Artifacts

A successful cleanup produces:

1. **Consolidated document** - Single source of truth
2. **Value analysis** - Section-by-section justification
3. **Before/after metrics** - Lines reduced, value preserved
4. **Updated references** - CLAUDE.md or README with pointer to new location
