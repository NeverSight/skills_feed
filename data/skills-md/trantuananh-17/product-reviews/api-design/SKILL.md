---
name: api-design
description: Use this skill when the user asks to "create an API endpoint", "build a REST API", "add a controller", "design an API", "implement CRUD operations", "add validation", "handle API errors", or any backend API development work. Provides REST API design patterns, response formats, validation, and best practices.
---

# REST API Design (packages/functions)

> For **security patterns**, see `security` skill

## Directory Structure

```
packages/functions/src/
├── routes/              # Route definitions
│   ├── api.js           # Admin API routes
│   ├── restApiV2.js     # Public REST API v2
│   └── apiHookV1.js     # Webhook routes
├── controllers/         # Request handlers
├── middleware/          # Auth, validation, rate limiting
├── validations/         # Yup schemas
└── helpers/
    └── restApiResponse.js  # Response helpers
```

---

## Response Format

### Response Helpers

```javascript
import {
  successResponse,
  errorResponse,
  paginatedResponse,
  itemResponse
} from '../helpers/restApiResponse';

// Single item
ctx.body = itemResponse(customer);

// Paginated list
ctx.body = paginatedResponse(customers, pageInfo, total);

// Error
ctx.status = 400;
ctx.body = errorResponse('Invalid email', 'VALIDATION_ERROR', 400);
```

### Response Structure

| Type | Format |
|------|--------|
| Success | `{success: true, data, meta, timestamp}` |
| Error | `{success: false, error: {message, code, statusCode}, timestamp}` |
| Paginated | `{success: true, data: [], meta: {pagination: {...}}}` |

---

## HTTP Status Codes

| Code | When to Use |
|------|-------------|
| 200 | Successful GET, PUT |
| 201 | Successful POST (created) |
| 204 | Successful DELETE |
| 400 | Validation error, malformed request |
| 401 | Missing/invalid authentication |
| 403 | Authenticated but not authorized |
| 404 | Resource not found |
| 422 | Business logic error |
| 429 | Rate limit exceeded |
| 500 | Server error |

---

## Route Design

### RESTful Conventions

| Action | Method | Route |
|--------|--------|-------|
| List | GET | `/resources` |
| Get one | GET | `/resources/:id` |
| Create | POST | `/resources` |
| Update | PUT | `/resources/:id` |
| Delete | DELETE | `/resources/:id` |
| Action | POST | `/resources/:id/action` |

### Route Organization

```javascript
import Router from 'koa-router';

const router = new Router({prefix: '/api/v2'});

router.use(verifyAuthenticate);
router.use(verifyPlanAccess);

// Resources
router.get('/customers', validateQuery(paginationSchema), getCustomers);
router.get('/customers/:id', getCustomer);
router.post('/customers', validateInput(createSchema), createCustomer);
router.put('/customers/:id', validateInput(updateSchema), updateCustomer);

// Sub-resources
router.get('/customers/:id/rewards', getCustomerRewards);

// Actions
router.post('/customers/:id/points/award', awardPoints);
```

---

## Input Validation

### Yup Schemas

```javascript
import * as Yup from 'yup';

export const createCustomerSchema = Yup.object({
  email: Yup.string().email().required(),
  firstName: Yup.string().max(100).optional(),
  points: Yup.number().positive().optional()
});

export const paginationSchema = Yup.object({
  limit: Yup.number().min(1).max(100).default(20),
  cursor: Yup.string().optional()
});
```

### Validation Middleware

```javascript
export function validateInput(schema) {
  return async (ctx, next) => {
    try {
      ctx.request.body = await schema.validate(ctx.request.body, {
        stripUnknown: true
      });
      await next();
    } catch (error) {
      ctx.status = 400;
      ctx.body = errorResponse(error.message, 'VALIDATION_ERROR', 400);
    }
  };
}
```

---

## Controller Pattern

```javascript
export async function getOne(ctx) {
  try {
    const {shop} = ctx.state;
    const {id} = ctx.params;

    const resource = await repository.getById(shop.id, id);

    if (!resource) {
      ctx.status = 404;
      ctx.body = errorResponse('Not found', 'NOT_FOUND', 404);
      return;
    }

    ctx.body = itemResponse(pick(resource, publicFields));
  } catch (error) {
    console.error('Error:', error);
    ctx.status = 500;
    ctx.body = errorResponse('Server error', 'INTERNAL_ERROR', 500);
  }
}
```

---

## Pagination

### Cursor-Based (Preferred)

```javascript
// Request
GET /api/customers?limit=20&cursor=eyJpZCI6IjEyMyJ9

// Response
{
  "data": [...],
  "meta": {
    "pagination": {
      "hasNext": true,
      "nextCursor": "eyJpZCI6IjE0MyJ9",
      "limit": 20
    }
  }
}
```

---

## Error Codes

| Code | When |
|------|------|
| `UNAUTHORIZED` | Missing/invalid credentials |
| `FORBIDDEN` | No permission |
| `PLAN_RESTRICTED` | Feature not in plan |
| `VALIDATION_ERROR` | Invalid input |
| `NOT_FOUND` | Resource doesn't exist |
| `RATE_LIMITED` | Too many requests |
| `INTERNAL_ERROR` | Server error |

---

## Best Practices

| Do | Don't |
|----|-------|
| Use response helpers | Return raw objects |
| Set correct status codes | Return 200 for errors |
| Validate all inputs | Trust user input |
| Pick response fields | Expose internal fields |
| Scope queries by shopId | Query without shop filter |
| Use cursor pagination | Use offset at scale |

---

## Checklist

```
□ Uses response helpers (successResponse/errorResponse)
□ Correct HTTP status codes
□ Input validated with Yup schema
□ Queries scoped by shopId
□ Response fields picked (no internal data)
□ Error handling with try-catch
□ Rate limiting applied
□ Authentication middleware
```