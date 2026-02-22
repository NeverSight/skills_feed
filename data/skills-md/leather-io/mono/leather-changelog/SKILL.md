---
name: leather-changelog
description: Generate product changelog entries, X/Twitter posts, and Slack announcements for Leather wallet releases. Use when creating release communications including changelog entries for app.leather.io/changelog, announcement tweets (single or threads), and community Slack posts. Inputs may include verbal feature descriptions, Linear projects, or GitHub PRs.
---

# Leather Release Communications

Generate consistent, on-brand release communications for Leather wallet across changelog entries, X posts, and Slack announcements.

## Process

1. **Gather context** — Review provided feature description, Linear project, or GitHub PRs
2. **Identify the "why"** — Determine the user problem being solved or improvement being delivered
3. **Read format references** — See `references/voice-and-formats.md` for voice guidelines and templates
4. **Generate outputs** — Create requested formats (changelog, X post, Slack, or all three)

## Output Summary

| Format | Purpose | Length |
|--------|---------|--------|
| Changelog | Permanent product record at app.leather.io/changelog | 50-150 words |
| X single | Quick announcement for smaller features | 280 chars max |
| X thread | Major releases needing context | 3-5 tweets |
| Slack | Community announcement | 100-200 words |

## Voice Principles

- **Lead with impact** — Start with why this matters to users, not what changed technically
- **Understated confidence** — Let the product speak; avoid hype words ("excited", "thrilled", "game-changing")
- **One idea per sentence** — Short, declarative statements
- **Show don't tell** — Concrete benefits over abstract claims

See `references/voice-and-formats.md` for detailed guidelines and examples.

## Sanity CMS Integration

Use `scripts/sanity-changelog.js` to upload changelog entries to Sanity CMS as drafts.

### Setup

```bash
export SANITY_PROJECT_ID="your-project-id"
export SANITY_DATASET="production"  # optional, defaults to "production"
export SANITY_API_TOKEN="your-write-token"
```

### Usage

```bash
# Test upload without creating (dry run)
node scripts/sanity-changelog.js --title "Feature title" --body changelog.md --dry-run

# Create draft in Sanity
node scripts/sanity-changelog.js --title "Feature title" --body changelog.md

# With custom slug and publication date
node scripts/sanity-changelog.js \
  --title "Feature title" \
  --body changelog.md \
  --slug "custom-slug" \
  --published-at "2025-01-15T10:00:00Z"
```

### Markdown Support

The script converts markdown to Sanity Portable Text:
- Paragraphs (separated by blank lines)
- `## Headings` and `### Headings` → h2 blocks
- `**bold**`, `*italic*`, `` `code` `` inline formatting

### Options

| Option | Description |
|--------|-------------|
| `--title, -t` | Changelog entry title (required) |
| `--body, -b` | Path to markdown file (required) |
| `--slug, -s` | URL slug (auto-generated if not provided) |
| `--published-at` | ISO datetime (default: now) |
| `--hero-image` | Sanity asset ID for hero image |
| `--dry-run` | Test without creating document |
