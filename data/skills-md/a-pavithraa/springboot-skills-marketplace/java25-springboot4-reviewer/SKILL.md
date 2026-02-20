---
name: java25-springboot4-reviewer
description: Comprehensive code review for Java 25 and Spring Boot 4 apps. Use when reviewing, checking, auditing, or analyzing Java/Spring Boot code (files, modules, PRs, or full codebases) for migration risks, Spring Boot 4 best practices, JSpecify null-safety, security vulnerabilities, performance bottlenecks, data access pitfalls, architecture boundaries (DDD/Hexagonal/Spring Modulith), or modern Java 25 usage.
---

# Java 25 & Spring Boot 4 Reviewer

**Version:** Based on Java 25 (JDK 25) and Spring Boot 4.0.x (as of January 2026)

**Note:** Spring Boot 4 and Java 25 are actively evolving. Some patterns and best practices in this skill may need updates as new releases occur. Always consult official documentation for the latest guidance.

## Critical Rules

**NEVER review without code context. ALWAYS ask for files or diff.**

**ALWAYS cite file paths and line numbers for findings.**

**MANDATORY baseline:** Java 25 + Spring Boot 4.0.x (latest stable). Flag if build files show otherwise.

**ANALYZE workload before architectural recommendations.** Don't suggest virtual threads, reactive patterns, or architectural changes without understanding actual concurrency, traffic patterns, and workload characteristics. Pattern matching without analysis leads to inappropriate recommendations.

**JSpecify is the null-safety baseline.** Avoid `org.springframework.lang` annotations; use package-level `@NullMarked` + explicit `@Nullable` in type usage. Copy nullability annotations when overriding.

**Prefer official Spring docs as source of truth.** If a pattern in code conflicts with documented guidance, flag it and link to the official rule via the relevant reference files.

## Workflow

### Step 1: Scope and Constraints

Ask:
1. **Scope** - single file, module, or full PR?
2. **Target versions** - confirm Java 25 + Spring Boot 4.0.x
3. **Focus areas** - security, data, performance, architecture, null-safety, migration, or all
4. **Testing expectations** - unit, integration, contract, performance

### Step 2: Load References

| Focus | Load |
|------|------|
| **Spring Boot 4 patterns** | `references/spring-boot-4-patterns.md` |
| **Java 25 adoption** | `references/java-25-features.md` |
| **Security** | `references/security-checklist.md` |
| **Performance** | `references/performance-patterns.md` |
| **Architecture** | `references/architecture-patterns.md` |
| **Null-safety** | `references/jspecify-null-safety.md` |
| **Spring Data JPA** | Use the `spring-data-jpa` skill |
| **Migration** | Use the `springboot-migration` skill |

### Step 3: Review Passes

**Pass A: Build + configuration**
- Verify Java and Spring Boot versions in build files
- Check starter names (webmvc/aspectj/test-classic)
- Scan for deprecated annotations and Jackson 3 migration issues

**Pass B: API + correctness**
- Controllers/services boundaries
- Validation and error handling (ProblemDetail)
- Null-safety contracts in public APIs

**Pass C: Package structure**
- Identify the architecture style used (layered, package-by-module, modulith, tomato, DDD+hex)
- Verify folder/package layout matches the selected pattern
- Flag cross-module leakage (controllers using repositories, infra types in domain)

**Pass D: Data access**
- Repository placement (aggregate roots only)
- N+1, pagination, projections, transactions

**Pass E: Security**
- Authentication/authorization
- Input validation and secrets handling
- Sensitive data logging

**Pass F: Performance + resilience**
- Caching strategy
- Virtual threads evaluation (MUST verify 10,000+ concurrent tasks and I/O-bound workload before recommending - see `java-25-features.md` for threshold explanation)
- Thread pool sizing matches workload (check actual concurrency, not daily totals)
- Timeouts, retries, backoff

### Step 4: Report Findings

Order by severity and include:
- **Category**
- **File + line**
- **Impact**
- **Fix recommendation**

Use this structure:

