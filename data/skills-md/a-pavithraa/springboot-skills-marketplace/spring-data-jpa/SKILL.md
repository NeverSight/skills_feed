---
name: spring-data-jpa
description: Implement Spring Data JPA repositories, entities, and queries following modern best practices. Use for creating repositories (only for aggregate roots), writing queries (@Query, DTO projections), custom repositories (Criteria API, bulk ops), CQRS query services, entity relationships, and performance optimization. Covers patterns from simple repositories to advanced CQRS with detailed anti-patterns guidance.
---

# Spring Data JPA Implementation

## Critical Rules

**NEVER create repositories for every entity. ALWAYS create repositories only for aggregate roots.**

**NEVER use complex query method names. ALWAYS use @Query for non-trivial queries.**

**NEVER use save() blindly. ALWAYS understand persist vs merge semantics (see Vlad Mihalcea's guidance).**

## Step 1: Identify Repository Needs

Ask:
1. **Is this an aggregate root?** - Only aggregate roots get repositories
2. **Query complexity?** - Simple lookup or complex filtering?
3. **Read vs Write?** - Commands (write) or queries (read)?
4. **Performance critical?** - Large datasets, pagination, or projections?

## Step 2: Choose Pattern

| Pattern | When | Read |
|---------|------|------|
| **Simple Repository** | Basic CRUD, 1-2 custom queries | - |
| **@Query Repository** | Multiple filters, joins, sorting | `references/query-patterns.md` |
| **DTO Projection** | Read-only, performance-critical | `references/dto-projections.md` |
| **Custom Repository** | Complex logic, bulk ops, Criteria API | `references/custom-repositories.md` |
| **CQRS Query Service** | Separate read/write, multiple projections | `references/cqrs-query-service.md` |

**Decision criteria:**

| Need | Simple | @Query | DTO | Custom | CQRS |
|------|--------|--------|-----|--------|------|
| Basic CRUD | ✅ | ✅ | ❌ | ✅ | ✅ |
| Custom Queries | ❌ | ✅ | ✅ | ✅ | ✅ |
| Best Performance | ✅ | ✅ | ✅✅ | ✅✅ | ✅✅ |
| Complex Logic | ❌ | ❌ | ❌ | ✅ | ✅ |
| Read/Write Separation | ❌ | ❌ | ✅ | ✅ | ✅✅ |

## Step 3: Implement Repository

### Simple Repository

For basic lookups (1-2 properties):

```java
public interface ProductRepository extends JpaRepository<ProductEntity, Long> {
    Optional<ProductEntity> findByCode(String code);
    List<ProductEntity> findByStatus(ProductStatus status);
}
```

**Asset:** Use existing entity and repository patterns

### @Query Repository

For 3+ filters, joins, or readability. **Read:** `references/query-patterns.md`

```java
public interface OrderRepository extends JpaRepository<OrderEntity, Long> {

    @Query("""
        SELECT DISTINCT o
        FROM OrderEntity o
        LEFT JOIN FETCH o.items
        WHERE o.userId = :userId
        ORDER BY o.createdAt DESC
        """)
    List<OrderEntity> findUserOrders(@Param("userId") Long userId);
}
```

**Asset:** `assets/query-repository.java` - Complete template with examples

### DTO Projections

For read-only, performance-critical queries. **Read:** `references/dto-projections.md`

```java
public record ProductSummary(Long id, String name, BigDecimal price) {}

@Query("""
    SELECT new com.example.ProductSummary(p.id, p.name, p.price)
    FROM ProductEntity p
    WHERE p.status = 'ACTIVE'
    """)
List<ProductSummary> findActiveSummaries();
```

**Asset:** `assets/dto-projection.java` - Records, interfaces, native queries

### Custom Repository

For Criteria API, bulk ops. **Read:** `references/custom-repositories.md`

```java
// 1. Custom interface
public interface ProductRepositoryCustom {
    List<ProductEntity> findByDynamicCriteria(SearchCriteria criteria);
}

// 2. Implementation (must be named <Repository>Impl)
@Repository
class ProductRepositoryImpl implements ProductRepositoryCustom {
    @PersistenceContext
    private EntityManager entityManager;
    // Implementation using Criteria API
}

// 3. Main repository extends both
public interface ProductRepository extends JpaRepository<ProductEntity, Long>,
                                           ProductRepositoryCustom {
    Optional<ProductEntity> findBySku(String sku);
}
```

**Asset:** `assets/custom-repository.java` - Complete pattern

### CQRS Query Service

For Tomato/DDD architectures. **Read:** `references/cqrs-query-service.md`

```java
// Repository (package-private) - writes only
interface ProductRepository extends JpaRepository<ProductEntity, ProductId> {
    Optional<ProductEntity> findBySku(ProductSKU sku);
}

// QueryService (public) - reads only
@Service
@Transactional(readOnly = true)
public class ProductQueryService {

    private final JdbcTemplate jdbcTemplate;

    public List<ProductVM> findAllActive() {
        return jdbcTemplate.query("""
            SELECT id, name, price FROM products
            WHERE status = 'ACTIVE'
            """,
            (rs, rowNum) -> new ProductVM(
                rs.getLong("id"),
                rs.getString("name"),
                rs.getBigDecimal("price")
            )
        );
    }
}
```

**Asset:** `assets/query-service.java` - Full CQRS pattern with JdbcTemplate

## Step 4: Entity Relationships

**Read:** `references/relationships.md` for detailed guidance

**Quick patterns:**

```java
// ✅ GOOD: @ManyToOne (most common)
@ManyToOne(fetch = FetchType.LAZY, optional = false)
@JoinColumn(name = "order_id", nullable = false)
private Order order;

// ✅ ALTERNATIVE: Just use ID (loose coupling)
@Column(name = "product_id", nullable = false)
private Long productId;

// ❌ AVOID: @OneToMany (query from many side instead)
// Instead: List<OrderItem> items = itemRepository.findByOrderId(orderId);

// ❌ NEVER: @ManyToMany (create join entity instead)
@Entity
public class Enrollment {
    @ManyToOne private Student student;
    @ManyToOne private Course course;
    private LocalDate enrolledAt;
}
```

**Asset:** `assets/relationship-patterns.java` - All relationship types with examples

## Step 5: Performance Optimization

**Read:** `references/performance-guide.md` for complete checklist

**Critical optimizations:**

1. **Prevent N+1 queries:**
   ```java
   // Use JOIN FETCH
   @Query("SELECT o FROM Order o JOIN FETCH o.customer")
   List<Order> findWithCustomer();

   // Or use DTO projection
   @Query("SELECT new OrderSummary(o.id, c.name) FROM Order o JOIN o.customer c")
   List<OrderSummary> findSummaries();
   ```

2. **Use pagination:**
   ```java
   Pageable pageable = PageRequest.of(0, 20);
   Page<Product> page = repository.findByCategory("Electronics", pageable);
   ```

3. **Mark read services as readOnly:**
   ```java
   @Service
   @Transactional(readOnly = true)
   public class ProductQueryService { }
   ```

4. **Configure batch size:**
   ```yaml
   spring.jpa.properties.hibernate.jdbc.batch_size: 25
   ```

## Step 6: Transaction Management

**Best practices:**

```java
@Service
@Transactional(readOnly = true)  // Class-level for read services
public class ProductService {

    public List<ProductVM> findAll() {
        // Read operations
    }

    @Transactional  // Override for writes
    public void createProduct(CreateProductCmd cmd) {
        ProductEntity product = ProductEntity.create(cmd);
        repository.save(product);
    }
}
```

**Rules:**
- Use `@Transactional(readOnly = true)` at class level for query services
- Put `@Transactional` at service layer, not repository
- Override with `@Transactional` for write methods in read services

## Step 7: Testing

```java
@DataJpaTest
@Testcontainers
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class ProductRepositoryTest {

    @Container
    static PostgreSQLContainer<?> postgres =
        new PostgreSQLContainer<>("postgres:16-alpine");

    @Autowired
    private ProductRepository repository;

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }

    @Test
    void shouldFindProductByCode() {
        ProductEntity product = createTestProduct("P001");
        repository.save(product);

        Optional<ProductEntity> found = repository.findByCode("P001");

        assertThat(found).isPresent();
    }
}
```

## Anti-Patterns

| Don't | Do | Why |
|-------|-----|-----|
| Repository for every entity | Only for aggregate roots | Maintains boundaries |
| Use save() blindly | Understand persist/merge | Avoids unnecessary SELECT |
| Long query method names | Use @Query | Readability |
| findAll() without pagination | Use Page<> or Stream | Memory issues |
| Fetch entities for read views | Use DTO projections | Performance |
| FetchType.EAGER | LAZY + JOIN FETCH | Avoids N+1 |
| @ManyToMany | Use join entity | Allows relationship attributes |
| @Transactional in repository | Put in service layer | Proper boundaries |
| Return entities from controllers | Return DTOs/VMs | Prevents lazy issues |

## Common Pitfalls

### 1. LazyInitializationException
**Problem:** Accessing lazy associations outside transaction

**Solution:** Use DTO projection or JOIN FETCH
```java
@Query("SELECT o FROM Order o JOIN FETCH o.items WHERE o.id = :id")
Optional<Order> findByIdWithItems(@Param("id") Long id);
```

### 2. N+1 Queries
**Problem:** Loading associations in loop

**Solution:** See `references/performance-guide.md`

### 3. Cartesian Product
**Problem:** Multiple JOIN FETCH with collections

**Solution:** Separate queries or DTO projections

## Quick Reference

### When to Load References

- **Multiple filters/joins needed** → `references/query-patterns.md`
- **Read-only, performance-critical** → `references/dto-projections.md`
- **Dynamic queries, bulk operations** → `references/custom-repositories.md`
- **CQRS, read/write separation** → `references/cqrs-query-service.md`
- **Entity associations** → `references/relationships.md`
- **Slow queries, N+1 issues** → `references/performance-guide.md`

### Available Assets

All templates in `assets/`:
- `query-repository.java` - @Query examples, pagination, bulk ops
- `dto-projection.java` - Records, interfaces, native queries
- `custom-repository.java` - Criteria API, EntityManager
- `query-service.java` - CQRS with JdbcTemplate
- `relationship-patterns.java` - All JPA associations

## References

Incorporates best practices from:
- [Vlad Mihalcea - Best Spring Data JpaRepository](https://vladmihalcea.com/best-spring-data-jparepository/)
- [Vlad Mihalcea - Spring Data JPA DTO Projections](https://vladmihalcea.com/spring-jpa-dto-projection/)
- [Vlad Mihalcea - Spring Data Query Methods](https://vladmihalcea.com/spring-data-query-methods/)
- [Vlad Mihalcea - Spring Transaction Best Practices](https://vladmihalcea.com/spring-transaction-best-practices/)
- [Vlad Mihalcea - ManyToOne Best Practices](https://vladmihalcea.com/manytoone-jpa-hibernate/)

Browse [vladmihalcea.com/blog](https://vladmihalcea.com/blog/) for deep-dive articles.
