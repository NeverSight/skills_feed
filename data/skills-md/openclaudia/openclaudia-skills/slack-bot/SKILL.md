---
name: slack-bot
description: >
  Send messages and rich content to Slack channels via webhooks or Bot API. Use Block Kit for
  formatted announcements, marketing reports, and community updates. Trigger phrases:
  "post to slack", "slack message", "slack webhook", "slack notification", "slack announcement",
  "send to slack", "slack marketing", "slack update", "slack channel".
allowed-tools:
  - Bash
  - WebFetch
  - WebSearch
---

# Slack Bot

Send messages and rich content to Slack channels using Incoming Webhooks or the Slack Web API.
Build formatted announcements, marketing reports, metrics dashboards, and community updates
with Block Kit.

## Prerequisites

Requires either `SLACK_WEBHOOK_URL` or `SLACK_BOT_TOKEN` set in `.env`, `.env.local`, or
`~/.claude/.env.global`.

```bash
source ~/.claude/.env.global 2>/dev/null
source .env 2>/dev/null
source .env.local 2>/dev/null

if [ -n "$SLACK_WEBHOOK_URL" ]; then
  echo "SLACK_WEBHOOK_URL is set. Webhook mode available."
elif [ -n "$SLACK_BOT_TOKEN" ]; then
  echo "SLACK_BOT_TOKEN is set. Web API mode available."
else
  echo "Neither SLACK_WEBHOOK_URL nor SLACK_BOT_TOKEN is set."
  echo "See the Setup Guide below to configure Slack credentials."
fi
```

If neither variable is set, instruct the user to follow the Setup Guide section below.

---

## Setup Guide

### Option A: Incoming Webhook (Simple)

Incoming Webhooks are the fastest way to post messages. They require no OAuth scopes and are
scoped to a single channel.

1. Go to https://api.slack.com/apps and click **Create New App** > **From scratch**.
2. Name the app (e.g., "Marketing Bot") and select your workspace.
3. In the left sidebar, click **Incoming Webhooks** and toggle it **On**.
4. Click **Add New Webhook to Workspace** at the bottom.
5. Select the channel to post to and click **Allow**.
6. Copy the Webhook URL (starts with `https://hooks.slack.com/services/...`).
7. Add it to your environment:

```bash
echo 'SLACK_WEBHOOK_URL=https://hooks.slack.com/services/T.../B.../xxxx' >> .env
```

**Limitations:** One webhook per channel. Cannot read messages, list channels, or reply to
threads programmatically (you must know the `thread_ts` from a prior API response).

### Option B: Bot Token (Full Featured)

Bot tokens give access to the full Slack Web API: post to any channel the bot is in, reply to
threads, list channels, upload files, and more.

1. Go to https://api.slack.com/apps and click **Create New App** > **From scratch**.
2. Name the app and select your workspace.
3. In the left sidebar, click **OAuth & Permissions**.
4. Under **Bot Token Scopes**, add these scopes:
   - `chat:write` - Post messages
   - `chat:write.public` - Post to channels without joining
   - `channels:read` - List public channels
   - `files:write` - Upload files (optional, for images/reports)
   - `reactions:write` - Add emoji reactions (optional)
5. Click **Install to Workspace** at the top and authorize.
6. Copy the **Bot User OAuth Token** (starts with `xoxb-`).
7. Add it to your environment:

```bash
echo 'SLACK_BOT_TOKEN=xoxb-your-token-here' >> .env
```

8. Invite the bot to the channels it should post in: type `/invite @YourBotName` in each channel.

**Optional:** Set a default channel for convenience:

```bash
echo 'SLACK_DEFAULT_CHANNEL=#marketing' >> .env
```

---

## Method 1: Incoming Webhooks

### Send a Simple Text Message

```bash
curl -s -X POST "$SLACK_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello from the marketing bot!"
  }'
```

### Send a Message with Username and Icon Override

```bash
curl -s -X POST "$SLACK_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "New blog post published!",
    "username": "Marketing Bot",
    "icon_emoji": ":mega:"
  }'
```

### Send a Message with Block Kit (Webhook)

