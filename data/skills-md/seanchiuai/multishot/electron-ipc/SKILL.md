---
name: electron-ipc
description: Electron IPC communication patterns between main and renderer processes. Use when implementing IPC handlers, sending events between processes, or working with the preload script.
---

# Electron IPC & UI (MVP)

## Files

- `src/main/index.ts` - Main process, BrowserWindow config
- `src/main/ipc.ts` - IPC handlers
- `src/preload/index.ts` - Context bridge API
- `src/renderer/styles.css` - Global styles (Tailwind + custom)
- `src/renderer/components/` - React UI components

---

## Preload API (window.api)

```typescript
interface API {
  // Invoke handlers (renderer → main)
  startRun(prompt: string, credentials: Credentials): Promise<void>
  selectWinner(agentId: string): Promise<void>
  cancelRun(): Promise<void>
  previewAll(): Promise<PreviewResult[]>

  // Event listeners (main → renderer)
  onAgentOutput(cb: (data: { agentId: string; chunk: string }) => void): () => void
  onAgentStatus(cb: (data: { agentId: string; status: AgentStatus }) => void): () => void
  onError(cb: (error: string) => void): () => void
}

interface Credentials {
  daytonaApiKey: string
  claudeOAuthToken?: string
  anthropicApiKey?: string
}

interface PreviewResult {
  agentId: string
  url: string | null
  error?: string
}

type AgentStatus = 'idle' | 'running' | 'completed' | 'failed'
```

---

## IPC Communication

### Main → Renderer Events

```typescript
sendToRenderer('agent-output', { agentId, chunk })  // Terminal data
sendToRenderer('agent-status', { agentId, status }) // Status change
sendToRenderer('error', errorMessage)               // Error string
```

### Renderer → Main Handlers

```typescript
ipcMain.handle('start-run', async (_event, { prompt, credentials }) => { ... })
ipcMain.handle('select-winner', async (_event, { agentId }) => { ... })
ipcMain.handle('cancel-run', async () => { ... })
ipcMain.handle('preview-all', async () => { ... })
```

### Output Buffering

```typescript
const buffer = new OutputBuffer((agentId, data) => {
  sendToRenderer('agent-output', { agentId, chunk: data })
})

buffer.append(agentId, chunk)  // Add to buffer
buffer.flush(agentId)          // Force flush
buffer.flushAll()              // Flush all agents
```

---

## BrowserWindow Configuration

Current config in `src/main/index.ts`:

```typescript
const mainWindow = new BrowserWindow({
  width: 1400,
  height: 900,
  minWidth: 1000,
  minHeight: 700,
  show: false,
  autoHideMenuBar: true,
  backgroundColor: '#171717',
  webPreferences: {
    preload: join(__dirname, '../preload/index.js'),
    sandbox: false,
    contextIsolation: true,
    nodeIntegration: false
  }
})
```

---

## UI Beautification Options

### Custom Title Bar (Frameless Window)

```typescript
// Hidden title bar with traffic lights (macOS)
const win = new BrowserWindow({
  titleBarStyle: 'hidden',
  trafficLightPosition: { x: 15, y: 15 }
})

// Hidden with custom overlay (cross-platform)
const win = new BrowserWindow({
  titleBarStyle: 'hidden',
  titleBarOverlay: {
    color: '#171717',
    symbolColor: '#ffffff',
    height: 40
  }
})

// Custom traffic light behavior (macOS)
const win = new BrowserWindow({
  titleBarStyle: 'hiddenInset'  // Inset traffic lights
})
const win = new BrowserWindow({
  titleBarStyle: 'customButtonsOnHover'  // Show on hover only
})
```

### Platform Vibrancy Effects

```typescript
// macOS Vibrancy
win.setVibrancy('sidebar')  // Options: titlebar, sidebar, window, hud, etc.
win.setVibrancy('under-window')  // Translucent background

// Windows 11 Mica/Acrylic (22H2+)
const win = new BrowserWindow({
  backgroundColor: '#00000000',  // Transparent for effects
  // ...
})
win.setBackgroundMaterial('mica')    // Long-lived windows
win.setBackgroundMaterial('acrylic') // Transient/popup windows
```

### Transparent Window

```typescript
const win = new BrowserWindow({
  frame: false,
  transparent: true,
  resizable: false,  // Required when transparent
  backgroundColor: '#00000000'
})
```

