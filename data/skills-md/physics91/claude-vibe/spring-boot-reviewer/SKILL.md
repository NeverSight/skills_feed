---
name: spring-boot-reviewer
description: |
  WHEN: Spring Boot code review, DI patterns, @Transactional, REST API design, security configuration
  WHAT: Dependency injection + Transaction management + API design + Security config + JPA patterns
  WHEN NOT: Kotlin Spring → kotlin-spring-reviewer, Pure Java → java-reviewer, Django/FastAPI → respective reviewers
---

# Spring Boot Reviewer Skill

## Purpose
Reviews Spring Boot applications for dependency injection patterns, transaction management, REST API design, security configuration, and JPA best practices.

## When to Use
- Spring Boot code review requests
- "Spring", "@Transactional", "JPA", "REST controller" mentions
- API security configuration review
- Projects with `spring-boot-starter-*` dependencies
- `@SpringBootApplication` class present

## Project Detection
- `spring-boot-starter-*` in pom.xml/build.gradle
- `@SpringBootApplication` annotation
- `application.yml` or `application.properties`
- `src/main/resources/application*.yml`

## Workflow

### Step 1: Analyze Project
```
**Spring Boot**: 3.2.x
**Java**: 17 / 21
**Dependencies**:
  - spring-boot-starter-web
  - spring-boot-starter-data-jpa
  - spring-boot-starter-security
  - spring-boot-starter-validation
```

### Step 2: Select Review Areas
**AskUserQuestion:**
```
"Which Spring Boot areas to review?"
Options:
- Full Spring Boot audit (recommended)
- Dependency Injection patterns
- Transaction management
- REST API design
- Security configuration
- JPA/Repository patterns
multiSelect: true
```

## Detection Rules

### Critical: Field Injection
| Pattern | Issue | Severity |
|---------|-------|----------|
| `@Autowired` on field | Not testable | HIGH |
| `@Inject` on field | Same issue | HIGH |
| `@Value` on field | Consider constructor | MEDIUM |

```java
// BAD: Field injection
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;

    @Autowired
    private EmailService emailService;
}

// GOOD: Constructor injection
@Service
public class UserService {
    private final UserRepository userRepository;
    private final EmailService emailService;

    public UserService(UserRepository userRepository,
                      EmailService emailService) {
        this.userRepository = userRepository;
        this.emailService = emailService;
    }
}

// BETTER: Lombok + constructor injection
@Service
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepository;
    private final EmailService emailService;
}
```

### Critical: JPA N+1 Query Problem
| Pattern | Issue | Severity |
|---------|-------|----------|
| Lazy load in loop | N+1 queries | CRITICAL |
| Missing `@EntityGraph` | Suboptimal fetching | HIGH |
| No `fetch join` | Multiple queries | HIGH |

```java
// BAD: N+1 problem
@Entity
public class Order {
    @OneToMany(mappedBy = "order", fetch = FetchType.LAZY)
    private List<OrderItem> items;
}

// In service - N+1 queries!
List<Order> orders = orderRepository.findAll();
for (Order order : orders) {
    order.getItems().size();  // Triggers query per order
}

// GOOD: Fetch join in repository
@Query("SELECT o FROM Order o JOIN FETCH o.items WHERE o.status = :status")
List<Order> findByStatusWithItems(@Param("status") OrderStatus status);

// GOOD: @EntityGraph
@EntityGraph(attributePaths = {"items", "customer"})
List<Order> findByStatus(OrderStatus status);

// GOOD: Batch fetching
@Entity
public class Order {
    @OneToMany(mappedBy = "order")
    @BatchSize(size = 20)  // Fetch 20 at a time
    private List<OrderItem> items;
}
```

### Critical: Missing Security
| Pattern | Issue | Severity |
|---------|-------|----------|
| No `@PreAuthorize` | Unauthorized access | CRITICAL |
| Hardcoded credentials | Security breach | CRITICAL |
| Exposed Actuator endpoints | Info/control leak | CRITICAL |
| Missing CSRF config | CSRF vulnerable | HIGH |
| No rate limiting | DoS vulnerable | HIGH |
| Entity returned from Controller | Data leak / OSIV | HIGH |

