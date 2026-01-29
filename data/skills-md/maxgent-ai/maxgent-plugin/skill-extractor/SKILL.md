---
name: skill-extractor
description: 从当前会话中提取经验，自动生成可复用的 Claude Code Skill。Use when user wants to 提取skill, 总结成skill, 固化经验, 生成skill, extract skill, create skill from context, save as skill, 把经验变成skill.
---

# Skill Extractor

从当前会话的上下文中提取成功经验和失败教训，自动生成可复用的 Claude Code Skill 文件。

## Background

这是一个"元技能"——用于创建其他技能的技能。通过分析当前会话中完成的任务，提取关键步骤、常见陷阱和最佳实践，将一次性的问题解决固化为可重复的工作流。

## Instructions

你是一个经验提取助手，帮助用户将会话中的工作经验转化为可复用的 Claude Code Skill。请按以下步骤操作：

### Step 1: 分析当前会话上下文

回顾整个会话历史，识别并提取以下信息：

1. **原始需求**：用户最初想解决什么问题？
2. **执行步骤**：完成任务经历了哪些关键步骤？
3. **失败经验**：哪些尝试失败了？失败的原因是什么？
4. **成功方案**：最终采用的解决方案是什么？
5. **关键发现**：有哪些重要的注意事项、检查点或技巧？

### Step 2: 收集用户输入

**⚠️ 必须：使用 AskUserQuestion 工具收集必要信息。**

使用 AskUserQuestion 工具询问用户：

1. **Skill 名称**：这个 skill 叫什么名字？
   - 让用户输入，建议使用 kebab-case 格式（如 `api-caller`、`file-processor`）

2. **主要功能描述**：一句话描述这个 skill 做什么
   - 让用户输入或基于分析结果建议

3. **触发词**：用户会用什么词来触发这个 skill？
   - 让用户输入，建议中英文各 2-3 个

4. **保存位置**：
   - 选项：
     - "当前插件目录 skills/ (Recommended)"
     - "自定义路径"

### Step 3: 决定是否需要脚本

根据任务性质自动判断是否需要配套脚本（不要问用户）：

**需要脚本的情况：**
- 调用外部 API（如 OpenRouter、OpenAI 等）
- 复杂的文件处理（二进制文件、编码转换等）
- 需要依赖特定库（如 ffmpeg、whisper 等）
- 涉及网络请求、数据解析等

**不需要脚本的情况：**
- 纯 prompt 驱动的工作流
- 主要是 bash 命令的组合
- 简单的文件操作

**脚本语言选择：**
- **优先使用 Python**，采用 uv script 格式（内联依赖声明）
- 需要 JavaScript 时使用 Bun（Max 内置，比 Node.js 更快）

**Python uv script 模板：**
```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
#     "其他依赖",
# ]
# ///

import sys
# 脚本内容...
```

### Step 4: 生成 SKILL.md 内容

根据分析结果和用户输入，生成以下格式的 SKILL.md：

```markdown
---
name: {skill-name}
description: {功能描述}。Use when user wants to {触发词1}, {触发词2}, {trigger1}, {trigger2}.
---

# {Skill Title}

{简要说明这个 skill 的功能和来源}

## Background

> 此 skill 从 [具体任务描述] 的实践经验中提取。

{描述这个 skill 解决的问题场景}

## Prerequisites

{列出依赖条件，如环境变量、工具等}

## Instructions

{详细的执行步骤，来自成功的方案}

### Step 1: {步骤标题}

{具体操作}

### Step 2: {步骤标题}

{具体操作}

...

## Common Pitfalls

{从失败经验中提取的常见陷阱}

| 错误做法 | 正确做法 | 原因 |
|---------|---------|------|
| ❌ {错误示例} | ✅ {正确示例} | {解释} |

## Best Practices

{从成功经验中提取的最佳实践}

- {实践1}
- {实践2}
- ...

## Troubleshooting

{常见问题及解决方案，来自实际遇到的错误}

**问题：{问题描述}**
- 原因：{原因分析}
- 解决：{解决方案}

## Example Interaction

{一个典型的使用示例}

用户：{示例输入}

助手：
1. {步骤1}
2. {步骤2}
...
```

### Step 5: 写入文件

使用 Write 工具将生成的内容写入对应目录：

```
skills/{skill-name}/SKILL.md
skills/{skill-name}/{script-name}.py  # 如果需要脚本
```

如果创建了 Python 脚本，添加可执行权限：
```bash
chmod +x skills/{skill-name}/{script-name}.py
```

### Step 6: 更新文档（可选）

询问用户是否需要更新 CLAUDE.md 来注册新 skill：

- 更新项目结构图
- 更新 Skills 表格

### Step 7: 展示结果

完成后告诉用户：
1. 创建的文件路径
2. Skill 的使用方法
3. 触发词列表

## Output Quality Guidelines

生成的 SKILL.md 应该：

1. **可执行**：步骤清晰，可以直接按照执行
2. **有价值**：包含真正有用的经验，不是泛泛而谈
3. **避坑优先**：突出失败经验和常见陷阱
4. **代码示例**：关键步骤要有代码或命令示例
5. **简洁明了**：避免冗余，保持结构清晰

## Example

假设用户刚完成了一个"使用 OpenRouter API 实现图片理解"的任务，调用此 skill 后可能生成：

```markdown
---
name: openrouter-vision
description: 使用 OpenRouter API 进行图片理解。Use when user wants to 调用视觉API, 图片分析API, call vision API.
---

# OpenRouter Vision API

通过 OpenRouter 调用视觉模型分析图片。

## Background

> 此 skill 从 image-understand skill 开发实践中提取。

## Prerequisites

1. `OPENROUTER_API_KEY` 环境变量
2. Python 3.11+ 和 uv

## Instructions

### Step 1: 准备图片
- 支持格式：PNG、JPG、JPEG、GIF、WebP
- 大小限制：20MB

### Step 2: 构建 API 请求
...

## Common Pitfalls

| 错误做法 | 正确做法 | 原因 |
|---------|---------|------|
| ❌ `ext === 'jpg'` | ✅ `ext === 'jpg' \|\| ext === 'jpeg'` | jpeg 扩展名也需要处理 |
| ❌ 不检查文件大小 | ✅ 添加 20MB 限制 | API 有大小限制 |

## Best Practices

- 使用 `fs.statSync()` 检查文件大小后再读取
- MIME 类型映射要完整
- 添加可执行权限 `chmod +x`
...
```

## Notes

- 这个 skill 依赖于会话上下文，需要在完成任务后立即使用
- 生成的 skill 是初稿，用户可能需要根据实际情况调整
- 鼓励用户审查并补充遗漏的经验
