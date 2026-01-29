---
name: writing-openapi-specs
description: Reference guide for OpenAPI specification best practices, naming conventions, and expressing complex REST API patterns like polymorphism, enums, file uploads, and server-sent events. Use when writing or improving OpenAPI specs to ensure they follow established conventions and generate quality SDKs.
---

# Writing OpenAPI Specs

Reference for OpenAPI best practices and conventions. This skill provides guidance on taste, conventions, and grey areas not covered by the OpenAPI specification itself.

## When to Use This Skill

- Writing a new OpenAPI specification
- Improving operation naming and organization
- Expressing complex data types (enums, polymorphism, nullable)
- Handling file uploads, streaming, or server-sent events
- Making specs more code-gen friendly
- Understanding reusability patterns (components vs inline)

## Core Principles

### Naming Conventions

**Operation IDs**: Use lowercase with underscores, following `resource_action` pattern:

```yaml
# Good
operationId: users_list
operationId: users_get
operationId: users_create

# Avoid
operationId: GetApiV1Users    # Auto-generated, not semantic
```

**Component Names**: Use PascalCase for schemas, parameters, and other reusable components:

```yaml
components:
  schemas:
    UserProfile:      # PascalCase
    OrderHistory:     # PascalCase
  parameters:
    PageLimit:        # PascalCase
```

**Tags**: Use lowercase with hyphens for machine-friendly tags:

```yaml
tags:
  - name: user-management
    description: Operations for managing users
  - name: order-processing
    description: Operations for processing orders
```

For more details, see [reference/operations.md](reference/operations.md) and [reference/components.md](reference/components.md).

### Documentation Standards

**Use CommonMark**: All `description` fields support CommonMark syntax for rich formatting:

```yaml
description: |
  Retrieves a user by ID.

  ## Authorization
  Requires `users:read` scope.

  ## Rate Limits
  - 100 requests per minute per API key
  - 1000 requests per hour per IP
```

**Be Specific**: Provide actionable information, not generic descriptions:

```yaml
# Good
description: Returns a paginated list of active users, ordered by creation date (newest first)

# Avoid
description: Gets users
```

**Use `examples` over `example`**: The plural `examples` field provides better SDK generation:

```yaml
# Good
examples:
  basic_user:
    value:
      id: 123
      name: "John Doe"
  admin_user:
    value:
      id: 456
      name: "Jane Admin"
      role: admin

# Avoid single example
example:
  id: 123
  name: "John Doe"
```

For more details, see [reference/examples.md](reference/examples.md).

### Reusability

**Create components for**:
- Schemas used in multiple operations
- Common parameters (pagination, filtering)
- Common responses (errors, success patterns)
- Security schemes

**Keep inline for**:
- Operation-specific request bodies
- Unique response shapes
- One-off parameters

```yaml
# Reusable schema
components:
  schemas:
    User:
      type: object
      properties:
        id: {type: integer}
        name: {type: string}

# Reference it
paths:
  /users/{id}:
    get:
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
```

For more details, see [reference/components.md](reference/components.md).

## Complex Patterns Quick Reference

These patterns are commonly challenging. Brief examples below with links to detailed guidance.

### Enums

Use string enums with clear, semantic values:

```yaml
type: string
enum:
  - pending
  - approved
  - rejected
  - cancelled
```

**Avoid**:
- Numeric strings ("0", "1", "2")
- Generic values ("value1", "value2")
- Unclear abbreviations ("pnd", "appr")