```bash
curl -s -X POST "$SLACK_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "blocks": [
      {
        "type": "header",
        "text": {
          "type": "plain_text",
          "text": "New Product Launch"
        }
      },
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "*Product X* is now live! Check out the announcement."
        }
      },
      {
        "type": "divider"
      },
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "Read the full announcement on our blog."
        },
        "accessory": {
          "type": "button",
          "text": {
            "type": "plain_text",
            "text": "Read More"
          },
          "url": "https://example.com/blog/launch"
        }
      }
    ]
  }'
```

---

## Method 2: Slack Web API (Bot Token)

The Web API provides full control over message delivery, threading, channel management, and more.

### API Base

All requests go to `https://slack.com/api/` with the header `Authorization: Bearer {SLACK_BOT_TOKEN}`.

### Post a Message to a Channel

```bash
curl -s -X POST "https://slack.com/api/chat.postMessage" \
  -H "Authorization: Bearer ${SLACK_BOT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "#marketing",
    "text": "Weekly metrics report is ready!",
    "blocks": [
      {
        "type": "header",
        "text": {
          "type": "plain_text",
          "text": "Weekly Marketing Metrics"
        }
      },
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "Here are the numbers for this week."
        }
      }
    ]
  }'
```

The response includes a `ts` (timestamp) field which identifies the message. Save this value
for threading replies:

```bash
# Post and capture the message timestamp for threading
RESPONSE=$(curl -s -X POST "https://slack.com/api/chat.postMessage" \
  -H "Authorization: Bearer ${SLACK_BOT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "#marketing",
    "text": "Thread parent message"
  }')

MESSAGE_TS=$(echo "$RESPONSE" | python3 -c "import json,sys; print(json.load(sys.stdin).get('ts',''))")
echo "Message timestamp: $MESSAGE_TS"
```

### Reply to a Thread

Use the `thread_ts` parameter to reply inside an existing thread:

```bash
curl -s -X POST "https://slack.com/api/chat.postMessage" \
  -H "Authorization: Bearer ${SLACK_BOT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"channel\": \"#marketing\",
    \"thread_ts\": \"${MESSAGE_TS}\",
    \"text\": \"This is a threaded reply with additional details.\"
  }"
```

To also broadcast the reply to the channel (so it appears in the main conversation as well),
add `"reply_broadcast": true`.

### Update an Existing Message

```bash
curl -s -X POST "https://slack.com/api/chat.update" \
  -H "Authorization: Bearer ${SLACK_BOT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"channel\": \"#marketing\",
    \"ts\": \"${MESSAGE_TS}\",
    \"text\": \"Updated message content.\",
    \"blocks\": []
  }"
```

### Delete a Message

```bash
curl -s -X POST "https://slack.com/api/chat.delete" \
  -H "Authorization: Bearer ${SLACK_BOT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"channel\": \"#marketing\",
    \"ts\": \"${MESSAGE_TS}\"
  }"
```

### List Public Channels

Useful for discovering which channel to post to:

```bash
curl -s "https://slack.com/api/conversations.list?types=public_channel&limit=100" \
  -H "Authorization: Bearer ${SLACK_BOT_TOKEN}" | \
  python3 -c "
import json, sys
data = json.load(sys.stdin)
for ch in data.get('channels', []):
    members = ch.get('num_members', 0)
    print(f\"#{ch['name']}  |  Members: {members}  |  ID: {ch['id']}\")
"
```

### Upload a File to a Channel

```bash
curl -s -X POST "https://slack.com/api/files.uploadV2" \
  -H "Authorization: Bearer ${SLACK_BOT_TOKEN}" \
  -F "file=@report.pdf" \
  -F "filename=weekly-report.pdf" \
  -F "channel_id=C0123456789" \
  -F "initial_comment=Here is this week's marketing report."
```

### Add an Emoji Reaction

```bash
curl -s -X POST "https://slack.com/api/reactions.add" \
  -H "Authorization: Bearer ${SLACK_BOT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"channel\": \"C0123456789\",
    \"timestamp\": \"${MESSAGE_TS}\",
    \"name\": \"white_check_mark\"
  }"
```

