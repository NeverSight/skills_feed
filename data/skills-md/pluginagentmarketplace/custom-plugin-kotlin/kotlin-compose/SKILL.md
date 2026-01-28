---
name: kotlin-compose
description: Jetpack Compose - composables, state, effects, theming
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
    - name: topic
      type: string
      validation: "^(composables|state|effects|theming|testing)$"
  optional:
    - name: compose_version
      type: string
      default: "1.6.0"

logging:
  level: info
  events: [skill_invoked, topic_loaded, error_occurred]
---

# Kotlin Compose Skill

Build modern UIs with Jetpack Compose declarative patterns.

## Topics Covered

### State Management
```kotlin
@Composable
fun Counter() {
    var count by remember { mutableIntStateOf(0) }
    Button(onClick = { count++ }) { Text("Count: $count") }
}

// Derived state
val isValid by remember { derivedStateOf { email.isNotBlank() && password.length >= 8 } }
```

### Side Effects
```kotlin
@Composable
fun UserScreen(userId: String) {
    LaunchedEffect(userId) {
        viewModel.loadUser(userId)
    }

    DisposableEffect(Unit) {
        val listener = viewModel.addListener()
        onDispose { listener.remove() }
    }
}
```

### Modifiers
```kotlin
Box(
    modifier = Modifier
        .fillMaxSize()
        .padding(16.dp)
        .background(MaterialTheme.colorScheme.surface)
        .clickable { onClick() }
)
```

### Material 3 Theming
```kotlin
@Composable
fun AppTheme(content: @Composable () -> Unit) {
    val colorScheme = if (isSystemInDarkTheme()) darkColorScheme() else lightColorScheme()
    MaterialTheme(colorScheme = colorScheme, typography = Typography, content = content)
}
```

## Troubleshooting

| Issue | Resolution |
|-------|------------|
| Infinite recomposition | Use remember or derivedStateOf |
| State lost on rotation | Use rememberSaveable or ViewModel |

## Usage
```
Skill("kotlin-compose")
```
