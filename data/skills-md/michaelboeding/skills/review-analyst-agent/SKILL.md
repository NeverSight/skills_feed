---
name: review-analyst-agent
description: >
  Use this skill to analyze product reviews, find common issues, and prioritize improvements.
  Triggers: "analyze reviews", "review analysis", "customer feedback", "what are people saying",
  "product reviews", "review sentiment", "find complaints", "customer complaints",
  "improvement recommendations", "voice of customer", "VOC analysis", "feedback analysis"
  Outputs: Prioritized issues, sentiment analysis, improvement recommendations.
---

# Review Analyst Agent

Analyze product reviews to find issues and prioritize improvements.

**This skill uses 4 specialized agents** that analyze reviews from different angles, then synthesizes into actionable recommendations.

## What It Produces

| Output | Description |
|--------|-------------|
| **Sentiment Overview** | Overall sentiment breakdown (positive/neutral/negative) |
| **Top Complaints** | Prioritized list of issues by frequency and severity |
| **Top Praise** | What customers love (to protect/emphasize) |
| **Feature Requests** | What customers want that doesn't exist |
| **Priority Matrix** | Critical/Important/Nice-to-have improvements |
| **Action Plan** | Specific recommendations with expected impact |

## Prerequisites

- Web access for scraping reviews
- No API keys required

## Workflow

### Step 1: Identify Product and Sources (REQUIRED)

⚠️ **DO NOT skip this step. Use interactive questioning — ask ONE question at a time.**

#### Question Flow

⚠️ **Use the `AskUserQuestion` tool for each question below.** Do not just print questions in your response — use the tool to create interactive prompts with the options shown.

**Q1: Product**
> "I'll analyze reviews for your product! First — **what's the product?**
> 
> *(Product name or URL)*"

*Wait for response.*

**Q2: Sources**
> "**Where should I look** for reviews?
> 
> - Amazon
> - App Store / Google Play
> - G2 / Capterra
> - Reddit
> - All of the above
> - Or specify"

*Wait for response.*

**Q3: Context**
> "Is this **your product** or a **competitor's**?
> 
> *(Helps frame the analysis)*"

*Wait for response.*

**Q4: Issues**
> "Any **known issues** you want me to validate or explore?
> 
> - Yes — describe them
> - No — find all issues"

*Wait for response.*

#### Quick Reference

| Question | Determines |
|----------|------------|
| Product | What to analyze |
| Sources | Where to scrape reviews |
| Context | Framing of recommendations |
| Issues | Focus areas for analysis |

---

### Step 2: Collect Reviews

Use browser tools to scrape reviews from:

| Source Type | Platforms |
|-------------|-----------|
| **E-commerce** | Amazon, Walmart, Target, Best Buy |
| **Software** | G2, Capterra, TrustRadius, Product Hunt |
| **Apps** | App Store, Google Play Store |
| **General** | Trustpilot, BBB, Yelp |
| **Social** | Reddit, Twitter/X, YouTube comments |
| **Forums** | Product-specific communities |

**Collect for each review:**
- Rating (if available)
- Date
- Review text
- Helpful votes (if available)

---

### Step 3: Run Specialized Analysis Agents in Parallel

Deploy 4 agents, each analyzing from a different perspective:

#### Agent 1: Review Scraper
Focus: Find and collect reviews from multiple sources
```
Tasks:
- Navigate to review platforms
- Extract review text and ratings
- Collect metadata (date, helpful votes)
- Handle pagination
- De-duplicate reviews
```

#### Agent 2: Sentiment Analyzer
Focus: Analyze sentiment and emotional patterns
```
Analyze:
- Overall sentiment (positive/neutral/negative)
- Emotional intensity
- Frustration indicators
- Satisfaction indicators
- Sentiment trends over time
```

#### Agent 3: Issue Identifier
Focus: Categorize complaints and find patterns
```
Identify:
- Common complaint themes
- Frequency of each issue
- Severity indicators
- Specific quotes as evidence
- Root cause patterns
```

#### Agent 4: Improvement Recommender
Focus: Prioritize and recommend fixes
```
Recommend:
- Priority ranking of issues
- Specific improvement suggestions
- Expected impact of each fix
- Quick wins vs long-term investments
- Competitive gaps to address
```

---

### Step 4: Synthesize into Analysis Report

Combine all agent outputs into a structured report:

