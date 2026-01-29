---
name: ai-content-generation
description: AI content generation with OpenAI and Claude, callAIWithPrompt usage, prompt storage in app_settings, structured outputs, response format validation, multi-criteria scoring, rate limiting, JSON schema, and AI API best practices. Use when generating content, creating prompts, scoring articles, or working with OpenAI/Claude APIs.
---

# AI Content Generation - Integration Guide

## Purpose

Comprehensive guide for AI content generation in the AIProDaily platform, covering OpenAI/Claude integration, prompt management, structured outputs, and content scoring systems.

## When to Use

Automatically activates when:
- Calling AI APIs (OpenAI, Claude)
- Using `callAIWithPrompt()`
- Creating or modifying prompts
- Working with `app_settings` AI prompts
- Implementing content generation
- Building scoring systems
- Handling AI responses

---

## Core Pattern: callAIWithPrompt()

### Standard Usage

**Location**: `src/lib/openai.ts`

```typescript
import { callAIWithPrompt } from '@/lib/openai'

// Generate article title
const result = await callAIWithPrompt(
  'ai_prompt_primary_article_title',  // Prompt key in app_settings
  newsletterId,                        // Tenant context
  {
    // Variables for placeholder replacement
    title: post.title,
    description: post.description,
    content: post.full_article_text
  }
)

// result = { headline: "AI-Generated Title" }
```

### How It Works

1. **Loads prompt** from `app_settings` table by key + newsletter_id
2. **Replaces placeholders** like `{{title}}`, `{{content}}` with provided variables
3. **Calls AI API** (OpenAI or Claude) with complete request
4. **Parses response** according to `response_format` schema
5. **Returns** structured JSON object

### Key Features

✅ **Database-driven**: All prompts stored in database, not hardcoded
✅ **Tenant-scoped**: Each newsletter can customize prompts
✅ **Type-safe**: JSON schema enforces response structure
✅ **Flexible**: Supports both OpenAI and Claude
✅ **Reusable**: Same function for all AI operations

---

## Prompt Storage Format

### Database Schema

```sql
-- app_settings table
CREATE TABLE app_settings (
  key TEXT PRIMARY KEY,
  value JSONB NOT NULL,
  description TEXT,
  newsletter_id UUID NOT NULL,
  ai_provider TEXT,  -- 'openai' or 'claude'
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
)
```

### Complete Prompt Structure

```sql
INSERT INTO app_settings (key, value, newsletter_id, ai_provider, description)
VALUES (
  'ai_prompt_primary_article_title',
  '{
    "model": "gpt-4o",
    "temperature": 0.7,
    "max_output_tokens": 500,
    "response_format": {
      "type": "json_schema",
      "json_schema": {
        "name": "article_title_response",
        "strict": true,
        "schema": {
          "type": "object",
          "properties": {
            "headline": {
              "type": "string",
              "description": "The generated article headline"
            }
          },
          "required": ["headline"],
          "additionalProperties": false
        }
      }
    },
    "messages": [
      {
        "role": "system",
        "content": "You are an expert headline writer for accounting professionals..."
      },
      {
        "role": "user",
        "content": "Source Title: {{title}}\n\nSource Content: {{content}}\n\nWrite a compelling headline."
      }
    ]
  }'::jsonb,
  'newsletter-uuid-here',
  'openai',
  'Content Generation - Primary Article Title: Generates engaging headlines'
);
```

**All parameters stored in database**:
- `model` - AI model to use
- `temperature` - Creativity level (0-1)
- `max_output_tokens` - Response length limit
- `response_format` - JSON schema for structured output
- `messages` - System and user prompts with placeholders

---

## Response Format Patterns

### Simple String Response

```json
{
  "response_format": {
    "type": "json_schema",
    "json_schema": {
      "name": "simple_response",
      "strict": true,
      "schema": {
        "type": "object",
        "properties": {
          "result": { "type": "string" }
        },
        "required": ["result"],
        "additionalProperties": false
      }
    }
  }
}
```

### Complex Structured Response

```json
{
  "response_format": {
    "type": "json_schema",
    "json_schema": {
      "name": "article_body_response",
      "strict": true,
      "schema": {
        "type": "object",
        "properties": {
          "headline": { "type": "string" },
          "body": { "type": "string" },
          "summary": { "type": "string" },
          "key_points": {
            "type": "array",
            "items": { "type": "string" }
          }
        },
        "required": ["headline", "body"],
        "additionalProperties": false
      }
    }
  }
}
```

### Scoring Response

```json
{
  "response_format": {
    "type": "json_schema",
    "json_schema": {
      "name": "content_score_response",
      "strict": true,
      "schema": {
        "type": "object",
        "properties": {
          "score": {
            "type": "number",
            "minimum": 0,
            "maximum": 10
          },
          "reasoning": { "type": "string" }
        },
        "required": ["score", "reasoning"],
        "additionalProperties": false
      }
    }
  }
}
```

---

## Multi-Criteria Scoring System

### Overview

