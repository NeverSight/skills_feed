---
name: frontend-prompt
description: 前端开发辅助 Skill。将模糊需求转化为结构化开发方案，自动检测项目技术栈，生成审批流、工作流和澄清问题。Use when starting frontend development tasks like adding pages, fixing bugs, or optimizing code.
---

# Frontend Prompt Skill

帮助 Agent 将模糊的前端开发需求转化为专业的结构化方案。

## When to use this skill

- 用户提出前端开发任务时（新增页面、修复 Bug、优化性能、重构等）
- 需要将模糊需求转化为结构化方案时
- 需要查询前端开发最佳实践和规范时

## How to use it

### 1. 优化需求 (推荐)

使用 npm 包将需求转化为详细开发方案：

```bash
npx -y @jdzhang225gmail/frontend-prompt optimize "<用户需求>" --fields optimizedPrompt,workflow
```

**输出字段说明：**
- `optimizedPrompt`: 优化后的完整 Prompt
- `workflow`: 工作流步骤和审批关口
- `guardrails`: 开发守则清单
- `clarifyingQuestions`: 需要向用户确认的问题

### 2. 查询本地规范数据

搜索 guardrails、gates 和 questions：

```bash
node .agent/skills/frontend-prompt/scripts/index.js search "<关键词>"
```

## Decision tree

```
用户需求
    │
    ├─ UI/UX 相关？
    │   ├─ 是 → 先获取设计建议 → 再运行 optimize
    │   └─ 否 → 直接运行 optimize
    │
    ├─ 需求是否清晰？
    │   ├─ 是 → 执行 optimize 输出的 workflow
    │   └─ 否 → 使用 clarifyingQuestions 向用户确认
    │
    └─ workflow 包含 gates？
        ├─ 是 → 在 gate 节点暂停并请求用户确认
        └─ 否 → 继续执行
```

## Guardrails

执行时应遵循 `optimize` 命令输出中的 `guardrails` 列表，主要包括：

- **禁止凭空捏造** - 信息不足时必须反问用户
- **禁止引入新依赖** - 无明确理由不得引入新 npm 包
- **禁止占位符代码** - 必须输出完整可执行代码
- **KISS 原则** - 优先选择最简单的实现方案

## Approval Gates

如果 workflow 输出包含 `gates`，这是审批关口。Agent 必须在对应步骤：

1. 完成当前阶段的输出
2. 暂停并提示用户审批
3. 等待用户确认后才继续下一阶段

常见的 gate 节点包括：设计方案确认、开发计划确认、变更说明确认等。
