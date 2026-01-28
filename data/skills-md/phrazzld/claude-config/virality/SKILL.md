---
name: virality
description: |
  Viral growth infrastructure. Social sharing, OG images, referral systems, distribution.
  Make your product inherently shareable. Audit, implement, verify—every time.
argument-hint: "[focus area, e.g. 'og-images' or 'referrals']"
---

# /virality

Make your product spread. Social sharing, referral loops, distribution channels—every time.

## Philosophy

**Virality is a feature, not an accident.** Products don't go viral by luck. They're engineered to spread.

**Every user interaction is a sharing opportunity.** Completed a task? Share it. Hit a milestone? Share it. Created something? Share it.

**Remove friction from sharing.** One click to share. Beautiful previews. Pre-filled copy.

**Measure the loop.** K-factor (viral coefficient) tells you if growth is self-sustaining.

## What This Does

Audits your product for shareability, identifies viral loop opportunities, implements sharing infrastructure, and verifies the mechanics work. Every run does the full cycle.

## Branching

Assumes you start on `master`/`main`. Before making code changes:

```bash
git checkout -b feat/virality-$(date +%Y%m%d)
```

## Process

### 1. Audit

#### Social Metadata Check

```bash
# OG tags present?
grep -rE "og:title|og:description|og:image" \
  --include="*.tsx" --include="*.ts" --include="*.html" \
  app/ src/ pages/ 2>/dev/null | head -5

# Twitter cards?
grep -rE "twitter:card|twitter:title|twitter:image" \
  --include="*.tsx" --include="*.ts" \
  app/ src/ pages/ 2>/dev/null | head -5

# Dynamic OG images?
[ -f "app/api/og/route.tsx" ] || [ -d "pages/api/og" ] && echo "✓ OG image endpoint" || echo "✗ OG image endpoint"

# Metadata in layout?
grep -q "generateMetadata\|metadata" app/layout.tsx 2>/dev/null && echo "✓ Root metadata" || echo "✗ Root metadata"
```

#### Share Mechanics Check

```bash
# Share buttons exist?
grep -rE "share|Share|navigator.share|clipboard" \
  --include="*.tsx" --include="*.ts" \
  components/ src/ 2>/dev/null | head -5

# Shareable URLs?
grep -rE "shareUrl|shareLink|getShareUrl" \
  --include="*.tsx" --include="*.ts" \
  . 2>/dev/null | grep -v node_modules | head -5

# Deep linking?
grep -rE "searchParams|useSearchParams|\[.*\]" \
  --include="*.tsx" --include="*.ts" \
  app/ pages/ 2>/dev/null | head -5
```

#### Referral System Check

```bash
# Referral codes?
grep -rE "referral|invite|inviteCode|refCode" \
  --include="*.tsx" --include="*.ts" --include="*.sql" \
  . 2>/dev/null | grep -v node_modules | head -5

# Attribution tracking?
grep -rE "utm_|referrer|attribution" \
  --include="*.tsx" --include="*.ts" \
  . 2>/dev/null | grep -v node_modules | head -5
```

#### Distribution Readiness Check

```bash
# Product Hunt assets?
[ -f "public/product-hunt-logo.png" ] || [ -d "public/launch" ] && echo "✓ Launch assets" || echo "✗ Launch assets"

# Press kit / media assets?
[ -d "public/press" ] || [ -d "public/media" ] && echo "✓ Press kit" || echo "✗ Press kit"

# Changelog / updates page?
[ -f "app/changelog/page.tsx" ] || [ -f "pages/changelog.tsx" ] && echo "✓ Changelog page" || echo "✗ Changelog page"
```

### 2. Plan

Every shareable product needs:

**Essential (every product):**
- Open Graph tags on all public pages
- Twitter Card tags
- Dynamic OG images for key content
- Copy-to-clipboard share URLs
- Mobile-friendly share (Web Share API)

**For user-generated content:**
- Unique shareable URLs per item
- Beautiful social previews per item
- One-click sharing after creation
- "Share your [thing]" prompts

**For growth:**
- Referral system with tracking
- Invite flows
- Attribution (UTM) tracking
- K-factor measurement

**For launches:**
- Product Hunt assets and timing
- Press kit with logos/screenshots
- Changelog page for updates
- Social proof (testimonials, stats)

### 3. Execute

#### Add Root Metadata

```typescript
// app/layout.tsx
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

#### Create Dynamic OG Image Endpoint

```typescript
// app/api/og/route.tsx
import { ImageResponse } from 'next/og';

export const runtime = 'edge';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const title = searchParams.get('title') ?? 'Your Product';
  const description = searchParams.get('description') ?? '';

  return new ImageResponse(
    (
      <div
        style={{
          height: '100%',
          width: '100%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: '#000',
          color: '#fff',
          fontFamily: 'system-ui',
        }}
      >
        <div style={{ fontSize: 60, fontWeight: 'bold' }}>{title}</div>
        {description && (
          <div style={{ fontSize: 30, marginTop: 20, opacity: 0.8 }}>
            {description}
          </div>
        )}
      </div>
    ),
    { width: 1200, height: 630 }
  );
}
```

#### Add Page-Specific Metadata

```typescript
// app/[slug]/page.tsx
import type { Metadata } from 'next';

export async function generateMetadata({ params }): Promise<Metadata> {
  const item = await getItem(params.slug);

  return {
    title: item.title,
    description: item.description,
    openGraph: {
      title: item.title,
      description: item.description,
      images: [`/api/og?title=${encodeURIComponent(item.title)}`],
    },
  };
}
```

#### Create Share Component

```typescript
// components/share-button.tsx
'use client';

