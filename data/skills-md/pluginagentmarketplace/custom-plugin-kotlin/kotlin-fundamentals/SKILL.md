---
name: kotlin-fundamentals
description: Kotlin language fundamentals - syntax, null safety, data classes, extensions
version: "1.0.0"
sasmp_version: "1.3.0"
bonded_agent: 01-kotlin-fundamentals
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
      validation: "^(syntax|null_safety|data_classes|extensions|collections|idioms)$"
  optional:
    - name: kotlin_version
      type: string
      default: "2.0"

logging:
  level: info
  events: [skill_invoked, topic_loaded, error_occurred]
---

# Kotlin Fundamentals Skill

Master Kotlin programming fundamentals with production-ready patterns.

## Topics Covered

### Null Safety
```kotlin
// Safe call + Elvis
val name = user?.name ?: "Anonymous"

// requireNotNull for validation
requireNotNull(user) { "User required" }
```

### Data Classes
```kotlin
data class User(val id: Long, val name: String) {
    init { require(name.isNotBlank()) }
}
```

### Scope Functions
| Function | Context | Returns | Use Case |
|----------|---------|---------|----------|
| `let` | it | Lambda result | Null-safe transforms |
| `apply` | this | Same object | Object configuration |
| `run` | this | Lambda result | Object scope + result |
| `also` | it | Same object | Side effects |

## Troubleshooting

| Issue | Resolution |
|-------|------------|
| NPE despite null check | Check platform types from Java |
| Smart cast fails | Use local variable or let |

## Usage
```
Skill("kotlin-fundamentals")
```
