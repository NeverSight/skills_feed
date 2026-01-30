---
name: composable-svelte-navigation
description: Navigation and animation patterns for Composable Svelte. Use when implementing modals, sheets, drawers, alerts, navigation flows, or component lifecycle animations. Covers state-driven navigation, PresentationState, parent observation, URL routing, and Motion One integration.
---

# Composable Svelte Navigation & Animation

This skill covers state-driven navigation patterns, PresentationState lifecycle animations, and URL routing integration.

---

## CRITICAL RULE

### Rule 3: State-Driven Animations Only

**Principle**: Component lifecycle animations MUST use Motion One + PresentationState. NO CSS transitions for UI interactions.

#### Animation Decision Tree
```
Does component have animation?
├─ NO → No animation system needed
└─ YES → What kind?
    ├─ Infinite loop (spinner, shimmer) → CSS @keyframes ONLY
    ├─ Hover/focus/click → NO TRANSITION (instant visual feedback)
    └─ Lifecycle (appear/disappear/expand/collapse) → Motion One + PresentationState
```

#### ❌ WRONG - CSS Transitions
```css
.button {
  transition: background-color 0.2s; /* ❌ REMOVED */
}

.modal {
  transition: opacity 0.3s; /* ❌ Not state-driven, not testable */
}
```

#### ✅ CORRECT - State-Driven with Motion One
```typescript
interface ModalState {
  content: Content | null;
  presentation: PresentationState<Content>;
}

// Reducer manages lifecycle
case 'show':
  return [
    {
      ...state,
      content,
      presentation: { status: 'presenting', content, duration: 0.3 }
    },
    Effect.afterDelay(300, (d) => d({
      type: 'presentation',
      event: { type: 'presentationCompleted' }
    }))
  ];

// Component executes animation
$effect(() => {
  if (store.state.presentation.status === 'presenting') {
    animateModalIn(element).then(() => {
      store.dispatch({
        type: 'presentation',
        event: { type: 'presentationCompleted' }
      });
    });
  }
});
```

**WHY**: State-driven animations are predictable, testable with TestStore, and composable with the navigation system.

---

## TREE-BASED NAVIGATION PATTERN

### Core Principle

**Non-null state = presented, null = dismissed**

This creates a navigation tree where each node can optionally present a child screen.

### State Structure

```typescript
// Parent state
interface AppState {
  items: Item[];
  destination: DestinationState | null; // What to show
}

// Destination is enum of possible screens
type DestinationState =
  | { type: 'addItem'; state: AddItemState }
  | { type: 'editItem'; state: EditItemState; itemId: string }
  | { type: 'confirmDelete'; state: ConfirmDeleteState; itemId: string };

// Child states
interface AddItemState {
  name: string;
  quantity: number;
}

interface EditItemState {
  name: string;
  quantity: number;
}

interface ConfirmDeleteState {
  itemName: string;
}
```

### Actions

```typescript
type AppAction =
  | { type: 'addButtonTapped' }
  | { type: 'editButtonTapped'; itemId: string }
  | { type: 'deleteButtonTapped'; itemId: string }
  | { type: 'destination'; action: PresentationAction<DestinationAction> };

type DestinationAction =
  | { type: 'addItem'; action: AddItemAction }
  | { type: 'editItem'; action: EditItemAction }
  | { type: 'confirmDelete'; action: ConfirmDeleteAction };

// PresentationAction wraps child actions
type PresentationAction<A> =
  | { type: 'presented'; action: A }
  | { type: 'dismiss' };
```

---

## IFLET COMPOSITION FOR OPTIONAL CHILDREN

**When**: Child may or may not be present (modal, sheet, drawer, detail view)

### Basic Pattern

