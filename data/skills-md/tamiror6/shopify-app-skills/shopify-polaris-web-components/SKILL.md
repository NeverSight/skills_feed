---
name: shopify-polaris-web-components
description: Use Shopify Polaris Web Components (s-* custom elements) for App Home UI. Use when building App Home surfaces (not embedded apps), designing UI with s-page, s-section, s-stack, s-box, s-button, and other s-* components. Do not use @shopify/polaris React - App Home requires Web Components.
---

# Shopify Polaris Web Components

Use this skill when building UI for **Shopify App Home** surfaces using Polaris Web Components.

## When to Use

- Building App Home pages (the app surface outside of Shopify Admin iframe)
- Creating UI with `s-*` custom elements
- Designing layouts with s-section, s-stack, s-box
- Building forms, modals, or lists for App Home

**Important**: App Home uses **Polaris Web Components** (`s-*` elements), NOT Polaris React (`@shopify/polaris`). These are different technologies.

## Polaris React vs Web Components

| Feature | Polaris React | Polaris Web Components |
|---------|---------------|------------------------|
| Use for | Embedded admin apps | App Home surfaces |
| Import | `@shopify/polaris` | No import (native elements) |
| Syntax | `<Button>` | `<s-button>` |
| Framework | React components | Custom HTML elements |

## Core Components

### Page Structure

```html
<s-page heading="Dashboard">
  <s-section heading="Overview">
    <!-- Content -->
  </s-section>
  
  <s-section heading="Settings">
    <!-- More content -->
  </s-section>
</s-page>
```

### Layout with Stack

```html
<!-- Vertical stack (default) -->
<s-stack direction="block" gap="large">
  <s-text>Item 1</s-text>
  <s-text>Item 2</s-text>
</s-stack>

<!-- Horizontal stack -->
<s-stack direction="inline" gap="medium" alignItems="center">
  <s-button>Cancel</s-button>
  <s-button variant="primary">Save</s-button>
</s-stack>

<!-- Stack with justification -->
<s-stack 
  direction="inline" 
  justifyContent="space-between"
  alignItems="center"
>
  <s-text variant="headingMd">Title</s-text>
  <s-button>Action</s-button>
</s-stack>
```

### Section (Card-like Container)

Use `s-section` for grouped content with optional heading:

```html
<!-- Section with heading -->
<s-section heading="Chat Widget Settings">
  <s-stack direction="block" gap="medium">
    <s-text>Configure your widget appearance.</s-text>
    <!-- Form fields -->
  </s-stack>
</s-section>

<!-- Section without heading -->
<s-section>
  <s-text>Simple content block</s-text>
</s-section>
```

### Box (Generic Layout Container)

Use `s-box` for padding, borders, and spacing - NOT for cards:

```html
<!-- Box with padding -->
<s-box padding="large">
  <s-text>Padded content</s-text>
</s-box>

<!-- Box with border -->
<s-box 
  padding="medium" 
  borderWidth="base" 
  borderRadius="base"
>
  <s-text>Bordered content</s-text>
</s-box>

<!-- Box for spacing -->
<s-box paddingBlockStart="large">
  <s-text>Content with top margin</s-text>
</s-box>
```

**Rule**: Use `s-section` for card-like containers, `s-box` for layout/spacing only.

### Buttons

```html
<!-- Primary action -->
<s-button variant="primary" type="submit">
  Save Settings
</s-button>

<!-- Default button -->
<s-button>Cancel</s-button>

<!-- Destructive -->
<s-button variant="primary" tone="critical">
  Delete
</s-button>

<!-- Disabled -->
<s-button disabled>Unavailable</s-button>

<!-- With click handler (in JS) -->
<s-button id="save-btn">Save</s-button>
<script>
  document.getElementById('save-btn').addEventListener('click', handleSave);
</script>
```

### Text

```html
<!-- Headings -->
<s-text variant="headingLg">Large Heading</s-text>
<s-text variant="headingMd">Medium Heading</s-text>
<s-text variant="headingSm">Small Heading</s-text>

<!-- Body text -->
<s-text>Default body text</s-text>
<s-text variant="bodySm">Small body text</s-text>

<!-- Tones -->
<s-text tone="subdued">Muted text</s-text>
<s-text tone="critical">Error text</s-text>
<s-text tone="success">Success text</s-text>
```

### Banner

