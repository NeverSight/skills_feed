---
name: Unity Fundamentals
description: This skill should be used when the user asks about "Unity lifecycle", "MonoBehaviour methods", "Awake vs Start", "Update vs FixedUpdate", "Unity serialization", "[SerializeField]", "GetComponent", "component references", "Unity prefabs", "prefab workflow", or needs guidance on fundamental Unity patterns and best practices.
version: 0.1.0
---

# Unity Fundamentals

Comprehensive guidance on Unity's core systems, MonoBehaviour lifecycle, serialization, component architecture, and prefab workflows.

## Overview

Unity development centers around MonoBehaviour components, the Component pattern, and a specific lifecycle of callback methods. Understanding these fundamentals is critical for writing correct, performant Unity code. This skill covers:

- MonoBehaviour lifecycle methods and their proper usage
- Serialization system and Inspector integration
- Component-based architecture and GetComponent patterns
- Prefab workflows and best practices

## MonoBehaviour Lifecycle

Unity calls specific methods on MonoBehaviour scripts in a predetermined order. Using the wrong method leads to bugs, null references, and poor performance.

### Initialization Methods

#### Awake()

Called when the script instance loads, before any Start() calls. Use for **initializing this object's state**.

```csharp
private void Awake()
{
    // Cache component references on THIS GameObject
    rigidbody = GetComponent<Rigidbody>();
    animator = GetComponent<Animator>();

    // Initialize private state
    currentHealth = maxHealth;
    inventory = new List<Item>();

    // DON'T reference other objects - they may not be initialized yet
}
```

**Use Awake() for:**
- Caching component references
- Initializing private fields
- Setting up internal state
- Creating singletons/managers

**Don't use Awake() for:**
- Referencing other GameObjects (use Start instead)
- Performing operations that depend on other scripts being ready

#### Start()

Called before the first Update(), after all Awake() calls complete. Use for **setup that references other objects**.

```csharp
private void Start()
{
    // Safe to reference other GameObjects - they're initialized
    playerTransform = GameObject.FindWithTag("Player").transform;
    gameManager = FindObjectOfType<GameManager>();

    // Register with managers or systems
    GameManager.Instance.RegisterEnemy(this);

    // Perform initialization that depends on other components
    SetupWeapon(gameManager.GetStartingWeapon());
}
```

**Use Start() for:**
- Finding and referencing other GameObjects
- Calling initialization methods on other components
- Registering with managers or systems
- Setup that depends on scene being fully initialized

**Common Pattern:**
```csharp
private Camera mainCamera;  // Cache in Awake
private Transform target;    // Find in Start

private void Awake()
{
    mainCamera = Camera.main;  // Cache expensive lookup
}

private void Start()
{
    target = GameObject.FindWithTag("Target").transform;  // Find after scene loads
}
```

#### OnEnable() / OnDisable()

Called when GameObject becomes active/inactive. Use for **subscribing/unsubscribing from events**.

```csharp
private void OnEnable()
{
    // Subscribe to events
    GameEvents.OnPlayerDied += HandlePlayerDeath;
    InputManager.OnJumpPressed += HandleJump;

    // Re-enable functionality
    StartCoroutine(SpawnEnemies());
}

private void OnDisable()
{
    // Unsubscribe from events (prevents memory leaks!)
    GameEvents.OnPlayerDied -= HandlePlayerDeath;
    InputManager.OnJumpPressed -= HandleJump;

    // Clean up temporary state
    StopAllCoroutines();
}
```

**Critical:** Always unsubscribe in OnDisable() to prevent memory leaks.

### Update Methods

#### Update()

Called every frame. Use sparingly - performance critical.

```csharp
private void Update()
{
    // Input handling
    if (Input.GetKeyDown(KeyCode.Space))
        Jump();

    // Frame-dependent logic
    UpdateUI();

    // AVOID expensive operations here
    // DON'T call GetComponent every frame
    // DON'T use Find methods
}
```

**Avoid Update() when possible.** Prefer event-driven approaches.

#### FixedUpdate()

Called at fixed timestep (default 50 FPS). Use for **physics operations only**.

```csharp
private void FixedUpdate()
{
    // Physics operations
    rigidbody.AddForce(moveDirection * moveSpeed);

    // Physics-based movement
    rigidbody.MovePosition(transform.position + velocity * Time.fixedDeltaTime);

    // DON'T handle input here (use Update)
    // DON'T update UI here (use Update or LateUpdate)
}
```

