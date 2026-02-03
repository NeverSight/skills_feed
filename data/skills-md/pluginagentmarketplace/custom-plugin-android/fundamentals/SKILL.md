---
name: fundamentals
description: Master Kotlin syntax, OOP principles, SOLID practices, functional programming, and data structures.
version: "2.0.0"
sasmp_version: "1.3.0"

# Agent Binding
bonded_agent: 01-android-fundamentals
bond_type: PRIMARY_BOND

# Skill Configuration
atomic: true
single_responsibility: Kotlin & OOP fundamentals

# Parameter Validation
parameters:
  topic:
    type: string
    enum: [kotlin, oop, solid, functional, collections]
    required: false
  code_context:
    type: string
    required: false

# Retry Configuration
retry:
  max_attempts: 2
  backoff: exponential
  on_failure: return_basic_example

# Observability
logging:
  level: info
  include: [query, response_time, errors]
---

# Kotlin Fundamentals Skill

## Quick Start

```kotlin
// Variables
val immutable = "constant"
var mutable = "variable"

// Functions
fun greet(name: String): String = "Hello, $name"

// Classes
data class User(val id: Int, val name: String)

// Null safety
val user: User? = null
user?.name // safe call
user?.name ?: "Unknown" // elvis operator
```

## Key Concepts

### Null Safety
- `?` for nullable types
- `!!` for non-null assertion (avoid)
- `?:` elvis operator for defaults
- `?.let { }` for null-safe blocks

### Extension Functions
```kotlin
fun String.isValidEmail(): Boolean = contains("@")
val valid = "user@example.com".isValidEmail()
```

### Scope Functions
- `apply`: Configure object
- `let`: Transform
- `run`: Execute with context
- `with`: Receiver operations
- `also`: Side effects

### Coroutines
```kotlin
viewModelScope.launch {
    val data = withContext(Dispatchers.IO) {
        fetchData()
    }
}
```

## SOLID Principles Summary

1. **SRP**: One responsibility per class
2. **OCP**: Open for extension, closed for modification  
3. **LSP**: Substitutable subtypes
4. **ISP**: Specific interfaces
5. **DIP**: Depend on abstractions

## Learning Resources

- [Kotlin Docs](https://kotlinlang.org/docs/)
- [Kotlin Coroutines](https://kotlinlang.org/docs/coroutines-overview.html)
- [Effective Kotlin](https://kt.academy/)
