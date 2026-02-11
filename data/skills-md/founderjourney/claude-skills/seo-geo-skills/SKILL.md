---
name: seo-geo-skills
description: Comprehensive SEO and GEO (Generative Engine Optimization) skills covering research, building, optimization, and monitoring phases. 16 specialized skills for search optimization.
original_source: https://github.com/aaron-he-zhu/seo-geo-claude-skills
author: aaron-he-zhu
license: Apache-2.0
---

# SEO & GEO Skills Collection

A comprehensive collection of Claude Skills for both traditional search engine optimization (SEO) and generative engine optimization (GEO), organized around a systematic methodology framework.

## When to Use This Skill

- Keyword research and discovery
- Competitor SEO analysis
- Content optimization for search
- Technical SEO audits
- Schema markup generation
- Rank tracking and monitoring
- Optimizing for AI search (GEO)

## Skills by Phase

### Research Phase (4 skills)

#### 1. Keyword Research
```
Research keywords for [topic/niche]
Include: search volume, difficulty, intent
```

#### 2. Competitor Analysis
```
Analyze SEO strategy of [competitor URL]
Show: top keywords, backlinks, content gaps
```

#### 3. SERP Analysis
```
Analyze SERP for [keyword]
Show: featured snippets, PAA, content patterns
```

#### 4. Content Gap Identification
```
Find content gaps between my site [URL] and competitors [URLs]
```

### Build Phase (4 skills)

#### 5. SEO Content Writing
```
Write SEO-optimized content for [keyword]
Target: [word count], include [LSI keywords]
```

#### 6. GEO Content Optimization
```
Optimize this content for AI search engines:
[paste content]
```

#### 7. Meta Tag Optimization
```
Generate optimized meta tags for:
Title: [page topic]
URL: [target URL]
```

#### 8. Schema Markup Generation
```
Generate schema markup for:
Type: [Article/Product/FAQ/HowTo/LocalBusiness]
Content: [details]
```

### Optimize Phase (4 skills)

#### 9. On-Page SEO Audit
```
Audit on-page SEO for [URL]
Check: title, meta, headings, content, images
```

#### 10. Technical SEO Check
```
Technical SEO audit for [domain]
Check: speed, mobile, indexing, crawlability
```

#### 11. Internal Linking Optimization
```
Suggest internal links for [URL]
Based on: site structure, topic clusters
```

#### 12. Content Refresh
```
Refresh this outdated content for current SEO:
[paste content]
Original date: [date]
```

### Monitor Phase (4 skills)

#### 13. Rank Tracking
```
Track rankings for:
Domain: [URL]
Keywords: [list]
```

#### 14. Backlink Analysis
```
Analyze backlink profile for [domain]
Show: authority, toxic links, opportunities
```

#### 15. Performance Reporting
```
Generate SEO performance report for [domain]
Period: [date range]
Metrics: traffic, rankings, conversions
```

#### 16. Alert Management
```
Set up SEO alerts for:
- Ranking drops > 5 positions
- Traffic drops > 20%
- New/lost backlinks
```

## GEO (Generative Engine Optimization)

### What is GEO?

GEO optimizes content for AI-powered search engines (ChatGPT, Perplexity, Claude) that synthesize answers rather than list links.

### GEO Best Practices

1. **Clear, Structured Answers**
   - Direct answers in first paragraph
   - Logical heading hierarchy
   - Bullet points for lists

2. **Authoritative Sources**
   - Cite credible sources
   - Include statistics and data
   - Reference experts

3. **Comprehensive Coverage**
   - Cover topic thoroughly
   - Answer related questions
   - Include FAQ sections

4. **Entity Optimization**
   - Clear entity definitions
   - Consistent naming
   - Structured data

### GEO Content Checklist

```markdown
[ ] Direct answer in first 100 words
[ ] H2/H3 structure for subtopics
[ ] Statistics with sources
[ ] Expert quotes
[ ] FAQ section
[ ] Schema markup
[ ] Internal links to related content
[ ] External links to authorities
```

## Quick Commands

```
# Research
/seo research keywords [topic]
/seo analyze competitor [URL]
/seo serp [keyword]

# Build
/seo write [keyword] [word count]
/seo meta [URL]
/seo schema [type]

# Optimize
/seo audit [URL]
/seo technical [domain]
/seo refresh [content]

# Monitor
/seo rank [domain] [keywords]
/seo backlinks [domain]
/seo report [domain]
```

## Output Formats

- **Keyword Research**: CSV with volume, difficulty, intent
- **Content**: Markdown with SEO annotations
- **Audits**: Prioritized issue list with fixes
- **Reports**: Executive summary + detailed metrics

## Integration

Works with:
- Google Search Console
- Google Analytics
- Ahrefs/SEMrush (manual data input)
- Screaming Frog exports

## Credits

Created by [aaron-he-zhu](https://github.com/aaron-he-zhu/seo-geo-claude-skills). Licensed under Apache 2.0.