---

## Slack Block Kit Reference

Block Kit is Slack's UI framework for building rich, interactive messages. Messages are composed
of an array of blocks, each with a specific type and structure.

### Block Types

| Block Type | Purpose | Supports mrkdwn |
|------------|---------|-----------------|
| `header` | Large bold title text | No (plain_text only) |
| `section` | Primary content block with text and optional accessory | Yes |
| `divider` | Horizontal line separator | N/A |
| `image` | Full-width image with alt text | N/A |
| `context` | Small, muted text and images (for metadata, timestamps) | Yes |
| `actions` | Row of interactive elements (buttons, selects, date pickers) | N/A |
| `rich_text` | Advanced formatted text (lists, quotes, code blocks) | N/A |

### Header Block

```json
{
  "type": "header",
  "text": {
    "type": "plain_text",
    "text": "Weekly Marketing Report",
    "emoji": true
  }
}
```

### Section Block

Plain text section:

```json
{
  "type": "section",
  "text": {
    "type": "mrkdwn",
    "text": "*Traffic is up 23%* this week compared to last week.\nOrganic search drove most of the growth."
  }
}
```

Section with fields (two-column layout):

```json
{
  "type": "section",
  "fields": [
    {
      "type": "mrkdwn",
      "text": "*Visitors*\n12,450"
    },
    {
      "type": "mrkdwn",
      "text": "*Signups*\n342"
    },
    {
      "type": "mrkdwn",
      "text": "*MRR*\n$28,500"
    },
    {
      "type": "mrkdwn",
      "text": "*Churn*\n1.2%"
    }
  ]
}
```

Section with a button accessory:

```json
{
  "type": "section",
  "text": {
    "type": "mrkdwn",
    "text": "New blog post: *How We Grew 10x in 6 Months*"
  },
  "accessory": {
    "type": "button",
    "text": {
      "type": "plain_text",
      "text": "Read Post"
    },
    "url": "https://example.com/blog/growth-story",
    "action_id": "read_blog_post"
  }
}
```

Section with an image accessory:

```json
{
  "type": "section",
  "text": {
    "type": "mrkdwn",
    "text": "*New Feature: Dark Mode*\nOur most requested feature is finally here."
  },
  "accessory": {
    "type": "image",
    "image_url": "https://example.com/images/dark-mode-preview.png",
    "alt_text": "Dark mode preview"
  }
}
```

### Divider Block

```json
{
  "type": "divider"
}
```

### Image Block

```json
{
  "type": "image",
  "image_url": "https://example.com/images/chart.png",
  "alt_text": "Weekly traffic chart",
  "title": {
    "type": "plain_text",
    "text": "Traffic Overview"
  }
}
```

### Context Block

```json
{
  "type": "context",
  "elements": [
    {
      "type": "mrkdwn",
      "text": "Posted by *Marketing Team* | Feb 10, 2026"
    },
    {
      "type": "image",
      "image_url": "https://example.com/logo-small.png",
      "alt_text": "Company logo"
    }
  ]
}
```

### Actions Block (Buttons)

```json
{
  "type": "actions",
  "elements": [
    {
      "type": "button",
      "text": {
        "type": "plain_text",
        "text": "Approve"
      },
      "style": "primary",
      "action_id": "approve_action",
      "value": "approved"
    },
    {
      "type": "button",
      "text": {
        "type": "plain_text",
        "text": "Reject"
      },
      "style": "danger",
      "action_id": "reject_action",
      "value": "rejected"
    },
    {
      "type": "button",
      "text": {
        "type": "plain_text",
        "text": "View Details"
      },
      "url": "https://example.com/details",
      "action_id": "view_details"
    }
  ]
}
```

Button styles: `"primary"` (green), `"danger"` (red), or omit for default (gray).

**Note on interactivity:** Buttons with `action_id` (no `url`) require a Request URL configured
in your Slack App settings under **Interactivity & Shortcuts** to receive the button click
payload. Buttons with a `url` field open the link directly and do not require a backend.

### Block Kit Limits