```html
<!-- Info banner -->
<s-banner>
  <p>This is an informational message.</p>
</s-banner>

<!-- Critical banner -->
<s-banner tone="critical">
  <p>Something went wrong. Please try again.</p>
</s-banner>

<!-- Success banner -->
<s-banner tone="success">
  <p>Settings saved successfully!</p>
</s-banner>

<!-- Dismissible banner -->
<s-banner tone="warning" onDismiss="handleDismiss">
  <p>Your trial ends in 3 days.</p>
</s-banner>
```

### Link

```html
<s-link href="/settings">Go to Settings</s-link>

<s-link href="https://shopify.dev" external>
  Documentation
</s-link>
```

### Form Elements

```html
<!-- Text field -->
<s-text-field 
  label="Store name"
  value="My Store"
  helpText="This appears in your widget"
></s-text-field>

<!-- Select -->
<s-select label="Language">
  <option value="en">English</option>
  <option value="es">Spanish</option>
</s-select>

<!-- Checkbox -->
<s-checkbox label="Enable notifications" checked></s-checkbox>
```

## Common Patterns

### Settings Page

```html
<s-page heading="Settings">
  <s-stack direction="block" gap="large">
    
    <s-section heading="General">
      <s-stack direction="block" gap="medium">
        <s-text-field 
          label="Welcome message"
          value="Hello! How can we help?"
        ></s-text-field>
        <s-checkbox label="Enable auto-reply"></s-checkbox>
      </s-stack>
    </s-section>
    
    <s-section heading="Appearance">
      <s-stack direction="block" gap="medium">
        <s-select label="Theme">
          <option value="light">Light</option>
          <option value="dark">Dark</option>
        </s-select>
      </s-stack>
    </s-section>
    
    <s-box paddingBlockStart="large">
      <s-stack direction="inline" gap="medium" justifyContent="flex-end">
        <s-button>Cancel</s-button>
        <s-button variant="primary">Save</s-button>
      </s-stack>
    </s-box>
    
  </s-stack>
</s-page>
```

### Empty State

```html
<s-section>
  <s-stack direction="block" gap="medium" alignItems="center">
    <s-text variant="headingMd">No campaigns yet</s-text>
    <s-text tone="subdued">
      Create your first campaign to get started.
    </s-text>
    <s-button variant="primary">Create Campaign</s-button>
  </s-stack>
</s-section>
```

### List with Actions

```html
<s-section heading="Campaigns">
  <s-stack direction="block" gap="none">
    
    <s-box padding="medium" borderBlockEnd="base">
      <s-stack direction="inline" justifyContent="space-between" alignItems="center">
        <s-stack direction="block" gap="extraSmall">
          <s-text variant="headingSm">Welcome Series</s-text>
          <s-text tone="subdued">Active • 1,234 sent</s-text>
        </s-stack>
        <s-button>Edit</s-button>
      </s-stack>
    </s-box>
    
    <s-box padding="medium" borderBlockEnd="base">
      <s-stack direction="inline" justifyContent="space-between" alignItems="center">
        <s-stack direction="block" gap="extraSmall">
          <s-text variant="headingSm">Abandoned Cart</s-text>
          <s-text tone="subdued">Paused • 567 sent</s-text>
        </s-stack>
        <s-button>Edit</s-button>
      </s-stack>
    </s-box>
    
  </s-stack>
</s-section>
```

## TypeScript Support

Add types for s-* components in your `tsconfig.json`:

```json
{
  "compilerOptions": {
    "types": ["@shopify/polaris-types"]
  }
}
```

## Best Practices

1. **Use s-section for cards** - Not s-box
2. **Use s-box for layout only** - Padding, borders, spacing
3. **Prefer s-* over custom divs** - Only use div when s-* can't achieve the layout
4. **Use semantic structure** - s-page > s-section > content
5. **Consistent spacing** - Use gap props, not manual margins
6. **Check the docs** - Components have many props not shown here

## When to Use Custom Styles

Only use plain `div` and inline styles when:
- The user explicitly requests it
- After trying s-* components and they can't achieve the required layout
- For very specific visual effects not supported by Polaris

## References

- [Polaris Web Components](https://shopify.dev/docs/api/app-home/polaris-web-components)
- [Using Polaris Components](https://shopify.dev/docs/api/app-home/using-polaris-components)
- [App Home Overview](https://shopify.dev/docs/apps/app-home)
- [Component Reference](https://shopify.dev/docs/api/app-home/components)
