---
name: beautiful-mermaid-ascii
description: Render Mermaid diagrams as readable ASCII/Unicode art in the terminal (from .mmd/.mermaid files, stdin, or Markdown ```mermaid fences). Use when installing or using lukilabs/beautiful-mermaid, creating a CLI renderer for Mermaid-to-ASCII output, previewing Mermaid diagrams in terminal, or extracting/rendering Mermaid blocks from Markdown files.
---

# Beautiful Mermaid ASCII Rendering

Use `lukilabs/beautiful-mermaid` (a JS library, not a CLI) to turn Mermaid diagrams into terminal-friendly ASCII/Unicode art.

## Quick start

Render a Mermaid file:

```bash
skills/beautiful-mermaid-ascii/scripts/mermaid-ascii path/to/diagram.mmd
```

Install a clean `mermaid-ascii` command on your PATH (symlink into `~/.local/bin` by default):

```bash
skills/beautiful-mermaid-ascii/scripts/install-mermaid-ascii
```

Render from stdin:

```bash
cat path/to/diagram.mmd | skills/beautiful-mermaid-ascii/scripts/mermaid-ascii
```

Render the first Mermaid fenced block from Markdown:

```bash
skills/beautiful-mermaid-ascii/scripts/mermaid-ascii --md README.md
```

Select a different fenced block (1-based):

```bash
skills/beautiful-mermaid-ascii/scripts/mermaid-ascii --md README.md --block 2
```

## Installation approach (how this skill “deals with installing”)

`scripts/mermaid-ascii` auto-installs `beautiful-mermaid` into a writable cache directory (defaults to `$XDG_CACHE_HOME/beautiful-mermaid-ascii`, or `/tmp/beautiful-mermaid-ascii`) when needed, then runs the renderer.

If you want a “real” command on your PATH, prefer the symlink installer:

```bash
skills/beautiful-mermaid-ascii/scripts/install-mermaid-ascii
```

You can also install this folder as a local/global npm package (use a writable npm cache if your `~/.npm` is not writable):

```bash
# from the repo root
NPM_CONFIG_CACHE=/tmp/npm-cache npm install -g --prefix ~/.local ./skills/beautiful-mermaid-ascii
```

If you already have `beautiful-mermaid` installed in the current project, run with:

```bash
skills/beautiful-mermaid-ascii/scripts/mermaid-ascii --pkg-dir . path/to/diagram.mmd
```

## Troubleshooting

- If installs fail due to permission errors in `~/.npm` or `~/Library/Caches`, run with a writable cache directory:
  - `skills/beautiful-mermaid-ascii/scripts/mermaid-ascii --cache-dir /tmp/bm-cache ...`
- If output is empty, verify the Mermaid text is valid and starts with a diagram type (`flowchart`, `sequenceDiagram`, etc.).
- For multiple diagrams in Markdown, use `--list` to enumerate fenced blocks and choose one with `--block`.

## Bundled resources

- `skills/beautiful-mermaid-ascii/scripts/mermaid-ascii`: Shell wrapper that ensures dependencies are available, then renders.
- `skills/beautiful-mermaid-ascii/scripts/mermaid-ascii.mjs`: Node CLI that extracts Mermaid (raw or from Markdown fences) and calls `renderMermaidAscii`.
- `skills/beautiful-mermaid-ascii/references/notes.md`: Small notes about Mermaid inputs and common patterns.
