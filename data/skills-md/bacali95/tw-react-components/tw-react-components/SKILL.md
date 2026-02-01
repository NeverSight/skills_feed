---
name: tw-react-components
description: Use the tw-react-components library for building React UIs with TailwindCSS. Provides components (Button, Dialog, DataTable, Form controls, Layout, etc.), hooks (useToast, usePagination, useOutsideClick, etc.), and helpers. Use when building dashboards, forms, or UI features with this library.
---

# tw-react-components

React component library built with TailwindCSS for dashboards and applications.

## Installation & Setup

```bash
# Using bun
bun add tw-react-components

# Using npm
npm install tw-react-components

# Using yarn
yarn add tw-react-components

# Using pnpm
pnpm add tw-react-components
```

**tailwind.config.js:**

```js
module.exports = {
  content: ['./node_modules/tw-react-components/**/*.{js,ts,jsx,tsx}'],
  plugins: [
    require('@tailwindcss/forms'),
    require('tailwindcss-animate'),
    require('tw-react-components/tailwindcss-plugin'),
  ],
};
```

**Import CSS:**

```css
@import 'tw-react-components/index.css';
```

## Core Types

```typescript
type Size = 'small' | 'medium';
type Color = 'primary' | 'secondary' | 'slate' | 'gray' | 'red' | 'green' | 'blue' | /* ...all Tailwind colors */;
```

## Quick Reference

### Button

```tsx
import { Button } from 'tw-react-components';

<Button>Default</Button>
<Button variant="outlined" color="blue">Outlined</Button>
<Button prefixIcon={SaveIcon} loading>Saving...</Button>
```

See [references/components/button.md](references/components/button.md) for full API.

### Form Controls

Two patterns: `FormInputs.*` with react-hook-form, or standalone components.

```tsx
// With react-hook-form
<FormProvider {...form}>
  <FormInputs.Text name="username" label="Username" required />
  <FormInputs.Select name="country" items={countries} search />
</FormProvider>

// Standalone
<TextInput value={text} onChange={(e) => setText(e.target.value)} />
<SelectInput items={items} value={selected} onChange={setSelected} />
```

See [references/components/form-controls.md](references/components/form-controls.md) for full API.

### Dialog

```tsx
<Dialog open={isOpen} onOpenChange={setIsOpen}>
  <Dialog.Trigger asChild><Button>Open</Button></Dialog.Trigger>
  <Dialog.Content>
    <Dialog.Title>Title</Dialog.Title>
    <p>Content</p>
  </Dialog.Content>
</Dialog>

<ConfirmDialog open={open} title="Delete?" onConfirm={handleDelete} onClose={close}>
  Are you sure?
</ConfirmDialog>
```

See [references/components/dialog.md](references/components/dialog.md) for FormDialog, PdfViewerDialog, etc.

### DataTable

```tsx
<DataTable
  rows={data}
  columns={{
    id: { header: 'ID', field: 'id' },
    name: { header: 'Name', field: 'name' },
  }}
  sorting={{ sorting, onSortingChange: setSorting }}
  pagination={{ currentPage, setCurrentPage, totalItems, pageSize }}
  actions={[
    { icon: EditIcon, onClick: handleEdit },
    { icon: TrashIcon, color: 'red', onClick: handleDelete },
  ]}
/>
```

See [references/components/data-table.md](references/components/data-table.md) for full API.

### Layout

```tsx
<Layout
  sidebarProps={{
    items: [
      { type: 'item', pathname: '', title: 'Home', Icon: HomeIcon },
      { type: 'group', title: 'Admin', items: [...] },
    ],
  }}
  NavLink={NavLink}
  useLocation={useLocation}
>
  {children}
</Layout>
```

See [references/components/layout.md](references/components/layout.md) for full API.

### Sheet

```tsx
<Sheet open={isOpen} onOpenChange={setIsOpen}>
  <Sheet.Content side="right">
    <Sheet.Title>Title</Sheet.Title>
    <div>Content</div>
  </Sheet.Content>
</Sheet>
```

