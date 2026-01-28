---
name: changelog
description: |
  Complete changelog and release notes infrastructure. Audits current state,
  implements missing components, and verifies the release pipeline works end-to-end.
argument-hint: "[focus area, e.g. 'LLM synthesis' or 'public page']"
---

# /changelog

Automated changelogs, semantic versioning, and user-friendly release notes. Audit, fix, verify—every time.

## What This Does

Examines your release infrastructure, identifies every gap, implements fixes, and verifies the full pipeline works. No partial modes. Every run does the full cycle.

## Process

### 1. Audit

Check what exists and what's broken:

```bash
# Configuration
[ -f ".releaserc.js" ] || [ -f ".releaserc.json" ] && echo "✓ semantic-release" || echo "✗ semantic-release"
[ -f "commitlint.config.js" ] || [ -f "commitlint.config.cjs" ] && echo "✓ commitlint" || echo "✗ commitlint"
grep -q "commit-msg" lefthook.yml 2>/dev/null && echo "✓ commit-msg hook" || echo "✗ commit-msg hook"

# GitHub Actions
[ -f ".github/workflows/release.yml" ] && echo "✓ release workflow" || echo "✗ release workflow"
grep -q "semantic-release" .github/workflows/release.yml 2>/dev/null && echo "✓ runs semantic-release" || echo "✗ doesn't run semantic-release"
grep -q "GEMINI_API_KEY" .github/workflows/release.yml 2>/dev/null && echo "✓ LLM synthesis configured" || echo "✗ LLM synthesis missing"

# Public page
ls app/changelog/page.tsx src/app/changelog/page.tsx 2>/dev/null && echo "✓ changelog page" || echo "✗ changelog page"

# Health
gh release list --limit 3 2>/dev/null || echo "✗ no releases"
```

**Commit history check:**
```bash
git log --oneline -10 | while read line; do
  echo "$line" | grep -qE "^[a-f0-9]+ (feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+\))?: " || echo "NON-CONVENTIONAL: $line"
done
```

### 2. Plan

From audit findings, build remediation plan. Every project needs:

**Must have:**
- semantic-release configured with changelog, git, github plugins
- commitlint enforcing conventional commits
- Lefthook commit-msg hook running commitlint
- GitHub Actions workflow running semantic-release on push to main

**Should have:**
- LLM synthesis transforming technical changelog to user-friendly notes
- Public `/changelog` page fetching from GitHub Releases API
- RSS feed at `/changelog.xml` or `/changelog/rss`

### 3. Execute

**Fix everything.** Don't stop at a report.

**Installing semantic-release:**
```bash
pnpm add -D semantic-release @semantic-release/changelog @semantic-release/git @semantic-release/github
```

Create `.releaserc.js`:
```javascript
module.exports = {
  branches: ['main'],
  plugins: [
    '@semantic-release/commit-analyzer',
    '@semantic-release/release-notes-generator',
    ['@semantic-release/changelog', { changelogFile: 'CHANGELOG.md' }],
    ['@semantic-release/git', { assets: ['CHANGELOG.md', 'package.json'] }],
    '@semantic-release/github',
  ],
};
```

**Installing commitlint:**
```bash
pnpm add -D @commitlint/cli @commitlint/config-conventional
```

Create `commitlint.config.js`:
```javascript
module.exports = { extends: ['@commitlint/config-conventional'] };
```

Add to `lefthook.yml`:
```yaml
commit-msg:
  commands:
    commitlint:
      run: pnpm commitlint --edit {1}
```

**Creating release workflow:**
Create `.github/workflows/release.yml` per `changelog-setup` reference.

**Adding LLM synthesis:**

> **REQUIRED:** Before implementing, read `llm-infrastructure/references/model-research-required.md`
>
> Do NOT use model names from this document or your training data.
> Run the OpenRouter fetch script and web search to determine current best model for this task.

Steps:
1. **Research current models** (MANDATORY):
   ```bash
   # Query OpenRouter for current fast/cheap models
   python3 ~/.claude/skills/llm-infrastructure/scripts/fetch-openrouter-models.py \
     --task fast --filter "google|anthropic|openai" --top 10

   # Web search: "best LLM for text summarization 2026"
   # Web search: "Gemini API current models 2026"
   ```

