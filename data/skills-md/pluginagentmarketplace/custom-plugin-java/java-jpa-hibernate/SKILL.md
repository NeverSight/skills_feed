---
name: java-jpa-hibernate
description: Master JPA/Hibernate - entity design, queries, transactions, performance optimization
sasmp_version: "1.3.0"
version: "3.0.0"
bonded_agent: 06-java-persistence
bond_type: PRIMARY_BOND
allowed-tools: Read, Write, Bash, Glob, Grep

# Parameter Validation
parameters:
  database:
    type: string
    enum: [postgresql, mysql, oracle, h2]
    description: Target database
  focus:
    type: string
    enum: [entities, queries, transactions, caching]
    description: Topic focus area
---

# Java JPA Hibernate Skill

Master data persistence with JPA and Hibernate for production applications.

## Overview

This skill covers JPA entity design, Hibernate optimization, Spring Data repositories, query strategies, and caching. Focuses on preventing N+1 queries and building high-performance persistence layers.

## When to Use This Skill

Use when you need to:
- Design JPA entities with relationships
- Optimize database queries
- Configure Hibernate for performance
- Implement caching strategies
- Debug persistence issues

## Topics Covered

### Entity Design
- Entity mapping annotations
- Relationship types (1:1, 1:N, N:M)
- Inheritance strategies
- Lifecycle callbacks
- Auditing

### Query Optimization
- N+1 problem prevention
- JOIN FETCH vs EntityGraph
- Batch fetching
- Projections and DTOs

### Transactions
- @Transactional configuration
- Propagation and isolation
- Optimistic vs pessimistic locking
- Deadlock prevention

### Caching
- First and second level cache
- Query cache
- Cache invalidation
- Redis integration

## Quick Reference

```java
// Entity with relationships
@Entity
@Table(name = "orders")
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "customer_id", nullable = false)
    private Customer customer;

    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL, orphanRemoval = true)
    @BatchSize(size = 20)
    private List<OrderItem> items = new ArrayList<>();

    @Version
    private Long version;

    // Bidirectional helper
    public void addItem(OrderItem item) {
        items.add(item);
        item.setOrder(this);
    }
}

// Auditing base class
@MappedSuperclass
@EntityListeners(AuditingEntityListener.class)
public abstract class Auditable {
    @CreatedDate
    @Column(updatable = false)
    private Instant createdAt;

    @LastModifiedDate
    private Instant updatedAt;
}

// Repository with query optimization
public interface OrderRepository extends JpaRepository<Order, Long> {

    // JOIN FETCH to prevent N+1
    @Query("SELECT DISTINCT o FROM Order o JOIN FETCH o.items WHERE o.status = :status")
    List<Order> findByStatusWithItems(@Param("status") Status status);

    // EntityGraph alternative
    @EntityGraph(attributePaths = {"items", "customer"})
    Optional<Order> findById(Long id);

    // DTO Projection
    @Query("SELECT new com.example.OrderSummary(o.id, o.status, c.name) " +
           "FROM Order o JOIN o.customer c WHERE o.id = :id")
    Optional<OrderSummary> findSummaryById(@Param("id") Long id);
}
```

## N+1 Prevention Strategies

| Strategy | Use When | Example |
|----------|----------|---------|
| JOIN FETCH | Always need relation | `JOIN FETCH o.items` |
| EntityGraph | Dynamic fetching | `@EntityGraph(attributePaths)` |
| @BatchSize | Collection access | `@BatchSize(size = 20)` |
| DTO Projection | Read-only queries | `new OrderSummary(...)` |

## Hibernate Configuration

```yaml
spring:
  jpa:
    open-in-view: false  # Critical!
    properties:
      hibernate:
        jdbc.batch_size: 50
        order_inserts: true
        order_updates: true
        default_batch_fetch_size: 20
        generate_statistics: ${HIBERNATE_STATS:false}

  datasource:
    hikari:
      maximum-pool-size: 20
      minimum-idle: 5
      leak-detection-threshold: 60000
```

## Troubleshooting

### Common Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| N+1 queries | Lazy in loop | JOIN FETCH, EntityGraph |
| LazyInitException | Session closed | DTO projection |
| Slow queries | Missing index | EXPLAIN ANALYZE |
| Connection leak | No @Transactional | Add annotation |

### Debug Properties
```properties
spring.jpa.show-sql=true
logging.level.org.hibernate.SQL=DEBUG
logging.level.org.hibernate.orm.jdbc.bind=TRACE
hibernate.generate_statistics=true
```

### Debug Checklist
```
□ Enable SQL logging
□ Check query count per request
□ Verify fetch strategies
□ Review @Transactional
□ Check connection pool
```

## Usage

```
Skill("java-jpa-hibernate")
```

## Related Skills
- `java-performance` - Query optimization
- `java-spring-boot` - Spring Data
