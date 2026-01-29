---
name: webhook-push
description: "Unified webhook messaging for WeCom, DingTalk, and Feishu platforms. Send notifications to enterprise communication platforms with a single interface."
license: MIT
compatibility: "Requires Python 3.9+ and network access to target platforms"
metadata:
    skill-author: Webhook Push Team
---

# Webhook Push Skill

## Overview

This skill provides a unified interface for sending webhook notifications to three major Chinese enterprise communication platforms:

- **WeCom (企业微信)** - Enterprise WeChat by Tencent
- **DingTalk (钉钉)** - Enterprise communication platform by Alibaba
- **Feishu (飞书)** - Collaboration platform by ByteDance

## When to Use This Skill

Use this skill when you need to:

- Send notifications to enterprise chat groups
- Integrate monitoring alerts into enterprise platforms
- Automate notifications for CI/CD pipelines
- Build incident management workflows
- Send reports and updates to team channels
- Create multi-platform notification systems

## Core Capabilities

### 1. Unified Message Model

Send messages using a single, platform-agnostic interface:

```python
from webhook_push import UnifiedMessage, MessageSender

message = UnifiedMessage(
    content={
        "type": "text",
        "body": {"text": "Deployment completed successfully!"}
    }
)

sender = MessageSender()
result = await sender.send(message, "dingtalk", webhook_url="https://oapi.dingtalk.com/robot/send?access_token=xxx")
```

### 2. Rich Message Types

Support for various message types:

- **Text** - Simple text messages with @mentions
- **Markdown** - Rich formatted messages
- **Image** - Send images (WeCom, Feishu)
- **Link** - Link cards (DingTalk)
- **Card** - Interactive cards with buttons
- **File** - File attachments (WeCom, Feishu)
- **Feed** - Multiple link cards (DingTalk)

### 3. Automatic Platform Conversion

Messages are automatically converted to platform-specific formats:

```python
# Same message works across platforms
message = UnifiedMessage(
    content={
        "type": "markdown",
        "title": "Daily Report",
        "body": {
            "content": "# Daily Stats\n- Users: 128\n- Revenue: $5,000"
        }
    }
)

# Send to all platforms automatically
result = await sender.send_auto(message)
```

### 4. Graceful Degradation

Unsupported features are automatically downgraded:

- Cards → Markdown with links
- Markdown → Plain text
- Rich features → Simple alternatives

### 5. Retry Mechanism

Built-in exponential backoff retry logic handles transient failures.

## Message Types

### Text Message

```python
message = UnifiedMessage(
    content={
        "type": "text",
        "body": {"text": "Hello, team!"},
        "mentions": [
            {"type": "mobile", "value": "13800000000", "display_name": "Zhang San"}
        ]
    }
)
```

### Markdown Message

```python
message = UnifiedMessage(
    content={
        "type": "markdown",
        "title": "Deployment Report",
        "body": {
            "content": """# Deployment Complete

## Status: ✅ Success
- Version: v1.2.3
- Environment: Production
- Deployed by: @zhangsan

[View Logs](https://example.com/logs)"""
        }
    }
)
```

### Card Message

Card messages provide interactive elements with buttons and rich content. Each platform has its own card format:

#### WeCom Template Card (text_notice)

```python
from webhook_push import UnifiedMessage, MessageContent

message = UnifiedMessage(
    content=MessageContent(
        type="card",
        body={
            "card_type": "text_notice",
            "title": "系统告警",
            "description": "CPU使用率超过阈值",
            "emphasis": {
                "title": "95%",
                "desc": "当前CPU使用率"
            },
            "horizontal_content_list": [
                {"keyname": "服务器", "value": "web-01"},
                {"keyname": "阈值", "value": "80%"}
            ],
            "jump_list": [
                {"type": 1, "url": "https://example.com/alerts", "title": "查看详情"}
            ],
            "action": {"type": 1, "url": "https://example.com/alerts"}
        }
    )
)

result = await sender.send(message, "wecom")
```

#### WeCom News (Article Card)

```python
message = UnifiedMessage(
    content={
        "type": "news",
        "body": {
            "links": [
                {
                    "title": "技术分享: Webhook 最佳实践",
                    "description": "了解如何设计可靠的 webhook 系统",
                    "url": "https://example.com/article",
                    "image_url": "https://example.com/cover.jpg"
                }
            ]
        }
    }
)

result = await sender.send(message, "wecom")
```

