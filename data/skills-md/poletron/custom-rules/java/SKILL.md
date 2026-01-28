---
name: java
description: >
  Java programming with Spring Boot, Maven, and modern Java 17+ features.
  Trigger: When developing Java/Spring Boot applications.
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [root]
  auto_invoke: "Working with java"

## When to Use

Use this skill when:
- Building Spring Boot 3.x applications
- Using Java 17+ features (records, sealed classes)
- Implementing REST APIs with Spring
- Writing JUnit 5 tests

---

## Critical Patterns

### Constructor Injection (REQUIRED)

```java
// ✅ ALWAYS: Constructor injection for testability
@Service
public class OrderService {
    private final OrderRepository repository;
    private final PaymentService paymentService;
    
    public OrderService(OrderRepository repository, PaymentService paymentService) {
        this.repository = repository;
        this.paymentService = paymentService;
    }
}

// ❌ NEVER: Field injection
@Service
public class OrderService {
    @Autowired
    private OrderRepository repository;
}
```

### Records for DTOs (REQUIRED)

```java
// ✅ ALWAYS: Use records for immutable DTOs
public record UserDTO(
    String id,
    String name,
    String email
) {}

// ❌ NEVER: Mutable POJOs for data transfer
public class UserDTO {
    private String id;
    // ... getters, setters, equals, hashCode
}
```

### Exception Handling (REQUIRED)

```java
// ✅ ALWAYS: Use @ControllerAdvice
@ControllerAdvice
public class GlobalExceptionHandler {
    
    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(ResourceNotFoundException ex) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
            .body(new ErrorResponse(ex.getMessage()));
    }
}
```

---

## Decision Tree

```
Need REST API?          → Use @RestController
Need data validation?   → Use @Valid + Bean Validation
Need database access?   → Use Spring Data JPA
Need async processing?  → Use @Async
Need caching?           → Use @Cacheable
Need config properties? → Use @ConfigurationProperties
```

---

## Code Examples

### REST Controller

```java
@RestController
@RequestMapping("/api/users")
public class UserController {
    
    private final UserService userService;
    
    public UserController(UserService userService) {
        this.userService = userService;
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<UserDTO> getUser(@PathVariable String id) {
        return userService.findById(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }
    
    @PostMapping
    public ResponseEntity<UserDTO> createUser(@Valid @RequestBody CreateUserRequest request) {
        UserDTO created = userService.create(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }
}
```

### Bean Validation

```java
public record CreateUserRequest(
    @NotBlank(message = "Name is required")
    String name,
    
    @Email(message = "Invalid email format")
    @NotBlank
    String email,
    
    @Size(min = 8, message = "Password must be at least 8 characters")
    String password
) {}
```

---

## Commands

```bash
mvn clean install              # Build project
mvn spring-boot:run            # Run application
mvn test                       # Run tests
mvn dependency:tree            # View dependencies
./mvnw spring-boot:run         # Run with wrapper
```

---

## Resources

- **Spring Boot Docs**: https://spring.io/projects/spring-boot
