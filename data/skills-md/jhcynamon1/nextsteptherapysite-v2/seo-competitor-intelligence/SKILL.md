---
name: seo-competitor-intelligence
description: Reverse-engineer top-ranking competitor pages to identify content gaps and create "beat the competition" briefs. Analyzes content structure, schema markup, E-E-A-T signals, local SEO, and generates actionable outlines. Use when user mentions "competitor analysis", provides competitor URLs, asks "why am I not ranking", or requests content gap analysis for therapy/healthcare keywords.
---

# SEO Competitor Intelligence Skill

## Purpose
Analyze 3-5 competitor pages to reverse-engineer their SEO success and generate actionable "beat the competition" briefs for therapy content.

## When to Use
- User provides competitor URLs
- User asks "why are they outranking me?"
- User mentions "competitor analysis" or "content gap"
- User wants to understand ranking factors for a keyword

## Quick Start Workflow

### Step 1: Input Collection
```
Target keyword: [e.g., "anxiety therapy ontario"]
Competitor URLs: [3-5 top-ranking URLs]
Your page URL: [optional - for comparison]
NextStep differentiators: CRPO #10979, ACT specialty, same-week availability
```

### Step 2: Fetch Competitor Pages
Use WebFetch to retrieve each competitor page content.

### Step 3: Content Structure Analysis
For each competitor, extract:
- **H1 title**
- **All H2/H3 headings** (topic structure)
- **Word count**
- **Number of paragraphs, lists, tables**
- **Internal/external links count**
- **Images/media count**

### Step 4: Schema Markup Detection
Scan for schema types:
- MedicalWebPage
- LocalBusiness
- FAQPage
- Organization
- BreadcrumbList

Note format (JSON-LD preferred) and completeness.

### Step 5: E-E-A-T Signal Detection
Check for YMYL compliance signals:
- [ ] Author name + credentials visible
- [ ] Last updated date
- [ ] Professional license/registration mentioned
- [ ] Citations to authoritative sources (CRPO, CMHA, research)
- [ ] Privacy policy link
- [ ] Contact information
- [ ] About page linked
- [ ] Testimonials (note: prohibited for CRPO members)

### Step 6: Local SEO Signals (Ontario)
- Ontario city mentions
- CRPO/provincial regulatory info
- OHIP coverage details
- Insurance provider specifics
- Local Business schema with Ontario address

### Step 7: Topic Cluster Mapping
1. Extract all H2/H3 headings from competitors
2. Group by semantic similarity
3. Identify patterns:
   - **Core topics** (covered by 4-5 competitors)
   - **Secondary topics** (covered by 2-3 competitors)
   - **Gap topics** (covered by 0-1 competitors)

### Step 8: Generate "Beat the Competition" Brief

## Output Format