### Window Controls Overlay API

Exposes native controls area to web content:

```typescript
const win = new BrowserWindow({
  titleBarStyle: 'hidden',
  titleBarOverlay: true  // Enable CSS env() variables
})
```

In CSS, use safe area insets:

```css
.titlebar {
  padding-top: env(titlebar-area-y, 0);
  padding-left: env(titlebar-area-x, 0);
  height: env(titlebar-area-height, 40px);
}

/* Draggable region */
.drag-region {
  -webkit-app-region: drag;
}

.no-drag {
  -webkit-app-region: no-drag;
}
```

---

## Tailwind CSS Patterns

Current setup uses Tailwind with dark theme. Key patterns:

### Color Palette (neutral-based)

```css
bg-neutral-900  /* Main background #171717 */
bg-neutral-800  /* Cards, inputs */
bg-neutral-700  /* Borders, dividers */
text-neutral-100  /* Primary text */
text-neutral-400  /* Secondary text */
text-neutral-500  /* Muted text, placeholders */
```

### Status Colors

```css
/* Running */
bg-yellow-500/20 text-yellow-400 animate-pulse

/* Completed */
bg-green-500/20 text-green-400

/* Failed */
bg-red-500/20 text-red-400

/* Winner highlight */
border-green-500 bg-green-500/5
```

### Interactive Elements

```css
/* Buttons - Primary */
bg-blue-600 hover:bg-blue-500 disabled:bg-neutral-700

/* Buttons - Danger */
bg-red-600/20 text-red-400 hover:bg-red-600/30

/* Inputs */
bg-neutral-800 border-neutral-700 focus:ring-2 focus:ring-blue-500

/* Cards */
rounded-lg border border-neutral-700 bg-neutral-800
```

### Useful Effects for Beautification

```css
/* Glassmorphism */
backdrop-blur-md bg-white/10

/* Subtle gradients */
bg-gradient-to-br from-neutral-800 to-neutral-900

/* Glow effects */
shadow-lg shadow-blue-500/20

/* Smooth transitions */
transition-all duration-200

/* Hover lift */
hover:-translate-y-0.5 hover:shadow-lg
```

---

## xterm.js Theme

Current terminal theme in `Terminal.tsx`:

```typescript
const terminal = new XTerm({
  theme: {
    background: '#1e1e1e',
    foreground: '#d4d4d4',
    cursor: '#d4d4d4',
    selectionBackground: '#264f78',
    black: '#1e1e1e',
    red: '#f44747',
    green: '#6a9955',
    yellow: '#dcdcaa',
    blue: '#569cd6',
    magenta: '#c586c0',
    cyan: '#4ec9b0',
    white: '#d4d4d4'
  },
  fontSize: 12,
  fontFamily: 'Menlo, Monaco, "Courier New", monospace',
  scrollback: 10000,
  cursorBlink: false,
  disableStdin: true
})
```

Alternative themes to consider:

```typescript
// Dracula
theme: {
  background: '#282a36',
  foreground: '#f8f8f2',
  cursor: '#f8f8f2',
  red: '#ff5555',
  green: '#50fa7b',
  yellow: '#f1fa8c',
  blue: '#bd93f9',
  magenta: '#ff79c6',
  cyan: '#8be9fd'
}

// One Dark
theme: {
  background: '#282c34',
  foreground: '#abb2bf',
  cursor: '#528bff',
  red: '#e06c75',
  green: '#98c379',
  yellow: '#e5c07b',
  blue: '#61afef',
  magenta: '#c678dd',
  cyan: '#56b6c2'
}
```

---

## Component Architecture

```
App.tsx                    # State: phase, credentials, agents, winner
├── SetupWizard.tsx        # Credentials input form
└── GridView.tsx           # Header bar + 2x2 grid
    └── AgentCard.tsx      # Card with status badge + terminal
        └── Terminal.tsx   # xterm.js instance
```

### App Phases

1. `setup` - Show SetupWizard
2. `ready` - Show prompt input + idle grid
3. `running` - Agents executing, cancel available
4. `completed` - All done, select winner

---

## Cleanup

Always return unsubscribe function and call on unmount to prevent memory leaks:

```typescript
useEffect(() => {
  const unsub = window.api.onAgentOutput(({ agentId, chunk }) => {
    terminals[agentId].write(chunk)
  })
  return () => unsub()
}, [])
```
