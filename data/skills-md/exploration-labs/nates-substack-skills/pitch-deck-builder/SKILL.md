---
name: pitch-deck-builder
description: Comprehensive pitch deck creation with conversational discovery, narrative structuring, and context-aware chunking strategies. This skill should be used when users request help creating pitch decks, investor presentations, fundraising decks, or startup presentations. It guides through narrative development, data collection, and professional slide creation.
license: MIT
---

# Pitch Deck Builder

This skill provides a comprehensive workflow for creating professional pitch decks through conversational discovery, narrative structuring, and technical execution with context-aware best practices.

## Overview

Creating effective pitch decks requires balancing compelling storytelling with strategic information architecture. This skill guides the process from initial concept through final presentation, with special attention to:

- Conversational discovery to extract key business insights
- Narrative arc construction that resonates with target audiences
- Modern, uncluttered slide design that emphasizes clarity
- Token-aware chunking strategies to prevent context window overflow
- Iterative refinement based on presentation goals

## When to Use This Skill

Use this skill when:
- Creating investor pitch decks or fundraising presentations
- Building sales decks or business presentations
- Developing product launch presentations
- Crafting founder or team introductions
- Any scenario requiring strategic narrative presentation of business concepts

## Core Workflow

### Phase 1: Discovery Interview

**CRITICAL**: Before creating any slides, conduct a structured discovery interview to understand the pitch requirements. This prevents wasted effort and ensures the final deck aligns with user goals.

The discovery process should be conversational and adaptive, not a rigid questionnaire. Ask 2-3 questions at a time, then build on responses naturally. Focus on understanding the story before collecting details.

#### Stage 1: Foundation (3-5 questions)

Start with high-level questions to understand the pitch context:

1. **Pitch Type & Audience**: "What type of pitch deck are you creating, and who's the primary audience? For example: pre-seed investors, enterprise customers, strategic partners, internal stakeholders, etc."

2. **Core Narrative**: "In 2-3 sentences, what's the most compelling story you want to tell? Think about the transformation or opportunity you're presenting."

3. **Stage & Goals**: "What stage is your company/product at, and what's your goal for this deck? For example: raising $2M seed round, closing enterprise deals, securing partnerships, etc."

4. **Key Constraints**: "Are there any specific constraints I should know about? For example: must be under 15 slides, needs to address specific concerns, follows a particular format, etc."

#### Stage 2: Business Fundamentals (5-8 questions)

Based on initial responses, dive into the business model and value proposition:

1. **Problem Definition**: "Describe the problem you're solving. What pain point exists today, and how acute is it for your target customers?"

2. **Solution Approach**: "What's your solution, and why is it uniquely positioned to solve this problem? What's your unfair advantage?"

3. **Market Opportunity**: "What's the market size and your addressable segment? Are there any particularly compelling market dynamics or timing factors?"

4. **Business Model**: "How do you make money? What are your unit economics or revenue model?"

5. **Traction & Validation**: "What traction or validation do you have? This could be revenue, users, partnerships, pilot results, etc."

6. **Competition**: "Who are your main competitors or alternatives, and how are you differentiated?"

#### Stage 3: Narrative Elements (4-6 questions)

Gather the elements needed to craft a compelling narrative:

1. **Founding Story**: "Is there a compelling founding story or insight that led to creating this company/product?"

2. **Customer Evidence**: "Do you have any customer quotes, case studies, or success stories that illustrate your impact?"

3. **Vision**: "What's your long-term vision? Where do you see this in 3-5 years?"

4. **Team**: "What makes your team uniquely qualified? Any notable backgrounds, expertise, or relevant achievements?"

5. **Milestones**: "What are your key milestones or roadmap items for the next 12-18 months?"

#### Stage 4: Data & Materials (3-4 questions)

Collect specific data points and existing materials:

1. **Quantitative Data**: "What are your key metrics or numbers? For example: revenue, growth rate, user count, retention, CAC/LTV, margins, etc."

