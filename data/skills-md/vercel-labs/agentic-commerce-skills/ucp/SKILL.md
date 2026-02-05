---
name: ucp
description: >-
  Expert-level implementation assistant for the Universal Commerce Protocol
  (UCP). Provides comprehensive tooling for adding UCP support to Next.js
  ecommerce codebases — from initial consultation through full implementation,
  testing, and validation.
arguments:
  Optional sub-command: init | consult | plan | gaps | scaffold | validate | profile | test | docs
user_invocable: true
---

# UCP Skill — Universal Commerce Protocol Implementation

## Core Principles

1. **Edge runtime is NOT USED** — Only Node.js (default) or Bun (opt-in) runtimes
2. **Interactive error handling** — When ambiguous, ask the user how to proceed
3. **Config-driven** — All decisions persist in `ucp.config.json`
4. **Spec-grounded** — All implementations reference the canonical UCP specification
5. **Next.js conventions** — Follow App Router patterns for code organization
6. **Deep analysis** — Use AST parsing and data flow tracing for gap detection

---

## Spec Repository Handling

### Location Priority
Check in this order:
1. `./ucp/` — User's local copy (use as-is)
2. `./.ucp-spec/` — Previously cloned spec (update it)
3. Neither exists — Clone fresh

### Clone Procedure
When cloning is needed:
```bash
git clone --depth 1 https://github.com/Universal-Commerce-Protocol/ucp.git .ucp-spec
```

If HTTPS fails, try SSH:
```bash
git clone --depth 1 git@github.com:Universal-Commerce-Protocol/ucp.git .ucp-spec
```

### Update Procedure
When `./.ucp-spec/` exists:
```bash
cd .ucp-spec && git pull && cd ..
```

### Gitignore Management
After cloning, ensure `.ucp-spec/` is in `.gitignore`:
- Read `.gitignore` if it exists
- Check if `.ucp-spec/` or `.ucp-spec` is already listed
- If not, append `.ucp-spec/` on a new line

### Spec File Locations (read on demand)
```
docs/specification/overview.md
docs/specification/checkout.md
docs/specification/checkout-rest.md
docs/specification/checkout-mcp.md
docs/specification/checkout-a2a.md
docs/specification/embedded-checkout.md
docs/specification/order.md
docs/specification/fulfillment.md
docs/specification/discount.md
docs/specification/buyer-consent.md
docs/specification/identity-linking.md
docs/specification/ap2-mandates.md
docs/specification/payment-handler-guide.md
docs/specification/tokenization-guide.md
spec/services/shopping/rest.openapi.json
spec/services/shopping/mcp.openrpc.json
spec/services/shopping/embedded.openrpc.json
spec/handlers/tokenization/openapi.json
spec/schemas/shopping/*
spec/discovery/profile_schema.json
```

---

## Configuration File

### Location
`./ucp.config.json` at project root

### Schema
```json
{
  "$schema": "./ucp.config.schema.json",
  "ucp_version": "2026-01-11",
  "roles": ["business"],
  "runtime": "nodejs",
  "capabilities": {
    "core": ["dev.ucp.shopping.checkout"],
    "extensions": []
  },
  "transports": ["rest"],
  "transport_priority": ["rest", "mcp", "a2a", "embedded"],
  "payment_handlers": [],
  "features": {
    "ap2_mandates": false,
    "identity_linking": false,
    "multi_destination_fulfillment": false
  },
  "domain": "",
  "existing_apis": {},
  "policy_urls": {
    "privacy": "",
    "terms": "",
    "refunds": "",
    "shipping": ""
  },
  "scaffold_depth": "full",
  "generated_files": [],
  "answers": {},
  "deployment": {
    "platform": "vercel",
    "region": "iad1",
    "mcp": {
      "enabled": false,
      "max_duration": 60
    }
  }
}
```

### Field Descriptions
| Field | Type | Description |
|-------|------|-------------|
| `ucp_version` | string | UCP spec version (date-based) |
| `roles` | string[] | One or more of: `business`, `platform`, `payment_provider`, `host_embedded` |
| `runtime` | string | `nodejs` (default) or `bun` |
| `capabilities.core` | string[] | Required capabilities to implement |
| `capabilities.extensions` | string[] | Optional extensions to implement |
| `transports` | string[] | Enabled transports: `rest`, `mcp`, `a2a`, `embedded` |
| `transport_priority` | string[] | Order to implement transports |
| `payment_handlers` | string[] | Payment handler IDs to support |
| `features.ap2_mandates` | boolean | Enable AP2 mandate signing |
| `features.identity_linking` | boolean | Enable OAuth identity linking |
| `features.multi_destination_fulfillment` | boolean | Enable multi-destination shipping |
| `domain` | string | Business domain for `/.well-known/ucp` |
| `existing_apis` | object | Map of existing API endpoints to analyze |
| `policy_urls` | object | URLs for privacy, terms, refunds, shipping policies |
| `scaffold_depth` | string | `types` \| `scaffolding` \| `full` |
| `generated_files` | string[] | Files created by scaffold (for tracking) |
| `answers` | object | Raw answers to qualifying questions |

---

## Sub-command: (no argument)

### Trigger
User runs `/ucp` with no sub-command

### Behavior
Display help listing all available sub-commands:

```
UCP Skill — Universal Commerce Protocol Implementation

Available commands:
  /ucp init      — Initialize UCP in this project (clone spec, create config)
  /ucp consult   — Full consultation: answer qualifying questions, build roadmap
  /ucp plan      — Generate detailed implementation plan
  /ucp gaps      — Analyze existing code against UCP requirements
  /ucp scaffold  — Generate full working UCP implementation
  /ucp validate  — Validate implementation against UCP schemas
  /ucp profile   — Generate /.well-known/ucp discovery profile
  /ucp test      — Generate unit tests for UCP handlers
  /ucp docs      — Generate internal documentation

Typical workflow:
  /ucp init → /ucp consult → /ucp plan → /ucp scaffold → /ucp profile → /ucp test → /ucp validate

Configuration: ./ucp.config.json
Spec location: ./ucp/ or ./.ucp-spec/
```

---

## Sub-command: init

### Trigger
User runs `/ucp init`

### Purpose
Bootstrap UCP in a project: clone spec, create config, ask essential questions.

### Procedure

#### Step 1: Check/Clone Spec Repository
1. Check if `./ucp/` exists
   - If yes: "Found local UCP spec at ./ucp/"
2. If not, check if `./.ucp-spec/` exists
   - If yes: Run `git pull` to update
   - If no: Clone the repo (see Spec Repository Handling)
3. After cloning, add `.ucp-spec/` to `.gitignore`

#### Step 2: Check for Existing Config
1. Check if `./ucp.config.json` exists
2. If yes, ask: "Config file exists. Overwrite, merge, or abort?"
   - Overwrite: Delete and create fresh
   - Merge: Keep existing values as defaults
   - Abort: Stop init

#### Step 3: Ask Essential Questions (4 questions)

**Q1: What role(s) are you implementing?**
- Business (merchant of record)
- Platform (consumer app or agent)
- Payment credential provider
- Host embedding checkout
- Multiple (specify)

If user selects multiple roles, WARN:
> "Implementing multiple roles is unusual. This is typically for marketplace/aggregator scenarios. Are you sure?"

**Q2: What runtime will you use?**
- Node.js (recommended, stable)
- Bun (opt-in, experimental)

NOTE: If user mentions Edge, respond:
> "Edge runtime is not supported for UCP implementations. Please choose Node.js or Bun."

**Q3: What is your business domain?**
- The domain that will host `/.well-known/ucp`
- Example: `shop.example.com`

**Q4: Which transports do you need at launch?**
- REST (recommended baseline)
- MCP (Model Context Protocol)
- A2A (Agent-to-Agent)
- Embedded (iframe checkout)

#### Step 4: Create Config File
Create `./ucp.config.json` with:
- Answers from essential questions
- Sensible defaults for other fields
- `ucp_version` set to latest from spec

#### Step 5: Output Ready Message
```
UCP initialized successfully!

Config: ./ucp.config.json
Spec:   ./.ucp-spec/ (or ./ucp/)
Role:   {role}
Domain: {domain}

Next steps:
  /ucp consult  — Complete full consultation (recommended)
  /ucp plan     — Skip to implementation planning
  /ucp gaps     — Analyze existing code first
```

---

## Sub-command: consult

### Trigger
User runs `/ucp consult`

### Purpose
Walk through all 12 qualifying questions, update config, produce implementation roadmap.

### Prerequisites
- Config file must exist (run `/ucp init` first)
- Spec must be available

### Procedure

#### Step 1: Load Existing Config
Read `./ucp.config.json` and use existing answers as defaults.

#### Step 2: Walk Through 12 Qualifying Questions

Ask each question. If already answered in config, show current value and ask to confirm or change.

**Q1: Are we implementing the business side, the platform side, or both?**
- Map to `roles` in config
- If both/multiple, warn about unusual scenario

**Q2: Which UCP version and which capabilities/extensions are in scope?**
- Read available versions from spec
- Present capability options:
  - Core: `dev.ucp.shopping.checkout` (required)
  - Extensions:
    - `dev.ucp.shopping.fulfillment`
    - `dev.ucp.shopping.discount`
    - `dev.ucp.shopping.buyer_consent`
    - `dev.ucp.shopping.ap2_mandate`
    - `dev.ucp.shopping.order`
    - `dev.ucp.common.identity_linking`

**Q3: Which payment handlers do we need?**
- Wallets (Apple Pay, Google Pay)
- PSP tokenization (Stripe, Adyen, etc.)
- Custom handler
- None yet (decide later)

**Q4: Do we need AP2 mandates and signing key infrastructure?**
- Yes → set `features.ap2_mandates: true`
- No → set `features.ap2_mandates: false`
- If yes, explain: "You'll need to provide JWS signing keys (ES256 recommended)"

