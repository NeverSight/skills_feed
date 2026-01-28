---
name: streamlit
description: Fast Python framework for building interactive web apps, dashboards, and data visualizations without HTML/CSS/JavaScript. Use when user wants to create data apps, ML demos, dashboards, data exploration tools, or interactive visualizations. Transforms Python scripts into web apps in minutes with automatic UI updates.
---

# Streamlit

## Overview

Streamlit is a Python framework for rapidly building and deploying interactive web applications for data science and machine learning. Create beautiful web apps with just Python - no frontend development experience required. Apps automatically update in real-time as code changes.

## When to Use This Skill

Activate when the user:
- Wants to build a web app, dashboard, or data visualization tool
- Mentions Streamlit explicitly
- Needs to create an ML/AI demo or prototype
- Wants to visualize data interactively
- Asks for a data exploration tool
- Needs interactive widgets (sliders, buttons, file uploads)
- Wants to share analysis results with stakeholders

## Installation and Setup

Check if Streamlit is installed:

```bash
python3 -c "import streamlit; print(streamlit.__version__)"
```

If not installed:

```bash
pip3 install streamlit
```

Create and run your first app:

```bash
# Create app.py with Streamlit code
streamlit run app.py
```

The app opens automatically in your browser at `http://localhost:8501`

## Basic App Structure

Every Streamlit app follows this simple pattern:

```python
import streamlit as st

# Set page configuration (must be first Streamlit command)
st.set_page_config(
    page_title="My App",
    page_icon="📊",
    layout="wide"
)

# Title and description
st.title("My Data App")
st.write("Welcome to my interactive dashboard!")

# Your app code here
# Streamlit automatically reruns from top to bottom when widgets change
```

## Core Capabilities

### 1. Displaying Text and Data

```python
import streamlit as st, pandas as pd
# Text elements
st.title("Main Title")
st.header("Section Header")
st.subheader("Subsection Header")
st.text("Fixed-width text")
st.markdown("**Bold** and *italic* text")
st.caption("Small caption text")

# Code blocks
st.code("""
def hello():
    print("Hello, World!")
""", language="python")

# Display data
df = pd.DataFrame({
    'Column A': [1, 2, 3],
    'Column B': [4, 5, 6]
})

st.dataframe(df)  # Interactive table
st.table(df)      # Static table
st.json({'key': 'value'})  # JSON data

# Metrics
st.metric(
    label="Revenue",
    value="$1,234",
    delta="12%"
)
```

### 2. Interactive Widgets

```python
import streamlit as st
# Text input
name = st.text_input("Enter your name")
email = st.text_input("Email", type="default")
password = st.text_input("Password", type="password")
text = st.text_area("Long text", height=100)

# Numbers
age = st.number_input("Age", min_value=0, max_value=120, value=25)
slider_val = st.slider("Select a value", 0, 100, 50)
range_val = st.slider("Select range", 0, 100, (25, 75))

# Selections
option = st.selectbox("Choose one", ["Option 1", "Option 2", "Option 3"])
options = st.multiselect("Choose multiple", ["A", "B", "C", "D"])
radio = st.radio("Pick one", ["Yes", "No", "Maybe"])

# Checkboxes
agree = st.checkbox("I agree to terms")
show_data = st.checkbox("Show raw data")

# Buttons
if st.button("Click me"):
    st.write("Button clicked!")

# Date and time
date = st.date_input("Select date")
time = st.time_input("Select time")

# File upload
uploaded_file = st.file_uploader("Choose a file", type=['csv', 'xlsx', 'txt'])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)

# Download button
st.download_button(
    label="Download data",
    data=df.to_csv(index=False),
    file_name="data.csv",
    mime="text/csv"
)
```

### 3. Charts and Visualizations

