---
name: rest-api-design
description: REST API design patterns and MicroProfile OpenAPI documentation. Use when designing endpoints, choosing HTTP methods, status codes, or documenting APIs with OpenAPI annotations.
---

# REST API Design Best Practices

Design consistent, intuitive REST APIs with proper documentation.

---

## Endpoint Design Rules

### Use Nouns, Not Verbs

```java
// ❌ Bad
@GET @Path("/getUsers")
@POST @Path("/createUser")

// ✓ Good
@GET @Path("/users")
@POST @Path("/users")
```

### Use Plural Nouns for Collections

```java
@Path("/users")        // Collection
@Path("/users/{id}")   // Single resource
@Path("/orders")       // Collection
@Path("/orders/{id}")  // Single resource
```

### Nest Related Resources (Max 3 Levels)

```java
@Path("/users/{userId}/orders")              // User's orders
@Path("/users/{userId}/orders/{orderId}")    // Specific order
@Path("/posts/{postId}/comments")            // Post's comments
```

**Cookbook**: [endpoint-design.md](./cookbook/endpoint-design.md)

---

## HTTP Methods

| Method   | Purpose          | Idempotent | Request Body |
| -------- | ---------------- | ---------- | ------------ |
| `GET`    | Retrieve         | Yes        | No           |
| `POST`   | Create           | No         | Yes          |
| `PUT`    | Replace entirely | Yes        | Yes          |
| `PATCH`  | Partial update   | Yes        | Yes          |
| `DELETE` | Remove           | Yes        | No           |

**Cookbook**: [http-methods.md](./cookbook/http-methods.md)

---

## Status Codes

| Code | Meaning              | When to Use                |
| ---- | -------------------- | -------------------------- |
| 200  | OK                   | Successful GET, PUT, PATCH |
| 201  | Created              | Successful POST            |
| 204  | No Content           | Successful DELETE          |
| 400  | Bad Request          | Validation errors          |
| 401  | Unauthorized         | Missing/invalid auth       |
| 403  | Forbidden            | Insufficient permissions   |
| 404  | Not Found            | Resource doesn't exist     |
| 422  | Unprocessable Entity | Business rule violation    |
| 500  | Internal Error       | Unexpected server error    |

**Cookbook**: [status-codes.md](./cookbook/status-codes.md)

---

## Filtering & Pagination

```java
@GET
@Path("/products")
public List<Product> list(
    @QueryParam("category") String category,
    @QueryParam("minPrice") BigDecimal minPrice,
    @QueryParam("sort") @DefaultValue("name") String sort,
    @QueryParam("page") @DefaultValue("0") int page,
    @QueryParam("size") @DefaultValue("20") int size
) { }
```

**Cookbook**: [filtering-pagination.md](./cookbook/filtering-pagination.md)

---

## API Versioning

```java
// URL path versioning (recommended)
@Path("/v1/users")
public class UserResourceV1 { }

@Path("/v2/users")
public class UserResourceV2 { }
```

**Cookbook**: [versioning.md](./cookbook/versioning.md)

---

## MicroProfile OpenAPI Documentation

```java
@Path("/users")
@Tag(name = "Users", description = "User management")
public class UserResource {

    @GET
    @Path("/{id}")
    @Operation(summary = "Get user by ID")
    @APIResponse(responseCode = "200", description = "User found")
    @APIResponse(responseCode = "404", description = "User not found")
    public User getById(@PathParam("id") Long id) { }
}
```

**Cookbook**: [openapi-documentation.md](./cookbook/openapi-documentation.md)

---

## Cookbook Index

**Design**: [Endpoint Design](./cookbook/endpoint-design.md) · [HTTP Methods](./cookbook/http-methods.md)

**Responses**: [Status Codes](./cookbook/status-codes.md)

**Querying**: [Filtering & Pagination](./cookbook/filtering-pagination.md)

**Evolving**: [Versioning](./cookbook/versioning.md)

**Documentation**: [OpenAPI Documentation](./cookbook/openapi-documentation.md)
