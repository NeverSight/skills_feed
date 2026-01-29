---
name: patent-lawyer-agent
description: >
  Use this skill for intellectual property guidance, prior art research, patent strategy, and drafting patent applications.
  Triggers: "patent", "prior art", "IP protection", "intellectual property", "patent search",
  "patentability", "patent claims", "invention disclosure", "patent strategy", "trade secret",
  "patent application", "freedom to operate", "infringement", "draft patent", "write patent",
  "provisional patent", "patent document", "design around", "get around patent", "avoid patent",
  "work around patent", "FTO", "freedom to operate analysis", "patent analysis"
  Outputs: Patentability assessment, prior art report, draft claims, IP strategy, full patent application draft, design-around analysis.
  DISCLAIMER: This is informational only, not legal advice. Consult a licensed patent attorney.
---

# Patent Lawyer Agent

Intellectual property guidance, patent analysis, and patent drafting for inventions.

**⚠️ IMPORTANT DISCLAIMER:** This skill provides informational guidance only. It is NOT legal advice and does NOT create an attorney-client relationship. Always consult a licensed patent attorney for actual legal matters.

**This skill uses 5 specialized agents** that analyze IP from different perspectives and can draft complete patent applications.

## What It Produces

| Output | Description |
|--------|-------------|
| **Prior Art Report** | Similar existing patents and publications |
| **Patentability Assessment** | Analysis of novelty and non-obviousness |
| **Draft Claims** | Example patent claim language |
| **IP Strategy** | Recommended protection approach |
| **Full Patent Draft** | Complete patent application document with figures |
| **Patent Figures** | Generated technical drawings (via image-generation skill) |

## Prerequisites

- Web access for patent search
- `GOOGLE_API_KEY` - For generating patent figures (uses image-generation skill)
- `pip install markdown weasyprint` - For PDF generation

## How It Works

**This agent is request-driven.** Just tell it what you want and it will do what's needed:

| You Ask | What Happens |
|---------|--------------|
| "Look at this product, can I patent it?" | Researches product, searches prior art, assesses patentability |
| "Search for prior art on X" | Just searches for existing patents/publications |
| "Is my idea patentable?" | Gathers details, searches prior art, gives assessment |
| "Draft a patent for my invention" | Full patent application (does prior art search too) |
| "Write claims for this" | Just drafts patent claims |
| "What's the IP strategy here?" | Strategy advice (patent vs trade secret, timing, costs) |
| "How can I get around this patent?" | Analyzes claims, finds gaps, suggests design alternatives |

**You don't need to follow a rigid workflow.** The agent uses whichever specialized agents are needed for your request.

---

## Request Types

### 1. Analyze a Product or Idea

"Can I patent this?" / "Look at this product and assess patentability"

**What it does:**
1. Gathers details about the product/idea (asks if needed)
2. Searches for prior art (existing patents, publications)
3. Assesses novelty and non-obviousness
4. Delivers patentability verdict with rationale

**Uses agents:** Prior Art Searcher, Patentability Analyst

---

### 2. Prior Art Search Only

"Search for prior art on foldable drone designs"

**What it does:**
1. Searches Google Patents, USPTO, academic papers
2. Identifies closest existing patents
3. Reports relevance and key differences

**Uses agents:** Prior Art Searcher

---

### 3. Draft a Full Patent Application

"Write a complete patent for my invention" / "Create a patent document for this"

**Use the `AskUserQuestion` tool for each question below.** Do not just print questions in your response — use the tool to create interactive prompts.

**Q1: Invention**
> "I'll draft a complete patent application for your invention!
> 
> **⚠️ Note:** This is informational only, not legal advice.
> 
> First — **tell me about your invention.**
> 
> *(What is it? How does it work? What problem does it solve?)*"

*Wait for response.*

