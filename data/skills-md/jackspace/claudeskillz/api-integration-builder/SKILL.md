---
name: api-integration-builder
description: Generates production-ready API clients with TypeScript types, retry logic, rate limiting, authentication (OAuth, API keys), error handling, and mock responses. Use when user says "integrate API", "API client", "connect to service", or requests third-party service integration.
---

# API Integration Builder

## Purpose

Generates complete, production-ready API clients with all the boilerplate handled: TypeScript types, authentication, retry logic, rate limiting, and error handling.

**For ADHD users**: Instant integration - no need to read API docs and implement everything manually.
**For all users**: Saves hours of boilerplate code, type-safe, production-ready from day one.

## Activation Triggers

- User says: "integrate API", "API client", "connect to service", "create SDK"
- Requests for: Stripe integration, SendGrid, Twilio, any third-party API
- "Set up OAuth" or "implement API authentication"

## Core Workflow

### 1. Gather Requirements

Ask user for:
```javascript
{
  api_name: "Stripe",
  api_base_url: "https://api.stripe.com/v1",
  auth_type: "api_key|oauth|bearer|basic",
  endpoints: [
    { method: "GET", path: "/customers", description: "List customers" },
    { method: "POST", path: "/customers", description: "Create customer" }
  ],
  rate_limit: { requests: 100, per: "minute" } // optional
}
```

**If user provides API documentation URL**, fetch it and extract this information automatically.

### 2. Generate TypeScript Client

**File structure**:
```
api-client/
├── client.ts              # Main client class
├── types.ts               # TypeScript types
├── auth.ts                # Authentication handler
├── errors.ts              # Custom error classes
├── retry.ts               # Retry logic
├── rate-limiter.ts        # Rate limiting
└── mocks.ts               # Mock responses for testing
```

### 3. Client Template

```typescript
// client.ts
import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';
import { AuthHandler } from './auth';
import { RateLimiter } from './rate-limiter';
import { RetryHandler } from './retry';
import { APIError, RateLimitError, AuthenticationError } from './errors';
import type { ClientConfig, APIResponse } from './types';

export class {APIName}Client {
  private axios: AxiosInstance;
  private auth: AuthHandler;
  private rateLimiter: RateLimiter;
  private retryHandler: RetryHandler;

  constructor(config: ClientConfig) {
    this.auth = new AuthHandler(config.apiKey);
    this.rateLimiter = new RateLimiter(config.rateLimit);
    this.retryHandler = new RetryHandler(config.retryConfig);

    this.axios = axios.create({
      baseURL: config.baseURL,
      timeout: config.timeout || 30000,
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': '{APIName}-Client/1.0.0',
        ...config.defaultHeaders,
      },
    });

    // Request interceptor for auth
    this.axios.interceptors.request.use(
      async (config) => {
        await this.rateLimiter.wait();
        return this.auth.addAuthHeaders(config);
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor for retry logic
    this.axios.interceptors.response.use(
      (response) => response,
      async (error) => {
        if (this.retryHandler.shouldRetry(error)) {
          return this.retryHandler.retry(error);
        }
        return Promise.reject(this.handleError(error));
      }
    );
  }

  private handleError(error: any): Error {
    if (error.response?.status === 401) {
      return new AuthenticationError('Invalid API credentials');
    }
    if (error.response?.status === 429) {
      return new RateLimitError('Rate limit exceeded');
    }
    if (error.response?.data?.message) {
      return new APIError(error.response.data.message, error.response.status);
    }
    return new APIError('Unknown API error', error.response?.status);
  }

  // Generated methods for each endpoint
  async listCustomers(params?: ListCustomersParams): Promise<APIResponse<Customer[]>> {
    const response = await this.axios.get('/customers', { params });
    return response.data;
  }

  async createCustomer(data: CreateCustomerData): Promise<APIResponse<Customer>> {
    const response = await this.axios.post('/customers', data);
    return response.data;
  }

  // ... more generated methods
}
```

### 4. Authentication Handler

