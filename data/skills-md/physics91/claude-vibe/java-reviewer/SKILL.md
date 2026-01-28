---
name: java-reviewer
description: |
  WHEN: Java code review, Java idioms, exception handling, collections, streams, Java 17+ features
  WHAT: Exception patterns + resource management + null safety + stream usage + modern Java features
  WHEN NOT: Spring specific → spring-boot-reviewer, Android → kotlin-android-reviewer, Kotlin → kotlin-spring-reviewer
---

# Java Reviewer Skill

## Purpose
Reviews Java code for idiomatic patterns, exception handling, resource management, null safety, and modern Java (17+) feature adoption.

## When to Use
- Java code review requests
- "Java patterns", "exception handling", "Java best practices" mentions
- Legacy Java modernization
- Projects with `pom.xml` or `build.gradle`
- `src/main/java/**/*.java` files

## Project Detection
- `pom.xml` (Maven) or `build.gradle` (Gradle)
- `src/main/java/` directory structure
- `.java` source files
- `java.version` property in build config

## Workflow

### Step 1: Analyze Project
```
**Java Version**: 17 / 21
**Build Tool**: Maven / Gradle
**Testing**: JUnit 5
**Key Dependencies**:
  - Lombok
  - MapStruct
  - Jakarta EE
```

### Step 2: Select Review Areas
**AskUserQuestion:**
```
"Which Java areas to review?"
Options:
- Full Java idiom check (recommended)
- Exception handling
- Resource management (try-with-resources)
- Null safety (Optional, annotations)
- Stream/Collection patterns
- Modern Java features (17+)
multiSelect: true
```

## Detection Rules

### Critical: Empty Catch Blocks
| Pattern | Issue | Severity |
|---------|-------|----------|
| Empty catch block | Silent failure | CRITICAL |
| Catch all `Exception` | Over-broad handling | HIGH |
| Catch `Throwable` | Catching errors | CRITICAL |
| Missing logging in catch | Lost error info | HIGH |

```java
// BAD: Empty catch block
try {
    parseFile(path);
} catch (IOException e) {
    // Silent failure - CRITICAL
}

// BAD: Catch all Exception
try {
    process();
} catch (Exception e) {
    log.error("Error", e);  // Too broad
}

// GOOD: Specific exception handling
try {
    parseFile(path);
} catch (FileNotFoundException e) {
    log.warn("File not found: {}", path);
    return Optional.empty();
} catch (IOException e) {
    log.error("Failed to read file: {}", path, e);
    throw new ProcessingException("File read error", e);
}

// BAD: Catching Throwable
try {
    compute();
} catch (Throwable t) {  // Catches OutOfMemoryError, StackOverflowError
    log.error("Error", t);
}

// GOOD: Catch Exception, let Errors propagate
try {
    compute();
} catch (Exception e) {
    log.error("Processing failed", e);
    throw new ServiceException(e);
}
```

### Critical: Mutable Static Fields
| Pattern | Issue | Severity |
|---------|-------|----------|
| `public static` non-final | Thread-unsafe | CRITICAL |
| Static mutable collection | Race condition | CRITICAL |
| Static `DateFormat` | Not thread-safe | CRITICAL |

```java
// BAD: Mutable static field
public class Config {
    public static String apiUrl;  // CRITICAL: Thread-unsafe
    public static List<String> allowedHosts = new ArrayList<>();  // CRITICAL
}

// GOOD: Immutable static
public class Config {
    public static final String API_URL = "https://api.example.com";
    public static final List<String> ALLOWED_HOSTS = List.of("a.com", "b.com");
}

// BAD: Static DateFormat (not thread-safe)
public class DateUtils {
    private static final SimpleDateFormat FORMAT = new SimpleDateFormat("yyyy-MM-dd");
}

// GOOD: ThreadLocal or DateTimeFormatter
public class DateUtils {
    private static final DateTimeFormatter FORMAT = DateTimeFormatter.ofPattern("yyyy-MM-dd");
}
```