**Rule:** If it touches Rigidbody or physics, use FixedUpdate(). Everything else uses Update() or event-driven approaches.

#### LateUpdate()

Called after all Update() calls. Use for **camera follow and final adjustments**.

```csharp
private void LateUpdate()
{
    // Camera follow (after player moved in Update)
    transform.position = target.position + offset;

    // Final position adjustments
    ClampToBounds();

    // UI updates that depend on world state
    UpdateHealthBar();
}
```

### Destruction Methods

#### OnDestroy()

Called when GameObject is destroyed. Use for **final cleanup**.

```csharp
private void OnDestroy()
{
    // Unsubscribe from static events
    GameEvents.OnPlayerDied -= HandlePlayerDeath;

    // Release resources
    if (texture != null)
        Destroy(texture);

    // Notify other systems
    GameManager.Instance.UnregisterEnemy(this);
}
```

### Lifecycle Order Summary

1. **Awake()** - Initialize self
2. **OnEnable()** - Subscribe to events
3. **Start()** - Reference others, final setup
4. **FixedUpdate()** - Physics (50 FPS)
5. **Update()** - Per-frame logic (variable FPS)
6. **LateUpdate()** - Camera, final adjustments
7. **OnDisable()** - Unsubscribe from events
8. **OnDestroy()** - Final cleanup

## Serialization System

Unity's serialization system controls what appears in the Inspector and how data persists.

### Serialized Fields

Make private fields editable in Inspector:

```csharp
[SerializeField] private int maxHealth = 100;
[SerializeField] private float moveSpeed = 5f;
[SerializeField] private GameObject prefab;
```

**Benefits:**
- Keeps encapsulation (private access)
- Inspector editing
- Prefab/scene data persistence

**Best Practice:** Prefer `[SerializeField] private` over `public` fields.

### Header and Tooltip

Organize Inspector sections:

```csharp
[Header("Movement Settings")]
[Tooltip("Maximum movement speed in units per second")]
[SerializeField] private float moveSpeed = 5f;

[Tooltip("Rotation speed in degrees per second")]
[SerializeField] private float rotationSpeed = 180f;

[Header("Combat Settings")]
[SerializeField] private int attackDamage = 25;
```

### Serialization Rules

**What Unity serializes:**
- Public fields (unless [HideInInspector])
- Private fields with [SerializeField]
- Supported types: primitives, Unity objects, structs, arrays, Lists

**What Unity doesn't serialize:**
- Properties
- Private fields without [SerializeField]
- Dictionaries
- Interfaces
- Static fields

### Properties vs Serialized Fields

```csharp
// DON'T expose internal state directly
public int health;  // Bad: public field

// DO use properties for controlled access
[SerializeField] private int health = 100;
public int Health
{
    get => health;
    set
    {
        health = Mathf.Clamp(value, 0, maxHealth);
        OnHealthChanged?.Invoke(health);
    }
}
```

## Component Architecture

Unity uses the Component pattern - functionality composed from multiple components.

### GetComponent Pattern

**Cache references in Awake()** to avoid repeated lookups:

```csharp
// ❌ BAD - Repeated GetComponent calls
private void Update()
{
    GetComponent<Rigidbody>().velocity = Vector3.forward;  // Expensive!
}

// ✅ GOOD - Cache once
private Rigidbody rb;

private void Awake()
{
    rb = GetComponent<Rigidbody>();
}

private void Update()
{
    rb.velocity = Vector3.forward;  // Fast
}
```

### Component Variations

```csharp
// GetComponent<T>() - On this GameObject
rb = GetComponent<Rigidbody>();

// GetComponentInChildren<T>() - This GameObject and children
animator = GetComponentInChildren<Animator>();

// GetComponentInParent<T>() - This GameObject and parents
canvas = GetComponentInParent<Canvas>();

// GetComponents<T>() - Multiple components
Collider[] colliders = GetComponents<Collider>();
```

**Performance:** Cache all GetComponent results. Never call in Update/FixedUpdate.

### Required Components

Declare component dependencies:

```csharp
[RequireComponent(typeof(Rigidbody))]
[RequireComponent(typeof(Collider))]
public class PlayerMovement : MonoBehaviour
{
    private Rigidbody rb;

    private void Awake()
    {
        rb = GetComponent<Rigidbody>();  // Guaranteed to exist
    }
}
```

