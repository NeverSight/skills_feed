---
name: typefully
description: >
  Create, schedule, and manage social media posts via Typefully. ALWAYS use this
  skill when asked to draft, schedule, post, or check tweets, posts, threads, or
  social media content for Twitter/X, LinkedIn, Threads, Bluesky, or Mastodon.
last-updated: 2026-01-27
allowed-tools: Bash(./scripts/typefully.sh:*)
---

# Typefully Skill

Create, schedule, and publish social media content across multiple platforms using [Typefully](https://typefully.com).

> **Freshness check**: If more than 30 days have passed since the `last-updated` date above, inform the user that this skill may be outdated and point them to the update options below.

## Keeping This Skill Updated

**Source**: [github.com/typefully/agent-skills](https://github.com/typefully/agent-skills)
**API docs**: [typefully.com/docs/api](https://typefully.com/docs/api)

Update methods by installation type:

| Installation | How to update |
|--------------|---------------|
| CLI (`npx skills`) | `npx skills update` |
| Claude Code plugin | `/plugin update typefully@typefully-skills` |
| Cursor | Remote rules auto-sync from GitHub |
| Manual | Pull latest from repo or re-copy `skills/typefully/` |

API changes ship independently—updating the skill ensures you have the latest commands and workflows.

## Setup

Before using this skill, ensure:

1. **API Key**: Set the `TYPEFULLY_API_KEY` environment variable
   - Get your key at https://typefully.com/settings/api
   - Export it: `export TYPEFULLY_API_KEY=your_key`

2. **Dependencies**: `curl`, `jq`, and `perl` must be installed (perl is pre-installed on macOS and most Linux systems)

## Social Sets

The Typefully API uses the term "social set" to refer to what users commonly call an "account". A social set contains the connected social media platforms (X, LinkedIn, Threads, etc.) for a single identity.

When determining which social set to use:

1. **Check project context first** - Look for configuration in project files like `CLAUDE.md` or `AGENTS.md`. Examples of how users might configure this:

   ```markdown
   ## Typefully
   Default social set ID: 12345
   ```

   ```markdown
   ## Social Media
   Use Typefully account ID 67890 for all posts.
   ```

   ```markdown
   ## Configuration
   - Typefully social_set_id: 11111
   ```

2. **Reuse previously resolved social set** - If determined earlier in the session, use it without asking again

3. **Ask only when ambiguous** - If multiple social sets exist and no default is configured, ask the user which to use

4. **Single social set shortcut** - If the user only has one social set, use it automatically

## Common Actions

| User says... | Action |
|--------------|--------|
| "Draft a tweet about X" | `draft:create <social_set_id> --platform x --text "..."` |
| "Post this to LinkedIn" | `draft:create <social_set_id> --platform linkedin --text "..."` |
| "What's scheduled?" | `draft:list <social_set_id> --status scheduled` |
| "Show my recent posts" | `draft:list <social_set_id> --status published` |
| "Schedule this for tomorrow" | `draft:create ... --schedule "2025-01-21T09:00:00Z"` |
| "Post this now" | `draft:create ... --schedule now` or `publish <social_set_id> <draft_id>` |

## Workflow

Always follow this workflow when creating posts:

1. **List social sets first** to get the `social_set_id`:
   ```bash
   ./scripts/typefully.sh social-sets
   ```

2. **Create drafts** using the social_set_id from step 1:
   ```bash
   ./scripts/typefully.sh draft:create <social_set_id> --platform x --text "Your post"
   ```

3. **Schedule or publish** as needed

## Commands Reference

### User & Social Sets

| Command | Description |
|---------|-------------|
| `me` | Get authenticated user info |
| `social-sets` | List all social sets you can access |
| `social-set <id>` | Get social set details including connected platforms |

### Drafts

| Command | Description |
|---------|-------------|
| `draft:list <social_set_id>` | List drafts (add `--status scheduled` to filter, `--sort` to order) |
| `draft:get <social_set_id> <draft_id>` | Get a specific draft with full content |
| `draft:create <social_set_id> --platform x --text "..."` | Create a new draft |
| `draft:create <social_set_id> --platform x --file <path>` | Create draft from file content |
| `draft:create ... --media <media_ids>` | Create draft with attached media |
| `draft:create ... --reply-to <url>` | Reply to an existing X post |
| `draft:create ... --community <id>` | Post to an X community |
| `draft:create ... --share` | Generate a public share URL for the draft |
| `draft:update <social_set_id> <draft_id> --text "..."` | Update an existing draft |
| `draft:update <social_set_id> <draft_id> --append --text "..."` | Append to existing thread |
| `draft:delete <social_set_id> <draft_id>` | Delete a draft |

### Scheduling & Publishing

| Command | Description |
|---------|-------------|
| `schedule <social_set_id> <draft_id> --time next-free-slot` | Schedule to next available slot |
| `schedule <social_set_id> <draft_id> --time "2025-01-20T14:00:00Z"` | Schedule for specific time |
| `publish <social_set_id> <draft_id>` | Publish immediately |

### Tags

| Command | Description |
|---------|-------------|
| `tag:list <social_set_id>` | List all tags |
| `tag:create <social_set_id> --name "Tag Name"` | Create a new tag |

### Media

| Command | Description |
|---------|-------------|
| `media:upload <social_set_id> <file_path>` | Upload image/video, returns media_id |
| `media:status <social_set_id> <media_id>` | Check if media is processed |

## Examples

### Create a tweet
```bash
./scripts/typefully.sh draft:create 123 --platform x --text "Hello, world!"
```

### Create a cross-platform post
```bash
./scripts/typefully.sh draft:create 123 --platform x,linkedin,threads --text "Big announcement!"
```

### Create and schedule for next slot
```bash
./scripts/typefully.sh draft:create 123 --platform x --text "Scheduled post" --schedule next-free-slot
```

### Create with tags
```bash
./scripts/typefully.sh draft:create 123 --platform x --text "Marketing post" --tags marketing,product
```

### List scheduled posts sorted by date
```bash
./scripts/typefully.sh draft:list 123 --status scheduled --sort scheduled_date
```

### Reply to a tweet
```bash
./scripts/typefully.sh draft:create 123 --platform x --text "Great thread!" --reply-to "https://x.com/user/status/123456"
```

### Post to an X community
```bash
./scripts/typefully.sh draft:create 123 --platform x --text "Community update" --community 1493446837214187523
```

### Create draft with share URL
```bash
./scripts/typefully.sh draft:create 123 --platform x --text "Check this out" --share
```

### Upload media and create post with it
```bash
# Step 1: Upload the image
./scripts/typefully.sh media:upload 123 ./image.jpg
# Returns: {"media_id": "abc-123-def", "message": "Upload complete. Use media:status to check processing."}

# Step 2: Wait for processing (poll until status is "processed")
./scripts/typefully.sh media:status 123 abc-123-def
# Returns: {"status": "processed", ...}

# Step 3: Create post with the media attached
./scripts/typefully.sh draft:create 123 --platform x --text "Check out this image!" --media abc-123-def
```

### Upload multiple media files
```bash
# Upload each file
./scripts/typefully.sh media:upload 123 ./photo1.jpg  # Returns media_id: id1
./scripts/typefully.sh media:upload 123 ./photo2.jpg  # Returns media_id: id2

# Create post with multiple media (comma-separated)
./scripts/typefully.sh draft:create 123 --platform x --text "Photo dump!" --media id1,id2
```

### Add media to an existing draft
```bash
# Upload media
./scripts/typefully.sh media:upload 123 ./new-image.jpg  # Returns media_id: xyz

# Update draft with media
./scripts/typefully.sh draft:update 123 456 --text "Updated post with image" --media xyz
```

## Platform Names

Use these exact names for the `--platform` option:
- `x` - X (formerly Twitter)
- `linkedin` - LinkedIn
- `threads` - Threads
- `bluesky` - Bluesky
- `mastodon` - Mastodon

## Draft URLs

Typefully draft URLs contain the social set and draft IDs:
```
https://typefully.com/?a=<social_set_id>&d=<draft_id>
```

Example: `https://typefully.com/?a=12345&d=67890`
- `a=12345` → social_set_id
- `d=67890` → draft_id

## Automation Guidelines

When automating posts, especially on X, follow these rules to keep accounts in good standing:

- **No duplicate content** across multiple accounts
- **No unsolicited automated replies** - only reply when explicitly requested by the user
- **No trending manipulation** - don't mass-post about trending topics
- **No fake engagement** - don't automate likes, reposts, or follows
- **Respect rate limits** - the API has rate limits, don't spam requests
- **Drafts are private** - content stays private until published or explicitly shared

When in doubt, create drafts for user review rather than publishing directly.

## Tips

- **Default to X/Twitter** unless another platform is specified
- **Character limits**: X (280), LinkedIn (3000), Threads (500), Bluesky (300), Mastodon (500)
- **Thread creation**: Use `---` on its own line to split into multiple posts (thread)
- **Scheduling**: Use `next-free-slot` to let Typefully pick the optimal time
- **Cross-posting**: List multiple platforms separated by commas: `--platform x,linkedin`
- **Draft titles**: Use `--title` for internal organization (not posted to social media)
- **Read from file**: Use `--file ./post.txt` instead of `--text` to read content from a file
- **Sorting drafts**: Use `--sort` with values like `created_at`, `-created_at`, `scheduled_date`, etc.