```typescript
// Parent state
interface AppState {
  items: Item[];
  destination: AddItemState | null; // Optional child
}

// Parent actions
type AppAction =
  | { type: 'addButtonTapped' }
  | { type: 'destination'; action: PresentationAction<AddItemAction> };

// Reducer
import { ifLetPresentation } from '@composable-svelte/core';

case 'addButtonTapped':
  return [
    { ...state, destination: { name: '', quantity: 0 } },
    Effect.none()
  ];

case 'destination': {
  // Handle dismiss
  if (action.action.type === 'dismiss') {
    return [{ ...state, destination: null }, Effect.none()];
  }

  // Compose child
  const [newState, effect] = ifLetPresentation(
    (s) => s.destination,
    (s, d) => ({ ...s, destination: d }),
    'destination',
    (ca): AppAction => ({ type: 'destination', action: { type: 'presented', action: ca } }),
    addItemReducer
  )(state, action, deps);

  // Parent observes child completion
  if ('action' in action &&
      action.action.type === 'presented' &&
      action.action.action.type === 'saveButtonTapped') {
    const item = newState.destination!;
    return [
      {
        ...newState,
        destination: null, // Dismiss
        items: [...newState.items, { id: crypto.randomUUID(), ...item }]
      },
      effect
    ];
  }

  return [newState, effect];
}
```

---

## PARENT OBSERVATION PATTERN

**Critical Pattern**: Parent can observe child actions to react to completion, cancellation, or other child events.

### Example: Observing Save/Cancel

```typescript
case 'destination': {
  // Handle dismiss
  if (action.action.type === 'dismiss') {
    return [{ ...state, destination: null }, Effect.none()];
  }

  // Route to child reducer based on destination type
  let newState = state;
  let effect: Effect<AppAction> = Effect.none();

  if (state.destination?.type === 'addItem' && 'action' in action && action.action.type === 'presented') {
    const [childState, childEffect] = addItemReducer(
      state.destination.state,
      action.action.action,
      deps
    );

    newState = {
      ...state,
      destination: { type: 'addItem', state: childState }
    };

    effect = Effect.map(childEffect, (childAction): AppAction => ({
      type: 'destination',
      action: { type: 'presented', action: { type: 'addItem', action: childAction } }
    }));

    // Observe child completion
    if (action.action.action.type === 'saveButtonTapped') {
      return [
        {
          ...newState,
          destination: null,
          items: [...newState.items, {
            id: crypto.randomUUID(),
            name: childState.name,
            quantity: childState.quantity
          }]
        },
        effect
      ];
    }

    // Observe child cancellation
    if (action.action.action.type === 'cancelButtonTapped') {
      return [
        { ...newState, destination: null },
        effect
      ];
    }
  }

  // Similar for editItem and confirmDelete...

  return [newState, effect];
}
```

---

## SCOPING STORES FOR NAVIGATION

### scopeToDestination Pattern

```typescript
import { scopeToDestination } from '@composable-svelte/core';

// In component
const addItemStore = $derived(
  scopeToDestination(store, 'destination', 'addItem')
);

{#if addItemStore}
  <Modal open={true} onOpenChange={(open) => !open && addItemStore.dismiss()}>
    <AddItemForm store={addItemStore} />
  </Modal>
{/if}
```

**What it does**:
- Returns scoped store when destination matches the specified type
- Returns `null` when destination is null or different type
- Scoped store has `dismiss()` method that dispatches dismiss action

---

## PRESENTATIONSTATE LIFECYCLE

### The Lifecycle

```
idle → presenting → presented → dismissing → idle
  ↑        ↓           ↓           ↓         ↑
  └────────┴───────────┴───────────┴─────────┘
```

### PresentationState Type

```typescript
type PresentationState<Content> =
  | { status: 'idle' }
  | { status: 'presenting'; content: Content; duration: number }
  | { status: 'presented'; content: Content }
  | { status: 'dismissing'; content: Content; duration: number };

type PresentationEvent =
  | { type: 'presentationCompleted' }
  | { type: 'dismissalCompleted' };
```

### Complete Animated Modal Example

