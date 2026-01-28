---
name: gsc-analyzer
description: Strategic analysis of Google Search Console data for startup founders and marketing leaders. Transforms GSC exports into actionable growth insights with revenue impact estimates, competitive positioning, and prioritized action plans. Use when a user provides a GSC zip/CSV for (1) Brand vs non-brand analysis with revenue implications, (2) SEO opportunities with business impact sizing, (3) Content gap analysis with funnel mapping, (4) Paid search strategy with budget allocation, or (5) Strategic summaries with prioritized recommendations.
---

# Google Search Console Analyzer

Transform GSC data into strategic, revenue-focused insights for startup founders and marketing leaders.

## Workflow

1. Parse the GSC data (read CSV files or run parser for zip)
2. **Confirm brand terms** (use AskUserQuestion)
3. **Ask for business context** (conversion rate, ACV, goals)
4. Filter irrelevant/spam queries
5. Ask which analysis mode(s) to run
6. Execute analysis with revenue impact estimates
7. Generate strategic report with prioritized actions

## Business Context Collection

Before analysis, gather key inputs to size opportunities:

```
AskUserQuestion:
1. "What's your approximate trial/signup conversion rate from organic traffic?"
   - Options: <1%, 1-2%, 2-4%, 4%+, Not sure

2. "What's your average contract value (ACV)?"
   - Options: <$200/yr, $200-500/yr, $500-2000/yr, $2000+/yr, Enterprise pricing

3. "What's your primary goal for this analysis?"
   - Options: Growth planning, Competitive analysis, Quarterly prioritization, All of the above
```

## Brand Term Detection (Required)

**Read**: `references/brand_analysis.md` for methodology.

1. Auto-detect brand terms (exact name, domain, misspellings)
2. Use AskUserQuestion to confirm
3. Flag irrelevant/spam queries for exclusion

## Analysis Modes

### Mode 1: Brand vs. Non-Brand Analysis

**For**: Understanding marketing effectiveness and growth sustainability.

**Read**: `references/brand_analysis.md`

**Key outputs**:
- Brand dependency score (healthy: 20-40%)
- Traffic composition breakdown
- Trend analysis (is brand or non-brand growing?)
- Risk assessment if brand-heavy

### Mode 2: SEO Analyst

**For**: Finding quick wins and optimization opportunities.

**Read**: `references/seo_analysis.md`

**Key outputs**:
- Quick wins: Position 4-10, high volume (with revenue estimate)
- Striking distance: Position 11-20 keywords
- CTR optimization opportunities
- Cannibalization issues

### Mode 3: Content Strategist

**For**: Identifying content gaps and new opportunities.

**Read**: `references/content_opportunities.md`

**Key outputs**:
- Topic clusters without dedicated content
- Question-based content opportunities
- Comparison content gaps (vs competitors)
- International/multilingual opportunities

### Mode 4: Paid Search Specialist

**For**: Building Google Ads strategy from organic data.

**Read**: `references/paid_search.md`

**Key outputs**:
- High-intent keywords not ranking organically
- SERP domination opportunities
- Competitor conquesting targets
- Budget allocation recommendations

### Mode 5: Strategic Summary

**For**: Quarterly planning, team alignment, prioritization.

**Read**: `references/strategic_frameworks.md`

**Output format**:
```markdown
# [Company] Organic Search Performance - [Period]

## Headline Metrics (table)
## Key Risks (numbered, with business impact)
## Key Opportunities (numbered, with revenue estimates)
## Resource Requirements (specific asks)
## 90-Day Priorities (with owners)
```

## Strategic Frameworks

**Read**: `references/strategic_frameworks.md` for all frameworks.

### Revenue Impact Estimation
Size every opportunity in dollars:
```
Revenue = Traffic Gain × Conv Rate × Trial-to-Paid × ACV
```

### Funnel Stage Classification
| Stage | Keywords Contain | Priority |
|-------|------------------|----------|
| TOFU | "what is", "how to" | Content marketing |
| MOFU | "best", "vs", "comparison" | HIGH - conversion |
| BOFU | "pricing", "[brand]", "demo" | Highest intent |

### Share of Voice
Estimate competitive position from ranking data:
- Position 1 = 25-35% of clicks
- Position 2-3 = 8-18% of clicks
- Position 4-10 = 2-8% of clicks

### Anomaly Detection
Flag automatically:
- Traffic drops >20%
- CTR anomalies (high impressions, low clicks)
- Position changes on key terms

## Quick Reference

### Intent Classification
| Signal Words | Intent | Best For |
|-------------|--------|----------|
| buy, price, demo, trial | High (transactional) | Paid Search |
| best, vs, compare, review | Medium-High (MOFU) | SEO + PPC |
| how to, guide, what is | Medium (TOFU) | Content |
| [brand], login | Navigational | Brand defense |

### Healthy Benchmarks
| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| Brand % of traffic | 20-40% | 40-60% | >60% |
| Non-brand CTR | 5-15% | 2-5% | <2% |
| Avg non-brand position | <5 | 5-10 | >10 |

## Example Outputs

- "Analyze this GSC data" → Full analysis with strategic summary
- "How much revenue are we leaving on the table?" → Revenue impact mode
- "Give me the TL;DR on our SEO performance" → Strategic summary
- "What should we focus on this quarter?" → Prioritized recommendations