**Q5: Do we need fulfillment options and multi-group/multi-destination support?**
- No fulfillment needed
- Single destination only
- Multi-destination support → set `features.multi_destination_fulfillment: true`

**Q6: Do we need discounts, buyer consent capture, or identity linking?**
- Discounts → add `dev.ucp.shopping.discount` to extensions
- Buyer consent → add `dev.ucp.shopping.buyer_consent` to extensions
- Identity linking → add `dev.ucp.common.identity_linking`, set `features.identity_linking: true`

**Q7: What are the existing checkout and order APIs we should map to UCP?**
- Ask for existing endpoint paths
- Store in `existing_apis` object
- Examples: `/api/checkout`, `/api/cart`, `/api/orders`

**Q8: What are the required policy URLs?**
- Privacy policy URL
- Terms of service URL
- Refund policy URL
- Shipping policy URL
- Store in `policy_urls` object

**Q9: What authentication model is required for checkout endpoints?**
- None (anonymous checkout)
- API key
- OAuth 2.0
- Session-based
- Store in `answers.authentication_model`

**Q10: Who will receive order webhooks and what event cadence is required?**
- Webhook URL for order events
- Event types needed: `order.created`, `order.updated`, `order.fulfilled`, `order.canceled`
- Store in `answers.webhook_config`

**Q11: Do we need to support MCP, A2A, or embedded checkout at launch?**
- Confirm/update `transports` array
- Set `transport_priority` order

**Q12: What is the business domain that will host /.well-known/ucp?**
- Confirm/update `domain` field

#### Step 3: Update Config
Write all answers to `./ucp.config.json`

#### Step 4: Generate Implementation Roadmap
Based on answers, produce a roadmap:

```
UCP Implementation Roadmap
==========================

Role: Business (merchant)
Version: 2026-01-11
Domain: shop.example.com

Capabilities to implement:
  ✓ dev.ucp.shopping.checkout (core)
  ✓ dev.ucp.shopping.fulfillment
  ✓ dev.ucp.shopping.discount
  ○ dev.ucp.shopping.order

Transports (in order):
  1. REST
  2. MCP

Payment handlers:
  - Stripe tokenization

Key implementation tasks:
  1. Create /.well-known/ucp discovery profile
  2. Implement checkout session endpoints (create, get, update, complete)
  3. Implement fulfillment options logic
  4. Implement discount code application
  5. Set up payment handler integration
  6. Implement order webhooks
  7. Add MCP transport layer

Estimated files to create/modify: ~15-20

Run /ucp plan for detailed file-by-file plan.
```

---

## Sub-command: plan

### Trigger
User runs `/ucp plan`

### Purpose
Generate detailed implementation plan with specific files and order of operations.

### Prerequisites
- Config file must exist with completed consultation
- Spec must be available

### Procedure

#### Step 1: Load Config and Spec
- Read `./ucp.config.json`
- Read relevant spec files based on capabilities/transports

#### Step 2: Analyze Existing Codebase Structure
- Detect Next.js version (App Router vs Pages Router)
- Find existing API routes
- Find existing lib/utils structure
- Find existing types/schemas
- Identify package manager (npm, yarn, pnpm, bun)

#### Step 3: Generate File Plan
For each capability/transport, list files to create/modify.

**Example output:**

```
UCP Implementation Plan
=======================

Phase 1: Core Types and Schemas
-------------------------------
CREATE  lib/ucp/types/checkout.ts
        - CheckoutSession interface
        - LineItem, Totals, Payment types
        - Status enum

CREATE  lib/ucp/types/index.ts
        - Re-export all types

CREATE  lib/ucp/schemas/checkout.ts
        - Zod schemas for validation

Phase 2: Discovery Profile
--------------------------
CREATE  app/.well-known/ucp/route.ts
        - GET handler returning profile JSON
        - Read capabilities from config

CREATE  lib/ucp/profile.ts
        - Profile generation logic

Phase 3: Checkout Endpoints (REST)
----------------------------------
CREATE  app/api/ucp/checkout/route.ts
        - POST: Create checkout session
        - Capability negotiation logic

CREATE  app/api/ucp/checkout/[id]/route.ts
        - GET: Retrieve checkout
        - PATCH: Update checkout
        - POST: Complete checkout (action=complete)

CREATE  lib/ucp/handlers/checkout.ts
        - Business logic for checkout operations
        - State machine implementation

Phase 4: Fulfillment Extension
------------------------------
CREATE  lib/ucp/handlers/fulfillment.ts
        - Fulfillment options calculation
        - Destination validation

MODIFY  lib/ucp/handlers/checkout.ts
        - Integrate fulfillment into checkout response

Phase 5: Discount Extension
---------------------------
CREATE  lib/ucp/handlers/discount.ts
        - Discount code validation
        - Applied discount calculation

MODIFY  lib/ucp/handlers/checkout.ts
        - Integrate discounts into checkout

Phase 6: Payment Integration
----------------------------
CREATE  lib/ucp/handlers/payment.ts
        - Payment handler registry
        - payment_data processing

CREATE  lib/ucp/handlers/stripe.ts
        - Stripe-specific tokenization

Phase 7: Order Webhooks
-----------------------
CREATE  lib/ucp/handlers/order.ts
        - Order event emission
        - Webhook signing (JWS)

CREATE  lib/ucp/webhooks/sender.ts
        - Webhook delivery with retries

Phase 8: MCP Transport (if enabled)
-----------------------------------
CREATE  lib/ucp/transports/mcp.ts
        - MCP tool definitions
        - JSON-RPC handlers

Dependencies to install:
------------------------
  zod          — Schema validation
  jose         — JWS signing (if AP2/webhooks enabled)

Run /ucp scaffold to generate these files.
```

#### Step 4: Save Plan to Config
Store the plan in `answers.implementation_plan` for scaffold reference.

---

## Sub-command: gaps

### Trigger
User runs `/ucp gaps`

### Purpose
Deep analysis of existing codebase against UCP requirements. Uses AST parsing and data flow tracing.

### Prerequisites
- Config file should exist (for role/capability context)
- Spec must be available

### Procedure

#### Step 1: Load Context
- Read config for declared capabilities
- Read relevant spec files

#### Step 2: Discover Existing Code
Scan for:
- API routes (`app/api/**`, `pages/api/**`)
- Checkout-related files (search for "checkout", "cart", "order")
- Payment handling code
- Webhook implementations

#### Step 3: Deep Analysis (AST-based)
For each relevant file:
- Parse AST
- Trace data flow for checkout objects
- Identify existing patterns

**Analyze against UCP requirements:**

| Requirement | Status | Finding |
|-------------|--------|---------|
| Discovery profile at /.well-known/ucp | MISSING | No route found |
| Checkout session creation | PARTIAL | Found /api/checkout but missing UCP fields |
| Status lifecycle | MISSING | No status state machine |
| Capability negotiation | MISSING | No UCP-Agent header handling |
| Payment handler support | PARTIAL | Stripe exists but not UCP-compliant |
| Response metadata (ucp object) | MISSING | Responses don't include ucp field |

#### Step 4: Generate Gap Report

```
UCP Gap Analysis Report
=======================

Existing codebase: Next.js 14 (App Router)
Target role: Business
Target capabilities: checkout, fulfillment, discount

CRITICAL GAPS (must fix)
------------------------
[GAP-001] Missing discovery profile
  - Required: /.well-known/ucp endpoint
  - Status: NOT FOUND
  - Fix: Create app/.well-known/ucp/route.ts

[GAP-002] Missing UCP response envelope
  - Required: All responses must include `ucp` object with version/capabilities
  - Found: app/api/checkout/route.ts returns raw checkout data
  - Fix: Wrap responses with UCP metadata

[GAP-003] Missing capability negotiation
  - Required: Read UCP-Agent header, compute intersection
  - Found: No header processing in checkout routes
  - Fix: Add middleware or handler logic

PARTIAL IMPLEMENTATIONS
-----------------------
[PARTIAL-001] Checkout session exists but non-compliant
  - File: app/api/checkout/route.ts
  - Missing: id, status, currency, totals.grand_total, links, payment fields
  - Has: line_items (needs schema adjustment)

[PARTIAL-002] Payment integration exists
  - File: lib/stripe.ts
  - Issue: Direct Stripe API, not UCP payment_data flow
  - Fix: Wrap with UCP payment handler abstraction

COMPLIANT AREAS
---------------
[OK] Policy URLs configured in existing checkout
[OK] HTTPS enforced
[OK] Idempotency key support in POST handlers

RECOMMENDATIONS
---------------
1. Start with /ucp scaffold to generate compliant structure
2. Migrate existing checkout logic into new handlers
3. Run /ucp validate after migration

Total: 3 critical gaps, 2 partial, 3 compliant
```

---

## Sub-command: scaffold

### Trigger
User runs `/ucp scaffold`

### Purpose
Generate full working UCP implementation based on config and plan.

### Prerequisites
- Config file must exist
- Plan should exist (run `/ucp plan` first, or scaffold will generate one)

### Procedure

#### Step 1: Confirm Scaffold Depth
Ask user:
> "What level of code generation do you want?"
> - **types**: TypeScript interfaces and Zod schemas only
> - **scaffolding**: Structure with TODO markers for business logic
> - **full**: Complete working implementation (recommended)

Store choice in `config.scaffold_depth`

#### Step 2: Check Dependencies
Identify required packages based on config:
- `zod` — Always needed
- `jose` — If AP2 mandates or webhook signing enabled
- `uuid` — For session ID generation

Ask before installing:
> "The following packages are required: zod, jose, uuid"
> "Install now? (npm install / bun add)"

If yes, run appropriate install command.

#### Step 3: Generate Code
Generate files according to plan. For each file:
1. Create parent directories if needed
2. Write file content
3. Track in `config.generated_files`

