---
name: changelog-setup
description: |
  Full changelog infrastructure from scratch. Greenfield workflow.
  Installs semantic-release, commitlint, GitHub Actions, LLM synthesis, public page.
---

# Changelog Setup

Complete changelog and release notes infrastructure for a project that doesn't have one.

## When to Use

Project has no release infrastructure. Starting fresh.

## Workflow

This workflow installs components in sequence:

### 1. Assess (confirm greenfield)

Run `changelog-assess` to confirm this is actually greenfield. If partial infrastructure exists, consider audit/reconcile instead.

### 2. Install Dependencies

```bash
pnpm add -D semantic-release \
  @semantic-release/changelog \
  @semantic-release/git \
  @semantic-release/github \
  @commitlint/cli \
  @commitlint/config-conventional
```

### 3. Configure semantic-release

Create `.releaserc.js`:

```javascript
// See references/semantic-release-config.md for full config
module.exports = {
  branches: ['main', 'master'],
  plugins: [
    '@semantic-release/commit-analyzer',
    '@semantic-release/release-notes-generator',
    ['@semantic-release/changelog', {
      changelogFile: 'CHANGELOG.md',
    }],
    '@semantic-release/npm', // or remove if not publishing to npm
    ['@semantic-release/git', {
      assets: ['CHANGELOG.md', 'package.json'],
      message: 'chore(release): ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}',
    }],
    '@semantic-release/github',
  ],
};
```

### 4. Configure commitlint

Create `commitlint.config.js`:

```javascript
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [2, 'always', [
      'feat', 'fix', 'docs', 'style', 'refactor',
      'perf', 'test', 'build', 'ci', 'chore', 'revert'
    ]],
    'subject-case': [2, 'always', 'lower-case'],
    'header-max-length': [2, 'always', 100],
  },
};
```

### 5. Add Lefthook Hook

Update `lefthook.yml` (create if doesn't exist):

```yaml
commit-msg:
  commands:
    commitlint:
      run: pnpm commitlint --edit {1}
```

Run `pnpm lefthook install` to activate.

### 6. Create GitHub Actions Workflow

Create `.github/workflows/release.yml`:

```yaml
# See references/github-actions-release.md for full workflow
name: Release

on:
  push:
    branches: [main, master]

permissions:
  contents: write
  issues: write
  pull-requests: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          persist-credentials: false

      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile
      - run: pnpm build

      - name: Release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
        run: pnpm semantic-release

  synthesize-notes:
    needs: release
    if: needs.release.outputs.new_release_published == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Synthesize Release Notes
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: |
          # See references/llm-synthesis.md for script
          node scripts/synthesize-release-notes.mjs
```

### 7. Configure LLM Synthesis

Create `.release-notes-config.yml`:

```yaml
# App-specific configuration for release notes synthesis
app_name: "Your App Name"
personality: "professional, friendly, confident"
audience: "non-technical users"

tone_examples:
  - "We made it faster to find what you need"
  - "Your dashboard now shows more detail"

avoid:
  - Technical jargon (API, SDK, webhook, etc.)
  - Git commit references
  - Internal code names
  - Version numbers in descriptions

categories:
  feat: "New Features"
  fix: "Improvements"
  perf: "Performance"
  chore: "Behind the Scenes"
  refactor: "Behind the Scenes"
  docs: "Documentation"
  test: "Quality"
```

Create `scripts/synthesize-release-notes.mjs`:
(See `references/llm-synthesis-script.md` for full implementation)

### 8. Scaffold Public Changelog Page

Run `changelog-page` to scaffold:
- `/app/changelog/page.tsx` - Main page component
- `/app/changelog.xml/route.ts` - RSS feed
- `/lib/github-releases.ts` - GitHub API client

### 9. Set Up Secrets

Required GitHub secrets:
- `GITHUB_TOKEN` - Automatically provided
- `GEMINI_API_KEY` - Get from Google AI Studio
- `NPM_TOKEN` - Only if publishing to npm

```bash
# Add Gemini API key to GitHub secrets
gh secret set GEMINI_API_KEY --body "your-api-key"
```

### 10. Verify

Run `changelog-verify` to confirm everything works:
- Commit with conventional format succeeds
- commitlint rejects bad commits
- Push to main triggers release workflow
- GitHub Release created
- LLM synthesis runs
- Public page displays notes

## Quality Gate

Do not consider setup complete until `changelog-verify` passes.

## Handoff

When complete, the project should have:
- semantic-release configured
- commitlint enforcing conventional commits
- Lefthook running commitlint on commit-msg
- GitHub Actions workflow for releases
- LLM synthesis for user-friendly notes
- Public changelog page at `/changelog`
- RSS feed at `/changelog.xml`

Developer workflow:
1. Write code
2. Commit with `feat:`, `fix:`, etc.
3. Push/merge to main
4. Everything else is automatic
