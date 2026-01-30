---
name: strategic-planning-manager
description: Organizational strategic planning for K-12 school districts using a hybrid CoSN/research-backed 7-phase process
triggers:
  - "strategic planning"
  - "district strategic plan"
  - "k-12 strategic planning"
  - "school district planning"
  - "strategic plan"
  - "SWOT analysis"
  - "practical vision"
  - "strategic directions"
  - "strategic retreat"
  - "organizational planning"
allowed-tools:
  - Read
  - Write
  - Bash
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - WebSearch
  - mcp__obsidian-vault__create_vault_file
  - mcp__obsidian-vault__get_vault_file
  - mcp__obsidian-vault__search_vault_simple
version: 1.0.0
---

# Strategic Planning Manager Skill

Organizational strategic planning system for K-12 school districts, combining the CoSN Technology of Participation (ToP) methodology with research-backed best practices from ThoughtExchange, Education Elements, Hanover Research, and AASA.

> **Quick Start:** New to this skill? Read `guides/quick-start.md` first for practical entry points and common workflows.

> **Note:** For personal life/work strategic planning, use the `personal-strategic-planning` skill instead.

## When to Activate

This skill activates when the user requests:

**Full Strategic Planning Process:**
- "Help me create a strategic plan for our district"
- "We need to do strategic planning"
- "Let's start the district strategic planning process"
- "Facilitate our strategic planning retreat"

**Phase-Specific Work:**
- "Analyze our survey data for strategic planning"
- "Help me process focus group transcripts"
- "Generate a SWOT analysis"
- "Create a practical vision"
- "Identify underlying contradictions"
- "Define strategic directions"
- "Build our implementation timeline"

**Plan Update Mode:**
- "Update our existing strategic plan"
- "It's time to refresh our strategic plan"
- "Annual strategic plan review"

## Skill Modes

### Mode 1: Full Process Guide
Walk through all 7 phases sequentially, prompting for data inputs and facilitating each step.
- Best for: New strategic plans, comprehensive planning retreats

### Mode 2: Phase-Specific Entry
Jump directly into any specific phase with appropriate inputs.
- Best for: Working on one component, picking up where you left off

### Mode 3: Data Analysis Only
Process surveys, transcripts, and documents without running the full planning process.
- Best for: Pre-work, discovery phase, feeding data into existing processes

### Mode 4: Plan Update
Start from an existing plan, analyze progress, update for a new cycle.
- Best for: Annual reviews, mid-cycle adjustments, refresh cycles

---

## The 7-Phase Strategic Planning Process

Based on CoSN's Technology of Participation (ToP) methodology enhanced with K-12 best practices.

### Phase 1: Discovery & Data Collection
**AI Role:** Primary executor | **Human Role:** Data provider

**Purpose:** Gather and synthesize all available data about the current state.

**Data Sources Processed:**
- Survey data (CSV, JSON, Excel)
- Focus group transcripts (text files)
- Existing strategic plan documents
- Board meeting minutes
- Community feedback compilations
- Demographic and enrollment data

**AI Actions:**
1. Ingest and validate data files
2. Extract themes using NLP analysis
3. Identify sentiment patterns
4. Cross-reference findings across sources
5. Generate initial theme clusters
6. Create Discovery Summary Report

**Available Scripts:**
```bash
# Analyze survey data
uv run skills/strategic-planning-manager/scripts/analyze_surveys.py \
  --input survey_results.csv \
  --output-dir ./discovery

# Process focus group transcripts
uv run skills/strategic-planning-manager/scripts/process_transcripts.py \
  --input-dir ./transcripts \
  --output ./discovery/transcript-themes.json

# Generate combined discovery report
uv run skills/strategic-planning-manager/scripts/generate_discovery.py \
  --data-dir ./discovery \
  --output ./outputs/discovery-report.md
```

**Outputs:**
- Discovery Summary Report (`templates/discovery-report.md`)
- Theme Analysis with supporting evidence
- Stakeholder sentiment analysis
- Initial data-driven SWOT draft

