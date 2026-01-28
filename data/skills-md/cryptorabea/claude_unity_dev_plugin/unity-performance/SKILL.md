---
name: Unity Performance
description: This skill should be used when the user asks about "Unity performance", "optimization", "GC allocation", "object pooling", "caching", "Update loop optimization", "memory management", "profiling", "framerate", "garbage collection", or needs guidance on performance best practices for Unity games.
version: 0.1.0
---

# Unity Performance Optimization

Essential performance optimization techniques for Unity games, covering memory management, CPU optimization, rendering, and profiling strategies.

## Overview

Performance is critical for Unity games across all platforms. Poor performance manifests as low framerates, stuttering, long load times, and crashes. This skill covers proven optimization techniques that apply to all Unity projects.

**Core optimization areas:**
- CPU optimization (Update loops, caching, pooling)
- Memory management (GC reduction, allocation patterns)
- Rendering optimization (batching, culling, LOD)
- Profiling and measurement (identifying bottlenecks)

## Reference Caching

The most common Unity performance mistake is repeated expensive lookups. Cache all references to avoid redundant operations.

### GetComponent Caching

Never call GetComponent repeatedly - cache results in Awake:

```csharp
// ❌ BAD - GetComponent every frame
private void Update()
{
    GetComponent<Rigidbody>().velocity = Vector3.forward;  // SLOW!
}

// ✅ GOOD - Cache once
private Rigidbody rb;

private void Awake()
{
    rb = GetComponent<Rigidbody>();
}

private void Update()
{
    rb.velocity = Vector3.forward;  // FAST
}
```

**Performance impact**: GetComponent is 10-100x slower than cached reference.

### Transform Caching

Cache `transform` access, especially for frequently accessed GameObjects:

```csharp
// ❌ BAD - Property access overhead
private void Update()
{
    transform.position += Vector3.forward * Time.deltaTime;
    transform.rotation = Quaternion.identity;
}

// ✅ GOOD - Cache transform reference
private Transform myTransform;

private void Awake()
{
    myTransform = transform;
}

private void Update()
{
    myTransform.position += Vector3.forward * Time.deltaTime;
    myTransform.rotation = Quaternion.identity;
}
```

**Why**: `transform` property has overhead. Cached reference eliminates repeated lookups.

### Find Method Caching

Never use Find methods in Update - cache results:

```csharp
// ❌ BAD - Find every frame (EXTREMELY SLOW)
private void Update()
{
    GameObject player = GameObject.Find("Player");
    Transform target = GameObject.FindWithTag("Enemy").transform;
}

// ✅ GOOD - Cache in Start
private GameObject player;
private Transform target;

private void Start()
{
    player = GameObject.Find("Player");
    target = GameObject.FindWithTag("Enemy")?.transform;
}

private void Update()
{
    // Use cached references
}
```

**Performance impact**: Find methods scan entire scene hierarchy. 100-1000x slower than cached references.

### Material Caching

Access `renderer.material` creates new Material instance - cache to avoid leaks:

```csharp
// ❌ BAD - Creates new Material every frame (MEMORY LEAK)
private void Update()
{
    GetComponent<Renderer>().material.color = Color.red;  // Creates new Material!
}

// ✅ GOOD - Cache material reference
private Material material;

private void Awake()
{
    material = GetComponent<Renderer>().material;
}

private void Update()
{
    material.color = Color.red;  // Modifies cached Material
}

private void OnDestroy()
{
    // Clean up instantiated material
    if (material != null)
        Destroy(material);
}
```

**Critical**: Accessing `.material` creates new instance. Use `.sharedMaterial` for read-only access to avoid instantiation.

## Object Pooling

Instantiate and Destroy are expensive. Reuse objects instead of creating/destroying repeatedly.

### Basic Pool Implementation

