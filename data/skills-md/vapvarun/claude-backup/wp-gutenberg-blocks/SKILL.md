---
name: wp-gutenberg-blocks
description: "Use when developing WordPress (Gutenberg) blocks: block.json metadata, register_block_type, attributes/serialization, supports, dynamic rendering (render.php), deprecations/migrations, InnerBlocks, viewScript/viewScriptModule, and @wordpress/scripts build workflows."
compatibility: "Targets WordPress 6.9+ (PHP 8.0+). Requires Node.js for build tooling."
---

# WP Block Development

## When to use

Use this skill for block work such as:

- creating a new block or updating an existing one
- changing `block.json` (scripts/styles/supports/attributes/render)
- fixing "block invalid / not saving / attributes not persisting"
- adding dynamic rendering (`render.php` / `render_callback`)
- block deprecations and migrations (`deprecated` versions)
- build tooling (`@wordpress/scripts`, `@wordpress/create-block`)
- block patterns and variations

## Inputs required

- Repo root and target (plugin vs theme vs full site).
- The block name/namespace and where it lives (path to `block.json` if known).
- Target WordPress version range (especially for `viewScriptModule` / apiVersion 3).

## Procedure

### 0) Triage and locate blocks

1. Search for existing `block.json` files
2. Search for `register_block_type` calls
3. Identify the block root (directory containing `block.json`)

### 1) Create a new block (if needed)

If creating a new block, prefer scaffolding:

```bash
npx @wordpress/create-block@latest my-custom-block
```

For interactive blocks, use the interactive template.

Read:
- `references/creating-blocks.md`

### 2) Ensure apiVersion 3 (WordPress 6.9+)

WordPress 6.9 enforces `apiVersion: 3` in block.json schema. Blocks with apiVersion 2 or lower trigger console warnings when `SCRIPT_DEBUG` is enabled.

**Why this matters:**
- WordPress 7.0 will run the post editor in an iframe regardless of block apiVersion
- apiVersion 3 ensures your block works correctly inside the iframed editor (style isolation, viewport units, media queries)

**Migration from apiVersion 2:**
1. Update the `apiVersion` field in `block.json` to `3`
2. Test in a local environment with the iframe editor enabled
3. Ensure any style handles are included in `block.json` (styles missing from the iframe won't apply)
4. Third-party scripts attached to a specific `window` may have scoping issues

```json
{
  "apiVersion": 3,
  "name": "my-plugin/my-block",
  "...": "..."
}
```

Read:
- `references/block-json.md`

### 3) Pick the right block model

- **Static block** (markup saved into post content): implement `save()`
- **Dynamic block** (server-rendered): use `render` in `block.json` and keep `save()` minimal or `null`
- **Interactive frontend**: use `viewScriptModule` for modern module-based view scripts

**viewScript vs viewScriptModule:**

| Property | `viewScript` | `viewScriptModule` |
|----------|--------------|-------------------|
| Module type | Classic script | ES Module |
| Loading | Synchronous | Async/deferred |
| Use for | Legacy/compatibility | Interactivity API, modern JS |
| Dependencies | Manual registration | Import statements |

```json
{
  "viewScript": "file:./view.js",
  "viewScriptModule": "file:./view.js"
}
```

Prefer `viewScriptModule` for:
- Interactivity API (`@wordpress/interactivity`)
- Modern ES module imports
- Better performance (deferred loading)

### 4) Update block.json safely

For field-by-field guidance:

Read:
- `references/block-json.md`

Common pitfalls:
- Changing `name` breaks compatibility (treat it as stable API)
- Changing saved markup without adding `deprecated` causes "Invalid block"
- Adding attributes without defining source/serialization causes "attribute not saving"

### 5) Register the block (server-side preferred)

Prefer PHP registration using metadata for:
- Dynamic rendering
- Translations (`wp_set_script_translations`)
- Conditional asset loading

Read:
- `references/registration.md`

### 6) Implement edit/save/render patterns

Follow wrapper attribute best practices:
- Editor: `useBlockProps()`
- Static save: `useBlockProps.save()`
- Dynamic render (PHP): `get_block_wrapper_attributes()`

Read:
- `references/edit-save-render.md`

### 7) Inner blocks (block composition)

If your block is a container that nests other blocks:
- Use `useInnerBlocksProps()` to integrate inner blocks with wrapper props
- Keep migrations in mind if you change inner markup

Read:
- `references/inner-blocks.md`

### 8) Block patterns and variations

- Patterns: predefined block arrangements
- Variations: different configurations of a single block

Read:
- `references/patterns-variations.md`

### 9) Migrations and deprecations

If you change saved markup or attributes:
1. Add a `deprecated` entry (newest → oldest)
2. Provide `save` for old versions and optional `migrate`

Read:
- `references/deprecations.md`

## Verification

- Block appears in inserter and inserts successfully.
- Saving + reloading does not create "Invalid block".
- Frontend output matches expectations (static: saved markup; dynamic: server output).
- Assets load where expected (editor vs frontend).
- Run the repo's lint/build/tests.

## Failure modes / debugging

- "Invalid block content" after changes:
  - Missing deprecation entry, changed markup without migration
- Block attributes not saving:
  - Missing `source` definition, wrong attribute type, serialization mismatch
- Block not appearing in inserter:
  - Registration failed, wrong category, PHP fatal error
- Styles not applying in editor:
  - Missing `editorStyle` in block.json, wrong asset path

Read:
- `references/debugging.md`

## Escalation

For canonical detail, consult:
- [Block Editor Handbook](https://developer.wordpress.org/block-editor/)
- [Block API Reference](https://developer.wordpress.org/block-editor/reference-guides/block-api/)
- [Gutenberg Storybook](https://wordpress.github.io/gutenberg/)
