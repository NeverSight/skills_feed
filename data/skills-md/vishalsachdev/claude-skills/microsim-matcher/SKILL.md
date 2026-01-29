---
name: microsim-matcher
description: This skill analyzes diagram, chart, or simulation specifications and returns a ranked list of the most suitable MicroSim generator skills to use. It compares the specification against capabilities of all available microsim generators (p5.js, ChartJS, Plotly, Mermaid, vis-network, timeline, map, Venn, bubble) and provides match scores (0-100) with detailed reasoning for each recommendation. Use this skill when a user has a diagram specification and needs guidance on which MicroSim generator skill to use.
---

# MicroSim Matcher

## Overview

This skill analyzes diagram, chart, or simulation specifications and recommends the most appropriate MicroSim generator skill(s) to use. It evaluates the specification against the capabilities of all 9 available MicroSim generators and returns a ranked list with match scores (0-100) and detailed reasoning.

## Purpose

When creating educational MicroSims, choosing the right generator is critical for success. This skill automates the matching process by:

1. Analyzing the characteristics of the desired visualization
2. Comparing against capabilities of all MicroSim generators
3. Scoring each generator on a 0-100 scale
4. Providing ranked recommendations with clear reasoning

This helps users quickly identify the best tool for their needs without manually comparing all generator options.

## When to Use This Skill

Invoke this skill when:

- User has a diagram or visualization specification and needs to know which generator to use
- User describes a desired MicroSim but hasn't specified a generator
- User asks "Which MicroSim generator should I use for...?"
- User needs to compare multiple generator options
- You need to recommend the best generator for a given specification

## Available MicroSim Generators

The skill evaluates matches against these 9 generators:

1. **microsim-p5** - General p5.js simulations and custom animations
2. **chartjs-generator** - Standard statistical charts (bar, line, pie, etc.)
3. **math-function-plotter-plotly** - Mathematical function plots with Plotly.js
4. **mermaid-generator** - Flowcharts, diagrams, and workflows
5. **vis-network** - Network graphs with nodes and edges
6. **timeline-generator** - Chronological timelines with events
7. **map-generator** - Geographic visualizations with Leaflet.js
8. **venn-diagram-generator** - Set relationship diagrams (2-4 sets)
9. **bubble-chart-generator** - Priority matrices and multi-dimensional comparisons

Detailed capabilities for each generator are documented in `references/matching-criteria.md`.

## Workflow

Follow these 7 steps to match a specification to the best MicroSim generator(s):

### Step 0: Check for Reference File Updates (Version Check)

**IMPORTANT**: Before analyzing the specification, verify that the local `matching-criteria.md` file is up-to-date with the latest version on GitHub. An outdated reference file will lead to poor recommendations.

**Version Check Process:**

1. **Get local file timestamp**:
   ```bash
   stat -f "%Sm" -t "%Y-%m-%d %H:%M:%S" skills/microsim-matcher/references/matching-criteria.md
   # On Linux: stat -c "%y" skills/microsim-matcher/references/matching-criteria.md
   ```

2. **Check GitHub version** using the GitHub API:
   ```bash
   curl -s https://api.github.com/repos/dmccreary/claude-skills/commits?path=skills/microsim-matcher/references/matching-criteria.md&page=1&per_page=1 | grep -o '"date": "[^"]*"' | head -1
   ```

3. **Compare timestamps**:
   - If GitHub version is newer → **WARNING: Reference file may be outdated**
   - If local version is current → Proceed with confidence

**Automated Check (Optional):**

A Python script is available in `skills/microsim-matcher/scripts/check-version.py` to automate this check.

**If Reference File is Outdated:**

Display a prominent warning to the user:

```
⚠️  WARNING: Reference File May Be Outdated

Your local matching-criteria.md file was last modified on [LOCAL_DATE].
The GitHub repository has a newer version from [GITHUB_DATE].

This may result in:
- Missing information about new MicroSim generators
- Outdated scoring guidelines
- Incorrect recommendations

Recommended actions:
1. Update your local copy:
   git pull origin main

2. Or download the latest version:
   https://github.com/dmccreary/claude-skills/blob/main/skills/microsim-matcher/references/matching-criteria.md

3. Or continue with potentially outdated information (not recommended)

Continue anyway? [Proceed if user confirms]
```

**When to Skip Version Check:**

- No internet connection available
- User explicitly requests to skip (with understanding of risks)
- Working in an isolated/offline environment

**Version Check Frequency:**

- Always check when skill is invoked
- Cache result for 24 hours to avoid repeated API calls
- Re-check if more than 24 hours since last check

