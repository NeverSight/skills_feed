---
name: monetize-service
description: Build and deploy a paid API that other agents can pay to use via x402. Use when you or the user want to monetize an API, make money, earn money, offer a service, sell a service to other agents, charge for endpoints, create a paid endpoint, or set up a paid service. Covers "make money by offering an endpoint", "sell a service", "monetize your data", "create a paid API".
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(npx awal@latest status*)", "Bash(npx awal@latest address*)", "Bash(npx awal@latest x402 details *)", "Bash(npx awal@latest x402 pay *)", "Bash(npm *)", "Bash(node *)", "Bash(curl *)", "Bash(mkdir *)"]
---

# Build an x402 Payment Server

Create an Express server that charges USDC for API access using the x402 payment protocol. Callers pay per-request in USDC on Base — no accounts, API keys, or subscriptions needed.

## How It Works

x402 is an HTTP-native payment protocol. When a client hits a protected endpoint without paying, the server returns HTTP 402 with payment requirements. The client signs a USDC payment and retries with a payment header. The facilitator verifies and settles the payment, and the server returns the response.

## Confirm wallet is initialized and authed

```bash
npx awal@latest status
```

If the wallet is not authenticated, refer to the `authenticate-wallet` skill.

## Step 1: Get the Payment Address

Run this to get the wallet address that will receive payments:

```bash
npx awal@latest address
```

Use this address as the `payTo` value.

## Step 2: Set Up the Project

```bash
mkdir x402-server && cd x402-server
npm init -y
npm install express x402-express
```

Create `index.js`:

```js
const express = require("express");
const { paymentMiddleware } = require("x402-express");

const app = express();
app.use(express.json());

const PAY_TO = "<address from step 1>";

// x402 payment middleware — protects routes below
const payment = paymentMiddleware(PAY_TO, {
  "GET /api/example": {
    price: "$0.01",
    network: "base",
    config: {
      description: "Description of what this endpoint returns",
    },
  },
});

// Protected endpoint
app.get("/api/example", payment, (req, res) => {
  res.json({ data: "This costs $0.01 per request" });
});

app.listen(3000, () => console.log("Server running on port 3000"));
```

## Step 3: Run It

```bash
node index.js
```

Test with curl — you should get a 402 response with payment requirements:

```bash
curl -i http://localhost:3000/api/example
```

## API Reference

### paymentMiddleware(payTo, routes, facilitator?)

Creates Express middleware that enforces x402 payments.

| Parameter     | Type     | Description                                           |
| ------------- | -------- | ----------------------------------------------------- |
| `payTo`       | string   | Ethereum address (0x...) to receive USDC payments     |
| `routes`      | object   | Route config mapping route patterns to payment config |
| `facilitator` | object?  | Optional custom facilitator (defaults to x402.org)    |

### Route Config

Each key in the routes object is `"METHOD /path"`. The value is either a price string or a config object:

```js
// Simple — just a price
{ "GET /api/data": "$0.05" }

// Full config
{
  "POST /api/query": {
    price: "$0.25",
    network: "base",
    config: {
      description: "Human-readable description of the endpoint",
      inputSchema: {
        bodyType: "json",
        bodyFields: {
          query: { type: "string", description: "The query to run" },
        },
      },
      outputSchema: {
        type: "object",
        properties: {
          result: { type: "string" },
        },
      },
    },
  },
}
```

### Route Config Fields

| Field                     | Type    | Description                                        |
| ------------------------- | ------- | -------------------------------------------------- |
| `price`                   | string  | USDC price (e.g. "$0.01", "$1.00")                 |
| `network`                 | string  | Blockchain network: "base" or "base-sepolia"       |
| `config.description`      | string? | What this endpoint does (shown to clients)         |
| `config.inputSchema`      | object? | Expected request body/query schema                 |
| `config.outputSchema`     | object? | Response body schema                               |
| `config.maxTimeoutSeconds` | number? | Max time for payment settlement                   |

### Supported Networks

| Network        | Description                    |
| -------------- | ------------------------------ |
| `base`         | Base mainnet (real USDC)       |
| `base-sepolia` | Base Sepolia testnet (test USDC) |

## Patterns

### Multiple endpoints with different prices

```js
const payment = paymentMiddleware(PAY_TO, {
  "GET /api/cheap": { price: "$0.001", network: "base" },
  "GET /api/expensive": { price: "$1.00", network: "base" },
  "POST /api/query": { price: "$0.25", network: "base" },
});

app.get("/api/cheap", payment, (req, res) => { /* ... */ });
app.get("/api/expensive", payment, (req, res) => { /* ... */ });
app.post("/api/query", payment, (req, res) => { /* ... */ });
```

### Wildcard routes

```js
const payment = paymentMiddleware(PAY_TO, {
  "GET /api/*": { price: "$0.05", network: "base" },
});

app.use(payment);
app.get("/api/users", (req, res) => { /* ... */ });
app.get("/api/posts", (req, res) => { /* ... */ });
```

### Health check (no payment)

Register free endpoints before the payment middleware:

```js
app.get("/health", (req, res) => res.json({ status: "ok" }));

// Payment middleware only applies to routes registered after it
app.get("/api/data", payment, (req, res) => { /* ... */ });
```

### POST with body schema

```js
const payment = paymentMiddleware(PAY_TO, {
  "POST /api/analyze": {
    price: "$0.10",
    network: "base",
    config: {
      description: "Analyze text sentiment",
      inputSchema: {
        bodyType: "json",
        bodyFields: {
          text: { type: "string", description: "Text to analyze" },
        },
      },
      outputSchema: {
        type: "object",
        properties: {
          sentiment: { type: "string" },
          score: { type: "number" },
        },
      },
    },
  },
});

app.post("/api/analyze", payment, (req, res) => {
  const { text } = req.body;
  // ... your logic
  res.json({ sentiment: "positive", score: 0.95 });
});
```

### Using the CDP facilitator (authenticated)

For production use with the Coinbase facilitator (supports mainnet):

```bash
npm install @coinbase/x402
```

```js
const { facilitator } = require("@coinbase/x402");

const payment = paymentMiddleware(PAY_TO, routes, facilitator);
```

This requires `CDP_API_KEY_ID` and `CDP_API_KEY_SECRET` environment variables. Get these from https://portal.cdp.coinbase.com.

## Testing with the pay-for-service Skill

Once the server is running, use the `pay-for-service` skill to test payments:

```bash
# Check the endpoint's payment requirements
npx awal@latest x402 details http://localhost:3000/api/example

# Make a paid request
npx awal@latest x402 pay http://localhost:3000/api/example
```

## Pricing Guidelines

| Use Case               | Suggested Price |
| ---------------------- | --------------- |
| Simple data lookup     | $0.001 - $0.01 |
| API proxy / enrichment | $0.01 - $0.10  |
| Compute-heavy query    | $0.10 - $0.50  |
| AI inference           | $0.05 - $1.00  |

## Checklist

- [ ] Get wallet address with `npx awal@latest address`
- [ ] Install `express` and `x402-express`
- [ ] Define routes with prices and descriptions
- [ ] Register payment middleware before protected routes
- [ ] Keep health/status endpoints before payment middleware
- [ ] Test with `curl` (should get 402) and `npx awal@latest x402 pay` (should get 200)
- [ ] Announce your service so other agents can find and use it