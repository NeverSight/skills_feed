---
name: composable-svelte-components
description: UI component library reference for Composable Svelte. Use when implementing designs, choosing components, styling layouts, or working with shadcn-svelte components. Covers component props, variants, accessibility patterns, visual composition, and when to use which component. For specialized components see composable-svelte-graphics (3D), composable-svelte-code (editors/media), composable-svelte-charts (visualization), composable-svelte-maps (geospatial).
---

# Composable Svelte Components

This skill covers the UI component library for Composable Svelte applications, focusing on shadcn-svelte components and integration patterns.

**For Specialized Components**: See dedicated skills for graphics (3D), code (editors/media), charts (data viz), and maps (geospatial).

---

## COMPONENT LIBRARY OVERVIEW

Composable Svelte includes 73+ shadcn-svelte components for building modern UIs. All components integrate with the Composable Architecture via props and state management.

**Integration Pattern**:
- Props for configuration (labels, variants, styles)
- State from `$store` for reactive data
- Dispatch actions for user interactions

**Package Organization**:
- `@composable-svelte/core` - UI components (this skill)
- `@composable-svelte/graphics` - 3D graphics (see composable-svelte-graphics skill)
- `@composable-svelte/code` - Code editors, media players (see composable-svelte-code skill)
- `@composable-svelte/charts` - Data visualization (see composable-svelte-charts skill)
- `@composable-svelte/maps` - Interactive maps (see composable-svelte-maps skill)

---

## NAVIGATION COMPONENTS

**Purpose**: Overlay-based UI elements for state-driven navigation.

**Integration Pattern**: State-driven open/close via store, dismiss via PresentationAction.

See **composable-svelte-navigation** skill for implementation details. This section provides REFERENCE only.

### Modal

Full-screen overlay with backdrop, centered content.

**When to use**: Primary actions, form submissions, important warnings.

**Props**:
- `open: boolean` - Whether modal is open
- `onOpenChange: (open: boolean) => void` - Callback when open state changes

```typescript
import { Modal } from '@composable-svelte/core/components';

{#if modalStore}
  <Modal
    open={true}
    onOpenChange={(open) => !open && modalStore.dismiss()}
  >
    <ModalContent store={modalStore} />
  </Modal>
{/if}
```

### Sheet

Bottom drawer that slides up (mobile-first).

**When to use**: Mobile-first UIs, filters, settings panels.

**Props**:
- `open: boolean`
- `onOpenChange: (open: boolean) => void`

### Drawer

Side panel that slides from left or right.

**When to use**: Navigation menus, sidebars, settings.

**Props**:
- `side: 'left' | 'right'` - Which side to slide from
- `open: boolean`
- `onOpenChange: (open: boolean) => void`

### Alert

Confirmation dialog, centered, smaller than Modal.

**When to use**: Destructive actions, confirmations, yes/no decisions.

**Props**:
- `open: boolean`
- `onOpenChange: (open: boolean) => void`

### Popover

Contextual menu positioned near trigger element.

**When to use**: Dropdown menus, tooltips, context menus.

**Props**:
- `open: boolean`
- `onOpenChange: (open: boolean) => void`

---

## FORM COMPONENTS

**Purpose**: User input elements that integrate with Composable Architecture.

**Integration Pattern**: Value from $store.state, dispatch on change, validation state from store.

See **composable-svelte-forms** skill for full patterns.

### Input

Text input field with variants.

**Types**: text, email, password, number, tel, url, search, date, time.

**Props**:
- `type: string` - Input type
- `value: string` - Current value
- `oninput: (e: Event) => void` - Change handler
- `placeholder: string` - Placeholder text
- `disabled: boolean` - Disabled state

```typescript
import { Input } from '@composable-svelte/core/components';

<Input
  type="text"
  value={$store.name}
  oninput={(e) => store.dispatch({ type: 'nameChanged', name: e.currentTarget.value })}
  placeholder="Enter name"
  disabled={$store.isSubmitting}
/>

{#if $store.nameError}
  <span class="error">{$store.nameError}</span>
{/if}
```

### Select

Dropdown selector.

**Props**:
- `value: string` - Selected value
- `onValueChange: (value: string) => void` - Selection handler

```typescript
import { Select, SelectTrigger, SelectContent, SelectItem } from '@composable-svelte/core/components';

<Select
  value={$store.category}
  onValueChange={(value) => store.dispatch({ type: 'categoryChanged', category: value })}
>
  <SelectTrigger>
    <SelectValue placeholder="Select category" />
  </SelectTrigger>
  <SelectContent>
    <SelectItem value="electronics">Electronics</SelectItem>
    <SelectItem value="clothing">Clothing</SelectItem>
    <SelectItem value="food">Food</SelectItem>
  </SelectContent>
</Select>
```

