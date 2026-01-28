---
name: api-integration
description: Design and implement REST API integrations with proper error handling, authentication, rate limiting, and testing. Use when building API clients, integrating third-party services, or when users mention API, REST, webhooks, HTTP requests, or service integration.
license: MIT
metadata:
  author: agent-skills-demo
  version: "1.0"
  category: integration
compatibility: Requires Python 3.8+ with requests library, or Node.js 14+ with fetch/axios
---

# API Integration Skill

## When to Use This Skill

Use this skill when:
- Building a client to consume a REST API
- Integrating third-party services (Stripe, Twilio, etc.)
- Implementing webhooks
- Creating or testing HTTP endpoints
- Users mention "API", "REST", "integration", "webhook", or "HTTP"

## Integration Process

### 1. API Discovery & Planning

**Understand the API:**
- Review API documentation thoroughly
- Identify base URL and API version
- Note authentication requirements
- Check rate limits and quotas
- Review error response formats

**Plan the integration:**
- List required endpoints
- Map data models
- Identify dependencies
- Plan error handling strategy

### 2. Authentication Setup

Choose the appropriate authentication method:

**API Key:**
```python
headers = {
    'X-API-Key': os.environ.get('API_KEY'),
    'Content-Type': 'application/json'
}
```

**Bearer Token:**
```python
headers = {
    'Authorization': f'Bearer {os.environ.get("ACCESS_TOKEN")}',
    'Content-Type': 'application/json'
}
```

**OAuth 2.0:**
- Implement token refresh logic
- Store tokens securely
- Handle token expiration

**Basic Auth:**
```python
from requests.auth import HTTPBasicAuth
auth = HTTPBasicAuth(username, password)
```

### 3. Client Implementation

See [references/API-PATTERNS.md](references/API-PATTERNS.md) for detailed patterns.

**Basic structure:**
```python
import os
import requests
from typing import Dict, Any, Optional
import time

class APIClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': api_key,
            'Content-Type': 'application/json'
        })
        self.rate_limit_remaining = None
        self.rate_limit_reset = None
    
    def _request(
        self, 
        method: str, 
        endpoint: str, 
        **kwargs
    ) -> Dict[str, Any]:
        """Make HTTP request with error handling."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            
            # Track rate limits
            self.rate_limit_remaining = response.headers.get('X-RateLimit-Remaining')
            self.rate_limit_reset = response.headers.get('X-RateLimit-Reset')
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            self._handle_http_error(e)
        except requests.exceptions.ConnectionError:
            raise APIConnectionError("Failed to connect to API")
        except requests.exceptions.Timeout:
            raise APITimeoutError("Request timed out")
        except requests.exceptions.RequestException as e:
            raise APIError(f"API request failed: {str(e)}")
    
    def _handle_http_error(self, error):
        """Handle HTTP errors with specific status codes."""
        status_code = error.response.status_code
        
        if status_code == 401:
            raise APIAuthenticationError("Invalid credentials")
        elif status_code == 403:
            raise APIAuthorizationError("Insufficient permissions")
        elif status_code == 404:
            raise APINotFoundError("Resource not found")
        elif status_code == 429:
            retry_after = error.response.headers.get('Retry-After', 60)
            raise APIRateLimitError(f"Rate limit exceeded. Retry after {retry_after}s")
        elif 500 <= status_code < 600:
            raise APIServerError(f"Server error: {status_code}")
        else:
            raise APIError(f"HTTP {status_code}: {error.response.text}")
```

### 4. Error Handling

**Define custom exceptions:**
```python
class APIError(Exception):
    """Base exception for API errors."""
    pass

class APIConnectionError(APIError):
    """Network connection failed."""
    pass

class APIAuthenticationError(APIError):
    """Authentication failed."""
    pass

class APIRateLimitError(APIError):
    """Rate limit exceeded."""
    pass

class APIServerError(APIError):
    """Server-side error."""
    pass
```

**Implement retry logic:**
```python
from functools import wraps
import time

def retry_on_failure(max_attempts=3, backoff_factor=2):
    """Decorator for retrying failed requests."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except (APIConnectionError, APIServerError) as e:
                    if attempt == max_attempts - 1:
                        raise
                    wait_time = backoff_factor ** attempt
                    time.sleep(wait_time)
            return None
        return wrapper
    return decorator
```

