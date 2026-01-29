---
name: competitive-intel-agent
description: >
  Use this skill to analyze competitors, find competitive gaps, and develop competitive strategy.
  Triggers: "competitor analysis", "competitive analysis", "analyze competitor", "competitive intel",
  "competitive intelligence", "competitive landscape", "competitor comparison", "beat competitor",
  "competitor weakness", "competitive advantage", "competitor research"
  Outputs: Competitive matrix, gap analysis, differentiation strategy, battlecards.
---

# Competitive Intel Agent

Analyze competitors and develop strategies to win against them.

**This skill uses 4 specialized agents** that analyze competitors from different angles, then synthesizes into actionable intelligence.

## What It Produces

| Output | Description |
|--------|-------------|
| **Competitive Matrix** | Feature-by-feature comparison |
| **SWOT Analysis** | Strengths, weaknesses, opportunities, threats |
| **Gap Analysis** | Where you can differentiate |
| **Battlecard** | Quick reference for sales/marketing |
| **Strategy Recommendations** | How to position against each competitor |
| **Visual Charts** | Positioning matrix, feature comparison, pricing charts (optional) |

## Prerequisites

- Web access for research
- `GOOGLE_API_KEY` - For generating comparison charts (optional, uses image-generation skill)

## Workflow

### Step 1: Gather Requirements (REQUIRED)

⚠️ **DO NOT skip this step. Use interactive questioning — ask ONE question at a time.**

#### Question Flow

⚠️ **Use the `AskUserQuestion` tool for each question below.** Do not just print questions in your response — use the tool to create interactive prompts with the options shown.

**Q1: Product**
> "I'll analyze your competitive landscape! First — **what's your product or service?**
> 
> *(What you offer)*"

*Wait for response.*

**Q2: Competitors**
> "Who are your **main competitors**?
> 
> *(Company names or URLs — or say 'help me identify them' if unsure)*"

*Wait for response.*

**Q3: Aspects**
> "What **aspects** should I compare?
> 
> - Features and capabilities
> - Pricing and packaging
> - Market position
> - All of the above
> - Or specify"

*Wait for response.*

**Q4: Goal**
> "What's your **goal** for this analysis?
> 
> - Differentiate from competitors
> - Enter a new market
> - Win specific deals
> - Understand the landscape
> - Or describe"

*Wait for response.*

**Q5: Visuals**
> "Do you want me to **generate visual charts**?
> 
> - 📊 Yes — positioning matrix, feature comparison, pricing charts
> - 📝 No — text and tables only"

*Wait for response.*

#### Quick Reference

| Question | Determines |
|----------|------------|
| Product | What we're positioning |
| Competitors | Who to research |
| Aspects | Depth of analysis |
| Goal | Framing and recommendations |
| Visuals | Whether to generate charts |

---

### Step 2: Run Specialized Analysis Agents in Parallel

Deploy 4 agents, each analyzing from a different perspective:

#### Agent 1: Feature Analyst
Focus: Product features and capabilities
```
Compare:
- Core features and functionality
- Feature depth vs breadth
- Unique capabilities
- Missing features
- Roadmap/recent launches
- Integrations and ecosystem
```

#### Agent 2: Pricing Analyst
Focus: Pricing and value proposition
```
Compare:
- Pricing models (subscription, usage, one-time)
- Price points and tiers
- Feature packaging
- Free tier/trial offerings
- Enterprise pricing
- Total cost of ownership
```

#### Agent 3: Positioning Analyst
Focus: Brand positioning and messaging
```
Compare:
- Target audience claims
- Key messaging themes
- Brand personality
- Thought leadership
- Customer testimonials
- Marketing channels
```

#### Agent 4: Market Position Analyst
Focus: Market share and business health
```
Compare:
- Estimated market share
- Company size/funding
- Growth trajectory
- Customer base
- Partnerships
- Public perception
```

---

### Step 3: Synthesize into Competitive Intelligence

Combine all agent outputs into structured intelligence:

```json
{
  "analysis_scope": {
    "your_product": "Your product/service",
    "competitors_analyzed": ["Competitor 1", "Competitor 2", "Competitor 3"],
    "analysis_date": "2026-01-04"
  },
  "competitive_matrix": {
    "features": {
      "Feature Category 1": {
        "your_product": "✅ Full",
        "competitor_1": "✅ Full",
        "competitor_2": "⚠️ Partial",
        "competitor_3": "❌ None"
      }
    },
    "pricing": {
      "your_product": "$XX/mo",
      "competitor_1": "$XX/mo",
      "competitor_2": "$XX/mo"
    }
  },
  "competitor_profiles": [
    {
      "name": "Competitor 1",
      "website": "https://competitor1.com",
      "positioning": "How they position themselves",
      "target_audience": "Who they target",
      "strengths": ["Strength 1", "Strength 2"],
      "weaknesses": ["Weakness 1", "Weakness 2"],
      "pricing": "$XX/mo for Pro tier",
      "differentiator": "What makes them unique",
      "threat_level": "High/Medium/Low"
    }
  ],
  "swot": {
    "strengths": ["Your strength vs competitors"],
    "weaknesses": ["Your weakness vs competitors"],
    "opportunities": ["Gaps to exploit"],
    "threats": ["Competitive threats to address"]
  },
  "gap_analysis": {
    "underserved_segments": ["Segment competitors ignore"],
    "missing_features": ["Features no one offers"],
    "pricing_gaps": ["Price point opportunities"],
    "positioning_gaps": ["Messaging white space"]
  },
  "battlecard": {
    "competitor_1": {
      "when_we_win": ["Scenario 1", "Scenario 2"],
      "when_they_win": ["Scenario 1", "Scenario 2"],
      "key_differentiators": ["What to emphasize"],
      "objection_handling": {
        "They're cheaper": "Response...",
        "They have feature X": "Response..."
      },
      "landmines": ["Questions to ask that expose their weakness"]
    }
  },
  "recommendations": {
    "positioning": "How to position against the field",
    "messaging": "Key messages to emphasize",
    "features_to_build": ["Feature gaps to close"],
    "segments_to_target": ["Where you can win"],
    "pricing_strategy": "How to price competitively"
  }
}
```

---

### Step 4: Generate Comparison Charts (If Requested)

If user wants visual charts, generate using the `image-generation` skill.

**Charts to generate:**

| Chart Type | Purpose | Example Prompt |
|------------|---------|----------------|
| **Positioning Matrix** | Show competitive landscape | "Competitive positioning 2x2 matrix, X-axis: Price (low to high), Y-axis: Features (basic to advanced), with company logos/names plotted, clean business style" |
| **Feature Comparison** | Compare capabilities | "Feature comparison chart, [Your Product] vs [Comp A] vs [Comp B], checkmarks and X marks, clean table visualization" |
| **Pricing Chart** | Compare price points | "Bar chart comparing pricing, [Products] on X-axis, price on Y-axis, professional business colors" |
| **Market Share** | Show market positions | "Pie chart showing market share, [Company names] with percentages, business presentation style" |

**Prompt template:**
```
Professional competitive analysis chart,
[CHART TYPE] showing [COMPETITORS],
[DATA TO VISUALIZE],
clean business presentation style,
professional colors,
easy to read labels
```

**Example generation:**
```bash
python3 ${SKILL_PATH}/skills/image-generation/scripts/gemini.py \
  --prompt "Competitive positioning 2x2 matrix, X-axis labeled 'Price' from Low to High, Y-axis labeled 'Features' from Basic to Enterprise, showing Salesforce in top-right, HubSpot in middle, Pipedrive in bottom-left, clean business presentation style, professional blue colors, labeled quadrants" \
  --aspect-ratio "16:9" \
  --resolution "2K"
```

**Save files as:**
- `competitive_matrix.png` - 2x2 positioning matrix
- `feature_comparison.png` - Feature checkmark grid
- `pricing_comparison.png` - Pricing bar chart

---

### Step 5: Deliver Actionable Intelligence

