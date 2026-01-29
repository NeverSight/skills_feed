---
name: terminal-streaming
description: xterm.js terminal integration for streaming agent output. Use when implementing AgentCard terminal display, configuring xterm addons, or handling real-time output streaming.
---

# Terminal Streaming

> Source: [xterm.js API](https://xtermjs.org/docs/api/terminal/interfaces/iterminaloptions/), [GitHub](https://github.com/xtermjs/xterm.js)

## Installation

```bash
npm install @xterm/xterm @xterm/addon-fit @xterm/addon-web-links
```

## Import & CSS

```typescript
import { Terminal } from '@xterm/xterm'
import { FitAddon } from '@xterm/addon-fit'
import { WebLinksAddon } from '@xterm/addon-web-links'
import '@xterm/xterm/css/xterm.css'
```

## Terminal Constructor

```typescript
const terminal = new Terminal(options?: ITerminalOptions)
```

### ITerminalOptions (Key Properties)

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `theme` | `ITheme` | - | Color theme |
| `fontSize` | `number` | `15` | Font size in pixels |
| `fontFamily` | `string` | `'monospace'` | Font family |
| `fontWeight` | `FontWeight` | `'normal'` | Normal text weight |
| `fontWeightBold` | `FontWeight` | `'bold'` | Bold text weight |
| `lineHeight` | `number` | `1.0` | Line height multiplier |
| `letterSpacing` | `number` | `0` | Pixel spacing between chars |
| `cursorBlink` | `boolean` | `false` | Enable cursor blinking |
| `cursorStyle` | `'block' \| 'underline' \| 'bar'` | `'block'` | Cursor style when focused |
| `cursorInactiveStyle` | `'outline' \| 'block' \| 'bar' \| 'underline' \| 'none'` | `'outline'` | Cursor when unfocused |
| `cursorWidth` | `number` | `1` | Bar cursor width in pixels |
| `scrollback` | `number` | `1000` | Lines retained above viewport |
| `scrollSensitivity` | `number` | `1` | Scroll speed multiplier |
| `fastScrollSensitivity` | `number` | `5` | Scroll speed with Alt key |
| `smoothScrollDuration` | `number` | `0` | Smooth scroll ms (0=instant) |
| `scrollOnUserInput` | `boolean` | `true` | Auto-scroll on input |
| `disableStdin` | `boolean` | `false` | Disable user input |
| `allowTransparency` | `boolean` | `false` | Allow transparent backgrounds |
| `tabStopWidth` | `number` | `8` | Tab stop size |
| `screenReaderMode` | `boolean` | `false` | Accessibility mode |
| `minimumContrastRatio` | `number` | `1` | Min color contrast (1-21) |
| `logLevel` | `LogLevel` | `'info'` | Logging verbosity |
| `allowProposedApi` | `boolean` | `false` | Enable experimental APIs |

### ITheme (Color Properties)

```typescript
interface ITheme {
  // Core colors
  foreground?: string      // Default text color
  background?: string      // Default background

  // Cursor
  cursor?: string          // Cursor color
  cursorAccent?: string    // Cursor text color (block cursor)

  // Selection
  selectionBackground?: string
  selectionForeground?: string
  selectionInactiveBackground?: string

  // Scrollbar
  scrollbarSliderBackground?: string
  scrollbarSliderHoverBackground?: string
  scrollbarSliderActiveBackground?: string

  // ANSI standard colors (0-7)
  black?: string           // \x1b[30m
  red?: string             // \x1b[31m
  green?: string           // \x1b[32m
  yellow?: string          // \x1b[33m
  blue?: string            // \x1b[34m
  magenta?: string         // \x1b[35m
  cyan?: string            // \x1b[36m
  white?: string           // \x1b[37m

  // ANSI bright colors (8-15)
  brightBlack?: string     // \x1b[1;30m
  brightRed?: string       // \x1b[1;31m
  brightGreen?: string     // \x1b[1;32m
  brightYellow?: string    // \x1b[1;33m
  brightBlue?: string      // \x1b[1;34m
  brightMagenta?: string   // \x1b[1;35m
  brightCyan?: string      // \x1b[1;36m
  brightWhite?: string     // \x1b[1;37m

  // Extended ANSI (16-255)
  extendedAnsi?: string[]
}
```

## Recommended Dark Theme

```typescript
const darkTheme: ITheme = {
  background: '#1e1e1e',
  foreground: '#d4d4d4',
  cursor: '#d4d4d4',
  cursorAccent: '#1e1e1e',
  selectionBackground: '#264f78',
  selectionForeground: '#ffffff',
  black: '#1e1e1e',
  red: '#f44747',
  green: '#6a9955',
  yellow: '#dcdcaa',
  blue: '#569cd6',
  magenta: '#c586c0',
  cyan: '#4ec9b0',
  white: '#d4d4d4',
  brightBlack: '#808080',
  brightRed: '#f44747',
  brightGreen: '#6a9955',
  brightYellow: '#dcdcaa',
  brightBlue: '#569cd6',
  brightMagenta: '#c586c0',
  brightCyan: '#4ec9b0',
  brightWhite: '#ffffff'
}
```

## Terminal Methods

### Core Methods

```typescript
// Attach to DOM (required before writing)
terminal.open(container: HTMLElement): void

// Write output (supports ANSI escape codes)
terminal.write(data: string | Uint8Array, callback?: () => void): void
terminal.writeln(data: string | Uint8Array, callback?: () => void): void

// Clear terminal
terminal.clear(): void          // Clear viewport + scrollback
terminal.reset(): void          // Full reset to initial state

// Scrolling
terminal.scrollToTop(): void
terminal.scrollToBottom(): void
terminal.scrollLines(amount: number): void
terminal.scrollPages(amount: number): void
terminal.scrollToLine(line: number): void

// Selection
terminal.select(column: number, row: number, length: number): void
terminal.selectAll(): void
terminal.selectLines(start: number, end: number): void
terminal.clearSelection(): void
terminal.getSelection(): string
terminal.hasSelection(): boolean

// Focus
terminal.focus(): void
terminal.blur(): void

// Cleanup (IMPORTANT: call on unmount)
terminal.dispose(): void

// Addon loading
terminal.loadAddon(addon: ITerminalAddon): void
```

### Properties

```typescript
terminal.cols: number           // Current column count
terminal.rows: number           // Current row count
terminal.buffer: IBuffer        // Access to terminal buffer
terminal.options: ITerminalOptions  // Current options (can modify)
terminal.element: HTMLElement | undefined  // Container element
terminal.textarea: HTMLTextAreaElement | undefined  // Input element
```

## Events

```typescript
// User input (for shell connection)
terminal.onData((data: string) => {
  // Send to process stdin
})

// Key press
terminal.onKey(({ key, domEvent }: { key: string; domEvent: KeyboardEvent }) => {
  // Handle key events
})

// Resize
terminal.onResize(({ cols, rows }: { cols: number; rows: number }) => {
  // Notify process of new size
})

// Title change (from escape sequence)
terminal.onTitleChange((title: string) => {
  // Update window title
})

// Selection change
terminal.onSelectionChange(() => {
  // Handle selection
})

// Scroll
terminal.onScroll((newPosition: number) => {
  // Handle scroll
})

// Cursor move
terminal.onCursorMove(() => {
  // Handle cursor position change
})

// Link hover (with WebLinksAddon)
terminal.onLineFeed(() => {
  // Line feed occurred
})
```

## FitAddon

Auto-resize terminal to fit container.

```typescript
import { FitAddon } from '@xterm/addon-fit'

const fitAddon = new FitAddon()
terminal.loadAddon(fitAddon)
terminal.open(container)

// Fit to container size
fitAddon.fit()

// Get proposed dimensions without applying
const dimensions = fitAddon.proposeDimensions()
// { cols: 80, rows: 24 }
```

## WebLinksAddon

Make URLs clickable.

```typescript
import { WebLinksAddon } from '@xterm/addon-web-links'

const webLinksAddon = new WebLinksAddon(
  (event: MouseEvent, uri: string) => {
    // Custom handler (optional)
    window.open(uri, '_blank')
  },
  {
    urlRegex: /https?:\/\/[^\s]+/,  // Custom regex (optional)
    hover: (event, uri, range) => { /* hover handler */ }
  }
)
terminal.loadAddon(webLinksAddon)
```

## Complete React Component

```typescript
import { useEffect, useRef, useCallback } from 'react'
import { Terminal } from '@xterm/xterm'
import { FitAddon } from '@xterm/addon-fit'
import { WebLinksAddon } from '@xterm/addon-web-links'
import '@xterm/xterm/css/xterm.css'

interface TerminalComponentProps {
  agentId: string
  onData?: (data: string) => void
}

export function TerminalComponent({ agentId, onData }: TerminalComponentProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const terminalRef = useRef<Terminal | null>(null)
  const fitAddonRef = useRef<FitAddon | null>(null)

  // Handle resize
  const handleResize = useCallback(() => {
    fitAddonRef.current?.fit()
  }, [])

  useEffect(() => {
    if (!containerRef.current) return

    // Create terminal
    const terminal = new Terminal({
      theme: {
        background: '#1e1e1e',
        foreground: '#d4d4d4',
        cursor: '#d4d4d4',
        selectionBackground: '#264f78'
      },
      fontSize: 12,
      fontFamily: 'Menlo, Monaco, "Courier New", monospace',
      cursorBlink: false,
      scrollback: 10000,
      disableStdin: true  // Read-only for agent output
    })

    // Load addons
    const fitAddon = new FitAddon()
    const webLinksAddon = new WebLinksAddon()
    terminal.loadAddon(fitAddon)
    terminal.loadAddon(webLinksAddon)

    // Open and fit
    terminal.open(containerRef.current)
    fitAddon.fit()

    // Store refs
    terminalRef.current = terminal
    fitAddonRef.current = fitAddon

    // Handle user input if enabled
    if (onData) {
      terminal.onData(onData)
    }

    // Listen for agent output via IPC
    const handleOutput = (data: { agentId: string; chunk: string }) => {
      if (data.agentId === agentId) {
        terminal.write(data.chunk)
      }
    }
    const unsubscribe = window.api?.onAgentOutput?.(handleOutput)

    // Window resize handler
    window.addEventListener('resize', handleResize)

    // Cleanup
    return () => {
      window.removeEventListener('resize', handleResize)
      unsubscribe?.()
      terminal.dispose()
    }
  }, [agentId, onData, handleResize])

  // Expose write method
  const write = useCallback((data: string) => {
    terminalRef.current?.write(data)
  }, [])

  // Expose clear method
  const clear = useCallback(() => {
    terminalRef.current?.clear()
  }, [])

  return (
    <div
      ref={containerRef}
      className="h-full w-full"
      style={{ backgroundColor: '#1e1e1e' }}
    />
  )
}
```

## Grid Layout (2x2)

```tsx
<div className="grid grid-cols-2 grid-rows-2 h-screen gap-1 p-1 bg-neutral-900">
  {agents.map(agent => (
    <div key={agent.id} className="relative bg-neutral-800 rounded overflow-hidden">
      {/* Header */}
      <div className="absolute top-0 left-0 right-0 z-10 px-2 py-1 bg-neutral-800/90 flex items-center justify-between">
        <span className="text-sm text-neutral-300">{agent.label}</span>
        <StatusBadge status={agent.status} />
      </div>

      {/* Terminal */}
      <div className="absolute inset-0 pt-8">
        <TerminalComponent agentId={agent.id} />
      </div>
    </div>
  ))}
</div>
```

## Output Buffering

Buffer output to prevent IPC flooding (100ms intervals):

```typescript
class OutputBuffer {
  private buffer = ''
  private timer: NodeJS.Timeout | null = null
  private readonly flushInterval = 100

  constructor(private onFlush: (data: string) => void) {}

  append(chunk: string): void {
    this.buffer += chunk

    if (!this.timer) {
      this.timer = setTimeout(() => this.flush(), this.flushInterval)
    }
  }

  flush(): void {
    if (this.buffer) {
      this.onFlush(this.buffer)
      this.buffer = ''
    }
    if (this.timer) {
      clearTimeout(this.timer)
      this.timer = null
    }
  }
}

// Usage in IPC handler
const buffer = new OutputBuffer((data) => {
  mainWindow.webContents.send('agent-output', { agentId, chunk: data })
})

// From sandbox stdout
sandbox.process.getSessionCommandLogs(session, cmdId,
  (stdout) => buffer.append(stdout),
  (stderr) => buffer.append(stderr)
)
```

## Memory Management

```typescript
// Clear scrollback periodically if needed
if (terminal.buffer.active.length > 10000) {
  terminal.clear()
  terminal.write('[Scrollback cleared]\r\n')
}

// Always dispose on unmount
useEffect(() => {
  return () => {
    terminal.dispose()
  }
}, [])

// Remove IPC listeners
useEffect(() => {
  const unsubscribe = window.api.onAgentOutput(handler)
  return () => unsubscribe()
}, [])
```

## ResizeObserver Pattern (Current Implementation)

MVP uses ResizeObserver for container-aware resizing:

```typescript
useEffect(() => {
  const observer = new ResizeObserver(() => {
    if (fitAddonRef.current) {
      fitAddonRef.current.fit()
    }
  })

  if (containerRef.current) {
    observer.observe(containerRef.current)
  }

  return () => observer.disconnect()
}, [])
```

## Line Ending Normalization

xterm.js needs `\r\n` for proper line breaks:

```typescript
const normalized = data.chunk.replace(/\r?\n/g, '\r\n')
terminal.write(normalized)
```

## Performance Target

- **Latency**: < 500ms from sandbox stdout to terminal display
- **Buffer interval**: 100ms batching
- **Scrollback**: 10000 lines max
- **Resize debounce**: Consider debouncing fit() calls during rapid resize
