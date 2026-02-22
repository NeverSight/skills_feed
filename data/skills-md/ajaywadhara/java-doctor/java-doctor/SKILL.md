---
name: java-doctor
description: Comprehensive Java code health analyzer. 0-100 score with diagnostics. Progressive loading - detects project tech (Spring, gRPC, JPA) and loads relevant rules. Version-aware for Java 8-25 & Spring Boot 3.x/4.x. Dead code detection included. Use when reviewing Java code, finding bugs, or preparing for PR.
license: MIT
compatibility: Java 8+, git
metadata:
  author: Ajay Wadhara
  version: "1.2"
  triggers:
    - run java doctor
    - scan my java code
    - java code review
    - find bugs in java
    - check for security issues in java
    - find performance problems
    - check for dead code
allowed-tools: Bash(git:*) Read Write Glob Grep Edit question
---

# Java Doctor - Comprehensive Java Code Health Analyzer

You are an expert Java code reviewer. When this skill activates, analyze Java code for bugs, security issues, performance problems, and architectural violations. Output a 0-100 score with actionable diagnostics.

## Your Task - Progressive Analysis Workflow

### Step 1: Detect Project Technologies (ALWAYS RUN FIRST)

Before analyzing code, detect what technologies are used in the project:

**Check these files to detect technologies:**
- `pom.xml` - Maven dependencies
- `build.gradle` or `build.gradle.kts` - Gradle dependencies
- `build.xml` - Ant (legacy)
- `pom.xml` - Check for grpc, spring, jakarta keywords
- `build.gradle` - Check for plugins and dependencies

**Technology Detection Patterns:**

| Technology | Maven (pom.xml) | Gradle | Detection Priority |
|------------|-----------------|--------|-------------------|
| Spring Boot | `spring-boot-starter-parent` | `id("org.springframework.boot")` | HIGH |
| Spring Framework | `spring-context`, `spring-web` | `spring-context`, `spring-web` | HIGH |
| Jakarta EE | `jakarta.*` | `jakarta.*` | HIGH |
| gRPC | `grpc-java`, `grpc-protobuf` | `grpc-java` | HIGH |
| JPA/Hibernate | `spring-data-jpa`, `hibernate-core` | `spring-data-jpa` | MEDIUM |
| JUnit | `junit-jupiter`, `junit` | `junit-jupiter` | MEDIUM |
| Testcontainers | `testcontainers` | `testcontainers` | LOW |
| Lombok | `lombok` | `lombok` | LOW |
| Kotlin | N/A | `kotlin("stdlib")` | LOW |

### Step 2: Load Relevant Rules Based on Detection

**Load rules incrementally:**

1. **ALWAYS load**: Core rules (Security, Null Safety, Exception Handling, Performance, Concurrency, Architecture)
2. **If Spring Boot detected**: Load Spring/Boot 4.x rules
3. **If gRPC detected**: Load gRPC rules
4. **If JPA detected**: Load JPA/Hibernate rules
5. **If Lombok detected**: Load Lombok rules
6. **Always load**: Google Checkstyle rules

### Step 3: Ask for Missing Information

If technologies cannot be detected:

```
Question: "I couldn't detect all technologies in your project. Which technologies are you using?"
Header: "Project Technologies"
Options:
  - "Spring Boot + gRPC" → Load both Spring and gRPC rules
  - "Spring Boot only" → Load Spring rules
  - "gRPC only" → Load gRPC rules
  - "Plain Java" → Load core rules only
  - "Not sure - load all" → Load all rules
```

## Core Rules (Always Load)

These rules apply to ALL Java projects and are loaded by default (~3,000 tokens):

### 1. Security (16 rules)
### 2. Null Safety (8 rules)  
### 3. Exception Handling (8 rules)
### 4. Performance (12 rules)
### 5. Concurrency (12 rules)
### 6. Architecture (10 rules)
### 7. Logging (7 rules)
### 8. Google Checkstyle (35 rules)

## Technology-Specific Rules (Load On-Demand)

### 9. Spring Framework / Spring Boot (23 rules)
**Load if Spring detected:** pom.xml contains `spring-boot` or `spring-context`

### 10. gRPC Java (26 rules)
**Load if gRPC detected:** pom.xml contains `grpc-java` or `grpc-protobuf`

### 11. JPA / Hibernate (15 rules)
**Load if JPA detected:** pom.xml contains `hibernate` or `spring-data-jpa`

### 12. Lombok (5 rules)
**Load if Lombok detected:** pom.xml contains `lombok`

### 13. Build Tools - Maven/Gradle (20 rules)
**Always check:** Check pom.xml or build.gradle for best practices

## Java Version Detection

**Detect Java version** by checking:
- `pom.xml` - Look for `<java.version>` or `<maven.compiler.source>`
- `build.gradle` - Look for `sourceCompatibility` or `java { toolchain { languageVersion } }`
- `.java-version` or `SDKMAN` config

**If version cannot be detected from any of these sources, ASK the user:**

```
Question: "I couldn't detect the Java version from your project. Which Java version is your project using?"
Header: "Java Version"
Options:
  - "Java 8 (1.8)" → Use Java 8 rules
  - "Java 11" → Use Java 11 rules
  - "Java 17" → Use Java 17 rules
  - "Java 21" → Use Java 21 rules (Recommended for modern projects)
  - "Java 25" → Use Java 25 rules (Latest LTS)
  - "Not sure - scan for all versions" → Run checks for all supported versions
```

**Also detect Spring Boot version** (if Spring Boot project):
- `pom.xml` - Look for `<parent><version>` with `spring-boot-starter-parent`
- `build.gradle` - Look for `springBootVersion` or `id("org.springframework.boot") version "x.x.x"`

```
Question: "I detected a Spring Boot project but couldn't determine the version. Which Spring Boot version are you using?"
Header: "Spring Boot Version"
Options:
  - "Spring Boot 3.x" → Use Spring Boot 3.x rules (Jakarta EE 9+, Security 6.x)
  - "Spring Boot 4.x" → Use Spring Boot 4.x rules (Jakarta EE 11, Security 7.x)
  - "Not sure" → Run checks for both versions
```

**Version-Specific Checks:**