```typescript
// auth.ts
import { AxiosRequestConfig } from 'axios';

export type AuthConfig =
  | { type: 'api_key'; key: string; header?: string }
  | { type: 'bearer'; token: string }
  | { type: 'oauth'; clientId: string; clientSecret: string; tokenUrl: string }
  | { type: 'basic'; username: string; password: string };

export class AuthHandler {
  private config: AuthConfig;
  private accessToken?: string;
  private tokenExpiry?: Date;

  constructor(config: AuthConfig) {
    this.config = config;
  }

  async addAuthHeaders(axiosConfig: AxiosRequestConfig): Promise<AxiosRequestConfig> {
    const headers = axiosConfig.headers || {};

    switch (this.config.type) {
      case 'api_key':
        headers[this.config.header || 'Authorization'] = `Bearer ${this.config.key}`;
        break;

      case 'bearer':
        headers['Authorization'] = `Bearer ${this.config.token}`;
        break;

      case 'oauth':
        const token = await this.getOAuthToken();
        headers['Authorization'] = `Bearer ${token}`;
        break;

      case 'basic':
        const credentials = Buffer.from(
          `${this.config.username}:${this.config.password}`
        ).toString('base64');
        headers['Authorization'] = `Basic ${credentials}`;
        break;
    }

    return { ...axiosConfig, headers };
  }

  private async getOAuthToken(): Promise<string> {
    // Check if token is still valid
    if (this.accessToken && this.tokenExpiry && this.tokenExpiry > new Date()) {
      return this.accessToken;
    }

    // Fetch new token
    const response = await axios.post(this.config.tokenUrl, {
      grant_type: 'client_credentials',
      client_id: this.config.clientId,
      client_secret: this.config.clientSecret,
    });

    this.accessToken = response.data.access_token;
    this.tokenExpiry = new Date(Date.now() + response.data.expires_in * 1000);

    return this.accessToken;
  }
}
```

### 5. Retry Logic

```typescript
// retry.ts
import { AxiosError, AxiosRequestConfig } from 'axios';

export interface RetryConfig {
  maxRetries: number;
  initialDelay: number; // ms
  maxDelay: number; // ms
  backoffFactor: number;
  retryableStatuses: number[];
}

export class RetryHandler {
  private config: RetryConfig;
  private retryCount: Map<string, number> = new Map();

  constructor(config?: Partial<RetryConfig>) {
    this.config = {
      maxRetries: config?.maxRetries || 3,
      initialDelay: config?.initialDelay || 1000,
      maxDelay: config?.maxDelay || 30000,
      backoffFactor: config?.backoffFactor || 2,
      retryableStatuses: config?.retryableStatuses || [408, 429, 500, 502, 503, 504],
    };
  }

  shouldRetry(error: AxiosError): boolean {
    if (!error.response) return true; // Network error, retry
    if (!this.config.retryableStatuses.includes(error.response.status)) return false;

    const key = this.getRequestKey(error.config);
    const count = this.retryCount.get(key) || 0;

    return count < this.config.maxRetries;
  }

  async retry(error: AxiosError): Promise<any> {
    const key = this.getRequestKey(error.config);
    const count = this.retryCount.get(key) || 0;

    this.retryCount.set(key, count + 1);

    const delay = Math.min(
      this.config.initialDelay * Math.pow(this.config.backoffFactor, count),
      this.config.maxDelay
    );

    await this.sleep(delay);

    return axios.request(error.config);
  }

  private getRequestKey(config: AxiosRequestConfig): string {
    return `${config.method}:${config.url}`;
  }

  private sleep(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}
```

### 6. Rate Limiter

