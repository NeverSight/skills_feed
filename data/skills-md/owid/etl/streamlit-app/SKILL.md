---
name: streamlit-app
description: Create or modify Streamlit apps in the Wizard. Use when building new wizard apps, adding Streamlit pages, or working with apps/wizard/ code.
---

# Streamlit Apps in Wizard

Apps live in `apps/wizard/app_pages/`. Run with `make wizard` or `.venv/bin/etlwiz <alias>`.

## Creating a New App

1. Create `apps/wizard/app_pages/your_app/app.py`:

```python
import streamlit as st
st.set_page_config(page_title="Wizard: Your App", page_icon="🪄", layout="wide")

def main():
    st.title("Your App")

main()
```

2. Register in `apps/wizard/config/config.yml` under a section's `apps` list:

```yaml
- title: "Your App"
  alias: your-app
  entrypoint: app_pages/your_app/app.py
  description: "What it does"
  maintainer: "@slack-handle"
  icon: ":material/icon:"
```

## Key Utilities

```python
# Caching (supports ttl, show_time, works outside Streamlit too)
from apps.wizard.utils.components import st_cache_data
@st_cache_data(custom_text="Loading...", ttl="1h")

# URL-synced widgets (shareable state)
from apps.wizard.utils.components import url_persist
url_persist(st.selectbox)(label="Option", options=["a", "b"], key="my_key")
# ⚠️ Booleans stored as "True"/"False" strings in URL

# Charts
from apps.wizard.utils.components import grapher_chart, grapher_chart_from_url
grapher_chart(catalog_path="grapher/ns/ver/ds#var")
grapher_chart(variable_id=123, selected_entities=["France"], tab="map")

# Data loading
from apps.wizard.utils.cached import load_variables_in_dataset, load_variable_data

# Environment & DB
from etl.config import OWID_ENV  # .base_site, .indicators_url, .data_api_url
from etl.db import get_engine
from sqlalchemy.orm import Session
```

## Components (`apps.wizard.utils.components`)

- `st_horizontal()` — flexbox row context manager
- `Pagination(items, items_per_page, pagination_key)` — paginated lists
- `grapher_chart()` / `grapher_chart_from_url()` — OWID charts
- `st_wizard_page_link(alias)` — link to another Wizard page
- `st_tag(name, color, icon)` / `tag_in_md()` — colored badges
- `st_toast_success()` / `st_toast_error()` — toast notifications
- `preview_file(path)` — code preview in expander

## Rules

- `st.set_page_config()` must be the **first** Streamlit command
- Use `@st_cache_data` for expensive operations
- Use `url_persist()` for shareable widget state
- Material icons: `:material/icon_name:` (Google Material Symbols)
- HTTP requests: always `timeout=30` and `.raise_for_status()`
