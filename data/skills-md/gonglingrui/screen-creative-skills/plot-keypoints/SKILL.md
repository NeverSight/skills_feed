---
name: plot-keypoints
description: 梳理故事主线，提炼并按发展阶段排列主要情节点。适用于快速掌握故事结构、制作大纲及剧本改编结构梳理
category: story-analysis
version: 2.1.0
last_updated: 2026-01-11
license: MIT
compatibility: Claude Code 1.0+
maintainer: 宫凡
allowed-tools:
  - Read
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
        content: 添加 allowed-tools (Read) 和 model 字段
      - type: added
        content: 添加 references/ 结构存放详细示例
  - version: 1.0.0
    date: 2026-01-10
    changes:
      - type: added
        content: 初始版本
---

# 大情节点分析专家

## 功能

梳理故事主线，提炼并按故事发展阶段排列主要情节点。

## 使用场景

- 快速掌握故事的整体结构和情节发展。
- 为详细情节分析提供基础框架。
- 制作故事大纲或梗概。
- 剧本改编前进行结构梳理。

## 核心步骤

1. **阅读理解**: 充分阅读并理解故事文本，把握整体结构和主题。
2. **脉络梳理**: 梳理故事准确完整的脉络，识别关键转折点。
3. **情节点提炼**: 根据情节点定义，准确总结主要情节点，确保完整准确。
4. **阶段划分**: 按故事发展阶段（如三幕式结构）进行划分和排列。
5. **结构化输出**: 按照指定格式输出，确保清晰易读。

## 输入要求

- 完整的故事文本（小说、剧本、故事大纲等）
- 建议文本长度：1000字以上以获得更完整的分析

## 输出格式

```
【阶段一：情节主旨】：
- 子情节点1
- 子情节点2
- 子情节点3

【阶段二：情节主旨】：
- 子情节点1
- 子情节点2
- 子情节点3

【阶段三：情节主旨】：
...
```

## 约束条件

- 每个情节点表述不超过150字。
- 严格按照故事文本原文意思总结，不自行创作改编。
- 确保主要情节点的总结完整、准确、细致。
- 不使用阿拉伯数字为情节点标号。

## 示例

请参见 `{baseDir}/references/examples.md` 获取详细示例。该文件包含了多种故事结构（如三幕式、五幕式、竖屏短剧、多线叙事等）的完整输入输出示例和分析说明，以及情节点提炼技巧。

## 详细文档

参见 `{baseDir}/references/` 目录获取更多文档:
- `examples.md` - 详细分析示例（三幕式、五幕式、多线叙事等不同结构类型）
- `guide.md` - 完整分析指南和最佳实践

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 2.1.0 | 2026-01-11 | 优化 description 字段，添加 allowed-tools 和 model 字段，调整主内容语言风格，删除最佳实践，并引导至 references/examples.md |
| 2.0.0 | 2026-01-11 | 按官方规范重构，添加 references 结构 |
| 1.0.0 | 2026-01-10 | 初始版本 |
