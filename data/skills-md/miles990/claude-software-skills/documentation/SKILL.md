---
name: documentation
description: Technical writing, API docs, and documentation best practices
domain: software-engineering
version: 1.0.0
tags: [documentation, technical-writing, api-docs, adr, readme, runbooks]
triggers:
  keywords:
    primary: [documentation, docs, readme, api docs, technical writing, wiki]
    secondary: [adr, runbook, changelog, jsdoc, docstring, swagger, typedoc]
  context_boost: [write, explain, onboarding, knowledge]
  context_penalty: [deployment, infrastructure, testing]
  priority: medium
---

# Documentation

## Overview

Documentation as a first-class engineering artifact. Good docs reduce onboarding time, support tickets, and cognitive load.

---

## Documentation Types

| Type | Audience | Purpose | Update Frequency |
|------|----------|---------|------------------|
| README | New developers | Quick start | Per major change |
| API Docs | API consumers | Reference | Per API change |
| Architecture | Team | Design decisions | Per design change |
| Runbooks | Operations | Incident response | Per incident |
| Tutorials | Users | Learning | Periodically |

---

## README Best Practices

### Structure

```markdown
# Project Name

> One-line description of what this project does.

[![Build Status](badge)](link)
[![Coverage](badge)](link)
[![License](badge)](link)

## Features

- Feature 1: Brief description
- Feature 2: Brief description
- Feature 3: Brief description

## Quick Start

```bash
# Install
npm install my-project

# Configure
export API_KEY=your-key

# Run
npx my-project start
```

## Installation

### Prerequisites
- Node.js 18+
- PostgreSQL 15+

### Steps
1. Clone the repository
2. Install dependencies: `npm install`
3. Copy `.env.example` to `.env`
4. Run migrations: `npm run db:migrate`
5. Start the server: `npm start`

## Usage

### Basic Example
```javascript
import { Client } from 'my-project';

const client = new Client({ apiKey: 'xxx' });
const result = await client.doSomething();
```

### Advanced Configuration
[Link to detailed docs]

## API Reference

[Link to API docs]

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT - see [LICENSE](LICENSE)
```

---

## API Documentation

### OpenAPI/Swagger

```yaml
openapi: 3.0.3
info:
  title: User API
  description: |
    API for managing users.

    ## Authentication
    All endpoints require Bearer token authentication.

    ## Rate Limiting
    - 100 requests per minute per API key
    - 429 response when exceeded
  version: 1.0.0

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://staging-api.example.com/v1
    description: Staging

paths:
  /users:
    get:
      summary: List users
      description: Returns a paginated list of users.
      operationId: listUsers
      tags:
        - Users
      parameters:
        - name: limit
          in: query
          description: Maximum number of users to return
          schema:
            type: integer
            default: 20
            maximum: 100
        - name: cursor
          in: query
          description: Pagination cursor from previous response
          schema:
            type: string
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'
              example:
                data:
                  - id: "usr_123"
                    email: "user@example.com"
                    name: "John Doe"
                meta:
                  hasMore: true
                  nextCursor: "eyJpZCI6MTIzfQ"
        '401':
          $ref: '#/components/responses/Unauthorized'

components:
  schemas:
    User:
      type: object
      required:
        - id
        - email
      properties:
        id:
          type: string
          description: Unique identifier
          example: "usr_123"
        email:
          type: string
          format: email
          description: User's email address
        name:
          type: string
          description: User's display name

  responses:
    Unauthorized:
      description: Authentication required
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: string
                example: "Invalid or missing API key"
```

### Code Examples in Docs

```markdown
## Creating a User

### Request

```bash
curl -X POST https://api.example.com/v1/users \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "name": "John Doe"
  }'
```

### Response

```json
{
  "id": "usr_123",
  "email": "user@example.com",
  "name": "John Doe",
  "createdAt": "2024-01-15T10:30:00Z"
}
```

### Error Response

```json
{
  "error": {
    "code": "validation_error",
    "message": "Invalid email format",
    "field": "email"
  }
}
```
```

---

## Architecture Decision Records (ADR)

### Template

```markdown
# ADR-001: Use PostgreSQL for Primary Database

## Status
Accepted

## Context
We need to choose a primary database for our application.
Requirements:
- ACID transactions
- Complex queries with joins
- Proven reliability at scale
- Good ecosystem and tooling

## Decision
We will use PostgreSQL as our primary database.

## Alternatives Considered

### MySQL
- Pros: Widely used, good performance
- Cons: Less feature-rich, weaker JSON support

### MongoDB
- Pros: Flexible schema, easy horizontal scaling
- Cons: No ACID transactions across documents, eventual consistency

### CockroachDB
- Pros: Distributed, PostgreSQL-compatible
- Cons: Higher operational complexity, newer technology

## Consequences

### Positive
- Strong consistency guarantees
- Rich query capabilities (CTEs, window functions)
- Excellent JSON support for semi-structured data
- Large community and ecosystem

### Negative
- Vertical scaling limits
- Need to manage read replicas for high read loads
- Schema migrations require careful planning

### Risks
- May need sharding solution if we exceed single-node capacity
- Team needs PostgreSQL expertise

## References
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Internal benchmark results](link)
```