import { useState } from 'react';

interface ShareButtonProps {
  url: string;
  title: string;
  text?: string;
}

export function ShareButton({ url, title, text }: ShareButtonProps) {
  const [copied, setCopied] = useState(false);

  const share = async () => {
    // Try native share first (mobile)
    if (navigator.share) {
      try {
        await navigator.share({ url, title, text });
        return;
      } catch {
        // User cancelled or not supported
      }
    }

    // Fallback to clipboard
    await navigator.clipboard.writeText(url);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <button onClick={share}>
      {copied ? 'Copied!' : 'Share'}
    </button>
  );
}
```

#### Add Share Prompts at Key Moments

```typescript
// After user completes an action
function onComplete() {
  // Show share prompt
  showShareModal({
    title: "You did the thing!",
    prompt: "Share your achievement?",
    url: `${baseUrl}/share/${resultId}`,
    prefilledText: "I just [did thing] with @YourProduct!",
  });
}
```

#### Implement Referral System

```typescript
// lib/referrals.ts
export function generateReferralCode(userId: string): string {
  // Short, memorable codes
  return `${userId.slice(0, 4).toUpperCase()}${randomChars(4)}`;
}

export function getReferralUrl(code: string): string {
  return `${process.env.NEXT_PUBLIC_APP_URL}?ref=${code}`;
}

// Track on signup
export async function trackReferral(newUserId: string, refCode: string | null) {
  if (!refCode) return;

  const referrer = await getUserByRefCode(refCode);
  if (!referrer) return;

  await db.referrals.create({
    referrerId: referrer.id,
    referredId: newUserId,
    code: refCode,
    createdAt: new Date(),
  });

  // Reward referrer (if applicable)
  await grantReferralReward(referrer.id);
}
```

#### Track Attribution (UTMs)

```typescript
// middleware.ts or on page load
export function captureAttribution() {
  if (typeof window === 'undefined') return;

  const params = new URLSearchParams(window.location.search);
  const attribution = {
    utm_source: params.get('utm_source'),
    utm_medium: params.get('utm_medium'),
    utm_campaign: params.get('utm_campaign'),
    ref: params.get('ref'),
    referrer: document.referrer,
  };

  // Store for later (signup, conversion)
  sessionStorage.setItem('attribution', JSON.stringify(attribution));
}
```

#### Measure K-Factor

```typescript
// K-factor = invites sent per user × conversion rate
// K > 1 means viral growth

export async function calculateKFactor(timeWindow: string = '30d') {
  const activeUsers = await countActiveUsers(timeWindow);
  const invitesSent = await countInvitesSent(timeWindow);
  const inviteConversions = await countInviteConversions(timeWindow);

  const invitesPerUser = invitesSent / activeUsers;
  const conversionRate = inviteConversions / invitesSent;
  const kFactor = invitesPerUser * conversionRate;

  return {
    kFactor,
    invitesPerUser,
    conversionRate,
    isViral: kFactor > 1,
  };
}
```

### 4. Verify

**Test OG tags:**
```bash
# Use a validator
open "https://www.opengraph.xyz/url/$(echo $YOUR_URL | jq -sRr @uri)"

# Or curl and check
curl -s "$YOUR_URL" | grep -E "og:|twitter:" | head -10
```

**Test dynamic OG images:**
```bash
# Check the endpoint works
curl -I "https://yoursite.com/api/og?title=Test"
# Should return image/png content-type
```

**Test share flow:**
1. Create/complete something in the app
2. Click share button
3. Verify URL is correct and copyable
4. Paste URL in Twitter/LinkedIn preview checker
5. Verify preview looks good

**Test referral flow:**
1. Get your referral link
2. Open in incognito
3. Sign up
4. Verify referral tracked
5. Verify referrer credited

**Test mobile share:**
1. Open on mobile device
2. Click share
3. Verify native share sheet appears
4. Complete share to an app

If any verification fails, go back and fix it.

## Viral Loop Patterns

### The Creation Loop
```
User creates something → Prompted to share → Friend sees → Creates their own → ...
```
Best for: Tools, generators, creative apps

### The Achievement Loop
```
User hits milestone → Shareable achievement card → Social proof → Friend tries → ...
```
Best for: Games, learning apps, fitness apps

### The Invitation Loop
```
User invites friend → Friend joins → Both rewarded → Friend invites → ...
```
Best for: Marketplaces, social apps, collaboration tools

### The Content Loop
```
User creates content → Content has product watermark → Viewer sees → Visits product → ...
```
Best for: Design tools, video editors, meme generators

## Launch Checklist

For Product Hunt and similar:

- [ ] OG image at exactly 1200x630
- [ ] Tagline under 60 characters
- [ ] Description under 260 characters
- [ ] 4-6 screenshots/GIFs
- [ ] Maker comment prepared
- [ ] First comment prepared
- [ ] Launch day = Tuesday/Wednesday
- [ ] Launch time = 12:01 AM PT
- [ ] Notify your network to upvote early

## CLI Tools

```bash
# Validate OG tags
npx open-graph-scraper https://yoursite.com

# Generate social images locally
npx @vercel/og-image "Title" --output og.png

# Check Twitter card
open "https://cards-dev.twitter.com/validator"
```

## Related Skills

- `launch-strategy` - Product launch planning
- `social-content` - Social media content creation
- `marketing-ideas` - Growth tactics
