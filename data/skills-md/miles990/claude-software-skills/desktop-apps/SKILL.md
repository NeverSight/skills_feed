---
name: desktop-apps
description: Desktop application development with Electron and Tauri
domain: domain-applications
version: 1.0.0
tags: [electron, tauri, desktop, cross-platform, native]
triggers:
  keywords:
    primary: [electron, tauri, desktop app, cross-platform, native app]
    secondary: [ipc, preload, auto-updater, rust backend, menu, tray]
  context_boost: [desktop, windows, macos, linux, native]
  context_penalty: [web, mobile, browser, api]
  priority: medium
---

# Desktop Application Development

## Overview

Building cross-platform desktop applications using web technologies with Electron and Tauri.

---

## Electron

### Main Process

```typescript
// main.ts
import { app, BrowserWindow, ipcMain, dialog, Menu } from 'electron';
import path from 'path';

let mainWindow: BrowserWindow | null = null;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
    titleBarStyle: 'hiddenInset', // macOS
    frame: process.platform !== 'darwin',
  });

  // Load the app
  if (process.env.NODE_ENV === 'development') {
    mainWindow.loadURL('http://localhost:3000');
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(path.join(__dirname, '../dist/index.html'));
  }

  // Window events
  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// App lifecycle
app.whenReady().then(() => {
  createWindow();
  createMenu();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// IPC handlers
ipcMain.handle('dialog:openFile', async () => {
  const result = await dialog.showOpenDialog(mainWindow!, {
    properties: ['openFile'],
    filters: [
      { name: 'Documents', extensions: ['txt', 'md', 'json'] },
    ],
  });

  if (!result.canceled && result.filePaths.length > 0) {
    return result.filePaths[0];
  }
  return null;
});

ipcMain.handle('dialog:saveFile', async (_, content: string) => {
  const result = await dialog.showSaveDialog(mainWindow!, {
    filters: [{ name: 'JSON', extensions: ['json'] }],
  });

  if (!result.canceled && result.filePath) {
    await fs.writeFile(result.filePath, content);
    return result.filePath;
  }
  return null;
});

ipcMain.handle('app:getVersion', () => app.getVersion());

// Auto-updater
import { autoUpdater } from 'electron-updater';

autoUpdater.checkForUpdatesAndNotify();

autoUpdater.on('update-available', () => {
  mainWindow?.webContents.send('update-available');
});

autoUpdater.on('update-downloaded', () => {
  mainWindow?.webContents.send('update-downloaded');
});

ipcMain.handle('app:installUpdate', () => {
  autoUpdater.quitAndInstall();
});
```

### Preload Script

```typescript
// preload.ts
import { contextBridge, ipcRenderer } from 'electron';

// Expose safe APIs to renderer
contextBridge.exposeInMainWorld('electronAPI', {
  // File operations
  openFile: () => ipcRenderer.invoke('dialog:openFile'),
  saveFile: (content: string) => ipcRenderer.invoke('dialog:saveFile', content),
  readFile: (path: string) => ipcRenderer.invoke('fs:readFile', path),
  writeFile: (path: string, content: string) =>
    ipcRenderer.invoke('fs:writeFile', path, content),

  // App info
  getVersion: () => ipcRenderer.invoke('app:getVersion'),
  getPlatform: () => process.platform,

  // Updates
  installUpdate: () => ipcRenderer.invoke('app:installUpdate'),
  onUpdateAvailable: (callback: () => void) => {
    ipcRenderer.on('update-available', callback);
    return () => ipcRenderer.removeListener('update-available', callback);
  },
  onUpdateDownloaded: (callback: () => void) => {
    ipcRenderer.on('update-downloaded', callback);
    return () => ipcRenderer.removeListener('update-downloaded', callback);
  },

  // Window controls
  minimize: () => ipcRenderer.send('window:minimize'),
  maximize: () => ipcRenderer.send('window:maximize'),
  close: () => ipcRenderer.send('window:close'),

  // Native notifications
  showNotification: (title: string, body: string) =>
    ipcRenderer.invoke('notification:show', title, body),
});

// TypeScript types for renderer
declare global {
  interface Window {
    electronAPI: {
      openFile: () => Promise<string | null>;
      saveFile: (content: string) => Promise<string | null>;
      readFile: (path: string) => Promise<string>;
      writeFile: (path: string, content: string) => Promise<void>;
      getVersion: () => Promise<string>;
      getPlatform: () => string;
      installUpdate: () => Promise<void>;
      onUpdateAvailable: (callback: () => void) => () => void;
      onUpdateDownloaded: (callback: () => void) => () => void;
      minimize: () => void;
      maximize: () => void;
      close: () => void;
      showNotification: (title: string, body: string) => Promise<void>;
    };
  }
}
```