**Q2: Figures**
> "Do you want me to **generate patent figures**?
> 
> - 📐 Yes — perspective views, cross-sections, block diagrams (B&W technical drawings)
> - 📝 No — figure descriptions only (you'll create your own drawings)
> 
> *(Generating figures requires `GOOGLE_API_KEY`)*"

*Wait for response.*

**What it does:**
1. Gathers invention details (asks if needed)
2. Searches prior art (automatically)
3. Generates complete patent application:
   - Title, Field, Background
   - Summary, Detailed Description
   - Claims (10-20 independent + dependent)
   - Abstract
4. **If user requested figures:** Generates patent figures (technical drawings)

**Uses agents:** Prior Art Searcher, Patent Drafter + image-generation skill (if figures requested)

**Output:** Full patent application in Markdown + generated figure images (if requested)

---

### 4. Full Analysis + Draft

"Analyze my invention and then draft the patent"

**What it does:**
1. Full patentability analysis (all 4 analysis agents)
2. Drafts complete patent application
3. **If user requested figures:** Generates patent figures
4. Delivers both assessment AND draft document

**Uses agents:** All 5 agents + image-generation (if figures requested)

**Note:** Will ask about figure generation preference (same as section 3)

---

### 5. IP Strategy Advice

"Should I patent this or keep it as a trade secret?"

**What it does:**
1. Analyzes protection options
2. Considers timing, costs, enforceability
3. Recommends approach with rationale

**Uses agents:** IP Strategy Advisor

---

### 6. Claims Only

"Draft patent claims for my wireless charging system"

**What it does:**
1. Understands the invention
2. Drafts independent and dependent claims
3. Explains claim strategy

**Uses agents:** Claims Strategist

---

### 7. Design-Around Analysis (Freedom to Operate)

"How can I get around this patent?" / "Analyze this patent and find ways to design around it"

**Use the `AskUserQuestion` tool for each question below.**

**Q1: Patent**
> "I'll analyze that patent and identify design-around opportunities!
> 
> **⚠️ Note:** This is informational only, not legal advice.
> 
> First — **which patent do you want to analyze?**
> 
> *(Provide patent number, URL, or describe the patented technology)*"

*Wait for response.*

**Q2: Your Goal**
> "What's your **goal**?
> 
> - Build a competing product
> - Improve on the patented technology
> - Avoid infringement in my own invention
> - Understand the patent landscape
> - Or describe your specific situation"

*Wait for response.*

**Q3: Report Depth**
> "How **detailed** should the analysis be?
> 
> - Quick overview — key claims and obvious gaps
> - Standard analysis — claims breakdown + design alternatives
> - Deep dive — comprehensive FTO report with multiple strategies"

*Wait for response.*

**What it does:**
1. Analyzes the patent's claims (the legal boundaries)
2. Identifies the **scope** of what's protected
3. Finds **gaps** in the claims (what's NOT covered)
4. Suggests **design alternatives** that achieve similar goals without infringing
5. Searches for **prior art** that might invalidate or narrow the patent
6. Provides a **risk assessment** for each alternative

**Output: Design-Around Report**
```
## Patent Analysis: [Patent Number]

### 1. Patent Overview
- Title, assignee, filing date, status
- Core invention summary

### 2. Claim Analysis
- Independent claims breakdown
- Claim elements and limitations
- What's actually protected vs. assumed

### 3. Design-Around Opportunities
| Alternative | How It Differs | Risk Level | Feasibility |
|-------------|----------------|------------|-------------|
| Option A    | Changes X to Y | Low        | High        |
| Option B    | Omits element Z| Medium     | Medium      |

### 4. Prior Art That May Narrow Scope
- Patents/publications that predate this patent
- Potential invalidity arguments

### 5. Recommended Strategy
- Safest approach
- Cost/benefit analysis
- Next steps

### ⚠️ Disclaimer
This is informational guidance only. Consult a patent attorney.
```

**Uses agents:** Prior Art Searcher, Claims Strategist, IP Strategy Advisor, Patentability Analyst

---

## Specialized Agents

Each agent has a specific focus. The skill uses whichever are needed:

| Agent | What It Does |
|-------|--------------|
| **Prior Art Searcher** | Finds existing patents, publications, products |
| **Patentability Analyst** | Assesses novelty, non-obviousness, utility |
| **Claims Strategist** | Drafts patent claims with fallback positions |
| **IP Strategy Advisor** | Advises on patent vs trade secret, timing, costs |
| **Patent Drafter** | Writes complete patent applications |

---

## Output Formats

### Patentability Assessment
```json
{
  "invention": "Title",
  "patentability": "Likely/Questionable/Unlikely",
  "novelty": "Strong/Moderate/Weak",
  "non_obviousness": "Strong/Moderate/Weak",
  "closest_prior_art": ["Patent 1", "Patent 2"],
  "key_differences": "What makes this different",
  "concerns": ["Concern 1"],
  "recommendation": "File provisional / Trade secret / etc.",
  "estimated_cost": "$X,XXX - $XX,XXX"
}
```

### Full Patent Draft
Complete patent application with all sections (Title, Background, Description, Claims, Abstract) in Markdown format, plus generated technical drawings.

**Output files:**
- `patent_application.pdf` - **Final PDF with all figures embedded**
- `patent_application.md` - Editable source document
- `patent_fig_1.png` - Perspective/overview view
- `patent_fig_2.png` - Cross-section or mechanism view
- `patent_fig_3.png` - Block diagram or flowchart
- Additional figures as needed

---

## Integration with Other Skills

| Skill | Use Case |
|-------|----------|
| `image-generation` | **Generates patent figures** (technical drawings) |
| `product-engineer-agent` | Identify patentable aspects of product |
| `competitive-intel-agent` | Understand competitor IP landscape |
| `market-researcher-agent` | Assess commercial value of patent |

---

## Agent Files

| Agent | File |
|-------|------|
| Prior Art Searcher | `agents/prior-art-searcher.md` |
| Patentability Analyst | `agents/patentability-analyst.md` |
| Claims Strategist | `agents/claims-strategist.md` |
| IP Strategy Advisor | `agents/ip-strategy-advisor.md` |
| Patent Drafter | `agents/patent-drafter.md` |

---

## Important Limitations

1. **Not Legal Advice** - This is informational guidance only
2. **Not a Full Search** - A complete prior art search requires professional tools
3. **No Attorney-Client Privilege** - Conversations are not privileged
4. **May Miss References** - Prior art search is never exhaustive
5. **Laws Change** - IP law varies by jurisdiction and changes over time

**Always consult a licensed patent attorney for actual legal matters.**

---

## Example Prompts

**Analyze a product:**
> "Look at the Dyson bladeless fan and tell me if I could patent a similar concept with my modifications"

**Check patentability:**
> "I invented a new way to charge phones wirelessly from across the room. Is it patentable?"

**Prior art search:**
> "Search for prior art on foldable drone designs"

**Full patent from idea:**
> "I have an idea for a self-watering planter. Create a complete patent application for it."

**Draft patent:**
> "Write a patent for my new compression algorithm"

**Analyze then draft:**
> "Analyze my invention for patentability, then draft the full patent application"

**Strategy question:**
> "Should I patent my invention or keep it as a trade secret?"

**Claims only:**
> "Draft patent claims for my modular furniture system"

**Specific comparison:**
> "How does my invention differ from US Patent 10,123,456?"

**Design-around analysis:**
> "How can I get around this patent? [provide patent number or URL]"

**Freedom to operate:**
> "Analyze US Patent 9,876,543 and find ways to design around it for my competing product"

**Patent gap analysis:**
> "What's NOT covered by Apple's patent on [technology]? I want to build something similar legally"
