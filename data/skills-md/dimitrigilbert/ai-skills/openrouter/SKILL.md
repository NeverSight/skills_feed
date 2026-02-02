---
name: openrouter
description: Expert OpenRouter API assistant for AI agents. Use when making API calls to OpenRouter's unified API for 400+ AI models. Covers chat completions, streaming, tool calling, structured outputs, web search, embeddings, multimodal inputs, model selection, routing, and error handling.
---

# OpenRouter API for AI Agents

Expert guidance for AI agents integrating with OpenRouter API - unified access to 400+ models from 90+ providers.

**When to use this skill:**
- Making chat completions via OpenRouter API
- Selecting appropriate models and variants
- Implementing streaming responses
- Using tool/function calling
- Enforcing structured outputs
- Integrating web search
- Handling multimodal inputs (images, audio, video, PDFs)
- Managing model routing and fallbacks
- Handling errors and retries
- Optimizing cost and performance

---

## API Basics

### Making a Request

**Endpoint**: `POST https://openrouter.ai/api/v1/chat/completions`

**Headers** (required):
```typescript
{
  'Authorization': `Bearer ${apiKey}`,
  'Content-Type': 'application/json',
  // Optional: for app attribution
  'HTTP-Referer': 'https://your-app.com',
  'X-Title': 'Your App Name'
}
```

**Minimal request structure**:
```typescript
const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${apiKey}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    model: 'anthropic/claude-3.5-sonnet',
    messages: [
      { role: 'user', content: 'Your prompt here' }
    ]
  })
});
```

### Response Structure

**Non-streaming response**:
```json
{
  "id": "gen-abc123",
  "choices": [{
    "message": {
      "role": "assistant",
      "content": "Response text here"
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 20,
    "total_tokens": 30
  },
  "model": "anthropic/claude-3.5-sonnet"
}
```

**Key fields**:
- `choices[0].message.content` - The assistant's response
- `choices[0].finish_reason` - Why generation stopped (stop, length, tool_calls, etc.)
- `usage` - Token counts and cost information
- `model` - Actual model used (may differ from requested)

### When to Use Streaming vs Non-Streaming

**Use streaming (`stream: true`)** when:
- Real-time responses needed (chat interfaces, interactive tools)
- Latency matters (user-facing applications)
- Large responses expected (long-form content)
- Want to show progressive output

**Use non-streaming** when:
- Processing in background (batch jobs, async tasks)
- Need complete response before processing
- Building to an API/endpoint
- Response is short (few tokens)

**Streaming basics**:
```typescript
const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
  method: 'POST',
  headers: { /* ... */ },
  body: JSON.stringify({
    model: 'anthropic/claude-3.5-sonnet',
    messages: [{ role: 'user', content: '...' }],
    stream: true
  })
});

for await (const chunk of response.body) {
  const text = new TextDecoder().decode(chunk);
  const lines = text.split('\n').filter(line => line.startsWith('data: '));

  for (const line of lines) {
    const data = line.slice(6); // Remove 'data: '
    if (data === '[DONE]') break;

    const parsed = JSON.parse(data);
    const content = parsed.choices?.[0]?.delta?.content;
    if (content) {
      // Accumulate or display content
    }
  }
}
```

---

## Model Selection

### Model Identifier Format

**Format**: `provider/model-name[:variant]`

Examples:
- `anthropic/claude-3.5-sonnet` - Specific model
- `openai/gpt-4o:online` - With web search enabled
- `google/gemini-2.0-flash:free` - Free tier variant

### Model Variants and When to Use Them

| Variant | Use When | Tradeoffs |
|---------|----------|-----------|
| `:free` | Cost is primary concern, testing, prototyping | Rate limits, lower quality models |
| `:online` | Need current information, real-time data | Higher cost, web search latency |
| `:extended` | Large context window needed | May be slower, higher cost |
| `:thinking` | Complex reasoning, multi-step problems | Higher token usage, slower |
| `:nitro` | Speed is critical | May have quality tradeoffs |
| `:exacto` | Need specific provider | No fallbacks, may be less available |

### Default Model Choices by Task

**General purpose**: `anthropic/claude-3.5-sonnet` or `openai/gpt-4o`
- Balanced quality, speed, cost
- Good for most tasks

**Coding**: `anthropic/claude-3.5-sonnet` or `openai/gpt-4o`
- Strong code generation and understanding
- Good reasoning

**Complex reasoning**: `anthropic/claude-opus-4:thinking` or `openai/o3`
- Deep reasoning capabilities
- Higher cost, slower