| Version | Specific Checks |
|---------|-----------------|
| Java 8 | Stream API usage, lambda best practices, try-with-resources, Optional |
| Java 11 | Local-Variable Type Inference (var), String improvements, Files.readString() |
| Java 17 | Sealed classes, Pattern matching for instanceof, Records basics |
| Java 21 | Virtual threads, Sequenced collections, Record patterns, Pattern matching for switch |
| Java 25 | Scoped Values (JEP 506), Primitive Patterns (JEP 507), Flexible Constructor Bodies (JEP 513), Stable Values (JEP 502), Module Import Declarations (JEP 511) |

**Virtual Threads (Java 21+):**
- Use `Thread.ofVirtual().start()` or `Executors.newVirtualThreadPerTaskExecutor()`
- Replace `newFixedThreadPool` with virtual thread executors for I/O-bound tasks
- Do NOT use `Thread.sleep()` in virtual threads (use `LockSupport.parkNanos()`)

---

## Spring Boot Version Detection

**Also detect Spring Boot version** by checking:
- `pom.xml` - Look for `<parent><version>` with `spring-boot-starter-parent`
- `build.gradle` - Look for `springBootVersion` in `ext` or `plugins { id 'org.springframework.boot' }`
- `build.gradle` - Look for `id("org.springframework.boot") version "x.x.x"`
- `application.properties/yml` - Check `spring-boot.version` property

**If Spring Boot version detected:**

| Version | Specific Checks |
|---------|-----------------|
| Spring Boot 3.x | Jakarta EE 9+, Spring Security 6.x, Jackson 2.x |
| Spring Boot 4.x | Jakarta EE 11, Spring Security 7.x, Jackson 3.x, JUnit 6, Observability starter |

---

## Score Calculation

**Base Score: 100** (Starts perfect, deduct points for issues)

| Severity | Deduction | Example |
|----------|-----------|---------|
| CRITICAL | -15 each | Security vulnerability, NPE risk, resource leak |
| ERROR | -10 each | Missing null check, improper exception handling |
| WARNING | -5 each | Code smell, performance concern, missing @Override |
| SUGGESTION | -2 each | Style improvement, Effective Java recommendation |

**Score Ranges:**
- **75-100**: Great - Production-ready code
- **50-74**: Needs Work - Address warnings before release
- **0-49**: Critical - Blockers must be fixed

---

## Rule Categories (~260 rules)

**Progressive Loading:**
- Core Rules (~100 tokens) - Always loaded
- Spring/Boot Rules (~500 tokens) - Loaded if Spring detected
- gRPC Rules (~600 tokens) - Loaded if gRPC detected
- JPA Rules (~300 tokens) - Loaded if JPA detected
- Build Rules (~200 tokens) - Always checked

### 1. Security (CRITICAL - Always Check First)

| Rule ID | Issue | Severity | Fix |
|---------|-------|----------|-----|
| SEC-001 | Hardcoded passwords/secrets/keys | CRITICAL | Use environment variables or config |
| SEC-002 | SQL injection (string concatenation in queries) | CRITICAL | Use parameterized queries |
| SEC-003 | Sensitive data in logs (passwords, tokens, PII) | CRITICAL | Mask sensitive fields |
| SEC-004 | Missing input validation on public methods | ERROR | Add @Valid, Bean Validation |
| SEC-005 | Weak cryptographic algorithms (MD5, SHA1) | CRITICAL | Use SHA-256+, AES-256 |
| SEC-006 | Missing authentication/authorization checks | CRITICAL | Add security annotations |
| SEC-007 | XML External Entity (XXE) vulnerability | CRITICAL | Disable external entities |
| SEC-008 | Deserialization of untrusted data | CRITICAL | Use whitelisting, ObjectInputFilter |
| SEC-009 | Path traversal vulnerability | CRITICAL | Validate and sanitize paths |
| SEC-010 | Missing CORS configuration on public APIs | WARNING | Explicit CORS policy |
| SEC-011 | Weak password hashing (MD5, SHA1 for passwords) | CRITICAL | Use BCrypt, Argon2, PBKDF2 |
| SEC-012 | Insecure random number generation | ERROR | Use SecureRandom |
| SEC-013 | Hardcoded salt for hashing | WARNING | Use random salt per user |
| SEC-014 | Trust boundary violation | WARNING | Validate all cross-boundary data |
| SEC-015 | LDAP injection | CRITICAL | Sanitize LDAP input |
| SEC-016 | XPath injection | CRITICAL | Use parameterized XPath |

### 2. Null Safety & Correctness

| Rule ID | Issue | Severity | Fix |
|---------|-------|----------|-----|
| NULL-001 | Optional.get() without isPresent check | CRITICAL | Use orElseThrow(), orElse() |
| NULL-002 | Null check on primitive wrapper (autoboxing) | ERROR | Use Optional, default values |
| NULL-003 | Returning null instead of empty collection | WARNING | Return empty collection |
| NULL-004 | Null parameter without validation | ERROR | Add null checks, @NonNull |
| NULL-005 | Chained method calls without null guards | ERROR | Use Optional chaining |
| NULL-006 | Overloading with null parameters | WARNING | Use method overloading carefully |
| NULL-007 | Null-safety annotation missing (@NonNull, @Nullable) | SUGGESTION | Add null annotations |
| NULL-008 | Mutable fields that should be immutable | WARNING | Make final, use builder |

### 3. Exception Handling

| Rule ID | Issue | Severity | Fix |
|---------|-------|----------|-----|
| EXC-001 | Swallowed exceptions (empty catch block) | ERROR | Log and rethrow, or handle |
| EXC-002 | Catching generic Exception/Throwable | WARNING | Catch specific exceptions |
| EXC-003 | Throwing generic RuntimeException | WARNING | Use specific exception types |
| EXC-004 | Swallowing InterruptedException | WARNING | Restore interrupt flag |
| EXC-005 | Not using try-with-resources | ERROR | Use try-with-resources |
| EXC-006 | Finally block returning or throwing | CRITICAL | Move outside finally |
| EXC-007 | Exception catching order (subclass after super) | WARNING | Catch subclass first |
| EXC-008 | Suppressed exceptions not handled | WARNING | Handle via getSuppressed() |

### 4. Performance

