---
name: java-best-practices
description: Use this skill when working with Java code, Optional handling, CompletableFuture, records, sealed classes, or virtual threads.
version: 1.0.0
---

# Java Best Practices

Guidance for writing type-safe, concurrent, and modern Java code targeting Java 17+ and Java 21 LTS. Covers null safety, concurrency patterns, and modern language features.

## Core Principles

1. **Null safety first**: Use Optional for return values, @Nullable/@NonNull for parameters
2. **Immutability preferred**: Use records for data carriers, final fields where possible
3. **Explicit error handling**: Use checked exceptions sparingly, prefer Result patterns
4. **Modern features**: Leverage records, sealed classes, and pattern matching
5. **Virtual threads for IO**: Use virtual threads (Java 21) for IO-bound operations

## Type Safety

### Use Optional for Return Values

```java
// Good - explicit absence representation
public Optional<User> findById(String id) {
    User user = userRepository.findById(id);
    return Optional.ofNullable(user);
}

// Bad - null return
public User findById(String id) {
    return userRepository.findById(id); // May return null
}
```

### Never Use Optional as Parameter or Field

```java
// Bad - Optional as parameter
public void processUser(Optional<User> user) { ... }

// Good - use @Nullable annotation or overloading
public void processUser(@Nullable User user) { ... }
public void processUser(User user) { ... } // Overload for non-null

// Bad - Optional as field
private Optional<String> middleName;

// Good - nullable field with annotation
@Nullable
private String middleName;
```

### Use Null Safety Annotations

```java
import org.jspecify.annotations.Nullable;
import org.jspecify.annotations.NonNull;

// Good - explicit null contract
public @NonNull User createUser(@NonNull String name, @Nullable String email) {
    Objects.requireNonNull(name, "name cannot be null");
    return new User(name, email);
}
```

### Defensive Coding with Objects.requireNonNull

```java
public class UserService {
    private final UserRepository repository;
    private final EmailService emailService;

    // Good - fail-fast validation in constructor
    public UserService(UserRepository repository, EmailService emailService) {
        this.repository = Objects.requireNonNull(repository, "repository cannot be null");
        this.emailService = Objects.requireNonNull(emailService, "emailService cannot be null");
    }
}
```

## Null Handling

### Optional Transformation with map/flatMap

```java
// Good - chained transformations
String city = findUserById(id)
    .map(User::getAddress)
    .map(Address::getCity)
    .orElse("Unknown");

// Good - flatMap for Optional-returning methods
Optional<Order> latestOrder = findUserById(id)
    .flatMap(User::getLatestOrder);
```

### Prefer orElseGet for Expensive Defaults

```java
// Good - lazy evaluation for expensive default
User user = findUserById(id)
    .orElseGet(() -> userService.createDefaultUser());

// Bad - always evaluates default
User user = findUserById(id)
    .orElse(userService.createDefaultUser()); // Always creates default user!
```

### Use orElseThrow for Required Values

```java
// Good - explicit exception for missing required value
User user = findUserById(id)
    .orElseThrow(() -> new UserNotFoundException("User not found: " + id));

// Good - Java 10+ simplified version
User user = findUserById(id)
    .orElseThrow(); // Throws NoSuchElementException
```

### Avoid Optional.get() Without Check

```java
// Bad - may throw NoSuchElementException
User user = findUserById(id).get();

// Good - use orElseThrow with meaningful exception
User user = findUserById(id)
    .orElseThrow(() -> new IllegalStateException("Expected user to exist"));

// Good - check presence first if needed
Optional<User> userOpt = findUserById(id);
if (userOpt.isPresent()) {
    User user = userOpt.get();
    // ...
}

// Better - use ifPresent or map
findUserById(id).ifPresent(user -> {
    // Process user
});
```

### Filter with Optional

```java
// Good - combine filter with map
Optional<String> activeUserEmail = findUserById(id)
    .filter(User::isActive)
    .map(User::getEmail);

// Equivalent to
Optional<String> activeUserEmail = findUserById(id)
    .flatMap(user -> user.isActive()
        ? Optional.of(user.getEmail())
        : Optional.empty());
```

### Optional in Streams

```java
// Good - filter out empty Optionals (Java 9+)
List<User> users = userIds.stream()
    .map(this::findUserById)
    .flatMap(Optional::stream)
    .toList();

// Pre-Java 9
List<User> users = userIds.stream()
    .map(this::findUserById)
    .filter(Optional::isPresent)
    .map(Optional::get)
    .collect(Collectors.toList());
```

