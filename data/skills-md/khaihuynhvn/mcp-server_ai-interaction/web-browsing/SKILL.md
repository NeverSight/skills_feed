---
name: web-browsing
description: Web research with automatic fallback mechanism. WebFetch → Browser MCP → User assistance via ai_interaction. Use when need to browse web.
---

# Web Browsing Skill

Automatic fallback mechanism for web research.

## CRITICAL: Tool Availability

**NEVER check mcps folder to verify tool existence.**
Tools are ALWAYS available - just call them directly:
- `WebFetch` - Cursor built-in fetch tool (fastest)
- `cursor-browser-extension` - Cursor built-in browser
- `user-chrome-devtools` - Chrome DevTools (alternative)

## Fallback Chain

```
1. WebFetch (fast, preferred)
   ↓ fails/error
2. Browser MCP (cursor-browser-extension)
   ↓ captcha/block
3. ai_interaction (request user help)
```

## Step 1: WebFetch (Default)

```
WebFetch url="https://example.com"
```

**Continue to Step 2 if:**
- HTTP error (4xx, 5xx)
- Content empty or truncated
- Authentication required
- Rate limited

## Step 2: Browser MCP

Use `cursor-browser-extension` MCP tools directly:

```
1. browser_navigate → target URL
2. browser_snapshot → get page content
3. browser_take_screenshot → visual reference (if needed)
```

**Alternative:** `user-chrome-devtools` if cursor-browser-extension fails.

**Continue to Step 3 if:**
- Captcha detected
- Bot check / "verify you're human"
- Login required
- Cloudflare/DDoS protection
- Page content not loading

## Step 3: User Assistance

**CRITICAL RULES:**
- NEVER make autonomous decisions (e.g., switching to DuckDuckGo when Google blocked)
- NEVER bypass user by trying alternative search engines/sites without asking
- ALWAYS inform user and wait for instruction via ai_interaction

Call `ai_interaction` tool with message:

```
"Browser bị chặn bởi [captcha/bot check/login].
URL: [url]
Cần bạn:
1. Mở browser manual
2. Bypass protection
3. Báo lại khi xong để tôi tiếp tục

Hoặc bạn muốn thử [alternative option]?"
```

Then wait for user confirmation via ai_interaction before retrying.

## Detection Patterns

### Captcha/Block Indicators
- "verify you are human"
- "captcha"
- "cloudflare"
- "access denied"
- "please wait while we verify"
- Blank page with only scripts
- HTTP 403, 429, 503

### Success Indicators
- Meaningful content returned
- Expected HTML structure
- No error messages

## Best Practices

1. **Always try WebFetch first** - fastest option
2. **Check response quality** - not just HTTP status
3. **Don't spam retries** - wait between attempts
4. **Be transparent** - tell user what's happening
5. **Save useful content** - don't re-fetch unnecessarily

## Integration with ai_interaction

When user helps bypass protection:
1. User completes manual action
2. User responds via ai_interaction
3. Agent retries with Browser MCP (cookies preserved)
4. Continue with research
