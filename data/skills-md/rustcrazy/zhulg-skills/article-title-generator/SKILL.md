---
name: article-title-generator
description: Generate engaging article titles for WeChat public accounts
version: 1.0.0
author: Claude
tags:
  - article
  - title
  - wechat
  - content
  - marketing
commands:
  - name: /article-title-generator
    description: Generate 10+ engaging article titles from text input or markdown files
    usage: /article-title-generator [content|file] [input]
    examples:
      - "/article-title-generator content 'Here is your article content about AI technology...'"
      - "/article-title-generator file /path/to/article.md"
---

# Article Title Generator

A Claude skill to generate engaging, attention-grabbing article titles specifically designed for WeChat public accounts.

## Features

- ✅ Support both text input and markdown file reading
- ✅ Generate 10+ compelling article titles
- ✅ Focus on WeChat-specific engagement styles
- ✅ Simple and easy to use
- ✅ No complex categorization required

## Usage

### Basic Usage

```bash
# Generate titles from text content
/article-title-generator content "Your article content here..."

# Generate titles from a markdown file
/article-title-generator file /path/to/article.md
```

### Command Options

- **content**: Direct text input for title generation
- **file**: Read from a markdown file for title generation

## How It Works

1. **Input Processing**: Accepts either raw text or markdown files
2. **Content Analysis**: Analyzes the main themes and key points
3. **Title Generation**: Creates 10+ engaging titles with WeChat-style hooks
4. **Output**: Returns a list of compelling, shareable titles

## Title Generation Focus

The skill generates titles that are:

- **Attention-grabbing**: Using curiosity gaps and emotional triggers
- **WeChat-optimized**: Short enough for WeChat's display format
- **Shareable**: Designed to increase click-through rates
- **Value-driven**: Highlighting benefits and solutions

## Requirements

- Claude Code with skill support
- No additional dependencies required

## Examples

Input content:
> "The future of artificial intelligence in business transformation"

Sample output titles:
1. "震惊！AI正在悄悄改变你的生意模式"
2. "老板必看：AI如何让你的企业效率翻倍"
3. "深度解析：AI时代的商业新机遇"
4. "为什么说不懂AI的企业正在被淘汰？"
5. "实战案例：AI驱动营收增长的秘诀"