### High: Raw Types (No Generics)
| Pattern | Issue | Severity |
|---------|-------|----------|
| `List` instead of `List<T>` | Type safety lost | MEDIUM |
| `Map` instead of `Map<K, V>` | Unchecked operations | MEDIUM |
| `Class` instead of `Class<?>` | Wildcard missing | LOW |

```java
// BAD: Raw types
List users = new ArrayList();
users.add("string");  // No compile error, runtime issue
User user = (User) users.get(0);  // ClassCastException

// GOOD: Generics
List<User> users = new ArrayList<>();
users.add(new User("John"));  // Type-safe
User user = users.get(0);  // No cast needed

// BAD: Raw Map
Map config = new HashMap();
config.put("key", 123);
String value = (String) config.get("key");  // ClassCastException

// GOOD: Typed Map
Map<String, Object> config = new HashMap<>();
// Or better:
Map<String, String> stringConfig = new HashMap<>();
```

### High: Resource Management
| Pattern | Issue | Severity |
|---------|-------|----------|
| Manual close() | Leak on exception | HIGH |
| Finally without null check | NPE risk | MEDIUM |
| Missing try-with-resources | Resource leak | HIGH |

```java
// BAD: Manual resource management
InputStream is = null;
try {
    is = new FileInputStream(file);
    process(is);
} finally {
    is.close();  // NPE if exception in constructor
}

// GOOD: try-with-resources
try (InputStream is = new FileInputStream(file)) {
    process(is);
}  // Auto-closed, even on exception

// GOOD: Multiple resources
try (
    Connection conn = dataSource.getConnection();
    PreparedStatement stmt = conn.prepareStatement(sql);
    ResultSet rs = stmt.executeQuery()
) {
    while (rs.next()) {
        process(rs);
    }
}

// Java 9+: Effectively final variables
InputStream is = new FileInputStream(file);
try (is) {  // Can use existing variable
    process(is);
}
```

### High: Collection Null Returns
| Pattern | Issue | Severity |
|---------|-------|----------|
| Return `null` for empty | NPE risk | HIGH |
| `null` collection parameter | Hidden bug | MEDIUM |
| No defensive copy | Mutation leak | MEDIUM |

```java
// BAD: Return null for empty
public List<User> findUsers(String query) {
    List<User> results = repository.search(query);
    if (results.isEmpty()) {
        return null;  // Client must null-check
    }
    return results;
}

// GOOD: Return empty collection
public List<User> findUsers(String query) {
    List<User> results = repository.search(query);
    return results != null ? results : Collections.emptyList();
}

// BETTER: Use Optional for single values
public Optional<User> findUser(String id) {
    return Optional.ofNullable(repository.findById(id));
}

// BAD: No defensive copy
public List<String> getItems() {
    return items;  // Caller can modify
}

// GOOD: Defensive copy or unmodifiable
public List<String> getItems() {
    return List.copyOf(items);  // Java 10+
    // or: return Collections.unmodifiableList(items);
}
```

### Medium: String Concatenation in Loops
| Pattern | Issue | Severity |
|---------|-------|----------|
| `+` in loop | O(n^2) complexity | MEDIUM |
| `String.format` in loop | Performance hit | LOW |

```java
// BAD: String concatenation in loop
String result = "";
for (String item : items) {
    result += item + ",";  // Creates new String each iteration
}

// GOOD: StringBuilder
StringBuilder sb = new StringBuilder();
for (String item : items) {
    sb.append(item).append(",");
}
String result = sb.toString();

// BETTER: String.join (Java 8+)
String result = String.join(",", items);

// BEST: Collectors.joining (streams)
String result = items.stream()
    .collect(Collectors.joining(","));
```

### Medium: Stream Anti-patterns
| Pattern | Issue | Severity |
|---------|-------|----------|
| forEach with side effects | Not functional | MEDIUM |
| Nested streams | Performance | MEDIUM |
| Stream in loop | Create once | LOW |
| Parallel without need | Overhead | LOW |

