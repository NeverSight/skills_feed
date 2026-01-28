---
name: Unity Architecture
description: This skill should be used when the user asks about "game architecture", "design patterns", "manager pattern", "singleton pattern", "ScriptableObject", "ScriptableObject architecture", "event system", "Observer pattern", "pub-sub", "MVC in Unity", "dependency injection", "service locator", or needs guidance on structuring Unity projects and game systems.
version: 0.1.0
---

# Unity Game Architecture

Essential architectural patterns and design principles for scalable, maintainable Unity projects.

## Overview

Good architecture separates concerns, reduces coupling, and makes code testable and maintainable. This skill covers proven patterns for Unity game development.

**Core architectural concepts:**
- Manager patterns and global systems
- ScriptableObject-based data architecture
- Event-driven communication
- Component composition patterns
- Dependency management

## Manager Pattern

Centralized systems that coordinate game-wide functionality.

### Singleton Manager

Most common pattern for global managers:

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

    public void StartGame() { }
    public void PauseGame() { }
    public void EndGame() { }
}

// Access from anywhere
public class Player : MonoBehaviour
{
    private void Start()
    {
        GameManager.Instance.StartGame();
    }
}
```

**When to use:**
- Game state management (GameManager)
- Audio management (AudioManager)
- Input management (InputManager)
- Save/load systems (SaveManager)
- UI management (UIManager)

**When NOT to use:**
- Everything (avoid "singleton hell")
- Temporary systems
- Systems that need multiple instances

### Generic Singleton Base

Reusable singleton pattern:

```csharp
public class Singleton<T> : MonoBehaviour where T : MonoBehaviour
{
    private static T instance;

    public static T Instance
    {
        get
        {
            if (instance == null)
            {
                instance = FindObjectOfType<T>();

                if (instance == null)
                {
                    GameObject singleton = new GameObject(typeof(T).Name);
                    instance = singleton.AddComponent<T>();
                    DontDestroyOnLoad(singleton);
                }
            }

            return instance;
        }
    }

    protected virtual void Awake()
    {
        if (instance == null)
        {
            instance = this as T;
            DontDestroyOnLoad(gameObject);
        }
        else if (instance != this)
        {
            Destroy(gameObject);
        }
    }
}

// Usage
public class GameManager : Singleton<GameManager>
{
    protected override void Awake()
    {
        base.Awake();
        // Additional initialization
    }
}
```

### Manager Initialization Order

Control manager initialization:

```csharp
// Use Script Execution Order:
// Edit > Project Settings > Script Execution Order

// Or explicit initialization
public class GameBootstrap : MonoBehaviour
{
    private void Awake()
    {
        InitializeManagers();
    }

    private void InitializeManagers()
    {
        // Initialize in specific order
        var saveManager = SaveManager.Instance;
        var audioManager = AudioManager.Instance;
        var gameManager = GameManager.Instance;

        // Managers initialize in Awake, but access here ensures order
    }
}
```

**Best practice**: Use explicit initialization scene or bootstrapper.

### Service Locator Pattern

Alternative to singleton for dependency injection:

```csharp
public class ServiceLocator
{
    private static ServiceLocator instance;
    public static ServiceLocator Instance => instance ?? (instance = new ServiceLocator());

    private readonly Dictionary<Type, object> services = new Dictionary<Type, object>();

    public void RegisterService<T>(T service)
    {
        services[typeof(T)] = service;
    }

    public T GetService<T>()
    {
        if (services.TryGetValue(typeof(T), out var service))
        {
            return (T)service;
        }

        throw new Exception($"Service {typeof(T)} not found");
    }
}

// Register services
public class GameBootstrap : MonoBehaviour
{
    private void Awake()
    {
        var audioManager = new AudioManager();
        ServiceLocator.Instance.RegisterService(audioManager);

        var saveManager = new SaveManager();
        ServiceLocator.Instance.RegisterService(saveManager);
    }
}

// Access services
public class Player : MonoBehaviour
{
    private void Start()
    {
        var audio = ServiceLocator.Instance.GetService<AudioManager>();
        audio.PlaySound("Jump");
    }
}
```

**Benefits over singleton:**
- Testable (inject mock services)
- No static dependencies
- Clear dependencies

**Drawbacks:**
- More setup code
- Runtime dictionary lookup
- Less discoverable

## ScriptableObject Architecture

Data-driven design using ScriptableObjects.

### ScriptableObject Data Containers

Store data separate from behavior:

```csharp
[CreateAssetMenu(fileName = "WeaponData", menuName = "Game/Weapon Data")]
public class WeaponData : ScriptableObject
{
    public string weaponName;
    public int damage;
    public float fireRate;
    public Sprite icon;
    public GameObject projectilePrefab;
}

