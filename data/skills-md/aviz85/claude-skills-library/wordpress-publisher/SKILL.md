---
name: wordpress-publisher
description: "Publish posts to WordPress. Use for: publish blog post, upload to WordPress, פרסם בבלוג."
version: "1.0.0"
author: aviz85
tags:
  - wordpress
  - blog
  - publishing
  - cms
---

# WordPress Publisher

Publish content to WordPress with a two-step flow: draft first, then publish after user confirmation.

## Configuration

Create `.env` file in the skill directory:

```bash
# ~/.claude/skills/wordpress-publisher/.env
WP_URL=https://your-site.com
WP_USERNAME=your_username
WP_APP_PASSWORD=YourApplicationPasswordNoSpaces
```

**Creating Application Password:**
1. Go to WordPress Admin → Users → Profile
2. Scroll to "Application Passwords"
3. Enter a name (e.g., "Claude Code") and click "Add New"
4. Copy the password and **remove all spaces**

## Usage

### Create Draft

```bash
node ~/.claude/skills/wordpress-publisher/scripts/wp-publish.js create "Post Title" content.html
```

### Create with Featured Image

```bash
node ~/.claude/skills/wordpress-publisher/scripts/wp-publish.js create "Post Title" content.html --image=cover.jpg
```

### Create and Publish Immediately

```bash
node ~/.claude/skills/wordpress-publisher/scripts/wp-publish.js create "Post Title" content.html --publish
```

### Publish Existing Draft

```bash
node ~/.claude/skills/wordpress-publisher/scripts/wp-publish.js publish POST_ID
```

### Check Post Status

```bash
node ~/.claude/skills/wordpress-publisher/scripts/wp-publish.js status POST_ID
```

### Read from stdin

```bash
echo "<h1>Hello</h1>" | node ~/.claude/skills/wordpress-publisher/scripts/wp-publish.js create "Hello" -
```

## Options

| Option | Description |
|--------|-------------|
| `--publish` | Publish immediately (default: draft) |
| `--image=<path>` | Featured image (uploaded to media library) |
| `--excerpt=<text>` | Add excerpt |
| `--categories=<ids>` | Category IDs (comma-separated) |
| `--tags=<ids>` | Tag IDs (comma-separated) |

## Response Format

### After Creating Draft:
```
Draft created!

**Post ID:** 123
**Edit in WordPress:** https://your-site.com/wp-admin/post.php?post=123&action=edit
**Preview:** https://your-site.com/?p=123

Publish now or review first?
```

### After Publishing:
```
Post is live!

**URL:** https://your-site.com/your-post-slug/
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Wrong credentials | Check WP_USERNAME and WP_APP_PASSWORD |
| 403 Forbidden | No permissions | Ensure user has Editor/Admin role |
| 404 Not Found | Wrong URL or API disabled | Check WP_URL, enable REST API |

## Hebrew/RTL Content

For Hebrew content, wrap in RTL container:

```html
<article dir="rtl" lang="he">
  <!-- Hebrew content here -->
</article>
```

