---
name: subtitle-correction
description: Correct subtitle files (.srt) generated from speech recognition. Use when the user uploads subtitle files and asks to correct, fix, or proofread subtitles, especially for technical content like programming tutorials, AI/ML courses, or any content with domain-specific terminology. Supports Chinese and English subtitles with intelligent error detection and correction while preserving exact timeline information.
---

# Subtitle Correction Skill

This skill corrects speech recognition errors in subtitle files while strictly preserving timeline information.

## Interactive Workflow

### Step 1: Request Terminology from User

**IMPORTANT**: Before starting any correction, ALWAYS ask the user for domain-specific terms.

Prompt the user with:

```
在开始修正之前，请提供一些关键术语，帮助我更准确地识别和修正语音识别错误：

1. **专有名词**：人名、品牌名、产品名等（如：Anthropic、Claude）
2. **技术术语**：框架、库、工具名称（如：LangChain、OpenAI、PyTorch）
3. **领域词汇**：行业特定词汇（如：checkpointer、middleware、runtime）
4. **其他关键词**：视频中频繁出现的重要词汇

请用逗号分隔，例如：`LangChain, Agent, OpenAI, checkpointer`
```

For English users:

```
Before I begin correction, please provide key terms to help me accurately identify speech recognition errors:

1. **Proper nouns**: Names, brands, products (e.g., Anthropic, Claude)
2. **Technical terms**: Frameworks, libraries, tools (e.g., LangChain, PyTorch)
3. **Domain vocabulary**: Industry-specific terms (e.g., checkpointer, middleware)
4. **Other keywords**: Important words that appear frequently

Please separate with commas, e.g.: `LangChain, Agent, OpenAI, checkpointer`
```

### Step 2: Confirm Understanding

After receiving terms, confirm by:
1. Listing the terms received
2. Identifying the likely domain/context (AI/ML tutorial, web dev, etc.)
3. Asking if there are any additional terms before proceeding

Example response:
```
收到以下术语：
- 技术框架：LangChain, LangGraph, OpenAI
- 技术概念：Agent, checkpointer, runtime

看起来这是一个 LangChain 智能体开发的教程视频。

还有其他需要补充的术语吗？如果没有，我将开始修正字幕。
```

### Step 3: Process with Terms

Use the provided terms to:
1. Build a mental model of expected vocabulary
2. Identify likely speech recognition errors
3. Apply consistent corrections throughout

### When User Doesn't Provide Terms

If user says "没有" / "no" / "直接开始":
1. Proceed with correction using built-in patterns
2. Flag uncertain corrections for user review
3. After completion, ask if any terms were missed

## Core Workflow

1. **Read the subtitle file** - Load the .srt file provided by the user
2. **Identify error patterns** - Recognize common speech recognition mistakes
3. **Apply corrections** - Fix errors while preserving timestamps exactly
4. **Output corrected file** - Return or save based on user's context

## Strict Rules

### Timeline Preservation
- **NEVER modify timestamps** - Keep all `00:00:00,000 --> 00:00:00,000` lines exactly as-is
- **NEVER change subtitle numbering** - Preserve sequence numbers
- **NEVER merge or split subtitle entries** - One-to-one correspondence

### Error Categories

#### 1. Phonetic Errors (同音字/谐音错误)
Common in Chinese speech recognition:
- 会话 ↔ 绘画 (huìhuà)
- 元数据 ↔ 源数据 (yuán shùjù)
- 本课 ↔ 本科 (běnkè)
- 示例 ↔ 事例 (shìlì)
- 实践 ↔ 时间 (shíjiàn)

#### 2. Technical Term Errors
Speech recognition often fails on:
- Framework names: LangChain, LangGraph, OpenAI, PyTorch, TensorFlow
- Programming terms: API, SDK, runtime, checkpointer, middleware
- Code identifiers: snake_case names, function names, class names

#### 3. English-Chinese Mixed Content
- Luncheon/lunch → langchain
- open EI/open Email → OpenAI
- land GRAPH → langgraph
- a memory Server → MemorySaver

#### 4. Code-Related Terms
Convert spoken descriptions to proper format:
- "underscore" → "_" in variable names
- "dot" → "." in method calls
- Recognize camelCase, snake_case, PascalCase patterns

## User-Provided Terminology

When users provide a terminology list, use it as the primary reference for corrections:

```
用户提供的术语：LangChain,Agent,OpenAI,LangGraph
```

These terms indicate:
- Expected proper spellings of technical terms
- Context about the content domain
- Hints for identifying speech recognition errors

## Processing Strategy

### For Long Files (>200 lines)
1. Process in chunks using `view_range` parameter
2. Maintain context across chunks
3. Build complete corrected file incrementally

### For Technical Content
1. Identify the domain (AI/ML, web dev, etc.)
2. Build mental model of expected terminology
3. Apply domain-specific corrections consistently

### Quality Checks
Before outputting:
- Verify all timestamps unchanged
- Verify subtitle count unchanged
- Check terminology consistency throughout
- Ensure no orphaned corrections (partial fixes)