**Interview Questions (for context):**
1. "What data sources do you have available?" (surveys, transcripts, documents)
2. "What's the timeframe for the data?" (when collected, relevance)
3. "Who are the key stakeholder groups represented?"
4. "What do you already know/suspect about the findings?"

---

### Phase 2: Environmental Analysis (SWOT)
**AI Role:** Synthesis and preparation | **Human Role:** Validation and refinement

**Purpose:** Develop comprehensive understanding of internal and external factors.

**AI Actions:**
1. Generate SWOT from discovery data
2. Create "Where Will We Invest?" analysis (Strengths × Opportunities)
3. Create "What's Holding Us Back?" analysis (Weaknesses focus)
4. Prepare briefing materials for human sessions

**Human Session Support:**
- Provide facilitator guide with session agenda
- Suggest small group discussion prompts
- Capture and organize human additions

**Outputs:**
- SWOT Analysis Matrix (`templates/swot-template.md`)
- Investment Priority Grid (S×O quadrant)
- Barriers Analysis (W focus)
- Facilitator Guide (`guides/phase2-swot-guide.md`)

**CoSN Format Reference:**
| Strengths | Weaknesses |
|-----------|------------|
| What we do well | What limits us |
| What others see as strengths | Where we're vulnerable |

| Opportunities | Threats |
|---------------|---------|
| External factors to leverage | External risks to navigate |
| Trends we can capitalize on | Competitive/regulatory concerns |

**Key Questions:**
- "Where Will We Invest?" (top S×O opportunities)
- "What's Holding Us Back?" (key weaknesses to address)

---

### Phase 3: Practical Vision Development
**AI Role:** Facilitation support | **Human Role:** Primary creator

**Purpose:** Define what success looks like 3 years from now through collaborative brainstorming.

**The CoSN Approach:**
1. **Individual brainstorming:** "What do we want to see in 3 years?"
2. **Small group sharing:** Combine and refine ideas
3. **Large group clustering:** Organize into 8-10 thematic columns
4. **Naming columns:** Give each vision cluster a descriptive title

**AI Support Actions:**
1. Provide vision prompts based on discovery themes
2. Suggest initial category groupings as ideas emerge
3. Capture and organize inputs in real-time
4. Ensure all voices are represented

**Vision Categories (Common in K-12):**
- Student Achievement & Learning
- Equity & Access
- Staff Quality & Development
- Community Engagement
- Technology & Innovation
- Facilities & Resources
- Safety & Wellness
- Fiscal Sustainability

**Outputs:**
- Practical Vision Matrix (`templates/practical-vision.md`)
- Vision statement narratives per category
- Facilitator Guide (`guides/phase3-vision-guide.md`)

**Matrix Format (CoSN slide 11 style):**
| Learning | Equity | Staff | Community | Technology | Facilities | Safety | Finance |
|----------|--------|-------|-----------|------------|------------|--------|---------|
| Vision items... | Vision items... | ... | ... | ... | ... | ... | ... |

---

### Phase 4: Underlying Contradictions
**AI Role:** Pattern identification | **Human Role:** Primary creator

**Purpose:** Identify the deep tensions (not just barriers) that must be resolved for the vision to be realized.

**Key Distinction:**
- **Barriers** = obstacles to remove
- **Contradictions** = tensions that need resolution, often involving trade-offs

**Examples of Contradictions:**
- "Need for innovation" vs "Risk aversion in district culture"
- "Desire for personalized learning" vs "Standardized testing requirements"
- "Staff wanting autonomy" vs "Need for consistent practices"

**AI Actions:**
1. Suggest potential contradictions based on discovery data
2. Help frame contradictions (not just barriers)
3. Organize and categorize as groups work
4. Identify patterns across stakeholder groups

**Human Session Support:**
1. Small group brainstorming of contradictions
2. Large group clustering and naming
3. Identification of root tensions

**Outputs:**
- Underlying Contradictions Matrix (`templates/contradictions.md`)
- Root tension analysis
- Facilitator Guide (`guides/phase4-contradictions-guide.md`)