### Component Communication

**Direct Reference (Inspector):**
```csharp
[SerializeField] private HealthDisplay healthDisplay;

private void TakeDamage(int amount)
{
    health -= amount;
    healthDisplay.UpdateHealth(health);  // Direct call
}
```

**GetComponent (Runtime):**
```csharp
private void OnTriggerEnter(Collider other)
{
    var health = other.GetComponent<Health>();
    if (health != null)
        health.TakeDamage(10);
}
```

**Events (Decoupled):**
```csharp
public event Action<int> OnHealthChanged;

private void TakeDamage(int amount)
{
    health -= amount;
    OnHealthChanged?.Invoke(health);  // Any subscribers get notified
}
```

## Prefab Workflows

Prefabs are reusable GameObject templates. Understanding prefab workflows prevents common issues.

### Creating Prefabs

Drag GameObject from Hierarchy to Project window. Blue text in Hierarchy indicates prefab instance.

### Prefab Instances

Changes to prefab instances:
- **Override** - Changes to this instance only (bold blue)
- **Apply** - Push changes to prefab asset (affects all instances)
- **Revert** - Discard instance changes, match prefab

### Prefab Variants

Create variations of a base prefab:

```
Base Prefab: Enemy
├── Variant: FastEnemy (increased speed)
├── Variant: TankEnemy (increased health)
└── Variant: FlyingEnemy (added flight)
```

Changes to base prefab propagate to variants.

### Nested Prefabs

Prefabs can contain other prefabs:

```
Car Prefab
├── Wheel Prefab (x4)
├── Engine Prefab
└── Door Prefab (x4)
```

Edit nested prefabs independently.

### Programmatic Prefab Usage

```csharp
[SerializeField] private GameObject enemyPrefab;
[SerializeField] private Transform spawnPoint;

private void SpawnEnemy()
{
    // Instantiate prefab
    GameObject enemy = Instantiate(enemyPrefab, spawnPoint.position, Quaternion.identity);

    // Configure instance
    enemy.GetComponent<Enemy>().SetTarget(player);

    // Parent to container (optional)
    enemy.transform.SetParent(enemyContainer);
}
```

### Prefab Best Practices

1. **Use prefabs for anything spawned at runtime** (enemies, projectiles, UI panels)
2. **Create prefab variants** instead of duplicating prefabs
3. **Apply changes carefully** - affects all instances
4. **Keep prefabs in organized folders** - Prefabs/Characters, Prefabs/UI, etc.
5. **Test prefab changes** before applying to all instances

## Common Patterns

### Singleton Manager

```csharp
public class GameManager : MonoBehaviour
{
    public static GameManager Instance { get; private set; }

    private void Awake()
    {
        if (Instance != null && Instance != this)
        {
            Destroy(gameObject);
            return;
        }

        Instance = this;
        DontDestroyOnLoad(gameObject);
    }
}
```

### Object Initialization

```csharp
public class Enemy : MonoBehaviour
{
    [SerializeField] private int health = 100;

    private Rigidbody rb;
    private Transform target;

    // 1. Cache components on self
    private void Awake()
    {
        rb = GetComponent<Rigidbody>();
    }

    // 2. Find external references
    private void Start()
    {
        target = GameObject.FindWithTag("Player").transform;
    }

    // 3. Subscribe to events
    private void OnEnable()
    {
        GameEvents.OnWaveComplete += HandleWaveComplete;
    }

    // 4. Unsubscribe from events
    private void OnDisable()
    {
        GameEvents.OnWaveComplete -= HandleWaveComplete;
    }
}
```

## Additional Resources

### Reference Files

For detailed guidance on specific topics:

- **`references/lifecycle-detailed.md`** - Complete lifecycle method reference
- **`references/serialization-guide.md`** - Advanced serialization patterns
- **`references/component-patterns.md`** - Component architecture best practices
- **`references/prefab-workflows.md`** - Comprehensive prefab usage guide

### Quick Reference

**Lifecycle Order:** Awake → OnEnable → Start → FixedUpdate → Update → LateUpdate → OnDisable → OnDestroy

**Serialization:** `[SerializeField] private` over `public`

**Components:** Cache in Awake(), never call GetComponent in Update()

**Prefabs:** Use for reusable objects, test before applying changes

---

Follow these fundamentals to build solid Unity projects that are performant, maintainable, and bug-free.
