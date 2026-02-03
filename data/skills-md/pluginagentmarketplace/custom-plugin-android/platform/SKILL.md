---
name: platform
description: Android core components lifecycle, Activities, Fragments, Services, Intent system.
version: "2.0.0"
sasmp_version: "1.3.0"

# Agent Binding
bonded_agent: 02-platform
bond_type: PRIMARY_BOND

# Skill Configuration
atomic: true
single_responsibility: Android platform components & lifecycle

# Parameter Validation
parameters:
  component:
    type: string
    enum: [activity, fragment, service, intent, permission]
    required: false
  lifecycle_state:
    type: string
    required: false

# Retry Configuration
retry:
  max_attempts: 2
  backoff: exponential
  on_failure: return_lifecycle_diagram

# Observability
logging:
  level: info
  include: [query, component_type, response_time]
---

# Android Platform Skill

## Quick Start

### Activity Lifecycle
```kotlin
class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
    }
    
    override fun onDestroy() {
        super.onDestroy()
        // Cleanup
    }
}
```

### Fragment Usage
```kotlin
class UserFragment : Fragment() {
    private val viewModel: UserViewModel by viewModels()
    
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        viewModel.user.observe(viewLifecycleOwner) { user ->
            updateUI(user)
        }
    }
}
```

## Key Concepts

### Lifecycle Callbacks
- `onCreate()`: Initial setup
- `onStart()`: Become visible
- `onResume()`: Gain focus
- `onPause()`: Lose focus
- `onStop()`: Hidden
- `onDestroy()`: Final cleanup

### Fragment Lifecycle
Similar to Activity but with:
- `onAttach()`: Attached to activity
- `onDetach()`: Detached
- Fragment manager for transactions

### Intent System
```kotlin
// Explicit
startActivity(Intent(this, DetailActivity::class.java))

// Implicit
startActivity(Intent(Intent.ACTION_VIEW, Uri.parse("https://example.com")))
```

### Services
- Started: `startService()`
- Bound: `bindService()`
- Foreground: Visible notification

## Best Practices

✅ Handle lifecycle properly
✅ Use ViewModel for state
✅ Unregister listeners
✅ Test configuration changes
✅ Respect process lifecycle

## Resources

- [Activity Lifecycle](https://developer.android.com/guide/components/activities)
- [Fragment Guide](https://developer.android.com/guide/fragments)
- [Service Documentation](https://developer.android.com/guide/components/services)
