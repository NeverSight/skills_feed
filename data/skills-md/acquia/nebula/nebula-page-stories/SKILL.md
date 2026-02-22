---
name: nebula-page-stories
description:
  Create example page stories that compose multiple components into realistic
  layouts. Use when building page-level Storybook stories that showcase how
  components work together. Covers PageLayout usage, composition rules, spacing
  with Spacer, and single-story hoisting.
---

# Example page stories with Storybook

Page stories showcase how components work together in realistic layouts. They
should closely mirror what end users will experience in Drupal Canvas, so avoid
patterns that won't be available in Canvas.

## Location and naming

- Page stories MUST be placed in `src/stories/example-pages/`
- Page story files should be named `<page-name>.stories.jsx`
- The Storybook title MUST use this format:
  `title: "Example pages/[Page Title]"`

### Single-story hoisting

**Use single-story hoisting for cleaner navigation.** Page stories should use
Storybook's single-story hoisting feature to avoid unnecessary nesting in the
sidebar. This is achieved by:

1. Including the full page name in the `title`
2. Exporting only one story (typically `Default`)
3. Setting the story's `name` property to match the last segment of the title

```jsx
// src/stories/example-pages/product-detail.stories.jsx
export default {
  title: "Example pages/Product: Detail",
  component: ProductDetailPage,
  parameters: {
    layout: "fullscreen",
  },
};

export const Default = {
  name: "Product: Detail",
};
```

This results in a flat sidebar entry "Product: Detail" under "Example pages",
rather than a nested "Product: Detail" → "Default" structure.

- When creating new components, consider adding them to existing page stories if
  they fit naturally, or create new page stories to demonstrate the component in
  context.
- When modifying existing components, review page stories in
  `src/stories/example-pages/` to ensure changes work well in composed layouts
  and update them if needed.

## PageLayout component

All page stories must use a shared `PageLayout` component from
`src/stories/example-pages/page-layout.jsx`.

### Create PageLayout when

- Creating the first page story, OR
- It doesn't exist in `src/stories/example-pages/`

### PageLayout structure

```jsx
// src/stories/example-pages/page-layout.jsx
import Footer from "@/components/footer";
import Header from "@/components/header";
import Section from "@/components/section";

const footerData = {
  // Shared footer data
};

const PageLayout = ({ children }) => (
  <>
    <Section width="wide" content={<Header />} />
    {children}
    <Section width="wide" content={<Footer {...footerData} />} />
  </>
);

export default PageLayout;
```

### Using PageLayout

```jsx
// src/stories/example-pages/about-page.stories.jsx
import Section from "@/components/section";
import Text from "@/components/text";

import PageLayout from "./page-layout";

const AboutPage = () => (
  <PageLayout>
    <Section width="normal" content={<Text text="<p>About us...</p>" />} />
  </PageLayout>
);

export default {
  title: "Example pages/About",
  component: AboutPage,
  parameters: { layout: "fullscreen" },
};

export const Default = { name: "About" };
```

## Composition rules

Page stories must only import and compose components.

### Allowed

- Import from `@/components/<name>`
- Pass props and compose together
- Define sample data (strings, objects, arrays)

### Not allowed

- Define React components inline
- Use raw HTML elements (`<div>`, `<span>`) for layout
- Duplicate existing component code

```jsx
// Wrong - defines inline components and uses raw HTML elements
const Logo = ({ color }) => <div className="flex">...</div>;

const Page = () => (
  <div className="flex flex-col gap-8">
    <Logo color="#000" />
    <div className="mx-auto max-w-3xl">Content</div>
  </div>
);
```

```jsx
// Correct - imports and composes existing components
import Footer from "@/components/footer";
import Header from "@/components/header";
import Section from "@/components/section";
import Text from "@/components/text";

const Page = () => (
  <>
    <Header />
    <Section width="normal" content={<Text text="<p>Content here</p>" />} />
    <Footer />
  </>
);
```

If you need a `<div>`, look for an existing component. If none exists, create it
in `src/components/` first.

## No className in page stories

The `className` prop is not exposed in Canvas. Page stories should not pass it.

```jsx
// Wrong
const AboutPage = () => (
  <PageLayout>
    <Section width="normal">
      <Text className="mt-8 mb-12" content="..." />
    </Section>
    <Card className="shadow-xl" title="Mission" />
  </PageLayout>
);

// Correct
const AboutPage = () => (
  <PageLayout>
    <Section width="normal">
      <Text content="..." />
    </Section>
    <Card title="Mission" />
  </PageLayout>
);
```

When className IS appropriate:

- Inside a component's `index.jsx` when composing other components
- In individual component stories (not page stories)

## Spacing with Spacer component

Control spacing between components using `spacer`, not margins or padding.

If spacer doesn't exist, copy it:

```bash
cp -r examples/components/spacer src/components/
cp examples/stories/spacer.stories.jsx src/stories/
```

```jsx
// Correct
import Spacer from "@/components/spacer";

const AboutPage = () => (
  <PageLayout>
    <Hero title="About Us" />
    <Spacer height="large" />
    <Section width="normal">
      <Text content="<p>Our story...</p>" />
    </Section>
    <Spacer height="medium" />
    <Section width="normal">
      <Text content="<p>Our mission...</p>" />
    </Section>
  </PageLayout>
);

// Wrong
const AboutPage = () => (
  <PageLayout>
    <Hero title="About Us" />
    <div className="mt-16">
      <Section width="normal">
        <Text content="<p>Our story...</p>" />
      </Section>
    </div>
  </PageLayout>
);
```

## Layout components

Use existing layout components instead of inline styles.

Check `src/components/` and `examples/components/` for:

- **Width constraints**: `section`, `container`
- **Column layouts**: `grid-container`, `columns`
- **Spacing**: `spacer`, `divider`

```jsx
// Correct
<WidthConstraintComponent variant="wide">
  <ColumnLayoutComponent columns="sidebar-main">
    {/* Content */}
  </ColumnLayoutComponent>
</WidthConstraintComponent>

// Wrong
<div className="mx-auto max-w-6xl px-4">
  <div className="grid grid-cols-[300px_1fr] gap-8">
    {/* Content */}
  </div>
</div>
```
