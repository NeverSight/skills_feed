---
name: market-researcher-agent
description: >
  Use this skill to research markets, understand trends, find opportunities, and validate ideas.
  Triggers: "market research", "market analysis", "market opportunity", "market size",
  "TAM SAM SOM", "industry analysis", "market trends", "validate idea", "market validation",
  "customer research", "market sizing", "opportunity analysis"
  Outputs: Market report with size, trends, opportunities, competitive landscape.
---

# Market Researcher Agent

Research markets and validate opportunities with comprehensive analysis.

**This skill uses 4 specialized agents** that analyze markets from different perspectives, then synthesizes into a complete market research report.

## What It Produces

| Output | Description |
|--------|-------------|
| **Market Size** | TAM, SAM, SOM estimates with methodology |
| **Trends Analysis** | Current trends and future outlook |
| **Competitive Landscape** | Key players and their positions |
| **Opportunities** | Gaps and opportunities identified |
| **Go/No-Go Recommendation** | Assessment of market attractiveness |

## Prerequisites

- Web access for research (browser tools)
- No API keys required

## Workflow

### Step 1: Define Research Scope (REQUIRED)

⚠️ **DO NOT skip this step. Use interactive questioning — ask ONE question at a time.**

#### Question Flow

⚠️ **Use the `AskUserQuestion` tool for each question below.** Do not just print questions in your response — use the tool to create interactive prompts with the options shown.

**Q1: Market**
> "I'll research this market for you! First — **what market or industry?**
> 
> *(e.g., 'smart home devices', 'pet food', 'B2B SaaS')*"

*Wait for response.*

**Q2: Product**
> "Do you have a **specific product or idea** you're exploring?
> 
> - Yes — describe it
> - No — just researching the market"

*Wait for response.*

**Q3: Geography**
> "What's the **geographic focus**?
> 
> - US only
> - North America
> - Europe
> - Global
> - Or specify regions"

*Wait for response.*

