---
name: kotlin-multiplatform
description: Kotlin Multiplatform - shared code, expect/actual, iOS integration
version: "1.0.0"
sasmp_version: "1.3.0"
bonded_agent: 04-kotlin-multiplatform
bond_type: PRIMARY_BOND

execution:
  timeout_ms: 30000
  retry:
    max_attempts: 3
    backoff: exponential
    initial_delay_ms: 1000

parameters:
  required:
    - name: target
      type: string
      validation: "^(setup|shared|expect_actual|ios)$"
  optional:
    - name: platforms
      type: array
      default: ["android", "ios"]

logging:
  level: info
  events: [skill_invoked, target_loaded, error_occurred]
---

# Kotlin Multiplatform Skill

Build cross-platform applications with shared Kotlin code.

## Topics Covered

### Project Setup
```kotlin
kotlin {
    androidTarget()
    listOf(iosX64(), iosArm64(), iosSimulatorArm64()).forEach {
        it.binaries.framework { baseName = "Shared"; isStatic = true }
    }
    sourceSets {
        commonMain.dependencies {
            implementation("io.ktor:ktor-client-core:2.3.8")
        }
        androidMain.dependencies { implementation("io.ktor:ktor-client-okhttp:2.3.8") }
        iosMain.dependencies { implementation("io.ktor:ktor-client-darwin:2.3.8") }
    }
}
```

### expect/actual
```kotlin
// commonMain
expect class SecureStorage { fun get(key: String): String? }

// androidMain
actual class SecureStorage { actual fun get(key: String) = prefs.getString(key, null) }

// iosMain
actual class SecureStorage { actual fun get(key: String) = KeychainWrapper.get(key) }
```

## Troubleshooting

| Issue | Resolution |
|-------|------------|
| "No actual for expect" | Add implementation in platform source set |
| iOS framework not found | Run linkDebugFrameworkIos task |

## Usage
```
Skill("kotlin-multiplatform")
```
