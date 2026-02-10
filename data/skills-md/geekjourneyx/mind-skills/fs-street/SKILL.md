---
name: fs-street
description: Fetches articles from Farnam Street RSS. Use when asking about decision-making, mental models, learning, or wisdom from Farnam Street blog.
---

# Farnam Street

Fetches articles from Farnam Street blog, covering topics like mental models, decision-making, leadership, and learning.

## Quick Start

```
# Basic queries
昨天的文章
今天的FS文章
2024-06-13的文章

# Search
有哪些可用的日期
```

## Query Types

| Type | Examples | Description |
|------|----------|-------------|
| Relative date | `昨天的文章` `今天的文章` `前天` | Yesterday, today, day before |
| Absolute date | `2024-06-13的文章` | YYYY-MM-DD format |
| Date range | `有哪些日期` `可用的日期` | Show available dates |
| Topic search | `关于决策的文章` `思维模型` | Search by keyword |

## Workflow

```
- [ ] Step 1: Parse date from user request
- [ ] Step 2: Fetch RSS data
- [ ] Check content availability
- [ ] Format and display results
```

---

## Step 1: Parse Date

| User Input | Target Date | Calculation |
|------------|-------------|-------------|
| `昨天` | Yesterday | today - 1 day |
| `前天` | Day before | today - 2 days |
| `今天` | Today | Current date |
| `2024-06-13` | 2024-06-13 | Direct parse |

**Format**: Always use `YYYY-MM-DD`

---

## Step 2: Fetch RSS

```bash
python skills/fs-street/scripts/fetch_blog.py --date YYYY-MM-DD
```

**Available commands**:

```bash
# Get specific date
python skills/fs-street/scripts/fetch_blog.py --date 2024-06-13

# Get date range
python skills/fs-street/scripts/fetch_blog.py --date-range

# Relative dates
python skills/fs-street/scripts/fetch_blog.py --relative yesterday
```

**Requirements**: `pip install feedparser requests`

---

## Step 3: Check Content

### When NOT Found

```markdown
Sorry, no article available for 2024-06-14

Available date range: 2023-04-19 ~ 2024-06-13

Suggestions:
- View 2024-06-13 article
- View 2024-06-12 article
```

### Members Only Content

Some articles are marked `[FS Members]` - these are premium content and may only show a teaser.

---

## Step 4: Format Results

**Example Output**:

```markdown
# Farnam Street · 2024年6月13日

> Experts vs. Imitators: How to tell the difference between real expertise and imitation

## Content

If you want the highest quality information, you have to speak to the best people. The problem is many people claim to be experts, who really aren't.

**Key Insights**:
- Imitators can't answer questions at a deeper level
- Experts can tell you all the ways they've failed
- Imitators don't know the limits of their expertise

---
Source: Farnam Street
URL: https://fs.blog/experts-vs-imitators/
```

---

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| RSS_URL | RSS feed URL | `https://fs.blog/feed/` |

No API keys required.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| RSS fetch fails | Check network connectivity |
| Invalid date | Use YYYY-MM-DD format |
| No content | Check available date range |
| Members only | Some articles are premium content |

---

## CLI Reference

```bash
# Get specific date
python skills/fs-street/scripts/fetch_blog.py --date 2024-06-13

# Get date range
python skills/fs-street/scripts/fetch_blog.py --date-range

# Relative dates
python skills/fs-street/scripts/fetch_blog.py --relative yesterday
```
