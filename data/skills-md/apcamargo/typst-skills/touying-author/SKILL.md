---
name: touying-author
description: Author, refactor, and troubleshoot Typst slide decks built with Touying
---

# Touying Author

Guide Typst presentation authoring with Touying, emphasizing clean structure, repeatable configuration, and slide-safe patterns.

## Quick start
- Import Touying and a theme, then apply the theme with `#show: <theme>.with(...)`.
- Keep configuration centralized; include slide content from separate files.
- Use headings to create slides; use `#slide` for custom layouts or animations.
- Start from `examples/simple.typ` for a minimal deck, or `examples/default.typ` for the bare theme.

Snippet from `examples/simple.typ`:

```typst
#import "@preview/touying:0.6.1": *
#import themes.simple: *

#show: simple-theme.with(
  aspect-ratio: "16-9",
  footer: [Simple slides],
)
```

## Best practices and code structure

- Use a single entry file (e.g., `main.typ`) that applies `#show` and all `config-*` calls.
- For multi-file decks, follow the `globals.typ` + `main.typ` + `content.typ` pattern; use `#include` for content and `#import` for globals to avoid circular refs.
- Docs use both `config.typ` (see `docs/start.md`) and `globals.typ` (see `docs/multi-file.md`) for the shared config file; pick one name and use it consistently in your project.
- For large decks, move `content.typ` into `sections/` and include `sections/content.typ` (and optional `sections/another-section.typ`) from `main.typ`.
- Prefer `config-page`, `config-common`, `config-info`, `config-colors`, `config-methods`, and `config-store` over direct `set page` or ad-hoc global `show`.
- Use headings for most slides; use `config-common(slide-level: n)` to choose which heading levels create slides.
- Use `#slide` only for custom layout or animation; always wrap slide functions with `touying-slide-wrapper`.
- For callback-style animation (`#slide(repeat: n, self => [...])`), set `repeat` explicitly and use `utils.methods(self)` to access `uncover`, `only`, and `alternatives`.

### Single-file structure

```
.
├── globals.typ
├── main.typ
└── content.typ
```

### Multi-file structure

```
.
├── globals.typ
├── main.typ
└── sections/
    ├── content.typ
    └── another-section.typ
```

## Core API map (exports)

- Slides: `touying-slides`, `slide`, `touying-slide`, `touying-slide-wrapper`, `empty-slide`
- Dynamics: `pause`, `meanwhile`, `uncover`, `only`, `effect`, `alternatives`, `alternatives-match`, `alternatives-fn`, `alternatives-cases`
- Config: `config-common`, `config-page`, `config-info`, `config-colors`, `config-methods`, `config-store`, `default-config`, `touying-set-config`, `appendix`
- Utilities: `utils.*` (fit-to-height, fit-to-width, cover helpers, progress, heading helpers)
- Components: `components.side-by-side`, `components.adaptive-columns`, `components.progressive-outline`, `components.custom-progressive-outline`
- Integrations: `touying-reducer`, `touying-equation`, `touying-mitex`, `speaker-note`, `pdfpc.*`
- Recall: `touying-recall`, `touying-fn-wrapper`

## Slide structure and headings

- Use heading labels to control numbering/outline/bookmarks: use `<touying:hidden>` (see `docs/code-styles.md`), and see `docs/changelog.md` for `<touying:unnumbered>`, `<touying:unoutlined>`, `<touying:unbookmarked>`, and `<touying:skip>`.
- Use `components.adaptive-columns(outline(...))` for a table of contents slide; use `components.progressive-outline` for progress-aware outlines.
- Use `== <touying:hidden>` to insert a blank title slide and clear the previous heading context.
- Use `#pagebreak()` or `---` to split slides without changing headings.
- Use `#empty-slide[...]` for slides without header/footer.
- Use `config-common(handout: true)` to keep only the last subslide per slide in handout output.
- Use `#show: appendix` to freeze last-slide counts after the main deck.

Snippet from `examples/default.typ`:

```typst
= Outline <touying:hidden>

#components.adaptive-columns(outline(title: none, indent: 1em))
```

## Animations and dynamic content

- Use `#pause` and `#meanwhile` for simple reveals; avoid using them inside `context` where marks are not supported.
- Use `#uncover` to reserve layout space; use `#only` to remove layout space when hidden.
- When marks cause warnings, use callback-style slides with `repeat` and `utils.methods(self)`.
- For math animations, use `pause`/`meanwhile` inside `$ ... $`; use `touying-equation` when you need the helper for inline equation text (you can also use `#pause` or `#pause;`).
- See `examples/example.typ` for simple/complex/callback animations and equation animations.

