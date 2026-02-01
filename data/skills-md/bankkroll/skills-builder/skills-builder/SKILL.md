---
name: "skills-builder"
description: "Build Claude Code skills from documentation websites. Scrapes Mintlify, ReadTheDocs/Sphinx, Docusaurus, GitBook, and static HTML sites. Generates properly formatted skills with SKILL.md and reference files. Use when: creating skills from docs, scraping documentation, generating reference materials from URLs."
---

# Skills Scraper

Build Claude Code skills directly from documentation websites.

## Quick Start

```bash
pip install requests beautifulsoup4 lxml playwright
playwright install chromium

python scripts/build.py https://mintlify.com/docs mintlify-docs
```

## Supported Platforms

| Platform      | Description              | Browser |
| ------------- | ------------------------ | ------- |
| `mintlify`    | Mintlify-powered docs    | Yes     |
| `readthedocs` | ReadTheDocs/Sphinx sites | No      |
| `docusaurus`  | Docusaurus/React docs    | Yes     |
| `gitbook`     | GitBook-powered sites    | Yes     |
| `generic`     | Static HTML sites        | No      |
| `auto`        | Auto-detect (default)    | -       |

## Usage

```bash
python scripts/build.py <url> <name> [options]
```

**Options:**

- `-o, --output` - Output directory (default: ./skills)
- `-p, --platform` - Platform (default: auto)
- `--max-pages N` - Limit pages (0 = unlimited)
- `--max-depth N` - Max crawl depth (default: 10)
- `--no-browser` - Disable Playwright
- `--no-sitemap` - Disable sitemap discovery
- `-v, --verbose` - Verbose output

## Examples

```bash
# Mintlify
python scripts/build.py https://resend.com/docs resend-api

# ReadTheDocs/Sphinx
python scripts/build.py https://flask.palletsprojects.com/en/stable/ flask-docs

# Docusaurus
python scripts/build.py https://reactnative.dev/docs/getting-started react-native

# GitBook
python scripts/build.py https://docs.cortex.io cortex-docs

# Static HTML
python scripts/build.py https://docs.python.org/3/ python-docs -p generic
```

## Output Structure

```
skill-name/
├── SKILL.md           # Metadata + instructions
└── references/        # Documentation files
    ├── api.md
    ├── getting-started.md
    └── ...
```

## Requirements

- Python 3.10+
- requests, beautifulsoup4, lxml
- playwright (for JS-rendered sites)
