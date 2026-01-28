---
name: memory-management
version: "2.0.0"
description: |
  Game memory optimization, object pooling, garbage collection tuning,
  and efficient resource management for target platforms.
sasmp_version: "1.3.0"
bonded_agent: 02-game-programmer
bond_type: PRIMARY_BOND

parameters:
  - name: platform
    type: string
    required: false
    validation:
      enum: [pc, console, mobile, vr, web]
  - name: issue_type
    type: string
    required: false
    validation:
      enum: [leak, fragmentation, gc_spikes, budget_exceeded]

retry_policy:
  enabled: true
  max_attempts: 3
  backoff: exponential

observability:
  log_events: [start, complete, error, gc_collect]
  metrics: [heap_size_mb, gc_time_ms, allocation_rate, pool_usage]
---

# Memory Management

## Memory Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GAME MEMORY LAYOUT                        │
├─────────────────────────────────────────────────────────────┤
│  STACK (Fast, Auto-managed):                                 │
│  ├─ Local variables                                         │
│  ├─ Function parameters                                     │
│  └─ Return addresses                                        │
│                                                              │
│  HEAP (Slower, Manual/GC-managed):                           │
│  ├─ Dynamic allocations (new/malloc)                        │
│  ├─ Game objects                                            │
│  └─ Asset data                                              │
│                                                              │
│  STATIC (Fixed at compile time):                             │
│  ├─ Global variables                                        │
│  ├─ Static class members                                    │
│  └─ Constant data                                           │
│                                                              │
│  VRAM (GPU Memory):                                          │
│  ├─ Textures                                                │
│  ├─ Meshes                                                  │
│  └─ Render targets                                          │
└─────────────────────────────────────────────────────────────┘
```

## Platform Memory Budgets

```
MEMORY BUDGET GUIDELINES:
┌─────────────────────────────────────────────────────────────┐
│  PLATFORM      │ TOTAL    │ GAME LOGIC │ ASSETS   │ BUFFER │
├────────────────┼──────────┼────────────┼──────────┼────────┤
│  Mobile Low    │ 512 MB   │ 50 MB      │ 350 MB   │ 112 MB │
│  Mobile High   │ 2 GB     │ 200 MB     │ 1.5 GB   │ 300 MB │
│  Console       │ 8 GB     │ 500 MB     │ 6 GB     │ 1.5 GB │
│  PC Min        │ 4 GB     │ 300 MB     │ 3 GB     │ 700 MB │
│  PC High       │ 16 GB    │ 1 GB       │ 12 GB    │ 3 GB   │
│  VR            │ 8 GB     │ 400 MB     │ 6 GB     │ 1.6 GB │
└────────────────┴──────────┴────────────┴──────────┴────────┘

VRAM BUDGETS:
┌─────────────────────────────────────────────────────────────┐
│  Mobile:    512 MB - 1 GB                                   │
│  Console:   8-12 GB (shared with RAM)                       │
│  PC Low:    2-4 GB                                          │
│  PC High:   8-16 GB                                         │
└─────────────────────────────────────────────────────────────┘
```

## Object Pooling

```csharp
// ✅ Production-Ready: Generic Object Pool
public class ObjectPool<T> where T : class
{
    private readonly Stack<T> _pool;
    private readonly Func<T> _createFunc;
    private readonly Action<T> _onGet;
    private readonly Action<T> _onReturn;
    private readonly int _maxSize;

    public int CountActive { get; private set; }
    public int CountInPool => _pool.Count;

    public ObjectPool(
        Func<T> createFunc,
        Action<T> onGet = null,
        Action<T> onReturn = null,
        int initialSize = 10,
        int maxSize = 100)
    {
        _createFunc = createFunc;
        _onGet = onGet;
        _onReturn = onReturn;
        _maxSize = maxSize;
        _pool = new Stack<T>(initialSize);

        // Pre-warm pool
        for (int i = 0; i < initialSize; i++)
        {
            _pool.Push(_createFunc());
        }
    }

    public T Get()
    {
        T item = _pool.Count > 0 ? _pool.Pop() : _createFunc();
        _onGet?.Invoke(item);
        CountActive++;
        return item;
    }

    public void Return(T item)
    {
        if (item == null) return;

        _onReturn?.Invoke(item);
        CountActive--;

        if (_pool.Count < _maxSize)
        {
            _pool.Push(item);
        }
        // If pool is full, let GC collect the item
    }

    public void Clear()
    {
        _pool.Clear();
        CountActive = 0;
    }
}

// Usage Example: Bullet Pool
public class BulletManager : MonoBehaviour
{
    private ObjectPool<Bullet> _bulletPool;

