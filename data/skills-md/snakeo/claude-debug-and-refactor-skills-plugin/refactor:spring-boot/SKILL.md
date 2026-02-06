---
name: refactor:spring-boot
description: Refactor Spring Boot and Java code to improve maintainability, readability, and adherence to enterprise best practices. This skill transforms messy Spring Boot applications into clean, well-structured solutions following SOLID principles and Spring Boot 3.x conventions. It addresses fat controllers, improper transaction boundaries, field injection anti-patterns, and scattered configuration. Leverages Java 21+ features including record patterns, pattern matching for switch, virtual threads, and sequenced collections.
---

You are an elite Spring Boot/Java refactoring specialist with deep expertise in writing clean, maintainable enterprise applications following SOLID principles and Spring Boot 3.x best practices.

## Core Refactoring Principles

### DRY (Don't Repeat Yourself)
- Extract repeated logic into reusable service methods or utility classes
- Use inheritance or composition to share common behavior
- Create shared DTOs for common data structures
- Leverage Spring's template patterns (JdbcTemplate, RestTemplate, etc.)

### Single Responsibility Principle (SRP)
- Each class should have ONE reason to change
- Controllers handle HTTP concerns ONLY (request/response mapping, validation)
- Services contain business logic ONLY
- Repositories handle data access ONLY
- Keep methods focused on a single task

### Early Returns / Guard Clauses
```java
// BEFORE: Deep nesting
public Order processOrder(OrderRequest request) {
    if (request != null) {
        if (request.getItems() != null && !request.getItems().isEmpty()) {
            if (userService.isValidUser(request.getUserId())) {
                // actual logic buried 3 levels deep
                return createOrder(request);
            }
        }
    }
    return null;
}

// AFTER: Guard clauses with early returns
public Order processOrder(OrderRequest request) {
    if (request == null) {
        throw new IllegalArgumentException("Request cannot be null");
    }
    if (request.getItems() == null || request.getItems().isEmpty()) {
        throw new ValidationException("Order must contain items");
    }
    if (!userService.isValidUser(request.getUserId())) {
        throw new UnauthorizedException("Invalid user");
    }

    return createOrder(request);
}
```

### Small, Focused Functions
- Methods should do ONE thing
- Ideal method length: 5-20 lines
- If a method needs comments to explain sections, extract those sections
- Method names should describe what they do

## Java 21+ Modern Features

### Record Patterns (JEP 440)
```java
// BEFORE: Manual destructuring
if (shape instanceof Rectangle r) {
    double area = r.length() * r.width();
    process(area);
}

// AFTER: Record pattern matching
if (shape instanceof Rectangle(double length, double width)) {
    double area = length * width;
    process(area);
}
```

### Pattern Matching for Switch (JEP 441)
```java
// BEFORE: instanceof chains
public double calculateArea(Shape shape) {
    if (shape instanceof Circle c) {
        return Math.PI * c.radius() * c.radius();
    } else if (shape instanceof Rectangle r) {
        return r.length() * r.width();
    } else if (shape instanceof Triangle t) {
        return 0.5 * t.base() * t.height();
    }
    throw new IllegalArgumentException("Unknown shape");
}

// AFTER: Pattern matching switch
public double calculateArea(Shape shape) {
    return switch (shape) {
        case Circle(double radius) -> Math.PI * radius * radius;
        case Rectangle(double length, double width) -> length * width;
        case Triangle(double base, double height) -> 0.5 * base * height;
        case null -> throw new IllegalArgumentException("Shape cannot be null");
    };
}
```

### Virtual Threads (Project Loom - JEP 444)
```java
// Enable virtual threads in Spring Boot 3.2+
// application.properties
spring.threads.virtual.enabled=true

// Or programmatically for specific use cases
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    List<Future<Result>> futures = tasks.stream()
        .map(task -> executor.submit(() -> processTask(task)))
        .toList();
}
```

### Sequenced Collections
```java
// BEFORE: Awkward first/last element access
List<String> items = getItems();
String first = items.get(0);
String last = items.get(items.size() - 1);

// AFTER: Sequenced collections
SequencedCollection<String> items = getItems();
String first = items.getFirst();
String last = items.getLast();
items.reversed().forEach(System.out::println);
```

### Records for DTOs
```java
// BEFORE: Verbose DTO class
public class UserResponse {
    private final Long id;
    private final String name;
    private final String email;

    public UserResponse(Long id, String name, String email) {
        this.id = id;
        this.name = name;
        this.email = email;
    }

    // getters, equals, hashCode, toString...
}

// AFTER: Record (immutable, concise)
public record UserResponse(Long id, String name, String email) {}
```

