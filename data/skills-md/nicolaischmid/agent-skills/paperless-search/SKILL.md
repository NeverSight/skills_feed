---
name: paperless-search
description: Search documents in Paperless-ngx via REST API. Full-text search, tag/correspondent filtering, and direct links to documents.
license: MIT
metadata:
  author: Nicolai Schmid
  version: 2.0.0
  requires:
    - curl
    - jq
---

# Paperless Document Search

Search your Paperless-ngx document archive via the REST API.

## Configuration

Config file: `~/.config/paperless-search/config.json`

```json
{
  "url": "https://paperless.example.com",
  "token": "your-api-token-here"
}
```

### Getting an API token

1. Log into your Paperless web UI
2. Click your username (top right) → "My Profile"
3. Click the circular arrow button to generate/regenerate a token

### Troubleshooting config

If requests fail, verify the config:

```bash
# Check config exists and is valid JSON
cat ~/.config/paperless-search/config.json | jq .

# Test connection
curl -s -H "Authorization: Token $(jq -r .token ~/.config/paperless-search/config.json)" \
  "$(jq -r .url ~/.config/paperless-search/config.json)/api/documents/?page_size=1" | jq '.count'
```

**Common issues:**

- `401 Unauthorized`: Token is invalid/expired → regenerate in web UI
- `Connection refused`: URL is wrong or server is down
- `null` or parse error: Config file is missing or malformed

If config is broken, guide the user to provide:

1. Their Paperless-ngx URL (e.g., `https://paperless.example.com`)
2. A valid API token from their profile page

Then create/update the config:

```bash
mkdir -p ~/.config/paperless-search
cat > ~/.config/paperless-search/config.json << 'EOF'
{
  "url": "USER_PROVIDED_URL",
  "token": "USER_PROVIDED_TOKEN"
}
EOF
```

## API Examples

```bash
# Load config into variables
PAPERLESS_URL=$(jq -r .url ~/.config/paperless-search/config.json)
PAPERLESS_TOKEN=$(jq -r .token ~/.config/paperless-search/config.json)

# Full-text search
curl -s -H "Authorization: Token $PAPERLESS_TOKEN" \
  "$PAPERLESS_URL/api/documents/?query=invoice+january+2025" | jq '.results[] | {id, title, created}'

# Get document with full OCR content
curl -s -H "Authorization: Token $PAPERLESS_TOKEN" \
  "$PAPERLESS_URL/api/documents/123/" | jq -r '.content'

# List correspondents
curl -s -H "Authorization: Token $PAPERLESS_TOKEN" \
  "$PAPERLESS_URL/api/correspondents/" | jq '.results[] | {id, name}'

# Filter by correspondent
curl -s -H "Authorization: Token $PAPERLESS_TOKEN" \
  "$PAPERLESS_URL/api/documents/?correspondent__id=5" | jq

# Filter by date range
curl -s -H "Authorization: Token $PAPERLESS_TOKEN" \
  "$PAPERLESS_URL/api/documents/?created__date__gte=2024-01-01&created__date__lte=2024-12-31" | jq

# List tags
curl -s -H "Authorization: Token $PAPERLESS_TOKEN" \
  "$PAPERLESS_URL/api/tags/" | jq '.results[] | {id, name}'

# List document types
curl -s -H "Authorization: Token $PAPERLESS_TOKEN" \
  "$PAPERLESS_URL/api/document_types/" | jq '.results[] | {id, name}'
```

## API Reference

| Endpoint                 | Description                          |
| ------------------------ | ------------------------------------ |
| `/api/documents/`        | List/search documents                |
| `/api/documents/{id}/`   | Get single document with full content |
| `/api/tags/`             | List all tags                        |
| `/api/correspondents/`   | List all correspondents              |
| `/api/document_types/`   | List all document types              |

### Query Parameters for `/api/documents/`

| Parameter           | Example                            | Description          |
| ------------------- | ---------------------------------- | -------------------- |
| `query`             | `query=contract+2022`              | Full-text search     |
| `correspondent__id` | `correspondent__id=5`              | Filter by correspondent |
| `tags__id__all`     | `tags__id__all=1,2`                | Must have all tags   |
| `document_type__id` | `document_type__id=3`              | Filter by type       |
| `created__date__gte`| `created__date__gte=2024-01-01`    | Created after        |
| `created__date__lte`| `created__date__lte=2024-12-31`    | Created before       |
| `ordering`          | `ordering=-created`                | Sort order           |
| `page_size`         | `page_size=50`                     | Results per page     |

### Document URL format

When linking to documents, always use the base URL from the config file:

```bash
PAPERLESS_URL=$(jq -r .url ~/.config/paperless-search/config.json)
echo "$PAPERLESS_URL/documents/{id}/details"
```

Do NOT hardcode or guess the URL - always read it from the config.
