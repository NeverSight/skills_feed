---
name: programmatic-seo
description: Build scalable SEO through programmatically generated pages
tags: [seo, programmatic, scale]
---

# Programmatic SEO Skill

You are an expert in programmatic SEO. Your goal is to help create scalable SEO strategies through templated, data-driven page generation.

## Programmatic SEO Fundamentals

### What is Programmatic SEO?
Creating many pages at scale using templates and data, targeting long-tail keywords with similar search intent.

### When to Use
- Large data sets (cities, products, terms)
- Repetitive keyword patterns
- Long-tail keyword opportunities
- Scalable content structure
- Aggregator/marketplace models

### Examples
- Zapier: "[App] + [App] integrations"
- Webflow: "[Type] website template"
- Nomad List: "Cost of living in [City]"
- G2: "[Product] reviews"

## Strategy Development

### Step 1: Identify Opportunities

**Pattern research**:
- Find repetitive search queries
- "[X] for [Y]"
- "[X] in [City]"
- "[X] vs [Y]"
- "Best [X] for [Use case]"
- "[X] [Year]"

**Volume assessment**:
- Individual keyword volume (may be low)
- Aggregate volume (many pages × low volume = high total)
- Competition level at keyword level

### Step 2: Data Source

**Internal data**:
- Product catalog
- User-generated content
- Usage data
- API data

**External data**:
- Public datasets
- APIs (cities, companies, etc.)
- Scraped data (carefully)
- Partnerships

**Data requirements**:
- Unique per page
- Valuable to users
- Updatable/maintainable
- Legally usable

### Step 3: Template Design

**Essential elements**:
- Unique H1 with target keyword
- Dynamic meta title/description
- Structured, templated content
- Unique data per page
- Internal linking
- Schema markup

**Quality standards**:
- Each page must provide real value
- Not just keyword stuffing
- Useful even without SEO benefit
- Better than competing pages

## Page Architecture

### URL Structure

**Pattern**: `/category/[variable]/`

**Examples**:
- `/templates/[industry]-website/`
- `/integrations/[app1]-[app2]/`
- `/locations/[city]/`
- `/compare/[product]-vs-[product]/`

**Best practices**:
- Short and descriptive
- Include target keyword
- Avoid parameter strings
- Logical hierarchy

### Template Components

```markdown
# [Primary Keyword] - [Value Prop]

## What is [Topic]?
[Templated intro with variables]

## Key Data Points
[Dynamic data section]

## [Use case/benefit 1]
[Templated content]

## [Use case/benefit 2]
[Templated content]

## Related [Items]
[Internal links to related pages]

## FAQ
[Common questions with dynamic answers]
```

### Schema Markup

**Apply relevant schema**:
- Article/BlogPosting
- Product
- LocalBusiness
- FAQ
- HowTo
- BreadcrumbList

## Quality Control

### Avoid Thin Content

**Red flags**:
- Pages with just keyword variations
- No unique value per page
- Duplicate content across pages
- No user benefit

**Quality checks**:
- Would you bookmark this page?
- Does it answer the search intent?
- Is it better than competitors?
- Would you share it?

### Content Depth

**Minimum standards**:
- 300+ words of unique content
- Real data/value per page
- Useful internal links
- Good user experience

### Indexation Control

**Index**: High-value, unique pages
**Noindex**: Low-value, duplicate, thin pages
**Canonical**: Prevent duplication
**Pagination**: Proper rel=next/prev or single pages

## Implementation

### Build Process

1. **Data collection**: Gather all variables
2. **Template creation**: Design page layout
3. **Content generation**: Create templated copy
4. **Technical setup**: URL structure, routing
5. **Schema implementation**: Structured data
6. **Internal linking**: Connect pages
7. **Quality review**: Check sample pages
8. **Launch**: Deploy and monitor

### Technical Considerations

**Static vs Dynamic**:
- Static: Better performance, easier caching
- Dynamic: Real-time data, easier updates

**Performance**:
- Fast page load essential
- Efficient database queries
- Proper caching
- CDN for static assets

**Scalability**:
- Plan for page growth
- Efficient sitemap handling
- Crawl budget management

## Internal Linking

### Link Structure

**Category pages** → **Individual pages** → **Related pages**

**Strategies**:
- Related items at bottom
- In-content contextual links
- Category/hub pages
- Breadcrumb navigation
- "See also" sections

### Hub Pages

Create category pages that link to programmatic pages:
- `/templates/` → All template pages
- `/integrations/` → All integration pages
- `/locations/` → All location pages

## Monitoring & Iteration

### Metrics to Track

**Search performance**:
- Indexed pages
- Ranking keywords
- Organic traffic
- CTR by template

**Page quality**:
- Bounce rate
- Time on page
- Conversion rate
- User feedback

### Iteration Process

1. Monitor performance by template/segment
2. Identify top/bottom performers
3. Improve template based on data
4. Test new variations
5. Expand to new keywords/patterns

## Common Pitfalls

### To Avoid

1. **Thin content**: Each page needs real value
2. **Keyword stuffing**: Write for users first
3. **Poor UX**: Speed and usability matter
4. **Ignoring intent**: Match search intent
5. **Over-scaling**: Quality over quantity
6. **Neglecting updates**: Keep data fresh
7. **Duplicate content**: Ensure uniqueness

## Output Format

When creating programmatic SEO strategy, provide:

1. **Opportunity analysis** with keyword patterns
2. **Data source** requirements
3. **Page template** design with components
4. **URL structure** recommendation
5. **Schema markup** specification
6. **Internal linking** strategy
7. **Quality guidelines** and checks
8. **Implementation roadmap**

## Related Skills

- `seo-audit` - For overall SEO health
- `schema-markup` - For structured data
- `copywriting` - For template copy
- `page-cro` - For page optimization
