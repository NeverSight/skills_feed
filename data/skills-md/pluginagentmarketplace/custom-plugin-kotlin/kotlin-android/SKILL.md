---
name: kotlin-android
description: Modern Android development - Jetpack, Compose, Architecture Components
version: "1.0.0"
sasmp_version: "1.3.0"
bonded_agent: 02-kotlin-android
bond_type: PRIMARY_BOND

execution:
  timeout_ms: 30000
  retry:
    max_attempts: 3
    backoff: exponential
    initial_delay_ms: 1000

parameters:
  required:
    - name: component
      type: string
      validation: "^(viewmodel|compose|navigation|room|workmanager)$"
  optional:
    - name: min_sdk
      type: integer
      default: 24

logging:
  level: info
  events: [skill_invoked, component_loaded, error_occurred]
---

# Kotlin Android Skill

Production-ready Android development with Jetpack libraries.

## Topics Covered

### MVVM Pattern
```kotlin
@HiltViewModel
class UserViewModel @Inject constructor(
    private val repository: UserRepository
) : ViewModel() {
    private val _uiState = MutableStateFlow(UiState())
    val uiState = _uiState.asStateFlow()

    fun load() = viewModelScope.launch {
        _uiState.update { it.copy(isLoading = true) }
        repository.getUsers()
            .onSuccess { users -> _uiState.update { it.copy(users = users, isLoading = false) } }
    }
}
```

### Compose UI
```kotlin
@Composable
fun UserScreen(viewModel: UserViewModel = hiltViewModel()) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    UserContent(state)
}
```

### Type-Safe Navigation
```kotlin
@Serializable
data class ProfileRoute(val userId: String)

composable<ProfileRoute> { entry ->
    val route: ProfileRoute = entry.toRoute()
}
```

## Troubleshooting

| Issue | Resolution |
|-------|------------|
| Recomposition loop | Mark class @Stable or use derivedStateOf |
| ViewModel recreated | Use hiltViewModel() not viewModel() |

## Usage
```
Skill("kotlin-android")
```
