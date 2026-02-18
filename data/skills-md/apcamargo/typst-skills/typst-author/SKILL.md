---
name: typst-author
description: Generate idiomatic Typst (.typ) code, edit existing Typst files, and answer Typst syntax questions. Use when working with Typst files (*.typ) or when the user mentions Typst markup, document creation, or formatting.
---

# typst-author skill

## Overview

This skill helps agents generate, edit, and reason about Typst documents. It provides quick‑start examples, detailed workflows, and links to the full Typst documentation (guides, tutorials, reference).

## Minimal document example

```typst
#set document(title: "My Document", author: "Author Name")
#set page(numbering: "1")
#set text(lang: "en")

// Enable paragraph justification and character-level justification
#set par(
  justify: true,
  justification-limits: (
    tracking: (min: -0.012em, max: 0.012em),
    spacing: (min: 75%, max: 120%),
  )
)

#title[My Document]

= Heading 1

This is a paragraph in Typst.

== Heading 2

#lorem(50)
```

## Workflows

- **Creating a new Typst project**: Use the "Minimal document example" above as a starting point. Skim the tutorial for the basics ([docs/tutorial/writing-in-typst.md](docs/tutorial/writing-in-typst.md)), then create the `.typ` file(s).
- **Editing existing content**: Locate the target text and apply changes; confirm syntax against the reference when needed ([docs/reference/](docs/reference/)).
- **Formatting & Styling**: Consult the styling guide ([docs/reference/styling.md](docs/reference/styling.md)) for `set rule`, `show rule`, and custom themes.

## Documentation

- **Guides**: `docs/guides/*.md`
- **Tutorials**: `docs/tutorial/*.md`
- **Full reference tree**: `docs/reference/**/*.md`

## Detailed instructions

1. **PRIORITY: Trust local documentation**. Your internal training data regarding Typst may be outdated or hallucinated. Always verify function names, parameters, and syntax against the local `docs/` folder before generating code.
2. **Read the relevant documentation** (use `Read`/`Grep`/`Glob` on the paths above).
3. **Generate or modify the `.typ` source** according to the user's request.
4. **Validate** the generated Typst by running `typst compile` (if tool access is allowed).
5. **Provide the final `.typ` content** and optionally a rendered preview (PDF/HTML).

## Quick syntax reference

### Critical distinctions

- **Arrays**: `(item1, item2)` (parentheses). See [docs/reference/foundations/array.md](docs/reference/foundations/array.md).
- **Dictionaries**: `(key: value, key2: value2)` (parentheses with colons). See [docs/reference/foundations/dictionary.md](docs/reference/foundations/dictionary.md).
- **Content blocks**: `[markup content]` (square brackets). See [docs/reference/foundations/content.md](docs/reference/foundations/content.md).
- **NO tuples**: Typst only has arrays.

### Hash usage (markup vs code)

- Use `#` to start a code expression inside markup or content blocks; it disambiguates code from text. This is required for content-producing function calls and field access in markup: `#figure[...]`, `#image("file.png")`, `text(...)[#numbering(...)]`.
- Do not use `#` inside code contexts (argument lists, code blocks, show-rule bodies). Example: `#figure(image("file.png"))` (no `#` before `image`).
- Reference: [docs/reference/scripting.md](docs/reference/scripting.md), [docs/tutorial/writing-in-typst.md](docs/tutorial/writing-in-typst.md)

```typst
// Incorrect (missing # inside content block)
text(...)[(numbering(...))]

// Correct
text(...)[(#numbering(...))]
```

### Styling rules: set vs show

- `set`: Set rule to configure optional parameters on element functions (style defaults scoped to the current block or file).
- `show`: Show rule to target selected elements and apply a set rule or transform/replace the element output.
- Use `set` for common styling; use `show` for selective or structural changes (e.g., `heading.where(level: 1)`, labels, text, regex).

```typst
// Set rule: configure optional parameters for an element type
#set heading(numbering: "I.")
#set text(font: "New Computer Modern")

// Show-set rule: apply a set rule only to selected elements
#show heading: set text(navy)

// Show transform rule: replace/reshape element output
#show heading: it => block[#emph(it.body)]
```

## Common mistakes to avoid

- Calling things "tuples" (Typst only has arrays).
- Using `[]` for arrays (use `()` instead).
- Accessing array elements with `arr[0]` (use `arr.at(0)`).
- Omitting `#` in markup/content blocks (e.g., `text(...)[numbering(...)]` should be `text(...)[#numbering(...)]`).
- Using `#` inside code contexts (e.g., `figure(#image("x.png"))` in an argument list).
- Mixing up content blocks `[]` with code blocks `{}`.
- Forgetting to include the namespace when accessing imported variables/functions (e.g., use `color.hsl` instead of just `hsl`).
- Using LaTeX syntax (do **NOT** use `\begin{...}`, `\section`, or other LaTeX commands).
- Hallucinating environments (e.g., `tabular` does not exist; use `table`).

## Advanced features

- **Custom themes**: See [docs/reference/styling.md](docs/reference/styling.md) for theme creation.
- **Scripting**: Use Typst's scripting capabilities ([docs/reference/scripting.md](docs/reference/scripting.md)) for automatic generation.
- **Math and visualisation**: Reference [docs/reference/math/](docs/reference/math/) and [docs/reference/visualize/](docs/reference/visualize/) for formulas and diagrams.

### For large projects

When working on large projects, consider organizing the project across multiple files.

- Use `#include "file.typ"` to split into multiple files
- Relevant documentation: [docs/reference/foundations/module.md](docs/reference/foundations/module.md)

## Troubleshooting

### Missing font warnings

If you see "unknown font family" warnings, remove the font specification to use system defaults. Note: Font warnings don't prevent compilation; the document will use fallback fonts.

### Template/Package not found

If import fails with "package not found":

- Verify exact package name and version on Typst Universe.
- Check for typos in `@preview/package:version` syntax.
- **Remember**: Typst uses fully qualified imports with specific versions - there's no package cache to update.

### Compilation errors

Common fixes:

- **"expected content, found ..."**: You're using code where markup is expected - wrap in `#{ }` or use proper syntax.
- **"expected expression, found ..."**: Missing `#` (or `#(...)`) in markup/content blocks.
- **"unknown variable"**: Check spelling, ensure imports are correct.
- **Array/dictionary errors**: Review syntax - use `()` for both, dictionaries need `key: value`, singleton arrays are `(elem,)`.
