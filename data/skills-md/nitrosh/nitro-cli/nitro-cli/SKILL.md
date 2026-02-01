---
name: nitro-cli
description: Build static sites with Nitro CLI - a Python static site generator using nitro-ui for programmatic HTML generation instead of templates
---

# Nitro CLI - LLM Knowledge Base

This document contains everything needed to build static sites with Nitro CLI.

## Overview

Nitro CLI is a Python-based static site generator. Pages are written in Python using nitro-ui for HTML generation. The CLI provides scaffolding, a development server with live reload, and optimized production builds. It includes an islands architecture for partial hydration, responsive image optimization, build caching for incremental builds, and a plugin system.

## Installation

```bash
pip install nitro-cli
```

## Public API

All public classes are importable from the top-level `nitro` package:

```python
from nitro import (
    Config,            # Project configuration
    Page,              # Page object returned by render()
    env,               # Environment variable accessor (auto-loads .env)
    ImageConfig,       # Image optimization settings
    ImageOptimizer,    # Image optimization engine
    OptimizedImage,    # Result of optimizing an image
    Island,            # Interactive island component
    IslandConfig,      # Island system configuration
    IslandProcessor,   # HTML processor for island hydration
)
```

## CLI Commands

All commands support `--verbose` / `-v` for detailed output and `--debug` for full tracebacks.

### `nitro new <name>`
Create a new project with full scaffolding.

```bash
nitro new my-site
nitro new my-site --no-git      # Skip git initialization
nitro new my-site --no-install  # Skip dependency installation
```

### `nitro init`
Initialize Nitro in an existing directory (minimal scaffolding).

```bash
nitro init           # Create config, directories, starter page
nitro init --force   # Overwrite existing files
```

### `nitro dev` / `nitro serve`
Start development server with live reload.

```bash
nitro dev                    # Default: localhost:3000
nitro dev --port 8080        # Custom port
nitro dev --host 0.0.0.0     # Expose to network
nitro dev --open             # Open browser automatically
nitro dev --no-reload        # Disable live reload
```

### `nitro build`
Build for production with optimizations.

```bash
nitro build                  # Full build with all optimizations
nitro build --no-minify      # Skip HTML/CSS minification
nitro build --no-optimize    # Skip image optimization
nitro build --no-fingerprint # Skip cache-busting hashes
nitro build --no-responsive  # Skip responsive image generation
nitro build --no-islands     # Skip island hydration processing
nitro build --clean          # Clean build dir first
nitro build --force          # Force full rebuild (ignore cache)
nitro build --output dist    # Custom output directory
nitro build --quiet          # Minimal output
nitro build --verbose        # Detailed output
nitro build --debug          # Full tracebacks
```

Build uses an incremental cache (stored in `.nitro/cache.json`) to skip unchanged pages. Use `--force` to bypass the cache.

### `nitro preview`
Preview production build locally.

```bash
nitro preview                # Default: localhost:4000
nitro preview --port 5000    # Custom port
nitro preview --host 0.0.0.0 # Expose to network
nitro preview --open         # Open browser
```

### `nitro clean`
Remove build artifacts. Defaults to cleaning everything when no flags are specified.

```bash
nitro clean           # Clean build + cache (same as --all)
nitro clean --all     # Clean everything
nitro clean --build   # Clean only build directory
nitro clean --cache   # Clean only .nitro/ cache
nitro clean --dry-run # Show what would be deleted
```

### `nitro deploy`
Deploy to hosting platforms. Auto-detects platform by checking for config files (`netlify.toml`, `vercel.json`, `wrangler.toml`) and installed CLIs.

```bash
nitro deploy                      # Auto-detect platform
nitro deploy --platform netlify   # Specific platform
nitro deploy --platform vercel
nitro deploy --platform cloudflare
nitro deploy --prod               # Production deployment
nitro deploy --no-build           # Skip build step
```

### `nitro info`
Show project and environment information (Nitro version, Python version, platform, directory stats, dependency status).

```bash
nitro info
nitro info --json  # Output as JSON
```

### `nitro routes`
List all routes the site will generate.