### Code Generation Templates

#### lib/ucp/types/checkout.ts
```typescript
/**
 * UCP Checkout Types
 * Generated by /ucp scaffold
 * Spec: {spec_version}
 */

export type CheckoutStatus =
  | 'incomplete'
  | 'requires_escalation'
  | 'ready_for_complete'
  | 'complete_in_progress'
  | 'completed'
  | 'canceled';

export type MessageSeverity =
  | 'recoverable'
  | 'requires_buyer_input'
  | 'requires_buyer_review';

export interface UCPMetadata {
  version: string;
  capabilities: string[];
}

export interface LineItem {
  id: string;
  name: string;
  quantity: number;
  unit_price: number;
  total_price: number;
  currency: string;
  // Extension fields added based on config
}

export interface Totals {
  subtotal: number;
  tax: number;
  shipping: number;
  discount: number;
  grand_total: number;
  currency: string;
}

export interface PaymentInfo {
  status: 'pending' | 'authorized' | 'captured' | 'failed';
  handlers: PaymentHandler[];
  amount_due: number;
  currency: string;
}

export interface PaymentHandler {
  id: string;
  type: string;
  config?: Record<string, unknown>;
}

export interface CheckoutMessage {
  code: string;
  severity: MessageSeverity;
  message: string;
  field?: string;
}

export interface CheckoutLinks {
  self: string;
  continue_url?: string;
  privacy_policy: string;
  terms_of_service: string;
  refund_policy?: string;
  shipping_policy?: string;
}

export interface CheckoutSession {
  ucp: UCPMetadata;
  id: string;
  status: CheckoutStatus;
  currency: string;
  line_items: LineItem[];
  totals: Totals;
  payment: PaymentInfo;
  links: CheckoutLinks;
  messages: CheckoutMessage[];
  expires_at: string;
  created_at: string;
  updated_at: string;
  // Extension fields populated based on negotiated capabilities
  buyer?: BuyerInfo;
  fulfillment?: FulfillmentInfo;
  discounts?: DiscountInfo;
}

export interface BuyerInfo {
  email?: string;
  phone?: string;
  name?: string;
  // consent fields if buyer_consent extension enabled
}

// Conditional types based on extensions...
```

#### lib/ucp/schemas/checkout.ts
```typescript
/**
 * UCP Checkout Zod Schemas
 * Generated by /ucp scaffold
 */

import { z } from 'zod';

export const LineItemSchema = z.object({
  id: z.string(),
  name: z.string(),
  quantity: z.number().int().positive(),
  unit_price: z.number().int(), // minor units (cents)
  total_price: z.number().int(),
  currency: z.string().length(3),
});

export const TotalsSchema = z.object({
  subtotal: z.number().int(),
  tax: z.number().int(),
  shipping: z.number().int(),
  discount: z.number().int(),
  grand_total: z.number().int(),
  currency: z.string().length(3),
});

export const CreateCheckoutRequestSchema = z.object({
  line_items: z.array(LineItemSchema).min(1),
  currency: z.string().length(3),
  buyer: z.object({
    email: z.string().email().optional(),
    phone: z.string().optional(),
  }).optional(),
  // Extension fields...
});

export const UpdateCheckoutRequestSchema = z.object({
  line_items: z.array(LineItemSchema).optional(),
  buyer: z.object({
    email: z.string().email().optional(),
    phone: z.string().optional(),
  }).optional(),
  // Extension fields...
});

export const CompleteCheckoutRequestSchema = z.object({
  action: z.literal('complete'),
  payment_data: z.record(z.unknown()),
});

export type CreateCheckoutRequest = z.infer<typeof CreateCheckoutRequestSchema>;
export type UpdateCheckoutRequest = z.infer<typeof UpdateCheckoutRequestSchema>;
export type CompleteCheckoutRequest = z.infer<typeof CompleteCheckoutRequestSchema>;
```

#### app/.well-known/ucp/route.ts
```typescript
/**
 * UCP Discovery Profile Endpoint
 * GET /.well-known/ucp
 * Generated by /ucp scaffold
 */

import { NextResponse } from 'next/server';
import { generateProfile } from '@/lib/ucp/profile';

export const runtime = 'nodejs'; // Edge runtime is not supported

export async function GET() {
  const profile = generateProfile();

  return NextResponse.json(profile, {
    headers: {
      'Cache-Control': 'public, max-age=3600',
      'Content-Type': 'application/json',
    },
  });
}
```

#### lib/ucp/profile.ts
```typescript
/**
 * UCP Discovery Profile Generator
 * Generated by /ucp scaffold
 */

import config from '@/../ucp.config.json';

export interface UCPProfile {
  ucp: {
    version: string;
    services: Record<string, ServiceDefinition>;
    capabilities: CapabilityDefinition[];
  };
  payment?: {
    handlers: PaymentHandlerDefinition[];
  };
  signing_keys?: JsonWebKey[];
}

interface ServiceDefinition {
  version: string;
  spec: string;
  rest?: { schema: string; endpoint: string };
  mcp?: { schema: string; endpoint: string };
  a2a?: { endpoint: string };
  embedded?: { schema: string };
}

interface CapabilityDefinition {
  name: string;
  version: string;
  spec: string;
  schema: string;
  extends?: string;
  config?: Record<string, unknown>;
}

interface PaymentHandlerDefinition {
  id: string;
  type: string;
  spec: string;
  config_schema: string;
}

export function generateProfile(): UCPProfile {
  const baseUrl = `https://${config.domain}`;

  const profile: UCPProfile = {
    ucp: {
      version: config.ucp_version,
      services: {
        'dev.ucp.shopping': {
          version: config.ucp_version,
          spec: 'https://ucp.dev/spec/services/shopping',
          ...(config.transports.includes('rest') && {
            rest: {
              schema: 'https://ucp.dev/spec/services/shopping/rest.openapi.json',
              endpoint: `${baseUrl}/api/ucp`,
            },
          }),
          ...(config.transports.includes('mcp') && {
            mcp: {
              schema: 'https://ucp.dev/spec/services/shopping/mcp.openrpc.json',
              endpoint: `${baseUrl}/api/ucp/mcp`,
            },
          }),
          ...(config.transports.includes('a2a') && {
            a2a: {
              endpoint: `${baseUrl}/api/ucp/a2a`,
            },
          }),
          ...(config.transports.includes('embedded') && {
            embedded: {
              schema: 'https://ucp.dev/spec/services/shopping/embedded.openrpc.json',
            },
          }),
        },
      },
      capabilities: buildCapabilities(config),
    },
  };

  if (config.payment_handlers.length > 0) {
    profile.payment = {
      handlers: config.payment_handlers.map(buildHandlerDefinition),
    };
  }

  return profile;
}

function buildCapabilities(config: typeof import('@/../ucp.config.json')): CapabilityDefinition[] {
  const capabilities: CapabilityDefinition[] = [];

  // Core checkout capability (always present)
  capabilities.push({
    name: 'dev.ucp.shopping.checkout',
    version: config.ucp_version,
    spec: 'https://ucp.dev/spec/capabilities/checkout',
    schema: 'https://ucp.dev/spec/schemas/shopping/checkout.json',
  });

  // Add extensions based on config
  for (const ext of config.capabilities.extensions) {
    capabilities.push(buildExtensionCapability(ext, config));
  }

  return capabilities;
}

function buildExtensionCapability(
  extension: string,
  config: typeof import('@/../ucp.config.json')
): CapabilityDefinition {
  // Map extension names to spec URLs
  const extMap: Record<string, { spec: string; schema: string; extends?: string }> = {
    'dev.ucp.shopping.fulfillment': {
      spec: 'https://ucp.dev/spec/capabilities/fulfillment',
      schema: 'https://ucp.dev/spec/schemas/shopping/fulfillment.json',
      extends: 'dev.ucp.shopping.checkout',
    },
    'dev.ucp.shopping.discount': {
      spec: 'https://ucp.dev/spec/capabilities/discount',
      schema: 'https://ucp.dev/spec/schemas/shopping/discount.json',
      extends: 'dev.ucp.shopping.checkout',
    },
    'dev.ucp.shopping.buyer_consent': {
      spec: 'https://ucp.dev/spec/capabilities/buyer-consent',
      schema: 'https://ucp.dev/spec/schemas/shopping/buyer-consent.json',
      extends: 'dev.ucp.shopping.checkout',
    },
    'dev.ucp.shopping.order': {
      spec: 'https://ucp.dev/spec/capabilities/order',
      schema: 'https://ucp.dev/spec/schemas/shopping/order.json',
      config: {
        webhook_url: config.answers?.webhook_config?.url,
      },
    },
    'dev.ucp.common.identity_linking': {
      spec: 'https://ucp.dev/spec/capabilities/identity-linking',
      schema: 'https://ucp.dev/spec/schemas/common/identity-linking.json',
    },
  };

  const def = extMap[extension];
  return {
    name: extension,
    version: config.ucp_version,
    spec: def?.spec || '',
    schema: def?.schema || '',
    ...(def?.extends && { extends: def.extends }),
    ...(def?.config && { config: def.config }),
  };
}

function buildHandlerDefinition(handlerId: string): PaymentHandlerDefinition {
  // Map known handlers
  const handlerMap: Record<string, Omit<PaymentHandlerDefinition, 'id'>> = {
    stripe: {
      type: 'tokenization',
      spec: 'https://ucp.dev/spec/handlers/stripe',
      config_schema: 'https://ucp.dev/spec/handlers/stripe/config.json',
    },
    // Add more handlers as needed
  };

  const def = handlerMap[handlerId] || {
    type: 'custom',
    spec: '',
    config_schema: '',
  };

  return { id: handlerId, ...def };
}
```

#### app/api/ucp/checkout/route.ts
```typescript
/**
 * UCP Checkout Session Endpoint
 * POST /api/ucp/checkout - Create checkout session
 * Generated by /ucp scaffold
 */