**Matrix Format (CoSN slide 20 style):**
| Category | Contradiction | Impact on Vision |
|----------|---------------|------------------|
| Culture | [Tension description] | [Which vision areas affected] |
| Resources | [Tension description] | [Which vision areas affected] |

---

### Phase 5: Strategic Directions
**AI Role:** Synthesis support | **Human Role:** Decision making

**Purpose:** Define innovative actions that resolve contradictions and move toward the vision.

**Key Principle:**
Strategic directions are NOT just goals—they are the actions and approaches that will resolve the underlying contradictions while advancing the practical vision.

**AI Actions:**
1. Map contradictions to potential strategic directions
2. Suggest evidence-based actions from K-12 research
3. Ensure each direction addresses multiple contradictions
4. Connect directions to vision categories

**Human Session Support:**
1. Define 4-6 major strategic directions
2. Prioritize based on impact and feasibility
3. Assign preliminary ownership
4. Validate contradiction resolution

**Outputs:**
- Strategic Directions Framework (`templates/strategic-directions.md`)
- Direction-to-Contradiction mapping
- Direction-to-Vision alignment matrix
- Facilitator Guide (`guides/phase5-directions-guide.md`)

**Framework Format (CoSN slide 22 style):**
| Strategic Direction | Contradictions Addressed | Vision Categories Served |
|---------------------|--------------------------|--------------------------|
| [Direction 1] | [C1, C2, C3] | [Learning, Equity, Staff] |
| [Direction 2] | [C2, C4] | [Technology, Community] |

---

### Phase 6: Focused Implementation
**AI Role:** Structure and tracking | **Human Role:** Validation and commitment

**Purpose:** Translate strategic directions into concrete, time-bound implementation plans.

**The CoSN Three-Column Approach:**
For each strategic direction, define:
1. **Current Reality:** Where are we now?
2. **1-Year Accomplishments:** What will be true in 12 months?
3. **3-Year Outcomes:** What will be true at plan completion?

**AI Actions:**
1. Generate implementation framework structure
2. Create Current Reality → 1-Year → 3-Year tables
3. Suggest success indicators and metrics
4. Draft quarterly timeline for Year 1

**Human Session Support:**
1. Confirm current reality assessments
2. Commit to 1-year accomplishments
3. Define measurable success indicators
4. Assign ownership and accountability

**Outputs:**
- Focused Implementation Tables (`templates/focused-implementation.md`)
- First-Year Timeline (`templates/first-year-timeline.md`)
- Success Indicators Matrix
- Facilitator Guide (`guides/phase6-implementation-guide.md`)

**Implementation Table Format (CoSN slides 24-26 style):**
| Strategic Direction: [Name] |
|----------------------------|
| **Current Reality** | **1-Year Accomplishments** | **3-Year Outcomes** |
| [Where we are] | [What's true in 12 months] | [What's true in 36 months] |

**First-Year Timeline Format (CoSN slide 27 style):**
| Strategic Direction | Q1 | Q2 | Q3 | Q4 |
|---------------------|----|----|----|----|
| [Direction 1] | [Actions] | [Actions] | [Actions] | [Actions] |

---

### Phase 7: Plan Document Generation
**AI Role:** Primary executor | **Human Role:** Review and approval

**Purpose:** Compile all outputs into professional, stakeholder-ready documents.

**AI Actions:**
1. Compile all phase outputs into cohesive plan document
2. Generate executive summary for board presentation
3. Create stakeholder-specific versions (board, staff, community)
4. Build monitoring dashboard structure

**Outputs:**
- Full Strategic Plan Document (`templates/full-strategic-plan.md`)
- Executive Summary (`templates/executive-summary.md`)
- Board presentation outline
- Staff communication version
- Community-facing summary

**Document Structure:**
1. Executive Summary
2. Planning Process Overview
3. Discovery Findings
4. Environmental Analysis (SWOT)
5. Practical Vision
6. Underlying Contradictions
7. Strategic Directions
8. Implementation Plan
9. Year-One Timeline
10. Success Metrics & Monitoring
11. Appendices (data, methodology)

