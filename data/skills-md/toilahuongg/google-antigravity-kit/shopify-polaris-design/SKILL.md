---
name: shopify-polaris-design
description: Design and implement Shopify Admin interfaces using the Polaris Design System. Use this skill when building Shopify Apps, Admin extensions, or any interface that needs to feel native to Shopify.
---

This skill ensures that interfaces are built using Shopify's Polaris Design System, guaranteeing a native, accessible, and professional look and feel for Shopify Merchants.

## Core Principles

1.  **Merchant-Focused**: Design for efficiency and clarity. Merchants use these tools to run their business. 
2.  **Native Feel**: The app should feel like a natural extension of the Shopify Admin. Do not introduce foreign design patterns (e.g. Material Design shadows, distinct bootstappy buttons) unless absolutely necessary.
3.  **Accessibility**: Polaris is built with accessibility in mind. Maintain this by using semantic components (e.g., `Button`, `Link`, `TextField`) rather than custom `div` implementations.
4.  **Predictability**: Follow standard Shopify patterns. Save buttons go in the Contextual Save Bar. Page actions go in the top right. Primary content is centered.

## Technical Implementation

### Dependencies
- `@shopify/polaris`
- `@shopify/polaris-icons`
- `@shopify/app-bridge-react` (for navigation, title bar, toasts, save bar)

### Fundamental Components

- **AppProvider**: All Polaris apps must be wrapped in `<AppProvider i18n={enTranslations}>`.
- **Page**: The top-level container for a route. Always set `title` and `primaryAction` (if applicable).
  ```jsx
  <Page title="Products" primaryAction={{content: 'Add product', onAction: handleAdd}}>
  ```
- **Layout**: Use `Layout` and `Layout.Section` to structure content.
    - `Layout.AnnotatedSection`: For settings pages (Title/Description on left, Card on right).
    - `Layout.Section`: Standard Full (default), 1/2 (`variant="oneHalf"`), or 1/3 (`variant="oneThird"`) width columns.
- **Card**: The primary container for content pieces. Group related information in a Card. 
    - Use `BlockStack` (vertical) or `InlineStack` (horizontal) for internal layout within a Card.
    - **Do not** use `Card.Section` as it is deprecated in newer versions; use `BlockStack` with `gap`.

### Data Display

- **IndexTable**: For lists of objects (Products, Orders) with bulk actions and filtering. It replaces the older `ResourceList` for complex table cases.
- **LegacyCard** + **ResourceList**: Still valid for simple lists where table headers aren't needed.
- **DataTable**: For simple, non-interactive data grids (e.g., analytics data).
- **Text**: Use `<Text as="h2" variant="headingMd">` instead of `<h2>`. Strict typography control is key.

### Form Design

- Use `FormLayout` to automatically handle spacing and alignment of form fields.
- Use `TextField`, `Select`, `Checkbox`, `RadioButton`.
- **Validation**: Pass `error` prop (string or boolean) to form fields to show validation messages inline.
- **ContextualSaveBar**: For forms that edit existing data, use the App Bridge `useSaveBar` or `<ContextualSaveBar>` component to show the specialized top bar for saving/discarding changes.

## Design Tokens & CSS

- **Avoid Custom CSS**: 95% of styling should be handled by Polaris props (`gap`, `padding`, `align`, `justify`).
- **Design Tokens**: If you MUST use custom CSS, use Polaris CSS Custom Properties (Tokens).
  - Backgrounds: `var(--p-color-bg-surface)`
  - Text: `var(--p-color-text-default)`
  - Spacing: `var(--p-space-400)` (16px)
  - Borders: `var(--p-border-radius-200)`

## Code Style Example

```jsx
import { Page, Layout, Card, BlockStack, Text, Button, InlineStack, Badge } from '@shopify/polaris';

export default function Dashboard() {
  return (
    <Page 
        title="Dashboard" 
        primaryAction={{content: 'Create Campaign', onAction: () => {}}}
        secondaryActions={[{content: 'View Logs', onAction: () => {}}]}
    >
      <Layout>
        <Layout.Section>
          <Card>
            <BlockStack gap="400">
              <InlineStack align="space-between">
                <Text as="h2" variant="headingMd">Recent Activity</Text>
                <Badge tone="success">Active</Badge>
              </InlineStack>
              <Text as="p" tone="subdued">Everything is running smoothly.</Text>
            </BlockStack>
          </Card>
        </Layout.Section>
        
        <Layout.Section variant="oneThird">
            <Card>
                <BlockStack gap="200">
                    <Text as="h3" variant="headingSm">Quick Helper</Text>
                    <Button variant="plain">Read Documentation</Button>
                </BlockStack>
            </Card>
        </Layout.Section>
      </Layout>
    </Page>
  );
}
```

## Anti-Patterns to AVOID

- **DO NOT** use Shadows or Borders manually. Cards handle this.
- **DO NOT** use `style={{ margin: 10 }}`. Use `<Box padding="400">` or `<BlockStack gap="400">`.
- **DO NOT** create a "Save" button at the bottom of a form. Use the `ContextualSaveBar` at the top of the viewport.
- **DO NOT** use generic loading spinners. Use `<SkeletonPage>` or `<SkeletonBodyText>` for loading states.
