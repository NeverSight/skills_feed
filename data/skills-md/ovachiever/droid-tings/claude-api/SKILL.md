---
name: claude-api
description: |
  Build with Claude Messages API using structured outputs (v0.69.0+, Nov 2025) for guaranteed JSON schema validation. Covers prompt caching (90% savings), streaming SSE, tool use, model deprecations (3.5/3.7 retired Oct 2025). Use when: building chatbots/agents with validated JSON responses, or troubleshooting rate_limit_error, structured output validation, prompt caching not activating, streaming SSE parsing.
license: MIT
metadata:
  version: 2.0.0
  last_verified: 2025-11-22
  sdk_version: 0.70.1
  token_savings: ~48%
  errors_prevented: 12
  breaking_changes: Oct 2025 - Claude 3.5/3.7 models retired, Nov 2025 - Structured outputs beta
  keywords:
    - claude api
    - anthropic api
    - messages api
    - "@anthropic-ai/sdk"
    - structured outputs
    - output_format
    - strict tool use
    - json schema validation
    - claude streaming
    - prompt caching
    - cache_control
    - tool use
    - vision
    - extended thinking
    - claude sonnet 4.5
    - claude haiku 4.5
    - claude opus 4
    - function calling
    - SSE
    - rate limits
    - 429 errors
    - agent skills api
    - context management
    - clear thinking
    - streaming sse parsing
    - prompt caching not working
    - structured output validation
    - model deprecated
    - model retired
---

# Claude API - Structured Outputs & Error Prevention Guide

**Package**: @anthropic-ai/sdk@0.70.1 (Nov 20, 2025)
**Breaking Changes**: Oct 2025 - Claude 3.5/3.7 models retired, Nov 2025 - Structured outputs beta
**Last Updated**: 2025-11-22

---

## What's New in v0.69.0+ (Nov 2025)

**Major Features:**

### 1. Structured Outputs (v0.69.0, Nov 14, 2025) - CRITICAL ⭐

**Guaranteed JSON schema conformance** - Claude's responses strictly follow your JSON schema with two modes:

**JSON Outputs (`output_format`)** - For data extraction and formatting:
```typescript
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

const message = await anthropic.messages.create({
  model: 'claude-sonnet-4-5-20250929',
  max_tokens: 1024,
  messages: [{ role: 'user', content: 'Extract contact info: John Doe, john@example.com, 555-1234' }],
  betas: ['structured-outputs-2025-11-13'],
  output_format: {
    type: 'json_schema',
    json_schema: {
      name: 'Contact',
      strict: true,
      schema: {
        type: 'object',
        properties: {
          name: { type: 'string' },
          email: { type: 'string' },
          phone: { type: 'string' }
        },
        required: ['name', 'email', 'phone'],
        additionalProperties: false
      }
    }
  }
});

// Guaranteed valid JSON matching schema
const contact = JSON.parse(message.content[0].text);
console.log(contact.name); // "John Doe"
```

**Strict Tool Use (`strict: true`)** - For validated function parameters:
```typescript
const message = await anthropic.messages.create({
  model: 'claude-sonnet-4-5-20250929',
  max_tokens: 1024,
  messages: [{ role: 'user', content: 'Get weather for San Francisco' }],
  betas: ['structured-outputs-2025-11-13'],
  tools: [{
    name: 'get_weather',
    description: 'Get current weather',
    input_schema: {
      type: 'object',
      properties: {
        location: { type: 'string' },
        unit: { type: 'string', enum: ['celsius', 'fahrenheit'] }
      },
      required: ['location'],
      additionalProperties: false
    },
    strict: true  // ← Guarantees schema compliance
  }]
});
```

**Requirements:**
- **Beta header**: `structured-outputs-2025-11-13` (via `betas` array)
- **Models**: Claude Sonnet 4.5, Claude Opus 4.1 only
- **SDK**: v0.69.0+ required

**Limitations:**
- ❌ No recursive schemas
- ❌ No numerical constraints (`minimum`, `maximum`)
- ❌ Limited regex support (no backreferences/lookahead)
- ❌ Incompatible with citations and message prefilling
- ⚠️ Grammar compilation adds latency on first request (cached 24hrs)

**When to Use:**
- Data extraction from unstructured text
- API response formatting
- Agentic workflows requiring validated tool inputs
- Eliminating JSON parse errors

### 2. Model Changes (Oct 2025) - BREAKING

