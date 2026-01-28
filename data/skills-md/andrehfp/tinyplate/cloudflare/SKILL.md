---
name: cloudflare
description: "Setup domains in Cloudflare with DNS for Clerk, Vercel, and email routing. Use when adding new domains, configuring DNS records, or setting up email redirects."
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, WebSearch
---

# Cloudflare Setup

Automate Cloudflare workflows: DNS setup, Clerk integration, Vercel deployment, email routing, and R2 storage.

## Prerequisites

### Authentication (Choose One)

**Option 1: API Token (Recommended)**
```bash
# Add to .env.local
CLOUDFLARE_API_TOKEN="your-api-token"
CLOUDFLARE_ACCOUNT_ID="your-account-id"
```

Create token at: https://dash.cloudflare.com/profile/api-tokens
Required permissions:
- Zone:DNS:Edit
- Zone:Zone:Read
- Email Routing Addresses:Edit
- Email Routing Rules:Edit
- Account:R2:Edit (for R2 storage)

**Option 2: Wrangler CLI**
```bash
# Install wrangler
bun add -g wrangler

# Login (opens browser)
wrangler login

# Verify
wrangler whoami
```

### Other Tools
```bash
# Vercel CLI (required)
bun add -g vercel
vercel login
```

## Workflow

When setting up a new domain, follow these steps:

### Step 1: Gather Information

Ask the user for:
1. **Domain name** (e.g., `example.com`)
2. **Clerk DNS records** (paste from Clerk dashboard)
3. **Vercel project name** (e.g., `my-app`)
4. **Email addresses** to create (e.g., `contact`, `support`)
5. **Redirect target email** (e.g., `me@gmail.com`)

### Step 2: Get Zone ID

```bash
# If using API token
curl -X GET "https://api.cloudflare.com/client/v4/zones?name=DOMAIN" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" | jq '.result[0].id'

# If using wrangler
wrangler pages project list  # Shows associated zones
```

### Step 3: Create DNS Records for Clerk

Clerk provides specific DNS records for each project. Common patterns:

```bash
# Example: CNAME record
curl -X POST "https://api.cloudflare.com/client/v4/zones/ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "CNAME",
    "name": "clerk",
    "content": "frontend-api.clerk.dev",
    "ttl": 1,
    "proxied": false
  }'

# Example: TXT record for verification
curl -X POST "https://api.cloudflare.com/client/v4/zones/ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "TXT",
    "name": "@",
    "content": "clerk-verification=xxxxx",
    "ttl": 1
  }'
```

### Step 4: Add Domain to Vercel

```bash
# Add domain to Vercel project
vercel domains add DOMAIN --scope=TEAM_SLUG

# Or link to specific project
vercel domains add DOMAIN PROJECT_NAME
```

Then create Vercel DNS records:

```bash
# A record for root domain
curl -X POST "https://api.cloudflare.com/client/v4/zones/ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "A",
    "name": "@",
    "content": "76.76.21.21",
    "ttl": 1,
    "proxied": false
  }'

# CNAME for www subdomain
curl -X POST "https://api.cloudflare.com/client/v4/zones/ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "CNAME",
    "name": "www",
    "content": "cname.vercel-dns.com",
    "ttl": 1,
    "proxied": false
  }'
```

### Step 5: Setup Email Routing

First, enable email routing for the zone (do this in Cloudflare dashboard first time).

Then create routing rules:

```bash
# Create destination address (must be verified first)
curl -X POST "https://api.cloudflare.com/client/v4/accounts/ACCOUNT_ID/email/routing/addresses" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "email": "your-main-email@gmail.com"
  }'

# Create routing rule for contact@domain.com
curl -X POST "https://api.cloudflare.com/client/v4/zones/ZONE_ID/email/routing/rules" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "name": "Forward contact",
    "enabled": true,
    "matchers": [{"type": "literal", "field": "to", "value": "contact@DOMAIN"}],
    "actions": [{"type": "forward", "value": ["your-main-email@gmail.com"]}]
  }'
```

Required MX records for email routing:
```bash
# MX records for Cloudflare Email Routing
curl -X POST "https://api.cloudflare.com/client/v4/zones/ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "MX",
    "name": "@",
    "content": "route1.mx.cloudflare.net",
    "priority": 69,
    "ttl": 1
  }'

curl -X POST "https://api.cloudflare.com/client/v4/zones/ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "MX",
    "name": "@",
    "content": "route2.mx.cloudflare.net",
    "priority": 46,
    "ttl": 1
  }'

curl -X POST "https://api.cloudflare.com/client/v4/zones/ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "MX",
    "name": "@",
    "content": "route3.mx.cloudflare.net",
    "priority": 89,
    "ttl": 1
  }'

# TXT record for SPF
curl -X POST "https://api.cloudflare.com/client/v4/zones/ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "TXT",
    "name": "@",
    "content": "v=spf1 include:_spf.mx.cloudflare.net ~all",
    "ttl": 1
  }'
```

### Step 6: Verification Checklist

After setup, verify:

```bash
# List all DNS records
curl -X GET "https://api.cloudflare.com/client/v4/zones/ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" | jq '.result[] | {type, name, content}'

# Check Vercel domain status
vercel domains inspect DOMAIN

# Test email routing (send test email to contact@DOMAIN)
```