```java
// BAD: forEach with mutation
List<User> activeUsers = new ArrayList<>();
users.stream()
    .filter(User::isActive)
    .forEach(activeUsers::add);  // Side effect

// GOOD: Collect
List<User> activeUsers = users.stream()
    .filter(User::isActive)
    .collect(Collectors.toList());

// Java 16+: toList()
List<User> activeUsers = users.stream()
    .filter(User::isActive)
    .toList();

// BAD: Unnecessary parallel
users.parallelStream()  // Only 10 users
    .map(User::getName)
    .collect(Collectors.toList());

// GOOD: Sequential for small collections
users.stream()
    .map(User::getName)
    .collect(Collectors.toList());
```

### Low: Missing @Override
| Pattern | Issue | Severity |
|---------|-------|----------|
| No @Override on override | Typo not caught | LOW |
| Missing equals/hashCode | Collection issues | MEDIUM |

```java
// BAD: Missing @Override
public class User {
    public boolean equals(Object obj) {  // Typo not caught
        // ...
    }
}

// GOOD: With @Override
public class User {
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        User user = (User) obj;
        return Objects.equals(id, user.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}
```

### Modern Java Features (17+)
| Old Pattern | Modern Alternative | Since |
|-------------|-------------------|-------|
| `instanceof` + cast | Pattern matching | Java 16 |
| Switch statement | Switch expression | Java 14 |
| Verbose records | `record` | Java 16 |
| Text blocks (`\n`) | `"""` | Java 15 |
| Sealed classes | `sealed`, `permits` | Java 17 |

```java
// OLD: instanceof + cast
if (obj instanceof User) {
    User user = (User) obj;
    process(user.getName());
}

// NEW: Pattern matching (Java 16+)
if (obj instanceof User user) {
    process(user.getName());
}

// OLD: Switch statement
String status;
switch (code) {
    case 200:
        status = "OK";
        break;
    case 404:
        status = "Not Found";
        break;
    default:
        status = "Unknown";
}

// NEW: Switch expression (Java 14+)
String status = switch (code) {
    case 200 -> "OK";
    case 404 -> "Not Found";
    default -> "Unknown";
};

// OLD: Verbose DTO
public class UserDto {
    private final String name;
    private final int age;
    // constructor, getters, equals, hashCode, toString
}

// NEW: Record (Java 16+)
public record UserDto(String name, int age) {}

// Text blocks (Java 15+)
String json = """
    {
        "name": "John",
        "age": 30
    }
    """;
```

## Response Template
```
## Java Code Review Results

**Project**: [name]
**Java Version**: 17 / 21
**Build Tool**: Maven / Gradle

### Exception Handling

#### CRITICAL
| File | Line | Issue |
|------|------|-------|
| Service.java | 45 | Empty catch block |
| Utils.java | 78 | Catching Throwable |

#### HIGH
| File | Line | Issue |
|------|------|-------|
| Dao.java | 23 | Catching generic Exception |
| Config.java | 12 | Mutable static field |

### Resource Management
| File | Line | Issue |
|------|------|-------|
| FileService.java | 56 | Missing try-with-resources |

### Modern Java Adoption
- [ ] Use pattern matching instanceof (Java 16+)
- [ ] Convert DTOs to records
- [ ] Use switch expressions
- [ ] Use text blocks for multiline strings

### Recommendations
1. [ ] Replace empty catch blocks with proper handling
2. [ ] Use try-with-resources for all IO
3. [ ] Return empty collections instead of null
4. [ ] Enable preview features if using Java 21

### Positive Patterns
- Good use of Optional for nullable returns
- Proper use of streams for collection processing
```

## Best Practices
1. **Fail Fast**: Validate inputs early
2. **Immutability**: Prefer final fields, records
3. **Null Safety**: Optional, @Nullable/@NonNull
4. **Modern APIs**: java.time, List.of, Map.of
5. **Checked Exceptions**: Use sparingly, wrap in runtime

## Integration
- `spring-boot-reviewer` skill: Spring-specific patterns
- `orm-reviewer` skill: JPA/Hibernate patterns
- `code-reviewer` skill: General quality
- `security-scanner` skill: Security audit

## Notes
- Based on Java 17+ best practices
- Encourages adoption of modern Java features
- Compatible with Maven and Gradle projects
- Works with Lombok and other code generators
