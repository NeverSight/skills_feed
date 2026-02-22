---
name: nebula-storybook-stories
description:
  Create Storybook stories for Canvas components. Use when (1) Creating a new
  component that needs a story, (2) Adding or modifying component stories, (3)
  Verifying story files exist. Covers CSF3 format, argTypes, and decorators.
---

**CRITICAL: Every component MUST have an individual story file.**

Each component in `src/components/` requires a corresponding story file in
`src/stories/`. The story file:

- Must be named `<component-name>.stories.jsx` (kebab-case with hyphens)
- Must import the component from `@/components/<component-name>`
- Must showcase the component's props and variants

**Example structure:**

```
src/components/my-card/
├── index.jsx
└── component.yml

src/stories/my-card.stories.jsx  # Required story file for my-card component
```

## Name mapping

Use this canonical mapping for component/story naming:

- `component.yml machineName`: `my-card`
- Component folder: `src/components/my-card/`
- Component import: `@/components/my-card`
- Story file: `src/stories/my-card.stories.jsx`

**Story file requirements:**

- Use Storybook CSF3 format (object-based stories).
- Include `argTypes` for props with predefined options (like enums).
- Create multiple story exports to showcase different variants.
- Use decorators when components need specific backgrounds (e.g., dark
  backgrounds for light-colored components).

After creating components, verify story files exist:

```bash
# List all story files
ls src/stories/*.stories.jsx

# Verify a specific component has its story
ls src/stories/<component-name>.stories.jsx
```