**Fast responses**: `openai/gpt-4o-mini:nitro` or `google/gemini-2.0-flash`
- Minimal latency
- Good for real-time applications

**Cost-sensitive**: `google/gemini-2.0-flash:free` or `meta-llama/llama-3.1-70b:free`
- No cost with limits
- Good for high-volume, lower-complexity tasks

**Current information**: `anthropic/claude-3.5-sonnet:online` or `google/gemini-2.5-pro:online`
- Web search built-in
- Real-time data

**Large context**: `anthropic/claude-3.5-sonnet:extended` or `google/gemini-2.5-pro:extended`
- 200K+ context windows
- Document analysis, codebase understanding

### Provider Routing Preferences

**Default behavior**: OpenRouter automatically selects best provider

**Explicit provider order**:
```typescript
{
  provider: {
    order: ['anthropic', 'openai', 'google'],
    allow_fallbacks: true,
    sort: 'price' // 'price', 'latency', or 'throughput'
  }
}
```

**When to set provider order**:
- Have preferred provider arrangements
- Need to optimize for specific metric (cost, speed)
- Want to exclude certain providers
- Have BYOK (Bring Your Own Key) for specific providers

### Model Fallbacks

**Automatic fallback** - try multiple models in order:
```typescript
{
  models: [
    'anthropic/claude-3.5-sonnet',
    'openai/gpt-4o',
    'google/gemini-2.0-flash'
  ]
}
```

**When to use fallbacks**:
- High reliability required
- Multiple providers acceptable
- Want graceful degradation
- Avoid single point of failure

**Fallback behavior**:
- Tries first model
- Falls to next on error (5xx, 429, timeout)
- Uses whichever succeeds
- Returns which model was used in `model` field

---

## Parameters You Need

### Core Parameters

**model** (string, optional)
- Which model to use
- Default: user's default model
- **Always specify for consistency**

**messages** (Message[], required)
- Conversation history
- Structure: `{ role: 'user'|'assistant'|'system', content: string | ContentPart[] }`
- For multimodal: content can be array of text and image_url parts

**stream** (boolean, default: false)
- Enable Server-Sent Events streaming
- Use for real-time responses

**temperature** (float, 0.0-2.0, default: 1.0)
- Controls randomness
- **0.0-0.3**: Deterministic, factual responses (code, precise answers)
- **0.4-0.7**: Balanced (general use)
- **0.8-1.2**: Creative (brainstorming, creative writing)
- **1.3-2.0**: Highly creative, unpredictable (experimental)

**max_tokens** (integer, optional)
- Maximum tokens to generate
- **Always set** to control cost and prevent runaway responses
- Typical: 100-500 for short, 1000-2000 for long responses
- Model limit: context_length - prompt_length

**top_p** (float, 0.0-1.0, default: 1.0)
- Nucleus sampling - limits to top probability mass
- **Use instead of temperature** when you want predictable diversity
- **0.9-0.95**: Common settings for quality

**top_k** (integer, 0+, default: 0/disabled)
- Limit to K most likely tokens
- **1**: Always most likely (deterministic)
- **40-50**: Balanced
- Not available for OpenAI models

### Sampling Strategy Guidelines

**For code generation**: `temperature: 0.1-0.3, top_p: 0.95`
**For factual responses**: `temperature: 0.0-0.2`
**For creative writing**: `temperature: 0.8-1.2`
**For brainstorming**: `temperature: 1.0-1.5`
**For chat**: `temperature: 0.6-0.8`

### Tool Calling Parameters

**tools** (Tool[], default: [])
- Available functions for model to call
- Structure:
```typescript
{
  type: 'function',
  function: {
    name: 'function_name',
    description: 'What it does',
    parameters: { /* JSON Schema */ }
  }
}
```

**tool_choice** (string | object, default: 'auto')
- Control when tools are called
- `'auto'`: Model decides (default)
- `'none'`: Never call tools
- `'required'`: Must call a tool
- `{ type: 'function', function: { name: 'specific_tool' } }`: Force specific tool

**parallel_tool_calls** (boolean, default: true)
- Allow multiple tools simultaneously
- Set `false` for sequential execution

**When to use tools**:
- Need to query external APIs (weather, search, database)
- Need to perform calculations or data processing
- Building agentic systems
- Need structured data extraction

### Structured Output Parameters

**response_format** (object, optional)
- Enforce specific output format

**JSON object mode**:
```typescript
{ type: 'json_object' }
```
- Model returns valid JSON
- Must also instruct model in system message

