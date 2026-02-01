---
name: ts-tui-game-skill
description: Build beautiful, performant TUI applications and games with TypeScript and blessed. Provides patterns, templates, and best practices for terminal interfaces.
---

# TS TUI Game Skill

Build beautiful, performant TUI applications and games with TypeScript and blessed.

## Triggers

Use this skill when:
- Creating a new TUI application or game
- Building terminal-based interfaces with blessed
- Implementing game loops, render schedulers, or input handling in terminals
- Designing layouts for terminal applications
- Working with blessed widgets (Box, List, Form, etc.)
- Optimizing terminal rendering performance
- Adding keyboard and mouse input handling
- Creating modals, panels, or complex UI compositions

Keywords: tui, terminal, blessed, ncurses, console, cli game, terminal game, terminal ui, text interface

## Core Instructions

When helping with blessed TUI development, follow these principles:

### Project Setup

1. **Always use TypeScript with strict mode**
2. **Recommended screen options:**
   ```typescript
   const screen = blessed.screen({
     smartCSR: true,      // Efficient change-scroll-region rendering
     autoPadding: true,   // Automatic border/padding handling
     fullUnicode: true,   // Support for box drawing and unicode
     warnings: true,      // Development warnings
   });
   ```

3. **Directory structure** - Separate game logic from UI:
   ```
   src/
     main.ts              # Entrypoint, screen init, lifecycle
     ui/
       app.ts             # Root composition, layout creation
       theme.ts           # Centralized theme tokens
       widgets/           # Custom widgets
       panels/            # Composed windows
       input/
         keymap.ts        # Key binding definitions
         input-router.ts  # Focus-aware dispatch
     game/
       state.ts           # Authoritative state types
       reducer.ts         # Pure state updates
       systems/           # Simulation systems
     engine/
       scheduler.ts       # Tick + render scheduling
       events.ts          # Event bus
   ```

### Rendering Rules

**CRITICAL: Never call `screen.render()` directly from event handlers.**

Use a render scheduler pattern:
```typescript
export function createRenderScheduler(screen: blessed.Widgets.Screen, maxFps = 30) {
  let pending = false;
  const frameMs = Math.floor(1000 / maxFps);

  const timer = setInterval(() => {
    if (!pending) return;
    pending = false;
    screen.render();
  }, frameMs);

  return {
    requestRender() { pending = true; },
    stop() { clearInterval(timer); }
  };
}
```

### State Management

1. **Single authoritative state** - One state object owned by game core
2. **Pure reducers** - Actions in, state out, no side effects
3. **UI dispatches actions** - Never mutate state directly from widgets

### Layout Guidelines

**Standard 3-pane game layout:**
- Main viewport: map/scene (largest, fluid)
- Right sidebar: stats, inventory (24-32 cols fixed)
- Bottom log: messages, hints (7-12 rows fixed)

```typescript
const sidebarWidth = 30;
const logHeight = 9;

const main = blessed.box({
  parent: screen,
  top: 0, left: 0,
  width: `100%-${sidebarWidth}`,
  height: `100%-${logHeight}`,
  border: 'line',
});
```

### Theme System

Centralize all colors and styles:
```typescript
export const theme = {
  fg: 'white',
  bg: 'black',
  panel: { fg: 'white', bg: 'black', border: { fg: '#888888' } },
  accent: { fg: 'black', bg: '#f4d03f' },
  danger: { fg: 'white', bg: 'red' },
  muted: { fg: '#aaaaaa', bg: 'black' },
};
```

**Rule:** Pick 1 accent color and 1 danger color. Everything else muted.

### Input Handling

Implement a router pattern for context-aware input:
```typescript
function onKey(ch: string, key: blessed.Widgets.Events.IKeyEventArg) {
  const name = key.full || ch;

  if (globalKeys[name]) return globalKeys[name]();
  if (state.ui.modal) return modalHandler(ch, key);
  if (state.ui.activePanel === 'map') return mapHandler(ch, key);
}
screen.on('keypress', onKey);
```

**Standard controls:**
- Movement: arrows + hjkl
- Help: `?`
- Cycle focus: `tab`
- Confirm: `enter`
- Back/close: `esc`
- Quit: `q` or `C-c`

### Performance Rules

**Hard rules:**
- Never `screen.render()` in tight loops
- Never rebuild widget trees every frame
- Never create new elements every tick without destroying them

**Soft rules:**
- Update content/styles on existing elements
- One `setContent()` per frame for large viewports
- Keep tag parsing minimal in grid renders
- Use `alwaysScroll` only where necessary

### Modal Pattern

1. Create semi-transparent overlay covering screen
2. Create centered modal box on top
3. Capture input in modal
4. On close: `destroy()` both, restore focus

### Cleanup (REQUIRED)

```typescript
function safeExit(screen: blessed.Widgets.Screen, code = 0) {
  try {
    screen.destroy();
  } finally {
    process.exit(code);
  }
}

screen.key(['escape', 'q', 'C-c'], () => safeExit(screen));
```

## Resources

See the `resources/` directory for:
- [Style Guide](resources/style-guide.md) - Comprehensive development guidelines
- [Widget Reference](resources/widget-reference.md) - Blessed widget API quick reference

See the `templates/` directory for starter code.

## Best Practices Checklist

When reviewing or creating blessed TUI code, verify:

- [ ] One render scheduler controls `screen.render()`
- [ ] Game core is pure and testable (no terminal dependency)
- [ ] Layout uses stable proportions and resize behavior
- [ ] Theme tokens are centralized
- [ ] Controls are discoverable (`?` help, footer hints)
- [ ] Modals capture input and restore focus
- [ ] No per-tick widget creation
- [ ] Exit path calls `screen.destroy()` and clears timers
- [ ] Tags used sparingly in large grid renders
- [ ] Keyboard-first design (mouse is bonus)
