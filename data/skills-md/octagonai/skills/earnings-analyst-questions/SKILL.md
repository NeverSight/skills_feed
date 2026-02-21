---
name: earnings-analyst-questions
description: Identify key themes and concerns raised by analysts during earnings calls, including specific analyst attribution and topic categorization.
---

# Earnings Analyst Questions

Identify and analyze the key themes, concerns, and questions raised by analysts during earnings calls, with specific analyst attribution and topic categorization.

## Prerequisites

Ensure Octagon MCP is configured. See [references/mcp-setup.md](references/mcp-setup.md) for installation instructions.

## Workflow

### Step 1: Extract Analyst Questions

Use the Octagon MCP to identify analyst questions and concerns:

```
Identify key themes and concerns raised by analysts during <TICKER>'s latest earnings call.
```

### Step 2: Targeted Question Analysis

Focus on specific aspects of analyst questions:

```
# All Analyst Concerns
What concerns did analysts raise in <TICKER>'s latest earnings call?

# Specific Topic
What questions did analysts ask about AI in <TICKER>'s earnings call?

# Analyst Coverage
Which analysts participated in <TICKER>'s earnings call Q&A?

# Most Frequent Topics
What were the most frequently asked topics in <TICKER>'s earnings call?

# Unanswered Questions
Were there questions that management avoided or didn't fully answer in <TICKER>'s call?
```

## Expected Output

The skill returns structured analyst question analysis including:

| Component | Description |
|-----------|-------------|
| Key Themes | Major topics raised by analysts |
| Analyst Attribution | Which analyst asked which question |
| Concern Categories | Grouped by topic area |
| Management Response | How questions were addressed |
| Follow-up Questions | AI-generated questions for deeper research |
| Source Citations | Transcript page references |

## Example Query

```
Identify key themes and concerns raised by analysts during TSLA's latest earnings call.
```

## Example Response

Analysts highlighted several critical topics during Tesla's latest earnings call, as documented in the TSLA_Q22025 transcript:

**Key Analyst Questions**

- **Robotaxi Business Funding** – Analysts questioned how Tesla plans to finance the costs of scaling its robotaxi initiative, specifically whether it will rely on auto business cash flows or alternative funding sources [Dan Meir Levy]

- **Full Self-Driving (FSD) Revenue Potential** – Interest focused on trends and monetization strategies for FSD subscriptions [Mark Trevor Delaney]

- **Megapack Sales Impact** – The elimination of tax credits for solar projects raised concerns about its effect on Tesla's Megapack sales pipeline

- **Incentive Loss and Autonomy Challenges** – Analysts warned of potential rough quarters due to the loss of U.S. incentives and the early-stage risks of autonomy development [Elon Musk]

- **Lower-Cost Model Details** – Requests for more information on production timelines and cost-saving strategies for Tesla's upcoming lower-cost vehicle [Lars Moravy]

**Follow-up Questions**
- What specific funding mechanisms has Tesla outlined for the robotaxi business?
- How does Tesla plan to mitigate risks from the loss of U.S. tax incentives?
- What are the projected timelines for the lower-cost model's production launch?

**Source**: TSLA_Q22025, Page: 5

## Analyst Question Categories

### Financial Topics
| Category | Example Questions |
|----------|-------------------|
| Revenue | Segment growth, pricing, demand |
| Margins | Cost structure, pricing power |
| Guidance | Outlook clarification, assumptions |
| Capital | Allocation, returns, leverage |

### Strategic Topics
| Category | Example Questions |
|----------|-------------------|
| Growth Initiatives | New products, markets, investments |
| Competitive | Market share, differentiation |
| M&A | Deal pipeline, integration |
| Technology | R&D, innovation, roadmap |

### Operational Topics
| Category | Example Questions |
|----------|-------------------|
| Execution | Production, capacity, efficiency |
| Supply Chain | Sourcing, costs, risks |
| Workforce | Hiring, retention, costs |
| Geographic | Regional performance, expansion |