```python
import streamlit as st
import pandas as pd, numpy as np, matplotlib.pyplot as plt
import plotly.express as px
# Sample data
df = pd.DataFrame({
    'x': range(10),
    'y': np.random.randn(10)
})

# Streamlit native charts
st.line_chart(df)
st.area_chart(df)
st.bar_chart(df)

# Scatter plot with map data
map_data = pd.DataFrame(
    np.random.randn(100, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon']
)
st.map(map_data)

# Matplotlib
fig, ax = plt.subplots()
ax.plot(df['x'], df['y'])
ax.set_title("Matplotlib Chart")
st.pyplot(fig)

# Plotly (interactive)
fig = px.scatter(df, x='x', y='y', title="Interactive Plotly Chart")
st.plotly_chart(fig, use_container_width=True)

# Altair, Bokeh, and other libraries also supported
```

### 4. Layout and Containers

```python
import streamlit as st
# Columns
col1, col2, col3 = st.columns(3)
with col1:
    st.header("Column 1")
    st.write("Content here")
with col2:
    st.header("Column 2")
    st.write("More content")
with col3:
    st.header("Column 3")
    st.write("Even more")

# Tabs
tab1, tab2, tab3 = st.tabs(["Overview", "Data", "Settings"])
with tab1:
    st.write("Overview content")
with tab2:
    st.write("Data content")
with tab3:
    st.write("Settings content")

# Expander (collapsible section)
with st.expander("Click to expand"):
    st.write("Hidden content that can be expanded")

# Container
with st.container():
    st.write("This is inside a container")
    st.write("Another line")

# Sidebar
st.sidebar.title("Sidebar")
st.sidebar.selectbox("Choose option", ["A", "B", "C"])
st.sidebar.slider("Sidebar slider", 0, 100)
```

### 5. Status and Progress

```python
import streamlit as st, time
# Success, info, warning, error messages
st.success("Success! Everything worked.")
st.info("This is an informational message.")
st.warning("This is a warning.")
st.error("This is an error message.")

# Progress bar
progress_bar = st.progress(0)
for i in range(100):
    time.sleep(0.01)
    progress_bar.progress(i + 1)

# Spinner (loading indicator)
with st.spinner("Processing..."):
    time.sleep(3)
st.success("Done!")

# Balloons (celebration)
st.balloons()

# Snow (celebration)
# st.snow()
```

### 6. Caching for Performance

```python
import streamlit as st, pandas as pd, time

# Cache data loading (persists across reruns)
@st.cache_data
def load_data():
    time.sleep(2)  # Simulate slow data load
    return pd.read_csv('large_file.csv')

# Cache resource (connections, models)
@st.cache_resource
def load_model():
    # Load ML model (expensive operation)
    return load_my_model()

# Use cached data
df = load_data()  # Only loads once, then cached
model = load_model()  # Cached globally

st.write(f"Loaded {len(df)} rows")
```

### 7. Session State (Persistent Data)

```python
import streamlit as st

# Initialize session state
if 'count' not in st.session_state:
    st.session_state.count = 0

# Increment counter
if st.button("Increment"):
    st.session_state.count += 1

st.write(f"Count: {st.session_state.count}")

# Store user data across reruns
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

name = st.text_input("Name")
if name:
    st.session_state.user_data['name'] = name
    st.write(f"Hello, {st.session_state.user_data['name']}!")
```

## Common Patterns

### Pattern 1: Data Dashboard

```python
import streamlit as st, pandas as pd, plotly.express as px

st.set_page_config(page_title="Sales Dashboard", layout="wide")

# Sidebar filters
st.sidebar.header("Filters")
date_range = st.sidebar.date_input("Date Range", [])
category = st.sidebar.multiselect("Category", ["A", "B", "C"])

# Load data
@st.cache_data
def load_sales_data():
    return pd.read_csv('sales_data.csv')

df = load_sales_data()

# Apply filters
if date_range:
    df = df[df['date'].between(date_range[0], date_range[1])]
if category:
    df = df[df['category'].isin(category)]

# Metrics row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"${df['revenue'].sum():,.0f}")
col2.metric("Orders", f"{len(df):,}")
col3.metric("Avg Order", f"${df['revenue'].mean():.2f}")
col4.metric("Top Product", df['product'].mode()[0])

# Charts
col1, col2 = st.columns(2)
with col1:
    st.subheader("Revenue by Category")
    fig = px.bar(df.groupby('category')['revenue'].sum().reset_index(),
                 x='category', y='revenue')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Revenue Trend")
    fig = px.line(df.groupby('date')['revenue'].sum().reset_index(),
                  x='date', y='revenue')
    st.plotly_chart(fig, use_container_width=True)

# Data table
with st.expander("View Raw Data"):
    st.dataframe(df)
```

