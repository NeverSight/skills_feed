---
name: solo-scope
description: 从 Solo Scope RSS（https://www.mixdao.world/feed）拉取条目，按主题整理成 3～6 类，每类生成 140 字核心价值摘要，并附每条原标题与 URL 输出简报。由 Agent 自行完成拉取、整理、写简报。触发示例：「做 Solo Scope」「 olo Scope」「整理 mixdao feed」「RSS 分类简报」。
---

# Solo Scope（RSS 简报）

由 Agent 拉取 Solo Scope 实时动态 RSS，归纳成若干类别，每类一段 140 字摘要（核心价值），并保留每条的原标题与原文链接，直接输出 Markdown 简报。

## 数据源

- **RSS 地址**：`https://www.mixdao.world/feed`
- **拉取方式**：Agent 用 `curl -s -L -H "Accept: application/rss+xml" "https://www.mixdao.world/feed"`
- **格式**：RSS 2.0，每条含 `title`、`link`、`description`、`pubDate`、`guid`。

## 工作流程（Agent 执行）

1. **拉取 RSS**：用 curl 或可用工具请求上述地址，得到 RSS XML。
2. **解析条目**：从 XML 中提取每条 `item` 的 `title`、`link`、`description`。
3. **整理分类**：根据标题与描述将条目归纳为 **3～6 个类别**（如：AI 代理与安全、模型与定价、奢侈品与零售、硬件与可穿戴、融资与投资、开发者工具等），类别名简洁。
4. **写简报**：为每个类别写一段 **140 字以内** 的「核心价值」摘要，提炼对该类内容的洞察或可行动点；下列该类别内的条目，每条格式：`- [标题](原URL)`。
5. **输出**：将完整简报以 Markdown 形式输出（可写入项目内文件，或直接回复）。

## 输出模板

```markdown
# MIXLAB Solo Scope#简报

> 来源: https://www.mixdao.world/feed  |  生成: YYYY-MM-DD | 技术支持：MIXLAB AgentOS

## 类别一名称

**摘要（核心价值）** 本段 140 字以内…

- [标题一](原URL一)
- [标题二](原URL二)

## 类别二名称
…
```

## 输出要求

- **分类**：3～6 个类别，类别名简短、可读。
- **类别摘要**：每类一段，**140 字以内**，提炼核心价值（创业者/一人公司视角）。
- **条目**：每类下列出该类条目，格式 `- [标题](原URL)`，标题与 URL 与 RSS 一致。