**Q4: Questions**
> "Any **specific questions** you want answered?
> 
> *(e.g., 'is this market growing?', 'who are the key players?', 'what's the market size?')*
> 
> Or say 'comprehensive analysis' for a full report."

*Wait for response.*

#### Quick Reference

| Question | Determines |
|----------|------------|
| Market | Industry and category focus |
| Product | Whether to include product-market fit analysis |
| Geography | Regional scope of research |
| Questions | Specific areas to emphasize |

---

### Step 2: Run Specialized Research Agents in Parallel

Deploy 4 agents, each researching a different dimension:

#### Agent 1: Trend Analyst
Focus: Market trends, growth trajectory, future outlook
```
Research:
- Current market size and growth rate
- Historical growth trends
- Future projections (3-5 years)
- Technology trends affecting the market
- Consumer behavior shifts
- Regulatory changes impacting the market
```

#### Agent 2: Consumer Researcher
Focus: Customer segments, behavior, needs
```
Research:
- Primary customer segments
- Customer demographics
- Buying behavior and preferences
- Pain points and unmet needs
- Willingness to pay
- Decision-making process
```

#### Agent 3: Industry Analyst
Focus: Market structure, players, dynamics
```
Research:
- Major players and market share
- Industry value chain
- Distribution channels
- Barriers to entry
- Supplier/buyer power
- Key success factors
```

#### Agent 4: Opportunity Finder
Focus: Gaps, opportunities, entry points
```
Research:
- Underserved segments
- Unmet needs
- Technology gaps
- Geographic white spaces
- Timing opportunities
- Disruption potential
```

---

### Step 3: Synthesize into Market Report

Combine all agent outputs into a structured report:

```json
{
  "market": {
    "name": "Market Name",
    "definition": "How we define this market",
    "geography": "Geographic scope",
    "year": "2026"
  },
  "market_size": {
    "tam": {
      "value": "$XX billion",
      "definition": "Total Addressable Market definition"
    },
    "sam": {
      "value": "$XX billion",
      "definition": "Serviceable Addressable Market definition"
    },
    "som": {
      "value": "$XX million",
      "definition": "Serviceable Obtainable Market definition"
    },
    "methodology": "How these were calculated",
    "sources": ["Source 1", "Source 2"]
  },
  "growth": {
    "current_cagr": "X%",
    "projected_cagr": "X% (2026-2030)",
    "growth_drivers": ["Driver 1", "Driver 2"],
    "growth_inhibitors": ["Inhibitor 1", "Inhibitor 2"]
  },
  "trends": [
    {
      "trend": "Trend name",
      "description": "What's happening",
      "impact": "High/Medium/Low",
      "timeframe": "Now/Near-term/Long-term"
    }
  ],
  "customer_segments": [
    {
      "segment": "Segment name",
      "size": "X% of market",
      "characteristics": "Key traits",
      "needs": ["Need 1", "Need 2"],
      "underserved": true
    }
  ],
  "competitive_landscape": {
    "market_structure": "Fragmented/Consolidated/Oligopoly",
    "key_players": [
      {
        "name": "Company",
        "market_share": "X%",
        "positioning": "How they're positioned",
        "strengths": ["Strength 1"],
        "weaknesses": ["Weakness 1"]
      }
    ],
    "barriers_to_entry": ["Barrier 1", "Barrier 2"]
  },
  "opportunities": [
    {
      "opportunity": "Opportunity name",
      "description": "What the opportunity is",
      "size": "Potential value",
      "difficulty": "Easy/Medium/Hard",
      "timing": "Why now"
    }
  ],
  "threats": [
    {
      "threat": "Threat name",
      "likelihood": "High/Medium/Low",
      "impact": "High/Medium/Low"
    }
  ],
  "recommendation": {
    "assessment": "Attractive/Moderate/Unattractive",
    "rationale": "Why this assessment",
    "suggested_positioning": "How to enter/compete",
    "key_success_factors": ["Factor 1", "Factor 2"]
  }
}
```

---

### Step 4: Deliver and Offer Deep Dives

**Delivery message:**

"✅ Market research complete!

**Market:** [Name]
**Size:** $XX billion (TAM) → $XX million (SOM)
**Growth:** X% CAGR

**Key Finding:** [Most important insight]

**Opportunity:** [Best opportunity identified]

**Recommendation:** [Go/Caution/No-Go] because [rationale]

**Want me to:**
- Deep dive on any segment?
- Research specific competitors?
- Explore a particular opportunity?
- Validate with additional sources?"

---

## Integration with Other Agents

| Agent | Use Case |
|-------|----------|
| `product-engineer-agent` | Design product for validated market |
| `competitive-intel-agent` | Deep competitive analysis |
| `pitch-deck-agent` | Use market data in investor deck |
| `brand-research-agent` | Understand competitor brands |
| `media-utils` | **Generate PDF report** from analysis |

---

## Generate PDF Report

After completing the analysis, offer to generate a PDF:

> "Would you like me to generate a **PDF report** of this market research?"

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/media-utils/scripts/report_to_pdf.py \
  --input market_research.md \
  --output market_research.pdf \
  --title "Market Research Report" \
  --style executive
```

---

## Agents

| Agent | File | Focus |
|-------|------|-------|
| Trend Analyst | `trend-analyst.md` | Growth, trends, future |
| Consumer Researcher | `consumer-researcher.md` | Customers, needs |
| Industry Analyst | `industry-analyst.md` | Players, structure |
| Opportunity Finder | `opportunity-finder.md` | Gaps, opportunities |

---

## Example Prompts

**Market sizing:**
> "What's the market size for smart pet feeders in the US?"

**Opportunity validation:**
> "Is there an opportunity in sustainable packaging for e-commerce?"

**Competitive landscape:**
> "Who are the major players in the CRM software market?"

**Trend analysis:**
> "What are the trends in the plant-based food market?"
