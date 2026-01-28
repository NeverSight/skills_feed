---
name: openrouter
description: Use this skill when the user wants to call different LLM models through OpenRouter's unified API, compare model responses, track costs and response times, or find the best model for a task. Triggers include requests to test models, benchmark performance, use specific providers (OpenAI, Anthropic, Google, etc.), or optimize for speed/cost.
---

# OpenRouter

## Overview

OpenRouter provides a unified API to access hundreds of LLM models from different providers (OpenAI, Anthropic, Google, Meta, and more) with automatic routing, cost tracking, and performance monitoring. Use this skill to make API calls to any OpenRouter model, compare responses across models, track costs and latency, and optimize model selection.

## Quick Start

To call an OpenRouter model:

1. Set `OPENROUTER_API_KEY` in your environment
2. Use the `scripts/call_openrouter.sh` script with `--model` and `--prompt` flags
3. Add `--json` flag for structured output

The script returns:
- **Response time** in seconds (wall-clock time)
- **Cost** in dollars (OpenRouter pricing)
- **Full response content**
- **Token counts** (prompt, completion, total)

## Making API Calls

### Basic Usage

The `scripts/call_openrouter.sh` script provides a flexible CLI interface:

```bash
# Basic call
bash scripts/call_openrouter.sh \
  --model "anthropic/claude-3.5-sonnet" \
  --prompt "Explain quantum computing" \
  --json

# With optional parameters
bash scripts/call_openrouter.sh \
  --model "openai/gpt-4o:nitro" \
  --prompt "Write a haiku" \
  --max-tokens 100 \
  --temperature 0.7 \
  --json
```

### Command-Line Arguments

- `--model` (required): Model ID (e.g., "anthropic/claude-3.5-sonnet")
- `--prompt` (required): User prompt/question
- `--system`: Optional system message
- `--max-tokens`: Maximum tokens to generate
- `--temperature`: Temperature (0.0-2.0)
- `--json`: Output as JSON (default: human-readable)

### Environment Variables

