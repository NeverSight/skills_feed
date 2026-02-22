---
name: convert-url-html-to-md
description: "Convert HTML web pages to Markdown for documentation extraction. Use when fetching documentation from websites, extracting structured content, getting clean main content (clean=true), or getting full page with nav/sidebar to discover URLs (clean=false). Ideal for learning libraries and building context from web sources."
---

# Convert URL HTML to Markdown

Extract web content as markdown using a two-phase approach for comprehensive documentation gathering.

## Two-Phase Workflow

For optimal documentation extraction:

1. **Discovery (clean=false)**: Get full page including navigation and sidebars to discover all documentation URLs
2. **Extraction (clean=true)**: Extract main content from discovered URLs

## Usage

```bash
# From the skill directory
cd ~/.claude/skills/convert-url-html-to-md

# Clean mode - main content only (recommended for docs)
node scripts/convert_url.js <url> --clean=true

# Full page mode - includes nav/sidebar (for discovering URLs)
node scripts/convert_url.js <url> --clean=false

# Default is clean=true
node scripts/convert_url.js <url>
```

## Examples

```bash
# Get all navigation links from a docs site
node scripts/convert_url.js https://ui.shadcn.com/docs --clean=false

# Extract specific documentation content
node scripts/convert_url.js https://ui.shadcn.com/docs/components/radix/aspect-ratio --clean=true
```

## Installation

Dependencies are included. Run once:

```bash
cd ~/.claude/skills/convert-url-html-to-md
npm install
```

## Output

The script outputs markdown directly to stdout. Redirect to file if needed:

```bash
node scripts/convert_url.js <url> --clean=true > output.md
```

## Credits

This skill is based on [urltomarkdown](https://github.com/macsplit/urltomarkdown) by [Lee Hanken](https://github.com/macsplit), licensed under MIT. Modified and adapted as a Claude skill by [1naichii](https://github.com/1naichii).