public class Weapon : MonoBehaviour
{
    [SerializeField] private WeaponData data;

    public void Fire()
    {
        Instantiate(data.projectilePrefab, firePoint.position, firePoint.rotation);
    }

    public int GetDamage() => data.damage;
}
```

**Benefits:**
- Separate data from code
- Share data across scenes
- Edit without code changes
- Designer-friendly

**Use for:**
- Item/weapon stats
- Character data
- Game balance values
- Configuration

### ScriptableObject Events

Event system using ScriptableObjects:

```csharp
[CreateAssetMenu(fileName = "GameEvent", menuName = "Events/Game Event")]
public class GameEvent : ScriptableObject
{
    private readonly List<GameEventListener> listeners = new List<GameEventListener>();

    public void Raise()
    {
        for (int i = listeners.Count - 1; i >= 0; i--)
        {
            listeners[i].OnEventRaised();
        }
    }

    public void RegisterListener(GameEventListener listener)
    {
        if (!listeners.Contains(listener))
            listeners.Add(listener);
    }

    public void UnregisterListener(GameEventListener listener)
    {
        listeners.Remove(listener);
    }
}

public class GameEventListener : MonoBehaviour
{
    [SerializeField] private GameEvent gameEvent;
    [SerializeField] private UnityEvent response;

    private void OnEnable()
    {
        gameEvent.RegisterListener(this);
    }

    private void OnDisable()
    {
        gameEvent.UnregisterListener(this);
    }

    public void OnEventRaised()
    {
        response.Invoke();
    }
}
```

**Usage:**
```
Create GameEvent asset: "OnPlayerDeath"
Attach GameEventListener to UI
Configure response: Show death screen
Raise event when player dies
```

**Benefits:**
- Designer-accessible
- Visual wiring in Inspector
- Decoupled systems
- Reusable events

### ScriptableObject Variables

Shared variables across scenes:

```csharp
public abstract class ScriptableVariable<T> : ScriptableObject
{
    [SerializeField] private T value;

    public T Value
    {
        get => value;
        set
        {
            this.value = value;
            OnValueChanged?.Invoke(value);
        }
    }

    public event Action<T> OnValueChanged;
}

[CreateAssetMenu(fileName = "IntVariable", menuName = "Variables/Int")]
public class IntVariable : ScriptableVariable<int> { }

[CreateAssetMenu(fileName = "FloatVariable", menuName = "Variables/Float")]
public class FloatVariable : ScriptableVariable<float> { }
```

**Usage:**
```csharp
public class Player : MonoBehaviour
{
    [SerializeField] private IntVariable playerHealth;

    public void TakeDamage(int damage)
    {
        playerHealth.Value -= damage;  // Updates all subscribers
    }
}

public class HealthUI : MonoBehaviour
{
    [SerializeField] private IntVariable playerHealth;
    [SerializeField] private Text healthText;

    private void OnEnable()
    {
        playerHealth.OnValueChanged += UpdateUI;
        UpdateUI(playerHealth.Value);
    }

    private void OnDisable()
    {
        playerHealth.OnValueChanged -= UpdateUI;
    }

    private void UpdateUI(int health)
    {
        healthText.text = $"Health: {health}";
    }
}
```

**Benefits:**
- Persistent across scenes
- Multiple listeners
- Inspector-editable
- Runtime changes reflected everywhere

## Event Systems

Decoupled communication between components.

### C# Events

Standard C# event pattern:

```csharp
public class Health : MonoBehaviour
{
    public event Action<int> OnHealthChanged;
    public event Action OnDeath;

    private int health = 100;

    public void TakeDamage(int damage)
    {
        health -= damage;
        OnHealthChanged?.Invoke(health);

        if (health <= 0)
        {
            OnDeath?.Invoke();
        }
    }
}

public class HealthUI : MonoBehaviour
{
    [SerializeField] private Health playerHealth;

    private void OnEnable()
    {
        playerHealth.OnHealthChanged += UpdateHealthBar;
        playerHealth.OnDeath += ShowDeathScreen;
    }

    private void OnDisable()
    {
        playerHealth.OnHealthChanged -= UpdateHealthBar;
        playerHealth.OnDeath -= ShowDeathScreen;
    }

