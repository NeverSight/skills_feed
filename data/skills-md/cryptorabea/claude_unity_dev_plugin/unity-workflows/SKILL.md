---
name: Unity Workflows
description: This skill should be used when the user asks about "Unity editor scripting", "Custom Inspector", "EditorWindow", "PropertyDrawer", "Unity Input System", "new Input System", "UI Toolkit", "uGUI", "Canvas", "asset management", "AssetDatabase", "build pipeline", "Editor utilities", or needs guidance on Unity editor extensions, input handling, UI systems, and workflow optimization.
version: 0.1.0
---

# Unity Workflows and Editor Tools

Essential workflows for Unity editor scripting, input systems, UI development, and asset management.

## Overview

Efficient Unity workflows accelerate development and reduce errors. This skill covers editor customization, modern input handling, UI systems, and asset pipeline optimization.

**Core workflow areas:**
- Editor scripting and custom tools
- Input System (new and legacy)
- UI development (UI Toolkit, uGUI)
- Asset management and build pipeline

## Editor Scripting Basics

### Menu Items

Create custom menu commands:

```csharp
using UnityEditor;

public static class CustomMenu
{
    [MenuItem("Tools/My Tool")]
    private static void ExecuteTool()
    {
        Debug.Log("Custom tool executed");
    }

    [MenuItem("Tools/My Tool", true)]  // Validation
    private static bool ValidateTool()
    {
        return Selection.activeGameObject != null;
    }

    // Keyboard shortcut: Ctrl+Shift+T (Windows), Cmd+Shift+T (Mac)
    [MenuItem("Tools/Quick Action %#t")]
    private static void QuickAction()
    {
        // Action
    }
}
```

**Shortcut keys:**
- `%` = Ctrl (Cmd on Mac)
- `#` = Shift
- `&` = Alt
- `_g` = G key

### Context Menus

Right-click context menu for GameObjects/Components:

```csharp
[MenuItem("GameObject/My Custom Action", false, 10)]
private static void CustomAction()
{
    GameObject selected = Selection.activeGameObject;
    // Perform action
}

// Component context menu
public class MyComponent : MonoBehaviour
{
    [ContextMenu("Do Something")]
    private void DoSomething()
    {
        Debug.Log("Context menu action");
    }

    [ContextMenuItem("Reset Value", "ResetValue")]
    [SerializeField] private int value;

    private void ResetValue()
    {
        value = 0;
    }
}
```

### Custom Inspector

Override Inspector for custom types:

```csharp
[CustomEditor(typeof(MyScript))]
public class MyScriptEditor : Editor
{
    public override void OnInspectorGUI()
    {
        // Draw default inspector
        DrawDefaultInspector();

        MyScript script = (MyScript)target;

        // Custom button
        if (GUILayout.Button("Execute Action"))
        {
            script.ExecuteAction();
        }

        // Custom fields
        EditorGUILayout.LabelField("Custom Section", EditorStyles.boldLabel);
        script.customValue = EditorGUILayout.IntSlider("Custom Value", script.customValue, 0, 100);

        // Apply changes
        if (GUI.changed)
        {
            EditorUtility.SetDirty(target);
        }
    }
}
```

### Property Drawers

Custom property display in Inspector:

```csharp
[System.Serializable]
public class Range
{
    public float min;
    public float max;
}

[CustomPropertyDrawer(typeof(Range))]
public class RangeDrawer : PropertyDrawer
{
    public override void OnGUI(Rect position, SerializedProperty property, GUIContent label)
    {
        EditorGUI.BeginProperty(position, label, property);

        position = EditorGUI.PrefixLabel(position, GUIUtility.GetControlID(FocusType.Passive), label);

        var minProp = property.FindPropertyRelative("min");
        var maxProp = property.FindPropertyRelative("max");

        float halfWidth = position.width / 2;

        Rect minRect = new Rect(position.x, position.y, halfWidth - 5, position.height);
        Rect maxRect = new Rect(position.x + halfWidth, position.y, halfWidth - 5, position.height);

        EditorGUI.PropertyField(minRect, minProp, GUIContent.none);
        EditorGUI.PropertyField(maxRect, maxProp, GUIContent.none);

        EditorGUI.EndProperty();
    }
}
```

### EditorWindow

Create custom editor windows:

```csharp
public class MyEditorWindow : EditorWindow
{
    private string textField = "";
    private int intField = 0;

    [MenuItem("Window/My Editor Window")]
    private static void ShowWindow()
    {
        var window = GetWindow<MyEditorWindow>();
        window.titleContent = new GUIContent("My Tool");
        window.minSize = new Vector2(300, 200);
        window.Show();
    }

    private void OnGUI()
    {
        GUILayout.Label("My Custom Tool", EditorStyles.boldLabel);

        textField = EditorGUILayout.TextField("Text Field", textField);
        intField = EditorGUILayout.IntField("Int Field", intField);

        if (GUILayout.Button("Execute"))
        {
            Execute();
        }
    }

    private void Execute()
    {
        Debug.Log($"Executed with: {textField}, {intField}");
    }
}
```