#### DingTalk Action Card (single button)

```python
from webhook_push import UnifiedMessage, MessageContent

message = UnifiedMessage(
    content=MessageContent(
        type="card",
        body={
            "card_type": "single",
            "config": {"hide_avatar": "0"},
            "title": "审批请求",
            "elements": [{"type": "div", "text": "您有一个新的审批请求待处理"}],
            "actions": [
                {"text": "立即审批", "url": "https://example.com/approve", "style": "positive"}
            ]
        }
    )
)

result = await sender.send(message, "dingtalk")
```

#### DingTalk Action Card (multiple buttons)

```python
message = UnifiedMessage(
    content=MessageContent(
        type="card",
        body={
            "card_type": "multi",
            "config": {"hide_avatar": "0", "btn_orientation": "1"},
            "title": "满意度调查",
            "elements": [{"type": "div", "text": "请对本次服务进行评价"}],
            "actions": [
                {"text": "非常满意", "url": "https://example.com/survey/1", "style": "positive"},
                {"text": "满意", "url": "https://example.com/survey/2", "style": "default"},
                {"text": "不满意", "url": "https://example.com/survey/3", "style": "default"}
            ]
        }
    )
)

result = await sender.send(message, "dingtalk")
```

#### Feishu Interactive Card

```python
message = UnifiedMessage(
    content={
        "type": "card",
        "body": {
            "config": {
                "wide_screen_mode": True,
                "enable_forward": True
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {"tag": "lark_md", "content": "**审批提醒**\n您有一个新的待审批事项"}
                }
            ],
            "actions": [
                {
                    "tag": "button",
                    "text": {"tag": "plain_text", "content": "立即审批"},
                    "url": "https://example.com/approve",
                    "type": "primary"
                }
            ]
        }
    }
)

result = await sender.send(message, "feishu")
```

### Image Message

```python
message = UnifiedMessage(
    content={
        "type": "image",
        "body": {
            "url": "https://example.com/screenshot.png",
            "alt": "System dashboard screenshot"
        }
    }
)
```

## Usage Patterns

### Basic Pattern

```python
from webhook_push import MessageSender, UnifiedMessage

# Create message
message = UnifiedMessage(
    content={
        "type": "text",
        "body": {"text": "Your notification message"}
    }
)

# Send to specific platform
sender = MessageSender()
result = await sender.send(
    message,
    "dingtalk",
    webhook_url="https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN"
)

if result.success:
    print("Sent!")
else:
    print(f"Failed: {result.error}")
```

### Multi-Platform

```python
# Send to multiple platforms
result = await sender.send_multi(
    message,
    platforms=["wecom", "dingtalk", "feishu"],
    webhook_urls={
        "wecom": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=XXX",
        "dingtalk": "https://oapi.dingtalk.com/robot/send?access_token=YYY",
        "feishu": "https://open.feishu.cn/open-apis/bot/v2/hook/ZZZ"
    }
)

print(f"Success: {result.success_count}, Failed: {result.failed_count}")
```

### Automatic Selection

```python
# Send to all configured platforms
result = await sender.send_auto(message)

print(f"Sent to: {result.sent_platforms}")
print(f"Skipped: {result.skipped_platforms}")
```

## Platform Configuration

### Enterprise WeChat

```python
# Via webhook URL
webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"

message = UnifiedMessage(content={"type": "text", "body": {"text": "Hello WeCom!"}})
await sender.send(message, "wecom", webhook_url)
```

**Message Types**: text, markdown, markdown_v2, image, news, file, voice, template_card

### DingTalk

```python
# Via webhook URL
webhook_url = "https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN"

message = UnifiedMessage(content={"type": "markdown", "body": {"content": "Hello DingTalk!"}})
await sender.send(message, "dingtalk", webhook_url)
```

**Message Types**: text, markdown, link, actionCard, feedCard

**Note**: Supports signature verification for security

### Feishu

```python
# Via webhook URL
webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_ID"

# With signature verification (recommended)
from webhook_push import FeishuAdapter

adapter = FeishuAdapter(
    webhook_id="YOUR_ID",
    secret="YOUR_SECRET"  # Enable signature verification
)

message = UnifiedMessage(content={"type": "text", "body": {"text": "Hello Feishu!"}})
await sender.send(message, "feishu", webhook_url)
```

**Message Types**: text, post, image, file, card, audio

**Note**: Supports HMAC-SHA256 signature verification for enhanced security (recommended)

