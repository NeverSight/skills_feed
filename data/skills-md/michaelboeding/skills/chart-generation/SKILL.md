---
name: chart-generation
description: >
  Use this skill for generating data-driven charts and visualizations using Python.
  Triggers: "create chart", "generate graph", "plot data", "visualize data", "bar chart",
  "line chart", "pie chart", "comparison chart", "positioning matrix", "trend chart",
  "market size chart", "TAM SAM SOM", "growth chart", "data visualization"
  Outputs: PNG/SVG chart images with accurate data representation.
  Used by: competitive-intel-agent, market-researcher-agent, pitch-deck-agent, review-analyst-agent
---

# Chart Generation Skill

Generate accurate, data-driven charts and visualizations using Python (matplotlib/plotly).

**Use this for real data.** For concept art and illustrations, use `image-generation` instead.

## What It Produces

| Chart Type | Use Case | Script |
|------------|----------|--------|
| **Bar Chart** | Compare values across categories | `bar_chart.py` |
| **Line Chart** | Show trends over time | `line_chart.py` |
| **Pie Chart** | Show proportions/percentages | `pie_chart.py` |
| **Positioning Matrix** | 2x2 competitive positioning | `positioning_matrix.py` |
| **Comparison Table** | Feature comparison grid | `comparison_table.py` |
| **TAM/SAM/SOM** | Market size visualization | `tam_sam_som.py` |

## Prerequisites

```bash
pip install matplotlib numpy pillow
```

No API keys required - runs locally.

## When to Use This vs Image Generation

| Scenario | Use This | Use image-generation |
|----------|----------|---------------------|
| Real data from analysis | ✅ | ❌ |
| Accurate numbers/labels | ✅ | ❌ |
| Reproducible charts | ✅ | ❌ |
| Concept/mockup visuals | ❌ | ✅ |
| Artistic illustrations | ❌ | ✅ |
| Icons and graphics | ❌ | ✅ |

---

## Chart Types

### 1. Bar Chart

Compare values across categories.

```bash
python3 ${SKILL_PATH}/skills/chart-generation/scripts/bar_chart.py \
  --labels '["Product A", "Product B", "Product C"]' \
  --values '[85, 62, 45]' \
  --title "Feature Comparison" \
  --ylabel "Score" \
  --output bar_chart.png
```

**Options:**
- `--horizontal` - Horizontal bars instead of vertical
- `--colors` - Custom colors: `'["#4CAF50", "#2196F3", "#FF9800"]'`
- `--show-values` - Display values on bars

---

### 2. Line Chart

Show trends over time or progression.

```bash
python3 ${SKILL_PATH}/skills/chart-generation/scripts/line_chart.py \
  --x '["Jan", "Feb", "Mar", "Apr", "May", "Jun"]' \
  --y '[100, 150, 180, 220, 310, 450]' \
  --title "Monthly Revenue Growth" \
  --xlabel "Month" \
  --ylabel "Revenue ($K)" \
  --output growth_chart.png
```

**Options:**
- `--multi` - Multiple lines: `--y '[[100,150,200], [80,120,180]]' --legend '["Product A", "Product B"]'`
- `--fill` - Fill area under line
- `--markers` - Show data point markers

---

### 3. Pie Chart

Show proportions and percentages.

```bash
python3 ${SKILL_PATH}/skills/chart-generation/scripts/pie_chart.py \
  --labels '["Engineering", "Marketing", "Sales", "Operations"]' \
  --values '[40, 25, 20, 15]' \
  --title "Use of Funds" \
  --output pie_chart.png
```

**Options:**
- `--donut` - Donut chart (hollow center)
- `--explode` - Explode a slice: `--explode 0` (first slice)
- `--show-percent` - Show percentages on slices

---

### 4. Positioning Matrix (2x2)

Competitive positioning on two axes.

```bash
python3 ${SKILL_PATH}/skills/chart-generation/scripts/positioning_matrix.py \
  --companies '["Your Product", "Competitor A", "Competitor B", "Competitor C"]' \
  --x-values '[70, 90, 50, 30]' \
  --y-values '[80, 85, 60, 45]' \
  --x-label "Price (Low → High)" \
  --y-label "Features (Basic → Advanced)" \
  --title "Competitive Positioning" \
  --output positioning.png
```

