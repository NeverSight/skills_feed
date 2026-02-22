---
name: mini-six-ren
description: "小六壬占卜系统 (Mini Six Ren Divination) - 中国传统占卜和命理分析。Use when the user asks for divination, fortune telling, or prediction using mini six ren (小六壬), or mentions keywords: 占卜、算卦、小六壬、三传、运势、占一卦、divination、fortune. Supports three input modes: numbers, date/time, and Chinese characters (汉字笔画). Generates three-pass (三传) predictions with five-element (五行) analysis and LLM-powered interpretation."
---

# Mini Six Ren (小六壬占卜)

Chinese traditional divination system based on the Nine-Palace hand technique. Generate three-pass (三传) predictions and provide AI-powered analysis.

## Workflow

1. Determine input mode (numbers / datetime / Chinese chars / current time)
2. Run `scripts/xiaoliu.py --format json` to compute the prediction
3. Check if `config.yaml` exists and has a `model` field:
   - **No config** (default): Display `ℹ️ 当前使用 Claude Code 内置模型解读。如需使用第三方模型，请创建 config.yaml`。Then use the built-in LLM to analyze the result following the "LLM Analysis" section below.
   - **Has config + API key**: Display `ℹ️ 当前使用 <model> 解读`。Run `scripts/interpret.py` with the prediction JSON piped in:
     ```bash
     uv run scripts/xiaoliu.py --now --question "问题" --format json | \
       uv run scripts/interpret.py --question "问题"
     ```
   - **Has config, missing API key**: Display `⚠️ 请在 .env 中设置 <ENV_KEY>`。Fall back to built-in LLM analysis.
4. Format the report using `assets/template.md`

## Quick Start

Run the divination script (uv single-file script, no project install needed):

```bash
# By three numbers
uv run scripts/xiaoliu.py --numbers 1,2,3 --question "今日运势" --format json

# By date/time (converts to lunar calendar internally)
uv run scripts/xiaoliu.py --datetime "2025-07-15 10:30" --question "面试能成功吗" --format json

# By Chinese characters (uses stroke count)
uv run scripts/xiaoliu.py --chars "天地人" --question "感情运势" --format json

# By current time
uv run scripts/xiaoliu.py --now --question "今天适合出行吗" --format json
```

Use `--format json` to get structured output for LLM analysis. Use `--format text` for human-readable display.

## Input Mode Selection

| User says | Mode | Example |
|---|---|---|
| gives 3 numbers | `--numbers` | `--numbers 3,5,7` |
| mentions a date/time | `--datetime` | `--datetime "2025-01-31 14:30"` |
| gives Chinese characters | `--chars` | `--chars "天地人"` |
| "用现在的时间" / "now" | `--now` | `--now` |
| no specific input | `--now` | default to current time |

## LLM Analysis

After getting the JSON prediction result, provide an analysis following this structure. Role-play as a 小六壬占卜大师 with deep traditional culture knowledge.

### Analysis structure

1. **卦象总览**: Summarize the three passes and their elements
2. **时间发展脉络**:
   - 初传（前期/当前）: What the first symbol means for this question
   - 中传（中期/发展）: How the middle symbol drives change
   - 末传（后期/结果）: What the final symbol predicts
3. **五行生克解读**: Explain how the element relationships affect the outcome
4. **具体建议**: Practical, actionable advice tied to the question
5. **关键提示**: Notable directions, timing, or deity influences

### Analysis guidelines

- Always tie the interpretation to the specific question asked
- Prioritize the final pass (末传) as the most important indicator
- Explain five-element relationships in terms the user understands
- Keep analysis under 800 characters (Chinese) for conciseness
- Use elegant, philosophical Chinese language but remain accessible

## Report Output

After generating the prediction and LLM analysis, format using `assets/template.md`. Replace all `{{placeholder}}` variables with actual values from the script output and LLM analysis.

## Third-Party Model Configuration (Optional)

By default, the skill uses Claude Code's built-in LLM for interpretation. To use a third-party model instead:

### Step 1: Create `config.yaml`

Create `config.yaml` in the skill root directory (`mini-six-ren/config.yaml`):

```yaml
# 格式: provider:model_name
model: deepseek:deepseek-chat
```

Format: `provider:model_name`

### Step 2: Set API Key in `.env`

Add your API key to `mini-six-ren/.env`:

```bash
DEEPSEEK_API_KEY=sk-...
```

### Supported Providers

| Provider prefix | API Key env var | Notes |
|---|---|---|
| `openai` | `OPENAI_API_KEY` | GPT series |
| `anthropic` | `ANTHROPIC_API_KEY` | Claude series |
| `google-gla` | `GEMINI_API_KEY` | Gemini series |
| `deepseek` | `DEEPSEEK_API_KEY` | DeepSeek |
| `kimi` | `MOONSHOT_API_KEY` | Moonshot Kimi |
| `qwen` | `DASHSCOPE_API_KEY` | Alibaba Qwen |
| `glm` | `ZHIPU_API_KEY` | Zhipu ChatGLM |

### Examples

```yaml
# DeepSeek
model: deepseek:deepseek-chat

# GPT-4o
# model: openai:gpt-4o

# Qwen
# model: qwen:qwen-plus
```

To switch back to built-in LLM, simply delete `config.yaml`.

## Reference

For detailed symbol meanings and five-element relationships: see [references/symbols_reference.md](references/symbols_reference.md)

For usage examples: see the `examples/` directory
