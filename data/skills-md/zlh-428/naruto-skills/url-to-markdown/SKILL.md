---
name: url-to-markdown
description: Fetch any URL and convert to markdown using Chrome CDP. Supports two modes - auto-capture on page load, or wait for user signal (for pages requiring login). Use when user wants to save a webpage as markdown.
---

# URL to Markdown

Fetches any URL via Chrome CDP and converts HTML to clean markdown.

## Script Directory

**Important**: All scripts are located in `scripts/` subdirectory of this skill.

**Agent Execution Instructions**:
1. Determine this SKILL.md file's directory path as `SKILL_DIR`
2. Script path = `${SKILL_DIR}/scripts/<script-name>.ts`
3. Replace all `${SKILL_DIR}` in this document with actual path

**Script Reference**:
| Script | Purpose |
|--------|---------|
| `scripts/main.ts` | CLI entry point for URL fetching |

## Features

- Chrome CDP for full JavaScript rendering
- Two capture modes: auto or wait-for-user
- Clean markdown output with metadata
- Handles login-required pages via wait mode

## Usage

```bash
# Auto mode (default) - capture when page loads
npx -y bun ${SKILL_DIR}/scripts/main.ts <url>

# Wait mode - wait for user signal before capture
npx -y bun ${SKILL_DIR}/scripts/main.ts <url> --wait

# Save to specific file
npx -y bun ${SKILL_DIR}/scripts/main.ts <url> -o output.md
```

## Options

| Option | Description |
|--------|-------------|
| `<url>` | URL to fetch |
| `-o <path>` | Output file path (default: auto-generated) |
| `--wait` | Wait for user signal before capturing |
| `--timeout <ms>` | Page load timeout (default: 30000) |

## Capture Modes

### Auto Mode (default)

Page loads → waits for network idle → captures immediately.

Best for:
- Public pages
- Static content
- No login required

### Wait Mode (`--wait`)

Page opens → user can interact (login, scroll, etc.) → user signals ready → captures.

Best for:
- Login-required pages
- Dynamic content needing interaction
- Pages with lazy loading

**Agent workflow for wait mode**:
1. Run script with `--wait` flag
2. Script outputs: `Page opened. Press Enter when ready to capture...`
3. Use `AskUserQuestion` to ask user if page is ready
4. When user confirms, send newline to stdin to trigger capture

## Output Format

```markdown
---
url: https://example.com/page
title: "Page Title"
description: "Meta description if available"
author: "Author if available"
published: "2024-01-01"
captured_at: "2024-01-15T10:30:00Z"
---

# Page Title

Converted markdown content...
```

## Mode Selection Guide

When user requests URL capture, help select appropriate mode:

**Suggest Auto Mode when**:
- URL is public (no login wall visible)
- Content appears static
- User doesn't mention login requirements

**Suggest Wait Mode when**:
- User mentions needing to log in
- Site known to require authentication
- User wants to scroll/interact before capture
- Content is behind paywall

**Ask user when unclear**:
```
The page may require login or interaction before capturing.

Which mode should I use?
1. Auto - Capture immediately when loaded
2. Wait - Wait for you to interact first
```

## Output Directory

Each capture creates a file organized by domain:

```
url-to-markdown/
└── <domain>/
    └── <slug>.md
```

**Path Components**:
- `<domain>`: Site domain (e.g., `example.com`, `github.com`)
- `<slug>`: Generated from page title or URL path (kebab-case)

**Slug Generation**:
1. Extract from page title (preferred) or URL path
2. Convert to kebab-case, 2-6 words
3. Example: "Getting Started with React" → `getting-started-with-react`

**Conflict Resolution**:
If `url-to-markdown/<domain>/<slug>.md` already exists:
- Append timestamp: `<slug>-YYYYMMDD-HHMMSS.md`
- Example: `getting-started.md` exists → `getting-started-20260118-143052.md`

## Error Handling

| Error | Resolution |
|-------|------------|
| Chrome not found | Install Chrome or set `URL_CHROME_PATH` env |
| Page timeout | Increase `--timeout` value |
| Capture failed | Try wait mode for complex pages |
| Empty content | Page may need JS rendering time |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `URL_CHROME_PATH` | Custom Chrome executable path |
| `URL_DATA_DIR` | Custom data directory |
| `URL_CHROME_PROFILE_DIR` | Custom Chrome profile directory |

## Extension Support

Custom configurations via EXTEND.md.

**Check paths** (priority order):
1. `.content-gen-skills/url-to-markdown/EXTEND.md` (project)
2. `~/.content-gen-skills/url-to-markdown/EXTEND.md` (user)

If found, load before workflow. Extension content overrides defaults.
