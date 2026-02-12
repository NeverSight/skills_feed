---
name: mcdonalds-coupons
description: Use when user wants to check McDonald's promotions, claim coupons, or save money on McDonald's orders. Triggers on keywords like coupons, deals, McDonald's, McD, promotions, claim.
---

# McDonald's Coupon Assistant

A skill that connects to McDonald's China MCP Server to help users discover promotions, claim coupons, and manage their coupon wallet.

## Overview

This skill uses McDonald's official MCP (Model Context Protocol) service to:
- Query available coupons (麦麦省)
- One-click claim all coupons
- Check campaign calendar
- View user's coupon wallet

## Token Management

### Check if Token Exists

First, check if user has configured a token:

```bash
python scripts/token-manager.py list
```

### No Token? Guide User to Get One

```
📝 首次使用需要 MCP Token

获取步骤:
1. 访问 https://open.mcd.cn/mcp
2. 点击右上角「登录」
3. 使用手机号验证登录
4. 点击「控制台」→「激活」
5. 复制生成的 Token

添加 Token:
python scripts/token-manager.py add <名称> <token>

示例:
python scripts/token-manager.py add personal 1kxNLFYT...
```

### Multi-Token Management

Users can manage multiple tokens with **custom nicknames**:

```bash
# Add tokens - nickname can be anything user wants
python scripts/token-manager.py add 我自己 <token1>
python scripts/token-manager.py add 老妈 <token2>
python scripts/token-manager.py add 女朋友 <token3>

# List all tokens
python scripts/token-manager.py list
# Output:
# 🎫 已保存的 Token:
# ----------------------------------------
#   我自己: 1kxNLFYT...LuqJ ← 当前
#   老妈: 2abCDEFG...XyZ
#   女朋友: 3mnOPQRS...123
# ----------------------------------------

# Switch active token
python scripts/token-manager.py switch 老妈

# Remove a token
python scripts/token-manager.py remove 女朋友
```

**Storage:** `~/.mcd-tokens.json` (auto-created, permissions 600)

Token is cached persistently - user only needs to add once, then it's always available.

## Quick Reference

| Action | MCP Tool | Description |
|--------|----------|-------------|
| List available coupons | `available-coupons` | Shows claimable 麦麦省 coupons |
| Claim all coupons | `auto-bind-coupons` | One-click claim everything |
| View my coupons | `my-coupons` | User's claimed coupon wallet |
| Check promotions | `campaign-calender` | Current and upcoming campaigns |
| Get current time | `now-time-info` | Server time for validity check |

## Implementation

### Using Helper Script (Recommended)

```bash
# Uses token from token manager automatically
python scripts/mcd-mcp.py available-coupons

# Or specify token directly
python scripts/mcd-mcp.py available-coupons <token>
```

### Direct HTTP Call

```bash
curl -X POST https://mcp.mcd.cn/mcp-servers/mcd-mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"available-coupons"}}'
```

### Response Parsing

```json
{
  "result": {
    "content": [{"type": "text", "text": "...coupon data..."}]
  }
}
```

Extract text: `result.content[0].text`

## Example Workflows

**User: "有什么麦当劳优惠？"**
1. Check token exists → if not, guide user to add
2. Call `available-coupons`
3. Present coupons with prices
4. Offer to claim all

**User: "帮我领券" / "一键领取"**
1. Call `auto-bind-coupons`
2. Report success count
3. Remind expiry dates

**User: "切换到我妈的账号领券"**
1. Run `python scripts/token-manager.py switch 老妈`
2. Then call `auto-bind-coupons`
3. Confirm: "已用「老妈」的账号领取了 X 张券"

**User: "帮我把女朋友的麦当劳加进来"**
1. Guide to get token from https://open.mcd.cn/mcp
2. Ask user for nickname: "你想给这个账号起什么名字？"
3. Run `python scripts/token-manager.py add <用户起的名字> <token>`
4. Confirm addition

## Response Style

When presenting coupon info:
- Use emojis for food (🍔🍟🍗)
- Highlight prices and savings
- Group by category
- Note expiration dates
- Show which account is active (if multiple)

## Common Issues

| Issue | Solution |
|-------|----------|
| 401 Unauthorized | Token invalid/expired, get new one |
| 429 Too Many Requests | Rate limit (600/min), wait and retry |
| No token configured | Guide user through token-manager.py add |
| Wrong account | Use token-manager.py switch <name> |

## Rate Limits

- 600 requests per minute per token
- Each token is independent (can use multiple accounts in parallel)
