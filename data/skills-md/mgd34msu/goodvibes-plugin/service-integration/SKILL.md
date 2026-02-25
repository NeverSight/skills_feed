---
name: service-integration
description: "Load PROACTIVELY when task involves connecting external services or third-party APIs. Use when user says \"add email sending\", \"integrate a CMS\", \"set up file uploads\", \"add analytics\", or \"connect to S3\". Covers email services (Resend, SendGrid), CMS platforms (Sanity, Contentful, Payload), file upload solutions (UploadThing, Cloudinary, S3), analytics integration, webhook handling, error recovery, and credential management."
metadata:
  version: 1.0.0
  category: outcome
  tags: [email, cms, uploads, resend, sendgrid, sanity, contentful, uploadthing, s3, analytics]
---

## Resources
```
scripts/
  validate-services.sh
references/
  service-patterns.md
```

# Service Integration Implementation

This skill guides you through integrating external services into applications, from service selection to production deployment. It leverages GoodVibes precision tools for type-safe, resilient service integrations with proper error handling and testing.

## When to Use This Skill

Use this skill when you need to:
- Integrate email providers (Resend, SendGrid, Postmark)
- Set up content management systems (Sanity, Contentful, Payload, Strapi)
- Implement file upload services (UploadThing, Cloudinary, S3)
- Add analytics and tracking (PostHog, Plausible, Google Analytics)
- Configure webhook endpoints for third-party services
- Implement retry logic and circuit breakers
- Test service integrations without hitting production APIs

## Prerequisites

**Required context:**
- Service requirements (email, CMS, uploads, analytics)
- Expected traffic volume and scale requirements
- Budget constraints
- Self-hosted vs managed service preference

**Tools:**
- precision_grep for detecting existing integrations
- precision_read for analyzing service configurations
- precision_write for creating integration code
- precision_exec for testing and validation
- discover for batch analysis

## Phase 1: Discovery - Detect Existing Integrations

Before adding new services, analyze existing integrations to maintain consistency.

### Step 1.1: Detect Service SDKs and Patterns

Use discover to analyze multiple aspects in parallel:

```yaml
discover:
  queries:
    - id: email-sdks
      type: grep
      pattern: "(resend|sendgrid|postmark|nodemailer)"
      glob: "package.json"
    
    - id: cms-sdks
      type: grep
      pattern: "(@sanity|contentful|@payloadcms|@strapi)"
      glob: "package.json"
    
    - id: upload-sdks
      type: grep
      pattern: "(uploadthing|cloudinary|@aws-sdk/client-s3)"
      glob: "package.json"
    
    - id: analytics-sdks
      type: grep
      pattern: "(posthog-js|plausible|@vercel/analytics)"
      glob: "package.json"
    
    - id: api-keys-env
      type: grep
      pattern: "(RESEND_|SENDGRID_|SANITY_|CONTENTFUL_|UPLOADTHING_|CLOUDINARY_|AWS_|POSTHOG_)"
      glob: ".env.example"
    
    - id: service-clients
      type: glob
      patterns: ["src/lib/*client.ts", "src/services/**/*.ts", "lib/services/**/*.ts"]
    
    - id: webhook-routes
      type: glob
      patterns: ["src/app/api/webhooks/**/*.ts", "pages/api/webhooks/**/*.ts"]
  
  verbosity: files_only
```

### Step 1.2: Analyze Service Client Patterns

Read existing service clients to understand the project's patterns:

```yaml
precision_read:
  files:
    - path: "src/lib/email-client.ts"
      extract: outline
    - path: "src/services/upload.ts"
      extract: symbols
  
  output:
    format: minimal
```

**Decision Point:** Use existing patterns for new integrations. If no patterns exist, follow the implementation guide below.

## Phase 2: Service Selection

Choose services based on requirements, scale, and budget.

### Email Services Decision Tree

**For transactional emails:**
- **Resend** - Best DX, React Email support, 100 emails/day free, $20/month for 50K
- **SendGrid** - Enterprise features, 100 emails/day free, $20/month for 100K
- **Postmark** - High deliverability focus, $15/month for 10K, no free tier
- **AWS SES** - Cheapest at scale ($0.10/1000), requires more setup