**Purpose**: Evaluate RSS posts using multiple weighted criteria
**Location**: `src/lib/rss-processor.ts`
**Storage**: `post_ratings` table

### Configuration

```typescript
// Criteria settings in app_settings
{
  "criteria_enabled_count": 3,  // 1-5 criteria
  "criteria_1_name": "Interest Level",
  "criteria_1_weight": 1.5,
  "criteria_2_name": "Relevance",
  "criteria_2_weight": 1.5,
  "criteria_3_name": "Impact",
  "criteria_3_weight": 1.0
}
```

### Scoring Process

```typescript
// Each criterion gets separate AI call
for (let i = 1; i <= criteriaCount; i++) {
  const promptKey = `ai_prompt_criteria_${i}`
  const weight = settings[`criteria_${i}_weight`]

  // Call AI for this criterion
  const result = await callAIWithPrompt(
    promptKey,
    newsletterId,
    {
      title: post.title,
      description: post.description,
      content: post.content
    }
  )

  // Store individual score
  await supabaseAdmin
    .from('post_ratings')
    .insert({
      post_id: post.id,
      newsletter_id: newsletterId,
      criterion_name: criteriaName,
      score: result.score,        // 0-10
      weighted_score: result.score * weight,
      reasoning: result.reasoning
    })
}

// Calculate total score (sum of weighted scores)
const totalScore = ratings.reduce((sum, r) => sum + r.weighted_score, 0)
```

### Example Scoring

```
Criterion 1: Interest Level (weight 1.5) → score 8 → weighted 12.0
Criterion 2: Relevance (weight 1.5)     → score 7 → weighted 10.5
Criterion 3: Impact (weight 1.0)        → score 6 → weighted 6.0
═══════════════════════════════════════════════════════════════
Total Score: 28.5
```

---

## Prompt Design Best Practices

### System Message

```typescript
{
  "role": "system",
  "content": `You are an expert content writer for accounting professionals.
Your audience is CPAs, accountants, and financial professionals.
Write in a professional yet engaging tone.
Focus on practical, actionable information.
Keep content concise and scannable.`
}
```

### User Message with Placeholders

```typescript
{
  "role": "user",
  "content": `Source Article:
Title: {{title}}
Description: {{description}}
Full Content: {{content}}

Task: Write a 200-300 word article summary that:
1. Captures the key takeaways
2. Explains why this matters to accountants
3. Uses clear, professional language
4. Ends with a thought-provoking statement

Output the summary as a JSON object with a "body" field.`
}
```

### Temperature Guidelines

```typescript
// Creative content (headlines, summaries)
"temperature": 0.7

// Factual content (analysis, scoring)
"temperature": 0.3

// Consistent output (classifications)
"temperature": 0.1
```

---

## Model Selection

### OpenAI Models

```typescript
// Fast, cost-effective (most common)
"model": "gpt-4o"

// Latest, most capable
"model": "gpt-4o-2024-11-20"

// Smaller, faster for simple tasks
"model": "gpt-4o-mini"
```

### Claude Models

```typescript
// Most capable
"model": "claude-3-5-sonnet-20241022"

// Fast, cost-effective
"model": "claude-3-5-haiku-20241022"

// Older, still powerful
"model": "claude-3-opus-20240229"
```

---

## Error Handling

### Standard Pattern

```typescript
try {
  const result = await callAIWithPrompt(
    promptKey,
    newsletterId,
    variables
  )

  // Validate response
  if (!result || !result.headline) {
    throw new Error('Invalid AI response: missing required fields')
  }

  return result

} catch (error: any) {
  console.error('[AI] Error calling AI:', error.message)

  // Check for specific errors
  if (error.message.includes('rate_limit')) {
    console.error('[AI] Rate limit exceeded, implement backoff')
  }
  if (error.message.includes('context_length')) {
    console.error('[AI] Input too long, need to truncate')
  }

  throw error
}
```

### Retry with Backoff

```typescript
async function callAIWithRetry(
  promptKey: string,
  newsletterId: string,
  variables: Record<string, any>,
  maxRetries = 2
) {
  let retryCount = 0

  while (retryCount <= maxRetries) {
    try {
      return await callAIWithPrompt(promptKey, newsletterId, variables)
    } catch (error: any) {
      retryCount++

      // Don't retry on validation errors
      if (error.message.includes('Invalid')) {
        throw error
      }

      if (retryCount > maxRetries) {
        throw error
      }

      console.log(`[AI] Retry ${retryCount}/${maxRetries} after error`)
      await new Promise(resolve => setTimeout(resolve, 2000 * retryCount))
    }
  }
}
```

---

## Rate Limiting

### OpenAI Limits

**Tier 1** (free/trial):
- gpt-4o: 500 requests/day
- gpt-4o-mini: 10,000 requests/day

**Tier 2** (paid):
- gpt-4o: 5,000 requests/min
- gpt-4o-mini: 30,000 requests/min

### Batching Strategy

