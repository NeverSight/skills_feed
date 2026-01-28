---
name: kotlin-flow
description: Kotlin Flow - StateFlow, SharedFlow, operators, testing
version: "1.0.0"
sasmp_version: "1.3.0"
bonded_agent: 03-kotlin-coroutines
bond_type: PRIMARY_BOND

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
      validation: "^(basics|operators|hot_flows|testing)$"
  optional:
    - name: include_examples
      type: boolean
      default: true

logging:
  level: info
  events: [skill_invoked, topic_loaded, error_occurred]
---

# Kotlin Flow Skill

Reactive programming with Kotlin Flow.

## Topics Covered

### Cold vs Hot Flows
```kotlin
// Cold Flow - starts fresh for each collector
fun loadData(): Flow<Data> = flow {
    emit(fetchData())
}

// Hot Flow - shared state
private val _state = MutableStateFlow(State())
val state: StateFlow<State> = _state.asStateFlow()
```

### Flow Operators
```kotlin
fun searchUsers(query: Flow<String>): Flow<List<User>> =
    query
        .debounce(300)
        .filter { it.length >= 2 }
        .distinctUntilChanged()
        .flatMapLatest { term -> userRepository.search(term) }
        .catch { emit(emptyList()) }
```

### Combining Flows
```kotlin
val dashboard: Flow<Dashboard> = combine(
    userFlow,
    ordersFlow,
    notificationsFlow
) { user, orders, notifications ->
    Dashboard(user, orders.size, notifications.count())
}
```

### Testing with Turbine
```kotlin
@Test
fun `flow emits values`() = runTest {
    viewModel.state.test {
        assertThat(awaitItem().isLoading).isFalse()
        viewModel.load()
        assertThat(awaitItem().isLoading).isTrue()
        advanceUntilIdle()
        assertThat(awaitItem().data).isNotNull()
    }
}
```

## Troubleshooting

| Issue | Resolution |
|-------|------------|
| Flow never emits | Add terminal operator (collect, first) |
| Stale data in UI | Use stateIn or shareIn properly |

## Usage
```
Skill("kotlin-flow")
```
