---
name: pymupdf
description: PyMuPDF (fitz) - PDF manipulation library. Use for PDF text extraction, table detection, image extraction, and document parsing.
---

# Pymupdf Skill

Comprehensive assistance with pymupdf development, generated from official documentation.

## When to Use This Skill

This skill should be triggered when:
- Working with pymupdf
- Asking about pymupdf features or APIs
- Implementing pymupdf solutions
- Debugging pymupdf code
- Learning pymupdf best practices

## Quick Reference

### Common Patterns

**Pattern 1:** The name identifying the colorspace. Example: pymupdf.csCMYK.name = ‘DeviceCMYK’.

```
csRGB
```

**Pattern 2:** Added a method paper_rect() which returns a Rect for a supplied paper format string. Example: fitz.paper_rect(“letter”) = fitz.Rect(0.0, 0.0, 612.0, 792.0).

```
paper_rect()
```

**Pattern 3:** Example:

```
bottom-left -> top-left
```

**Pattern 4:** A typical use of this attribute would be setting Page.cropbox_position to this value, when you are creating shapes for later or external use. If you have not manipulated the attribute yourself, it should reflect a rectangle that contains all drawings so far.

```
Page.cropbox_position
```

**Pattern 5:** With Document.insert_file() you can invoke the method to merge supported files with PDF. For example:

```
Document.insert_file()
```

**Pattern 6:** Example:

```
Page.cropbox_position()
```

**Pattern 7:** pix is a Pixmap object which (in this case) contains an RGB image of the page, ready to be used for many purposes. Method Page.get_pixmap() offers lots of variations for controlling the image: resolution / DPI, colorspace (e.g. to produce a grayscale image or an image with a subtractive color scheme), transparency, rotation, mirroring, shifting, shearing, etc. For example: to create an RGBA image (i.e. containing an alpha channel), specify pix = page.get_pixmap(alpha=True).

```
pix
```

**Pattern 8:** Please see the Stories recipes for a number of typical use cases.

```
Document.convert_to_pdf()
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **_images.md** -  Images documentation
- **api.md** - Api documentation
- **index.html.md** - Index.Html documentation
- **other.md** - Other documentation
- **tutorials.md** - Tutorials documentation

Use `view` to read specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners
Start with the getting_started or tutorials reference files for foundational concepts.

### For Specific Features
Use the appropriate category reference file (api, guides, etc.) for detailed information.

### For Code Examples
The quick reference section above contains common patterns extracted from the official docs.

## Resources

### references/
Organized documentation extracted from official sources. These files contain:
- Detailed explanations
- Code examples with language annotations
- Links to original documentation
- Table of contents for quick navigation

### scripts/
Add helper scripts here for common automation tasks.

### assets/
Add templates, boilerplate, or example projects here.

## Notes

- This skill was automatically generated from official documentation
- Reference files preserve the structure and examples from source docs
- Code examples include language detection for better syntax highlighting
- Quick reference patterns are extracted from common usage examples in the docs

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information
