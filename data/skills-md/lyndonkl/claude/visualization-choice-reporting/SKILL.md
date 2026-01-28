---
name: visualization-choice-reporting
description: Use when you need to choose the right visualization for your data and question, then create a narrated report that highlights insights and recommends actions. Invoke when analyzing data for patterns (trends, comparisons, distributions, relationships, compositions), building dashboards or reports, presenting metrics to stakeholders, monitoring KPIs, exploring datasets for insights, communicating findings from analysis, or when user mentions "visualize this", "what chart should I use", "create a dashboard", "analyze this data", "show trends", "compare these metrics", "report on", "what does this data tell us", or needs to turn data into actionable insights. Apply to business analytics (revenue, growth, churn, funnel, cohort, segmentation), product metrics (usage, adoption, retention, feature performance, A/B tests), marketing analytics (campaign ROI, attribution, funnel, customer acquisition), financial reporting (P&L, budget, forecast, variance), operational metrics (uptime, performance, capacity, SLA), sales analytics (pipeline, forecast, territory, quota attainment), HR metrics (headcount, turnover, engagement, DEI), and any scenario where data needs to become a clear, actionable story with the right visual form.
---
# Visualization Choice & Reporting

## Overview

**Visualization choice & reporting** matches visualization types to questions and data, then creates narrated dashboards that highlight signal and recommend actions.

**Three core components:**

**1. Chart selection:** Match chart type to question type and data structure (comparison → bar chart, trend → line chart, distribution → histogram, relationship → scatter, composition → treemap, geographic → map, hierarchy → tree diagram, flow → sankey)

**2. Visualization best practices:** Apply perceptual principles (position > length > angle > area > color for accuracy), reduce chart junk, use pre-attentive attributes (color, size, position) to highlight signal, respect accessibility (colorblind-safe palettes, alt text), choose appropriate scales (linear, log, normalized)

**3. Narrative reporting:** Lead with insight headline, annotate key patterns, provide context (vs benchmark, vs target, vs previous period), interpret what it means, recommend next actions

**When to use:** Data analysis, dashboards, reports, presentations, monitoring, exploration, stakeholder communication

## Workflow

Copy this checklist and track your progress:

```
Visualization Choice & Reporting Progress:
- [ ] Step 1: Clarify question and profile data
- [ ] Step 2: Select visualization type
- [ ] Step 3: Design effective chart
- [ ] Step 4: Narrate insights and actions
- [ ] Step 5: Validate and deliver
```

**Step 1: Clarify question and profile data**

