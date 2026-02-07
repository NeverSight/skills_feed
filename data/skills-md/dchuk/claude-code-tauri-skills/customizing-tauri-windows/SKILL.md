---
name: customizing-tauri-windows
description: Guides users through Tauri window customization including custom titlebar implementation, transparent windows, window decorations, drag regions, window menus, submenus, and menu keyboard shortcuts for desktop applications.
---

# Tauri Window Customization

Covers window customization in Tauri v2: custom titlebars, transparent windows, and window menus.

## Configuration Methods

- **tauri.conf.json** - Static configuration at build time
- **JavaScript Window API** - Runtime modifications from frontend
- **Rust Window struct** - Runtime modifications from backend

## Window Configuration (tauri.conf.json)

```json
{
  "app": {
    "windows": [{
      "title": "My App",
      "width": 800,
      "height": 600,
      "decorations": true,
      "transparent": false,
      "alwaysOnTop": false,
      "center": true
    }]
  }
}
```

## Custom Titlebar Implementation

### Step 1: Disable Decorations

```json
{ "app": { "windows": [{ "decorations": false }] } }
```

### Step 2: Configure Permissions (src-tauri/capabilities/default.json)

```json
{
  "identifier": "main-capability",
  "windows": ["main"],
  "permissions": [
    "core:window:default",
    "core:window:allow-start-dragging",
    "core:window:allow-close",
    "core:window:allow-minimize",
    "core:window:allow-toggle-maximize"
  ]
}
```

### Step 3: HTML Structure

```html
<div class="titlebar">
  <div class="titlebar-drag" data-tauri-drag-region>
    <span class="title">My Application</span>
  </div>
  <div class="titlebar-controls">
    <button id="titlebar-minimize">-</button>
    <button id="titlebar-maximize">[]</button>
    <button id="titlebar-close">x</button>
  </div>
</div>
<main class="content"><!-- App content --></main>
```

### Step 4: CSS Styling

```css
.titlebar {
  height: 30px;
  background: #329ea3;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  display: grid;
  grid-template-columns: 1fr auto;
  user-select: none;
}

.titlebar-drag {
  display: flex;
  align-items: center;
  padding-left: 12px;
}

.titlebar-controls { display: flex; }

.titlebar-controls button {
  width: 46px;
  height: 30px;
  border: none;
  background: transparent;
  color: white;
  cursor: pointer;
}

.titlebar-controls button:hover { background: rgba(255,255,255,0.1); }
.titlebar-controls button#titlebar-close:hover { background: #e81123; }
.content { margin-top: 30px; padding: 16px; }
```

### Step 5: JavaScript Controls

```typescript
import { getCurrentWindow } from '@tauri-apps/api/window';

const appWindow = getCurrentWindow();

document.getElementById('titlebar-minimize')
  ?.addEventListener('click', () => appWindow.minimize());
document.getElementById('titlebar-maximize')
  ?.addEventListener('click', () => appWindow.toggleMaximize());
document.getElementById('titlebar-close')
  ?.addEventListener('click', () => appWindow.close());
```

### Drag Region Behavior

The `data-tauri-drag-region` attribute applies only to its element, not children. This preserves button interactivity. Add the attribute to each draggable child if needed.

### Manual Drag with Double-Click Maximize

```typescript
document.getElementById('titlebar')?.addEventListener('mousedown', (e) => {
  if (e.buttons === 1 && e.target === e.currentTarget) {
    e.detail === 2 ? appWindow.toggleMaximize() : appWindow.startDragging();
  }
});
```

## macOS Transparent Titlebar

### Cargo.toml

```toml
[target."cfg(target_os = \"macos\")".dependencies]
cocoa = "0.26"
```

### Rust Implementation

```rust
use tauri::{TitleBarStyle, WebviewUrl, WebviewWindowBuilder};

pub fn run() {
    tauri::Builder::default()
        .setup(|app| {
            let win_builder = WebviewWindowBuilder::new(app, "main", WebviewUrl::default())
                .title("Transparent Titlebar Window")
                .inner_size(800.0, 600.0);

            #[cfg(target_os = "macos")]
            let win_builder = win_builder.title_bar_style(TitleBarStyle::Transparent);

            let window = win_builder.build().unwrap();

            #[cfg(target_os = "macos")]
            {
                use cocoa::appkit::{NSColor, NSWindow};
                use cocoa::base::{id, nil};
                let ns_window = window.ns_window().unwrap() as id;
                unsafe {
                    let bg_color = NSColor::colorWithRed_green_blue_alpha_(
                        nil, 50.0/255.0, 158.0/255.0, 163.5/255.0, 1.0
                    );
                    ns_window.setBackgroundColor_(bg_color);
                }
            }
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application")
}
```

**Note**: Custom titlebars on macOS lose native features like window snapping. Transparent titlebar preserves these.

## Window Menus

### Menu Item Types

| Type | Description |
|------|-------------|
| Text | Basic labeled menu option |
| Check | Toggleable entry with checked state |
| Separator | Visual divider between sections |
| Icon | Entry with custom icon (Tauri 2.8.0+) |

### Creating Menus (JavaScript/TypeScript)