### Checkbox

Boolean toggle with label.

**Props**:
- `checked: boolean` - Checked state
- `onCheckedChange: (checked: boolean) => void` - Toggle handler

```typescript
import { Checkbox } from '@composable-svelte/core/components';

<Checkbox
  checked={$store.agreeToTerms}
  onCheckedChange={(checked) => store.dispatch({ type: 'toggleTerms', checked })}
>
  I agree to the terms and conditions
</Checkbox>
```

### RadioGroup

Mutually exclusive options.

**Props**:
- `value: string` - Selected value
- `onValueChange: (value: string) => void` - Selection handler

```typescript
import { RadioGroup, RadioGroupItem } from '@composable-svelte/core/components';

<RadioGroup
  value={$store.plan}
  onValueChange={(value) => store.dispatch({ type: 'planChanged', plan: value })}
>
  <RadioGroupItem value="free">Free</RadioGroupItem>
  <RadioGroupItem value="pro">Pro ($9/mo)</RadioGroupItem>
  <RadioGroupItem value="enterprise">Enterprise ($99/mo)</RadioGroupItem>
</RadioGroup>
```

### Switch

Toggle switch.

**Props**:
- `checked: boolean`
- `onCheckedChange: (checked: boolean) => void`

### Textarea

Multi-line text input.

**Props**:
- `value: string`
- `oninput: (e: Event) => void`
- `rows: number` - Number of visible rows
- `placeholder: string`

### Combobox

Autocomplete dropdown.

**Props**:
- `value: string` - Selected value
- `options: Array<{ label: string; value: string }>` - Available options
- `onValueChange: (value: string) => void` - Selection handler
- `onSearchChange: (query: string) => void` - Search handler

---

## DATA DISPLAY COMPONENTS

**Purpose**: Display data from store.state, often derived/computed.

**Integration Pattern**: Map from store.state arrays, use $derived for filtering/sorting.

### Table

Tabular data display with sorting/filtering.

**When to use**: Lists of structured data, data grids.

```typescript
import { Table, TableHeader, TableRow, TableHead, TableBody, TableCell } from '@composable-svelte/core/components';

<Table>
  <TableHeader>
    <TableRow>
      <TableHead>Name</TableHead>
      <TableHead>Email</TableHead>
      <TableHead>Status</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    {#each $store.users as user (user.id)}
      <TableRow>
        <TableCell>{user.name}</TableCell>
        <TableCell>{user.email}</TableCell>
        <TableCell>{user.status}</TableCell>
      </TableRow>
    {/each}
  </TableBody>
</Table>
```

### Card

Container for related content with header/footer.

**When to use**: Product cards, user profiles, content previews.

```typescript
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@composable-svelte/core/components';

{#each $store.products as product (product.id)}
  <Card>
    <CardHeader>
      <CardTitle>{product.name}</CardTitle>
      <CardDescription>{product.category}</CardDescription>
    </CardHeader>
    <CardContent>
      <p>${product.price}</p>
      <Button onclick={() => store.dispatch({ type: 'addToCart', productId: product.id })}>
        Add to Cart
      </Button>
    </CardContent>
  </Card>
{/each}
```

### Badge

Small label/tag.

**Variants**: default, success, secondary, destructive, outline.

```typescript
import { Badge } from '@composable-svelte/core/components';

<Badge variant={$store.status === 'active' ? 'success' : 'secondary'}>
  {$store.status}
</Badge>
```

### Avatar

User profile image with fallback.

```typescript
import { Avatar, AvatarImage, AvatarFallback } from '@composable-svelte/core/components';

<Avatar>
  <AvatarImage src={$store.user?.avatarUrl} alt={$store.user?.name} />
  <AvatarFallback>{$store.user?.initials}</AvatarFallback>
</Avatar>
```

---

## FEEDBACK COMPONENTS

**Purpose**: Communicate loading states, errors, and notifications.

**Integration Pattern**: Render based on loading/error/success state from store.

### Toast

Temporary notification.

**When to use**: Success messages, errors, notifications.

```typescript
import { toast } from '@composable-svelte/core/components';

// In reducer
case 'itemAdded':
  return [
    { ...state, items: [...state.items, action.item] },
    Effect.fireAndForget(async () => {
      toast.success('Item added successfully');
    })
  ];

case 'itemDeleteFailed':
  return [
    { ...state, error: action.error },
    Effect.fireAndForget(async () => {
      toast.error('Failed to delete item');
    })
  ];
```

### Progress

Linear progress indicator.

**When to use**: Upload progress, loading progress.