| Rule ID | Issue | Severity | Fix |
|---------|-------|----------|-----|
| PERF-001 | N+1 query problem | CRITICAL | Use JOIN FETCH, EntityGraph |
| PERF-002 | EAGER fetching on collections | ERROR | Use LAZY, fetch explicitly |
| PERF-003 | String concatenation in loops | ERROR | Use StringBuilder |
| PERF-004 | Boxing/Unboxing in loops | WARNING | Use primitive streams |
| PERF-005 | Creating unnecessary objects | WARNING | Reuse, use flyweight |
| PERF-006 | Missing database indexes (in comments) | WARNING | Add index hints |
| PERF-007 | Large blob/clob in entity | WARNING | Use LAZY, separate table |
| PERF-008 | Unclosed streams, connections, files | CRITICAL | Use try-with-resources |
| PERF-009 | Synchronized on mutable objects | ERROR | Use immutable objects |
| PERF-010 | HashMap in concurrent environment | ERROR | Use ConcurrentHashMap |
| PERF-011 | Inefficient collection: LinkedList for random access | WARNING | Use ArrayList |
| PERF-012 | toArray() without generic type | WARNING | Use toArray(new Type[0]) |

### 5. Concurrency & Thread Safety

| Rule ID | Issue | Severity | Fix |
|---------|-------|----------|-----|
| CONC-001 | Shared mutable state between threads | CRITICAL | Use immutability, synchronization |
| CONC-002 | Double-checked locking broken (pre-Java 5) | CRITICAL | Use volatile or eager init |
| CONC-003 | Starting thread in constructor | CRITICAL | Use lazy initialization |
| CONC-004 | Calling overridable methods from constructor | ERROR | Use initializer blocks |
| CONC-005 | Missing volatile on shared variables | ERROR | Add volatile keyword |
| CONC-006 | Using Thread.stop() | CRITICAL | Use interruption pattern |
| CONC-007 | Not handling InterruptedException | WARNING | Restore interrupt status |
| CONC-008 | ExecutorService not shutdown | ERROR | Call shutdown(), awaitTermination() |
| CONC-009 | Future.get() without timeout | WARNING | Use timeout to prevent deadlock |
| CONC-010 | Blocking operations in synchronized block | WARNING | Use java.util.concurrent |
| CONC-011 | Using wait()/notify() instead of java.util.concurrent | WARNING | Use higher-level utilities |
| CONC-012 | Race condition in concurrent collection modification | CRITICAL | Use atomic operations or concurrent collections |

### 6. Resource Management

| Rule ID | Issue | Severity | Fix |
|---------|-------|----------|-----|
| RES-001 | Unclosed FileInputStream/FileOutputStream | CRITICAL | Use try-with-resources |
| RES-002 | Unclosed database connections | CRITICAL | Use try-with-resources, HikariCP |
| RES-003 | Unclosed ResultSet/Statement | CRITICAL | Use try-with-resources |
| RES-004 | Unclosed HTTP client connections | CRITICAL | Use try-with-resources, OkHttp |
| RES-005 | Unclosed streams in loops | CRITICAL | Use try-with-resources |
| RES-006 | Resource leak in exception path | CRITICAL | Use try-with-resources |
| RES-007 | InputStream/Reader not closed on exception | WARNING | Use try-with-resources |

### 7. Spring Framework Specific

| Rule ID | Issue | Severity | Fix |
|---------|-------|----------|-----|
| SPR-001 | @Transactional on private method | CRITICAL | Make public, use self-injection |
| SPR-002 | @Transactional without rollbackFor | WARNING | Specify exception types |
| SPR-003 | Returning JPA entity to controller | WARNING | Use DTO/MapStruct |
| SPR-004 | Missing @Transactional on data operations | ERROR | Add annotation |
| SPR-005 | Circular dependency | ERROR | Use @Lazy, refactor |
| SPR-006 | @Value on static field | CRITICAL | Use setter or @Bean |
| SPR-007 | @Autowired on optional dependency | WARNING | Use constructor injection |
| SPR-008 | Missing @ComponentScan for new packages | ERROR | Add package to scan |
| SPR-009 | @RequestBody without @Valid | WARNING | Add @Valid for validation |
| SPR-010 | Using @Scope("prototype") with singleton | ERROR | Use @Scope(proxy = ...) |

### 7.1 Spring Boot 4.x Specific (If Spring Boot 4.x detected)

| Rule ID | Issue | Severity | Fix |
|---------|-------|----------|-----|
| BOOT4-001 | Using @MockBean instead of @MockitoBean | WARNING | Use @MockitoBean from org.springframework.test.context.bean.override.mockito |
| BOOT4-002 | Using @SpyBean instead of @MockitoSpyBean | WARNING | Use @MockitoSpyBean from Spring Boot 4 |
| BOOT4-003 | Using javax.* instead of jakarta.* | ERROR | Migrate all javax.* imports to jakarta.* (Jakarta EE 11) |
| BOOT4-004 | Using TestRestTemplate | WARNING | Use RestTestClient in Spring Boot 4.x |
| BOOT4-005 | Using Jackson 2.x APIs | WARNING | Update to Jackson 3.x APIs (package changes) |
| BOOT4-006 | Using Spring Security 6.x config | WARNING | Update to Spring Security 7.x DSL |
| BOOT4-007 | Using deprecated actuator endpoints | WARNING | Use new observability endpoints |
| BOOT4-008 | Using spring-boot-starter-data-* without proper test config | WARNING | Update test configuration for Boot 4 |
| BOOT4-009 | Not using spring-boot-starter-opentelemetry | SUGGESTION | Use unified observability in Boot 4 |
| BOOT4-010 | Missing explicit @SpringBootTest configuration | WARNING | Use @TestPropertySource or properties in @SpringBootTest |
| BOOT4-011 | Using JUnit 4 assertions | WARNING | Use JUnit 5/6 assertions |
| BOOT4-012 | Using @DirtiesContext without proper handling | WARNING | Boot 4 handles test context caching better |
| BOOT4-013 | Using Spring Security 6.x lambda DSL | WARNING | Update to Security 7.x configuration |

### 8. Modern Java & Effective Java (Version Aware)

