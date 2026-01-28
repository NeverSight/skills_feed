---
name: openapi
description: >
  Best practices for API documentation using OpenAPI/Swagger.
  Trigger: When writing OpenAPI/Swagger specifications.
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [root]
  auto_invoke: "Working with openapi"

## When to Use

Use this skill when:
- Creating OpenAPI 3.0+ specifications
- Documenting REST API endpoints
- Defining request/response schemas
- Generating API documentation

---

## Critical Patterns

### Schema Definition (REQUIRED)

```yaml
components:
  schemas:
    User:
      type: object
      description: Represents a user in the system
      required:
        - id
        - email
      properties:
        id:
          type: string
          format: uuid
          description: Unique identifier
          example: "123e4567-e89b-12d3-a456-426614174000"
        email:
          type: string
          format: email
          description: User's email address
          example: "user@example.com"
        name:
          type: string
          description: User's full name
          example: "John Doe"
```

### Endpoint Documentation (REQUIRED)

```yaml
paths:
  /users/{userId}:
    get:
      summary: Get user by ID
      description: |
        Retrieves detailed information about a specific user.
        Requires authentication.
      operationId: getUserById
      tags:
        - Users
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: User found successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          description: User not found
        '401':
          description: Authentication required
```

---

## Decision Tree

```
Need reusable schema?      → Define in components/schemas
Need auth info?            → Use securitySchemes
Need examples?             → Add example field
Need multiple formats?     → Use content negotiation
Need error response?       → Define error schema
```

---

## Code Examples

### Error Response

```yaml
components:
  schemas:
    Error:
      type: object
      required:
        - code
        - message
      properties:
        code:
          type: string
          example: "USER_NOT_FOUND"
        message:
          type: string
          example: "User with specified ID does not exist"
```

### Authentication

```yaml
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - bearerAuth: []
```

---

## Commands

```bash
# Validate spec
npx @redocly/cli lint openapi.yaml

# Generate docs
npx @redocly/cli build-docs openapi.yaml

# Generate client
npx openapi-generator-cli generate -i openapi.yaml -g typescript-axios -o ./client
```
