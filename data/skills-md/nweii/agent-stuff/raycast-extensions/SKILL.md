---
name: raycast-extensions
description: "Build Raycast extensions using React and Node.js. Use for creating commands, UI components (List, Form, Grid), hooks (useFetch), AI integration, and manifest configuration."
metadata:
  author: nweii
  version: "1.0.0"
---

# Raycast Extension Development

Build Raycast extensions using React, TypeScript, and Node.js.

## Quick Start

1. **Create extension**: Run "Create Extension" command in Raycast
2. **Install & develop**: `npm install && npm run dev`
3. **Edit**: Modify `src/index.tsx`, changes hot-reload automatically
4. **Test**: Extension appears at top of Raycast root search

## Choosing a UI Primitive

| Need | Component |
|------|-----------|
| Searchable list of items | `List` |
| Image gallery/grid | `Grid` |
| User input collection | `Form` |
| Rich content display | `Detail` |
| Status bar presence | `MenuBarExtra` |

### Decision Tree

1. **Displaying items the user searches/filters?**
   - Text-focused → `List`
   - Image-focused → `Grid`

2. **Collecting user input?** → `Form`

3. **Showing detailed content?** → `Detail` (supports markdown + metadata)

4. **Always-visible status bar?** → `MenuBarExtra`

## Core Patterns

### List with ActionPanel

```tsx
import { ActionPanel, Action, List } from "@raycast/api";

export default function Command() {
  return (
    <List>
      <List.Item
        title="Item"
        actions={
          <ActionPanel>
            <Action.CopyToClipboard content="Copied!" />
            <Action.OpenInBrowser url="https://raycast.com" />
          </ActionPanel>
        }
      />
    </List>
  );
}
```

### Data Fetching

```tsx
import { List } from "@raycast/api";
import { useFetch } from "@raycast/utils";

export default function Command() {
  const { data, isLoading } = useFetch<Item[]>("https://api.example.com/items");
  
  return (
    <List isLoading={isLoading}>
      {data?.map((item) => <List.Item key={item.id} title={item.name} />)}
    </List>
  );
}
```

### AI Integration

```tsx
import { AI, Clipboard } from "@raycast/api";

export default async function Command() {
  const answer = await AI.ask("Summarize this text");
  await Clipboard.copy(answer);
}
```

> [!NOTE]
> AI requires Raycast Pro. Check access with `environment.canAccess(AI)`.

## References

For detailed documentation, see:

- **UI Components**: [references/ui-components.md](references/ui-components.md) - List, Detail, Form, Grid, ActionPanel, MenuBarExtra
- **Hooks & Utilities**: [references/hooks-utilities.md](references/hooks-utilities.md) - useFetch, LocalStorage, Clipboard, OAuth, runAppleScript
- **AI API**: [references/ai-api.md](references/ai-api.md) - AI.ask, useAI, model selection, streaming
- **Package Structure**: [references/package-structure.md](references/package-structure.md) - manifest, commands, preferences

## Examples

Runnable examples in `examples/`:

| File | Pattern |
|------|---------|
| `list-with-actions.tsx` | List + ActionPanel basics |
| `list-with-detail.tsx` | List with detail panel |
| `form-with-validation.tsx` | Form + useForm validation |
| `detail-with-metadata.tsx` | Detail markdown + metadata |
| `grid-with-images.tsx` | Grid layout |
| `data-fetching.tsx` | useFetch patterns |
| `ai-integration.tsx` | AI.ask with streaming |
| `menubar-extra.tsx` | MenuBarExtra interactions |