```typescript
// rate-limiter.ts
export interface RateLimitConfig {
  requests: number;
  per: 'second' | 'minute' | 'hour';
}

export class RateLimiter {
  private config: RateLimitConfig;
  private timestamps: number[] = [];

  constructor(config: RateLimitConfig) {
    this.config = config;
  }

  async wait(): Promise<void> {
    const now = Date.now();
    const windowMs = this.getWindowMs();

    // Remove timestamps outside the window
    this.timestamps = this.timestamps.filter((ts) => now - ts < windowMs);

    if (this.timestamps.length >= this.config.requests) {
      const oldestTimestamp = this.timestamps[0];
      const waitTime = oldestTimestamp + windowMs - now;

      if (waitTime > 0) {
        await this.sleep(waitTime);
        return this.wait(); // Recursive call after waiting
      }
    }

    this.timestamps.push(now);
  }

  private getWindowMs(): number {
    switch (this.config.per) {
      case 'second':
        return 1000;
      case 'minute':
        return 60000;
      case 'hour':
        return 3600000;
    }
  }

  private sleep(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}
```

### 7. TypeScript Types

```typescript
// types.ts
export interface ClientConfig {
  baseURL: string;
  apiKey?: string;
  oauthConfig?: OAuthConfig;
  timeout?: number;
  rateLimit?: RateLimitConfig;
  retryConfig?: Partial<RetryConfig>;
  defaultHeaders?: Record<string, string>;
}

export interface OAuthConfig {
  clientId: string;
  clientSecret: string;
  tokenUrl: string;
}

export interface APIResponse<T> {
  data: T;
  status: number;
  headers: Record<string, string>;
}

export interface PaginatedResponse<T> {
  data: T[];
  page: number;
  totalPages: number;
  totalItems: number;
  hasMore: boolean;
}

// Auto-generated types for each API entity
export interface Customer {
  id: string;
  email: string;
  name: string;
  created: number;
  metadata?: Record<string, any>;
}

export interface CreateCustomerData {
  email: string;
  name?: string;
  metadata?: Record<string, any>;
}

export interface ListCustomersParams {
  limit?: number;
  starting_after?: string;
  ending_before?: string;
}
```

### 8. Custom Errors

```typescript
// errors.ts
export class APIError extends Error {
  constructor(
    message: string,
    public statusCode?: number,
    public response?: any
  ) {
    super(message);
    this.name = 'APIError';
  }
}

export class AuthenticationError extends APIError {
  constructor(message: string) {
    super(message, 401);
    this.name = 'AuthenticationError';
  }
}

export class RateLimitError extends APIError {
  constructor(message: string, public retryAfter?: number) {
    super(message, 429);
    this.name = 'RateLimitError';
  }
}

export class ValidationError extends APIError {
  constructor(message: string, public fields?: Record<string, string[]>) {
    super(message, 400);
    this.name = 'ValidationError';
  }
}
```

### 9. Mock Responses (for Testing)

```typescript
// mocks.ts
export const mockCustomers: Customer[] = [
  {
    id: 'cus_test123',
    email: 'test@example.com',
    name: 'Test User',
    created: Date.now(),
  },
];

export const mockResponses = {
  'GET /customers': {
    data: mockCustomers,
    status: 200,
  },
  'POST /customers': {
    data: mockCustomers[0],
    status: 201,
  },
};

export class Mock{APIName}Client {
  async listCustomers(): Promise<APIResponse<Customer[]>> {
    return mockResponses['GET /customers'];
  }

  async createCustomer(data: CreateCustomerData): Promise<APIResponse<Customer>> {
    return mockResponses['POST /customers'];
  }
}
```

## Additional Features

### Webhook Handling

```typescript
// webhooks.ts
import crypto from 'crypto';

export class WebhookHandler {
  constructor(private secret: string) {}

  verify(payload: string, signature: string): boolean {
    const hmac = crypto.createHmac('sha256', this.secret);
    const digest = hmac.update(payload).digest('hex');
    return crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(digest));
  }

  parse<T>(payload: string, signature: string): T {
    if (!this.verify(payload, signature)) {
      throw new Error('Invalid webhook signature');
    }
    return JSON.parse(payload);
  }
}
```

### Pagination Helper