**For marketing emails:**
- **ConvertKit** - Creator-focused, $29/month for 1K subscribers
- **Mailchimp** - All-in-one platform, free for 500 subscribers
- **Loops** - Developer-friendly, $49/month for 2K subscribers

**Recommendation:** Start with Resend for transactional, migrate to SES at 1M+ emails/month.

### CMS Platform Decision Tree

**For structured content (blog, docs):**
- **Sanity** - Best DX, real-time collaboration, free tier generous
- **Contentful** - Enterprise-ready, robust GraphQL, complex pricing
- **Payload** - Self-hosted, full TypeScript, no vendor lock-in

**For app content (products, user-generated):**
- **Payload** - Best for complex data models, authentication built-in
- **Strapi** - Large plugin ecosystem, self-hosted

**For marketing pages:**
- **Builder.io** - Visual editor, A/B testing built-in
- **Sanity** - Developer-friendly, visual editing with Sanity Studio

**Recommendation:** Sanity for content-heavy sites, Payload for app backends.

### File Upload Decision Tree

**For images (profile pics, product photos):**
- **UploadThing** - Zero config, Next.js integration, $10/month for 2GB storage
- **Cloudinary** - Image transformations, free tier 25GB bandwidth
- **Vercel Blob** - Edge network, $0.15/GB storage

**For large files (videos, documents):**
- **AWS S3** - Industry standard, $0.023/GB storage, cheapest at scale
- **Cloudflare R2** - S3-compatible, zero egress fees, $0.015/GB storage
- **Backblaze B2** - Cheapest storage at $0.005/GB

**For user-facing uploads with virus scanning:**
- **UploadThing** - Built-in virus scanning
- **AWS S3 + Lambda** - DIY scanning with ClamAV

**Recommendation:** UploadThing for prototypes, S3/R2 for production scale.

### Analytics Decision Tree

**For product analytics:**
- **PostHog** - Self-hosted option, session replay, feature flags, free tier 1M events
- **Mixpanel** - User-centric analytics, free tier 20M events/month
- **Amplitude** - Advanced cohort analysis, free tier 10M events/month

**For web analytics:**
- **Plausible** - Privacy-focused, GDPR-compliant, $9/month for 10K pageviews
- **Umami** - Self-hosted, simple, open source
- **Vercel Analytics** - Web Vitals focus, free for Vercel projects

**Recommendation:** PostHog for product apps, Plausible for marketing sites.

## Phase 3: Email Integration

### Step 3.1: Install Resend SDK

```yaml
precision_exec:
  commands:
    - cmd: "npm install resend"
      expect:
        exit_code: 0
  
  verbosity: minimal
```

### Step 3.2: Create Email Client

Write a type-safe email client with error handling:

```yaml
precision_write:
  files:
    - path: "src/lib/email.ts"
      mode: fail_if_exists
      content: |
        import type { ReactElement } from 'react';
        import { Resend } from 'resend';
        
        if (!process.env.RESEND_API_KEY) {
          throw new Error('RESEND_API_KEY is required');
        }
        
        export const resend = new Resend(process.env.RESEND_API_KEY);
        
        export interface SendEmailOptions {
          to: string | string[];
          subject: string;
          html?: string;
          react?: ReactElement;
          from?: string;
        }
        
        export async function sendEmail(options: SendEmailOptions) {
          const { to, subject, html, react, from = 'noreply@yourapp.com' } = options;
          
          try {
            const { data, error } = await resend.emails.send({
              from,
              to,
              subject,
              html,
              react,
            });
            
            if (error) {
              console.error('[Email] Send failed:', error);
              throw new Error(`Email send failed: ${error.message}`);
            }
            
            console.log('[Email] Sent successfully:', data?.id);
            return { success: true, id: data?.id };
          } catch (error: unknown) {
            console.error('[Email] Unexpected error:', error);
            throw error;
          }
        }
  
  verbosity: minimal
```

### Step 3.3: Create React Email Templates

For transactional emails, use React Email for type-safe templates:

```yaml
precision_exec:
  commands:
    - cmd: "npm install react-email @react-email/components"
      expect:
        exit_code: 0
  
  verbosity: minimal
```

```yaml
precision_write:
  files:
    - path: "emails/welcome.tsx"
      mode: fail_if_exists
      content: |
        import {
          Body,
          Button,
          Container,
          Head,
          Heading,
          Html,
          Preview,
          Text,
        } from '@react-email/components';
        
        interface WelcomeEmailProps {
          userName: string;
          loginUrl: string;
        }
        
        export default function WelcomeEmail({ userName, loginUrl }: WelcomeEmailProps) {
          return (
            <Html>
              <Head />
              <Preview>Welcome to our platform!</Preview>
              <Body style={main}>
                <Container style={container}>
                  <Heading style={h1}>Welcome, {userName}!</Heading>
                  <Text style={text}>
                    We're excited to have you on board. Click the button below to get started.
                  </Text>
                  <Button href={loginUrl} style={button}>
                    Get Started
                  </Button>
                </Container>
              </Body>
            </Html>
          );
        }
        
        const main = { backgroundColor: '#f6f9fc', fontFamily: '-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif' };
        const container = { margin: '0 auto', padding: '40px 20px' };
        const h1 = { color: '#1f2937', fontSize: '24px', fontWeight: 'bold', marginBottom: '20px' };
        const text = { color: '#4b5563', fontSize: '16px', lineHeight: '24px', marginBottom: '20px' };
        const button = { backgroundColor: '#3b82f6', borderRadius: '6px', color: '#ffffff', display: 'inline-block', fontSize: '16px', fontWeight: '600', padding: '12px 24px', textDecoration: 'none' };
  
  verbosity: minimal
```

### Step 3.4: Document Environment Variables

```yaml
precision_write:
  files:
    - path: ".env.example"
      mode: overwrite
      content: |
        # Email (Resend)
        RESEND_API_KEY=your_resend_api_key_here
  
  verbosity: minimal
```

## Phase 4: CMS Integration

### Step 4.1: Install Sanity SDK

```yaml
precision_exec:
  commands:
    - cmd: "npm install @sanity/client @sanity/image-url"
      expect:
        exit_code: 0
  
  verbosity: minimal
```

### Step 4.2: Create Sanity Client

```yaml
precision_write:
  files:
    - path: "src/lib/sanity.ts"
      mode: fail_if_exists
      content: |
        import { createClient } from '@sanity/client';
        import imageUrlBuilder from '@sanity/image-url';
        import type { SanityImageSource } from '@sanity/image-url/lib/types/types';
        
        if (!process.env.NEXT_PUBLIC_SANITY_PROJECT_ID) {
          throw new Error('NEXT_PUBLIC_SANITY_PROJECT_ID is required');
        }
        
        if (!process.env.NEXT_PUBLIC_SANITY_DATASET) {
          throw new Error('NEXT_PUBLIC_SANITY_DATASET is required');
        }
        
        export const sanityClient = createClient({
          projectId: process.env.NEXT_PUBLIC_SANITY_PROJECT_ID,
          dataset: process.env.NEXT_PUBLIC_SANITY_DATASET,
          apiVersion: '2026-01-01', // Update to current API version date
          useCdn: process.env.NODE_ENV === 'production',
        });
        
        const builder = imageUrlBuilder(sanityClient);
        
        // Import from @sanity/image-url
        export function urlForImage(source: SanityImageSource) {
          return builder.image(source).auto('format').fit('max');
        }
        
        // Type-safe query helper
        export async function sanityFetch<T>(query: string, params?: Record<string, unknown>): Promise<T> {
          try {
            const result = await sanityClient.fetch<T>(query, params);
            return result;
          } catch (error: unknown) {
            console.error('[Sanity] Query failed:', error);
            throw new Error('Failed to fetch from Sanity');
          }
        }
  
  verbosity: minimal
```

### Step 4.3: Set Up Webhook Endpoint

For real-time content updates, implement a webhook handler:

