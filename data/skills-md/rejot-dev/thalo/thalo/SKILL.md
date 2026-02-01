---
name: thalo
description:
  "Use when working with Thalo (Thought And Lore Language): creating or editing .thalo files or
  thalo code blocks in Markdown, setting up a knowledge base with thalo-cli (init, check,
  actualize), defining entities/syntheses, or generating an AGENTS.md guide for collaborators."
---

# Thalo

## Quick start workflow

- Initialize a knowledge base with `thalo init` to generate `entities.thalo`, `AGENTS.md`, and
  `personal-bio.md`.
- Add or edit entries in `*.thalo` files or fenced code blocks inside Markdown (lang: `thalo`).
- Validate after changes with `thalo check` to catch schema, link, and syntax issues.
- Format with `thalo format` when preparing a commit or cleanup (or use Prettier with the plugin)
- Run `thalo actualize` to materialize syntheses (queries + prompt) for LLM use.

## Entry syntax

Follow this structure:

```text
{timestamp} {directive} {entity} "Title" [^link-id] [#tags...]
  {key}: {value}
  ...

  # Section
  {content}
```

Guidelines:

- Use ISO 8601 local time with timezone, e.g. `2026-01-05T15:30Z`.
- Use `create` for new entries and `update` for modifications.
- Provide a stable `^link-id` when you want to reference the entry elsewhere.
- Put all content inside sections; required sections are defined in `entities.thalo`.
- Entities are typically `journal`, `opinion`, `reference`, or `lore` (see `entities.thalo`).

## Metadata

Metadata fields are indented key-value pairs. Values can be:

- Strings: `author: "Jane Doe"` or unquoted `author: Jane Doe`
- Links: `subject: ^self` or `related: ^my-other-entry`
- Dates: `published: 2023-03-16`
- Date ranges: `date: 2020 ~ 2021`

## Sections

Content sections start with `# SectionName` (indented). **All content must be within a section.**
Each entity type defines which sections are required/optional in `entities.thalo`.

## Defining entities

Define or update entities in `entities.thalo` using `define-entity` blocks. Each entity specifies:

- **Metadata** fields with types (`string`, `link`, `datetime`, `date-range`, enums, arrays,
  unions).
- **Sections** that determine required/optional content.

After editing or adding entries or entities, generally run `thalo check` to validate.

If you need the default entity templates, load `references/entities.thalo.txt`.

## Syntheses

Syntheses are queries plus prompts that let you generate structured summaries or narratives.

- Create with `define-synthesis` blocks.
- Use `sources:` to select entries by entity, tag, or metadata filters.
- Run `thalo actualize` to output the sources and prompt for downstream LLM use.

## Working in Markdown

Thalo can live inside Markdown files. The fenced code block language SHOULD be `thalo` (don't use it
in this file as an example because it would be parsed):

````text
```text
...entries...
```
````

The CLI and LSP will parse fenced `thalo` blocks in `.md` files.

## Installation

If `thalo` is not available, install via the user's package manager (local or global):

```bash
# Local (recommended for repo tooling)
npm install --save-dev @rejot-dev/thalo-cli

# Or with your preferred PM:
pnpm add -D @rejot-dev/thalo-cli
yarn add -D @rejot-dev/thalo-cli

# Global (optional)
npm install -g @rejot-dev/thalo-cli
```

## Prettier integration

This repo uses the Thalo Prettier plugin. The config is in `prettier.config.mjs` and includes:

```js
plugins: ["@rejot-dev/thalo-prettier"];
```

Use `thalo format` for CLI formatting, or run Prettier normally and it will format Thalo/Markdown
with the plugin enabled.

## CLI reference (condensed)

- `thalo init [directory]` (options: `--dry-run`, `--force`) creates `entities.thalo`, `AGENTS.md`,
  `personal-bio.md`.
- `thalo check [paths...]` validates syntax, metadata, sections, links, enums. Options include
  `--format`, `--severity`, `--max-warnings`, `--rule`, `--watch`, `--file-type`.
- `thalo format [paths...]` formats `.thalo` and `.md` (options: `--check`, `--write`,
  `--file-type`).
- `thalo actualize [links...]` outputs pending synthesis updates and prompts. Supports `-i` for
  custom instructions templates. Tracks changes via git or timestamps.
- `thalo query "<query>" [paths...]` filters by entity, tags, links, metadata. Options: `--format`,
  `--limit`.
- `thalo rules list` shows validation rules (filter by `--severity`, `--category`, `--json`).
- `thalo lsp` starts the language server (stdio).
- Global: `--help`, `--version`.

## References

- Use `references/entities.thalo.txt` for the default entity definitions from `thalo init`.
- Use `references/example-entries.thalo.txt` for sample entries.
- Use `references/scripting-api.md` for the scripting API summary.
- Use `date -u +"%Y-%m-%dT%H:%MZ"` to generate timestamps quickly.
