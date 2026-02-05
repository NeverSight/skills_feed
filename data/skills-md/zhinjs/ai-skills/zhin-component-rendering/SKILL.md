---
name: zhin-component-rendering
description: Covers Zhin component rendering, defineComponent usage, and message template composition. Use when creating reusable message UI components.
license: MIT
metadata:
  author: zhinjs
  version: "1.0"
  framework: zhin
---

# Zhin Component Rendering Skill

Use this skill when developers need to create reusable message components with Zhin's component system.

## Define and Register a Component

```ts
import { defineComponent, usePlugin } from '@zhin.js/core'

const plugin = usePlugin()

const StatusCard = defineComponent((props: { title: string, value: string }, context) => {
  return `<text>${props.title}: ${props.value}</text>`
}, 'status-card')

plugin.addComponent(StatusCard)
```

## Template Usage

Components render within message templates:

```ts
await message.$reply('<status-card title="CPU" value="40%"/>')
```

You can nest components:

```ts
await message.$reply('<Fragment><status-card title="Memory" value="512MB"/></Fragment>')
```

## Props & Expressions

Props support inline expressions with `{}` and template interpolation via `${}` when rendering:

```ts
const Card = defineComponent((props: { title: string, count: number }) => {
  return `<text>${props.title}: ${props.count}</text>`
}, 'card')

await message.$reply('<card title="Jobs" count="{1 + 2}"/>')
```

## Rendering Lifecycle

The component service attaches a `before.sendMessage` listener to render templates before messages send.

If you need to pre-render a template manually, use `renderComponents`:

```ts
import { renderComponents } from '@zhin.js/core'

const options = await renderComponents(componentService.byName, {
  context: 'process',
  bot: 'dev',
  type: 'private',
  id: '123',
  content: '<status-card title="CPU" value="40%"/>'
})
```

## Built-in Components

Zhin includes:
- `Fragment` for grouping/children rendering
- `fetch` for loading remote content (use carefully and validate URLs)

## Best Practices

- Keep components small and reusable.
- Validate and sanitize user input before passing it into templates.
- Avoid untrusted URLs with the `fetch` component.
