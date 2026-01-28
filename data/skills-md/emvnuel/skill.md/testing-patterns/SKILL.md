---
name: testing-patterns
description: REST integration testing patterns with JUnit 5, Mockito, RestAssured. Use when writing integration tests that mock external dependencies, use Testcontainers/H2 for databases, and test endpoints with raw JSON bodies.
---

# REST Integration Testing Patterns

Write integration tests for REST endpoints using Quarkus test framework.

---

## Quick Start

Basic REST integration test with RestAssured:

```java
@QuarkusTest
class OrderResourceTest {

    @Test
    void shouldCreateOrder() {
        given()
            .contentType(ContentType.JSON)
            .body("""
                {
                    "customerId": "cust-123",
                    "items": [{"productId": "prod-1", "quantity": 2}]
                }
                """)
        .when()
            .post("/orders")
        .then()
            .statusCode(201)
            .body("id", notNullValue())
            .body("status", equalTo("PENDING"));
    }
}
```

---

## Core Patterns

### REST Integration Tests

**Use**: Test full request/response cycle through REST layer  
**Stack**: `@QuarkusTest` + RestAssured  
**Cookbook**: [rest-integration-tests.md](./cookbook/rest-integration-tests.md)

### Mocking External Dependencies

**Use**: Isolate tests from external HTTP services, queues, etc.  
**Stack**: `@InjectMock` with Mockito  
**Cookbook**: [mocking-dependencies.md](./cookbook/mocking-dependencies.md)

### Database with Testcontainers

**Use**: Test against real PostgreSQL/MySQL  
**Stack**: Quarkus DevServices or `@Testcontainers`  
**Cookbook**: [testcontainers-setup.md](./cookbook/testcontainers-setup.md)

### Database with H2

**Use**: Fast in-memory alternative when container not needed  
**Stack**: H2 with test profile  
**Cookbook**: [h2-setup.md](./cookbook/h2-setup.md)

### Raw JSON Request Bodies

**Use**: Test with exact JSON payloads (no object serialization)  
**Stack**: Text blocks + JsonPath assertions  
**Cookbook**: [json-request-bodies.md](./cookbook/json-request-bodies.md)

### Test Structure & Lifecycle

**Use**: Organize tests with JUnit 5 features  
**Stack**: `@Nested`, `@BeforeEach`, naming conventions  
**Cookbook**: [test-structure.md](./cookbook/test-structure.md)

---

## Quick Reference

| Pattern             | When to Use                    | Key Annotation/Tool     |
| ------------------- | ------------------------------ | ----------------------- |
| REST Integration    | Test endpoint behavior         | `@QuarkusTest`          |
| Mock Dependencies   | Isolate from external services | `@InjectMock`           |
| Testcontainers      | Need real database behavior    | DevServices / Container |
| H2 In-Memory        | Fast tests, simple queries     | `%test` profile         |
| Raw JSON Bodies     | Exact payload control          | Text blocks             |
| Nested Test Classes | Group related scenarios        | `@Nested`               |

---

## Cookbook Index

**Core Testing**: [REST Integration Tests](./cookbook/rest-integration-tests.md) · [Test Structure](./cookbook/test-structure.md)

**Dependencies**: [Mocking Dependencies](./cookbook/mocking-dependencies.md)

**Database**: [Testcontainers Setup](./cookbook/testcontainers-setup.md) · [H2 Setup](./cookbook/h2-setup.md)

**Request/Response**: [JSON Request Bodies](./cookbook/json-request-bodies.md)
