---
name: gptrans
description: Instructions for using the GPTrans Node.js library for AI-powered translations with smart batching, caching, context-aware translations, refinement, and image translation. Use when adding i18n/localization to a Node.js project, translating text or images between languages, or managing multilingual content.
version: 1.0.0
tags: [nodejs, translation, i18n, localization, ai, gpt, multilingual]
---

# GPTrans Library Skill

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Core Concepts](#core-concepts)
- [Basic Usage](#basic-usage)
- [Common Tasks](#common-tasks)
- [Agent Usage Rules](#agent-usage-rules)
- [API Quick Reference](#api-quick-reference)
- [References](#references)

## Overview

GPTrans is a Node.js library that provides AI-powered translations with smart batching, caching, and context awareness. It uses LLMs (via ModelMix) to produce high-quality, culturally-adapted translations while minimizing API calls through intelligent debouncing and batch processing.

Use this skill when:
- Adding internationalization (i18n) or localization to a Node.js application
- Translating text content between languages using AI
- Translating images between languages (via Gemini)
- Managing multilingual content with caching and manual correction support
- Building tools that need context-aware translations (gender, tone, domain)
- Pre-translating or bulk-translating content with `preload()`
- Refining existing translations with specific style instructions

Do NOT use this skill for:
- Python or non-Node.js projects
- Simple key-value i18n (use `i18next` or similar instead)
- Projects that don't need AI-quality translations

## Installation

```bash
npm install gptrans
```

### Environment Setup

GPTrans requires API keys for the underlying LLM providers. Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
GEMINI_API_KEY=your_gemini_api_key  # only for image translation
```

### Dependencies

GPTrans uses [ModelMix](https://github.com/clasen/ModelMix) internally for LLM calls. It is installed automatically as a dependency.

## Core Concepts

### How It Works

1. **First call to `t()`**: Returns the original text immediately. The translation is queued in the background.
2. **Batching**: Queued translations are grouped by character count (`batchThreshold`) and debounce timer (`debounceTimeout`) to optimize API usage and provide better context to the LLM.
3. **Caching**: Completed translations are stored in `db/gptrans_<locale>.json`. Subsequent calls return instantly from cache.
4. **Second call to `t()`**: Returns the cached translation.

### Language Tags

GPTrans uses BCP 47 language tags: `en-US`, `es-AR`, `pt-BR`, `fr`, `de`, etc. Region can be omitted for universal variants (e.g., `es` for generic Spanish).

### Translation Cache Files

Translations are stored as JSON in `db/` directory:
- `db/gptrans_<target>.json` — cached translations for target locale
- `db/gptrans_from_<source>.json` — source text registry

You can manually edit translation files to override specific entries.

## Basic Usage

```javascript
import GPTrans from 'gptrans';

const gptrans = new GPTrans({
  from: 'en-US',
  target: 'es-AR',
  model: 'sonnet45'
});

// Translate text — returns original on first call, cached translation after
console.log(gptrans.t('Hello, {name}!', { name: 'John' }));

// Context-aware translation (e.g., gender)
console.log(gptrans.setContext('Message is for a woman').t('You are very good'));

// Context auto-clears — pass empty to reset
console.log(gptrans.setContext().t('Welcome back'));
```

### Constructor Options

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `from` | `string` | `'en-US'` | Source language (BCP 47) |
| `target` | `string` | `'es'` | Target language (BCP 47) |
| `model` | `string \| string[]` | `'sonnet45'` | Model key or array for fallback chain |
| `batchThreshold` | `number` | `1500` | Max characters before triggering batch |
| `debounceTimeout` | `number` | `500` | Milliseconds to wait before processing |
| `freeze` | `boolean` | `false` | Prevent new translations from being queued |
| `name` | `string` | `''` | Instance name (isolates cache files) |
| `context` | `string` | `''` | Default context for translations |
| `instruction` | `string` | `''` | Additional instruction for the translator (tone, style). Does not affect cache key |
| `promptFile` | `string` | `null` | Custom prompt file path (overrides built-in) |
| `debug` | `boolean` | `false` | Enable debug output |

## Common Tasks

### Translate text with parameter substitution

```javascript
const gptrans = new GPTrans({ from: 'en', target: 'es-AR' });
console.log(gptrans.t('Hello, {name}!', { name: 'Martin' }));
// First call: "Hello, Martin!" (original)
// After caching: "Hola, Martin!" (translated)
```

### Use model fallback for resilience

```javascript
const gptrans = new GPTrans({
  from: 'en',
  target: 'fr',
  model: ['sonnet45', 'gpt41']  // falls back to gpt41 if sonnet45 fails
});
```

### Pre-translate all pending texts

```javascript
const gptrans = new GPTrans({ from: 'en', target: 'es' });

// Register texts
gptrans.t('Welcome');
gptrans.t('Sign in');
gptrans.t('Sign out');

// Wait for all translations to complete
await gptrans.preload();

// Now all calls return cached translations
console.log(gptrans.t('Welcome'));  // "Bienvenido"
```

### Pre-translate with reference languages

Use existing translations in other languages as context for better accuracy:

```javascript
const gptrans = new GPTrans({ from: 'es', target: 'fr' });
await gptrans.preload({
  references: ['en', 'pt']  // AI sees English and Portuguese as reference
});
```

### Pre-translate using an alternate base language

Translate from an intermediate language instead of the original (useful for gender-neutral intermediaries):

```javascript
const gptrans = new GPTrans({ from: 'es', target: 'pt' });
await gptrans.preload({
  baseLanguage: 'en',       // translate FROM English instead of Spanish
  references: ['es']        // show original Spanish for context
});
```

### Set context for gender-aware translations

```javascript
const gptrans = new GPTrans({ from: 'en', target: 'es-AR' });

// Context applies to next translation(s) in the batch
console.log(gptrans.setContext('The user is female').t('You are welcome'));

// Reset context
console.log(gptrans.setContext().t('Thank you'));
```

### Set instruction for translation style

```javascript
const gptrans = new GPTrans({
  from: 'en', target: 'es-AR',
  instruction: 'Use a formal and professional tone'
});

console.log(gptrans.t('Welcome to our platform'));
```

### Refine existing translations

Improve cached translations with specific instructions:

```javascript
const gptrans = new GPTrans({ from: 'en', target: 'es-AR' });

// Single instruction
await gptrans.refine('Use a more colloquial tone');

// Multiple instructions (single API pass — preferred)
await gptrans.refine([
  'Use "vos" instead of "tu"',
  'Shorten texts where possible without losing meaning',
  'Use a more friendly and natural tone'
]);

// Custom refine prompt
await gptrans.refine('More formal', { promptFile: './my-refine-prompt.md' });
```

### Translate an image

Requires `GEMINI_API_KEY`. Auto-detects language folders for output path:

```javascript
const gptrans = new GPTrans({ from: 'en', target: 'es' });

// en/banner.jpg → es/banner.jpg (auto sibling folder)
const translatedPath = await gptrans.img('en/banner.jpg');

// With options
const result = await gptrans.img('en/hero.jpg', {
  quality: '1K',
  jpegQuality: 92,
  prompt: 'Translate all visible text to Spanish. Keep layout and style.'
});
```

### Freeze mode (prevent new translations)

```javascript
const gptrans = new GPTrans({ from: 'en', target: 'es', freeze: true });

// Returns original text, logs "[key] text" — nothing queued
console.log(gptrans.t('New text'));

// Toggle at runtime
gptrans.setFreeze(false);
```

### Purge orphaned translations

Remove cached translations whose source text no longer exists:

```javascript
await gptrans.purge();
```

### Translate between regional variants

```javascript
// Spain Spanish → Argentina Spanish
const es2ar = new GPTrans({
  from: 'es-ES',
  target: 'es-AR',
  model: 'sonnet45'
});

console.log(es2ar.t('Eres muy bueno'));
```

### Check language availability

```javascript
import GPTrans from 'gptrans';

if (GPTrans.isLanguageAvailable('pt-BR')) {
  // Language is supported
}
```

## Agent Usage Rules

- Always check `package.json` for `gptrans` before running `npm install`.
- Store API keys (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`) in `.env`. Never hardcode keys.
- Use BCP 47 language tags for `from` and `target` (e.g., `en-US`, `es-AR`, `pt-BR`, or just `es`).
- The `t()` method is synchronous and non-blocking. It returns the original text on first call and the cached translation on subsequent calls. Do NOT `await` it.
- To ensure translations are complete before using them, call `await gptrans.preload()` after registering texts with `t()`.
- Use `setContext()` for gender-aware or domain-specific translations. Context is captured per-batch and auto-resets when changed.
- Use the `instruction` constructor option for style/tone guidance (e.g., "Use a more natural tone"). Unlike `context`, `instruction` does NOT affect the cache key — different instructions for the same text overwrite the same translation entry.
- Prefer passing an array of instructions to `refine()` over multiple calls — it processes everything in a single API pass.
- Use model arrays (`model: ['sonnet45', 'gpt41']`) for production resilience with automatic fallback.
- Translation caches live in `db/gptrans_<locale>.json`. These files can be manually edited to override specific translations.
- The `name` constructor option isolates cache files (`db/gptrans_<name>_<locale>.json`), useful for multiple independent translation contexts in the same project.
- When translating images, ensure `GEMINI_API_KEY` is set. The `img()` method auto-creates sibling language folders.
- Do NOT use `freeze: true` during initial translation — it prevents all new translations from being queued.
- Variables in curly braces (`{name}`, `{count}`) in source text are preserved through translation. Parameter substitution happens at `t()` call time.

## API Quick Reference

| Method | Returns | Description |
| --- | --- | --- |
| `new GPTrans(options)` | `GPTrans` | Create instance with `from`, `target`, `model`, etc. |
| `.t(text, params?)` | `string` | Translate text (sync). Returns cached or original. |
| `.get(key, text)` | `string \| undefined` | Get translation by key, queue if missing. |
| `.setContext(context?)` | `this` | Set context for next batch (gender, tone, etc.). |
| `.setFreeze(freeze?)` | `this` | Enable/disable freeze mode at runtime. |
| `await .preload(options?)` | `this` | Pre-translate all pending texts. Options: `{ references, baseLanguage }`. |
| `await .refine(instruction, options?)` | `this` | Refine existing translations. Accepts string or array. |
| `await .img(path, options?)` | `string` | Translate image text. Returns output path. |
| `await .purge()` | `this` | Remove orphaned translations from cache. |
| `GPTrans.isLanguageAvailable(code)` | `boolean` | Check if a language code is supported. |

## References

- [GitHub Repository](https://github.com/clasen/GPTrans)
- [npm Package](https://www.npmjs.com/package/gptrans)
- [ModelMix (underlying LLM library)](https://github.com/clasen/ModelMix)