### AssetDatabase Operations

Manipulate assets programmatically:

```csharp
using UnityEditor;

public static class AssetUtilities
{
    [MenuItem("Assets/Create Prefab From Selection")]
    private static void CreatePrefab()
    {
        GameObject selected = Selection.activeGameObject;
        if (selected == null)
            return;

        string path = $"Assets/Prefabs/{selected.name}.prefab";

        // Create prefab
        PrefabUtility.SaveAsPrefabAsset(selected, path);

        AssetDatabase.Refresh();
    }

    public static T LoadAsset<T>(string path) where T : UnityEngine.Object
    {
        return AssetDatabase.LoadAssetAtPath<T>(path);
    }

    public static void CreateFolder(string path)
    {
        if (!AssetDatabase.IsValidFolder(path))
        {
            AssetDatabase.CreateFolder(System.IO.Path.GetDirectoryName(path), System.IO.Path.GetFileName(path));
        }
    }
}
```

## Unity Input System

### New Input System Setup

**Install: Window > Package Manager > Input System**

**Create Input Actions:**
1. Create > Input Actions
2. Add Action Maps (Player, UI, etc.)
3. Add Actions (Move, Jump, Fire, etc.)
4. Bind inputs (Keyboard, Gamepad, etc.)
5. Generate C# class (Inspector > Generate C# Class)

### Using Input Actions

```csharp
using UnityEngine.InputSystem;

public class PlayerController : MonoBehaviour
{
    private PlayerInput playerInput;
    private InputAction moveAction;
    private InputAction jumpAction;

    private void Awake()
    {
        playerInput = GetComponent<PlayerInput>();

        moveAction = playerInput.actions["Move"];
        jumpAction = playerInput.actions["Jump"];
    }

    private void OnEnable()
    {
        jumpAction.performed += OnJump;
    }

    private void OnDisable()
    {
        jumpAction.performed -= OnJump;
    }

    private void Update()
    {
        Vector2 moveInput = moveAction.ReadValue<Vector2>();
        Move(moveInput);
    }

    private void OnJump(InputAction.CallbackContext context)
    {
        Jump();
    }

    private void Move(Vector2 input) { }
    private void Jump() { }
}
```

### Input Action Asset (Generated C#)

```csharp
// After generating C# class from Input Actions asset
private PlayerInputActions inputActions;

private void Awake()
{
    inputActions = new PlayerInputActions();
}

private void OnEnable()
{
    inputActions.Player.Enable();
    inputActions.Player.Jump.performed += OnJump;
}

private void OnDisable()
{
    inputActions.Player.Disable();
    inputActions.Player.Jump.performed -= OnJump;
}

private void Update()
{
    Vector2 move = inputActions.Player.Move.ReadValue<Vector2>();
}
```

**Benefits:**
- Type-safe action access
- Auto-completion
- Compile-time checking

### Legacy Input System

```csharp
// Still functional, simpler for basic games
private void Update()
{
    // Keyboard
    if (Input.GetKeyDown(KeyCode.Space))
        Jump();

    // Mouse
    if (Input.GetMouseButtonDown(0))
        Fire();

    // Axis (configured in Edit > Project Settings > Input Manager)
    float horizontal = Input.GetAxis("Horizontal");
    float vertical = Input.GetAxis("Vertical");

    Move(new Vector2(horizontal, vertical));
}
```

**Use for:**
- Simple prototypes
- Mobile touch input
- Legacy projects

**New Input System preferred for:**
- Multi-platform support
- Rebindable controls
- Complex input handling

## UI Systems

### uGUI (Canvas-Based UI)

Standard Unity UI system:

```csharp
using UnityEngine.UI;
using TMPro;  // TextMeshPro

public class UIManager : MonoBehaviour
{
    [SerializeField] private TextMeshProUGUI scoreText;
    [SerializeField] private Button playButton;
    [SerializeField] private Slider healthSlider;

    private void Start()
    {
        playButton.onClick.AddListener(OnPlayClicked);
    }

    private void OnDestroy()
    {
        playButton.onClick.RemoveListener(OnPlayClicked);
    }

    public void UpdateScore(int score)
    {
        scoreText.text = $"Score: {score}";
    }

    public void UpdateHealth(float health, float maxHealth)
    {
        healthSlider.value = health / maxHealth;
    }

    private void OnPlayClicked()
    {
        Debug.Log("Play button clicked");
    }
}
```

**Canvas render modes:**
- **Screen Space - Overlay**: UI always on top, no camera needed (fastest)
- **Screen Space - Camera**: UI rendered by camera, supports post-processing
- **World Space**: 3D UI in game world

**UI Optimization:**
- Separate static/dynamic UI to different canvases
- Disable raycast targets on non-interactive elements
- Use sprite atlases
- Minimize Layout Groups (expensive)

### UI Toolkit (Modern UI)

Runtime and Editor UI (Unity 2021+):

