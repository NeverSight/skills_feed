---
name: product-engineer-agent
description: >
  Use this skill to design new products, iterate on product ideas, or develop product specifications.
  Triggers: "design product", "new product idea", "product concept", "product development",
  "product spec", "iterate on product", "product design", "invention", "prototype spec",
  "product requirements", "product engineering", "develop product"
  Outputs: Product specification, BOM estimate, feature breakdown, differentiation analysis.
---

# Product Engineer Agent

Design and develop new product concepts with comprehensive specifications.

**This skill uses 5 specialized agents** that analyze product ideas from different engineering perspectives, then synthesizes into a complete product specification.

## What It Produces

| Output | Description |
|--------|-------------|
| **Product Spec** | Complete product specification document |
| **Feature Matrix** | Prioritized feature list with rationale |
| **BOM Estimate** | Bill of materials with rough cost estimates |
| **Differentiation** | How it differs from existing products |
| **Next Steps** | Recommended path to prototype/production |
| **Concept Renders** | Product visualization images (via image-generation) |
| **Engineering Drawings** | Exploded views, cross-sections, assembly diagrams |

## Prerequisites

- `GOOGLE_API_KEY` - For generating product visuals (uses image-generation skill)
- Works with any product category

## Workflow

### Step 1: Gather Product Idea (REQUIRED)

⚠️ **DO NOT skip this step. Use interactive questioning — ask ONE question at a time.**

#### Question Flow

⚠️ **Use the `AskUserQuestion` tool for each question below.** Do not just print questions in your response — use the tool to create interactive prompts with the options shown.

**Q1: Problem**
> "I'll help you design this product! First — **what problem does it solve?**
> 
> *(The core user need)*"

*Wait for response.*

**Q2: User**
> "Who is the **target user**?
> 
> *(Who will use this product?)*"

*Wait for response.*

**Q3: Features**
> "Any **must-have features** or key requirements?
> 
> *(Or say 'help me figure it out')*"

*Wait for response.*

**Q4: Constraints**
> "Any **constraints** to consider?
> 
> - Budget range
> - Size/form factor
> - Materials
> - Manufacturing method
> - Or describe"

*Wait for response.*

**Q5: Visuals**
> "Do you want me to **generate visuals**?
> 
> - 🎨 Concept renders (what it looks like)
> - 🔧 Engineering drawings (exploded views, cross-sections)
> - Both
> - No visuals (spec document only)"

*Wait for response.*

#### Quick Reference

| Question | Determines |
|----------|------------|
| Problem | Core value proposition |
| User | User research focus |
| Features | Feature prioritization |
| Constraints | Manufacturing and design boundaries |
| Visuals | Whether to generate renders/drawings |

**Parse visual preferences:**
- "yes", "visuals", "show me", "render", "drawings" → Generate all visuals
- "concept only" → Just concept render + lifestyle
- "engineering only" → Just exploded/technical views
- "no visuals" or not mentioned → Skip visual generation
- Unclear → Default to generating visuals (they add value)

---

### Step 2: Run Specialized Engineering Agents in Parallel

Deploy 5 agents, each analyzing from a different perspective:

#### Agent 1: Industrial Designer
Focus: Form, ergonomics, aesthetics, user interaction
```
Consider:
- Physical form factor and dimensions
- Ergonomics and human factors
- Visual aesthetics and brand expression
- User interaction points (buttons, displays, etc.)
- Packaging and unboxing experience
```

#### Agent 2: Mechanical Engineer
Focus: How it works, materials, mechanisms
```
Consider:
- Core mechanism / how it functions
- Materials selection (strength, weight, cost)
- Manufacturing feasibility
- Durability and lifecycle
- Assembly and serviceability
```

#### Agent 3: User Researcher
Focus: User needs, pain points, usability
```
Consider:
- User journey with the product
- Pain points addressed
- Potential usability issues
- Onboarding and learning curve
- Accessibility considerations
```

#### Agent 4: Manufacturing Advisor
Focus: Feasibility, cost, production
```
Consider:
- Manufacturing methods (injection molding, CNC, etc.)
- Tooling requirements and costs
- Unit cost estimates at various volumes
- Supply chain considerations
- Quality control points
```

#### Agent 5: Innovation Scout
Focus: Existing solutions, patents, differentiation
```
Consider:
- Similar products in market
- Patent landscape (potential conflicts)
- Unique differentiators
- Technology trends to leverage
- Blue ocean opportunities
```

---

### Step 3: Synthesize into Product Specification

Combine all agent outputs into a structured specification:

```json
{
  "product": {
    "name": "Product Name",
    "tagline": "One-line description",
    "problem_solved": "Core problem it addresses",
    "target_user": "Who it's for",
    "category": "Product category"
  },
  "design": {
    "form_factor": "Physical description",
    "dimensions": "L x W x H",
    "weight": "Estimated weight",
    "materials": ["Material 1", "Material 2"],
    "colors": ["Primary options"],
    "key_interactions": ["How users interact with it"]
  },
  "features": {
    "must_have": [
      {"feature": "Feature 1", "rationale": "Why it's essential"}
    ],
    "should_have": [
      {"feature": "Feature 2", "rationale": "High value add"}
    ],
    "could_have": [
      {"feature": "Feature 3", "rationale": "Nice to have"}
    ]
  },
  "technical": {
    "mechanism": "How it works",
    "power_source": "Battery/plug/manual/etc.",
    "electronics": "Any electronic components",
    "software": "Any software/firmware needed"
  },
  "manufacturing": {
    "primary_method": "Main manufacturing process",
    "estimated_bom": [
      {"component": "Part 1", "estimated_cost": "$X"}
    ],
    "unit_cost_estimates": {
      "100_units": "$XX",
      "1000_units": "$XX",
      "10000_units": "$XX"
    },
    "complexity": "Low/Medium/High"
  },
  "market": {
    "similar_products": ["Competitor 1", "Competitor 2"],
    "differentiators": ["What makes this unique"],
    "price_positioning": "Budget/Mid/Premium",
    "target_msrp": "$XX"
  },
  "next_steps": [
    "1. Validate with potential users",
    "2. Create detailed CAD model",
    "3. Build first prototype",
    "4. Patent search (if applicable)"
  ]
}
```

---

### Step 4: Generate Product Visuals (If Requested)

**Only generate visuals if user requested them in Step 1.**

If user wants visuals, generate using the `image-generation` skill:

| Visual Type | When to Generate |
|-------------|------------------|
| **Concept Render** | User said "yes", "visuals", "concept", or "both" |
| **Lifestyle/Context** | User said "yes", "visuals", "concept", or "both" |
| **Exploded View** | User said "engineering", "assembly", "exploded", or "both" |
| **Cross-Section** | User said "engineering" AND product has internal mechanism |

**From Industrial Designer:**
- `product_concept.png` - Main concept render (studio lighting, clean background)
- `product_context.png` - Product in-use/lifestyle shot

**From Mechanical Engineer:**
- `product_exploded.png` - Exploded view showing all components
- `product_section.png` - Cross-section (if internal mechanism is key)

**Visual Generation Order:**
1. Concept render first (shows overall design)
2. In-context shot (shows usage)
3. Exploded view (shows engineering)
4. Cross-section (if needed)

**If user didn't request visuals:** Skip to Step 5 with spec document only.

---

### Step 5: Deliver Complete Package

**Delivery message (with visuals):**

"✅ Product design complete!

**Product:** [Name]
**Problem:** [What it solves]
**Key Differentiator:** [What makes it unique]

**Estimated unit cost:** $XX at 1,000 units
**Suggested MSRP:** $XX

**Generated visuals:**
- Concept render ✓
- Lifestyle/context shot ✓
- Exploded assembly view ✓

**Next steps:**
1. [First recommended action]
2. [Second recommended action]

**Want me to:**
- Deep dive on any section?
- Generate additional views or angles?
- Explore alternative designs?
- Estimate costs for different volumes?
- Compare to specific competitors?"

---

**Delivery message (spec only, no visuals):**

"✅ Product specification complete!

**Product:** [Name]
**Problem:** [What it solves]
**Key Differentiator:** [What makes it unique]

**Estimated unit cost:** $XX at 1,000 units
**Suggested MSRP:** $XX

**Next steps:**
1. [First recommended action]
2. [Second recommended action]

**Want me to:**
- **Generate visuals?** (concept renders, engineering drawings)
- Deep dive on any section?
- Explore alternative designs?
- Estimate costs for different volumes?"

---

## Integration with Other Skills

This skill works well with:

| Skill | Use Case |
|-------|----------|
| `image-generation` | **Generates concept renders and engineering drawings** |
| `brand-research-agent` | Ensure product fits brand guidelines |
| `patent-lawyer-agent` | Check patentability and draft patents |
| `market-researcher-agent` | Validate market opportunity |
| `pitch-deck-agent` | Create investor presentation |
| `media-utils` | **Generate PDF report** from product spec |

---

## Generate PDF Report

After completing the product specification, offer to generate a PDF:

> "Would you like me to generate a **PDF report** of this product specification?"

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/media-utils/scripts/report_to_pdf.py \
  --input product_spec.md \
  --output product_spec.pdf \
  --title "Product Specification" \
  --style technical
```

---

## Agents

| Agent | File | Focus |
|-------|------|-------|
| Industrial Designer | `industrial-designer.md` | Form, aesthetics, UX |
| Mechanical Engineer | `mechanical-engineer.md` | Function, materials |
| User Researcher | `user-researcher.md` | Needs, usability |
| Manufacturing Advisor | `manufacturing-advisor.md` | Cost, feasibility |
| Innovation Scout | `innovation-scout.md` | Competition, patents |

---

## Output Files

When generating a complete product design, you'll receive:

```
product_spec.md           ← Complete specification document
product_concept.png       ← 3D concept render
product_context.png       ← Lifestyle/in-use shot
product_exploded.png      ← Exploded assembly view
product_section.png       ← Cross-section (if applicable)
```

---

## Example Prompts

**Basic:**
> "Design a new portable phone charger that's more convenient"

**With context:**
> "I want to create a kitchen gadget that helps with meal prep. Target audience is busy parents. Budget under $30 retail."

**Iteration:**
> "Take my existing product idea and suggest improvements: [description]"

**Competitive:**
> "Design something better than [competitor product]"

**With visuals:**
> "Design a smart water bottle and show me what it would look like"

**Engineering focus:**
> "Design a modular desk organizer and show me the exploded assembly view"