**Options:**
- `--quadrant-labels` - Label quadrants: `'["Niche", "Leaders", "Laggards", "Challengers"]'`
- `--highlight` - Highlight your position: `--highlight 0`
- `--sizes` - Bubble sizes for market share

---

### 5. Comparison Table

Feature comparison grid as an image.

```bash
python3 ${SKILL_PATH}/skills/chart-generation/scripts/comparison_table.py \
  --features '["Feature A", "Feature B", "Feature C", "Feature D"]' \
  --companies '["You", "Comp A", "Comp B"]' \
  --data '[["✓", "✓", "✗"], ["✓", "✗", "✓"], ["✓", "✓", "✓"], ["✓", "✗", "✗"]]' \
  --title "Feature Comparison" \
  --output comparison.png
```

**Options:**
- `--highlight-column` - Highlight your column: `--highlight-column 0`
- `--colors` - Use colors instead of symbols

---

### 6. TAM/SAM/SOM Chart

Market size visualization (concentric circles).

```bash
python3 ${SKILL_PATH}/skills/chart-generation/scripts/tam_sam_som.py \
  --tam 50 \
  --sam 8 \
  --som 0.5 \
  --unit "B" \
  --title "Market Opportunity" \
  --output market_size.png
```

**Options:**
- `--unit` - "B" for billions, "M" for millions
- `--labels` - Custom labels: `'["Total Market", "Serviceable", "Obtainable"]'`

---

## Usage by Other Skills

### competitive-intel-agent
```python
# Generate positioning matrix from analysis
positioning_matrix.py \
  --companies '["You", "Salesforce", "HubSpot"]' \
  --x-values '[30, 95, 70]' \
  --y-values '[75, 90, 60]'
```

### market-researcher-agent
```python
# Generate TAM/SAM/SOM from research
tam_sam_som.py --tam 120 --sam 15 --som 2.5 --unit "B"
```

### pitch-deck-agent
```python
# Generate traction chart
line_chart.py \
  --x '["Q1", "Q2", "Q3", "Q4"]' \
  --y '[50, 120, 280, 500]' \
  --title "Revenue Growth"
```

### review-analyst-agent
```python
# Generate sentiment distribution
pie_chart.py \
  --labels '["Positive", "Neutral", "Negative"]' \
  --values '[65, 20, 15]' \
  --title "Review Sentiment"
```

---

## Output Formats

All scripts support:
- `--output file.png` - PNG image (default)
- `--output file.svg` - SVG vector
- `--output file.pdf` - PDF document

---

## Styling Options

All scripts support these common options:

| Option | Description | Example |
|--------|-------------|---------|
| `--title` | Chart title | `"Monthly Revenue"` |
| `--width` | Width in inches | `12` |
| `--height` | Height in inches | `8` |
| `--dpi` | Resolution | `150` |
| `--style` | Matplotlib style | `"seaborn"`, `"dark_background"` |
| `--colors` | Custom color palette | `'["#4CAF50", "#2196F3"]'` |
| `--font-size` | Base font size | `12` |

---

## Integration Pattern

Higher-level skills call chart-generation like this:

```markdown
## In competitive-intel-agent workflow:

1. Analyze competitors (gather data)
2. Structure data as JSON
3. Call chart-generation script with data
4. Embed resulting PNG in report
```

**Example flow:**
```python
# 1. Analysis produces this data
data = {
    "companies": ["You", "Competitor A", "Competitor B"],
    "features": [8, 6, 5],
    "prices": [29, 49, 39]
}

# 2. Generate chart
python3 bar_chart.py \
  --labels '["You", "Competitor A", "Competitor B"]' \
  --values '[8, 6, 5]' \
  --title "Feature Count Comparison" \
  --output features.png

# 3. Embed in report
![Feature Comparison](features.png)
```

---

## Example Prompts

**Direct chart creation:**
> "Create a bar chart comparing our features to competitors"

**As part of analysis:**
> "Analyze these companies and generate a positioning matrix"

**Data visualization:**
> "Plot our monthly revenue growth from this data: [100, 150, 220, 350]"

**Market sizing:**
> "Create a TAM/SAM/SOM chart: TAM $50B, SAM $5B, SOM $500M"