### Step 1: Read and Parse the Diagram Specification

Read the specification file provided by the user. The specification may be in various formats:

- Plain text description
- Structured markdown
- JSON/YAML data
- Requirements list
- User conversation describing the need

**Extract the following information:**

- **Visual type**: Chart, diagram, plot, map, timeline, network, simulation, animation
- **Data type**: Numerical, categorical, temporal, geographic, relational, mathematical, structural
- **Data source**: What kind of data will be visualized (events, functions, nodes/edges, coordinates, sets, etc.)
- **Interactivity needs**: Static, hover tooltips, click actions, drag, sliders, real-time updates
- **Explicit mentions**: Does the spec mention specific tools (p5.js, Plotly, Mermaid, etc.)?
- **Domain/context**: Educational subject area (math, history, science, CS, business, etc.)

### Step 2: Extract Key Characteristics

Analyze the specification and identify:

**Primary Characteristics:**

1. **Temporal**: Does it involve dates, chronological events, or time-based sequences?
   - Keywords: "timeline", "chronological", "dates", "events", "history", "schedule"

2. **Geographic**: Does it involve locations, coordinates, or maps?
   - Keywords: "map", "location", "coordinates", "latitude", "longitude", "geographic"

3. **Mathematical**: Does it involve mathematical functions or equations?
   - Keywords: "function", "f(x)", "equation", "plot", "calculus", "trigonometric"

4. **Network/Graph**: Does it involve nodes, edges, or network relationships?
   - Keywords: "network", "graph", "nodes", "edges", "connections", "dependencies"

5. **Process/Flow**: Does it show workflows, processes, or state transitions?
   - Keywords: "flowchart", "workflow", "process", "state machine", "sequence diagram"

6. **Set-based**: Does it compare sets with overlaps and intersections?
   - Keywords: "venn", "sets", "overlap", "intersection", "categories"

7. **Statistical/Data**: Does it visualize numerical or categorical data as charts?
   - Keywords: "chart", "bar", "line", "pie", "statistics", "data", "compare"

8. **Priority/Matrix**: Does it show 2D priority or decision matrix?
   - Keywords: "priority", "impact vs effort", "matrix", "quadrant", "bubble"

9. **Custom/Unique**: Does it require custom animations or unique visualizations?
   - Keywords: "animation", "simulation", "custom", "interactive", "p5.js"

**Secondary Characteristics:**

- **Complexity level**: Simple (1-10 items) vs. Complex (100+ items)
- **Interactivity requirements**: Passive viewing vs. Active manipulation
- **Educational features**: Lesson plans, assessments, tooltips with definitions
- **Responsiveness needs**: Desktop only vs. Mobile-friendly required

### Step 3: Load MicroSim Generator Capabilities

Read the matching criteria from `references/matching-criteria.md`. This file contains:

- Detailed profiles for all 9 generators
- Primary use cases and strengths
- Data type requirements
- Interactivity capabilities
- Trigger words and phrases
- Scoring guidelines (when to score high vs. low)
- Limitations and caveats

**Load additional details if needed:**

- Review `/docs/skill-descriptions/microsims/index.md` for overview
- Read detailed skill descriptions in `/docs/skill-descriptions/microsims/[generator-name].md`
- Check full workflows in `/skills/[generator-name]/SKILL.md`

### Step 4: Score Each MicroSim Generator

For each of the 9 generators, assign a match score from 0-100 using this scale:

**Scoring Scale:**

- **90-100**: Perfect match - Primary use case for this generator
- **70-89**: Strong match - Well-suited, minor limitations
- **50-69**: Moderate match - Could work but not optimal
- **30-49**: Weak match - Significant limitations or workarounds needed
- **0-29**: Poor match - Not recommended, use different generator

**Scoring Methodology:**

For each generator, evaluate:

1. **Data Type Match (40 points max)**
   - Does the specification's data type align with what the generator expects?
   - Perfect match: 40 points
   - Partial match: 20-35 points
   - Poor match: 0-15 points

2. **Interactivity Match (25 points max)**
   - Do the interactivity requirements match the generator's capabilities?
   - Perfect match: 25 points
   - Partial match: 10-20 points
   - Poor match: 0-5 points

3. **Visual Style Match (25 points max)**
   - Does the desired visual output align with the generator's strengths?
   - Perfect match: 25 points
   - Partial match: 10-20 points
   - Poor match: 0-5 points

4. **Trigger Word Bonus (10 points max)**
   - Specification contains strong trigger words for this generator: +10 points
   - Specification contains weak trigger words: +5 points
   - No trigger words: 0 points

**Example Scoring:**

