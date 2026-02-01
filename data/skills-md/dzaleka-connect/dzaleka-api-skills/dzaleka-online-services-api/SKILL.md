---
name: dzaleka-online-services-api
description: Interact with the Dzaleka Online Services API to fetch community data (services, events, news, photos, jobs) or search across collections. Use when the user asks for community information or resources in Dzaleka.
license: MIT
metadata:
  version: "1.0.0"
  author: Dzaleka Digital Heritage Team
  tags: "api, dzaleka, community-data, rest"
  platforms: "claude-code, codex, chatgpt"
---

# Dzaleka Online Services API Skill

## Overview

This skill allows agents to interact with the **Dzaleka Online Services REST API** to retrieve data about the Dzaleka community.
It supports fetching lists of services, events, resources, news, photos, jobs, and documentation, as well as searching across these collections.

## When to Use

Use this skill when:
- The user asks for information about services, events, or jobs in Dzaleka.
- You need to search for specific community resources or news.
- You are retrieving list data to display or process.

## API Endpoints

See [references/endpoints.md](references/endpoints.md) for the complete list of endpoints and parameters.

Base URL: `https://services.dzaleka.com/api`

### Quick Reference

- **Search:** `GET /api/search?q=...`
- **Services:** `GET /api/services`
- **Events:** `GET /api/events`

## API Endpoints

Base URL:

```
https://services.dzaleka.com/api
```

### 1) Search

```
GET /api/search?q=<term>&collections=<list>&limit=<n>
```

- `q`: required search term (min 2 characters).
- `collections`: optional comma-separated collections (services, events, resources, news, photos, jobs, docs).
- `limit`: optional max results per collection.
**Example:**

```
GET /api/search?q=education&collections=resources,events&limit=5
```

### 2) Collections

Fetch all items from each collection:

| Resource | Path |
|----------|------|
| Services | `/api/services` |
| Events   | `/api/events` |
| Resources| `/api/resources` |
| News     | `/api/news` |
| Photos   | `/api/photos` |
| Jobs     | `/api/jobs` |
| Docs     | `/api/docs` |

**Example:**

```
curl https://services.dzaleka.com/api/services
```

## Expected Responses

Most endpoints return a JSON object wrapping the results or data.

### Standard Collections (Services, Events, etc.) & Search

Returns a `status` and `results` (or collection-keyed results for search).

```json
{
  "status": "success",
  "results": [
    {
      "id": "community-health-service",
      "title": "Community Health Service",
      ...
    }
  ]
}
```

### Docs Endpoint

The `/api/docs` endpoint returns a slightly different structure:

```json
{
  "status": "success",
  "data": {
    "docs": [
      {
        "id": "about",
        "title": "About Dzaleka Online Services",
        ...
      }
    ]
  }
}
```

Errors follow standard HTTP status codes but also return a JSON body:

```json
{
  "status": "error",
  "message": "Search query must be at least 2 characters long"
}
```

* **400 — Bad Request**: e.g., validation errors
* **429 — Too Many Requests**: rate limit exceeded
* **500 — Server Error**

Agents should check for `status === 'success'` and handle gracefully.

## Examples

### JavaScript Fetch

```javascript
async function fetchServices() {
  const res = await fetch("https://services.dzaleka.com/api/services");
  const data = await res.json();
  if (data.status === 'success') {
    console.log(data.results);
  } else {
    console.error('API Error:', data.message);
  }
}
```

### Python Requests

```python
import requests

url = "https://services.dzaleka.com/api/events"
resp = requests.get(url)
data = resp.json()

if data.get('status') == 'success':
    events = data.get('results', [])
    print(events)
else:
    print("Error:", data.get('message'))
```

## Best Practices

* **Rate limits:** Respect typical limits (e.g., 60 requests/minute).
* **Search filters:** Use `collections` and `limit` to reduce response size.
* **Error handling:** Check the `status` field in the response.
* **CORS support:** Frontends can fetch directly from browsers.

## Do’s & Don’ts

### Do

* Check `status` property before accessing `results`.
* Handle the nested structure of `/api/docs` correctly (`data.data.docs`).
* Use explicit paths.

### Don’t

* Assume a flat array response.
* Assume write capabilities (GET only).

## References

- [API Endpoints](references/endpoints.md)
- [Data Schemas](references/schemas.md)
- [Error Handling](references/errors.md)
- [Usage Patterns](references/usage-patterns.md)
- [Official API Docs](https://services.dzaleka.com/api-docs/)
- Base URL: `https://services.dzaleka.com/api`
