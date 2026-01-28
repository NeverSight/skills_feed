---
name: java-dev
description: "Comprehensive Java development skill based on Alibaba Java Coding Guidelines (Songshan Edition). Use when writing, reviewing, or refactoring Java code to ensure compliance with industry best practices. Triggers on: (1) Writing new Java code (.java files), (2) Reviewing existing Java code, (3) Refactoring Java projects, (4) Database design with MySQL, (5) API design and implementation, (6) Unit testing, (7) Concurrent programming, (8) Security implementation, or any Java development tasks requiring adherence to coding standards."
---

# Java Development - Alibaba Coding Guidelines

## Overview

This skill provides comprehensive Java development guidance based on the Alibaba Java Coding Guidelines (Songshan Edition). It ensures all Java code follows industry best practices covering naming conventions, coding standards, concurrency, exception handling, database design, security, testing, and architectural design.

## Core Principles

When writing Java code, always follow these fundamental principles:

1. **Code Readability**: Write code that is easy to understand and maintain
2. **Consistency**: Follow consistent naming and formatting conventions
3. **Safety First**: Prevent common pitfalls like NPE, SQL injection, and concurrency issues
4. **Performance Awareness**: Consider performance implications of design decisions
5. **Test Coverage**: Ensure adequate unit test coverage for critical code

## Quick Reference

### Naming Conventions
- **Classes**: UpperCamelCase (e.g., `UserService`, `OrderController`)
- **Methods/Variables**: lowerCamelCase (e.g., `getUserById`, `userName`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `MAX_COUNT`, `DEFAULT_SIZE`)
- **Packages**: lowercase, single word preferred (e.g., `com.company.module`)

### Common Patterns
- Abstract classes: `Abstract*` or `Base*` prefix
- Exception classes: `*Exception` suffix
- Test classes: `*Test` suffix
- Service implementations: `*Impl` suffix
- Boolean variables: No `is` prefix in POJO classes
- DAO methods: `get*` (single), `list*` (multiple), `count*`, `save*`, `remove*`, `update*`

### Critical Rules
- ❌ Never use magic numbers directly in code
- ❌ Never catch exceptions without handling them
- ❌ Never use `==` to compare wrapper types (use `equals()`)
- ❌ Never create threads directly (use thread pools)
- ❌ Never use `SELECT *` in SQL queries
- ✅ Always use parameterized queries to prevent SQL injection
- ✅ Always specify initial capacity for collections when size is known
- ✅ Always close resources in `finally` blocks or use try-with-resources
- ✅ Always validate external inputs

## Workflow

### 1. Before Writing Code

**Check the detailed guidelines:**
- For naming rules → See [naming-conventions.md](references/naming-conventions.md)
- For coding standards → See [coding-standards.md](references/coding-standards.md)
- For concurrency → See [concurrency.md](references/concurrency.md)
- For database design → See [database.md](references/database.md)
- For security → See [security.md](references/security.md)
- For testing → See [testing.md](references/testing.md)
- For design patterns → See [design.md](references/design.md)

### 2. Writing Code

Apply the following checks as you write:

**Naming**
- Class names use UpperCamelCase
- Method/variable names use lowerCamelCase
- Constants use UPPER_SNAKE_CASE
- Meaningful English names (no pinyin)

**Code Structure**
- Methods under 80 lines
- Single responsibility per class/method
- Proper access modifiers (private by default)
- Use `@Override` for overridden methods

**Common Pitfalls to Avoid**
```java
// ❌ Wrong: Magic numbers
if (status == 1) { ... }

// ✅ Correct: Named constants
private static final int STATUS_ACTIVE = 1;
if (status == STATUS_ACTIVE) { ... }

// ❌ Wrong: Comparing wrapper types with ==
Integer a = 128;
Integer b = 128;
if (a == b) { ... }  // May fail!

// ✅ Correct: Use equals()
if (a.equals(b)) { ... }

// ❌ Wrong: Empty catch block
try {
    doSomething();
} catch (Exception e) {
    // Silent failure
}

// ✅ Correct: Handle or rethrow
try {
    doSomething();
} catch (Exception e) {
    logger.error("Failed to do something", e);
    throw new BusinessException("Operation failed", e);
}

// ❌ Wrong: Creating threads directly
new Thread(() -> doWork()).start();

// ✅ Correct: Use thread pool
ExecutorService executor = new ThreadPoolExecutor(
    corePoolSize, maxPoolSize, keepAliveTime,
    TimeUnit.SECONDS, new LinkedBlockingQueue<>(),
    new ThreadFactoryBuilder().setNameFormat("worker-%d").build()
);
executor.submit(() -> doWork());
```

