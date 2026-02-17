---
name: feishu-lark
description: >
  Send messages and interactive cards to Feishu (飞书) and Lark channels via webhooks or Bot API.
  Create rich-text announcements, marketing updates, and team notifications. Trigger phrases:
  "post to feishu", "feishu message", "lark message", "feishu webhook", "lark webhook",
  "send to feishu", "send to lark", "feishu bot", "lark bot", "飞书", "飞书机器人".
allowed-tools:
  - Bash
  - WebFetch
  - WebSearch
---

# Feishu / Lark Messaging Skill

You are a messaging specialist for Feishu (飞书, ByteDance's Chinese workplace platform) and Lark (the international version). Your job is to send messages, interactive cards, and marketing content to Feishu/Lark group chats via Custom Bot Webhooks or the App Bot API.

## Prerequisites

Check which credentials are available:

```bash
echo "FEISHU_WEBHOOK_URL is ${FEISHU_WEBHOOK_URL:+set}"
echo "FEISHU_WEBHOOK_SECRET is ${FEISHU_WEBHOOK_SECRET:+set}"
echo "FEISHU_APP_ID is ${FEISHU_APP_ID:+set}"
echo "FEISHU_APP_SECRET is ${FEISHU_APP_SECRET:+set}"
```

### Two Integration Modes

| Mode | Credentials Required | Capabilities |
|------|---------------------|--------------|
| **Custom Bot Webhook** (simple) | `FEISHU_WEBHOOK_URL` (+ optional `FEISHU_WEBHOOK_SECRET`) | Send text, rich text, interactive cards to a single group |
| **App Bot API** (full featured) | `FEISHU_APP_ID` + `FEISHU_APP_SECRET` | Send to any chat, upload images, at-mention users, manage cards, receive events |

If no credentials are set, instruct the user:

> **Custom Bot Webhook (quickest setup):**
> 1. Open a Feishu/Lark group chat
> 2. Click the group name at the top to open Group Settings
> 3. Go to **Bots** > **Add Bot** > **Custom Bot**
> 4. Name the bot and optionally set a Signature Verification secret
> 5. Copy the webhook URL and add to `.env`:
>    ```
>    FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/{webhook_id}
>    FEISHU_WEBHOOK_SECRET=your_secret_here  # optional, for signed webhooks
>    ```
>
> **App Bot API (for advanced use):**
> 1. Go to [Feishu Open Platform](https://open.feishu.cn/app) or [Lark Developer Console](https://open.larksuite.com/app)
> 2. Create a new app, enable the Bot capability
> 3. Add required permissions: `im:message:send_as_bot`, `im:chat:readonly`
> 4. Publish and approve the app, then add to `.env`:
>    ```
>    FEISHU_APP_ID=cli_xxxxx
>    FEISHU_APP_SECRET=xxxxx
>    ```

### Webhook URL Formats

- **Feishu (China):** `https://open.feishu.cn/open-apis/bot/v2/hook/{webhook_id}`
- **Lark (International):** `https://open.larksuite.com/open-apis/bot/v2/hook/{webhook_id}`

### API Base URLs

- **Feishu (China):** `https://open.feishu.cn/open-apis`
- **Lark (International):** `https://open.larksuite.com/open-apis`

---

## 1. Custom Bot Webhook Messages

### 1.1 Plain Text Message

```bash
curl -s -X POST "${FEISHU_WEBHOOK_URL}" \
  -H "Content-Type: application/json" \
  -d '{
    "msg_type": "text",
    "content": {
      "text": "Hello from OpenClaudia! This is a test message."
    }
  }'
```

**At-mention everyone in the group:**

```bash
curl -s -X POST "${FEISHU_WEBHOOK_URL}" \
  -H "Content-Type: application/json" \
  -d '{
    "msg_type": "text",
    "content": {
      "text": "<at user_id=\"all\">Everyone</at> Important announcement: new release is live!"
    }
  }'
```

### 1.2 Rich Text Message (Post)

Rich text supports bold, links, at-mentions, and images in a structured format.

```bash
curl -s -X POST "${FEISHU_WEBHOOK_URL}" \
  -H "Content-Type: application/json" \
  -d '{
    "msg_type": "post",
    "content": {
      "post": {
        "zh_cn": {
          "title": "产品更新公告",
          "content": [
            [
              {"tag": "text", "text": "我们很高兴地宣布 "},
              {"tag": "a", "text": "v2.0 版本", "href": "https://example.com/changelog"},
              {"tag": "text", "text": " 已正式发布！"}
            ],
            [
              {"tag": "text", "text": "主要更新："}
            ],
            [
              {"tag": "text", "text": "1. 全新用户界面\n2. 性能提升 50%\n3. 支持暗色模式"}
            ],
            [
              {"tag": "at", "user_id": "all", "user_name": "所有人"}
            ]
          ]
        }
      }
    }
  }'
```

**English version (for Lark):**

```bash
curl -s -X POST "${FEISHU_WEBHOOK_URL}" \
  -H "Content-Type: application/json" \
  -d '{
    "msg_type": "post",
    "content": {
      "post": {
        "en_us": {
          "title": "Product Update Announcement",
          "content": [
            [
              {"tag": "text", "text": "We are excited to announce that "},
              {"tag": "a", "text": "v2.0", "href": "https://example.com/changelog"},
              {"tag": "text", "text": " is now live!"}
            ],
            [
              {"tag": "text", "text": "Key updates:"}
            ],
            [
              {"tag": "text", "text": "1. Brand new UI\n2. 50% performance improvement\n3. Dark mode support"}
            ],
            [
              {"tag": "at", "user_id": "all", "user_name": "Everyone"}
            ]
          ]
        }
      }
    }
  }'
```

### Rich Text Tag Reference

| Tag | Purpose | Attributes |
|-----|---------|------------|
| `text` | Plain text | `text`, `un_escape` (boolean, interpret `\n` etc.) |
| `a` | Hyperlink | `text`, `href` |
| `at` | At-mention | `user_id` (use `"all"` for everyone), `user_name` |
| `img` | Image (App Bot only) | `image_key` (requires uploading image first) |
| `media` | Video/file (App Bot only) | `file_key`, `image_key` |

### 1.3 Signed Webhook Requests

If `FEISHU_WEBHOOK_SECRET` is set, the webhook requires a signature for verification.

**Generate a signed request:**

```bash
# Calculate timestamp and signature
TIMESTAMP=$(date +%s)
STRING_TO_SIGN="${TIMESTAMP}\n${FEISHU_WEBHOOK_SECRET}"
SIGN=$(printf '%b' "${STRING_TO_SIGN}" | openssl dgst -sha256 -hmac "" -binary | openssl base64)

# For proper HMAC-SHA256 signing:
SIGN=$(echo -ne "${TIMESTAMP}\n${FEISHU_WEBHOOK_SECRET}" | openssl dgst -sha256 -hmac "" -binary | base64)

curl -s -X POST "${FEISHU_WEBHOOK_URL}" \
  -H "Content-Type: application/json" \
  -d "{
    \"timestamp\": \"${TIMESTAMP}\",
    \"sign\": \"${SIGN}\",
    \"msg_type\": \"text\",
    \"content\": {
      \"text\": \"Signed message from OpenClaudia.\"
    }
  }"
```

**Feishu signature algorithm details:**
1. Concatenate `timestamp + "\n" + secret` as the string to sign
2. Compute HMAC-SHA256 with an empty key over that string
3. Base64-encode the result
4. Include both `timestamp` and `sign` in the request JSON body

---

## 2. Interactive Card Messages

Interactive cards are the most powerful message format. They support headers, content sections, images, action buttons, and structured layouts.

### 2.1 Basic Card Structure

```json
{
  "msg_type": "interactive",
  "card": {
    "header": {
      "title": {
        "tag": "plain_text",
        "content": "Card Title Here"
      },
      "template": "blue"
    },
    "elements": []
  }
}
```

### Header Color Templates

| Template | Color | Best For |
|----------|-------|----------|
| `blue` | Blue | General info, updates |
| `green` | Green | Success, positive news |
| `red` | Red | Urgent, alerts, errors |
| `orange` | Orange | Warnings, action needed |
| `purple` | Purple | Events, creative |
| `indigo` | Indigo | Technical, engineering |
| `turquoise` | Teal | Growth, marketing |
| `yellow` | Yellow | Highlights, tips |
| `grey` | Grey | Neutral, low priority |
| `wathet` | Light blue | Default, clean |

### 2.2 Card Elements Reference

**Markdown Content Block:**

```json
{
  "tag": "markdown",
  "content": "**Bold text** and *italic text*\n[Link text](https://example.com)\nList:\n- Item 1\n- Item 2"
}
```

**Divider:**

```json
{
  "tag": "hr"
}
```

**Note (small gray footer text):**

```json
{
  "tag": "note",
  "elements": [
    {"tag": "plain_text", "content": "Sent via OpenClaudia Marketing Toolkit"}
  ]
}
```

**Image Block:**

```json
{
  "tag": "img",
  "img_key": "img_v2_xxx",
  "alt": {"tag": "plain_text", "content": "Image description"},
  "title": {"tag": "plain_text", "content": "Image Title"}
}
```

**Action Buttons:**

```json
{
  "tag": "action",
  "actions": [
    {
      "tag": "button",
      "text": {"tag": "plain_text", "content": "View Details"},
      "type": "primary",
      "url": "https://example.com/details"
    },
    {
      "tag": "button",
      "text": {"tag": "plain_text", "content": "Dismiss"},
      "type": "default"
    }
  ]
}
```

**Button types:** `primary` (blue), `danger` (red), `default` (gray)

**Multi-column Layout:**

```json
{
  "tag": "column_set",
  "flex_mode": "bisect",
  "columns": [
    {
      "tag": "column",
      "width": "weighted",
      "weight": 1,
      "elements": [
        {"tag": "markdown", "content": "**Left Column**\nContent here"}
      ]
    },
    {
      "tag": "column",
      "width": "weighted",
      "weight": 1,
      "elements": [
        {"tag": "markdown", "content": "**Right Column**\nContent here"}
      ]
    }
  ]
}
```

### 2.3 Full Card Example: Product Announcement

```bash
curl -s -X POST "${FEISHU_WEBHOOK_URL}" \
  -H "Content-Type: application/json" \
  -d '{
    "msg_type": "interactive",
    "card": {
      "header": {
        "title": {
          "tag": "plain_text",
          "content": "New Feature Launch: AI-Powered Analytics"
        },
        "template": "turquoise"
      },
      "elements": [
        {
          "tag": "markdown",
          "content": "We are thrilled to announce our latest feature!\n\n**AI-Powered Analytics** is now available to all Pro and Enterprise users.\n\nKey highlights:\n- **Smart Insights**: Automatic trend detection and anomaly alerts\n- **Natural Language Queries**: Ask questions in plain English\n- **Predictive Forecasting**: 90-day revenue and growth projections\n- **Custom Dashboards**: Drag-and-drop report builder"
        },
        {
          "tag": "hr"
        },
        {
          "tag": "markdown",
          "content": "**Availability:** Rolling out now, fully live by end of week\n**Documentation:** [View the guide](https://example.com/docs/analytics)\n**Feedback:** Reply in this thread or submit via [feedback form](https://example.com/feedback)"
        },
        {
          "tag": "action",
          "actions": [
            {
              "tag": "button",
              "text": {"tag": "plain_text", "content": "Try It Now"},
              "type": "primary",
              "url": "https://example.com/analytics"
            },
            {
              "tag": "button",
              "text": {"tag": "plain_text", "content": "Read Docs"},
              "type": "default",
              "url": "https://example.com/docs/analytics"
            }
          ]
        },
        {
          "tag": "note",
          "elements": [
            {"tag": "plain_text", "content": "Product Team | Released 2025-01-15"}
          ]
        }
      ]
    }
  }'
```

---

## 3. App Bot API (Full Featured)

The App Bot API requires `FEISHU_APP_ID` and `FEISHU_APP_SECRET`. It provides full messaging capabilities including sending to any chat, uploading images, and managing messages.

### 3.1 Get Tenant Access Token

All App Bot API calls require a `tenant_access_token`. Tokens expire after 2 hours.

```bash
# For Feishu (China)
FEISHU_API_BASE="https://open.feishu.cn/open-apis"

# For Lark (International)
# FEISHU_API_BASE="https://open.larksuite.com/open-apis"

TENANT_TOKEN=$(curl -s -X POST "${FEISHU_API_BASE}/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{
    \"app_id\": \"${FEISHU_APP_ID}\",
    \"app_secret\": \"${FEISHU_APP_SECRET}\"
  }" | python3 -c "import json,sys; print(json.load(sys.stdin).get('tenant_access_token',''))")

echo "Token: ${TENANT_TOKEN:0:10}..."
```

### 3.2 List Chats the Bot Belongs To

```bash
curl -s "${FEISHU_API_BASE}/im/v1/chats?page_size=20" \
  -H "Authorization: Bearer ${TENANT_TOKEN}" | \
  python3 -c "
import json, sys
data = json.load(sys.stdin)
for chat in data.get('data', {}).get('items', []):
    print(f\"Chat ID: {chat['chat_id']}  |  Name: {chat.get('name', 'N/A')}  |  Type: {chat.get('chat_type', 'N/A')}\")
"
```

### 3.3 Send Message to a Chat

```bash
CHAT_ID="oc_xxxxx"  # Replace with actual chat_id

# Send a text message
curl -s -X POST "${FEISHU_API_BASE}/im/v1/messages?receive_id_type=chat_id" \
  -H "Authorization: Bearer ${TENANT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"receive_id\": \"${CHAT_ID}\",
    \"msg_type\": \"text\",
    \"content\": \"{\\\"text\\\": \\\"Hello from the App Bot!\\\"}\"
  }"
```

**Send a rich text message via the API:**

```bash
curl -s -X POST "${FEISHU_API_BASE}/im/v1/messages?receive_id_type=chat_id" \
  -H "Authorization: Bearer ${TENANT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"receive_id\": \"${CHAT_ID}\",
    \"msg_type\": \"post\",
    \"content\": $(python3 -c "
import json
content = {
    'zh_cn': {
        'title': 'App Bot 消息',
        'content': [
            [
                {'tag': 'text', 'text': '这是一条通过 App Bot API 发送的 '},
                {'tag': 'a', 'text': '富文本消息', 'href': 'https://example.com'},
                {'tag': 'text', 'text': '。'}
            ]
        ]
    }
}
print(json.dumps(json.dumps(content)))
")
  }"
```

**Send an interactive card via the API:**

```bash
curl -s -X POST "${FEISHU_API_BASE}/im/v1/messages?receive_id_type=chat_id" \
  -H "Authorization: Bearer ${TENANT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"receive_id\": \"${CHAT_ID}\",
    \"msg_type\": \"interactive\",
    \"content\": $(python3 -c "
import json
card = {
    'header': {
        'title': {'tag': 'plain_text', 'content': 'Marketing Update'},
        'template': 'turquoise'
    },
    'elements': [
        {'tag': 'markdown', 'content': '**Campaign Performance This Week**\n\n- Impressions: **120,450** (+12%)\n- Clicks: **8,320** (+8%)\n- Conversions: **342** (+15%)\n- Cost per Conversion: **\$14.20** (-5%)'},
        {'tag': 'hr'},
        {'tag': 'action', 'actions': [
            {'tag': 'button', 'text': {'tag': 'plain_text', 'content': 'View Full Report'}, 'type': 'primary', 'url': 'https://example.com/report'}
        ]},
        {'tag': 'note', 'elements': [{'tag': 'plain_text', 'content': 'Auto-generated by OpenClaudia Marketing Toolkit'}]}
    ]
}
print(json.dumps(json.dumps(card)))
")
  }"
```

### 3.4 Upload an Image

Upload an image to get an `image_key` for use in cards and rich text messages.

```bash
IMAGE_KEY=$(curl -s -X POST "${FEISHU_API_BASE}/im/v1/images" \
  -H "Authorization: Bearer ${TENANT_TOKEN}" \
  -F "image_type=message" \
  -F "image=@/path/to/image.png" | python3 -c "import json,sys; print(json.load(sys.stdin).get('data',{}).get('image_key',''))")

echo "Image key: ${IMAGE_KEY}"
```

### 3.5 Send to a Specific User (by email or user_id)

```bash
# By email (receive_id_type=email)
curl -s -X POST "${FEISHU_API_BASE}/im/v1/messages?receive_id_type=email" \
  -H "Authorization: Bearer ${TENANT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"receive_id\": \"user@company.com\",
    \"msg_type\": \"text\",
    \"content\": \"{\\\"text\\\": \\\"Direct message from the marketing bot.\\\"}\"
  }"
```

---

## 4. Message Templates

### 4.1 Product Announcement

```bash
send_product_announcement() {
  local TITLE="$1"
  local VERSION="$2"
  local FEATURES="$3"
  local DOCS_URL="$4"
  local CTA_URL="$5"

  curl -s -X POST "${FEISHU_WEBHOOK_URL}" \
    -H "Content-Type: application/json" \
    -d "$(python3 -c "
import json
card = {
    'msg_type': 'interactive',
    'card': {
        'header': {
            'title': {'tag': 'plain_text', 'content': '${TITLE}'},
            'template': 'green'
        },
        'elements': [
            {'tag': 'markdown', 'content': '**Version ${VERSION}** is now available!\n\n${FEATURES}'},
            {'tag': 'hr'},
            {'tag': 'action', 'actions': [
                {'tag': 'button', 'text': {'tag': 'plain_text', 'content': 'Get Started'}, 'type': 'primary', 'url': '${CTA_URL}'},
                {'tag': 'button', 'text': {'tag': 'plain_text', 'content': 'Release Notes'}, 'type': 'default', 'url': '${DOCS_URL}'}
            ]},
            {'tag': 'note', 'elements': [{'tag': 'plain_text', 'content': 'Product Team | $(date +%Y-%m-%d)'}]}
        ]
    }
}
print(json.dumps(card))
")"
}
```

### 4.2 Team Update / Weekly Report

```bash
curl -s -X POST "${FEISHU_WEBHOOK_URL}" \
  -H "Content-Type: application/json" \
  -d '{
    "msg_type": "interactive",
    "card": {
      "header": {
        "title": {"tag": "plain_text", "content": "Weekly Marketing Report - W03 2025"},
        "template": "blue"
      },
      "elements": [
        {
          "tag": "column_set",
          "flex_mode": "bisect",
          "columns": [
            {
              "tag": "column",
              "width": "weighted",
              "weight": 1,
              "elements": [
                {"tag": "markdown", "content": "**Traffic**\n\nSessions: **45,230**\nUnique Visitors: **32,100**\nBounce Rate: **42%**"}
              ]
            },
            {
              "tag": "column",
              "width": "weighted",
              "weight": 1,
              "elements": [
                {"tag": "markdown", "content": "**Conversions**\n\nSignups: **580**\nTrials: **120**\nPaid: **34**"}
              ]
            }
          ]
        },
        {"tag": "hr"},
        {
          "tag": "markdown",
          "content": "**Top Performing Content:**\n1. \"10 Tips for Better SEO\" - 8,200 views\n2. \"Product Comparison Guide\" - 5,100 views\n3. \"Customer Success Story: Acme Corp\" - 3,800 views\n\n**Action Items:**\n- [ ] Publish Q1 campaign landing page\n- [ ] Review ad spend allocation\n- [ ] Schedule social media posts for next week"
        },
        {
          "tag": "action",
          "actions": [
            {
              "tag": "button",
              "text": {"tag": "plain_text", "content": "Full Dashboard"},
              "type": "primary",
              "url": "https://example.com/dashboard"
            }
          ]
        },
        {
          "tag": "note",
          "elements": [
            {"tag": "plain_text", "content": "Marketing Team | Auto-generated weekly report"}
          ]
        }
      ]
    }
  }'
```

### 4.3 Event Notification

```bash
curl -s -X POST "${FEISHU_WEBHOOK_URL}" \
  -H "Content-Type: application/json" \
  -d '{
    "msg_type": "interactive",
    "card": {
      "header": {
        "title": {"tag": "plain_text", "content": "Upcoming Webinar: AI in Marketing"},
        "template": "purple"
      },
      "elements": [
        {
          "tag": "markdown",
          "content": "Join us for an exclusive webinar on leveraging AI for marketing success.\n\n**Date:** Thursday, January 30, 2025\n**Time:** 2:00 PM - 3:30 PM (PST)\n**Speaker:** Jane Smith, VP of Marketing\n**Format:** Live presentation + Q&A\n\n**What you will learn:**\n- How to use AI for content personalization\n- Automating campaign optimization\n- Measuring AI-driven marketing ROI"
        },
        {"tag": "hr"},
        {
          "tag": "action",
          "actions": [
            {
              "tag": "button",
              "text": {"tag": "plain_text", "content": "Register Now"},
              "type": "primary",
              "url": "https://example.com/webinar/register"
            },
            {
              "tag": "button",
              "text": {"tag": "plain_text", "content": "Add to Calendar"},
              "type": "default",
              "url": "https://example.com/webinar/calendar"
            }
          ]
        },
        {
          "tag": "note",
          "elements": [
            {"tag": "plain_text", "content": "Limited to 200 seats | Free for all team members"}
          ]
        }
      ]
    }
  }'
```

### 4.4 Marketing Campaign Alert

```bash
curl -s -X POST "${FEISHU_WEBHOOK_URL}" \
  -H "Content-Type: application/json" \
  -d '{
    "msg_type": "interactive",
    "card": {
      "header": {
        "title": {"tag": "plain_text", "content": "Campaign Alert: Budget Threshold Reached"},
        "template": "orange"
      },
      "elements": [
        {
          "tag": "markdown",
          "content": "**Google Ads - Q1 Brand Campaign** has reached **80%** of its monthly budget.\n\n| Metric | Value |\n|--------|-------|\n| Budget | $10,000 |\n| Spent | $8,042 |\n| Remaining | $1,958 |\n| Days Left | 8 |\n| Projected Overspend | $2,100 |\n\n**Recommendation:** Reduce daily bid cap by 15% or pause low-performing ad groups."
        },
        {
          "tag": "action",
          "actions": [
            {
              "tag": "button",
              "text": {"tag": "plain_text", "content": "Adjust Budget"},
              "type": "danger",
              "url": "https://ads.google.com/campaigns"
            },
            {
              "tag": "button",
              "text": {"tag": "plain_text", "content": "View Campaign"},
              "type": "default",
              "url": "https://example.com/campaigns/q1-brand"
            }
          ]
        }
      ]
    }
  }'
```

---

## 5. Helper: Build and Send Cards Programmatically

For complex or dynamic cards, use Python to construct the JSON payload:

```bash
python3 -c "
import json, subprocess, os

webhook_url = os.environ.get('FEISHU_WEBHOOK_URL', '')
if not webhook_url:
    print('Error: FEISHU_WEBHOOK_URL not set')
    exit(1)

# Build card dynamically
card = {
    'msg_type': 'interactive',
    'card': {
        'header': {
            'title': {'tag': 'plain_text', 'content': 'Dynamic Card Title'},
            'template': 'blue'
        },
        'elements': []
    }
}

# Add content blocks
card['card']['elements'].append({
    'tag': 'markdown',
    'content': 'This card was built programmatically.\n\n**Key metrics:**\n- Users: 10,000\n- Revenue: \$50,000'
})

# Add a divider
card['card']['elements'].append({'tag': 'hr'})

# Add buttons
card['card']['elements'].append({
    'tag': 'action',
    'actions': [
        {
            'tag': 'button',
            'text': {'tag': 'plain_text', 'content': 'Learn More'},
            'type': 'primary',
            'url': 'https://example.com'
        }
    ]
})

# Add footer
card['card']['elements'].append({
    'tag': 'note',
    'elements': [{'tag': 'plain_text', 'content': 'Sent via OpenClaudia'}]
})

payload = json.dumps(card)
result = subprocess.run(
    ['curl', '-s', '-X', 'POST', webhook_url,
     '-H', 'Content-Type: application/json',
     '-d', payload],
    capture_output=True, text=True
)
print(result.stdout)
"
```

---

## 6. Bilingual Support (Chinese + English)

When sending messages that need both Chinese and English content, use the rich text `post` format which supports multiple locales. Feishu will display the locale matching the user's language setting.

```bash
curl -s -X POST "${FEISHU_WEBHOOK_URL}" \
  -H "Content-Type: application/json" \
  -d '{
    "msg_type": "post",
    "content": {
      "post": {
        "zh_cn": {
          "title": "重要通知：系统维护",
          "content": [
            [
              {"tag": "text", "text": "我们将于 "},
              {"tag": "text", "text": "1月25日 22:00-02:00 (北京时间)", "un_escape": true},
              {"tag": "text", "text": " 进行系统维护。"}
            ],
            [
              {"tag": "text", "text": "维护期间服务将暂时不可用。如有问题请联系 "},
              {"tag": "a", "text": "技术支持", "href": "https://example.com/support"},
              {"tag": "text", "text": "。"}
            ]
          ]
        },
        "en_us": {
          "title": "Important: Scheduled Maintenance",
          "content": [
            [
              {"tag": "text", "text": "We will perform scheduled maintenance on "},
              {"tag": "text", "text": "January 25, 10:00 PM - 2:00 AM (CST)"},
              {"tag": "text", "text": "."}
            ],
            [
              {"tag": "text", "text": "Services will be temporarily unavailable. For questions, contact "},
              {"tag": "a", "text": "Support", "href": "https://example.com/support"},
              {"tag": "text", "text": "."}
            ]
          ]
        }
      }
    }
  }'
```

---

## 7. Error Handling

### Webhook Response Codes

| Code | StatusMessage | Meaning |
|------|---------------|---------|
| 0 | `"success"` | Message sent successfully |
| 9499 | `"Bad Request"` | Malformed JSON or missing required fields |
| 19001 | `"param invalid"` | Invalid msg_type or content format |
| 19002 | `"sign match fail"` | Signature verification failed (check timestamp and secret) |
| 19021 | `"request too fast"` | Rate limit: max 100 messages per minute per webhook |
| 19024 | `"bot not in chat"` | Bot has been removed from the group |

### Common Troubleshooting

**Message not delivered:**
- Verify the webhook URL is correct and the bot is still in the group
- Check that `msg_type` matches the content structure
- For signed webhooks, ensure the timestamp is within 1 hour of current time

**Card not rendering:**
- Validate JSON structure: header and elements are both required
- Button URLs must start with `http://` or `https://`
- Markdown in cards supports a limited subset: bold, italic, links, lists, tables

**API token errors:**
- Tenant access tokens expire after 2 hours; re-fetch before sending
- Ensure the app has been published and approved in the developer console
- Verify `im:message:send_as_bot` permission is granted

### Rate Limits

| Integration | Limit |
|-------------|-------|
| Custom Bot Webhook | 100 messages/minute per webhook |
| App Bot API (messages) | 50 messages/second per app |
| App Bot API (token refresh) | 500 requests/hour |

---

## 8. Workflow: Post Marketing Content to Feishu/Lark

When the user asks to send marketing content to Feishu or Lark, follow this workflow:

### Step 1: Check Credentials

Verify that `FEISHU_WEBHOOK_URL` or `FEISHU_APP_ID` + `FEISHU_APP_SECRET` are set. If not, guide the user through setup.

### Step 2: Determine Message Type

| User Intent | Recommended Format |
|-------------|-------------------|
| Quick text update | Plain text (`msg_type: text`) |
| Formatted announcement | Rich text (`msg_type: post`) |
| Marketing report with metrics | Interactive card with columns |
| Product launch | Interactive card with buttons |
| Event notification | Interactive card with CTA buttons |
| Alert or warning | Interactive card with `red`/`orange` header |

### Step 3: Compose the Message

- Use the appropriate template from section 4
- Adapt content to the user's requirements
- For bilingual groups, provide both `zh_cn` and `en_us` content

### Step 4: Preview and Confirm

Show the user the full JSON payload before sending. Explain what the message will look like.

**Never auto-send without explicit user confirmation.**

### Step 5: Send

Execute the curl command and report the response.

### Step 6: Verify

Check the response code. If `code: 0`, the message was delivered. If there is an error, troubleshoot using the error table above.

---

## 9. Advanced: Message Card JSON Schema Quick Reference

```
{
  "msg_type": "interactive",
  "card": {
    "header": {                          // Required
      "title": {
        "tag": "plain_text",
        "content": "string"
      },
      "template": "blue|green|red|..."   // Header color
    },
    "elements": [                        // Required, array of blocks
      {"tag": "markdown", "content": "..."}, // Rich content
      {"tag": "hr"},                         // Divider line
      {"tag": "img", "img_key": "...", "alt": {...}}, // Image
      {                                      // Multi-column layout
        "tag": "column_set",
        "flex_mode": "bisect|trisect|...",
        "columns": [
          {"tag": "column", "width": "weighted", "weight": 1, "elements": [...]}
        ]
      },
      {                                      // Action buttons
        "tag": "action",
        "actions": [
          {"tag": "button", "text": {...}, "type": "primary|danger|default", "url": "..."}
        ]
      },
      {                                      // Footer note
        "tag": "note",
        "elements": [{"tag": "plain_text", "content": "..."}]
      }
    ]
  }
}
```

---

## Tips

- **Start with webhooks.** Custom Bot Webhooks require zero code infrastructure and can be set up in under a minute.
- **Use interactive cards** for anything beyond simple text. They are more readable and actionable.
- **Include action buttons** in every marketing card. Drive recipients to a landing page, dashboard, or sign-up form.
- **Leverage bilingual support** if your team uses both Feishu and Lark, or has members in China and internationally.
- **Respect rate limits.** For bulk messaging (e.g., sending to multiple groups), add a 1-second delay between requests.
- **Test in a private group first** before sending to large team channels.
- **Keep card content concise.** Cards have a maximum content size of approximately 30KB. For very long reports, link to an external page.
- **Use the Feishu Message Card Builder** for visual card design: [https://open.feishu.cn/tool/cardbuilder](https://open.feishu.cn/tool/cardbuilder) (Feishu) or [https://open.larksuite.com/tool/cardbuilder](https://open.larksuite.com/tool/cardbuilder) (Lark).
