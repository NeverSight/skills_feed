---
name: announce
description: Draft social media posts (Twitter/X and LinkedIn) announcing a new release. Triggered by requests to announce a release, write a tweet about a version, or create social posts for a launch.
---

# Release Announcement Generator

Draft social media posts for Twitter/X and LinkedIn by analyzing what actually changed — not just parroting commit messages.

## Gathering Context

### Step 1: Determine what's being announced

```bash
# Get the most recent tag
CURRENT_TAG=$(git describe --tags --abbrev=0)
PREVIOUS_TAG=$(git describe --tags --abbrev=0 "$CURRENT_TAG^")

# Get the date of the previous tag for filtering PRs/issues
SINCE_DATE=$(git log -1 --format=%aI "$PREVIOUS_TAG")
```

### Step 2: Gather signals (in order of usefulness)

**PRs merged since last release:**
```bash
gh pr list --state merged --search "merged:>=$SINCE_DATE" --json number,title,body,labels --limit 100
```

**Issues closed since last release:**
```bash
gh issue list --state closed --search "closed:>=$SINCE_DATE" --json number,title,body,labels --limit 100
```

**Diff between tags:**
```bash
git diff "$PREVIOUS_TAG".."$CURRENT_TAG" -- '*.ts' '*.js' '*.tsx' '*.jsx' '*.py' '*.go' '*.rs' ':!*.lock' ':!*.min.*'
```

**Files changed (reveals scope):**
```bash
git diff --name-only "$PREVIOUS_TAG".."$CURRENT_TAG"
```

**New or changed test descriptions:**
```bash
git diff "$PREVIOUS_TAG".."$CURRENT_TAG" -- '**/*.test.*' '**/*.spec.*' '**/test_*' '**/*_test.*'
```

**Config and dependency changes:**
```bash
git diff "$PREVIOUS_TAG".."$CURRENT_TAG" -- 'package.json' '*.toml' '*.yaml' '*.yml' '*.env.example' '*.config.*'
```

**Commit messages (last resort):**
```bash
git log --oneline "$PREVIOUS_TAG".."$CURRENT_TAG"
```

### Step 3: Also check for existing release notes

```bash
# Check if there's a GitHub release with notes already
gh release view "$CURRENT_TAG" --json body --jq '.body' 2>/dev/null
```

If release notes already exist, use them as the primary source and supplement with the gathered context.

## Selecting What to Announce

Not everything in a release is announcement-worthy.

### Include
- Major new features users asked for (check closed issues)
- Significant performance improvements with real numbers
- Long-standing bug fixes that affected many users
- New integrations or platform support

### Skip
- Internal refactors
- Minor bug fixes
- Dependency updates
- CI/CD changes
- Test improvements

### Newsworthiness check
Ask: "Would a user of this product care enough to click through?" If no, skip it.

## Writing Rules

- Lead with the single most compelling change
- Write about benefits, not features: "Ship 3x faster" not "Add parallel build pipeline"
- Never mention file names, function names, or technical internals
- Use active voice
- Sound human — not like a corporate press release
- Include a link to the release or changelog if available
- Keep Twitter/X posts under 280 characters
- For LinkedIn, keep it to 3-5 short paragraphs max

## Output Format

Generate both formats:

### Twitter/X

```
ProjectName v2.4.0 is out!

Biggest addition: bulk CSV export for any report type — custom date ranges, filters, the works.

Also: keyboard shortcuts, faster search, and bug fixes.

→ https://github.com/org/repo/releases/tag/v2.4.0
```

### LinkedIn

```
ProjectName v2.4.0 just shipped with a feature our users have been asking for: bulk CSV export.

You can now export any report — including custom reports — to CSV with full control over date ranges and filters. No more copying data by hand.

We also added keyboard shortcuts for common actions, improved search performance for large workspaces, and fixed several bugs.

Check out the full release notes: https://github.com/org/repo/releases/tag/v2.4.0
```

## Example: Bad Commits → Good Announcement

**Typical commit messages:**
```
fix stuff
wip
update deps
john's changes
PR #89
```

**What the skill produces by analyzing PRs, issues, and diffs:**

### Twitter/X
```
ProjectName v3.0 just dropped 🚀

Real-time collaboration — edit documents with your team, see their cursors live.

Plus: Slack notifications for deploys and a bunch of bug fixes.

→ https://github.com/org/repo/releases/tag/v3.0.0
```

### LinkedIn
```
Excited to share ProjectName v3.0 — our biggest release this year.

The headline: real-time collaboration. You can now edit documents with your team simultaneously, with live cursors and instant syncing.

We also added Slack integration for deployment notifications, fixed duplicate search results, and resolved an issue with SSO password resets.

Full release notes: https://github.com/org/repo/releases/tag/v3.0.0
```

## Final Steps

- Present both Twitter/X and LinkedIn drafts
- Ask the user if they want to adjust tone, add hashtags, or mention specific accounts
- Offer to copy to clipboard
