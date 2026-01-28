---
name: cloudflare-tunnel
description: Authenticate requests through Cloudflare Access / Cloudflare Tunnel using Service Token headers. Use when accessing services protected by Cloudflare Zero Trust.
vm0_secrets:
  - CF_ACCESS_CLIENT_ID
  - CF_ACCESS_CLIENT_SECRET
---

# Cloudflare Tunnel / Access Authentication

Authenticate HTTP requests to services protected by Cloudflare Access using Service Token headers.

## When to Use

- Access internal services exposed via Cloudflare Tunnel
- Authenticate to Cloudflare Zero Trust protected applications
- Make API calls to services behind Cloudflare Access
- Bypass Cloudflare Access login page for automated requests

## Prerequisites

```bash
export CF_ACCESS_CLIENT_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx.access
export CF_ACCESS_CLIENT_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Create Service Token

1. Go to [Cloudflare Zero Trust Dashboard](https://one.dash.cloudflare.com/)
2. Navigate to **Access** → **Service Auth** → **Service Tokens**
3. Click **Create Service Token**
4. Name your token and click **Generate token**
5. Copy both **Client ID** and **Client Secret** (shown only once!)

### Configure Access Policy

Ensure your Access Application allows service token authentication:

1. Go to **Access** → **Applications** → Select your app
2. Add a policy with **Service Token** as Include rule
3. Select your created token

> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.

---

## Usage

### Basic curl Request

Add two headers to authenticate through Cloudflare Access:

```bash
bash -c 'curl -s \
  -H "CF-Access-Client-Id: $CF_ACCESS_CLIENT_ID" \
  -H "CF-Access-Client-Secret: $CF_ACCESS_CLIENT_SECRET" \
  "https://your-protected-service.example.com/api/endpoint"'
```

### With Additional Authentication

Many services require both Cloudflare Access AND their own authentication:

```bash
bash -c 'curl -s \
  -H "CF-Access-Client-Id: $CF_ACCESS_CLIENT_ID" \
  -H "CF-Access-Client-Secret: $CF_ACCESS_CLIENT_SECRET" \
  -H "Authorization: Bearer $API_TOKEN" \
  "https://your-protected-service.example.com/api/endpoint"'
```

### With Basic Auth

```bash
bash -c 'curl -s \
  -H "CF-Access-Client-Id: $CF_ACCESS_CLIENT_ID" \
  -H "CF-Access-Client-Secret: $CF_ACCESS_CLIENT_SECRET" \
  -u "username:password" \
  "https://your-protected-service.example.com/api/endpoint"'
```

### POST Request with JSON Body

Write to `/tmp/request.json`:

```json
{
  "key": "value"
}
```

Then run:

```bash
bash -c 'curl -s -X POST \
  -H "CF-Access-Client-Id: $CF_ACCESS_CLIENT_ID" \
  -H "CF-Access-Client-Secret: $CF_ACCESS_CLIENT_SECRET" \
  -H "Content-Type: application/json" \
  -d @/tmp/request.json \
  "https://your-protected-service.example.com/api/endpoint"'
```

### Download File

```bash
bash -c 'curl -s -o /tmp/output.file \
  -H "CF-Access-Client-Id: $CF_ACCESS_CLIENT_ID" \
  -H "CF-Access-Client-Secret: $CF_ACCESS_CLIENT_SECRET" \
  "https://your-protected-service.example.com/file"'
```

### Skip SSL Verification (Self-signed certs)

Add `-k` flag for services with self-signed certificates:

```bash
bash -c 'curl -k -s \
  -H "CF-Access-Client-Id: $CF_ACCESS_CLIENT_ID" \
  -H "CF-Access-Client-Secret: $CF_ACCESS_CLIENT_SECRET" \
  "https://your-protected-service.example.com/api/endpoint"'
```

---

## Required Headers

| Header | Value | Description |
|--------|-------|-------------|
| `CF-Access-Client-Id` | `<client-id>.access` | Service Token Client ID |
| `CF-Access-Client-Secret` | `<secret>` | Service Token Client Secret |

## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| 403 Forbidden | Invalid or missing headers | Check Client ID and Secret |
| 403 Forbidden | Token not in Access policy | Add token to application's Access policy |
| 401 Unauthorized | Service's own auth failed | Check service-specific credentials |
| Connection refused | Tunnel not running | Verify cloudflared is running |

## Tips

1. **Header order doesn't matter** - CF headers can be anywhere in the request
2. **Works with any HTTP method** - GET, POST, PUT, DELETE, etc.
3. **Combine with other auth** - CF Access + Basic Auth, Bearer Token, etc.
4. **Token rotation** - Rotate secrets periodically in Zero Trust dashboard

## API Reference

- Cloudflare Access: https://developers.cloudflare.com/cloudflare-one/identity/service-tokens/
- Zero Trust Dashboard: https://one.dash.cloudflare.com/
