---
name: google-ai-studio
description: Enables Claude to use Google AI Studio for testing prompts, exploring models, and prototyping AI applications
category: google
---

# Google AI Studio Skill

## Overview
Claude can use Google AI Studio at aistudio.google.com to test prompts, explore Gemini models, tune parameters, and prototype AI applications. Useful for prompt engineering, model comparison, and API experimentation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/google-ai-studio/install.sh | bash
```

Or manually:
```bash
cp -r skills/google-ai-studio ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set GOOGLE_EMAIL "your-email@gmail.com"
```

## Privacy & Authentication

**Your credentials, your choice.** Canifi LifeOS respects your privacy.

### Option 1: Manual Browser Login (Recommended)
If you prefer not to share credentials with Claude Code:
1. Complete the [Browser Automation Setup](/setup/automation) using CDP mode
2. Login to the service manually in the Playwright-controlled Chrome window
3. Claude will use your authenticated session without ever seeing your password

### Option 2: Environment Variables
If you're comfortable sharing credentials, you can store them locally:
```bash
canifi-env set SERVICE_EMAIL "your-email"
canifi-env set SERVICE_PASSWORD "your-password"
```

**Note**: Credentials stored in canifi-env are only accessible locally on your machine and are never transmitted.

## Capabilities
- Test prompts with different models
- Adjust model parameters (temperature, tokens)
- Create and save prompt templates
- Test structured outputs
- Explore model capabilities
- Generate API code snippets
- Test function calling
- Create chat-based applications
- Compare model outputs
- Debug prompt issues

## Usage Examples

### Example 1: Test Prompt
```
User: "Test this prompt in AI Studio with different temperatures"
Claude: Opens AI Studio, enters prompt, tests at temp 0.2, 0.7, 1.0.
        Returns: "Results comparison:
        Low temp: More focused, deterministic
        High temp: More creative, varied..."
```

### Example 2: Generate API Code
```
User: "Get the API code for my prompt in Python"
Claude: Opens AI Studio, configures prompt, exports code.
        Returns Python code snippet ready for integration.
```

### Example 3: Test Structured Output
```
User: "Test getting JSON output from Gemini"
Claude: Opens AI Studio, configures structured output schema,
        tests prompt. Returns: "Structured output working, here's the schema..."
```

### Example 4: Model Comparison
```
User: "Compare Gemini Pro vs Gemini Flash for my use case"
Claude: Tests same prompt on both models, compares:
        Speed, quality, cost considerations.
        Returns: "Recommendation: Flash for speed, Pro for complex reasoning"
```

## Authentication Flow
1. Claude navigates to aistudio.google.com via Playwright MCP
2. Authenticates with GOOGLE_EMAIL if needed
3. Handles 2FA if prompted (notifies user via iMessage)
4. Accesses studio interface

## AI Studio Workflow
```
1. Navigate to aistudio.google.com
2. Create new prompt or open existing
3. Configure model and parameters
4. Enter prompt content
5. Run and evaluate output
6. Iterate on prompt
7. Export code or save template
```

## Selectors Reference
```javascript
// New prompt button
'[aria-label="Create new prompt"]'

// Model selector
'.model-selector' or '[aria-label="Model"]'

// Temperature slider
'[aria-label="Temperature"]'

// Max tokens
'[aria-label="Maximum output tokens"]'

// Prompt input
'.prompt-input' or '[aria-label="Prompt"]'

// Run button
'[aria-label="Run"]'

// Output panel
'.output-panel'

// Get code button
'[aria-label="Get code"]'

// Save button
'[aria-label="Save"]'

// History panel
'.history-panel'
```

## Model Parameters
```
Temperature: 0.0-2.0 (creativity vs consistency)
Max Output Tokens: Up to model limit
Top-P: 0.0-1.0 (nucleus sampling)
Top-K: Number of tokens to consider
Stop Sequences: Strings to stop generation
Safety Settings: Content filtering levels
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Model Not Available**: Try alternative model, notify user
- **Rate Limited**: Wait and retry with backoff
- **Prompt Too Long**: Truncate or split, suggest alternatives
- **API Error**: Retry, report error details

## Self-Improvement Instructions
When you learn a better way to use Google AI Studio:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific parameter combinations that work well
4. Note any new models or features available

## Notes
- AI Studio provides access to latest Gemini models
- Free tier has usage limits; check quota
- API keys generated here work with Gemini API
- Tuned models can be created and saved
- Supports text, image, and multimodal prompts
- Code export available in Python, Node.js, cURL
- History of prompts maintained for reference
- Useful for prototyping before production deployment