## Concurrency

### CompletableFuture Basics

```java
// Good - create async operations
CompletableFuture<User> future = CompletableFuture.supplyAsync(() -> {
    return userRepository.findById(id);
});

// Good - chain transformations
CompletableFuture<String> emailFuture = future
    .thenApply(User::getEmail)
    .thenApply(String::toLowerCase);

// Good - combine multiple futures
CompletableFuture<UserProfile> profile = CompletableFuture
    .allOf(userFuture, ordersFuture, preferencesFuture)
    .thenApply(v -> new UserProfile(
        userFuture.join(),
        ordersFuture.join(),
        preferencesFuture.join()
    ));
```

### CompletableFuture Error Handling

```java
// Good - handle errors with exceptionally
CompletableFuture<User> userFuture = fetchUserAsync(id)
    .exceptionally(ex -> {
        log.error("Failed to fetch user: {}", id, ex);
        return User.anonymous();
    });

// Good - handle with recovery
CompletableFuture<User> userFuture = fetchUserAsync(id)
    .handle((user, ex) -> {
        if (ex != null) {
            log.warn("Fetch failed, using cache", ex);
            return userCache.get(id);
        }
        return user;
    });

// Good - chain error handling with whenComplete
fetchUserAsync(id)
    .whenComplete((user, ex) -> {
        if (ex != null) {
            metrics.incrementFailure();
        } else {
            metrics.incrementSuccess();
        }
    });
```

### Parallel Execution with CompletableFuture

```java
// Good - execute multiple operations in parallel
public CompletableFuture<DashboardData> loadDashboard(String userId) {
    CompletableFuture<User> userFuture = fetchUserAsync(userId);
    CompletableFuture<List<Order>> ordersFuture = fetchOrdersAsync(userId);
    CompletableFuture<List<Notification>> notificationsFuture = fetchNotificationsAsync(userId);

    return CompletableFuture.allOf(userFuture, ordersFuture, notificationsFuture)
        .thenApply(v -> new DashboardData(
            userFuture.join(),
            ordersFuture.join(),
            notificationsFuture.join()
        ));
}

// Good - first to complete wins
CompletableFuture<String> fastest = CompletableFuture.anyOf(
    fetchFromPrimary(),
    fetchFromSecondary(),
    fetchFromCache()
).thenApply(result -> (String) result);
```

### Virtual Threads (Java 21)

```java
// Good - virtual threads for IO-bound tasks
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    List<Future<String>> futures = urls.stream()
        .map(url -> executor.submit(() -> fetchUrl(url)))
        .toList();

    List<String> results = new ArrayList<>();
    for (Future<String> future : futures) {
        results.add(future.get());
    }
}

// Good - structured concurrency (Java 21 preview)
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Subtask<User> userTask = scope.fork(() -> fetchUser(id));
    Subtask<List<Order>> ordersTask = scope.fork(() -> fetchOrders(id));

    scope.join();
    scope.throwIfFailed();

    return new UserWithOrders(userTask.get(), ordersTask.get());
}
```

### When to Use Virtual Threads

```java
// Good use case - many concurrent IO operations
// Each virtual thread blocks on IO without consuming OS thread
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    // Can handle thousands of concurrent requests efficiently
    List<Future<Response>> responses = requests.stream()
        .map(req -> executor.submit(() -> httpClient.send(req)))
        .toList();
}

// Bad use case - CPU-bound computation
// Use platform threads or ForkJoinPool for CPU-intensive work
ForkJoinPool.commonPool().submit(() -> {
    // Heavy computation here
});
```

### ExecutorService Patterns

```java
// Good - bounded thread pool with rejection handling
ExecutorService executor = new ThreadPoolExecutor(
    4,                      // core pool size
    8,                      // max pool size
    60, TimeUnit.SECONDS,   // keep-alive time
    new ArrayBlockingQueue<>(100),  // bounded queue
    new ThreadPoolExecutor.CallerRunsPolicy()  // rejection policy
);

// Good - always shutdown executors
try {
    // Submit tasks
} finally {
    executor.shutdown();
    if (!executor.awaitTermination(30, TimeUnit.SECONDS)) {
        executor.shutdownNow();
    }
}

// Better - use try-with-resources (Java 19+)
try (var executor = Executors.newFixedThreadPool(4)) {
    // Submit tasks
} // Auto-shutdown
```

### Thread Safety Patterns