```typescript
// State
interface ModalState {
  content: ModalContent | null;
  presentation: PresentationState<ModalContent>;
}

interface ModalContent {
  title: string;
  message: string;
}

// Actions
type ModalAction =
  | { type: 'show'; content: ModalContent }
  | { type: 'hide' }
  | { type: 'presentation'; event: PresentationEvent };

// Reducer
const modalReducer: Reducer<ModalState, ModalAction> = (state, action) => {
  switch (action.type) {
    case 'show':
      // Guard: Don't show if already presenting/presented
      if (state.presentation.status !== 'idle') {
        return [state, Effect.none()];
      }

      return [
        {
          ...state,
          content: action.content,
          presentation: {
            status: 'presenting',
            content: action.content,
            duration: 0.3
          }
        },
        Effect.afterDelay(300, (d) => d({
          type: 'presentation',
          event: { type: 'presentationCompleted' }
        }))
      ];

    case 'presentation':
      if (action.event.type === 'presentationCompleted' &&
          state.presentation.status === 'presenting') {
        return [
          {
            ...state,
            presentation: {
              status: 'presented',
              content: state.presentation.content
            }
          },
          Effect.none()
        ];
      }

      if (action.event.type === 'dismissalCompleted' &&
          state.presentation.status === 'dismissing') {
        return [
          {
            ...state,
            content: null,
            presentation: { status: 'idle' }
          },
          Effect.none()
        ];
      }

      return [state, Effect.none()];

    case 'hide':
      // Guard: Can only hide from 'presented'
      if (state.presentation.status !== 'presented') {
        return [state, Effect.none()];
      }

      return [
        {
          ...state,
          presentation: {
            status: 'dismissing',
            content: state.presentation.content,
            duration: 0.2
          }
        },
        Effect.afterDelay(200, (d) => d({
          type: 'presentation',
          event: { type: 'dismissalCompleted' }
        }))
      ];

    default:
      const _never: never = action;
      return [state, Effect.none()];
  }
};

// Component
<script lang="ts">
  import { animate } from 'motion';

  let dialogElement: HTMLElement;

  $effect(() => {
    if ($store.presentation.status === 'presenting' && dialogElement) {
      animate(
        dialogElement,
        { opacity: [0, 1], scale: [0.95, 1] },
        { duration: 0.3, easing: 'ease-out' }
      ).finished.then(() => {
        store.dispatch({
          type: 'presentation',
          event: { type: 'presentationCompleted' }
        });
      });
    }

    if ($store.presentation.status === 'dismissing' && dialogElement) {
      animate(
        dialogElement,
        { opacity: [1, 0], scale: [1, 0.95] },
        { duration: 0.2, easing: 'ease-in' }
      ).finished.then(() => {
        store.dispatch({
          type: 'presentation',
          event: { type: 'dismissalCompleted' }
        });
      });
    }
  });
</script>

{#if $store.content}
  <div class="modal-backdrop">
    <dialog bind:this={dialogElement}>
      <h2>{$store.content.title}</h2>
      <p>{$store.content.message}</p>
      <button onclick={() => store.dispatch({ type: 'hide' })}>
        Close
      </button>
    </dialog>
  </div>
{/if}
```

---

## MOTION ONE ANIMATION SYSTEM

### Animation Helpers

```typescript
import {
  animateModalIn,
  animateModalOut,
  animateSheetIn,
  animateSheetOut,
  animateAccordionExpand,
  animateAccordionCollapse
} from '@composable-svelte/core/animation';

// Usage
$effect(() => {
  if ($store.presentation.status === 'presenting') {
    animateModalIn(element).then(() => {
      store.dispatch({
        type: 'presentation',
        event: { type: 'presentationCompleted' }
      });
    });
  }
});
```

### When to Use Motion One (REQUIRED)

1. **Component Lifecycle Animations**: Modal/Dialog fade/scale, Dropdown appear/disappear, Sheet slide in/out
2. **Expand/Collapse Animations**: Accordion items, Collapsible sections, height transitions
3. **Toast/Alert Animations**: Slide in from edge, Notification animations
4. **Navigation Animations**: Page transitions, Stack push/pop, route changes

### Animation Helpers Reference

```typescript
// Modal animations (fade + scale)
animateModalIn(element: HTMLElement): Promise<void>
animateModalOut(element: HTMLElement): Promise<void>

// Sheet animations (slide from bottom)
animateSheetIn(element: HTMLElement): Promise<void>
animateSheetOut(element: HTMLElement): Promise<void>

// Drawer animations (slide from side)
animateDrawerIn(element: HTMLElement, side: 'left' | 'right'): Promise<void>
animateDrawerOut(element: HTMLElement, side: 'left' | 'right'): Promise<void>

// Accordion animations (height)
animateAccordionExpand(element: HTMLElement): Promise<void>
animateAccordionCollapse(element: HTMLElement): Promise<void>

// Dropdown animations (fade + slide)
animateDropdownIn(element: HTMLElement): Promise<void>
animateDropdownOut(element: HTMLElement): Promise<void>
```

### CSS @keyframes (EXCEPTIONS ONLY)

