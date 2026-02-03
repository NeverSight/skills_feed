---
name: ui
description: XML layouts, ConstraintLayout, Jetpack Compose, Material Design 3.
version: "2.0.0"
sasmp_version: "1.3.0"

# Agent Binding
bonded_agent: 03-ui-development
bond_type: PRIMARY_BOND

# Skill Configuration
atomic: true
single_responsibility: UI design & implementation

# Parameter Validation
parameters:
  paradigm:
    type: string
    enum: [xml, compose, both]
    default: compose
  design_system:
    type: string
    enum: [material2, material3]
    default: material3

# Retry Configuration
retry:
  max_attempts: 2
  backoff: exponential
  on_failure: return_basic_layout

# Observability
logging:
  level: info
  include: [query, ui_type, accessibility_check]
---

# UI Design Skill

## Quick Start

### ConstraintLayout
```xml
<androidx.constraintlayout.widget.ConstraintLayout>
    <Button
        android:id="@+id/btn"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintTop_toTopOf="parent" />
</androidx.constraintlayout.widget.ConstraintLayout>
```

### Jetpack Compose
```kotlin
Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
    Text("Hello Compose", fontSize = 20.sp)
    Button(onClick = { }) { Text("Click Me") }
}
```

### Material Design 3
```kotlin
Scaffold(
    topBar = { TopAppBar(title = { Text("MyApp") }) }
) { padding ->
    // Content
}
```

## Key Concepts

### Constraint Types
- Start/End, Top/Bottom
- Chains (spread, packed)
- Guidelines
- Barriers
- Bias

### Compose State
```kotlin
var count by remember { mutableStateOf(0) }
Button(onClick = { count++ }) { Text("Count: $count") }
```

### Material Components
- Buttons (filled, outlined, text)
- Cards, FABs, Dialogs
- Navigation patterns
- Theme system

## Best Practices

✅ Use ConstraintLayout for efficiency
✅ Implement Material Design
✅ Test on multiple screen sizes
✅ Optimize rendering performance
✅ Support accessibility

## Resources

- [ConstraintLayout Guide](https://developer.android.com/training/constraint-layout)
- [Compose Documentation](https://developer.android.com/develop/ui/compose)
- [Material Design 3](https://m3.material.io/)
