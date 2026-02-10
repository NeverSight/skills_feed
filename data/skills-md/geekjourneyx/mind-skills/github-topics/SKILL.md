---
name: github-topics
description: Fetches GitHub topic trending repositories. Use when asking about GitHub trending repos or open source projects.
---

# GitHub Topics Trending

Fetch GitHub topic trending repositories and README summaries.

## Quick Start

```
# View rankings
今天 claude-code 话题排行榜
Top 10 GitHub 项目
热门仓库

# View repository details
anthropics/claude-code 介绍
这个仓库是做什么的
```

## Query Types

| Type | Examples | Description |
|------|----------|-------------|
| Rankings | `热门仓库` `Top 10` | Current rankings by stars |
| Detail | `xxx/xxx 介绍` | Repository README summary |
| Topic | `python 话题排行榜` | Custom topic search |

## Workflow

```
- [ ] Step 1: Parse query type
- [ ] Step 2: Fetch data from GitHub
- [ ] Step 3: Format and display results
```

---

## Step 1: Parse Query Type

| User Input | Query Type | Action |
|------------|------------|--------|
| `热门仓库` | rankings | Show top N repos |
| `Top 10 项目` | rankings | Show top N repos |
| `xxx/xxx 介绍` | detail | Get README summary |
| `python 话题` | rankings | Search python topic |

---

## Step 2: Fetch Data

### Fetch Rankings

```bash
cd skills/github-topics
python src/github_fetcher.py
```

**Requirements**:
```bash
pip install requests
```

### Fetch README (Optional)

```bash
python src/readme_fetcher.py
```

---

## Step 3: Format Results

### Rankings Output

```markdown
# GitHub Trending - python

| # | Repository | Stars | Language |
|---|------------|-------|----------|
| 1 | donnemartin/system-design-primer | 334K | Python |
| 2 | vinta/awesome-python | 281K | Python |
| 3 | project-based-learning | 257K | - |
```

### Detail Output

```markdown
# anthropics/claude-code

**Stars**: 15.2K
**Language**: TypeScript
**URL**: https://github.com/anthropics/claude-code

## README Summary
Official Claude Code CLI for AI-powered software development. Claude Code is Anthropic's official CLI tool...
```

---

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `GH_TOKEN` | GitHub Personal Access Token (optional, for higher rate limits) | - |
| `TOPIC` | GitHub topic to track | `claude-code` |

**Note**: `GH_TOKEN` is optional but recommended:
- With token: 5,000 requests/hour
- Without token: 60 requests/hour

Create token at: https://github.com/settings/tokens

---

## GitHub API Notes

| Limit Type | Rate |
|------------|------|
| Authenticated | 5,000 requests/hour |
| Unauthenticated | 60 requests/hour |

**Recommendation**: Use `GH_TOKEN` for higher rate limits.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Rate limit | Set `GH_TOKEN` env var |
| Network timeout | Check internet connection |
| Empty results | Check topic name exists |

---

## CLI Reference

```bash
# Fetch rankings (default topic: claude-code)
python skills/github-topics/src/github_fetcher.py

# Fetch README
python skills/github-topics/src/readme_fetcher.py
```