```typescript
import { Menu, MenuItem, Submenu, PredefinedMenuItem, CheckMenuItem } from '@tauri-apps/api/menu';

const fileSubmenu = await Submenu.new({
  text: 'File',
  items: [
    await MenuItem.new({
      id: 'new', text: 'New', accelerator: 'CmdOrCtrl+N',
      action: () => console.log('New')
    }),
    await MenuItem.new({
      id: 'open', text: 'Open', accelerator: 'CmdOrCtrl+O',
      action: () => console.log('Open')
    }),
    await MenuItem.new({
      id: 'save', text: 'Save', accelerator: 'CmdOrCtrl+S',
      action: () => console.log('Save')
    }),
    { type: 'Separator' },
    await MenuItem.new({
      id: 'quit', text: 'Quit', accelerator: 'CmdOrCtrl+Q',
      action: () => console.log('Quit')
    })
  ]
});

const editSubmenu = await Submenu.new({
  text: 'Edit',
  items: [
    await PredefinedMenuItem.new({ item: 'Undo' }),
    await PredefinedMenuItem.new({ item: 'Redo' }),
    await PredefinedMenuItem.new({ item: 'Separator' }),
    await PredefinedMenuItem.new({ item: 'Cut' }),
    await PredefinedMenuItem.new({ item: 'Copy' }),
    await PredefinedMenuItem.new({ item: 'Paste' })
  ]
});

const viewSubmenu = await Submenu.new({
  text: 'View',
  items: [
    await CheckMenuItem.new({
      id: 'sidebar', text: 'Show Sidebar', checked: true,
      action: async (item) => console.log('Sidebar:', await item.isChecked())
    })
  ]
});

const menu = await Menu.new({ items: [fileSubmenu, editSubmenu, viewSubmenu] });
await menu.setAsAppMenu();
```

### Creating Menus (Rust)

```rust
use tauri::menu::{MenuBuilder, SubmenuBuilder};

let file_menu = SubmenuBuilder::new(app, "File")
    .text("new", "New")
    .text("open", "Open")
    .text("save", "Save")
    .separator()
    .text("quit", "Quit")
    .build()?;

let edit_menu = SubmenuBuilder::new(app, "Edit")
    .undo()
    .redo()
    .separator()
    .cut()
    .copy()
    .paste()
    .build()?;

let menu = MenuBuilder::new(app)
    .items(&[&file_menu, &edit_menu])
    .build()?;

app.set_menu(menu)?;
```

**macOS Note**: All menu items must be grouped under submenus. Top-level items are ignored.

### Handling Menu Events (Rust)

```rust
app.on_menu_event(|_app_handle, event| {
    match event.id().0.as_str() {
        "new" => println!("New file"),
        "open" => println!("Open file"),
        "save" => println!("Save file"),
        "quit" => std::process::exit(0),
        _ => {}
    }
});
```

### Dynamic Menu Updates

**JavaScript:**
```typescript
const statusItem = await menu.get('status');
if (statusItem) await statusItem.setText('Status: Ready');
```

**Rust:**
```rust
menu.get("status").unwrap().as_menuitem_unchecked().set_text("Status: Ready")?;
```

## Keyboard Shortcuts (Accelerators)

| Shortcut | Accelerator String |
|----------|-------------------|
| Ctrl+S / Cmd+S | `CmdOrCtrl+S` |
| Ctrl+Shift+S | `CmdOrCtrl+Shift+S` |
| Alt+F4 | `Alt+F4` |
| F11 | `F11` |

## Complete Example

### main.rs

```rust
use tauri::menu::{MenuBuilder, SubmenuBuilder};

pub fn run() {
    tauri::Builder::default()
        .setup(|app| {
            let file_menu = SubmenuBuilder::new(app, "File")
                .text("new", "New")
                .text("open", "Open")
                .separator()
                .text("quit", "Quit")
                .build()?;

            let edit_menu = SubmenuBuilder::new(app, "Edit")
                .undo().redo().separator().cut().copy().paste()
                .build()?;

            let menu = MenuBuilder::new(app)
                .items(&[&file_menu, &edit_menu])
                .build()?;
            app.set_menu(menu)?;
            Ok(())
        })
        .on_menu_event(|_app, event| {
            match event.id().0.as_str() {
                "quit" => std::process::exit(0),
                id => println!("Menu event: {}", id),
            }
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application")
}
```

### React Component

```tsx
import { useEffect } from 'react';
import { getCurrentWindow } from '@tauri-apps/api/window';

function App() {
  useEffect(() => {
    const appWindow = getCurrentWindow();
    const minimize = () => appWindow.minimize();
    const maximize = () => appWindow.toggleMaximize();
    const close = () => appWindow.close();

    document.getElementById('titlebar-minimize')?.addEventListener('click', minimize);
    document.getElementById('titlebar-maximize')?.addEventListener('click', maximize);
    document.getElementById('titlebar-close')?.addEventListener('click', close);

    return () => {
      document.getElementById('titlebar-minimize')?.removeEventListener('click', minimize);
      document.getElementById('titlebar-maximize')?.removeEventListener('click', maximize);
      document.getElementById('titlebar-close')?.removeEventListener('click', close);
    };
  }, []);

  return (
    <>
      <div className="titlebar">
        <div className="titlebar-drag" data-tauri-drag-region>
          <span>My Tauri App</span>
        </div>
        <div className="titlebar-controls">
          <button id="titlebar-minimize">-</button>
          <button id="titlebar-maximize">[]</button>
          <button id="titlebar-close">x</button>
        </div>
      </div>
      <main className="content">
        <h1>Welcome to Tauri</h1>
      </main>
    </>
  );
}

export default App;
```
