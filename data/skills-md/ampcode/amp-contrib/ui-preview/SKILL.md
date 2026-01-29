---
name: ui-preview
description: 'Preview and screenshot local dev servers and storybooks. Use when asked to view UI components, take screenshots of storybooks, or inspect the web/server apps.'
metadata:
  version: '1'
---

# UI Preview Skill

Preview local dev servers and storybooks using Chrome DevTools.

## Available Tools

- `navigate_page` - Navigate to a URL
- `take_screenshot` - Capture a screenshot of the current page
- `new_page` - Open a new browser tab
- `press_key` - Press keyboard keys (e.g., scrolling with PageDown, End)
- `evaluate_script` - Run JavaScript on the page

## Workflow

1. **Navigate** to the target URL using `navigate_page`
2. **Screenshot** the page using `take_screenshot`
3. **Analyze** captured screenshots with `look_at` for visual analysis

## Local Dev URLs

Check `.amp/dev-environment.txt` for the running URLs (defaults: web=http://localhost:7001, server=https://localhost:7002).

| Service           | Path        |
| ----------------- | ----------- |
| Web dev server    | /           |
| Server dev server | /           |
| Webview storybook | /storybook  |
| Server storybook  | /storybook  |

## Storybooks

Access a specific story directly using the hash: `/storybook#${story-title}`

The story title is derived from the filename: `handoff-story.svelte` → `#handoff-tool`

### Webview Storybook (localhost:7001)

Components for the VS Code extension webview UI.

**Thread Components:**

- `#thread` - Full thread view
- `#streaming-thread` - Thread with streaming content
- `#scrollable-thread` - Thread with scroll behavior
- `#thread-reply-area` - Message input area
- `#thread-status` - Thread status indicators
- `#thread-summary` - Thread summary view
- `#thread-hints` - Thread hint suggestions
- `#thread-environment-input` - Environment input

**Tool Calls:**

- `#bash` - Bash tool output
- `#edit-file` - File edit diffs
- `#create-file` - File creation
- `#read` - File read output
- `#grep` - Search results
- `#glob` - File glob results
- `#handoff-tool` - Handoff tool states
- `#mermaid` - Diagram rendering
- `#oracle-tool` - Oracle tool output
- `#task-tool` - Task tool output
- `#web-search` - Web search results

**Editor & Input:**

- `#prompt-editor` - Message input editor
- `#mention-menu` - @mention autocomplete
- `#combobox` - Combobox component
- `#agent-mode-selector` - Agent mode picker

**Diff Viewer:**

- `#diff-viewer` - Side-by-side diff
- `#diff-display` - Inline diff display
- `#unified-diff` - Unified diff format

**Settings:**

- `#settings-page` - Settings page
- `#settings-error-modal` - Error modal
- `#sign-in-page` - Authentication page

**Layout:**

- `#layout-navbar` - Navigation bar
- `#current-thread-navbar-item` - Thread nav item

### Server Storybook (localhost:7002)

Components for the ampcode.com web app.

**Thread Management:**

- `#thread-feed` - Thread list feed
- `#thread-feed-item` - Individual thread item
- `#thread-feed-list` - Virtualized thread list
- `#thread-actions` - Thread action buttons
- `#thread-visibility` - Visibility settings
- `#thread-visibility-edit` - Edit visibility
- `#thread-page` - Full thread page
- `#thread-open-in-button` - Open in editor button
- `#pull-request-badge` - PR badge display

**Settings:**

- `#settings-access-token-section` - API tokens
- `#settings-advanced-section` - Advanced settings
- `#settings-client-section` - Client settings
- `#billing-section` - Billing info
- `#amp-free-section` - Free tier info
- `#code-host-connections-section` - GitHub/GitLab connections

**User & Profile:**

- `#avatar` - User avatar
- `#profile-card` - Profile card
- `#profile-dropdown` - Profile menu
- `#user-display` - User name display

**Dashboard:**

- `#welcome` - Welcome page
- `#usage-by-day` - Usage metrics

**UI Components:**

- `#amp-logo` - Logo variants
- `#badge-single` - Single badge
- `#badge-group` - Badge group
- `#copyable-text` - Copy-to-clipboard text
- `#colors` - Color palette
- `#icons` - Icon set

**OG Images:**

- `#og-images` - Social preview images

## Tips

- Story titles use kebab-case from filenames (remove `-story.svelte`)
- Reload the skill if MCP tools become unavailable
- Use `list_pages` to manage multiple browser tabs
- Use `press_key` with "End" or "PageDown" to scroll the page
- Use `evaluate_script` for custom page interactions