    private void UpdateHealthBar(int health) { }
    private void ShowDeathScreen() { }
}
```

**Critical**: Always unsubscribe in OnDisable to prevent memory leaks.

### UnityEvent

Inspector-assignable events:

```csharp
public class Interactable : MonoBehaviour
{
    [SerializeField] private UnityEvent onInteract;
    [SerializeField] private UnityEvent<int> onScoreChanged;

    public void Interact()
    {
        onInteract?.Invoke();
    }

    public void AddScore(int points)
    {
        onScoreChanged?.Invoke(points);
    }
}
```

**Benefits:**
- Designer-accessible in Inspector
- No code for simple interactions
- Visual wiring

**Drawbacks:**
- Slower than C# events
- No compile-time checking
- Harder to debug

**Use for:**
- Simple interactions
- Designer-driven events
- Prototyping

### Global Event Bus

Centralized event system:

```csharp
public static class EventBus
{
    private static readonly Dictionary<Type, Delegate> eventTable = new Dictionary<Type, Delegate>();

    public static void Subscribe<T>(Action<T> handler)
    {
        if (eventTable.TryGetValue(typeof(T), out var existingHandler))
        {
            eventTable[typeof(T)] = Delegate.Combine(existingHandler, handler);
        }
        else
        {
            eventTable[typeof(T)] = handler;
        }
    }

    public static void Unsubscribe<T>(Action<T> handler)
    {
        if (eventTable.TryGetValue(typeof(T), out var existingHandler))
        {
            var newHandler = Delegate.Remove(existingHandler, handler);
            if (newHandler == null)
                eventTable.Remove(typeof(T));
            else
                eventTable[typeof(T)] = newHandler;
        }
    }

    public static void Publish<T>(T eventData)
    {
        if (eventTable.TryGetValue(typeof(T), out var handler))
        {
            (handler as Action<T>)?.Invoke(eventData);
        }
    }
}

// Event data types
public struct PlayerDiedEvent
{
    public Vector3 position;
    public string killedBy;
}

// Subscribe
public class DeathUI : MonoBehaviour
{
    private void OnEnable()
    {
        EventBus.Subscribe<PlayerDiedEvent>(OnPlayerDied);
    }

    private void OnDisable()
    {
        EventBus.Unsubscribe<PlayerDiedEvent>(OnPlayerDied);
    }

    private void OnPlayerDied(PlayerDiedEvent data)
    {
        ShowDeathScreen(data.position, data.killedBy);
    }
}

// Publish
public class Player : MonoBehaviour
{
    private void Die()
    {
        EventBus.Publish(new PlayerDiedEvent
        {
            position = transform.position,
            killedBy = "Enemy"
        });
    }
}
```

**Benefits:**
- Fully decoupled
- No direct references needed
- Type-safe with structs

**Drawbacks:**
- Runtime overhead (dictionary lookup)
- Harder to trace event flow
- Memory leak risk if forgot unsubscribe

## Component Composition Patterns

### Strategy Pattern

Interchangeable behaviors:

```csharp
public interface IMovementStrategy
{
    void Move(Transform transform, float speed);
}

public class GroundMovement : MonoBehaviour, IMovementStrategy
{
    public void Move(Transform transform, float speed)
    {
        // Ground-based movement
    }
}

public class FlyingMovement : MonoBehaviour, IMovementStrategy
{
    public void Move(Transform transform, float speed)
    {
        // Flying movement
    }
}

public class Character : MonoBehaviour
{
    [SerializeField] private float speed = 5f;
    private IMovementStrategy movementStrategy;

    private void Awake()
    {
        movementStrategy = GetComponent<IMovementStrategy>();
    }

    private void Update()
    {
        movementStrategy.Move(transform, speed);
    }
}
```

**Benefits:**
- Swap behaviors at runtime
- Reusable strategies
- Open/closed principle

### State Machine Pattern

Manage object states:

```csharp
public interface IState
{
    void Enter();
    void Execute();
    void Exit();
}

public class IdleState : MonoBehaviour, IState
{
    public void Enter() => Debug.Log("Entering Idle");
    public void Execute() { }
    public void Exit() => Debug.Log("Exiting Idle");
}

public class StateMachine : MonoBehaviour
{
    private IState currentState;

    public void ChangeState(IState newState)
    {
        currentState?.Exit();
        currentState = newState;
        currentState?.Enter();
    }

    private void Update()
    {
        currentState?.Execute();
    }
}

