---
name: validation
description: Validate data with JSON Schema and AJV. Use when validating API requests, form submissions, database inputs, or any data boundaries. Provides deterministic validation with consistent error formats.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# JSON Schema Validation Skill

Validate data at all boundaries using JSON Schema definitions with AJV runtime validation.

---

## When to Use

- Creating API endpoints that accept user input
- Validating form submissions server-side
- Ensuring data integrity before database writes
- Defining contracts between services
- Generating TypeScript types from schemas

---

## Schema File Location

Schemas live in `/schemas/` directory with this structure:

```
schemas/
  common/                    # Shared/reusable schemas
    uuid.schema.json
    error-response.schema.json
    pagination.schema.json
  entities/                  # Domain entity schemas
    user.schema.json         # Full entity
    user.create.schema.json  # Create input (no id/timestamps)
    user.update.schema.json  # Partial update (all optional)
  api/                       # API-specific request schemas
    login.schema.json
    register.schema.json
```

---

## Schema Naming Convention

| Pattern | Example | Purpose |
|---------|---------|---------|
| `{entity}.schema.json` | `user.schema.json` | Full entity with all fields |
| `{entity}.create.schema.json` | `user.create.schema.json` | Create input (no id, no timestamps) |
| `{entity}.update.schema.json` | `user.update.schema.json` | Partial update (all fields optional) |
| `{context}.schema.json` | `login.schema.json` | Context-specific schemas |

---

## Schema Authoring

### Basic Schema Template

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "entities/user.create",
  "title": "Create User",
  "description": "Schema for creating a new user",
  "type": "object",
  "required": ["email", "password"],
  "properties": {
    "email": {
      "type": "string",
      "format": "email",
      "maxLength": 254,
      "description": "User's email address"
    },
    "password": {
      "type": "string",
      "minLength": 8,
      "maxLength": 128,
      "description": "User's password (8-128 characters)"
    },
    "name": {
      "type": "string",
      "minLength": 1,
      "maxLength": 100,
      "description": "User's display name"
    }
  },
  "additionalProperties": false
}
```

### Key Attributes

| Attribute | Purpose |
|-----------|---------|
| `$id` | Unique identifier for referencing (e.g., "entities/user.create") |
| `required` | Array of mandatory field names |
| `additionalProperties: false` | Reject unknown fields (security) |
| `minProperties: 1` | For update schemas - require at least one field |

### Common Validation Keywords

**String Validation:**
```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 255,
  "pattern": "^[a-z0-9-]+$",
  "format": "email"
}
```

**Number Validation:**
```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 100,
  "default": 20
}
```

**Enum Validation:**
```json
{
  "type": "string",
  "enum": ["draft", "active", "archived"],
  "default": "draft"
}
```

**Nullable Fields:**
```json
{
  "type": ["string", "null"],
  "maxLength": 2000
}
```

### Available Formats

AJV with `ajv-formats` supports:
- `email` - Email address
- `uri` - Full URI
- `uuid` - UUID v4
- `date` - ISO date (YYYY-MM-DD)
- `date-time` - ISO datetime
- `time` - ISO time
- `ipv4`, `ipv6` - IP addresses
- `hostname` - Hostname

Custom formats (defined in validator.js):
- `phone` - E.164 phone format (+1234567890)
- `slug` - URL-safe identifier (lowercase, hyphens)

---

## Using Validation Middleware

### Import and Apply

```javascript
import { validateBody, validateQuery, validateParams } from './middleware/validate.js';

// Validate request body
app.post('/api/users',
  validateBody('entities/user.create'),
  createUser
);

// Validate query parameters
app.get('/api/items',
  validateQuery('api/list-items'),
  listItems
);

// Validate path parameters
app.get('/api/users/:id',
  validateParams('common/uuid-param'),
  getUser
);

// Combined validation
app.patch('/api/users/:id',
  validateParams('common/uuid-param'),
  validateBody('entities/user.update'),
  updateUser
);
```

### Error Response Format

Validation failures return:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {
        "path": "/email",
        "message": "Invalid email format",
        "keyword": "format"
      },
      {
        "path": "/password",
        "message": "Must be at least 8 characters",
        "keyword": "minLength"
      }
    ]
  }
}
```

Status codes:
- `422` - Body validation failed
- `400` - Query or params validation failed

---

## Validating in Services

For validation outside middleware (e.g., before database writes):

```javascript
import { validate } from '../api/middleware/validate.js';

async function createUser(data) {
  // Validate before database insert (defense in depth)
  validate(data, 'entities/user.create');

  // Proceed with insert...
  const result = await query(userQueries.create, [data.email, data.name]);
  return result.rows[0];
}
```

---

## Query Parameter Coercion

Query strings are always strings. The middleware automatically coerces:

| Schema Type | Input | Result |
|-------------|-------|--------|
| `integer` | `"20"` | `20` |
| `boolean` | `"true"` | `true` |
| `array` | `"a,b,c"` | `["a", "b", "c"]` |