2. **Visual Materials**: "Do you have any existing materials I should incorporate? For example: logos, brand colors, product screenshots, team photos, existing slides, etc."

3. **Must-Include Elements**: "Are there any specific slides, data points, or messages that absolutely must be included?"

#### Context Window Management Strategy

**BEFORE proceeding to Phase 2**, assess the context implications:

1. **Calculate estimated token usage**:
   - Discovery interview: ~2,000-4,000 tokens
   - Narrative planning: ~1,500-3,000 tokens
   - Slide content creation: ~500-800 tokens per slide
   - Technical execution: ~3,000-5,000 tokens
   - Base overhead: ~2,000 tokens

2. **Identify chunking needs**:
   - If deck > 15 slides: **STRONGLY RECOMMEND** chunking strategy
   - If deck > 20 slides: **REQUIRE** chunking strategy
   - If user provides extensive existing content: Consider chunking

3. **Propose chunking approach** (if needed):
   "Based on your requirements, we're looking at approximately [X] slides. To maintain quality and avoid context constraints, I recommend we build this deck in [2-3] phases:
   
   - **Phase 1**: Opening slides (Cover, Problem, Solution, Product) - slides 1-[X]
   - **Phase 2**: Business slides (Market, Business Model, Traction, Competition) - slides [X]-[Y]  
   - **Phase 3**: Closing slides (Team, Financials, Milestones, Ask) - slides [Y]-[Z]
   
   We'll create each phase completely, then combine them at the end. This ensures every slide gets proper attention and design quality. Does this approach work for you?"

4. **Document phase boundaries**: If using chunking, clearly document in narrative plan which slides belong to which phase

### Phase 2: Narrative Planning

After completing discovery, create a detailed narrative plan that serves as the blueprint for the deck.

#### Step 1: Determine Slide Sequence

Based on pitch type and discovery insights, recommend an appropriate slide sequence. Common structures:

**Standard Investor Pitch (12-15 slides)**:
1. Cover slide (Company name, tagline, contact)
2. Problem (The pain point)
3. Solution (Your approach)
4. Product/Demo (How it works)
5. Market Opportunity (TAM/SAM/SOM)
6. Business Model (Revenue streams)
7. Traction (Metrics, growth)
8. Competition (Landscape, differentiation)
9. Go-to-Market (Distribution, customer acquisition)
10. Team (Founders, key hires)
11. Financials (Projections, unit economics)
12. Milestones (12-18 month roadmap)
13. Funding Ask (Amount, use of funds)
14. Vision (Long-term impact)
15. Contact/Thank You

**Product Pitch (8-12 slides)**:
1. Cover
2. Problem
3. Solution Overview
4. Product Details/Demo
5. Benefits & ROI
6. Customer Success Stories
7. Competitive Advantage
8. Pricing/Packages
9. Implementation
10. Team/Company
11. Next Steps
12. Contact

**CRITICAL**: Adapt the sequence based on discovery insights. If the user has exceptional traction, move that slide earlier. If the team is the strongest asset, elevate it. The narrative should build momentum toward the most compelling elements.

#### Step 2: Create Detailed Content Outline

For each slide, document:

1. **Slide title**: Clear, assertive statement (not generic labels)
2. **Core message**: The single most important point this slide must convey
3. **Supporting points**: 2-4 key facts, data points, or arguments (bullet form)
4. **Visual strategy**: How this slide should be visually presented
5. **Speaker notes**: 1-3 sentences the presenter should say about this slide
6. **Data requirements**: Specific numbers, percentages, or facts needed

Example outline entry:
```
Slide 7: "We've Grown 40% Month-Over-Month for 6 Months"

Core message: Our consistent growth demonstrates product-market fit and validates our approach

Supporting points:
- 10,000+ active users, up from 500 six months ago
- 85% of users remain active after 30 days (industry benchmark: 25%)
- NPS score of 72 (promoter-heavy user base)
- Zero paid marketing spend - all organic and referral growth

Visual strategy: Large growth chart showing MoM trajectory, with key metrics callouts around it

Speaker notes: "This isn't a spike - it's sustained, compounding growth driven by genuine product love. Our users are becoming our sales team, and retention numbers show they're staying because we're solving a real problem for them."

Data requirements: Monthly user count for last 6 months, retention cohort data, NPS score
```

