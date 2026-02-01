---
name: humanizerai
description: Detect AI-generated content and humanize text to bypass AI detectors. Use when the user wants to check if text is AI-generated, make AI text undetectable, or bypass GPTZero/Turnitin.
license: MIT
metadata:
  author: humanizerai
  version: "1.0.0"
  website: https://humanizerai.com
allowed-tools: WebFetch Bash
---

# HumanizerAI Skill

This skill provides AI detection and text humanization capabilities via the HumanizerAI API.

## Capabilities

1. **Detect AI Content** - Analyze text to determine if it was written by AI
2. **Humanize Text** - Transform AI-generated text into natural human writing

## Setup

Before using this skill, you need a HumanizerAI API key:

1. Sign up at https://humanizerai.com
2. Subscribe to Pro or Business plan
3. Go to Settings > API Keys
4. Create and copy your API key

Set your API key as an environment variable:
```bash
export HUMANIZERAI_API_KEY="hum_your_api_key_here"
```

## Available Commands

### /detect-ai

Check if text is AI-generated. Returns a score (0-100) and detailed metrics.

**Usage:**
```
/detect-ai [paste your text here]
```

### /humanize

Rewrite AI-generated text to make it undetectable. Uses credits (1 word = 1 credit).

**Usage:**
```
/humanize [paste your text here]
```

**With intensity:**
```
/humanize --intensity aggressive [paste your text here]
```

Intensity options:
- `light` (Light) - Subtle changes, preserves style
- `medium` (Medium) - Balanced rewrites (default)
- `aggressive` (Bypass) - Maximum bypass mode

## API Reference

See [api-reference.md](api-reference.md) for full endpoint documentation.

## Examples

See [examples.md](examples.md) for usage examples.