```java
// Good - immutable objects are thread-safe
public record User(String id, String name, String email) {}

// Good - use concurrent collections
private final ConcurrentHashMap<String, User> userCache = new ConcurrentHashMap<>();
private final CopyOnWriteArrayList<EventListener> listeners = new CopyOnWriteArrayList<>();

// Good - atomic operations
private final AtomicInteger counter = new AtomicInteger(0);
private final AtomicReference<Config> config = new AtomicReference<>(defaultConfig);

// Good - use locks for complex operations
private final ReentrantReadWriteLock lock = new ReentrantReadWriteLock();

public User getUser(String id) {
    lock.readLock().lock();
    try {
        return userCache.get(id);
    } finally {
        lock.readLock().unlock();
    }
}

public void updateUser(User user) {
    lock.writeLock().lock();
    try {
        userCache.put(user.id(), user);
    } finally {
        lock.writeLock().unlock();
    }
}
```

### Async Error Handling Patterns

```java
// Good - Result type for async operations
public sealed interface AsyncResult<T> {
    record Success<T>(T value) implements AsyncResult<T> {}
    record Failure<T>(Throwable error) implements AsyncResult<T> {}
}

public CompletableFuture<AsyncResult<User>> fetchUserSafe(String id) {
    return fetchUserAsync(id)
        .<AsyncResult<User>>thenApply(AsyncResult.Success::new)
        .exceptionally(AsyncResult.Failure::new);
}

// Good - timeout handling
CompletableFuture<User> userFuture = fetchUserAsync(id)
    .orTimeout(5, TimeUnit.SECONDS)
    .exceptionally(ex -> {
        if (ex instanceof TimeoutException) {
            return User.anonymous();
        }
        throw new CompletionException(ex);
    });

// Good - retry with exponential backoff
public <T> CompletableFuture<T> withRetry(
        Supplier<CompletableFuture<T>> operation,
        int maxRetries,
        Duration initialDelay) {

    return operation.get().exceptionallyCompose(ex -> {
        if (maxRetries <= 0) {
            return CompletableFuture.failedFuture(ex);
        }
        return CompletableFuture
            .delayedExecutor(initialDelay.toMillis(), TimeUnit.MILLISECONDS)
            .execute(() -> {});
        // Continue with recursive retry...
    });
}
```

## Modern Java Features

### Records (Java 17+)

```java
// Good - immutable data carrier with automatic equals, hashCode, toString
public record User(String id, String name, String email) {}

// Good - compact constructor for validation
public record User(String id, String name, String email) {
    public User {
        Objects.requireNonNull(id, "id cannot be null");
        Objects.requireNonNull(name, "name cannot be null");
        if (email != null && !email.contains("@")) {
            throw new IllegalArgumentException("Invalid email format");
        }
    }
}

// Good - add computed properties
public record Rectangle(double width, double height) {
    public double area() {
        return width * height;
    }

    public double perimeter() {
        return 2 * (width + height);
    }
}

// Good - static factory methods
public record Point(int x, int y) {
    public static Point origin() {
        return new Point(0, 0);
    }

    public static Point of(int x, int y) {
        return new Point(x, y);
    }
}
```

### When to Use Records

```java
// Good use cases for records:
// 1. DTOs (Data Transfer Objects)
public record UserDTO(String id, String name, String email) {}

// 2. Value objects
public record Money(BigDecimal amount, Currency currency) {}

// 3. API responses
public record ApiResponse<T>(T data, int status, String message) {}

// 4. Configuration objects
public record DatabaseConfig(String host, int port, String database) {}

// 5. Compound map keys
public record CacheKey(String userId, String resourceType) {}

// Bad use cases - don't use records when:
// - You need mutable state
// - You need inheritance
// - You need custom equals/hashCode that differs from all fields
```

### Sealed Classes (Java 17+)

```java
// Good - restrict inheritance hierarchy
public sealed interface Shape
    permits Circle, Rectangle, Triangle {

    double area();
}

public record Circle(double radius) implements Shape {
    @Override
    public double area() {
        return Math.PI * radius * radius;
    }
}

public record Rectangle(double width, double height) implements Shape {
    @Override
    public double area() {
        return width * height;
    }
}

public record Triangle(double base, double height) implements Shape {
    @Override
    public double area() {
        return 0.5 * base * height;
    }
}
```

### Sealed Classes for Result Types

