---
name: rewrite-en2zh
description: 将英文内容重写为简体中文。用于英文文章、文档、博客的中文重写。使用 deverbalization 技巧，理解原意后脱离英文外壳，用中文自然表达，而非逐字对照。保留 Markdown 格式、AI 专有名词。
license: MIT
metadata:
  author: simonwong
  version: "1.0.0"
---

# 英文重写为简体中文

## 核心理念

这是**重写**，不是翻译。

像口译大师一样工作：

1. **理解** - 完全理解原文的意思
2. **脱壳** - 忘掉英文的词汇和句式
3. **重写** - 用中文自然地表达同样的意思

目标：让读者感觉这就是中文母语者写的文章。

**重要原则：尊重原意，保持原有格式不变。** 重写是换一种语言表达，不是删减、增添或改变原文的意思和结构。

## 重写规则

### 保留不变

- **AI 专有名词**：Agent、OpenAI、Claude、Gemini、GPT、LLM、Prompt、Token、RAG、Fine-tuning 等
- **技术术语**：API、SDK、JSON、Markdown、GitHub、Docker、Kubernetes 等
- **品牌/产品名**：React、Next.js、Vercel、Anthropic 等
- **Markdown 格式**：图片、链接、加粗、斜体、代码块、列表等全部保留
- **代码块内容**：完全保留，禁止改动

### 标点符号

中文内容使用中文标点，但代码、命令、URL 内保持英文标点。

### 领域固定术语

某些术语在特定语境下有固定的中文表达，需要根据语境判断，不能随意改写：

- context：AI 语境是"上下文"，其他语境可能是"背景"或"情境"
- model：AI 语境是"模型"，时尚语境是"模特"
- training：AI 语境是"训练"，HR 语境是"培训"

### 链接处理

链接文本重写为中文，URL 保留：

```markdown
原文：[Learn more about agents](https://example.com/agents)
重写：[进一步了解 Agent](https://example.com/agents)
```

### 禁止格式

禁止出现中英对照的括号格式：

```markdown
错误：English（英文）
错误：中文（Chinese）
错误：翻译（Translation）
```

直接用一种语言表达即可。

## 重写示例

### 示例 1：句子重写

```
原文：The agent autonomously decides which tools to use based on the context.

逐字对照（错误）：Agent 自主地决定基于上下文使用哪些工具。

重写（正确）：Agent 会根据当前上下文自行判断该用哪些工具。
```

### 示例 2：段落重写

```
原文：
This is a breaking change. If you're upgrading from v1, you'll need to
update your configuration files. Don't worry - the migration is straightforward.

逐字对照（错误）：
这是一个破坏性更改。如果你正在从 v1 升级，你将需要更新你的配置文件。
不要担心 - 迁移是简单直接的。

重写（正确）：
这是一个不兼容的更新。从 v1 升级的话，需要改一下配置文件。不用担心，过程很简单。
```

### 示例 3：保留格式

```markdown
原文：
**Important:** Check out [this guide](https://docs.example.com) for more details.

![Architecture diagram](https://example.com/arch.png)

重写：
**重要提示：** 更多细节请参考[这份指南](https://docs.example.com)。

![架构图](https://example.com/arch.png)
```

## 执行流程

1. 通读全文，理解整体意思和语境
2. 逐段重写，脱离英文句式
3. 保留所有 Markdown 格式
4. 保留专有名词和技术术语
5. 检查是否有中英对照的括号格式，如有则删除
6. 通读重写后的中文，确保流畅自然
