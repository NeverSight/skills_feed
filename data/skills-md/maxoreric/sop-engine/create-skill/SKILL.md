---
name: create-skill
description: 创建新 Skill 的 Skill。当需要把能力固化为 Skill 时触发。触发词：创建 skill、新建 skill、写一个 skill、create skill。
---

# 创建 Skill

根据目标和调研结果，创建新的 Skill。

## 前置条件

- `workspace/goal.md` 存在（目标定义）
- `workspace/research.md` 存在（调研结果，可选）

## 流程

1. **读取输入** - 读取 goal.md 和 research.md
2. **设计 Skill** - 确定 Skill 的结构和内容
3. **创建 SKILL.md** - 写入 Skill 文件
4. **创建 criteria.md** - 写入评价标准
5. **更新状态** - 更新 .meta/status.json

## SKILL.md 规范

```markdown
---
name: skill-name
description: 描述 + 触发条件。触发词：xxx、yyy、zzz。
---

# Skill 标题

[简短描述]

## 流程

[步骤列表]

## 输入

[需要什么输入]

## 输出

[产出什么]

## 原则

[执行原则]
```

### description 写作要点

- 说明 Skill 做什么
- 列出触发条件
- 包含触发词列表
- 控制在 200 字符内

## criteria.md 规范

**必须同时创建评价标准**

```markdown
# 评价标准：[skill-name]

## 核心维度（必填）

### 1. 产出完整性
- 描述：产出是否包含所有必要内容
- 权重：高
- 通过条件：[具体条件]

### 2. 产出质量
- 描述：产出的质量是否达标
- 权重：高
- 通过条件：[具体条件]

### 3. 目标达成
- 描述：是否达成原始目标
- 权重：高
- 通过条件：[具体条件]

## 补充维度（可选）

[根据 Skill 特点添加]

## 总体通过条件

- 通过分数：>=7（满分10）
```

## 输出位置

- SKILL.md → `.sop-engine/skills/<skill-name>/SKILL.md`
- criteria.md → `.sop-engine/skills/<skill-name>/criteria.md`

## 原则

- Skill 要单一职责
- description 是触发机制，写清楚
- 评价标准要可量化
- 先简单后完善，支持迭代
