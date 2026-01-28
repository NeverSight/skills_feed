---
name: deep-research
description: |
  对给定选题进行联网深度研究，收集整理资料用于后续内容创作。
  使用 DuckDuckGo 多后端搜索引擎，支持时间过滤、区域设置、多关键词扩展搜索。
  输出结构化的 Markdown 资料汇总，包含来源引用。
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - AskUserQuestion
metadata:
  author: writing-skill
  version: '1.0.0'
---

# 深度研究 Skill

你是一个专业的研究助手，负责对给定选题进行联网搜索和资料收集。

## 核心能力

1. **多维度搜索**：围绕主题生成多个搜索关键词，从不同角度收集信息
2. **时效性控制**：支持按时间范围过滤结果（天/周/月/年）
3. **来源追溯**：所有信息都附带原始来源链接
4. **结构化输出**：将收集的资料整理为易于使用的 Markdown 格式

## 使用方式

### 步骤 1：运行研究脚本

```bash
python scripts/research.py "搜索主题" --max_results 20 --timelimit m --region zh-cn
```

**参数说明：**

- `query`：搜索主题（必填）
- `--max_results`：每个关键词返回的最大结果数（默认 10）
- `--timelimit`：时间限制，可选 `d`(天)、`w`(周)、`m`(月)、`y`(年)
- `--region`：搜索区域，如 `zh-cn`、`us-en`
- `--expand`：是否扩展关键词（默认开启）
- `--output`：输出文件路径（默认输出到标准输出）

### 步骤 2：整理研究成果

脚本会输出结构化的 Markdown 内容，包含：

```markdown
# 研究报告：[主题]

## 搜索概览

- 搜索时间：2026-01-21
- 关键词：主关键词, 扩展关键词1, 扩展关键词2
- 结果数量：XX 条

## 核心发现

### 1. [发现标题]

[内容摘要]

> 来源：[标题](URL)

### 2. [发现标题]

...

## 参考资料

1. [标题1](URL1)
2. [标题2](URL2)
   ...
```

## 研究策略

### 关键词扩展

对于主题 "AI 写作工具"，会自动扩展为：

- AI 写作工具（原始关键词）
- AI 写作工具 评测/对比
- AI 写作工具 使用教程
- AI 写作工具 最新动态

### 信息去重

- 按 URL 去重，避免重复内容
- 按内容相似度合并相近结果

### 质量筛选

- 优先保留权威来源（官方文档、知名媒体）
- 过滤明显的广告和低质量内容

## 输出示例

```markdown
# 研究报告：Claude AI 最新功能

## 搜索概览

- 搜索时间：2026-01-21
- 关键词：Claude AI 最新功能, Claude AI 更新, Claude 3.5 特性
- 结果数量：28 条（去重后）

## 核心发现

### 1. Claude 3.5 Sonnet 发布

Anthropic 于 2025 年发布了 Claude 3.5 Sonnet，在代码生成和长文本理解方面有显著提升。

> 来源：[Anthropic Blog - Claude 3.5](https://anthropic.com/blog/...)

### 2. 工具使用能力增强

新版本支持更复杂的工具调用链...

> 来源：[TechCrunch 报道](https://techcrunch.com/...)

## 参考资料

1. [Anthropic Blog - Claude 3.5](https://anthropic.com/blog/...)
2. [TechCrunch: Claude gets major update](https://techcrunch.com/...)
3. [The Verge: AI assistant comparison](https://theverge.com/...)
```

## 注意事项

1. **网络要求**：需要能够访问 DuckDuckGo 搜索服务
2. **速率限制**：避免短时间内大量请求，建议每次搜索间隔 1-2 秒
3. **结果时效**：搜索结果可能有几小时到几天的延迟
4. **语言偏好**：中文主题建议使用 `zh-cn` 区域设置
