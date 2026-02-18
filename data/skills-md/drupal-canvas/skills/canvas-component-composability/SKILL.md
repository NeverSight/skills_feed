---
name: canvas-component-composability
description:
  Design Canvas-ready React components with slots and decomposition-first
  patterns. Use when (1) Designing a component's prop/slot structure, (2) A
  component is growing too large, (3) Deciding between props vs slots, (4)
  Refactoring monolithic components. Ensures Canvas compatibility.
---

**Prefer small, focused components over monolithic ones with many props.** When
a component starts accumulating many unrelated props, it's often a sign that it
should be decomposed into smaller, composable pieces.

## Signs a component should be decomposed

Consider breaking up a component when it has:

- **More than 6-8 props** that serve distinct purposes
- **Props for elements that make sense as standalone components** (breadcrumbs,
  titles, metadata, navigation)
- **Built-in layout assumptions** that limit where the component can be used
- **Multiple distinct visual sections** that could be reused independently

## Use slots for flexible composition

**Slots are the primary mechanism for composability.** Instead of passing
complex data through props, use slots to let parent components accept child
components. This matches how Canvas users build pages—by placing components
inside other components.

### Prefer slots over complex props

When a component needs to render variable content, use a slot instead of props
with complex structures:

```jsx
// Wrong
const ResourceDetail = ({
  metadata: [
    { label: "Type", value: "Report" },
    { label: "Author", value: "UNICEF" },
  ],
}) => (
  <div>
    {metadata.map((item) => (
      <MetadataItem key={item.label} {...item} />
    ))}
  </div>
);

// Correct
const ResourceMetadata = ({ items }) => (
  <div className="flex flex-col gap-2">{items}</div>
);

// Usage: pass MetadataItem components through the slot
<ResourceMetadata
  items={
    <>
      <MetadataItem label="Type" value="Report" />
      <MetadataItem label="Author" value="UNICEF" />
    </>
  }
/>;
```

### Slots enable Canvas compatibility

In Drupal Canvas, users compose pages by dragging components into slots. When
you design components with slots:

- Users can add, remove, or reorder child components freely
- Each child component's props can be edited independently
- The parent component doesn't need to know about child component types

### When to use slots vs props

| Use slots for                         | Use props for                       |
| ------------------------------------- | ----------------------------------- |
| Variable number of child components   | Single, required values (text, URL) |
| Content that users should compose     | Configuration options (size, color) |
| Complex nested structures             | Simple data (strings, booleans)     |
| Content that varies between instances | Content consistent across instances |

### Declare slots in component.yml

Every slot must be declared in the component's `component.yml`:

```yaml
slots:
  content:
    title: Content
  sidebar:
    title: Sidebar
```

In the JSX, slots are received as props and rendered directly:

```jsx
const TwoColumnLayout = ({ content, sidebar }) => (
  <div className="grid grid-cols-[1fr_300px] gap-8">
    <div>{content}</div>
    <aside>{sidebar}</aside>
  </div>
);
```

## Common decomposition patterns

### Page-level elements should be separate components

Elements that appear on many pages but aren't always needed together should be
separate components:

```jsx
// Wrong
const ResourceDetail = ({
  breadcrumbItems,
  title,
  date,
  taxonomyTag,
  coverImage,
  downloadButtonUrl,
  metadata,
  description,
}) => (
  <div>
    <Breadcrumb items={breadcrumbItems} />
    <Heading text={title} element="h1" />
    {/* ... */}
  </div>
);

// Correct
const ResourceDetailPage = () => (
  <PageLayout>
    <Section width="wide" content={<Breadcrumb items={breadcrumbItems} />} />
    <Section width="wide" content={<Heading text={title} element="h1" />} />
    <Section width="wide" content={<ArticleMeta date="May 2023" taxonomyTag="Climate" />} />
    <Section width="wide" content={/* ... */} />
  </PageLayout>
);
```

### Extract repeated patterns into small components

When you see the same combination of elements repeated, extract them:

| Pattern                       | Extract to component |
| ----------------------------- | -------------------- |
| Date + category/tag           | `article-meta`       |
| Cover image + download button | `resource-cover`     |
| Label + value pairs           | `metadata-item`      |
| Icon + text link              | `icon-link`          |

### Use layout components instead of built-in layouts

Don't build two-column or grid layouts into content components. Use layout
components like `grid-container` and compose content into them:

```jsx
// Wrong
const ResourceDetail = ({ leftContent, rightContent }) => (
  <div className="flex gap-10">
    <div className="w-[300px]">{leftContent}</div>
    <div className="flex-1">{rightContent}</div>
  </div>
);

// Correct
<GridContainer
  layout="25-75"
  gap="extra_large"
  content={
    <>
      <ResourceCover image={coverImage} />
      <div className="flex flex-col gap-5">
        <ResourceMetadata items={metadata} />
        <Text text={description} />
      </div>
    </>
  }
/>;
```

## When NOT to decompose

Keep components together when:

- **They always appear together** and never make sense separately
- **They share significant internal state** that would be awkward to lift up
- **The visual design tightly couples them** (e.g., overlapping elements, shared
  backgrounds)
- **Decomposition would create components with only 1-2 props** that aren't
  useful elsewhere