**JSON Schema mode** (strict):
```typescript
{
  type: 'json_schema',
  json_schema: {
    name: 'schema_name',
    strict: true,
    schema: { /* JSON Schema */ }
  }
}
```
- Model returns JSON matching exact schema
- **Use when structure is critical** (APIs, data processing)

**When to use structured outputs**:
- Need predictable response format
- Integrating with systems (APIs, databases)
- Data extraction
- Form filling

### Web Search Parameters

**Enable via model variant** (simplest):
```typescript
{ model: 'anthropic/claude-3.5-sonnet:online' }
```

**Enable via plugin**:
```typescript
{
  plugins: [{
    id: 'web',
    enabled: true,
    max_results: 5
  }]
}
```

**When to use web search**:
- Need current information (news, prices, events)
- User asks about recent developments
- Need factual verification
- Topic requires real-time data

### Other Important Parameters

**user** (string, optional)
- Stable identifier for end-user
- **Set when you have user IDs**
- Helps with abuse detection and caching

**session_id** (string, optional)
- Group related requests
- **Set for conversation tracking**
- Improves caching and observability

**metadata** (Record<string, string>, optional)
- Custom metadata (max 16 key-value pairs)
- **Use for analytics and tracking**
- Keys: max 64 chars, Values: max 512 chars

**stop** (string | string[], optional)
- Stop sequences to halt generation
- Common: `['\n\n', '###', 'END']`

---

## Handling Responses

### Non-Streaming Responses

Extract content:
```typescript
const response = await fetch(/* ... */);
const data = await response.json();

const content = data.choices[0].message.content;
const finishReason = data.choices[0].finish_reason;
const usage = data.usage;
```

Check for tool calls:
```typescript
const toolCalls = data.choices[0].message.tool_calls;
if (toolCalls) {
  // Model wants to call tools
  for (const toolCall of toolCalls) {
    const { name, arguments: args } = toolCall.function;
    const parsedArgs = JSON.parse(args);
    // Execute tool...
  }
}
```

### Streaming Responses

Process SSE stream:
```typescript
let fullContent = '';
const response = await fetch(/* ... */);

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;

  const chunk = decoder.decode(value);
  const lines = chunk.split('\n').filter(line => line.startsWith('data: '));

  for (const line of lines) {
    const data = line.slice(6);
    if (data === '[DONE]') break;

    const parsed = JSON.parse(data);
    const content = parsed.choices?.[0]?.delta?.content;
    if (content) {
      fullContent += content;
      // Process incrementally...
    }

    // Handle usage in final chunk
    if (parsed.usage) {
      console.log('Usage:', parsed.usage);
    }
  }
}
```

Handle streaming tool calls:
```typescript
// Tool calls stream across multiple chunks
let currentToolCall = null;
let toolArgs = '';

for (const parsed of chunks) {
  const toolCallChunk = parsed.choices?.[0]?.delta?.tool_calls?.[0];

  if (toolCallChunk?.function?.name) {
    currentToolCall = { id: toolCallChunk.id, ...toolCallChunk.function };
  }

  if (toolCallChunk?.function?.arguments) {
    toolArgs += toolCallChunk.function.arguments;
  }

  if (parsed.choices?.[0]?.finish_reason === 'tool_calls' && currentToolCall) {
    // Complete tool call
    currentToolCall.arguments = toolArgs;
    // Execute tool...
  }
}
```

### Usage and Cost Tracking

```typescript
const { usage } = data;
console.log(`Prompt: ${usage.prompt_tokens}`);
console.log(`Completion: ${usage.completion_tokens}`);
console.log(`Total: ${usage.total_tokens}`);

// Cost (if available)
if (usage.cost) {
  console.log(`Cost: $${usage.cost.toFixed(6)}`);
}

// Detailed breakdown
console.log(usage.prompt_tokens_details);
console.log(usage.completion_tokens_details);
```

---

## Error Handling

### Common HTTP Status Codes

**400 Bad Request**
- Invalid request format
- Missing required fields
- Parameter out of range
- **Fix**: Validate request structure and parameters

**401 Unauthorized**
- Missing or invalid API key
- **Fix**: Check API key format and permissions

**403 Forbidden**
- Insufficient permissions
- Model not allowed
- **Fix**: Check guardrails, model access, API key permissions

**402 Payment Required**
- Insufficient credits
- **Fix**: Add credits to account

**408 Request Timeout**
- Request took too long
- **Fix**: Reduce prompt length, use streaming, try simpler model

**429 Rate Limited**
- Too many requests
- **Fix**: Implement exponential backoff, reduce request rate

**502 Bad Gateway**
- Provider error
- **Fix**: Use model fallbacks, retry with different model

