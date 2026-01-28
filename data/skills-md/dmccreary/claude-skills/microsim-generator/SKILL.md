---
name: microsim-generator
description: Creates interactive educational MicroSims using the best-matched JavaScript library (p5.js, Chart.js, Plotly, Mermaid, vis-network, vis-timeline, Leaflet, Venn.js). Analyzes user requirements to route to the appropriate visualization type and generates complete MicroSim packages with HTML, JavaScript, CSS, documentation, and metadata.
---

# MicroSim Generator

## Overview

This meta-skill routes MicroSim creation requests to the appropriate specialized generator based on visualization requirements. It consolidates 14 individual MicroSim generator skills into a single entry point with on-demand loading of specific implementation guides.

## When to Use This Skill

Use this skill when users request:

- Interactive educational visualizations
- Data visualizations (charts, graphs, plots)
- Timelines or chronological displays
- Geographic/map visualizations
- Network diagrams or concept maps
- Flowcharts or workflow diagrams
- Mathematical function plots
- Set diagrams (Venn)
- Priority matrices or bubble charts
- Custom simulations or animations
- Comparison tables with ratings
- Matrix comparisons with expandable cell details

## Step 1: Analyze Request and Match Generator

Scan the user's request for trigger keywords and match to the appropriate generator guide.

### Quick Reference Routing Table

| Trigger Keywords | Guide File | Library |
|------------------|------------|---------|
| timeline, dates, chronological, events, history, schedule, milestones | `references/timeline-guide.md` | vis-timeline |
| map, geographic, coordinates, latitude, longitude, locations, markers | `references/map-guide.md` | Leaflet.js |
| function, f(x), equation, plot, calculus, sine, cosine, polynomial | `references/plotly-guide.md` | Plotly.js |
| network, nodes, edges, graph, dependencies, concept map, knowledge graph | `references/vis-network-guide.md` | vis-network |
| flowchart, workflow, process, state machine, UML, sequence diagram | `references/mermaid-guide.md` | Mermaid.js |
| venn, sets, overlap, intersection, union, categories | `references/venn-guide.md` | Custom |
| chart, bar, line, pie, doughnut, radar, statistics, data | `references/chartjs-guide.md` | Chart.js |
| bubble, priority, matrix, quadrant, impact vs effort, risk vs value | `references/bubble-guide.md` | Chart.js |
| causal, feedback, loop, systems thinking, reinforcing, balancing | `references/causal-loop-guide.md` | vis-network |
| comparison, table, ratings, stars, side-by-side, features | `references/comparison-table-guide.md` | Custom |
| matrix, framework comparison, clickable cells, detail panel, expandable | `references/html-table.md` | Custom |
| animation, celebration, particles, confetti, effects | `references/celebration-guide.md` | p5.js |
| custom, simulation, physics, interactive, bouncing, movement, p5.js | `references/p5-guide.md` | p5.js |

### Decision Tree

```
Has dates/timeline/chronological events?
  → YES: timeline-guide.md

Has geographic coordinates/locations?
  → YES: map-guide.md

Mathematical function f(x) or equation?
  → YES: plotly-guide.md

Nodes and edges/network relationships?
  → YES: vis-network-guide.md (or causal-loop-guide.md if systems thinking)

Flowchart/workflow/process diagram?
  → YES: mermaid-guide.md

Sets with overlaps (2-4 categories)?
  → YES: venn-guide.md

Priority matrix/2x2 quadrant/multi-dimensional?
  → YES: bubble-guide.md

Standard chart (bar/line/pie/radar)?
  → YES: chartjs-guide.md

Comparison table with ratings/stars?
  → YES: comparison-table-guide.md

Matrix comparison with clickable cells/detail panels?
  → YES: html-table.md

Celebration/particles/visual feedback?
  → YES: celebration-guide.md

Custom simulation/animation/physics?
  → YES: p5-guide.md
```

## Step 2: Instructional Design Checkpoint (MANDATORY)

**Before loading any generator guide, you MUST complete this checkpoint.**

### 2.1 Identify Learning Objective Details

Extract from the specification:
- **Bloom Level**: Remember, Understand, Apply, Analyze, Evaluate, or Create
- **Bloom Verb**: The action verb (explain, demonstrate, calculate, etc.)
- **Learning Objective**: The full statement of what learners will be able to do

