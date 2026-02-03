---
name: doc-review
description: "Reviews and cleans up outdated documentation. Use periodically to maintain documentation health. Triggers on: review docs, clean up documentation, check for stale docs."
---

# Doc Review Skill

Systematically review documentation for staleness, accuracy, and relevance.

---

## The Job

1. Scan all documentation files
2. Check for staleness indicators
3. Verify referenced code/files still exist
4. Identify outdated content
5. Generate cleanup report
6. Optionally apply fixes

---

## When to Use

### Scheduled

- After each milestone completion
- Monthly maintenance cycle
- Before major releases

### On Demand

- When documentation feels outdated
- After significant refactoring
- When onboarding reveals confusion

---

## Review Process

### Step 1: Inventory Documentation

Scan for documentation files:

```bash
find . -name "*.md" -not -path "./.git/*" -not -path "./.vendor/*" -not -path "./.worktrees/*"
```

Common locations:
- `README.md` (root and subdirs)
- `docs/` directory
- `AGENTS.md`, `CLAUDE.md`
- `.claude/skills/*/SKILL.md`
- `knowledge/` directory
- `scripts/aha-loop/templates/`

### Step 2: Check Staleness Indicators

For each document, check:

| Indicator | Check Method | Threshold |
|-----------|--------------|-----------|
| Last modified | `git log -1` | > 30 days |
| Referenced files | grep + verify | Missing = stale |
| Code examples | Syntax check | Errors = stale |
| Version numbers | Compare to actual | Mismatch = stale |
| Links | HTTP check | Broken = stale |

### Step 3: Verify Code References

For each code reference in docs:

```markdown
## Code Reference Check

File: [doc-path]
Reference: `src/main.rs:45-60`
Status: [Exists | Missing | Changed]

If Changed:
- Original: [what doc says]
- Current: [what code shows]
- Action: [Update doc | Flag for review]
```

### Step 4: Check External Links

```bash
# Extract URLs
grep -oP 'https?://[^\s)]+' file.md

# Check each URL
curl -s -o /dev/null -w "%{http_code}" URL
```

### Step 5: Generate Report

Create `docs-review-report.md`:

```markdown
# Documentation Review Report

**Date:** [YYYY-MM-DD]
**Reviewed:** [N] files
**Issues Found:** [N]

## Summary

| Category | Count |
|----------|-------|
| Stale (>30 days) | [N] |
| Missing References | [N] |
| Broken Links | [N] |
| Outdated Examples | [N] |

## Issues by File

### [file1.md]
- [ ] Line 45: Reference to `src/old.rs` - file no longer exists
- [ ] Line 78: Code example uses deprecated API

### [file2.md]
- [ ] Line 12: Version "1.0.0" should be "2.0.0"
- [ ] Line 56: Broken link to external docs

## Recommended Actions

1. **Delete:** [files that should be removed]
2. **Update:** [files that need content updates]
3. **Review:** [files that need human review]

## Auto-fixable

The following can be auto-fixed:
- [ ] Update version numbers
- [ ] Remove dead links
- [ ] Update file paths

Run `./scripts/aha-loop/doc-cleaner.sh --fix` to apply.
```

---

## Staleness Criteria

### Definitely Stale

- References files that don't exist
- Contains code that doesn't compile
- Links to 404 pages
- Describes features that were removed

### Probably Stale

- Not modified in 60+ days
- Uses old API patterns
- References old version numbers
- No recent git commits mention the file

### Needs Human Review

- Contains outdated but complex content
- Describes deprecated but still-supported features
- Historical documentation (changelogs, decisions)

---

## Auto-Fix Rules

### Safe to Auto-Fix

- Update file paths (if clear mapping exists)
- Remove broken external links
- Update version numbers in dependency lists
- Fix obvious typos in code references

### Requires Human Review

- Content changes beyond mechanical updates
- Removing entire sections
- Changing technical instructions
- Modifying architecture decisions

---

## Integration

### With Doc Cleaner Script

```bash
# Generate report only
./scripts/aha-loop/doc-cleaner.sh --report

# Apply safe fixes
./scripts/aha-loop/doc-cleaner.sh --fix

# Interactive mode
./scripts/aha-loop/doc-cleaner.sh --interactive
```

### With Observability

Log review activities:

```markdown
## 2026-01-29 16:00:00 | Task: Maintenance | Phase: Doc Review

### Documentation Review
Scanned 45 files, found 7 issues.

### Key Findings
- AGENTS.md references outdated skill paths
- README example code uses deprecated API

### Actions Taken
- Auto-fixed 3 version number issues
- Flagged 4 items for human review
```

---

## Checklist

Before completing review:

- [ ] All markdown files scanned
- [ ] Code references verified
- [ ] External links checked
- [ ] Report generated
- [ ] Auto-fixes applied (if safe)
- [ ] Human review items flagged

---

## Example Review

### Input

File: `docs/api.md` last modified 90 days ago

```markdown
# API Documentation

## Authentication

See `src/auth/mod.rs` for implementation.

Use version 0.5.0 of the auth library:
```toml
auth-lib = "0.5.0"
```

More info: https://example.com/old-docs
```

### Review Findings

1. **Stale**: Last modified 90 days ago
2. **Missing Reference**: `src/auth/mod.rs` doesn't exist (moved to `src/api/auth.rs`)
3. **Outdated Version**: Current version is 1.2.0, not 0.5.0
4. **Broken Link**: https://example.com/old-docs returns 404

### Report Entry

```markdown
### docs/api.md

**Staleness:** 90 days since last update
**Issues:**
- [ ] Line 5: `src/auth/mod.rs` → `src/api/auth.rs`
- [ ] Line 8: Version 0.5.0 → 1.2.0
- [ ] Line 12: Broken link (404)

**Recommendation:** Update file paths and versions, remove broken link
```

---

## Prevention

To reduce future staleness:

1. **Update docs with code** - When changing code, update related docs
2. **Add doc checks to CI** - Fail on broken references
3. **Schedule regular reviews** - Monthly or per-milestone
4. **Use relative links** - Easier to maintain than absolute
5. **Date-stamp examples** - "As of v1.2.0"