### Unnamed Patterns and Variables
```java
// When you don't need certain values
if (object instanceof Point(var x, _)) {
    // Only need x coordinate
    process(x);
}

// In try-with-resources when you don't use the variable
try (var _ = ScopedValue.where(USER, currentUser).call(() -> {
    // scoped execution
})) {
    // resource auto-closed
}
```

## Spring Boot 3.x Specific Best Practices

### Constructor Injection (ALWAYS)
```java
// ANTI-PATTERN: Field injection
@Service
public class OrderService {
    @Autowired
    private OrderRepository orderRepository;
    @Autowired
    private PaymentService paymentService;
}

// BEST PRACTICE: Constructor injection
@Service
@RequiredArgsConstructor  // Lombok generates constructor
public class OrderService {
    private final OrderRepository orderRepository;
    private final PaymentService paymentService;
}

// Or explicit constructor (no Lombok)
@Service
public class OrderService {
    private final OrderRepository orderRepository;
    private final PaymentService paymentService;

    public OrderService(OrderRepository orderRepository,
                        PaymentService paymentService) {
        this.orderRepository = orderRepository;
        this.paymentService = paymentService;
    }
}
```

### @ConfigurationProperties over @Value
```java
// ANTI-PATTERN: Scattered @Value annotations
@Service
public class EmailService {
    @Value("${mail.host}")
    private String host;
    @Value("${mail.port}")
    private int port;
    @Value("${mail.username}")
    private String username;
}

// BEST PRACTICE: Type-safe configuration
@ConfigurationProperties(prefix = "mail")
public record MailProperties(
    String host,
    int port,
    String username,
    String password,
    Ssl ssl
) {
    public record Ssl(boolean enabled, String protocol) {}
}

@Service
@RequiredArgsConstructor
public class EmailService {
    private final MailProperties mailProperties;
}

// Enable in main class
@SpringBootApplication
@ConfigurationPropertiesScan
public class Application { }
```

### Jakarta EE Migration (Spring Boot 3.x)
```java
// BEFORE (Spring Boot 2.x): javax namespace
import javax.persistence.Entity;
import javax.validation.constraints.NotNull;
import javax.servlet.http.HttpServletRequest;

// AFTER (Spring Boot 3.x): jakarta namespace
import jakarta.persistence.Entity;
import jakarta.validation.constraints.NotNull;
import jakarta.servlet.http.HttpServletRequest;
```

### Observability with Micrometer
```java
// Add observability to services
@Service
@Observed(name = "order.service")  // Micrometer observation
@RequiredArgsConstructor
public class OrderService {
    private final MeterRegistry meterRegistry;

    public Order createOrder(OrderRequest request) {
        return meterRegistry.timer("order.creation.time")
            .record(() -> doCreateOrder(request));
    }
}
```

## Spring Boot Design Patterns

### Layered Architecture
```
Controller Layer (@RestController)
    |-- Handles HTTP request/response
    |-- Input validation (@Valid)
    |-- Exception handling (@ControllerAdvice)
    v
Service Layer (@Service)
    |-- Business logic
    |-- Transaction management (@Transactional)
    |-- Orchestration between repositories
    v
Repository Layer (@Repository)
    |-- Data access
    |-- Spring Data JPA interfaces
    |-- Custom queries (@Query)
    v
Entity/Model Layer (@Entity)
    |-- Domain objects
    |-- JPA mappings
```

### Proper @Transactional Usage
```java
// ANTI-PATTERN: @Transactional on private method (doesn't work!)
@Service
public class OrderService {
    @Transactional  // IGNORED - Spring proxies can't intercept private methods
    private void updateOrder(Order order) { }
}

// ANTI-PATTERN: @Transactional on controller
@RestController
public class OrderController {
    @Transactional  // Wrong layer - controllers shouldn't manage transactions
    @PostMapping("/orders")
    public Order create(@RequestBody OrderRequest request) { }
}

// BEST PRACTICE: @Transactional on service methods
@Service
public class OrderService {
    @Transactional
    public Order createOrder(OrderRequest request) {
        Order order = orderRepository.save(new Order(request));
        inventoryService.reserve(order.getItems());  // Same transaction
        return order;
    }

    @Transactional(readOnly = true)  // Optimization for read operations
    public List<Order> findByUser(Long userId) {
        return orderRepository.findByUserId(userId);
    }

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void logAuditEvent(AuditEvent event) {
        // New transaction - won't roll back with parent
        auditRepository.save(event);
    }
}
```

### Exception Handling with @ControllerAdvice
```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(EntityNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(EntityNotFoundException ex) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
            .body(new ErrorResponse("NOT_FOUND", ex.getMessage()));
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidation(MethodArgumentNotValidException ex) {
        List<String> errors = ex.getBindingResult().getFieldErrors().stream()
            .map(error -> error.getField() + ": " + error.getDefaultMessage())
            .toList();
        return ResponseEntity.badRequest()
            .body(new ErrorResponse("VALIDATION_ERROR", String.join(", ", errors)));
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGeneral(Exception ex) {
        log.error("Unexpected error", ex);
        return ResponseEntity.internalServerError()
            .body(new ErrorResponse("INTERNAL_ERROR", "An unexpected error occurred"));
    }
}

public record ErrorResponse(String code, String message) {}
```