```bash
nitro routes         # Table output with URL, source, type, status
nitro routes --json  # JSON output
```

### `nitro check`
Validate site without building (render check + internal link check).

```bash
nitro check              # Check all pages and links
nitro check --verbose    # Show detailed output
nitro check --no-links   # Skip link checking
```

### `nitro export`
Export built site as a zip archive.

```bash
nitro export                    # Export build/ to <project>-<date>.zip
nitro export -o site.zip        # Custom output path
nitro export --build-first      # Build before exporting
```

## Project Structure

```
my-site/
├── nitro.config.py      # Project configuration
├── src/
│   ├── pages/           # Page files (→ HTML)
│   │   ├── index.py     # → /index.html
│   │   ├── about.py     # → /about.html
│   │   └── blog/
│   │       └── [slug].py  # Dynamic route
│   ├── components/      # Reusable components
│   ├── styles/          # CSS files
│   │   └── main.css     # → /assets/styles/main.css
│   ├── public/          # Files copied to build root (like static/)
│   ├── plugins/         # Local plugins (auto-discovered)
│   └── data/            # JSON/YAML data files
├── static/              # Static assets (copied as-is to build root)
├── .nitro/              # Build cache (gitignored)
│   └── cache.json       # Incremental build hashes
└── build/               # Generated output (gitignored)
```

Both `static/` and `src/public/` are copied to the build root. `src/styles/` is copied to `build/assets/styles/`.

## Configuration

Create `nitro.config.py` in project root:

```python
from nitro import Config

config = Config(
    site_name="My Site",
    base_url="https://mysite.com",
    build_dir="build",       # Output directory (default: "build")
    source_dir="src",        # Source directory (default: "src")
    renderer={
        "pretty_print": True,   # Format HTML output (default: False)
        "minify_html": False,   # Minify in dev (always minified in build)
    },
    plugins=[],              # Plugin names list (installed packages or src/plugins/ files)
)
```

The `config` variable must be a `Config` instance. The file is loaded dynamically via `load_config()`.

## Writing Pages

### Basic Page Structure

Pages are Python files in `src/pages/` with a `render()` function:

```python
# src/pages/index.py
from nitro_ui import HTML, Head, Body, Title, Meta, H1, Paragraph
from nitro import Page

def render():
    page = HTML(
        Head(
            Meta(charset="UTF-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            Title("My Page"),
        ),
        Body(
            H1("Hello, World!"),
            Paragraph("Welcome to my site."),
        ),
    )

    return Page(
        title="My Page",
        meta={"description": "Page description"},
        content=page,
    )
```

### The Page Object

```python
from nitro import Page

Page(
    title="Page Title",           # Required: page title
    content=html_element,         # Required: nitro-ui element
    meta={"key": "value"},        # Optional: meta tags dict (arbitrary keys)
    template="layout",            # Optional: template name
    draft=False,                  # Optional: exclude from production builds
)
```

### Draft Pages

Pages with `draft=True` are:
- Rendered during development (`nitro dev`)
- Excluded from production builds (`nitro build`)
- Excluded from sitemap generation
- Shown with "draft" status in `nitro routes`

```python
def render():
    return Page(
        title="Work in Progress",
        content=html_element,
        draft=True,  # Won't be included in production build
    )
```

### File Path to URL Mapping

| File Path                     | Output URL             |
|-------------------------------|------------------------|
| `src/pages/index.py`          | `/index.html`          |
| `src/pages/about.py`          | `/about.html`          |
| `src/pages/blog/post.py`      | `/blog/post.html`      |
| `src/pages/docs/api/index.py` | `/docs/api/index.html` |

## nitro-ui Elements

All HTML elements are imported directly from `nitro_ui` as PascalCase classes:

```python
from nitro_ui import (
    # Document
    HTML, Head, Body, Title, Meta, Link, Style, Script,

    # Sections
    Header, Footer, Main, Section, Article, Aside, Nav,

    # Content
    Div, Span, Paragraph, Href, Image, Br, HorizontalRule,

    # Headings
    H1, H2, H3, H4, H5, H6,

    # Lists
    UnorderedList, OrderedList, ListItem,
    DescriptionList, DescriptionTerm, DescriptionDetails,

    # Tables
    Table, TableHeader, TableBody, TableFooter,
    TableRow, TableHeaderCell, TableDataCell,

    # Forms
    Form, Input, Label, Button, Select, Option, Textarea,

    # Text formatting
    Strong, Em, Code, Pre, Blockquote, Small, Mark,

    # Media
    Video, Audio, Source, Picture, Figure, Figcaption,

    # Other
    IFrame, Canvas, Details, Summary,
)
```

### Element Name Mapping

Some element names differ from their HTML tag names:

| nitro-ui Class      | HTML Tag     |
|---------------------|--------------|
| `Paragraph`         | `<p>`        |
| `Href`              | `<a>`        |
| `Image`             | `<img>`      |
| `HorizontalRule`    | `<hr>`       |
| `UnorderedList`     | `<ul>`       |
| `OrderedList`       | `<ol>`       |
| `ListItem`          | `<li>`       |
| `DescriptionList`   | `<dl>`       |
| `DescriptionTerm`   | `<dt>`       |
| `DescriptionDetails`| `<dd>`       |
| `TableHeader`       | `<thead>`    |
| `TableBody`         | `<tbody>`    |
| `TableFooter`       | `<tfoot>`    |
| `TableRow`          | `<tr>`       |
| `TableHeaderCell`   | `<th>`       |
| `TableDataCell`     | `<td>`       |

### Attribute Naming

Python reserved words are suffixed with `_`:

- `class_name="container"` → renders as `class="container"`
- `for_="email"` → renders as `for="email"`

All other HTML attributes use their standard names as keyword arguments.

### Element Usage

```python
# Basic element
Div("Hello")                           # <div>Hello</div>

# With attributes
Div("Content", class_name="container") # <div class="container">Content</div>
Href("Click", href="/page")            # <a href="/page">Click</a>

# Nested elements
Div(
    H1("Title"),
    Paragraph("Paragraph 1"),
    Paragraph("Paragraph 2"),
    class_name="content"
)

# Mixed content
Paragraph("Visit ", Href("our site", href="/"), " for more.")

# Self-closing
Image(src="/logo.png", alt="Logo")
Meta(charset="UTF-8")

# Boolean attributes
Input(type="email", required=True)
```

### Common Patterns

```python
# Navigation
Nav(
    Href("Home", href="/"),
    Href("About", href="/about.html"),
    Href("Contact", href="/contact.html"),
    class_name="nav"
)

# Card component
Div(
    Image(src="/image.jpg", alt="Card image"),
    H3("Card Title"),
    Paragraph("Card description"),
    Href("Read more", href="/details"),
    class_name="card"
)

# Form
Form(
    Label("Email:", for_="email"),
    Input(type="email", id="email", name="email", required=True),
    Label("Message:", for_="msg"),
    Textarea(id="msg", name="message", rows="4"),
    Button("Submit", type="submit"),
    action="/submit",
    method="post"
)
```

## Components

Create reusable components in `src/components/`:

```python
# src/components/card.py
from nitro_ui import Div, H3, Paragraph, Href, Image

def Card(title, description, image=None, link=None):
    """Reusable card component."""
    children = []

    if image:
        children.append(Image(src=image, alt=title))

    children.append(H3(title))
    children.append(Paragraph(description))

    if link:
        children.append(Href("Learn more", href=link))

    return Div(*children, class_name="card")
```

Use in pages:

```python
# src/pages/index.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from nitro_ui import HTML, Body
from components.card import Card

def render():
    return HTML(
        Body(
            Card("Title 1", "Description 1", link="/page1"),
            Card("Title 2", "Description 2", image="/img.jpg"),
        )
    )
```

## Dynamic Routes

Generate multiple pages from data using `[param].py` naming:

```python
# src/pages/blog/[slug].py
from nitro_ui import HTML, Head, Body, Title, H1, Paragraph, Article
from nitro import Page
from nitro_datastore import NitroDataStore

def get_paths():
    """Return list of parameter dicts for each page to generate."""
    data = NitroDataStore.from_file("src/data/posts.json")
    return [{"slug": post.slug, "title": post.title, "content": post.content}
            for post in data.posts]

def render(slug, title, content):
    """Render page for each set of parameters."""
    page = HTML(
        Head(Title(f"{title} - Blog")),
        Body(
            Article(
                H1(title),
                Paragraph(content),
            )
        )
    )

    return Page(title=title, content=page)
```

Output: `[slug].py` with `slug="hello-world"` → `build/blog/hello-world.html`

### Multiple Parameters

```python
# src/pages/[category]/[slug].py

def get_paths():
    return [
        {"category": "tech", "slug": "python"},
        {"category": "tech", "slug": "rust"},
        {"category": "life", "slug": "travel"},
    ]

def render(category, slug):
    # Generates:
    # - build/tech/python.html
    # - build/tech/rust.html
    # - build/life/travel.html
    ...
```

## Data Loading

Use nitro-datastore for loading JSON/YAML with dot notation:

```python
from nitro_datastore import NitroDataStore

# Load JSON file
data = NitroDataStore.from_file("src/data/site.json")

# Access with dot notation
site_name = data.site.name
posts = data.posts  # List access

# Iterate
for post in data.posts:
    print(post.title, post.slug)
```

Example data file:

```json
// src/data/site.json
{
  "site": {
    "name": "My Site",
    "tagline": "Built with Nitro"
  },
  "posts": [
    {"slug": "hello", "title": "Hello World"},
    {"slug": "intro", "title": "Introduction"}
  ]
}
```

## Islands (Partial Hydration)

Islands allow interactive components to be hydrated on the client while the rest of the page remains static HTML. This is useful for adding interactivity to specific parts of a page without shipping JavaScript for the entire page.

### Hydration Strategies

| Strategy      | Behavior                                                    |
|---------------|-------------------------------------------------------------|
| `load`        | Hydrate immediately when page loads                         |
| `idle`        | Hydrate when browser is idle (`requestIdleCallback`)        |
| `visible`     | Hydrate when component scrolls into view (`IntersectionObserver`) |
| `media`       | Hydrate when a CSS media query matches                      |
| `interaction` | Hydrate on first user interaction (click, focus, touchstart, mouseenter) |
| `none`        | No client-side hydration (server-render only)               |

Default strategy is `idle`.

### Creating an Island

```python
from nitro import Island
from nitro_ui import Div, Button, Span

def Counter(count=0):
    """A component that will be hydrated on the client."""
    return Div(
        Button("-"),
        Span(str(count)),
        Button("+"),
        class_name="counter"
    )

# Create an island with a hydration strategy
island = Island(
    name="counter",              # Component name (used for registration)
    component=Counter,           # The component function
    props={"count": 0},          # Props passed to the component
    client="visible",            # Hydration strategy (default: "idle")
    client_only=False,           # If True, skip server-side rendering
    media=None,                  # Media query string (only for "media" strategy)
)

# Use in a page - renders as HTML with data-* hydration attributes
def render():
    return HTML(
        Body(
            H1("My Page"),
            island,  # Island renders to HTML via str() or .render()
        )
    )
```

### Island Output HTML

An island renders a `<div>` with hydration marker attributes:

```html
<div data-island="counter" data-island-id="counter-a1b2c3d4" data-hydrate="visible" data-props="...">
  <!-- Server-rendered component HTML -->
</div>
```

### Client-Side Component Registration

Register JavaScript components for hydration in a `<script>` tag:

```javascript
// Register a component for hydration
window.__registerIsland("counter", function(props) {
    // Return a string, or an object with mount() or render() method
    return "<div>Interactive counter: " + props.count + "</div>";
});
```

### Island Configuration

```python
from nitro import IslandConfig

config = IslandConfig(
    output_dir="_islands",     # Output directory for island scripts (relative to build)
    default_strategy="idle",   # Default hydration strategy
    debug=False,               # Enable debug logging in browser console
)
```