- `OPENROUTER_API_KEY` (required): Your API key
- `OPENROUTER_REFERER` (optional): HTTP referer for tracking (default: http://localhost)
- `OPENROUTER_TITLE` (optional): Title for tracking (default: Local Test)
- `MODEL` (optional): Override the default model

### Reading the Output

The script outputs:
1. Response time in seconds (measured client-side)
2. Complete JSON response with:
   - `choices[0].message.content`: The model's response
   - `usage.prompt_tokens`: Input token count
   - `usage.completion_tokens`: Output token count
   - `usage.total_tokens`: Total tokens used

### Cost Calculation

To calculate costs:
1. Get the model's pricing from the models list (see references)
2. Calculate: `(prompt_tokens × prompt_price) + (completion_tokens × completion_price)`

Example: If a model costs $0.0000025/token for prompts and $0.000002/token for completions, and uses 14 prompt + 277 completion tokens:
- Cost = (14 × 0.0000025) + (277 × 0.000002) = $0.000035 + $0.000554 = $0.000589

## Model Selection

### Finding Models

Retrieve the full models list with pricing and capabilities:

```bash
curl https://openrouter.ai/api/v1/models -H "Authorization: Bearer $OPENROUTER_API_KEY" > models.json
```

The list is sorted by creation date (newest first), serving as a proxy for quality.

**Important**: The models list can be very large. Consider saving to a file and using grep/jq to filter by:
- Price range
- Context length
- Specific providers
- Capabilities (vision, function calling, etc.)

### Model Naming Format

OpenRouter uses `provider/model-name`:
- `anthropic/claude-3.5-sonnet`
- `openai/gpt-4o`
- `google/gemini-pro-1.5`
- `meta-llama/llama-3.1-405b-instruct`

### Speed and Feature Modifiers

**`:nitro`** - Use the fastest available provider for a model
```
anthropic/claude-3.5-sonnet:nitro
```

**`:online`** - Enable web search capabilities
```
openai/gpt-4o:online
```

**Combine modifiers:**
```
anthropic/claude-3.5-sonnet:nitro:online
```

## Common Use Cases

### Testing a Specific Model

Edit the script's `PAYLOAD` to use the desired model and messages:

```bash
{
  "model": "anthropic/claude-3.5-sonnet",
  "messages": [
    {"role": "user", "content": "Explain quantum computing in simple terms"}
  ]
}
```

### Comparing Models

Run the script multiple times with different models and compare:
- Response quality
- Response time
- Token usage and cost

### Finding the Cheapest/Fastest Model

1. Fetch the models list and save to file
2. Use jq or grep to filter by criteria
3. Test top candidates with the script
4. Compare performance vs. cost trade-offs

For speed: Try models with `:nitro` suffix
For cost: Filter models.json by lowest pricing values

## Accessing Provider Information (Non-API)

### Opening Provider Pages with Query Parameters

While the OpenRouter API provides model information, **provider-specific details** like throughput, latency, and availability are only accessible via the web interface. You can programmatically open these pages with sorting parameters.

#### URL Structure

```
https://openrouter.ai/<model-slug>/providers?sort=<sorting-option>
```

**Available Sorting Options:**
- `throughput` - Sort by provider throughput (tokens/sec)
- `price` - Sort by cost
- `latency` - Sort by response latency

#### Example: Opening Provider Page Sorted by Throughput

For the model `moonshotai/kimi-k2-0905`:

```
https://openrouter.ai/moonshotai/kimi-k2-0905/providers?sort=throughput
```

#### Use Case: Finding the Fastest Provider

When you need to identify which provider offers the best throughput for a specific model:

1. Extract the model slug from the model ID (e.g., `openai/gpt-4o` → `openai/gpt-4o`)
2. Construct the URL: `https://openrouter.ai/<model-slug>/providers?sort=throughput`
3. Open the URL in a browser or use web automation tools
4. The page will display providers sorted by throughput (highest first)

**Note**: This information is **not available through the API** and requires web interface access. The `:nitro` modifier automatically routes to the fastest provider, but if you need to see provider-specific metrics, use the web interface with query parameters.

#### Workflow for Agent Tools

If you have browser automation capabilities:
- Use `mcp__chrome-devtools__new_page` or similar to open the provider page
- The `?sort=throughput` parameter ensures the page loads pre-sorted
- Extract provider metrics from the rendered page

### Accessing Model Rankings by Category

OpenRouter provides model rankings filtered by specific use cases and categories. These rankings show which models perform best for different tasks based on user ratings and token usage.

#### URL Structure

```
https://openrouter.ai/rankings?category=<category-value>#categories
```

#### Available Categories

| Category Display Name | Query Parameter Value | Example URL |
|----------------------|----------------------|-------------|
| Programming | `programming` | `https://openrouter.ai/rankings?category=programming#categories` |
| Roleplay | `roleplay` | `https://openrouter.ai/rankings?category=roleplay#categories` |
| Marketing | `marketing` | `https://openrouter.ai/rankings?category=marketing#categories` |
| Marketing/Seo | `marketing/seo` | `https://openrouter.ai/rankings?category=marketing/seo#categories` |
| Technology | `technology` | `https://openrouter.ai/rankings?category=technology#categories` |
| Science | `science` | `https://openrouter.ai/rankings?category=science#categories` |
| Translation | `translation` | `https://openrouter.ai/rankings?category=translation#categories` |
| Legal | `legal` | `https://openrouter.ai/rankings?category=legal#categories` |
| Finance | `finance` | `https://openrouter.ai/rankings?category=finance#categories` |
| Health | `health` | `https://openrouter.ai/rankings?category=health#categories` |
| Trivia | `trivia` | `https://openrouter.ai/rankings?category=trivia#categories` |
| Academia | `academia` | `https://openrouter.ai/rankings?category=academia#categories` |

#### Usage Notes

- Most categories use lowercase versions of their names (e.g., `programming`, `science`)
- The **Marketing/Seo** category uses `marketing/seo` with a slash
- The `#categories` anchor is optional but helps navigate to the categories section
- Rankings are **not available through the API** and require web interface access
- Each category shows models ranked by performance for that specific use case

#### Use Case: Finding the Best Model for a Specific Task

When you need to identify top-performing models for a particular domain:

1. Select the appropriate category from the table above
2. Construct the URL: `https://openrouter.ai/rankings?category=<value>#categories`
3. Open the URL in a browser or use web automation tools
4. The page displays models ranked by performance for that category

Example for programming tasks:
```
https://openrouter.ai/rankings?category=programming#categories
```

#### Workflow for Agent Tools

If you have browser automation capabilities:
- Use `mcp__chrome-devtools__new_page` to open the rankings page
- The `?category=<value>` parameter loads the page with the selected category
- Verify the category dropdown shows the expected category name
- Extract model rankings and performance data from the rendered page

## Resources

### scripts/call_openrouter.sh

Bash script that makes an API call to OpenRouter and returns timing, cost, and full response. Uses curl and jq for simple, dependency-free execution.

**Requirements**: `jq` (for JSON parsing)

**Usage**:
```bash
bash call_openrouter.sh --model "anthropic/claude-3.5-sonnet" --prompt "Your question" --json
```

### references/models_and_features.md

Detailed reference on:
- How to fetch and filter the models list
- Model naming conventions
- Speed (`:nitro`) and web search (`:online`) modifiers
- Cost calculation from usage data