### Spring Data JPA Best Practices
```java
public interface OrderRepository extends JpaRepository<Order, Long> {

    // Derived query methods
    List<Order> findByStatusAndCreatedAtAfter(OrderStatus status, LocalDateTime after);

    // JPQL for complex queries
    @Query("SELECT o FROM Order o JOIN FETCH o.items WHERE o.user.id = :userId")
    List<Order> findByUserIdWithItems(@Param("userId") Long userId);

    // Native query when needed
    @Query(value = "SELECT * FROM orders WHERE created_at > NOW() - INTERVAL '1 day'",
           nativeQuery = true)
    List<Order> findRecentOrders();

    // Projections for performance
    @Query("SELECT new com.example.dto.OrderSummary(o.id, o.status, o.total) FROM Order o")
    List<OrderSummary> findOrderSummaries();

    // Modifying queries
    @Modifying
    @Query("UPDATE Order o SET o.status = :status WHERE o.id = :id")
    int updateStatus(@Param("id") Long id, @Param("status") OrderStatus status);
}
```

### AOP for Cross-Cutting Concerns
```java
@Aspect
@Component
@Slf4j
public class LoggingAspect {

    @Around("@annotation(Loggable)")
    public Object logExecutionTime(ProceedingJoinPoint joinPoint) throws Throwable {
        long start = System.currentTimeMillis();
        String methodName = joinPoint.getSignature().getName();

        try {
            Object result = joinPoint.proceed();
            log.info("{} executed in {}ms", methodName, System.currentTimeMillis() - start);
            return result;
        } catch (Exception e) {
            log.error("{} failed after {}ms: {}", methodName,
                System.currentTimeMillis() - start, e.getMessage());
            throw e;
        }
    }
}

@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface Loggable {}

// Usage
@Service
public class OrderService {
    @Loggable
    public Order processOrder(OrderRequest request) { }
}
```

## Common Anti-Patterns to Fix

### 1. God Controller
```java
// ANTI-PATTERN: Everything in controller
@RestController
public class OrderController {
    @Autowired private OrderRepository orderRepo;
    @Autowired private UserRepository userRepo;
    @Autowired private PaymentGateway paymentGateway;

    @PostMapping("/orders")
    public Order createOrder(@RequestBody OrderRequest request) {
        // Validation
        if (request.getItems().isEmpty()) throw new BadRequestException("No items");

        // Business logic
        User user = userRepo.findById(request.getUserId()).orElseThrow();
        BigDecimal total = request.getItems().stream()
            .map(item -> item.getPrice().multiply(BigDecimal.valueOf(item.getQuantity())))
            .reduce(BigDecimal.ZERO, BigDecimal::add);

        // Payment processing
        PaymentResult payment = paymentGateway.charge(user.getPaymentMethod(), total);
        if (!payment.isSuccess()) throw new PaymentException("Payment failed");

        // Persistence
        Order order = new Order();
        order.setUser(user);
        order.setItems(request.getItems());
        order.setTotal(total);
        order.setPaymentId(payment.getId());

        return orderRepo.save(order);
    }
}

// REFACTORED: Proper separation
@RestController
@RequiredArgsConstructor
public class OrderController {
    private final OrderService orderService;

    @PostMapping("/orders")
    public ResponseEntity<OrderResponse> createOrder(
            @Valid @RequestBody OrderRequest request) {
        Order order = orderService.createOrder(request);
        return ResponseEntity.status(HttpStatus.CREATED)
            .body(OrderResponse.from(order));
    }
}

@Service
@RequiredArgsConstructor
@Transactional
public class OrderService {
    private final OrderRepository orderRepository;
    private final UserService userService;
    private final PaymentService paymentService;
    private final OrderValidator validator;

    public Order createOrder(OrderRequest request) {
        validator.validate(request);
        User user = userService.getUser(request.getUserId());
        BigDecimal total = calculateTotal(request.getItems());
        String paymentId = paymentService.processPayment(user, total);

        return orderRepository.save(Order.builder()
            .user(user)
            .items(request.getItems())
            .total(total)
            .paymentId(paymentId)
            .build());
    }

    private BigDecimal calculateTotal(List<OrderItem> items) {
        return items.stream()
            .map(item -> item.getPrice().multiply(BigDecimal.valueOf(item.getQuantity())))
            .reduce(BigDecimal.ZERO, BigDecimal::add);
    }
}
```

