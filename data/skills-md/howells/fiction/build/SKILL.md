---
name: build
description: Build an EPUB from your fiction project. Compiles chapters, metadata, and optionally a cover image.
argument-hint: "[--sync] [--cover file.png] [path]"
disable-model-invocation: true
---

Build an EPUB file from the current fiction project.

## Build Context

- Chapter count: !`ls chapters/*.md 2>/dev/null | wc -l | tr -d ' '`
- Has cover: !`ls covers/cover.* 2>/dev/null | head -1 || echo "no cover found"`

## What This Does

1. Reads project metadata from README.md
2. Compiles all chapters from `chapters/` in order
3. Applies styling from `epub.css` (if present)
4. Includes cover image from `covers/` (if specified)
5. Sets a stable EPUB identifier (preserves highlights across builds)
6. Outputs to `builds/` directory

## Usage

```
/fiction:build                    # Build dated epub (archive mode)
/fiction:build --sync             # Build for Apple Books sync (preserves highlights)
/fiction:build --cover cover.png  # Include specific cover image
/fiction:build /path/to/project   # Build specific project
```

If arguments provided: $ARGUMENTS

## Build Modes

### Archive Mode (default)

Outputs: `builds/YYYY-MM-DD/project-name-YYYY-MM-DD.epub`

- Each build is date-stamped
- Preserves history of versions
- Good for milestones and backups

### Sync Mode (`--sync`)

Outputs: `builds/project-name.epub`

- Same filename every time
- Uses stable EPUB identifier
- **Preserves highlights and reading position in Apple Books**
- Ideal for reading on devices while writing

## What to Do

### 1. Find Project Root

Look for README.md, chapters/ directory. Support both flat and part-based structures:

**Flat structure:**
```
chapters/01-chapter.md
chapters/02-chapter.md
```

**Part-based structure:**
```
part-1-name/chapters/01-chapter.md
part-2-name/chapters/10-chapter.md
```

### 2. Gather Metadata

Extract from README.md:
- **Title** — Project name (H1 heading)
- **Author** — From frontmatter or infer from git config
- **Description** — From "The Story" section or premise

### 3. Generate Identifier

Create a stable identifier for the EPUB:
```
com.author-name.project-name
```

This identifier is what Apple Books uses to recognize "same book, updated" — preserving highlights and reading position between builds.

### 4. Collect Chapters

Read all markdown files from `chapters/` in order:
- Sort by filename (01-chapter.md, 02-chapter.md, etc.)
- For part-based projects, read parts in order (part-1, part-2, etc.)
- Convert markdown to HTML
- Preserve chapter breaks

### 5. Check for Cover

Look in `covers/` for:
- `cover.png` or `cover.jpg` (default)
- Or use `--cover` argument to specify

### 6. Check for Styles

Look for `epub.css` in project root. If present, include in epub.

### 7. Build EPUB

Create a metadata file with the stable identifier:
```yaml
---
title: "Book Title"
author: "Author Name"
identifier: "com.author-name.book-title"
lang: en-GB
---
```

Use pandoc to compile:
```bash
pandoc chapters/*.md \
  --metadata-file=/tmp/metadata.yaml \
  -o "builds/project-name.epub" \
  --epub-cover-image=covers/cover.png \
  --css=epub.css \
  --split-level=1 \
  --toc \
  --toc-depth=1
```

**Key options:**
- `--split-level=1` — Only break chapters on H1 headings (avoids empty pages)
- `--toc` — Include table of contents
- `--toc-depth=1` — Only show chapter titles in TOC

### 8. Create Metadata File (Archive Mode)

Write `builds/YYYY-MM-DD/metadata.yaml`:
```yaml
title: "Book Title"
author: "Author Name"
identifier: "com.author-name.book-title"
built: "2026-01-18T21:30:00Z"
chapters: 18
word_count: 75000
cover: "cover.png"
```

### 9. Report Build

Output build summary:
```
## Build Complete

**File:** builds/project-name.epub
**Size:** 8.4 MB
**Chapters:** 18
**Word count:** ~75,000

Cover: covers/cover.png included
Styles: epub.css applied

To open in Apple Books:
  open -a 'Books' builds/project-name.epub
```

## Build Directory Structure

### Archive Mode
```
builds/
├── 2026-01-15/
│   ├── project-name-2026-01-15.epub
│   └── metadata.yaml
└── 2026-01-18/
    ├── project-name-2026-01-18.epub
    └── metadata.yaml
```

### Sync Mode
```
builds/
└── project-name.epub    # Always same file, updated in place
```

## Apple Books Sync

For highlights to persist between builds:

1. **Same identifier** — The `identifier` field in metadata must stay constant
2. **Same filename** — Use `--sync` mode for consistent naming
3. **iCloud sync enabled** — Both Mac and iPhone need Books enabled in iCloud settings

**How it works:** Apple Books uses the EPUB's `dc:identifier` (stored in the OPF file) to recognize books. When you import a new build with the same identifier, it updates the existing book rather than adding a duplicate.

**Caveat:** Highlights are tied to text position. Major edits (adding/removing paragraphs) may shift or orphan highlights in that area. Minor edits (typos, word changes) are fine.

## Covers Directory

```
covers/
├── cover-01-concept.png      # Early iterations
├── cover-02-revised.png      # Refinements
├── cover-final.png           # Selected cover
└── cover.png                 # Symlink or copy of final (used by build)
```

Store all cover iterations. The build uses `cover.png` by default.

## Dependencies

Requires `pandoc` for epub generation:
```bash
brew install pandoc
```

## Tips

- Use `--sync` for daily reading while writing
- Use archive mode (default) for milestone builds
- Test epub in Apple Books, Kindle Previewer, or Calibre
- The `covers/` directory is for iterations; `cover.png` is what gets built

## After Building

- Open in Apple Books to test formatting
- Check chapter breaks and styling
- Verify cover displays correctly
- For sync mode, delete old version in Books first if highlights don't update

## Troubleshooting

### Highlights Not Persisting

1. Ensure you're using `--sync` mode
2. Check that the identifier hasn't changed
3. Try deleting the old book from Apple Books, then importing fresh
4. Verify iCloud sync is enabled for Books on both devices

### Empty Pages

If you see blank pages between chapters:
1. Check for `page-break-after: always` in epub.css — remove or change to `auto`
2. Look for double line breaks or `\newpage` in markdown files
3. Ensure `--split-level=1` is set (breaks only on H1)
4. Check chapter files don't end with multiple blank lines

### Recommended epub.css

Minimal CSS that avoids empty page issues:
```css
body {
  font-family: Georgia, serif;
  line-height: 1.6;
}
h1 {
  page-break-before: auto;
  margin-top: 2em;
}
p {
  text-indent: 1.5em;
  margin: 0;
}
p:first-of-type {
  text-indent: 0;
}
```