**Retired (return errors):**
- ❌ Claude 3.5 Sonnet (all versions)
- ❌ Claude 3.7 Sonnet - DEPRECATED (Oct 28, 2025)

**Active Models (Nov 2025):**

| Model | ID | Context | Best For | Cost (per MTok) |
|-------|-----|---------|----------|-----------------|
| **Claude Sonnet 4.5** | claude-sonnet-4-5-20250929 | 200k | Balanced performance | $3/$15 (in/out) |
| **Claude Opus 4** | claude-opus-4-20250514 | 200k | Highest capability | $15/$75 |
| **Claude Haiku 4.5** | claude-3-5-haiku-20241022 | 200k | Near-frontier, fast | $1/$5 |

### 3. Context Management (Oct 28, 2025)

**Clear Thinking Blocks** - Automatic thinking block cleanup:
```typescript
const message = await anthropic.messages.create({
  model: 'claude-sonnet-4-5-20250929',
  max_tokens: 4096,
  messages: [{ role: 'user', content: 'Solve complex problem' }],
  betas: ['clear_thinking_20251015']
});
// Thinking blocks automatically managed
```

### 4. Agent Skills API (Oct 16, 2025)

Pre-built skills for Office files (PowerPoint, Excel, Word, PDF):
```typescript
const message = await anthropic.messages.create({
  model: 'claude-sonnet-4-5-20250929',
  max_tokens: 1024,
  messages: [{ role: 'user', content: 'Analyze this spreadsheet' }],
  betas: ['skills-2025-10-02'],
  // Requires code execution tool enabled
});
```

📚 **Docs**: https://platform.claude.com/docs/en/build-with-claude/structured-outputs

---

## Streaming Responses (SSE)

**CRITICAL Error Pattern** - Errors occur AFTER initial 200 response:
```typescript
const stream = anthropic.messages.stream({
  model: 'claude-sonnet-4-5-20250929',
  max_tokens: 1024,
  messages: [{ role: 'user', content: 'Hello' }],
});

stream
  .on('error', (error) => {
    // Error can occur AFTER stream starts
    console.error('Stream error:', error);
    // Implement fallback or retry logic
  })
  .on('abort', (error) => {
    console.warn('Stream aborted:', error);
  });
```

**Why this matters**: Unlike regular HTTP errors, SSE errors happen mid-stream after 200 OK, requiring error event listeners

---

## Prompt Caching (⭐ 90% Cost Savings)

**CRITICAL Rule** - `cache_control` MUST be on LAST block:
```typescript
const message = await anthropic.messages.create({
  model: 'claude-sonnet-4-5-20250929',
  max_tokens: 1024,
  system: [
    {
      type: 'text',
      text: 'System instructions...',
    },
    {
      type: 'text',
      text: LARGE_CODEBASE, // 50k tokens
      cache_control: { type: 'ephemeral' }, // ← MUST be on LAST block
    },
  ],
  messages: [{ role: 'user', content: 'Explain auth module' }],
});

// Monitor cache usage
console.log('Cache reads:', message.usage.cache_read_input_tokens);
console.log('Cache writes:', message.usage.cache_creation_input_tokens);
```

**Minimum requirements:**
- Claude Sonnet 4.5: 1,024 tokens minimum
- Claude Haiku 4.5: 2,048 tokens minimum
- 5-minute TTL (refreshes on each use)
- Cache shared only with IDENTICAL content

---

## Tool Use (Function Calling)

**CRITICAL Patterns:**

**Strict Tool Use** (with structured outputs):
```typescript
const message = await anthropic.messages.create({
  model: 'claude-sonnet-4-5-20250929',
  max_tokens: 1024,
  betas: ['structured-outputs-2025-11-13'],
  tools: [{
    name: 'get_weather',
    description: 'Get weather data',
    input_schema: {
      type: 'object',
      properties: {
        location: { type: 'string' },
        unit: { type: 'string', enum: ['celsius', 'fahrenheit'] }
      },
      required: ['location'],
      additionalProperties: false
    },
    strict: true  // ← Guarantees schema compliance
  }],
  messages: [{ role: 'user', content: 'Weather in NYC?' }]
});
```

**Tool Result Pattern** - `tool_use_id` MUST match:
```typescript
const toolResults = [];
for (const block of response.content) {
  if (block.type === 'tool_use') {
    const result = await executeToolFunction(block.name, block.input);

    toolResults.push({
      type: 'tool_result',
      tool_use_id: block.id,  // ← MUST match tool_use block id
      content: JSON.stringify(result),
    });
  }
}

messages.push({
  role: 'user',
  content: toolResults,
});
```

