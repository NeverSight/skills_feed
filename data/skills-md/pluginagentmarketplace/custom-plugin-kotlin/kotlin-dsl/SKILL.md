---
name: kotlin-dsl
description: Kotlin DSL - type-safe builders, Gradle DSL, @DslMarker
version: "1.0.0"
sasmp_version: "1.3.0"
bonded_agent: 07-kotlin-dsl
bond_type: PRIMARY_BOND

execution:
  timeout_ms: 30000
  retry:
    max_attempts: 3
    backoff: exponential
    initial_delay_ms: 1000

parameters:
  required:
    - name: type
      type: string
      validation: "^(gradle|custom|html|config)$"
  optional:
    - name: immutable
      type: boolean
      default: true

logging:
  level: info
  events: [skill_invoked, type_loaded, error_occurred]
---

# Kotlin DSL Skill

Build type-safe DSLs with Kotlin's language features.

## Topics Covered

### @DslMarker for Scope Control
```kotlin
@DslMarker
annotation class HtmlDsl

@HtmlDsl
class HTML { fun body(block: Body.() -> Unit) { } }

@HtmlDsl
class Body { fun p(text: String) { } }

// Usage - scoped correctly
html { body { p("Text") } }
```

### Gradle Convention Plugin
```kotlin
// kotlin-library.gradle.kts
plugins { kotlin("jvm"); `java-library` }

kotlin { jvmToolchain(17) }

dependencies {
    testImplementation(kotlin("test"))
    testImplementation("io.mockk:mockk:1.13.9")
}

tasks.test { useJUnitPlatform() }
```

### Type-Safe Config Builder
```kotlin
@ConfigDsl
class ServerConfig private constructor(val host: String, val port: Int) {
    class Builder {
        var host = "localhost"
        var port = 8080
        fun build() = ServerConfig(host, port)
    }
}

fun serverConfig(block: ServerConfig.Builder.() -> Unit) =
    ServerConfig.Builder().apply(block).build()

// Usage
val config = serverConfig { host = "api.example.com"; port = 443 }
```

## Troubleshooting

| Issue | Resolution |
|-------|------------|
| Scope pollution | Add @DslMarker annotation |
| Gradle cache stale | Run ./gradlew --stop |

## Usage
```
Skill("kotlin-dsl")
```