    void Awake()
    {
        _bulletPool = new ObjectPool<Bullet>(
            createFunc: () => Instantiate(bulletPrefab).GetComponent<Bullet>(),
            onGet: bullet => bullet.gameObject.SetActive(true),
            onReturn: bullet => bullet.gameObject.SetActive(false),
            initialSize: 50,
            maxSize: 200
        );
    }

    public Bullet SpawnBullet(Vector3 position, Vector3 direction)
    {
        var bullet = _bulletPool.Get();
        bullet.Initialize(position, direction);
        bullet.OnDestroyed += () => _bulletPool.Return(bullet);
        return bullet;
    }
}
```

## Garbage Collection Optimization

```
GC SPIKE PREVENTION:
┌─────────────────────────────────────────────────────────────┐
│  AVOID IN UPDATE/HOT PATHS:                                  │
│  ✗ new object()                                             │
│  ✗ string concatenation ("a" + "b")                         │
│  ✗ LINQ queries (ToList(), Where(), etc.)                   │
│  ✗ Boxing value types                                       │
│  ✗ Closures/lambdas capturing variables                     │
│  ✗ foreach on non-struct enumerators                        │
│                                                              │
│  DO INSTEAD:                                                 │
│  ✓ Object pooling                                           │
│  ✓ StringBuilder for strings                                │
│  ✓ Pre-allocated collections                                │
│  ✓ Struct-based data                                        │
│  ✓ Cache delegates                                          │
│  ✓ for loops with index                                     │
└─────────────────────────────────────────────────────────────┘
```

```csharp
// ✅ Production-Ready: Allocation-Free Patterns
public class AllocationFreePatterns
{
    // ❌ BAD: Allocates every frame
    void BadUpdate()
    {
        string status = "Health: " + health + "/" + maxHealth; // Allocates
        var enemies = allEntities.Where(e => e.IsEnemy).ToList(); // Allocates
        foreach (var enemy in enemies) { } // May allocate enumerator
    }

    // ✓ GOOD: Zero allocations
    private StringBuilder _sb = new StringBuilder(64);
    private List<Entity> _enemyCache = new List<Entity>(100);

    void GoodUpdate()
    {
        // Reuse StringBuilder
        _sb.Clear();
        _sb.Append("Health: ").Append(health).Append("/").Append(maxHealth);

        // Reuse list, avoid LINQ
        _enemyCache.Clear();
        for (int i = 0; i < allEntities.Count; i++)
        {
            if (allEntities[i].IsEnemy)
                _enemyCache.Add(allEntities[i]);
        }

        // Index-based iteration
        for (int i = 0; i < _enemyCache.Count; i++)
        {
            ProcessEnemy(_enemyCache[i]);
        }
    }
}
```

## Memory Profiling

```
PROFILING WORKFLOW:
┌─────────────────────────────────────────────────────────────┐
│  1. BASELINE: Measure memory at known state                 │
│     → Startup, menu, gameplay, level transition            │
│                                                              │
│  2. MONITOR: Track over time                                │
│     → Memory growth indicates leaks                         │
│     → Spikes indicate heavy allocations                    │
│                                                              │
│  3. SNAPSHOT: Capture heap at suspicious moments            │
│     → Compare snapshots to find what's growing             │
│                                                              │
│  4. TRACE: Find allocation source                           │
│     → Stack trace shows where allocation happened          │
│     → Identify hot paths                                   │
│                                                              │
│  5. FIX: Apply optimization                                 │
│     → Pool, cache, or eliminate allocation                 │
│                                                              │
│  6. VERIFY: Confirm fix worked                              │
│     → Re-profile same scenario                             │
└─────────────────────────────────────────────────────────────┘

PROFILING TOOLS:
┌─────────────────────────────────────────────────────────────┐
│  Unity:                                                      │
│  • Memory Profiler (Package)                                │
│  • Profiler window (Memory section)                         │
│  • Deep Profile mode                                        │
│                                                              │
│  Unreal:                                                     │
│  • Unreal Insights                                          │
│  • memreport command                                        │
│  • stat memory                                              │
│                                                              │
│  Native:                                                     │
│  • Valgrind (Linux)                                         │
│  • Instruments (macOS)                                      │
│  • Visual Studio Diagnostic Tools                           │
└─────────────────────────────────────────────────────────────┘
```

## Asset Streaming

```
STREAMING STRATEGY:
┌─────────────────────────────────────────────────────────────┐
│                    STREAMING ZONES                           │
│                                                              │
│     [Loaded]  [Loading...]  [Unloaded]  [Unloaded]         │
│        ▲           ▲            │            │              │
│        │           │            │            │              │
│  ──────●───────────●────────────●────────────●──────        │
│     Player      Trigger     Far Zone     Very Far           │
│     Position                                                 │
│                                                              │
│  STREAMING RULES:                                            │
│  • Load when player approaches (predictive)                 │
│  • Unload when player far away + timeout                   │
│  • Priority: Visible > Nearby > Background                 │
│  • Async loading to avoid hitches                          │
└─────────────────────────────────────────────────────────────┘
```

```csharp
// ✅ Production-Ready: Asset Streaming Manager
public class StreamingManager : MonoBehaviour
{
    [SerializeField] private float loadDistance = 50f;
    [SerializeField] private float unloadDistance = 100f;
    [SerializeField] private float unloadDelay = 5f;

