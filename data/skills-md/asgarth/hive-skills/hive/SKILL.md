---
name: hive
description: Hive blockchain CLI skill for querying accounts, blocks, posts, and raw API calls, uploading images, plus broadcasting votes, posts, comments, transfers, and custom JSON via hive-tx-cli.
homepage: https://github.com/asgarth/hive-tx-cli
metadata:
  {
    'openclaw':
      {
        'emoji': '🐝',
        'requires': { 'bins': ['hive'] },
        'install': [{ 'id': 'npm', 'kind': 'node', 'package': '@peakd/hive-tx-cli', 'bins': ['hive'], 'label': 'Install hive-tx-cli (npm)' }]
      }
  }
---

# Hive CLI 🐝

Use the `hive` CLI (hive-tx-cli) to query the Hive blockchain, upload images, and broadcast transactions with the correct key type.

## Install

```bash
# npm/pnpm/bun
npm install -g @peakd/hive-tx-cli

# One-shot (no install)
bunx @peakd/hive-tx-cli account peakd
```

## Requirements

- Node.js >= 22.0.0

## Quick Start

```bash
hive config                    # Interactive configuration
hive status                    # Check configuration status
hive account peakd             # Query an account
```

## Authentication & Keys

- **Posting key**: Required for voting, commenting, posting, uploading images
- **Active key**: Required for transfers and high-privilege operations
- Keys stored in `~/.hive-tx-cli/config.json` with 600 permissions
- Environment variables override config file values

```bash
hive config                    # Interactive setup
hive config --show             # Show current configuration
hive config --clear            # Clear all configuration
hive config set account <name>
hive config set postingKey <private-key>
hive config set activeKey <private-key>
hive config set node <url>
hive config get account
```

## Query Commands

```bash
hive account <username>        # Account information
hive props                     # Dynamic global properties
hive block <number>            # Block by number
hive content <author> <permlink> # Post/comment content
hive call database_api get_accounts '[["username"]]' # Raw API call
```

## Broadcast Commands

### Voting

```bash
hive vote --author <author> --permlink <permlink> --weight 100
```

### Posts & Comments

**Body format**: Post body must be in Markdown format.

**Image workflow**: If the post contains images, upload them first using `hive upload`, then insert the returned URLs into the post body before publishing.

```bash
# Create a post
hive post --permlink my-post --title "My Post" --body "Content" --tags "hive,blockchain"

# Create a reply
hive comment --permlink my-reply --body "Comment" --parent-author <author> --parent-permlink <permlink>
```

#### Post Metadata

The `--metadata` option accepts a JSON string with post metadata. All fields are optional.

**Schema:**

- `app`: Application identifier (e.g., "hive-tx-cli/2026.1.1")
- `description`: Short summary of the post content
- `image`: Array of image URLs for the post thumbnail
- `tags`: Array of post tags (should match --tags)
- `users`: Array of mentioned usernames
- `ai_tools`: Object indicating AI involvement in creating content
  - `writing_edit`: AI assisted with writing/editing
  - `media_generation`: AI generated images/media
  - `research`: AI assisted with research
  - `translation`: AI performed translation
  - `post_draft`: AI helped draft the post
  - `other`: Other AI assistance

**Guidelines:**

- Set `app` to the tool you're using
- Include a `description` summarizing the post (1-2 sentences)
- Add `image` URLs when the post contains images
- If the post was created with AI assistance, set appropriate `ai_tools` flags to `true`

**Example:**

```bash
hive post --permlink my-post --title "My Post" --body "Content" --tags "hive,ai" \
  --metadata '{"app":"hive-tx-cli/2026.1.1","description":"A post about Hive and AI tools","image":["https://example.com/image.jpg"],"ai_tools":{"writing_edit":true}}'
```

### Transfers

```bash
hive transfer --to <recipient> --amount "1.000 HIVE" --memo "Thanks!"
hive transfer --to <recipient> --amount "1.000 HBD" --memo "Payment" --token HBD
```

### Custom JSON & Raw Operations

```bash
hive custom-json --id <app-id> --json '{"key":"value"}'
hive broadcast '["vote",{"voter":"me","author":"you","permlink":"post","weight":10000}]' --key-type posting
```

## Image Uploads

If tools are available to resize or compress images, do so before uploading.
Target ~300kb output size for images above 500kb by reducing dimensions and slightly lowering quality.

```bash
hive upload --file ./path/to/image.jpg
hive upload --file ./image.png --host https://images.ecency.com
```

## Global Options

```bash
--node <url>                   # Override Hive node
hive --node https://api.hive.blog account peakd
```

## Configuration File

`~/.hive-tx-cli/config.json` (permissions 600):

```json
{
  "account": "your-username",
  "postingKey": "your-posting-private-key",
  "activeKey": "your-active-private-key",
  "node": "https://api.hive.blog"
}
```

Never commit private keys to version control.

## Environment Variables

```bash
export HIVE_ACCOUNT="your-username"
export HIVE_POSTING_KEY="your-posting-private-key"
export HIVE_ACTIVE_KEY="your-active-private-key"

hive vote --author author --permlink permlink --weight 100
```

## Troubleshooting

### Authentication errors

- Verify keys are private keys (not public keys)
- Check account name matches exactly
- Ensure config file permissions: `chmod 600 ~/.hive-tx-cli/config.json`

### Node connection issues

- Try different node: `hive config set node https://api.hiveworks.com`
- Check network connectivity

### Transaction failures

- Ensure sufficient Resource Credits (stake HIVE for RC)
- Use correct key type (posting vs active) for the operation
- Start with `hive status` to diagnose

## References

- Hive docs: https://developers.hive.io/
- hive-tx-cli: https://github.com/asgarth/hive-tx-cli

---

**TL;DR**: Query with `hive account/block/content`. Broadcast with `hive vote/post/comment/transfer/custom-json`. Upload with `hive upload`. Configure keys via `hive config`. 🐝
