---
name: moldable
description: Complete guide for building Moldable apps. Use this skill when creating new apps with scaffoldApp, modifying existing apps, implementing workspace-aware storage, integrating with the Moldable desktop via postMessage APIs (moldable:show-in-folder, moldable:set-chat-input, moldable:set-chat-instructions, moldable:save-file), configuring workspaces, managing skills/MCPs, or troubleshooting app issues. Essential for any Moldable app development task.
---

# Moldable App Development

This skill provides comprehensive knowledge for building and modifying apps within the Moldable desktop application.

## Quick Reference

| Resource | Path |
|----------|------|
| App source code | `~/.moldable/shared/apps/{app-id}/` |
| App runtime data | `~/.moldable/workspaces/{workspace-id}/apps/{app-id}/data/` |
| Workspace config | `~/.moldable/workspaces/{workspace-id}/config.json` |
| MCP config | `~/.moldable/shared/config/mcp.json` |
| Skills | `~/.moldable/shared/skills/{repo}/{skill}/` |
| Environment | `~/.moldable/shared/.env` |

## Default Tech Stack

- **Framework**: Next.js 16 + React 19 + TypeScript
- **Styling**: Tailwind CSS 4 + shadcn/ui (semantic colors only)
- **State**: TanStack Query v5
- **Storage**: Filesystem via `@moldable-ai/storage`
- **Package Manager**: pnpm

## Creating Apps

**ALWAYS use the `scaffoldApp` tool** — never create app files manually.

```typescript
scaffoldApp({
  appId: "expense-tracker",   // lowercase, hyphens only
  name: "Expense Tracker",    // Display name
  icon: "💰",                 // Emoji icon
  description: "Track expenses and generate reports",
  widgetSize: "medium",       // small, medium, or large
  extraDependencies: {        // Optional npm packages
    "zod": "^3.0.0"
  }
})
```

**After scaffolding**, customize:
- `src/app/page.tsx` — Main app view
- `src/app/widget/page.tsx` — Widget view
- `src/app/api/` — API routes
- `src/components/` — React components

## Detailed References

Read these for in-depth guidance:

### Core Concepts
- [references/app-lifecycle.md](references/app-lifecycle.md) — Creating, starting, managing, and deleting apps
- [references/app-scaffold.md](references/app-scaffold.md) — **Required files**, lint rules, templates for new apps
- [references/workspaces.md](references/workspaces.md) — Workspace system, data isolation, environment layering
- [references/configuration.md](references/configuration.md) — moldable.json, config.json, environment variables

### Implementation Patterns
- [references/ui.md](references/ui.md) — **@moldable-ai/ui components**, shadcn/ui, themes, rich text editor
- [references/storage-patterns.md](references/storage-patterns.md) — Filesystem storage, React Query, workspace-aware APIs
- [references/desktop-apis.md](references/desktop-apis.md) — postMessage APIs (open-url, show-in-folder, set-chat-input, save-file)
- [references/skills-mcps.md](references/skills-mcps.md) — Skills library, MCP configuration, custom MCP servers

## Essential Patterns

### 1. UI Components (@moldable-ai/ui)

**Always use `@moldable-ai/ui`** for all UI work. It includes shadcn/ui components, theme support, and a rich text editor.

```tsx
// Import components from @moldable-ai/ui (NOT from shadcn directly)
import { 
  Button, Card, Input, Dialog, Select, Tabs,
  ThemeProvider, WorkspaceProvider, useTheme,
  Markdown, CodeBlock, WidgetLayout,
  downloadFile, sendToMoldable
} from '@moldable-ai/ui'

// For rich text editing
import { MarkdownEditor } from '@moldable-ai/editor'
```

**Use semantic colors only:**
```tsx
// ✅ Correct
<div className="bg-background text-foreground border-border" />
<Button className="bg-primary text-primary-foreground" />

// ❌ Wrong - raw colors don't adapt to theme
<div className="bg-white text-gray-900" />
```

