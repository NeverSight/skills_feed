---
name: component-scaffolding
description: Generate Drupal/Twig component skeletons with web components and Miyagi validation. Use when user requests to create, scaffold, or add a new component at a specific path (e.g., "add component skeleton at patterns/share-button"), or when creating component files including Twig templates, CSS, JavaScript web components, JSON schemas, or mock data files.
---

# Component Scaffolding

Generate component skeletons for a Drupal theme using Twig, web components, and Miyagi for validation.

## Trigger Phrases

- "Add component skeleton at patterns/..."
- "Create new component..."
- "Scaffold component..."
- Creating/updating schema.yaml or mocks.yaml files

## Configuration

### Component Library Root

This skill assumes it lives within a component library project, e.g.:

```
apps/component-library/
├── .claude/
│   └── skills/
│       └── component-scaffolding/   ← this skill
├── src/
│   ├── components/
│   └── css/
└── <theme-name>.libraries.yml
```

The **component library root** is three levels up from this skill (i.e., `../../..` relative to this SKILL.md).

### Theme Name Discovery

The `<theme-name>` placeholder must be replaced with the actual Drupal theme name. To determine it:

1. Navigate to the component library root
2. Find the `*.libraries.yml` file — the filename prefix is the theme name
3. Example: `circle_dot.libraries.yml` → theme name is `circle_dot`

If the theme name cannot be determined from existing files, ask the user.

## File Templates

### 1. Twig Template: `<component-name>.twig`

```twig
{{ attach_library("<theme-name>/pattern-<component-name>") }}

<div class="<ComponentName>">
	{# Component implementation #}
</div>
```

- Library name: `pattern-<component-name>` (kebab-case)
- CSS class: `<ComponentName>` (PascalCase)
- Single tab indentation

### 2. CSS: `<component-name>.css`

```css
/** @define <ComponentName>; */

.<ComponentName > {
  /* Component styles */
}
```

- PascalCase in `@define` comment
- Tab indentation

### 3. JavaScript: `<component-name>.js`

**Only create if explicitly needed.** Skip if user says "no JavaScript", "CSS only", etc.

```javascript
// @ts-check

class <ComponentName> extends HTMLElement {
	constructor() {
		super();
	}

	connectedCallback() {
		this.#addEventListeners();
	}

	/**
	 * Add event listeners
	 */
	#addEventListeners() {
		// Add event listeners here
	}
}

customElements.define("<component-name>", <ComponentName>);
```

- PascalCase class name
- **NO prefix** on custom element name (use kebab-case directly)
- Only `#addEventListeners()` method in skeleton
- **NO `#elements` field or `#getElements()` method**

### 4. Schema: `schema.yaml`

```yaml
$schema: http://json-schema.org/draft-07/schema#
$id: /<tier>/<component-name>

type: object

required:
  - property1

additionalProperties: false
properties:
```

- `$id` matches component tier path
- Include `required` array with placeholder names
- Leave `properties:` empty in skeleton
- 2-space indentation (YAML standard)

For detailed schema patterns, see [references/schema-and-mocks.md](references/schema-and-mocks.md).

### 5. Mocks: `mocks.yaml`

```yaml

```

- Single blank line only in skeleton
- User adds their own mock data later

For mock data patterns, see [references/schema-and-mocks.md](references/schema-and-mocks.md).

### 6. CSS Entry Point: `src/css/<component-name>.css`

```css
@import url("../components/<tier>/<component-name>/<component-name>.css")
layer(components);
```

> Note: If the component is an element, you can use the `elements.css` entry point instead.

### 7. Library Definition: `<theme-name>.libraries.yml`

Add entry **alphabetically** within the appropriate tier section:

```yaml
pattern-<component-name>:
  header: true
  css:
    component:
      build/assets/css/<component-name>.css: {}
  js:
    build/assets/components/<tier>/<component-name>/<component-name>.js:
      attributes:
        type: module
```

- **Omit the `js:` block entirely if no JavaScript file is created**
- Maintain blank line between library definitions
- **Omit the `css:` block entirely if the component is an element**

## Naming Conventions

| Item            | Format                | Example                  |
| --------------- | --------------------- | ------------------------ |
| Directory/files | kebab-case            | `share-button`           |
| CSS class       | PascalCase            | `ShareButton`            |
| JS class        | PascalCase            | `class ShareButton`      |
| Custom element  | kebab-case, NO prefix | `share-button`           |
| Library name    | `<prefix>-<kebab>`    | `pattern-share-button`   |
| Schema $id      | `/<tier>/<kebab>`     | `/patterns/share-button` |

## Component Tiers

| Tier                | Location                              | Library Prefix        |
| ------------------- | ------------------------------------- | --------------------- |
| Elements            | `src/components/elements/`            | `element-`            |
| Patterns            | `src/components/patterns/`            | `pattern-`            |
| Template Components | `src/components/template-components/` | `template-component-` |
| Templates           | `src/components/templates/`           | `template-`           |

## Workflow

1. Create component directory: `src/components/<tier>/<component-name>/`
2. Create component files (twig, css, schema.yaml, mocks.yaml, and js **only if needed**)
3. Create CSS entry point: `src/css/<component-name>.css`
4. Add library definition to `<theme-name>.libraries.yml` (alphabetically in tier section)
5. Run linters to verify

## Optional Files

Pay attention to user requests indicating which files to skip:

| User says                         | Action                                    |
| --------------------------------- | ----------------------------------------- |
| "no JavaScript" / "CSS only"      | Skip .js file, omit `js:` from library    |
| "no CSS" / "JavaScript only"      | Skip .css files, omit `css:` from library |
| "schema only" / "just the schema" | Create only schema.yaml                   |

## Notes

- Skeletons provide structure, not functionality
- All files use tabs except YAML (2 spaces)
- Run linters after creation to verify
