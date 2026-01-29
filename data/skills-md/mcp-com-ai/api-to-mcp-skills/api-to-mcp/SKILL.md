---
name: api-to-mcp
description: Convert OpenAPI v3 specifications into MCP servers using HAPI CLI. Supports local, Docker, and Cloudflare Workers deployment. Zero code required. Use when you need to expose API functionality as MCP tools or deploy API-based services to multiple hosting platforms.
license: MIT
compatibility: Requires hapi, curl; optionally docker and wrangler for deployment
metadata:
  author: mcp.com.ai agent-skills
  version: "0.1.0"
allowed-tools: Bash(curl:*) Bash(hapi:*) Read Bash(docker:*) Bash(wrangler:*)
---

# API to MCP Server Skill

Convert OpenAPI v3 specifications into fully functional MCP (Model Context Protocol) servers using HAPI CLI — no code required.

## Workflow

### Phase 1: Environment Setup

1. **Verify HAPI CLI installation**
   ```bash
   hapi --version
   ```
   
   If not installed, install using:
   - **Linux/macOS**: `curl -fsSL https://get.mcp.com.ai/hapi.sh | bash`
   - **Windows**: `irm https://get.mcp.com.ai/hapi.ps1 | iex`
   - **Docker**: Use `hapimcp/hapi-cli:latest` image directly

2. **Validate OpenAPI spec** is v3.x (not v2/Swagger). HAPI requires OpenAPI 3.0+ specifications.

### Phase 2: Local Development & Testing

1. **Start local MCP server**
   ```bash
   hapi serve <project-name> \
     --openapi <path-or-url-to-openapi-spec> \
     --url <backend-api-url> \
     --headless \
     --port 3030
   ```

2. **Verify server health**
   ```bash
   curl -s http://localhost:3030/health
   # Expected: 200 OK
   
   curl -s http://localhost:3030/mcp/ping
   # Expected: pong
   ```

3. **Test MCP endpoint** — The MCP transport is available at `/mcp` using Streamable HTTP:
   - `POST /mcp` — JSON-RPC messages
   - `GET /mcp` — Server info (returns 204)

### Phase 3: Deployment

Choose deployment target based on requirements:

#### Option A: Cloudflare Workers (Recommended for simplicity)

1. **Authenticate** (first time only):
   ```bash
   hapi login
   ```

2. **Deploy**:
   ```bash
   hapi deploy \
     --openapi <path-or-url-to-openapi-spec> \
     --url <backend-api-url> \
     --name <worker-name> \
     --project <project-name>
   ```

3. **Verify deployment**:
   ```bash
   curl -s https://<worker-name>.<account>.workers.dev/health
   ```

#### Option B: Docker (Self-hosted)

```bash
docker run --name hapi-<project> -d --rm \
  -p 3030:3030 \
  hapimcp/hapi-cli:latest serve <project-name> \
  --openapi <openapi-url> \
  --url <backend-api-url> \
  --port 3030 \
  --headless
```

### Phase 4: Verification Checklist

Before considering deployment complete:

- [ ] `/health` returns 200 OK
- [ ] `/mcp/ping` returns `pong`
- [ ] At least one tool call succeeds via MCP transport
- [ ] Error responses include actionable messages

## Key Concepts

### Headless Mode
Use `--headless` flag when the MCP server proxies requests to an existing backend API. Without this flag, HAPI serves the OpenAPI spec documentation UI.

### Streamable HTTP Transport
HAPI uses Streamable HTTP (not stdio). MCP clients connect via HTTP POST to `/mcp` endpoint. SSE is supported for streaming responses.

### OpenAPI Spec Sources
HAPI accepts specs from:
- Local file path: `--openapi ./specs/api.yaml`
- Remote URL: `--openapi https://api.example.com/openapi.json`
- Pre-loaded specs in `~/.hapi/specs/<project>/`

## References

For detailed documentation, consult:
- [references/hapi-cli-commands.md](references/hapi-cli-commands.md) — Complete CLI reference
- [references/deployment-patterns.md](references/deployment-patterns.md) — Docker & Cloudflare recipes
- [references/troubleshooting.md](references/troubleshooting.md) — Common issues & fixes

## Quick Examples

### Petstore API (Demo)
```bash
hapi serve petstore \
  --openapi https://petstore3.swagger.io/api/v3/openapi.json \
  --url https://petstore3.swagger.io/api/v3 \
  --headless --port 3030
```

### Custom API
```bash
hapi serve my-api \
  --openapi https://my-api.example.com/openapi.json \
  --url https://my-api.example.com \
  --headless --port 3030
```

### Deploy to Cloudflare
```bash
hapi deploy \
  --openapi https://my-api.example.com/openapi.json \
  --url https://my-api.example.com \
  --name my-api-mcp
```
