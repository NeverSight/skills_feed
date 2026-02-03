---
name: architecture
description: MVVM pattern, Clean Architecture, Repository pattern, dependency injection, SOLID principles.
version: "2.0.0"
sasmp_version: "1.3.0"

# Agent Binding
bonded_agent: 06-architecture
bond_type: PRIMARY_BOND

# Skill Configuration
atomic: true
single_responsibility: App architecture & design patterns

# Parameter Validation
parameters:
  pattern:
    type: string
    enum: [mvvm, clean_architecture, repository, di]
    required: false
  complexity:
    type: string
    enum: [simple, medium, complex]
    default: medium

# Retry Configuration
retry:
  max_attempts: 2
  backoff: exponential
  on_failure: suggest_simpler_pattern

# Observability
logging:
  level: info
  include: [pattern_type, layer, dependencies]
---

# App Architecture Skill

## Quick Start

### MVVM Pattern
```kotlin
@HiltViewModel
class UserViewModel @Inject constructor(
    private val repository: UserRepository
) : ViewModel() {
    private val _state = MutableLiveData<UiState>()
    val state: LiveData<UiState> = _state
    
    fun loadUser(id: Int) {
        viewModelScope.launch {
            _state.value = repository.getUser(id)
        }
    }
}
```

### Repository Pattern
```kotlin
interface UserRepository {
    suspend fun getUser(id: Int): User
}

class UserRepositoryImpl(
    private val dao: UserDao,
    private val api: UserApi
) : UserRepository {
    override suspend fun getUser(id: Int): User {
        return dao.getUser(id) ?: api.fetchUser(id)
    }
}
```

### Dependency Injection (Hilt)
```kotlin
@Module
@InstallIn(SingletonComponent::class)
object RepositoryModule {
    @Provides
    fun provideUserRepository(dao: UserDao, api: UserApi): UserRepository {
        return UserRepositoryImpl(dao, api)
    }
}
```

## Key Concepts

### MVVM Benefits
- Lifecycle awareness
- Configuration change handling
- Separation of concerns
- Testability

### Clean Architecture Layers
- Domain: Business rules
- Application: Use cases
- Presentation: UI
- Infrastructure: Data sources

### SOLID Principles
- S: Single Responsibility
- O: Open/Closed
- L: Liskov Substitution
- I: Interface Segregation
- D: Dependency Inversion

## Best Practices

✅ Dependency injection
✅ Interface-based design
✅ Layered architecture
✅ Single responsibility
✅ Testable code

## Resources

- [Architecture Guide](https://developer.android.com/jetpack/guide)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
- [Hilt Documentation](https://developer.android.com/training/dependency-injection/hilt-android)
