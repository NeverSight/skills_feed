---
name: electron-architect
description: Electron desktop application architect. Use when designing Electron apps, implementing IPC communication, handling security best practices, or packaging for distribution.
---

# Electron Architecture Expert

Expert assistant for Electron desktop application architecture, Main/Renderer process design, IPC communication, security best practices, and application packaging.

## How It Works

1. Analyzes application requirements
2. Designs secure Main/Renderer architecture
3. Implements safe IPC communication patterns
4. Provides packaging and distribution configuration
5. Ensures security best practices

## Usage

### Scaffold New Project

```bash
bash /mnt/skills/user/electron-architect/scripts/scaffold-project.sh [project-name] [ui-framework] [package-manager]
```

**Arguments:**
- `project-name` - Name of the project (default: my-electron-app)
- `ui-framework` - UI framework: vanilla, react, svelte, vue (default: vanilla)
- `package-manager` - Package manager: pnpm, npm, yarn (default: pnpm)

**Examples:**
```bash
bash /mnt/skills/user/electron-architect/scripts/scaffold-project.sh my-app
bash /mnt/skills/user/electron-architect/scripts/scaffold-project.sh my-app react
bash /mnt/skills/user/electron-architect/scripts/scaffold-project.sh my-app svelte pnpm
```

**Security defaults:**
- nodeIntegration: false
- contextIsolation: true
- sandbox: true

## Documentation Resources

**Official Documentation:**
- Electron: `https://www.electronjs.org/docs/latest/`
- Electron Forge: `https://www.electronforge.io/`
- electron-builder: `https://www.electron.build/`

## Project Structure

```
src/
├── main/
│   ├── main.ts              # Main process entry
│   ├── ipc/                  # IPC handlers
│   │   └── file-handlers.ts
│   ├── services/             # Backend services
│   │   └── database.ts
│   └── menu.ts               # Application menu
├── preload/
│   └── preload.ts            # Context bridge
├── renderer/                 # UI (React/Svelte/Vue)
│   ├── App.tsx
│   └── components/
└── shared/
    └── types.ts              # Shared type definitions
```

## Security Configuration

### BrowserWindow Settings

```typescript
// main.ts - Secure configuration
const mainWindow = new BrowserWindow({
  width: 1200,
  height: 800,
  webPreferences: {
    nodeIntegration: false,      // Disable Node.js
    contextIsolation: true,      // Enable context isolation
    sandbox: true,               // Sandbox mode
    preload: path.join(__dirname, 'preload.js'),
    webSecurity: true,           // Enforce same-origin
  }
});
```

### Preload Script Pattern

```typescript
// preload.ts - Safe API exposure
import { contextBridge, ipcRenderer } from 'electron';

contextBridge.exposeInMainWorld('electronAPI', {
  // One-way: Renderer → Main
  saveFile: (content: string) =>
    ipcRenderer.invoke('file:save', content),

  // One-way: Main → Renderer
  onUpdateAvailable: (callback: (version: string) => void) =>
    ipcRenderer.on('update-available', (_, version) => callback(version)),

  // Request-response pattern
  openFile: () => ipcRenderer.invoke('dialog:openFile'),
});

// Type declaration for renderer
declare global {
  interface Window {
    electronAPI: {
      saveFile: (content: string) => Promise<boolean>;
      onUpdateAvailable: (callback: (version: string) => void) => void;
      openFile: () => Promise<string | null>;
    }
  }
}
```

### Main Process Handlers

```typescript
// main/ipc/file-handlers.ts
import { ipcMain, dialog } from 'electron';
import { readFile, writeFile } from 'fs/promises';

export function registerFileHandlers() {
  ipcMain.handle('dialog:openFile', async () => {
    const { canceled, filePaths } = await dialog.showOpenDialog({
      properties: ['openFile'],
      filters: [{ name: 'Text', extensions: ['txt', 'md'] }]
    });
    if (canceled) return null;
    return readFile(filePaths[0], 'utf-8');
  });

  ipcMain.handle('file:save', async (_, content: string) => {
    const { canceled, filePath } = await dialog.showSaveDialog({});
    if (canceled || !filePath) return false;
    await writeFile(filePath, content);
    return true;
  });
}
```

## IPC Communication Patterns

### Pattern 1: Invoke (Request-Response)
```typescript
// Renderer
const data = await window.electronAPI.fetchData(id);

// Main
ipcMain.handle('fetch-data', async (event, id) => {
  return await database.get(id);
});
```

### Pattern 2: Send/On (Fire-and-Forget)
```typescript
// Main → Renderer
mainWindow.webContents.send('notification', message);

// Renderer
window.electronAPI.onNotification((msg) => showToast(msg));
```

### Pattern 3: Two-Way Events
```typescript
// Renderer sends, awaits Main response
const result = await window.electronAPI.processFile(path);
```

## Packaging Configuration

### Electron Forge

```json
{
  "config": {
    "forge": {
      "packagerConfig": {
        "asar": true,
        "icon": "./assets/icon"
      },
      "makers": [
        { "name": "@electron-forge/maker-squirrel" },
        { "name": "@electron-forge/maker-dmg" },
        { "name": "@electron-forge/maker-deb" }
      ]
    }
  }
}
```

## Present Results to User

When providing Electron solutions:
- Always follow security best practices
- Provide complete IPC communication examples
- Consider cross-platform compatibility
- Include TypeScript types for the API
- Note Electron version differences

## Troubleshooting

**"require is not defined"**
- nodeIntegration is correctly disabled
- Use preload script with contextBridge

**"Cannot access window.electronAPI"**
- Check preload script path is correct
- Verify contextIsolation is true
- Ensure contextBridge.exposeInMainWorld is called

**"IPC message not received"**
- Verify channel names match exactly
- Check if handler is registered before window loads
- Use invoke for async responses