Specification: "Timeline showing product development milestones from 2020-2025"

**timeline-generator scoring:**
- Data Type Match: 40/40 (temporal data with dates - perfect match)
- Interactivity Match: 25/25 (needs zoom/pan/click - perfect match)
- Visual Style Match: 25/25 (timeline visual - perfect match)
- Trigger Words: +10 (contains "timeline" and "milestones")
- **Total: 100/100**

**chartjs-generator scoring:**
- Data Type Match: 15/40 (temporal data, but chartjs not optimized for timelines)
- Interactivity Match: 10/25 (basic interactivity, lacks timeline-specific features)
- Visual Style Match: 10/25 (could show as line chart, but not ideal)
- Trigger Words: 0 (no chart-related words)
- **Total: 35/100**

### Step 5: Rank Generators by Score

Sort the 9 generators from highest to lowest score.

**Ranking Guidelines:**

- **Include top 3-5 generators minimum** in the output
- **Always include at least one generator with score ≥ 70** if possible
- **Show a range of scores** to help user understand alternatives
- **Include lower scores** (30-50 range) to show what NOT to use
- **Omit scores below 30** unless specifically relevant

If no generator scores above 70, this may indicate:
- Specification is unclear or incomplete
- Specification requires multiple MicroSims
- Specification needs custom development outside existing generators

### Step 6: Format Output with Reasoning

Present the results as a numbered list with the following format for each generator:

```
## MicroSim Generator Recommendations

[Brief summary of specification analysis]

### Ranked Results:

1. **[generator-name]** (Score: [0-100]/100)

   **Reasoning:** [2-4 sentences explaining why this score was assigned. Include:
   - What matches well (data type, interactivity, visual style)
   - Specific features that align with requirements
   - Any limitations or caveats
   - Why this is better/worse than alternatives]

   **Key Features:** [Bullet list of relevant features for this use case]

   **Skill Location:** `skills/[generator-name]/SKILL.md`

2. **[generator-name]** (Score: [0-100]/100)
   [Same format as above]

[Continue for top 3-5 generators]
```

**Output Quality Requirements:**

1. **Clear reasoning**: Each score should be justified with specific features
2. **Honest assessment**: Don't oversell poor matches
3. **Practical guidance**: Help user make an informed decision
4. **Alternative suggestions**: If top choice has limitations, note alternatives
5. **Skill locations**: Always include path to the full skill file

**Example Output:**

```
## MicroSim Generator Recommendations

Your specification describes a "network diagram showing prerequisite relationships between course concepts." This is clearly a network/graph visualization with nodes (concepts) and edges (prerequisites).

### Ranked Results:

1. **vis-network** (Score: 95/100)

   **Reasoning:** This is the primary use case for vis-network. The specification describes nodes (concepts) and edges (prerequisite relationships), which is exactly what vis-network is designed for. The skill supports physics-based layouts that automatically position related concepts, interactive dragging to explore the network, and click events to show concept details. The only minor limitation is that very large networks (500+ concepts) may require performance optimization.

   **Key Features:**
   - Physics-based automatic layout
   - Interactive drag, click, zoom, pan
   - Group/cluster support for organizing concepts by topic
   - Hover tooltips for concept definitions
   - Learning graph JSON format support

   **Skill Location:** `skills/vis-network/SKILL.md`

2. **mermaid-generator** (Score: 70/100)

   **Reasoning:** Mermaid supports flowcharts and graphs that could represent prerequisite relationships. However, Mermaid diagrams are more static compared to vis-network and don't offer the same level of interactivity (no dragging, less dynamic layout). Mermaid would work well for smaller, simpler prerequisite chains but may become cluttered with many concepts. Use this if you prefer a more static, documentation-style diagram.

   **Key Features:**
   - Text-based diagram specification
   - Clean, professional appearance
   - Good for documentation
   - Multiple diagram types available

   **Skill Location:** `skills/mermaid-generator/SKILL.md`

3. **microsim-p5** (Score: 50/100)

   **Reasoning:** While p5.js could create a custom network visualization, it would require significantly more development effort compared to using vis-network, which is specifically designed for this purpose. Only choose p5.js if you need custom animations, unique visual effects, or interactivity patterns not available in vis-network. For standard network diagrams, vis-network is the better choice.

   **Key Features:**
   - Complete customization flexibility
   - Custom animations possible
   - Unique interaction patterns

   **Skill Location:** `skills/microsim-p5/SKILL.md`

4. **chartjs-generator** (Score: 25/100)

   **Reasoning:** Not recommended. ChartJS is designed for statistical charts (bar, line, pie), not network diagrams. There's no way to represent nodes and edges in standard chart types. Use vis-network or mermaid-generator instead.

   **Skill Location:** `skills/chartjs-generator/SKILL.md`

### Recommendation:

Use **vis-network** (Score: 95/100) for your prerequisite relationship diagram. It's specifically designed for this use case and will provide the best user experience with minimal development effort.
```