Define the question you're answering (What's the trend? How do X and Y compare? What's the distribution? What drives Z? What's the composition?). Profile your data: type (categorical, numerical, temporal, geospatial), granularity (daily, user-level, aggregated), size (10 rows, 10K, 10M), dimensions (1D, 2D, multivariate). See [Question-Data Profiling](#question-data-profiling).

**Step 2: Select visualization type**

Match question type to chart family using [Chart Selection Guide](#chart-selection-guide). Consider data size (small → tables, medium → standard charts, large → heatmaps/binned), number of series (1-3 → standard, 4-10 → small multiples, 10+ → interactive/aggregated), and audience expertise (executives → simple with insights, analysts → detailed exploration).

**Step 3: Design effective chart**

For simple cases → Apply [Design Checklist](#design-checklist) (clear title, labeled axes, legend if needed, annotations, accessible colors). For complex cases (multivariate, dashboards, interactive) → Study [resources/methodology.md](resources/methodology.md) for advanced techniques (small multiples, layered charts, dashboard layout, interaction patterns).

**Step 4: Narrate insights and actions**

Lead with insight headline ("Revenue up 30% YoY driven by Enterprise segment"), annotate key patterns (arrows, labels, shading), provide context (vs benchmark, target, previous), interpret meaning ("Suggests product-market fit in Enterprise"), recommend actions ("Double down on Enterprise sales hiring"). See [Narrative Framework](#narrative-framework).

**Step 5: Validate and deliver**

Self-assess using [resources/evaluators/rubric_visualization_choice_reporting.json](resources/evaluators/rubric_visualization_choice_reporting.json). Check: Does chart answer the question clearly? Are insights obvious at a glance? Are next actions clear? Create `visualization-choice-reporting.md` with question, data summary, visualization spec, narrative, and actions. See [Delivery Format](#delivery-format).

---

## Question-Data Profiling

**Question Types → Chart Families**

| Question Type | Example | Primary Chart Families |
|---------------|---------|------------------------|
| **Trend** | How has X changed over time? | Line, area, sparkline, horizon |
| **Comparison** | How do categories compare? | Bar (horizontal for names), column, dot plot, slope chart |
| **Distribution** | What's the spread/frequency? | Histogram, box plot, violin, density plot |
| **Relationship** | How do X and Y relate? | Scatter, bubble, connected scatter, hexbin |
| **Composition** | What are the parts? | Treemap, pie/donut, stacked bar, waterfall, sankey |
| **Geographic** | Where is it happening? | Choropleth, bubble map, flow map, dot map |
| **Hierarchical** | What's the structure? | Tree, dendrogram, sunburst, circle packing |
| **Multivariate** | How do many variables interact? | Small multiples, parallel coordinates, heatmap, SPLOM |

**Data Type → Encoding Considerations**

- **Categorical** (product, region, status): Use position, color hue, shape. Bar length better than pie angle for accuracy.
- **Numerical** (revenue, count, score): Use position, length, size. Prefer linear scales; use log only when spanning orders of magnitude.
- **Temporal** (date, timestamp): Always use consistent intervals. Annotate events. Show seasonality if relevant.
- **Geospatial** (lat/lon, region): Use maps for absolute location; use tables/charts if geography not central to insight.

---

## Chart Selection Guide

| Question Type | Chart Types | When to Use |
|---------------|-------------|-------------|
| **Comparison** | Bar (horizontal), Column, Grouped bar, Dot plot, Slope chart | Categorical → Numerical. Horizontal bar for long names/ranking. Grouped for 2-3 metrics. Slope for before/after. |
| **Trend** | Line, Area, Sparkline, Step, Candlestick | Time → Numerical. Line for continuous trends. Area for cumulative/part-to-whole. Sparkline for inline. Step for discrete changes. |
| **Distribution** | Histogram, Box plot, Violin, Density plot | Numerical → Frequency. Histogram for shape/outliers. Box for quartiles across groups. Violin for full density. |
| **Relationship** | Scatter, Bubble, Hexbin, Connected scatter | Numerical X → Numerical Y. Scatter for correlation. Bubble for 3rd/4th variable (size/color). Hexbin for dense data. |
| **Composition** | Treemap, Pie/Donut, Stacked bar (100%), Waterfall, Sankey | Parts of whole. Treemap for hierarchy. Pie for 2-5 categories (part-to-whole key). Waterfall for cumulative. Sankey for flow. |
| **Geographic** | Choropleth, Bubble map, Flow map | Spatial patterns. Choropleth for regions. Bubble for precise locations. Flow for origin-destination. |
| **Multivariate** | Small multiples, Heatmap, Parallel coordinates | Many variables. Small multiples for consistent comparison. Heatmap for matrix (time×day). Parallel for dimensions. |

---

## Design Checklist

**Essential Elements**

- [ ] **Insight headline title:** Not "Revenue by Month" but "Revenue Up 30% YoY, Driven by Enterprise"
- [ ] **Clear axis labels with units:** "Revenue ($M)", "Month (2024)", not just "Revenue", "Date"
- [ ] **Legend if multiple series:** Position near chart, use direct labels on lines when possible
- [ ] **Annotations for key points:** Arrows, labels, shading for important events/patterns
- [ ] **Source and timestamp:** "Source: Analytics DB, as of 2024-11-14" builds trust

**Perceptual Best Practices**

- [ ] **Start Y-axis at zero for bar/column charts** (to avoid exaggerating differences)
- [ ] **Use position over angle/area** (bar > pie for accuracy, scatter > bubble when size isn't critical)
- [ ] **Colorblind-safe palette:** Avoid red-green only; use blue-orange or add patterns
- [ ] **Limit colors to 5-7 distinct hues** (more requires legend lookup, slows comprehension)
- [ ] **Use pre-attentive attributes** (color, size, position) to highlight signal, not decoration

**Declutter**

- [ ] **Remove chart junk:** No 3D, no gradients, no heavy gridlines, no background images
- [ ] **Mute non-data ink:** Light gray gridlines, thin axes, subtle colors for reference lines
- [ ] **Use white space:** Don't cram; let data breathe

**Accessibility**

- [ ] **Alt text describing insight:** "Line chart showing revenue grew from $2M to $2.6M (30% increase) from Q1 to Q4 2024, with Enterprise segment contributing 80% of growth."
- [ ] **Sufficient contrast:** Text readable, lines distinguishable
- [ ] **Patterns in addition to color** for critical distinctions (dashed/solid lines, hatched fills)

---

## Narrative Framework

**Structure: Headline → Pattern → Context → Meaning → Action**

**1. Headline (one sentence, insight-first):**
- Not: "This chart shows monthly revenue."
- **But:** "Revenue grew 30% YoY, driven by Enterprise segment."

**2. Pattern (what do you see?):**
- "Q1-Q2 flat at $2M/month, then steady climb to $2.6M in Q4."
- "Enterprise segment grew 120% while SMB declined 10%."

**3. Context (compared to what?):**
- "vs target: 15% above plan"
- "vs last year: Q4 2023 was $2.0M, now $2.6M"
- "vs industry: Our 30% growth vs 10% industry average"

**4. Meaning (why does it matter?):**
- "Suggests product-market fit in Enterprise; SMB churn indicates pricing mismatch."
- "If sustained, Q1 2025 could hit $3M/month."

**5. Action (what should we do?):**
- "Prioritize: Hire 2 Enterprise AEs, launch SMB annual plans to reduce churn."
- "Monitor: Enterprise win rate, SMB churn by plan type."

**Example Full Narrative:**

> **Headline:** Enterprise revenue up 120% YoY while SMB declined 10%, resulting in overall 30% growth.
>
> **Pattern:** Revenue grew from $2M/month (Q1) to $2.6M (Q4). Enterprise segment contributed $1.5M in Q4 (up from $680K in Q1), while SMB dropped from $1.3M to $1.1M.
>
> **Context:** Total revenue 15% above plan. Enterprise growth (120%) far exceeds industry average (25%). SMB churn rate doubled from 5% to 10% in Q3-Q4.
>
> **Meaning:** Strong product-market fit in Enterprise; SMB pricing or feature set may be misaligned. Enterprise is now 58% of revenue vs 34% in Q1, reducing diversification.
>
> **Actions:**
> 1. **Prioritize:** Hire 2 Enterprise AEs for Q1, double down on Enterprise playbook
> 2. **Fix:** Launch SMB annual plans (Q1) to reduce churn; interview churned SMB customers to identify gaps
> 3. **Monitor:** Enterprise win rate, SMB churn by plan type, revenue concentration risk

---

## Delivery Format

Create `visualization-choice-reporting.md` with these sections:

**1. Question:** The question you're answering with data (e.g., "How has revenue trended over the past year?")

**2. Data Summary:** Source, time period, granularity, dimensions, size (e.g., "Analytics DB, Jan-Dec 2024, monthly, revenue by segment, 24 rows")

**3. Visualization:**
- Chart type selected (e.g., "Multi-line chart with annotations")
- Rationale (why this chart? question type, data structure, chart advantages)
- Design decisions (Y-axis scale, labels, annotations, colors)
- Chart specification (embed image, code, or detailed spec with axes, series, annotations)

**4. Narrative:** (Headline → Pattern → Context → Meaning → Action structure from above)
- Headline: Insight-first one-liner
- Pattern: What you see
- Context: vs benchmark/target/history
- Meaning: Why it matters
- Actions: What to do next

**5. Validation:** Self-check with rubric (Clarity ✓, Accuracy ✓, Insight ✓, Actionability ✓, Accessibility ✓)

**6. Appendix (optional):** Raw data, alternatives considered, statistical tests, assumptions

See [resources/template.md](resources/template.md) for full template with examples.

---

## Common Mistakes

**Chart Selection Errors**

❌ **Pie chart for >5 categories:** Hard to compare angles accurately
✓ **Use horizontal bar chart:** Position on common scale is more accurate

❌ **Line chart for categorical data:** Implies continuity that doesn't exist (e.g., revenue by product)
✓ **Use bar chart:** Discrete categories

❌ **3D charts:** Perspective distorts values, adds no information
✓ **Use 2D with color/size:** Clearer, more accurate

**Design Mistakes**

❌ **Y-axis doesn't start at zero (bar chart):** Exaggerates differences
✓ **Start at zero for bar/column:** Accurate visual proportion

❌ **Dual Y-axes with different scales:** Misleading correlations
✓ **Use small multiples or index to 100:** Compare shapes, not scales

❌ **Rainbow color scheme:** Not colorblind-safe, no perceptual ordering
✓ **Sequential (light→dark) or diverging (blue→white→red) palette**

**Narrative Failures**

❌ **Title: "Revenue by Month":** Descriptive, not insightful
✓ **"Revenue up 30% YoY, driven by Enterprise":** Insight-first

❌ **No context:** "Revenue is $2.6M" (vs what?)
✓ **Add benchmark:** "Revenue $2.6M, 15% above $2.25M target"

❌ **Pattern without meaning:** "Revenue increased" (so what?)
✓ **Interpret:** "Revenue up 30%, suggests Enterprise product-market fit, informs 2025 hiring plan"

❌ **No actions:** Ends with "interesting pattern"
✓ **Recommend:** "Hire 2 Enterprise AEs, investigate SMB churn"

---

## Resources

- **Simple cases:** Use [resources/template.md](resources/template.md) for question profiling → chart selection → narrative
- **Complex cases:** Study [resources/methodology.md](resources/methodology.md) for dashboards, small multiples, interactive visualizations, advanced chart types
- **Self-assessment:** [resources/evaluators/rubric_visualization_choice_reporting.json](resources/evaluators/rubric_visualization_choice_reporting.json)

**Further reading:**
- "Storytelling with Data" by Cole Nussbaumer Knaflic (chart choice, decluttering, narrative)
- "The Visual Display of Quantitative Information" by Edward Tufte (principles, chart junk, data-ink ratio)
- "Show Me the Numbers" by Stephen Few (dashboard design, perceptual principles)
