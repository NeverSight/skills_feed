---
name: data-visualization
description: EDA, dashboards, Matplotlib, Seaborn, Plotly, and BI tools. Use for creating visualizations, exploratory analysis, or dashboards.
sasmp_version: "1.3.0"
bonded_agent: 05-visualization-communication
bond_type: PRIMARY_BOND
---

# Data Visualization

Create compelling visualizations to explore and communicate data insights.

## Quick Start

### Matplotlib Basics
```python
import matplotlib.pyplot as plt

# Line plot
plt.figure(figsize=(10, 6))
plt.plot(x, y, marker='o', linestyle='-', color='blue', label='Series 1')
plt.xlabel('X Label')
plt.ylabel('Y Label')
plt.title('Title')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# Bar chart
plt.bar(categories, values, color='skyblue', edgecolor='black')
plt.xlabel('Categories')
plt.ylabel('Values')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

### Seaborn for Statistical Plots
```python
import seaborn as sns

# Set style
sns.set_style("whitegrid")

# Distribution
sns.histplot(data=df, x='value', kde=True, bins=30)

# Box plot
sns.boxplot(data=df, x='category', y='value')

# Violin plot
sns.violinplot(data=df, x='category', y='value')

# Heatmap
corr = df.corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)

# Pairplot
sns.pairplot(df, hue='target', diag_kind='kde')
```

## Exploratory Data Analysis

```python
# Quick overview
df.info()
df.describe()

# Missing values
df.isnull().sum()

# Value counts
df['category'].value_counts().plot(kind='bar')

# Distribution
df.hist(figsize=(12, 10), bins=30)
plt.tight_layout()
plt.show()

# Correlation matrix
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm',
            center=0, square=True)
plt.title('Correlation Matrix')
plt.show()
```

## Interactive Visualizations with Plotly

```python
import plotly.express as px
import plotly.graph_objects as go

# Interactive scatter
fig = px.scatter(df, x='feature1', y='target',
                 color='category', size='value',
                 hover_data=['name', 'date'],
                 title='Interactive Scatter Plot')
fig.show()

# Time series
fig = px.line(df, x='date', y='value', color='category',
              title='Time Series')
fig.update_xaxes(rangeslider_visible=True)
fig.show()

# 3D scatter
fig = px.scatter_3d(df, x='x', y='y', z='z',
                    color='category', size='value')
fig.show()
```

## Dashboard with Plotly Dash

```python
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Sales Dashboard'),

    dcc.Dropdown(
        id='category-dropdown',
        options=[{'label': cat, 'value': cat}
                for cat in df['category'].unique()],
        value=df['category'].unique()[0]
    ),

    dcc.Graph(id='sales-graph'),

    dcc.RangeSlider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=[df['year'].min(), df['year'].max()],
        marks={str(year): str(year)
              for year in df['year'].unique()}
    )
])

@app.callback(
    Output('sales-graph', 'figure'),
    [Input('category-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_graph(selected_category, year_range):
    filtered_df = df[
        (df['category'] == selected_category) &
        (df['year'] >= year_range[0]) &
        (df['year'] <= year_range[1])
    ]
    fig = px.line(filtered_df, x='date', y='sales')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
```

## Subplots

```python
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Top left
axes[0, 0].hist(data1, bins=30)
axes[0, 0].set_title('Histogram')

# Top right
axes[0, 1].scatter(x, y)
axes[0, 1].set_title('Scatter')

# Bottom left
axes[1, 0].plot(x, y)
axes[1, 0].set_title('Line Plot')

# Bottom right
axes[1, 1].boxplot([data1, data2, data3])
axes[1, 1].set_title('Box Plot')

plt.tight_layout()
plt.show()
```

## Visualization Best Practices

1. **Choose the right chart type:**
   - Comparison: Bar chart
   - Distribution: Histogram, box plot
   - Relationship: Scatter plot
   - Time series: Line chart
   - Composition: Pie chart, stacked bar

2. **Design principles:**
   - Clear labels and titles
   - Appropriate color schemes
   - Remove chart junk
   - Consistent formatting
   - Accessibility (color-blind friendly)

3. **Common pitfalls to avoid:**
   - Misleading axes (non-zero baseline)
   - Too many colors
   - 3D charts (distort perception)
   - Pie charts with many categories
   - Dual y-axes (confusing)

## Color Palettes

```python
# Seaborn palettes
sns.color_palette("viridis", as_cmap=True)
sns.color_palette("coolwarm", as_cmap=True)
sns.color_palette("Set2")

# Custom colors
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
```

## Export Figures

```python
# High-resolution PNG
plt.savefig('figure.png', dpi=300, bbox_inches='tight')

# Vector format (PDF, SVG)
plt.savefig('figure.pdf', bbox_inches='tight')
plt.savefig('figure.svg', bbox_inches='tight')
```
