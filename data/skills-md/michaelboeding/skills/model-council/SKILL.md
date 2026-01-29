---
name: model-council
description: This skill should be used when the user asks for "model council", "multi-model", "compare models", "ask multiple AIs", "consensus across models", "run on different models", or wants to get solutions from multiple AI providers (Claude, GPT, Gemini, Grok) and compare results. Orchestrates parallel execution across AI models/CLIs and synthesizes the best answer.
---

# Model Council: Multi-Model Consensus

Run the same problem through multiple AI models in parallel, collect their **analysis only**, then Claude Code synthesizes and decides the best approach.

Unlike code-council (which uses one model with multiple approaches), model-council leverages **different model architectures** for true ensemble diversity.

## Critical: Analysis Only Mode

**IMPORTANT**: External models provide analysis and recommendations ONLY. They do NOT make code changes.

- External models: Analyze, suggest, reason, compare options
- Claude Code: Synthesizes all inputs, makes final decision, implements changes

This ensures:
1. Claude Code remains in control of the codebase
2. No conflicting changes from multiple sources
3. Best ideas from all models, unified execution

## Why Multi-Model?

Different models have different:
- Training data and knowledge cutoffs
- Reasoning patterns and biases
- Strengths (math, code, creativity, etc.)

When multiple independent models agree → High confidence the answer is correct.

## Execution Modes

### Mode 1: CLI Agents (Uses Your Existing Accounts)

Call CLI tools that use your logged-in accounts - leverages existing subscriptions!

| CLI Tool | Model | Status |
|----------|-------|--------|
| `claude` | Claude (this session) | ✅ Already running |
| `codex` | OpenAI Codex | Requires setup |
| `gemini` | Google Gemini | Requires setup |
| `aider` | Multi-model | Requires setup |

#### CLI Setup Instructions

**OpenAI Codex CLI:**
```bash
# Install via npm
npm install -g @openai/codex

# Login (uses browser auth)
codex auth

# Verify
codex --version
```

**Google Gemini CLI:**
```bash
# Install via npm  
npm install -g @anthropic-ai/gemini-cli

# Or use gcloud with Vertex AI
gcloud auth application-default login

# Verify
gemini --version
```

**Aider (Multi-model, Recommended):**
```bash
# Install via pip
pip install aider-chat

# Configure with your API keys
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."

# Run with specific model
aider --model gpt-4o --message "analyze this code"
```

**Check What's Installed:**
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/model-council/scripts/detect_clis.py
```

### Mode 2: API Calls (Pay per token)

Direct API calls - more reliable, works without CLI setup, but costs money.

Required environment variables:
- `ANTHROPIC_API_KEY` - For Claude API (https://console.anthropic.com/)
- `OPENAI_API_KEY` - For GPT-4 API (https://platform.openai.com/api-keys)
- `GOOGLE_API_KEY` - For Gemini API (https://aistudio.google.com/apikey)
- `XAI_API_KEY` - For Grok API (https://console.x.ai/)

## Configuration

### User Model Selection

Users can specify models inline:

```
model council with claude, gpt-4o, gemini: solve this problem

model council (claude + codex): fix this bug

model council all: use all available models
```

### Default Models

If not specified, use all available:
1. Check which CLI tools are installed
2. Check which API keys are set
3. Use what's available

### Config File (Optional)

Users can create `~/.model-council.yaml`:

```yaml
# Preferred models (in order)
models:
  - claude      # Use Claude Code CLI (current session)
  - codex       # Use Codex CLI if installed
  - gemini-cli  # Use Gemini CLI if installed
  
# Fallback to APIs if CLIs not available
fallback_to_api: true

# API models to use when falling back
api_models:
  anthropic: claude-sonnet-4-20250514
  openai: gpt-4o
  google: gemini-2.0-flash
  xai: grok-3
  
# Timeout per model (seconds)
timeout: 120

# Run in parallel or sequential
parallel: true
```

## Workflow

### Step 1: Parse Model Selection

Determine which models to use:
1. Check user's inline specification (e.g., "with claude, gpt-4o")
2. If none specified, check config file
3. If no config, detect available CLIs and APIs

### Step 2: Prepare the Prompt

Format the problem for each model with **analysis-only instructions**:

```
Analyze the following problem and provide your recommendations.
DO NOT output code changes directly.
Instead, provide:
1. Your analysis of the problem
2. Recommended approach(es)
3. Potential issues or edge cases to consider
4. Trade-offs between different solutions

