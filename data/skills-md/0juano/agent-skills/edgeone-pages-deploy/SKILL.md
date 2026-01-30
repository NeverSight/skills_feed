---
name: edgeone-pages-deploy
description: Deploys static HTML to a public URL instantly with no authentication required. Use when asked to "host this", "deploy this site", "get a public link", "share this HTML", "quick deploy", "publish this page", or any request to make an HTML file publicly accessible via URL. Supports self-contained HTML files with inline CSS/JS.
metadata:
  author: 0juano
  version: "1.0.0"
---

# EdgeOne Pages Deploy

Deploy any HTML file or directory to a public URL in seconds. No authentication, no accounts, no configuration.

## Quick Deploy

```bash
# Single HTML file
scripts/deploy.sh path/to/index.html

# Directory containing index.html
scripts/deploy.sh path/to/site/
```

Returns a public URL like `https://mcp.edgeone.site/share/abc123`.

## How It Works

Uses EdgeOne Pages' public MCP endpoint to deploy HTML content via JSON-RPC.

- **Endpoint:** `https://mcp-on-edge.edgeone.app/mcp-server`
- **Method:** `tools/call` → `deploy-html`
- **Auth:** None required

## Manual Deploy (curl)

```bash
HTML=$(python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))' < index.html)

curl -s -X POST https://mcp-on-edge.edgeone.app/mcp-server \
  -H "Content-Type: application/json" \
  -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/call\",\"params\":{\"name\":\"deploy-html\",\"arguments\":{\"value\":$HTML}}}"
```

## Validation

After deploying, SHOULD verify the URL returns HTTP 200:

```bash
curl -s -o /dev/null -w "%{http_code}" <returned-url>
```

## Constraints

- Single HTML file only — multi-file sites with separate CSS/JS/images are NOT supported
- Self-contained HTML works best (inline styles, inline scripts, base64 images)
- No custom domains
- No delete/update — each deploy creates a new URL
- Link persistence depends on EdgeOne's retention policy

## Requirements

- `curl`
- `python3` (for JSON encoding)