### 3. Database Operations

**Table Design**
- Table names: lowercase with underscores (e.g., `user_order`)
- Required fields: `id`, `create_time`, `update_time`
- Boolean fields: `is_*` prefix (e.g., `is_deleted`)
- Use `BIGINT UNSIGNED` for IDs
- Use `DECIMAL` for monetary values (never `FLOAT` or `DOUBLE`)

**SQL Best Practices**
```java
// ✅ Correct: Parameterized query
String sql = "SELECT id, user_name, email FROM user WHERE id = ?";
PreparedStatement ps = conn.prepareStatement(sql);
ps.setLong(1, userId);

// ✅ Correct: MyBatis parameter binding
@Select("SELECT * FROM user WHERE user_name = #{userName}")
User selectByUserName(@Param("userName") String userName);

// ❌ Wrong: String concatenation (SQL injection risk!)
String sql = "SELECT * FROM user WHERE user_name = '" + userName + "'";
```

### 4. Exception Handling

**Exception Hierarchy**
- Use specific exception types
- Checked exceptions for recoverable errors
- Unchecked exceptions for programming errors
- Always include context in exception messages

```java
// ✅ Correct exception handling
public User getUserById(Long userId) {
    if (userId == null) {
        throw new IllegalArgumentException("userId cannot be null");
    }

    User user = userDao.selectById(userId);
    if (user == null) {
        throw new NotFoundException("User not found: " + userId);
    }

    return user;
}

// ✅ Correct logging with exception
try {
    processOrder(order);
} catch (Exception e) {
    logger.error("Failed to process order, orderId: {}", order.getId(), e);
    throw new BusinessException("订单处理失败", e);
}
```

### 5. Concurrency

**Thread Safety Rules**
- Use `ThreadPoolExecutor` instead of `Executors`
- Name your threads for debugging
- Use `volatile` for visibility, `AtomicXxx` for atomic operations
- Avoid `SimpleDateFormat` in multi-threaded code (use `DateTimeFormatter`)
- Clean up `ThreadLocal` variables

```java
// ✅ Correct: Thread pool with proper configuration
ThreadPoolExecutor executor = new ThreadPoolExecutor(
    10,  // corePoolSize
    20,  // maximumPoolSize
    60L, // keepAliveTime
    TimeUnit.SECONDS,
    new LinkedBlockingQueue<>(100),
    new ThreadFactoryBuilder().setNameFormat("order-processor-%d").build(),
    new ThreadPoolExecutor.CallerRunsPolicy()
);

// ✅ Correct: ThreadLocal cleanup
private static final ThreadLocal<User> USER_CONTEXT = new ThreadLocal<>();

public void processRequest() {
    try {
        USER_CONTEXT.set(getCurrentUser());
        // Process request
    } finally {
        USER_CONTEXT.remove();  // Critical: prevent memory leak
    }
}
```

### 6. Security

**Input Validation**
- Validate all external inputs
- Use parameterized queries (never string concatenation)
- Sanitize HTML output to prevent XSS
- Implement CSRF protection
- Mask sensitive data in logs

```java
// ✅ Correct: Input validation
public void createUser(UserCreateRequest request) {
    if (StringUtils.isBlank(request.getUserName())) {
        throw new ValidationException("用户名不能为空");
    }
    if (!ValidationUtils.isValidMobile(request.getMobile())) {
        throw new ValidationException("手机号格式不正确");
    }
    // Process...
}

// ✅ Correct: Sensitive data masking
logger.info("User login, mobile: {}", maskMobile(user.getMobile()));
```

### 7. Unit Testing

**Testing Standards**
- Test class naming: `*Test`
- Test method naming: `test*`
- Target coverage: 70% statement coverage minimum
- Use JUnit 5 + Mockito
- Follow BCDE principle (Border, Correct, Design, Error)

```java
@ExtendWith(MockitoExtension.class)
public class UserServiceTest {

    @Mock
    private UserDao userDao;

    @InjectMocks
    private UserService userService;

    @Test
    @DisplayName("根据ID获取用户 - 正常情况")
    public void testGetUserById_Success() {
        // Given
        Long userId = 1L;
        User mockUser = new User();
        mockUser.setId(userId);
        mockUser.setUserName("test");
        when(userDao.selectById(userId)).thenReturn(mockUser);

        // When
        User result = userService.getUserById(userId);

        // Then
        assertNotNull(result);
        assertEquals(userId, result.getId());
        verify(userDao, times(1)).selectById(userId);
    }

    @Test
    @DisplayName("根据ID获取用户 - 参数为null")
    public void testGetUserById_NullParameter() {
        assertThrows(IllegalArgumentException.class, () -> {
            userService.getUserById(null);
        });
    }
}
```

