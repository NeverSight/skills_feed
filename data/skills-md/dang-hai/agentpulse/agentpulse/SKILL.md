---
name: agentpulse
description: |
  Help write useExpose hooks to make React components controllable by AI agents.
  Use when: exposing a component to AgentPulse, writing useExpose bindings, deciding what to expose,
  or improving descriptions for AI agents. For initial project setup, use "agentpulse-setup" instead.
license: MIT
compatibility: React >=18 with AgentPulse installed.
metadata:
  author: agentpulse
  version: "1.0"
allowed-tools: Read Write Edit Glob
---

# AgentPulse Component Exposure

Help users write effective `useExpose` hooks to make React components controllable by AI agents.

## Core Principle: Expose Workflows, Not Just State

**AI agents should interact with UI the same way humans do.** This means:

1. **Visibility first** - A human can't fill a form that's hidden. Neither should an AI. Expose actions to make elements visible (`openModal`, `expandSection`, `showForm`) before the elements inside them.

2. **Workflow-oriented** - Structure exposures around user workflows, not implementation details:
   - Create project → Configure settings → Add team members
   - Open form → Fill fields → Submit
   - Expand section → Make changes → Collapse

3. **Sequential visibility** - If a UI requires steps (wizard, nested panels, accordions), expose the navigation actions so the AI follows the same path a human would.

### Example: Form in Modal

```tsx
// ❌ Bad: Exposes form fields but no way to show the modal
useExpose('contact-form', {
  name, setName,
  email, setEmail,
  submit,
});

// ✅ Good: Exposes the workflow - open modal, fill fields, submit
useExpose('contact-form', {
  isOpen,
  openForm,      // AI must call this first to show the modal
  closeForm,
  name, setName,
  email, setEmail,
  submit,
}, {
  description: 'Contact form. Call openForm() first to show modal, then fill fields with setName/setEmail, then submit().',
});
```

### Example: Collapsible Section

```tsx
// ✅ Good: Expose expand/collapse so AI can make content visible
useExpose('advanced-settings', {
  isExpanded,
  expand,        // AI calls this to reveal settings
  collapse,
  // Settings only accessible after expand()
  debugMode, setDebugMode,
  logLevel, setLogLevel,
}, {
  description: 'Advanced settings panel. Call expand() to reveal options, then modify settings, collapse() when done.',
});
```

### Example: Multi-Step Workflow

```tsx
// ✅ Good: Expose the full workflow for creating a project
useExpose('project-wizard', {
  // Navigation state
  currentStep,     // 'details' | 'team' | 'settings' | 'review'

  // Step transitions (AI follows same flow as human)
  goToDetails,
  goToTeam,
  goToSettings,
  goToReview,

  // Per-step actions
  setProjectName,
  addTeamMember,
  removeTeamMember,
  toggleSetting,

  // Final action
  createProject,
}, {
  description: 'Project creation wizard. Navigate: goToDetails() → goToTeam() → goToSettings() → goToReview(). Fill each step before advancing. Call createProject() on review step.',
});
```

## Quick Reference

```tsx
import { useExpose } from 'agentpulse';

useExpose('component-id', {
  // State (read-only) - AI can read
  value,
  items,
  isLoading,

  // Setters (read-write) - AI can modify (auto-detected by setXxx naming)
  setValue,
  setFilter,

  // Actions (callable) - AI can call
  submit,
  refresh,
  clear,
}, {
  description: 'What it is. How to use it. What to expect.',
  tags: ['category'],
});
```

## What to Expose

Expose components users interact with. **Always include visibility controls when elements can be hidden.**

| Component Type | Visibility Controls | Content/Actions | Example ID |
|---------------|---------------------|-----------------|------------|
| Forms in modals | isOpen, openForm, closeForm | fields, setters, submit, errors | `contact-form` |
| Collapsible sections | isExpanded, expand, collapse | settings, setters | `advanced-settings` |
| Tabs/Panels | activeTab, setActiveTab | per-tab content | `settings-tabs` |
| Wizards | currentStep, goToStep, next, prev | per-step fields, submit | `signup-wizard` |
| Drawers/Sidebars | isOpen, open, close | content inside | `filter-drawer` |
| Dropdowns | isOpen, open, close | options, select | `user-menu` |
| Lists | (usually visible) | items, add, remove, toggle | `todo-list` |
| Inline inputs | (usually visible) | value, setValue, clear | `search-input` |

