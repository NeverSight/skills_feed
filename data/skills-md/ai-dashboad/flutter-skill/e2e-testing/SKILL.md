---
name: e2e-testing
description: AI-powered E2E testing for any app — Flutter, React Native, iOS, Android, Electron, Tauri, KMP, .NET MAUI. Test 8 platforms with natural language through MCP. No test code needed. Just describe what to test and the agent sees screenshots, taps elements, enters text, scrolls, and verifies UI state automatically.
version: 0.8.3
---

# AI E2E Testing — 8 Platforms, Zero Test Code

> Give your AI agent eyes and hands inside any running app.

flutter-skill is an MCP server that connects AI agents to running apps. The agent can see screenshots, tap elements, enter text, scroll, navigate, inspect UI trees, and verify state — all through natural language.

## Supported Platforms

| Platform | Setup |
|----------|-------|
| Flutter (iOS/Android/Web) | `flutter pub add flutter_skill` |
| React Native | `npm install flutter-skill-react-native` |
| Electron | `npm install flutter-skill-electron` |
| iOS (Swift/UIKit) | SPM: `FlutterSkillSDK` |
| Android (Kotlin) | Gradle: `flutter-skill-android` |
| Tauri (Rust) | `cargo add flutter-skill-tauri` |
| KMP Desktop | Gradle dependency |
| .NET MAUI | NuGet package |

**Test scorecard: 562/567 (99.1%) across all 8 platforms.**

## Install

```bash
# npm (recommended)
npm install -g flutter-skill

# Homebrew
brew install ai-dashboad/flutter-skill/flutter-skill

# Or download binary from GitHub Releases
```

## MCP Configuration

Add to your AI agent's MCP config (Claude Desktop, Cursor, Windsurf, OpenClaw, etc.):

```json
{
  "mcpServers": {
    "flutter-skill": {
      "command": "flutter-skill",
      "args": ["server"]
    }
  }
}
```

### OpenClaw

If using OpenClaw, add to your gateway config under `mcp.servers`:

```yaml
mcp:
  servers:
    flutter-skill:
      command: flutter-skill
      args: ["server"]
```

## Quick Start

### 1. Initialize your app (one-time)

```bash
cd /path/to/your/app
flutter-skill init
```

Auto-detects project type and patches your app with the testing bridge.

### 2. Launch and connect

```bash
flutter-skill launch .
```

### 3. Test with natural language

Tell the agent what to test:

> "Test the login flow — enter admin@test.com and password123, tap Login, verify Dashboard appears"

The agent will automatically:
1. `screenshot()` → see the current screen
2. `inspect_interactive()` → discover all tappable/typeable elements with semantic refs
3. `tap(ref: "button:Login")` → tap using stable semantic reference
4. `enter_text(ref: "input:Email", text: "admin@test.com")` → type into field
5. `wait_for_element(key: "Dashboard")` → verify navigation
6. `screenshot()` → confirm final state

## Available MCP Tools

### Core Actions
| Tool | Description |
|------|-------------|
| `screenshot` | Capture current screen as image |
| `tap` | Tap element by key, text, ref, or coordinates |
| `enter_text` | Type text into a field |
| `scroll` | Scroll up/down/left/right |
| `swipe` | Swipe gesture between points |
| `long_press` | Long press an element |
| `drag` | Drag from point A to B |
| `go_back` | Navigate back |
| `press_key` | Send keyboard key events |

### Inspection (v0.8.0+)
| Tool | Description |
|------|-------------|
| `inspect_interactive` | **NEW** — Get all interactive elements with semantic ref IDs |
| `get_elements` | List all elements on screen |
| `find_element` | Find element by key or text |
| `wait_for_element` | Wait for element to appear (with timeout) |
| `get_element_properties` | Get detailed properties of an element |

### Text Manipulation
| Tool | Description |
|------|-------------|
| `set_text` | Replace text in a field |
| `clear_text` | Clear a text field |
| `get_text` | Read text content |

### App Control
| Tool | Description |
|------|-------------|
| `get_logs` | Read app logs |
| `clear_logs` | Clear log buffer |

## Semantic Refs (v0.8.0)

`inspect_interactive` returns elements with stable semantic reference IDs:

```
button:Login          → Login button
input:Email           → Email text field
toggle:Dark Mode      → Dark mode switch
button:Submit[1]      → Second Submit button (disambiguated)
```

Format: `{role}:{content}[{index}]`

7 roles: `button`, `input`, `toggle`, `slider`, `select`, `link`, `item`

Use refs for reliable element targeting that survives UI changes:
```
tap(ref: "button:Login")
enter_text(ref: "input:Email", text: "test@example.com")
```

## Testing Workflow

### Basic Flow
```
screenshot() → inspect_interactive() → tap/enter_text → screenshot() → verify
```

### Comprehensive Testing
> "Explore every screen of this app. Test all buttons, forms, navigation, and edge cases. Report any bugs you find."

The agent will systematically:
- Navigate every screen via tab bars, menus, links
- Interact with every interactive element
- Test form validation (empty, invalid, valid inputs)
- Test edge cases (long text, special characters, emoji)
- Verify navigation flows (forward, back, deep links)
- Take screenshots at each step for verification

### Example Prompts

**Quick smoke test:**
> "Tap every tab and screenshot each page"

**Form testing:**
> "Fill the registration form with edge case data — emoji name, very long email, short password — and verify error messages"

**Navigation:**
> "Test the complete user journey: sign up → create post → like → comment → delete → sign out"

**Accessibility:**
> "Check every screen for missing labels, small tap targets, and contrast issues"

## Tips

1. **Always start with `screenshot()`** — see before you act
2. **Use `inspect_interactive()` to discover elements** — don't guess at selectors
3. **Prefer `ref:` selectors** — more stable than text or coordinates
4. **`wait_for_element()` after navigation** — apps need time to transition
5. **Screenshot after every action** — verify the expected effect
6. **Use `press_key` for keyboard shortcuts** — test keyboard navigation

## Links

- [GitHub](https://github.com/ai-dashboad/flutter-skill)
- [npm](https://www.npmjs.com/package/flutter-skill)
- [Documentation](https://github.com/ai-dashboad/flutter-skill/blob/main/docs/USAGE_GUIDE.md)
- [Demo Video](https://github.com/user-attachments/assets/d4617c73-043f-424c-9a9a-1a61d4c2d3c6)
- [pub.dev](https://pub.dev/packages/flutter_skill)
- [VSCode Extension](https://marketplace.visualstudio.com/items?itemName=AIDashboard.flutter-skill)