| Limit | Value |
|-------|-------|
| Blocks per message | 50 |
| Characters per text block | 3,000 |
| Characters per header | 150 |
| Fields per section | 10 |
| Elements per actions block | 25 |
| Elements per context block | 10 |

### Block Kit Builder

Use the visual builder to design and preview messages before coding them:
https://app.slack.com/block-kit-builder

---

## Slack mrkdwn Formatting Guide

Slack uses its own markdown variant called mrkdwn. It differs from standard Markdown in
several ways.

| Formatting | Syntax | Example |
|-----------|--------|---------|
| Bold | `*text*` | *bold text* |
| Italic | `_text_` | _italic text_ |
| Strikethrough | `~text~` | ~strikethrough~ |
| Code (inline) | `` `text` `` | `inline code` |
| Code block | ` ```text``` ` | Multi-line code block |
| Blockquote | `>text` | Quoted text |
| Link | `<https://url\|display text>` | Clickable link |
| User mention | `<@U0123456>` | @username |
| Channel mention | `<#C0123456>` | #channel |
| Emoji | `:emoji_name:` | :rocket: |
| Bulleted list | Start line with `- ` or `* ` | Bullet point |
| Numbered list | Start line with `1. ` | Numbered item |
| Line break | `\n` in JSON string | New line |

**Important differences from standard Markdown:**
- Bold uses single asterisks `*bold*`, not double `**bold**`.
- Italic uses underscores `_italic_`, not single asterisks.
- Links use `<url|text>` format with a pipe, not `[text](url)`.
- Headers do not exist in mrkdwn. Use the `header` block type instead.
- Images cannot be inlined in mrkdwn. Use the `image` block or `accessory` instead.

---

## Message Templates

### Template 1: Product Announcement

```bash
curl -s -X POST "$SLACK_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "blocks": [
      {
        "type": "header",
        "text": {
          "type": "plain_text",
          "text": ":rocket: New Feature: [Feature Name]",
          "emoji": true
        }
      },
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "We just shipped *[Feature Name]* — here is what it does and why it matters.\n\n:point_right: *What it does:* [One-sentence description]\n:point_right: *Why it matters:* [Key benefit for users]\n:point_right: *How to try it:* [Quick instructions or link]"
        }
      },
      {
        "type": "image",
        "image_url": "https://example.com/feature-screenshot.png",
        "alt_text": "Feature screenshot"
      },
      {
        "type": "divider"
      },
      {
        "type": "actions",
        "elements": [
          {
            "type": "button",
            "text": {
              "type": "plain_text",
              "text": ":newspaper: Read Announcement",
              "emoji": true
            },
            "url": "https://example.com/blog/feature-launch",
            "action_id": "read_announcement"
          },
          {
            "type": "button",
            "text": {
              "type": "plain_text",
              "text": ":play_or_pause_button: Watch Demo",
              "emoji": true
            },
            "url": "https://example.com/demo",
            "action_id": "watch_demo"
          }
        ]
      },
      {
        "type": "context",
        "elements": [
          {
            "type": "mrkdwn",
            "text": "Posted by *Product Team* | :speech_balloon: Reply in thread with questions"
          }
        ]
      }
    ]
  }'
```

### Template 2: Weekly Metrics Report