#### Step 3: Validate Narrative Arc

Review the complete outline and validate:

1. **Opening strength**: Do the first 3 slides hook attention and establish credibility?
2. **Logical flow**: Does each slide build naturally to the next?
3. **Peak placement**: Is the strongest material positioned for maximum impact (typically slides 6-9)?
4. **Emotional resonance**: Are there moments of human connection (customer stories, founding insight, vision)?
5. **Objection handling**: Are likely concerns addressed before they become barriers?
6. **Clear ask**: Is the call-to-action unambiguous and compelling?

Present the complete narrative outline to the user for approval before proceeding to design. Make it easy to review by presenting in a clear, scannable format.

### Phase 3: Design & Technical Execution

Once the narrative plan is approved, execute the technical creation using the pptx skill and html2pptx workflow.

#### Design Principles

**CRITICAL**: Pitch decks must balance professionalism with visual impact. Follow these principles:

1. **Whitespace is strategic**: Each slide should have 40-60% whitespace. Crowded slides lose impact.

2. **One idea per slide**: If a slide tries to communicate multiple ideas, split it into multiple slides.

3. **Typography hierarchy**:
   - Headlines: Large (36-48pt), bold, assertive statements
   - Body text: Readable (18-24pt), limited to 3-5 bullets maximum
   - Data callouts: Extra large (48-72pt) for key numbers
   - Avoid paragraphs: Use bullet points, but even better - use short phrases

4. **Color strategy**:
   - Primary: Brand color for key elements and data visualization
   - Accent: Complementary color for highlights and emphasis  
   - Neutral: Dark gray (not black) for body text, light gray for backgrounds
   - Limit palette to 3-4 colors total

5. **Data visualization**:
   - Prefer charts over tables when showing trends
   - Use large, simple charts with clear labels
   - Highlight the key insight (annotate charts with the "so what?")
   - Remove chart junk - no 3D effects, excessive gridlines, or decorative elements

6. **Layout patterns**:
   - Full-bleed: Image or color background with text overlay (cover, section dividers)
   - Two-column: Text on left, visual on right (most content slides)
   - Centered: Single key message or data point (impact slides)
   - Grid: Multiple items of equal importance (team, customers, features)

#### Technical Implementation

**IMPORTANT**: Read `/mnt/skills/public/pptx/SKILL.md` completely before beginning slide creation. The pptx skill contains critical requirements for html2pptx workflow.

Follow this execution sequence:

1. **Read pptx skill documentation**: `view /mnt/skills/public/pptx/SKILL.md` (no range limits - read entire file)

2. **Read html2pptx documentation**: `view /mnt/skills/public/pptx/html2pptx.md` (no range limits - read entire file)

3. **Install html2pptx if needed**: Verify installation with `npm list -g @ant/html2pptx` and install if necessary

4. **Create shared CSS file**: Define CSS variables for colors, typography, and spacing that will be used across all slides

5. **Create HTML files for each slide**:
   - Use proper dimensions (960px × 540px for 16:9)
   - Embed shared CSS in `<style>` tags
   - Use semantic HTML (`<h1>`, `<p>`, `<ul>`, etc.)
   - Use row/col/fit classes for layout (NOT flexbox)
   - Apply CSS variables consistently
   - Include `class="placeholder"` for chart/table areas

6. **Create conversion script**: Write JavaScript to convert HTML to PPTX using html2pptx library and PptxGenJS

7. **Execute and validate**: Run the conversion script and generate thumbnail grid for visual validation

8. **Iterate if needed**: Fix any layout issues, text overflow, or visual problems identified in thumbnails

#### Chunking Execution Strategy

If using a multi-phase approach (recommended for >15 slides):

