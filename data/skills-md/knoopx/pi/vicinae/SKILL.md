---
name: vicinae
description: Builds Vicinae launcher extensions with TypeScript and React, defines commands, and creates List/Form/Detail views. Use when creating new extensions and implementing view/no-view commands.
---

# Vicinae Extensions

Extensions for Vicinae launcher using TypeScript and React.

## Contents

- [Core Concepts](#core-concepts)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Command Types](#command-types)
- [Development Workflow](#development-workflow)
- Advanced: [UX Patterns](./references/ux-patterns.md)
- Advanced: [API Reference](./references/api-reference.md)
- Advanced: [Keyboard Shortcuts](./references/shortcuts.md)

## Core Concepts

| Concept             | Description                                    |
| ------------------- | ---------------------------------------------- |
| **Extension**       | Package adding commands to the launcher        |
| **View Command**    | Displays React UI (`mode: "view"`)             |
| **No-View Command** | Executes action without UI (`mode: "no-view"`) |
| **Manifest**        | `package.json` with extension metadata         |

## Quick Start

**Recommended**: Use Vicinae's built-in "Create Extension" command.

**Manual**:

```bash
mkdir my-extension && cd my-extension
npm init -y
npm install @vicinae/api typescript @types/react @types/node
mkdir src && touch src/command.tsx
```

## Project Structure

```
my-extension/
├── package.json          # Manifest with commands
├── tsconfig.json
├── src/
│   ├── command.tsx       # View commands
│   └── action.ts         # No-view commands
└── assets/               # Icons
```

## Manifest (package.json)

```json
{
  "name": "my-extension",
  "title": "My Extension",
  "version": "1.0.0",
  "commands": [
    {
      "name": "my-command",
      "title": "My Command",
      "description": "What this command does",
      "mode": "view"
    }
  ],
  "dependencies": {
    "@vicinae/api": "^0.8.2"
  }
}
```

## Command Types

### View Command (src/command.tsx)

```tsx
import { List, ActionPanel, Action, Icon } from "@vicinae/api";

export default function MyCommand() {
  return (
    <List searchBarPlaceholder="Search items...">
      <List.Item
        title="Item"
        icon={Icon.Document}
        actions={
          <ActionPanel>
            <Action
              icon={Icon.Eye}
              title="View"
              onAction={() => console.log("viewed")}
            />
          </ActionPanel>
        }
      />
    </List>
  );
}
```

**Important**: All actions must have an `icon` prop.

### No-View Command (src/action.ts)

```typescript
import { showToast } from "@vicinae/api";

export default async function QuickAction() {
  await showToast({ title: "Done!" });
}
```

## Development Workflow

```bash
npm run build         # Production build
npx tsc --noEmit      # Type check

# Run Vicinae dev server in tmux
# Creates the session only if it does not exist
tmux has -t vicinae-dev || tmux new-session -d -s vicinae-dev 'bunx vici develop'

# Read logs
tmux capture-pane -t vicinae-dev -p -S -
```

## Common APIs

```typescript
import {
  // UI Components
  List,
  Detail,
  Form,
  Grid,
  ActionPanel,
  Action,
  Icon,
  Color,
  // Utilities
  showToast,
  Toast,
  Clipboard,
  open,
  closeMainWindow,
  getPreferenceValues,
  useNavigation,
} from "@vicinae/api";
```

## Keyboard Shortcuts

Use `Ctrl` for common actions, `Shift+Delete` for destructive:

| Shortcut       | Action  |
| -------------- | ------- |
| `Ctrl+R`       | Refresh |
| `Shift+Delete` | Delete  |
| `Ctrl+N`       | New     |
| `Ctrl+E`       | Edit    |

```tsx
<Action
  title="Refresh"
  icon={Icon.RotateClockwise}
  shortcut={{ modifiers: ["ctrl"], key: "r" }}
  onAction={handleRefresh}
/>

<Action
  title="Delete"
  icon={Icon.Trash}
  style={Action.Style.Destructive}
  shortcut={{ modifiers: ["shift"], key: "delete" }}
  onAction={handleDelete}
/>
```

See [Keyboard Shortcuts](./references/shortcuts.md) for full reference.

## Navigation

```tsx
function ListView() {
  const { push, pop } = useNavigation();

  return (
    <List.Item
      title="Go to Detail"
      icon={Icon.Document}
      actions={
        <ActionPanel>
          <Action
            icon={Icon.Eye}
            title="View"
            onAction={() => push(<DetailView />)}
          />
        </ActionPanel>
      }
    />
  );
}
```

## Preferences

Define in manifest:

```json
{
  "preferences": [
    {
      "name": "apiKey",
      "title": "API Key",
      "type": "password",
      "required": true
    }
  ]
}
```

Access in code:

```typescript
const { apiKey } = getPreferenceValues();
```

## Related Skills

- **typescript**: Type safety for extensions