### Build Integration

Islands are processed during `nitro build` by default. The `IslandProcessor` scans HTML for `data-island` attributes and injects the hydration runtime script before `</body>`. Disable with `nitro build --no-islands`.

## Image Optimization

The image optimization pipeline generates responsive images with multiple sizes and formats (AVIF, WebP) during production builds.

### ImageConfig

```python
from nitro import ImageConfig

config = ImageConfig(
    sizes=[320, 640, 768, 1024, 1280, 1920],  # Responsive breakpoints (widths in px)
    formats=["avif", "webp", "original"],      # Output formats in preference order
    quality={                                   # Quality per format (0-100)
        "avif": 80,
        "webp": 85,
        "jpeg": 85,
        "png": 85,
    },
    lazy_load=True,                            # Add loading="lazy" to img tags
    default_sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw",
    output_dir="_images",                      # Output dir (relative to build)
    min_size=1024,                             # Skip images smaller than this (bytes)
    max_width=2560,                            # Maximum dimension to generate
)
```

### Using ImageOptimizer

```python
from nitro import ImageOptimizer, ImageConfig
from pathlib import Path

optimizer = ImageOptimizer(config=ImageConfig())

# Optimize a single image (returns OptimizedImage or None)
optimized = optimizer.optimize_image(
    source_path=Path("static/images/hero.jpg"),
    output_dir=Path("build"),
    base_url="",
)

if optimized:
    # Generate a <picture> element with all format variants
    html = optimizer.generate_picture_element(
        optimized,
        alt="Hero image",
        css_class="hero-img",
        sizes="(max-width: 768px) 100vw, 50vw",  # Optional, uses default_sizes if None
    )

# Process an entire HTML string - replaces <img> tags with <picture> elements
processed_html = optimizer.process_html(
    html_content=html_string,
    source_dir=Path("static"),
    output_dir=Path("build"),
    base_url="",
)
```

### OptimizedImage

```python
optimized.original_path    # Path to source image
optimized.original_width   # Original width in pixels
optimized.original_height  # Original height in pixels
optimized.variants         # Dict[format, Dict[width, Path]] - all generated variants
optimized.hash             # Content hash of source image

# Generate srcset string for a format
srcset = optimized.get_srcset("webp")  # "/_images/hero-320w-abc123.webp 320w, ..."

# Get single src path
src = optimized.get_src("webp", width=640)  # Specific width, or largest if None
```

### Build Behavior

During `nitro build`, the optimizer:
- Skips external images (http/https), data URLs, and already-optimized images
- Skips images smaller than `min_size` bytes
- Only processes `.jpg`, `.jpeg`, `.png`, `.gif` files
- Generates variants at each breakpoint that doesn't exceed the original width
- Caches results to avoid re-processing unchanged images
- Requires Pillow (`pip install Pillow`); AVIF support depends on Pillow build

Enable/disable with `nitro build --responsive` / `--no-responsive`.

## Plugins

Nitro uses nitro-dispatch for its plugin system. Plugins hook into the build lifecycle.

### Available Hooks

| Hook                  | When                                | Data                    |
|-----------------------|-------------------------------------|-------------------------|
| `nitro.init`          | Plugin is loaded                    | -                       |
| `nitro.pre_generate`  | Before HTML generation              | -                       |
| `nitro.post_generate` | After HTML generation (can modify)  | `{"output": html_str}`  |
| `nitro.pre_build`     | Before production build starts      | -                       |
| `nitro.post_build`    | After production build completes    | -                       |
| `nitro.process_data`  | When processing data files          | -                       |
| `nitro.add_commands`  | When registering CLI commands       | -                       |

### Creating a Plugin