**Don't expose**: Layout components, pure displays with no interaction, internal implementation details.

**Key rule**: If a human must click to reveal something before interacting with it, the AI must do the same.

## Writing Good Descriptions

Descriptions tell the AI how to use your component. They're critical for workflow ordering.

**Formula**: `[What it is]. [Visibility step if needed]. [How to use it]. [What to expect/check].`

**Bad**:
- `"User form"` - What can AI do?
- `"Handles input"` - Too vague
- `"Set email and password"` - Missing visibility step if form is in modal

**Good** (with visibility steps):
- `"Contact form in modal. Call openForm() first, then fill name/email/message, then submit(). Check errors after."`
- `"Settings panel. Call expand() to reveal options, modify settings, collapse() when done."`
- `"Project wizard. Navigate goToDetails() → goToTeam() → goToSettings(). Fill each step, then createProject()."`

**Good** (always visible):
- `"Search box. Use setQuery(text), then search(). Check loading, read results when done."`
- `"Todo list. Use add(text) to create, toggle(id) to complete, remove(id) to delete."`

## Common Patterns

### Form in Modal (visibility-first)
```tsx
useExpose('contact-form', {
  // Visibility - AI must call openForm() first
  isOpen,
  openForm,
  closeForm,

  // Fields - only interact after form is visible
  name, setName,
  email, setEmail,
  message, setMessage,

  // Validation
  errors,
  isValid,

  // Actions
  submit,
  reset,
}, {
  description: 'Contact form in modal. Call openForm() first, fill name/email/message, check isValid, then submit(). closeForm() to dismiss.',
});
```

### Collapsible Settings
```tsx
useExpose('advanced-options', {
  // Visibility - AI must expand first
  isExpanded,
  expand,
  collapse,

  // Settings - only interact when expanded
  debugMode, setDebugMode,
  verboseLogging, setVerboseLogging,
  cacheEnabled, setCacheEnabled,
}, {
  description: 'Advanced options (collapsed by default). Call expand() to reveal, modify settings, collapse() when done.',
});
```

### Inline Input (always visible)
```tsx
useExpose('search-input', {
  value,
  setValue,
  clear: () => setValue(''),
  submit: () => onSearch(value),
}, {
  description: 'Search input. Use setValue(text), then submit() to search. clear() resets.',
});
```

### List with Add Form
```tsx
useExpose('todo-list', {
  // Add form visibility
  showAddForm,
  hideAddForm,
  isAddFormVisible,

  // Add form fields
  newItemText, setNewItemText,
  addItem: () => { addTodo(newItemText); hideAddForm(); },

  // List operations (always visible)
  items,
  count: items.length,
  toggle: (id) => toggleItem(id),
  remove: (id) => removeItem(id),
}, {
  description: 'Todo list. To add: showAddForm(), setNewItemText(text), addItem(). List: toggle(id) to check, remove(id) to delete.',
});
```

### Tabbed Interface
```tsx
useExpose('settings-tabs', {
  // Tab navigation
  tabs: ['profile', 'security', 'notifications'],
  activeTab,
  setActiveTab,

  // Profile tab fields (visible when activeTab === 'profile')
  displayName, setDisplayName,
  bio, setBio,

  // Security tab fields (visible when activeTab === 'security')
  changePassword,
  enable2FA,

  // Notifications tab fields
  emailNotifs, setEmailNotifs,

  // Save applies to current tab
  save,
}, {
  description: 'Settings tabs: profile, security, notifications. Use setActiveTab(name) to switch, modify fields for that tab, then save().',
});
```

### Confirmation Dialog
```tsx
useExpose('confirm-dialog', {
  isOpen,
  title,
  message,
  open: (title, message) => showDialog(title, message),
  confirm: () => { onConfirm(); close(); },
  cancel: () => { onCancel(); close(); },
}, {
  description: 'Confirmation dialog. Use open(title, message) to show. Respond with confirm() or cancel().',
});
```

## Binding Types

AgentPulse auto-detects types:

| Pattern | Type | AI Access |
|---------|------|-----------|
| `value` (primitive/object) | Value | Read |
| `setValue` (function named `set*`) | Setter | Read + Write |
| `submit` (other function) | Action | Call |
| `{ get, set }` | Accessor | Read + Write |

## Tags for Organization

```tsx
useExpose('login-form', bindings, { tags: ['auth', 'form'] });
useExpose('profile-form', bindings, { tags: ['auth', 'form'] });
```

