---
name: quarto-netlify
description: Quarto + Netlify Deployment Setup. Use when setting up a Quarto project for Netlify deployment with RevealJS presentation support.
---

# Quarto + Netlify Deployment Setup

Set up a Quarto project for Netlify deployment with RevealJS presentation support.

## When to use

- When deploying a Quarto project to Netlify
- When setting up RevealJS presentations with Quarto
- When configuring automated builds for Quarto sites
- When you need the proven netlify.toml configuration for Quarto

## Instructions

### \_quarto.yml Configuration

```yaml
project:
  type: default
  output-dir: _site # Keep root clean, output to _site/
  render:
    - index.qmd

format:
  revealjs:
    output-file: slides.html
    theme: [default, custom.scss]
    slide-number: true
    # Add plugins as needed
```

### netlify.toml (Proven Pattern)

```toml
[build]
  command = """
    curl -LO https://quarto.org/download/latest/quarto-linux-amd64.deb && \
    dpkg -x quarto-linux-amd64.deb . && \
    export PATH=$PWD/opt/quarto/bin:$PATH && \
    quarto render
  """
  publish = "_site"

[[redirects]]
  from = "/"
  to = "/slides.html"
  status = 302
```

Key points:

- Use `.deb` package with `dpkg -x` extraction (not tar.gz)
- Extract to current dir `.` (not a subfolder)
- Path is `$PWD/opt/quarto/bin` (not nested)
- Just `quarto render` (uses `_quarto.yml` automatically)

### .gitignore

```
# Quarto output
/.quarto/
/_site/

# Node modules
node_modules/

# OS/Editor
.DS_Store
*.swp
```

### Makefile

```makefile
.PHONY: all render preview clean

render:
	quarto render index.qmd

preview:
	quarto preview index.qmd

clean:
	rm -rf _site .quarto
```

### RevealJS Extensions

Copy `_extensions/` folder for plugins:

- `simplemenu` - Navigation menu bar
- `reveal-auto-agenda` - Auto-generated agenda
- `code-fullscreen` - Expand code to fullscreen
- `codefocus` - Progressive line highlighting

### Deployment Steps

1. `gh repo create [name] --public --source=. --remote=origin`
2. `git push -u origin main`
3. Netlify: Import from GitHub, auto-detects `netlify.toml`
4. Deploy triggers on push to main