**503 Service Unavailable**
- Service overloaded
- **Fix**: Retry with backoff, use fallbacks

### Retry Strategy

**Exponential backoff**:
```typescript
async function requestWithRetry(url, body, maxRetries = 3) {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      const response = await fetch(url, body);

      if (response.ok) {
        return await response.json();
      }

      // Retry on rate limit or server errors
      if (response.status === 429 || response.status >= 500) {
        const delay = Math.min(1000 * Math.pow(2, attempt), 10000);
        await new Promise(resolve => setTimeout(resolve, delay));
        continue;
      }

      // Don't retry other errors
      return response;
    } catch (error) {
      if (attempt === maxRetries - 1) throw error;
      const delay = Math.min(1000 * Math.pow(2, attempt), 10000);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
}
```

**Retryable status codes**: 408, 429, 502, 503
**Do not retry**: 400, 401, 403, 402

### Graceful Degradation

**Use model fallbacks**:
```typescript
{
  models: [
    'anthropic/claude-3.5-sonnet',  // Primary
    'openai/gpt-4o',                // Fallback 1
    'google/gemini-2.0-flash'        // Fallback 2
  ]
}
```

**Handle partial failures**:
- Log errors but continue
- Fall back to simpler features
- Use cached responses when available
- Provide degraded experience rather than failing completely

---

## Advanced Features

### When to Use Tool Calling

**Good use cases**:
- Querying external APIs (weather, stock prices, databases)
- Performing calculations or data processing
- Extracting structured data from unstructured text
- Building agentic systems with multiple steps
- When decisions require external information

**Implementation pattern**:
1. Define tools with clear descriptions and parameters
2. Send request with `tools` array
3. Check if `tool_calls` present in response
4. Execute tools with parsed arguments
5. Send tool results back in a new request
6. Repeat until model provides final answer

**See**: `references/ADVANCED_PATTERNS.md` for complete agentic loop implementation

### When to Use Structured Outputs

**Good use cases**:
- API responses (need specific schema)
- Data extraction (forms, documents)
- Configuration files (JSON, YAML)
- Database operations (structured queries)
- When downstream processing requires specific format

**Implementation pattern**:
1. Define JSON Schema for desired output
2. Set `response_format: { type: 'json_schema', json_schema: { ... } }`
3. Instruct model to produce JSON (system or user message)
4. Validate response against schema
5. Handle parsing errors gracefully

**Add response healing** for robustness:
```typescript
{
  response_format: { /* ... */ },
  plugins: [{ id: 'response-healing' }]
}
```

### When to Use Web Search

**Good use cases**:
- User asks about recent events, news, or current data
- Need verification of facts
- Questions with time-sensitive information
- Topic requires up-to-date information
- User explicitly requests current information

**Simple implementation** (variant):
```typescript
{
  model: 'anthropic/claude-3.5-sonnet:online'
}
```

**Advanced implementation** (plugin):
```typescript
{
  model: 'openrouter.ai/auto',
  plugins: [{
    id: 'web',
    enabled: true,
    max_results: 5,
    engine: 'exa' // or 'native'
  }]
}
```

### When to Use Multimodal Inputs

**Images** (vision):
- OCR, image understanding, visual analysis
- Models: `openai/gpt-4o`, `anthropic/claude-3.5-sonnet`, `google/gemini-2.5-pro`

**Audio**:
- Speech-to-text, audio analysis
- Models with audio support

**Video**:
- Video understanding, frame analysis
- Models with video support

**PDFs**:
- Document parsing, content extraction
- Requires `file-parser` plugin

**Implementation**: See `references/ADVANCED_PATTERNS.md` for multimodal patterns

---

## Best Practices for AI

### Default Model Selection

**Start with**: `anthropic/claude-3.5-sonnet` or `openai/gpt-4o`
- Good balance of quality, speed, cost
- Strong at most tasks
- Wide compatibility

**Switch based on needs**:
- Need speed → `openai/gpt-4o-mini:nitro` or `google/gemini-2.0-flash`
- Complex reasoning → `anthropic/claude-opus-4:thinking`
- Need web search → `:online` variant
- Large context → `:extended` variant
- Cost-sensitive → `:free` variant

### Default Parameters

```typescript
{
  model: 'anthropic/claude-3.5-sonnet',
  messages: [...],
  temperature: 0.6,  // Balanced creativity
  max_tokens: 1000,   // Reasonable length
  top_p: 0.95        // Common for quality
}
```

**Adjust based on task**:
- Code: `temperature: 0.2`
- Creative: `temperature: 1.0`
- Factual: `temperature: 0.0-0.3`

