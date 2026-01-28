---
name: mapstruct-patterns
description: Constructor-based MapStruct mapping for compile-time safety in Jakarta EE. Use when implementing DTO mapping or using @Default annotations.
---

# MapStruct Patterns for Jakarta EE

Best practices for using MapStruct with constructor-based mapping to achieve compile-time safety. When constructors change, mappings fail to compile — no runtime surprises.

## Core Philosophy

> **Use constructors, not setters**. This gives you compile-time errors when fields change.

Records naturally enforce this. For mutable entities, use the `@Default` annotation.

## CDI Setup

```java
@Mapper(componentModel = "cdi")  // CDI injection
public interface OrderMapper {
    OrderResponse toResponse(Order order);
}
```

## The @Default Annotation Trick

MapStruct uses any annotation named `@Default` to select the constructor. Create your own:

```java
package com.example.mapstruct;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Target(ElementType.CONSTRUCTOR)
@Retention(RetentionPolicy.CLASS)
public @interface Default {
}
```

### Usage on Mutable Entities

```java
@Entity
public class Order {

    @Id @GeneratedValue
    private Long id;
    private String customerId;
    private BigDecimal total;
    private OrderStatus status;

    // JPA needs this
    protected Order() {}

    // MapStruct uses this - CHANGE HERE = COMPILER ERROR in mapper
    @Default
    public Order(String customerId, BigDecimal total, OrderStatus status) {
        this.customerId = customerId;
        this.total = total;
        this.status = status;
    }
}
```

## Records (Ideal Case)

Records automatically work with constructor mapping:

```java
// No @Default needed - single constructor
public record OrderResponse(
    String orderId,
    String customerId,
    String total,
    String status
) {}

@Mapper(componentModel = "cdi")
public interface OrderMapper {

    @Mapping(target = "orderId", source = "id")
    @Mapping(target = "total", expression = "java(order.getTotal().toString())")
    OrderResponse toResponse(Order order);
}
```

## Key Patterns

### 1. Constructor-Based Mapping

```java
@Mapper(componentModel = "cdi")
public interface CustomerMapper {

    // MapStruct uses Customer constructor, fail if signature changes
    Customer toEntity(CreateCustomerRequest request);

    // MapStruct uses CustomerResponse constructor
    CustomerResponse toResponse(Customer customer);
}
```

### 2. Custom @Default for Entities

```java
@Entity
public class Product {

    @Id @GeneratedValue
    private Long id;
    private String name;
    private BigDecimal price;
    private String category;

    protected Product() {}

    @Default  // Your custom annotation
    public Product(String name, BigDecimal price, String category) {
        this.name = name;
        this.price = price;
        this.category = category;
    }
}
```

## Anti-Pattern: Setter-Based Mapping

```java
// ❌ Can add field to DTO, forget mapper, get null at runtime
public class OrderDTO {
    private String id;
    private String status;
    private String newField;  // Added later, no error!

    // Just setters...
}

// ✓ Add field to constructor = compiler error in mapper
public record OrderDTO(String id, String status, String newField) {}
```

## Compile-Time Safety Benefit

```java
// Before: Record has 3 fields
public record OrderResponse(String id, String status, String total) {}

// After: Added customerName field
public record OrderResponse(String id, String status, String total, String customerName) {}

// Mapper now FAILS TO COMPILE until you add the mapping:
@Mapper(componentModel = "cdi")
public interface OrderMapper {
    @Mapping(target = "customerName", source = "customer.name")  // Must add this
    OrderResponse toResponse(Order order);
}
```

## Cookbook Index

### Setup & Configuration

- [cdi-setup](cookbook/cdi-setup.md) - CDI/MicroProfile setup
- [default-annotation](cookbook/default-annotation.md) - Custom @Default annotation

### Mapping Patterns

- [constructor-mapping](cookbook/constructor-mapping.md) - Constructor-based mapping
- [record-mapping](cookbook/record-mapping.md) - Java Records mapping
- [entity-mapping](cookbook/entity-mapping.md) - JPA entity mapping
