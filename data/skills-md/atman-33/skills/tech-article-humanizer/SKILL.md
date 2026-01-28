---
name: tech-article-humanizer
description: Transform technical article drafts or source materials into human-like, high-quality Japanese technical articles. Use this skill when the user wants to generate, rewrite, or humanize technical articles (especially about TypeScript, JavaScript, React, or frontend topics) following specific human-writing patterns and style guidelines. Triggers include requests like "記事を人間風に", "tech article を生成", "humanize this article", or providing article source materials.
---

# Tech Article Humanizer

## Overview

This skill transforms technical article drafts into authentic, human-like Japanese technical articles that are indistinguishable from content written by experienced developers. It follows a comprehensive style guide that eliminates AI writing patterns and produces natural, engaging technical content.

## Workflow

### 1. Understand Source Material

Accept input in any of these formats:
- Markdown draft with rough structure
- Bullet points or outline
- Raw notes or technical concepts
- Existing article that needs humanization

Ask the user: **"Please provide the source material for the article (file path or content)"**

### 2. Load Style Guide

**CRITICAL**: Before generating any article content, read the complete style guide:

```
references/style-guide-human-tone.md
```

This guide contains:
- Forbidden patterns that must have ZERO violations
- Polite form (です/ます) distribution requirements
- Authenticity markers and human-like writing patterns
- Technical accuracy standards
- Pre-submission checklist

**Do NOT proceed without reading this guide completely.**

### 3. Generate Article

Follow the style guide strictly while generating content:

**Critical Requirements (Publication Blockers):**
- ZERO sentence-ending contracted forms (てる。てた。てます。)
- ZERO paragraph-initial "で、"
- ZERO colons (：) in prose before code/lists
- MINIMUM 15+ です/ます sentence endings
- TARGET 45-60% です/ます distribution
- Valid frontmatter (title, emoji, type, topics, published)

**Authenticity Markers (for 8.0+ quality):**
- Show code evolution (bug → fix, V1 → V2)
- Include 2-3 unresolved elements
- Add ecosystem context (GitHub refs, community mentions)
- Vary depth dramatically (15 para on favorite topic, 2 sentences on boring)
- Maximum 6-7 H2 sections

### 4. Save Output

Save the generated article to:

```
outputs/YYYYMMDD-{topic-slug}.md
```

Example: `outputs/20260110-typescript-const-parameters.md`

### 5. Validation (Optional)

Run validation script to check for forbidden patterns:

```bash
python scripts/validate_article.py outputs/YYYYMMDD-{topic-slug}.md
```

## Usage Examples

**Example 1: From bullet points**

User: "これを元に技術記事を作成してください"
```markdown
- TypeScript 5.0の新機能
- const type parametersについて
- 使い方と利点
```

Agent: [Loads style guide] → Generates full article → Saves to `outputs/20260110-typescript-const-parameters.md`

**Example 2: Humanize existing draft**

User: "この記事を人間風にリライトして" + provides draft.md

Agent: [Loads style guide] → Rewrites following human patterns → Saves to `outputs/20260110-rewritten-article.md`

**Example 3: With validation**

User: "記事を生成して、バリデーションもお願い"

Agent: [Generate article] → Saves output → Runs validation → Reports results


## Resources

### scripts/

- **validate_article.py**: Validates generated articles against forbidden patterns and style requirements

Usage:
```bash
python scripts/validate_article.py <article-path>
```

### references/

- **style-guide-human-tone.md**: Complete style guide for generating human-like Japanese technical articles. MUST be read before generating any content.
