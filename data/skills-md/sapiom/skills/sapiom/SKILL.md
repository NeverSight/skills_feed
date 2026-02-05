---
name: sapiom
description: Access paid services (verification, search, AI models, images, audio, browser automation) for AI agents via Sapiom. Use when building agents that need to verify phone/email, search the web, call AI models, generate images, convert text-to-speech, or automate browsers — without setting up vendor accounts.
---

# Sapiom

Instant access to paid services with pay-per-use pricing. No vendor account setup required.

## Documentation

**Always fetch the markdown docs for endpoint details, parameters, and examples.**

| Service | Documentation |
|---------|---------------|
| Verify | https://docs.sapiom.ai/capabilities/verify.md |
| Search | https://docs.sapiom.ai/capabilities/search.md |
| AI Models | https://docs.sapiom.ai/capabilities/ai-models.md |
| Images | https://docs.sapiom.ai/capabilities/images.md |
| Audio | https://docs.sapiom.ai/capabilities/audio.md |
| Browser | https://docs.sapiom.ai/capabilities/browser.md |
| Service Proxy | https://docs.sapiom.ai/service-proxy.md |

## Two Access Patterns

Sapiom offers two ways to call services:

### 1. Direct Access (Node.js SDK)

Use the SDK to call provider gateways directly with native API formats.

**When to use:** Node.js/TypeScript projects, need full provider API features.

```typescript
import { withSapiom } from "@sapiom/axios";
import axios from "axios";

const client = withSapiom(axios.create(), {
  apiKey: process.env.SAPIOM_API_KEY,
});

// Calls go to provider gateways (e.g., prelude.services.sapiom.ai)
const { data } = await client.post(
  "https://linkup.services.sapiom.ai/v1/search",
  { query: "quantum computing", depth: "standard", outputType: "sourcedAnswer" }
);
```

**Service URLs:**
| Service | Base URL |
|---------|----------|
| Verify | `https://prelude.services.sapiom.ai` |
| Search (Linkup) | `https://linkup.services.sapiom.ai` |
| Search (You.com) | `https://you-com.services.sapiom.ai` |
| AI Models | `https://openrouter.services.sapiom.ai` |
| Images | `https://fal-ai.services.sapiom.ai` |
| Audio | `https://elevenlabs.services.sapiom.ai` |
| Browser | `https://anchor-browser.services.sapiom.ai` |

### 2. Semantic Endpoints (Python/REST)

Use simplified REST endpoints without an SDK. Currently supports Verify only.

**When to use:** Python, or any language without SDK support.

```python
import requests
import os

headers = {
    "Authorization": f"Bearer {os.environ['SAPIOM_API_KEY']}",
    "Content-Type": "application/json"
}

# Calls go to unified gateway (api.sapiom.ai) with simplified schema
resp = requests.post(
    "https://api.sapiom.ai/v1/services/verify/send",
    headers=headers,
    json={"phoneNumber": "+15551234567"}
)
```

**See:** https://docs.sapiom.ai/service-proxy.md for available semantic endpoints.

## Setup

1. Get your API key from https://app.sapiom.ai/settings
2. Set environment variable:
   ```bash
   export SAPIOM_API_KEY="your_key"
   ```

### Node.js SDK

```bash
npm install @sapiom/axios axios
# or
npm install @sapiom/fetch
```

### Python

No SDK required. Use REST with Bearer token authentication.

## Navigating Documentation

Add `.md` to any docs URL to get the markdown version:

| HTML Page | Markdown |
|-----------|----------|
| `https://docs.sapiom.ai/capabilities/search` | `https://docs.sapiom.ai/capabilities/search.md` |
| `https://docs.sapiom.ai/quick-start` | `https://docs.sapiom.ai/quick-start.md` |

**Pattern:** Add `.md` to any URL

## Need Details?

Fetch the markdown documentation:

```bash
curl https://docs.sapiom.ai/capabilities/verify.md
```