    private Dictionary<string, StreamingZone> _zones = new();
    private Queue<AsyncOperation> _loadQueue = new();

    void Update()
    {
        Vector3 playerPos = Player.Position;

        foreach (var zone in _zones.Values)
        {
            float distance = Vector3.Distance(playerPos, zone.Center);

            if (distance < loadDistance && !zone.IsLoaded)
            {
                StartCoroutine(LoadZoneAsync(zone));
            }
            else if (distance > unloadDistance && zone.IsLoaded)
            {
                StartCoroutine(UnloadZoneDelayed(zone, unloadDelay));
            }
        }
    }

    private IEnumerator LoadZoneAsync(StreamingZone zone)
    {
        zone.State = ZoneState.Loading;

        var operation = SceneManager.LoadSceneAsync(zone.SceneName, LoadSceneMode.Additive);
        operation.allowSceneActivation = false;

        while (operation.progress < 0.9f)
        {
            yield return null;
        }

        operation.allowSceneActivation = true;
        zone.State = ZoneState.Loaded;
    }
}
```

## 🔧 Troubleshooting

```
┌─────────────────────────────────────────────────────────────┐
│ PROBLEM: Memory keeps growing over time (leak)              │
├─────────────────────────────────────────────────────────────┤
│ DEBUG:                                                       │
│ → Take memory snapshots at intervals                        │
│ → Compare snapshots to find growing objects                 │
│ → Check for missing unsubscribes (events)                   │
│ → Look for collections that never clear                     │
├─────────────────────────────────────────────────────────────┤
│ SOLUTIONS:                                                   │
│ → Implement IDisposable pattern                             │
│ → Use weak references for caches                            │
│ → Clear collections when changing scenes                    │
│ → Unsubscribe from events in OnDestroy                      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ PROBLEM: GC causing frame spikes                            │
├─────────────────────────────────────────────────────────────┤
│ DEBUG:                                                       │
│ → Profile with GC.Alloc markers                             │
│ → Look for allocations in Update/FixedUpdate               │
│ → Check for string operations in hot paths                  │
├─────────────────────────────────────────────────────────────┤
│ SOLUTIONS:                                                   │
│ → Implement object pooling                                  │
│ → Use structs instead of classes where possible             │
│ → Pre-allocate collections with known capacity              │
│ → Spread GC across frames (incremental GC)                  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ PROBLEM: Out of memory on mobile                            │
├─────────────────────────────────────────────────────────────┤
│ DEBUG:                                                       │
│ → Check texture memory usage                                │
│ → Look for duplicate assets                                 │
│ → Monitor during level transitions                          │
├─────────────────────────────────────────────────────────────┤
│ SOLUTIONS:                                                   │
│ → Reduce texture resolution                                 │
│ → Implement aggressive streaming                            │
│ → Unload unused assets (Resources.UnloadUnusedAssets)       │
│ → Use compressed texture formats                            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ PROBLEM: Hitches during level loading                       │
├─────────────────────────────────────────────────────────────┤
│ SOLUTIONS:                                                   │
│ → Use async loading (LoadSceneAsync)                        │
│ → Spread instantiation across frames                        │
│ → Pre-warm object pools during loading screen               │
│ → Stream assets instead of loading all at once              │
└─────────────────────────────────────────────────────────────┘
```

## Memory Optimization Checklist

| Area | Technique | Impact | Effort |
|------|-----------|--------|--------|
| Objects | Object Pooling | High | Medium |
| Strings | StringBuilder | Medium | Low |
| Collections | Pre-allocation | Medium | Low |
| Assets | Streaming | High | High |
| Textures | Compression | High | Low |
| GC | Incremental GC | Medium | Low |
| Events | Weak References | Low | Medium |

---

**Use this skill**: When optimizing memory usage, reducing frame stutters, or supporting mobile platforms.
