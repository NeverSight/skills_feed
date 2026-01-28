---
name: fix-virality
description: |
  Run /check-virality, then fix the highest priority virality issue.
  Creates one fix per invocation. Invoke again for next issue.
  Use /log-virality-issues to create issues without fixing.
---

# /fix-virality

Fix the highest priority viral growth gap.

## What This Does

1. Invoke `/check-virality` to audit shareability
2. Identify highest priority gap
3. Fix that one issue
4. Verify the fix
5. Report what was done

**This is a fixer.** It fixes one issue at a time. Run again for next issue. Use `/virality` for full setup.

## Process

### 1. Run Primitive

Invoke `/check-virality` skill to get prioritized findings.

### 2. Fix Priority Order

Fix in this order:
1. **P0**: No OG tags, no root metadata
2. **P1**: Dynamic OG images, share mechanics, Twitter cards
3. **P2**: Referral system, UTM tracking, share prompts
4. **P3**: Launch assets, changelog

### 3. Execute Fix

**No OG tags (P0):**
Add to `app/layout.tsx`:
```typescript
import type { Metadata } from 'next';

export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_APP_URL!),
  title: {
    default: 'Your Product - Tagline',
    template: '%s | Your Product',
  },
  description: 'One sentence that makes people want to try it.',
  openGraph: {
    type: 'website',
    locale: 'en_US',
    siteName: 'Your Product',
    images: ['/og-default.png'],
  },
  twitter: {
    card: 'summary_large_image',
    creator: '@yourhandle',
  },
};
```

**No dynamic OG images (P1):**
```bash
pnpm add @vercel/og
```

Create `app/api/og/route.tsx`:
```typescript
import { ImageResponse } from 'next/og';

export const runtime = 'edge';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const title = searchParams.get('title') ?? 'Your Product';

  return new ImageResponse(
    (
      <div style={{
        height: '100%',
        width: '100%',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#000',
        color: '#fff',
      }}>
        <div style={{ fontSize: 60, fontWeight: 'bold' }}>{title}</div>
      </div>
    ),
    { width: 1200, height: 630 }
  );
}
```

**No share button (P1):**
Create `components/share-button.tsx`:
```typescript
'use client';

import { useState } from 'react';

export function ShareButton({ url, title }: { url: string; title: string }) {
  const [copied, setCopied] = useState(false);

  const share = async () => {
    if (navigator.share) {
      await navigator.share({ url, title });
    } else {
      await navigator.clipboard.writeText(url);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return <button onClick={share}>{copied ? 'Copied!' : 'Share'}</button>;
}
```

**No referral system (P2):**
Add referral tracking to database schema and implement referral code generation.

### 4. Verify

After fix:
```bash
# Test OG tags
curl -s https://yoursite.com | grep -E "og:|twitter:" | head -10

# Test OG image endpoint
curl -I "http://localhost:3000/api/og?title=Test"
```

Or use OG validators:
- https://www.opengraph.xyz/
- https://cards-dev.twitter.com/validator

### 5. Report

```
Fixed: [P0] No OG tags configured

Updated: app/layout.tsx
- Added metadataBase
- Added openGraph configuration
- Added Twitter card configuration

Verified: curl shows og:title, og:image, twitter:card

Next highest priority: [P1] No dynamic OG images
Run /fix-virality again to continue.
```

## Branching

Before making changes:
```bash
git checkout -b feat/virality-$(date +%Y%m%d)
```

## Single-Issue Focus

Each viral feature should be tested independently. Fix one at a time:
- Verify share previews look correct
- Test on actual social platforms
- Measure impact

Run `/fix-virality` repeatedly to build shareability.

## Related

- `/check-virality` - The primitive (audit only)
- `/log-virality-issues` - Create issues without fixing
- `/virality` - Full viral growth setup
- `/launch-strategy` - Launch planning