```css
/* ✅ ALLOWED - Infinite loop */
@keyframes spin {
  to { transform: rotate(360deg); }
}

.spinner {
  animation: spin 1s linear infinite;
}

/* ✅ ALLOWED - Shimmer effect */
@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

.skeleton {
  animation: shimmer 1.5s infinite;
}
```

**CSS Animations**:
- ✅ **Allowed**: Infinite loops (Spinner, Skeleton shimmer effects, Progress indicators)
- ❌ **Prohibited**: Hover states, Focus states, Click/Active states
- ❌ **Prohibited**: Any lifecycle animations (appearing, disappearing, expanding, collapsing)

---

## URL ROUTING INTEGRATION

### Pattern: Sync Browser History with State

URL routing is state synchronization, not a separate navigation system. Use the router's pure functions for serialization/parsing.

```typescript
import { syncBrowserHistory } from '@composable-svelte/core/routing';

// In client hydration
syncBrowserHistory(store, {
  serializers: serializerConfig.serializers,
  parsers: parserConfig.parsers,
  // Map state → destination for URL serialization
  getDestination: (state) => {
    if (state.selectedPostId !== null) {
      return { type: 'post' as const, state: { postId: state.selectedPostId } };
    }
    return null;
  },
  // Map destination → action for back/forward navigation
  destinationToAction: (dest) => {
    if (dest?.type === 'post') {
      return { type: 'selectPost', postId: dest.state.postId };
    }
    return null;
  }
});
```

### Server-Side URL Parsing

```typescript
import { parseDestination } from './routing';

// In server route handler
async function renderApp(request: any, reply: any) {
  const posts = await loadPosts();
  const path = request.url;
  const requestedPostId = parsePostFromURL(path, posts[0]?.id || 1);

  const store = createStore({
    initialState: {
      ...initialState,
      posts,
      selectedPostId: requestedPostId,
      meta: computeMetaForPost(posts.find(p => p.id === requestedPostId))
    },
    reducer: appReducer,
    dependencies: {}
  });

  const html = renderToHTML(App, { store });
  reply.type('text/html').send(html);
}
```

### Router Configuration

```typescript
import { createRouter } from '@composable-svelte/core/routing';

// Define destination types
type Destination =
  | { type: 'post'; state: { postId: number } };

// Create router with patterns
const router = createRouter<Destination>()
  .route('/', null)
  .route('/posts/:postId', (params) => ({
    type: 'post',
    state: { postId: parseInt(params.postId, 10) }
  }))
  .build();

// Use for parsing
const destination = router.parse('/posts/42');
// { type: 'post', state: { postId: 42 } }

// Use for serialization
const path = router.serialize({ type: 'post', state: { postId: 42 } });
// '/posts/42'
```

---

## NAVIGATION COMPONENTS HOW-TO

These components are from the shadcn-svelte component library. See **composable-svelte-components** skill for full reference.

### Modal - Full-Screen Overlay

**When to use**: Primary action, form submission, important warnings

```svelte
<script lang="ts">
  import { Modal } from '@composable-svelte/core/components';
  import { scopeToDestination } from '@composable-svelte/core';

  const modalStore = $derived(scopeToDestination(store, 'destination', 'addItem'));
</script>

{#if modalStore}
  <Modal
    open={true}
    onOpenChange={(open) => !open && modalStore.dismiss()}
  >
    <ModalContent store={modalStore} />
  </Modal>
{/if}
```

### Sheet - Bottom Drawer

**When to use**: Mobile-first UIs, filters, settings panels

```svelte
<script lang="ts">
  import { Sheet } from '@composable-svelte/core/components';

  const sheetStore = $derived(scopeToDestination(store, 'destination', 'filters'));
</script>

{#if sheetStore}
  <Sheet
    open={true}
    onOpenChange={(open) => !open && sheetStore.dismiss()}
  >
    <SheetContent store={sheetStore} />
  </Sheet>
{/if}
```

### Drawer - Side Panel

**When to use**: Navigation menus, sidebars, settings

```svelte
<script lang="ts">
  import { Drawer } from '@composable-svelte/core/components';

  const drawerStore = $derived(scopeToDestination(store, 'destination', 'menu'));
</script>

{#if drawerStore}
  <Drawer
    side="left"
    open={true}
    onOpenChange={(open) => !open && drawerStore.dismiss()}
  >
    <DrawerContent store={drawerStore} />
  </Drawer>
{/if}
```

### Alert - Confirmation Dialog