### 5. Rate Limiting

**Implement rate limit handling:**
```python
class RateLimiter:
    def __init__(self, calls_per_second: float):
        self.calls_per_second = calls_per_second
        self.min_interval = 1.0 / calls_per_second
        self.last_call = 0
    
    def wait_if_needed(self):
        """Wait if necessary to respect rate limit."""
        elapsed = time.time() - self.last_call
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_call = time.time()
```

### 6. Testing

**Test endpoints with the provided script:**
```bash
python scripts/test-endpoint.py \
    --url "https://api.example.com/v1/users" \
    --method GET \
    --headers '{"Authorization": "Bearer token"}'
```

**Write unit tests:**
```python
import pytest
from unittest.mock import Mock, patch

def test_successful_request(api_client):
    with patch.object(api_client.session, 'request') as mock_request:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'id': 1, 'name': 'Test'}
        mock_request.return_value = mock_response
        
        result = api_client.get_user(1)
        
        assert result['id'] == 1
        assert result['name'] == 'Test'

def test_rate_limit_error(api_client):
    with patch.object(api_client.session, 'request') as mock_request:
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.headers = {'Retry-After': '60'}
        mock_request.return_value = mock_response
        
        with pytest.raises(APIRateLimitError):
            api_client.get_user(1)
```

## Best Practices

### Configuration Management
- Store API keys in environment variables
- Never commit credentials to version control
- Use different keys for dev/staging/production

### Logging
```python
import logging

logger = logging.getLogger(__name__)

def _request(self, method, endpoint, **kwargs):
    logger.info(f"API Request: {method} {endpoint}")
    try:
        response = self.session.request(method, url, **kwargs)
        logger.info(f"API Response: {response.status_code}")
        return response.json()
    except Exception as e:
        logger.error(f"API Error: {str(e)}")
        raise
```

### Response Caching
```python
from functools import lru_cache
from datetime import datetime, timedelta

class CachedAPIClient(APIClient):
    def __init__(self, *args, cache_ttl=300, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache_ttl = cache_ttl
    
    @lru_cache(maxsize=100)
    def get_user(self, user_id: int):
        """Cached user lookup."""
        return self._request('GET', f'/users/{user_id}')
```

### Pagination
```python
def get_all_items(self, endpoint: str) -> list:
    """Fetch all items from paginated endpoint."""
    all_items = []
    page = 1
    
    while True:
        response = self._request('GET', endpoint, params={'page': page})
        items = response.get('data', [])
        
        if not items:
            break
            
        all_items.extend(items)
        
        if not response.get('has_more', False):
            break
            
        page += 1
    
    return all_items
```

### Webhooks
```python
import hmac
import hashlib

def verify_webhook_signature(
    payload: bytes, 
    signature: str, 
    secret: str
) -> bool:
    """Verify webhook signature."""
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, expected)
```

## Common Patterns

### Async/Await (Python)
```python
import aiohttp
import asyncio

class AsyncAPIClient:
    async def fetch(self, endpoint: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/{endpoint}") as response:
                return await response.json()
```

### Batch Requests
```python
def batch_create(self, items: list, batch_size: int = 100):
    """Create items in batches."""
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        self._request('POST', '/batch', json={'items': batch})
```

## Troubleshooting

### Debug Mode
```python
import http.client
http.client.HTTPConnection.debuglevel = 1
```

### Common Issues
- **SSL Certificate errors**: Set `verify=False` temporarily (not for production!)
- **Timeout issues**: Increase timeout: `timeout=30`
- **Large responses**: Use streaming: `stream=True`
- **Rate limits**: Implement exponential backoff

## Documentation Template

Document your integration:
```markdown
# [Service Name] API Integration

## Setup
1. Get API key from [service dashboard]
2. Set environment variable: `export API_KEY=your_key`

## Usage
python
from api_client import ServiceClient
client = ServiceClient(api_key=os.environ['API_KEY'])
users = client.list_users()


## Rate Limits
- 1000 requests per hour
- 10 requests per second

## Error Handling
[List common errors and solutions]
```
