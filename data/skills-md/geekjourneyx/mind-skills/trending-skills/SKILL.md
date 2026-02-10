---
name: trending-skills
description: Fetches skills.sh trending rankings. Use when asking about skill rankings or popular tools.
---

# Trending Skills

Fetch skills.sh trending rankings and skill details.

## Quick Start

```
# View rankings
今天技能排行榜
Top 10 skills
技能榜单
```

## Query Types

| Type | Examples | Description |
|------|----------|-------------|
| Rankings | `今天技能排行榜` `Top 10` | Current rankings |
| Detail | `xxx是什么` `xxx介绍` | Skill details (requires extra packages) |

## Workflow

```
- [ ] Step 1: Parse query type
- [ ] Step 2: Fetch data from skills.sh
- [ ] Step 3: Format and display results
```

---

## Step 1: Parse Query Type

| User Input | Query Type | Action |
|------------|------------|--------|
| `今天技能排行榜` | rankings | Show top N skills |
| `Top 10 skills` | rankings | Show top N skills |
| `xxx是什么` | detail | Show skill details |

---

## Step 2: Fetch Data

### Fetch Rankings

```bash
cd skills/trending-skills
python src/skills_fetcher.py
```

**Requirements**:

For basic rankings:
```bash
pip install playwright
playwright install chromium --with-deps
```

For skill details (optional):
```bash
pip install beautifulsoup4 lxml requests
```

**Note**: `--with-deps` automatically installs required system libraries.

### Fetch Skill Details (Optional)

```bash
python src/detail_fetcher.py <skill-name>
```

---

## Step 3: Format Results

### Rankings Output

```markdown
# Skills Trending

| # | Skill | Owner | Installs |
|---|-------|-------|----------|
| 1 | remotion-best-practices | remotion-dev | 5.6K |
| 2 | react-best-practices | vercel-labs | 5.4K |
| 3 | web-design-guidelines | vercel-labs | 4.0K |
```

### Detail Output (Optional)

```markdown
# remotion-best-practices

**Owner**: remotion-dev/skills
**Installs**: 5.6K

**When to use**:
[Usage description from skills.sh]

**Rules** (27 total):
- 3d.md: 3D content in Remotion...
- audio.md: Audio processing...

**URL**: https://skills.sh/remotion-dev/remotion-best-practices
```

---

## Configuration

No configuration required.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Playwright error | Run `playwright install chromium` |
| Network timeout | Check internet connection |
| Skill not found | Verify skill name on skills.sh |

---

## CLI Reference

```bash
# Fetch rankings
python skills/trending-skills/src/skills_fetcher.py

# Fetch skill detail (optional)
python skills/trending-skills/src/detail_fetcher.py <skill-name>
```