import { NextRequest, NextResponse } from 'next/server';
import { createCheckout } from '@/lib/ucp/handlers/checkout';
import { CreateCheckoutRequestSchema } from '@/lib/ucp/schemas/checkout';
import { negotiateCapabilities, parseUCPAgent } from '@/lib/ucp/negotiation';
import { wrapResponse, errorResponse } from '@/lib/ucp/response';

export const runtime = 'nodejs'; // Edge runtime is not supported

export async function POST(request: NextRequest) {
  try {
    // Parse UCP-Agent header for capability negotiation
    const ucpAgent = parseUCPAgent(request.headers.get('UCP-Agent'));

    // Negotiate capabilities
    const negotiation = await negotiateCapabilities(ucpAgent?.profile);

    // Parse and validate request body
    const body = await request.json();
    const parsed = CreateCheckoutRequestSchema.safeParse(body);

    if (!parsed.success) {
      return errorResponse(400, 'invalid_request', parsed.error.message);
    }

    // Get idempotency key
    const idempotencyKey = request.headers.get('Idempotency-Key');

    // Create checkout session
    const checkout = await createCheckout(parsed.data, {
      capabilities: negotiation.capabilities,
      idempotencyKey,
    });

    return wrapResponse(checkout, negotiation, 201);
  } catch (error) {
    console.error('Checkout creation failed:', error);
    return errorResponse(500, 'internal_error', 'Failed to create checkout session');
  }
}
```

#### lib/ucp/handlers/checkout.ts
```typescript
/**
 * UCP Checkout Handler
 * Core business logic for checkout operations
 * Generated by /ucp scaffold
 */

import { randomUUID } from 'crypto';
import type {
  CheckoutSession,
  CheckoutStatus,
  CreateCheckoutRequest,
  UpdateCheckoutRequest,
} from '@/lib/ucp/types/checkout';
import config from '@/../ucp.config.json';

// In-memory store for demo - replace with your database
const checkoutStore = new Map<string, CheckoutSession>();

interface CreateCheckoutOptions {
  capabilities: string[];
  idempotencyKey?: string | null;
}

export async function createCheckout(
  request: CreateCheckoutRequest,
  options: CreateCheckoutOptions
): Promise<CheckoutSession> {
  const id = randomUUID();
  const now = new Date().toISOString();
  const expiresAt = new Date(Date.now() + 30 * 60 * 1000).toISOString(); // 30 min

  // Calculate totals
  const subtotal = request.line_items.reduce((sum, item) => sum + item.total_price, 0);
  const tax = calculateTax(subtotal); // Implement your tax logic
  const shipping = 0; // Set by fulfillment extension
  const discount = 0; // Set by discount extension

  const checkout: CheckoutSession = {
    ucp: {
      version: config.ucp_version,
      capabilities: options.capabilities,
    },
    id,
    status: 'incomplete',
    currency: request.currency,
    line_items: request.line_items.map((item, index) => ({
      ...item,
      id: item.id || `line_${index}`,
    })),
    totals: {
      subtotal,
      tax,
      shipping,
      discount,
      grand_total: subtotal + tax + shipping - discount,
      currency: request.currency,
    },
    payment: {
      status: 'pending',
      handlers: getPaymentHandlers(options.capabilities),
      amount_due: subtotal + tax + shipping - discount,
      currency: request.currency,
    },
    links: {
      self: `https://${config.domain}/api/ucp/checkout/${id}`,
      continue_url: `https://${config.domain}/checkout/${id}`,
      privacy_policy: config.policy_urls.privacy,
      terms_of_service: config.policy_urls.terms,
      ...(config.policy_urls.refunds && { refund_policy: config.policy_urls.refunds }),
      ...(config.policy_urls.shipping && { shipping_policy: config.policy_urls.shipping }),
    },
    messages: [],
    expires_at: expiresAt,
    created_at: now,
    updated_at: now,
  };

  // Add buyer info if provided
  if (request.buyer) {
    checkout.buyer = request.buyer;
  }

  // Validate checkout state and set appropriate status
  checkout.status = determineStatus(checkout);
  checkout.messages = generateMessages(checkout);

  // Store checkout
  checkoutStore.set(id, checkout);

  return checkout;
}

export async function getCheckout(id: string): Promise<CheckoutSession | null> {
  return checkoutStore.get(id) || null;
}

export async function updateCheckout(
  id: string,
  request: UpdateCheckoutRequest,
  capabilities: string[]
): Promise<CheckoutSession | null> {
  const checkout = checkoutStore.get(id);
  if (!checkout) return null;

  // Check if checkout can be modified
  if (['completed', 'canceled'].includes(checkout.status)) {
    throw new Error('Checkout cannot be modified in current state');
  }

  // Apply updates
  if (request.line_items) {
    checkout.line_items = request.line_items;
    recalculateTotals(checkout);
  }

  if (request.buyer) {
    checkout.buyer = { ...checkout.buyer, ...request.buyer };
  }

  // Update metadata
  checkout.updated_at = new Date().toISOString();
  checkout.ucp.capabilities = capabilities;
  checkout.status = determineStatus(checkout);
  checkout.messages = generateMessages(checkout);

  checkoutStore.set(id, checkout);
  return checkout;
}

export async function completeCheckout(
  id: string,
  paymentData: Record<string, unknown>,
  capabilities: string[]
): Promise<CheckoutSession | null> {
  const checkout = checkoutStore.get(id);
  if (!checkout) return null;

  if (checkout.status !== 'ready_for_complete') {
    throw new Error('Checkout is not ready for completion');
  }

  checkout.status = 'complete_in_progress';
  checkout.updated_at = new Date().toISOString();
  checkoutStore.set(id, checkout);

  try {
    // Process payment
    await processPayment(checkout, paymentData);

    checkout.status = 'completed';
    checkout.payment.status = 'captured';
    checkout.updated_at = new Date().toISOString();
    checkoutStore.set(id, checkout);

    // Emit order event if order capability enabled
    if (capabilities.includes('dev.ucp.shopping.order')) {
      await emitOrderCreated(checkout);
    }

    return checkout;
  } catch (error) {
    checkout.status = 'incomplete';
    checkout.payment.status = 'failed';
    checkout.messages.push({
      code: 'payment_failed',
      severity: 'recoverable',
      message: error instanceof Error ? error.message : 'Payment processing failed',
    });
    checkout.updated_at = new Date().toISOString();
    checkoutStore.set(id, checkout);
    return checkout;
  }
}

function determineStatus(checkout: CheckoutSession): CheckoutStatus {
  // Check for missing required fields
  const missingFields: string[] = [];

  if (!checkout.buyer?.email) {
    missingFields.push('buyer.email');
  }

  // Check fulfillment if extension enabled
  if (checkout.fulfillment && !checkout.fulfillment.selected_option) {
    missingFields.push('fulfillment.selected_option');
  }

  if (missingFields.length > 0) {
    return 'incomplete';
  }

  // Check if buyer input needed
  if (checkout.messages.some(m => m.severity === 'requires_buyer_input')) {
    return 'requires_escalation';
  }

  return 'ready_for_complete';
}

function generateMessages(checkout: CheckoutSession): CheckoutSession['messages'] {
  const messages: CheckoutSession['messages'] = [];

  if (!checkout.buyer?.email) {
    messages.push({
      code: 'missing_email',
      severity: 'recoverable',
      message: 'Buyer email is required',
      field: 'buyer.email',
    });
  }

  return messages;
}

function recalculateTotals(checkout: CheckoutSession): void {
  const subtotal = checkout.line_items.reduce((sum, item) => sum + item.total_price, 0);
  checkout.totals.subtotal = subtotal;
  checkout.totals.tax = calculateTax(subtotal);
  checkout.totals.grand_total =
    subtotal + checkout.totals.tax + checkout.totals.shipping - checkout.totals.discount;
  checkout.payment.amount_due = checkout.totals.grand_total;
}

function calculateTax(subtotal: number): number {
  // Implement your tax calculation logic
  return Math.round(subtotal * 0.08); // Example: 8% tax
}

function getPaymentHandlers(capabilities: string[]): CheckoutSession['payment']['handlers'] {
  // Return configured payment handlers
  return config.payment_handlers.map(id => ({
    id,
    type: 'tokenization',
  }));
}

async function processPayment(
  checkout: CheckoutSession,
  paymentData: Record<string, unknown>
): Promise<void> {
  // Validate handler_id against advertised handlers
  const handlerId = paymentData.handler_id as string;
  if (!config.payment_handlers.includes(handlerId)) {
    throw new Error(`Unknown payment handler: ${handlerId}`);
  }

  // Implement payment processing based on handler
  // This is where you integrate with Stripe, etc.
}

async function emitOrderCreated(checkout: CheckoutSession): Promise<void> {
  // Implement order webhook emission
  // See lib/ucp/webhooks/sender.ts
}
```

#### lib/ucp/negotiation.ts
```typescript
/**
 * UCP Capability Negotiation
 * Generated by /ucp scaffold
 */

import config from '@/../ucp.config.json';

interface UCPAgentInfo {
  profile: string;
}

interface NegotiationResult {
  capabilities: string[];
  version: string;
}

/**
 * Parse UCP-Agent header (RFC 8941 dictionary syntax)
 * Example: profile="https://platform.example.com/.well-known/ucp"
 */
export function parseUCPAgent(header: string | null): UCPAgentInfo | null {
  if (!header) return null;

  const profileMatch = header.match(/profile="([^"]+)"/);
  if (!profileMatch) return null;

  return { profile: profileMatch[1] };
}

/**
 * Negotiate capabilities between business and platform
 */
