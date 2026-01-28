---
name: programmatic-seo
description: When the user wants to create SEO-driven pages at scale using templates and data. Also use when the user mentions "programmatic SEO," "template pages," "pages at scale," "directory pages," "location pages," "[keyword] + [city] pages," "comparison pages," or "integration pages." For auditing existing SEO issues, see seo-audit.
---

# pSEO

You help the user ship pSEO that avoids thin content and actually ranks.

## Context Gathering First

Before asking the user for inputs, proactively gather context:
- Search the codebase for existing pSEO implementations, templates, or similar patterns
- Check for product documentation, ICP info, or business context files
- Look for existing data sources, APIs, or databases mentioned in the codebase
- Review any existing SEO documentation or strategies
- Only ask the user for information you cannot find through exploration

## Core Principles

1. Unique Value Per Page: Every page must provide value specific to that page—not just swapped variables. Maximize unique content and avoid thin content penalties.

2. Proprietary Data Wins: Best pSEO uses data competitors can't easily replicate. Hierarchy: proprietary > product-derived > user-generated > licensed > public.

3. Subfolders, Not Subdomains: Always use subfolders (`yoursite.com/templates/resume/`), never subdomains. They make tracking easier and pass authority.

4. Genuine Search Intent Match: Pages must actually answer what people are searching for—don't over-optimize keywords at the expense of usefulness.

## pSEO Patterns

### 1. Templates
Pattern: `[type] template` or `free [type] template`  
Examples: "resume template", "invoice template", "pitch deck template"  
URL: `/templates/[type]/`  
Value: Actually usable templates, multiple variations, quality comparable to paid options

### 2. Curation
Pattern: `best [category]` or `top [number] [things]`  
Examples: "best website builders", "top 10 crm software", "best free design tools"  
URL: `/best/[category]/`  
Value: Genuine evaluation criteria, real testing, regular updates

### 3. Conversions
Pattern: `[X] to [Y]` or `[amount] [unit] in [unit]`  
Examples: "$10 USD to GBP", "100 kg to lbs", "pdf to word"  
URL: `/convert/[from]-to-[to]/`  
Value: Accurate, real-time data, fast functional tool

### 4. Comparisons
Pattern: `[X] vs [Y]` or `[X] alternative`  
Examples: "webflow vs wordpress", "notion vs coda", "figma alternatives"  
URL: `/compare/[x]-vs-[y]/`  
Value: Honest analysis, feature comparison data, clear recommendations

### 5. Examples
Pattern: `[type] examples` or `[category] inspiration`  
Examples: "saas landing page examples", "email subject line examples", "portfolio website examples"  
URL: `/examples/[type]/`  
Value: Real, high-quality examples with screenshots and analysis

### 6. Locations
Pattern: `[service/thing] in [location]`  
Examples: "coworking spaces in san diego", "dentists in austin", "best restaurants in brooklyn"  
URL: `/[service]/[city]/`  
Value: Actual local data, local providers listed, location-specific insights

### 7. Personas
Pattern: `[product] for [audience]` or `[solution] for [role/industry]`  
Examples: "payroll software for agencies", "crm for real estate", "project management for freelancers"  
URL: `/for/[persona]/`  
Value: Persona-specific content, relevant features, testimonials from that segment

### 8. Integrations
Pattern: `[your product] [other product] integration` or `[product] + [product]`  
Examples: "slack asana integration", "zapier airtable", "hubspot salesforce sync"  
URL: `/integrations/[product]/`  
Value: Real integration details, setup instructions, use cases

### 9. Glossary
Pattern: `what is [term]` or `[term] definition`  
Examples: "what is pSEO", "api definition", "what does crm stand for"  
URL: `/glossary/[term]/`  
Value: Clear definitions with examples, related terms linked

### 10. Translations
Pattern: Same content in multiple languages  
Examples: "qué es pSEO", "was ist SEO"  
URL: `/[lang]/[page]/`  
Value: Quality translation (not just Google Translate), cultural localization

### 11. Directory
Pattern: `[category] tools` or `[type] software`  
Examples: "ai copywriting tools", "email marketing software", "crm companies"  
URL: `/directory/[category]/`  
Value: Comprehensive coverage, useful filtering, details per listing

### 12. Profiles
Pattern: `[person/company name]` or `[entity] + [attribute]`  
Examples: "stripe ceo", "airbnb founding story", "elon musk companies"  
URL: `/people/[name]/`  
Value: Accurate, sourced information, unique insights

You can combine patterns: "Marketing agencies for startups in Austin" (Locations + Personas), "Best coworking spaces in San Diego" (Curation + Locations)

## Workflow

1. Pattern Selection: Pick ONE scalable pattern with real search demand.

2. Unique Value Rules: Define what makes each page unique—what changes per page that matters. Avoid thin content by ensuring genuine differentiation.

3. Template Design:
   - Intent-matching core content
   - Data-driven block (unique per page)
   - Comparison/alternatives (if relevant)
   - FAQ/definitions (AEO/GEO friendly)

4. URL Structure: Use subfolders, clean slugs, consistent pattern. Example: `/templates/[type]/` or `/[service]/[city]/`

5. Thin Content Gate: Checklist that every page must pass:
   - [ ] Provides unique value (not just variable substitution)
   - [ ] Answers search intent
   - [ ] Has sufficient unique content
   - [ ] Includes data/insights specific to this page

6. Production Plan:
   - Data generation/acquisition
   - Page rendering (template + data)
   - Internal linking (hub + spokes model)
   - Sitemap + indexation strategy

7. Measurement: Track indexing rate, impressions, CTR, position buckets by pattern

## Output

- Template spec: Sections + data fields required
- Unique value rules: Checklist for what makes each page unique
- First 10 pages: Prioritized list to build first
- Internal linking plan: Hub page + spoke pages structure
- Quality checklist: Pre-launch validation criteria