## Interactive Prompts Template

When running `/cloudflare`, ask:

```
What domain are you setting up?
> example.com

Paste the Clerk DNS records from your Clerk dashboard:
> [user pastes records]

What's the Vercel project name?
> my-saas-app

What email addresses should I create? (comma-separated)
> contact, support, hello

What email should these redirect to?
> myemail@gmail.com
```

## Common DNS Record Types

| Type | Use Case | Proxied |
|------|----------|---------|
| A | Root domain to IP | No (for Vercel) |
| CNAME | Subdomain to hostname | No (for Clerk/Vercel) |
| TXT | Verification, SPF | N/A |
| MX | Email routing | N/A |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Zone not found | Domain must be added to Cloudflare first |
| DNS propagation slow | Wait 5-10 minutes, check with `dig` |
| Email not forwarding | Verify destination email first |
| Vercel 404 | Check DNS proxied=false for Vercel records |
| Clerk verification failed | Ensure TXT record is on root (@) |

## Useful Commands

```bash
# Check DNS propagation
dig DOMAIN +short
dig DOMAIN MX +short
dig DOMAIN TXT +short

# List zones in account
curl -X GET "https://api.cloudflare.com/client/v4/zones" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" | jq '.result[] | {name, id}'

# Delete a DNS record
curl -X DELETE "https://api.cloudflare.com/client/v4/zones/ZONE_ID/dns_records/RECORD_ID" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN"
```

---

# R2 Storage Setup

Setup R2 buckets for file storage: user uploads, static assets, backups.

## R2 Workflow

### Step 1: Determine Use Case

Ask the user:
```
What do you want to do with R2?
1. Create new bucket (full setup)
2. Configure existing bucket (CORS, public access)
3. Setup custom domain for bucket
```

### Step 2: Gather Bucket Info

```
Bucket name?
> my-app-uploads

What will this bucket store?
1. User uploads (images, files) - needs CORS + presigned URLs
2. Static assets (public CDN) - needs public access
3. Backups (private) - no public access
> 1

Custom domain? (optional, press enter to skip)
> uploads.myapp.com
```

### Step 3: Create Bucket

```bash
# Create bucket via wrangler
wrangler r2 bucket create my-app-uploads

# Or via API
curl -X PUT "https://api.cloudflare.com/client/v4/accounts/{account_id}/r2/buckets" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"name": "my-app-uploads", "locationHint": "wnam"}'
```

### Step 4: Configure CORS (for user uploads)

Create `cors.json`:
```json
{
  "corsRules": [
    {
      "allowedOrigins": ["https://myapp.com", "http://localhost:3000"],
      "allowedMethods": ["GET", "PUT", "POST", "DELETE", "HEAD"],
      "allowedHeaders": ["*"],
      "exposeHeaders": ["ETag", "Content-Length"],
      "maxAgeSeconds": 3600
    }
  ]
}
```

Apply CORS:
```bash
wrangler r2 bucket cors put my-app-uploads --file=cors.json
```

### Step 5: Setup Public Access (for static assets)

Option A: Enable R2.dev subdomain (via dashboard)
- Go to R2 > Bucket > Settings > Public access

Option B: Custom domain:
```bash
# Add CNAME record
curl -X POST "https://api.cloudflare.com/client/v4/zones/ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "CNAME",
    "name": "uploads",
    "content": "{account_id}.r2.cloudflarestorage.com",
    "ttl": 1,
    "proxied": true
  }'
```

Then enable custom domain in R2 bucket settings.

### Step 6: Generate S3 API Credentials (for SDK access)

1. Go to R2 > Manage R2 API Tokens
2. Create token with Object Read & Write
3. Add to `.env.local`:

```bash
R2_ACCESS_KEY_ID="your-access-key"
R2_SECRET_ACCESS_KEY="your-secret-key"
R2_ENDPOINT="https://{account_id}.r2.cloudflarestorage.com"
R2_BUCKET_NAME="my-app-uploads"
```

## R2 Quick Commands

```bash
# List buckets
wrangler r2 bucket list

# Create bucket
wrangler r2 bucket create BUCKET_NAME

# Delete bucket
wrangler r2 bucket delete BUCKET_NAME

# List objects
wrangler r2 object list BUCKET_NAME

# Upload file
wrangler r2 object put BUCKET_NAME/path/file.png --file=./local.png

# View CORS config
wrangler r2 bucket cors get BUCKET_NAME
```

## R2 Use Case Presets

| Use Case | CORS | Public | Custom Domain |
|----------|------|--------|---------------|
| User uploads | Yes | No | Optional |
| Static assets/CDN | No | Yes | Recommended |
| Backups | No | No | No |
| Public downloads | No | Yes | Optional |

## R2 Troubleshooting

| Issue | Solution |
|-------|----------|
| CORS error in browser | Add domain to allowedOrigins |
| 403 Forbidden | Check API token has R2:Edit permission |
| Custom domain not working | Ensure CNAME is proxied (orange cloud) |
| Upload fails | Verify Content-Type header matches file |
