---
name: publish-to-marketplaces
description: Publish and update agent skills on agentskill.sh and skills.sh marketplaces. Covers SKILL.md preparation, submission, verification, and ongoing sync. Use when the user mentions publishing skills, listing on marketplace, updating skill listings, or asks about agentskill.sh or skills.sh.
---

# Publish Skills to Marketplaces

Guide for listing agent skills on **agentskill.sh** and **skills.sh** — the two largest skill directories.

## Platform Comparison

| | agentskill.sh | skills.sh |
|--|---------------|-----------|
| Scale | 47,000+ skills | 33,500+ skills |
| Backed by | Yuki Capital | Vercel Labs |
| Install cmd | `/learn @owner/repo` | `npx skills add owner/repo` |
| Submit method | Web form (Analyze & Import) | CLI telemetry on first install |
| Auto-sync | Yes (pulls from GitHub) | Partial (telemetry-driven cache) |
| Ranking | Quality score + installs | Anonymous install telemetry |

## Prerequisites

Before publishing, ensure:

1. **GitHub repo is public** with a valid `SKILL.md` at a discoverable path (root or `.cursor/skills/<name>/`)
2. **SKILL.md has proper frontmatter:**

```yaml
---
name: your-skill-name          # lowercase, hyphens, max 64 chars
description: >-                 # English, max 1024 chars
  What it does and when to use it.
license: MIT
compatibility: Requirements and supported agents.
metadata:
  author: github-username
  version: "1.0"
  tags: tag1 tag2 tag3
---
```

3. **Description is in English** — both platforms have international audiences
4. **Body content is in English** — skills.sh renders the full SKILL.md as the listing page

## Step 1: Publish to agentskill.sh

### First-time submission

1. Navigate to `https://agentskill.sh/submit`
2. Paste the GitHub repo URL (e.g. `https://github.com/owner/repo`)
3. Click **Analyze & Import** — wait for security scan to complete
4. Verify the result card shows the correct skill name and description

### Verify listing

Search at `https://agentskill.sh/q/<skill-name>` and confirm:
- Skill name matches `name` field in frontmatter
- Description matches `description` field
- Security score is displayed (aim for 100/100)

Detail page lives at: `https://agentskill.sh/@owner/skill-name`

### Install command for users

```
/learn @owner/skill-name
```

## Step 2: Publish to skills.sh

### First-time submission

skills.sh has no web submission form. Listing is triggered by the first install:

```bash
npx skills add owner/repo --yes
```

The `--yes` flag skips interactive prompts. This command:
- Clones the repo
- Detects all SKILL.md files
- Installs to all compatible agent directories
- Sends anonymous telemetry to skills.sh (registers the skill)

### Verify listing

Check `https://skills.sh/owner/repo/skill-name` — the page renders the full SKILL.md content.

### Install command for users

```bash
npx skills add owner/repo
```

Or install a specific skill from a multi-skill repo:

```bash
npx skills add owner/repo --skill skill-name
```

## Step 3: Update Listings After Changes

When you modify SKILL.md and push to GitHub:

| Platform | Update mechanism | Action needed |
|----------|-----------------|---------------|
| agentskill.sh | Auto-sync from GitHub | Re-submit at `/submit` for immediate refresh, or wait for auto-sync |
| skills.sh | Telemetry on next install | Run `npx skills add owner/repo --yes` in a temp dir to trigger |

### Quick update script

```bash
# 1. Push changes to GitHub
git add -A && git commit -m "update skill listing" && git push

# 2. Re-submit to agentskill.sh (browser)
# Navigate to https://agentskill.sh/submit → paste repo URL → Analyze & Import

# 3. Trigger skills.sh refresh
TMPDIR=$(mktemp -d)
cd "$TMPDIR"
npx skills add owner/repo --yes
rm -rf "$TMPDIR"
```

## Troubleshooting

### skills.sh shows stale content

skills.sh caches content from telemetry data. After a rename or major update:
- Run a fresh install via `npx skills add` to send new telemetry
- Allow 12–24 hours for the platform to aggregate and refresh
- If still stale after 48h, contact the platform

### skills.sh shows old skill name

The skill name is cached from the first telemetry report. A rename requires:
1. Push the updated SKILL.md with the new `name` field
2. Run `npx skills add owner/repo --yes` to send fresh telemetry
3. Wait for platform cache refresh (may take 24–48h)

### agentskill.sh not showing updates

Re-submit at `https://agentskill.sh/submit` with the same repo URL. This forces a fresh fetch from GitHub.

### Security score issues

- **Socket alert**: Usually minor dependency concerns — review and assess
- **Snyk warning**: Check for known vulnerabilities in scripts
- **Gen Agent Trust Hub**: Automated content safety check — ensure no harmful patterns

## Checklist

```
Publishing Checklist:
- [ ] SKILL.md has valid YAML frontmatter (name, description)
- [ ] Description is in English, specific, includes trigger terms
- [ ] Body content is in English for international visibility
- [ ] GitHub repo is public
- [ ] Submitted to agentskill.sh via /submit
- [ ] Verified agentskill.sh listing and security score
- [ ] Triggered skills.sh listing via npx skills add
- [ ] Verified skills.sh detail page
- [ ] Updated README with install commands for both platforms
```