### Renderer (React)

```tsx
// App.tsx
function App() {
  const [updateAvailable, setUpdateAvailable] = useState(false);
  const [updateReady, setUpdateReady] = useState(false);

  useEffect(() => {
    const removeAvailable = window.electronAPI.onUpdateAvailable(() => {
      setUpdateAvailable(true);
    });

    const removeDownloaded = window.electronAPI.onUpdateDownloaded(() => {
      setUpdateReady(true);
    });

    return () => {
      removeAvailable();
      removeDownloaded();
    };
  }, []);

  const handleOpenFile = async () => {
    const filePath = await window.electronAPI.openFile();
    if (filePath) {
      const content = await window.electronAPI.readFile(filePath);
      // Handle file content
    }
  };

  const handleSaveFile = async () => {
    const content = JSON.stringify(data, null, 2);
    await window.electronAPI.saveFile(content);
  };

  return (
    <div className="app">
      {/* Custom title bar for frameless window */}
      <TitleBar />

      <main>
        <button onClick={handleOpenFile}>Open File</button>
        <button onClick={handleSaveFile}>Save File</button>

        {updateReady && (
          <button onClick={() => window.electronAPI.installUpdate()}>
            Install Update & Restart
          </button>
        )}
      </main>
    </div>
  );
}

// Custom title bar component
function TitleBar() {
  const platform = window.electronAPI.getPlatform();

  return (
    <div className="title-bar" style={{ WebkitAppRegion: 'drag' }}>
      <span className="title">My App</span>

      {platform !== 'darwin' && (
        <div className="window-controls" style={{ WebkitAppRegion: 'no-drag' }}>
          <button onClick={() => window.electronAPI.minimize()}>−</button>
          <button onClick={() => window.electronAPI.maximize()}>□</button>
          <button onClick={() => window.electronAPI.close()}>×</button>
        </div>
      )}
    </div>
  );
}
```

---

## Tauri

### Rust Backend