See [references/components/sheet.md](references/components/sheet.md) for full API.

### Tabs

```tsx
<Tabs defaultValue="tab1">
  <Tabs.List>
    <Tabs.Trigger value="tab1">Tab 1</Tabs.Trigger>
    <Tabs.Trigger value="tab2">Tab 2</Tabs.Trigger>
  </Tabs.List>
  <Tabs.Content value="tab1">Content 1</Tabs.Content>
  <Tabs.Content value="tab2">Content 2</Tabs.Content>
</Tabs>
```

See [references/components/tabs.md](references/components/tabs.md) for full API.

### Accordion

```tsx
<Accordion type="single" collapsible>
  <Accordion.Item value="item-1">
    <Accordion.Trigger>Section 1</Accordion.Trigger>
    <Accordion.Content>Content 1</Accordion.Content>
  </Accordion.Item>
</Accordion>
```

See [references/components/accordion.md](references/components/accordion.md) for full API.

### DropdownMenu

```tsx
<DropdownMenu>
  <DropdownMenu.Trigger asChild>
    <Button>Menu</Button>
  </DropdownMenu.Trigger>
  <DropdownMenu.Content>
    <DropdownMenu.Item onClick={action}>
      <DropdownMenu.Icon icon={UserIcon} />
      Profile
    </DropdownMenu.Item>
  </DropdownMenu.Content>
</DropdownMenu>
```

See [references/components/dropdown-menu.md](references/components/dropdown-menu.md) for submenus, checkboxes, radio groups.

### Toast

```tsx
// Setup: Add <Toaster /> to app root
const { toast } = useToast();

toast({ title: 'Saved!', variant: 'success' });
toast({ title: 'Error', variant: 'destructive', description: 'Failed to save.' });
```

See [references/components/toast.md](references/components/toast.md) for full API.

### Other Components

| Component       | Usage                                                      | Reference                                                    |
| --------------- | ---------------------------------------------------------- | ------------------------------------------------------------ |
| `Tooltip`       | `<Tooltip content="Hint"><Button>Hover</Button></Tooltip>` | [tooltip.md](references/components/tooltip.md)               |
| `Popover`       | Floating content relative to trigger                       | [popover.md](references/components/popover.md)               |
| `Badge`         | `<Badge color="green">Status</Badge>`                      | [badge.md](references/components/badge.md)                   |
| `Spinner`       | `<Spinner />` or `<Spinner fullScreen />`                  | [spinner.md](references/components/spinner.md)               |
| `Skeleton`      | `<Skeleton className="h-4 w-48" />`                        | [skeleton.md](references/components/skeleton.md)             |
| `Separator`     | `<Separator orientation="vertical" />`                     | [separator.md](references/components/separator.md)           |
| `Switch`        | `<Switch checked={on} onCheckedChange={setOn} />`          | [switch.md](references/components/switch.md)                 |
| `Pagination`    | Page navigation control                                    | [pagination.md](references/components/pagination.md)         |
| `ThemeSelector` | Light/dark mode toggle                                     | [theme-selector.md](references/components/theme-selector.md) |
| `Hint`          | Notification dots/badges                                   | [hint.md](references/components/hint.md)                     |
| `Flex`          | Flexbox layout                                             | [flex.md](references/components/flex.md)                     |
| `Block`         | Block container                                            | [block.md](references/components/block.md)                   |
| `Card`          | Container component                                        | [card.md](references/components/card.md)                     |

## Hooks

### useToast

```tsx
const { toast, dismiss } = useToast();
const { id, update } = toast({ title: 'Saving...' });
update({ title: 'Saved!', variant: 'success' });
```

See [references/hooks/use-toast.md](references/hooks/use-toast.md) for full API.

### usePagination

```tsx
const pages = usePagination(currentPage, totalPages);
// [1, 2, 3, '...', 10]
```

### useOutsideClick