### 2.2 Match Interaction Pattern to Bloom Level

| Bloom Level | Appropriate Patterns | Inappropriate Patterns |
|-------------|---------------------|------------------------|
| Remember (L1) | Flashcards, matching, labeling | Complex simulations |
| **Understand (L2)** | **Step-through worked examples, concrete data visibility** | **Continuous animation, particle effects** |
| Apply (L3) | Parameter sliders, calculators, practice problems | Passive viewing only |
| Analyze (L4) | Network explorers, comparison tools, pattern finders | Pre-computed results |
| Evaluate (L5) | Sorting/ranking activities, rubric tools | No feedback mechanisms |
| Create (L6) | Builders, editors, canvas tools | Rigid templates |

### 2.3 Answer These Questions

Before proceeding, answer these questions:

1. **What specific data must the learner SEE?**
   - Not "animated particles" but "the tokenized array ['physics', 'ball']"

2. **Does the learner need to PREDICT before observing?**
   - If YES → Use step-through with Next/Previous buttons
   - If YES → Do NOT use continuous animation

3. **What does animation add that static arrows don't?**
   - If you can't answer this clearly → Don't use animation

4. **Is continuous animation appropriate for this Bloom level?**
   - For Understand (L2) with verb "explain" → Almost always NO
   - For Apply (L3) with real-time feedback → Often YES

### 2.4 Modify Specification If Needed

If the specification requests animation/effects for an UNDERSTAND level objective:
- **Flag this as a potential instructional design issue**
- **Recommend step-through pattern instead**
- **Ask user**: "The specification requests animation, but for an 'explain' objective, a step-through approach with concrete data visibility typically supports learning better. Should I proceed with step-through instead?"

### 2.5 Document Your Decision

Add to your response:
```
Instructional Design Check:
- Bloom Level: [level]
- Bloom Verb: [verb]
- Recommended Pattern: [pattern]
- Specification Alignment: [aligned/modified]
- Rationale: [why this pattern supports the learning objective]
```

---

## Step 3: Load the Matched Guide

Once you complete the instructional design checkpoint, **read the corresponding guide file** from the `references/` directory and follow its workflow.

Example:
- User asks for "a timeline showing the history of Unix"
- Match: `timeline` keyword → Load `references/timeline-guide.md`
- Follow the timeline-guide.md workflow

## Step 5: Execute Generator Workflow

Each guide contains:
1. Library-specific requirements
2. Directory structure to create
3. Step-by-step implementation workflow
4. Code templates and patterns
5. Best practices for that visualization type

## Handling Ambiguous Requests

If the request could match multiple generators:

1. **Read `references/routing-criteria.md`** for detailed scoring methodology
2. **Score top 3 candidates** using the 0-100 scale
3. **Present options to user** with reasoning:
   ```
   Based on your request, I recommend:
   1. [Generator A] (Score: 85) - Best for [reason]
   2. [Generator B] (Score: 70) - Alternative if you need [feature]
   3. [Generator C] (Score: 55) - Possible if [condition]

   Which would you prefer?
   ```
4. **Proceed with user's selection**

## Common Ambiguities

| Ambiguous Term | Clarification Needed |
|----------------|---------------------|
| "graph" | Chart (ChartJS) or Network graph (vis-network)? |
| "diagram" | Structural (Mermaid), Network (vis-network), or Custom (p5)? |
| "map" | Geographic (Leaflet) or Concept map (vis-network)? |
| "table" | Star ratings (comparison-table) or Clickable cells with detail panels (html-table)? |
| "visualization" | What type of data? What interaction needed? |

## Available Generators

### Primary Generators