## Environment Variables

```bash
# Optional: Configure default platforms
WECOM_WEBHOOK_KEY=your-key
DINGTALK_ACCESS_TOKEN=your-token
DINGTALK_SECRET=your-secret
FEISHU_WEBHOOK_ID=your-id
FEISHU_SECRET=your-secret  # Optional, for signature verification
```

## CLI Usage

```bash
# Send a text message
webhook-push send dingtalk "https://oapi.dingtalk.com/robot/send?access_token=xxx" \
    --content "Hello from CLI!"

# Send a markdown message
webhook-push send wecom "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx" \
    --type markdown \
    --title "Report" \
    --content "# Daily Report\n- Metrics here"

# Send to multiple platforms
webhook-push send-multi wecom dingtalk --content "Notification"

# Send to all available platforms
webhook-push send-auto --content "All platforms"

# Show platform info
webhook-push info dingtalk
```

## Best Practices

### 1. Use Markdown for Rich Content

Markdown provides the best compatibility across platforms:

```python
message = UnifiedMessage(
    content={
        "type": "markdown",
        "body": {
            "content": """# Report

## Summary
- Metric 1: **128**
- Metric 2: 3,421

> Last updated: 18:00"""
        }
    }
)
```

### 2. Handle Failures Gracefully

```python
result = await sender.send(message, "dingtalk", webhook_url)

if not result.success:
    if result.retry_suggested:
        # Retry later or queue for retry
        await retry_queue.add(message)
    else:
        # Log the error
        logger.error(f"Send failed: {result.error}")
```

### 3. Use Card Messages for Actions

Cards with buttons provide better user experience:

```python
message = UnifiedMessage(
    content={
        "type": "card",
        "body": {
            "card_type": "interactive",
            "elements": [{"type": "div", "text": "Review required"}],
            "actions": [
                {"type": "button", "text": "Approve", "url": "...", "style": "primary"},
                {"type": "button", "text": "Reject", "url": "..."}
            ]
        }
    }
)
```

### 4. Monitor Rate Limits

Each platform has different rate limits:

| Platform | Rate Limit |
|----------|------------|
| WeCom | 20/min |
| DingTalk | 20/min |
| Feishu | ~100/min |

The sender automatically handles rate limit errors.

## Advanced Features

### Custom Retry Policy

```python
from webhook_push import MessageSender, RetryPolicy, SenderOptions

options = SenderOptions(
    retry_policy=RetryPolicy(
        max_retries=5,
        initial_delay=1000,
        max_delay=30000,
        backoff_multiplier=2.0
    )
)

sender = MessageSender(options)
```

### Message Deduplication

Use `message_id` for deduplication:

```python
message = UnifiedMessage(
    metadata={"message_id": "unique-id-123"},
    content={"type": "text", "body": {"text": "Same message"}}
)
```

### Correlation Tracking

Use `correlation_id` to track related messages:

```python
message = UnifiedMessage(
    metadata={"correlation_id": "deployment-123"},
    content={"type": "markdown", "body": {"content": "Deployment update"}}
)
```

## Error Handling

Common error codes:

| Code | Meaning | Action |
|------|---------|--------|
| UNKNOWN_PLATFORM | Invalid platform name | Check platform name |
| UNSUPPORTED | Platform doesn't support message type | Use different message type |
| RATE_LIMIT | Too many requests | Wait and retry |
| NETWORK_ERROR | Network failure | Retry later |
| PLATFORM_ERROR | Platform returned error | Check error message |

## Performance Tips

1. **Use `send_multi`** for sending to multiple platforms
2. **Use `send_auto`** to leverage all available platforms
3. **Configure timeouts** for long-running operations
4. **Monitor rate limits** for high-volume scenarios

## Dependencies

- Python 3.9+
- httpx (HTTP client)
- pydantic (Data validation)
- tenacity (Retry logic)

See `pyproject.toml` for full dependencies.

## References

- [Design Document](references/webhook-push-skill-design.md)
- [Unified Message Design](references/webhook-push-unified-message-design.md)
- [API Reference](references/api-reference.md)
- [Platform Documentation](references/platform-docs.md)
- [WeCom Documentation](https://developer.work.weixin.qq.com/document/path/99110)
- [DingTalk Documentation](https://open.dingtalk.com/document/dingstart/obtain-the-webhook-address-of-a-custom-robot)
- [Feishu Documentation](https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot)
