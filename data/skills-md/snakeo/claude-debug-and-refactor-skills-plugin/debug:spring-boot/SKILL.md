---
name: debug:spring-boot
description: Debug Spring Boot issues systematically. Use when encountering bean errors like NoSuchBeanDefinitionException, circular dependency issues, application startup failures, JPA/Hibernate problems including LazyInitializationException and N+1 queries, security misconfigurations causing 403 Forbidden errors, property binding failures, CSRF token issues, or any Spring Boot application requiring diagnosis with Actuator endpoints and JVM debugging.
---

# Spring Boot Debugging Guide

You are an expert Spring Boot debugger. Follow this systematic approach to diagnose and resolve issues efficiently.

## Common Error Patterns

### 1. NoSuchBeanDefinitionException
**Symptoms:**
- "Field xyz required a bean of type 'X' that could not be found"
- "No qualifying bean of type 'X' available"

**Debugging Steps:**
1. Verify the class has `@Component`, `@Service`, `@Repository`, or `@Controller` annotation
2. Check if the class is in a package scanned by `@ComponentScan` (must be in or below `@SpringBootApplication` class package)
3. Verify `@Configuration` classes with `@Bean` methods are being loaded
4. Check for conditional annotations (`@ConditionalOnProperty`, `@Profile`) that might exclude the bean
5. Look for typos in qualifier names with `@Qualifier`

**Quick Fixes:**
```java
// Ensure main class is at root package
@SpringBootApplication
public class Application { ... }

// Explicit component scan if needed
@ComponentScan(basePackages = {"com.example.main", "com.example.other"})

// Check bean registration
@Autowired
private ApplicationContext context;
Arrays.stream(context.getBeanDefinitionNames()).forEach(System.out::println);
```

### 2. Application Failed to Start
**Symptoms:**
- "Web server failed to start. Port 8080 was already in use"
- "Application run failed"
- Context initialization errors

**Debugging Steps:**
1. Check for port conflicts: `lsof -i :8080` or `netstat -an | grep 8080`
2. Review full stack trace for root cause (scroll up past Spring banner)
3. Check database connectivity if using JPA
4. Verify all required environment variables are set
5. Look for missing dependencies in pom.xml or build.gradle

**Quick Fixes:**
```properties
# Change port if in use
server.port=8081

# Enable debug startup logging
debug=true
logging.level.org.springframework=DEBUG

# Fail fast on missing properties
spring.main.allow-bean-definition-overriding=false
```

### 3. Circular Dependency
**Symptoms:**
- "The dependencies of some of the beans in the application context form a cycle"
- "Requested bean is currently in creation"

**Debugging Steps:**
1. Read the cycle chain in error message (A -> B -> C -> A)
2. Identify which dependency can be broken
3. Consider if the design needs refactoring

**Quick Fixes:**
```java
// Option 1: Use @Lazy on one dependency
@Autowired
@Lazy
private ServiceB serviceB;

// Option 2: Use setter injection
private ServiceB serviceB;

@Autowired
public void setServiceB(ServiceB serviceB) {
    this.serviceB = serviceB;
}

// Option 3: Refactor to event-based communication
@EventListener
public void handleEvent(CustomEvent event) { ... }
```

### 4. JPA/Hibernate Issues
**Symptoms:**
- "No EntityManager with actual transaction available"
- LazyInitializationException
- "Table doesn't exist" / Schema validation errors
- N+1 query problems

**Debugging Steps:**
1. Enable SQL logging to see actual queries
2. Check `@Transactional` placement (must be on public methods)
3. Verify entity relationships and cascade types
4. Check database schema matches entity definitions

**Quick Fixes:**
```properties
# Enable SQL debugging
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true
logging.level.org.hibernate.SQL=DEBUG
logging.level.org.hibernate.type.descriptor.sql.BasicBinder=TRACE

# Schema handling
spring.jpa.hibernate.ddl-auto=validate  # Recommended for debugging
spring.jpa.hibernate.ddl-auto=update    # Auto-update schema (dev only)
```

```java
// Fix LazyInitializationException
@Transactional(readOnly = true)
public Entity getWithChildren(Long id) {
    Entity e = repository.findById(id).orElseThrow();
    e.getChildren().size(); // Force initialization
    return e;
}

// Or use EntityGraph
@EntityGraph(attributePaths = {"children", "children.grandchildren"})
Optional<Entity> findById(Long id);
```

### 5. Security Configuration Problems
**Symptoms:**
- 403 Forbidden on all endpoints
- Authentication not working
- CORS errors
- CSRF token issues

**Debugging Steps:**
1. Enable security debug logging
2. Check filter chain order
3. Verify authentication provider configuration
4. Review SecurityFilterChain bean configuration