```java
// BAD: No authorization check
@RestController
@RequestMapping("/api/admin")
public class AdminController {
    @GetMapping("/users")
    public List<User> getAllUsers() {  // Anyone can access!
        return userService.findAll();
    }
}

// GOOD: Method-level security
@RestController
@RequestMapping("/api/admin")
public class AdminController {
    @GetMapping("/users")
    @PreAuthorize("hasRole('ADMIN')")
    public List<User> getAllUsers() {
        return userService.findAll();
    }
}

// Security configuration
@Configuration
@EnableWebSecurity
@EnableMethodSecurity
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/public/**").permitAll()
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .csrf(csrf -> csrf.csrfTokenRepository(
                CookieCsrfTokenRepository.withHttpOnlyFalse()))
            .build();
    }
}
```

### High: Controller with Business Logic
| Pattern | Issue | Severity |
|---------|-------|----------|
| DB access in controller | Layer violation | HIGH |
| Complex logic in controller | Not testable | HIGH |
| Transaction in controller | Wrong layer | HIGH |

```java
// BAD: Business logic in controller
@RestController
@RequestMapping("/api/orders")
public class OrderController {
    @Autowired
    private OrderRepository orderRepository;

    @PostMapping
    @Transactional  // Wrong layer!
    public Order createOrder(@RequestBody CreateOrderRequest request) {
        // Business logic in controller
        if (request.getItems().isEmpty()) {
            throw new BadRequestException("Items required");
        }

        Order order = new Order();
        order.setCustomerId(request.getCustomerId());

        BigDecimal total = BigDecimal.ZERO;
        for (ItemRequest item : request.getItems()) {
            total = total.add(item.getPrice().multiply(
                BigDecimal.valueOf(item.getQuantity())));
        }
        order.setTotal(total);

        return orderRepository.save(order);
    }
}

// GOOD: Thin controller, service layer
@RestController
@RequestMapping("/api/orders")
@RequiredArgsConstructor
public class OrderController {
    private final OrderService orderService;

    @PostMapping
    public ResponseEntity<OrderResponse> createOrder(
            @Valid @RequestBody CreateOrderRequest request) {
        Order order = orderService.create(request);
        return ResponseEntity.created(
            URI.create("/api/orders/" + order.getId()))
            .body(OrderResponse.from(order));
    }
}

@Service
@RequiredArgsConstructor
public class OrderService {
    private final OrderRepository orderRepository;

    @Transactional  // Correct layer
    public Order create(CreateOrderRequest request) {
        // Business logic here
        Order order = buildOrder(request);
        return orderRepository.save(order);
    }
}
```

### High: Missing @Transactional
| Pattern | Issue | Severity |
|---------|-------|----------|
| Multiple saves without txn | Partial commit | HIGH |
| Self-invocation of @Transactional | Proxy bypassed | CRITICAL |
| Read without `readOnly` | Missed optimization | MEDIUM |
| Wrong propagation | Unexpected behavior | HIGH |

