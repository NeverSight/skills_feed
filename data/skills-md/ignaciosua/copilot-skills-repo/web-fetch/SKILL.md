---
name: web-fetch
description: HTTP requests (GET/POST/PUT/DELETE) to URLs. Use for API calls, endpoint testing, or basic scraping.
---

# Web Fetch

Makes HTTP requests and returns response content.

## Usage

```bash
python ~/.copilot/skills/web-fetch/web_fetch.py <url> [options]
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--method` | HTTP method: GET, POST, PUT, DELETE, PATCH, HEAD | GET |
| `-H` | Add header (repeatable) | - |
| `--data` | JSON body for POST/PUT | - |
| `--timeout` | Request timeout in seconds | 30 |
| `--pretty` | Format JSON output nicely | false |

## Output

JSON with:
- `success`: true/false
- `status_code`: HTTP status code
- `headers`: Response headers
- `content`: Response body (parsed JSON or text)
- `content_type`: "json" or "text"
- `error`: Error message if failed

## Examples

### Simple GET
```bash
python ~/.copilot/skills/web-fetch/web_fetch.py https://api.github.com/zen
```

### GET with Headers
```bash
python ~/.copilot/skills/web-fetch/web_fetch.py https://api.github.com/user \
  -H "Authorization: token YOUR_TOKEN"
```

### POST with JSON Data
```bash
python ~/.copilot/skills/web-fetch/web_fetch.py https://httpbin.org/post \
  --method POST \
  --data '{"name": "test", "value": 123}'
```

### Pretty Output
```bash
python ~/.copilot/skills/web-fetch/web_fetch.py https://api.github.com/repos/python/cpython --pretty
```