### Risk Topics
| Category | Example Questions |
|----------|-------------------|
| Regulatory | Policy changes, compliance |
| Macro | Economic sensitivity, cycles |
| Competitive | Market threats, disruption |
| Execution | Delivery, timeline risks |

## Analyst Attribution

### Understanding Analyst Context

| Analyst Type | Typical Focus |
|--------------|---------------|
| Sell-side (Bulge Bracket) | Broad coverage, key themes |
| Sell-side (Boutique) | Sector expertise, detailed |
| Buy-side | Specific thesis questions |
| Independent | Alternative perspectives |

### Notable Analyst Patterns

| Pattern | Interpretation |
|---------|----------------|
| Same analyst, same topic | Persistent concern |
| Multiple analysts, same topic | Widespread concern |
| New topic raised | Emerging issue |
| Detailed follow-up | Dissatisfied with response |

## Question Intensity Analysis

### Measuring Topic Importance

| Metric | Interpretation |
|--------|----------------|
| Number of questions | Topic priority |
| Number of follow-ups | Incomplete answers |
| Analyst seniority | Credibility weight |
| Time spent | Management engagement |

### Heat Map Framework

| Topic | Questions | Follow-ups | Intensity |
|-------|-----------|------------|-----------|
| FSD Revenue | 3 | 2 | High |
| Margins | 2 | 1 | Medium |
| CapEx | 1 | 0 | Low |

## Concern Classification

### Severity Assessment

| Severity | Indicators |
|----------|------------|
| Critical | Multiple analysts, pushback, unresolved |
| High | Several questions, detailed probing |
| Medium | Standard questions, adequate response |
| Low | Single mention, brief discussion |

### Resolution Status

| Status | Description |
|--------|-------------|
| Resolved | Clear, specific answer provided |
| Partially Resolved | Some detail, gaps remain |
| Deflected | Redirected, not directly answered |
| Unresolved | Avoided, promised future update |

## Tracking Questions Over Time

### Quarter-over-Quarter Analysis

| Topic | Q1 | Q2 | Q3 | Q4 | Trend |
|-------|----|----|----|----|-------|
| FSD | 1 | 2 | 3 | 4 | Rising |
| Margins | 3 | 2 | 2 | 1 | Declining |
| China | 2 | 3 | 2 | 2 | Stable |

### New vs. Recurring Topics

| Type | What It Means |
|------|---------------|
| New topic | Emerging concern or opportunity |
| Recurring topic | Persistent issue |
| Dropped topic | Resolved or no longer relevant |
| Intensifying | Growing importance |

## Use Cases

1. **Sentiment Analysis**: Gauge Street concerns and focus areas
2. **Risk Discovery**: Identify issues analysts are probing
3. **Thesis Validation**: Check if your concerns are shared
4. **Peer Comparison**: Compare question themes across competitors
5. **Management Assessment**: Evaluate response quality
6. **Pre-Earnings Prep**: Anticipate likely questions

## Combining with Other Skills

| Skill | Combined Analysis |
|-------|-------------------|
| earnings-qa-analysis | Questions + management responses |
| earnings-call-analysis | Full context + analyst focus |
| price-target-consensus | Analyst concerns vs. targets |
| stock-grades | Questions aligned with ratings |
| stock-price-change | Question impact on price |

## Analysis Tips

1. **Track Analyst Names**: Note who asks what repeatedly

2. **Count Question Frequency**: More questions = higher priority

3. **Watch for Pushback**: Analysts pressing = important issue

4. **Note Unanswered Questions**: What's management avoiding?

5. **Compare to Peers**: Are same questions asked of competitors?

6. **Pre-Earnings Prediction**: Anticipate topics based on history

## Interpreting Results

See [references/interpreting-results.md](references/interpreting-results.md) for detailed guidance on analyzing analyst questions.