**Error Handling** - Handle tool execution failures:
```typescript
try {
  const result = await executeToolFunction(block.name, block.input);
  toolResults.push({
    type: 'tool_result',
    tool_use_id: block.id,
    content: JSON.stringify(result),
  });
} catch (error) {
  // Return error to Claude for handling
  toolResults.push({
    type: 'tool_result',
    tool_use_id: block.id,
    is_error: true,
    content: `Tool execution failed: ${error.message}`,
  });
}
```

---

## Vision (Image Understanding)

**CRITICAL Rules:**
- **Formats**: JPEG, PNG, WebP, GIF (non-animated)
- **Max size**: 5MB per image
- **Base64 overhead**: ~33% size increase
- **Context impact**: Images count toward token limit
- **Caching**: Consider for repeated image analysis

**Format validation** - Check before encoding:
```typescript
const validFormats = ['image/jpeg', 'image/png', 'image/webp', 'image/gif'];
if (!validFormats.includes(mimeType)) {
  throw new Error(`Unsupported format: ${mimeType}`);
}
```

---

## Extended Thinking Mode

**⚠️ Model Compatibility:**
- ❌ Claude 3.7 Sonnet - DEPRECATED (Oct 28, 2025)
- ❌ Claude 3.5 Sonnet - RETIRED (not supported)
- ✅ Claude Sonnet 4.5 - Extended thinking supported
- ✅ Claude Opus 4 - Extended thinking supported

**CRITICAL:**
- Thinking blocks are NOT cacheable
- Requires higher `max_tokens` (thinking consumes tokens)
- Check model before expecting thinking blocks

---

## Rate Limits

**CRITICAL Pattern** - Respect `retry-after` header with exponential backoff:
```typescript
async function makeRequestWithRetry(
  requestFn: () => Promise<any>,
  maxRetries = 3,
  baseDelay = 1000
): Promise<any> {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await requestFn();
    } catch (error) {
      if (error.status === 429) {
        // CRITICAL: Use retry-after header if present
        const retryAfter = error.response?.headers?.['retry-after'];
        const delay = retryAfter
          ? parseInt(retryAfter) * 1000
          : baseDelay * Math.pow(2, attempt);

        console.warn(`Rate limited. Retrying in ${delay}ms...`);
        await new Promise(resolve => setTimeout(resolve, delay));
      } else {
        throw error;
      }
    }
  }
  throw new Error('Max retries exceeded');
}
```

**Rate limit headers:**
- `anthropic-ratelimit-requests-limit` - Total RPM allowed
- `anthropic-ratelimit-requests-remaining` - Remaining requests
- `anthropic-ratelimit-requests-reset` - Reset timestamp

---

## Error Handling

**Common Error Codes:**

| Status | Error Type | Cause | Solution |
|--------|-----------|-------|----------|
| 400 | invalid_request_error | Bad parameters | Validate request body |
| 401 | authentication_error | Invalid API key | Check env variable |
| 403 | permission_error | No access to feature | Check account tier |
| 404 | not_found_error | Invalid endpoint | Check API version |
| 429 | rate_limit_error | Too many requests | Implement retry logic |
| 500 | api_error | Internal error | Retry with backoff |
| 529 | overloaded_error | System overloaded | Retry later |

**CRITICAL:**
- Streaming errors occur AFTER initial 200 response
- Always implement error event listeners for streams
- Respect `retry-after` header on 429 errors
- Have fallback strategies for critical operations

---

## Known Issues Prevention

This skill prevents **12** documented issues:

### Issue #1: Rate Limit 429 Errors Without Backoff
**Error**: `429 Too Many Requests: Number of request tokens has exceeded your per-minute rate limit`
**Source**: https://docs.claude.com/en/api/errors
**Why It Happens**: Exceeding RPM, TPM, or daily token limits
**Prevention**: Implement exponential backoff with `retry-after` header respect

