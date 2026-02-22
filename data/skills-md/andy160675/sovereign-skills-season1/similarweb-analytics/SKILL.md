---
name: similarweb-analytics
description: "Analyze websites and domains using SimilarWeb traffic data. Get traffic metrics, engagement stats, global rankings, traffic sources, and geographic distribution for comprehensive website research."
---

# SimilarWeb Analytics

Comprehensive website and domain analysis using SimilarWeb traffic data.

## Core Capabilities

- **Traffic Analysis**: Total visits, unique visitors, traffic trends
- **Engagement Metrics**: Bounce rate, pages per visit, average visit duration
- **Global Ranking**: Website ranking over time
- **Traffic Sources**: Marketing channels (desktop and mobile)
- **Geographic Distribution**: Traffic breakdown by country

## API Usage

All APIs use `ApiClient` from `/opt/.manus/.sandbox-runtime`. Common parameters:
- `domain`: Website domain (e.g., "google.com")
- `start_date`: Start date (YYYY-MM). Max 12 months ago
- `end_date`: End date (YYYY-MM). Max 12 months ago, default is 1 month ago (most recent complete month)
- `main_domain_only`: Exclude subdomains if True (default: False)

**Default time ranges vary by API:**
- Global Rank, Visits Total, Unique Visit, Bounce Rate: default **6 months**
- Traffic Sources (Desktop/Mobile), Traffic by Country: default **3 months**

### Get Global Rank

```python
import sys
sys.path.append('/opt/.manus/.sandbox-runtime')
from data_api import ApiClient

client = ApiClient()
result = client.call_api('SimilarWeb/get_global_rank', path_params={'domain': 'amazon.com'})
```

### Get Website Visits Total

```python
import sys
sys.path.append('/opt/.manus/.sandbox-runtime')
from data_api import ApiClient

client = ApiClient()
result = client.call_api('SimilarWeb/get_visits_total',
    path_params={'domain': 'amazon.com'},
    query={'country': 'world', 'granularity': 'monthly', 'start_date': '2025-07', 'end_date': '2025-12'})
```

### Get Unique Visit

```python
import sys
sys.path.append('/opt/.manus/.sandbox-runtime')
from data_api import ApiClient

client = ApiClient()
result = client.call_api('SimilarWeb/get_unique_visit',
    path_params={'domain': 'amazon.com'},
    query={'start_date': '2025-07', 'end_date': '2025-12'})
```

### Get Bounce Rate

```python
import sys
sys.path.append('/opt/.manus/.sandbox-runtime')
from data_api import ApiClient

client = ApiClient()
result = client.call_api('SimilarWeb/get_bounce_rate',
    path_params={'domain': 'amazon.com'},
    query={'country': 'world', 'granularity': 'monthly', 'start_date': '2025-07', 'end_date': '2025-12'})
```

### Get Traffic Sources - Desktop

Returns breakdown by channel: Organic Search, Paid Search, Direct, Display Ads, Email, Referrals, Social Media.

```python
import sys
sys.path.append('/opt/.manus/.sandbox-runtime')
from data_api import ApiClient

client = ApiClient()
result = client.call_api('SimilarWeb/get_traffic_sources_desktop',
    path_params={'domain': 'amazon.com'},
    query={'country': 'world', 'granularity': 'monthly', 'start_date': '2025-07', 'end_date': '2025-12'})
```

### Get Traffic Sources - Mobile

```python
import sys
sys.path.append('/opt/.manus/.sandbox-runtime')
from data_api import ApiClient

client = ApiClient()
result = client.call_api('SimilarWeb/get_traffic_sources_mobile',
    path_params={'domain': 'amazon.com'},
    query={'country': 'world', 'granularity': 'monthly', 'start_date': '2025-07', 'end_date': '2025-12'})
```

### Get Total Traffic by Country

Returns traffic share, visits, pages per visit, average time, bounce rate and rank by country.

- `limit`: Number of countries to return (default: 1, max: 10)
- **Date range limit**: max 3 months (unlike other APIs)

```python
import sys
sys.path.append('/opt/.manus/.sandbox-runtime')
from data_api import ApiClient

client = ApiClient()
result = client.call_api('SimilarWeb/get_total_traffic_by_country',
    path_params={'domain': 'amazon.com'},
    query={'start_date': '2025-10', 'end_date': '2025-12', 'limit': '10'})
```

## When to Use

Invoke APIs when users mention:
- Domain names: "google.com", "amazon.com"
- Traffic queries: "traffic", "visits", "visitors"
- Ranking queries: "rank", "ranking", "how popular"
- Engagement queries: "bounce rate", "engagement"
- Source queries: "traffic sources", "marketing channels"
- Geographic queries: "countries", "geographic"
- Comparison queries: "compare", "vs"

## Data Limitations

- Historical data: max 12 months
- Geography: worldwide only
- Granularity: monthly only
- Latest data: last complete month

## Important: Save Data to Files

API calls may fail mid-execution due to credit depletion. **Always save all retrieved data to files immediately** to avoid data loss and prevent redundant API calls.