Problem:
[user's problem here]
```

Key rules:
- Keep the core problem identical across models
- Explicitly request analysis, not implementation
- Include relevant context (code snippets, error messages)

### Step 3: Execute in Parallel

Use the API council script to query multiple models:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/model-council/scripts/api_council.py \
  --prompt "Analyze this problem and recommend solutions (do not implement): [problem]" \
  --models "claude-sonnet,gpt-4o,gemini-flash"
```

Available models:
- `claude-sonnet`, `claude-opus` - Anthropic
- `gpt-4o`, `gpt-4-turbo`, `o1` - OpenAI
- `gemini-flash`, `gemini-pro` - Google
- `grok` - xAI

List all models:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/model-council/scripts/api_council.py --list-models
```

### Step 4: Collect Responses

Gather all model responses with metadata:
- Model name and version
- Response time
- Token usage (if available)
- Full response

### Step 5: Analyze Consensus

Compare responses looking for:
- **Agreement**: Do models produce the same answer/approach?
- **Unique insights**: Does one model catch something others missed?
- **Disagreements**: Where do models differ and why?

### Step 6: Claude Code Synthesizes and Decides

Claude Code (this session) uses ultrathink to:
1. Evaluate each model's analysis
2. Identify the strongest reasoning and recommendations
3. Note where models agree (high confidence) vs disagree (investigate further)
4. Make the final decision on approach
5. **Implement the solution** - only Claude Code makes code changes

This is the key difference from just asking one model:
- Multiple perspectives inform the decision
- Claude Code remains the single source of truth for implementation
- No conflicting changes from different models

### Step 7: Deliver Results

Provide:
1. **Final synthesized answer** (best combined solution)
2. **Consensus score** (how many models agreed)
3. **Individual responses** (for transparency)
4. **Insights** (what each model contributed)

## CLI Detection

To check available CLIs:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/model-council/scripts/detect_clis.py
```

This checks for:
- `claude` - Claude Code CLI
- `codex` - OpenAI Codex CLI
- `gemini` - Gemini CLI
- `aider` - Aider (multi-model)
- `cursor` - Cursor AI (if applicable)

## Comparison: code-council vs model-council

| Aspect | code-council | model-council |
|--------|--------------|---------------|
| Models used | Claude only | Multiple (Claude, GPT, Gemini, etc.) |
| Diversity source | Different approaches | Different architectures |
| Cost | Free (uses current session) | Free (CLIs) or paid (APIs) |
| Speed | Fast (single model) | Slower (parallel calls) |
| Best for | Quick iterations | High-stakes decisions |

## When to Use Each

**Use code-council when:**
- You want fast iterations
- The problem is well-defined
- You trust Claude's reasoning

**Use model-council when:**
- High-stakes code (production, security)
- You want architectural diversity
- Models might have different knowledge
- You want to verify Claude's answer

## Error Handling

**CLI not found**: Skip that model, log warning, continue with others.

**API key missing**: Skip that provider, try CLI fallback if available.

**Timeout**: Return partial results, note which models timed out.

**No models available**: Error with setup instructions.

## Example Output

```
## Model Council Analysis Results

### Consensus: HIGH (3/3 models agree on approach)

### Summary of Recommendations:
All models recommend using a hash map for O(1) lookup. 
Key considerations raised:
- Handle null/empty input (Claude, GPT-4o)
- Consider memory vs speed tradeoff (Gemini)
- Add input validation (all models)

### Individual Analyses:

#### Claude Sonnet (API)
Analysis: The bug is caused by off-by-one error in the loop boundary.
Recommendation: Change `i <= len` to `i < len`
Edge cases noted: Empty array, single element
Confidence: High

#### GPT-4o (API)
Analysis: Loop iterates one element past array bounds.
Recommendation: Fix loop condition, add bounds check
Additional insight: Could also use forEach to avoid index errors
Confidence: High

#### Gemini Flash (API)
Analysis: Array index out of bounds on final iteration.
Recommendation: Adjust loop termination condition
Reference: Similar to common off-by-one patterns
Confidence: High

### Claude Code Decision:
Based on consensus, implementing fix with:
- Loop condition change (i < len)
- Added null check for robustness
- Unit test for edge cases

[Claude Code now implements the solution]
```