```typescript
// pagination.ts
export class PaginationHelper<T> {
  constructor(
    private client: any,
    private endpoint: string,
    private pageSize: number = 100
  ) {}

  async *iterate(params?: any): AsyncGenerator<T> {
    let hasMore = true;
    let startingAfter: string | undefined;

    while (hasMore) {
      const response = await this.client[this.endpoint]({
        ...params,
        limit: this.pageSize,
        starting_after: startingAfter,
      });

      for (const item of response.data) {
        yield item;
      }

      hasMore = response.has_more;
      if (hasMore && response.data.length > 0) {
        startingAfter = response.data[response.data.length - 1].id;
      }
    }
  }

  async all(params?: any): Promise<T[]> {
    const items: T[] = [];
    for await (const item of this.iterate(params)) {
      items.push(item);
    }
    return items;
  }
}
```

## Usage Examples

See [examples.md](examples.md) for complete integration examples including:
- Stripe API client
- SendGrid email integration
- GitHub API client
- Custom REST API
- GraphQL API client

## Delivery Format

**Generated files**:
1. Complete TypeScript API client
2. README with usage examples
3. Test file with mock examples
4. Package.json with dependencies

**Dependencies included**:
```json
{
  "dependencies": {
    "axios": "^1.5.0"
  },
  "devDependencies": {
    "typescript": "^5.2.0",
    "@types/node": "^20.8.0",
    "jest": "^29.7.0",
    "@types/jest": "^29.5.0"
  }
}
```

**Notify user**:
```
✅ **{API Name} Client** generated!

**Features:**
- ✅ TypeScript types
- ✅ {Auth type} authentication
- ✅ Automatic retries (up to 3x)
- ✅ Rate limiting ({X} requests per {Y})
- ✅ Error handling
- ✅ Mock responses for testing

**Generated files:**
- client.ts (main client)
- types.ts (TypeScript definitions)
- auth.ts (authentication)
- mocks.ts (test mocks)

**Usage:**
```typescript
import { {APIName}Client } from './client';

const client = new {APIName}Client({
  baseURL: '{API_URL}',
  apiKey: process.env.API_KEY,
  rateLimit: { requests: 100, per: 'minute' }
});

const customers = await client.listCustomers();
```

**Next steps:**
1. Install dependencies: `npm install`
2. Set API key in .env
3. Import and use the client
```

## Integration with Other Skills

### Context Manager
Save API integration details:
```
remember: Integrated Stripe API
Type: PROCEDURE
Tags: api, stripe, payments, typescript
Content: Stripe client with retry logic, rate limiting (100/min),
         webhook verification implemented
```

### Error Debugger
If API integration has issues:
```
Automatically invokes error-debugger for:
- Authentication failures
- Rate limit errors
- Network timeouts
```

### Rapid Prototyper
For testing integration:
```
rapid-prototyper generates test server
→ Mock API responses for development
```

## Quality Checklist

Before delivering, verify:
- ✅ TypeScript types for all endpoints
- ✅ Authentication implemented correctly
- ✅ Retry logic with exponential backoff
- ✅ Rate limiting configured
- ✅ Custom error classes
- ✅ Mock responses for testing
- ✅ README with usage examples
- ✅ No hardcoded secrets

## Success Criteria

✅ Generated client compiles without errors
✅ All endpoints have TypeScript types
✅ Authentication works
✅ Retries happen automatically
✅ Rate limiting prevents 429 errors
✅ Errors are properly caught and typed
✅ Mock client available for testing
✅ Production-ready code

## Additional Resources

- **[Integration Examples](examples.md)** - Complete API client examples
- **[Reference Patterns](reference.md)** - Common API patterns and best practices

## Quick Reference

### Trigger Phrases
- "integrate API"
- "API client"
- "connect to service"
- "create SDK"
- "Stripe integration"
- "OAuth setup"

### Supported Auth Types
- API Key (Bearer, Custom Header)
- OAuth 2.0 (Client Credentials, Authorization Code)
- Basic Auth
- Custom (user provides implementation)

### Output Location
- Linux/macOS: `~/.claude-artifacts/api-client-{name}-{timestamp}/`
- Windows: `%USERPROFILE%\.claude-artifacts\api-client-{name}-{timestamp}\`
