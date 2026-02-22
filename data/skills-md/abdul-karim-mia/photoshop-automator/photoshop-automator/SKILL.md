---
name: photoshop-automator
description: "Professional Adobe Photoshop automation via COM/ExtendScript bridge. Supports text updates, filters, and action playback."
metadata:
  {
    "openclaw":
      {
        "requires": { 
          "bins": ["cscript", "osascript"], 
          "os": ["windows", "macos"],
          "env": [], 
          "config": [] 
        }
      }
  }
---

# Photoshop Automator Skill (v1.2.4)

This skill provides a high-performance bridge for automating Adobe Photoshop (vCS6 - 2026+) on Windows and macOS using the ExtendScript (JSX) engine via VBScript or AppleScript.

## Commands

- **runScript**: Executes raw ExtendScript (ES3) code. Use this for complex document manipulation.
- **updateText**: Target a specific text layer by name and update its contents instantly.
- **createLayer**: Create new art layers with custom opacity and blending modes.
- **applyFilter**: Apply a professional Gaussian Blur filter to the active layer.
- **playAction**: Play recorded Photoshop actions (.atn) by name and set.
- **export**: Save the active document as a high-quality PNG or JPEG.

## 🛠 AI Protocol

### 1. Technical Constraints (Strict)
- **ES3 Syntax Only**: Photoshop's ExtendScript engine uses **ECMAScript 3 (ES3)**. 
    - ❌ **DO NOT USE**: `const`, `let`, arrow functions `() => {}`, template literals `` `${}` ``, or `Map`/`Set`.
    - ✅ **USE**: Only `var`, standard `function` declarations, and string concatenation (`'a' + b`).
- **Assume Active Document**: Commands operate on the *active* document. If none is open, scripts will fail unless they call `app.documents.add()`.

### 2. Security & Side Effects
- **Filesystem Access**: The `runScript` command allows execution of arbitrary ExtendScript. This engine has **direct access to the host filesystem**.
- **Side Effects**: Scripts can create, modify, or delete files on the local machine via the `File` and `Folder` objects.
- **Verification**: Always review dynamically generated scripts before execution to prevent unintended document or filesystem modifications.

### 3. Error Handling
- **GUI Blocks**: If Photoshop has a modal dialog open (e.g., Save As window, error popup), COM operations will hang or fail. Direct the user to close any open dialogs.
- **Layer Presence**: If `updateText` fails, ensure the layer name provided matches exactly (case-sensitive) with the layer in the PSD.

## Setup

Ensure Adobe Photoshop is installed on the host system. The skill automatically uses the registered COM server.

---
Developed for the OpenClaw community by [Abdul Karim Mia](https://github.com/abdul-karim-mia).