**When to use**: Destructive actions, confirmations

```svelte
<script lang="ts">
  import { Alert, AlertTitle, AlertDescription, AlertActions, Button } from '@composable-svelte/core/components';

  const confirmStore = $derived(scopeToDestination(store, 'destination', 'confirmDelete'));
</script>

{#if confirmStore}
  <Alert
    open={true}
    onOpenChange={(open) => !open && confirmStore.dismiss()}
  >
    <AlertTitle>Delete Item?</AlertTitle>
    <AlertDescription>This action cannot be undone.</AlertDescription>
    <AlertActions>
      <Button onclick={() => confirmStore.dismiss()}>Cancel</Button>
      <Button variant="destructive" onclick={() => confirmStore.dispatch({ type: 'confirm' })}>
        Delete
      </Button>
    </AlertActions>
  </Alert>
{/if}
```

### Popover - Contextual Menu

**When to use**: Dropdown menus, tooltips, context menus

```svelte
<script lang="ts">
  import { Popover, PopoverTrigger, PopoverContent } from '@composable-svelte/core/components';
</script>

<Popover open={$store.showMenu} onOpenChange={(open) => store.dispatch({ type: 'toggleMenu', open })}>
  <PopoverTrigger>
    <Button>Options</Button>
  </PopoverTrigger>
  <PopoverContent>
    <button onclick={() => store.dispatch({ type: 'edit' })}>Edit</button>
    <button onclick={() => store.dispatch({ type: 'delete' })}>Delete</button>
  </PopoverContent>
</Popover>
```

---

## COMPLETE EXAMPLES

### Example 1: Modal with Edit Form

```typescript
// State
interface AppState {
  user: User | null;
  editProfile: EditProfileState | null;
}

interface EditProfileState {
  name: string;
  email: string;
  bio: string;
}

// Actions
type AppAction =
  | { type: 'editProfileTapped' }
  | { type: 'destination'; action: PresentationAction<EditProfileAction> };

type EditProfileAction =
  | { type: 'nameChanged'; name: string }
  | { type: 'emailChanged'; email: string }
  | { type: 'bioChanged'; bio: string }
  | { type: 'saveButtonTapped' }
  | { type: 'cancelButtonTapped' };

// Reducer
case 'editProfileTapped':
  return [
    {
      ...state,
      editProfile: {
        name: state.user?.name || '',
        email: state.user?.email || '',
        bio: state.user?.bio || ''
      }
    },
    Effect.none()
  ];

case 'destination': {
  if (action.action.type === 'dismiss') {
    return [{ ...state, editProfile: null }, Effect.none()];
  }

  const [childState, childEffect] = editProfileReducer(
    state.editProfile!,
    action.action.action,
    deps
  );

  const newState = { ...state, editProfile: childState };
  const effect = Effect.map(childEffect, (ca): AppAction => ({
    type: 'destination',
    action: { type: 'presented', action: ca }
  }));

  // Observe save
  if (action.action.action.type === 'saveButtonTapped') {
    return [
      {
        ...newState,
        editProfile: null,
        user: {
          ...state.user!,
          name: childState.name,
          email: childState.email,
          bio: childState.bio
        }
      },
      Effect.batch(
        effect,
        Effect.run(async (d) => {
          await api.updateProfile(childState);
          d({ type: 'profileUpdated' });
        })
      )
    ];
  }

  // Observe cancel
  if (action.action.action.type === 'cancelButtonTapped') {
    return [{ ...newState, editProfile: null }, effect];
  }

  return [newState, effect];
}

// Component
<script lang="ts">
  import { Modal, Button } from '@composable-svelte/core/components';
  import { scopeToDestination } from '@composable-svelte/core';

  const editProfileStore = $derived(
    scopeToDestination(store, 'editProfile')
  );
</script>

<Button onclick={() => store.dispatch({ type: 'editProfileTapped' })}>
  Edit Profile
</Button>

{#if editProfileStore}
  <Modal
    open={true}
    onOpenChange={(open) => !open && editProfileStore.dismiss()}
  >
    <EditProfileForm store={editProfileStore} />
  </Modal>
{/if}
```

### Example 2: Sheet with Animated Filters

