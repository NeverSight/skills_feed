---
name: deep-think
description: 'Use when user requests deep analysis, thorough thinking, or detailed breakdown of a problem. Triggered by phrases like: 帮我深入思考, 请仔细分析, 帮我详细拆解, 请梳理一下思路, 仔细考虑, 深入理解, 详细分析, or similar expressions indicating need for systematic thinking. The skill applies ReAct-Plan framework: interleaving chain-of-thought reasoning with explicit global planning, dynamic prediction, and reflection to overcome myopic behaviors.'
---

# Deep Think (ReAct-Plan Framework)

## When This Skill Activates

Trigger when user requests deeper analysis beyond surface-level responses:
- "帮我深入思考", "请仔细分析", "帮我详细拆解", "请梳理一下思路"
- "深入理解", "仔细考虑", "详细分析"

## Core Philosophy

**Think Globally, Act Locally, Reflect Continuously**

- **Explicit Planning**: Create structured plan before execution
- **Dynamic Re-planning**: Update plan after new insights emerge
- **Prediction**: Anticipate outcomes before diving in
- **Reflection**: Assess progress and update belief state

## Output Structure

### 1. Initial Planning (P0)

```markdown
## 初始规划

**核心问题**: [简述]

**目标**: [成功标准]

**已知**: [关键事实 1-3 条]

**关键未知**: [需要弄清 1-3 条]

**计划 P0**:
1. [阶段 1: 步骤 1-2]
2. [阶段 2: 步骤 1-2]
3. [阶段 3: 步骤 1-2]
```

### 2. Iterative Deep Dives (2-4 次)

**Keep it concise!** 每个迭代聚焦一个核心维度：

```markdown
## 思考：[主题]

**问题**: [当前步骤的不足或新发现的问题]

**分析**: [1-2 句关键分析]

**新发现**: [简列 1-2 条]

**计划更新**:
- [阶段 X]: [新增/修改的内容]
  - [子要点]
```

**重要原则**:
- 只显示变化的部分，不要重复整个计划
- 每个迭代 10-15 行以内
- 聚焦关键发现，避免细节堆砌

### 3. Final Synthesis

```markdown
## 最终综合

**核心发现** (3-5 条核心洞察):
1. [发现 1]
2. [发现 2]

**最终计划**:
- 阶段 1: [步骤 1, 2] ([关键细节])
- 阶段 2: [步骤 1, 2, 3] ([关键细节])
- 阶段 3: [步骤 1, 2] ([关键细节])

**关键成功因素** (3 条):
- [因素 1]
- [因素 2]

**主要风险**:
- [风险 1] → [应对]
- [风险 2] → [应对]
```

## Conciseness Guidelines

| 避免这样做 | 建议这样做 |
|------------|------------|
| 完整重复之前的计划 | 只显示变化部分 |
| 长篇分析解释 | 1-2 句直击要点 |
| 细节过多堆砌 | 提炼关键信息 |
| 迭代次数过多 | 2-4 次迭代即可 |
| 最终计划重复前文 | 精炼总结，聚焦变化 |

## Example

```markdown
## 初始规划

**核心问题**: 如何到达火星

**目标**: 安全送达火星并返回

**计划 P0**:
1. 发射火箭
2. 飞往火星
3. 着陆火星

## 思考：运载能力

**问题**: "发射火箭"太笼统，未考虑载荷和燃料

**分析**: 地火转移需 50-100 吨载荷，单次发射无法满足

**新发现**: 需要轨道加油，多次发射补给燃料

**计划更新**:
- 阶段 1: 增加轨道加油能力

## 思考：时间窗口

**问题**: 未考虑返程窗口

**分析**: 需在火星停留 500 天等返程窗口

**新发现**: 任务总时长约 3 年

**计划更新**:
- 新增 阶段 4: 火星停留 (~500 天)
- 新增 阶段 5: 返程

## 思考：生存与 ISRU

**问题**: 返程燃料从哪来？

**分析**: 无法从地球携带，必须就地生产

**新发现**: 利用火星 CO₂ 生产甲烷+氧气

**计划更新**:
- 阶段 2: 增加 货运先行，运送 ISRU 设备
- 阶段 4: 增加 ISRU 生产返程燃料

## 最终综合

**核心发现**:
1. 轨道加油和货运先行是必需策略
2. ISRU 就地生产燃料是返程关键
3. 任务总时长约 3 年

**最终计划**:
- 阶段 1: 技术开发 (运载+着陆+ISRU)
- 阶段 2: 货运先行 (4 艘船预置基础设施)
- 阶段 3: 载人发射 (轨道加油 → 地火转移 200 天)
- 阶段 4: 火星停留 (500-800 天，生产燃料+探索)
- 阶段 5: 返程 (200 天返回地球)

**关键成功因素**:
- Starship 达到设计载荷
- ISRU 无故障运行
- 生命保障维持 3 年

**主要风险**:
- 着陆失败 → 货运先行验证
- ISRU 产能不足 → 增加设备，延长停留期
```
