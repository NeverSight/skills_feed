---
name: readthedocs-search-api
description: Query the Read the Docs Search API to find documentation across projects and repositories. Use when searching documentation, finding related docs, finding API documentation, or gathering information about projects on Read the Docs.
metadata:
  source: "https://github.com/readthedocs/readthedocs.org/pull/12601"
---

# Read the Docs Search API

Query the public Read the Docs Search API to find documentation across millions of pages.
This API is available on both Community and Business sites; the base URL changes by host.

## Step-by-step instructions

### 1. Make a search request

Set `RTD_HOST` for your site:

- Community: `https://app.readthedocs.org`
- Business: `https://app.readthedocs.com`

Query the API using:
```
GET ${RTD_HOST}/api/v3/search/?q={query}&page={page}
```

Required parameters:
- `q`: Your search query (e.g., "authentication", "API pagination")
- `page`: Result page number (default: 1)

Note on scoping: You will generally get better and more consistent results by scoping your query to a specific project. Use fielded search syntax inside `q`, for example `project:{project-slug} your terms`.
Examples: `project:docs build`, `project:sphinx configuration`.

### 2. Parse the response

The API returns JSON with this structure:
```json
{
  "count": 1234,
  "next": "https://readthedocs.org/api/v3/search/?q=query&page=2",
  "previous": null,
  "results": [
    {
      "id": "project-name:doc-title",
      "project": "project-name",
      "version": "latest",
      "title": "Documentation Title",
      "path": "/en/latest/path/to/page.html",
      "domain": "project-name.readthedocs.io",
      "highlight": "snippet of matching <mark>text</mark>...",
      "blocks": [
        {
          "id": "section-id",
          "title": "Section Title",
          "path": "/path#section-id"
        }
      ]
    }
  ]
}
```

### 3. Handle pagination

If there are more results, use the `next` URL to fetch the next page. Continue until `next` is null.

## Examples

### Search for authentication documentation
```bash
curl "${RTD_HOST}/api/v3/search/?q=authentication"
```

### Search within a specific project
```bash
curl "${RTD_HOST}/api/v3/search/?q=project:docs%20authentication"
```

### Project-scoped quick queries
```bash
# Sphinx
curl "${RTD_HOST}/api/v3/search/?q=project:sphinx%20configuration"
curl "${RTD_HOST}/api/v3/search/?q=project:sphinx%20autodoc"

# Requests
curl "${RTD_HOST}/api/v3/search/?q=project:requests%20proxies"
curl "${RTD_HOST}/api/v3/search/?q=project:requests%20authentication"

# Read the Docs
curl "${RTD_HOST}/api/v3/search/?q=project:readthedocs%20build"
curl "${RTD_HOST}/api/v3/search/?q=project:readthedocs%20redirects"
```

### Search with pagination
```bash
curl "${RTD_HOST}/api/v3/search/?q=API&page=2"
```

### Parse results with Python
```python
import os
import requests

response = requests.get(
    f"{os.environ['RTD_HOST']}/api/v3/search/",
    params={"q": "REST API"}
)

data = response.json()
for result in data['results']:
    print(f"{result['project']}: {result['title']}")
    print(f"  Domain: {result['domain']}")
    print(f"  Path: {result['path']}")
```

### Get all paginated results
```python
def search_all(query):
    all_results = []
    page = 1
    while True:
        response = requests.get(
            f"{os.environ['RTD_HOST']}/api/v3/search/",
            params={"q": query, "page": page}
        )
        data = response.json()
        all_results.extend(data['results'])
        if not data['next']:
            break
        page += 1
    return all_results
```

## Common edge cases

**No authentication required**: The Search API is public and does not require API keys or authentication.

**Rate limiting**: The API applies reasonable rate limits. If you receive HTTP 429, implement exponential backoff.

**Private documentation excluded**: Only publicly available documentation is searchable. Private projects are not included.

**Search delay**: The search index updates with a slight delay. New documentation may not appear immediately.

**Empty results**: If a query returns no results, try simpler keywords or browse the project directly on Read the Docs.

**Project scoping recommended**: The global index is large and queries can be broad. For most use cases, include a `project:{project-slug}` filter in `q` to scope results to the relevant documentation project.