## Scoring Reference

Quick reference for common specification types:

| Specification Type | Top Generator | Score | Alternative |
|-------------------|---------------|-------|-------------|
| Timeline with dates | timeline-generator | 90-100 | chartjs (30-40) |
| Geographic map | map-generator | 90-100 | - |
| Math function f(x) | math-function-plotter-plotly | 90-100 | microsim-p5 (50-60) |
| Network graph | vis-network | 90-100 | mermaid (60-70) |
| Flowchart/process | mermaid-generator | 90-100 | microsim-p5 (40-50) |
| Venn diagram | venn-diagram-generator | 90-100 | microsim-p5 (50) |
| Bar/pie/line chart | chartjs-generator | 90-100 | microsim-p5 (40) |
| Priority matrix | bubble-chart-generator | 90-100 | chartjs (60-70) |
| Custom animation | microsim-p5 | 90-100 | - |

## Best Practices

### Be Specific in Reasoning

**Good reasoning:**
> "The specification describes plotting y = sin(x) over the domain [-2π, 2π], which is exactly what math-function-plotter-plotly is designed for. The skill provides interactive sliders to explore points on the curve, hover tooltips showing coordinates, and responsive design. Score: 98/100."

**Poor reasoning:**
> "This looks like a math thing, so use the math plotter. Score: 90/100."

### Address Limitations Honestly

**Good honesty:**
> "While chartjs-generator could show temporal data as a line chart (Score: 40/100), it lacks the specialized timeline features (zoom to date ranges, event details panels, category filtering) that make timeline-generator the better choice (Score: 95/100)."

**Poor honesty:**
> "ChartJS can do anything with data, use it. Score: 85/100."

### Consider the User's Context

- **Educational use**: Emphasize lesson plans, tooltips, accessibility
- **Technical documentation**: Note text-based specs (Mermaid) vs. data-driven (vis-network)
- **Student projects**: Consider ease of customization and learning curve
- **Professional use**: Emphasize polish, standard libraries, maintainability

### Provide Actionable Guidance

End with a clear recommendation:

**Good:**
> "**Recommendation:** Use timeline-generator (95/100) for your product roadmap. It's specifically designed for temporal data and will give you the best results with minimal effort."

**Less useful:**
> "These are your scores. Pick one."

## Handling Edge Cases

### Multiple Visualizations Needed

If the specification requires multiple types of visualizations:

```
Your specification describes both a timeline of events AND a network graph of relationships. This requires two separate MicroSims:

1. **For the timeline portion:** timeline-generator (Score: 95/100)
2. **For the network portion:** vis-network (Score: 95/100)

Consider creating two separate MicroSims and linking between them in your textbook.
```

### Unclear or Incomplete Specification

If you can't determine a clear match:

```
The specification is somewhat unclear about the desired visual format. Based on the available information:

**If the focus is on [interpretation A]:**
- Recommended: [generator A] (Score: 80/100)

**If the focus is on [interpretation B]:**
- Recommended: [generator B] (Score: 85/100)

Please clarify: [specific questions to ask]
```

### No Good Match (All Scores Below 70)

If no generator scores above 70:

```
After analyzing your specification, none of the existing MicroSim generators are an ideal match. Here are your options:

1. **Modify requirements** to fit an existing generator:
   - [suggestion] could work if [modification]

2. **Create custom MicroSim** with microsim-p5:
   - Full flexibility but requires more development
   - Estimated complexity: [assessment]

3. **Split into multiple MicroSims**:
   - Use [generator 1] for [aspect 1]
   - Use [generator 2] for [aspect 2]

Would you like help refining the specification or exploring custom development?
```

### Ambiguous Terminology

"Graph" can mean network graph OR chart. Clarify:

```
The term "graph" is ambiguous. Please clarify:

- **If you mean a network graph** (nodes and edges): Use vis-network (Score: 95/100)
- **If you mean a chart/plot** (data points): Use chartjs-generator (Score: 90/100) or math-function-plotter-plotly (Score: 90/100)
```

## Common Mistakes to Avoid

