---
name: newsletter-campaign-workflow
description: Guide for working with newsletter campaigns, RSS processing workflows, article generation, MailerLite integration, multi-tenant isolation, campaign status management, Vercel workflows, advertorial rotation, and publication automation. Use when creating campaigns, processing RSS feeds, generating articles, managing workflow steps, handling campaign statuses, or working with newsletter-related database operations.
---

# Newsletter Campaign Workflow Skill

## Purpose

Comprehensive guide for working with the AIProDaily newsletter platform's campaign workflow system, including RSS processing, article generation, multi-tenant data management, and automated publication.

## When to Use

Automatically activates when working with:
- Campaign creation and management
- RSS feed processing and article generation
- Workflow steps and automation
- Newsletter publication and sending
- MailerLite integration
- Multi-tenant campaign operations
- Advertorial and ad management
- Campaign status transitions

---

## System Architecture

### Multi-Tenant Structure

```
Newsletter (slug: "accounting")
  → publication_id (UUID)
    → Campaigns (daily)
      → RSS Posts (scored, assigned)
        → Articles (generated from posts)
          → Email (sent via MailerLite)
```

**CRITICAL**: ALL database queries MUST filter by `publication_id`

### Issue Status Lifecycle

```
draft → processing → ready → approved → sent
         ↓ (if error)
       failed
```

**Status Meanings**:
- `draft`: Issue created, ready for workflow
- `processing`: Workflow actively running
- `ready`: Content generated, ready for review
- `approved`: Manual approval for sending
- `sent`: Published to subscribers
- `failed`: Workflow error occurred

**Note:** "Issue" replaced "campaign" in the codebase. The `issues` table was formerly `newsletter_campaigns`.

---

## Core Workflow: 10-Step RSS Processing

**Location**: `src/lib/workflows/process-rss-workflow.ts`
**Architecture**: Vercel Workflows
**Timeout**: 800 seconds per step
**Trigger**: `/api/cron/trigger-workflow` (every 5 minutes)

### Workflow Steps

1. **Setup** (800s)
   - Create tomorrow's campaign
   - Select AI apps/prompts
   - Assign top 24 posts (12 primary + 12 secondary)
   - Run deduplication

2. **Generate Primary Titles** (800s)
   - Generate 6 primary headlines

3-4. **Generate Primary Bodies** (800s each)
   - Batch 1: Generate 3 primary articles
   - Batch 2: Generate 3 more primary articles

5. **Fact-Check Primary** (800s)
   - Fact-check all 6 primary articles
   - Store fact_check_score (0-10)

6. **Generate Secondary Titles** (800s)
   - Generate 6 secondary headlines

7-8. **Generate Secondary Bodies** (800s each)
   - Batch 1: Generate 3 secondary articles
   - Batch 2: Generate 3 more secondary articles

9. **Fact-Check Secondary** (800s)
   - Fact-check all 6 secondary articles

10. **Finalize** (800s)
    - Auto-select top 3 per section
    - Generate welcome section
    - Generate subject line
    - Set status to `draft`
    - Unassign unused posts

### Workflow Best Practices

✅ **Error Handling Pattern**:
```typescript
let retryCount = 0
const maxRetries = 2

while (retryCount <= maxRetries) {
  try {
    await processStep()
    return  // Success
  } catch (error) {
    retryCount++
    if (retryCount > maxRetries) {
      console.error('[Step X/10] Failed after retries')
      throw error
    }
    console.log(`[Step X/10] Retrying (${retryCount}/${maxRetries})...`)
    await new Promise(resolve => setTimeout(resolve, 2000))
  }
}
```

✅ **Logging Pattern**:
```typescript
// One-line summaries with prefixes
console.log('[Workflow] Step 1/10: Setup complete, 24 posts assigned')
console.log('[AI] Batch 1/4: Scored 3 posts, avg: 7.2')
console.error('[DB] Query failed:', error.message)
```

**Log Prefixes**:
- `[Workflow]` - Vercel Workflow orchestration
- `[RSS]` - RSS processing
- `[AI]` - OpenAI/Claude API calls
- `[DB]` - Database operations
- `[CRON]` - Cron job execution

