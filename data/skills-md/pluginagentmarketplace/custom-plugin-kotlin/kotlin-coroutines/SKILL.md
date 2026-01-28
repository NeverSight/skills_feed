---
name: kotlin-coroutines
description: Kotlin coroutines - structured concurrency, Flows, exception handling
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
    - name: pattern
      type: string
      validation: "^(basic|structured|exception|testing)$"
  optional:
    - name: dispatcher
      type: string
      default: "Default"

logging:
  level: info
  events: [skill_invoked, pattern_loaded, error_occurred]
---

# Kotlin Coroutines Skill

Master asynchronous programming with structured concurrency.

## Topics Covered

### Structured Concurrency
```kotlin
// ✅ Structured - cancellation propagates
class Repository(private val scope: CoroutineScope) {
    suspend fun load() = withContext(Dispatchers.IO) { fetch() }
}

// ❌ Avoid GlobalScope
GlobalScope.launch { /* leaks */ }
```

### Exception Handling
```kotlin
suspend fun loadData() = supervisorScope {
    val a = async { fetchA() }
    val b = async { fetchB() }
    Result(a.awaitOrNull(), b.awaitOrNull())
}

// Never swallow CancellationException
catch (e: Exception) {
    if (e is CancellationException) throw e
}
```

### Testing
```kotlin
@Test
fun test() = runTest {
    val vm = ViewModel(testDispatcher)
    vm.load()
    advanceUntilIdle()
    assertThat(vm.state.value.data).isNotNull()
}
```

## Troubleshooting

| Issue | Resolution |
|-------|------------|
| Coroutine leak | Use structured scopes, not GlobalScope |
| Test hangs | Inject TestDispatcher, use advanceUntilIdle() |

## Usage
```
Skill("kotlin-coroutines")
```
