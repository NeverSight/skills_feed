---
name: tech-article-polished-writer
description: Generate clear, professional, and polished Japanese technical articles suitable for corporate blogs, official documentation, and technical publications. Use this skill when the user wants to create enterprise-level content with consistent polite tone (です/ます), logical structure, and authoritative voice. Triggers include requests like "polished article", "professional tone", "enterprise blog", "公式ドキュメント", "プロフェッショナルな記事", or when content needs formal technical writing.
---

# Tech Article Polished Writer

## Overview

This skill generates clear, professional, and polished Japanese technical articles suitable for enterprise environments, corporate blogs, official documentation, and formal technical publications. It maintains a consistent, authoritative tone with logical structure and professional vocabulary.

## When to Use This Skill

### Use Polished Writer for:
- **Corporate blogs** and company technical articles
- **Official documentation** and technical guides
- **Tutorial content** for products or services
- **Enterprise-level** technical content
- **Formal publications** requiring professional tone
- Content needing **consistent polite form** (です/ます)

### Use Human Tone Writer instead for:
- Personal blogs (Zenn, Qiita, personal sites)
- Casual technical articles with personality
- Content that benefits from conversational style
- Articles targeting individual developers

## Workflow

### 1. Understand Source Material

Accept input in any of these formats:
- Markdown draft with technical content
- Bullet points or structured outline
- Raw technical notes or concepts
- Existing article that needs professionalization

Ask the user: **"Please provide the source material for the article (file path or content)"**

### 2. Load Style Guide

**CRITICAL**: Before generating any article content, read the complete style guide:

```
references/style-guide-polished-tone.md
```

This guide contains:
- Forbidden patterns (casual expressions, AI-isms, unprofessional language)
- Consistent polite tone requirements (です/ます)
- Professional vocabulary standards
- Logical structure guidelines
- Code explanation best practices

**Do NOT proceed without reading this guide completely.**

### 3. Generate Article

Follow the style guide strictly while generating content:

**Critical Requirements (Publication Blockers):**
- ZERO casual/slang endings (〜だね。〜じゃん。contracted forms)
- ZERO unprofessional connectors (で、なんか、ぶっちゃけ)
- ZERO AI-isms (robotic repetition, excessive また/さらに)
- ZERO colons (：) in prose before code/lists
- CONSISTENT polite form (です/ます) throughout main text (target: 90%+)
- Valid frontmatter (title, emoji, type, topics, published)

**Professional Quality Standards:**
- Clear, logical structure with proper headings (H2, H3)
- Introduction states problem and solution clearly
- Conclusion summarizes key points effectively
- Professional vocabulary and standard terminology
- Code explanations include "why" and "how"
- Active voice preference for clarity

### 4. Save Output

Save the generated article to:

```
outputs/YYYYMMDD-{topic-slug}.md
```

Example: `outputs/20260110-typescript-advanced-types.md`

### 5. Validation (Optional)

Run validation script to check for forbidden patterns and polite form consistency:

```bash
python scripts/validate_article.py outputs/YYYYMMDD-{topic-slug}.md
```

## Usage Examples

**Example 1: Corporate blog post**

User: "この技術資料を企業ブログ向けの記事にして"
```markdown
- React 19の新機能紹介
- Server Componentsの利点
- 移行ガイド
```

Agent: [Loads style guide] → Generates professional article → Saves to `outputs/20260110-react-19-server-components.md`

**Example 2: Official documentation**

User: "公式ドキュメント用にpolishedトーンで記事作成"

Agent: [Loads style guide] → Creates formal technical guide → Saves with professional tone

**Example 3: Professionalize existing content**

User: "このカジュアルな記事をプロフェッショナルに書き直して" + provides draft.md

Agent: [Loads style guide] → Rewrites with polished tone → Saves to `outputs/20260110-polished-article.md`


## Resources

### scripts/

- **validate_article.py**: Validates generated articles against polished tone requirements, forbidden patterns, and professional standards

Usage:
```bash
python scripts/validate_article.py <article-path>
```

### references/

- **style-guide-polished-tone.md**: Complete style guide for generating professional, polished Japanese technical articles. MUST be read before generating any content.
