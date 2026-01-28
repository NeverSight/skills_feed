---
name: documentation
description: |
  Complete documentation infrastructure. Audits current docs, generates missing pieces,
  updates stale content, and verifies everything works. Every run does the full cycle.
argument-hint: "[focus area, e.g. 'README' or 'architecture']"
---

# /documentation

Ensure this project has complete, current documentation. Audit, fix, verify—every time.

## What This Does

Examines project documentation, identifies gaps and staleness, generates/updates what's needed, and verifies links and examples work. No partial modes.

## Branching

Assumes you start on `master`/`main`. Before making documentation changes:

```bash
git checkout -b docs/update-$(date +%Y%m%d)
```

## Process

### 1. Audit

**Quick scan for what exists:**
```bash
# Core docs
[ -f "README.md" ] && echo "✓ README" || echo "✗ README"
[ -f "ARCHITECTURE.md" ] || [ -f "docs/ARCHITECTURE.md" ] || [ -f "docs/CODEBASE_MAP.md" ] && echo "✓ Architecture" || echo "✗ Architecture"
[ -f "CONTRIBUTING.md" ] && echo "✓ CONTRIBUTING" || echo "✗ CONTRIBUTING"
[ -f ".env.example" ] && echo "✓ .env.example" || echo "✗ .env.example"
[ -d "docs/adr" ] || [ -d "docs/adrs" ] && echo "✓ ADR directory" || echo "✗ ADR directory"

# API docs (for libraries)
[ -f "docs/api.md" ] || [ -d "docs/api" ] && echo "✓ API docs" || echo "✗ API docs"

# Subdirectory READMEs (for complex projects)
find . -type d -name "src" -o -name "packages" -o -name "apps" 2>/dev/null | head -5 | while read d; do
  [ -f "$d/README.md" ] && echo "✓ $d/README.md" || echo "⚠ $d/README.md missing"
done
```

**Check staleness:**
```bash
# Find docs not updated in 90+ days
find . -name "*.md" -path "./docs/*" -o -name "README.md" -o -name "CONTRIBUTING.md" | while read f; do
  if [ -f "$f" ]; then
    age=$(( ($(date +%s) - $(stat -f %m "$f" 2>/dev/null || stat -c %Y "$f" 2>/dev/null)) / 86400 ))
    [ $age -gt 90 ] && echo "STALE ($age days): $f"
  fi
done
```

**Check link validity (if lychee installed):**
```bash
command -v lychee >/dev/null && lychee --offline *.md docs/**/*.md 2>/dev/null || echo "Install lychee for link checking: brew install lychee"
```

**Spawn agent for deep review:**
Spawn `documentation-quality-reviewer` agent for comprehensive analysis if docs exist but quality is uncertain.

### 2. Plan

Prioritize gaps based on project type:

**Every project needs:**
- README.md (what, why, quick start, setup)
- .env.example (if any env vars used)

**Applications need:**
- ARCHITECTURE.md or CODEBASE_MAP.md (system design)
- ADRs for significant decisions

**Libraries need:**
- API documentation (JSDoc → generated docs)
- CONTRIBUTING.md
- Examples in README

**Monorepos need:**
- Root README with overview
- Subdirectory READMEs for each package/app
- Workspace setup instructions

**Open source projects need:**
- CONTRIBUTING.md (must have)
- CODE_OF_CONDUCT.md
- Issue/PR templates

### 3. Execute

**Fix everything.** Don't stop at a report.

**Generate README.md (if missing):**
Delegate to Codex with context from package.json, code structure:
```bash
codex exec --full-auto "Generate README.md for this project. \
Include: project name, description, features, prerequisites, installation, \
quick start, configuration, development commands. \
Reference package.json for scripts and dependencies. \
Follow documentation-standards skill patterns." \
--output-last-message /tmp/codex-readme.md 2>/dev/null
```