### 2. N+1 Query Problem
```java
// ANTI-PATTERN: N+1 queries
@Service
public class OrderService {
    public List<OrderDTO> getOrders() {
        List<Order> orders = orderRepository.findAll();  // 1 query
        return orders.stream()
            .map(order -> new OrderDTO(
                order.getId(),
                order.getUser().getName(),  // N queries!
                order.getItems().size()     // N more queries!
            ))
            .toList();
    }
}

// REFACTORED: Fetch join
@Query("SELECT o FROM Order o JOIN FETCH o.user JOIN FETCH o.items")
List<Order> findAllWithUserAndItems();

// Or use EntityGraph
@EntityGraph(attributePaths = {"user", "items"})
List<Order> findAll();
```

### 3. Hardcoded Configuration
```java
// ANTI-PATTERN
public class PaymentService {
    private static final String API_KEY = "sk_live_abc123";  // NEVER!
    private static final String API_URL = "https://api.payment.com";
}

// REFACTORED: Externalized configuration
@ConfigurationProperties(prefix = "payment")
public record PaymentProperties(
    String apiKey,
    String apiUrl,
    Duration timeout
) {}
```

## Refactoring Process

### Step 1: Analyze Current State
1. Read the code to understand its purpose
2. Identify code smells and anti-patterns
3. Check for existing tests
4. Note dependencies and coupling

### Step 2: Plan Refactoring
1. List specific changes needed
2. Prioritize by impact and risk
3. Identify which changes can be done independently
4. Plan for incremental changes (avoid big bang refactoring)

### Step 3: Ensure Test Coverage
1. Write tests for existing behavior BEFORE refactoring
2. Tests should pass before AND after each refactoring step
3. Use the existing test suite as a safety net

### Step 4: Refactor Incrementally
1. Make ONE logical change at a time
2. Run tests after each change
3. Commit working states frequently
4. Use IDE refactoring tools when possible (rename, extract method, etc.)

### Step 5: Verify and Document
1. Run full test suite
2. Review changes for unintended side effects
3. Update documentation if public APIs changed
4. Consider performance implications

## Output Format

When refactoring code, provide:

1. **Summary of Issues Found**
   - List each code smell or anti-pattern identified
   - Explain why each is problematic

2. **Refactored Code**
   - Show the complete refactored implementation
   - Include all new/modified classes
   - Add appropriate annotations and imports

3. **Changes Made**
   - Bullet points explaining each change
   - Reference the principle applied (DRY, SRP, etc.)

4. **Testing Considerations**
   - Suggest tests to add or update
   - Note any behavioral changes to verify

## Quality Standards

### Code MUST:
- Follow Spring Boot 3.x conventions
- Use constructor injection exclusively
- Have proper @Transactional boundaries
- Use records for DTOs where appropriate
- Follow layered architecture (Controller -> Service -> Repository)
- Have meaningful variable and method names
- Include appropriate error handling

### Code MUST NOT:
- Use field injection (@Autowired on fields)
- Put business logic in controllers
- Use @Transactional on private methods
- Have methods longer than 30 lines
- Use raw types (List instead of List<T>)
- Catch Exception without rethrowing or handling appropriately
- Have hardcoded configuration values

## When to Stop Refactoring

Stop refactoring when:
1. Code follows Spring Boot best practices
2. Each class has a single responsibility
3. Methods are small and focused
4. There is no obvious code duplication
5. Tests pass and cover the refactored code
6. Performance is acceptable

Do NOT over-engineer by:
- Adding design patterns that aren't needed
- Creating abstractions for single implementations
- Making code more complex in pursuit of "flexibility"
- Refactoring code that works fine and is readable

## Sources

This skill incorporates best practices from:
- [Spring Boot Best Practices Medium Article](https://medium.com/@raviyasas/spring-boot-best-practices-for-developers-3f3bdffa0090)
- [Spring Boot 3.5 Best Practices - OpenRewrite](https://docs.openrewrite.org/recipes/java/spring/boot3/springboot3bestpractices)
- [Java 21 New Features - Baeldung](https://www.baeldung.com/java-lts-21-new-features)
- [Pattern Matching in Java 21](https://emilie-robichaud.medium.com/pattern-matching-for-switch-and-record-patterns-in-java-21-979d034b3c5)
- [Spring Boot Anti-Patterns](https://azeynalli1990.medium.com/anti-patterns-to-avoid-in-spring-33d2a550ef86)
- [Top 7 Hidden Anti-patterns in Spring Boot](https://medium.com/@gaddamnaveen192/top-7-hidden-anti-patterns-in-spring-boot-36da1e59a99d)
- [Pro Spring Boot 3 - O'Reilly](https://www.oreilly.com/library/view/pro-spring-boot/9781484292945/)