AI can filter: `discover({ tag: 'auth' })`

## Scroll Bindings

For scrollable containers, use `createScrollBindings` to add scroll control:

```tsx
import { useExpose, createScrollBindings } from 'agentpulse';

function MessageList({ messages }) {
  const listRef = useRef<HTMLUListElement>(null);

  useExpose('message-list', {
    messages,
    count: messages.length,
    ...createScrollBindings(listRef),
  }, {
    description: 'Message list. Read messages array. Scroll: scrollToTop(), scrollToBottom(), scrollBy(delta).',
  });

  return <ul ref={listRef}>{/* ... */}</ul>;
}
```

**Exposed bindings:**
- `scrollTop` (read/write) - Current scroll position
- `scrollHeight` (read-only) - Total scrollable height
- `clientHeight` (read-only) - Visible height
- `scrollToTop()` - Scroll to top
- `scrollToBottom()` - Scroll to bottom
- `scrollTo(position)` - Scroll to specific position
- `scrollBy(delta)` - Scroll by relative amount

**Options:**
```tsx
createScrollBindings(ref, { behavior: 'smooth' }); // default
createScrollBindings(ref, { behavior: 'auto' });   // instant
```

## Multiple Instances

For components that render multiple times (list items), use `useExposeId`:

```tsx
import { useExpose, useExposeId } from 'agentpulse';

function TodoItem({ item }) {
  const exposeId = useExposeId('todo-item');

  useExpose(exposeId, {
    text: item.text,
    completed: item.completed,
    toggle: () => toggleItem(item.id),
  });

  return <li>{/* ... */}</li>;
}
```

Generates IDs like `todo-item:r1a2b3`, unique per component instance.

**Alternative:** Use item ID directly:
```tsx
useExpose(`todo-item:${item.id}`, { ... });
```

## Non-React Usage

For exposing state outside React components (services, modules), use `expose`:

```tsx
import { expose } from 'agentpulse';

// In a service
const unregister = expose('api-client', {
  isConnected: { get: () => client.connected, set: () => {} },
  reconnect: () => client.reconnect(),
}, {
  description: 'API client. Check isConnected, call reconnect() if needed.',
});

// Cleanup when done
unregister();
```

## Connection Status

Check AgentPulse connection status with `useAgentPulse`:

```tsx
import { useAgentPulse } from 'agentpulse';

function StatusIndicator() {
  const { isConnected } = useAgentPulse();

  return (
    <div className={isConnected ? 'connected' : 'disconnected'}>
      {isConnected ? 'AI Connected' : 'Offline'}
    </div>
  );
}
```

## Error Handling

Handle registration errors with `onRegistrationError`:

```tsx
useExpose('critical-form', bindings, {
  description: '...',
  onRegistrationError: (error) => {
    console.error('Failed to register with server:', error);
    // Component still works locally, just not remotely controllable
  },
});
```

## Visual Overlay Integration

For visual animations (cursor, typing effects), add `data-agentpulse-id` attributes to elements:

```tsx
useExpose('contact-form', {
  setName: (v) => setName(v),
  setEmail: (v) => setEmail(v),
  submitForm: () => handleSubmit(),
});

// Add data attributes for visual targeting
<input data-agentpulse-id="contact-form-name" />
<input data-agentpulse-id="contact-form-email" />
<button data-agentpulse-id="contact-form-submitform">Submit</button>
```

**Format:** `data-agentpulse-id="componentId-normalizedKey"`

Where `normalizedKey` = binding key with `set` prefix removed, lowercased.

See the `visual-overlay` skill for full targeting documentation.

## Process for Exposing a Component

1. **Identify the workflow** - What task does the user accomplish? (create project, submit form, configure settings)
2. **Map the visibility steps** - What must be clicked/opened before interacting? (modal, accordion, tab, drawer)
3. **List user actions in order** - First open/expand, then fill/modify, then submit/save, then close/collapse
4. **Map to bindings** - Visibility controls first, then state, then actions
5. **Write description with workflow** - Include the sequence: "Call X first, then Y, then Z"
6. **Add useExpose** - Import hook, add call inside component
7. **Test the workflow** - Verify AI can complete the full task, not just individual actions

## More Patterns

See `references/EXPOSE_PATTERNS.md` for:
- Multi-step forms/wizards
- Filtered/sorted/paginated lists
- Navigation patterns
- State management integration (Redux/Zustand)
- Testing exposed components
