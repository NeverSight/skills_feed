---
name: check-docs
description: |
  Audit documentation: README, architecture, API docs, .env.example.
  Outputs structured findings. Use log-doc-issues to create issues.
  Invoke for: documentation audit, gap analysis, staleness check.
---

# /check-docs

Audit project documentation. Output findings as structured report.

## What This Does

1. Check for required documentation files
2. Assess documentation completeness
3. Detect stale/outdated content
4. Verify links and examples
5. Output prioritized findings (P0-P3)

**This is a primitive.** It only investigates and reports. Use `/log-doc-issues` to create GitHub issues or `/fix-docs` to fix.

## Process

### 1. Core Documentation Check

```bash
# Required docs
[ -f "README.md" ] && echo "✓ README" || echo "✗ README"
[ -f ".env.example" ] && echo "✓ .env.example" || echo "✗ .env.example"
[ -f "ARCHITECTURE.md" ] || [ -f "docs/ARCHITECTURE.md" ] || [ -f "docs/CODEBASE_MAP.md" ] && echo "✓ Architecture" || echo "✗ Architecture"
[ -f "CONTRIBUTING.md" ] && echo "✓ CONTRIBUTING" || echo "✗ CONTRIBUTING"
[ -d "docs/adr" ] || [ -d "docs/adrs" ] && echo "✓ ADR directory" || echo "✗ ADR directory"
```

### 2. README Quality Check

```bash
# Check README sections
grep -q "## Installation" README.md 2>/dev/null && echo "✓ Installation section" || echo "✗ Installation section"
grep -q "## Quick Start" README.md 2>/dev/null || grep -q "## Getting Started" README.md 2>/dev/null && echo "✓ Quick start" || echo "✗ Quick start"
grep -q "## Configuration" README.md 2>/dev/null || grep -q "## Setup" README.md 2>/dev/null && echo "✓ Configuration" || echo "✗ Configuration"
```

### 3. .env.example Coverage

```bash
# Find env vars used but not documented
grep -rhoE "process\.env\.[A-Z_]+" --include="*.ts" --include="*.tsx" src/ app/ 2>/dev/null | \
  sort -u | sed 's/process.env.//' > /tmp/env-used.txt
[ -f ".env.example" ] && cut -d= -f1 .env.example > /tmp/env-documented.txt || touch /tmp/env-documented.txt
comm -23 <(sort /tmp/env-used.txt) <(sort /tmp/env-documented.txt) 2>/dev/null
```

### 4. Staleness Check

```bash
# Find docs not updated in 90+ days
find . -name "*.md" \( -path "./docs/*" -o -name "README.md" -o -name "CONTRIBUTING.md" \) 2>/dev/null | while read f; do
  if [ -f "$f" ]; then
    age=$(( ($(date +%s) - $(stat -f %m "$f" 2>/dev/null || stat -c %Y "$f" 2>/dev/null)) / 86400 ))
    [ $age -gt 90 ] && echo "STALE ($age days): $f"
  fi
done
```

### 4a. Auth System Consistency Check

When auth system changes (Clerk, Auth0, Convex Auth, etc.), docs often reference the old system.

```bash
# Detect auth inconsistencies
# Check README for current auth
current_auth=$(grep -oE "Clerk|Auth0|Convex Auth|NextAuth|Magic Link|Supabase Auth" README.md 2>/dev/null | head -1)

# Check docs for references to OTHER auth systems
if [ "$current_auth" = "Clerk" ]; then
  # Look for outdated auth references
  grep -rlE "Magic Link|Resend|RESEND_API_KEY|Convex Auth|EMAIL_FROM" docs/ 2>/dev/null | while read f; do
    echo "⚠ INCONSISTENT ($f): References old auth system, but README uses Clerk"
  done
fi
```

**Common auth migration leftovers:**
- `RESEND_API_KEY` when moved to Clerk (Clerk handles email)
- `Magic Link` references when using Clerk social login
- `Convex Auth` when using Clerk with Convex
- `EMAIL_FROM` env var when no longer sending auth emails

### 5. Link Validation

```bash
# Check for broken links (if lychee installed)
command -v lychee >/dev/null && lychee --offline *.md docs/**/*.md 2>/dev/null || echo "Install lychee for link checking"
```

## Output Format

```markdown
## Documentation Audit

### P0: Critical (Blocking)
- Missing README.md - Users cannot understand project
- Missing .env.example - Developers cannot set up environment

### P1: Essential (Required)
- README missing Installation section
- README missing Quick Start section
- 5 env vars used but not in .env.example: STRIPE_SECRET_KEY, ...
- No architecture documentation

### P2: Important (Should Have)
- README.md stale (120 days since update)
- No CONTRIBUTING.md for open source project
- No ADR directory for significant decisions

### P3: Nice to Have
- Consider adding API documentation
- Consider subdirectory READMEs for packages/

## Summary
- P0: 2 | P1: 4 | P2: 3 | P3: 2
- Missing files: README.md, .env.example
- Stale docs: 1
- Recommendation: Create README and .env.example immediately
```

## Priority Mapping

| Gap | Priority |
|-----|----------|
| Missing README.md | P0 |
| Missing .env.example (with env vars used) | P0 |
| Incomplete README sections | P1 |
| Missing architecture docs | P1 |
| Undocumented env vars | P1 |
| Stale documentation | P2 |
| Missing CONTRIBUTING.md | P2 |
| Missing ADRs | P2 |
| Polish and extras | P3 |

## Related

- `/log-doc-issues` - Create GitHub issues from findings
- `/fix-docs` - Fix documentation gaps
- `/documentation` - Full documentation workflow
- `/cartographer` - Generate architecture docs