### Pattern 2: Data Explorer

```python
import streamlit as st, pandas as pd, plotly.express as px

st.title("📊 Data Explorer")

# File upload
uploaded_file = st.file_uploader("Upload CSV", type=['csv'])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Show basic info
    st.subheader("Dataset Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", len(df))
    col2.metric("Columns", len(df.columns))
    col3.metric("Memory", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

    # Column selection
    st.subheader("Explore Data")
    columns = st.multiselect("Select columns", df.columns.tolist(), default=df.columns.tolist()[:5])

    if columns:
        st.dataframe(df[columns])

        # Statistics
        st.subheader("Statistics")
        st.write(df[columns].describe())

        # Visualization
        st.subheader("Visualize")
        col1, col2 = st.columns(2)

        with col1:
            x_col = st.selectbox("X-axis", columns)
        with col2:
            y_col = st.selectbox("Y-axis", columns)

        chart_type = st.radio("Chart Type", ["Scatter", "Line", "Bar"])

        if chart_type == "Scatter":
            fig = px.scatter(df, x=x_col, y=y_col)
        elif chart_type == "Line":
            fig = px.line(df, x=x_col, y=y_col)
        else:
            fig = px.bar(df, x=x_col, y=y_col)

        st.plotly_chart(fig, use_container_width=True)
```

### Pattern 3: Multi-Page App

Create a multi-page app with file structure:
```
app/
├── main.py
└── pages/
    ├── 1_📊_Dashboard.py
    ├── 2_📈_Analytics.py
    └── 3_⚙️_Settings.py
```

Main page (`main.py`):

```python
import streamlit as st
st.set_page_config(page_title="Multi-Page App", page_icon="🏠")

st.title("Welcome to My App")
st.sidebar.success("Select a page above.")

st.markdown("""
This is the home page. Navigate using the sidebar.
""")
```

Pages automatically appear in the sidebar. Each page is a separate Python file.

## Form Handling

```python
import streamlit as st
# Forms prevent rerun on every widget change
with st.form("my_form"):
    st.write("Fill out the form")

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, max_value=120)
    favorite_color = st.selectbox("Favorite Color", ["Red", "Green", "Blue"])

    # Form submit button
    submitted = st.form_submit_button("Submit")

    if submitted:
        st.write(f"Name: {name}")
        st.write(f"Age: {age}")
        st.write(f"Color: {favorite_color}")
```

## Best Practices

1. **Use caching** - Cache expensive operations with `@st.cache_data` and `@st.cache_resource`
2. **Session state for persistence** - Use `st.session_state` to persist data across reruns
3. **Organize with containers** - Use columns, tabs, and expanders for clean layouts
4. **Forms for multiple inputs** - Prevent reruns with forms when collecting multiple inputs
5. **Wide layout for dashboards** - Use `st.set_page_config(layout="wide")` for dashboards
6. **Sidebar for controls** - Put filters and settings in the sidebar
7. **Progress indicators** - Show spinners for long operations

## Common Issues

### Issue: App reruns on every interaction

Use `st.form()` to batch inputs or `st.session_state` to control behavior.

### Issue: Slow performance

Cache expensive operations:

```python
@st.cache_data
def expensive_computation(param):
    # Your code here
    return result
```

### Issue: State not persisting

Use session state:

```python
if 'my_var' not in st.session_state:
    st.session_state.my_var = initial_value
```

## Resources

- **references/api_reference.md**: Quick reference for common Streamlit components
- Official docs: https://docs.streamlit.io/
- API reference: https://docs.streamlit.io/develop/api-reference
- Gallery: https://streamlit.io/gallery
- Community: https://discuss.streamlit.io/
