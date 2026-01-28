---
name: fix-docs
description: |
  Run /check-docs, then fix the highest priority documentation issue.
  Creates one fix per invocation. Invoke again for next issue.
  Use /log-doc-issues to create issues without fixing.
---

# /fix-docs

Fix the highest priority documentation gap.

## What This Does

1. Invoke `/check-docs` to audit documentation
2. Identify highest priority gap
3. Fix that one issue
4. Verify the fix
5. Report what was done

**This is a fixer.** It fixes one issue at a time. Run again for next issue. Use `/documentation` for full setup.

## Process

### 1. Run Primitive

Invoke `/check-docs` skill to get prioritized findings.

### 2. Fix Priority Order

Fix in this order:
1. **P0**: Missing README.md, missing .env.example
2. **P1**: README sections, undocumented env vars, architecture
3. **P2**: Stale docs, CONTRIBUTING.md, ADRs
4. **P3**: Polish, extras

### 3. Execute Fix

**Missing README.md (P0):**
Generate README with proper structure:
- Project name and tagline
- What it does (one paragraph)
- Quick Start (3 commands max)
- Configuration (env vars)
- Development commands
- License

Delegate to Codex or write directly.

**Missing .env.example (P0):**
```bash
# Scan for env vars and create .env.example
grep -rhoE "process\.env\.[A-Z_]+" --include="*.ts" --include="*.tsx" src/ app/ 2>/dev/null | \
  sort -u | sed 's/process.env.//' | \
  awk '{print $1"="}' > .env.example
```

**README missing sections (P1):**
Add the missing section with appropriate content.

**Undocumented env vars (P1):**
Add missing vars to .env.example with comments.

**Missing architecture docs (P1):**
Invoke `/cartographer` to generate CODEBASE_MAP.md.

**Stale documentation (P2):**
Review and update outdated content.

### 4. Verify

After fix:
```bash
# Verify file exists
[ -f "README.md" ] && echo "✓ README exists"
[ -f ".env.example" ] && echo "✓ .env.example exists"

# Verify content
grep -q "## Installation" README.md && echo "✓ Has installation"
grep -q "## Quick Start" README.md && echo "✓ Has quick start"
```

### 5. Report

```
Fixed: [P0] Missing README.md

Created README.md with:
- Project description
- Quick start guide
- Environment setup
- Development commands

Next highest priority: [P1] Missing .env.example
Run /fix-docs again to continue.
```

## Branching

Before making changes:
```bash
git checkout -b docs/fix-$(date +%Y%m%d)
```

## Single-Issue Focus

This skill fixes **one issue at a time**. Benefits:
- Small, reviewable changes
- Easy to revert if needed
- Clear commit history
- Predictable behavior

Run `/fix-docs` repeatedly to work through the backlog.

## Related

- `/check-docs` - The primitive (audit only)
- `/log-doc-issues` - Create issues without fixing
- `/documentation` - Full documentation workflow
- `/cartographer` - Generate architecture docs
