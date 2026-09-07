---
name: hz-unity-tmp-resources
license: Apache-2.0
description: Imports and configures TextMesh Pro Essential Resources for Unity projects targeting Meta Quest and Horizon OS. Use when setting up TMP UI, fixing missing TMP materials or fonts, or resolving pink/magenta TMP text.
---

# TextMesh Pro Resources Import

## When to use this skill

Use this skill automatically when any of the following are detected:

- TMP text appears **pink/magenta** in the scene
- Console errors mentioning `LiberationSans SDF`, `TMP Settings`, or missing TMP materials
- Creating the first TMP text element in a project
- User asks to set up TextMesh Pro or create UI text
- `Assets/TextMesh Pro/Resources/` folder does not exist

## Step 1: Check if TMP resources are already imported

Before importing, check whether resources already exist using `Unity_RunCommand`:

```csharp
using UnityEngine;
using UnityEditor;
using System.IO;

internal class CommandScript : IRunCommand
{
    public void Execute(ExecutionResult result)
    {
        string resourcesPath = Path.Combine(Application.dataPath, "TextMesh Pro", "Resources");
        bool imported = Directory.Exists(resourcesPath);

        if (imported)
        {
            string fontPath = "Assets/TextMesh Pro/Resources/Fonts & Materials/LiberationSans SDF.asset";
            var font = AssetDatabase.LoadAssetAtPath<Object>(fontPath);
            result.Log("TMP Essential Resources: ALREADY IMPORTED. Default font present: {0}", font != null);
        }
        else
        {
            result.Log("TMP Essential Resources: NOT IMPORTED. Resources folder missing at {0}", resourcesPath);
        }
    }
}
```

If already imported, stop here — no action needed.

## Step 2: Import TMP Essential Resources

**IMPORTANT**: The TMP import process opens a Unity dialog that requires manual user interaction. This cannot be fully automated via MCP.

Use `Unity_RunCommand` to trigger the import dialog:

```csharp
using UnityEngine;
using UnityEditor;

internal class CommandScript : IRunCommand
{
    public void Execute(ExecutionResult result)
    {
        EditorApplication.ExecuteMenuItem("Window/TextMeshPro/Import TMP Essential Resources");
        result.Log("TMP Essential Resources import dialog opened. User must click Import in the Unity Editor.");
    }
}
```

After executing, **you MUST**:
1. Tell the user: "The Import Unity Package dialog has opened in Unity. Please click the **Import** button, then let me know when it's done."
2. **Wait** for the user to confirm before proceeding.
3. Do NOT assume import succeeded without confirmation.

## Step 3: Verify import succeeded

After the user confirms, verify with `Unity_RunCommand`:

```csharp
using UnityEngine;
using UnityEditor;
using System.IO;

internal class CommandScript : IRunCommand
{
    public void Execute(ExecutionResult result)
    {
        string resourcesPath = Path.Combine(Application.dataPath, "TextMesh Pro", "Resources");
        if (!Directory.Exists(resourcesPath))
        {
            result.LogError("Import failed: Resources folder not found at " + resourcesPath);
            return;
        }

        string fontPath = "Assets/TextMesh Pro/Resources/Fonts & Materials/LiberationSans SDF.asset";
        var font = AssetDatabase.LoadAssetAtPath<Object>(fontPath);
        if (font == null)
        {
            result.LogError("Import incomplete: Default font asset not found at " + fontPath);
            return;
        }

        var settingsGuids = AssetDatabase.FindAssets("t:TMP_Settings");
        if (settingsGuids.Length == 0)
        {
            result.LogError("Import incomplete: TMP_Settings asset not found.");
            return;
        }

        result.Log("TMP Essential Resources verified: folder exists, default font present, TMP_Settings found.");
    }
}
```

## Troubleshooting

### Pink/magenta text after import

If text still appears pink after importing resources, force a shader recompilation via `Unity_RunCommand`:

```csharp
using UnityEngine;
using UnityEditor;

internal class CommandScript : IRunCommand
{
    public void Execute(ExecutionResult result)
    {
        var shaderGuids = AssetDatabase.FindAssets("t:Shader TextMeshPro");
        int reimported = 0;
        foreach (var guid in shaderGuids)
        {
            string path = AssetDatabase.GUIDToAssetPath(guid);
            AssetDatabase.ImportAsset(path, ImportAssetOptions.ForceUpdate);
            reimported++;
        }
        result.Log("Reimported {0} TMP shaders.", reimported);
    }
}
```

### Menu item grayed out or missing

If `Window/TextMeshPro/Import TMP Essential Resources` is not available:
- Resources may already be imported — run Step 1 to check.
- TMP package may not be installed. Install it via `Unity_RunCommand`:

```csharp
using UnityEngine;
using UnityEditor;
using UnityEditor.PackageManager;

internal class CommandScript : IRunCommand
{
    public void Execute(ExecutionResult result)
    {
        var request = Client.Add("com.unity.textmeshpro");
        // Busy-wait is required here because Unity_RunCommand scripts run synchronously.
        // This will briefly block the editor (typically < 5 seconds).
        while (!request.IsCompleted) { }

        if (request.Status == StatusCode.Success)
            result.Log("TextMesh Pro package installed: {0}", request.Result.version);
        else
            result.LogError("Failed to install TMP: " + request.Error.message);
    }
}
```

## Integration with meta-quest-ui skill

This skill handles **importing TMP resources**. For VR-specific UI configuration (canvas setup, text sizing, viewing distances), use the **meta-quest-ui** skill after TMP resources are imported.