```bash
curl -s -X POST "$SLACK_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "blocks": [
      {
        "type": "header",
        "text": {
          "type": "plain_text",
          "text": ":bar_chart: Weekly Marketing Metrics — Feb 3-9, 2026",
          "emoji": true
        }
      },
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "Here is this week'\''s performance snapshot."
        }
      },
      {
        "type": "divider"
      },
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": ":globe_with_meridians: *Website Traffic*"
        },
        "fields": [
          {
            "type": "mrkdwn",
            "text": "*Sessions*\n45,230 (:arrow_up: 12%)"
          },
          {
            "type": "mrkdwn",
            "text": "*Unique Visitors*\n31,870 (:arrow_up: 8%)"
          },
          {
            "type": "mrkdwn",
            "text": "*Bounce Rate*\n42.3% (:arrow_down: 2.1%)"
          },
          {
            "type": "mrkdwn",
            "text": "*Avg. Session Duration*\n3m 42s (:arrow_up: 15s)"
          }
        ]
      },
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": ":money_with_wings: *Conversion Metrics*"
        },
        "fields": [
          {
            "type": "mrkdwn",
            "text": "*Signups*\n487 (:arrow_up: 18%)"
          },
          {
            "type": "mrkdwn",
            "text": "*Trial-to-Paid*\n12.4% (:arrow_up: 1.2%)"
          },
          {
            "type": "mrkdwn",
            "text": "*MRR*\n$52,300 (:arrow_up: $3,200)"
          },
          {
            "type": "mrkdwn",
            "text": "*Churn*\n1.8% (:arrow_down: 0.3%)"
          }
        ]
      },
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": ":email: *Email Performance*"
        },
        "fields": [
          {
            "type": "mrkdwn",
            "text": "*Emails Sent*\n12,400"
          },
          {
            "type": "mrkdwn",
            "text": "*Open Rate*\n34.2%"
          },
          {
            "type": "mrkdwn",
            "text": "*Click Rate*\n4.8%"
          },
          {
            "type": "mrkdwn",
            "text": "*Unsubscribes*\n23"
          }
        ]
      },
      {
        "type": "divider"
      },
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "*:bulb: Key Takeaways*\n- Organic traffic up 15% after publishing 3 new blog posts\n- Email welcome sequence A/B test: Variant B outperformed by 22%\n- Trial signup spike on Thursday correlated with Product Hunt feature"
        }
      },
      {
        "type": "actions",
        "elements": [
          {
            "type": "button",
            "text": {
              "type": "plain_text",
              "text": "Full Dashboard",
              "emoji": true
            },
            "url": "https://analytics.example.com/dashboard",
            "action_id": "view_dashboard"
          }
        ]
      },
      {
        "type": "context",
        "elements": [
          {
            "type": "mrkdwn",
            "text": "Auto-generated by Marketing Bot | Data from Google Analytics + Stripe"
          }
        ]
      }
    ]
  }'
```

### Template 3: Blog Post Share

```bash
curl -s -X POST "$SLACK_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "blocks": [
      {
        "type": "header",
        "text": {
          "type": "plain_text",
          "text": ":pencil: New Blog Post Published",
          "emoji": true
        }
      },
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "*<https://example.com/blog/post-slug|Blog Post Title Here>*\n\nA brief summary of what the post covers — keep it to 2-3 sentences that capture the key value and make people want to click through."
        },
        "accessory": {
          "type": "image",
          "image_url": "https://example.com/blog/post-og-image.png",
          "alt_text": "Blog post cover image"
        }
      },
      {
        "type": "context",
        "elements": [
          {
            "type": "mrkdwn",
            "text": ":bust_in_silhouette: Author: *Jane Smith* | :clock1: 6 min read | :label: SEO, Growth"
          }
        ]
      },
      {
        "type": "divider"
      },
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": ":mega: *Help us amplify!* Share this post on your socials. Here are ready-to-use snippets:\n\n*Twitter/X:* _Just published: [title]. [Key insight from the post]. Link in reply._\n\n*LinkedIn:* _We just published a deep dive on [topic]. Here is the #1 takeaway: [insight]._"
        }
      },
      {
        "type": "actions",
        "elements": [
          {
            "type": "button",
            "text": {
              "type": "plain_text",
              "text": "Read the Post",
              "emoji": true
            },
            "style": "primary",
            "url": "https://example.com/blog/post-slug",
            "action_id": "read_post"
          },
          {
            "type": "button",
            "text": {
              "type": "plain_text",
              "text": "Share on Twitter",
              "emoji": true
            },
            "url": "https://twitter.com/intent/tweet?text=Check%20out%20this%20post&url=https://example.com/blog/post-slug",
            "action_id": "share_twitter"
          },
          {
            "type": "button",
            "text": {
              "type": "plain_text",
              "text": "Share on LinkedIn",
              "emoji": true
            },
            "url": "https://www.linkedin.com/sharing/share-offsite/?url=https://example.com/blog/post-slug",
            "action_id": "share_linkedin"
          }
        ]
      }
    ]
  }'
```

### Template 4: Team Update / Standup

