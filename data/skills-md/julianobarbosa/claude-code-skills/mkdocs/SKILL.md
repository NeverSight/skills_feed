---
name: mkdocs
description: Build project documentation sites with MkDocs static site generator. USE WHEN user mentions mkdocs, documentation site, docs site, project documentation, OR wants to create, configure, build, or deploy documentation using Markdown. Covers installation, configuration, theming, plugins, and deployment.
---

# MkDocs Documentation Site Generator

MkDocs is a fast, simple static site generator for building project documentation from Markdown files. Configuration uses a single YAML file (`mkdocs.yml`).

## Quick Start

### Installation

```bash
# Install MkDocs
pip install mkdocs

# Verify installation
mkdocs --version
```

### Create New Project

```bash
# Create project structure
mkdocs new my-project
cd my-project

# Start development server
mkdocs serve
```

**Project Structure Created:**
```
my-project/
├── mkdocs.yml      # Configuration file
└── docs/
    └── index.md    # Homepage
```

### Minimal Configuration

```yaml
# mkdocs.yml
site_name: My Project
site_url: https://example.com/
nav:
  - Home: index.md
  - About: about.md
```

## Core Commands

| Command | Purpose |
|---------|---------|
| `mkdocs new PROJECT` | Create new project |
| `mkdocs serve` | Start dev server (localhost:8000) |
| `mkdocs build` | Build static site to `site/` |
| `mkdocs gh-deploy` | Deploy to GitHub Pages |
| `mkdocs get-deps` | Show required packages |

**Common Options:**
- `-f, --config-file FILE` - Use custom config file
- `-s, --strict` - Fail on warnings
- `-d, --site-dir DIR` - Custom output directory
- `--dirty` - Only rebuild changed files
- `--clean` - Clean output before build

## Project Structure

```
project/
├── mkdocs.yml              # Configuration (required)
├── docs/
│   ├── index.md            # Homepage
│   ├── about.md            # Additional pages
│   ├── user-guide/
│   │   ├── index.md        # Section homepage
│   │   ├── getting-started.md
│   │   └── configuration.md
│   ├── img/                # Images
│   │   └── logo.png
│   └── css/                # Custom CSS
│       └── extra.css
└── custom_theme/           # Theme customizations (optional)
    └── main.html
```

## Navigation Configuration

```yaml
# Automatic navigation (alphabetically sorted)
# Omit nav key to auto-generate

# Explicit navigation with sections
nav:
  - Home: index.md
  - User Guide:
    - Getting Started: user-guide/getting-started.md
    - Configuration: user-guide/configuration.md
  - API Reference: api/
  - External Link: https://example.com/
```

## Writing Documentation

### Internal Links

```markdown
# Link to another page
[See Configuration](configuration.md)

# Link to page in another directory
[Installation](../getting-started/installation.md)

# Link to section anchor
[See Options](configuration.md#options)
```

### Page Metadata

```yaml
---
title: Custom Page Title
description: Page description for SEO
authors:
  - John Doe
date: 2024-01-01
---

# Page Content Here
```

### Code Blocks

````markdown
```python
def hello():
    print("Hello, World!")
```
````

### Tables

```markdown
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
```

## Theme Configuration

### Built-in Themes

```yaml
# Default MkDocs theme
theme:
  name: mkdocs
  color_mode: auto           # light, dark, auto
  user_color_mode_toggle: true
  nav_style: primary         # primary, dark, light
  highlightjs: true
  navigation_depth: 2
  locale: en

# ReadTheDocs theme
theme:
  name: readthedocs
  prev_next_buttons_location: bottom
  navigation_depth: 4
  collapse_navigation: true
```

### Material for MkDocs (Popular Third-Party)

```bash
pip install mkdocs-material
```

```yaml
theme:
  name: material
  palette:
    primary: indigo
    accent: indigo
  features:
    - navigation.tabs
    - navigation.sections
    - search.suggest
```

### Custom CSS/JavaScript

```yaml
extra_css:
  - css/extra.css

extra_javascript:
  - js/extra.js
  - path: js/analytics.mjs
    type: module
```

## Plugins

```yaml
plugins:
  - search:
      lang: en
      min_search_length: 3
  - tags
  - blog
```

**Popular Plugins:**
- `search` - Full-text search (built-in, enabled by default)
- `blog` - Blog functionality (Material theme)
- `tags` - Content categorization
- `social` - Social media cards

> **Note:** Defining `plugins` disables defaults. Add `- search` explicitly.

## Markdown Extensions

```yaml
markdown_extensions:
  - toc:
      permalink: true
      separator: "-"
  - tables
  - fenced_code
  - admonition
  - pymdownx.highlight
  - pymdownx.superfences
```

## Deployment

### GitHub Pages

```bash
# Deploy to gh-pages branch
mkdocs gh-deploy

# With options
mkdocs gh-deploy --force --message "Deploy docs"
```

### Build for Any Host

```bash
# Build static files
mkdocs build

# Files output to site/ directory
# Upload to any static host
```

### Custom Domain

Create `docs/CNAME` file:
```
docs.example.com
```

## Common Workflows

### New Documentation Project

1. Create project: `mkdocs new my-docs`
2. Edit `mkdocs.yml` with site_name and nav
3. Add Markdown files to `docs/`
4. Preview: `mkdocs serve`
5. Build: `mkdocs build`
6. Deploy: `mkdocs gh-deploy`

### Add New Section

1. Create directory: `docs/new-section/`
2. Add `index.md` and content files
3. Update `nav` in `mkdocs.yml`
4. Preview and verify links

### Customize Theme

1. Set `theme.custom_dir: custom_theme/`
2. Create override files matching theme structure
3. Use template blocks to extend base templates

## Detailed References

- **Configuration options:** See [references/configuration.md](references/configuration.md)
- **Theme customization:** See [references/themes.md](references/themes.md)
- **Plugin development:** See [references/plugins.md](references/plugins.md)
- **Deployment strategies:** See [references/deployment.md](references/deployment.md)
- **Best practices:** See [references/best-practices.md](references/best-practices.md)
