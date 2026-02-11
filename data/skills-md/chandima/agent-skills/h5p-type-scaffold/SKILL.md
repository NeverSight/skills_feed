---
name: h5p-type-scaffold
description: Scaffold and guide creation of H5P content types. Use when asked "build an H5P type", "create an H5P content type", "scaffold an H5P library", or "start a new H5P".
allowed-tools: Read, Write, Bash(./scripts/*)
---

# H5P Content Type Scaffolder

Create a modern H5P content type starting from established boilerplates, with a minimal build pipeline and editor semantics.

## How It Works

1. Collect metadata (title, machine name, version, author, license).
2. Generate a boilerplate (default: SNORDIAN) that aligns with current H5P best practices.
3. Provide starter `library.json`, `semantics.json`, and JS/CSS entrypoints.
4. Outline build and packaging steps using `h5p-cli`.

## Concepts

- Content types are runnable libraries under `H5P.*` (`runnable: 1`).
- Editor widgets are non-runnable libraries under `H5PEditor.*` (`runnable: 0`).
- `semantics.json` defines the editor form schema and validation rules.
- Non-runnable dependency libraries (often `H5P.*` or `H5PApi.*`) are used as shared building blocks.

See `references/CONCEPTS.md` for details and official links.

## Usage

```bash
bash /mnt/skills/user/h5p-type-scaffold/scripts/scaffold.sh \
  --title "My Content Type" \
  --machine "H5P.MyContentType" \
  --kind "content" \
  --version "1.0.0" \
  --description "Short description" \
  --author "Your Name" \
  --license "MIT" \
  --template "snordian" \
  --out /path/to/output
```

Editor widget example:

```bash
bash /mnt/skills/user/h5p-type-scaffold/scripts/scaffold.sh \
  --title "My Editor Widget" \
  --machine "H5PEditor.MyWidget" \
  --kind "editor" \
  --out /path/to/output
```

## Output

- `library.json` and `semantics.json`
- `src/entries`, `src/scripts`, `src/styles`
- `README.md` (templates)
- `DEV.md` (templates, dev harness)
- Build config and lint config (varies by template)
- Templates live under `assets/templates/`

## Build & Package (h5p-cli)

- Install deps: `npm install`
- Build assets: `npm run build`
- Set up dev environment: `h5p core` then `h5p setup <library>`
- Run local editor/server: `h5p server`
- Pack to `.h5p`: `h5p pack <library> [my.h5p]` (see `h5p help pack`)

## Dev Harness (h5p-cli)

- Manual steps: `references/DEV-HARNESS.md`
- Helper script: `scripts/h5p-dev.sh`

## xAPI Integration

- Guidance: `references/XAPI.md` (emit + listen + platform notes)

See `references/H5P-CLI.md` for a fuller command overview and `references/CONTENT-TYPE-AUTHORING.md` for authoring essentials.

## Guidance (2024/2025 Best Practices)

- Default to the SNORDIAN boilerplate for linting, i18n scaffolding, and CI-ready conventions.
- Use the official `h5p/h5p-boilerplate` when you want the simplest baseline.
- Prefer vanilla JS for community maintainability.
- Use `h5p-cli` to pack and manage libraries.
- Validate semantics and editor UX early with a minimal field set.

## Related Community Patterns (Incorporated)

- H5P content is often embedded via iframe in LMS or CMS platforms.
- Common education-focused content types include Interactive Video, Course Presentation, Question Sets, Dialog Cards, and Timeline.
- When embedding, wrap iframes in a responsive container and apply safe, minimal styling.

## Templates

- `snordian` (default): Linting + i18n scaffolding + modern webpack config.
- `vanilla`: Official minimal boilerplate structure.
- `editor`: H5P editor widget boilerplate (`H5PEditor.*`).

## Additional Upstream Options (Not Bundled)

- `h5p/h5p-boilerplate` branches like `question-type` and `question-type-vue` for specialized starting points.
- `otacke/h5p-editor-boilerplate` for building custom H5P editor widgets.
- `NDLA-H5P/generator-h5p-content-type` if you prefer a Yeoman-based generator workflow.
- `tarmoj/h5p-react-boilerplate` for a React-based starter (note: appears stale).

## Troubleshooting

- If machine name is invalid, use `H5P.YourContentType`.
- For editor widgets, use `--kind editor` and a `H5PEditor.YourWidget` machine name.
- If versioning is unclear, start with `1.0.0` and update later.
- If build fails, ensure `node` and `npm` are installed and run `npm install`.
