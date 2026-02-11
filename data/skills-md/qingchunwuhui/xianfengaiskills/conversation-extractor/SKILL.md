---
name: conversation-extractor
description: |
  快速提取对话中的关键内容并生成基础笔记（问题+解决方案）。
  适用于记录Bug修复、技术问题解答、工具发现等实战内容。
  Triggers: /note, /save
---

# 对话提取器 (Conversation Extractor)

**角色定位**：对话内容的快速记录器，帮你把对话中的价值信息转化为可检索的笔记。

## 核心职责

**单一职责**：快速采集对话内容，完整保留实战过程，只添加元数据，**不做任何内容判断和重组**。

## 设计原则：分离关注点

```
📥 采集阶段（本技能） → 完整保留，不判断
📋 日清阶段（人工）   → 初步筛选，决定去留
💎 提炼阶段（其他技能）→ 深度整理，资产化
```

**核心理念**："采集不判断，日清做决策，周回顾做提炼"

## 使用场景

触发指令：`/note` 或 `/save`

适用场景：
- 刚修好一个Bug，想快速记录
- 刚解决了技术问题，想保存对话
- 发现了有用的工具或方法
- 获得了新的认知洞察
- **任何觉得可能有价值的对话**（不确定时也存，日清时再决定）

## 工作流程

当你输入 `/note` 或 `/save` 时，我会：

1. **读取采集标准**
   - 执行前必须先读取 `references/extraction_criteria.md`
   - 严格按照其中的规则执行（完整保留，不做判断）

2. **回溯对话**
   - 向上翻阅对话历史，识别实质性内容

3. **完整复制**
   - 按照采集标准保留所有内容
   - 只删除明显无关的工具调用提示和礼貌用语

4. **优化问题可读性**
   - 对于依赖上下文的简短问题（如"那这个呢？"），添加澄清注释
   - 格式：`_（即：...）_`（斜体+括号）
   - 保留原问题，不替换

5. **添加元数据**
   - 按照 `references/note_template.md` 添加 frontmatter
   - 生成文件名：`{YYYY-MM-DD}-实战-{任务名称}.md`

6. **保存到收集箱**
   - 存入 `E:\OBData\ObsidianDatas\0收集箱日清\` 文件夹
   - 保持对话原貌，不添加任何结构化标记

## 后续深化

如果需要记录完整的**排查过程**和**思考复盘**，请使用：
- `process-doc-generator` skill（生成完整过程文档）

如果需要对笔记进行**问答追加**，请使用：
- `qa-appender` skill（智能问答追加）

## 资源文件
- 笔记模板：[references/note_template.md](references/note_template.md)
- 提取标准：[references/extraction_criteria.md](references/extraction_criteria.md)
- 示例：[references/examples.md](references/examples.md)
