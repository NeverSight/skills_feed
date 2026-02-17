---
name: visualization
description: Use when "data visualization", "plotting", "charts", "matplotlib", "plotly", "seaborn", "graphs", "figures", "heatmap", "scatter plot", "bar chart", "interactive plots"
version: 1.0.0
---

# Data Visualization

Python libraries for creating static and interactive visualizations.

## Comparison

| Library | Best For | Interactive | Learning Curve |
|---------|----------|-------------|----------------|
| **Matplotlib** | Publication, full control | No | Steep |
| **Seaborn** | Statistical, beautiful defaults | No | Easy |
| **Plotly** | Dashboards, web | Yes | Medium |
| **Altair** | Declarative, grammar of graphics | Yes | Easy |

---

## Matplotlib

Foundation library - everything else builds on it.

**Strengths**: Complete control, publication quality, extensive customization
**Limitations**: Verbose, dated API, learning curve

**Key concepts:**

- **Figure**: The entire canvas
- **Axes**: Individual plot area (a figure can have multiple)
- **Object-oriented API**: `fig, ax = plt.subplots()` - preferred over pyplot

---

## Seaborn

Statistical visualization with beautiful defaults.

**Strengths**: One-liners for complex plots, automatic aesthetics, works with pandas
**Limitations**: Less control than matplotlib, limited customization

**Key concepts:**

- **Statistical plots**: histplot, boxplot, violinplot, regplot
- **Categorical plots**: boxplot, stripplot, swarmplot
- **Matrix plots**: heatmap, clustermap
- Built on matplotlib - use matplotlib for fine-tuning

---

## Plotly

Interactive, web-ready visualizations.

**Strengths**: Interactivity (zoom, pan, hover), web embedding, Dash integration
**Limitations**: Large bundle size, different mental model

**Key concepts:**

- **Express API**: High-level, similar to seaborn (`px.scatter()`)
- **Graph Objects**: Low-level, full control (`go.Figure()`)
- Output as HTML or embedded in web apps

---

## Chart Type Selection

| Data Type | Chart |
|-----------|-------|
| Trends over time | Line chart |
| Distribution | Histogram, box plot, violin |
| Comparison | Bar chart, grouped bar |
| Relationship | Scatter, bubble |
| Composition | Pie, stacked bar |
| Correlation | Heatmap |
| Part-to-whole | Treemap, sunburst |

---

## Design Principles

- **Data-ink ratio**: Maximize data, minimize decoration
- **Color**: Use sparingly, consider colorblind users
- **Labels**: Always label axes, include units
- **Legend**: Only when necessary, prefer direct labeling
- **Aspect ratio**: ~1.6:1 (golden ratio) for most plots

---

## Decision Guide

| Task | Recommendation |
|------|----------------|
| Publication figures | Matplotlib |
| Quick EDA | Seaborn |
| Statistical analysis | Seaborn |
| Interactive dashboards | Plotly |
| Web embedding | Plotly |
| Complex customization | Matplotlib |

## Resources

- Matplotlib: <https://matplotlib.org/stable/gallery/>
- Seaborn: <https://seaborn.pydata.org/examples/>
- Plotly: <https://plotly.com/python/>
