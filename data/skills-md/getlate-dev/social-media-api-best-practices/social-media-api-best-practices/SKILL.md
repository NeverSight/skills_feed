---
name: social-media-api-best-practices
description: Best practices for integrating social media APIs (Instagram, TikTok, YouTube, Twitter/X, LinkedIn, Facebook, Threads, Pinterest, Bluesky, Snapchat, Google Business, Reddit, Telegram). Covers OAuth, AT Protocol, rate limiting, media uploads, encryption, and error handling. Use when building social media integrations, scheduling systems, or debugging platform API issues.
---

# Social Media API Best Practices

Battle-tested patterns from scheduling 1M+ posts across 13 platforms.

---

## 1. Authentication Patterns

### OAuth 2.0 Platforms

**Instagram (Meta Graph API)**
- Two-step token exchange: short-lived (1 hour) → long-lived (60 days)
- Use `auth_type: 'rerequest'` to force permission re-prompts
- Exchange endpoint: `ig_exchange_token` grant type
- Scopes: `instagram_business_basic`, `instagram_business_content_publish`, `instagram_business_manage_messages`, `instagram_business_manage_comments`, `instagram_business_manage_insights`

**Twitter/X (PKCE Required)**
- PKCE with S256 code challenge is mandatory
- Embed code verifier in state: `${state}-cv_${codeVerifier}`
- Scopes: `tweet.read`, `tweet.write`, `users.read`, `offline.access`, `media.write`, `dm.read`, `dm.write`
- Access token: 2 hours, refresh token: long-lived

```typescript
function generateCodeVerifier(): string {
  return crypto.randomBytes(32).toString('base64url');
}

function generateCodeChallenge(verifier: string): string {
  return crypto.createHash('sha256').update(verifier).digest('base64url');
}

function extractCodeVerifierFromState(state: string): string {
  const match = state.match(/-cv_(.+)$/);
  return match ? match[1] : '';
}
```

**TikTok**
- Full UX compliance required for API audit approval
- Must show: privacy_level selector, comment/duet/stitch toggles
- Commercial content disclosure mandatory
- Scopes: `user.info.basic`, `user.info.profile`, `user.info.stats`, `video.publish`, `video.upload`, `video.list`

**LinkedIn**
- Always include header: `X-RestLi-Protocol-Version: 2.0.0`
- API version header: `LinkedIn-Version: 202511` (some endpoints use `202505` or `202401`)
- Access token: 60 days, refresh token: 365 days
- Supports both personal (`urn:li:person:`) and organization (`urn:li:organization:`) posts
- Personal scopes: `openid`, `profile`, `r_basicprofile`, `email`, `w_member_social`, `w_member_social_feed`, `r_member_postAnalytics`, `r_member_profileAnalytics`, `r_1st_connections_size`
- Organization scopes: `w_organization_social`, `w_organization_social_feed`, `r_organization_admin`, `r_organization_social`, `r_organization_social_feed`, `r_organization_followers`

**YouTube**
- Requires `access_type=offline` AND `prompt=consent` for refresh tokens
- Supports both user channels and brand accounts
- Scopes: `youtube.upload`, `youtube`, `youtube.force-ssl`, `yt-analytics.readonly`

**Facebook**
- Page access tokens are separate from user tokens
- Exchange user token for page token via `/me/accounts`
- Supports scheduled publishing via `scheduled_publish_time`
- Scopes: `pages_manage_posts`, `pages_show_list`, `pages_read_engagement`, `pages_manage_engagement`, `pages_read_user_content`, `business_management`, `pages_messaging`

**Threads**
- Similar to Instagram (Meta), 2-step token exchange
- Use `th_exchange_token` grant type
- Scopes: `threads_basic`, `threads_content_publish`, `threads_manage_replies`, `threads_read_replies`, `threads_manage_insights`, `threads_delete`

**Pinterest**
- OAuth 2.0 with refresh tokens
- Scopes: `pins:read`, `pins:write`, `boards:read`, `boards:write`, `user_accounts:read`

**Google Business Profile**
- Google OAuth with scopes: `business.manage`, `userinfo.profile`, `userinfo.email`
- Uses My Business v4 API

**Reddit**
- OAuth with `duration=permanent` for long-lived tokens
- **Strict user-agent requirement** - Reddit enforces descriptive user agents
- Scopes: `identity`, `submit`, `read`, `mysubreddits`, `privatemessages`, `history`, `edit`, `vote`

```typescript
const headers = {
  'User-Agent': 'YourApp/1.0 by /u/YourUsername'
};
```

### Non-OAuth Platforms

