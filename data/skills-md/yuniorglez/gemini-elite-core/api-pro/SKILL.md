---
name: api-pro
description: Expert in integrating third-party APIs with proper authentication, error handling, rate limiting, and retry logic. Specializes in Auth.js v5, GPT-5 model orchestration, Stripe SDK v13+, and architectural context packing for large codebases. Optimized for 2026 standards with Edge-first performance and autonomous agent integration.
---

# API Integration Specialist (v2026.1)

Expert guidance for integrating external APIs and LLMs into modern applications with production-ready patterns, security best practices, and autonomous agent capabilities.

## 1. Executive Summary: The 2026 Standard

As of January 2026, API integration has shifted from simple REST calls to **Autonomous Orchestration**. Systems must now support:
- **Edge-First Execution**: Minimum latency via Vercel Edge/Cloudflare Workers.
- **Agentic Logic**: Integration with the GPT-5 family for complex reasoning.
- **Context-Aware Architecture**: Using tools like Repomix to provide full repository context to AI agents.
- **High-Velocity Authentication**: Migrating to Auth.js v5 for 25% faster session handling.

## 2. Core Integration Pillars

### 2.1 Authentication & Security (Auth.js v5)

The gold standard for 2026 is **Auth.js v5**, which provides a unified, secret-first approach optimized for the Edge.

#### The `AUTH_` Prefix Standard
All environment variables MUST now use the `AUTH_` prefix for automatic discovery by the framework. This ensures that the framework can securely handle these variables across different environments (Preview, Staging, Production) without manual mapping in your code.

```bash
# .env.local
AUTH_SECRET=your_signing_secret_here  # REQUIRED: Used for JWT signing
AUTH_URL=https://myapp.com/api/auth   # Base URL for the auth system
AUTH_GOOGLE_ID=google_client_id        # Provider specific
AUTH_GOOGLE_SECRET=google_client_secret
AUTH_GITHUB_ID=github_client_id
AUTH_GITHUB_SECRET=github_client_secret
```

#### Edge-Compatible Configuration
The configuration is designed to be lightweight. Heavy database adapters should be used sparingly in the main configuration file to ensure the Edge middleware remains performant.

```typescript
// auth.ts
import NextAuth from "next-auth"
import Google from "next-auth/providers/google"

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [Google],
  // 2026 Best Practice: Use JWT strategy for stateless, Edge-compatible sessions
  session: { strategy: "jwt" }, 
  pages: {
    signIn: "/auth/signin",
    error: "/auth/error",
  },
  callbacks: {
    async jwt({ token, user, account }) {
      // Persist the OAuth access_token to the token right after signin
      if (account && user) {
        token.accessToken = account.access_token;
        token.id = user.id;
      }
      return token;
    },
    async session({ session, token }) {
      // Send properties to the client, like an access_token from a provider.
      session.accessToken = token.accessToken as string;
      session.user.id = token.id as string;
      return session;
    },
    // The authorized callback is used to verify if the request is authorized via Next.js Middleware.
    authorized({ auth, request: { nextUrl } }) {
      const isLoggedIn = !!auth?.user
      const isApiRoute = nextUrl.pathname.startsWith("/api")
      const isPublicPath = nextUrl.pathname === "/public"
      
      if (isApiRoute && !isLoggedIn) return false
      if (isPublicPath) return true
      
      return isLoggedIn
    },
  },
})
```

#### Performance Gains
- **25% Faster Sessions**: v5 reduces database lookups by caching JWTs aggressively.
- **Edge Runtime**: Full support for `middleware.ts` without Node.js polyfills, reducing cold starts to < 100ms.

### 2.2 AI & Model Orchestration (GPT-5 & o3)

Integrating the **GPT-5 family** requires understanding "Reasoning Tokens" and autonomous agent loops.

#### GPT-5 Reasoning Integration
GPT-5 models use "internal thought processes" before emitting tokens. This requires a different approach to timeouts and token limits.

```typescript
import { generateText } from "ai"
import { gpt5 } from "@ai-sdk/openai"

/**
 * Executes a complex task using GPT-5 Reasoning.
 * reasoningTokens: Specifies the intensity of the "thought" process.
 */
async function executeAutonomousTask(goal: string) {
  // 1. Planning with GPT-5 Reasoning
  const plan = await generateText({
    model: gpt5("gpt-5-reasoning"),
    system: "You are a master architect. Plan the solution step-by-step.",
    prompt: goal,
    // Higher maxTokens for the "thought" process (RT - Reasoning Tokens)
    maxTokens: 8000 
  })

  console.log("GPT-5 Thought Process Completed. Executing Plan...");

  // 2. Execution with specialised sub-agents
  const result = await processPlanSteps(plan.text)
  return result
}
```

