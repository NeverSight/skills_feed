---
name: unicon
description: Help users add icons to their projects using the Unicon icon library. Unicon provides 19,000+ icons from Lucide, Phosphor, Hugeicons, Heroicons, Tabler, Feather, Remix, Simple Icons (brand logos), and Iconoir. Use when adding icons to React, Vue, Svelte, or web projects; using the unicon CLI to search, get, or bundle icons; setting up .uniconrc.json config; generating tree-shakeable icon components; using the Unicon API; or converting between icon formats.
license: MIT
metadata:
  author: webrenew
  version: "0.2.0"
  website: https://unicon.webrenew.com
  repository: https://github.com/WebRenew/unicon
---

# Unicon

Unicon is a unified icon library providing 19,000+ icons from 9 popular libraries. Unlike traditional npm packages that bundle thousands of icons, Unicon generates only the icons you need.

## Quick Start

```bash
# Install CLI globally
npm install -g @webrenew/unicon

# Or use directly with npx
npx @webrenew/unicon search "dashboard"
```

## Core Commands

| Command | Description |
|---------|-------------|
| `unicon search <query>` | AI-powered semantic search (supports `--pick` for interactive selection) |
| `unicon get <name>` | Get single icon to stdout, file, or clipboard (`--copy`) |
| `unicon info <name>` | Show detailed icon information |
| `unicon preview <name>` | ASCII art preview in terminal |
| `unicon bundle` | Bundle multiple icons (supports `--stars` for favorites) |
| `unicon init` | Create .uniconrc.json config (`--interactive` for wizard) |
| `unicon sync` | Regenerate bundles (`--watch` for auto-sync) |
| `unicon add <name>` | Add bundle to config |
| `unicon star <name>` | Add icon to favorites |
| `unicon audit` | Find unused/missing icons in project |
| `unicon sources` | List available icon libraries |
| `unicon categories` | List icon categories |
| `unicon cache` | Manage local cache |
| `unicon skill` | Install AI assistant skills |

## Output Formats

| Format | Extension | Use Case |
|--------|-----------|----------|
| `react` | `.tsx` | React/Next.js (auto-detected) |
| `vue` | `.vue` | Vue 3 SFC (auto-detected) |
| `svelte` | `.svelte` | Svelte components (auto-detected) |
| `svg` | `.svg` | Raw SVG markup |
| `json` | `.json` | Data/programmatic use |

**Note:** CLI auto-detects your framework from `package.json` and uses the appropriate format.

## Icon Sources

| Source | Icons | Description |
|--------|-------|-------------|
| `lucide` | 1,900+ | Beautiful & consistent |
| `phosphor` | 1,500+ | 6 weights available |
| `hugeicons` | 1,800+ | Modern outlined icons |
| `heroicons` | 292 | Tailwind Labs |
| `tabler` | 4,600+ | Pixel-perfect stroke |
| `feather` | 287 | Simple and clean |
| `remix` | 2,800+ | Multiple categories |
| `simple-icons` | 3,300+ | Brand logos |
| `iconoir` | 1,600+ | Modern outlined icons |

## Common Workflows

### Add Icons to a React Project

```bash
# 1. Initialize config (interactive wizard)
unicon init --interactive

# 2. Search for icons interactively
unicon search "navigation arrows" --pick

# 3. Add bundle to config
unicon add nav --query "arrow chevron menu"

# 4. Generate components
unicon sync

# 5. Import and use
# import { ArrowRight, Menu } from "./src/icons/nav"
```

### Get a Single Icon Quickly

```bash
# Output to stdout (auto-detects framework)
unicon get home

# Copy to clipboard directly
unicon get home --copy

# Save to file
unicon get settings --format react -o ./Settings.tsx

# Different framework
unicon get home --format vue -o ./Home.vue
```

### Interactive Search with Selection

```bash
# Search and pick icons interactively
unicon search "dashboard" --pick

# Then choose action: copy, save, star, or create bundle
```

### Bundle by Category

```bash
# Bundle all dashboard icons (tree-shakeable by default)
unicon bundle --category Dashboards -o ./src/icons

# Bundle specific icons by search
unicon bundle --query "social media" --format svg -o ./public/icons

# Bundle all favorited icons
unicon bundle --stars -o ./src/icons/favorites

# Single file mode (not tree-shakeable)
unicon bundle --query "ui" --single-file -o ./icons.tsx
```

### Favorites System

```bash
# Star icons for later
unicon star home
unicon star settings
unicon star user

# Bundle all starred icons
unicon bundle --stars -o ./src/icons/favorites

# View favorites
unicon favorites
```

### Watch Mode for Development

```bash
# Auto-regenerate when config changes
unicon sync --watch
```

### Audit Project Usage

```bash
# Find unused bundled icons and missing imports
unicon audit
```

### Preview Icons in Terminal

```bash
# ASCII art preview
unicon preview home

# Custom size
unicon preview star --width 24
```

## Tree-Shaking Benefits

Unlike `npm install lucide-react` which downloads thousands of icons:

- Generates **only the icons you need** as individual files
- **No external dependencies** to ship
- True tree-shaking with one component per file
- Import only what you use: `import { Home } from "./icons"`

## Web Interface

Browse and copy icons at: https://unicon.webrenew.com

- Visual search with AI
- One-click copy (SVG, React, Vue, Svelte)
- Filter by library and category
- Bundle builder for multiple icons

## References

- [CLI Commands](references/cli-commands.md) - All commands and options
- [Config File](references/config-file.md) - `.uniconrc.json` schema
- [API Reference](references/api-reference.md) - REST endpoints

## AI Assistant Integration

Install Unicon skills for AI coding assistants:

```bash
# List supported assistants
unicon skill --list

# Install for specific assistant
unicon skill --ide claude      # Claude Code
unicon skill --ide cursor      # Cursor
unicon skill --ide windsurf    # Windsurf

# Install for all supported assistants
unicon skill --all
```

### Supported AI Assistants

| IDE | Directory |
|-----|-----------|
| Claude Code | `.claude/skills/unicon/SKILL.md` |
| Cursor | `.cursor/rules/unicon.mdc` |
| Windsurf | `.windsurf/rules/unicon.md` |
| Agent | `.agent/rules/unicon.md` |
| Antigravity | `.antigravity/rules/unicon.md` |
| OpenCode | `.opencode/rules/unicon.md` |
| Codex | `.codex/unicon.md` |
| Aider | `.aider/rules/unicon.md` |

Once installed, ask your AI assistant: "Add a home icon to my project"

## Cache

Icons are cached locally at `~/.unicon/cache` for 24 hours:

```bash
unicon cache --stats   # Show cache info
unicon cache --clear   # Clear cache
```
