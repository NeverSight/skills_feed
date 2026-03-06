---
name: api-docs
description: Create OpenAPI specs, SDK docs, and API documentation. Use for API documentation or client library generation.
---

# API Documentation

Create comprehensive API documentation and OpenAPI specs.

## When to Use

- Documenting new APIs
- Creating OpenAPI/Swagger specs
- Generating SDK documentation
- Writing API guides
- Creating Postman collections

## OpenAPI Template

```yaml
openapi: 3.0.3
info:
  title: API Name
  version: 1.0.0
  description: API description

servers:
  - url: https://api.example.com/v1
    description: Production

paths:
  /users:
    get:
      summary: List users
      operationId: listUsers
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
      responses:
        "200":
          description: Success
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: "#/components/schemas/User"

    post:
      summary: Create user
      operationId: createUser
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CreateUser"
      responses:
        "201":
          description: Created
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/User"

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
          format: uuid
        name:
          type: string
        email:
          type: string
          format: email
      required:
        - id
        - name
        - email

    CreateUser:
      type: object
      properties:
        name:
          type: string
        email:
          type: string
          format: email
      required:
        - name
        - email

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - bearerAuth: []
```

## Documentation Structure

````markdown
# API Reference

## Authentication

All requests require a Bearer token in the Authorization header.

## Endpoints

### Users

#### List Users

`GET /users`

**Parameters:**

| Name  | Type    | Required | Description      |
| ----- | ------- | -------- | ---------------- |
| limit | integer | No       | Results per page |

**Response:**

    ```json
    [{ "id": "...", "name": "...", "email": "..." }]
    ```

#### Create User

`POST /users`

**Request Body:**

    ```json
    { "name": "John", "email": "john@example.com" }
    ```

## Error Codes

| Code | Description           |
| ---- | --------------------- |
| 400  | Bad Request           |
| 401  | Unauthorized          |
| 404  | Not Found             |
| 500  | Internal Server Error |
````

## Examples

**Input:** "Document the user API"
**Action:** Create OpenAPI spec with all endpoints, schemas, examples, error codes

**Input:** "Generate API docs from code"
**Action:** Extract endpoints, infer types, create structured documentation
