---
name: chrome-ai-extension
description: Create Chrome extensions that use built-in Chrome AI (Prompt API, Summarization, Translation, Writer). Use when building browser extensions that need AI capabilities like text generation, summarization, translation, or conversational AI features powered by Chrome's native on-device AI models.
---

# Chrome AI Extension Skill

Create Chrome extensions that leverage Chrome's built-in AI capabilities for on-device machine learning without external API calls.

## Chrome AI APIs Overview

Chrome provides several built-in AI APIs that run locally on-device:

- **LanguageModel API (Prompt API)**: General-purpose LLM for conversational AI and text generation using Gemini Nano
- **Summarization API**: Specialized for text summarization
- **Translation API**: Language translation  
- **Writer API**: Assisted writing and content generation

**Note**: The API is experimental and evolving. In current Chromium builds the exposed surface for extensions is the global `LanguageModel` object inside page contexts (content scripts, popups, etc.); the `chrome.ai` namespace is not wired up for service workers yet.

## Quick Start - Working Example

Here's a working pattern that matches what currently ships in Canary/Dev (127+):

```javascript
// content.js - injected into the page
let aiSession = null;

async function ensureSession() {
  if (!('LanguageModel' in self)) {
    throw new Error('Chrome on-device AI not available');
  }

  if (aiSession) {
    return aiSession;
  }

  aiSession = await LanguageModel.create({
    temperature: 0.7,
    topK: 3,
    systemPrompt: 'You are a helpful assistant.'
  });

  return aiSession;
}

async function askQuestion(question) {
  const session = await ensureSession();
  return session.prompt(question);
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'ask') {
    askQuestion(message.question)
      .then(response => sendResponse({ success: true, response }))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true; // async response
  }
});
```

## Quick Start Workflow

1. **Check API Availability**: Always verify API availability before use
2. **Request Capabilities**: Check if the user's browser supports the features
3. **Create Session**: Initialize an AI session
4. **Interact**: Use the session for AI operations
5. **Handle Errors**: Gracefully handle unavailable features

## Extension Architecture

### Manifest Configuration

Use Manifest V3 with appropriate permissions:

```json
{
  "manifest_version": 3,
  "name": "My AI Extension",
  "version": "1.0.0",
  "permissions": ["storage"],
  "background": {
    "service_worker": "background.js"
  },
  "action": {
    "default_popup": "popup.html"
  }
}
```

**Note**: Request `"aiLanguageModel"` in `permissions` or the API will not appear to the extension, even on Canary/Dev builds. Add any additional permissions (e.g., `activeTab`, `storage`) your feature set requires.

### File Structure

Standard Chrome extension structure:

```
extension/
├── manifest.json
├── background.js (service worker)
├── popup.html
├── popup.js
├── content.js (if needed)
└── styles.css
```

## API Usage Patterns

### Prompt API / LanguageModel API

The Prompt API provides conversational AI capabilities using Gemini Nano.

#### Current API Pattern (LanguageModel global)

**IMPORTANT**: In page-context scripts (content scripts, popups, option pages) the stable entry point is the global `LanguageModel`. The `chrome.ai` namespace is not exposed to service workers today.

**Availability Check**:
```javascript
if (!('LanguageModel' in self)) {
  // API not available
}

const capabilities = await LanguageModel.capabilities?.();
// Returns: { available: "readily" | "after-download" | "no" }
```

**Create Session with System Prompt**:
```javascript
const session = await LanguageModel.create({
  temperature: 0.7,
  topK: 3,
  systemPrompt: 'You are a helpful assistant...'
});
```

**Note**: Use `systemPrompt` (not `initialPrompts` or `outputLanguage`).

**Generate Response**:
```javascript
// Non-streaming
const response = await session.prompt("Your prompt here");

// Streaming (if supported)
if (session.promptStreaming) {
  const stream = await session.promptStreaming("Your prompt here");
  let result = '';
  let previous = '';
  for await (const chunk of stream) {
    const fragment = chunk.startsWith(previous) ? chunk.slice(previous.length) : chunk;
    result += fragment;
    previous = chunk;
  }
}
```

**Destroy Session**:
```javascript
if (session.destroy) {
  session.destroy();
}
```

#### Fallback API Pattern (window.ai / chrome.ai)

Some experimental builds briefly exposed the API under `window.ai.languageModel` or `chrome.ai.languageModel`. If you must support those variants, probe them after checking the global:

```javascript
const candidates = [
  self.LanguageModel,
  window?.ai?.languageModel,
  chrome?.ai?.languageModel
].filter(Boolean);

const provider = candidates.find(p => typeof p.create === 'function');
if (!provider) {
  throw new Error('No on-device language model API found');
}

const session = await provider.create({ temperature: 0.7, topK: 3 });
```

### Summarization API

Specialized for text summarization.

**Check Availability**:
```javascript
const canSummarize = await window.ai?.summarizer?.capabilities();
```

**Create Summarizer**:
```javascript
const summarizer = await window.ai.summarizer.create({
  type: 'tl;dr', // or 'key-points', 'teaser', 'headline'
  length: 'short' // or 'medium', 'long'
});
```

**Summarize Text**:
```javascript
const summary = await summarizer.summarize(longText);
```

### Translation API

For language translation tasks.

**Check Availability**:
```javascript
const canTranslate = await window.ai?.translator?.capabilities();
```

**Create Translator**:
```javascript
const translator = await window.ai.translator.create({
  sourceLanguage: 'en',
  targetLanguage: 'es'
});
```

**Translate Text**:
```javascript
const translated = await translator.translate('Hello, world!');
```

### Writer API

