---
name: blog-writer
description: Create category-aware, AEO-optimized blog posts for Lightfast. Use when writing technology deep-dives, company announcements, or product launches.
allowed-tools: Read, Grep, Glob, Write, Edit
---

# Blog Writer

Create clear, accurate blog posts that help developers understand Lightfast capabilities and industry trends.

## Critical: Accuracy Over Marketing

Before writing anything:

1. **Verify every claim:**
   - If you cite a number, confirm the source
   - If you mention a feature, confirm it exists in production
   - When uncertain, ask for clarification

2. **Never oversell:**
   - Disclose limitations: "Currently supports X; Y coming in vZ"
   - Be honest about beta status and rollout timelines

3. **Match category voice:**
   - Technology: Technical authority, data-driven
   - Company: Visionary, category-defining
   - Product: Problem-solver, benefit-oriented

## Writing Guidelines

1. **Concise & scannable**: Match category word counts
2. **Lead with value**: Start with what readers gain
3. **Be transparent**: Mention beta status, limitations
4. **Active voice**: "You can now..." not "Users are able to..."
5. **No emoji**: Professional tone
6. **Include TL;DR**: 80-100 words for AI citation
7. **FAQ section**: 3-5 questions matching search queries
8. **Code examples**: Required for Technology posts

## Workflow

1. **Detect category** from input or ask if unclear
2. **Load category style** from `resources/categories/{category}.md`
3. **Research topic** using web-search-researcher agent
4. **Draft following** category template and [templates](resources/templates.md)
5. **Add AEO elements** per [aeo-requirements](resources/aeo-requirements.md)
6. **Review with** [checklist](resources/checklist.md)

## Quick Reference

### Category Selection
| Category | Use When | Audience |
|----------|----------|----------|
| Technology | Technical deep-dives, architecture, research | Developers, engineers |
| Company | Funding, partnerships, events, hiring | Executives, investors |
| Product | Feature launches, updates, tutorials | Customers, prospects |

### Do
- Include code examples (Technology)
- Use "shift from/to" narratives (Company)
- Lead with pain point (Product)
- Link to 3-5 related docs

### Don't
- Marketing buzzwords without substance
- Claims without verification
- Long paragraphs (keep sections scannable)
- Generic corporate speak

## Output

Save drafts to: `thoughts/blog/{slug}-{YYYYMMDD-HHMMSS}.md`

### Required Frontmatter Fields

Every draft MUST include:
- `title`, `slug`, `publishedAt`, `category` (core)
- `excerpt`, `tldr` (AEO)
- `seo.metaDescription`, `seo.focusKeyword` (SEO)
- `_internal.status`, `_internal.generated` (traceability)

See `resources/templates.md` for complete frontmatter template.

## Resources

- [Document Templates](resources/templates.md)
- [AEO Requirements](resources/aeo-requirements.md)
- [Pre-Publish Checklist](resources/checklist.md)
- [Technology Style Guide](resources/categories/technology.md)
- [Company Style Guide](resources/categories/company.md)
- [Product Style Guide](resources/categories/product.md)