---

## Critical Rules

### 1. Multi-Tenant Isolation

**ALWAYS filter by `publication_id`**:

```typescript
// ✅ CORRECT
const { data } = await supabaseAdmin
  .from('articles')
  .select('*')
  .eq('campaign_id', campaignId)
  .eq('publication_id', newsletterId)  // REQUIRED

// ❌ WRONG - Data leakage!
const { data } = await supabaseAdmin
  .from('articles')
  .select('*')
  .eq('campaign_id', campaignId)
```

### 2. Date/Time Handling

**NEVER use UTC conversions for date comparisons**:

```typescript
// ✅ CORRECT: Local date comparison
const dateStr = date.split('T')[0]  // "2025-01-07"
const today = new Date().toISOString().split('T')[0]
if (dateStr === today) { /* ... */ }

// ❌ FORBIDDEN: UTC conversion shifts dates
date.toISOString()  // Wrong timezone!
date.toUTCString()  // Breaks comparisons!
```

**Why**: UTC conversion shifts dates by timezone. Users expect Central Time.

### 3. Performance & Limits

**Hard Limits (Vercel)**:
- Workflow step timeout: **800 seconds** (13 minutes per step)
- API route timeout: **600 seconds** (10 minutes max)
- Log size: **10MB maximum**
- Memory: **1024MB default**

---

## AI Integration

### Standard Pattern: callAIWithPrompt()

**Location**: `src/lib/openai.ts`

```typescript
import { callAIWithPrompt } from '@/lib/openai'

const result = await callAIWithPrompt(
  'ai_prompt_primary_article_title',  // Key in app_settings
  newsletterId,
  {
    title: post.title,
    description: post.description,
    content: post.full_article_text
  }
)
// result = { headline: "Your Generated Title" }
```

**How it works**:
1. Loads complete JSON prompt from `app_settings` table
2. Replaces placeholders (e.g., `{{title}}`, `{{content}}`)
3. Calls AI API (OpenAI or Claude)
4. Returns parsed JSON response

### Prompt Storage Format

```sql
INSERT INTO app_settings (key, value, publication_id, ai_provider)
VALUES (
  'ai_prompt_primary_article_title',
  '{
    "model": "gpt-4o",
    "temperature": 0.7,
    "max_output_tokens": 500,
    "response_format": { "type": "json_schema", "json_schema": {...} },
    "messages": [
      {"role": "system", "content": "You are a headline writer..."},
      {"role": "user", "content": "Title: {{title}}\n\nWrite a headline."}
    ]
  }',
  'newsletter-uuid',
  'openai'
);
```

**All parameters stored in database, not hardcoded.**

---

## Database Schema (Key Tables)

**Note:** "Issues" replaced "campaigns" in the database. The table `issues` was formerly `newsletter_campaigns`.

```
publications (formerly newsletters)
  ├── issues (status: draft → processing → ready → sent)
  │   ├── issue_articles (primary section, 6 generated, 3 active)
  │   ├── secondary_articles (secondary section, 6 generated, 3 active)
  │   └── rss_posts (assigned posts)
  │       └── post_ratings (multi-criteria scores)
  │
  ├── rss_feeds (active/inactive, section assignment)
  ├── publication_settings (key-value config, scoped by publication_id)
  ├── advertisements (advertorials for rotation)
  ├── issue_advertisements (tracks ad usage per issue)
  └── archived_articles, archived_rss_posts (historical data)
```

---

## API Route Template

```typescript
// app/api/[feature]/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { supabaseAdmin } from '@/lib/supabase'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()

    if (!body.campaignId) {
      return NextResponse.json(
        { error: 'Missing campaignId' },
        { status: 400 }
      )
    }

    const result = await processData(body)
    return NextResponse.json({ data: result })

  } catch (error: any) {
    console.error('[API] Error:', error.message)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}

export const maxDuration = 600  // 10 minutes for long operations
```

---

## Common Tasks

### Create New Campaign

```typescript
const { data: campaign } = await supabaseAdmin
  .from('newsletter_campaigns')
  .insert({
    publication_id: newsletterId,
    date: tomorrowDate,  // YYYY-MM-DD format
    status: 'draft',
    subject_line: null
  })
  .select()
  .single()
```