```typescript
import { Progress } from '@composable-svelte/core/components';

{#if $store.uploadProgress !== null}
  <Progress value={$store.uploadProgress} max={100} />
  <p>{$store.uploadProgress}% uploaded</p>
{/if}
```

### Skeleton

Loading placeholder with shimmer effect.

**When to use**: Content placeholders during loading.

```typescript
import { Skeleton } from '@composable-svelte/core/components';

{#if $store.isLoading}
  <Skeleton class="h-4 w-full mb-2" />
  <Skeleton class="h-4 w-3/4 mb-2" />
  <Skeleton class="h-4 w-1/2" />
{:else}
  <p>{$store.content}</p>
{/if}
```

### Spinner

Loading spinner.

**Props**:
- `size: 'small' | 'medium' | 'large'`

```typescript
import { Spinner } from '@composable-svelte/core/components';

{#if $store.isLoading}
  <Spinner size="large" />
{/if}
```

---

## LAYOUT COMPONENTS

**Purpose**: Organize UI with expand/collapse, tabs, resizable panels.

**Integration Pattern**: Expanded/active state lives in store, dispatch on user interaction.

### Accordion

Expandable/collapsible sections.

**When to use**: FAQs, collapsible content sections.

```typescript
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from '@composable-svelte/core/components';

// State
interface FAQState {
  expandedItems: string[]; // Array of expanded item IDs
}

// Reducer
case 'toggleItem':
  return [
    {
      ...state,
      expandedItems: state.expandedItems.includes(action.itemId)
        ? state.expandedItems.filter(id => id !== action.itemId)
        : [...state.expandedItems, action.itemId]
    },
    Effect.none()
  ];

// Component
<Accordion>
  {#each $store.faqItems as item (item.id)}
    <AccordionItem value={item.id}>
      <AccordionTrigger
        onclick={() => store.dispatch({ type: 'toggleItem', itemId: item.id })}
        expanded={$store.expandedItems.includes(item.id)}
      >
        {item.question}
      </AccordionTrigger>
      <AccordionContent>
        {item.answer}
      </AccordionContent>
    </AccordionItem>
  {/each}
</Accordion>
```

### Tabs

Tab navigation.

**When to use**: Multiple views of related content.

```typescript
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@composable-svelte/core/components';

// State
interface DashboardState {
  activeTab: 'overview' | 'analytics' | 'reports';
}

// Component
<Tabs value={$store.activeTab} onValueChange={(tab) => store.dispatch({ type: 'tabChanged', tab })}>
  <TabsList>
    <TabsTrigger value="overview">Overview</TabsTrigger>
    <TabsTrigger value="analytics">Analytics</TabsTrigger>
    <TabsTrigger value="reports">Reports</TabsTrigger>
  </TabsList>
  <TabsContent value="overview">
    <OverviewPanel store={store} />
  </TabsContent>
  <TabsContent value="analytics">
    <AnalyticsPanel store={store} />
  </TabsContent>
  <TabsContent value="reports">
    <ReportsPanel store={store} />
  </TabsContent>
</Tabs>
```

### Collapsible

Single collapsible section.

**When to use**: Sidebar toggles, advanced settings.

```typescript
import { Collapsible, CollapsibleTrigger, CollapsibleContent } from '@composable-svelte/core/components';

<Collapsible
  open={$store.sidebarExpanded}
  onOpenChange={(open) => store.dispatch({ type: 'toggleSidebar', open })}
>
  <CollapsibleTrigger>
    <Button>Toggle Sidebar</Button>
  </CollapsibleTrigger>
  <CollapsibleContent>
    <nav>
      <a href="/dashboard">Dashboard</a>
      <a href="/settings">Settings</a>
    </nav>
  </CollapsibleContent>
</Collapsible>
```

---

## SPECIALIZED COMPONENT PACKAGES

For specialized components beyond standard UI, see dedicated skills:

### 3D Graphics
**Skill**: `composable-svelte-graphics`
**Package**: `@composable-svelte/graphics`
**Components**: Scene, Camera, Light, Mesh
**Use cases**: 3D visualizations, WebGPU/WebGL rendering, geometry (box, sphere, cylinder, torus, plane)

### Code & Media
**Skill**: `composable-svelte-code`
**Package**: `@composable-svelte/code`
**Components**: CodeEditor, CodeHighlight, AudioPlayer, VideoEmbed, VoiceInput, NodeCanvas, StreamingChat
**Use cases**: Code editing, syntax highlighting, media playback, voice recognition, visual programming, chat interfaces

### Charts & Data Visualization
**Skill**: `composable-svelte-charts`
**Package**: `@composable-svelte/charts`
**Components**: Chart, ChartPrimitive, ChartTooltip
**Use cases**: Data visualization, interactive charts, statistical plots