```json
{
  "product": {
    "name": "Product Name",
    "sources_analyzed": ["Amazon (342 reviews)", "Reddit (89 posts)", "G2 (56 reviews)"],
    "total_reviews": 487,
    "date_range": "Jan 2025 - Jan 2026",
    "analysis_date": "2026-01-04"
  },
  "sentiment": {
    "overall_score": 3.8,
    "breakdown": {
      "positive": 62,
      "neutral": 18,
      "negative": 20
    },
    "trend": "Improving (up from 3.5 six months ago)",
    "net_promoter_estimate": 32
  },
  "top_complaints": [
    {
      "rank": 1,
      "issue": "Battery drains too fast",
      "frequency": 47,
      "percentage": "23% of negative reviews",
      "severity": "High",
      "sample_quotes": [
        "Battery only lasts 2 hours, not the 8 advertised",
        "Have to charge it 3x per day",
        "Battery life is a dealbreaker"
      ],
      "root_cause": "Hardware limitation or software optimization needed",
      "recommendation": "Improve battery capacity or optimize power consumption",
      "expected_impact": "Could improve rating by 0.3-0.5 stars"
    },
    {
      "rank": 2,
      "issue": "App crashes frequently",
      "frequency": 32,
      "percentage": "16% of negative reviews",
      "severity": "High",
      "sample_quotes": [
        "App crashes every time I try to sync",
        "Lost all my data after app crashed"
      ],
      "root_cause": "Sync functionality stability",
      "recommendation": "Stability audit of mobile app, fix crash on sync",
      "expected_impact": "Could reduce 1-star reviews by 15%"
    }
  ],
  "top_praise": [
    {
      "feature": "Build quality",
      "frequency": 89,
      "percentage": "45% of positive reviews",
      "sample_quotes": [
        "Feels premium in hand",
        "Solid construction, very durable"
      ],
      "recommendation": "Emphasize in marketing, protect in future versions"
    }
  ],
  "feature_requests": [
    {
      "request": "Water resistance",
      "frequency": 23,
      "sample_quotes": [
        "Wish I could use it in the rain",
        "Would pay extra for waterproof version"
      ],
      "recommendation": "Consider for v2 or premium tier"
    }
  ],
  "competitor_mentions": [
    {
      "competitor": "Competitor X",
      "context": "Switching from",
      "frequency": 15,
      "sentiment": "Mixed - some prefer us, some prefer them"
    }
  ],
  "priority_matrix": {
    "critical": [
      {"issue": "Battery life", "reason": "Top complaint, high severity"},
      {"issue": "App crashes", "reason": "Causes data loss, drives 1-star reviews"}
    ],
    "important": [
      {"issue": "Water resistance", "reason": "Frequent request, competitive gap"}
    ],
    "nice_to_have": [
      {"issue": "Color options", "reason": "Low frequency, low impact"}
    ]
  },
  "action_plan": [
    {
      "priority": 1,
      "action": "Fix app crash on sync",
      "effort": "Medium",
      "impact": "High",
      "expected_outcome": "Reduce 1-star reviews by 15%"
    },
    {
      "priority": 2,
      "action": "Improve battery life or set realistic expectations",
      "effort": "High",
      "impact": "High",
      "expected_outcome": "Improve rating by 0.3-0.5 stars"
    },
    {
      "priority": 3,
      "action": "Add water resistance to roadmap for v2",
      "effort": "High",
      "impact": "Medium",
      "expected_outcome": "Address top feature request"
    }
  ]
}
```

---

### Step 5: Deliver Actionable Insights

**Delivery message:**

"✅ Review analysis complete!

**Product:** [Name]
**Reviews Analyzed:** [Count] from [Sources]
**Overall Sentiment:** [Score] ([Positive]% positive)

**Top 3 Issues (by frequency):**
1. 🔴 [Issue 1] - [X]% of complaints
2. 🔴 [Issue 2] - [X]% of complaints
3. 🟡 [Issue 3] - [X]% of complaints

**What Customers Love:**
✅ [Praised feature 1]
✅ [Praised feature 2]

**Priority Action:**
→ Fix [Top Issue] first - expected to improve rating by [X]

**Want me to:**
- Deep dive on any issue?
- Compare to competitor reviews?
- Track changes over time?
- Create improvement roadmap?"

---

## Integration with Other Agents

```
review-analyst-agent
    ↓ "Battery is top complaint"
product-engineer-agent
    ↓ "Design better battery solution"
patent-lawyer-agent
    ↓ "Check if solution is patentable"
copywriter-agent
    ↓ "Update marketing to address concern"
```

| Agent | How It Uses Review Data |
|-------|-------------------------|
| `product-engineer-agent` | Inform what to fix/improve |
| `competitive-intel-agent` | Compare to competitor reviews |
| `market-researcher-agent` | Validate market needs |
| `copywriter-agent` | Address concerns in marketing |
| `pitch-deck-agent` | Show customer-centric improvements |
| `media-utils` | **Generate PDF report** from analysis |

---

## Generate PDF Report

After completing the analysis, offer to generate a PDF:

> "Would you like me to generate a **PDF report** of this review analysis?"

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/media-utils/scripts/report_to_pdf.py \
  --input review_analysis.md \
  --output review_analysis.pdf \
  --title "Customer Review Analysis" \
  --style business
```

---

## Agents

| Agent | File | Focus |
|-------|------|-------|
| Review Scraper | `review-scraper.md` | Find and collect reviews |
| Sentiment Analyzer | `sentiment-analyzer.md` | Analyze sentiment patterns |
| Issue Identifier | `issue-identifier.md` | Categorize complaints |
| Improvement Recommender | `improvement-recommender.md` | Prioritize and recommend |

---

## Example Prompts

**Your product:**
> "Analyze reviews for our Bluetooth headphones on Amazon"

**Competitor:**
> "What are people complaining about with Notion?"

**Comparison:**
> "Compare reviews of our product vs Competitor X"

**Feature focus:**
> "Find feature requests for our mobile app from App Store and Reddit"

**Priority:**
> "What should we fix first based on customer feedback?"

**Trend:**
> "How has sentiment changed over the last 6 months?"