### Assign RSS Posts to Campaign

```typescript
await supabaseAdmin
  .from('rss_posts')
  .update({
    campaign_id: campaignId,
    assigned_at: new Date().toISOString(),
    section: 'primary'  // or 'secondary'
  })
  .in('id', topPostIds)
  .eq('publication_id', newsletterId)  // REQUIRED
```

### Generate Article Content

```typescript
const result = await callAIWithPrompt(
  'ai_prompt_primary_article_body',
  newsletterId,
  {
    title: post.title,
    description: post.description,
    content: post.full_article_text
  }
)

await supabaseAdmin
  .from('articles')
  .insert({
    campaign_id: campaignId,
    publication_id: newsletterId,  // REQUIRED
    rss_post_id: post.id,
    headline: result.headline,
    article_text: result.body,
    fact_check_score: null,
    is_active: false
  })
```

---

## Automation & Cron Jobs

**Configuration**: `vercel.json`

### Active Crons
| Cron | Schedule | Purpose |
|------|----------|---------|
| `/api/cron/trigger-workflow` | Every 5 min | Trigger RSS workflow if scheduled |
| `/api/cron/ingest-rss` | Every 15 min | Fetch & score new RSS posts |
| `/api/cron/create-campaign` | Every 5 min | Create issue if schedule permits |
| `/api/cron/send-review` | Every 5 min | Send review emails (status: ready) |
| `/api/cron/send-final` | Every 5 min | Send final issues (status: approved) |
| `/api/cron/send-secondary` | Every 5 min | Send secondary newsletter |
| `/api/cron/monitor-workflows` | Every 5 min | Check for failed/stuck workflows |
| `/api/cron/process-mailerlite-updates` | Every 5 min | Process MailerLite webhooks |
| `/api/cron/cleanup-pending-submissions` | Daily 7 AM | Clear stale ad submissions |
| `/api/cron/import-metrics` | Daily 6 AM | Sync MailerLite metrics |
| `/api/cron/health-check` | Every 5 min (8AM-10PM) | System health check |

### Not Implemented (registered in vercel.json but empty)
| Cron | Schedule | Notes |
|------|----------|-------|
| `/api/cron/populate-events` | Every 5 min | Events system not implemented |
| `/api/cron/sync-events` | Daily midnight | Events system not implemented |
| `/api/cron/generate-weather` | Daily 8 PM | Route file missing |
| `/api/cron/collect-wordle` | Daily 7 PM | Route file missing |

---

## Troubleshooting

### Campaign Stuck in "processing"

```sql
-- Check workflow status
SELECT id, status, date, created_at, updated_at
FROM newsletter_campaigns
WHERE status = 'processing'
AND publication_id = 'your-newsletter-id'
ORDER BY created_at DESC;

-- Reset to draft (if needed)
UPDATE newsletter_campaigns
SET status = 'draft'
WHERE id = 'campaign-id'
AND publication_id = 'your-newsletter-id';
```

### Posts Not Scoring

1. Check RSS ingestion: `/api/cron/ingest-rss` logs
2. Verify criteria config: `SELECT * FROM app_settings WHERE key LIKE 'criteria_%' AND publication_id = ?`
3. Check prompts exist: `SELECT * FROM app_settings WHERE key LIKE 'ai_prompt_criteria_%' AND publication_id = ?`
4. Verify feeds active: `SELECT * FROM rss_feeds WHERE active = true AND publication_id = ?`

### Workflow Failures

1. Check Vercel logs: `vercel logs --since 1h`
2. Check workflow monitor cron: `/api/cron/monitor-workflows`
3. Look for timeout errors (step > 800s)
4. Check retry count in logs

---

## Reference Documentation

See `claude.md` in project root for:
- Complete workflow details
- Multi-criteria scoring system
- RSS feed management
- MailerLite integration
- Advertorial rotation
- Section management

---

**Skill Status**: ACTIVE ✅
**Line Count**: < 500 (following best practices) ✅
**Project-Specific**: Tailored for AIProDaily tech stack ✅