### Maps & Geospatial
**Skill**: `composable-svelte-maps`
**Package**: `@composable-svelte/maps`
**Components**: Map, MapPrimitive, GeoJSONLayer, HeatmapLayer, Popup, TileProviderControl
**Use cases**: Interactive maps, geospatial data, location-based features

---

## COMPONENT SELECTION DECISION TREE

### Navigation Components

```
What kind of overlay?
│
├─ Full-screen important action → Modal
├─ Bottom panel (mobile-first) → Sheet
├─ Side panel (navigation/settings) → Drawer
├─ Quick confirmation (yes/no) → Alert
└─ Contextual menu (dropdown) → Popover
```

### Form Components

```
What kind of input?
│
├─ Single line text → Input
├─ Multi-line text → Textarea
├─ Boolean toggle → Checkbox or Switch
├─ One from many options → RadioGroup or Select
├─ Autocomplete/search → Combobox
└─ Date/time → Input type="date" or Input type="time"
```

### Data Display

```
What kind of data?
│
├─ Tabular data → Table
├─ List of items → Cards or List
├─ Status/label → Badge
├─ User profile → Avatar
└─ Metrics/stats → Card with metrics
```

### Feedback

```
What kind of feedback?
│
├─ Loading state → Spinner or Skeleton
├─ Progress indicator → Progress
├─ Success/error notification → Toast
└─ Confirmation needed → Alert
```

---

## CUSTOM COMPONENT GUIDELINES

**Principles for Building Custom Components:**

1. **No `$state` for Application State**: All state that affects behavior or can be tested must be in the store
2. **Dispatch Actions**: User interactions dispatch actions to the store
3. **Read from Store**: Render based on `$store.state`
4. **Use `$derived`**: For computed values derived from store state
5. **Props for Configuration**: Static configuration (labels, styles) can be props

**Example Custom Component:**

```svelte
<script lang="ts">
  import type { Store } from '@composable-svelte/core';

  export let store: Store<State, Action>;
  export let label: string; // Static config
  export let variant: 'primary' | 'secondary' = 'primary'; // Static config

  // Derived from store
  const isDisabled = $derived($store.isLoading || $store.hasErrors);
  const displayText = $derived($store.count > 0 ? `${label} (${$store.count})` : label);
</script>

<button
  class={variant}
  disabled={isDisabled}
  onclick={() => store.dispatch({ type: 'buttonClicked' })}
>
  {displayText}
</button>
```

---

## ACCESSIBILITY PATTERNS

### Keyboard Navigation

All interactive components support keyboard navigation:
- **Tab**: Move focus between elements
- **Enter/Space**: Activate buttons, toggles
- **Escape**: Close modals, popovers, dropdowns
- **Arrow keys**: Navigate lists, select options

### Screen Reader Support

Components include ARIA attributes:
- `aria-label`: Descriptive labels
- `aria-expanded`: Expanded/collapsed state
- `aria-selected`: Selected state
- `role`: Semantic roles

### Focus Management

Components manage focus:
- Modal traps focus inside dialog
- Popover returns focus to trigger on close
- Forms focus first invalid field on submit

---

## STYLING PATTERNS

### Tailwind Integration

All components use Tailwind CSS classes:

```svelte
<Button class="bg-primary text-primary-foreground hover:bg-primary/90">
  Click me
</Button>
```

### Custom Styles

Override with custom CSS:

```svelte
<Card class="custom-card">
  <CardContent>
    ...
  </CardContent>
</Card>

<style>
  .custom-card {
    background: linear-gradient(to right, #667eea 0%, #764ba2 100%);
  }
</style>
```

---

## SUMMARY

This skill covers the component library for Composable Svelte:

1. **Navigation Components**: Modal, Sheet, Drawer, Alert, Popover
2. **Form Components**: Input, Select, Checkbox, RadioGroup, Switch, Textarea, Combobox
3. **Data Display**: Table, Card, Badge, Avatar
4. **Feedback**: Toast, Progress, Skeleton, Spinner
5. **Layout**: Accordion, Tabs, Collapsible
6. **3D Graphics**: Scene, Camera, Light, Mesh (box, sphere, cylinder, torus, plane)
7. **Component Selection**: Decision trees for choosing components
8. **Custom Components**: Guidelines for building custom components
9. **Accessibility**: Keyboard, screen reader, focus management
10. **Styling**: Tailwind integration, custom styles

**Remember**: Props for config, state in store, dispatch for interactions. Use the right component for each use case.

For navigation implementation, see **composable-svelte-navigation** skill.
For form integration, see **composable-svelte-forms** skill.
For core architecture, see **composable-svelte-core** skill.
For testing components, see **composable-svelte-testing** skill.
