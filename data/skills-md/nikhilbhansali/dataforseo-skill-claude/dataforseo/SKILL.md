---
name: dataforseo
description: Complete DataForSEO API integration for SEO data and analysis. Use when the user asks for keyword research, search volume, SERP analysis, backlink audits, competitor analysis, rank tracking, domain authority, technical SEO audits, content monitoring, Google Trends, or any SEO-related data queries. Covers all DataForSEO APIs including SERP, Keywords Data, DataForSEO Labs, Backlinks, OnPage, Domain Analytics, Content Analysis, Business Data, Merchant, App Data, and AI Optimization APIs. Outputs CSV files.
---

# DataForSEO API Skill

Universal interface to all DataForSEO APIs for comprehensive SEO data retrieval and analysis.

## Credential Setup

Before first use, set up credentials:

```python
import sys, os
sys.path.insert(0, os.path.expanduser('~/.agents/skills/dataforseo/scripts'))
from dataforseo_client import save_credentials, verify_credentials

# Get credentials from https://app.dataforseo.com/
login = "your_email@example.com"  # API login (email)
password = "your_api_password"    # API password (from dashboard)

# Verify and save
if verify_credentials(login, password):
    save_credentials(login, password)
    print("Credentials saved!")
```

Credentials stored at `~/.dataforseo_config.json`. To update, run setup again.

## Quick Start

```python
import sys, os
sys.path.insert(0, os.path.expanduser('~/.agents/skills/dataforseo/scripts'))
from dataforseo_client import *

# Example: Get search volume
response = keywords_search_volume(
    keywords=["seo tools", "keyword research"],
    location_name="United States"
)
results = extract_results(response)
csv_path = to_csv(results, "keyword_volumes")
print(f"Results saved to: {csv_path}")
```

## API Selection Guide

| User Request | Function to Use |
|--------------|-----------------|
| Search volume, CPC, competition | `keywords_search_volume()` |
| Keyword ideas/suggestions | `labs_keyword_ideas()` or `labs_related_keywords()` |
| Keywords a site ranks for | `labs_ranked_keywords()` |
| SERP results for keyword | `serp_google_organic()` |
| Local/Maps rankings | `serp_google_maps()` |
| YouTube rankings | `serp_youtube()` |
| Backlink profile | `backlinks_summary()` |
| List of backlinks | `backlinks_list()` |
| Referring domains | `backlinks_referring_domains()` |
| Domain authority/rank | `backlinks_bulk_ranks()` |
| Competing domains | `labs_competitors_domain()` |
| Keyword gap analysis | `labs_domain_intersection()` |
| Link gap analysis | `backlinks_domain_intersection()` |
| Technical page audit | `onpage_instant_pages()` |
| Lighthouse scores | `lighthouse_live()` |
| Technology stack | `domain_technologies()` |
| Brand mentions | `content_search()` |
| Google Trends | `google_trends()` |

## Core Workflow

1. **Import client**: Add skill path and import functions
2. **Call API function**: Pass required parameters
3. **Extract results**: Use `extract_results(response)`
4. **Export to CSV**: Use `to_csv(results, "filename")`

```python
import sys, os
sys.path.insert(0, os.path.expanduser('~/.agents/skills/dataforseo/scripts'))
from dataforseo_client import labs_ranked_keywords, extract_results, to_csv

response = labs_ranked_keywords(
    target="competitor.com",
    location_name="United States",
    language_name="English",
    limit=500
)
results = extract_results(response)
csv_path = to_csv(results, "ranked_keywords")
```

## Default Parameters

Most functions use these defaults:
- `location_name`: "United States" (override with "India", "United Kingdom", etc.)
- `language_name`: "English"
- `limit`: 100 (increase up to 1000 for more results)
- `device`: "desktop" (or "mobile" for SERP)

## Common Location Names
- United States, United Kingdom, India, Germany, Australia, Canada
- For city-level: "New York,New York,United States", "London,England,United Kingdom"

## Output

All results export to CSV at `~/dataforseo_outputs/`. Files auto-named with timestamp if not specified.

## Reference Files

- **API Reference**: `references/api_reference.md` - Complete endpoint documentation
- **Use Cases**: `references/use_cases.md` - Ready-to-use code recipes

## Error Handling

```python
response = some_api_function(...)
if response.get("status_code") == 20000:
    results = extract_results(response)
    # Process results
else:
    print(f"Error: {response.get('status_message')}")
```

## Rate Limits & Costs

- 2000 requests/minute max
- Live methods cost more than Standard
- Check usage with `get_user_data()`
- Response includes `cost` field

## Important Notes

1. **Async endpoints**: Some APIs (merchant, app_data, business reviews) create tasks. Check task status separately.
2. **Limits**: Increase `limit` parameter for comprehensive data (default 100, max usually 1000)
3. **Multiple keywords**: Pass as list: `keywords=["kw1", "kw2", "kw3"]`
