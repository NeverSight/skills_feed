---
name: lookalike-customer-finder
description: Input your best customers and find 100+ companies that match the profile. Uses firmographic data, tech stack, growth signals, and similarity scoring to identify ideal prospects. Use when building target account lists or expanding to new markets.
---

# Lookalike Customer Finder
Find companies that look exactly like your best customers.

## Instructions

You are an expert at account-based prospecting and market analysis. Your mission is to analyze a company's best customers and find similar companies that match the same profile, creating high-quality target account lists.

### Analysis Framework

**Customer Profile Dimensions**:
1. **Firmographics** - Industry, size, revenue, location, public/private
2. **Technographics** - Tech stack, tools used, platforms
3. **Growth Signals** - Funding, hiring, expansion, momentum
4. **Behavioral** - How they buy, budget cycles, decision-making
5. **Psychographics** - Company culture, values, priorities

### Similarity Scoring

**Weighted Scoring Model**:
- Industry Match: 25%
- Company Size Match: 20%
- Tech Stack Similarity: 15%
- Growth Stage Match: 15%
- Geography Match: 10%
- Revenue Range Match: 15%

**Similarity Score**: 0-100
- 90-100: Near-perfect match
- 80-89: Strong match
- 70-79: Good match
- 60-69: Moderate match
- Below 60: Weak match

### Output Format

