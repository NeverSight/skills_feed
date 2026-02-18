---
name: game-programming-languages
version: "2.0.0"
description: |
  Game programming languages - C#, C++, GDScript. Learn syntax, patterns,
  and engine-specific idioms for professional game development.
sasmp_version: "1.3.0"
bonded_agent: 02-game-programmer
bond_type: PRIMARY_BOND

parameters:
  - name: language
    type: string
    required: false
    validation:
      enum: [csharp, cpp, gdscript, rust, lua]
  - name: engine
    type: string
    required: false
    validation:
      enum: [unity, unreal, godot, custom]

retry_policy:
  enabled: true
  max_attempts: 3
  backoff: exponential

observability:
  log_events: [start, complete, error]
  metrics: [code_quality_score, compilation_time]
---

# Game Programming Languages

## C# (Unity)

**Easiest to learn**, **most used for game dev**

```csharp
// ✅ Production-Ready: Unity MonoBehaviour Template
public class GameEntity : MonoBehaviour
{
    [SerializeField] private float _speed = 5f;
    [SerializeField] private int _health = 100;

    public event Action<int> OnHealthChanged;
    public event Action OnDeath;

    private Rigidbody _rb;
    private bool _isInitialized;

    private void Awake()
    {
        _rb = GetComponent<Rigidbody>();
        _isInitialized = true;
    }

    public void TakeDamage(int amount)
    {
        if (!_isInitialized) return;

        _health = Mathf.Max(0, _health - amount);
        OnHealthChanged?.Invoke(_health);

        if (_health <= 0)
            OnDeath?.Invoke();
    }
}
```

**Key Features:**
- Object-oriented, managed memory
- LINQ for data queries
- Coroutines for async game logic
- Events and delegates
- Garbage collection (requires optimization)

**Learning Path**: 2-3 weeks basics, 2-3 months mastery

## C++ (Unreal Engine)

**Most powerful**, **steepest learning curve**

```cpp
// ✅ Production-Ready: Unreal Actor Template
UCLASS()
class MYGAME_API AGameEntity : public AActor
{
    GENERATED_BODY()

public:
    AGameEntity();

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stats")
    float Speed = 500.0f;

    UPROPERTY(ReplicatedUsing = OnRep_Health)
    int32 Health = 100;

    UFUNCTION(BlueprintCallable, Category = "Combat")
    void TakeDamage(int32 Amount);

    DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnHealthChanged, int32, NewHealth);
    UPROPERTY(BlueprintAssignable)
    FOnHealthChanged OnHealthChanged;

protected:
    virtual void BeginPlay() override;

    UFUNCTION()
    void OnRep_Health();
};
```

**Key Features:**
- Manual memory management (smart pointers)
- Templates and STL
- Maximum performance
- Unreal reflection system (UPROPERTY, UFUNCTION)
- Blueprint integration

**Learning Path**: 4-6 weeks basics, 4-6 months proficiency

## GDScript (Godot)

**Python-like**, **easiest syntax**

```gdscript
# ✅ Production-Ready: Godot Node Template
extends CharacterBody2D
class_name GameEntity

signal health_changed(new_health: int)
signal died

@export var speed: float = 200.0
@export var max_health: int = 100

var _health: int = max_health

func _ready() -> void:
    _health = max_health

func take_damage(amount: int) -> void:
    _health = max(0, _health - amount)
    health_changed.emit(_health)

    if _health <= 0:
        died.emit()
        queue_free()

func _physics_process(delta: float) -> void:
    var direction = Input.get_vector("left", "right", "up", "down")
    velocity = direction * speed
    move_and_slide()
```

**Key Features:**
- Dynamic typing with optional type hints
- Simple, Python-like syntax
- Signals for messaging
- First-class functions
- Growing ecosystem

**Learning Path**: 1-2 weeks basics, 4-8 weeks proficiency

## Language Comparison

| Feature | C# (Unity) | C++ (Unreal) | GDScript |
|---------|------------|--------------|----------|
| Memory | Managed (GC) | Manual | Managed |
| Speed | Fast | Fastest | Moderate |
| Learning | Moderate | Hard | Easy |
| Typing | Static | Static | Dynamic |
| Industry | Mobile/Indie | AAA | Indie |

## 🔧 Troubleshooting

```
┌─────────────────────────────────────────────────────────────┐
│ PROBLEM: Garbage collection spikes in C#                   │
├─────────────────────────────────────────────────────────────┤
│ SOLUTIONS:                                                   │
│ → Use object pooling                                        │
│ → Avoid allocations in Update()                             │
│ → Cache GetComponent results                                │
│ → Use structs for small data                                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ PROBLEM: Memory leaks in C++                                │
├─────────────────────────────────────────────────────────────┤
│ SOLUTIONS:                                                   │
│ → Use TSharedPtr/TWeakPtr                                   │
│ → UPROPERTY for UObject pointers                            │
│ → Run memory profiler regularly                             │
└─────────────────────────────────────────────────────────────┘
```

## Best Practices

| Practice | Benefit |
|----------|---------|
| Consistent naming | Readable code |
| Early returns | Reduced nesting |
| Composition over inheritance | Flexible design |
| Cache frequently used values | Performance |

---

**Use this skill**: When learning game programming languages or optimizing code.
