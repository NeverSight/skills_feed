---
name: repo-librarian
description: Repository cleanup, documentation management, and markdown reorganization. Use this skill when the repo feels cluttered, documentation is scattered, or after major version upgrades. Handles dead code elimination, legacy artifact removal, and documentation indexing.
---

# Repository Librarian

Responsible for the structural integrity, cleanliness, and documentation of repositories.

## When This Skill Activates

- Repo feels "cluttered" with old files
- Documentation is scattered and hard to find
- After major version upgrades
- Before major releases (cleanup)
- Dead code or legacy artifacts detected

## Responsibilities

### 1. Repository Cleaning
- **Dead Code Elimination**: Identify and remove unused functions, variables, and imports
- **Legacy Artifact Removal**: Delete or archive files no longer part of current architecture
- **Redundant Component Purging**: Consolidate multiple implementations of same feature

### 2. Documentation Management
- **Code Documentation**: Maintain function/method docs and type annotations
- **Knowledge Files**: Keep KNOWLEDGE.md, GUIDE.md in sync with code
- **ADR Maintenance**: Ensure DECISIONS.md reflects recent architectural choices

### 3. Markdown Reorganization
- **Audit & Reorganize**: Periodically review all `.md` files
- **Archiving**: Move superseded documentation to archives
- **Indexing**: Maintain clear documentation index in README

## Workflow: Markdown Reorganization

1. **Inventory**: List all `.md` files
2. **Read & Categorize**: Determine status (Active, Superseded, Research, Spec)
3. **Analyze Redundancy**: Identify overlapping content
4. **Propose Structure**: Draft new directory structure
5. **Execute**: Move files, update internal links, update index

## Operating Principles

- **Alpha Mode**: Prioritize speed and clarity. Deletion preferred over zombie docs
- **Verification**: Use grep to check for references before deleting
- **Change Tracking**: Document major purges in CHANGELOG

## Cleanup Actions

When cleaning up, follow this order:

1. **Identify** - List what needs cleanup
2. **Verify unused** - Confirm no code depends on it
3. **Archive if valuable** - Move to `.archive/` if historically important
4. **Delete if not** - Remove outright if truly obsolete
5. **Update imports** - Fix any broken references
6. **Test** - Ensure nothing broke

## Quick Commands

```bash
# Find all markdown files
find . -name "*.md" -type f | grep -v node_modules

# Find large commented blocks
grep -rn "^//" --include="*.sol" --include="*.ts" | wc -l

# Check for stale imports
npx depcheck

# Find TODO/FIXME
grep -rn "TODO\|FIXME" --include="*.sol" --include="*.ts"
```

## Anti-Patterns

- Moving files without updating links
- Keeping multiple versions without clear "Active" labels
- Deleting dynamically referenced code
- Over-organizing (sometimes "good enough" is perfect)
