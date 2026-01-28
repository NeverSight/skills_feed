---
name: changelog-audit
description: |
  Audit existing changelog/release infrastructure.
  Finds issues, misconfigurations, and drift.
---

# Changelog Audit

Deep analysis of existing release infrastructure.

## Objective

Find everything that's wrong, suboptimal, or missing. Produce actionable findings.

## Process

### 1. Configuration Audit

**semantic-release config:**
```bash
# Config exists and is valid?
node -e "require('./.releaserc.js')" 2>&1 || echo "INVALID CONFIG"

# Required plugins present?
grep -q "@semantic-release/changelog" .releaserc.js || echo "MISSING: changelog plugin"
grep -q "@semantic-release/git" .releaserc.js || echo "MISSING: git plugin"
grep -q "@semantic-release/github" .releaserc.js || echo "MISSING: github plugin"

# Branch configuration correct?
grep -q "main\|master" .releaserc.js || echo "WARNING: branch config may be wrong"
```

**commitlint config:**
```bash
# Config exists?
ls commitlint.config.* 2>/dev/null || echo "MISSING: commitlint config"

# Extends conventional config?
grep -q "config-conventional" commitlint.config.* 2>/dev/null || echo "WARNING: not using conventional config"
```

**Lefthook integration:**
```bash
# commit-msg hook exists?
grep -q "commit-msg" lefthook.yml 2>/dev/null || echo "MISSING: commit-msg hook in Lefthook"

# Hook runs commitlint?
grep -A5 "commit-msg" lefthook.yml 2>/dev/null | grep -q "commitlint" || echo "WARNING: commit-msg doesn't run commitlint"
```

### 2. GitHub Actions Audit

**Workflow exists and is correct:**
```bash
# Workflow file exists?
ls .github/workflows/release.yml 2>/dev/null || echo "MISSING: release workflow"

# Has required permissions?
grep -q "contents: write" .github/workflows/release.yml || echo "MISSING: contents write permission"

# Runs semantic-release?
grep -q "semantic-release" .github/workflows/release.yml || echo "WARNING: workflow doesn't run semantic-release"

# Has fetch-depth: 0?
grep -q "fetch-depth: 0" .github/workflows/release.yml || echo "WARNING: missing fetch-depth: 0 (needed for changelog)"
```

**LLM synthesis workflow:**
```bash
# Synthesis job exists?
grep -q "synthesize" .github/workflows/release.yml || echo "MISSING: synthesis job"

# References Gemini API key?
grep -q "GEMINI_API_KEY" .github/workflows/release.yml || echo "MISSING: GEMINI_API_KEY reference"

# Synthesis script exists?
ls scripts/synthesize-release-notes.mjs 2>/dev/null || echo "MISSING: synthesis script"
```

### 3. Secrets Audit

```bash
# Check if secrets are configured (can't read values, just check existence)
gh secret list | grep -q "GEMINI_API_KEY" || echo "MISSING: GEMINI_API_KEY secret"

# NPM_TOKEN only needed if publishing
grep -q "@semantic-release/npm" .releaserc.js && {
  gh secret list | grep -q "NPM_TOKEN" || echo "MISSING: NPM_TOKEN secret (needed for npm publish)"
}
```

### 4. Public Page Audit

```bash
# Page exists?
ls app/changelog/page.tsx src/app/changelog/page.tsx 2>/dev/null || echo "MISSING: changelog page"

# RSS feed exists?
ls app/changelog.xml/route.ts app/changelog/rss/route.ts public/changelog.xml 2>/dev/null || echo "MISSING: RSS feed"

# Page is public (no auth wrapper)?
grep -q "auth\|protect\|middleware" app/changelog/page.tsx 2>/dev/null && echo "WARNING: changelog page may have auth"
```

### 5. Release Health Check

```bash
# Recent releases exist?
RELEASES=$(gh release list --limit 5 --json tagName,publishedAt 2>/dev/null)
echo "Recent releases: $RELEASES"

# Releases have bodies (LLM notes)?
gh release view --json body | jq -r '.body' | head -5

# CHANGELOG.md in sync with releases?
head -50 CHANGELOG.md

# Any failed workflow runs?
gh run list --workflow=release.yml --status=failure --limit 5
```

### 6. Commit History Audit

```bash
# Recent commits follow conventional format?
git log --oneline -20 | while read line; do
  echo "$line" | grep -qE "^[a-f0-9]+ (feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+\))?: " || echo "NON-CONVENTIONAL: $line"
done

# Any commits that should have triggered releases but didn't?
git log --oneline main --since="1 week ago" | grep -E "^[a-f0-9]+ (feat|fix|perf):" | head -10
```

## Output

Structured findings report:

```
CHANGELOG AUDIT REPORT
======================

CONFIGURATION
├── semantic-release: [OK | ISSUE: description]
├── commitlint: [OK | ISSUE: description]
└── Lefthook hook: [OK | ISSUE: description]

GITHUB ACTIONS
├── Release workflow: [OK | ISSUE: description]
├── Permissions: [OK | ISSUE: description]
├── Synthesis job: [OK | ISSUE: description]
└── Synthesis script: [OK | ISSUE: description]

SECRETS
├── GEMINI_API_KEY: [CONFIGURED | MISSING]
└── NPM_TOKEN: [CONFIGURED | MISSING | NOT NEEDED]

PUBLIC PAGE
├── Changelog route: [OK | MISSING]
├── RSS feed: [OK | MISSING]
└── Auth status: [PUBLIC | WARNING: may have auth]

RELEASE HEALTH
├── Recent releases: [N releases | NONE]
├── Release notes: [POPULATED | EMPTY]
├── CHANGELOG.md: [IN SYNC | OUT OF SYNC]
└── Failed runs: [NONE | N failures]

COMMIT HEALTH
├── Conventional format: [N/20 compliant]
└── Missed releases: [NONE | N commits should have released]

---
SUMMARY: X pass, Y warn, Z fail

CRITICAL:
- [List critical issues]

HIGH:
- [List high priority issues]

MEDIUM:
- [List medium priority issues]
```

## Issue Categories

**CRITICAL** (blocks releases):
- Missing or invalid semantic-release config
- Missing GitHub Actions workflow
- Missing required permissions

**HIGH** (degrades quality):
- Missing commitlint enforcement
- Missing LLM synthesis
- Empty release notes

**MEDIUM** (nice to have):
- Missing RSS feed
- Non-conventional commits in history
- Missing public page
