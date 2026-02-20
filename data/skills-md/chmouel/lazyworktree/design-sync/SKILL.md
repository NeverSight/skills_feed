---
name: design-sync
description: Check DESIGN.md synchronization with codebase architecture
---

# DESIGN.md Synchronization Check

Verify that DESIGN.md accurately reflects the current codebase architecture.

## Current Directory Structure
!`ls -la internal/ | grep '^d'`

## DESIGN.md Directory Section
!`sed -n '/^## Directory Structure/,/^## /p' DESIGN.md | head -50`

## Critical File References from DESIGN.md
!`grep -oE 'internal/[a-z/]+\.go:[0-9]+-[0-9]+' DESIGN.md | sort -u`

## Recent Changes Since Last DESIGN.md Update
!`git log --since="$(git log -1 --format=%ai DESIGN.md 2>/dev/null || echo '1 month ago')" --name-only --oneline -- 'internal/**/*.go' | grep -E '^internal/' | sort -u`

## Current Package Import Graph
!`go list -f '{{.ImportPath}}: {{join .Imports ", "}}' ./internal/... 2>/dev/null | grep 'lazyworktree/internal' | head -30`

## DESIGN.md Metadata
!`head -20 DESIGN.md | grep -E '(Last updated|Version)'`

## Theme Fields Documented vs Actual
!`echo "=== Documented theme fields ===" && grep -A 20 'type Theme struct' DESIGN.md | grep -oE '^\s+[A-Z][a-zA-Z]+' | wc -l && echo "=== Actual theme fields ===" && grep -A 30 'type Theme struct' internal/app/theme.go | grep -oE '^\s+[A-Z][a-zA-Z]+' | wc -l`

---

## Analysis Instructions

Based on the data above, check for:

### 1. Directory Structure Drift
- Are there new directories under `internal/` not documented in DESIGN.md?
- Have documented directories been removed or renamed?
- Compare the actual directory listing with the documented structure section

### 2. Critical File References
- Extract all `file:line-range` references from DESIGN.md (e.g., `app.go:77-210`)
- For each reference:
  - Verify the file still exists at that path
  - Check if line numbers still point to the documented code section
  - If lines have shifted due to refactoring, report the new correct line numbers
- Report any broken references or significant drift

### 3. Recent Architectural Changes
- Review files changed since the last DESIGN.md update
- Identify if changes affect documented abstractions:
  - BubbleTea Model/Update/View pattern
  - Git service semaphore implementation
  - Screen manager stack
  - Theme system
  - Config cascade
- Flag changes to critical files that may require DESIGN.md updates

### 4. Import Graph Consistency
- Compare current package imports with the documented dependency graph
- Flag new internal dependencies not mentioned in DESIGN.md
- Flag removed dependencies still documented
- Check for circular dependencies (which violate documented patterns)

### 5. Theme System Accuracy
- Verify the count of theme fields matches between documentation and actual code
- If counts differ, identify which fields are missing from documentation

### 6. Staleness Check
- Report if DESIGN.md hasn't been updated in >90 days
- Suggest updating the "Last updated" date if structural changes were made

## Report Format

Provide output as:

### ✅ Up to Date
- List specific aspects that are still accurate and synchronized

### ⚠️ Needs Minor Updates
- Line number corrections (e.g., `app.go:77-210 → app.go:87-220`)
- New directories to add to documentation
- Minor import graph changes
- Theme field count discrepancies

### 🔴 Needs Major Updates
- New abstractions or components not documented
- Documented components removed or significantly changed
- Architecture decisions that have changed
- Broken file references

### 📝 Recommended Actions
1. Specific edits with DESIGN.md line numbers to update
2. New sections to add (with suggested content outline)
3. Sections to remove or rewrite
4. Line number corrections for all file references

---

## Usage Workflow

### When to Invoke `/design-sync`

**Proactive triggers** (before committing):
- Added new package under `internal/`
- Refactored critical files (app.go, service.go, model.go, etc.)
- Changed architecture pattern (Model-Update-View, semaphore, etc.)
- Added new screen type or theme field
- Modified config cascade or precedence rules

**Periodic triggers**:
- Quarterly maintenance review
- Before major release
- After merging large architectural PRs
- When DESIGN.md feels outdated

### Recommended Workflow
```bash
# 1. Make architectural changes

# 2. Run design-sync skill
/design-sync

# 3. Review output for needed updates

# 4. Update DESIGN.md based on recommendations

# 5. Update "Last updated" date in DESIGN.md

# 6. Re-run to verify
/design-sync  # Should now show ✅ Up to Date

# 7. Commit changes together
```