```csharp
public class ObjectPool : MonoBehaviour
{
    [SerializeField] private GameObject prefab;
    [SerializeField] private int initialSize = 10;

    private Queue<GameObject> pool = new Queue<GameObject>();

    private void Awake()
    {
        // Pre-instantiate objects
        for (int i = 0; i < initialSize; i++)
        {
            GameObject obj = Instantiate(prefab);
            obj.SetActive(false);
            pool.Enqueue(obj);
        }
    }

    public GameObject Get()
    {
        if (pool.Count > 0)
        {
            GameObject obj = pool.Dequeue();
            obj.SetActive(true);
            return obj;
        }

        // Pool exhausted - create new
        return Instantiate(prefab);
    }

    public void Return(GameObject obj)
    {
        obj.SetActive(false);
        pool.Enqueue(obj);
    }
}
```

**Use for:**
- Bullets, projectiles
- Particle effects
- UI elements (tooltips, damage numbers)
- Enemies in wave-based games
- Audio sources

**Performance gain**: 10-50x faster than Instantiate/Destroy, eliminates GC spikes.

### Pool Pattern Usage

```csharp
public class BulletSpawner : MonoBehaviour
{
    [SerializeField] private ObjectPool bulletPool;
    [SerializeField] private Transform firePoint;

    private void Fire()
    {
        // Get from pool
        GameObject bullet = bulletPool.Get();
        bullet.transform.position = firePoint.position;
        bullet.transform.rotation = firePoint.rotation;

        // Return after 3 seconds
        StartCoroutine(ReturnToPoolAfterDelay(bullet, 3f));
    }

    private IEnumerator ReturnToPoolAfterDelay(GameObject obj, float delay)
    {
        yield return new WaitForSeconds(delay);
        bulletPool.Return(obj);
    }
}
```

## Update Loop Optimization

Update, FixedUpdate, and LateUpdate are called frequently - minimize work done in these methods.

### Remove Empty Update Methods

```csharp
// ❌ BAD - Empty methods still have overhead
private void Update() { }
private void FixedUpdate() { }

// ✅ GOOD - Remove unused methods
// (No Update/FixedUpdate if not needed)
```

**Performance**: Unity calls all Update methods even if empty. Remove to reduce overhead.

### Reduce Update Frequency

Not all logic needs to run every frame:

```csharp
// ❌ BAD - Expensive check every frame
private void Update()
{
    CheckForNearbyEnemies();  // Expensive raycast/distance checks
}

// ✅ GOOD - Check every N frames
private int frameCounter = 0;
private const int checkInterval = 10;

private void Update()
{
    frameCounter++;
    if (frameCounter >= checkInterval)
    {
        frameCounter = 0;
        CheckForNearbyEnemies();
    }
}

// ✅ BETTER - Use InvokeRepeating or Coroutine
private void Start()
{
    InvokeRepeating(nameof(CheckForNearbyEnemies), 0f, 0.2f);  // Every 0.2 seconds
}
```

**Alternative: Coroutines**
```csharp
private void Start()
{
    StartCoroutine(CheckEnemiesRoutine());
}

private IEnumerator CheckEnemiesRoutine()
{
    while (true)
    {
        CheckForNearbyEnemies();
        yield return new WaitForSeconds(0.2f);
    }
}
```

### Event-Driven Architecture

Replace polling with events:

```csharp
// ❌ BAD - Poll for state change every frame
private bool wasGrounded;

private void Update()
{
    bool grounded = IsGrounded();
    if (grounded != wasGrounded)
    {
        OnGroundedChanged(grounded);
    }
    wasGrounded = grounded;
}

// ✅ GOOD - Event-driven
public event Action<bool> OnGroundedChanged;

private bool isGrounded;

private void SetGrounded(bool grounded)
{
    if (isGrounded != grounded)
    {
        isGrounded = grounded;
        OnGroundedChanged?.Invoke(grounded);
    }
}
```

## Garbage Collection Reduction

Avoid allocations in frequently-called methods to prevent GC spikes.

### String Concatenation

```csharp
// ❌ BAD - Allocates strings every frame
private void Update()
{
    string message = "Health: " + health;  // String allocation
    scoreText.text = "Score: " + score;    // String allocation
}

// ✅ GOOD - Use StringBuilder or string interpolation
private StringBuilder sb = new StringBuilder();

private void UpdateUI()
{
    sb.Clear();
    sb.Append("Health: ").Append(health);
    healthText.text = sb.ToString();
}

// ✅ ALTERNATIVE - Cache formatted strings
private void UpdateHealth(int newHealth)
{
    health = newHealth;
    healthText.text = health.ToString();  // Less allocation than concatenation
}
```

