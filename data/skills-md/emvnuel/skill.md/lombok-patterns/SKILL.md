---
name: lombok-patterns
description: Lombok annotations and best practices for Java 21+ projects. Use when reducing boilerplate, configuring builders, or choosing between Lombok and Records.
---

# Lombok Patterns

This skill provides guidance on using Project Lombok to reduce boilerplate code in Java applications, covering annotations, best practices, and integration patterns.

> **Note**: This guide targets Java 21+ projects. Some Lombok features are now obsolete due to modern Java features (Records, `var`, try-with-resources). See [Java 21+ Considerations](#java-21-considerations) below.

## Overview

Lombok is a Java library that automatically generates common code like getters, setters, constructors, builders, and more during compilation. It helps create cleaner, more maintainable code.

## Java 21+ Considerations

Some Lombok features are now redundant with modern Java:

| Lombok Feature | Java Alternative             | Recommendation                          |
| -------------- | ---------------------------- | --------------------------------------- |
| `val`/`var`    | `var` (Java 10+)             | Use Java `var`                          |
| `@Value`       | `record` (Java 16+)          | Prefer records for simple value objects |
| `@Data`        | `record` (Java 16+)          | Prefer records for simple DTOs          |
| `@Cleanup`     | try-with-resources (Java 7+) | Use try-with-resources                  |
| `@With`        | `record` wither methods      | Records can define wither methods       |

### When Lombok Still Adds Value

- **JPA Entities**: Records don't work with JPA (need no-arg constructor, mutable state)
- **`@Builder`**: Records don't have built-in builder support
- **`@Slf4j`**: No Java equivalent for logger generation
- **`@RequiredArgsConstructor`**: Useful for Spring dependency injection
- **Inheritance**: Records can't extend classes

## Annotation Categories

### Core Annotations (Still Valuable)

| Annotation                 | Purpose                               | Use Case                      |
| -------------------------- | ------------------------------------- | ----------------------------- |
| `@Getter`/`@Setter`        | Accessor methods                      | JPA entities, mutable classes |
| `@NoArgsConstructor`       | No-argument constructor               | JPA entities, serialization   |
| `@AllArgsConstructor`      | All-fields constructor                | Dependency injection          |
| `@RequiredArgsConstructor` | Constructor for final/@NonNull fields | Spring services               |
| `@Builder`                 | Builder pattern implementation        | Complex object construction   |

### Consider Java Records Instead

| Lombok   | Use Java Record When            |
| -------- | ------------------------------- |
| `@Value` | Simple immutable data carriers  |
| `@Data`  | Simple DTOs without inheritance |

```java
// ✅ Prefer Java Record for simple value objects
public record Money(BigDecimal amount, String currency) {}

// ✅ Prefer Java Record for simple DTOs
public record CustomerDTO(String name, String email) {}

// ✅ Use Lombok for JPA entities (records don't work with JPA)
@Entity
@Getter
@Setter
@NoArgsConstructor
public class Customer {
    @Id private Long id;
    private String name;
}
```

### Logging Annotations

| Annotation    | Logger Type            |
| ------------- | ---------------------- |
| `@Slf4j`      | SLF4J (recommended)    |
| `@Log4j2`     | Log4j 2                |
| `@Log`        | java.util.logging      |
| `@CommonsLog` | Apache Commons Logging |

### Field & Method Annotations

| Annotation           | Purpose                                      |
| -------------------- | -------------------------------------------- |
| `@NonNull`           | Null checks on parameters/fields             |
| `@With`              | Immutable setters (creates new instance)     |
| `@SneakyThrows`      | Throw checked exceptions without declaration |
| `@Synchronized`      | Thread-safe method synchronization           |
| `@ToString`          | Customizable toString() generation           |
| `@EqualsAndHashCode` | Customizable equals/hashCode                 |

## Quick Reference

### JPA Entities (Lombok Recommended)

```java
@Entity
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(onlyExplicitlyIncluded = true)
public class Product {
    @Id
    @EqualsAndHashCode.Include
    private Long id;

    private String name;
    private BigDecimal price;
}
```

### Spring Services

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class OrderService {
    private final OrderRepository orderRepository;
    private final PaymentService paymentService;

    public Order process(Order order) {
        log.info("Processing order: {}", order.getId());
        return orderRepository.save(order);
    }
}
```

### Builder Pattern (Lombok Adds Value)

```java
// Records don't have builder support - use Lombok
@Builder
public record Email(
    String to,
    String subject,
    String body,
    @Singular List<String> attachments
) {}

// Usage
Email email = Email.builder()
    .to("user@example.com")
    .subject("Hello")
    .body("Content")
    .attachment("file1.pdf")
    .build();
```

## Best Practices

### ✅ Do

- Use Java Records for simple value objects and DTOs
- Use `@RequiredArgsConstructor` with `final` fields for dependency injection
- Use `@Slf4j` for logging instead of manual logger creation
- Use `@Builder` for classes with many optional fields
- Be explicit with `@EqualsAndHashCode` on JPA entities

### ❌ Avoid

- Using `@Data` or `@Value` when a Java Record would suffice
- Using `@Data` on JPA entities (use individual annotations)
- Using `@EqualsAndHashCode` with lazy-loaded JPA relationships
- Overusing `@SneakyThrows` (makes exception handling unclear)

## Common Pitfalls

| Pitfall                      | Problem                                               | Solution                                                |
| ---------------------------- | ----------------------------------------------------- | ------------------------------------------------------- |
| `@Data` on entities          | Includes mutable setters, problematic equals/hashCode | Use `@Getter`, `@Setter`, explicit `@EqualsAndHashCode` |
| Missing `@NoArgsConstructor` | JPA/Jackson need no-arg constructor                   | Always add with `@AllArgsConstructor`                   |
| Circular `@ToString`         | StackOverflow with bidirectional relationships        | Use `@ToString.Exclude` on one side                     |
| Using Lombok for simple DTOs | Adds unnecessary dependency                           | Use Java Records instead                                |

## Cookbook Index

### Core Annotations

- [data-annotation](cookbook/data-annotation.md) - `@Data` (consider Records instead)
- [value-annotation](cookbook/value-annotation.md) - `@Value` (consider Records instead)
- [getter-setter](cookbook/getter-setter.md) - `@Getter` and `@Setter`
- [constructor-annotations](cookbook/constructor-annotations.md) - Constructor generation
- [builder-annotation](cookbook/builder-annotation.md) - Builder pattern with `@Builder`
- [logging-annotations](cookbook/logging-annotations.md) - Logger generation

### Field & Method Annotations

- [non-null](cookbook/non-null.md) - Null checking with `@NonNull`
- [with-annotation](cookbook/with-annotation.md) - Immutable setters with `@With`
- [sneaky-throws](cookbook/sneaky-throws.md) - Checked exception handling
- [synchronized-annotation](cookbook/synchronized-annotation.md) - Thread safety

### Integration Patterns

- [entity-patterns](cookbook/entity-patterns.md) - JPA/Hibernate best practices
- [equals-hashcode-jpa](cookbook/equals-hashcode-jpa.md) - Entity identity
- [dependency-injection](cookbook/dependency-injection.md) - Spring constructor injection
- [configuration-properties](cookbook/configuration-properties.md) - Spring Boot configuration
