---
name: modelmix
description: Instructions for using the ModelMix Node.js library to interact with multiple AI LLM providers through a unified interface. Use when integrating AI models (OpenAI, Anthropic, Google, Groq, Perplexity, Grok, etc.), chaining models with fallback, getting structured JSON from LLMs, adding MCP tools, streaming responses, or managing multi-provider AI workflows in Node.js.
---

# ModelMix Library Skill

## Overview

ModelMix is a Node.js library that provides a unified fluent API to interact with multiple AI LLM providers. It handles automatic fallback between models, round-robin load balancing, structured JSON output, streaming, MCP tool integration, rate limiting, and token tracking.

Use this skill when:
- Integrating one or more AI models into a Node.js project
- Chaining models with automatic fallback
- Extracting structured JSON from LLMs
- Adding MCP tools or custom tools to models
- Working with templates and file-based prompts

Do NOT use this skill for:
- Python or non-Node.js projects
- Direct HTTP calls to LLM APIs (use ModelMix instead)

## Common Tasks

- [Get a text response](#get-a-text-response)
- [Get structured JSON](#get-structured-json)
- [Stream a response](#stream-a-response)
- [Get raw response (tokens, thinking, tool calls)](#get-raw-response-tokens-thinking-tool-calls)
- [Access full response after `message()` or `json()` with `lastRaw`](#access-full-response-after-message-or-json-with-lastraw)
- [Add images](#add-images)
- [Use templates with placeholders](#use-templates-with-placeholders)
- [Round-robin load balancing](#round-robin-load-balancing)
- [MCP integration (external tools)](#mcp-integration-external-tools)
- [Custom local tools (addTool)](#custom-local-tools-addtool)
- [Rate limiting (Bottleneck)](#rate-limiting-bottleneck)
- [Debug mode](#debug-mode)
- [Use free-tier models](#use-free-tier-models)
- [Conversation history](#conversation-history)

## Installation

```bash
npm install modelmix
```

## Core Concepts

### Import

```javascript
import { ModelMix } from 'modelmix';
```

### Creating an Instance

```javascript
// Static factory (preferred)
const model = ModelMix.new();

// With global options
const model = ModelMix.new({
    options: { max_tokens: 4096, temperature: 0.7 },
    config: {
        system: "You are a helpful assistant.",
        max_history: 5,
        debug: 0,           // 0=silent, 1=minimal, 2=summary, 3=full (no truncate), 4=verbose
        roundRobin: false    // false=fallback, true=rotate models
    }
});
```

### Attaching Models (Fluent Chain)

Chain shorthand methods to attach providers. First model is primary; others are fallbacks:

```javascript
const model = ModelMix.new()
    .sonnet46()        // primary
    .gpt52()        // fallback 1
    .gemini3flash()    // fallback 2
    .addText("Hello!")
```

If `sonnet45` fails, it automatically tries `gpt5mini`, then `gemini3flash`.

## Available Model Shorthands

- **OpenAI**: `gpt52` `gpt51` `gpt5` `gpt5mini` `gpt5nano` `gpt41` `gpt41mini` `gpt41nano`
- **Anthropic**: `opus46` `opus45` `sonnet46` `sonnet45` `haiku45` `haiku35` (thinking variants: add `think` suffix)
- **Google**: `gemini3pro` `gemini3flash` `gemini25pro` `gemini25flash`
- **Grok**: `grok4` `grok41` (thinking variant available)
- **Perplexity**: `sonar` `sonarPro`
- **Groq**: `scout` `maverick`
- **Together**: `qwen3` `kimiK2`
- **Multi-provider**: `deepseekR1` `gptOss`
- **MiniMax**: `minimaxM21`
- **Fireworks**: `deepseekV32` `GLM47`

Each method is called as `mix.methodName()` and accepts optional `{ options, config }` to override per-model settings.

## Common Tasks

### Get a text response

```javascript
const answer = await ModelMix.new()
    .gpt5mini()
    .addText("What is the capital of France?")
    .message();
```

### Get structured JSON

```javascript
const result = await ModelMix.new()
    .gpt5mini()
    .addText("Name and capital of 3 South American countries.")
    .json(
        { countries: [{ name: "", capital: "" }] },                    // schema example
        { countries: [{ name: "country name", capital: "in uppercase" }] }, // descriptions
        { addNote: true }                                               // options
    );
// result.countries → [{ name: "Brazil", capital: "BRASILIA" }, ...]
```

`json()` signature: `json(schemaExample, schemaDescription?, { addSchema, addExample, addNote }?)`

#### Enhanced descriptors

Descriptions can be **strings** or **descriptor objects** with metadata:

```javascript
const result = await model.json(
    { name: 'martin', age: 22, sex: 'Male' },
    {
        name: { description: 'Name of the actor', required: false },
        age: 'Age of the actor',                                     // string still works
        sex: { description: 'Gender', enum: ['Male', 'Female', null] }
    }
);
```

Descriptor properties:
- `description` (string) — field description
- `required` (boolean, default `true`) — if `false`: removed from required array, type becomes nullable
- `enum` (array) — allowed values; if includes `null`, type auto-becomes nullable
- `default` (any) — default value

#### Array auto-wrap

Top-level arrays are auto-wrapped as `{ out: [...] }` for better LLM compatibility, and unwrapped on return:

```javascript
const result = await model.json([{ name: 'martin' }]);
// result is an array: [{ name: "Martin" }, { name: "Carlos" }, ...]
```

### Stream a response

```javascript
await ModelMix.new()
    .gpt5mini()
    .addText("Tell me a story.")
    .stream(({ delta, message }) => {
        process.stdout.write(delta);
    });
```

### Get raw response (tokens, thinking, tool calls)

```javascript
const raw = await ModelMix.new()
    .sonnet45think()
    .addText("Solve this step by step: 2+2*3")
    .raw();
// raw.message, raw.think, raw.tokens, raw.toolCalls, raw.response
```

### Access full response after `message()` or `json()` with `lastRaw`

After calling `message()`, `json()`, `block()`, or `stream()`, use `lastRaw` to access the complete response (tokens, thinking, tool calls, etc.). It has the same structure as `raw()`.

```javascript
const model = ModelMix.new().gpt5mini().addText("Hello!");
const text = await model.message();
console.log(model.lastRaw.tokens);
// { input: 122, output: 86, total: 541, cost: 0.000319 }
console.log(model.lastRaw.think);    // reasoning content (if available)
console.log(model.lastRaw.response); // raw API response
```

### Add images

```javascript
const model = ModelMix.new().sonnet45();
model.addImage('./photo.jpg');                         // from file
model.addImageFromUrl('https://example.com/img.png');  // from URL
model.addText('Describe this image.');
const description = await model.message();
```

### Use templates with placeholders

```javascript
const model = ModelMix.new().gpt5mini();
model.setSystemFromFile('./prompts/system.md');
model.addTextFromFile('./prompts/task.md');
model.replace({
    '{role}': 'data analyst',
    '{language}': 'Spanish'
});
model.replaceKeyFromFile('{code}', './src/utils.js');
console.log(await model.message());
```

### Round-robin load balancing

```javascript
const pool = ModelMix.new({ config: { roundRobin: true } })
    .gpt5mini()
    .sonnet45()
    .gemini3flash();

// Each call rotates to the next model
const r1 = await pool.new().addText("Request 1").message();
const r2 = await pool.new().addText("Request 2").message();
```

### MCP integration (external tools)

```javascript
const model = ModelMix.new({ config: { max_history: 10 } }).gpt5nano();
model.setSystem('You are an assistant. Today is ' + new Date().toISOString());
await model.addMCP('@modelcontextprotocol/server-brave-search');
model.addText('Use Internet: What is the latest news about AI?');
console.log(await model.message());
```

Requires `BRAVE_API_KEY` in `.env` for Brave Search MCP.

### Custom local tools (addTool)

```javascript
const model = ModelMix.new({ config: { max_history: 10 } }).gpt5mini();

model.addTool({
    name: "get_weather",
    description: "Get weather for a city",
    inputSchema: {
        type: "object",
        properties: { city: { type: "string" } },
        required: ["city"]
    }
}, async ({ city }) => {
    return `The weather in ${city} is sunny, 25C`;
});

model.addText("What's the weather in Tokyo?");
console.log(await model.message());
```

### Rate limiting (Bottleneck)

```javascript
const model = ModelMix.new({
    config: {
        bottleneck: {
            maxConcurrent: 4,
            minTime: 1000
        }
    }
}).gpt5mini();
```

### Debug mode

```javascript
const model = ModelMix.new({
    config: { debug: 2 }  // 0=silent, 1=minimal, 2=summary, 3=full (no truncate), 4=verbose
}).gpt5mini();
```

For full debug output, also set the env: `DEBUG=ModelMix* node script.js`

### Use free-tier models

```javascript
// These use providers with free quotas (OpenRouter, Groq, Cerebras)
const model = ModelMix.new()
    .gptOss()
    .kimiK2()
    .deepseekR1()
    .hermes3()
    .addText("What is the capital of France?");
console.log(await model.message());
```

### Conversation history

```javascript
const chat = ModelMix.new({ config: { max_history: 10 } }).gpt5mini();
chat.addText("My name is Martin.");
await chat.message();
chat.addText("What's my name?");
const reply = await chat.message();  // "Martin"
```

## Agent Usage Rules

- Always check `package.json` for `modelmix` before running `npm install`.
- Use `ModelMix.new()` static factory to create instances (not `new ModelMix()`).
- Store API keys in `.env` and load with `dotenv/config` or `process.loadEnvFile()`. Never hardcode keys.
- Chain models for resilience: primary model first, fallbacks after.
- When using MCP tools or `addTool()`, set `max_history` to at least 3.
- Use `.json()` for structured output instead of parsing text manually. Use descriptor objects `{ description, required, enum, default }` in descriptions for richer schema control.
- Use `.message()` for simple text, `.raw()` when you need tokens/thinking/toolCalls.
- For thinking models, append `think` to the method name (e.g. `sonnet45think()`).
- Template placeholders use `{key}` syntax in both system prompts and user messages.
- The library uses CommonJS internally (`require`) but supports ESM import via `{ ModelMix }`.
- Available provider Mix classes for custom setups: `MixOpenAI`, `MixAnthropic`, `MixGoogle`, `MixPerplexity`, `MixGroq`, `MixTogether`, `MixGrok`, `MixOpenRouter`, `MixOllama`, `MixLMStudio`, `MixCustom`, `MixCerebras`, `MixFireworks`, `MixMiniMax`.

## API Quick Reference

| Method | Returns | Description |
| --- | --- | --- |
| `.addText(text)` | `this` | Add user message |
| `.addTextFromFile(path)` | `this` | Add user message from file |
| `.setSystem(text)` | `this` | Set system prompt |
| `.setSystemFromFile(path)` | `this` | Set system prompt from file |
| `.addImage(path)` | `this` | Add image from file |
| `.addImageFromUrl(url)` | `this` | Add image from URL or data URI |
| `.replace({})` | `this` | Set placeholder replacements |
| `.replaceKeyFromFile(key, path)` | `this` | Replace placeholder with file content |
| `.message()` | `Promise<string>` | Get text response |
| `.json(example, desc?, opts?)` | `Promise<object\|array>` | Get structured JSON. Descriptions support descriptor objects `{ description, required, enum, default }`. Top-level arrays auto-wrapped |
| `.raw()` | `Promise<{message, think, toolCalls, tokens, response}>` | Full response |
| `.lastRaw` | `object \| null` | Full response from last `message()`/`json()`/`block()`/`stream()` call |
| `.stream(callback)` | `Promise` | Stream response |
| `.block()` | `Promise<string>` | Extract code block from response |
| `.addMCP(package)` | `Promise` | Add MCP server tools |
| `.addTool(def, callback)` | `this` | Register custom local tool |
| `.addTools([{tool, callback}])` | `this` | Register multiple tools |
| `.removeTool(name)` | `this` | Remove a tool |
| `.listTools()` | `{local, mcp}` | List registered tools |
| `.new()` | `ModelMix` | Clone instance sharing models |
| `.attach(key, provider)` | `this` | Attach custom provider |

## References

- [GitHub Repository](https://github.com/clasen/ModelMix)