### Issue #2: Streaming SSE Parsing Errors
**Error**: Incomplete chunks, malformed SSE events
**Source**: Common SDK issue (GitHub #323)
**Why It Happens**: Network interruptions, improper event parsing
**Prevention**: Use SDK stream helpers, implement error event listeners

### Issue #3: Prompt Caching Not Activating
**Error**: High costs despite cache_control blocks
**Source**: https://platform.claude.com/docs/en/build-with-claude/prompt-caching
**Why It Happens**: `cache_control` placed incorrectly (must be at END)
**Prevention**: Always place `cache_control` on LAST block of cacheable content

### Issue #4: Tool Use Response Format Errors
**Error**: `invalid_request_error: tools[0].input_schema is invalid`
**Source**: API validation errors
**Why It Happens**: Invalid JSON Schema, missing required fields
**Prevention**: Validate schemas with JSON Schema validator, test thoroughly

### Issue #5: Vision Image Format Issues
**Error**: `invalid_request_error: image source must be base64 or url`
**Source**: API documentation
**Why It Happens**: Incorrect encoding, unsupported formats
**Prevention**: Validate format (JPEG/PNG/WebP/GIF), proper base64 encoding

### Issue #6: Token Counting Mismatches for Billing
**Error**: Unexpected high costs, context window exceeded
**Source**: Token counting differences
**Why It Happens**: Not accounting for special tokens, formatting
**Prevention**: Use official token counter, monitor usage headers

### Issue #7: System Prompt Ordering Issues
**Error**: System prompt ignored or overridden
**Source**: API behavior
**Why It Happens**: System prompt placed after messages array
**Prevention**: ALWAYS place system prompt before messages

### Issue #8: Context Window Exceeded (200k)
**Error**: `invalid_request_error: messages: too many tokens`
**Source**: Model limits
**Why It Happens**: Long conversations without pruning
**Prevention**: Implement message history pruning, use caching

### Issue #9: Extended Thinking on Wrong Model
**Error**: No thinking blocks in response
**Source**: Model capabilities
**Why It Happens**: Using retired/deprecated models (3.5/3.7 Sonnet)
**Prevention**: Only use extended thinking with Claude Sonnet 4.5 or Claude Opus 4

### Issue #10: API Key Exposure in Client Code
**Error**: CORS errors, security vulnerability
**Source**: Security best practices
**Why It Happens**: Making API calls from browser
**Prevention**: Server-side only, use environment variables

### Issue #11: Rate Limit Tier Confusion
**Error**: Lower limits than expected
**Source**: Account tier system
**Why It Happens**: Not understanding tier progression
**Prevention**: Check Console for current tier, auto-scales with usage

### Issue #12: Message Batches Beta Headers Missing
**Error**: `invalid_request_error: unknown parameter: batches`
**Source**: Beta API requirements
**Why It Happens**: Missing `anthropic-beta` header
**Prevention**: Include `anthropic-beta: message-batches-2024-09-24` header

---

## Official Documentation

- **Claude API**: https://platform.claude.com/docs/en/api
- **Messages API**: https://platform.claude.com/docs/en/api/messages
- **Structured Outputs**: https://platform.claude.com/docs/en/build-with-claude/structured-outputs
- **Prompt Caching**: https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- **Tool Use**: https://platform.claude.com/docs/en/build-with-claude/tool-use
- **Vision**: https://platform.claude.com/docs/en/build-with-claude/vision
- **Rate Limits**: https://platform.claude.com/docs/en/api/rate-limits
- **Errors**: https://platform.claude.com/docs/en/api/errors
- **TypeScript SDK**: https://github.com/anthropics/anthropic-sdk-typescript
- **Context7 Library ID**: /anthropics/anthropic-sdk-typescript

---

## Package Versions

**Latest**: @anthropic-ai/sdk@0.70.1 (Nov 20, 2025)

```json
{
  "dependencies": {
    "@anthropic-ai/sdk": "^0.70.1"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "typescript": "^5.3.0",
    "zod": "^3.23.0"
  }
}
```

---

**Token Efficiency**:
- **Without skill**: ~8,000 tokens (basic setup, streaming, caching, tools, vision, errors)
- **With skill**: ~4,200 tokens (knowledge gaps + error prevention + critical patterns)
- **Savings**: ~48% (~3,800 tokens)

**Errors prevented**: 12 documented issues with exact solutions
**Key value**: Structured outputs (v0.69.0+), model deprecations (Oct 2025), prompt caching edge cases, streaming error patterns, rate limit retry logic

---

**Last verified**: 2025-11-22 | **Skill version**: 2.0.0 | **Changes**: Added structured outputs (v0.69.0), updated model table (retired 3.5/3.7), context management, agent skills API. Removed basic tutorials (~380 lines). Focused on knowledge gaps + error prevention + advanced patterns.
