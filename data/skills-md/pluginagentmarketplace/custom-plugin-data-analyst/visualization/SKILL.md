---
name: visualization
description: Data visualization design, tools, and storytelling for impactful analytics presentations
version: "2.0.0"
sasmp_version: "2.0.0"
bonded_agent: 04-visualization-architect
bond_type: PRIMARY_BOND

# Skill Configuration
config:
  atomic: true
  retry_enabled: true
  max_retries: 3
  backoff_strategy: exponential

# Parameter Validation
parameters:
  tool_focus:
    type: string
    required: true
    enum: [tableau, powerbi, python, r, all]
    default: all
  skill_level:
    type: string
    required: true
    enum: [beginner, intermediate, advanced]
    default: beginner
  audience_type:
    type: string
    required: false
    enum: [executive, technical, business, public]
    default: business

# Observability
observability:
  logging_level: info
  metrics: [dashboard_views, interaction_rate, load_time]
---

# Data Visualization Skill

## Overview
Master the art and science of data visualization to communicate insights effectively using modern tools and design principles.

## Core Topics

### Visualization Principles
- Chart selection guidelines
- Color theory for data visualization
- Visual hierarchy and attention
- Accessibility in visualization

### Tools & Platforms
- Tableau (dashboards, calculated fields, LOD expressions)
- Power BI (DAX, data modeling, reports)
- Python (Matplotlib, Seaborn, Plotly)
- R (ggplot2, Shiny)

### Chart Types
- Comparison charts (bar, column, dot plot)
- Trend charts (line, area, slope)
- Distribution charts (histogram, box plot, violin)
- Relationship charts (scatter, bubble, heatmap)
- Composition charts (pie, treemap, stacked bar)

### Data Storytelling
- Narrative structure for data presentations
- Annotation and callout techniques
- Interactive dashboard design
- Executive presentation best practices

## Learning Objectives
- Select appropriate visualization for data and audience
- Create professional dashboards in Tableau and Power BI
- Design effective data stories
- Apply visualization best practices

## Error Handling

| Error Type | Cause | Recovery |
|------------|-------|----------|
| Data connection failed | Source unavailable | Check connection, use cached data |
| Slow dashboard | Too much data | Aggregate, filter, or use extracts |
| Chart unreadable | Poor design choice | Apply chart selection guidelines |
| Accessibility issue | Color/contrast | Use colorblind-safe palette |
| Mobile display broken | Non-responsive | Redesign for mobile-first |

## Related Skills
- statistics (for data to visualize)
- programming (for programmatic visualization)
- career (for presenting to stakeholders)