**Quick Fixes:**
```properties
# Enable security debugging
logging.level.org.springframework.security=DEBUG
logging.level.org.springframework.security.web.FilterChainProxy=DEBUG
```

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/public/**").permitAll()
                .requestMatchers("/actuator/health").permitAll()
                .anyRequest().authenticated()
            )
            .csrf(csrf -> csrf.disable()) // Only for APIs with token auth
            .cors(Customizer.withDefaults());
        return http.build();
    }
}
```

### 6. Property Binding Failures
**Symptoms:**
- "Failed to bind properties under 'x.y.z'"
- "Could not resolve placeholder"
- Configuration values not being read

**Debugging Steps:**
1. Check property file location (src/main/resources)
2. Verify property name matches exactly (case-sensitive, hyphen vs camelCase)
3. Check active profiles (`spring.profiles.active`)
4. Verify `@ConfigurationProperties` prefix matches

**Quick Fixes:**
```java
// Debug property sources
@Autowired
private Environment env;

@PostConstruct
public void debugProperties() {
    System.out.println("Active profiles: " + Arrays.toString(env.getActiveProfiles()));
    System.out.println("Property value: " + env.getProperty("my.property"));
}

// Ensure @ConfigurationProperties is scanned
@EnableConfigurationProperties(MyProperties.class)
@SpringBootApplication
public class Application { ... }
```

```properties
# Add to see property resolution
logging.level.org.springframework.boot.context.properties=DEBUG
```

## Debugging Tools

### Spring Boot Actuator
Essential for runtime diagnostics:
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

```properties
# Expose all actuator endpoints (dev only)
management.endpoints.web.exposure.include=*
management.endpoint.health.show-details=always
```

**Key Endpoints:**
- `/actuator/health` - Application health status
- `/actuator/beans` - All registered beans
- `/actuator/env` - Environment properties
- `/actuator/mappings` - Request mappings
- `/actuator/configprops` - Configuration properties
- `/actuator/conditions` - Auto-configuration report

### Remote JVM Debugging
```bash
# Maven
mvn spring-boot:run -Dspring-boot.run.jvmArguments="-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005"

# Gradle
./gradlew bootRun --debug-jvm

# Java directly
java -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005 -jar app.jar

# Docker Compose
environment:
  - JAVA_TOOL_OPTIONS=-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005
ports:
  - "5005:5005"
```

### Logback/Log4j2 Configuration
Create `src/main/resources/logback-spring.xml`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <include resource="org/springframework/boot/logging/logback/defaults.xml"/>

    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>

    <!-- Debug specific packages -->
    <logger name="org.springframework.web" level="DEBUG"/>
    <logger name="org.hibernate.SQL" level="DEBUG"/>
    <logger name="com.yourapp" level="DEBUG"/>

    <root level="INFO">
        <appender-ref ref="CONSOLE"/>
    </root>
</configuration>
```

### Spring Boot DevTools
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-devtools</artifactId>
    <scope>runtime</scope>
    <optional>true</optional>
</dependency>
```

**Features:**
- Automatic restart on code changes
- LiveReload browser integration
- Relaxed property binding in dev
- H2 console auto-configuration

### IntelliJ IDEA Spring Debugger (2025.2+)
- View active loaded beans with metadata
- See actual property values inline in .properties/.yaml
- Inspect bean scope, profile, and context
- View database connections
- Navigate to bean definitions

## The Four Phases (Spring Boot-specific)

### Phase 1: Gather Information
```bash
# Check application logs
tail -f logs/spring.log

# Check JVM status
jps -lv
jstat -gc <pid>
jstack <pid>

# Check actuator endpoints
curl localhost:8080/actuator/health
curl localhost:8080/actuator/env
curl localhost:8080/actuator/beans
```

### Phase 2: Reproduce and Isolate
```java
// Create minimal test case
@SpringBootTest(classes = {TestConfig.class, ProblemBean.class})
class IsolatedTest {
    @Autowired
    private ProblemBean bean;

    @Test
    void reproduceIssue() {
        // Minimal steps to reproduce
    }
}

// Use test slices for faster isolation
@WebMvcTest(ProblemController.class)
@DataJpaTest
@JsonTest
```

### Phase 3: Diagnose Root Cause
```java
// Add diagnostic logging
@Aspect
@Component
public class DiagnosticAspect {
    private static final Logger log = LoggerFactory.getLogger(DiagnosticAspect.class);

    @Around("execution(* com.yourapp.service.*.*(..))")
    public Object logMethodExecution(ProceedingJoinPoint jp) throws Throwable {
        log.debug("Entering: {}", jp.getSignature());
        try {
            Object result = jp.proceed();
            log.debug("Exiting: {} with result: {}", jp.getSignature(), result);
            return result;
        } catch (Exception e) {
            log.error("Exception in {}: {}", jp.getSignature(), e.getMessage());
            throw e;
        }
    }
}
```

### Phase 4: Fix and Verify
```bash
# Run targeted tests
./mvnw test -Dtest=ProblemTest

# Run full test suite
./mvnw verify

# Check for regressions
./mvnw test -Dtest=*IntegrationTest
```

## Quick Reference Commands

### Maven
```bash
# Run with debug logging
./mvnw spring-boot:run -Dspring-boot.run.arguments="--debug"

# Run with specific profile
./mvnw spring-boot:run -Dspring-boot.run.profiles=dev

# Skip tests and run
./mvnw spring-boot:run -DskipTests

# Generate dependency tree
./mvnw dependency:tree

# Check for dependency conflicts
./mvnw dependency:analyze

# Force update dependencies
./mvnw clean install -U
```

### Gradle
```bash
# Run with debug logging
./gradlew bootRun --args='--debug'

# Run with specific profile
./gradlew bootRun --args='--spring.profiles.active=dev'

# Show dependencies
./gradlew dependencies

# Refresh dependencies
./gradlew build --refresh-dependencies
```

### Docker
```bash
# Check container logs
docker logs <container_name> -f

# Shell into container
docker exec -it <container_name> /bin/sh

# Check container health
docker inspect --format='{{.State.Health.Status}}' <container_name>

# View container environment
docker exec <container_name> env | grep SPRING
```

### Kubernetes
```bash
# Get pod logs
kubectl logs <pod-name> -f

# Get previous container logs (after crash)
kubectl logs <pod-name> --previous

# Describe pod for events
kubectl describe pod <pod-name>

# Port forward for debugging
kubectl port-forward <pod-name> 5005:5005

# Shell into pod
kubectl exec -it <pod-name> -- /bin/sh
```

### Database Debugging
```bash
# Connect to PostgreSQL
psql -h localhost -U user -d database

# Show running queries
SELECT * FROM pg_stat_activity WHERE state = 'active';

# Connect to MySQL
mysql -h localhost -u user -p database

# Show process list
SHOW PROCESSLIST;
```

### JVM Diagnostics
```bash
# List Java processes
jps -lv

# Thread dump
jstack <pid> > thread_dump.txt

# Heap dump
jmap -dump:format=b,file=heap.hprof <pid>

# GC stats
jstat -gcutil <pid> 1000

# JVM flags
jinfo -flags <pid>
```

## Debugging Microservices

### Distributed Tracing
```xml
<!-- Add Micrometer Tracing -->
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-tracing-bridge-brave</artifactId>
</dependency>
<dependency>
    <groupId>io.zipkin.reporter2</groupId>
    <artifactId>zipkin-reporter-brave</artifactId>
</dependency>
```

```properties
# Zipkin configuration
management.tracing.sampling.probability=1.0
management.zipkin.tracing.endpoint=http://zipkin:9411/api/v2/spans
```

### Correlation IDs
```java
@Component
public class CorrelationIdFilter extends OncePerRequestFilter {
    private static final String CORRELATION_ID = "X-Correlation-ID";

    @Override
    protected void doFilterInternal(HttpServletRequest request,
            HttpServletResponse response, FilterChain chain) {
        String correlationId = request.getHeader(CORRELATION_ID);
        if (correlationId == null) {
            correlationId = UUID.randomUUID().toString();
        }
        MDC.put("correlationId", correlationId);
        response.setHeader(CORRELATION_ID, correlationId);
        try {
            chain.doFilter(request, response);
        } finally {
            MDC.remove("correlationId");
        }
    }
}
```

## Common Gotchas

1. **@Transactional on private methods** - Does not work, must be public
2. **Calling @Transactional method from same class** - Bypasses proxy, no transaction
3. **Missing @Repository on custom implementations** - Exception translation not applied
4. **@Value in constructor** - Field not yet injected, use @PostConstruct
5. **Static fields with @Autowired** - Never injected
6. **@ComponentScan without basePackages** - Only scans current package and below
7. **application.properties in wrong location** - Must be in src/main/resources root
8. **Profile-specific config not loading** - Check spring.profiles.active is set

## Further Reading

- [Spring Boot Reference Documentation](https://docs.spring.io/spring-boot/docs/current/reference/html/)
- [Spring Framework Core Technologies](https://docs.spring.io/spring-framework/reference/core.html)
- [Baeldung Spring Tutorials](https://www.baeldung.com/spring-boot)