1. **Phase execution**:
   - Build Phase 1 completely (HTML + PPTX generation + validation)
   - Save Phase 1 output to `/mnt/user-data/outputs/`
   - Begin new conversation or clear context
   - Load Phase 1 PPTX and narrative plan
   - Build Phase 2 (append to existing PPTX)
   - Repeat for remaining phases

2. **Phase handoff checklist**:
   - [ ] Save phase PPTX file to outputs
   - [ ] Save narrative plan for next phase
   - [ ] Save CSS file for design consistency
   - [ ] Document any design decisions or patterns established
   - [ ] Note current slide number for next phase

3. **Combination approach**:
   - After all phases complete, combine using Python-PPTX or manual merge
   - Validate slide numbering and transitions
   - Generate final thumbnail grid
   - Check for design consistency across all slides

### Phase 4: Refinement & Delivery

After initial creation, support iterative improvement:

1. **Visual review**: Generate and examine thumbnail grid for layout issues

2. **Content refinement**: Offer to adjust messaging, data presentation, or narrative flow based on feedback

3. **Design iteration**: Make styling adjustments, color changes, or layout modifications

4. **Export preparation**: Ensure final PPTX is in `/mnt/user-data/outputs/` with clear filename

5. **Usage guidance**: Provide brief tips for presenting the deck effectively

## Best Practices

### Discovery Quality
- Listen more than prescribe - let the user's story emerge naturally
- Ask "why" and "so what" to uncover deeper insights
- Notice what the user emphasizes - these are often the strongest narrative elements
- Validate understanding by reflecting back key points

### Narrative Construction
- Start with why, not what - establish emotional connection before details
- Use assertive slide titles that make claims, not generic labels ("We're Growing 40% Monthly" not "Traction")
- Place the strongest material in the middle third of the deck (slides 6-9 in a 15-slide deck)
- End with clarity on the ask and vision for impact

### Design Execution
- When in doubt, remove elements rather than add them
- Use data visualization to replace bullet points whenever possible
- Test readability by viewing slides at thumbnail size - key points should still be clear
- Maintain consistent spacing, alignment, and typography throughout

### Context Management
- Propose chunking early if deck will exceed 15 slides
- Document design decisions in CSS comments for phase consistency
- Save phase outputs immediately to prevent context loss
- Keep narrative plan accessible across phases

## Common Pitch Deck Types

### Investor Pitch (Pre-Seed/Seed)
- Focus: Team, problem, early traction
- Length: 12-15 slides
- Tone: Ambitious but realistic, founder-driven
- Key slides: Problem, solution, why now, founding story, early metrics

### Investor Pitch (Series A+)
- Focus: Growth metrics, business model, competitive moats
- Length: 15-18 slides  
- Tone: Data-driven, scalable, market-leading
- Key slides: Growth charts, unit economics, competitive landscape, market expansion

### Sales/Product Pitch
- Focus: Customer value, ROI, implementation
- Length: 10-15 slides
- Tone: Customer-centric, benefit-oriented, practical
- Key slides: Problem/pain point, solution benefits, customer success, pricing, next steps

### Partnership Pitch
- Focus: Strategic alignment, mutual value, capabilities
- Length: 8-12 slides
- Tone: Collaborative, strategic, win-win
- Key slides: Company overview, strategic fit, proposed partnership model, case for collaboration

## References

For additional guidance on pitch deck best practices, narrative construction, and data visualization, see:
- `references/pitch-deck-best-practices.md` - Comprehensive guide to effective pitch decks
- `references/data-visualization-guide.md` - Chart types, design patterns, and storytelling with data
- `references/narrative-frameworks.md` - Story structures and persuasion techniques

## Technical Dependencies

This skill leverages the pptx skill for presentation creation. Ensure the following are available:
- pptx skill at `/mnt/skills/public/pptx/`
- html2pptx library (installed via npm)
- python-pptx and related dependencies

All technical execution should follow the workflows documented in `/mnt/skills/public/pptx/SKILL.md`.