### ADR Index

```markdown
# Architecture Decision Records

| ID | Title | Status | Date |
|----|-------|--------|------|
| [ADR-001](adr-001.md) | Use PostgreSQL | Accepted | 2024-01-01 |
| [ADR-002](adr-002.md) | JWT Authentication | Accepted | 2024-01-05 |
| [ADR-003](adr-003.md) | Microservices Split | Proposed | 2024-01-10 |
| [ADR-004](adr-004.md) | GraphQL vs REST | Superseded by ADR-006 | 2024-01-15 |
```

---

## Code Documentation

### JSDoc / TSDoc

```typescript
/**
 * Calculates the total price including tax and discounts.
 *
 * @param items - Array of cart items
 * @param options - Calculation options
 * @returns The calculated price breakdown
 *
 * @example
 * ```typescript
 * const result = calculatePrice(
 *   [{ id: '1', price: 100, quantity: 2 }],
 *   { taxRate: 0.1, discountCode: 'SAVE10' }
 * );
 * console.log(result.total); // 198
 * ```
 *
 * @throws {ValidationError} If items array is empty
 * @throws {InvalidDiscountError} If discount code is invalid
 *
 * @see {@link applyDiscount} for discount logic
 * @since 2.0.0
 */
function calculatePrice(
  items: CartItem[],
  options: PriceOptions
): PriceBreakdown {
  // Implementation
}

/**
 * Represents a user in the system.
 *
 * @remarks
 * Users are created through the signup flow or admin panel.
 * Soft deletion is used - check `deletedAt` for active status.
 */
interface User {
  /** Unique identifier (UUID v4) */
  id: string;

  /** Email address (unique, validated format) */
  email: string;

  /**
   * User's display name
   * @defaultValue Derived from email if not provided
   */
  name?: string;

  /** Account creation timestamp */
  createdAt: Date;

  /** Soft deletion timestamp, null if active */
  deletedAt: Date | null;
}
```

### Inline Comments

```typescript
// ✅ Good: Explains WHY
// Use binary search because items are sorted and list can have 100k+ entries
const index = binarySearch(items, target);

// ✅ Good: Explains non-obvious behavior
// Sleep 100ms to avoid rate limiting from external API
await sleep(100);

// ✅ Good: Documents workaround
// HACK: Safari doesn't support this API, fall back to polyfill
// TODO: Remove when Safari 17 adoption > 90%
const result = window.api?.call() ?? polyfill();

// ❌ Bad: States the obvious
// Loop through users
for (const user of users) {

// ❌ Bad: Outdated comment
// Returns user's full name (actually returns email now)
function getUserIdentifier() {
  return user.email;
}
```

---

## Runbooks

### Structure

```markdown
# Runbook: High Memory Usage Alert

## Overview
This runbook addresses alerts when application memory usage exceeds 80%.

## Prerequisites
- Access to Kubernetes cluster
- Permissions to view pods and logs
- Familiarity with application architecture

## Symptoms
- Alert: `HighMemoryUsage` firing
- Metric: `container_memory_usage_bytes` > 80% of limit
- Possible: OOMKilled pods, slow responses

## Diagnosis

### Step 1: Identify affected pods
```bash
kubectl top pods -n production | sort -k3 -rh | head -10
```

### Step 2: Check for memory leaks
```bash
# Get heap dump
kubectl exec -it <pod> -- node --heapsnapshot
kubectl cp <pod>:/app/heapsnapshot.heapsnapshot ./heapsnapshot.heapsnapshot
```

### Step 3: Check recent deployments
```bash
kubectl rollout history deployment/api -n production
```

## Mitigation

### Immediate (if pods are crashing)
```bash
# Scale up to distribute load
kubectl scale deployment/api --replicas=10

# Restart pods (rolling)
kubectl rollout restart deployment/api
```

### If memory leak confirmed
1. Identify the leaking code path from heap snapshot
2. Prepare hotfix
3. Deploy fix following standard process

## Resolution
- Memory usage returns below 70%
- No OOMKilled events for 30 minutes
- Alert auto-resolves

## Escalation
- L1: On-call engineer
- L2: Platform team (if infrastructure issue)
- L3: Application team lead (if code issue)

## Related
- [Memory Profiling Guide](link)
- [Incident INC-123](link) - Previous memory leak
```

---

## Documentation Tools

| Tool | Use Case | Format |
|------|----------|--------|
| Docusaurus | Documentation sites | MDX |
| Swagger UI | API reference | OpenAPI |
| Storybook | Component docs | JSX/TSX |
| MkDocs | Technical docs | Markdown |
| Notion | Team wikis | Rich text |

---

## Related Skills

- [[api-design]] - API documentation
- [[code-quality]] - Self-documenting code
- [[reliability-engineering]] - Runbooks