```typescript
// State with PresentationState
interface AppState {
  items: Item[];
  filters: FilterState | null;
  presentation: PresentationState<FilterState>;
}

interface FilterState {
  category: string;
  priceRange: [number, number];
  sortBy: 'name' | 'price' | 'date';
}

// Actions
type AppAction =
  | { type: 'showFilters' }
  | { type: 'hideFilters' }
  | { type: 'presentation'; event: PresentationEvent }
  | { type: 'destination'; action: PresentationAction<FilterAction> };

// Reducer with animation lifecycle
case 'showFilters':
  if (state.presentation.status !== 'idle') {
    return [state, Effect.none()];
  }

  const initialFilters = { category: 'all', priceRange: [0, 1000], sortBy: 'name' };

  return [
    {
      ...state,
      filters: initialFilters,
      presentation: { status: 'presenting', content: initialFilters, duration: 0.3 }
    },
    Effect.afterDelay(300, (d) => d({
      type: 'presentation',
      event: { type: 'presentationCompleted' }
    }))
  ];

case 'presentation':
  if (action.event.type === 'presentationCompleted') {
    return [
      { ...state, presentation: { status: 'presented', content: state.presentation.content } },
      Effect.none()
    ];
  }
  if (action.event.type === 'dismissalCompleted') {
    return [
      { ...state, filters: null, presentation: { status: 'idle' } },
      Effect.none()
    ];
  }
  return [state, Effect.none()];

// Component with animation
<script lang="ts">
  import { Sheet } from '@composable-svelte/core/components';
  import { animateSheetIn, animateSheetOut } from '@composable-svelte/core/animation';

  let sheetElement: HTMLElement;

  $effect(() => {
    if ($store.presentation.status === 'presenting' && sheetElement) {
      animateSheetIn(sheetElement).then(() => {
        store.dispatch({
          type: 'presentation',
          event: { type: 'presentationCompleted' }
        });
      });
    }

    if ($store.presentation.status === 'dismissing' && sheetElement) {
      animateSheetOut(sheetElement).then(() => {
        store.dispatch({
          type: 'presentation',
          event: { type: 'dismissalCompleted' }
        });
      });
    }
  });

  const filterStore = $derived(scopeToDestination(store, 'filters'));
</script>

{#if filterStore}
  <Sheet
    open={true}
    onOpenChange={(open) => !open && filterStore.dismiss()}
  >
    <div bind:this={sheetElement}>
      <FilterForm store={filterStore} />
    </div>
  </Sheet>
{/if}
```

---

## COMMON ANTI-PATTERNS

### 1. Forgetting to Handle Dismiss

#### ❌ WRONG
```typescript
case 'destination': {
  // Only handles child actions, not dismiss
  const [newState, effect] = ifLetPresentation(...)(state, action, deps);
  return [newState, effect];
}
```

#### ✅ CORRECT
```typescript
case 'destination': {
  if (action.action.type === 'dismiss') {
    return [{ ...state, destination: null }, Effect.none()];
  }

  const [newState, effect] = ifLetPresentation(...)(state, action, deps);
  return [newState, effect];
}
```

**WHY**: PresentationAction includes dismiss. Parent must handle it to close modal/sheet.

---

### 2. Not Using PresentationState for Animations

#### ❌ WRONG
```typescript
interface State {
  showModal: boolean; // Just a boolean, no animation lifecycle
}
```

#### ✅ CORRECT
```typescript
interface State {
  content: Content | null;
  presentation: PresentationState<Content>; // Full lifecycle
}
```

**WHY**: PresentationState tracks animation lifecycle (presenting → presented → dismissing), enabling state-driven animations.

---

### 3. CSS Transitions for Lifecycle Animations

#### ❌ WRONG
```css
.modal {
  transition: opacity 0.3s;
}
```

#### ✅ CORRECT
```typescript
$effect(() => {
  if ($store.presentation.status === 'presenting') {
    animateModalIn(element).then(() => {
      store.dispatch({ type: 'presentation', event: { type: 'presentationCompleted' } });
    });
  }
});
```

**WHY**: State-driven animations are testable, predictable, and composable.

---

## DECISION TOOLS

### Navigation Component Selection

```
What kind of overlay?
│
├─ Full-screen important action → Modal
├─ Bottom panel (mobile-first) → Sheet
├─ Side panel (navigation/settings) → Drawer
├─ Quick confirmation (yes/no) → Alert
└─ Contextual menu (dropdown) → Popover
```

### Animation Decision Tree