```java
// Good - algebraic data type pattern
public sealed interface Result<T>
    permits Result.Success, Result.Failure {

    record Success<T>(T value) implements Result<T> {}
    record Failure<T>(String error, Throwable cause) implements Result<T> {
        public Failure(String error) {
            this(error, null);
        }
    }

    default T getOrThrow() {
        return switch (this) {
            case Success<T> s -> s.value();
            case Failure<T> f -> throw new RuntimeException(f.error(), f.cause());
        };
    }

    default T getOrElse(T defaultValue) {
        return switch (this) {
            case Success<T> s -> s.value();
            case Failure<T> f -> defaultValue;
        };
    }
}
```

### Pattern Matching for instanceof (Java 17+)

```java
// Good - pattern matching eliminates cast
public String describe(Object obj) {
    if (obj instanceof String s) {
        return "String of length " + s.length();
    }
    if (obj instanceof Integer i) {
        return "Integer: " + i;
    }
    if (obj instanceof List<?> list && !list.isEmpty()) {
        return "Non-empty list with " + list.size() + " elements";
    }
    return "Unknown: " + obj;
}

// Bad - old style with explicit cast
public String describeOld(Object obj) {
    if (obj instanceof String) {
        String s = (String) obj;  // Redundant cast
        return "String of length " + s.length();
    }
    // ...
}
```

### Pattern Matching in Switch (Java 21+)

```java
// Good - exhaustive pattern matching
public double calculateArea(Shape shape) {
    return switch (shape) {
        case Circle c -> Math.PI * c.radius() * c.radius();
        case Rectangle r -> r.width() * r.height();
        case Triangle t -> 0.5 * t.base() * t.height();
    };
}

// Good - with guards
public String categorize(Shape shape) {
    return switch (shape) {
        case Circle c when c.radius() > 100 -> "Large circle";
        case Circle c -> "Small circle";
        case Rectangle r when r.width() == r.height() -> "Square";
        case Rectangle r -> "Rectangle";
        case Triangle t -> "Triangle";
    };
}

// Good - null handling in switch (Java 21+)
public String process(String input) {
    return switch (input) {
        case null -> "Input is null";
        case String s when s.isBlank() -> "Input is blank";
        case String s -> "Input: " + s;
    };
}
```

### Switch Expressions (Java 17+)

```java
// Good - switch as expression
public String getDayType(DayOfWeek day) {
    return switch (day) {
        case MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY -> "Weekday";
        case SATURDAY, SUNDAY -> "Weekend";
    };
}

// Good - with yield for complex cases
public int calculate(Operation op, int a, int b) {
    return switch (op) {
        case ADD -> a + b;
        case SUBTRACT -> a - b;
        case MULTIPLY -> a * b;
        case DIVIDE -> {
            if (b == 0) {
                throw new ArithmeticException("Division by zero");
            }
            yield a / b;
        }
    };
}
```

## Quick Reference: Modern Features Checklist

- [ ] Use records for immutable data carriers (DTOs, value objects)
- [ ] Add validation in compact constructors
- [ ] Use sealed classes to restrict type hierarchies
- [ ] Combine sealed interfaces with records for algebraic data types
- [ ] Use pattern matching with instanceof to avoid explicit casts
- [ ] Use switch expressions instead of switch statements
- [ ] Leverage exhaustive pattern matching with sealed types
- [ ] Use guards in switch patterns for conditional matching

## Quick Reference: Concurrency Checklist

- [ ] Use `CompletableFuture` for async operations, not raw threads
- [ ] Handle errors with `exceptionally()` or `handle()`
- [ ] Use `allOf()` for parallel operations that all must complete
- [ ] Use virtual threads (Java 21) for IO-bound tasks
- [ ] Use platform threads/ForkJoinPool for CPU-bound tasks
- [ ] Always shutdown ExecutorService in finally block or try-with-resources
- [ ] Prefer immutable objects and records for thread safety
- [ ] Use concurrent collections instead of synchronized wrappers
- [ ] Add timeouts to async operations with `orTimeout()`
- [ ] Implement retry logic for transient failures

## Quick Reference: Type Safety Checklist

- [ ] Return `Optional<T>` for potentially absent values
- [ ] Never use `Optional` as method parameter or field
- [ ] Use `@Nullable`/`@NonNull` annotations consistently
- [ ] Validate non-null parameters with `Objects.requireNonNull()`
- [ ] Prefer `orElseGet()` over `orElse()` for expensive defaults
- [ ] Use `orElseThrow()` for required values
- [ ] Never call `Optional.get()` without checking presence
- [ ] Use `map()`/`flatMap()` for Optional transformations
