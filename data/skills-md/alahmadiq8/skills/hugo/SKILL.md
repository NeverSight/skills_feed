---
name: hugo
description: Build, configure, and develop Hugo static sites and themes. Use when the user wants to create a new Hugo site, develop or customize a Hugo theme, write Hugo templates (layouts, partials, shortcodes), configure hugo.toml/yaml/json, work with Hugo's asset pipeline (images, CSS/Sass, JS bundling), manage content (pages, sections, taxonomies, menus), or deploy a Hugo site. Triggers on mentions of "Hugo", "hugo.toml", "static site generator", Hugo-related template syntax (Go templates, baseof, partials), or Hugo content workflows.
---

# Hugo Static Site Generator

## Quick Reference

- Docs: https://gohugo.io/documentation/
- Forum: https://discourse.gohugo.io/
- GitHub: https://github.com/gohugoio/hugo
- Template functions: https://gohugo.io/functions/
- Configuration: https://gohugo.io/configuration/introduction/

## Core Commands

```bash
hugo new site my-site        # Create new site
hugo new theme my-theme      # Create theme skeleton
hugo new content posts/my-post.md  # Create content
hugo server -D               # Dev server (include drafts)
hugo server --navigateToChanged    # Auto-navigate to changed content
hugo                         # Build site to public/
hugo --minify                # Build with minified output
hugo --gc                    # Build and clean unused cache
hugo mod init github.com/user/repo  # Initialize Hugo modules
```

## Project Structure

```
my-site/
├── hugo.toml              # Site configuration
├── archetypes/            # Content templates for `hugo new`
│   └── default.md
├── assets/                # Files processed by Hugo Pipes (Sass, JS, images)
├── content/               # Site content (Markdown)
├── data/                  # Data files (JSON, TOML, YAML)
├── i18n/                  # Translation strings
├── layouts/               # Templates (override theme)
├── static/                # Static files copied as-is
├── themes/                # Installed themes
└── public/                # Generated site (build output)
```

## Workflow

### Creating a New Site

1. Run `hugo new site <name>` to scaffold
2. Configure `hugo.toml` — see [references/configuration.md](references/configuration.md)
3. Add a theme (install or create custom) — see [references/theme-development.md](references/theme-development.md)
4. Create content with `hugo new content <section>/<name>.md`
5. Run `hugo server -D` for live development
6. Build with `hugo --minify` for production

### Theme Development

Create custom themes or modify existing ones. See [references/theme-development.md](references/theme-development.md) for:
- Theme directory structure and skeleton
- Template lookup order
- Base templates (`baseof.html`) and blocks
- Partials and partial caching
- List and single templates
- Taxonomy and term templates

### Templating

Write Go templates for layouts, partials, and shortcodes. See [references/templating.md](references/templating.md) for:
- Go template syntax and functions
- Context (the dot `.`) and variable scoping
- Range, with, if/else patterns
- Custom shortcodes
- Template debugging

### Content Management

Organize and manage site content. See [references/content-management.md](references/content-management.md) for:
- Page bundles (leaf vs branch)
- Front matter fields
- Sections and taxonomies
- Menus
- Multilingual / i18n
- Content archetypes

### Asset Pipeline

Process images, CSS/Sass, JavaScript, and more. See [references/asset-pipeline.md](references/asset-pipeline.md) for:
- Image processing (resize, crop, filters, WebP)
- Sass/SCSS compilation
- JavaScript bundling with esbuild
- Fingerprinting and SRI
- PostCSS / Tailwind CSS integration

### Deployment

Deploy to hosting platforms. See [references/deployment.md](references/deployment.md) for:
- Netlify configuration
- Vercel setup
- Cloudflare Pages
- GitHub Pages with Actions
- General CI/CD patterns

## Best Practices

- **Keep images with content**: Use page bundles (`index.md` + images in same directory) so Hugo can process them
- **Use `hugo.toml` config directory** for complex sites: split into `config/_default/hugo.toml`, `menus.toml`, `params.toml`
- **Asset pipeline minimum**: Always `minify`, `fingerprint`, and use `slice` for CSS/JS bundles
- **Override, don't fork themes**: Place overriding templates in project `layouts/` — Hugo's union file system gives project files precedence over theme files
- **Use partials for DRY templates**: Break complex templates into focused partials; use `partialCached` for expensive operations
- **Content organization mirrors URL structure**: Top-level directories under `content/` become sections
- **Draft workflow**: Use `draft: true` in front matter; `hugo server -D` shows drafts, production build excludes them
- **Use archetypes**: Define content templates in `archetypes/` for consistent front matter across content types