```typescript
// Process in batches to avoid rate limits
const BATCH_SIZE = 3
const BATCH_DELAY = 2000  // 2 seconds between batches

const batches = chunkArray(posts, BATCH_SIZE)

for (const batch of batches) {
  // Process batch in parallel
  await Promise.all(
    batch.map(post => generateArticle(post))
  )

  // Wait before next batch
  if (batches.indexOf(batch) < batches.length - 1) {
    await new Promise(resolve => setTimeout(resolve, BATCH_DELAY))
  }
}

console.log(`[AI] Processed ${posts.length} items in ${batches.length} batches`)
```

---

## Content Generation Workflows

### Article Title Generation

```typescript
const titleResult = await callAIWithPrompt(
  'ai_prompt_primary_article_title',
  newsletterId,
  {
    title: rssPost.title,
    description: rssPost.description,
    content: rssPost.full_article_text
  }
)

// Store generated title
await supabaseAdmin
  .from('articles')
  .insert({
    newsletter_id: newsletterId,
    campaign_id: campaignId,
    rss_post_id: rssPost.id,
    headline: titleResult.headline,
    article_text: null  // Body generated separately
  })
```

### Article Body Generation

```typescript
const bodyResult = await callAIWithPrompt(
  'ai_prompt_primary_article_body',
  newsletterId,
  {
    title: rssPost.title,
    headline: article.headline,  // Use AI-generated headline
    description: rssPost.description,
    content: rssPost.full_article_text
  }
)

// Update with generated body
await supabaseAdmin
  .from('articles')
  .update({
    article_text: bodyResult.body
  })
  .eq('id', article.id)
  .eq('newsletter_id', newsletterId)
```

### Fact-Checking

```typescript
const factCheckResult = await callAIWithPrompt(
  'ai_prompt_fact_check',
  newsletterId,
  {
    headline: article.headline,
    body: article.article_text,
    source_content: article.rss_post.full_article_text
  }
)

// Store fact-check score
await supabaseAdmin
  .from('articles')
  .update({
    fact_check_score: factCheckResult.score,
    fact_check_reasoning: factCheckResult.reasoning
  })
  .eq('id', article.id)
  .eq('newsletter_id', newsletterId)
```

---

## Testing Prompts

### Test in Isolation

```typescript
// Create test route: app/api/test/prompt/route.ts
export async function POST(request: NextRequest) {
  const { promptKey, variables } = await request.json()

  try {
    const result = await callAIWithPrompt(
      promptKey,
      'test-newsletter-id',
      variables
    )

    return NextResponse.json({
      success: true,
      result
    })
  } catch (error: any) {
    return NextResponse.json({
      error: error.message
    }, { status: 500 })
  }
}

export const maxDuration = 60
```

### Validate Response Schema

```typescript
function validateArticleResponse(result: any): boolean {
  if (!result) return false
  if (typeof result.headline !== 'string') return false
  if (typeof result.body !== 'string') return false
  if (result.headline.length < 10) return false
  if (result.body.length < 50) return false
  return true
}
```

---

## Best Practices

### ✅ DO:

- Store all prompts in `app_settings` database
- Use JSON schema for response format validation
- Include clear instructions in system message
- Use placeholders for dynamic content
- Implement retry logic for transient errors
- Batch API calls to respect rate limits
- Validate AI responses before using
- Log AI calls for debugging
- Use appropriate temperature for task
- Test prompts thoroughly before production

### ❌ DON'T:

- Hardcode prompts in code
- Skip response validation
- Ignore rate limits
- Use overly complex prompts
- Forget error handling
- Expose API keys client-side
- Use wrong model for task
- Trust AI output blindly
- Skip testing with real data
- Make unbatched parallel calls

---

## Troubleshooting

### AI Returns Invalid Format

**Check**:
1. JSON schema is correct
2. `strict: true` is set
3. Instructions are clear
4. Model supports structured outputs

### Rate Limit Errors

**Solutions**:
1. Implement batching (3-5 requests per batch)
2. Add delays between batches (2-5 seconds)
3. Use retry with exponential backoff
4. Upgrade API tier if needed

### Content Quality Issues

**Improve**:
1. Refine system message instructions
2. Adjust temperature (lower for consistency)
3. Provide better examples in prompt
4. Add validation rules
5. Use more capable model

### Timeout Errors

**Fix**:
1. Reduce max_output_tokens
2. Simplify prompt
3. Use faster model (gpt-4o-mini, claude-haiku)
4. Increase API route maxDuration

---

## Reference

**Main Function**: `src/lib/openai.ts` - `callAIWithPrompt()`
**Prompt Storage**: `app_settings` table
**Response Storage**: `articles`, `post_ratings` tables
**Scoring Logic**: `src/lib/rss-processor.ts`

**Related Docs**:
- `docs/AI_PROMPT_SYSTEM_GUIDE.md`
- `docs/OPENAI_RESPONSES_API_GUIDE.md`
- `docs/workflows/MULTI_CRITERIA_SCORING_GUIDE.md`

---

**Skill Status**: ACTIVE ✅
**Line Count**: < 500 ✅
**Integration**: OpenAI + Claude ✅