Example query schema:

```json
{
  "$id": "api/list-items",
  "type": "object",
  "properties": {
    "limit": {
      "type": "integer",
      "minimum": 1,
      "maximum": 100,
      "default": 20
    },
    "offset": {
      "type": "integer",
      "minimum": 0,
      "default": 0
    },
    "status": {
      "type": "string",
      "enum": ["draft", "active", "archived"]
    }
  },
  "additionalProperties": false
}
```

---

## Generating TypeScript Types

Generate `.d.ts` files from schemas for JSDoc type checking:

```bash
npm run generate:types
```

### How It Works

The script uses `json-schema-to-typescript` to convert JSON Schema files into TypeScript declaration files:

1. Reads all `.schema.json` files from `/schemas/`
2. Generates corresponding `.d.ts` files in `src/types/generated/`
3. Types can be imported in JSDoc comments for type checking

### Generated Structure

```
src/types/generated/
  common/
    uuid.d.ts
    error-response.d.ts
    pagination.d.ts
  entities/
    user.d.ts
    user.create.d.ts
    user.update.d.ts
  api/
    login.d.ts
    register.d.ts
```

### Using Generated Types

Import types in JSDoc comments:

```javascript
/**
 * @typedef {import('./types/generated/entities/user.create').UserCreate} CreateUserInput
 * @typedef {import('./types/generated/entities/user').User} User
 */

/**
 * Create a new user
 * @param {CreateUserInput} data - User creation data
 * @returns {Promise<User>} Created user
 */
async function createUser(data) {
  validate(data, 'entities/user.create');
  // data has full type information from schema
  const result = await db.query(userQueries.create, [data.email, data.password, data.name]);
  return result.rows[0];
}
```

### Regenerating Types

Run `npm run generate:types` whenever schemas are updated to keep types in sync.

---

## Aligning with Database Constraints

Schema validations should mirror database constraints:

| Database Constraint | JSON Schema Equivalent |
|---------------------|------------------------|
| `NOT NULL` | Include in `required` array |
| `UNIQUE` | Validate in service layer (not schema) |
| `CHECK (status IN ('a', 'b'))` | `"enum": ["a", "b"]` |
| `VARCHAR(255)` | `"maxLength": 255` |
| `CHECK (amount > 0)` | `"minimum": 1` (exclusive: `"exclusiveMinimum": 0`) |

---

## OpenAPI Integration

Reference schemas from OpenAPI spec:

```yaml
# openapi.yaml
paths:
  /users:
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: './schemas/entities/user.create.schema.json'
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: './schemas/entities/user.schema.json'
        '422':
          $ref: '#/components/responses/ValidationError'
```

---

## Type Checking with tsc

The project uses `tsc --checkJs` for type checking JavaScript files with JSDoc annotations.

### Running Type Check

```bash
npm run typecheck
```

### Requirements

Type checking requires:
1. `npm install` to install @types packages
2. Files must have JSDoc type annotations

### jsconfig.json Configuration

```json
{
  "compilerOptions": {
    "checkJs": true,
    "strict": true,
    "skipLibCheck": true,
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext"
  },
  "include": ["src/**/*.js", "test/**/*.js"],
  "exclude": ["node_modules"]
}
```

### Template Syntax Handling

Files containing template syntax (`{{VARIABLE}}`) are processed at project creation time and should be excluded from type checking until the project is generated.

**In starter templates:**
- Files like `config/index.js` contain `{{PROJECT_NAME}}` placeholders
- These are valid JavaScript after template processing
- Type checking runs correctly after `npm install` in a generated project

### Common Type Patterns

```javascript
// Import Express types
/**
 * @typedef {import('express').Request} Request
 * @typedef {import('express').Response} Response
 * @typedef {import('express').NextFunction} NextFunction
 */

// Type middleware parameters
/**
 * @param {Request} req
 * @param {Response} res
 * @param {NextFunction} next
 */
export function myMiddleware(req, res, next) {
  // ...
}

// Import schema types (after npm run generate:types)
/**
 * @typedef {import('./types/generated/entities/user.create').UserCreate} CreateUserInput
 */
```

---

## Best Practices

1. **Single source of truth** - Schema defines validation, types, and docs
2. **Strict by default** - Always use `additionalProperties: false`
3. **Descriptive error messages** - Use `description` on every property
4. **Defense in depth** - Validate at API boundary AND before database writes
5. **Align with database** - Schema constraints should match CHECK constraints
6. **Generate, don't duplicate** - Use `npm run generate:types` for TypeScript
7. **Add JSDoc types** - All exported functions should have parameter and return types

---

## Related Skills

- `rest-api` - API endpoint patterns and HTTP status codes
- `error-handling` - Custom error classes including ValidationError
- `forms` - Client-side HTML5 validation (UX layer)
- `security` - Input sanitization and output encoding
- `typescript-author` - TypeScript patterns and Zod alternative