| Rule ID | Issue | Severity | Fix | Version |
|---------|-------|----------|-----|---------|
| EJ-001 | Using StringBuilder for 1-2 concatenations | SUGGESTION | Use + for simple cases | 8+ |
| EJ-002 | Using == on boxed primitives | WARNING | Use equals() | 8+ |
| EJ-003 | Missing Override annotation | WARNING | Add @Override | 8+ |
| EJ-004 | Static nested class instead of inner | SUGGESTION | Make static if no outer ref | 8+ |
| EJ-005 | Returning null instead of empty | WARNING | Return empty collection | 8+ |
| EJ-006 | Using raw types instead of generics | ERROR | Use generic type | 8+ |
| EJ-007 | Modifying collection during iteration | CRITICAL | Use iterator.remove() | 8+ |
| EJ-008 | Using notify() instead of notifyAll() | WARNING | Use notifyAll() | 8+ |
| EJ-009 | Class with many static methods (not utility) | SUGGESTION | Consider singleton | 8+ |
| EJ-010 | Implementing Comparable without compareTo | ERROR | Implement fully or not at all | 8+ |
| EJ-011 | Not using try-with-resources | ERROR | Use try-with-resources | 9+ |
| EJ-012 | Using var incorrectly (all lowercase) | SUGGESTION | var is lowercase, not Var | 10+ |
| EJ-013 | Using var with lambda (ambiguous) | WARNING | Explicit type needed | 10+ |
| EJ-014 | String.isBlank() not used | SUGGESTION | Use String.isBlank() | 11+ |
| EJ-015 | Files.readAllLines() not used | SUGGESTION | Use Files.readString() | 11+ |
| EJ-016 | Using new ArrayList<>(Arrays.asList()) | SUGGESTION | Use List.of() | 9+ |
| EJ-017 | Not using List.of(), Set.of(), Map.of() | SUGGESTION | Use immutable collections | 9+ |
| EJ-018 | Using Optional.isPresent() instead of orElse | WARNING | Use orElseThrow(), orElse() | 8+ |
| EJ-019 | Using Optional.get() | WARNING | Use orElseThrow() | 8+ |
| EJ-020 | Not using Stream API where appropriate | SUGGESTION | Consider streams | 8+ |
| EJ-021 | Using .forEach() with side effects | WARNING | Use for-loop if side effects | 8+ |
| EJ-022 | Not using method references | SUGGESTION | Use :: method references | 8+ |
| EJ-023 | Sealed class not using permits | WARNING | Add permits or remove sealed | 17+ |
| EJ-024 | Using instanceof without pattern matching | WARNING | Use pattern matching | 16+ |
| EJ-025 | Record not using canonical constructor | SUGGESTION | Consider compact constructor | 16+ |
| EJ-026 | Switch expression not used | SUGGESTION | Use switch expression | 14+ |
| EJ-027 | Text blocks not used for multiline | SUGGESTION | Use """ text blocks | 15+ |
| EJ-028 | Not using Optional for return types | WARNING | Use Optional<T> for optional | 8+ |
| EJ-029 | Using .map(x -> x) unnecessarily | SUGGESTION | Remove unnecessary map | 8+ |
| EJ-030 | Not using .orElseGet() for lazy default | WARNING | Use orElseGet() for expensive ops | 8+ |
| EJ-031 | Not using Scoped Values (JEP 506) | SUGGESTION | Use ScopedValue instead of ThreadLocal | 25+ |
| EJ-032 | Primitive patterns not used in instanceof (JEP 507) | SUGGESTION | Use primitive patterns in instanceof | 25+ |
| EJ-033 | Not using Stable Values (JEP 502) | SUGGESTION | Consider StableValue for immutable caching | 25+ |
| EJ-034 | Flexible constructor bodies not used (JEP 513) | SUGGESTION | Use flexible constructor bodies | 25+ |
| EJ-035 | Module import declarations not used (JEP 511) | SUGGESTION | Use module imports for cleaner code | 25+ |
| EJ-036 | Using traditional thread pools for I/O-bound tasks | SUGGESTION | Use virtual threads (Executors.newVirtualThreadPerTaskExecutor()) | 21+ |
| EJ-037 | ThreadLocal usage without considering ScopedValue | SUGGESTION | Consider ScopedValue for better inheritance | 25+ |

### 9. Architecture & Design

| Rule ID | Issue | Severity | Fix |
|---------|-------|----------|-----|
| ARCH-001 | God class (2000+ lines) | ERROR | Split into smaller classes |
| ARCH-002 | Method too long (200+ lines) | WARNING | Extract methods |
| ARCH-003 | Too many parameters (5+) | WARNING | Use builder/DTO |
| ARCH-004 | Feature envy (class uses too much of another) | WARNING | Move method to target class |
| ARCH-005 | Shotgun surgery (one change affects many) | WARNING | Reduce coupling |
| ARCH-006 | Duplicate code | WARNING | Extract to common method |
| ARCH-007 | Primitive obsession | WARNING | Use value objects |
| ARCH-008 | Improper package structure | WARNING | Follow clean architecture |
| ARCH-009 | Circular dependency between packages | ERROR | Refactor, use interfaces |
| ARCH-010 | Exposing internal representation | WARNING | Use encapsulation, DTOs |

### 10. Logging & Debugging

| Rule ID | Issue | Severity | Fix |
|---------|-------|----------|-----|
| LOG-001 | Using System.out.println() | WARNING | Use logger |
| LOG-002 | Using System.err.println() | WARNING | Use logger |
| LOG-003 | Logging sensitive data (passwords, tokens) | CRITICAL | Mask before logging |
| LOG-004 | Not logging exceptions with stack trace | WARNING | Include full exception |
| LOG-005 | Logging at wrong level (info for errors) | WARNING | Use appropriate level |
| LOG-006 | String concatenation in logger | WARNING | Use placeholder {} | 
| LOG-007 | Not using logger for debug info | SUGGESTION | Add debug logging |

### 11. Testing

| Rule ID | Issue | Severity | Fix |
|---------|-------|----------|-----|
| TEST-001 | Missing unit tests for service layer | WARNING | Add unit tests |
| TEST-002 | Not testing exception cases | WARNING | Add exception tests |
| TEST-003 | Using @RunWith(SpringRunner.class) | SUGGESTION | Use @SpringBootTest | 5.0+ |
| TEST-004 | Test without assertions | ERROR | Add assertions |
| TEST-005 | Hardcoded test data | SUGGESTION | Use test builders |
| TEST-006 | Not using @Transactional on integration tests | WARNING | Add for test isolation |
| TEST-007 | Mocking internal implementation details | WARNING | Test via public API |
| TEST-008 | Not using @ParameterizedTest | SUGGESTION | Parameterize tests | 5.0+ |

### 12. API Design & REST

| Rule ID | Issue | Severity | Fix |
|---------|-------|----------|-----|
| API-001 | Using verbs in REST URLs | WARNING | Use nouns, HTTP methods |
| API-002 | Not using proper HTTP status codes | WARNING | Use 2xx, 4xx, 5xx correctly |
| API-003 | Exposing internal entity IDs | WARNING | Use UUIDs or DTOs |
| API-004 | Not versioning API | WARNING | Add /v1/ prefix |
| API-005 | Missing API documentation | WARNING | Add OpenAPI/Swagger |
| API-006 | No pagination on collection endpoints | WARNING | Add pagination |
| API-007 | Using POST for all operations | WARNING | Use appropriate method |
| API-008 | Not using HATEOAS | SUGGESTION | Consider HATEOAS |
| API-009 | Missing rate limiting on public APIs | WARNING | Add rate limiting |
| API-010 | Not using OpenAPI annotations for validation | SUGGESTION | Add @Schema, @Parameter annotations |
| API-011 | Verbose response wrapping | WARNING | Return data directly, not wrapped |

### 13. Best Practices

| Rule ID | Issue | Severity | Fix |
|---------|-------|----------|-----|
| BP-001 | Magic numbers/strings | WARNING | Use constants |
| BP-002 | Not using enums for fixed values | WARNING | Use enums |
| BP-003 | Using abbreviations in class names | WARNING | Use clear names |
| BP-004 | Not following naming conventions | WARNING | Follow Java naming |
| BP-005 | Missing Javadoc on public API | SUGGESTION | Add Javadoc |
| BP-006 | Comments describing "what" not "why" | SUGGESTION | Explain rationale |
| BP-007 | Too many comments | WARNING | Code should be self-documenting |
| BP-008 | Not using Builder pattern for complex objects | SUGGESTION | Use builder | 
| BP-009 | Public fields in class | WARNING | Use private + accessors |
| BP-010 | Not using @Data/@Value Lombok appropriately | WARNING | @Data for entities, @Value for DTOs |
| BP-011 | Code commented out should be removed | WARNING | Remove dead code, use version control |
| BP-012 | TODO/FIXME comments left in code | WARNING | Complete or create task in tracking system |
| BP-013 | Duplicate string literals | WARNING | Extract to constants |
| BP-014 | Unused imports/fields/variables/parameters | WARNING | Remove dead code |
| BP-015 | Cognitive complexity too high (nested logic) | WARNING | Simplify code, extract methods |

### 14. Google Checkstyle Rules (Formatting & Style)

Based on Google Java Style Guide - checks for code formatting, naming, and style:

| Rule ID | Issue | Severity | Fix |
|---------|-------|----------|-----|
| CS-001 | Line length exceeds 100 characters | WARNING | Break line at 100 chars |
| CS-002 | Missing newline at end of file | SUGGESTION | Add trailing newline |
| CS-003 | Tab character used for indentation | WARNING | Use spaces, not tabs |
| CS-004 | Wildcard imports used (e.g., `import java.util.*`) | ERROR | Use explicit imports |
| CS-005 | Imports not in alphabetical order | SUGGESTION | Sort imports alphabetically |
| CS-006 | Static imports not grouped with other imports | SUGGESTION | Group static imports |
| CS-007 | Missing empty line between import groups | SUGGESTION | Separate import groups with blank line |
| CS-008 | Incorrect brace style (not K&R) | WARNING | Use K&R style braces |
| CS-009 | Missing braces for single-line statements | WARNING | Add braces for clarity |
| CS-010 | Incorrect indentation (not +2 spaces) | WARNING | Use 2-space indentation |
| CS-011 | Multiple statements on same line | WARNING | Put each statement on new line |
| CS-012 | Variable declared far from first use | WARNING | Declare variables close to usage |
| CS-013 | Wrong field naming convention | WARNING | Use lowerCamelCase for fields |
| CS-014 | Wrong method naming convention | WARNING | Use lowerCamelCase for methods |
| CS-015 | Wrong class/interface naming convention | WARNING | Use UpperCamelCase for classes |
| CS-016 | Wrong constant naming convention | WARNING | Use UPPER_SNAKE_CASE for constants |
| CS-017 | Wrong package naming convention | WARNING | Use lowercase, no underscores |
| CS-018 | Missing @Override annotation | WARNING | Add @Override when overriding |
| CS-019 | Modifier order incorrect | WARNING | Use: public protected private abstract static final transient volatile synchronized native strictfp |
| CS-020 | Empty catch block | ERROR | Log exception or provide comment |
| CS-021 | Fall-through in switch without comment | WARNING | Add fall-through comment |
| CS-022 | Missing default in switch | WARNING | Add default case or document why not needed |
| CS-023 | Array type syntax (e.g., `int[] i`) | WARNING | Use `int[]` not `int i[]` |
| CS-024 | Using uppercase 'L' for long literals | WARNING | Use lowercase 'l' or remove |
| CS-025 | Missing Javadoc on public classes | SUGGESTION | Add Javadoc to public classes |
| CS-026 | Missing Javadoc on public methods | SUGGESTION | Add Javadoc to public methods |
| CS-027 | Javadoc format issues | SUGGESTION | Follow Javadoc conventions |
| CS-028 | Parameter name same as field name | WARNING | Use different name or use 'this' |
| CS-029 | Unused import | WARNING | Remove unused imports |
| CS-030 | Redundant 'public' modifier on interface methods | WARNING | Remove, interface methods are implicitly public |
| CS-031 | Variable declared at top of block | WARNING | Declare variables when first used |
| CS-032 | Long import statements | WARNING | Break long import lines |
| CS-033 | Missing serialVersionUID in Serializable class | SUGGESTION | Add serialVersionUID field |
| CS-034 | Using System.out.println | WARNING | Use logger instead |
| CS-035 | Magic numbers in code | WARNING | Extract to named constants |

### 15. gRPC Java Best Practices

**Load if gRPC detected:** pom.xml contains `grpc-java`, `grpc-protobuf`, or `.proto` files exist

| Rule ID | Issue | Severity | Fix |
|---------|-------|----------|-----|
| GRPC-001 | Creating new ManagedChannel per request | CRITICAL | Reuse ManagedChannel/Stubs |
| GRPC-002 | Not using keepalive pings | WARNING | Enable keepalive for long-lived connections |
| GRPC-003 | Missing connection timeout | ERROR | Set connection timeout |
| GRPC-004 | Not handling all gRPC status codes | WARNING | Handle CANCELLED, DEADLINE_EXCEEDED, etc. |
| GRPC-005 | Using OK status with error details | WARNING | Use proper gRPC status codes |
| GRPC-006 | Not using interceptors for auth | WARNING | Use ClientInterceptor/ServerInterceptor |
| GRPC-007 | Unary RPC for large payloads | WARNING | Use streaming for large data |
| GRPC-008 | Missing request validation | ERROR | Validate in interceptor or service |
| GRPC-009 | Not using deadline/expiration | WARNING | Set deadline for all calls |
| GRPC-010 | Hardcoded server addresses | WARNING | Use configuration |
| GRPC-011 | Not using SSL/TLS | CRITICAL | Enable TLS for production |
| GRPC-012 | Missing error handling in streams | ERROR | Handle onError properly in streaming |
| GRPC-013 | Using deprecated protobuf fields | WARNING | Use proper proto3 features |
| GRPC-014 | Not using proto package option | WARNING | Use java_package in proto files |
| GRPC-015 | Excessive logging in gRPC methods | WARNING | Use interceptors for logging |
| GRPC-016 | Not closing gRPC resources | CRITICAL | Use try-with-resources or shutdown |
| GRPC-017 | Missing circuit breaker pattern | SUGGESTION | Add resilience4j for failures |
| GRPC-018 | Not using load balancing | WARNING | Configure round-robin or pick-first |
| GRPC-019 | Client blocking on stream | WARNING | Use async stubs appropriately |
| GRPC-020 | Server not handling backpressure | WARNING | Implement flow control |

### 16. gRPC Security Rules

**Load if gRPC detected**

| Rule ID | Issue | Severity | Fix |
|---------|-------|----------|-----|
| GRPC-SEC-001 | No TLS/SSL encryption | CRITICAL | Enable TLS/SSL |
| GRPC-SEC-002 | No authentication mechanism | CRITICAL | Implement JWT or token auth |
| GRPC-SEC-003 | Unvalidated metadata/headers | ERROR | Validate in interceptor |
| GRPC-SEC-004 | Insecure channel credentials | ERROR | Use SecureChannelCredentials |
| GRPC-SEC-005 | Missing rate limiting | WARNING | Implement rate limiting interceptor |
| GRPC-SEC-006 | Exposing internal service addresses | WARNING | Use service mesh or proxy |

### 17. JPA / Hibernate Rules

**Load if JPA detected:** pom.xml contains `hibernate`, `spring-data-jpa`, or `jpa`

| Rule ID | Issue | Severity | Fix |
|---------|-------|----------|-----|
| JPA-001 | N+1 query problem | CRITICAL | Use JOIN FETCH |
| JPA-002 | EAGER fetching on collections | ERROR | Use LAZY |
| JPA-003 | Missing @Transactional | ERROR | Add @Transactional |
| JPA-004 | Returning JPA entity to controller | WARNING | Use DTO |
| JPA-005 | Missing database indexes | WARNING | Add @Index |
| JPA-006 | Large blob in entity | WARNING | Use LAZY or separate table |
| JPA-007 | Entity with no version field | WARNING | Add @Version for optimistic locking |
| JPA-008 | Circular entity relationships | WARNING | Use @JsonIgnore |
| JPA-009 | Native query without parameterization | ERROR | Use parameterized queries |
| JPA-010 | Missing cascade settings | WARNING | Configure cascades properly |

### 18. Lombok Rules

**Load if Lombok detected:** pom.xml contains `lombok`

| Rule ID | Issue | Severity | Fix |
|---------|-------|----------|-----|
| LOMBOK-001 | Using @Data on JPA entity | ERROR | Use @Entity, @Getter, @Setter |
| LOMBOK-002 | @Data on immutable class | WARNING | Use @Value |
| LOMBOK-003 | Missing @Builder.Default for non-initialized fields | WARNING | Add default value |
| LOMBOK-004 | Using @Getter on boolean with "is" prefix | WARNING | Use proper naming |
| LOMBOK-005 | Missing @NonNull on required fields | WARNING | Add validation |

### 19. Build Tools - Maven/Gradle Rules (20 rules)

**Always check build files for best practices**

| Rule ID | Issue | Severity | Fix |
|---------|-------|----------|-----|
| BUILD-001 | Using SNAPSHOT dependencies in production | CRITICAL | Use release versions |
| BUILD-002 | Outdated dependencies | WARNING | Update dependencies regularly |
| BUILD-003 | Missing dependency versions in Gradle | WARNING | Use version catalog or versions.toml |
| BUILD-004 | Using mavenCentral() only | SUGGESTION | Consider mavenCentral() and google() |
| BUILD-005 | Hardcoded credentials in build | CRITICAL | Use environment variables |
| BUILD-006 | Missing build cache configuration | WARNING | Enable Gradle build cache |
| BUILD-007 | Using deprecated Gradle plugins | WARNING | Update to latest plugins |
| BUILD-008 | Not using dependency locking | SUGGESTION | Use dependency lock for reproducible builds |
| BUILD-019 | Missing parallel build configuration | SUGGESTION | Enable parallel execution |
| BUILD-010 | Not using Gradle wrapper | WARNING | Use gradle wrapper for consistency |

### 20. Dead Code Detection (NEW!)

**Detects unused code - runs in parallel with lint checks**

| Rule ID | Issue | Severity | Fix |
|---------|-------|----------|-----|
| DEAD-001 | Unused public method | WARNING | Remove or mark with @SuppressWarnings |
| DEAD-002 | Unused private method | WARNING | Remove |
| DEAD-003 | Unused field | WARNING | Remove |
| DEAD-004 | Unused import | WARNING | Remove import statement |
| DEAD-005 | Unused local variable | WARNING | Remove variable |
| DEAD-006 | Unused private constructor | WARNING | Remove or make package-private |
| DEAD-007 | Unused parameter | WARNING | Remove parameter or add @SuppressWarnings("unused") |
| DEAD-008 | Unused inner class | WARNING | Remove or make static |
| DEAD-009 | Unreachable code | WARNING | Remove dead code |
| DEAD-010 | Duplicate code | WARNING | Extract to common method |
| DEAD-011 | Empty catch block | WARNING | Add logging or remove |
| DEAD-012 | Empty finally block | WARNING | Remove if not needed |
| DEAD-013 | Empty constructor | WARNING | Remove if class has no superclass call |
| DEAD-014 | Empty static initializer | WARNING | Remove if not needed |
| DEAD-015 | Commented-out code | WARNING | Remove, use version control |

**Dead Code Detection Patterns:**

```java
// DEAD-001: Unused public method - may be used by reflection or external code
// Only mark as dead code if you're certain no external usage exists
public void unusedPublicMethod() { } // Check for @Api exposure first

// DEAD-004: Unused import
import java.util.List; // If List is never used

// DEAD-009: Unreachable code
public int method() {
    return 1;
    return 2; // Unreachable - remove
}

// DEAD-010: Duplicate code
public class UserService {
    public void createUser(User user) {
        validateUser(user); // Same validation duplicated
        userRepository.save(user);
        sendEmail(user.getEmail());
    }
    
    public void updateUser(User user) {
        validateUser(user); // Duplicate!
        userRepository.save(user);
    }
    
    private void validateUser(User user) { /* ... */ }
}

// DEAD-011: Empty catch block
try {
    riskyOperation();
} catch (Exception e) {
    // Empty! At least log the error
}
```

---

## Review Modes

### Mode 1: Local Changes (Default)
Review uncommitted changes in working directory.

```bash
git status --porcelain
git diff
git diff --cached
```

### Mode 2: Branch Comparison
Compare feature branch against base (develop/main/master).

```bash
git branch --show-current
git diff <base-branch>..HEAD -- "*.java"
git log <base-branch>..HEAD --oneline
```

### Mode 3: Specific Files
Analyze specific Java files.

```bash
git diff <commit> -- path/to/File.java
```

## Install for Your Coding Agent

Teach your coding agent all Java best practice rules. Add this skill to your agent:

```bash
npx skills add ajaywadhara/java-doctor
```

Supports Cursor, Claude Code, Amp Code, Codex, Gemini CLI, OpenCode, Windsurf, and Antigravity.

---

## Analysis Workflow

1. **Detect Java Version**
   - Parse pom.xml or build.gradle
   - Note supported features for that version

2. **Collect Java Files**
   - If reviewing changes: `git diff --name-only -- "*.java"`
   - If reviewing branch: `git diff <base>..HEAD --name-only -- "*.java"`
   - If specific files: Use user-provided paths

3. **Run Pattern Analysis**
   - Use Grep to search for each rule pattern
   - Read relevant code sections for context

4. **Calculate Score**
   - Start with 100
   - Deduct based on severity table

5. **Generate Report**
   - Save to `.output/java-doctor-{context}-{timestamp}.md`

---

## Output Format

Save reports to `.output/` directory. Multiple formats available:

### Format 1: Markdown (Default)

Save report to `.output/java-doctor-{context}-{timestamp}.md`:

```markdown
# Java Doctor Report

## Summary
| Metric | Value |
|--------|-------|
| **Score** | X/100 |
| **Status** | Great / Needs Work / Critical |
| **Java Version** | X (detected from pom.xml/build.gradle) |
| **Files Analyzed** | N |
| **Issues Found** | CRITICAL: X, ERROR: X, WARNING: X, SUGGESTION: X |

## Files Analyzed
- `src/main/java/com/example/Service.java`
- `src/main/java/com/example/Controller.java`

## Issues by Category

### Security (CRITICAL)
1. **[File:Line]** - SEC-001: Hardcoded password found
   - **Severity:** CRITICAL
   - **Problem:** `private static final String PASSWORD = "********";`
   - **Fix:** Use environment variable or configuration

## Recommendations
1. Fix all CRITICAL issues immediately
2. Address ERROR issues before release
3. Review WARNING issues for improvement
4. Consider SUGGESTIONS for code quality

## Quick Fixes Available
- [ ] SEC-001: Replace hardcoded secret with @Value injection
- [ ] NULL-001: Replace .get() with orElseThrow()
- [ ] PERF-001: Add @Query with JOIN FETCH
```

### Format 2: JSON

Save to `.output/java-doctor-{context}-{timestamp}.json`:

```json
{
  "report": {
    "generated": "2024-01-15T10:30:00Z",
    "score": 85,
    "status": "Great",
    "javaVersion": "17",
    "springBootVersion": "3.2",
    "filesAnalyzed": 5
  },
  "issues": {
    "critical": [
      {
        "id": "SEC-001",
        "file": "src/main/java/com/example/AuthService.java",
        "line": 42,
        "title": "Hardcoded password found",
        "problem": "private static final String PASSWORD = \"********\";",
        "fix": "Use @Value injection or environment variable"
      }
    ],
    "error": [],
    "warning": [
      {
        "id": "NULL-001",
        "file": "src/main/java/com/example/UserService.java",
        "line": 15,
        "title": "Optional.get() without check",
        "problem": "userRepository.findById(id).get()",
        "fix": "Use .orElseThrow(() -> new NotFoundException())"
      }
    ],
    "suggestion": []
  },
  "summary": {
    "total": 12,
    "critical": 1,
    "error": 2,
    "warning": 5,
    "suggestion": 4
  }
}
```

### Format 3: HTML Report

Save to `.output/java-doctor-{context}-{timestamp}.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Java Doctor Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .score { font-size: 48px; font-weight: bold; }
        .great { color: #22c55e; }
        .needs-work { color: #eab308; }
        .critical { color: #ef4444; }
        .issue { border: 1px solid #ddd; padding: 10px; margin: 10px 0; }
        .critical-issue { border-left: 4px solid #ef4444; }
        .error-issue { border-left: 4px solid #f97316; }
        .warning-issue { border-left: 4px solid #eab308; }
    </style>
</head>
<body>
    <h1>Java Doctor Report</h1>
    <div class="score great">85/100</div>
    <p><strong>Status:</strong> Great</p>
    <p><strong>Java Version:</strong> 17</p>
    <p><strong>Files Analyzed:</strong> 5</p>
    
    <h2>Issues Found: 12</h2>
    <p>CRITICAL: 1 | ERROR: 2 | WARNING: 5 | SUGGESTION: 4</p>
    
    <h3>Critical Issues</h3>
    <div class="issue critical-issue">
        <strong>SEC-001:</strong> Hardcoded password found<br>
        <code>src/main/java/com/example/AuthService.java:42</code><br>
        Fix: Use @Value injection
    </div>
</body>
</html>
```

### Format 4: SARIF (For IDE Integration)

Save to `.output/java-doctor-{context}-{timestamp}.sarif`:

```json
{
  "version": "2.1.0",
  "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
  "runs": [{
    "tool": {
      "driver": {
        "name": "Java Doctor",
        "version": "1.0"
      }
    },
    "results": [
      {
        "ruleId": "SEC-001",
        "level": "error",
        "message": { "text": "Hardcoded password found" },
        "locations": [{
          "physicalLocation": {
            "artifactLocation": { "uri": "src/main/java/com/example/AuthService.java" },
            "region": { "startLine": 42 }
          }
        }]
      }
    ]
  }]
}
```

### Format 5: CSV (For Excel/Sheets)

Save to `.output/java-doctor-{context}-{timestamp}.csv`:

```csv
Severity,Rule ID,File,Line,Issue,Problem,Fix
CRITICAL,SEC-001,src/main/java/com/example/AuthService.java,42,Hardcoded password found,"private static final String PASSWORD = \"********\";","Use @Value injection"
WARNING,NULL-001,src/main/java/com/example/UserService.java,15,Optional.get() without check,userRepository.findById(id).get(),Use orElseThrow()
```

---

**Default format is Markdown.** To request a different format, specify in your command:
- "Run Java Doctor with JSON output"
- "Generate HTML report"
- "Export to CSV"

---

## Effective Java Reference

Based on "Effective Java" by Joshua Bloch:

| Item | Topic | Related Rules |
|------|-------|---------------|
| Item 1 | Consider static factory methods | BP-008 |
| Item 2 | Builder pattern for complex objects | BP-008 |
| Item 3 | Singleton or utility class | EJ-009 |
| Item 4 | Enforce noninstantiability | EJ-009 |
| Item 5 | Prefer dependency injection | SPR-007 |
| Item 6 | Avoid finalizers | RES-001 |
| Item 7 | Prefer try-with-resources | EJ-011, RES-001 |
| Item 8 | Prefer primitives | PERF-004 |
| Item 9 | Avoid strings where other types appropriate | ARCH-007 |
| Item 10 | Beware string concatenation | PERF-003 |
| Item 11 | Implement compareTo carefully | EJ-010 |
| Item 12 | Always override toString | BP-005 |
| Item 13 | Override clone judiciously | EJ-007 |
| Item 14 | Consider implementing Serializable | BP-005 |
| Item 15 | Minimize accessibility | ARCH-010 |
| Item 16 | Accessors over public fields | BP-009 |
| Item 17 | Minimize mutability | NULL-008 |
| Item 18 | Favor composition over inheritance | ARCH-004 |
| Item 19 | Use interfaces to define types | ARCH-006 |
| Item 20 | Prefer class hierarchies to tagged classes | ARCH-001 |
| Item 21 | Use function objects (strategies) | EJ-022 |
| Item 22 | Favor static over nonstatic member classes | EJ-004 |
| Item 24 | Prefer generic types | EJ-006 |
| Item 25 | Prefer lists to arrays | ARCH-007 |
| Item 26 | Use bounded wildcards | EJ-006 |
| Item 27 | Generic and可变性的取舍 | EJ-006 |
| Item 28 | Prefer batch to discrete operations | PERF-001 |
| Item 29 | Use interface for return types | API-003 |
| Item 30 | Use checked exceptions judiciously | EXC-003 |
| Item 31 | Document checked exceptions | EXC-003 |
| Item 32 | Document thread safety | CONC-001 |
| Item 33 | Document synchronization policy | CONC-001 |
| Item 34 | Lazy initialization judiciously | CONC-002 |
| Item 35 | Don't overuse synchronization | CONC-012 |
| Item 36 | Prefer executors to tasks | CONC-008 |
| Item 37 | Prefer concurrency utilities | CONC-010 |
| Item 38 | Check parameters for validity | NULL-004 |
| Item 39 | Make defensive copies | NULL-008 |
| Item 40 | Design method signatures carefully | API-001 |
| Item 41 | Use overloading judiciously | NULL-006 |
| Item 42 | Use varargs judiciously | ARCH-003 |
| Item 43 | Return empty collections, not nulls | NULL-003 |
| Item 44 | Optional return types | EJ-018 |
| Item 45 | Minimize scope of local variables | EJ-012 |
| Item 46 | Prefer for-each to traditional for | EJ-020 |
| Item 47 | Know and use libraries | PERF-012 |
| Item 48 | Avoid float/double for precise calculations | BP-001 |
| Item 49 | Know and use libraries (BigDecimal) | BP-001 |
| Item 50 | Avoid strings where other types appropriate | ARCH-007 |
```

---

## Interactive Workflow

After analysis, ask user what to do:

```
Question: "Java Doctor scan complete. Score: X/100 ({Status}). Found {N} issues."
Header: "Next Steps"
Options:
  - "Show me the issues" → Display all issues grouped by severity
  - "Fix critical issues" → Apply fixes for CRITICAL issues
  - "Fix all issues" → Apply fixes for all issues
  - "Save report" → Save to .output/ directory
  - "Re-scan" → Re-run analysis
```

---

## Quick Commands

| User Says | Your Action |
|-----------|-------------|
| "Run Java Doctor" | Full scan with version detection |
| "Scan my Java code" | Analyze local changes |
| "Check for security issues" | Focus on security rules |
| "Find performance problems" | Focus on performance rules |
| "Java code review" | Full analysis with all rules |
| "Check branch vs develop" | Branch comparison mode |
| "What's my score?" | Run scan and show score |

---

## References (Load When Needed)

- `references/bug-patterns.md` - Detailed bug patterns with code examples
- `references/security-checklist.md` - OWASP Top 10 for Java
- `references/performance-antipatterns.md` - N+1, memory, CPU issues
- `references/spring-best-practices.md` - Spring-specific rules
- `references/effective-java-mapping.md` - Items mapped to rules
- `references/version-specific-changes.md` - Java 8-21 changes

---

This skill is inspired by react-doctor but tailored specifically for Java, incorporating best practices from "Effective Java" by Joshua Bloch and version-aware checks for Java 8 through 21.