## Common Correction Patterns

### Chinese AI/ML Course Content

| Error | Correction | Context |
|-------|------------|---------|
| 蓝犬/蓝卷/Lantern | LangChain | Framework name |
| 绘画 | 会话 | Session/conversation |
| 拖/tour | tool | Tool concept |
| checkpoint组件 | checkpointer组件 | Memory component |
| 源数据 | 元数据 | Metadata |
| 大约模型 | 大模型 | Large model |
| 中间键 | 中间件 | Middleware |

### Code Identifiers

| Spoken | Written |
|--------|---------|
| user underscore 001 | user_001 |
| thread underscore id | thread_id |
| create underscore agent | create_agent |
| runtime dot state | runtime.state |

## Output Format

When saving, use `-corrected` suffix:
- Input: `filename.srt`
- Output: `filename-corrected.srt`

## Validation Script

Use `scripts/subtitle_tool.py` to validate and analyze subtitle files:

```bash
# Validate corrected file preserves structure
python scripts/subtitle_tool.py validate original.srt corrected.srt

# Show word-level diff with colored output (default, changes only)
python scripts/subtitle_tool.py diff original.srt corrected.srt

# Show ALL entries (changed and unchanged) in terminal
python scripts/subtitle_tool.py diff original.srt corrected.srt --all

# Generate HTML diff report (recommended for review)
python scripts/subtitle_tool.py diff original.srt corrected.srt --html report.html

# Show simple line-based diff (original/corrected lines)
python scripts/subtitle_tool.py diff original.srt corrected.srt --simple

# Disable colors for piping to files
python scripts/subtitle_tool.py diff original.srt corrected.srt --no-color

# Analyze file for potential speech recognition errors
python scripts/subtitle_tool.py analyze input.srt --terms "LangChain,OpenAI"
```

### Diff Output Formats

#### Terminal Output (Default)
Shows **word-level** changes with colors:

```
[1] 00:00:01,500 --> 00:00:04,500
  今天我们来学习[-Luncheon-]{+LangChain+}框架

[3] 00:00:08,000 --> 00:00:12,500
  我们可以用它来创建[-绘画-]{+会话+}应用程序
```

- `[-deleted-]` - Text removed (shown in red in terminal)
- `{+added+}` - Text added (shown in green in terminal)
- Use `--all` to show unchanged entries too

#### HTML Report (Recommended for Review)
Generates a full comparison report with:
- **All entries** displayed (changed and unchanged)
- **Side-by-side columns**: Original | Corrected | Diff View
- **Visual highlighting**: Red strikethrough for deletions, green for additions
- **Summary statistics**: Total entries, changed count, unchanged count
- **Jump links**: Quick navigation to changed entries
- **Change indicators**: Yellow dot marks changed rows

```bash
python scripts/subtitle_tool.py diff original.srt corrected.srt --html diff_report.html
```

Then open `diff_report.html` in a browser.

### Validation Workflow

1. **Before correction**: Run `analyze` to identify potential errors
2. **After correction**: Run `validate` to ensure structural integrity
3. **Review changes**: Run `diff --html report.html` to generate a visual comparison report

### Validation Checks
- Entry count matches original
- All timestamps unchanged
- All sequence numbers preserved
- No formatting corruption

## Example Interaction

### Interaction 1: User uploads file without terms

**User**: 帮我修正这个字幕文件

**Claude**:
```
在开始修正之前，请提供一些关键术语，帮助我更准确地识别语音识别错误：

1. **专有名词**：人名、品牌名、产品名
2. **技术术语**：框架、库、工具名称
3. **领域词汇**：行业特定词汇
4. **其他关键词**：视频中频繁出现的重要词汇

请用逗号分隔，例如：`LangChain, Agent, OpenAI`
```

**User**: LangChain, Agent, OpenAI, LangGraph, checkpointer

**Claude**:
```
收到以下术语：
- 技术框架：LangChain, LangGraph, OpenAI
- 技术概念：Agent, checkpointer

这是一个 LangChain 相关的技术教程。还有补充吗？
```

**User**: 没有了，开始吧

**Claude**: [Proceeds with correction workflow]

### Interaction 2: User provides terms upfront

**User**: 帮我修正字幕，术语：LangChain, OpenAI, Agent

**Claude**: [Confirms terms, then proceeds directly]

### Correction Process

1. Read uploaded .srt file
2. Run `analyze` to identify potential errors
3. Apply corrections using provided terms as primary reference
4. Run `validate` to confirm structural integrity
5. Save corrected file with `-corrected` suffix
6. Generate diff report and present summary of changes
7. **Offer HTML report**: Ask user if they want an HTML diff report for easier review

**Output**: Provide categorized summary of corrections made.

**After completion, prompt user**:
```
修正完成！我可以生成一个 HTML 差异报告，方便您在浏览器中查看所有修改。
需要生成 HTML 报告吗？

Correction complete! I can generate an HTML diff report for easier review in your browser.
Would you like me to generate the HTML report?
```
