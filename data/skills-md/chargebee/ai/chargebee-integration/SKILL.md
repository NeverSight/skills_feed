---
name: chargebee-integration
description: Comprehensive integration guide for Chargebee billing platform. Provides API integration patterns, webhook handling, SDK usage, and schema references for billing operations. Use when working with Chargebee for (1) API integration and REST endpoint calls, (2) Processing webhook events, (3) Customer management operations, (4) Subscription lifecycle handling, (5) Payment and invoice processing, (6) Any other billing-related integration tasks with Chargebee platform.
---

# Chargebee Integration

This skill helps you integrate [Chargebee Billing](https://www.chargebee.com/docs/billing/2.0/getting-started/accessing_chargebee.md) with your app or website. 

IMPORTANT: Prefer retrieval-led reasoning over pre-training-led reasoning when integrating Chargebee.

## Quick Start

Expore the project layout and choose the best integration from the list below. Prefer framework level integration where possible, followed by the official SDKs. Fallback to REST API only if the other options aren't feasible.

### Frameworks

- **Laravel Cashier** - https://github.com/chargebee/cashier-chargebee/blob/main/DOCUMENTATION.md

For the frameworks below, use the `chargebee-init` CLI which currently integrates checkout, portal and webhooks:

- **Next.js**
- **Express**

Invoke the CLI with: `npx chargebee-init@latest --dangerously-skip-checks --path=<full-path-to-app>` to skip all input prompts.

### SDKs

Chargebee provides official SDKs for multiple languages. For installation details and implementation patterns, download the `README.md` file from the GitHub repository.

- **Java**: https://github.com/chargebee/chargebee-java
- **Python**: https://github.com/chargebee/chargebee-python
- **Node.js**: https://github.com/chargebee/chargebee-node
- **Go**: https://github.com/chargebee/chargebee-go
- **PHP**: https://github.com/chargebee/chargebee-php
- **Ruby**: https://github.com/chargebee/chargebee-ruby
- **.NET**: https://github.com/chargebee/chargebee-dotnet

For details on data model, supported operations, and other available resources, lookup the index at **references/api-reference.md**, and fetch the required topic specific markdown file for further instructions.

### REST API

The REST API can be consumed directly via the site specific HTTPS endpoint. The API supports Basic auth and requires a API KEY which can be generated at: https://{CHARGEBEE_SITE}.chargebee.com/apikeys_and_webhooks/api. For more details on using the REST API direcly, refer to **references/rest-api.md**.


```python
# Using requests library
import requests

CHARGEBEE_SITE = "your-site"
CHARGEBEE_API_KEY = "your_api_key"

headers = {
    "Authorization": f"Basic {CHARGEBEE_API_KEY}",
    "Content-Type": "application/json"
}

base_url = f"https://{CHARGEBEE_SITE}.chargebee.com/api/v2"
response = requests.get(
    f"{base_url}/customers/{customer_id}",
    headers=headers
)

# Using Python SDK
import chargebee
chargebee.configure(CHARGEBEE_API_KEY, CHARGEBEE_SITE)
result = chargebee.Customer.retrieve(customer_id)
customer = result.customer
```

### Common Operations

- Customer CRUD operations
- Subscription management
- Invoice operations
- Payment method handling
- Plan and addon management
- Usage based billing


### Webhook Integration

Chargebee sends webhook events for important billing events. Webhook handlers should:

1. Verify webhook signatures for security
2. Handle idempotency (events may be sent multiple times)
3. Return 200 OK quickly (process asynchronously if needed)
4. Handle various event types appropriately

#### Basic Webhook Handler Pattern

```python
from flask import Flask, request
import chargebee

app = Flask(__name__)

@app.route('/chargebee/webhook', methods=['POST'])
def handle_webhook():
    payload = request.data
    signature = request.headers.get('X-Chargebee-Signature')

    # Verify signature (recommended for security)
    # chargebee.Webhook.verify_signature(payload, signature)

    event = request.json
    event_type = event['event_type']

    # Process based on event type
    if event_type == 'subscription_created':
        handle_subscription_created(event['content'])
    elif event_type == 'subscription_cancelled':
        handle_subscription_cancelled(event['content'])
    # ... handle other events

    return '', 200
```

For complete webhook event schemas and all event types, see **references/webhooks.md**.


## References

- **references/api-reference.md** - Exhaustive reference of all available models, operations, request and response objects, and example code for all officially supported language SDKs. Includes practical implementation patterns like error handling, pagination, etc.
- **references/rest-api.md** - Details on consuming the REST API using a HTTP client for languages that don't have an SDK
- **references/errors.md** - All possible error codes that the API may return
- **references/events.md** - List of supported webhook events