Snippet from `examples/simple.typ`:

```typst
== Dynamic slide

Did you know that...

#pause

...you can see the current section at the top of the slide?
```

Snippet from `examples/example.typ`:
```typst
#slide(
  repeat: 3,
  self => [
    #let (uncover, only, alternatives) = utils.methods(self)

    At subslide #self.subslide, we can

    use #uncover("2-")[`#uncover` function] for reserving space,

    use #only("2-")[`#only` function] for not reserving space,

    #alternatives[call `#only` multiple times \u{2717}][use `#alternatives` function #sym.checkmark] for choosing one of the alternatives.
  ],
)
```

## Layout and theming
- Use `composer` in `#slide` for columns; pass `(1fr, 2fr)` or a custom `grid` function.
- Use `config-page` for margin, header, footer, and background; do not use `set page` directly.
- Use `config-methods(cover: utils.semi-transparent-cover.with(alpha: 85%))` only when layout changes are acceptable.
- Use `config-store` to stash theme-specific values for headers/footers or navigation elements.
- Use `config-common(new-section-slide-fn: none)` to disable automatic section slides, or provide a custom function to replace them.
- Apply global styles either around `#show: <theme>.with(...)` or via `config-methods(init: ...)` in a theme.
- Use `config-info(...)` for title/author/date and `config-common(datetime-format: ...)` to control date formatting.

Snippet from `examples/default.typ`:

```typst
#import "@preview/touying:0.6.1": *
#import themes.default: *

#import "@preview/numbly:0.1.0": numbly

#show: default-theme.with(
  aspect-ratio: "16-9",
  config-common(
    slide-level: 3,
    zero-margin-header: false,
  ),
  config-colors(primary: blue),
  config-methods(alert: utils.alert-with-primary-color),
  config-page(
    header: text(gray, utils.display-current-short-heading(level: 2)),
  ),
)
```

## Speaker notes and presenter tools

- Add notes with `#speaker-note[...]`.
- Show notes on second screen with `config-common(show-notes-on-second-screen: right)` or `bottom`.
- Export pdfpc metadata with `enable-pdfpc: true` and `typst query --field value --one "<pdfpc-file>"`.

## Use bundled docs and examples

- Read only the specific docs needed for the task; avoid loading the full docs tree.
- Read `docs/start.md` and `docs/intro.md` for basics and import patterns.
- Read `docs/multi-file.md` for multi-file layout and include patterns.
- Read `docs/layout.md` and `docs/sections.md` for slide-level and heading behavior.
- Read `docs/code-styles.md` for simple vs block style and pagination tricks.
- Read `docs/global-settings.md` for global styles and `config-info` usage.
- Read `docs/dynamic/*.md` for `pause`, `meanwhile`, cover behavior, and equation animation.
- Read `docs/themes/*.md` for theme-specific APIs and defaults.
- Read `docs/external/*.md` for pdfpc and Pympress usage.
- Read `docs/integration/*.md` for CeTZ/Fletcher/Theorion/MiTeX integrations.
- Use `examples/*.typ` as working templates for each theme.

## File tree (docs and examples)

```
docs/
├── build-your-own-theme.md
├── changelog.md
├── code-styles.md
├── dynamic
│   ├── complex.md
│   ├── cover.md
│   ├── equation.md
│   ├── handout.md
│   ├── other.md
│   └── simple.md
├── external
│   ├── pdfpc.md
│   ├── pympress.md
│   └── typst-preview.md
├── global-settings.md
├── integration
│   ├── cetz.md
│   ├── codly.md
│   ├── fletcher.md
│   ├── mitex.md
│   ├── pinit.md
│   └── theorion.md
├── intro.md
├── layout.md
├── multi-file.md
├── progress
│   ├── counters.md
│   └── sections.md
├── sections.md
├── start.md
├── themes
│   ├── aqua.md
│   ├── custom.md
│   ├── dewdrop.md
│   ├── metropolis.md
│   ├── simple.md
│   ├── stargazer.md
│   └── university.md
└── utilities
    └── fit-to.md

examples/
├── aqua-zh.typ
├── aqua.typ
├── default.typ
├── dewdrop.typ
├── example.typ
├── metropolis.typ
├── simple.typ
├── stargazer.typ
└── university.typ
```
