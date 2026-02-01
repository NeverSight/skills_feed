---
name: output-formatter
description: 整合智能体输出结果为结构化最终输出，支持多种格式。适用于整合分析报告、生成结构化报告
category: result-processing
version: 2.1.0
last_updated: 2026-01-11
license: MIT
compatibility: Claude Code 1.0+
maintainer: 宫凡
allowed-tools: []
model: opus
changelog:
  - version: 2.1.0
    date: 2026-01-11
    changes:
      - type: improved
        content: 优化 description 字段，使其更精简并符合命令式语言规范
      - type: changed
        content: 模型更改为 opus
      - type: improved
        content: 优化功能、使用场景、核心能力、核心步骤、输入要求、输出格式的描述，使其更符合命令式语言规范
      - type: added
        content: 添加约束条件、示例和详细文档部分
  - version: 2.0.0
    date: 2026-01-11
    changes:
      - type: breaking
        content: 按照 Agent Skills 官方规范重构
      - type: improved
        content: 优化 description，使用命令式语言，精简主内容
      - type: added
        content: 添加 license、compatibility 可选字段
  - version: 1.0.0
    date: 2026-01-10
    changes:
      - type: added
        content: 初始版本
---

# 输出整理专家

## 功能

将各个智能体的输出结果整合为结构化的最终输出，支持多种输出格式。

## 使用场景

- 整合多个智能体的分析结果，生成统一的结构化报告。
- 将复杂数据转换为Markdown、JSON、HTML、纯文本等多种易读格式。
- 批处理大量智能体输出，确保格式一致性与可读性。
- 自动化报告生成流程，提升工作效率。

## 核心能力

- **结果整合**: 高效整合所有智能体的输出结果，确保数据完整性。
- **多格式输出**: 支持Markdown、JSON、HTML、纯文本等多种常用格式，满足不同需求。
- **结构化展示**: 提供清晰的层次结构和统一的格式风格，提升可读性。
- **批处理支持**: 能够批量处理多个智能体结果，实现自动化格式化。
- **错误处理**: 妥善处理输入数据异常，确保输出稳定可靠。

## 核心步骤

```
接收智能体输出结果
    ↓
根据指定输出格式进行格式化
    ↓
整合所有结果数据
    ↓
生成结构化最终输出
    ↓
返回格式化结果
```

## 输入要求

- **智能体输出结果**: 待整合的各个智能体输出数据（JSON、Markdown、Text等）。
- **目标输出格式**（可选）: 指定最终输出的格式（如 Markdown, JSON, HTML, Text）。默认为 Markdown。
- **结构化要求**（可选）: 具体的输出结构模板或字段定义。

## 输出格式

根据指定的输出格式，提供结构化的最终结果。例如，在Markdown格式下，可能包含以下内容：

```
# 综合报告标题

## 故事大纲
[完整的故事大纲内容]

## 大情节点
- 情节点1: [描述]
- 情节点2: [描述]

## 思维导图
![思维导图](图片URL)
[思维导图编辑链接]

## 详细情节点
### 情节点1
[详细描述]

## 元数据信息
- 创建日期: [日期]
- 报告版本: [版本号]
```

## 约束条件

- 输入数据必须是可解析的格式，以便正确提取信息。
- 严格遵守指定的输出格式要求，确保结果的规范性。
- 避免在输出中引入无关信息或幻觉。

## 示例

参见 `{baseDir}/references/examples.md` 目录获取更多详细示例:
- `examples.md` - 包含不同智能体输出整合（如故事大纲+情节点+思维导图）和多种格式转换的详细示例。

## 详细文档

参见 `{baseDir}/references/examples.md` 获取关于输出整理的详细指导与案例。

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 2.1.0 | 2026-01-11 | 优化 description 字段，使其更精简并符合命令式语言规范；模型更改为 opus；优化功能、使用场景、核心能力、核心步骤、输入要求、输出格式的描述，使其更符合命令式语言规范；添加约束条件、示例和详细文档部分。 |
| 2.0.0 | 2026-01-11 | 按官方规范重构 |
| 1.0.0 | 2026-01-10 | 初始版本 |