export async function negotiateCapabilities(
  platformProfileUrl?: string
): Promise<NegotiationResult> {
  // Business capabilities
  const businessCapabilities = new Set([
    ...config.capabilities.core,
    ...config.capabilities.extensions,
  ]);

  if (!platformProfileUrl) {
    // No platform profile - return all business capabilities
    return {
      capabilities: Array.from(businessCapabilities),
      version: config.ucp_version,
    };
  }

  try {
    // Fetch platform profile
    const response = await fetch(platformProfileUrl, {
      headers: { Accept: 'application/json' },
    });

    if (!response.ok) {
      console.warn(`Failed to fetch platform profile: ${response.status}`);
      return {
        capabilities: Array.from(businessCapabilities),
        version: config.ucp_version,
      };
    }

    const platformProfile = await response.json();

    // Validate namespace authority
    const profileUrl = new URL(platformProfileUrl);
    // Platform controls its own domain - trust it

    // Compute intersection
    const platformCapabilities = new Set(
      platformProfile.ucp?.capabilities?.map((c: { name: string }) => c.name) || []
    );

    const intersection = [...businessCapabilities].filter(c =>
      platformCapabilities.has(c)
    );

    // Version negotiation - accept platform version <= business version
    const platformVersion = platformProfile.ucp?.version;
    if (platformVersion && platformVersion > config.ucp_version) {
      throw new Error('version_unsupported');
    }

    return {
      capabilities: intersection,
      version: config.ucp_version,
    };
  } catch (error) {
    console.error('Capability negotiation failed:', error);
    // Fall back to business capabilities
    return {
      capabilities: Array.from(businessCapabilities),
      version: config.ucp_version,
    };
  }
}
```

#### lib/ucp/response.ts
```typescript
/**
 * UCP Response Helpers
 * Generated by /ucp scaffold
 */

import { NextResponse } from 'next/server';
import type { NegotiationResult } from './negotiation';

/**
 * Wrap a response with UCP metadata
 */
export function wrapResponse<T extends { ucp?: unknown }>(
  data: T,
  negotiation: NegotiationResult,
  status: number = 200
): NextResponse {
  // Ensure ucp metadata is present
  const response = {
    ...data,
    ucp: {
      version: negotiation.version,
      capabilities: negotiation.capabilities,
    },
  };

  return NextResponse.json(response, { status });
}

/**
 * Create an error response
 */
export function errorResponse(
  status: number,
  code: string,
  message: string,
  details?: Record<string, unknown>
): NextResponse {
  return NextResponse.json(
    {
      error: {
        code,
        message,
        ...(details && { details }),
      },
    },
    { status }
  );
}
```

### MCP Transport Code Templates (using mcp-handler)

When MCP transport is enabled in config, generate these additional files.

#### Dependencies for MCP Transport
```bash
npm install mcp-handler @modelcontextprotocol/sdk@1.25.2 zod
```

**IMPORTANT:** Use `@modelcontextprotocol/sdk@1.25.2` or later — earlier versions have security vulnerabilities.

#### app/api/mcp/[transport]/route.ts
```typescript
/**
 * UCP MCP Transport Endpoint
 * Model Context Protocol server for UCP checkout operations
 * Generated by /ucp scaffold
 *
 * Supports:
 * - Streamable HTTP transport (direct client connection)
 * - SSE transport (via mcp-remote bridge)
 *
 * @see https://github.com/vercel/mcp-handler
 */

import { createMcpHandler } from 'mcp-handler';
import { z } from 'zod';
import {
  createCheckout,
  getCheckout,
  updateCheckout,
  completeCheckout,
} from '@/lib/ucp/handlers/checkout';
import { negotiateCapabilities } from '@/lib/ucp/negotiation';
import { generateProfile } from '@/lib/ucp/profile';
import config from '@/../ucp.config.json';

export const runtime = 'nodejs'; // Edge runtime is not supported

const handler = createMcpHandler(
  (server) => {
    // =========================================================================
    // UCP Discovery
    // =========================================================================

    server.registerTool(
      'ucp_get_profile',
      {
        title: 'Get UCP Profile',
        description: 'Retrieve the UCP discovery profile for this business. Returns supported capabilities, transports, and payment handlers.',
        inputSchema: {},
      },
      async () => {
        const profile = generateProfile();
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(profile, null, 2),
            },
          ],
        };
      }
    );

    // =========================================================================
    // Checkout Session Management
    // =========================================================================

    server.registerTool(
      'ucp_create_checkout',
      {
        title: 'Create Checkout Session',
        description: 'Create a new UCP checkout session with line items. Returns a checkout session with id, status, totals, and available payment handlers.',
        inputSchema: {
          line_items: z.array(
            z.object({
              id: z.string().optional().describe('Unique identifier for the line item'),
              name: z.string().describe('Product name'),
              quantity: z.number().int().positive().describe('Quantity ordered'),
              unit_price: z.number().int().describe('Price per unit in minor units (cents)'),
              total_price: z.number().int().describe('Total price for this line (quantity * unit_price)'),
              currency: z.string().length(3).describe('ISO 4217 currency code'),
            })
          ).min(1).describe('Array of items in the checkout'),
          currency: z.string().length(3).describe('ISO 4217 currency code for the checkout'),
          buyer: z.object({
            email: z.string().email().optional().describe('Buyer email address'),
            phone: z.string().optional().describe('Buyer phone number'),
            name: z.string().optional().describe('Buyer full name'),
          }).optional().describe('Buyer information'),
          platform_profile_url: z.string().url().optional().describe('URL to the platform UCP profile for capability negotiation'),
        },
      },
      async ({ line_items, currency, buyer, platform_profile_url }) => {
        try {
          // Negotiate capabilities
          const negotiation = await negotiateCapabilities(platform_profile_url);

          const checkout = await createCheckout(
            { line_items, currency, buyer },
            { capabilities: negotiation.capabilities }
          );

          return {
            content: [
              {
                type: 'text',
                text: JSON.stringify(checkout, null, 2),
              },
            ],
          };
        } catch (error) {
          return {
            content: [
              {
                type: 'text',
                text: JSON.stringify({
                  error: {
                    code: 'checkout_creation_failed',
                    message: error instanceof Error ? error.message : 'Unknown error',
                  },
                }),
              },
            ],
            isError: true,
          };
        }
      }
    );

    server.registerTool(
      'ucp_get_checkout',
      {
        title: 'Get Checkout Session',
        description: 'Retrieve an existing checkout session by ID. Returns the current state including status, line items, totals, and messages.',
        inputSchema: {
          checkout_id: z.string().describe('The checkout session ID'),
        },
      },
      async ({ checkout_id }) => {
        const checkout = await getCheckout(checkout_id);

        if (!checkout) {
          return {
            content: [
              {
                type: 'text',
                text: JSON.stringify({
                  error: {
                    code: 'checkout_not_found',
                    message: `Checkout session ${checkout_id} not found`,
                  },
                }),
              },
            ],
            isError: true,
          };
        }

        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(checkout, null, 2),
            },
          ],
        };
      }
    );

    server.registerTool(
      'ucp_update_checkout',
      {
        title: 'Update Checkout Session',
        description: 'Update an existing checkout session. Can modify line items, buyer info, fulfillment selection, or discount codes.',
        inputSchema: {
          checkout_id: z.string().describe('The checkout session ID'),
          line_items: z.array(
            z.object({
              id: z.string(),
              name: z.string(),
              quantity: z.number().int().positive(),
              unit_price: z.number().int(),
              total_price: z.number().int(),
              currency: z.string().length(3),
            })
          ).optional().describe('Updated line items (replaces existing)'),
          buyer: z.object({
            email: z.string().email().optional(),
            phone: z.string().optional(),
            name: z.string().optional(),
          }).optional().describe('Updated buyer information (merged with existing)'),
          fulfillment: z.object({
            selected_option_id: z.string().optional().describe('ID of selected fulfillment option'),
            destination: z.object({
              address_line1: z.string(),
              address_line2: z.string().optional(),
              city: z.string(),
              state: z.string().optional(),
              postal_code: z.string(),
              country: z.string().length(2),
            }).optional().describe('Shipping destination address'),
          }).optional().describe('Fulfillment selection (if fulfillment extension enabled)'),
          discount_codes: z.array(z.string()).optional().describe('Discount codes to apply (if discount extension enabled)'),
          platform_profile_url: z.string().url().optional().describe('Platform profile URL for capability negotiation'),
        },
      },
      async ({ checkout_id, line_items, buyer, fulfillment, discount_codes, platform_profile_url }) => {
        try {
          const negotiation = await negotiateCapabilities(platform_profile_url);

          const checkout = await updateCheckout(
            checkout_id,
            { line_items, buyer },
            negotiation.capabilities
          );

          if (!checkout) {
            return {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify({
                    error: {
                      code: 'checkout_not_found',
                      message: `Checkout session ${checkout_id} not found`,
                    },
                  }),
                },
              ],
              isError: true,
            };
          }

          return {
            content: [
              {
                type: 'text',
                text: JSON.stringify(checkout, null, 2),
              },
            ],
          };
        } catch (error) {
          return {
            content: [
              {
                type: 'text',
                text: JSON.stringify({
                  error: {
                    code: 'checkout_update_failed',
                    message: error instanceof Error ? error.message : 'Unknown error',
                  },
                }),
              },
            ],
            isError: true,
          };
        }
      }
    );

    server.registerTool(
      'ucp_complete_checkout',
      {
        title: 'Complete Checkout',
        description: 'Complete a checkout session with payment. Checkout must be in ready_for_complete status. Returns the completed checkout or error messages.',
        inputSchema: {
          checkout_id: z.string().describe('The checkout session ID'),
          payment_data: z.object({
            handler_id: z.string().describe('Payment handler ID (must match one from checkout.payment.handlers)'),
            token: z.string().optional().describe('Payment token from tokenization handler'),
            instrument: z.record(z.unknown()).optional().describe('Payment instrument data'),
          }).describe('Payment data from the selected payment handler'),
          platform_profile_url: z.string().url().optional().describe('Platform profile URL'),
        },
      },
      async ({ checkout_id, payment_data, platform_profile_url }) => {
        try {
          const negotiation = await negotiateCapabilities(platform_profile_url);

          const checkout = await completeCheckout(
            checkout_id,
            payment_data,
            negotiation.capabilities
          );

          if (!checkout) {
            return {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify({
                    error: {
                      code: 'checkout_not_found',
                      message: `Checkout session ${checkout_id} not found`,
                    },
                  }),
                },
              ],
              isError: true,
            };
          }

          return {
            content: [
              {
                type: 'text',
                text: JSON.stringify(checkout, null, 2),
              },
            ],
          };
        } catch (error) {
          return {
            content: [
              {
                type: 'text',
                text: JSON.stringify({
                  error: {
                    code: 'checkout_completion_failed',
                    message: error instanceof Error ? error.message : 'Unknown error',
                  },
                }),
              },
            ],
            isError: true,
          };
        }
      }
    );

    // =========================================================================
    // Fulfillment Extension Tools (if enabled)
    // =========================================================================

    if (config.capabilities.extensions.includes('dev.ucp.shopping.fulfillment')) {
      server.registerTool(
        'ucp_get_fulfillment_options',
        {
          title: 'Get Fulfillment Options',
          description: 'Get available fulfillment/shipping options for a checkout. Requires a destination address.',
          inputSchema: {
            checkout_id: z.string().describe('The checkout session ID'),
            destination: z.object({
              address_line1: z.string(),
              address_line2: z.string().optional(),
              city: z.string(),
              state: z.string().optional(),
              postal_code: z.string(),
              country: z.string().length(2).describe('ISO 3166-1 alpha-2 country code'),
            }).describe('Shipping destination'),
          },
        },
        async ({ checkout_id, destination }) => {
          // Implementation would call fulfillment handler
          return {
            content: [
              {
                type: 'text',
                text: JSON.stringify({
                  checkout_id,
                  destination,
                  options: [
                    {
                      id: 'standard',
                      name: 'Standard Shipping',
                      description: '5-7 business days',
                      price: 599,
                      currency: 'USD',
                    },
                    {
                      id: 'express',
                      name: 'Express Shipping',
                      description: '2-3 business days',
                      price: 1299,
                      currency: 'USD',
                    },
                  ],
                }, null, 2),
              },
            ],
          };
        }
      );
    }

    // =========================================================================
    // Discount Extension Tools (if enabled)
    // =========================================================================

    if (config.capabilities.extensions.includes('dev.ucp.shopping.discount')) {
      server.registerTool(
        'ucp_validate_discount',
        {
          title: 'Validate Discount Code',
          description: 'Validate a discount code before applying to checkout. Returns discount details or rejection reason.',
          inputSchema: {
            checkout_id: z.string().describe('The checkout session ID'),
            code: z.string().describe('The discount code to validate'),
          },
        },
        async ({ checkout_id, code }) => {
          // Implementation would call discount handler
          return {
            content: [
              {
                type: 'text',
                text: JSON.stringify({
                  valid: true,
                  code,
                  discount: {
                    type: 'percentage',
                    value: 10,
                    description: '10% off your order',
                  },
                }, null, 2),
              },
            ],
          };
        }
      );
    }

    // =========================================================================
    // Payment Handler Tools
    // =========================================================================

    server.registerTool(
      'ucp_get_payment_handlers',
      {
        title: 'Get Payment Handlers',
        description: 'Get available payment handlers for a checkout session. Use this to determine how to collect payment information.',
        inputSchema: {
          checkout_id: z.string().describe('The checkout session ID'),
        },
      },
      async ({ checkout_id }) => {
        const checkout = await getCheckout(checkout_id);

        if (!checkout) {
          return {
            content: [
              {
                type: 'text',
                text: JSON.stringify({
                  error: {
                    code: 'checkout_not_found',
                    message: `Checkout session ${checkout_id} not found`,
                  },
                }),
              },
            ],
            isError: true,
          };
        }

        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify({
                checkout_id,
                amount_due: checkout.payment.amount_due,
                currency: checkout.payment.currency,
                handlers: checkout.payment.handlers,
              }, null, 2),
            },
          ],
        };
      }
    );
  },
  {
    // Server metadata
    name: 'ucp-shopping',
    version: config.ucp_version,
  },
  {
    // Handler options
    basePath: '/api/mcp',
    maxDuration: 60,
    verboseLogs: process.env.NODE_ENV === 'development',
  }
);