See [references/ui.md](references/ui.md) for complete component list and usage.

### 2. Workspace-Aware Storage

All apps **must** isolate data per workspace:

```tsx
// Client - use workspaceId in query keys
const { workspaceId, fetchWithWorkspace } = useWorkspace()
const { data } = useQuery({
  queryKey: ['items', workspaceId],  // ← Include workspace!
  queryFn: () => fetchWithWorkspace('/api/items').then(r => r.json())
})

// Server - extract workspace from request
import { getWorkspaceFromRequest, getAppDataDir } from '@moldable-ai/storage'

export async function GET(request: Request) {
  const workspaceId = getWorkspaceFromRequest(request)
  const dataDir = getAppDataDir(workspaceId)
  // Read/write files in dataDir
}
```

### 3. Desktop Integration

Apps communicate with Moldable desktop via postMessage:

```typescript
// Open external URL
window.parent.postMessage({ type: 'moldable:open-url', url: 'https://...' }, '*')

// Show file in Finder
window.parent.postMessage({ type: 'moldable:show-in-folder', path: '/path/to/file' }, '*')

// Pre-populate chat input
window.parent.postMessage({ type: 'moldable:set-chat-input', text: 'Help me...' }, '*')

// Provide context to AI
window.parent.postMessage({ 
  type: 'moldable:set-chat-instructions', 
  text: 'User is viewing meeting #123...' 
}, '*')
```

### 4. Layout Setup

Required providers for Moldable apps:

```tsx
// src/app/layout.tsx
import { ThemeProvider, WorkspaceProvider } from '@moldable-ai/ui'
import { QueryProvider } from '@/lib/query-provider'

export default function RootLayout({ children }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider>
          <WorkspaceProvider>
            <QueryProvider>{children}</QueryProvider>
          </WorkspaceProvider>
        </ThemeProvider>
      </body>
    </html>
  )
}
```

### 5. Adding Dependencies

Use `sandbox: false` for package manager commands:

```typescript
await runCommand({
  command: 'cd ~/.moldable/shared/apps/my-app && pnpm add zod',
  sandbox: false  // Required for network access
})
```

## App Management Tools

| Tool | Purpose | Reversible |
|------|---------|------------|
| `scaffoldApp` | Create new app | — |
| `getAppInfo` | Check which workspaces use an app | — |
| `unregisterApp` | Remove from current workspace only | ✅ Re-add later |
| `deleteAppData` | Delete app's data (keep installed) | ❌ Data lost |
| `deleteApp` | **Permanently** delete from ALL workspaces | ❌ Everything lost |

## File Structure

```
~/.moldable/
├── shared/
│   ├── apps/{app-id}/              # App source code
│   │   ├── moldable.json           # App manifest
│   │   ├── package.json
│   │   └── src/
│   ├── skills/{repo}/{skill}/      # Skills library
│   ├── mcps/{mcp-name}/            # Custom MCP servers
│   └── config/mcp.json             # Shared MCP config
│
└── workspaces/{workspace-id}/
    ├── config.json                 # Registered apps
    ├── .env                        # Workspace env overrides
    ├── apps/{app-id}/data/         # App runtime data
    └── conversations/              # Chat history
```

## Common Mistakes to Avoid

1. **❌ Creating apps manually** — Always use `scaffoldApp`
2. **❌ Using localStorage** — Use filesystem storage
3. **❌ Forgetting workspaceId** — Include in query keys and API calls
4. **❌ Hardcoding paths** — Use `getAppDataDir()` for portability
5. **❌ Using raw colors** — Use shadcn semantic colors (`bg-background`, not `bg-gray-100`)
6. **❌ Running pnpm with sandbox** — Set `sandbox: false` for network access

## Study Existing Apps

For complex features, reference apps in `~/.moldable/shared/apps/`:

- **scribo** — Translation journal with language selection
- **meetings** — Audio recording with real-time transcription
- **calendar** — Google Calendar integration with OAuth

These demonstrate data fetching, storage patterns, API routes, and UI components.
