---
name: powershell-ui-architect
description: Expert in building GUIs and TUIs with PowerShell using WinForms, WPF, and Console/TUI frameworks. Use when creating PowerShell tools with graphical or terminal interfaces. Triggers include "PowerShell GUI", "WinForms", "WPF PowerShell", "PowerShell TUI", "terminal UI", "PowerShell interface".
---

# PowerShell UI Architect

## Purpose
Provides expertise in building graphical user interfaces (GUI) and terminal user interfaces (TUI) with PowerShell. Specializes in WinForms, WPF, and console-based TUI frameworks for creating user-friendly PowerShell tools.

## When to Use
- Building PowerShell tools with GUI
- Creating WinForms applications
- Developing WPF interfaces for scripts
- Building terminal user interfaces (TUI)
- Adding dialogs to automation scripts
- Creating interactive admin tools
- Building configuration wizards
- Implementing progress displays

## Quick Start
**Invoke this skill when:**
- Creating GUIs for PowerShell scripts
- Building WinForms or WPF interfaces
- Developing terminal-based UIs
- Adding interactive dialogs to tools
- Creating admin tool interfaces

**Do NOT invoke when:**
- Cross-platform CLI tools → use `/cli-developer`
- PowerShell module design → use `/powershell-module-architect`
- Web interfaces → use `/frontend-design`
- Windows app development (non-PS) → use `/windows-app-developer`

## Decision Framework
```
UI Type Needed?
├── Simple Dialog
│   └── WinForms MessageBox / InputBox
├── Full Windows App
│   ├── Simple layout → WinForms
│   └── Rich UI → WPF with XAML
├── Console/Terminal
│   ├── Simple menu → Write-Host + Read-Host
│   └── Rich TUI → Terminal.Gui / PSReadLine
└── Cross-Platform
    └── Terminal-based only
```

## Core Workflows

### 1. WinForms Application
1. Add System.Windows.Forms assembly
2. Create Form object
3. Add controls (buttons, text boxes)
4. Wire up event handlers
5. Configure layout
6. Show form with ShowDialog()

### 2. WPF Interface
1. Define XAML layout
2. Load XAML in PowerShell
3. Get control references
4. Add event handlers
5. Implement logic
6. Display window

### 3. TUI with Terminal.Gui
1. Install Terminal.Gui module
2. Initialize application
3. Create window and views
4. Add controls (buttons, lists, text)
5. Handle events
6. Run main loop

## Best Practices
- Keep UI code separate from logic
- Use XAML for complex WPF layouts
- Handle errors gracefully with user feedback
- Provide progress indication for long operations
- Test on target Windows versions
- Use appropriate UI for audience (GUI vs TUI)

## Anti-Patterns
| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| UI logic mixed with business logic | Hard to maintain | Separate concerns |
| Blocking UI thread | Frozen interface | Use runspaces/jobs |
| No input validation | Crashes, bad data | Validate before use |
| Hardcoded sizes | Scaling issues | Use anchoring/docking |
| No error messages | Confused users | Friendly error dialogs |