export { handler as GET, handler as POST };
```

#### lib/ucp/transports/mcp-tools.ts
```typescript
/**
 * UCP MCP Tool Definitions
 * Reusable tool schemas for MCP transport
 * Generated by /ucp scaffold
 */

import { z } from 'zod';

// Common schemas
export const LineItemSchema = z.object({
  id: z.string().optional(),
  name: z.string(),
  quantity: z.number().int().positive(),
  unit_price: z.number().int(),
  total_price: z.number().int(),
  currency: z.string().length(3),
});

export const BuyerSchema = z.object({
  email: z.string().email().optional(),
  phone: z.string().optional(),
  name: z.string().optional(),
});

export const AddressSchema = z.object({
  address_line1: z.string(),
  address_line2: z.string().optional(),
  city: z.string(),
  state: z.string().optional(),
  postal_code: z.string(),
  country: z.string().length(2),
});

export const PaymentDataSchema = z.object({
  handler_id: z.string(),
  token: z.string().optional(),
  instrument: z.record(z.unknown()).optional(),
});

// Tool definitions for documentation
export const UCP_MCP_TOOLS = {
  ucp_get_profile: {
    description: 'Get UCP discovery profile',
    input: {},
  },
  ucp_create_checkout: {
    description: 'Create a new checkout session',
    input: {
      line_items: 'Array of line items (required)',
      currency: 'ISO 4217 currency code (required)',
      buyer: 'Buyer information (optional)',
      platform_profile_url: 'Platform UCP profile URL (optional)',
    },
  },
  ucp_get_checkout: {
    description: 'Get checkout session by ID',
    input: {
      checkout_id: 'Checkout session ID (required)',
    },
  },
  ucp_update_checkout: {
    description: 'Update checkout session',
    input: {
      checkout_id: 'Checkout session ID (required)',
      line_items: 'Updated line items (optional)',
      buyer: 'Updated buyer info (optional)',
      fulfillment: 'Fulfillment selection (optional)',
      discount_codes: 'Discount codes to apply (optional)',
    },
  },
  ucp_complete_checkout: {
    description: 'Complete checkout with payment',
    input: {
      checkout_id: 'Checkout session ID (required)',
      payment_data: 'Payment handler data (required)',
    },
  },
  ucp_get_fulfillment_options: {
    description: 'Get shipping options (fulfillment extension)',
    input: {
      checkout_id: 'Checkout session ID (required)',
      destination: 'Shipping address (required)',
    },
  },
  ucp_validate_discount: {
    description: 'Validate discount code (discount extension)',
    input: {
      checkout_id: 'Checkout session ID (required)',
      code: 'Discount code (required)',
    },
  },
  ucp_get_payment_handlers: {
    description: 'Get available payment handlers',
    input: {
      checkout_id: 'Checkout session ID (required)',
    },
  },
} as const;
```

---

## Vercel Deployment

### Deployment Configuration

#### vercel.json
```json
{
  "framework": "nextjs",
  "regions": ["iad1"],
  "functions": {
    "app/api/mcp/[transport]/route.ts": {
      "maxDuration": 60
    },
    "app/api/ucp/**/*.ts": {
      "maxDuration": 30
    }
  },
  "headers": [
    {
      "source": "/.well-known/ucp",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=3600"
        },
        {
          "key": "Content-Type",
          "value": "application/json"
        }
      ]
    }
  ]
}
```

#### Environment Variables
Set these in Vercel Dashboard → Settings → Environment Variables:

| Variable | Required | Description |
|----------|----------|-------------|
| `UCP_DOMAIN` | Yes | Production domain (e.g., `shop.example.com`) |
| `UCP_SIGNING_KEY` | If AP2 | JWS signing key (PEM or JWK) |
| `STRIPE_SECRET_KEY` | If Stripe | Stripe API secret key |

#### next.config.js (MCP-optimized)
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Required for mcp-handler streaming
  experimental: {
    serverActions: {
      bodySizeLimit: '2mb',
    },
  },

  // Ensure proper headers for MCP
  async headers() {
    return [
      {
        source: '/api/mcp/:path*',
        headers: [
          { key: 'Access-Control-Allow-Origin', value: '*' },
          { key: 'Access-Control-Allow-Methods', value: 'GET, POST, OPTIONS' },
          { key: 'Access-Control-Allow-Headers', value: 'Content-Type, Authorization' },
        ],
      },
    ];
  },

  // Required for MCP streaming responses
  async rewrites() {
    return [];
  },
};

module.exports = nextConfig;
```

### MCP Client Configuration

#### For Claude Desktop / Cursor / Windsurf

**Option 1: Direct HTTP (if client supports streamable HTTP)**
Add to MCP client config:
```json
{
  "mcpServers": {
    "ucp-shopping": {
      "url": "https://your-domain.vercel.app/api/mcp"
    }
  }
}
```

**Option 2: Via mcp-remote bridge (for stdio-only clients)**
```json
{
  "mcpServers": {
    "ucp-shopping": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://your-domain.vercel.app/api/mcp"]
    }
  }
}
```

### Testing MCP Deployment