---

## Available Scripts

### Survey Analysis
```bash
uv run skills/strategic-planning-manager/scripts/analyze_surveys.py \
  --input data.csv \
  --format csv \
  --output-dir ./discovery
```

**Supported formats:** CSV, JSON, Excel (.xlsx, .xls)

**Analysis includes:**
- Response distribution statistics
- Sentiment analysis per question
- Theme extraction from open-ended responses
- Stakeholder group comparisons (if demographics provided)
- Word frequency and phrase analysis

### Transcript Processing
```bash
uv run skills/strategic-planning-manager/scripts/process_transcripts.py \
  --input-dir ./transcripts \
  --output ./discovery/transcript-themes.json
```

**Analysis includes:**
- Theme extraction using NLP
- Sentiment patterns
- Speaker/stakeholder attribution (if labeled)
- Quote extraction for evidence
- Cross-transcript pattern identification

### SWOT Generation
```bash
uv run skills/strategic-planning-manager/scripts/generate_swot.py \
  --discovery-dir ./discovery \
  --output ./outputs/swot-analysis.md
```

**Generates:**
- Data-driven SWOT matrix
- Supporting evidence citations
- Investment priority recommendations
- Barrier analysis

### Plan Synthesis
```bash
uv run skills/strategic-planning-manager/scripts/synthesize_plan.py \
  --work-dir ./planning \
  --output ./outputs/strategic-plan.md \
  --format full  # or 'executive', 'board', 'staff', 'community'
```

**Generates:**
- Complete strategic plan document
- Multiple stakeholder versions
- Executive summary
- Board presentation outline

---

## Facilitator Guides

Detailed guides for each human session:

| Guide | Purpose | Duration |
|-------|---------|----------|
| `phase1-discovery-guide.md` | Data collection interviews, survey design | Varies |
| `phase2-swot-guide.md` | SWOT workshop facilitation | 2-3 hours |
| `phase3-vision-guide.md` | Practical vision brainstorming | 3-4 hours |
| `phase4-contradictions-guide.md` | Contradiction identification | 2-3 hours |
| `phase5-directions-guide.md` | Strategic direction development | 3-4 hours |
| `phase6-implementation-guide.md` | Implementation planning | 3-4 hours |
| `retreat-agenda-2day.md` | Full 2-day retreat structure | 2 days |
| `retreat-agenda-condensed.md` | Condensed 1-day format | 1 day |

Each guide includes:
- Detailed agenda with timing
- Facilitator prompts and questions
- Small group and large group activities
- Materials needed
- Expected outputs
- Common challenges and solutions

---

## Data Storage (Obsidian)

Strategic plans are stored in the Obsidian vault:

```
Personal_Notes/Geoffrey/Strategic-Plans/
├── {District-Name}/
│   ├── {Year}-Strategic-Plan.md
│   ├── Discovery-Report.md
│   ├── SWOT-Analysis.md
│   ├── Practical-Vision.md
│   ├── Contradictions-Analysis.md
│   ├── Strategic-Directions.md
│   ├── Implementation-Plan.md
│   └── Facilitator-Guides/
│       └── [Generated guides for this district]
```

**Frontmatter:**
```yaml
---
type: strategic-plan
district: {District Name}
year: {YYYY}
phase: {1-7 or complete}
status: draft | in-progress | final
created: {date}
updated: {date}
---
```

---

## Common K-12 Strategic Themes

Pre-loaded from `config/k12-themes.yaml`:

| Theme | Prevalence | Key Metrics |
|-------|------------|-------------|
| Student Achievement | 90%+ | Test scores, graduation rates, college readiness |
| Equity & Access | 90% | Gap reduction, program access, representation |
| Staff Quality & Retention | 80% | Hiring, development, turnover rates |
| Parent/Community Engagement | 80% | Participation, satisfaction, partnerships |
| Facilities & Technology | 75% | Infrastructure, device ratios, connectivity |
| Fiscal Sustainability | 70% | Budget balance, reserves, cost efficiency |
| Social-Emotional Learning | Growing | SEL metrics, climate surveys, wellness |
| Safety & Security | Variable | Incident rates, preparedness, climate |