```bash
curl -s -X POST "$SLACK_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "blocks": [
      {
        "type": "header",
        "text": {
          "type": "plain_text",
          "text": ":clipboard: Marketing Team Update — Monday, Feb 10",
          "emoji": true
        }
      },
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "*:white_check_mark: Completed Last Week*\n- Launched email welcome sequence v2\n- Published 3 blog posts (SEO, product, case study)\n- Set up Google Ads remarketing campaign\n- Shipped landing page A/B test (Variant B live)"
        }
      },
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "*:construction: In Progress*\n- Content calendar for March (70% done)\n- Competitor analysis report (due Wednesday)\n- Social media campaign for Product Hunt launch"
        }
      },
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "*:dart: This Week'\''s Priorities*\n1. Finalize Product Hunt launch assets\n2. Send weekly newsletter (Thursday 9am)\n3. Review and approve Q1 ad spend budget\n4. Onboard new content writer"
        }
      },
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "*:warning: Blockers*\n- Waiting on design team for Product Hunt gallery images\n- Need legal review on new case study before publishing"
        }
      },
      {
        "type": "divider"
      },
      {
        "type": "context",
        "elements": [
          {
            "type": "mrkdwn",
            "text": ":speech_balloon: Reply in thread with your own updates or questions"
          }
        ]
      }
    ]
  }'
```

### Template 5: Incident / Urgent Notification

```bash
curl -s -X POST "$SLACK_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "blocks": [
      {
        "type": "header",
        "text": {
          "type": "plain_text",
          "text": ":rotating_light: Marketing Alert",
          "emoji": true
        }
      },
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "*Issue:* [Brief description of the problem]\n*Impact:* [Who/what is affected]\n*Status:* :red_circle: Active\n*Owner:* <@U0123456>"
        }
      },
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "*Details:*\n[Longer explanation. What happened, when it started, what we know so far.]"
        }
      },
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "*Next Steps:*\n1. [Action item 1]\n2. [Action item 2]\n3. [Action item 3]"
        }
      },
      {
        "type": "actions",
        "elements": [
          {
            "type": "button",
            "text": {
              "type": "plain_text",
              "text": "Status Page"
            },
            "url": "https://status.example.com",
            "action_id": "status_page"
          }
        ]
      }
    ]
  }'
```

---

## Workflows

### Workflow 1: Post a Marketing Announcement

When the user asks to post an announcement, product update, or news to Slack:

1. **Gather details** - Ask for the announcement title, body, link, image URL, and target channel.
2. **Choose a template** - Select from the templates above or build a custom Block Kit payload.
3. **Build the payload** - Construct the JSON with proper mrkdwn formatting.
4. **Preview** - Show the user the full JSON payload and describe how it will render.
5. **Confirm** - Ask the user to approve before sending.
6. **Send** - Execute the curl command.
7. **Report** - Show the API response. For Web API, capture the `ts` for threading.

### Workflow 2: Post Weekly Metrics

When the user asks to send a metrics report or dashboard to Slack:

1. **Collect metrics** - Ask for the numbers or help pull them from analytics tools.
2. **Format with fields** - Use section blocks with `fields` for the two-column metric layout.
3. **Add context** - Include week-over-week comparisons with arrow emoji.
4. **Add takeaways** - Summarize 2-3 key insights in a section block.
5. **Include a dashboard link** - Add a button to the full analytics dashboard.
6. **Send and thread** - Post the main report, then thread detailed breakdowns as replies.

### Workflow 3: Share a Blog Post

When a new blog post needs to be distributed to the team:

1. **Get the URL** - Ask for the blog post URL, or fetch the latest from the blog.
2. **Extract metadata** - Use WebFetch to pull the title, description, author, and OG image.
3. **Build the share message** - Use Template 3 with social amplification snippets.
4. **Add share buttons** - Include Twitter and LinkedIn intent URLs pre-populated with the post.
5. **Post to the channel** - Send to the team marketing channel.

### Workflow 4: Community Engagement

For managing Slack community channels (public communities, customer channels):

