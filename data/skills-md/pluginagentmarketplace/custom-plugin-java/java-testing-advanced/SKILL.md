---
name: java-testing-advanced
description: Advanced testing - Testcontainers, contract testing, mutation testing, property-based
sasmp_version: "1.3.0"
version: "3.0.0"
bonded_agent: 04-java-testing
bond_type: SECONDARY_BOND
allowed-tools: Read, Write, Bash, Glob, Grep

# Parameter Validation
parameters:
  technique:
    type: string
    enum: [testcontainers, contract, mutation, property_based]
    description: Advanced testing technique
---

# Java Testing Advanced Skill

Advanced testing techniques for comprehensive test coverage.

## Overview

This skill covers advanced testing patterns including Testcontainers for integration testing, contract testing with Pact, mutation testing with PIT, and property-based testing.

## When to Use This Skill

Use when you need to:
- Test with real databases (Testcontainers)
- Verify API contracts
- Find gaps with mutation testing
- Generate test cases automatically

## Quick Reference

### Testcontainers

```java
@Testcontainers
@SpringBootTest
class OrderRepositoryIT {

    @Container
    static PostgreSQLContainer<?> postgres =
        new PostgreSQLContainer<>("postgres:15")
            .withDatabaseName("test")
            .withUsername("test")
            .withPassword("test");

    @Container
    static KafkaContainer kafka =
        new KafkaContainer(DockerImageName.parse("confluentinc/cp-kafka:7.4.0"));

    @DynamicPropertySource
    static void configure(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.kafka.bootstrap-servers", kafka::getBootstrapServers);
    }

    @Test
    void shouldPersistOrder() {
        Order saved = repository.save(new Order("item", 100.0));
        assertThat(saved.getId()).isNotNull();
    }
}
```

### Contract Testing (Pact)

```java
@ExtendWith(PactConsumerTestExt.class)
class UserServiceContractTest {

    @Pact(consumer = "order-service", provider = "user-service")
    public RequestResponsePact createPact(PactDslWithProvider builder) {
        return builder
            .given("user exists")
            .uponReceiving("get user request")
                .path("/users/1")
                .method("GET")
            .willRespondWith()
                .status(200)
                .body(new PactDslJsonBody()
                    .integerType("id", 1)
                    .stringType("name", "John"))
            .toPact();
    }

    @Test
    @PactTestFor(pactMethod = "createPact")
    void testGetUser(MockServer mockServer) {
        User user = client.getUser(mockServer.getUrl(), 1L);
        assertThat(user.getName()).isEqualTo("John");
    }
}
```

### Mutation Testing (PIT)

```xml
<plugin>
    <groupId>org.pitest</groupId>
    <artifactId>pitest-maven</artifactId>
    <version>1.15.0</version>
    <configuration>
        <targetClasses>
            <param>com.example.service.*</param>
        </targetClasses>
        <mutationThreshold>80</mutationThreshold>
    </configuration>
</plugin>
```

### Property-Based Testing

```java
@Property
void shouldReverseListTwiceReturnsOriginal(@ForAll List<Integer> list) {
    Collections.reverse(list);
    Collections.reverse(list);
    // Original order restored
}
```

## Testing Pyramid

```
     /\        E2E Tests (few)
    /  \       Contract Tests
   /----\      Integration Tests
  /------\     Unit Tests (many)
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Container slow | Reuse containers |
| Port conflicts | Random ports |
| Flaky tests | Wait strategies |

## Usage

```
Skill("java-testing-advanced")
```
