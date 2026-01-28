---
name: kotlin-spring
description: Spring Boot with Kotlin - controllers, services, coroutines
version: "1.0.0"
sasmp_version: "1.3.0"
bonded_agent: 05-kotlin-backend
bond_type: SECONDARY_BOND

execution:
  timeout_ms: 30000
  retry:
    max_attempts: 3
    backoff: exponential
    initial_delay_ms: 1000

parameters:
  required:
    - name: topic
      type: string
      validation: "^(setup|controllers|jpa|coroutines|testing)$"
  optional:
    - name: spring_version
      type: string
      default: "3.2"

logging:
  level: info
  events: [skill_invoked, topic_loaded, error_occurred]
---

# Kotlin Spring Skill

Idiomatic Spring Boot development with Kotlin.

## Topics Covered

### REST Controllers
```kotlin
@RestController
@RequestMapping("/api/v1/users")
class UserController(private val userService: UserService) {

    @GetMapping
    suspend fun findAll(): List<UserDTO> = userService.findAll()

    @GetMapping("/{id}")
    suspend fun findById(@PathVariable id: Long): UserDTO =
        userService.findById(id) ?: throw ResponseStatusException(NOT_FOUND)

    @PostMapping
    @ResponseStatus(CREATED)
    suspend fun create(@Valid @RequestBody request: CreateUserRequest) =
        userService.create(request)
}
```

### Coroutines Integration
```kotlin
@Service
class UserService(private val repository: UserRepository) {
    suspend fun findAll() = withContext(Dispatchers.IO) {
        repository.findAll().map { it.toDTO() }
    }
}
```

### Data JPA
```kotlin
@Entity
@Table(name = "users")
class User(
    @Id @GeneratedValue val id: Long = 0,
    @Column(nullable = false) val email: String,
    @Column(nullable = false) val name: String
)

interface UserRepository : JpaRepository<User, Long> {
    fun findByEmail(email: String): User?
}
```

### Testing
```kotlin
@WebMvcTest(UserController::class)
class UserControllerTest {
    @Autowired lateinit var mockMvc: MockMvc
    @MockkBean lateinit var userService: UserService

    @Test
    fun `GET users returns list`() {
        every { userService.findAll() } returns listOf(user)
        mockMvc.get("/api/v1/users").andExpect { status { isOk() } }
    }
}
```

## Troubleshooting

| Issue | Resolution |
|-------|------------|
| @RequestBody null | Add jackson-module-kotlin |
| Coroutines not working | Enable WebFlux or use blocking |

## Usage
```
Skill("kotlin-spring")
```