#### o3-deep-research for Autonomous Data Gathering
The o3 model is designed for long-running, iterative research.

```typescript
import { o3 } from "@ai-sdk/research"

/**
 * Conducts iterative deep research on a codebase or technical topic.
 */
const researchAgent = async (topic: string) => {
  const deepResearch = await o3.conductResearch({
    query: topic,
    maxDepth: 10,
    allowedTools: ["search", "arxiv", "github", "file_reader"],
    autonomousMode: true,
    // Reporting interval for progress updates
    onProgress: (update) => {
      console.log(`[Research Progress]: ${update.message}`);
    }
  })
  
  return deepResearch.summary
}
```

### 2.3 Financial Engineering (Stripe SDK v13+)

Stripe SDK v13+ introduces native auto-pagination and expanded object types with deep TypeScript support.

#### Auto-Pagination Example
Gone are the days of manual limit/starting_after loops.

```typescript
import Stripe from 'stripe';
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2025-10-14', // Ensure 2026 compatibility
});

async function cleanupStaleSubscriptions() {
  // list() returns an auto-paging iterable
  const subscriptions = stripe.subscriptions.list({
    status: 'past_due',
    limit: 100, // Still use limit for request chunking
  });

  // Native async iterator handles cursors automatically
  for await (const sub of subscriptions) {
    console.log(`Processing sub: ${sub.id}`);
    
    // Check if sub is older than 30 days
    const thirtyDaysAgo = Math.floor(Date.now() / 1000) - (30 * 24 * 60 * 60);
    if (sub.created < thirtyDaysAgo) {
      console.log(`Cancelling sub: ${sub.id} for customer ${sub.customer}`);
      await stripe.subscriptions.cancel(sub.id);
    }
  }
}
```

#### Expanded Objects with Type Safety
```typescript
/**
 * Retrieve a payment intent with full customer and payment method details.
 * The SDK automatically types the expanded fields.
 */
const paymentIntent = await stripe.paymentIntents.retrieve('pi_123', {
  expand: ['customer', 'payment_method'],
});

// Accessing expanded data safely with type narrowing
if (paymentIntent.customer && typeof paymentIntent.customer !== 'string') {
  console.log(`Customer Email: ${paymentIntent.customer.email}`);
}
```

## 3. Architectural Excellence

### 3.1 Monorepo Strategy (Bun & pnpm)

Modern 2026 projects use **Bun** for execution speed and **pnpm** for strict dependency management.

#### Bun Workspace Configuration (`package.json`)
```json
{
  "name": "squaads-monorepo",
  "workspaces": [
    "apps/*",
    "packages/*",
    "skills/*",
    "agents/*"
  ],
  "scripts": {
    "dev": "bun --filter \"*\" dev",
    "test": "bun test --recursive",
    "build": "bun x tsc --noEmit && bun run build:all"
  }
}
```

#### pnpm for Dependency Integrity
```bash
# Ensure no phantom dependencies
pnpm install --frozen-lockfile
# Run a command in all packages
pnpm -r exec bun run lint
```

### 3.2 Context Packing (Repomix)

To enable AI agents (like Gemini CLI) to understand the codebase, we use **Repomix** to pack context into a single, structured file.

```bash
# Generate context for GPT-5 or o3 models
# This includes all logic while excluding noise
bun x repomix --include "src/**/*.ts,lib/**/*.ts,package.json" \
              --exclude "node_modules,dist,.next,tests" \
              --output codebase-summary.md
```

### 3.3 Large Codebase Indexing (The "Archive" Pattern)

When the codebase exceeds 50,000 lines, context packing becomes too large. We implement **Context Indexing**.

```typescript
// scripts/generate-index.ts
import { glob } from "bun";

/**
 * Generates a lightweight index of all functions and classes.
 * This file is what the agent reads first to "know where to look".
 */
async function generateIndex() {
  const files = glob.scan("src/**/*.ts");
  const index = [];

  for await (const file of files) {
    const content = await Bun.file(file).text();
    const matches = content.matchAll(/(export (class|function|interface) (\w+))/g);
    for (const match of matches) {
      index.push({ symbol: match[3], type: match[2], path: file });
    }
  }

  await Bun.write("CODEBASE_INDEX.json", JSON.stringify(index, null, 2));
}
```

## 4. Resilience & Implementation Patterns

### 4.1 Exponential Backoff & Circuit Breaker

Preventing "Retry Cascades" is critical in distributed systems.