```java
// BAD: No transaction - partial failure
@Service
public class TransferService {
    public void transfer(Long fromId, Long toId, BigDecimal amount) {
        Account from = accountRepository.findById(fromId).orElseThrow();
        Account to = accountRepository.findById(toId).orElseThrow();

        from.setBalance(from.getBalance().subtract(amount));
        accountRepository.save(from);
        // Exception here = money lost!
        to.setBalance(to.getBalance().add(amount));
        accountRepository.save(to);
    }
}

// GOOD: Transactional
@Service
public class TransferService {
    @Transactional
    public void transfer(Long fromId, Long toId, BigDecimal amount) {
        Account from = accountRepository.findById(fromId).orElseThrow();
        Account to = accountRepository.findById(toId).orElseThrow();

        from.setBalance(from.getBalance().subtract(amount));
        to.setBalance(to.getBalance().add(amount));
        // Both or nothing
    }
}

// GOOD: readOnly for queries
@Transactional(readOnly = true)
public List<Account> findAll() {
    return accountRepository.findAll();
}

// GOOD: Propagation for nested transactions
@Transactional(propagation = Propagation.REQUIRES_NEW)
public void logAudit(String action) {
    // Commits even if outer transaction rolls back
}

// CRITICAL: Self-invocation bypasses proxy
@Service
public class OrderService {
    @Transactional
    public void processOrder(Order order) {
        // ...
        this.sendNotification(order);  // BAD: @Transactional ignored!
    }

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void sendNotification(Order order) {
        // This runs WITHOUT a new transaction due to self-invocation
    }
}

// GOOD: Inject self or use separate service
@Service
public class OrderService {
    private final NotificationService notificationService;  // Separate bean

    @Transactional
    public void processOrder(Order order) {
        notificationService.sendNotification(order);  // Proxy works
    }
}
```

### High: Missing DTO Validation
| Pattern | Issue | Severity |
|---------|-------|----------|
| No `@Valid` on request | Unvalidated input | HIGH |
| Missing validation annotations | Bad data accepted | HIGH |
| No error handling | 500 on validation fail | MEDIUM |

```java
// BAD: No validation
@PostMapping("/users")
public User createUser(@RequestBody CreateUserRequest request) {
    // name could be null, email invalid
    return userService.create(request);
}

// GOOD: Validated request
public record CreateUserRequest(
    @NotBlank(message = "Name is required")
    @Size(max = 100, message = "Name too long")
    String name,

    @NotBlank
    @Email(message = "Invalid email format")
    String email,

    @NotNull
    @Min(value = 0, message = "Age must be positive")
    @Max(value = 150, message = "Invalid age")
    Integer age
) {}

@PostMapping("/users")
public ResponseEntity<UserResponse> createUser(
        @Valid @RequestBody CreateUserRequest request) {
    return ResponseEntity.ok(userService.create(request));
}

// Global exception handler
@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidation(
            MethodArgumentNotValidException ex) {
        List<String> errors = ex.getBindingResult()
            .getFieldErrors().stream()
            .map(error -> error.getField() + ": " + error.getDefaultMessage())
            .toList();
        return ResponseEntity.badRequest()
            .body(new ErrorResponse("Validation failed", errors));
    }
}
```

### High: Hardcoded Configuration
| Pattern | Issue | Severity |
|---------|-------|----------|
| Hardcoded URL in code | Not configurable | HIGH |
| Hardcoded credentials | Security risk | CRITICAL |
| Magic numbers | Maintainability | MEDIUM |

```java
// BAD: Hardcoded configuration
@Service
public class ExternalApiService {
    private final String apiUrl = "https://api.example.com";  // Hardcoded
    private final String apiKey = "sk-secret-key";  // CRITICAL!
    private final int timeout = 5000;
}

// GOOD: Externalized configuration
@Configuration
@ConfigurationProperties(prefix = "external-api")
@Validated
public class ExternalApiProperties {
    @NotBlank
    private String url;

    @NotBlank
    private String apiKey;

    @Min(100)
    @Max(60000)
    private int timeout = 5000;

    // getters, setters
}

@Service
@RequiredArgsConstructor
public class ExternalApiService {
    private final ExternalApiProperties properties;

    public void call() {
        // Use properties.getUrl(), etc.
    }
}

// application.yml
external-api:
  url: ${EXTERNAL_API_URL}
  api-key: ${EXTERNAL_API_KEY}
  timeout: 5000
```

### Critical: WebFlux Blocking Calls
| Pattern | Issue | Severity |
|---------|-------|----------|
| JDBC in WebFlux | Blocks event loop | CRITICAL |
| Thread.sleep() | Blocks thread | CRITICAL |
| Blocking I/O | Performance death | CRITICAL |

