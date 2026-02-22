---
name: project-analysis
description: 项目分析工具，用于分析代码库的系统架构和模块数据流。当用户需要理解项目结构、生成架构图、分析模块间的数据流向、生成时序图时使用此技能。支持输出 Mermaid 语法的可视化图表。适用场景：(1) 项目架构梳理 (2) 模块依赖分析 (3) 数据流追踪 (4) 新成员项目入门 (5) 技术文档生成
---

# 项目分析技能

本技能提供两种分析模式，帮助理解和可视化代码库结构。

## 前置检查：已有文档检索

**在执行任何分析之前，必须先执行此步骤。**

### 步骤 1：扫描已有文档

使用 metadata 扫描脚本检查目标项目的 `docs/` 目录是否存在已有的分析文档：

```bash
python3 <skills-root>/skills/project-analysis/scripts/scan_docs_metadata.py <项目根目录>/docs
```

脚本会输出 JSON 格式的文档列表，包含每份文档的 metadata（type、scope、module、keywords）和内容摘要。

### 步骤 2：判断相似性

将用户当前的分析请求与扫描结果进行比对：

- **类型匹配**：用户请求的分析类型（architecture/dataflow/sequence）是否与已有文档的 `type` 字段匹配
- **范围匹配**：分析范围（full/module）和目标模块（`module` 字段）是否一致
- **关键词匹配**：用户描述中的关键词是否与已有文档的 `keywords` 字段高度重叠

### 步骤 3：发现相似文档时暂停

如果发现与用户请求**高度相似**的已有文档（类型+范围+模块匹配，或关键词重叠度高），**必须暂停分析任务**，使用 AskUserQuestion 工具向用户提问：

提问内容应包含：
1. 已有文档的文件路径
2. 已有文档的简要概述（基于 metadata 和 summary）
3. 已有文档的生成日期
4. 询问用户是否仍需继续进行新的分析

示例提问格式：
> 在 docs/ 目录下发现了类似的分析文档：
> - **文件**：docs/architecture.md
> - **类型**：系统架构分析
> - **日期**：2024-01-15
> - **概述**：全项目架构分析，涵盖 React + Node.js 技术栈...
>
> 是否仍需要重新进行分析？

用户确认继续后，才进入下方的分析模式执行实际分析。

如果 `docs/` 目录不存在或无相似文档，直接进入分析模式。

---

## 分析模式

### 模式一：系统架构分析

从宏观层面分析项目，生成整体架构视图。

> 详细分析步骤和执行指南参考：`references/mode-architecture.md`

### 模式二：模块数据流分析

深入分析特定模块或功能的数据流转过程。

> 详细分析步骤和执行指南参考：`references/mode-dataflow.md`

---

## 文档输出步骤

分析完成后，按以下步骤将结果保存到 `docs/` 目录。

### 步骤 1：确定输出文件路径

根据分析类型确定文件名（命名规范见 `references/output-spec.md`）：

| 分析类型 | 文件名 |
|---------|--------|
| 系统架构 | `docs/architecture.md` |
| 模块架构 | `docs/architecture-{模块}.md` |
| 数据流 | `docs/dataflow-{功能}.md` |
| 时序图 | `docs/sequence-{流程}.md` |

### 步骤 2：生成 Mermaid 在线预览链接

对报告中每个 Mermaid 图表，运行编码脚本生成预览链接：

```bash
python3 <skills-root>/skills/mermaid-live-preview/scripts/encode.py "<mermaid代码>"
```

将输出的 Edit 和 View 链接附加在对应代码块之后。

### 步骤 3：写入文档

使用 Write 工具将报告写入目标文件。文档必须采用两段式结构：

**第一段：YAML Frontmatter Metadata**

```yaml
---
type: architecture | dataflow | sequence
scope: full | module
module: ""          # scope=module 时必填
date: "YYYY-MM-DD"
keywords:
  - 关键词1
  - 关键词2
tech_stack:
  - 技术栈1
entry_point: ""     # 数据流分析时填写
---
```

**第二段：Markdown 正文**

按对应分析类型的报告模板填写（模板见 `references/output-spec.md`）。

### 步骤 4：确认输出

告知用户：
- 文档已保存的完整路径
- 各 Mermaid 图表的在线预览链接

---

## 参考文件

- 分析模式详细步骤：`references/mode-architecture.md`、`references/mode-dataflow.md`
- 文档模板与命名规范：`references/output-spec.md`
- Mermaid 图表模板：`references/mermaid-templates.md`