```typescript
import { CircuitBreaker } from 'opossum';

/**
 * Standard API Fetcher with integrated Resilience.
 */
const apiCall = async (endpoint: string) => {
  const response = await fetch(endpoint, {
    signal: AbortSignal.timeout(5000) // Hard 5s timeout
  });
  
  if (!response.ok) {
    if (response.status === 429) throw new Error('RATE_LIMITED');
    throw new Error(`API_ERROR_${response.status}`);
  }
  return response.json();
};

const breaker = new CircuitBreaker(apiCall, {
  timeout: 6000,
  errorThresholdPercentage: 50, // Open circuit if 50% calls fail
  resetTimeout: 30000, // Wait 30s before trying again
  capacity: 10 // Max 10 concurrent requests
});

breaker.on('open', () => console.error('!!! CIRCUIT BREAKER OPEN - FAILING FAST !!!'));
breaker.fallback(() => ({ status: 'unavailable', cached: true, data: [] }));

async function fetchWithResilience(url: string) {
  try {
    return await breaker.fire(url);
  } catch (err) {
    console.log("Handled Error via Circuit Breaker Fallback");
    return breaker.fallback();
  }
}
```

### 4.2 Webhook Signature Verification (Edge Ready)

Verification must be fast and secure. We use `crypto.subtle` for Web-native performance.

```typescript
/**
 * Verifies a webhook signature using Web Crypto API.
 * Optimized for Vercel Edge / Cloudflare Workers.
 */
async function verifySignature(payload: string, signature: string, secret: string) {
  const encoder = new TextEncoder();
  const key = await crypto.subtle.importKey(
    'raw',
    encoder.encode(secret),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['verify']
  );

  const verified = await crypto.subtle.verify(
    'HMAC',
    key,
    hexToBytes(signature),
    encoder.encode(payload)
  );

  return verified;
}

function hexToBytes(hex: string) {
  const bytes = new Uint8Array(hex.length / 2);
  for (let i = 0; i < hex.length; i += 2) {
    bytes[i / 2] = parseInt(hex.substr(i, 2), 16);
  }
  return bytes;
}
```

### 4.3 Bulkheading & Load Shedding

Bulkheading isolates different parts of the system so a failure in one doesn't bring down others.

```typescript
// Use separate client instances for different API services
const billingClient = new APIClient({ timeout: 2000, maxConnections: 5 });
const searchClient = new APIClient({ timeout: 10000, maxConnections: 20 });

// If searchClient hangs, billingClient remains responsive.
```

## 5. Large Codebase Search & Fast Navigation

When working with massive repositories, standard `grep` is insufficient.

### 5.1 Git Grep (The Speed King)
Leverage the git index for searches that are 10x faster than standard grep.

```bash
# Find all occurrences of AUTH_SECRET in the src directory
git grep "AUTH_SECRET" -- src/

# Find where a specific function is used across the whole repo
git grep -w "calculateTotal"
```

### 5.2 Advanced Grep with Pattern Files
Use a file containing hundreds of patterns to scan for specific vulnerabilities or deprecated APIs.

```bash
# patterns.txt
dangerouslySetInnerHTML
process.env.SECRET
eval\(
# Run search
grep -f patterns.txt -r ./src
```

## 6. Multi-Model Orchestration (Advanced Agentic Patterns)

In 2026, we rarely use a single model. We orchestrate.

```typescript
/**
 * Orchestrator: Uses GPT-5 for Planning and o3 for execution.
 */
class AgentOrchestrator {
  async runMission(task: string) {
    // 1. Plan with GPT-5 (Reasoning)
    const plan = await gpt5.generatePlan(task);
    
    // 2. Execute Research steps with o3
    for (const step of plan.researchSteps) {
      const data = await o3.deepResearch(step.query);
      this.updateKnowledge(data);
    }
    
    // 3. Final synthesis with GPT-5
    return gpt5.synthesize(this.knowledgeBase);
  }
}
```

## 7. The "Do Not" List (Common Anti-Patterns)

1.  **DO NOT** store API keys in the code. Use `AUTH_` prefixed environment variables for Auth.js.
2.  **DO NOT** use `any` for API responses. Use `zod` to validate and type all incoming data. This is the #1 cause of runtime crashes in 2026.
3.  **DO NOT** perform heavy processing in Webhook handlers. Acknowledge the receipt (200 OK) and queue the work (e.g., using Inngest or BullMQ).
4.  **DO NOT** use standard Node.js `http` modules in Edge functions. Use the `fetch` API exclusively.
5.  **DO NOT** assume API availability. Always implement timeouts and circuit breakers.
6.  **DO NOT** expose internal database IDs (e.g., `user_id: 123`). Use UUIDs or ULIDs for public-facing API resources to prevent enumeration attacks.
7.  **DO NOT** ignore rate limit headers (`X-RateLimit-Remaining`). Implement client-side throttling to stay within limits and avoid 429 penalties.
8.  **DO NOT** use synchronous libraries (like `fs.readFileSync`) in API routes. Always use async equivalents.
9.  **DO NOT** commit the `codebase-context.md` generated by Repomix to git. Add it to `.gitignore`.
10. **DO NOT** hardcode API versions in strings. Use a central configuration object.