---

## Research Foundations

This skill synthesizes best practices from:

**ThoughtExchange 3 Models:**
- Plan on a Page
- VMOSA (Vision → Mission → Objectives → Strategies → Action Plan)
- Five-Step Model

**Education Elements (7 Steps):**
- Pre-Planning Assessment
- Community Engagement Strategy
- Strategic Planning Team Formation
- Build Common Understanding
- Design Solutions (prioritization matrix)
- Communication Planning
- Monitoring and Adaptation

**Hanover Research (5 Phases):**
- Discovery (surveys, benchmarking)
- Analysis (SWOT synthesis)
- Visioning (workshops)
- Goal Setting (SMART goals)
- Implementation Roadmap (KPIs)

**AASA 10-Step Framework:**
- Comprehensive district leadership approach
- Emphasis on board/superintendent buy-in
- Quarterly monitoring, annual evaluation

**ICA Technology of Participation (ToP):**
- ORID Method (Objective → Reflective → Interpretive → Decisional)
- Focused Conversation
- Consensus Workshop
- Strategic Planning Matrix

**CoSN Strategic Planning (Direct Experience):**
- Discovery Findings
- SWOT → Investment/Barriers
- Practical Vision (3-year, categorized)
- Underlying Contradictions
- Strategic Directions
- Focused Implementation (Current → 1-Year → 3-Year)
- First-Year Timeline

---

## Example Workflow

### Starting a New Strategic Plan

```
User: "Help me create a strategic plan for our district"

Geoffrey:
1. Ask which mode: Full Process, Phase-Specific, or Data Analysis
2. If Full Process:
   - Ask about available data (surveys, transcripts, existing docs)
   - Ask about timeline (retreat dates, board presentation date)
   - Ask about stakeholder groups to involve
3. Begin Phase 1: Discovery
   - Ingest provided data files
   - Generate Discovery Report
4. Continue through phases with appropriate AI/human balance
5. Generate final plan documents
6. Save to Obsidian vault
```

### Analyzing Survey Data Only

```
User: "I have survey results I need to analyze for our strategic planning"

Geoffrey:
1. Ask for data file(s) and format
2. Run analyze_surveys.py
3. Present findings:
   - Key themes
   - Stakeholder differences
   - Sentiment analysis
   - Suggested SWOT inputs
4. Ask if user wants to continue to SWOT generation
```

### Updating an Existing Plan

```
User: "We need to update our strategic plan for year 2"

Geoffrey:
1. Load existing plan from Obsidian
2. Ask about progress on Year 1 accomplishments
3. Collect new data/feedback
4. Identify what's on track, at risk, off track
5. Recommend adjustments to timeline/directions
6. Generate updated plan document
```

---

## Error Handling

**1. No data provided for discovery:**
- Offer to conduct discovery interviews directly
- Suggest data collection templates
- Proceed with qualitative input only

**2. Insufficient stakeholder representation:**
- Flag which groups are missing
- Recommend targeted data collection
- Note limitation in final report

**3. Conflicting stakeholder priorities:**
- Surface contradictions explicitly in Phase 4
- Use as input for strategic direction decisions
- Document minority viewpoints

**4. Unrealistic implementation timeline:**
- Flag capacity concerns
- Suggest prioritization/phasing
- Recommend reducing scope or extending timeline

**5. Plan update with no progress data:**
- Conduct progress interview
- Use qualitative assessment
- Note "self-reported" vs "measured" progress

---

## Version History

**v1.0.0** (2026-01-26)
- Initial release
- 7-phase CoSN/ToP methodology
- 4 skill modes (Full, Phase-Specific, Data Analysis, Update)
- Python scripts for data analysis
- Facilitator guides for human sessions
- Obsidian integration for plan storage
- K-12 themes and metrics library
- Research-backed framework synthesis
