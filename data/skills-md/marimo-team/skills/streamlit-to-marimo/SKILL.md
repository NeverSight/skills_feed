---
name: streamlit-to-marimo
description: Convert a Streamlit app to a marimo notebook
---

# Converting Streamlit Apps to Marimo

For general marimo notebook conventions (cell structure, PEP 723 metadata, output rendering, `marimo check`, variable naming, etc.), refer to the `marimo-notebook` skill. This skill focuses specifically on **mapping Streamlit concepts to marimo equivalents**.

## Steps

1. **Read the Streamlit app** to understand its widgets, layout, and state management.

2. **Create a new marimo notebook** following the `marimo-notebook` skill conventions. Add all dependencies the Streamlit app uses (pandas, plotly, altair, etc.) — but replace `streamlit` with `marimo`. You should not overwrite the original file. 

3. **Map Streamlit components to marimo equivalents** using the reference tables below. Key principles:
   - UI elements are **assigned to variables** and their current value is accessed via `.value`.
   - Cells that reference a UI element automatically re-run when the user interacts with it — no callbacks needed.

4. **Handle conceptual differences** in execution model, state, and caching (see below).

5. **Run `uvx marimo check`** on the result and fix any issues.

## Widget Mapping Reference

### Input Widgets

| Streamlit | marimo | Notes |
|-----------|--------|-------|
| `st.slider()` | `mo.ui.slider()` | |
| `st.select_slider()` | `mo.ui.slider(steps=[...])` | Pass discrete values via `steps` |
| `st.text_input()` | `mo.ui.text()` | |
| `st.text_area()` | `mo.ui.text_area()` | |
| `st.number_input()` | `mo.ui.number()` | |
| `st.checkbox()` | `mo.ui.checkbox()` | |
| `st.toggle()` | `mo.ui.switch()` | |
| `st.radio()` | `mo.ui.radio()` | |
| `st.selectbox()` | `mo.ui.dropdown()` | |
| `st.multiselect()` | `mo.ui.multiselect()` | |
| `st.date_input()` | `mo.ui.date()` | |
| `st.time_input()` | `mo.ui.text()` | No dedicated time widget |
| `st.file_uploader()` | `mo.ui.file()` | Use `.contents()` to read bytes |
| `st.color_picker()` | `mo.ui.text(value="#000000")` | No dedicated color picker |
| `st.button()` | `mo.ui.button()` or `mo.ui.run_button()` | Use `run_button` for triggering expensive computations |
| `st.download_button()` | `mo.download()` | Returns a download link element |
| `st.form()` + `st.form_submit_button()` | `mo.ui.form(element)` | Wraps any element so its value only updates on submit |

### Display Elements

| Streamlit | marimo | Notes |
|-----------|--------|-------|
| `st.write()` | `mo.md()` or last expression | |
| `st.markdown()` | `mo.md()` | Supports f-strings: `mo.md(f"Value: {x.value}")` |
| `st.latex()` | `mo.md(r"$...$")` | marimo uses KaTeX; see `references/latex.md` |
| `st.code()` | `mo.md("```python\n...\n```")` | |
| `st.dataframe()` | `df` (last expression) | DataFrames render as interactive marimo widgets natively; use `mo.ui.dataframe(df)` only for no-code transformations |
| `st.table()` | `df` (last expression) | Use `mo.ui.table(df)` if you need row selection |
| `st.metric()` | `mo.stat()` | |
| `st.json()` | `mo.json()` or `mo.tree()` | `mo.tree()` for interactive collapsible view |
| `st.image()` | `mo.image()` | |
| `st.audio()` | `mo.audio()` | |
| `st.video()` | `mo.video()` | |

### Charts

| Streamlit | marimo | Notes |
|-----------|--------|-------|
| `st.plotly_chart(fig)` | `fig` (last expression) | Use `mo.ui.plotly(fig)` for selections |
| `st.altair_chart(chart)` | `chart` (last expression) | Use `mo.ui.altair_chart(chart)` for selections |
| `st.pyplot(fig)` | `fig` (last expression) | Use `mo.ui.matplotlib(fig)` for interactive matplotlib |

### Layout

| Streamlit | marimo | Notes |
|-----------|--------|-------|
| `st.sidebar` | `mo.sidebar([...])` | Pass a list of elements |
| `st.columns()` | `mo.hstack([...])` | Use `widths=[...]` for column ratios |
| `st.tabs()` | `mo.ui.tabs({...})` | Dict of `{"Tab Name": content}` |
| `st.expander()` | `mo.accordion({...})` | Dict of `{"Title": content}` |
| `st.container()` | `mo.vstack([...])` | |
| `st.empty()` | `mo.output.replace()` | |
| `st.progress()` | `mo.status.progress_bar()` | |
| `st.spinner()` | `mo.status.spinner()` | Context manager |

## Key Conceptual Differences

### Execution Model

Streamlit reruns the **entire script** top-to-bottom on every interaction. Marimo uses a **reactive cell DAG** — only cells that depend on changed variables re-execute.

- No need for `st.rerun()` — reactivity is automatic.
- No need for `st.stop()` — structure cells so downstream cells naturally depend on upstream values.

### State Management

| Streamlit | marimo |
|-----------|--------|
| `st.session_state["key"]` | Regular Python variables between cells |
| Callback functions (`on_change`) | Cells referencing `widget.value` re-run automatically |
| `st.query_params` | `mo.query_params` |

### Caching

| Streamlit | marimo |
|-----------|--------|
| `@st.cache_data` | `@mo.cache` | Caches based on function arguments; marimo-aware |
| `@st.cache_resource` | `@mo.persistent_cache` | Persists across notebook restarts (serializes to disk) |

`@mo.cache` is the primary caching decorator — it works like `functools.cache` but is aware of marimo's reactivity. `@mo.persistent_cache` goes further by persisting results to disk across sessions, useful for expensive computations like model training.

### Multi-Page Apps

Marimo offers two approaches for multi-page Streamlit apps:

- **Single notebook with routing**: Use `mo.routes` with `mo.nav_menu` or `mo.sidebar` to build multiple "pages" (tabs/routes) inside one notebook.
- **Multiple notebooks as a gallery**: Run a folder of notebooks with `marimo run folder/` to serve them as a gallery with navigation.

### Deploying 

marimo features molab to host marimo apps instead of the streamlit community cloud. You can generate an "open in molab" button via the `add-molab-badge` skill. 

### Custom components 

streamlit has a feature for custom components. These are not compatible with marimo. You might be able to generate an equivalent anywidget via the `marimo-anywidget` skill but discuss this with the user before working on that. 