**UXML (UI structure):**
```xml
<ui:UXML>
    <ui:VisualElement name="root">
        <ui:Label text="Score: 0" name="scoreLabel"/>
        <ui:Button text="Play" name="playButton"/>
    </ui:VisualElement>
</ui:UXML>
```

**USS (Styling):**
```css
.root {
    flex-grow: 1;
    background-color: rgb(50, 50, 50);
}

#scoreLabel {
    font-size: 24px;
    color: white;
}
```

**C# (Logic):**
```csharp
using UnityEngine.UIElements;

public class UIController : MonoBehaviour
{
    private UIDocument uiDocument;
    private Label scoreLabel;
    private Button playButton;

    private void Awake()
    {
        uiDocument = GetComponent<UIDocument>();

        var root = uiDocument.rootVisualElement;
        scoreLabel = root.Q<Label>("scoreLabel");
        playButton = root.Q<Button>("playButton");

        playButton.clicked += OnPlayClicked;
    }

    public void UpdateScore(int score)
    {
        scoreLabel.text = $"Score: {score}";
    }

    private void OnPlayClicked()
    {
        Debug.Log("Play clicked");
    }
}
```

**Benefits:**
- Faster performance (retained mode)
- Better for complex UI
- Modern web-like workflow (HTML/CSS equivalent)
- Shared with Editor UI

**Use for:**
- New projects (Unity 2021+)
- Complex UI
- Editor tools

## Asset Management

### Addressables

Async asset loading and memory management:

**Setup:**
1. Window > Asset Management > Addressables > Groups
2. Mark assets as Addressable
3. Organize into groups

**Loading assets:**
```csharp
using UnityEngine.AddressableAssets;
using UnityEngine.ResourceManagement.AsyncOperations;

public class AssetLoader : MonoBehaviour
{
    private async void Start()
    {
        // Load asset asynchronously
        var handle = Addressables.LoadAssetAsync<GameObject>("Enemy");
        await handle.Task;

        if (handle.Status == AsyncOperationStatus.Succeeded)
        {
            GameObject prefab = handle.Result;
            Instantiate(prefab);
        }

        // Release when done
        Addressables.Release(handle);
    }

    // Instantiate directly
    private async void SpawnEnemy()
    {
        var handle = Addressables.InstantiateAsync("Enemy");
        await handle.Task;

        GameObject enemy = handle.Result;
        // Use enemy
    }
}
```

**Benefits:**
- Async loading (no frame hitches)
- Memory management
- Remote content updates
- Build optimization

**Use for:**
- Large games
- DLC/live updates
- Mobile games (reduce install size)

### Resources Folder (Legacy)

Simple asset loading:

```csharp
// Load from Resources folder
GameObject prefab = Resources.Load<GameObject>("Prefabs/Enemy");

// All assets include in build - inefficient
```

**Avoid:** Use Addressables instead for new projects.

## Build Pipeline

### Build Settings

```csharp
using UnityEditor;
using UnityEditor.Build.Reporting;

public static class BuildUtility
{
    [MenuItem("Build/Build Windows")]
    private static void BuildWindows()
    {
        BuildPlayerOptions options = new BuildPlayerOptions
        {
            scenes = new[] { "Assets/Scenes/MainMenu.unity", "Assets/Scenes/Game.unity" },
            locationPathName = "Builds/Windows/Game.exe",
            target = BuildTarget.StandaloneWindows64,
            options = BuildOptions.None
        };

        BuildReport report = BuildPipeline.BuildPlayer(options);

        if (report.summary.result == BuildResult.Succeeded)
        {
            Debug.Log($"Build succeeded: {report.summary.totalSize} bytes");
        }
        else
        {
            Debug.LogError($"Build failed: {report.summary.result}");
        }
    }
}
```

### Build Preprocessing

```csharp
using UnityEditor.Build;
using UnityEditor.Build.Reporting;

public class BuildPreprocessor : IPreprocessBuildWithReport
{
    public int callbackOrder => 0;

    public void OnPreprocessBuild(BuildReport report)
    {
        Debug.Log("Preprocessing build...");

        // Validate assets
        // Update version number
        // Generate build info
    }
}
```

## Best Practices

✅ **DO:**
- Use Editor scripting to automate repetitive tasks
- Implement Custom Inspectors for complex components
- Use new Input System for multi-platform projects
- Optimize UI with separate canvases for static/dynamic content
- Use Addressables for large games and mobile
- Create editor tools for designers/artists
- Validate assets before builds

❌ **DON'T:**
- Hardcode editor paths (use AssetDatabase)
- Forget to unsubscribe from Input System actions
- Mix Layout Groups excessively (UI performance killer)
- Use Resources folder for new projects (use Addressables)
- Create UI in Update loop
- Skip editor validation for critical scripts

**Golden rule**: Automate workflows with editor tools. Time spent creating tools saves exponentially more time in iteration.

---

Apply these workflow optimizations and modern systems for efficient, scalable Unity development.