```tsx
const ref = useRef<HTMLDivElement>(null);
useOutsideClick(ref, () => setOpen(false));
```

### useIsMobile

```tsx
const isMobile = useIsMobile(); // true if < 768px
```

### Other Hooks

| Hook              | Usage                         | Reference                                                     |
| ----------------- | ----------------------------- | ------------------------------------------------------------- |
| `useOutsideClick` | Detect clicks outside element | [use-outside-click.md](references/hooks/use-outside-click.md) |
| `useIsMobile`     | Detect mobile viewport        | [use-is-mobile.md](references/hooks/use-is-mobile.md)         |
| `useDays`         | Days for calendar grid        | [use-days.md](references/hooks/use-days.md)                   |
| `useMonths`       | Month names                   | [use-months.md](references/hooks/use-months.md)               |
| `useLongPress`    | Long press detection          | [use-long-press.md](references/hooks/use-long-press.md)       |
| `useOnSwipe`      | Swipe gestures                | [use-on-swipe.md](references/hooks/use-on-swipe.md)           |

## Helpers

```tsx
import { cn, compareDates, getDisplayDate, isEmpty } from 'tw-react-components';

// Class merging
<div className={cn('base', condition && 'conditional')} />;

// Date formatting
getDisplayDate(new Date(), { format: 'LL' }); // "January 31, 2026"

// Comparison
compareDates(date1, date2); // -1, 0, or 1

// Empty check
isEmpty(null); // true
isEmpty(''); // true
isEmpty([]); // true
```

See [references/helpers.md](references/helpers.md) for full API.

## Common Patterns

### Form with Validation

```tsx
<FormInputs.Email
  name="email"
  label="Email"
  required
  validate={(value) => value.includes('@') || 'Invalid email'}
/>
```

### DataTable Custom Rendering

```tsx
columns={{
  status: {
    header: 'Status',
    field: 'status',
    render: (item) => <Badge color={item.active ? 'green' : 'gray'}>{item.status}</Badge>,
  },
}}
```

### Conditional DataTable Actions

```tsx
actions={[
  { icon: TrashIcon, hide: (item) => !item.canDelete, onClick: handleDelete },
]}
```

## Resources

- Live demo: https://bacali95.github.io/tw-react-components
- Source: `libs/tw-react-components/src/`

## Reference Files

### Components

- [button.md](references/components/button.md)
- [dialog.md](references/components/dialog.md)
- [form-controls.md](references/components/form-controls.md)
- [data-table.md](references/components/data-table.md)
- [layout.md](references/components/layout.md)
- [tabs.md](references/components/tabs.md)
- [accordion.md](references/components/accordion.md)
- [dropdown-menu.md](references/components/dropdown-menu.md)
- [sheet.md](references/components/sheet.md)
- [tooltip.md](references/components/tooltip.md)
- [popover.md](references/components/popover.md)
- [toast.md](references/components/toast.md)
- [badge.md](references/components/badge.md)
- [spinner.md](references/components/spinner.md)
- [skeleton.md](references/components/skeleton.md)
- [separator.md](references/components/separator.md)
- [switch.md](references/components/switch.md)
- [pagination.md](references/components/pagination.md)
- [theme-selector.md](references/components/theme-selector.md)
- [hint.md](references/components/hint.md)
- [flex.md](references/components/flex.md)
- [block.md](references/components/block.md)
- [card.md](references/components/card.md)

### Hooks

- [use-toast.md](references/hooks/use-toast.md)
- [use-pagination.md](references/hooks/use-pagination.md)
- [use-outside-click.md](references/hooks/use-outside-click.md)
- [use-is-mobile.md](references/hooks/use-is-mobile.md)
- [use-days.md](references/hooks/use-days.md)
- [use-months.md](references/hooks/use-months.md)
- [use-long-press.md](references/hooks/use-long-press.md)
- [use-on-swipe.md](references/hooks/use-on-swipe.md)

### Helpers

- [helpers.md](references/helpers.md)