1. **Welcome messages** - Post a welcome message with rules and resources when new members join.
2. **Scheduled updates** - Post weekly roundups of popular discussions or new resources.
3. **Event announcements** - Share upcoming webinars, AMAs, or meetups with RSVP buttons.
4. **Polls and feedback** - Use actions blocks with buttons to collect quick feedback.
5. **Thread management** - Reply to existing threads with updates or answers.

---

## Sending Messages with Dynamic Content

### Build Payloads with Shell Variables

```bash
TITLE="Product X v2.0 Released"
DESCRIPTION="Version 2.0 includes dark mode, API improvements, and 3x faster performance."
LINK="https://example.com/changelog/v2"
IMAGE_URL="https://example.com/images/v2-banner.png"
CHANNEL="#announcements"

curl -s -X POST "https://slack.com/api/chat.postMessage" \
  -H "Authorization: Bearer ${SLACK_BOT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "$(python3 -c "
import json
payload = {
    'channel': '${CHANNEL}',
    'text': '${TITLE}',
    'blocks': [
        {
            'type': 'header',
            'text': {'type': 'plain_text', 'text': '${TITLE}', 'emoji': True}
        },
        {
            'type': 'section',
            'text': {'type': 'mrkdwn', 'text': '${DESCRIPTION}'}
        },
        {
            'type': 'image',
            'image_url': '${IMAGE_URL}',
            'alt_text': '${TITLE}'
        },
        {
            'type': 'actions',
            'elements': [{
                'type': 'button',
                'text': {'type': 'plain_text', 'text': 'Learn More'},
                'url': '${LINK}',
                'style': 'primary',
                'action_id': 'learn_more'
            }]
        }
    ]
}
print(json.dumps(payload))
")"
```

### Build Payloads from a JSON File

For complex messages, write the payload to a file first:

```bash
# Write the payload
cat > /tmp/slack-message.json << 'PAYLOAD'
{
  "channel": "#marketing",
  "text": "Fallback text for notifications",
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "Message Title"
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "Message body with *bold* and _italic_ formatting."
      }
    }
  ]
}
PAYLOAD

# Send it
curl -s -X POST "https://slack.com/api/chat.postMessage" \
  -H "Authorization: Bearer ${SLACK_BOT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d @/tmp/slack-message.json
```

---

## Scheduled Messages

Post a message at a specific future time using `chat.scheduleMessage`:

```bash
# Schedule a message for a specific Unix timestamp
# Use: date -d "2026-02-12 09:00:00" +%s (Linux) or date -j -f "%Y-%m-%d %H:%M:%S" "2026-02-12 09:00:00" +%s (macOS)
SEND_AT=$(date -j -f "%Y-%m-%d %H:%M:%S" "2026-02-12 09:00:00" +%s 2>/dev/null || date -d "2026-02-12 09:00:00" +%s)

curl -s -X POST "https://slack.com/api/chat.scheduleMessage" \
  -H "Authorization: Bearer ${SLACK_BOT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"channel\": \"#marketing\",
    \"post_at\": ${SEND_AT},
    \"text\": \"Good morning team! Here is today's marketing agenda.\",
    \"blocks\": []
  }"
```

List scheduled messages:

```bash
curl -s "https://slack.com/api/chat.scheduledMessages.list" \
  -H "Authorization: Bearer ${SLACK_BOT_TOKEN}" | \
  python3 -c "
import json, sys, datetime
data = json.load(sys.stdin)
for msg in data.get('scheduled_messages', []):
    ts = datetime.datetime.fromtimestamp(msg['post_at']).strftime('%Y-%m-%d %H:%M')
    print(f\"ID: {msg['id']}  |  Channel: {msg['channel_id']}  |  Scheduled: {ts}\")
"
```

Delete a scheduled message:

```bash
curl -s -X POST "https://slack.com/api/chat.deleteScheduledMessage" \
  -H "Authorization: Bearer ${SLACK_BOT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "C0123456789",
    "scheduled_message_id": "Q0123456789"
  }'
```

---

## Multi-Channel Posting

Post the same message to multiple channels:

