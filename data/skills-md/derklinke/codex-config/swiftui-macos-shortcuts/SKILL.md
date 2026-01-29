---
name: swiftui-macos-shortcuts
description: Use when implementing or debugging macOS menu commands and keyboard shortcuts in SwiftUI (Commands, CommandGroup, FocusedValues), especially for File menu Save/Reload or global app shortcuts.
---

# SwiftUI macOS Commands & Shortcuts

## Goal

Implement reliable menu items and keyboard shortcuts in SwiftUI macOS apps, including File menu actions that work across focused views.

## Quick guidance

- Prefer `Commands` + `CommandGroup` (declared on the `App` via `.commands { ... }`) for menu items. Add `.keyboardShortcut` to the `Button`.
- For actions that need app state, prefer `@FocusedValue` so commands resolve to the active window/view context.
- Provide a `FocusedValues` key with a small action struct (e.g., `FileMenuActions`) and set it on the root view via `.focusedValue(...)`.
- Avoid `@EnvironmentObject` inside `Commands` for core actions; it can fail to resolve if no view is focused or when the menu is built before env injection.
- Do not rely on toolbar buttons for keyboard shortcuts; attach shortcuts to menu items instead so Cmd+S/R consistently fire.

## Minimal pattern (File menu)

1) Define a focused value key:

- `struct FileMenuActions { var saveAll: () -> Void; var reloadAll: () -> Void }`
- `extension FocusedValues { var fileMenuActions: FileMenuActions? }`

2) Provide actions on the root view:

- `.focusedValue(\.fileMenuActions, FileMenuActions(saveAll: { ... }, reloadAll: { ... }))`

3) Add commands:

- `CommandGroup(after: .newItem) { Button("Save All") { fileMenuActions?.saveAll() }.keyboardShortcut("s") }`
- `Button("Reload All") { fileMenuActions?.reloadAll() }.keyboardShortcut("r")`

## Notes

- Use `.disabled(fileMenuActions == nil)` to avoid menu items when no focus.
- Use `.keyboardShortcut("s", modifiers: [.command])` for Cmd+S if needed, but default for String uses Cmd automatically.
- If you want to replace default Save, use `CommandGroup(replacing: .saveItem)`.
- Keep menu items in File by using `.newItem` or `.saveItem` groups rather than `.appSettings` or `.toolbar`.