```python
# src/plugins/analytics.py (or an installed package)
from nitro.plugins import NitroPlugin, hook

class Plugin(NitroPlugin):
    name = "analytics"
    version = "1.0.0"
    description = "Injects analytics script"
    author = "Your Name"
    dependencies = []  # List of required plugin names

    def on_load(self):
        """Called when plugin is loaded."""
        pass

    def on_unload(self):
        """Called when plugin is unloaded."""
        pass

    def on_error(self, error):
        """Called when an error occurs in the plugin."""
        pass

    @hook('nitro.post_generate', priority=50)
    def add_analytics(self, data):
        """Modify HTML output after generation."""
        html = data.get('output', '')
        data['output'] = html.replace(
            '</body>',
            '<script src="/analytics.js"></script></body>'
        )
        return data
```

### Registering Plugins

Add plugin names to `config.plugins` in `nitro.config.py`:

```python
config = Config(
    plugins=["analytics", "my-other-plugin"],
)
```

Plugins are discovered in this order:
1. Installed Python packages (via `import plugin_name`)
2. Local files in `src/plugins/<name>.py`

The plugin module must export a `Plugin` class that extends `NitroPlugin`.

## Styling

### CSS Files

Place CSS in `src/styles/`. They're copied to `build/assets/styles/`:

```css
/* src/styles/main.css */
:root {
    --primary: #6366f1;
    --text: #1e293b;
}

body {
    font-family: system-ui, sans-serif;
    color: var(--text);
}
```

Link in pages:

```python
from nitro_ui import Link

Head(
    Link(rel="stylesheet", href="/assets/styles/main.css"),
)
```

### Inline Styles

```python
from nitro_ui import Style, Div

# In head
Style("""
    .container { max-width: 1200px; margin: 0 auto; }
    .hero { padding: 4rem 2rem; }
""")

# Inline on element
Div("Content", style="padding: 1rem; background: #f0f0f0;")
```

## Static Assets

Place files in `static/` or `src/public/` - both are copied to build root:

```
static/
├── favicon.ico      → build/favicon.ico
├── robots.txt       → build/robots.txt
└── images/
    └── logo.png     → build/images/logo.png

src/public/
└── manifest.json    → build/manifest.json
```

Reference in HTML:

```python
Image(src="/images/logo.png", alt="Logo")
Link(rel="icon", href="/favicon.ico")
```

## Build Optimizations

Production builds (`nitro build`) include:

1. **HTML Minification** - Removes whitespace, comments
2. **CSS Minification** - Compresses CSS files (requires `csscompressor`)
3. **Image Optimization** - Compresses JPG/PNG with Pillow
4. **Responsive Images** - Generates multi-size AVIF/WebP variants (`--no-responsive` to skip)
5. **Island Processing** - Injects hydration runtime for islands (`--no-islands` to skip)
6. **Asset Fingerprinting** - Adds content hashes to CSS/JS filenames for cache busting
7. **Sitemap Generation** - Creates `sitemap.xml` with all pages (respects page meta)
8. **Robots.txt** - Creates `robots.txt` pointing to sitemap
9. **Asset Manifest** - Creates `manifest.json` with file hashes and sizes
10. **Incremental Builds** - Only rebuilds changed pages (use `--force` to bypass)

## Build Caching

Nitro tracks file hashes in `.nitro/cache.json` for incremental builds:

- **Pages** - Rebuilds only pages whose source files have changed
- **Components** - If any component changes, all pages are rebuilt
- **Data files** - If any `.json`/`.yaml`/`.yml` data file changes, all pages are rebuilt
- **Config** - If `nitro.config.py` changes, a full rebuild is triggered

Use `nitro build --force` to ignore the cache and rebuild everything. Use `nitro clean --cache` to clear the cache.

## Live Reload

The dev server injects a WebSocket client (at `/__nitro__/livereload`) that reloads the page when files change. File changes are debounced at 0.5 seconds.

| File Changed          | Behavior                |
|-----------------------|-------------------------|
| `src/pages/*.py`      | Rebuilds changed page   |
| `src/components/*.py` | Rebuilds all pages      |
| `src/styles/*.css`    | Copies assets, reloads  |
| `src/public/*`        | Copies assets, reloads  |
| `nitro.config.py`     | Full rebuild            |

## Deployment

### Netlify

```bash
nitro deploy --platform netlify --prod
```

Or create `netlify.toml`:

```toml
[build]
  command = "pip install nitro-cli && nitro build"
  publish = "build"
```

### Vercel

```bash
nitro deploy --platform vercel --prod
```

### Cloudflare Pages

```bash
nitro deploy --platform cloudflare --prod
```

Platform auto-detection checks for config files (`netlify.toml`, `vercel.json`, `wrangler.toml`) and installed CLIs (`netlify`, `vercel`, `wrangler`).

## Common Patterns

### Layout Component

```python
# src/components/layout.py
from nitro_ui import HTML, Head, Body, Title, Meta, Link, Main, Header, Footer

def Layout(page_title, children, description=None):
    return HTML(
        Head(
            Meta(charset="UTF-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            Title(page_title),
            Meta(name="description", content=description or page_title),
            Link(rel="stylesheet", href="/assets/styles/main.css"),
        ),
        Body(
            Header(),  # nav content
            Main(*children if isinstance(children, (list, tuple)) else [children]),
            Footer(),  # footer content
        ),
    )
```

### SEO Meta Tags

```python
Head(
    Title("Page Title"),
    Meta(name="description", content="Page description for search engines"),
    Meta(name="keywords", content="keyword1, keyword2"),
    Meta(property="og:title", content="Title for social sharing"),
    Meta(property="og:description", content="Description for social"),
    Meta(property="og:image", content="https://site.com/image.jpg"),
    Meta(name="twitter:card", content="summary_large_image"),
    Link(rel="canonical", href="https://site.com/page"),
)
```

### Responsive Images

```python
# Manual approach
Picture(
    Source(srcset="/img/hero.avif", type="image/avif"),
    Source(srcset="/img/hero.webp", type="image/webp"),
    Image(src="/img/hero.jpg", alt="Hero image", loading="lazy"),
)

# Or use ImageOptimizer for automatic responsive image generation at build time
# (standard <img> tags are automatically replaced with <picture> during build)
```

### Environment Variables

Use `env` to access environment variables with automatic `.env` file loading:

```python
from nitro import env

# Access variables as attributes
api_key = env.API_KEY
debug_mode = env.DEBUG

# Check environment
if env.is_production():
    # Production-only code
    pass

if env.is_development():
    # Dev-only code
    pass
```

Requires `python-dotenv` for `.env` file support: `pip install nitro-cli[dotenv]`

### Conditional Content

```python
from nitro import env

def render():
    analytics = Script(src="/analytics.js") if env.is_production() else None

    return HTML(
        Head(Title("Page"), analytics),
        Body(H1("Page content")),
    )
```

## Troubleshooting

### Common Errors

**"Page missing render() function"**
- Every page file needs a `def render():` function

**"Dynamic page missing get_paths() function"**
- Files named `[param].py` need both `get_paths()` and `render()`

**Import errors for components**
- Add `sys.path.insert(0, str(Path(__file__).parent.parent))` before importing

**CSS not loading**
- Use absolute paths: `/assets/styles/main.css`
- Check file is in `src/styles/`

### Debug Mode

```bash
nitro build --debug   # Full tracebacks
nitro dev --verbose   # Detailed logging
```

## Sitemap Customization

Control sitemap generation via page `meta`:

```python
Page(
    title="My Page",
    content=html,
    meta={
        "sitemap": False,              # Exclude from sitemap
        "lastmod": "2024-01-15",       # Custom last modified date
        "sitemap_priority": 0.9,       # Priority (0.0-1.0, default: 0.8)
        "sitemap_changefreq": "daily", # Change frequency
    },
)
```

Draft pages are automatically excluded from the sitemap.

## Dependencies

- **nitro-ui** >= 1.0.6 - HTML element builder
- **nitro-datastore** >= 1.0.2 - Data loading with dot notation
- **nitro-dispatch** >= 1.0.0 - Plugin system hooks

**Optional:**
- **python-dotenv** - `.env` file support (`pip install nitro-cli[dotenv]`)
- **Pillow** - Image optimization and responsive image generation
- **csscompressor** - CSS minification
- **htmlmin** - HTML minification

## Version

Current: nitro-cli 1.0.8