**Generate architecture docs (if missing):**
Run Cartographer to create CODEBASE_MAP.md:
```
Invoke /cartographer to map this codebase
```
This creates `docs/CODEBASE_MAP.md` with architecture diagrams, module guide, navigation.

**Generate .env.example (if missing):**
Scan codebase for env var usage:
```bash
# Find env var references
grep -r "process\.env\." --include="*.ts" --include="*.tsx" --include="*.js" . | \
  grep -oE "process\.env\.[A-Z_]+" | sort -u | \
  sed 's/process.env.//' | \
  awk '{print $1"="}'
```
Create `.env.example` with discovered vars and placeholder values.

**Generate CONTRIBUTING.md (if missing and needed):**
Delegate to Codex:
```bash
codex exec --full-auto "Generate CONTRIBUTING.md for this project. \
Include: how to set up dev environment, coding standards, \
commit message format, PR process, testing requirements. \
Reference existing configs (ESLint, Prettier, Lefthook) for standards." \
--output-last-message /tmp/codex-contributing.md 2>/dev/null
```

**Create ADR directory and template (if missing):**
```bash
mkdir -p docs/adr
```
Create `docs/adr/template.md` and `docs/adr/README.md` per `documentation-standards`.

**Update stale docs:**
For each stale doc, analyze what's changed and update:
- Check git log for related changes since last doc update
- Identify sections that may be outdated
- Update or flag for manual review if significant

**Subdirectory READMEs:**
For complex projects with src/, packages/, apps/ directories, generate module-level READMEs explaining purpose and key exports.

### 4. Verify

**Link checking:**
```bash
# Install if needed
command -v lychee >/dev/null || brew install lychee

# Check all markdown files
lychee --offline *.md docs/**/*.md README.md
```

**Example validation:**
For code examples in docs, verify they're syntactically valid:
```bash
# Extract code blocks and check syntax (TypeScript)
grep -A 20 '```typescript' README.md | grep -v '```' > /tmp/example.ts
pnpm tsc --noEmit /tmp/example.ts 2>/dev/null && echo "✓ Examples valid" || echo "⚠ Example syntax issues"
```

**Completeness check:**
```bash
# Minimum viable docs
[ -f "README.md" ] && echo "✓ README exists" || echo "✗ README MISSING"
grep -q "## Installation" README.md && echo "✓ Installation section" || echo "⚠ No installation section"
grep -q "## Quick Start" README.md || grep -q "## Getting Started" README.md && echo "✓ Quick start section" || echo "⚠ No quick start section"
[ -f ".env.example" ] || ! grep -r "process.env" --include="*.ts" . -q && echo "✓ Env documented" || echo "⚠ Env vars used but no .env.example"
```

If any verification fails, go back and fix it.

## Documentation Standards

Reference `documentation-standards` skill throughout. Key principles:

**Comments:** Why, not what. Code should be self-documenting.

**README structure:**
1. What (one sentence)
2. Why (problem it solves)
3. Quick Start (fastest path to running)
4. Setup (prerequisites, installation, configuration)
5. Usage examples
6. Contributing (if applicable)
7. License

**Architecture docs:** Use Cartographer for comprehensive mapping.

**ADR format:** Context → Decision → Consequences → Alternatives Considered

## Tool Choices

**Link checking:** lychee (Rust, fast, offline-capable)
**Doc linting:** Vale (if style enforcement needed)
**Architecture mapping:** Cartographer (parallel subagent approach)

## What You Get

When complete:
- README.md with what, why, quick start, setup
- .env.example documenting all env vars
- Architecture docs (CODEBASE_MAP.md or ARCHITECTURE.md)
- ADR directory with template (for significant decisions)
- CONTRIBUTING.md (if open source or team project)
- All links verified working
- No stale documentation (or flagged for review)

User can:
- Clone repo and get running via README quick start
- Understand system architecture from docs
- Know what env vars to configure
- Find contributor guidelines easily
- Trust that documentation is current
