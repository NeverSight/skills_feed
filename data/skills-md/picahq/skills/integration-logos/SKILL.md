---
name: integration-logos
description: Get logos and icons for Gmail, Slack, HubSpot, and 200+ other integrations
---

# Integration Logos

Get logos and icons for all Pica-supported integrations.

## Overview

Pica provides logos and images for all 200+ supported integrations. Use this skill to display integration icons in your UI, documentation, or marketing materials.

## Prerequisites

- Pica API key from https://app.picaos.com/settings/api-keys

---

## Quick Reference

### Asset URL Pattern

All integration assets follow this pattern:

```
https://assets.picaos.com/logos/{platform}.svg
```

**Examples:**
- Gmail: `https://assets.picaos.com/logos/gmail.svg`
- Slack: `https://assets.picaos.com/logos/slack.svg`
- HubSpot: `https://assets.picaos.com/logos/hubspot.svg`

### Common Platform IDs

| Integration | Platform ID | Asset URL |
|-------------|-------------|-----------|
| Gmail | `gmail` | `https://assets.picaos.com/logos/gmail.svg` |
| Google Calendar | `google-calendar` | `https://assets.picaos.com/logos/google-calendar.svg` |
| Slack | `slack` | `https://assets.picaos.com/logos/slack.svg` |
| HubSpot | `hubspot` | `https://assets.picaos.com/logos/hubspot.svg` |
| Salesforce | `salesforce` | `https://assets.picaos.com/logos/salesforce.svg` |
| Notion | `notion` | `https://assets.picaos.com/logos/notion.svg` |
| Linear | `linear` | `https://assets.picaos.com/logos/linear.svg` |
| GitHub | `github` | `https://assets.picaos.com/logos/github.svg` |
| Jira | `jira` | `https://assets.picaos.com/logos/jira.svg` |
| Asana | `asana` | `https://assets.picaos.com/logos/asana.svg` |
| Stripe | `stripe` | `https://assets.picaos.com/logos/stripe.svg` |
| Shopify | `shopify` | `https://assets.picaos.com/logos/shopify.svg` |
| Zendesk | `zendesk` | `https://assets.picaos.com/logos/zendesk.svg` |
| Intercom | `intercom` | `https://assets.picaos.com/logos/intercom.svg` |
| Airtable | `airtable` | `https://assets.picaos.com/logos/airtable.svg` |

---

## Fetching Assets from API

The recommended way to get integration assets is via the Available Connectors API, which returns the official image URL for each integration.

### API Request

```
GET https://api.picaos.com/v1/available-connectors?limit=300
Headers:
  x-pica-secret: YOUR_PICA_SECRET_KEY
```

### Response Structure

```json
{
  "rows": [
    {
      "platform": "gmail",
      "name": "Gmail",
      "category": "Communication",
      "image": "https://assets.picaos.com/logos/gmail.svg",
      "description": "..."
    },
    {
      "platform": "slack",
      "name": "Slack",
      "category": "Communication",
      "image": "https://assets.picaos.com/logos/slack.svg",
      "description": "..."
    }
  ],
  "total": 200,
  "pages": 1,
  "page": 1
}
```

### Key Fields

| Field | Description |
|-------|-------------|
| `platform` | Platform identifier (use for constructing URLs) |
| `name` | Display name |
| `image` | Official logo URL |
| `category` | Integration category |

---

## Implementation

### Fetch All Integration Assets

```typescript
interface Integration {
  platform: string;
  name: string;
  image: string;
  category: string;
}

async function getIntegrations(): Promise<Integration[]> {
  const response = await fetch(
    "https://api.picaos.com/v1/available-connectors?limit=300",
    {
      headers: {
        "x-pica-secret": process.env.PICA_SECRET_KEY,
      },
    }
  );

  if (!response.ok) {
    throw new Error(`Failed to fetch integrations: ${response.status}`);
  }

  const data = await response.json();
  return data.rows;
}
```

### Build Asset URL from Platform ID

```typescript
function getIntegrationLogo(platform: string): string {
  return `https://assets.picaos.com/logos/${platform}.svg`;
}

// Usage
const gmailLogo = getIntegrationLogo("gmail");
// => "https://assets.picaos.com/logos/gmail.svg"
```

### Display Integration with Logo

```typescript
function IntegrationCard({ integration }) {
  const [imgError, setImgError] = useState(false);

  return (
    <div className="integration-card">
      {!imgError ? (
        <img
          src={integration.image}
          alt={integration.name}
          onError={() => setImgError(true)}
        />
      ) : (
        <div className="fallback-icon">
          {integration.name.charAt(0).toUpperCase()}
        </div>
      )}
      <span>{integration.name}</span>
    </div>
  );
}
```

### With Fallback URLs

If the primary asset URL fails, fall back to a generic icon service:

```typescript
function getIntegrationLogo(platform: string, primaryUrl?: string): string {
  // Use API-provided URL if available
  if (primaryUrl) {
    return primaryUrl;
  }

  // Construct from pattern
  return `https://assets.picaos.com/logos/${platform}.svg`;
}

function getFallbackLogo(platform: string): string {
  // SimpleIcons as fallback
  return `https://cdn.simpleicons.org/${platform}`;
}
```

---

## Caching Assets

For production applications, cache the integration list to reduce API calls:

```typescript
let cachedIntegrations: Integration[] | null = null;
let cacheTime: number = 0;
const CACHE_DURATION = 60 * 60 * 1000; // 1 hour

async function getIntegrationsCached(): Promise<Integration[]> {
  const now = Date.now();

  if (cachedIntegrations && now - cacheTime < CACHE_DURATION) {
    return cachedIntegrations;
  }

  cachedIntegrations = await getIntegrations();
  cacheTime = now;

  return cachedIntegrations;
}
```

---

## Filtering by AuthKit Support

To get only integrations that support OAuth via AuthKit:

```
GET https://api.picaos.com/v1/available-connectors?authkit=true&limit=300
```

This filters to integrations that can be connected via the AuthKit widget.

---

## Asset Specifications

| Property | Value |
|----------|-------|
| Format | SVG (scalable) |
| Background | Transparent |
| Recommended display size | 24x24 to 64x64 px |
| Color | Original brand colors |

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| 404 on asset URL | Invalid platform ID | Verify platform ID from API response |
| Image not loading | CORS or network issue | Use `img` tag or proxy through your server |
| Wrong logo displayed | Platform ID mismatch | Use exact `platform` value from API, not display name |
| Blurry logo | Scaling PNG | Assets are SVG, ensure proper rendering |

---

## API Reference

### Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /v1/available-connectors` | List all integrations with assets |
| `GET /v1/available-connectors?authkit=true` | List OAuth-enabled integrations |

### Asset URL

```
https://assets.picaos.com/logos/{platform}.svg
```

Replace `{platform}` with the platform identifier from the API response.

### Documentation

- Pica Docs: https://docs.picaos.com
- Available Connectors: https://docs.picaos.com/available-connectors
