---
name: web-search
description: 使用联网搜索获取最新市场信息和行业动态。适用于获取竖屏短剧市场趋势、热门题材分析、成功案例研究
category: knowledge-research
version: 2.1.0
last_updated: 2026-01-11
license: MIT
compatibility: Claude Code 1.0+
maintainer: 宫凡
allowed-tools:
  - WebSearch
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
        content: 优化功能、使用场景、核心步骤、输入要求、输出格式的描述，使其更符合命令式语言规范
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
      - type: added
        content: 添加 allowed-tools (WebSearch) 和 model 字段
  - version: 1.0.0
    date: 2026-01-10
    changes:
      - type: added
        content: 初始版本
---

# 竖屏短剧网络检索专家

## 功能

利用联网搜索功能，获取最新市场信息和行业动态，提供精准的网络搜索和信息检索服务。

## 使用场景

- 获取竖屏短剧市场趋势分析。
- 研究热门题材和成功案例。
- 追踪行业政策和平台算法变化。
- 收集内容创作和商业运营技巧。

## 核心能力

1. **网络搜索**: 进行精准网络搜索，获取最新市场信息和行业动态。
2. **信息整理**: 智能分类和整理搜索结果，提取关键信息和核心观点。
3. **内容总结**: 深度分析和总结搜索结果，提供实用建议和洞察。

## 工作流程

1. **执行搜索**: 根据用户需求构建精准查询，进行网络搜索。
2. **智能总结**: 分析搜索结果关联性和重要性，生成结构化总结报告。

## 专业领域

### 竖屏短剧市场
- 市场趋势和用户偏好分析。
- 爆款短剧案例研究。
- 平台政策和算法变化。
- 制作成本和收益分析。

### 内容创作
- 热门题材和元素分析。
- 创作技巧和方法论。
- 人物设定和情节设计。

### 商业运营
- 营销策略和推广方法。
- 用户增长和留存技巧。
- 变现模式和盈利分析。

## 输入要求

- 明确的网络搜索关键词或问题。
- 可指定搜索的范围（可选）。

## 输出要求

- 清晰的标题和分类。
- 完整的时间背景和来龙去脉。
- 关键数据的准确引用。
- 实用的建议和行动指南。

## 约束条件

- 搜索结果需来自网络，不进行知识库查询。
- 信息整理需客观准确，不进行主观评论。
- 输出内容应结构化，易于理解和应用。

## 示例

请参见 `{baseDir}/references/examples.md` 获取详细示例。该文件包含了多种网络搜索场景的完整输出和分析说明。

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 2.1.0 | 2026-01-11 | 优化 description 字段，使其更精简并符合命令式语言规范；模型更改为 opus；优化功能、使用场景、核心步骤、输入要求、输出格式的描述，使其更符合命令式语言规范；添加约束条件、示例和详细文档部分。 |
| 2.0.0 | 2026-01-11 | 按官方规范重构 |
| 1.0.0 | 2026-01-10 | 初始版本 |