## Code Review Checklist

When reviewing Java code, verify:

### Naming & Style
- [ ] Class names use UpperCamelCase
- [ ] Method/variable names use lowerCamelCase
- [ ] Constants use UPPER_SNAKE_CASE
- [ ] No magic numbers in code
- [ ] Meaningful English names (no pinyin)

### Code Quality
- [ ] Methods under 80 lines
- [ ] Single responsibility principle followed
- [ ] Proper access modifiers used
- [ ] No duplicate code
- [ ] Proper exception handling

### Safety
- [ ] No NPE risks (null checks where needed)
- [ ] Wrapper types compared with `equals()`, not `==`
- [ ] Resources properly closed (try-with-resources or finally)
- [ ] Thread-safe if used in concurrent context
- [ ] Input validation for external data

### Database
- [ ] Parameterized queries (no SQL injection risk)
- [ ] Specific columns selected (no `SELECT *`)
- [ ] Proper indexes defined
- [ ] Transaction boundaries correct

### Performance
- [ ] Collection initial capacity specified when size known
- [ ] String concatenation uses `StringBuilder` in loops
- [ ] Appropriate data structures chosen
- [ ] No unnecessary object creation in loops

### Testing
- [ ] Unit tests exist for new code
- [ ] Edge cases covered
- [ ] Exception cases tested
- [ ] Mock dependencies properly

## Reference Documentation

For detailed guidelines on specific topics, consult these reference documents:

### [naming-conventions.md](references/naming-conventions.md)
Complete naming rules for classes, methods, variables, packages, and domain models.

### [coding-standards.md](references/coding-standards.md)
Detailed coding standards including constants, formatting, OOP rules, date/time handling, collections, and control statements.

### [concurrency.md](references/concurrency.md)
Comprehensive concurrency guidelines covering thread pools, locks, volatile, concurrent collections, and common patterns.

### [exception-logging.md](references/exception-logging.md)
Exception handling best practices and logging standards using SLF4J.

### [database.md](references/database.md)
MySQL database design rules, indexing strategies, SQL optimization, and ORM mapping conventions.

### [security.md](references/security.md)
Security guidelines covering input validation, SQL injection prevention, XSS protection, CSRF defense, encryption, and sensitive data handling.

### [testing.md](references/testing.md)
Unit testing standards, frameworks (JUnit 5, Mockito), coverage requirements, and testing patterns.

### [design.md](references/design.md)
Design principles, layered architecture, domain models, design patterns, and API design conventions.

## Common Scenarios

### Scenario 1: Creating a New Service Class

1. Read [naming-conventions.md](references/naming-conventions.md) for service naming rules
2. Read [coding-standards.md](references/coding-standards.md) for class structure
3. Read [exception-logging.md](references/exception-logging.md) for error handling
4. Implement following the patterns shown above
5. Add unit tests following [testing.md](references/testing.md)

### Scenario 2: Database Table Design

1. Read [database.md](references/database.md) for table design rules
2. Ensure required fields: `id`, `create_time`, `update_time`
3. Use proper data types (DECIMAL for money, BIGINT for IDs)
4. Add appropriate indexes
5. Create corresponding DO class following naming conventions

### Scenario 3: Implementing Concurrent Processing

1. Read [concurrency.md](references/concurrency.md) for thread pool configuration
2. Use `ThreadPoolExecutor` with proper parameters
3. Name threads for debugging
4. Handle exceptions in worker threads
5. Clean up ThreadLocal variables

### Scenario 4: Security Review

1. Read [security.md](references/security.md) for security checklist
2. Verify input validation exists
3. Check for SQL injection vulnerabilities
4. Ensure sensitive data is masked in logs
5. Verify authentication and authorization

## Integration with Development Workflow

This skill integrates seamlessly into your development process:

1. **During Development**: Reference quick rules above and detailed guidelines as needed
2. **Code Review**: Use the checklist to ensure compliance
3. **Refactoring**: Apply guidelines to improve existing code
4. **Onboarding**: Use as training material for new team members

## Summary

This skill ensures all Java code adheres to Alibaba's industry-standard coding guidelines. Always prioritize:
- **Readability** over cleverness
- **Safety** over convenience
- **Maintainability** over quick fixes
- **Standards** over personal preference

When in doubt, consult the detailed reference documents for specific guidance.