### When to Prefer Streaming

**Always prefer streaming when**:
- User-facing (chat, interactive tools)
- Response length unknown
- Want progressive feedback
- Latency matters

**Use non-streaming when**:
- Batch processing
- Need complete response before acting
- Building API endpoints
- Very short responses (< 50 tokens)

### When to Enable Specific Features

**Tools**: Enable when you need external data or actions
**Structured outputs**: Enable when response format matters
**Web search**: Enable when current information needed
**Streaming**: Enable for user-facing, real-time responses
**Model fallbacks**: Enable when reliability critical
**Provider routing**: Enable when you have preferences or constraints

### Cost Optimization Patterns

**Use free models for**:
- Testing and prototyping
- Low-complexity tasks
- High-volume, low-value operations

**Use routing to optimize**:
```typescript
{
  provider: {
    order: ['openai', 'anthropic'],
    sort: 'price',  // Optimize for cost
    allow_fallbacks: true
  }
}
```

**Set max_tokens** to prevent runaway responses
**Use caching** via `user` and `session_id` parameters
**Enable prompt caching** when supported

### Performance Optimization

**Reduce latency**:
- Use `:nitro` variants for speed
- Use streaming for perceived speed
- Set `user` ID for caching benefits
- Choose faster models (mini, flash) when quality allows

**Increase throughput**:
- Use provider routing with `sort: 'throughput'`
- Parallelize independent requests
- Use streaming to reduce wait time

**Optimize for specific metrics**:
```typescript
{
  provider: {
    sort: 'latency'  // or 'price' or 'throughput'
  }
}
```

---

## Progressive Disclosure

For detailed reference information, consult:

### Parameters Reference
**File**: `references/PARAMETERS.md`
- Complete parameter reference (50+ parameters)
- Types, ranges, defaults
- Parameter support by model
- Usage examples

### Error Codes Reference
**File**: `references/ERROR_CODES.md`
- All HTTP status codes
- Error response structure
- Error metadata types
- Native finish reasons
- Retry strategies

### Model Selection Guide
**File**: `references/MODEL_SELECTION.md`
- Model families and capabilities
- Model variants explained
- Selection criteria by use case
- Model capability matrix
- Provider routing preferences

### Routing Strategies
**File**: `references/ROUTING_STRATEGIES.md`
- Model fallbacks configuration
- Provider selection patterns
- Auto router setup
- Routing by use case (cost, latency, quality)

### Advanced Patterns
**File**: `references/ADVANCED_PATTERNS.md`
- Tool calling with agentic loops
- Structured outputs implementation
- Web search integration
- Multimodal handling
- Streaming patterns
- Framework integrations

### Working Examples
**File**: `references/EXAMPLES.md`
- TypeScript patterns for common tasks
- Python examples
- cURL examples
- Advanced patterns
- Framework integration examples

### Ready-to-Use Templates
**Directory**: `templates/`
- `basic-request.ts` - Minimal working request
- `streaming-request.ts` - SSE streaming with cancellation
- `tool-calling.ts` - Complete agentic loop with tools
- `structured-output.ts` - JSON Schema enforcement
- `error-handling.ts` - Robust retry logic

---

## Quick Reference

### Minimal Request
```typescript
{
  model: 'anthropic/claude-3.5-sonnet',
  messages: [{ role: 'user', content: 'Your prompt' }]
}
```

### With Streaming
```typescript
{
  model: 'anthropic/claude-3.5-sonnet',
  messages: [{ role: 'user', content: '...' }],
  stream: true
}
```

### With Tools
```typescript
{
  model: 'anthropic/claude-3.5-sonnet',
  messages: [{ role: 'user', content: '...' }],
  tools: [{ type: 'function', function: { name, description, parameters } }],
  tool_choice: 'auto'
}
```

### With Structured Output
```typescript
{
  model: 'anthropic/claude-3.5-sonnet',
  messages: [{ role: 'system', content: 'Output JSON only...' }],
  response_format: { type: 'json_object' }
}
```

### With Web Search
```typescript
{
  model: 'anthropic/claude-3.5-sonnet:online',
  messages: [{ role: 'user', content: '...' }]
}
```

### With Model Fallbacks
```typescript
{
  models: ['anthropic/claude-3.5-sonnet', 'openai/gpt-4o'],
  messages: [{ role: 'user', content: '...' }]
}
```

---

**Remember**: OpenRouter is OpenAI-compatible. Use the OpenAI SDK with `baseURL: 'https://openrouter.ai/api/v1'` for a familiar experience.
