---
name: rest-conventions
description: Use when designing API endpoints. Use when using wrong HTTP methods. Use when POST is used for reads.
---

# REST Conventions

## Overview

**Use HTTP methods correctly. GET for reads. POST for creates. PUT/PATCH for updates. DELETE for deletes.**

REST conventions exist for caching, bookmarking, and semantic clarity. Violating them breaks HTTP infrastructure.

## When to Use

- Designing any HTTP API endpoint
- Asked to use POST for fetching data
- Naming endpoints with verbs
- Unsure which HTTP method to use

## The Iron Rule

```
NEVER use POST for read operations. NEVER put verbs in URLs.
```

**No exceptions:**
- Not for "it's simpler"
- Not for "we need a body"
- Not for "that's how we do it"
- Not for "GET URLs are limited"

## Detection: REST Violation Smell

If endpoints have verbs or wrong methods, STOP:

```typescript
// ❌ VIOLATIONS
POST /getOrders              // POST for read
POST /users/create           // Verb in URL
GET /deleteUser?id=123       // GET for delete
POST /api/fetchProducts      // Verb + wrong method
```

## The Correct Pattern: RESTful Endpoints

```typescript
// ✅ CORRECT: RESTful design

// Collections: plural nouns
GET    /users          // List users
POST   /users          // Create user
GET    /users/:id      // Get one user
PUT    /users/:id      // Replace user
PATCH  /users/:id      // Update user partially
DELETE /users/:id      // Delete user

// Nested resources
GET    /users/:id/orders     // User's orders
POST   /users/:id/orders     // Create order for user
GET    /orders/:id           // Get specific order

// Filtering via query params
GET    /orders?status=pending&userId=123
GET    /products?category=electronics&limit=20
```

## HTTP Methods Semantics

| Method | Use For | Idempotent | Safe |
|--------|---------|------------|------|
| GET | Read/fetch | Yes | Yes |
| POST | Create | No | No |
| PUT | Replace entirely | Yes | No |
| PATCH | Partial update | Yes | No |
| DELETE | Remove | Yes | No |

**Safe**: Doesn't modify state
**Idempotent**: Same result if called multiple times

## Common Patterns

### Filtering
```typescript
GET /orders?status=pending
GET /products?minPrice=10&maxPrice=100
GET /users?role=admin&active=true
```

### Pagination
```typescript
GET /orders?page=2&limit=20
GET /orders?cursor=abc123&limit=20
```

### Sorting
```typescript
GET /products?sort=price:asc
GET /users?sort=createdAt:desc
```

### Actions on Resources
For actions that don't fit CRUD, use sub-resources:
```typescript
POST /orders/:id/cancel     // Action on order
POST /users/:id/verify      // Action on user
POST /payments/:id/refund   // Action on payment
```

## Pressure Resistance Protocol

### 1. "POST Is Simpler"
**Pressure:** "Just use POST for everything"

**Response:** POST requests aren't cacheable and break HTTP semantics.

**Action:** Use the correct method. It's the same amount of code.

### 2. "We Need a Request Body"
**Pressure:** "GET can't have a body, so we use POST"

**Response:** Use query parameters for filtering. Bodies on GET are non-standard.

**Action:** `GET /orders?userId=123` instead of `POST /getOrders`

### 3. "GET URLs Are Limited"
**Pressure:** "Query string might get too long"

**Response:** If your query is that complex, you might need a search endpoint. Or paginate.

**Action:** For complex searches, `POST /search` is acceptable as an exception.

### 4. "That's How We Do It"
**Pressure:** "Our existing API uses POST for reads"

**Response:** New endpoints should follow conventions. Migrate old ones gradually.

**Action:** Follow REST for new endpoints. Document inconsistencies.

## Red Flags - STOP and Reconsider

- Verbs in URLs (`/getUser`, `/createOrder`)
- POST for fetching data
- GET for mutations
- Action names instead of resources
- Inconsistent URL structure

**All of these mean: Redesign the endpoint.**

## Quick Reference

| Bad | Good |
|-----|------|
| `POST /getOrders` | `GET /orders` |
| `POST /createUser` | `POST /users` |
| `GET /deleteUser/123` | `DELETE /users/123` |
| `POST /updateProduct` | `PATCH /products/:id` |
| `POST /fetchByFilter` | `GET /items?filter=x` |

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "POST is simpler" | Same code, better semantics. |
| "Need request body" | Use query parameters. |
| "GET URLs too long" | Paginate or use search endpoint. |
| "That's how we do it" | New code should be correct. |
| "Doesn't matter" | Caching, bookmarking, tools all depend on it. |

## The Bottom Line

**Nouns in URLs. Correct HTTP methods. Query params for filtering.**

GET reads. POST creates. PUT/PATCH updates. DELETE removes. URLs are nouns (resources), not verbs (actions).