**Delivery message (with charts):**

"✅ Competitive analysis complete!

**You vs [# competitors analyzed]**

**Your Biggest Advantage:** [Key differentiator]
**Biggest Threat:** [Competitor] because [reason]
**Best Opportunity:** [Gap or segment to exploit]

**Generated Charts:**
- competitive_matrix.png (positioning 2x2)
- feature_comparison.png
- pricing_comparison.png

**Quick Battlecard:**
- Against [Competitor 1]: Lead with [differentiator]
- Against [Competitor 2]: Emphasize [strength]

**Want me to:**
- Deep dive on any competitor?
- Create detailed battlecards for sales?
- Analyze additional competitors?
- Research specific features?"

---

**Delivery message (analysis only, no charts):**

"✅ Competitive analysis complete!

**You vs [# competitors analyzed]**

**Your Biggest Advantage:** [Key differentiator]
**Biggest Threat:** [Competitor] because [reason]
**Best Opportunity:** [Gap or segment to exploit]

**Quick Battlecard:**
- Against [Competitor 1]: Lead with [differentiator]
- Against [Competitor 2]: Emphasize [strength]

**Want me to:**
- **Generate visual charts?** (positioning matrix, comparisons)
- Deep dive on any competitor?
- Create detailed battlecards for sales?
- Analyze additional competitors?"

---

## Output Formats

### Competitive Matrix (Visual)
```
Feature          | You  | Comp A | Comp B | Comp C
-----------------|------|--------|--------|-------
Feature 1        | ✅   | ✅     | ⚠️     | ❌
Feature 2        | ✅   | ❌     | ✅     | ✅
Feature 3        | ✅   | ✅     | ✅     | ❌
Pricing (Pro)    | $29  | $49    | $39    | $19
Free Tier        | ✅   | ❌     | ✅     | ✅
```

### Sales Battlecard (Quick Reference)
```
## vs [Competitor Name]

WHEN WE WIN:
- Customer values X
- They need Y integration
- Budget is limited

WHEN THEY WIN:
- They're already using their ecosystem
- Need feature Z (we don't have)

OUR LANDMINES:
- "How do they handle [problem we solve better]?"
- "What's their uptime SLA?"

OBJECTION HANDLING:
- "They're the market leader" → "Size doesn't mean best fit..."
- "They have more features" → "More features = more complexity..."
```

---

## Integration with Other Skills

| Skill | Use Case |
|-------|----------|
| `image-generation` | **Generate comparison charts** (positioning matrix, features, pricing) |
| `brand-research-agent` | Deep dive on competitor's brand |
| `market-researcher-agent` | Market size and dynamics |
| `product-engineer-agent` | Design features to differentiate |
| `copywriter-agent` | Write competitive messaging |
| `media-utils` | **Generate PDF report** from analysis |

---

## Generate PDF Report

After completing the analysis, offer to generate a PDF:

> "Would you like me to generate a **PDF report** of this competitive analysis?"

**To generate the PDF:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/media-utils/scripts/report_to_pdf.py \
  --input competitive_analysis.md \
  --output competitive_analysis.pdf \
  --title "Competitive Intelligence Report" \
  --style business
```

**Available styles:** `business` (default), `executive`, `technical`, `minimal`

---

## Agents

| Agent | File | Focus |
|-------|------|-------|
| Feature Analyst | `feature-analyst.md` | Product features |
| Pricing Analyst | `pricing-analyst.md` | Pricing models |
| Positioning Analyst | `positioning-analyst.md` | Brand/messaging |
| Market Position Analyst | `market-position-analyst.md` | Market share |

---

## Example Prompts

**Full analysis:**
> "Analyze our CRM competitors: Salesforce, HubSpot, and Pipedrive"

**Specific competitor:**
> "Deep dive on Notion - find their weaknesses"

**Find competitors:**
> "Who are the main competitors to our AI writing tool?"

**Battlecard:**
> "Create a sales battlecard for when we compete against Slack"

**Gap analysis:**
> "What features do our competitors have that we're missing?"