```
# Competitor Analysis: [Keyword]
Date: [Today's date]

## Competitor Benchmarks

| Metric | Comp 1 | Comp 2 | Comp 3 | Average | Recommended |
|--------|--------|--------|--------|---------|-------------|
| Word Count | 2,400 | 1,800 | 2,200 | 2,133 | 2,500+ |
| H2 Sections | 8 | 6 | 7 | 7 | 9 |
| FAQs | 10 | 8 | 0 | 6 | 12 |
| Schema Types | 3 | 2 | 1 | 2 | 4 |
| Citations | 5 | 3 | 2 | 3.3 | 6+ |
| Last Updated | 2024 | 2023 | 2022 | - | 2024 |

## E-E-A-T Gap Analysis

### What Competitors Have:
- Author credentials visible: 2/3
- Last updated dates: 2/3
- External citations: 2/3
- FAQPage schema: 1/3

### NextStep Advantages:
✅ Specific CRPO license number (#10979) - more credible than generic "registered"
✅ ACT specialization - unique differentiator
✅ Same-week availability - mentioned by 0/3 competitors
✅ Virtual-first across Ontario - broader than competitors' city-specific focus

## Content Structure Recommendation

### Outline to Beat Competitors

**H1:** [Keyword] | Same-Week Sessions | NextStep Therapy

**Introduction (200 words)**
- Hook addressing pain point
- CRPO #10979 credential display
- Value proposition highlighting same-week availability

**H2: Core Topic 1** (covered by all competitors)
[300 words - must include to compete]

**H2: Core Topic 2** (covered by all competitors)
[300 words - must include to compete]

**H2: GAP OPPORTUNITY - [Unique angle]**
[400 words - THIS BEATS COMPETITORS]
Insight: None of the competitors cover [X]. This is your competitive advantage.

**H2: Secondary Topic** (covered by 2/3 competitors)
[250 words - good to include]

**H2: ACT Therapy for [Condition]** (UNIQUE to NextStep)
[350 words - leverages your specialization]

**H2: FAQ Section** (12 questions - more than competitors)
[600 words total]

**H2: How to Book** (CTA section)
[150 words]

**Target Word Count:** 2,500-2,800 words

## Schema Markup to Add

```json
{
  "@context": "https://schema.org",
  "@type": "MedicalWebPage",
  "name": "[Page Title]",
  "author": {
    "@type": "Person",
    "name": "Jesse Cynamon",
    "jobTitle": "Registered Psychotherapist",
    "credential": "RP #10979 (CRPO)"
  },
  "dateModified": "2024-12-09",
  "reviewedBy": {
    "@type": "Person",
    "name": "Jesse Cynamon",
    "credential": "CRPO #10979"
  }
}
```

**Plus:** FAQPage schema (competitors have weak/no FAQ schema)

## Internal Linking Opportunities
- Link to 3-5 related NextStep pages
- Anchor text variations of target keyword
- Deep link to student-specific or professional pages if relevant

## Content Gaps Identified

1. **Gap #1:** [Topic competitors missed]
   - Why it matters: [SEO/user value]
   - How to capitalize: [Content approach]

2. **Gap #2:** [Weak competitor coverage]
   - Current coverage: Shallow (100-150 words)
   - Opportunity: Deep dive (400+ words)

## Estimated Impact

**Current Position:** [Your current ranking]
**Competitor Positions:** #1, #3, #5
**With This Brief:** Potential to reach top 3 within 60-90 days

**Why:**
- Word count 15-20% higher than average
- Superior E-E-A-T signals (CRPO #10979, ACT specialization)
- Content gaps filled
- Better schema markup
- Unique differentiators highlighted

## Next Steps

1. Write content following this outline
2. Implement recommended schema markup
3. Add internal links
4. Set last updated date to current month
5. Submit to Google Search Console
6. Monitor rankings for 30 days
7. Iterate based on performance

## CRPO Compliance Note

**What Competitors Do (That You CANNOT):**
- Testimonials/reviews in content ❌
- "Best therapist" claims ❌
- Outcome guarantees ❌

**Your Compliant Advantages:**
- Specific license number (factual) ✅
- Same-week availability (factual) ✅
- ACT specialization (provable) ✅
- Evidence-based approach (supported by research) ✅
```

## Advanced Analysis

### Competitor Weakness Detection

```python
# Pattern: Identify weak E-E-A-T signals
- No author credentials: -20 E-E-A-T score
- No last updated date: -15 E-E-A-T score
- No citations: -25 E-E-A-T score
- Outdated content (2+ years): -30 freshness score

# Opportunity: Your page can rank higher with superior E-E-A-T
```

### Seasonal Opportunity Detection

Check competitors for:
- Seasonal content gaps (e.g., "January blues", "back to school anxiety")
- Holiday-specific pages
- Academic calendar alignment (for student pages)

## Scripts

### analyze_structure.py
Extracts headings, word count, content elements.

### analyze_schema.py
Detects and validates schema markup.

### analyze_eeat.py
Scores E-E-A-T signals (0-100).

### generate_brief.py
Compiles all analyses into actionable brief.

## Research Sources

**Content Gap Analysis:**
- [SEO Evolution 2024 Content Gap Analysis](https://www.allianzegcc.com/seo-evolution-2024-content-gap-analysis-in-6-steps/)
- [How to Conduct SEO Competitor Analysis (Backlinko)](https://backlinko.com/seo-competitor-analysis)
- [Content Gap Analysis Complete Guide](https://backlinko.com/hub/seo/content-gap)

**YMYL E-E-A-T:**
- [Healthcare Content and E-E-A-T](https://healthcaresuccess.com/blog/healthcare-marketing/google-e-a-t-and-healthcare-content-how-to-deliver-the-quality-google-demands.html)
- [YMYL Pages SEO Guide](https://ignitevisibility.com/ymyl-pages-what-are-ymyl-google-seo-pages/)

## Error Handling

**If competitor URLs are inaccessible:**
"I cannot access [URL]. This may be due to robots.txt restrictions or paywalls. Please provide the page content directly or try an alternative competitor."

**If no clear content gaps:**
"All competitors cover similar topics comprehensively. Your competitive advantage will come from superior E-E-A-T signals (CRPO #10979, ACT specialization) and better user experience (same-week availability, clear CTAs)."