```bash
CHANNELS=("#marketing" "#general" "#product")
MESSAGE='{"text":"Big announcement coming tomorrow!","blocks":[{"type":"section","text":{"type":"mrkdwn","text":":mega: *Big announcement coming tomorrow!* Stay tuned."}}]}'

for CHANNEL in "${CHANNELS[@]}"; do
  echo "Posting to ${CHANNEL}..."
  echo "$MESSAGE" | python3 -c "
import json, sys
msg = json.load(sys.stdin)
msg['channel'] = '${CHANNEL}'
print(json.dumps(msg))
" | curl -s -X POST "https://slack.com/api/chat.postMessage" \
    -H "Authorization: Bearer ${SLACK_BOT_TOKEN}" \
    -H "Content-Type: application/json" \
    -d @- | python3 -c "
import json, sys
r = json.load(sys.stdin)
if r.get('ok'):
    print(f'  Sent. ts={r[\"ts\"]}')
else:
    print(f'  Error: {r.get(\"error\", \"unknown\")}')
"
done
```

---

## Error Handling

### Common API Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `invalid_auth` | Bad or expired token | Regenerate the bot token in Slack App settings |
| `channel_not_found` | Bot not in channel or wrong channel name | Invite bot with `/invite @BotName` or use channel ID |
| `not_in_channel` | Bot needs to join the channel first | Invite the bot or use `chat:write.public` scope |
| `too_many_attachments` | Over 50 blocks | Split the message into multiple posts or thread replies |
| `msg_too_long` | Text exceeds 40,000 characters | Shorten the message or split into parts |
| `rate_limited` | Too many requests | Wait the number of seconds in the `Retry-After` header |
| `missing_scope` | Token lacks required permission | Add the scope in OAuth & Permissions and reinstall the app |

### Validate a Response

```bash
RESPONSE=$(curl -s -X POST "https://slack.com/api/chat.postMessage" \
  -H "Authorization: Bearer ${SLACK_BOT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"channel":"#marketing","text":"Test message"}')

python3 -c "
import json, sys
r = json.loads('${RESPONSE}'.replace(\"'\", \"\"))
if r.get('ok'):
    print(f'Message sent successfully. ts={r[\"ts\"]} channel={r[\"channel\"]}')
else:
    print(f'Error: {r.get(\"error\", \"unknown\")}')
    if r.get('response_metadata', {}).get('messages'):
        for m in r['response_metadata']['messages']:
            print(f'  Detail: {m}')
" 2>/dev/null || echo "$RESPONSE"
```

A more robust approach using a temp file:

```bash
RESPONSE_FILE=$(mktemp)
curl -s -X POST "https://slack.com/api/chat.postMessage" \
  -H "Authorization: Bearer ${SLACK_BOT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"channel":"#marketing","text":"Test message"}' \
  -o "$RESPONSE_FILE"

python3 -c "
import json
with open('${RESPONSE_FILE}') as f:
    r = json.load(f)
if r.get('ok'):
    print(f'Sent. ts={r[\"ts\"]}')
else:
    print(f'Error: {r.get(\"error\")}')
"
rm -f "$RESPONSE_FILE"
```

---

## Tips

- Always include a `text` field alongside `blocks` — it serves as the fallback for
  notifications, accessibility readers, and clients that do not support Block Kit.
- Use the Block Kit Builder at https://app.slack.com/block-kit-builder to visually design
  and preview messages before building the curl commands.
- For production workflows, use `chat.postMessage` (Web API) over webhooks. It returns a
  message `ts` you can use for threading, updating, and deleting.
- Thread long reports. Post a summary as the parent message and details as threaded replies
  to keep channels clean.
- Use `:emoji:` codes in `plain_text` fields with `"emoji": true` to render emoji in headers
  and button labels.
- Escape special characters in mrkdwn: `&` becomes `&amp;`, `<` becomes `&lt;`, `>` becomes `&gt;`.
- Rate limits: Slack allows roughly 1 message per second per channel. For bulk posting, add a
  1-second delay between requests.
- When posting metrics, use section `fields` for the two-column layout rather than trying to
  format tables in mrkdwn (Slack does not support tables).
- **Always show the user the full message payload and ask for confirmation before posting.**
