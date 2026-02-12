---
name: wordpress-content-manager
description: WordPress content management via REST API for managing posts. Requires Node.js and WordPress REST API credentials.
compatibility: Requires Node.js 16+ and npm. Uses WP_USERNAME and WP_APP_PASSWORD (Application Password) for authentication.
metadata:
  requires-setup: true
---

# WordPress Content Manager

Manage WordPress posts via the REST API. Fully configurable via environment variables - no manual file editing required.

## Required Environment Variables

Before using this skill, the agent must ensure these environment variables are set. If any are missing, **ask the user for the values and set them before proceeding**.

| Variable | Description | Example |
|----------|-------------|---------|
| `WP_SITE_URL` | WordPress site base URL | `https://blog.example.com` |
| `WP_USERNAME` | WordPress username | `admin` |
| `WP_APP_PASSWORD` | WordPress Application Password | `xxxx xxxx xxxx xxxx` |

**How to get an Application Password:**
1. Log in to WordPress admin
2. Go to Users → Profile
3. Scroll to "Application Passwords"
4. Enter a name and click "Add New Application Password"
5. Copy the generated password (spaces are optional)

### Optional Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `WP_API_URL` | REST API base URL | `{WP_SITE_URL}/wp-json/wp/v2` |

## First-Time Setup

Run the setup script after setting the required environment variables. It installs Node.js dependencies and validates the connection.

### Linux/macOS
```bash
export WP_SITE_URL="https://your-site.com"
export WP_USERNAME="your-username"
export WP_APP_PASSWORD="your-app-password"
bash ~/.claude/skills/wordpress-content-manager/scripts/setup.sh
```

### Windows (PowerShell)
```powershell
$env:WP_SITE_URL = "https://your-site.com"
$env:WP_USERNAME = "your-username"
$env:WP_APP_PASSWORD = "your-app-password"
pwsh ~/.claude/skills/wordpress-content-manager/scripts/setup.ps1
```

If using Codex CLI, replace `~/.claude/skills` with `~/.codex/skills`.

If Node.js is missing, the setup script will attempt to install it using common package managers.

## Commands

All commands are non-interactive and return JSON when `--json` is set.

### Describe Connection
```bash
node ~/.claude/skills/wordpress-content-manager/scripts/wp-content.mjs site info --json
```

### List or Search Posts
```bash
node ~/.claude/skills/wordpress-content-manager/scripts/wp-content.mjs posts list --status publish --search "keyword" --per_page 20 --page 1
```

### View a Post
```bash
node ~/.claude/skills/wordpress-content-manager/scripts/wp-content.mjs posts get 123 --json
```

### Create a Post (HTML or Markdown)
```bash
node ~/.claude/skills/wordpress-content-manager/scripts/wp-content.mjs posts create \
  --title "New Post" \
  --content-file ./post.md \
  --status draft \
  --categories 1,2 \
  --tags 5,7
```

### Schedule a Post
```bash
node ~/.claude/skills/wordpress-content-manager/scripts/wp-content.mjs posts create \
  --title "Scheduled Post" \
  --content "<p>HTML body</p>" \
  --status future \
  --date "2025-01-15T15:30:00"
```

### Update a Post
```bash
node ~/.claude/skills/wordpress-content-manager/scripts/wp-content.mjs posts update 123 \
  --title "Updated Title" \
  --status publish
```

### Delete a Post
```bash
node ~/.claude/skills/wordpress-content-manager/scripts/wp-content.mjs posts delete 123
```

### Bulk Delete (Dry-Run First)
```bash
node ~/.claude/skills/wordpress-content-manager/scripts/wp-content.mjs posts delete-many \
  --status draft \
  --search "test" \
  --dry-run

node ~/.claude/skills/wordpress-content-manager/scripts/wp-content.mjs posts delete-many \
  --status draft \
  --search "test" \
  --confirm
```

## Advanced: Profile Files (Optional)

For convenience, you can create profile files in `profiles/` to store site configurations. Environment variables always override profile values.

See `references/profiles.md` for the profile format.

Select a profile with `--profile <name>` or `WP_PROFILE=<name>`.