**Bluesky (AT Protocol)**
- No traditional OAuth - uses DIDs (Decentralized Identifiers)
- Authentication via `accessJwt` + `refreshJwt` from AT Protocol
- PDS (Personal Data Server) resolution required
- Auto-refresh on `ExpiredToken` error

```typescript
// Bluesky authentication
const session = await agent.login({
  identifier: 'user.bsky.social',
  password: 'app-password'
});
// session contains: accessJwt, refreshJwt, did, handle
```

**Snapchat**
- Basic auth, **allowlist-only** (requires Snapchat dev team approval)
- Limited public API - profile API focus
- Scopes: `snapchat-profile-api`

**Telegram**
- **Bot token only** - no OAuth flow
- Token format: `BOT_ID:SECRET`
- No user authentication, bot must be added to chat/channel

---

## 2. Rate Limiting Strategies

### Platform-Specific Limits

| Platform | Key Limit | Strategy |
|----------|-----------|----------|
| Instagram | 100 posts/day per account | Queue and spread |
| TikTok | 5 pending uploads/24h | Wait for processing |
| Twitter | 3-tier limits (app + user + endpoint) | Check all three |
| LinkedIn | Generous general, strict bulk | Batch carefully |
| YouTube | Daily upload quota per channel | Monitor quota |
| Reddit | 60 requests/minute | Respect headers |
| Threads | Aggressive rate limiting | Fails fast |

### Twitter's Three-Tier Rate Limits

Twitter has THREE levels of limits - check all:

1. **App-level 24-hour limit** (most restrictive)
2. **User-level 24-hour limit**
3. **Endpoint-specific rate limit**

```typescript
function parseRateLimitHeaders(headers: Headers) {
  return {
    // Endpoint limits
    remaining: parseInt(headers.get('x-rate-limit-remaining') || '0'),
    reset: parseInt(headers.get('x-rate-limit-reset') || '0'),
    // App-level 24h limits
    appRemaining: parseInt(headers.get('x-app-limit-24hour-remaining') || '0'),
    appReset: parseInt(headers.get('x-app-limit-24hour-reset') || '0'),
    // User-level 24h limits
    userRemaining: parseInt(headers.get('x-user-limit-24hour-remaining') || '0'),
    userReset: parseInt(headers.get('x-user-limit-24hour-reset') || '0'),
  };
}
```

### Exponential Backoff Pattern

```typescript
async function withRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 3,
  baseDelay = 5000
): Promise<T> {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (!isRetryableError(error) || attempt === maxRetries) throw error;
      const delay = Math.min(baseDelay * Math.pow(2, attempt), 30000);
      await sleep(delay);
    }
  }
  throw new Error('Max retries exceeded');
}

function isRetryableError(error: any): boolean {
  const status = error.status || error.statusCode;
  return [429, 500, 502, 503].includes(status);
}
```

---

## 3. Media Requirements

### Complete Platform Limits

| Platform | Max Image | Max Video | Aspect Ratio | Special |
|----------|-----------|-----------|--------------|---------|
| Instagram | 8MB | 100MB stories, 300MB reels | 4:5 to 1.91:1 feed, 9:16 stories | 10 carousel items |
| TikTok | 20MB | 4GB, 3s-10min | 9:16 strict | 35 photo carousel |
| Twitter | 5MB | 512MB, 2min 20s | Flexible | 1-4 images |
| LinkedIn | 8MB | 5GB | Flexible | 20 image carousel |
| YouTube | 2MB thumbnail | 256GB | 16:9 preferred | Resumable upload |
| Facebook | 10MB | 4GB | Flexible | 10 multi-image |
| Threads | 8MB | 1GB, 5min | 9:16 vertical | 10 carousel |
| Pinterest | 32MB | 2GB | Flexible | Requires cover image |
| Bluesky | 1MB | 50MB, 3min | Flexible | AT Protocol |
| Snapchat | 20MB | 500MB | 9:16 | **AES encryption** |
| Google Business | 5MB | N/A | Flexible | Images only |
| Reddit | 20MB | N/A | Flexible | Via URL |
| Telegram | 10MB | 50MB | Flexible | 4096 char limit |

### Golden Rule: Stream Large Files

Never load entire files into memory:

```typescript
// BAD - loads entire file into memory
const buffer = await fetch(url).then(r => r.arrayBuffer());

// GOOD - streams directly
const response = await fetch(url);
await uploadToPlatform(response.body); // Pass the stream
```

### Problematic Media Sources

These hosts return HTML or timeout instead of direct media:

```typescript
const PROBLEMATIC_HOSTS = [
  'drive.google.com',
  'docs.google.com',
  'dropbox.com',
  'onedrive.live.com',
  '1drv.ms'
];

// Solution: Re-host to your own storage first
if (PROBLEMATIC_HOSTS.some(h => url.includes(h))) {
  url = await reHostToStorage(url);
}
```

### Dropbox URL Fix

```typescript
function fixDropboxUrl(url: string): string {
  if (url.includes('dropbox.com') && url.includes('dl=0')) {
    return url.replace('dl=0', 'dl=1');
  }
  return url;
}
```

---

## 4. Video Upload Patterns

### Chunked Upload (Twitter)

```typescript
async function chunkedUpload(videoBuffer: Buffer, mediaType: string) {
  const CHUNK_SIZE = 4 * 1024 * 1024; // 4MB chunks

  // INIT
  const initRes = await api.post('/media/upload', {
    command: 'INIT',
    total_bytes: videoBuffer.length,
    media_type: mediaType
  });
  const mediaId = initRes.media_id_string;

  // APPEND chunks
  for (let i = 0; i < Math.ceil(videoBuffer.length / CHUNK_SIZE); i++) {
    const chunk = videoBuffer.slice(i * CHUNK_SIZE, (i + 1) * CHUNK_SIZE);
    await api.post('/media/upload', {
      command: 'APPEND',
      media_id: mediaId,
      media: chunk.toString('base64'),
      segment_index: i
    });
  }

  // FINALIZE
  await api.post('/media/upload', {
    command: 'FINALIZE',
    media_id: mediaId
  });

  // Poll for processing
  await pollProcessingStatus(mediaId);

  return mediaId;
}
```

### Resumable Upload (YouTube)

YouTube supports resumable uploads for reliability with large files. Use the `youtube-chunked-upload` module or implement the resumable upload protocol.

### Processing Status Polling

```typescript
async function pollProcessingStatus(mediaId: string, maxWaitMs = 300000) {
  const startTime = Date.now();

  while (Date.now() - startTime < maxWaitMs) {
    const status = await api.get(`/media/upload?command=STATUS&media_id=${mediaId}`);

    if (status.processing_info?.state === 'succeeded') return;
    if (status.processing_info?.state === 'failed') {
      throw new Error(status.processing_info.error?.message || 'Processing failed');
    }

    const checkAfter = (status.processing_info?.check_after_secs || 5) * 1000;
    await sleep(checkAfter);
  }

  throw new Error('Processing timeout');
}
```

---

## 5. Error Handling

### Error Categorization

```typescript
type ErrorType = 'refresh-token' | 'retry' | 'user-error';

function categorizeError(platform: string, error: any): ErrorType {
  if (isTokenError(error)) return 'refresh-token';
  if (isTemporaryError(error)) return 'retry';
  return 'user-error';
}
```

### Instagram Error Codes

| Code | Meaning | Action |
|------|---------|--------|
| 2207001 | Spam detected | User error |
| 2207003 | Media download timeout | Retry |
| 2207004 | Image too large (>8MB) | Compress |
| 2207006 | Media not found | User error |
| 2207026 | Unsupported video format | Re-encode |
| 2207042 | 100 posts/day exceeded | Wait 24h |
| 2207050 | User restricted | User error |
| **2207051** | **Blocked (but may have posted!)** | **Verify** |
| 2207052 | Media fetch failed | Use direct URLs |

### The Instagram 2207051 Edge Case

Instagram's anti-spam sometimes returns "blocked" but actually publishes:

```typescript
async function handleInstagram2207051(accountId: string) {
  await sleep(5000);

  const recentMedia = await getRecentMedia(accountId);
  const justPosted = recentMedia.find(m =>
    Date.now() - new Date(m.timestamp).getTime() < 60000
  );

  if (justPosted) {
    return { success: true, postId: justPosted.id };
  }
  throw new Error('Post actually failed');
}
```

### TikTok Error Codes

| Code | Meaning | Action |
|------|---------|--------|
| access_token_invalid | Token expired | Refresh |
| scope_not_authorized | Missing permission | Reconnect |
| rate_limit_exceeded | Too many requests | Retry |
| spam_risk_* | Content flagged | User error |
| file_format_check_failed | Invalid format | User error |
| unaudited_client_can_only_post_to_private | Dev mode | Private only |

### Twitter/X Error Codes

| Code | Meaning | Action |
|------|---------|--------|
| invalid_grant | Token revoked | Reconnect |
| usage-capped | Rate limited | Retry |
| duplicate | Same content exists | User error |
| 186 | Tweet too long | User error |

### Bluesky Error Codes

| Code | Meaning | Action |
|------|---------|--------|
| ExpiredToken | JWT expired | Auto-refresh |
| InvalidToken | Bad token | Reconnect |
| XRPCNotSupported | App password lacks DM | Use full auth |