#### scripts/test-mcp.mjs
```javascript
#!/usr/bin/env node
/**
 * MCP Server Test Script
 * Usage: node scripts/test-mcp.mjs [deployment-url]
 */

const deploymentUrl = process.argv[2] || 'http://localhost:3000';

async function testMcpServer() {
  console.log(`Testing MCP server at ${deploymentUrl}/api/mcp\n`);

  // Test 1: Get Profile
  console.log('1. Testing ucp_get_profile...');
  const profileResponse = await fetch(`${deploymentUrl}/api/mcp`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      jsonrpc: '2.0',
      id: 1,
      method: 'tools/call',
      params: {
        name: 'ucp_get_profile',
        arguments: {},
      },
    }),
  });
  const profileResult = await profileResponse.json();
  console.log('   Profile:', profileResult.result ? 'OK' : 'FAILED');

  // Test 2: Create Checkout
  console.log('2. Testing ucp_create_checkout...');
  const createResponse = await fetch(`${deploymentUrl}/api/mcp`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      jsonrpc: '2.0',
      id: 2,
      method: 'tools/call',
      params: {
        name: 'ucp_create_checkout',
        arguments: {
          line_items: [
            {
              name: 'Test Product',
              quantity: 1,
              unit_price: 1000,
              total_price: 1000,
              currency: 'USD',
            },
          ],
          currency: 'USD',
        },
      },
    }),
  });
  const createResult = await createResponse.json();
  console.log('   Create:', createResult.result ? 'OK' : 'FAILED');

  // Parse checkout ID for subsequent tests
  if (createResult.result?.content?.[0]?.text) {
    const checkout = JSON.parse(createResult.result.content[0].text);
    console.log(`   Checkout ID: ${checkout.id}`);
    console.log(`   Status: ${checkout.status}`);

    // Test 3: Get Checkout
    console.log('3. Testing ucp_get_checkout...');
    const getResponse = await fetch(`${deploymentUrl}/api/mcp`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        jsonrpc: '2.0',
        id: 3,
        method: 'tools/call',
        params: {
          name: 'ucp_get_checkout',
          arguments: { checkout_id: checkout.id },
        },
      }),
    });
    const getResult = await getResponse.json();
    console.log('   Get:', getResult.result ? 'OK' : 'FAILED');
  }

  console.log('\nMCP server tests completed.');
}

testMcpServer().catch(console.error);
```

### Vercel Deployment Checklist

When running `/ucp scaffold` with Vercel deployment, verify:

- [ ] `vercel.json` created with function timeouts
- [ ] Environment variables documented
- [ ] `next.config.js` updated for MCP streaming
- [ ] MCP route at `app/api/mcp/[transport]/route.ts`
- [ ] Test script at `scripts/test-mcp.mjs`
- [ ] `.env.example` updated with required variables

### Post-Deployment Verification

After deploying to Vercel:

1. **Check discovery profile:**
   ```bash
   curl https://your-domain.vercel.app/.well-known/ucp | jq .
   ```

2. **Test MCP endpoint:**
   ```bash
   node scripts/test-mcp.mjs https://your-domain.vercel.app
   ```

3. **Configure MCP client:**
   Add the server to Claude Desktop, Cursor, or your preferred MCP client.

4. **Verify in client:**
   Ask the AI to "list available UCP tools" — it should show the checkout tools.

---

### Post-Generation Steps

#### Step 4: Update Config
After generation, update `ucp.config.json`:
- Add all created files to `generated_files` array
- Update `scaffold_depth` to reflect what was generated

#### Step 5: Output Summary
```
UCP Scaffold Complete
=====================

Generated files:
  CREATE  lib/ucp/types/checkout.ts
  CREATE  lib/ucp/types/index.ts
  CREATE  lib/ucp/schemas/checkout.ts
  CREATE  lib/ucp/profile.ts
  CREATE  lib/ucp/negotiation.ts
  CREATE  lib/ucp/response.ts
  CREATE  lib/ucp/handlers/checkout.ts
  CREATE  app/.well-known/ucp/route.ts
  CREATE  app/api/ucp/checkout/route.ts
  CREATE  app/api/ucp/checkout/[id]/route.ts

MCP Transport (if enabled):
  CREATE  app/api/mcp/[transport]/route.ts
  CREATE  lib/ucp/transports/mcp-tools.ts

Vercel Deployment:
  CREATE  vercel.json
  CREATE  scripts/test-mcp.mjs
  MODIFY  next.config.js

Dependencies installed:
  zod, jose, uuid
  mcp-handler, @modelcontextprotocol/sdk (if MCP enabled)

Next steps:
  1. Review generated code and customize business logic
  2. Set environment variables in Vercel dashboard
  3. Deploy: vercel --prod
  4. Run /ucp profile to verify discovery profile
  5. Run /ucp test to generate unit tests
  6. Run /ucp validate to check compliance
  7. Configure MCP client with deployment URL
```

---

## Sub-command: validate

### Trigger
User runs `/ucp validate`

### Purpose
Validate the implementation against UCP JSON schemas.

### Prerequisites
- Implementation must exist (run `/ucp scaffold` first)
- Spec must be available

### Procedure

#### Step 1: Load Schemas
Read JSON schemas from spec:
- `spec/schemas/shopping/checkout.json`
- `spec/schemas/shopping/fulfillment.json`
- `spec/schemas/shopping/discount.json`
- `spec/discovery/profile_schema.json`

#### Step 2: Validate Discovery Profile
- Make request to `/.well-known/ucp` route (or read file directly)
- Validate against `profile_schema.json`

#### Step 3: Validate Response Shapes
For each implemented endpoint:
- Generate sample request
- Execute handler (mock mode)
- Validate response against schema

#### Step 4: Check Protocol Requirements
Verify:
- [ ] All responses include `ucp` object
- [ ] Status values are valid enum values
- [ ] Amounts are integers (minor units)
- [ ] Dates are RFC 3339 format
- [ ] Links are absolute HTTPS URLs
- [ ] Capability names follow reverse-DNS format

#### Step 5: Output Report
```
UCP Validation Report
=====================

Discovery Profile: PASS
  ✓ Schema valid
  ✓ Required fields present
  ✓ Service definitions valid
  ✓ Capability specs accessible

Checkout Endpoints:
  POST /api/ucp/checkout
    ✓ Response schema valid
    ✓ UCP metadata present
    ✓ Status enum valid

  GET /api/ucp/checkout/[id]
    ✓ Response schema valid
    ✓ Idempotent

  PATCH /api/ucp/checkout/[id]
    ✓ Response schema valid
    ✓ Partial update works

  POST /api/ucp/checkout/[id] (complete)
    ✓ Response schema valid
    ✓ State transition correct

Protocol Requirements:
  ✓ Amounts in minor units
  ✓ Dates in RFC 3339
  ✓ HTTPS links
  ✓ Reverse-DNS capability names

Overall: PASS (24/24 checks)
```

---

## Sub-command: profile

### Trigger
User runs `/ucp profile`

### Purpose
Generate and display the `/.well-known/ucp` discovery profile JSON.

### Prerequisites
- Config must exist

### Procedure

#### Step 1: Generate Profile
Use the `generateProfile()` function from `lib/ucp/profile.ts` (or generate inline if not scaffolded yet).

#### Step 2: Display Profile
Output the formatted JSON:

```json
{
  "ucp": {
    "version": "2026-01-11",
    "services": {
      "dev.ucp.shopping": {
        "version": "2026-01-11",
        "spec": "https://ucp.dev/spec/services/shopping",
        "rest": {
          "schema": "https://ucp.dev/spec/services/shopping/rest.openapi.json",
          "endpoint": "https://shop.example.com/api/ucp"
        }
      }
    },
    "capabilities": [
      {
        "name": "dev.ucp.shopping.checkout",
        "version": "2026-01-11",
        "spec": "https://ucp.dev/spec/capabilities/checkout",
        "schema": "https://ucp.dev/spec/schemas/shopping/checkout.json"
      }
    ]
  }
}
```

#### Step 3: Offer to Write File
Ask: "Write this to `public/.well-known/ucp` for static serving, or keep as dynamic route?"

If static:
- Create `public/.well-known/ucp` (no extension, JSON content)
- Note: May need Next.js config for extensionless files

---

## Sub-command: test

### Trigger
User runs `/ucp test`

### Purpose
Generate unit tests for UCP handlers.

### Prerequisites
- Implementation must exist
- Test framework detected (Jest, Vitest, etc.)

### Procedure

#### Step 1: Detect Test Framework
Look for:
- `jest.config.js` / `jest.config.ts` → Jest
- `vitest.config.js` / `vitest.config.ts` → Vitest
- `package.json` test script hints

#### Step 2: Generate Test Files
For each handler, generate corresponding test file.