2. Create `scripts/synthesize-release-notes.mjs` that:
   - Fetches latest release from GitHub API
   - Uses OpenRouter API (not direct provider APIs) for flexibility
   - Model name comes from environment variable, NOT hardcoded
   - Gets user-friendly summary back
   - Updates release body via GitHub API

3. Configure secrets in GitHub:
   - `OPENROUTER_API_KEY` (preferred) or provider-specific key
   - Model name as environment variable (e.g., `LLM_MODEL_SYNTHESIS`)

**Creating public changelog page:**
Per `changelog-page`, create:
- `app/changelog/page.tsx` - Fetches from GitHub Releases API
- Groups releases by minor version
- No auth required (public page)
- RSS feed support

**Making changelog discoverable (CRITICAL):**
A changelog page that users can't find is useless. Ensure:
- **Footer link**: Add "changelog" link to global footer (visible on landing page)
- **Settings link**: Add "View changelog" link in app settings/about section
- **Version display**: Show current app version in settings (use `NEXT_PUBLIC_APP_VERSION` env var)
- **RSS link**: Mention RSS feed on the changelog page itself

Example footer links:
```tsx
<Link href="/changelog">changelog</Link>
<Link href="/support">support</Link>
<Link href="/privacy">privacy</Link>
```

Example settings "About" section:
```tsx
<div className="flex items-center justify-between">
  <span>Version</span>
  <span className="font-mono">{process.env.NEXT_PUBLIC_APP_VERSION || '0.1.0'}</span>
</div>
<Link href="/changelog">View changelog →</Link>
```

Delegate implementation to Codex where appropriate.

### 4. Verify

**Prove it works.** Not "config exists"—actually works.

**Commitlint test:**
```bash
echo "bad message" | pnpm commitlint
# Should fail

echo "feat: valid message" | pnpm commitlint
# Should pass
```

**Commit hook test:**
```bash
# Try to commit with bad message (should be rejected)
git commit --allow-empty -m "bad message"
# Should fail due to commitlint hook
```

**Release workflow test:**
If you can trigger a release:
1. Merge a PR with `feat:` or `fix:` commit
2. Watch GitHub Actions run
3. Verify:
   - Version bumped in package.json
   - CHANGELOG.md updated
   - GitHub Release created
   - Release notes populated (LLM synthesis ran)

**Public page test:**
- Navigate to `/changelog`
- Verify releases displayed
- Verify grouped by minor version
- Check RSS feed works

If any verification fails, go back and fix it.

## The Release Flow

```
Commit with conventional format (enforced by Lefthook)
       ↓
Push/merge to main
       ↓
GitHub Actions runs semantic-release
       ↓
Version bumped, CHANGELOG.md updated, GitHub Release created
       ↓
Post-release action triggers LLM synthesis
       ↓
LLM (via OpenRouter) transforms changelog → user notes
       ↓
Enhanced notes stored in GitHub Release
       ↓
Public /changelog page displays latest
```

## Key Principles

**Every merge is a release.** Web apps deploy on merge. Embrace frequent releases.

**Every change gets notes.** Even `chore:` commits become "Behind-the-scenes improvements."

**Group for readability.** Public page groups patches under their minor version.

**Auto-publish.** No human gate on LLM synthesis. Trust the pipeline.

## Default Stack

Assumes Next.js + TypeScript + GitHub. Adapts gracefully to other stacks.

## What You Get

When complete:
- semantic-release configured and working
- Conventional commits enforced (can't commit without format)
- GitHub Actions workflow for releases
- LLM synthesis for user-friendly notes (model via env var)
- Public `/changelog` page with RSS feed
- **Discoverable links** from footer and settings
- **Version displayed** in app settings
- Verified end-to-end

User can:
- Merge a PR with conventional commit
- See automatic version bump
- See GitHub Release created
- See user-friendly notes synthesized
- **Find changelog from footer or settings** (not hidden)
- **See what version they're running**
- Subscribe to RSS feed for updates