See [reference/schemas.md#enums](reference/schemas.md) for more.

### Polymorphism (oneOf/allOf/anyOf)

**oneOf**: Value matches exactly one schema (type discrimination)

```yaml
PaymentMethod:
  oneOf:
    - $ref: '#/components/schemas/CreditCard'
    - $ref: '#/components/schemas/BankAccount'
    - $ref: '#/components/schemas/PayPal'
  discriminator:
    propertyName: type
    mapping:
      credit_card: '#/components/schemas/CreditCard'
      bank_account: '#/components/schemas/BankAccount'
      paypal: '#/components/schemas/PayPal'
```

**allOf**: Value matches all schemas (composition/inheritance)

```yaml
AdminUser:
  allOf:
    - $ref: '#/components/schemas/User'
    - type: object
      properties:
        permissions:
          type: array
          items: {type: string}
```

**anyOf**: Value matches one or more schemas (flexible union)

```yaml
SearchFilter:
  anyOf:
    - $ref: '#/components/schemas/TextFilter'
    - $ref: '#/components/schemas/DateFilter'
    - $ref: '#/components/schemas/NumericFilter'
```

See [reference/schemas.md#polymorphism](reference/schemas.md) for detailed guidance.

### Discriminators

Use discriminators with `oneOf` for efficient type identification:

```yaml
Pet:
  oneOf:
    - $ref: '#/components/schemas/Dog'
    - $ref: '#/components/schemas/Cat'
  discriminator:
    propertyName: petType
    mapping:
      dog: '#/components/schemas/Dog'
      cat: '#/components/schemas/Cat'

Dog:
  type: object
  required: [petType, bark]
  properties:
    petType:
      type: string
      enum: [dog]
    bark:
      type: string

Cat:
  type: object
  required: [petType, meow]
  properties:
    petType:
      type: string
      enum: [cat]
    meow:
      type: string
```

See [reference/schemas.md#discriminators](reference/schemas.md) for more.

### Nullable Types

Handle null values differently based on OpenAPI version:

**OpenAPI 3.1** (JSON Schema 2020-12 compliant):
```yaml
type: [string, "null"]
# or
type: string
nullable: true  # Still supported for compatibility
```

**OpenAPI 3.0**:
```yaml
type: string
nullable: true
```

For optional fields, use `required` array:
```yaml
type: object
properties:
  name: {type: string}      # Can be omitted
  email: {type: string}     # Can be omitted
required: [name]            # email is optional
```

See [reference/schemas.md#nullable](reference/schemas.md) for more.

### File Uploads

Use `multipart/form-data` for file uploads:

```yaml
requestBody:
  required: true
  content:
    multipart/form-data:
      schema:
        type: object
        properties:
          file:
            type: string
            format: binary
          metadata:
            type: object
            properties:
              description: {type: string}
              tags:
                type: array
                items: {type: string}
        required: [file]
```

For base64-encoded files in JSON:
```yaml
requestBody:
  content:
    application/json:
      schema:
        type: object
        properties:
          filename: {type: string}
          content:
            type: string
            format: byte  # base64-encoded
```

See [reference/request-bodies.md#file-uploads](reference/request-bodies.md) for more.

### Server-Sent Events (SSE)

Express streaming responses with `text/event-stream`:

```yaml
responses:
  '200':
    description: Stream of events
    content:
      text/event-stream:
        schema:
          type: string
          description: |
            Server-sent events stream. Each event follows the format:

            ```
            event: message
            data: {"type": "update", "content": "..."}

            ```
        examples:
          notification_stream:
            value: |
              event: message
              data: {"type": "notification", "message": "New order received"}

              event: message
              data: {"type": "notification", "message": "Order processing complete"}
```

See [reference/responses.md#streaming](reference/responses.md) for more patterns.

## Field Reference

Detailed guidance for each major OpenAPI field:

- **Operations**: Operation IDs, methods, tags, deprecation → [reference/operations.md](reference/operations.md)
- **Schemas**: Data types, polymorphism, enums, nullable → [reference/schemas.md](reference/schemas.md)
- **Parameters**: Path, query, header, cookie parameters → [reference/parameters.md](reference/parameters.md)
- **Request Bodies**: Content types, file uploads, encoding → [reference/request-bodies.md](reference/request-bodies.md)
- **Responses**: Status codes, streaming, error patterns → [reference/responses.md](reference/responses.md)
- **Components**: Reusable definitions, organization → [reference/components.md](reference/components.md)
- **Security**: Authentication schemes, scopes, granular control → [reference/security.md](reference/security.md)
- **Examples**: Single and multiple examples, placement → [reference/examples.md](reference/examples.md)

## SDK Generation Considerations

When writing specs for SDK generation:

1. **Always define `operationId`**: Required for meaningful method names
2. **Provide rich examples**: Helps generate better documentation and tests
3. **Be explicit about required fields**: Affects SDK method signatures
4. **Use discriminators with oneOf**: Generates type-safe unions
5. **Document error responses**: Generates better error handling code

Example SDK-friendly operation:

```yaml
paths:
  /users:
    get:
      operationId: users_list
      summary: List all users
      description: Returns a paginated list of users
      parameters:
        - name: limit
          in: query
          schema: {type: integer, default: 20}
        - name: offset
          in: query
          schema: {type: integer, default: 0}
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: object
                required: [data, pagination]
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
                  pagination:
                    $ref: '#/components/schemas/PaginationInfo'
              examples:
                success:
                  value:
                    data: [{id: 1, name: "Alice"}, {id: 2, name: "Bob"}]
                    pagination: {total: 100, limit: 20, offset: 0}
```

This generates: `sdk.users.list({limit: 20, offset: 0})`

## Common Pitfalls

**Don't**:
- Use generic descriptions like "Gets data" or "Returns object"
- Mix naming conventions (pick one style and stick to it)
- Forget `operationId` (causes auto-generated names)
- Use `example` when you mean `examples` (plural is better)
- Make everything required (be thoughtful about optional fields)
- Inline everything (use components for reusability)
- Reference everything (inline simple one-off schemas)
- Forget to document error responses
- Use magic numbers without explanation
- Omit content types (be explicit)

**Do**:
- Provide actionable, specific descriptions
- Use consistent naming patterns throughout
- Define clear `operationId` for every operation
- Use `examples` (plural) with named examples
- Carefully consider required vs optional fields
- Balance reusability with clarity
- Document all expected responses (success and errors)
- Explain constraints and validation rules
- Be explicit about content types and formats