#### Example: lib/ucp/handlers/__tests__/checkout.test.ts
```typescript
/**
 * UCP Checkout Handler Tests
 * Generated by /ucp test
 */

import { describe, it, expect, beforeEach } from 'vitest'; // or jest
import {
  createCheckout,
  getCheckout,
  updateCheckout,
  completeCheckout,
} from '../checkout';

describe('UCP Checkout Handler', () => {
  const validRequest = {
    line_items: [
      {
        id: 'item_1',
        name: 'Test Product',
        quantity: 1,
        unit_price: 1000,
        total_price: 1000,
        currency: 'USD',
      },
    ],
    currency: 'USD',
  };

  describe('createCheckout', () => {
    it('creates a checkout with valid request', async () => {
      const checkout = await createCheckout(validRequest, {
        capabilities: ['dev.ucp.shopping.checkout'],
      });

      expect(checkout.id).toBeDefined();
      expect(checkout.status).toBe('incomplete');
      expect(checkout.currency).toBe('USD');
      expect(checkout.line_items).toHaveLength(1);
      expect(checkout.ucp.version).toBeDefined();
      expect(checkout.ucp.capabilities).toContain('dev.ucp.shopping.checkout');
    });

    it('calculates totals correctly', async () => {
      const checkout = await createCheckout(validRequest, {
        capabilities: ['dev.ucp.shopping.checkout'],
      });

      expect(checkout.totals.subtotal).toBe(1000);
      expect(checkout.totals.grand_total).toBeGreaterThanOrEqual(checkout.totals.subtotal);
    });

    it('sets expiration time', async () => {
      const checkout = await createCheckout(validRequest, {
        capabilities: ['dev.ucp.shopping.checkout'],
      });

      expect(checkout.expires_at).toBeDefined();
      const expiresAt = new Date(checkout.expires_at);
      expect(expiresAt.getTime()).toBeGreaterThan(Date.now());
    });

    it('includes required links', async () => {
      const checkout = await createCheckout(validRequest, {
        capabilities: ['dev.ucp.shopping.checkout'],
      });

      expect(checkout.links.self).toContain(checkout.id);
      expect(checkout.links.privacy_policy).toBeDefined();
      expect(checkout.links.terms_of_service).toBeDefined();
    });
  });

  describe('getCheckout', () => {
    it('retrieves existing checkout', async () => {
      const created = await createCheckout(validRequest, {
        capabilities: ['dev.ucp.shopping.checkout'],
      });

      const retrieved = await getCheckout(created.id);
      expect(retrieved).toEqual(created);
    });

    it('returns null for non-existent checkout', async () => {
      const retrieved = await getCheckout('non-existent-id');
      expect(retrieved).toBeNull();
    });
  });

  describe('updateCheckout', () => {
    it('updates line items', async () => {
      const created = await createCheckout(validRequest, {
        capabilities: ['dev.ucp.shopping.checkout'],
      });

      const updated = await updateCheckout(
        created.id,
        {
          line_items: [
            { ...validRequest.line_items[0], quantity: 2, total_price: 2000 },
          ],
        },
        ['dev.ucp.shopping.checkout']
      );

      expect(updated?.totals.subtotal).toBe(2000);
    });

    it('updates buyer info', async () => {
      const created = await createCheckout(validRequest, {
        capabilities: ['dev.ucp.shopping.checkout'],
      });

      const updated = await updateCheckout(
        created.id,
        { buyer: { email: 'test@example.com' } },
        ['dev.ucp.shopping.checkout']
      );

      expect(updated?.buyer?.email).toBe('test@example.com');
    });

    it('transitions to ready_for_complete when requirements met', async () => {
      const created = await createCheckout(validRequest, {
        capabilities: ['dev.ucp.shopping.checkout'],
      });

      const updated = await updateCheckout(
        created.id,
        { buyer: { email: 'test@example.com' } },
        ['dev.ucp.shopping.checkout']
      );

      expect(updated?.status).toBe('ready_for_complete');
    });
  });

  describe('status lifecycle', () => {
    it('follows correct state transitions', async () => {
      // incomplete -> ready_for_complete -> complete_in_progress -> completed
      const checkout = await createCheckout(validRequest, {
        capabilities: ['dev.ucp.shopping.checkout'],
      });
      expect(checkout.status).toBe('incomplete');

      const updated = await updateCheckout(
        checkout.id,
        { buyer: { email: 'test@example.com' } },
        ['dev.ucp.shopping.checkout']
      );
      expect(updated?.status).toBe('ready_for_complete');
    });
  });
});
```

#### Step 3: Output Summary
```
Generated test files:
  CREATE  lib/ucp/handlers/__tests__/checkout.test.ts
  CREATE  lib/ucp/handlers/__tests__/fulfillment.test.ts
  CREATE  lib/ucp/__tests__/negotiation.test.ts
  CREATE  lib/ucp/__tests__/profile.test.ts
  CREATE  app/api/ucp/__tests__/checkout.route.test.ts

Run tests with: npm test (or bun test)
```

---

## Sub-command: docs

### Trigger
User runs `/ucp docs`

### Purpose
Generate internal documentation for the UCP integration.

### Prerequisites
- Config must exist
- Implementation ideally exists

### Procedure

#### Step 1: Gather Information
- Read config for capabilities, transports, handlers
- Scan generated files
- Read spec files for accurate descriptions

#### Step 2: Generate Documentation

Create `docs/ucp-integration.md`:

```markdown
# UCP Integration Documentation

## Overview

This codebase implements the Universal Commerce Protocol (UCP) version {version}.

**Role:** {role}
**Domain:** {domain}
**Transports:** {transports}

## Capabilities

### Core
- `dev.ucp.shopping.checkout` - Checkout session management

### Extensions
{list extensions with descriptions}

## API Endpoints

### Discovery
- `GET /.well-known/ucp` - UCP discovery profile

### Checkout (REST)
- `POST /api/ucp/checkout` - Create checkout session
- `GET /api/ucp/checkout/:id` - Get checkout session
- `PATCH /api/ucp/checkout/:id` - Update checkout session
- `POST /api/ucp/checkout/:id` (action=complete) - Complete checkout

## Checkout Status Lifecycle

```
incomplete → requires_escalation → ready_for_complete → complete_in_progress → completed
                                                                            ↘ canceled
```

## Payment Handlers

{list configured handlers with integration notes}

## Capability Negotiation

The platform sends their profile URL via `UCP-Agent` header:
```
UCP-Agent: profile="https://platform.example.com/.well-known/ucp"
```

The business fetches the platform profile, computes the capability intersection,
and includes the negotiated capabilities in every response.

## Configuration

Configuration is stored in `ucp.config.json` at the project root.

## Files

{list generated files with descriptions}

## Testing

Run unit tests:
```bash
npm test
```

## Validation

Validate implementation against UCP schemas:
```bash
# Using the skill
/ucp validate
```
```

#### Step 3: Output
```
Generated documentation:
  CREATE  docs/ucp-integration.md

Documentation includes:
  - Capability overview
  - API endpoint reference
  - Status lifecycle diagram
  - Configuration guide
  - File manifest
```

---

## Error Handling

### Interactive Error Resolution
When encountering ambiguous situations, always ask the user:

1. **Missing config:** "Config file not found. Run /ucp init first, or create manually?"
2. **Spec fetch failed:** "Could not clone UCP spec. Check network/auth. Retry, use local path, or abort?"
3. **Conflicting files:** "File {path} already exists. Overwrite, merge, skip, or abort?"
4. **Unknown role:** "Role '{role}' not recognized. Did you mean: business, platform, payment_provider, or host_embedded?"
5. **Validation failure:** "Schema validation failed for {file}. Show details, attempt fix, or skip?"

### Error Codes
| Code | Meaning | Resolution |
|------|---------|------------|
| `CONFIG_NOT_FOUND` | ucp.config.json missing | Run /ucp init |
| `SPEC_NOT_FOUND` | Spec repo not available | Check network, clone manually |
| `INVALID_ROLE` | Unknown role in config | Fix config |
| `SCHEMA_INVALID` | Response doesn't match schema | Review generated code |
| `EDGE_RUNTIME_DETECTED` | Edge runtime used | Change to nodejs/bun |

---

## Next.js Conventions

### File Structure
```
project/
├── app/
│   ├── .well-known/
│   │   └── ucp/
│   │       └── route.ts          # Discovery profile
│   └── api/
│       └── ucp/
│           ├── checkout/
│           │   ├── route.ts      # POST create
│           │   └── [id]/
│           │       └── route.ts  # GET, PATCH, POST complete
│           ├── mcp/
│           │   └── route.ts      # MCP transport (if enabled)
│           └── a2a/
│               └── route.ts      # A2A transport (if enabled)
├── lib/
│   └── ucp/
│       ├── types/
│       │   ├── checkout.ts
│       │   └── index.ts
│       ├── schemas/
│       │   └── checkout.ts
│       ├── handlers/
│       │   ├── checkout.ts
│       │   ├── fulfillment.ts
│       │   ├── discount.ts
│       │   └── payment.ts
│       ├── transports/
│       │   └── mcp.ts
│       ├── profile.ts
│       ├── negotiation.ts
│       └── response.ts
├── docs/
│   └── ucp-integration.md
├── ucp.config.json
└── .ucp-spec/                    # Cloned spec (gitignored)
```

### Runtime Declaration
Every route file must include:
```typescript
export const runtime = 'nodejs'; // Edge runtime is not supported
```

Or for Bun:
```typescript
export const runtime = 'nodejs'; // Bun-compatible Node.js runtime
```

### App Router Patterns
- Use Route Handlers (`route.ts`) not API Routes (`pages/api`)
- Use `NextRequest` and `NextResponse` from `next/server`
- Await `request.json()` for body parsing
- Use `request.headers.get()` for header access

---

## Credential Handling

### Keys Required For
- **AP2 Mandates:** JWS signing key (ES256)
- **Webhook Signing:** JWS signing key (ES256)
- **Identity Linking:** OAuth client credentials

### Prompting for Credentials
When a feature requires credentials, ask:

> "AP2 mandates require a JWS signing key (ES256 recommended).
> Do you have an existing key pair, or should I explain how to generate one?"

If user needs generation instructions:
```bash
# Generate ES256 key pair
openssl ecparam -genkey -name prime256v1 -noout -out private.pem
openssl ec -in private.pem -pubout -out public.pem

# Convert to JWK format (use jose library or online tool)
```

### Storage
Credentials should be stored in environment variables, not in config:
- `UCP_SIGNING_KEY` - Private key (PEM or JWK)
- `UCP_OAUTH_CLIENT_ID` - OAuth client ID
- `UCP_OAUTH_CLIENT_SECRET` - OAuth client secret

---

## Version History

- **2026-01-11**: Initial UCP spec version
- **Skill v1.0**: Initial skill release

---

## References

- UCP Spec Repository: https://github.com/Universal-Commerce-Protocol/ucp.git
- UCP Documentation: See `./ucp/docs/` or `./.ucp-spec/docs/`
- JSON Schema Draft 2020-12
- RFC 8941 (Structured Field Values)
- RFC 3339 (Date/Time Format)
- RFC 8785 (JSON Canonicalization Scheme)