1. **Don't score everything 50**: Show clear winners and losers
2. **Don't ignore trigger words**: They're strong signals of intent
3. **Don't recommend deprecated/unmaintained tools**: Note cautions (e.g., venn.js library)
4. **Don't skip the reasoning**: Scores without explanation aren't helpful
5. **Don't forget educational context**: MicroSims are for learning, not just visualization
6. **Don't overlook existing data**: Check if glossary exists for Venn diagram definitions

## References

- **Matching Criteria**: `skills/microsim-matcher/references/matching-criteria.md`
- **Version Check Script**: `skills/microsim-matcher/scripts/check-version.py`
- **GitHub Repository**: https://github.com/dmccreary/claude-skills
- **Reference File on GitHub**: https://github.com/dmccreary/claude-skills/blob/main/skills/microsim-matcher/references/matching-criteria.md
- **MicroSim Overview**: `/docs/skill-descriptions/microsims/index.md`
- **Individual Skill Descriptions**: `/docs/skill-descriptions/microsims/[generator-name].md`
- **Full Skill Workflows**: `/skills/[generator-name]/SKILL.md`

## Version Check Script Usage

The `check-version.py` script provides automated version checking:

**Basic check (with output):**
```bash
python skills/microsim-matcher/scripts/check-version.py
```

**Quiet mode (exit code only):**
```bash
python skills/microsim-matcher/scripts/check-version.py --quiet
echo $?  # 0=up-to-date, 1=outdated, 2=error
```

**Auto-update mode (downloads latest if outdated):**
```bash
python skills/microsim-matcher/scripts/check-version.py --update
```

**Exit codes:**
- `0` - Local file is up-to-date
- `1` - GitHub version is newer (outdated)
- `2` - Error occurred (network, file not found, etc.)

**Integration with CI/CD:**
```bash
# In a pre-commit hook or CI pipeline
if python skills/microsim-matcher/scripts/check-version.py --quiet; then
    echo "✅ Reference file is up-to-date"
else
    echo "⚠️  Reference file is outdated - consider updating"
fi
```

## Skill Maintenance

### When New MicroSim Generators Are Added

When new MicroSim generators are added to the repository:

1. **Update `references/matching-criteria.md`** with the new generator profile:
   - Add a new numbered section for the generator
   - Include primary use cases and strengths
   - Document data types and interactivity capabilities
   - List trigger words and scoring guidelines
   - Note any limitations or caveats

2. **Update this SKILL.md file**:
   - Add generator to "Available MicroSim Generators" list
   - Update generator count (currently 9)
   - Add examples of when to recommend the new generator
   - Update scoring reference table

3. **Test matching**:
   - Create test specifications that should trigger the new generator
   - Verify scoring logic produces expected results
   - Ensure reasoning is clear and accurate

4. **Commit changes**:
   - Commit updated files to GitHub
   - GitHub API will automatically track the new timestamp
   - Users will be notified on next version check

### When Existing Generators Are Updated

When existing generators gain new features or capabilities:

1. **Update matching criteria** for that generator in `references/matching-criteria.md`
2. **Revise scoring guidelines** if new features significantly change match quality
3. **Update examples** to showcase new capabilities
4. **Test edge cases** where new features might change recommendations

### Keeping Reference Files Current

**For Repository Maintainers:**

After making changes to `matching-criteria.md`:
```bash
# 1. Make your changes
vim skills/microsim-matcher/references/matching-criteria.md

# 2. Commit and push
git add skills/microsim-matcher/references/matching-criteria.md
git commit -m "Update matching criteria: [description of changes]"
git push origin main

# GitHub will automatically update the file timestamp
# Users will be notified via version check on next use
```

**For Skill Users:**

Check for updates regularly:
```bash
# Option 1: Run version check manually
python skills/microsim-matcher/scripts/check-version.py

# Option 2: Auto-update if outdated
python skills/microsim-matcher/scripts/check-version.py --update

# Option 3: Pull latest from GitHub
git pull origin main
```

**Recommended Update Schedule:**
- Before starting a new project: Always check for updates
- Monthly: Run version check even if not actively using
- After seeing announcement of new generators: Immediately update

### Version History Best Practices

To help users understand changes:

1. **Document changes** in commit messages:
   ```bash
   git commit -m "Add support for new scatter-plot-generator (10th generator)"
   ```

2. **Include change summary** at the top of `matching-criteria.md`:
   ```markdown
   ## Recent Updates

   - 2025-11-17: Added math-function-plotter-plotly (9th generator)
   - 2025-11-10: Updated vis-network scoring for large graphs
   - 2025-11-01: Initial release with 8 generators
   ```

3. **Tag major updates** in GitHub:
   ```bash
   git tag -a v1.1 -m "Added 10th generator, updated scoring"
   git push origin v1.1
   ```
