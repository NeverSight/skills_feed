---
name: api-integration
description: Connect to REST APIs, handle authentication, and process JSON responses
---

# API Integration

Connect to external REST APIs and process responses.

## Capabilities

- Make HTTP requests (GET, POST, PUT, DELETE)
- Handle authentication (API keys, OAuth, Bearer tokens)
- Parse and transform JSON responses
- Handle pagination and rate limiting

## Authentication Methods

| Method | Header Format |
|--------|---------------|
| API Key | `X-API-Key: <key>` |
| Bearer | `Authorization: Bearer <token>` |
| Basic | `Authorization: Basic <base64>` |

## Request Template

```python
import requests

response = requests.get(
    "https://api.example.com/v1/resource",
    headers={"Authorization": "Bearer TOKEN"},
    params={"limit": 100}
)
data = response.json()
```

## Error Handling

- 4xx: Client errors - check request parameters
- 5xx: Server errors - implement retry with backoff
- Timeout: Set reasonable timeouts (30s default)
