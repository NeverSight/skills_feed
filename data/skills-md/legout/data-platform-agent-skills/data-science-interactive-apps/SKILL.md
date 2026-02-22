---
name: data-science-interactive-apps
description: "Interactive web apps for data science: Streamlit, Panel, and Gradio. Use for prototyping ML models, creating data exploration dashboards, and sharing insights with non-technical stakeholders."
dependsOn: ["@data-science-notebooks", "@data-science-model-evaluation"]
---

# Interactive Web Apps

Use this skill for building lightweight web interfaces to ML models, data visualizations, and analytical tools.

## When to use this skill

- **ML model demos** — let stakeholders interact with predictions
- **Data exploration tools** — filter, visualize, drill down
- **Internal dashboards** — monitoring, reporting, self-service analytics
- **Prototyping** — validate UX before full engineering investment
- **A/B test interfaces** — experiment with different presentations

## Tool selection guide

| Tool | Best For | Strengths |
|---|---|---|
| **Streamlit** | Rapid ML demos, data apps | Simplest API, large community, great for Python devs |
| **Panel** | Complex dashboards, reactive layouts | Jupyter integration, flexible layout, HoloViz ecosystem |
| **Gradio** | ML model sharing, Hugging Face | Built-in sharing, model introspection, API generation |
| **Dash (Plotly)** | Production dashboards | Fine-grained control, React backend |
| **NiceGUI** | Desktop + web apps | Native-like UI, async support |

## Quick start: Streamlit

```python
# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Sales Dashboard")

# Sidebar controls
region = st.sidebar.selectbox("Region", ["All", "North", "South", "East", "West"])

# Load and filter data
df = pd.read_parquet("sales.parquet")
if region != "All":
    df = df[df['region'] == region]

# Display metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${df['sales'].sum():,.0f}")
col2.metric("Orders", len(df))
col3.metric("Avg Order", f"${df['sales'].mean():.2f}")

# Visualization
fig = px.line(df.groupby('date')['sales'].sum().reset_index(), x='date', y='sales')
st.plotly_chart(fig, use_container_width=True)

# Data table
st.dataframe(df.head(100))
```

Run: `streamlit run app.py`

## Quick start: Gradio

```python
import gradio as gr
from transformers import pipeline

# Load model (example: sentiment analysis)
classifier = pipeline("sentiment-analysis")

def predict(text):
    result = classifier(text)[0]
    return result['label'], result['score']

interface = gr.Interface(
    fn=predict,
    inputs=gr.Textbox(lines=2, placeholder="Enter text..."),
    outputs=[gr.Label(label="Sentiment"), gr.Number(label="Confidence")],
    title="Sentiment Analysis",
    description="Enter text to analyze sentiment"
)

interface.launch()
```

## Quick start: Panel

```python
import panel as pn
import hvplot.pandas
import pandas as pd

pn.extension()

df = pd.read_parquet("data.parquet")

# Widgets
region = pn.widgets.Select(name='Region', options=['All'] + df['region'].unique().tolist())
metric = pn.widgets.RadioBoxGroup(name='Metric', options=['sales', 'profit', 'units'])

# Reactive function
@pn.depends(region, metric)
def plot(region, metric):
    data = df if region == 'All' else df[df['region'] == region]
    return data.hvplot.line(x='date', y=metric, title=f'{metric.title()} by Date')

# Layout
app = pn.Column(
    "# Sales Dashboard",
    pn.Row(region, metric),
    plot
)

app.servable()
```

Run: `panel serve app.py`

## Core design principles

### 1) Start simple, iterate

- MVP with one widget + one visualization
- Add complexity only when needed
- Test with real users early

### 2) Optimize for the audience

| Audience | Approach |
|---|---|
| Executives | Key metrics, simple filters, clean layout |
| Data scientists | Raw data access, parameter tuning, debug info |
| Operations | Refresh buttons, alerts, mobile-friendly |

### 3) Handle state carefully

```python
# Streamlit: use session_state for persistence
if 'counter' not in st.session_state:
    st.session_state.counter = 0

st.session_state.counter += 1
```

### 4) Never expose secrets

```python
# ✅ Use st.secrets (Streamlit Cloud) or environment variables
api_key = st.secrets["openai_api_key"]

# ❌ Never hardcode
api_key = "sk-..."
```

## Deployment options

| Platform | Best For | Notes |
|---|---|---|
| **Streamlit Community Cloud** | Free sharing | GitHub integration, public by default |
| **Hugging Face Spaces** | ML demos | Free tier, Gradio/Streamlit/Docker |
| **Panel + Cloud Run/Heroku** | Custom hosting | More control, requires setup |
| **Docker + any cloud** | Enterprise | Scalable, private, more work |

## Common anti-patterns

- ❌ Loading data on every interaction (use caching)
- ❌ Blocking the UI with long computations
- ❌ No error handling for edge cases
- ❌ Hardcoded file paths or credentials
- ❌ Too many widgets (cognitive overload)
- ❌ No mobile consideration

## Progressive disclosure

- `references/streamlit-advanced.md` — Caching, custom components, multipage apps
- `references/panel-holoviz.md` — Linked brushing, geographic visualizations
- `references/gradio-ml.md` — Model sharing, API generation, Spaces deployment
- `references/app-testing.md` — Automated testing for interactive apps
- `references/production-deployment.md` — Docker, authentication, scaling

## Related skills

- `@data-science-notebooks` — Prototype in notebooks, convert to apps
- `@data-science-model-evaluation` — Present model metrics in apps
- `@data-engineering-orchestration` — Connect apps to production pipelines

## References

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Panel Documentation](https://panel.holoviz.org/)
- [Gradio Documentation](https://www.gradio.app/docs)
- [Hugging Face Spaces](https://huggingface.co/spaces)