```markdown
## Critical
- **[Category]**: Issue
  - **File**: `path/to/File.java:123`
  - **Impact**: What breaks or risks
  - **Fix**: Specific change

## High / Medium / Low
...
```

## Quick Reference: Review Triggers

### Migration and Boot 4
- Old starter names (`spring-boot-starter-web` → `spring-boot-starter-webmvc`)
- Old test annotations (`@MockBean` → `@MockitoBean`)
- Jackson 2 usage when Boot 4 expects Jackson 3

### Null-safety (JSpecify)
- Missing `package-info.java` with `@NullMarked`
- `org.springframework.lang` annotations still in use
- `@Nullable` placed on fields/params instead of type usage
- Overridden methods missing nullability annotations

### Security
- SQL/NoSQL injection risks
- Passwords not hashed (BCrypt/Argon2)
- Missing authz checks (`@PreAuthorize`)
- Secrets in code or logs

### Performance
- N+1 queries
- No pagination / unbounded queries
- No caching for heavy reads
- Virtual threads recommended without analyzing workload (MUST verify 10,000+ concurrent tasks, I/O-bound operations, and thread pool exhaustion - see `java-25-features.md`)
- Thread pool sizes that don't match actual workload characteristics

### Architecture
- Controllers calling repositories directly
- Exposing JPA entities in APIs
- Modulith boundary violations
- Business logic in controllers
- Package structure deviates from chosen pattern (layered, package-by-module, modulith, tomato, DDD+hex)

### Modern Java 25
- Old `instanceof` + cast
- Verbose DTOs instead of records
- String concatenation for SQL/JSON
- Old switch statements

## Anti-Patterns

| Don't | Do | Why |
|------|----|-----|
| Review with no files | Ask for files/diff | Prevents generic advice |
| Skip null-safety checks | Load JSpecify guidance | Boot 4 APIs are null-safe |
| Treat all findings equally | Prioritize by severity | Focus on risk |
| Suggest sweeping rewrites | Recommend incremental fixes | Safer for PRs |

## Key Principle

**Ground every finding in code, prioritize risk, and align with Java 25 + Spring Boot 4 + JSpecify null-safety.**
- Refactoring guidance

## Review Checklists

### Quick Security Check (5 minutes)

- [ ] No SQL string concatenation
- [ ] Passwords hashed (BCrypt/Argon2)
- [ ] Sensitive endpoints have `@PreAuthorize`
- [ ] No hardcoded secrets
- [ ] No sensitive data in logs
- [ ] HTTPS enforced

### Quick Performance Check (5 minutes)

- [ ] No lazy loading in loops
- [ ] Pagination used for large queries
- [ ] Read-only transactions marked
- [ ] Connection pool configured
- [ ] No resource leaks (try-with-resources)
- [ ] Thread pool sizing appropriate for workload (analyze actual concurrency before suggesting changes)

### Quick Migration Check (5 minutes)

- [ ] Spring Boot 4 starters (webmvc, aspectj)
- [ ] Jackson 3 imports (`tools.jackson.*`)
- [ ] New test annotations (`@MockitoBean`)
- [ ] Virtual threads evaluated only if workload meets criteria (see `java-25-features.md`)

### Comprehensive Review (30+ minutes)

Load all reference files and check:

- [ ] **Security**: All OWASP Top 10 items
- [ ] **Performance**: N+1, caching, async, virtual threads
- [ ] **Architecture**: Layering, boundaries, patterns
- [ ] **Migration**: Java 25 and Spring Boot 4 adoption
- [ ] **Best Practices**: Clean code, SOLID, DRY

## Tips for Effective Reviews

### Be Specific

❌ "This code has security issues"
✅ "SQL injection vulnerability at UserRepository.java:45 - use parameterized query"

### Prioritize

Focus on:
1. **Critical**: Security, data loss, crashes
2. **Important**: Performance, architecture violations
3. **Nice-to-have**: Code style, minor optimizations

### Provide Context

Explain WHY something is a problem:

❌ "Use records"
✅ "Use records to reduce boilerplate and ensure immutability. This DTO has 50 lines of boilerplate that records eliminate."

### Show Examples

Include code snippets showing the fix:

```java
// ❌ Before
String query = "SELECT * FROM users WHERE id = " + userId;

// ✅ After
@Query("SELECT u FROM User u WHERE u.id = :userId")
User findByUserId(@Param("userId") Long userId);
```

### Be Constructive

Frame feedback positively:

❌ "This is wrong"
✅ "Consider using pattern matching here to simplify the code and reduce casting"

## Common Review Scenarios

### Scenario 1: Quick PR Review

**Context**: User asks to review a pull request

**Actions:**
1. Ask for changed files or use Glob to find them
2. Read changed files
3. Load `java-25-features.md` and `spring-boot-4-patterns.md`
4. Run Quick Security + Performance checks
5. Report findings with file:line references

### Scenario 2: Security Audit

**Context**: User requests security review

**Actions:**
1. Load `security-checklist.md`
2. Glob for controllers, services, security config
3. Check OWASP Top 10 systematically
4. Focus on: SQL injection, authentication, authorization, secrets
5. Provide detailed security report

### Scenario 3: Performance Review

**Context**: User reports slowness or wants optimization

**Actions:**
1. Load `performance-patterns.md`
2. Glob for repositories, services
3. Check for: N+1 queries, missing pagination, no caching
4. Review connection pool and async configuration
5. Suggest specific optimizations with expected impact

### Scenario 4: Architecture Review

**Context**: User wants to validate architecture or refactor

**Actions:**
1. Load `architecture-patterns.md`
2. Understand current pattern (Layered? DDD? Hexagonal?)
3. Check for violations (layer bypassing, broken boundaries)
4. Validate Spring Modulith modules if used
5. Suggest architectural improvements aligned with their pattern

### Scenario 5: Migration Review

**Context**: Codebase recently migrated to Spring Boot 4 / Java 25

**Actions:**
1. Load `java-25-features.md` and `spring-boot-4-patterns.md`
2. Glob for all Java files
3. Identify old patterns still in use
4. Prioritize quick wins (records for DTOs, switch expressions)
5. Provide migration roadmap for larger changes

## When NOT to Use This Skill

- Kotlin code (this skill is Java-specific)
- Non-Spring Boot frameworks (Micronaut, Quarkus)
- Build/config files only (pom.xml, build.gradle) - unless reviewing dependencies
- Frontend code (React, Angular) - unless Spring MVC templates

## Example Usage

**User:** "Can you review OrderService.java for any issues?"

**Assistant:**

1. Reads `OrderService.java`
2. Loads `java-25-features.md`, `spring-boot-4-patterns.md`, `performance-patterns.md`, `security-checklist.md`
3. Analyzes code against checklists
4. Reports findings:

```markdown
## Critical Issues

🚨 **Performance - N+1 Query**
- **File**: `OrderService.java:45`
- **Problem**: Lazy loading `order.getItems()` in a loop causes N+1 queries
- **Solution**: Use `@EntityGraph` or fetch join in repository

🚨 **Security - Missing Authorization**
- **File**: `OrderService.java:30`
- **Problem**: `deleteOrder()` has no authorization check
- **Solution**: Add `@PreAuthorize("hasRole('ADMIN') or #order.userId == authentication.principal.id")`

## Warnings

⚠️ **Migration - Old Jackson Import**
- **File**: `OrderService.java:5`
- **Problem**: Using `com.fasterxml..jackson.*`
- **Recommendation**: Update to `tools.jackson.*`

## Suggestions

💡 **Modern Java - Use Record for DTO**
- **File**: `OrderService.java:78-120`
- **Suggestion**: Replace `OrderDTO` class with record to eliminate 42 lines of boilerplate
```

---

**User:** "Review the entire order module for architecture issues"

**Assistant:**

1. Uses Glob to find all files in `order/` module
2. Loads `architecture-patterns.md`
3. Checks for layer violations, DDD patterns, module boundaries
4. Reports architectural findings with recommendations