## 8. Reference Directory Map

| File | Description |
| :--- | :--- |
| `references/auth-next.md` | Deep dive into Auth.js v5 and Edge integration. |
| `references/ai-agents.md` | GPT-5 family and o3-deep-research agentic patterns. |
| `references/stripe-v13.md` | Stripe SDK v13+ features (auto-pagination, etc.). |
| `references/architect-archive.md` | Repomix context packing and large codebase indexing. |
| `references/resilience.md` | Advanced retry strategies and circuit breakers. |
| `references/nextjs-integration.md` | Patterns for Next.js 16 Server Components & Actions. |

## 9. Troubleshooting Guide

### 9.1 Authentication Failures
- **Symptom**: "Invalid CSRF Token" in Auth.js.
- **Fix**: Ensure `AUTH_URL` matches the request origin exactly. In Vercel, use `AUTH_URL=${VERCEL_URL}`.
- **Check**: Verify `AUTH_SECRET` is at least 32 characters long.

### 9.2 AI Hallucinations in API Calls
- **Symptom**: GPT-5 generating invalid API parameters.
- **Fix**: Provide the agent with the specific `zod` schema or the Stripe SDK TypeScript definitions in the context.
- **Technique**: Use "Few-Shot" examples in the system prompt.

### 9.3 Rate Limit Cascades
- **Symptom**: One service failing causes all upstream services to crash.
- **Fix**: Implement the Circuit Breaker pattern (see Section 4.1) to fail fast and provide cached fallbacks.

## 10. API Client Boilerplate (2026 Edition)

```typescript
import { z } from 'zod';

const UserSchema = z.object({
  id: z.string().uuid(),
  name: z.string(),
  email: z.string().email(),
  tier: z.enum(['free', 'pro', 'enterprise']),
});

type User = z.infer<typeof UserSchema>;

/**
 * Standard API Client with Validation and Logging.
 */
export class SecureAPIClient {
  private baseURL: string;
  private apiKey: string;

  constructor() {
    this.baseURL = process.env.API_BASE_URL!;
    this.apiKey = process.env.API_SECRET_KEY!;
    
    if (!this.apiKey) throw new Error("CRITICAL: API_SECRET_KEY is missing");
  }

  private async request<T>(endpoint: string, schema: z.ZodSchema<T>, options: RequestInit = {}): Promise<T> {
    const startTime = Date.now();
    
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      ...options,
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json',
        'X-Client-Version': '2026.1.0',
        ...options.headers,
      },
    });

    const duration = Date.now() - startTime;
    console.log(`[API] ${options.method || 'GET'} ${endpoint} - ${response.status} (${duration}ms)`);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(`API Request Failed: ${response.status} - ${JSON.stringify(errorData)}`);
    }

    const data = await response.json();
    
    // Validate at the boundary - 2026 Mandatory Rule
    const result = schema.safeParse(data);
    if (!result.success) {
      console.error("[SCHEMA_VALIDATION_ERROR]", result.error);
      throw new Error("API returned invalid data format");
    }
    
    return result.data;
  }

  async getUser(id: string): Promise<User> {
    return this.request(`/users/${id}`, UserSchema);
  }
}
```

## 11. Production Readiness Checklist (2026)

| Category | Requirement | Done? |
| :--- | :--- | :--- |
| **Security** | Auth.js v5 implemented with `AUTH_` prefix? | [ ] |
| **Security** | Webhook signatures verified using `crypto.subtle`? | [ ] |
| **Resilience** | Circuit Breakers active for all 3rd party SDKs? | [ ] |
| **Performance** | API routes marked as `runtime: 'edge'` where possible? | [ ] |
| **Observability** | Request/Response duration logged with Correlation IDs? | [ ] |
| **AI Readiness** | Repomix config updated to exclude `.env` and `dist`? | [ ] |
| **Types** | Zod schemas exist for every API entry/exit point? | [ ] |
| **Financial** | Stripe auto-pagination used for all bulk syncs? | [ ] |

## 12. Conclusion

Mastering API integration in 2026 requires a shift from manual coding to **Architectural Orchestration**. By leveraging Auth.js v5, GPT-5's reasoning capabilities, and the robust Stripe v13 SDK, developers can build systems that are not only faster but also more autonomous and resilient.

Always prioritize **Context Packing** via Repomix to ensure your AI agents have the clarity they need to assist in complex refactors and debugging sessions.

---

### Integration with other Skills
- **next16-expert**: Combine with `auth-next.md` for secure Server Actions.
- **db-enforcer**: Use for ensuring schema alignment between API models and DB.
- **debug-master**: Utilize trace-based debugging for failed API calls.

*Updated: January 22, 2026 - 15:20*