### Collection Allocation

```csharp
// ❌ BAD - Allocates new list every frame
private void Update()
{
    List<Enemy> nearbyEnemies = new List<Enemy>();  // GC allocation!
    FindNearbyEnemies(nearbyEnemies);
}

// ✅ GOOD - Reuse list
private List<Enemy> nearbyEnemies = new List<Enemy>();

private void Update()
{
    nearbyEnemies.Clear();  // Reuse existing list
    FindNearbyEnemies(nearbyEnemies);
}
```

### Array/List Best Practices

```csharp
// ❌ BAD - ToArray allocates
private void Update()
{
    GameObject[] enemies = enemyList.ToArray();  // GC allocation!
}

// ✅ GOOD - Iterate list directly
private void Update()
{
    for (int i = 0; i < enemyList.Count; i++)
    {
        Enemy enemy = enemyList[i];
        // Process enemy
    }
}

// ✅ GOOD - Use foreach (no allocation for List)
private void Update()
{
    foreach (var enemy in enemyList)
    {
        // Process enemy
    }
}
```

### Coroutine Allocation

```csharp
// ❌ BAD - Allocates WaitForSeconds every call
private IEnumerator DelayedAction()
{
    yield return new WaitForSeconds(1f);  // New allocation each time
}

// ✅ GOOD - Cache WaitForSeconds
private WaitForSeconds oneSecondWait = new WaitForSeconds(1f);

private IEnumerator DelayedAction()
{
    yield return oneSecondWait;  // Reuse cached wait
}
```

## Component Access Patterns

### Minimize Component Queries

```csharp
// ❌ BAD - Multiple GetComponent calls
private void OnTriggerEnter(Collider other)
{
    if (other.GetComponent<Enemy>() != null)
    {
        other.GetComponent<Enemy>().TakeDamage(10);  // Called twice!
    }
}

// ✅ GOOD - Single GetComponent with pattern matching
private void OnTriggerEnter(Collider other)
{
    if (other.TryGetComponent<Enemy>(out var enemy))
    {
        enemy.TakeDamage(10);  // Called once
    }
}
```

### Component Caching for Collisions

```csharp
// ❌ BAD - GetComponent on every collision
private void OnTriggerEnter(Collider other)
{
    var damageable = other.GetComponent<IDamageable>();
    if (damageable != null)
        damageable.TakeDamage(10);
}

// ✅ GOOD - Cache component on trigger enter
private Dictionary<Collider, IDamageable> damageableCache = new Dictionary<Collider, IDamageable>();

private void OnTriggerEnter(Collider other)
{
    if (!damageableCache.TryGetValue(other, out var damageable))
    {
        damageable = other.GetComponent<IDamageable>();
        damageableCache[other] = damageable;  // Cache for future collisions
    }

    damageable?.TakeDamage(10);
}

private void OnTriggerExit(Collider other)
{
    damageableCache.Remove(other);  // Clean up cache
}
```

## Physics Optimization

### Layer-Based Collision

Configure Physics Layer Collision Matrix to prevent unnecessary collision checks:

**Edit > Project Settings > Physics > Layer Collision Matrix**

```csharp
// Setup layers
Layer 8: Player
Layer 9: Enemies
Layer 10: Projectiles
Layer 11: Environment

// Disable unnecessary collisions:
- Player vs Player (disabled)
- Enemies vs Enemies (disabled)
- Projectiles vs Projectiles (disabled)
```

**Performance gain**: 30-50% reduction in physics overhead.

### Raycast Optimization

```csharp
// ❌ BAD - Raycast checks everything
bool hit = Physics.Raycast(origin, direction, out RaycastHit hitInfo);

// ✅ GOOD - Layer mask limits checks
int layerMask = 1 << LayerMask.NameToLayer("Enemy");
bool hit = Physics.Raycast(origin, direction, out RaycastHit hitInfo, maxDistance, layerMask);

// ✅ BETTER - Cache layer mask
private int enemyLayerMask;

private void Awake()
{
    enemyLayerMask = 1 << LayerMask.NameToLayer("Enemy");
}

private void Fire()
{
    bool hit = Physics.Raycast(origin, direction, out RaycastHit hitInfo, maxDistance, enemyLayerMask);
}
```

