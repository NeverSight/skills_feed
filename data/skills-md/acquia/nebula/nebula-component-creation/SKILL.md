---
name: nebula-component-creation
description:
  Create React components by copying and modifying examples from
  `examples/components/`. Use when asked to (1) Create, add, or build a new
  component, (2) Copy an example component to `src/components/`, (3) Add a
  component with dependencies. Handles dependency resolution and ensures each
  component has `index.jsx` and `component.yml`.
---

Story requirements are delegated to `nebula-storybook-stories` (canonical source
for story naming, structure, and CSF details).

## Workflow

### Creating a new component

Always start from an example. When asked to create a new component:

1. **Find a similar example** in `examples/components/` that can serve as a
   starting point (e.g., use `blockquote` for an "alert" component, or `button`
   for any interactive element)
2. **Copy the example component folder** to `src/components/<new_name>/`
3. **Copy the corresponding story** from `examples/stories/` to `src/stories/`
4. **Modify** the copied files to implement the new component

Always copy or create a story file for each component. For story naming,
structure, and CSF conventions, follow `nebula-storybook-stories`. Follow its
"Name Mapping" section for filename/path conversions.

This approach ensures consistent patterns for `component.yml` structure, JSX
conventions, and Storybook story format across all components.

```bash
# Example: Create an Alert component based on Blockquote
cp -r examples/components/blockquote src/components/alert
cp examples/stories/blockquote.stories.jsx src/stories/alert.stories.jsx
```

Then modify the copied files to implement the Alert component.

Components use the `@/components` import alias, which points to
`src/components`. When you copy and modify examples, the imports will work
automatically.

### Copying an existing example component

**Workflow for copying example components:**

1. **Check for existing example:** If the requested component (e.g., "hero")
   exists in `examples/components/`, plan to copy it directly.
2. **Analyze dependencies:** Read the example component's `index.jsx` file and
   identify all `@/components/<name>` imports. These are component dependencies.
3. **Recursively discover nested dependencies:** For each dependency found,
   check its `index.jsx` for additional `@/components/<name>` imports. Continue
   until all dependencies are discovered. For example, `hero` imports
   `two_column_text`, which imports `heading` and `text`.
4. **Check what already exists:** List the contents of `src/components/` to see
   which components are already present.
5. **Copy only missing components:** Copy only the example components (and their
   stories) that don't already exist in `src/components/`. Do NOT overwrite
   existing components.

**Example scenario:** User asks for a "hero" component.

```bash
# Step 1: Check existing components in src/
ls src/components/

# Suppose output shows only: button/  global.css

# Step 2: Analyze hero dependencies (hero → two_column_text → heading, text)
# Missing components: hero, two_column_text, heading, text
# button already exists, so skip it if it were a dependency

# Step 3: Copy all missing components and stories in one batch
cp -r examples/components/hero src/components/
cp -r examples/components/two_column_text src/components/
cp -r examples/components/heading src/components/
cp -r examples/components/text src/components/

cp examples/stories/hero.stories.jsx src/stories/
cp examples/stories/two-column-text.stories.jsx src/stories/
cp examples/stories/heading.stories.jsx src/stories/
cp examples/stories/text.stories.jsx src/stories/
```

## Required component folder structure

**CRITICAL:** Every component folder in `src/components/` MUST contain exactly
two files:

```
src/components/<component-name>/
├── index.jsx      # React component implementation
└── component.yml  # Component metadata and props for Drupal Canvas
```

**Never create a component folder without both files.** The `index.jsx` contains
the actual React component implementation. The `component.yml` defines the
component's metadata, props, and slots for Drupal Canvas.

The directory name must match machineName. The component folder name must
exactly match the `machineName` value defined in `component.yml`. Use
`kebab-case` (with hyphens) for new and modified components in
`src/components/`.

**Legacy exception:** `examples/components/` may contain legacy `snake_case`
names. Keep those examples unchanged unless explicitly asked to migrate them.

After creating components, verify the folder structure:

```bash
# List all component folders and their contents
ls -la src/components/*/

# Verify each new component has both required files
ls src/components/<component-name>/index.jsx
ls src/components/<component-name>/component.yml
```

If a component folder is missing either file, the component is incomplete and
will not work. Both `index.jsx` and `component.yml` are required.

## Best practices

### Reuse existing components

**Always check `src/components/` before creating new UI elements.** When
building a component that needs common UI elements (buttons, headings, images,
etc.), import and use existing components rather than duplicating their
functionality.

If the component you need doesn't exist in `src/components/` yet, check if it
exists in `examples/components/`. If so, copy it to `src/components/` first (see
"Copying an Existing Example Component" above), then import and use it.

```jsx
// Correct
import Button from "@/components/button";

const NewsletterSignup = ({ onSubmit }) => (
  <form onSubmit={onSubmit}>
    <input type="email" placeholder="Enter your email" />
    <Button variant="primary">Subscribe</Button>
  </form>
);

// Wrong
const NewsletterSignup = ({ onSubmit }) => (
  <form onSubmit={onSubmit}>
    <input type="email" placeholder="Enter your email" />
    <button className="rounded bg-primary-600 px-4 py-2 text-white">
      Subscribe
    </button>
  </form>
);
```

## Common pitfalls

- **Overwriting existing components** - Always check `src/components/` first
- **Missing dependencies** - Recursively check all `@/components/` imports
- **Incomplete component folder** - Both `index.jsx` and `component.yml` are
  required
- **Ignoring the `@/components` alias** - Use this import alias; it points to
  `src/components`