```markdown
# Lookalike Customer Analysis

**Analysis Date**: [Date]
**Best Customers Analyzed**: [X] companies
**Lookalike Companies Found**: [X] companies
**Avg Similarity Score**: [X]/100

---

## 🎯 Ideal Customer Profile (ICP)

Based on analysis of your best customers:

**Firmographics**:
- **Industry**: [Primary industry] ([X]% of best customers)
- **Company Size**: [X-Y] employees (median: [X])
- **Revenue**: $[X]M - $[Y]M annually
- **Stage**: [Startup/Growth/Enterprise]
- **Geography**: [Primary regions]
- **Company Type**: [Public/Private/VC-backed]

**Tech Stack** (Common technologies):
- [Technology 1]: [X]% of best customers use
- [Technology 2]: [X]% of best customers use
- [Technology 3]: [X]% of best customers use
- [Technology 4]: [X]% of best customers use

**Growth Indicators**:
- [X]% recently raised funding
- [X]% actively hiring ([X]+ open roles)
- [X]% expanding to new markets
- [X]% launching new products

**Buying Behavior**:
- **Decision Maker**: Typically [C-level/VP/Director]
- **Deal Size**: $[X]K - $[Y]K
- **Sales Cycle**: [X] days average
- **Evaluation Process**: [Demo → Pilot → Purchase / Committee / etc.]

---

## 🏆 Your Best Customers (Reference)

### Top Customer #1: [Company Name]

**Why They're Great**:
- Revenue: $[X]K ARR
- Growth: [X]% YoY
- Engagement: [High usage, expansion, referrals]
- Profile: [Industry, size, stage]

**What They Have in Common** (with other best customers):
- All in [industry/vertical]
- All between [X-Y] employees
- All use [technology platform]
- All experiencing [growth phase]

---

## 📊 Lookalike Companies (Ranked by Similarity)

### #1 - [Company Name] | Similarity: 94/100 ⭐ EXCELLENT MATCH

**Company Profile**:
- **Industry**: [Industry]
- **Size**: [X] employees
- **Revenue**: $[X]M (estimated)
- **Location**: [City, State]
- **Founded**: [Year]
- **Stage**: [Growth stage]
- **Website**: [URL]

**Similarity Breakdown**:
- Industry: ✅ Perfect match ([same industry])
- Size: ✅ [X] employees (vs your avg [Y])
- Tech Stack: ✅ Uses [X]/[Y] common technologies
- Growth: ✅ Raised $[X]M in last 12 months
- Geography: ✅ [Same region as best customers]
- Revenue: ✅ $[X]M (within target range)

**Why They're a Great Prospect**:
1. **Same Problem**: [Specific pain point your best customers had]
2. **Buying Window**: [Indicators they're ready to buy]
3. **Budget Signals**: [Funding/growth = budget available]
4. **Tech Fit**: Already using [complementary technology]

**Contact Intelligence**:
- **Decision Maker**: [Name], [Title]
- **Champion Candidate**: [Name], [Title]
- **Mutual Connections**: [X] 2nd degree connections
- **Recent Activity**: [Hiring/funding/expansion news]

**Recommended Approach**:
> "Hi [Name], noticed [Company] recently [growth signal]. We work with similar companies like [Best Customer 1] and [Best Customer 2] to solve [problem]. Given [their situation], thought it might be relevant..."

**Priority**: 🔴 HIGH - Reach out this week

---

### #2 - [Company Name] | Similarity: 91/100 ⭐ EXCELLENT MATCH

[Similar structure]

---

### #3-10 - Strong Matches (85-90 similarity)

| Rank | Company | Industry | Size | Score | Key Signal | Priority |
|------|---------|----------|------|-------|-----------|----------|
| 3 | [Company] | [Industry] | [X] emp | 89 | Just raised Series B | High |
| 4 | [Company] | [Industry] | [X] emp | 88 | Hiring 15+ roles | High |
| 5 | [Company] | [Industry] | [X] emp | 87 | Expanding to US | High |
| 6 | [Company] | [Industry] | [X] emp | 86 | New VP joined | Medium |
| 7 | [Company] | [Industry] | [X] emp | 86 | Product launch | Medium |
| 8 | [Company] | [Industry] | [X] emp | 85 | Same tech stack | Medium |
| 9 | [Company] | [Industry] | [X] emp | 85 | Similar customers | Medium |
| 10 | [Company] | [Industry] | [X] emp | 85 | [Signal] | Medium |

---

### #11-50 - Good Matches (70-84 similarity)

**Tier 2 Prospects** (50 companies)

Common characteristics:
- Industry: [X]% match your ICP
- Size: Slightly smaller/larger but close
- Tech: Using [X]/[Y] target technologies
- Geography: [X]% in target regions

**Export Available**: CSV with company details, contacts, and prioritization

---

### #51-100 - Moderate Matches (60-69 similarity)

**Tier 3 Prospects** (50 companies)

Why they score lower:
- Industry adjacent but not exact
- Size outside ideal range
- Different tech stack
- Different growth stage

**Recommendation**: Reach out if you exhaust Tier 1 & 2

---

## 🔍 Market Insights

### Industry Distribution

| Industry | # Companies | % of Lookalikes |
|----------|-------------|-----------------|
| [Industry 1] | XX | XX% |
| [Industry 2] | XX | XX% |
| [Industry 3] | XX | XX% |
| Other | XX | XX% |

**Insight**: [X]% of lookalikes concentrated in [industry], suggesting strong product-market fit there.

---

### Size Distribution

| Company Size | # Companies | % of Lookalikes |
|--------------|-------------|-----------------|
| 1-50 | XX | XX% |
| 51-200 | XX | XX% |
| 201-500 | XX | XX% |
| 500-1000 | XX | XX% |
| 1000+ | XX | XX% |

**Sweet Spot**: [X-Y] employees ([X]% of best customers in this range)

---

### Geographic Distribution

| Region | # Companies | % of Lookalikes |
|--------|-------------|-----------------|
| [Region 1] | XX | XX% |
| [Region 2] | XX | XX% |
| [Region 3] | XX | XX% |

**Insight**: [Observation about geographic concentration]

---

### Growth Stage Distribution

| Stage | # Companies | % of Lookalikes |
|-------|-------------|-----------------|
| Seed | XX | XX% |
| Series A | XX | XX% |
| Series B | XX | XX% |
| Series C+ | XX | XX% |
| Bootstrapped | XX | XX% |

**Best Stage**: [Stage] companies have highest win rate

---

## 🎯 Targeting Strategy

### Tier 1: Top 10 (Weeks 1-2)

**Approach**: Highly personalized, multi-channel outreach
- Research each company deeply
- Find warm intro paths
- Custom demos and case studies
- Executive-level engagement

**Expected Results**:
- Response Rate: 40-50%
- Meeting Rate: 25-30%
- Close Rate: 15-20%

---

### Tier 2: Next 40 (Weeks 3-6)

**Approach**: Personalized at scale
- AI-generated personalization
- Account-based sequences
- Industry-specific content
- Multi-threading

**Expected Results**:
- Response Rate: 20-30%
- Meeting Rate: 12-15%
- Close Rate: 8-12%

---

### Tier 3: Next 50 (Weeks 7-10)

**Approach**: Volume with relevance
- Template-based outreach
- Segment by characteristics
- Nurture over time
- Marketing automation

**Expected Results**:
- Response Rate: 10-15%
- Meeting Rate: 5-8%
- Close Rate: 3-5%

---

## 🚀 Quick Start Action Plan

### Week 1: Top 10 Deep Dive
- [ ] Research each of top 10 companies
- [ ] Find mutual connections
- [ ] Identify decision makers
- [ ] Draft personalized outreach
- [ ] Begin outreach

### Week 2: Tier 1 Follow-up + Tier 2 Prep
- [ ] Follow up with Tier 1 non-responders
- [ ] Schedule meetings with responders
- [ ] Export Tier 2 list (40 companies)
- [ ] Build outreach sequences
- [ ] Enrich contact data

### Week 3-4: Tier 2 Outreach
- [ ] Launch Tier 2 campaign
- [ ] Monitor responses
- [ ] Continue Tier 1 meetings
- [ ] Adjust messaging based on learnings

### Week 5-6: Tier 2 Follow-up + Tier 3 Launch
- [ ] Follow up Tier 2
- [ ] Prepare Tier 3 campaign
- [ ] Review what's working
- [ ] Optimize approach

---

## 💡 Enrichment Data Sources

**Recommended Tools**:
- **Company Data**: Crunchbase, ZoomInfo, LinkedIn
- **Tech Stack**: BuiltWith, Wappalyzer, Datanyze
- **Funding**: Crunchbase, PitchBook, CB Insights
- **Contacts**: Apollo, RocketReach, Hunter.io
- **Intent**: 6sense, Bombora, G2

**Data Points to Gather**:
- Decision maker names and emails
- Recent company news
- Tech stack details
- Employee count growth
- Job postings
- Social media activity

---

## 📈 Success Metrics

**Track These KPIs**:
- **Outreach Metrics**: Response rate, meeting rate
- **Quality Metrics**: Similarity score correlation to close rate
- **Efficiency Metrics**: Time to first meeting, sales cycle length
- **Outcome Metrics**: Win rate by similarity tier

**Hypothesis to Test**:
- Do 90+ similarity companies close faster?
- Do certain industries respond better?
- Does company size affect deal size?

---

## 🔄 Continuous Improvement

### Monthly Refresh
- Add new best customers to analysis
- Remove churned customers
- Update ICP based on recent wins
- Find new lookalikes matching updated profile

### Quarterly Review
- Analyze which lookalike tiers performed best
- Adjust similarity weightings
- Expand to adjacent markets
- Update targeting strategy

```

### Best Practices

1. **Quality Over Quantity**: 10 perfect matches > 100 mediocre ones
2. **Use Multiple Criteria**: Don't just match on industry and size
3. **Look for Growth Signals**: Companies in growth mode buy more
4. **Prioritize Recent Similarity**: Recently funded/hired companies
5. **Test and Learn**: Track which profiles actually close
6. **Refresh Regularly**: Markets change, keep list current
7. **Enrich Before Outreach**: Get contact data before campaign

### Common Use Cases

**Trigger Phrases**:
- "Find 100 companies like my top 10 customers"
- "Who else looks like [Best Customer Company]?"
- "Build a lookalike target account list"
- "Identify companies similar to our best customers"

**Example Request**:
> "Here are my top 10 customers: Stripe, Square, Braintree, Adyen, Checkout.com. All are payment processors between 200-1000 employees. Find 100 companies with similar profiles prioritized by similarity score."

**Response Approach**:
1. Analyze common characteristics of best customers
2. Build ideal customer profile (ICP)
3. Search market for matching companies
4. Score each on similarity dimensions
5. Rank and prioritize by score
6. Provide targeting strategy

Remember: Your best future customers look a lot like your best current customers!