```
Does component animate?
├─ NO → No animation system needed
└─ YES → What kind?
    ├─ Infinite loop (spinner, shimmer) → CSS @keyframes ONLY
    ├─ Hover/focus/click → NO TRANSITION (instant visual feedback)
    └─ Lifecycle (appear/disappear/expand/collapse) → Motion One + PresentationState
```

---

## CHECKLISTS

### Navigation Feature Checklist

- [ ] 1. Add optional destination field to state (`DestinationState | null`)
- [ ] 2. Use discriminated union if multiple destination types
- [ ] 3. Define PresentationAction wrapper
- [ ] 4. Handle dismiss action (set destination to null)
- [ ] 5. Use ifLetPresentation for child composition
- [ ] 6. Parent observes child completion actions
- [ ] 7. Use scopeToDestination in component
- [ ] 8. Add PresentationState if animations needed

### Animation Feature Checklist

- [ ] 1. Add PresentationState field to state
- [ ] 2. Add presentation actions (show, hide, presentation events)
- [ ] 3. Add guards to prevent invalid transitions
- [ ] 4. Use Motion One helpers (animateModalIn, etc.)
- [ ] 5. Dispatch presentation events after animation completes
- [ ] 6. Handle presentationCompleted and dismissalCompleted
- [ ] 7. Test animation lifecycle with TestStore (see composable-svelte-testing skill)

---

## TEMPLATES

### Navigation with Modal Template

```typescript
// types.ts
interface AppState {
  items: Item[];
  destination: AddItemState | null;
}

interface AddItemState {
  name: string;
  quantity: number;
}

type AppAction =
  | { type: 'addButtonTapped' }
  | { type: 'destination'; action: PresentationAction<AddItemAction> };

type AddItemAction =
  | { type: 'nameChanged'; name: string }
  | { type: 'quantityChanged'; quantity: number }
  | { type: 'saveButtonTapped' };

// reducer.ts
case 'addButtonTapped':
  return [
    { ...state, destination: { name: '', quantity: 0 } },
    Effect.none()
  ];

case 'destination': {
  if (action.action.type === 'dismiss') {
    return [{ ...state, destination: null }, Effect.none()];
  }

  const [newState, effect] = ifLetPresentation(
    (s) => s.destination,
    (s, d) => ({ ...s, destination: d }),
    'destination',
    (ca): AppAction => ({ type: 'destination', action: { type: 'presented', action: ca } }),
    addItemReducer
  )(state, action, deps);

  if ('action' in action &&
      action.action.type === 'presented' &&
      action.action.action.type === 'saveButtonTapped') {
    return [
      {
        ...newState,
        destination: null,
        items: [...newState.items, {
          id: crypto.randomUUID(),
          ...newState.destination!
        }]
      },
      effect
    ];
  }

  return [newState, effect];
}

// App.svelte
<script lang="ts">
  import { Modal } from '@composable-svelte/core/components';
  import { scopeToDestination } from '@composable-svelte/core';

  const addItemStore = $derived(scopeToDestination(store, 'destination'));
</script>

<Button onclick={() => store.dispatch({ type: 'addButtonTapped' })}>
  Add Item
</Button>

{#if addItemStore}
  <Modal open={true} onOpenChange={(open) => !open && addItemStore.dismiss()}>
    <AddItemForm store={addItemStore} />
  </Modal>
{/if}
```

---

## SUMMARY

This skill covers navigation and animation patterns for Composable Svelte:

1. **Critical Rule**: State-driven animations only (Motion One + PresentationState)
2. **Tree-Based Navigation**: Non-null = presented, null = dismissed
3. **ifLet Composition**: For optional children (modals, sheets, drawers)
4. **Parent Observation**: React to child completion/cancellation
5. **PresentationState Lifecycle**: idle → presenting → presented → dismissing → idle
6. **Motion One Integration**: Animation helpers for all lifecycle animations
7. **URL Routing**: Sync browser history with state
8. **Navigation Components**: Modal, Sheet, Drawer, Alert, Popover

**Remember**: All component lifecycle animations MUST use Motion One + PresentationState. NO CSS transitions for UI interactions.

For core architecture patterns, see **composable-svelte-core** skill.
For testing navigation flows, see **composable-svelte-testing** skill.
For component library reference, see **composable-svelte-components** skill.
For SSR with navigation, see **composable-svelte-ssr** skill.