### Reddit Error Codes

| Code | Meaning | Action |
|------|---------|--------|
| invalid token | Expired | Refresh |
| not allowed to submit | Subreddit restriction | User error |
| RATELIMIT | Too fast | Retry with delay |
| NO_LINKS | Links not allowed | User error |

### Telegram Error Codes

| Code | Meaning | Action |
|------|---------|--------|
| message too long | >4096 chars | Truncate |
| chat not found | Invalid chat ID | User error |
| bot was blocked | User blocked bot | User error |

---

## 6. Platform Quirks

### JavaScript Large Integer IDs (Instagram/Facebook)

Instagram IDs exceed MAX_SAFE_INTEGER (17+ digits):

```typescript
function safeJsonParse(text: string) {
  // Wrap large integers in quotes before parsing
  const safe = text.replace(/"id"\s*:\s*(\d{15,})/g, '"id":"$1"');
  return JSON.parse(safe);
}
```

### Twitter Character Counting

```typescript
function countTwitterCharacters(text: string): number {
  let count = 0;

  // URLs always count as 23 characters
  const urlRegex = /https?:\/\/[^\s]+/g;
  const urls = text.match(urlRegex) || [];
  const textWithoutUrls = text.replace(urlRegex, '');

  count += urls.length * 23;

  // Emojis and CJK count as 2
  for (const char of textWithoutUrls) {
    count += char.match(/[\u{1F600}-\u{1F64F}]|[\u4e00-\u9fff]/u) ? 2 : 1;
  }

  return count;
}
```

### Twitter Character Limits by Tier

| Tier | Limit |
|------|-------|
| Free | 280 |
| Premium | 4,000 |
| Premium+ | 25,000 |

### LinkedIn Text Escaping

Reserved characters: `| { } [ ] ( ) < > # \ * _ ~`

Note: `@` is deliberately NOT escaped to avoid `\@` showing in posts. URN mentions `@[Name](urn:li:person:ID)` and hashtags `#tag` are preserved automatically.

```typescript
function escapeLinkedInText(text: string): string {
  // Reserved chars (excluding @ to preserve readability)
  const reserved = /[\|\{\}\[\]\(\)\<\>\#\\\*\_\~]/;

  let output = '';
  let i = 0;

  while (i < text.length) {
    // Preserve URN mentions: @[Display Name](urn:li:person:ID)
    if (text[i] === '@' && text[i + 1] === '[') {
      const closeBracket = text.indexOf(']', i + 2);
      if (closeBracket !== -1 && text.substring(closeBracket + 1, closeBracket + 9) === '(urn:li:') {
        const closeParen = text.indexOf(')', closeBracket + 9);
        if (closeParen !== -1) {
          output += text.substring(i, closeParen + 1);
          i = closeParen + 1;
          continue;
        }
      }
    }

    // Preserve hashtags: #word
    if (text[i] === '#' && /[a-zA-Z0-9_]/.test(text[i + 1] || '')) {
      output += text[i++];
      while (i < text.length && /[a-zA-Z0-9_]/.test(text[i])) {
        output += text[i++];
      }
      continue;
    }

    // Escape reserved characters
    output += reserved.test(text[i]) ? '\\' + text[i] : text[i];
    i++;
  }

  return output;
}
```

### TikTok UX Compliance Requirements

TikTok requires full UX compliance for API audit:
- User must manually select privacy level (no defaults)
- Must show comment/duet/stitch toggles
- Commercial content disclosure with user confirmation
- Content preview before upload
- Express consent declaration

### Reddit User-Agent Requirement

Reddit strictly enforces descriptive user agents:

```typescript
// BAD - will be blocked
headers['User-Agent'] = 'axios/1.0';

// GOOD - descriptive format
headers['User-Agent'] = 'MyApp/1.0 (by /u/developer_username)';
```

### Telegram HTML Subset

Only these HTML tags are supported:

```html
<b>, <strong>       <!-- bold -->
<i>, <em>           <!-- italic -->
<u>                 <!-- underline -->
<s>, <strike>, <del><!-- strikethrough -->
<code>              <!-- monospace -->
<pre>               <!-- code block -->
<a href="...">      <!-- link -->
<tg-spoiler>        <!-- spoiler -->
<blockquote>        <!-- quote -->
```

---

## 7. Special Protocols

### AT Protocol (Bluesky)

Bluesky uses AT Protocol, not OAuth:

**Key Concepts:**
- **DID** (Decentralized Identifier): User's permanent ID (e.g., `did:plc:abc123`)
- **PDS** (Personal Data Server): Where user data lives
- **Handle**: Human-readable name (e.g., `user.bsky.social`)

**Rich Text Facets:**

Mentions and links use byte-offset positioning:

```typescript
function createFacets(text: string): Facet[] {
  const facets: Facet[] = [];
  const encoder = new TextEncoder();

  // Find mentions
  const mentionRegex = /@([a-zA-Z0-9.-]+)/g;
  let match;

  while ((match = mentionRegex.exec(text)) !== null) {
    const beforeText = text.slice(0, match.index);
    const byteStart = encoder.encode(beforeText).length;
    const byteEnd = byteStart + encoder.encode(match[0]).length;

    facets.push({
      index: { byteStart, byteEnd },
      features: [{
        $type: 'app.bsky.richtext.facet#mention',
        did: await resolveDid(match[1])
      }]
    });
  }

  return facets;
}
```

### Snapchat AES-256-CBC Encryption

Snapchat requires media encryption before upload:

```typescript
import crypto from 'crypto';

function encryptForSnapchat(buffer: Buffer): {
  encrypted: Buffer;
  key: string;
  iv: string;
} {
  const key = crypto.randomBytes(32); // 256 bits
  const iv = crypto.randomBytes(16);  // 128 bits

  const cipher = crypto.createCipheriv('aes-256-cbc', key, iv);
  const encrypted = Buffer.concat([
    cipher.update(buffer),
    cipher.final()
  ]);

  return {
    encrypted,
    key: key.toString('base64'),
    iv: iv.toString('base64')
  };
}
```

---

## 8. Quick Debugging Checklist

When a post fails:

1. **Check token validity** - Is the access token expired?
2. **Check rate limits** - Hit daily/hourly limits?
3. **Check media URL** - Can the platform fetch it directly?
4. **Check media specs** - Right format, size, dimensions, aspect ratio?
5. **Check the 2207051 case** - Did it post despite the error?
6. **Check account status** - Is the account restricted?
7. **Check subreddit rules** - (Reddit) Links allowed? Flair required?
8. **Check user-agent** - (Reddit) Descriptive enough?
9. **Check bot permissions** - (Telegram) Bot in chat with send rights?

---

## 9. Recommended Architecture

```
your-app/
├── lib/
│   ├── platforms/
│   │   ├── base.ts           # Abstract base class
│   │   ├── instagram.ts
│   │   ├── tiktok.ts
│   │   ├── twitter.ts
│   │   ├── bluesky.ts        # AT Protocol
│   │   ├── snapchat.ts       # With encryption
│   │   └── ...
│   ├── utils/
│   │   ├── rate-limiter.ts
│   │   ├── media-handler.ts
│   │   ├── error-mapper.ts
│   │   └── encryption.ts     # For Snapchat
│   └── queue/
│       └── scheduler.ts
```

---

## 10. Platform Comparison Matrix

| Feature | Instagram | TikTok | Twitter | LinkedIn | YouTube | Facebook | Threads | Pinterest | Bluesky | Snapchat | GBP | Reddit | Telegram |
|---------|-----------|--------|---------|----------|---------|----------|---------|-----------|---------|----------|-----|--------|----------|
| OAuth | 2-step | Standard | PKCE | Standard | Google | Standard | 2-step | Basic | AT Proto | Basic | Google | Standard | Bot Token |
| Token Life | 60d | 2y+ | 2h+refresh | 365d refresh | 1y | 60d+ | 60d | N/A | Auto | N/A | 1y | Permanent | N/A |
| Video | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | No | No | Yes |
| Carousel | 10 | 35 | 4 | 20 | No | 10 | 10 | No | 4 | No | No | Gallery | Album 10 |
| Scheduling | API | Draft | No | API | API | API | API | No | API | No | No | No | No |
| DMs | Yes | No | Yes | Yes | No | Yes | No | No | Yes | Yes | No | Yes | Yes |
| Analytics | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | No | No | Limited | No | Limited |

---

## About This Guide

This guide is maintained by [Late](https://getlate.dev), built from real patterns learned while scheduling **1M+ posts** across all 13 platforms.

Every error code, edge case, and quirk documented here comes from production experience. The Instagram 2207051 gotcha? We discovered it after hours of debugging. The Snapchat encryption requirement? Learned the hard way.

**Building a social media app?** If you'd rather not implement and maintain all these integrations yourself, [Late's API](https://getlate.dev) handles the complexity for you: OAuth, media processing, rate limits, error handling, and scheduling across all 13 platforms with a single integration.

---

*Maintained by [Late](https://getlate.dev) - Social Media Scheduling API for Developers*
