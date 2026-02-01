---
name: omega-prompt-forge
description: Create new prompts from scratch by analyzing user needs, selecting suitable prompt frameworks, and fusing OmegaPromptForge. Use when the user asks to 创建提示词/生成提示词, 设计 prompt 框架, or output a Markdown...
---

# Omega Prompt Forge

## Overview

用于从零创建提示词：先做需求分析，再用“去重后的核心字段”搭结构，需要时再选框架补缺口，必要时融合 OmegaPromptForge 作为增强层，先给创作方案确认，最后输出并保存 Markdown 提示词。

## Workflow (简化版 5 步：需求收集 → 核心提取 → 增强策略 → 方案确认 → 输出保存)

### 1. 需求收集（自动判断复杂度）
收集关键信息（缺少则提问补齐）：
- 任务目标、受众、使用场景
- 期望输出格式与长度
- 约束条件、禁用项
- 目标模型/平台
- 示例输入输出（可选）

**自动判断复杂度**：
```
简单任务：明确、一步到位 → 自动推荐 RTF/TAG/APE/BAB
中等任务：需要结构化 → 自动推荐 RACE/TRACE/CARE/RISE
复杂任务：多步推理、创新、高风险 → 自动推荐 CRISPE/CREATE/Tree of Thought
```

### 2. 核心字段提取
先填"核心字段槽位"：
- 角色/能力（Role/Persona）
- 目标/任务（Goal/Task）
- 背景/上下文（Context）
- 受众与语气（Audience/Tone）
- 输入数据（Input）
- 输出格式（Format）
- 约束条件（Constraints/Do-Not）
- 步骤/流程（Steps/Process）
- 示例/参考（Examples）
- 成功标准（Criteria）

**检查**：若核心字段已完整覆盖，框架可跳过。

### 3. 增强策略（自动推荐）
基于任务特征自动推荐：

#### 框架自动推荐（3 个维度）
```
维度 1：任务复杂度
  简单 → RTF, TAG, APE, BAB
  中等 → RACE, TRACE, CARE, RISE, COAST
  复杂 → CRISPE, CREATE, RISEN, Tree of Thought

维度 2：输出类型
  内容创作 → BAB, TRACE, BLOG, SPARK, COSTAR
  技术任务 → RTF, RISE, CIDI, GRADE
  教育培训 → Five S, ELI5, SCAMPER

维度 3：特殊需求
  语气/受众控制 → COSTAR, CRAFT, CLEAR
  推理/验证 → Tree of Thought, Self-Consistency, PROMPT
  创新/探索 → SCAMPER, CRISPE, P-I-V-O
```

#### 技巧自动推荐
基于任务风险等级：
- 容易跑偏/不稳定 → Step-Back + Few-shot
- 逻辑或计算密集 → Plan-and-Solve + Program-of-Thoughts
- 需要高可靠 → Self-Consistency + Chain-of-Verification
- 需要高创意 → Analogical Prompting + Divergent Expansion
- 复杂长流程 → Prompt Chaining + 质量检查清单

#### Omega 增强判断
**自动启用条件**（满足任一即启用）：
- 复杂任务：多步推理、跨领域整合
- 创意任务：需要突破性创新、非常规解决方案
- 高风险任务：关键决策、安全敏感、合规要求

**使用模板**：`references/omega-promptforge.md`（重度模板）

### 4. 方案确认（生成预览）
生成"创作方案"并等待用户确认：
- 核心字段填充结果
- 自动推荐的框架（用户可调整）
- 自动推荐的技巧（用户可调整）
- Omega 增强模块（仅保留必要部分）
- 预期输出结构（Markdown 目录）

### 5. 输出保存
用户确认后：
- 输出完整提示词（Markdown 格式）
- 保存到 `/Users/wisewong/Documents/Developer/prompts/<task-slug>/prompt.md`
- 仅在用户确认后写入文件

## Framework 自动推荐规则（已集成到 Workflow 第 3 步）

框架选择基于 3 个维度的自动匹配逻辑，详细规则见 `references/frameworks.md`：

1. **按复杂度匹配**（第一优先级）
   - 简单任务：RTF, TAG, APE, BAB
   - 中等任务：RACE, TRACE, CARE, RISE, COAST
   - 复杂任务：CRISPE, CREATE, RISEN, Tree of Thought

2. **按输出类型匹配**（第二优先级）
   - 内容创作：BAB, TRACE, BLOG, SPARK, COSTAR
   - 技术任务：RTF, RISE, CIDI, GRADE
   - 教育培训：Five S, ELI5, SCAMPER

3. **按特殊需求匹配**（覆盖前两个维度）
   - 语气/受众控制 → COSTAR, CRAFT, CLEAR
   - 推理/验证 → Tree of Thought, Self-Consistency, PROMPT
   - 创新/探索 → SCAMPER, CRISPE, P-I-V-O

**使用原则**：
- 优先选 1 个主框架；必要时再加 1 个辅助框架
- 框架用于"结构化提示词"，不要机械堆叠
- 若核心字段已完整覆盖，框架可跳过

## OmegaPromptForge 融合规则（简化版）

- **触发条件**：复杂任务、创意任务、高风险任务（自动判断）
- **模板选择**：统一使用 `references/omega-promptforge.md`（重度模板）
- **融合原则**：
  - 把 OmegaPromptForge 作为"增强层"，不要全文硬塞
  - 只保留与任务相关的模块：
    - 模式（SINGULARITY / METAMORPHOSIS / ZENITH）按需要择一
    - 输出架构可转为"质量检查清单"
    - 复杂任务可保留部分执行协议
  - 遇到显式 Chain-of-Thought 指令时，改写为"内部推理但只输出简要理由"
  - 优先保证可执行性与可读性，避免堆砌空洞口号

## Prompt Markdown 输出模板

```
# <Prompt Title>

## 角色
<明确角色>

## 任务目标
<清晰可衡量的目标>

## 背景/上下文
<必要信息>

## 输入
<输入格式或变量>

## 输出要求
<格式、结构、长度>

## 约束与偏好
<必须/禁止/风格>

## 质量检查
<MECE、完整性、对齐度>

## Omega 增强（可选）
<仅保留必要模块>
```

## 保存规则

- 默认保存到 `/Users/wisewong/Documents/Developer/prompts/<task-slug>/`。
- 默认文件名：`prompt.md`；如用户指定则按其要求。
- 仅在用户确认后写入文件。

## Resources

- `references/frameworks.md`: 框架清单与来源（2025 优化版，35 个精选框架）
- `references/techniques.md`: 提示工程技巧与使用规则
- `references/collections.md`: 资料库与适用场景
- `references/awesome-prompts-index.md`: Awesome ChatGPT Prompts 分类索引
- `references/omega-promptforge.md`: OmegaPromptForge 重度模板（统一使用此模板）