```rust
// src-tauri/src/main.rs
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri::{CustomMenuItem, Menu, MenuItem, Submenu};
use std::fs;

// Commands callable from frontend
#[tauri::command]
fn read_file(path: String) -> Result<String, String> {
    fs::read_to_string(&path).map_err(|e| e.to_string())
}

#[tauri::command]
fn write_file(path: String, content: String) -> Result<(), String> {
    fs::write(&path, &content).map_err(|e| e.to_string())
}

#[tauri::command]
fn get_app_version() -> String {
    env!("CARGO_PKG_VERSION").to_string()
}

#[tauri::command]
async fn perform_heavy_task(input: String) -> Result<String, String> {
    // Run CPU-intensive work in background
    tokio::task::spawn_blocking(move || {
        // Heavy computation here
        format!("Processed: {}", input)
    })
    .await
    .map_err(|e| e.to_string())
}

fn main() {
    let menu = Menu::new()
        .add_submenu(Submenu::new(
            "File",
            Menu::new()
                .add_item(CustomMenuItem::new("open", "Open").accelerator("CmdOrCtrl+O"))
                .add_item(CustomMenuItem::new("save", "Save").accelerator("CmdOrCtrl+S"))
                .add_native_item(MenuItem::Separator)
                .add_native_item(MenuItem::Quit),
        ))
        .add_submenu(Submenu::new(
            "Edit",
            Menu::new()
                .add_native_item(MenuItem::Undo)
                .add_native_item(MenuItem::Redo)
                .add_native_item(MenuItem::Separator)
                .add_native_item(MenuItem::Cut)
                .add_native_item(MenuItem::Copy)
                .add_native_item(MenuItem::Paste),
        ));

    tauri::Builder::default()
        .menu(menu)
        .on_menu_event(|event| {
            match event.menu_item_id() {
                "open" => {
                    event.window().emit("menu-open", {}).unwrap();
                }
                "save" => {
                    event.window().emit("menu-save", {}).unwrap();
                }
                _ => {}
            }
        })
        .invoke_handler(tauri::generate_handler![
            read_file,
            write_file,
            get_app_version,
            perform_heavy_task,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

### Tauri Configuration

```json
// src-tauri/tauri.conf.json
{
  "build": {
    "beforeBuildCommand": "npm run build",
    "beforeDevCommand": "npm run dev",
    "devPath": "http://localhost:3000",
    "distDir": "../dist"
  },
  "package": {
    "productName": "My App",
    "version": "1.0.0"
  },
  "tauri": {
    "allowlist": {
      "all": false,
      "dialog": {
        "all": true
      },
      "fs": {
        "all": true,
        "scope": ["$DOCUMENT/*", "$DOWNLOAD/*"]
      },
      "shell": {
        "open": true
      },
      "notification": {
        "all": true
      }
    },
    "bundle": {
      "active": true,
      "icon": [
        "icons/32x32.png",
        "icons/128x128.png",
        "icons/icon.icns",
        "icons/icon.ico"
      ],
      "identifier": "com.example.myapp",
      "targets": "all"
    },
    "windows": [
      {
        "title": "My App",
        "width": 1200,
        "height": 800,
        "minWidth": 800,
        "minHeight": 600,
        "resizable": true,
        "fullscreen": false
      }
    ],
    "updater": {
      "active": true,
      "endpoints": ["https://releases.example.com/{{target}}/{{current_version}}"],
      "pubkey": "YOUR_PUBLIC_KEY"
    }
  }
}
```

### Frontend Integration

```typescript
// Using Tauri APIs
import { invoke } from '@tauri-apps/api/tauri';
import { open, save } from '@tauri-apps/api/dialog';
import { readTextFile, writeTextFile } from '@tauri-apps/api/fs';
import { sendNotification } from '@tauri-apps/api/notification';
import { listen } from '@tauri-apps/api/event';

// Call Rust commands
async function readFile(path: string): Promise<string> {
  return invoke('read_file', { path });
}

async function writeFile(path: string, content: string): Promise<void> {
  return invoke('write_file', { path, content });
}

// Use Tauri dialog
async function openFileDialog() {
  const selected = await open({
    multiple: false,
    filters: [{ name: 'Documents', extensions: ['txt', 'md', 'json'] }],
  });

  if (selected && typeof selected === 'string') {
    const content = await readTextFile(selected);
    return { path: selected, content };
  }
  return null;
}

async function saveFileDialog(content: string) {
  const filePath = await save({
    filters: [{ name: 'JSON', extensions: ['json'] }],
  });

  if (filePath) {
    await writeTextFile(filePath, content);
    return filePath;
  }
  return null;
}

// Listen for menu events
listen('menu-open', async () => {
  const file = await openFileDialog();
  if (file) {
    // Handle file
  }
});

// Send notification
async function notify(title: string, body: string) {
  await sendNotification({ title, body });
}
```

---

## Local Storage & Database

```typescript
// SQLite with better-sqlite3 (Electron)
import Database from 'better-sqlite3';

const db = new Database('app.db');

// Initialize schema
db.exec(`
  CREATE TABLE IF NOT EXISTS documents (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )
`);

// CRUD operations
const insertDoc = db.prepare(
  'INSERT INTO documents (id, title, content) VALUES (?, ?, ?)'
);

const getDoc = db.prepare('SELECT * FROM documents WHERE id = ?');

const getAllDocs = db.prepare('SELECT * FROM documents ORDER BY updated_at DESC');

const updateDoc = db.prepare(
  'UPDATE documents SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?'
);

const deleteDoc = db.prepare('DELETE FROM documents WHERE id = ?');

// Usage
insertDoc.run(uuid(), 'New Document', '');
const doc = getDoc.get('doc-id');
const docs = getAllDocs.all();
```

---

## Related Skills

- [[frontend]] - Web technologies
- [[system-design]] - Application architecture
- [[devops-cicd]] - Desktop app distribution