### Rigidbody Sleep

Let Rigidbody sleep when not moving:

```csharp
// Rigidbody automatically sleeps when velocity < threshold
// Configure in Edit > Project Settings > Physics

// Wake up manually when needed
private void ApplyForce()
{
    if (rb.IsSleeping())
        rb.WakeUp();

    rb.AddForce(force);
}
```

## Profiling

Measure before optimizing. Use Unity Profiler to identify actual bottlenecks.

**Open Profiler: Window > Analysis > Profiler**

### Key Profiler Metrics

**CPU Usage:**
- Rendering (DrawCalls, SetPass calls)
- Scripts (Update, FixedUpdate, Coroutines)
- Physics (FixedUpdate.PhysicsFixedUpdate)
- GC.Alloc (garbage collection allocations)

**Memory:**
- Total Allocated
- GC Allocated
- Texture memory
- Mesh memory

### Profiling Workflow

1. **Identify bottleneck**: Run Profiler, find expensive frame
2. **Drill down**: Click spike, view call hierarchy
3. **Measure baseline**: Record current performance
4. **Apply optimization**: Make targeted changes
5. **Measure improvement**: Compare before/after
6. **Repeat**: Find next bottleneck

### Deep Profile

Enable **Deep Profile** for detailed call stack (impacts performance):

**Warning**: Deep Profile slows game significantly. Use for small scenes or targeted profiling.

### Custom Profiler Markers

Measure specific code sections:

```csharp
using Unity.Profiling;

public class AIController : MonoBehaviour
{
    private static readonly ProfilerMarker s_PathfindingMarker = new ProfilerMarker("AI.Pathfinding");
    private static readonly ProfilerMarker s_DecisionMarker = new ProfilerMarker("AI.DecisionMaking");

    private void Update()
    {
        s_PathfindingMarker.Begin();
        CalculatePath();
        s_PathfindingMarker.End();

        s_DecisionMarker.Begin();
        MakeDecision();
        s_DecisionMarker.End();
    }

    private void CalculatePath() { }
    private void MakeDecision() { }
}
```

Shows custom markers in Profiler for precise measurement.

## Performance Budgets

Set performance targets for each system:

**Target: 60 FPS (16.67ms per frame)**
- Rendering: 6ms
- Scripts: 4ms
- Physics: 2ms
- UI: 1ms
- Audio: 0.5ms
- Other: 3ms

Monitor with Profiler and optimize systems exceeding budget.

## Platform-Specific Optimization

### Mobile Optimization

**Key concerns:**
- Lower CPU/GPU power
- Memory constraints
- Battery life
- Touch input overhead

**Mobile-specific optimizations:**
- Reduce draw calls (<100 for mobile)
- Lower texture resolution
- Disable shadows or use simple shadows
- Reduce particle count
- Use occlusion culling
- Optimize UI (Canvas batching)

### PC/Console Optimization

**More headroom but still optimize:**
- Target 60 FPS minimum
- Allow higher quality settings
- Monitor VRAM usage
- Profile on minimum spec hardware

## Additional Resources

### Reference Files

For detailed performance techniques, consult:
- **`references/memory-optimization.md`** - Advanced GC reduction, allocation patterns
- **`references/rendering-optimization.md`** - Draw call batching, GPU optimization, shaders
- **`references/physics-optimization.md`** - Collision optimization, Rigidbody best practices
- **`references/profiling-guide.md`** - Complete profiling workflows, tools, analysis

## Quick Reference

**Caching priorities:**
1. Transform references
2. GetComponent results
3. Find results
4. Material instances
5. WaitForSeconds in coroutines

**Avoid in Update:**
- GetComponent
- Find methods
- String concatenation
- New allocations
- Physics raycasts (use sparingly)

**Always profile before optimizing:**
- Measure baseline
- Identify bottleneck
- Apply targeted fix
- Measure improvement

---

Apply these performance practices consistently for smooth, responsive Unity games across all platforms.