public class Enemy : MonoBehaviour
{
    private StateMachine stateMachine;
    private IdleState idleState;
    private ChaseState chaseState;

    private void Awake()
    {
        stateMachine = GetComponent<StateMachine>();
        idleState = GetComponent<IdleState>();
        chaseState = GetComponent<ChaseState>();

        stateMachine.ChangeState(idleState);
    }

    public void OnPlayerSpotted()
    {
        stateMachine.ChangeState(chaseState);
    }
}
```

### Observer Pattern

One-to-many notifications:

```csharp
public interface IObserver
{
    void OnNotify(string eventType);
}

public class Subject : MonoBehaviour
{
    private readonly List<IObserver> observers = new List<IObserver>();

    public void Attach(IObserver observer)
    {
        if (!observers.Contains(observer))
            observers.Add(observer);
    }

    public void Detach(IObserver observer)
    {
        observers.Remove(observer);
    }

    protected void Notify(string eventType)
    {
        for (int i = observers.Count - 1; i >= 0; i--)
        {
            observers[i].OnNotify(eventType);
        }
    }
}

public class Player : Subject
{
    public void Jump()
    {
        Notify("PlayerJumped");
    }
}

public class AudioObserver : MonoBehaviour, IObserver
{
    [SerializeField] private Player player;

    private void OnEnable()
    {
        player.Attach(this);
    }

    private void OnDisable()
    {
        player.Detach(this);
    }

    public void OnNotify(string eventType)
    {
        if (eventType == "PlayerJumped")
            PlayJumpSound();
    }
}
```

## MVC/MVP in Unity

### Model-View-Controller

Separate data, presentation, and logic:

```csharp
// Model - Data
public class PlayerModel
{
    public int Health { get; private set; } = 100;
    public int Score { get; private set; } = 0;

    public event Action<int> OnHealthChanged;
    public event Action<int> OnScoreChanged;

    public void TakeDamage(int damage)
    {
        Health -= damage;
        OnHealthChanged?.Invoke(Health);
    }

    public void AddScore(int points)
    {
        Score += points;
        OnScoreChanged?.Invoke(Score);
    }
}

// View - Presentation
public class PlayerView : MonoBehaviour
{
    [SerializeField] private Text healthText;
    [SerializeField] private Text scoreText;

    public void UpdateHealth(int health)
    {
        healthText.text = $"Health: {health}";
    }

    public void UpdateScore(int score)
    {
        scoreText.text = $"Score: {score}";
    }
}

// Controller - Logic
public class PlayerController : MonoBehaviour
{
    private PlayerModel model;
    private PlayerView view;

    private void Awake()
    {
        model = new PlayerModel();
        view = GetComponent<PlayerView>();

        model.OnHealthChanged += view.UpdateHealth;
        model.OnScoreChanged += view.UpdateScore;
    }

    private void OnDestroy()
    {
        model.OnHealthChanged -= view.UpdateHealth;
        model.OnScoreChanged -= view.UpdateScore;
    }

    public void TakeDamage(int damage)
    {
        model.TakeDamage(damage);
    }

    public void AddScore(int points)
    {
        model.AddScore(points);
    }
}
```

**Benefits:**
- Testable (mock model/view)
- Reusable components
- Clear separation

**When to use:**
- Complex UI
- Testable code required
- Multiple views of same data

## Additional Resources

### Reference Files

For detailed architectural patterns, consult:
- **`references/manager-patterns.md`** - Manager implementations, initialization, communication
- **`references/scriptableobject-architecture.md`** - Advanced SO patterns, runtime sets, variables
- **`references/event-systems.md`** - Event patterns, message buses, pub-sub systems
- **`references/design-patterns.md`** - Factory, Pool, Command, Strategy patterns for Unity

## Best Practices

✅ **DO:**
- Use managers for global systems (audio, input, save)
- Leverage ScriptableObjects for data
- Implement event-driven communication
- Favor composition over inheritance
- Always unsubscribe from events in OnDisable
- Use dependency injection for testability
- Keep managers focused (single responsibility)

❌ **DON'T:**
- Make everything a singleton
- Create god managers (handle one concern)
- Forget to unsubscribe from events
- Hardcode dependencies
- Use singletons for everything
- Mix data and presentation
- Create deep inheritance hierarchies

**Golden rule**: Design for change. Loosely coupled, highly cohesive systems are easier to maintain, test, and extend.

---

Apply these architectural patterns for scalable, maintainable Unity projects that stand the test of time.