```yaml
precision_write:
  files:
    - path: "src/app/api/webhooks/sanity/route.ts"
      mode: fail_if_exists
      content: |
        import { NextRequest, NextResponse } from 'next/server';
        import { revalidateTag } from 'next/cache';
        
        import { timingSafeEqual } from 'crypto';

        export async function POST(request: NextRequest) {
          const signature = request.headers.get('sanity-webhook-signature');
          
          // Verify webhook signature
          const secret = process.env.SANITY_WEBHOOK_SECRET;
          if (!secret) {
            return NextResponse.json({ error: 'Webhook secret not configured' }, { status: 500 });
          }
          const expected = Buffer.from(secret);
          const received = Buffer.from(signature || '');
          if (expected.length !== received.length || !timingSafeEqual(expected, received)) {
            return NextResponse.json({ error: 'Invalid signature' }, { status: 401 });
          }
          
          try {
            const body = await request.json();
            const { _type } = body;
            
            // Revalidate cache based on content type
            if (_type === 'post') {
              revalidateTag('posts');
            } else if (_type === 'page') {
              revalidateTag('pages');
            }
            
            console.log('[Webhook] Sanity content updated:', _type); // Note: Use structured logger in production
            return NextResponse.json({ revalidated: true });
          } catch (error: unknown) {
            console.error('[Webhook] Failed to process Sanity webhook:', error);
            return NextResponse.json({ error: 'Webhook processing failed' }, { status: 500 });
          }
        }
  
  verbosity: minimal
```

## Phase 5: File Upload Integration

### Step 5.1: Install UploadThing SDK

```yaml
precision_exec:
  commands:
    - cmd: "npm install uploadthing @uploadthing/react"
      expect:
        exit_code: 0
  
  verbosity: minimal
```

### Step 5.2: Create Upload Router

```yaml
precision_write:
  files:
    - path: "src/app/api/uploadthing/core.ts"
      mode: fail_if_exists
      content: |
        import { createUploadthing, type FileRouter } from 'uploadthing/next';
        
        const f = createUploadthing();
        
        export const ourFileRouter = {
          imageUploader: f({ image: { maxFileSize: '4MB', maxFileCount: 4 } })
            .middleware(async ({ req }) => {
              // Authenticate user (placeholder imports shown for context)
              // In real code: import { getUserFromRequest } from '@/lib/auth';
              const user = await getUserFromRequest(req); // Import from your auth module
              if (!user) throw new Error('Unauthorized');
              
              return { userId: user.id };
            })
            .onUploadComplete(async ({ metadata, file }) => {
              console.log('[Upload] Complete:', file.url);
              
              // Save to database (Assumes Prisma client or similar ORM)
              await db.image.create({
                data: {
                  url: file.url,
                  userId: metadata.userId,
                },
              });
              
              return { url: file.url };
            }),
          
          pdfUploader: f({ pdf: { maxFileSize: '16MB' } })
            .middleware(async ({ req }) => {
              const user = await getUserFromRequest(req);
              if (!user) throw new Error('Unauthorized');
              return { userId: user.id };
            })
            .onUploadComplete(async ({ metadata, file }) => {
              console.log('[Upload] PDF complete:', file.url);
              return { url: file.url };
            }),
        } satisfies FileRouter;
        
        export type OurFileRouter = typeof ourFileRouter;
  
  verbosity: minimal
```

### Step 5.3: Alternative - S3 Presigned URLs

For more control, use S3 with presigned URLs:

```yaml
precision_exec:
  commands:
    - cmd: "npm install @aws-sdk/client-s3 @aws-sdk/s3-request-presigner"
      expect:
        exit_code: 0
  
  verbosity: minimal
```

```yaml
precision_write:
  files:
    - path: "src/lib/s3.ts"
      mode: fail_if_exists
      content: |
        import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3';
        import { getSignedUrl } from '@aws-sdk/s3-request-presigner';
        
        // Validate S3 configuration
        if (!process.env.AWS_REGION || !process.env.AWS_ACCESS_KEY_ID || !process.env.AWS_SECRET_ACCESS_KEY || !process.env.AWS_S3_BUCKET) {
          throw new Error('Missing required AWS S3 environment variables');
        }
        
        const s3Client = new S3Client({
          region: process.env.AWS_REGION,
          credentials: {
            accessKeyId: process.env.AWS_ACCESS_KEY_ID,
            secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
          },
        });
        
        export async function getUploadUrl(key: string, contentType: string) {
          const command = new PutObjectCommand({
            Bucket: process.env.AWS_S3_BUCKET,
            Key: key,
            ContentType: contentType,
          });
          
          // URL expires in 5 minutes
          const url = await getSignedUrl(s3Client, command, { expiresIn: 300 });
          return url;
        }
  
  verbosity: minimal
```