```java
// BAD: Blocking call in reactive stack
@RestController
public class ReactiveController {
    @Autowired
    private JdbcTemplate jdbcTemplate;  // Blocking!

    @GetMapping("/users")
    public Mono<List<User>> getUsers() {
        // Blocks event loop thread!
        List<User> users = jdbcTemplate.query(...);
        return Mono.just(users);
    }
}

// GOOD: Use R2DBC for reactive DB access
@RestController
@RequiredArgsConstructor
public class ReactiveController {
    private final UserRepository userRepository;  // R2DBC

    @GetMapping("/users")
    public Flux<User> getUsers() {
        return userRepository.findAll();  // Non-blocking
    }
}

// If must use blocking: subscribeOn(Schedulers.boundedElastic())
@GetMapping("/legacy")
public Mono<String> callLegacy() {
    return Mono.fromCallable(() -> legacyBlockingService.call())
        .subscribeOn(Schedulers.boundedElastic());
}
```

### Medium: Missing API Versioning
| Pattern | Issue | Severity |
|---------|-------|----------|
| No version in URL | Breaking changes | MEDIUM |
| No version header | Hard to evolve | MEDIUM |

```java
// BAD: No versioning
@RestController
@RequestMapping("/api/users")
public class UserController { }

// GOOD: URL versioning
@RestController
@RequestMapping("/api/v1/users")
public class UserControllerV1 { }

@RestController
@RequestMapping("/api/v2/users")
public class UserControllerV2 { }

// ALTERNATIVE: Header versioning
@RestController
@RequestMapping("/api/users")
public class UserController {
    @GetMapping(headers = "X-API-Version=1")
    public List<UserV1Response> getUsersV1() { }

    @GetMapping(headers = "X-API-Version=2")
    public List<UserV2Response> getUsersV2() { }
}
```

## Response Template
```
## Spring Boot Code Review Results

**Project**: [name]
**Spring Boot**: 3.2.x | **Java**: 17
**Profile**: [dev/prod]

### Dependency Injection

#### HIGH
| File | Line | Issue |
|------|------|-------|
| UserService.java | 12 | Field injection with @Autowired |
| OrderService.java | 8 | Multiple @Autowired fields |

### Transaction Management
| File | Line | Issue |
|------|------|-------|
| TransferService.java | 34 | Missing @Transactional on multi-save |
| ReportService.java | 56 | Read method without readOnly=true |

### JPA/Repository
| File | Line | Issue |
|------|------|-------|
| OrderService.java | 23 | N+1 query in loop |
| ProductService.java | 45 | Missing fetch join |

### Security
| File | Line | Issue |
|------|------|-------|
| AdminController.java | 12 | Missing @PreAuthorize |
| application.yml | 34 | Hardcoded API key |

### REST API
| File | Line | Issue |
|------|------|-------|
| UserController.java | 23 | Business logic in controller |
| OrderController.java | 45 | Missing @Valid on request body |

### Recommendations
1. [ ] Replace field injection with constructor injection
2. [ ] Add @Transactional to service methods
3. [ ] Fix N+1 with @EntityGraph or fetch join
4. [ ] Add method-level security annotations
5. [ ] Move business logic to service layer

### Positive Patterns
- Good use of @ConfigurationProperties
- Proper exception handling with @RestControllerAdvice
```

## Best Practices
1. **Constructor Injection**: Always prefer over field injection
2. **Service Layer**: Keep controllers thin
3. **Transactions**: At service layer, readOnly for queries
4. **Validation**: @Valid on all request bodies
5. **Security**: Method-level with @PreAuthorize
6. **Configuration**: Externalize all config values

## Integration
- `java-reviewer` skill: Java idioms
- `kotlin-spring-reviewer` skill: Kotlin Spring
- `orm-reviewer` skill: JPA deep dive
- `security-scanner` skill: Security audit

## Notes
- Based on Spring Boot 3.x best practices
- Assumes Spring Security 6.x
- Works with both MVC and WebFlux
- Compatible with Java 17+ and Kotlin
