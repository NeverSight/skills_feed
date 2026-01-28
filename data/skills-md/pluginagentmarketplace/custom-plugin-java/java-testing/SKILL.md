---
name: java-testing
description: Test Java applications - JUnit 5, Mockito, integration testing, TDD patterns
sasmp_version: "1.3.0"
version: "3.0.0"
bonded_agent: 04-java-testing
bond_type: PRIMARY_BOND
allowed-tools: Read, Write, Bash, Glob, Grep

# Parameter Validation
parameters:
  test_type:
    type: string
    enum: [unit, integration, e2e, contract]
    description: Type of test to create
  framework:
    type: string
    default: junit5
    enum: [junit5, testng]
    description: Testing framework
---

# Java Testing Skill

Write comprehensive tests for Java applications with modern testing practices.

## Overview

This skill covers Java testing with JUnit 5, Mockito, AssertJ, and integration testing with Spring Boot Test and Testcontainers. Includes TDD patterns and test coverage strategies.

## When to Use This Skill

Use when you need to:
- Write unit tests with JUnit 5
- Create mocks with Mockito
- Build integration tests with Testcontainers
- Implement TDD/BDD practices
- Improve test coverage

## Topics Covered

### JUnit 5
- @Test, @Nested, @DisplayName
- @ParameterizedTest with sources
- Lifecycle annotations
- Extensions and custom annotations

### Mockito
- @Mock, @InjectMocks, @Spy
- Stubbing (when/thenReturn)
- Verification (verify, times)
- BDD style (given/willReturn)

### AssertJ
- Fluent assertions
- Collection assertions
- Exception assertions
- Custom assertions

### Integration Testing
- @SpringBootTest slices
- Testcontainers setup
- MockMvc for APIs
- Database testing

## Quick Reference

```java
// Unit Test with Mockito
@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private UserService userService;

    @Test
    @DisplayName("Should find user by ID")
    void shouldFindUserById() {
        // Given
        User user = new User(1L, "John");
        given(userRepository.findById(1L)).willReturn(Optional.of(user));

        // When
        Optional<User> result = userService.findById(1L);

        // Then
        assertThat(result)
            .isPresent()
            .hasValueSatisfying(u ->
                assertThat(u.getName()).isEqualTo("John"));
        then(userRepository).should().findById(1L);
    }
}

// Parameterized Test
@ParameterizedTest
@CsvSource({
    "valid@email.com, true",
    "invalid-email, false",
    "'', false"
})
void shouldValidateEmail(String email, boolean expected) {
    assertThat(validator.isValid(email)).isEqualTo(expected);
}

// Integration Test with Testcontainers
@Testcontainers
@SpringBootTest
class OrderRepositoryIT {

    @Container
    static PostgreSQLContainer<?> postgres =
        new PostgreSQLContainer<>("postgres:15");

    @DynamicPropertySource
    static void configure(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }

    @Autowired
    private OrderRepository repository;

    @Test
    void shouldPersistOrder() {
        Order saved = repository.save(new Order("item", 100.0));
        assertThat(saved.getId()).isNotNull();
    }
}

// API Test with MockMvc
@WebMvcTest(UserController.class)
class UserControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private UserService userService;

    @Test
    void shouldReturnUser() throws Exception {
        given(userService.findById(1L))
            .willReturn(Optional.of(new User(1L, "John")));

        mockMvc.perform(get("/api/users/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.name").value("John"));
    }
}
```

## Test Data Builders

```java
public class UserTestBuilder {
    private Long id = 1L;
    private String name = "John Doe";
    private String email = "john@example.com";
    private boolean active = true;

    public static UserTestBuilder aUser() {
        return new UserTestBuilder();
    }

    public UserTestBuilder withName(String name) {
        this.name = name;
        return this;
    }

    public UserTestBuilder inactive() {
        this.active = false;
        return this;
    }

    public User build() {
        return new User(id, name, email, active);
    }
}

// Usage
User user = aUser().withName("Jane").inactive().build();
```

## Coverage Goals

```xml
<!-- JaCoCo configuration -->
<configuration>
    <rules>
        <rule>
            <element>BUNDLE</element>
            <limits>
                <limit>
                    <counter>LINE</counter>
                    <value>COVEREDRATIO</value>
                    <minimum>0.80</minimum>
                </limit>
            </limits>
        </rule>
    </rules>
</configuration>
```

## Troubleshooting

### Common Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| Mock not working | Missing @ExtendWith | Add MockitoExtension |
| NPE in test | Mock not initialized | Check @InjectMocks |
| Flaky test | Shared state | Isolate test data |
| Context fails | Missing bean | Use @MockBean |

### Debug Checklist
```
□ Run single test in isolation
□ Check mock setup matches invocation
□ Verify @BeforeEach setup
□ Review @Transactional boundaries
□ Check for shared mutable state
```

## Usage

```
Skill("java-testing")
```

## Related Skills
- `java-testing-advanced` - Advanced patterns
- `java-spring-boot` - Spring test slices