| Generator | Library | Best For |
|-----------|---------|----------|
| p5-guide | p5.js | Custom simulations, physics, animations |
| chartjs-guide | Chart.js | Bar, line, pie, doughnut, radar charts |
| timeline-guide | vis-timeline | Chronological events, history, schedules |
| map-guide | Leaflet.js | Geographic data, locations, routes |
| vis-network-guide | vis-network | Network graphs, dependencies, concept maps |
| mermaid-guide | Mermaid.js | Flowcharts, workflows, UML diagrams |
| plotly-guide | Plotly.js | Mathematical function plots |
| venn-guide | Custom | Set relationships (2-4 sets) |
| bubble-guide | Chart.js | Priority matrices, multi-dimensional data |
| causal-loop-guide | vis-network | Systems thinking, feedback loops |
| comparison-table-guide | Custom | Side-by-side comparisons with ratings |
| html-table | Custom | Matrix comparisons with clickable cells, detail panels |
| celebration-guide | p5.js | Particle effects, visual feedback |

### Shared Standards

All MicroSims follow these standards regardless of generator:

**Directory Structure:**
```
docs/sims/<microsim-name>/
├── main.html       # Main visualization file
├── index.md        # Documentation page
├── *.js or *.css   # Supporting files
└── metadata.json   # Dublin Core metadata (optional)
```

**Integration:**
- Embedded via iframe in MkDocs pages
- Width-responsive design
- Non-scrolling iframe container
- Standard height: drawHeight + controlHeight + 2px

**Quality Checklist:**
- [ ] Runs without errors in modern browsers
- [ ] Responsive to container width
- [ ] Controls respond immediately
- [ ] Educational purpose is clear
- [ ] Code is well-commented

## Examples

### Example 1: Timeline Request
**User:** "Create a timeline showing key events in computer history"
**Routing:** Keywords "timeline", "events", "history" → `references/timeline-guide.md`
**Action:** Read timeline-guide.md and follow its workflow

### Example 2: Chart Request
**User:** "Make a bar chart comparing programming language popularity"
**Routing:** Keywords "bar chart", "comparing" → `references/chartjs-guide.md`
**Action:** Read chartjs-guide.md and follow its workflow

### Example 3: Custom Simulation
**User:** "Build an interactive bouncing ball simulation"
**Routing:** Keywords "interactive", "bouncing", "simulation" → `references/p5-guide.md`
**Action:** Read p5-guide.md and follow its workflow

### Example 4: Ambiguous Request
**User:** "Create a graph of our project dependencies"
**Routing:** "graph" + "dependencies" suggests network → `references/vis-network-guide.md`
**Action:** Read vis-network-guide.md (but clarify if user meant a chart)

## Reference Files

For detailed information, consult:

- `references/routing-criteria.md` - Complete scoring methodology for all generators
- `references/<generator>-guide.md` - Specific implementation guide for each generator
- `assets/templates/` - Shared templates and patterns

## Step 6: Auto-Standardization

**IMPORTANT**: After creating the MicroSim files, automatically run standardization to ensure quality and documentation standards are met.

### Why Auto-Standardize?

- Eliminates manual follow-up work
- Ensures consistent quality across all MicroSims
- Adds metadata.json, lesson plans, and references automatically
- Calculates and records quality_score in index.md

### Standardization Process

After the generator guide workflow completes (files created in `docs/sims/<microsim-name>/`):

1. **Read the standardization guide**: Load `../microsim-utils/references/standardization.md`
2. **Run the standardization checklist** on the newly created MicroSim directory
3. **Implement all fixes automatically** (skip user confirmation since this is a new MicroSim)
4. **Generate quality_score** and add to index.md frontmatter

### What Standardization Adds

The standardization process will add these elements if missing:

- **metadata.json** - Dublin Core metadata for discoverability
- **YAML frontmatter** - title, description, quality_score, image paths
- **Iframe examples** - Copy-paste code for embedding
- **Fullscreen button** - Link to view MicroSim fullscreen
- **Lesson Plan section** - Learning objectives, activities, assessment
- **References section** - Related resources and documentation

### Workflow Integration

```
[User Request]
    → [Route to Guide]
    → [Generate MicroSim Files]
    → [Auto-Standardize] ← NEW STEP
    → [Update mkdocs.yml]
    → [Done]
```

This eliminates the need to manually run `microsim-utils standardization` after every MicroSim creation.

## mkdocs.yml Integration

After creating and standardizing a MicroSim, add it to the site navigation:

```yaml
nav:
  - MicroSims:
    - List of MicroSims: sims/index.md
    - Existing Sim: sims/existing-sim/index.md
    - New MicroSim: sims/new-microsim-name/index.md  # Add here
```
