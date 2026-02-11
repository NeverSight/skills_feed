---
name: playwright-cli
description: "Automates browser interactions for web testing, form filling, screenshots, and data extraction. Use when the user needs to navigate websites, interact with web pages, fill forms, take screenshots, test web applications, or extract information from web pages."
---

# Playwright CLI

A token-efficient CLI for browser automation. Use `Bash` tool to run these commands.

## Installation

```bash
npm install -g @playwright/cli@latest
```

## Core Workflow

```bash
# 1. Open a page
playwright-cli open https://example.com

# 2. Capture snapshot (accessibility tree with element refs)
playwright-cli snapshot

# 3. Interact using refs from snapshot
playwright-cli click e15
playwright-cli fill e20 "hello@example.com"

# 4. Re-snapshot to verify state
playwright-cli snapshot
```

## Command Reference

### Navigation & Core
| Command | Description |
|---------|-------------|
| `playwright-cli open <url>` | Open URL in browser |
| `playwright-cli open <url> --headed` | Open in visible browser |
| `playwright-cli close` | Close browser |
| `playwright-cli snapshot` | Capture accessibility tree with element refs |
| `playwright-cli screenshot [ref]` | Take screenshot (viewport or element) |
| `playwright-cli screenshot --full-page` | Full-page screenshot |
| `playwright-cli pdf` | Save page as PDF |

### Interactions
| Command | Description |
|---------|-------------|
| `playwright-cli click <ref>` | Click element |
| `playwright-cli fill <ref> "<text>"` | Fill input field |
| `playwright-cli type "<text>"` | Type text sequentially |
| `playwright-cli hover <ref>` | Hover over element |
| `playwright-cli select <ref> "<value>"` | Select dropdown option |
| `playwright-cli check <ref>` | Check checkbox |
| `playwright-cli uncheck <ref>` | Uncheck checkbox |
| `playwright-cli upload <ref> <file>` | Upload file |
| `playwright-cli drag <startRef> <endRef>` | Drag and drop |

### Keyboard & Mouse
| Command | Description |
|---------|-------------|
| `playwright-cli press <key>` | Press key (e.g., `Enter`, `ArrowDown`) |
| `playwright-cli keydown <key>` | Key down |
| `playwright-cli keyup <key>` | Key up |
| `playwright-cli mousemove <x> <y>` | Move mouse |
| `playwright-cli mousedown` | Mouse button down |
| `playwright-cli mouseup` | Mouse button up |

### Navigation
| Command | Description |
|---------|-------------|
| `playwright-cli go-back` | Go back |
| `playwright-cli go-forward` | Go forward |
| `playwright-cli reload` | Reload page |

### Tabs
| Command | Description |
|---------|-------------|
| `playwright-cli tab-list` | List tabs |
| `playwright-cli tab-new [url]` | Open new tab |
| `playwright-cli tab-close [index]` | Close tab |
| `playwright-cli tab-select <index>` | Switch to tab |

### DevTools
| Command | Description |
|---------|-------------|
| `playwright-cli console` | View console messages |
| `playwright-cli network` | View network requests |
| `playwright-cli eval "<js>"` | Execute JavaScript |
| `playwright-cli run-code "<js>"` | Run Playwright code |

### Dialogs
| Command | Description |
|---------|-------------|
| `playwright-cli dialog-accept` | Accept dialog |
| `playwright-cli dialog-dismiss` | Dismiss dialog |

### Tracing & Video
| Command | Description |
|---------|-------------|
| `playwright-cli tracing-start` | Start trace recording |
| `playwright-cli tracing-stop` | Stop trace recording |
| `playwright-cli video-start` | Start video recording |
| `playwright-cli video-stop` | Stop video recording |

### Sessions
| Command | Description |
|---------|-------------|
| `playwright-cli open <url> --session=<name>` | Use named session |
| `playwright-cli session-list` | List sessions |
| `playwright-cli session-stop <name>` | Stop session |
| `playwright-cli session-delete <name>` | Delete session |

## Snapshot Output

When you run `playwright-cli snapshot`, you get an accessibility tree:

```
- button "Create Strategy" [ref: e12]
- textbox "Search" [ref: e13]
- grid [ref: e14]
- button "Filters" [ref: e15]
```

Use the `ref` values (e.g., `e12`) to interact with elements.

## Configuration

Create `playwright-cli.json` for custom settings:

```json
{
  "browser": "chromium",
  "headless": false,
  "timeout": 30000
}
```