## Phase 6: Analytics Integration

### Step 6.1: Install PostHog SDK

```yaml
precision_exec:
  commands:
    - cmd: "npm install posthog-js"
      expect:
        exit_code: 0
  
  verbosity: minimal
```

### Step 6.2: Create Analytics Provider

```yaml
precision_write:
  files:
    - path: "src/providers/analytics.tsx"
      mode: fail_if_exists
      content: |
        'use client';
        
        import { useEffect } from 'react';
        import type { ReactNode } from 'react';
        import posthog from 'posthog-js';
        
        export function AnalyticsProvider({ children }: { children: ReactNode }) {
          useEffect(() => {
            if (process.env.NEXT_PUBLIC_POSTHOG_KEY) {
              posthog.init(process.env.NEXT_PUBLIC_POSTHOG_KEY, {
                api_host: process.env.NEXT_PUBLIC_POSTHOG_HOST || 'https://app.posthog.com',
                loaded: (posthog) => {
                  if (process.env.NODE_ENV === 'development') {
                    posthog.opt_out_capturing(); // Disabled in dev to avoid polluting analytics (re-enable for testing with posthog.opt_in_capturing())
                  }
                },
              });
            }
          }, []);
          
          return <>{children}</>;
        }
        
        // Helper for tracking events
        export function trackEvent(eventName: string, properties?: Record<string, unknown>) {
          if (typeof window !== 'undefined') {
            posthog.capture(eventName, properties);
          }
        }
  
  verbosity: minimal
```

## Phase 7: Error Handling Patterns

### Step 7.1: Implement Exponential Backoff

For services with rate limits, implement retry logic:

```yaml
precision_write:
  files:
    - path: "src/lib/retry.ts"
      mode: fail_if_exists
      content: |
        export interface RetryOptions {
          maxAttempts?: number;
          initialDelayMs?: number;
          maxDelayMs?: number;
          backoffMultiplier?: number;
        }
        
        export async function withRetry<T>(
          fn: () => Promise<T>,
          options: RetryOptions = {}
        ): Promise<T> {
          const {
            maxAttempts = 3,
            initialDelayMs = 1000,
            maxDelayMs = 10000,
            backoffMultiplier = 2,
          } = options;
          
          let lastError: Error = new Error('All retry attempts failed');
          
          for (let attempt = 1; attempt <= maxAttempts; attempt++) {
            try {
              return await fn();
            } catch (error: unknown) {
              lastError = error instanceof Error ? error : new Error(String(error));
              
              if (attempt === maxAttempts) {
                break;
              }
              
              const delayMs = Math.min(
                initialDelayMs * Math.pow(backoffMultiplier, attempt - 1),
                maxDelayMs
              );
              
              console.log(`[Retry] Attempt ${attempt}/${maxAttempts} failed, retrying in ${delayMs}ms`); // Note: Use structured logger in production
              await new Promise(resolve => setTimeout(resolve, delayMs));
            }
          }
          
          throw lastError;
        }
  
  verbosity: minimal
```

### Step 7.2: Implement Circuit Breaker

Prevent cascading failures with a circuit breaker:

```yaml
precision_write:
  files:
    - path: "src/lib/circuit-breaker.ts"
      mode: fail_if_exists
      content: |
        export class CircuitBreaker {
          private failureCount = 0;
          private lastFailureTime: number | null = null;
          private state: 'closed' | 'open' | 'half-open' = 'closed';
          
          constructor(
            private readonly failureThreshold = 5,
            private readonly resetTimeoutMs = 60000
          ) {}
          
          async execute<T>(fn: () => Promise<T>): Promise<T> {
            if (this.state === 'open') {
              if (Date.now() - (this.lastFailureTime ?? 0) > this.resetTimeoutMs) {
                this.state = 'half-open';
              } else {
                throw new Error('Circuit breaker is open');
              }
            }
            
            try {
              const result = await fn();
              this.onSuccess();
              return result;
            } catch (error: unknown) {
              this.onFailure();
              throw error;
            }
          }
          
          private onSuccess() {
            this.failureCount = 0;
            this.state = 'closed';
          }
          
          private onFailure() {
            this.failureCount++;
            this.lastFailureTime = Date.now();
            
            if (this.failureCount >= this.failureThreshold) {
              this.state = 'open';
              console.error('[CircuitBreaker] Circuit opened due to repeated failures');
            }
          }
        }
  
  verbosity: minimal
```

## Phase 8: Testing Service Integrations

### Step 8.1: Mock Service Responses

Create mock implementations for testing:

```yaml
precision_write:
  files:
    - path: "src/lib/__mocks__/email.ts"
      mode: fail_if_exists
      content: |
        import { SendEmailOptions } from '../email';
        
        const sentEmails: Array<SendEmailOptions & { id: string }> = [];
        
        export async function sendEmail(options: SendEmailOptions) {
          const id = `mock-${Date.now()}`;
          sentEmails.push({ ...options, id });
          return { success: true, id };
        }
        
        export function getSentEmails() {
          return sentEmails;
        }
        
        export function clearSentEmails() {
          sentEmails.length = 0;
        }
  
  verbosity: minimal
```

### Step 8.2: Implement Webhook Testing

Test webhook handlers locally:

```yaml
precision_write:
  files:
    - path: "scripts/test-webhook.sh"
      mode: fail_if_exists
      content: |
        #!/usr/bin/env bash
        set -euo pipefail
        
        # Requires: bash 4+
        # Test Sanity webhook locally
        
        echo "[INFO] Testing Sanity webhook..."
        if curl -X POST http://localhost:3000/api/webhooks/sanity \
          -H "Content-Type: application/json" \
          -H "sanity-webhook-signature: $SANITY_WEBHOOK_SECRET" \
          -d '{
            "_type": "post",
            "_id": "test-123",
            "title": "Test Post"
          }'; then
          echo "[PASS] Webhook test successful"
        else
          echo "[FAIL] Webhook test failed"
          exit 1
        fi
  
  verbosity: minimal
```

## Phase 9: Validation

Run the validation script to ensure proper service integration:

```yaml
precision_exec:
  commands:
    - cmd: "bash plugins/goodvibes/skills/outcome/service-integration/scripts/validate-services.sh ."
      expect:
        exit_code: 0
  
  verbosity: standard
```

## Common Patterns

### Environment Variable Validation

Always validate required environment variables at startup:

```typescript
const requiredEnvVars = ['RESEND_API_KEY', 'SANITY_PROJECT_ID'];

for (const envVar of requiredEnvVars) {
  if (!process.env[envVar]) {
    throw new Error(`Missing required environment variable: ${envVar}`);
  }
}
```

### Rate Limiting Outbound Requests

Implement token bucket rate limiting:

```typescript
export class RateLimiter {
  private tokens: number;
  private lastRefill: number;
  
  constructor(
    private readonly maxTokens: number,
    private readonly refillRatePerSecond: number
  ) {
    this.tokens = maxTokens;
    this.lastRefill = Date.now();
  }
  
  async acquire(): Promise<void> {
    this.refill();
    
    if (this.tokens < 1) {
      const waitMs = (1 - this.tokens) * (1000 / this.refillRatePerSecond);
      await new Promise(resolve => setTimeout(resolve, waitMs));
      this.refill();
    }
    
    this.tokens -= 1;
  }
  
  private refill() {
    const now = Date.now();
    const elapsedSeconds = (now - this.lastRefill) / 1000;
    const tokensToAdd = elapsedSeconds * this.refillRatePerSecond;
    
    this.tokens = Math.min(this.maxTokens, this.tokens + tokensToAdd);
    this.lastRefill = now;
  }
}
```