For assisted writing and content generation.

**Check Availability**:
```javascript
const canWrite = await window.ai?.writer?.capabilities();
```

**Create Writer**:
```javascript
const writer = await window.ai.writer.create({
  tone: 'formal', // or 'casual', 'neutral'
  length: 'medium'
});
```

**Generate Content**:
```javascript
const content = await writer.write('Write about...');
```

## Common Patterns

### Robust JSON Parsing

AI models may return malformed JSON. Use multi-layer parsing:

```javascript
function sanitizeModelJson(text) {
  let cleaned = text.trim();
  
  // Remove markdown code blocks
  if (cleaned.startsWith('```')) {
    cleaned = cleaned.replace(/^```(?:json)?/i, '').replace(/```$/i, '').trim();
  }
  
  // Extract JSON object
  const firstBrace = cleaned.indexOf('{');
  const lastBrace = cleaned.lastIndexOf('}');
  if (firstBrace !== -1 && lastBrace !== -1 && lastBrace > firstBrace) {
    cleaned = cleaned.slice(firstBrace, lastBrace + 1).trim();
  }
  
  return cleaned;
}

function parseModelResponse(raw) {
  const cleaned = sanitizeModelJson(raw);
  
  try {
    return JSON.parse(cleaned);
  } catch (error) {
    console.warn('Failed to parse model JSON', { raw, cleaned }, error);
    throw new Error('Model returned malformed JSON. Try again.');
  }
}
```

### Reusable Prompt Helper

Handle both streaming and non-streaming sessions:

```javascript
async function runPrompt(session, prompt) {
  // Try non-streaming first
  if (session.prompt) {
    return await session.prompt(prompt);
  }
  
  // Fall back to streaming
  if (session.promptStreaming) {
    const stream = await session.promptStreaming(prompt);
    let result = '';
    let previous = '';
    
    for await (const chunk of stream) {
      // Handle incremental chunks
      const fragment = chunk.startsWith(previous) 
        ? chunk.slice(previous.length) 
        : chunk;
      result += fragment;
      previous = chunk;
    }
    
    return result;
  }
  
  throw new Error('Prompt API shape not supported');
}
```

### Error Handling

Always handle cases where APIs are unavailable:

```javascript
async function initializeAI() {
  try {
    if (!('LanguageModel' in self)) {
      return { error: 'Chrome AI API not available in this context' };
    }

    const capabilities = typeof LanguageModel.capabilities === 'function'
      ? await LanguageModel.capabilities()
      : null;

    if (capabilities) {
      if (capabilities.available === 'no') {
        return { error: 'AI not available on this device' };
      }

      if (capabilities.available === 'after-download') {
        return { error: 'AI model needs to be downloaded first. Check chrome://components' };
      }
    }

    const session = await LanguageModel.create({
      temperature: 0.7,
      topK: 3,
      systemPrompt: 'You are a helpful assistant.'
    });

    return { session };
  } catch (error) {
    return { error: error.message };
  }
}
```

### Background Script Communication

Service workers currently do **not** get the `LanguageModel` API. If you need background coordination, have the background script forward requests to a page-context script (content script, popup, or options page) that actually calls `LanguageModel.create()`.

### Content Script Integration

Interact with page content using content scripts:

```javascript
// Get selected text from page
const selectedText = window.getSelection().toString();

// Send to background for AI processing
chrome.runtime.sendMessage({
  action: 'summarize',
  text: selectedText
});
```

## Best Practices

1. **Always check availability** before attempting to use AI features
2. **Handle gracefully** when features are unavailable
3. **Destroy sessions** when done to free resources
4. **Use streaming** for long responses to improve UX
5. **Cache sessions** when making multiple requests with same config
6. **Provide fallbacks** for browsers without AI support
7. **Monitor token limits** - sessions have context limits
8. **Run AI calls in page contexts** – service workers currently lack the API surface
9. **Test across Chrome versions** - AI features are experimental

## Debugging

### Enable Chrome Flags

1. Navigate to `chrome://flags`
2. Enable: `#prompt-api-for-gemini-nano`
3. Enable: `#optimization-guide-on-device-model` → **Enabled BypassPerfRequirement**
4. Restart Chrome completely

### Download Gemini Nano Model

- Visit `chrome://components`
- Look for "Optimization Guide On Device Model"
- Click "Check for update"
- Wait for download (~1.7GB)
- Status should show "Up to date"

### Verify API Availability

Open DevTools Console (F12) on any page:

```javascript
// Check capabilities
await LanguageModel.capabilities?.()
// Should return: { available: "readily" }

// If "after-download", wait a few minutes after download completes
```

### Requirements

- Chrome Canary or Dev channel (version 127+)
- ~1.7GB disk space for Gemini Nano model
- Supported hardware (most modern systems)

## Common Use Cases

- Text summarization for articles
- Translation of web content
- Writing assistance and suggestions
- Conversational chatbots
- Content generation
- Text analysis and insights

## Reference Files

For detailed examples and patterns:

- **references/battle-tested-patterns.md**: Production-proven patterns from real Chrome AI extensions
- **references/api-examples.md**: Complete working examples for each API
- **references/extension-patterns.md**: Common extension architecture patterns
- **assets/template/**: Basic extension template to start from

## Limitations

- Chrome AI is experimental and API surface may change
- Requires Chrome Canary or Dev channel (version 127+)
- Model must be downloaded (~1.7GB - happens automatically)
- Rate limits and context length restrictions apply
- Not all devices support all features
- Currently supports English, Spanish, and Japanese output
- Quality may vary from cloud-based models
- JSON responses may require robust parsing
