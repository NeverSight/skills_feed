---
name: data-science-visualization
description: "Data visualization for Python: Matplotlib, Seaborn, Plotly, Altair, hvPlot/HoloViz, and Bokeh. Use when creating exploratory charts, interactive dashboards, publication-quality figures, or choosing the right library for your data and audience."
dependsOn: ["@data-science-eda", "@data-engineering-core"]
---

# Data Visualization

Use this skill for creating effective visualizations: choosing the right library, chart type, and interactivity level for your data and audience.

## When to use this skill

- Choosing a visualization library for a project
- Creating exploratory charts during EDA
- Building interactive dashboards
- Producing publication-quality figures
- Understanding tradeoffs between libraries

## Library selection guide (2026)

| Library | Best For | Interactivity | Learning Curve |
|---|---|---|---|
| **Matplotlib** | Publication-quality static plots, fine control | Static | Moderate |
| **Seaborn** | Statistical visualization, quick EDA | Static | Easy |
| **Plotly** | Interactive web charts, dashboards | High | Easy |
| **Altair** | Declarative statistical charts, large datasets | Medium | Easy |
| **hvPlot/HoloViz** | Large data, linked brushing, geospatial | High | Moderate |
| **Bokeh** | Custom interactive web apps | High | Moderate |

## Quick decision tree

```
Static publication figure?
  → Matplotlib (full control) or Seaborn (quick statistical)

Interactive web/dashboard?
  → Plotly (easiest), Dash (full apps)
  → Panel/HoloViz (complex linked views)
  → Bokeh (custom web apps)

Large datasets (100k+ points)?
  → hvPlot + Datashader (automatic rasterization)
  → Altair (smart aggregation with Vega-Lite)

Declarative grammar preferred?
  → Altair (Vega-Lite) or Plotly Express

Already using Pandas?
  → df.plot() → Matplotlib
  → df.hvplot() → HoloViz
  → px.scatter(df) → Plotly
```

## Core principles

### 1) Match chart to data and question

| Question | Chart Type |
|---|---|
| Distribution? | Histogram, KDE, boxplot, violin |
| Relationship? | Scatter, line, heatmap (correlation) |
| Composition? | Pie (avoid), stacked bar, treemap |
| Comparison? | Bar, grouped bar, dot plot |
| Trend over time? | Line, area, candlestick |
| Geographic? | Choropleth, scatter map, heatmap |

### 2) Maximize data-ink ratio

- Remove unnecessary gridlines, borders, backgrounds
- Use color purposefully (not decoration)
- Label directly when possible
- One message per visualization

### 3) Choose interactivity appropriately

| Audience | Interactivity Level |
|---|---|
| Paper/report | Static (Matplotlib/Seaborn) |
| Presentation | Limited (Plotly static export) |
| Exploratory analysis | High (zoom, pan, filter, hover) |
| Stakeholder dashboard | Medium (linked views, drill-down) |

## Quick examples

### Matplotlib (fine control)

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(x, y, c=colors, alpha=0.6, edgecolors='none')
ax.set_xlabel('Feature X', fontsize=12)
ax.set_ylabel('Target Y', fontsize=12)
ax.set_title('Relationship Analysis', fontsize=14, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
```

### Seaborn (statistical)

```python
import seaborn as sns

# Distribution with KDE
sns.histplot(data=df, x='value', hue='category', kde=True, bins=30)

# Correlation heatmap
corr = df.corr()
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0)

# Categorical comparison
sns.boxplot(data=df, x='category', y='value', palette='viridis')
```

### Plotly (interactive web)

```python
import plotly.express as px

# Scatter with marginal distributions
fig = px.scatter(df, x='x', y='y', color='category', size='size',
                 marginal_x='histogram', marginal_y='rug',
                 hover_data=['label'])
fig.show()

# Faceted small multiples
fig = px.line(df, x='date', y='value', facet_col='category',
              facet_col_wrap=3, height=800)
fig.show()
```

### Altair (declarative, large data)

```python
import altair as alt

# Smart aggregation for large datasets
chart = alt.Chart(df).mark_circle().encode(
    x=alt.X('x:Q', bin=alt.Bin(maxbins=50)),
    y=alt.Y('y:Q', bin=alt.Bin(maxbins=50)),
    size='count()'
).interactive()

chart.save('chart.html')  # Self-contained HTML
```

### hvPlot/HoloViz (large data, linked views)

```python
import hvplot.pandas
import panel as pn

# Linked brushing
scatter = df.hvplot.scatter(x='x', y='y', c='category', 
                            tools=['box_select'], 
                            width=400, height=400)
hist = df.hvplot.hist(y='y', width=400, height=200)

layout = pn.Row(scatter, hist)
layout.servable()
```

### Bokeh (custom web apps)

```python
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, HoverTool

source = ColumnDataSource(df)

p = figure(title="Interactive Plot", tools="pan,wheel_zoom,box_select")
p.circle('x', 'y', source=source, size=10, alpha=0.6)

hover = HoverTool(tooltips=[("X", "@x"), ("Y", "@y"), ("Label", "@label")])
p.add_tools(hover)

show(p)
```

## Anti-patterns

- ❌ Pie charts with many slices (use bar charts)
- ❌ Dual y-axes (hard to read, try normalization or small multiples)
- ❌ 3D charts (distorts perception)
- ❌ Rainbow colormaps (use perceptually uniform: viridis, plasma)
- ❌ Missing labels, titles, or units
- ❌ Overplotting without handling (sampling, alpha, or Datashader)

## Common issues and solutions

| Problem | Solution |
|---|---|
| Overplotting (100k+ points) | Use Datashader (rasterization), hexbin, or 2D histogram |
| Slow interactivity | Reduce data points, use WebGL (Plotly), or pre-aggregate |
| Large file size | Save as JSON (Plotly/Altair) or use static images |
| Color blindness | Use colorblind-friendly palettes (viridis, colorbrewer) |

## Progressive disclosure

- `references/matplotlib-advanced.md` — Subplots, annotations, custom styles
- `references/seaborn-statistical.md` — Complex statistical plots
- `references/plotly-dash.md` — Full dashboards with callbacks
- `references/altair-grammar.md` — Vega-Lite transformations
- `references/holoviz-datashader.md` — Large data visualization
- `references/bokeh-server.md` — Real-time streaming apps

## Related skills

- `@data-science-eda` — Exploration patterns
- `@data-science-interactive-apps` — Dashboard deployment
- `@data-science-notebooks` — Notebook-specific visualization

## References

- [Matplotlib Documentation](https://matplotlib.org/)
- [Seaborn Documentation](https://seaborn.pydata.org/)
- [Plotly Python](https://plotly.com/python/)
- [Altair Documentation](https://altair-viz.github.io/)
- [HoloViz Tutorial](https://holoviz.org/tutorial/)
- [Bokeh Documentation](https://docs.bokeh.org/)
- [Python Graph Gallery](https://python-graph-gallery.com/) (examples by chart type)