## Anti-Patterns to Avoid

### 1. Hardcoded API Keys

**BAD:**
```typescript
const resend = new Resend('re_abc123');
```

**GOOD:**
```typescript
if (!process.env.RESEND_API_KEY) {
  throw new Error('RESEND_API_KEY is required');
}
const resend = new Resend(process.env.RESEND_API_KEY);
```

### 2. No Error Handling

**BAD:**
```typescript
const result = await resend.emails.send(options);
return result.data;
```

**GOOD:**
```typescript
const { data, error } = await resend.emails.send(options);
if (error) {
  console.error('[Email] Send failed:', error);
  throw new Error(`Email send failed: ${error.message}`);
}
return data;
```

### 3. Synchronous External Calls

**BAD:**
```typescript
// Blocking user request
await sendEmail({ to: user.email, subject: 'Welcome' });
return res.json({ success: true });
```

**ACCEPTABLE (for simple cases):**
```typescript
// Send email async
// Note: Fire-and-forget is only suitable for non-critical operations.
// For production: use a queue-based approach with retries (see BEST example below).
sendEmail({ to: user.email, subject: 'Welcome' })
  .catch(err => console.error('[Email] Failed:', err));
return res.json({ success: true });
```

**BEST (production-ready):**
```typescript
// Queue-based approach with retries
await emailQueue.add('welcome-email', {
  to: user.email,
  subject: 'Welcome'
});
return res.json({ success: true });
```

### 4. Missing Webhook Verification

**BAD:**
```typescript
export async function POST(request: NextRequest) {
  const body = await request.json();
  // Process without verification
}
```

**GOOD:**
```typescript
import { timingSafeEqual } from 'crypto';

export async function POST(request: NextRequest) {
  const signature = request.headers.get('webhook-signature');
  
  // Validate webhook secret
  const secret = process.env.WEBHOOK_SECRET;
  if (!secret) {
    return NextResponse.json({ error: 'Webhook secret not configured' }, { status: 500 });
  }
  
  const expected = Buffer.from(secret);
  const received = Buffer.from(signature || '');
  if (expected.length !== received.length || !timingSafeEqual(expected, received)) {
    return NextResponse.json({ error: 'Invalid signature' }, { status: 401 });
  }
  const body = await request.json();
  // Process
}
```

## Troubleshooting

### Email Not Sending

1. Verify API key is set: `printf "%s\n" "${RESEND_API_KEY:0:5}..."` (bash parameter expansion to display first 5 chars)
2. Check API key permissions in provider dashboard
3. Verify sender domain is verified
4. Check rate limits in provider logs
5. Enable debug logging: `resend.setDebug(true)`

### CMS Content Not Updating

1. Verify webhook endpoint is publicly accessible
2. Check webhook secret matches
3. Test webhook locally with ngrok
4. Verify cache revalidation is working
5. Check CMS webhook logs

### File Upload Failing

1. Verify file size is within limits
2. Check CORS configuration
3. Verify authentication middleware
4. Test with smaller file
5. Check S3 bucket permissions (if using S3)

### Analytics Events Not Tracking

1. Verify API key is set
2. Check ad blockers aren't blocking requests
3. Verify opt-out is disabled in development
4. Check browser console for errors
5. Test with PostHog debug mode

## Related Skills

- **api-design** - Type-safe API layer patterns
- **authentication** - Secure service access patterns
- **testing-strategy** - Testing service integrations

## Success Criteria

- [ ] Service SDK installed and client created
- [ ] Environment variables documented in .env.example
- [ ] Error handling implemented with retries
- [ ] Webhook endpoints have signature verification
- [ ] Rate limiting configured for outbound requests
- [ ] Mock implementations for testing
- [ ] No hardcoded API keys in source code
- [ ] All validation checks pass

## Additional Resources

- [Resend Documentation](https://resend.com/docs)
- [Sanity Documentation](https://www.sanity.io/docs)
- [UploadThing Documentation](https://docs.uploadthing.com)
- [PostHog Documentation](https://posthog.com/docs)
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [Webhook Best Practices](https://webhooks.fyi)
