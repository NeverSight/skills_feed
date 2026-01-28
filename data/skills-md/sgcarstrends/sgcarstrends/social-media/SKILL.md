---
name: social-media
description: Add or update social media posting integrations (Discord, LinkedIn, Telegram, Twitter) in workflows. Use when adding new platforms, debugging posting failures, or modifying message templates.
allowed-tools: Read, Edit, Grep, Glob
---

# Social Media Integration Skill

This skill helps you work with social media integrations in `apps/api/src/lib/workflows/social/`.

## When to Use This Skill

- Adding new social media platforms
- Debugging posting failures
- Updating message templates and formatting
- Configuring webhook URLs and API credentials
- Testing social media workflows

## Supported Platforms

Current integrations:
- **Discord** - Webhook-based posting
- **LinkedIn** - OAuth-based API posting
- **Telegram** - Bot API posting
- **Twitter** - API v2 posting

## Architecture

```
apps/api/src/lib/workflows/social/
├── discord.ts           # Discord webhook integration
├── linkedin.ts          # LinkedIn API integration
├── telegram.ts          # Telegram bot integration
└── twitter.ts           # Twitter API integration
```

## Key Patterns

### 1. Telegram Integration

Telegram uses Bot API with chat IDs:

```typescript
export async function postToTelegram(message: string) {
  const botToken = process.env.TELEGRAM_BOT_TOKEN;
  const chatId = process.env.TELEGRAM_CHAT_ID;

  if (!botToken || !chatId) {
    throw new Error("Telegram credentials not configured");
  }

  const url = `https://api.telegram.org/bot${botToken}/sendMessage`;

  await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      chat_id: chatId,
      text: message,
      parse_mode: "Markdown",
      disable_web_page_preview: false,
    }),
  });
}
```

### 3. Twitter Integration

Twitter uses OAuth 2.0 with API v2:

```typescript
export async function postToTwitter(message: string) {
  const bearerToken = process.env.TWITTER_BEARER_TOKEN;

  if (!bearerToken) {
    throw new Error("Twitter bearer token not configured");
  }

  const url = "https://api.twitter.com/2/tweets";

  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${bearerToken}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text: message }),
  });

  if (!response.ok) {
    throw new Error(`Twitter API error: ${response.statusText}`);
  }

  return await response.json();
}
```

### 4. LinkedIn Integration

LinkedIn uses OAuth 2.0 with organization posting:

```typescript
export async function postToLinkedIn(message: string) {
  const accessToken = process.env.LINKEDIN_ACCESS_TOKEN;
  const organizationId = process.env.LINKEDIN_ORG_ID;

  if (!accessToken || !organizationId) {
    throw new Error("LinkedIn credentials not configured");
  }

  const url = "https://api.linkedin.com/v2/ugcPosts";

  await fetch(url, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${accessToken}`,
      "Content-Type": "application/json",
      "X-Restli-Protocol-Version": "2.0.0",
    },
    body: JSON.stringify({
      author: `urn:li:organization:${organizationId}`,
      lifecycleState: "PUBLISHED",
      specificContent: {
        "com.linkedin.ugc.ShareContent": {
          shareCommentary: { text: message },
          shareMediaCategory: "NONE",
        },
      },
      visibility: {
        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC",
      },
    }),
  });
}
```

## Message Templates

Create reusable message templates:

```typescript
export function createCarDataMessage(data: CarRegistrationData) {
  const { month, year, total, topMakes } = data;

  return `🚗 Car Registration Update - ${month} ${year}

📊 Total Registrations: ${total.toLocaleString()}
🏆 Top Makes: ${topMakes.slice(0, 3).join(", ")}

📈 View detailed analysis: https://sgcarstrends.com/data/${year}/${month}

#SingaporeCars #CarRegistration #DataAnalytics`;
}

export function createCOEMessage(data: COEBiddingData) {
  const { biddingNo, category, premium } = data;

  return `💰 COE Bidding Results - Round ${biddingNo}

Category ${category}: $${premium.toLocaleString()}
Change: ${data.change > 0 ? "+" : ""}${data.change}%

Full results: https://sgcarstrends.com/coe/${biddingNo}

#COE #Singapore #CarPrices`;
}
```

## Common Tasks

### Adding a New Platform

1. Create integration file (e.g., `instagram.ts`)
2. Implement posting function with authentication
3. Add environment variables for credentials
4. Create message template
5. Add to workflow that triggers posting
6. Test with development credentials

### Debugging Posting Failures

Check these common issues:

1. **Authentication errors**:
   - Verify environment variables are set
   - Check token expiration (especially OAuth)
   - Validate API credentials in platform console

2. **API rate limits**:
   - Check platform rate limit documentation
   - Implement retry logic with backoff
   - Add rate limit tracking

3. **Message formatting**:
   - Verify character limits (Twitter: 280, LinkedIn: 3000)
   - Check for invalid characters or formatting
   - Test markdown/HTML support

4. **Network issues**:
   - Add timeout handling
   - Implement retry logic
   - Log full error responses

### Updating Message Templates

1. Locate template function
2. Update message structure
3. Test with sample data
4. Verify formatting on each platform:
   - Discord: Embeds and markdown
   - Telegram: Markdown or HTML
   - Twitter: Plain text, URLs, hashtags
   - LinkedIn: Rich text, mentions

### Rate Limiting

Implement rate limiting to avoid API restrictions:

```typescript
import { Ratelimit } from "@upstash/ratelimit";
import { redis } from "@/config/redis";

const ratelimit = new Ratelimit({
  redis,
  limiter: Ratelimit.slidingWindow(10, "1 h"), // 10 posts per hour
});

export async function postToTwitter(message: string) {
  const { success } = await ratelimit.limit("twitter-posts");

  if (!success) {
    throw new Error("Rate limit exceeded for Twitter");
  }

  // Post to Twitter...
}
```

## Environment Variables

### Telegram
- `TELEGRAM_BOT_TOKEN` - Bot token from @BotFather
- `TELEGRAM_CHAT_ID` - Channel or group chat ID

### Twitter
- `TWITTER_BEARER_TOKEN` - OAuth 2.0 bearer token
- `TWITTER_API_KEY` - API key (if using OAuth 1.0a)
- `TWITTER_API_SECRET` - API secret

### LinkedIn
- `LINKEDIN_ACCESS_TOKEN` - OAuth 2.0 access token
- `LINKEDIN_ORG_ID` - Organization ID for company pages

## Testing Social Media Posts

Run integration tests:
```bash
pnpm -F @sgcarstrends/api test -- src/lib/workflows/social
```

Test individual platforms:
```bash
# Start dev server
pnpm dev

# Trigger social media workflow
curl -X POST http://localhost:3000/api/workflows/social/test \
  -H "Content-Type: application/json" \
  -d '{"platform": "discord", "message": "Test post"}'
```

## Error Handling

Implement comprehensive error handling:

```typescript
export async function postToAllPlatforms(message: string) {
  const results = await Promise.allSettled([
    postToDiscord(message).catch(err => ({ platform: "Discord", error: err })),
    postToTelegram(message).catch(err => ({ platform: "Telegram", error: err })),
    postToTwitter(message).catch(err => ({ platform: "Twitter", error: err })),
    postToLinkedIn(message).catch(err => ({ platform: "LinkedIn", error: err })),
  ]);

  const failures = results
    .filter(r => r.status === "rejected")
    .map(r => r.reason);

  if (failures.length > 0) {
    console.error("Social media posting failures:", failures);
  }

  return {
    success: failures.length === 0,
    failures,
  };
}
```

## Platform Character Limits

Respect platform limits:
- **Twitter**: 280 characters
- **LinkedIn**: 3,000 characters (posts), 700 (comments)
- **Telegram**: 4,096 characters
- **Discord**: 2,000 characters (message), 6,000 (embed total)

Implement truncation:
```typescript
export function truncateMessage(message: string, limit: number): string {
  if (message.length <= limit) return message;
  return message.slice(0, limit - 3) + "...";
}
```

## References

- Platform API docs: Use Context7 for latest documentation
- Related files:
  - `apps/api/src/lib/workflows/social/` - All integrations
  - `apps/api/src/routes/workflows.ts` - Workflow routes
  - `apps/api/CLAUDE.md` - API service documentation

## Best Practices

1. **Error Handling**: Always handle API failures gracefully
2. **Rate Limiting**: Implement rate limits to avoid bans
3. **Credentials**: Never commit API keys or tokens
4. **Testing**: Test on sandbox/dev accounts first
5. **Monitoring**: Track posting success rates
6. **Formatting**: Preview messages on each platform
7. **Compliance**: Follow platform posting guidelines
8. **Retries**: Implement exponential backoff for retries
