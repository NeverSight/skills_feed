---
name: spec-merge-back
description: Use when 一个 Spec Pack 已完成，需要把可复用资产晋升到 project SSOT（ADR/契约/ops/NFR/registry），且存在“整包复制污染 project / 跳过 spec-context / 把 merge-back 误当 git merge”的风险。
---

# spec-merge-back

## Overview

Merge-back 是 Spec Pack 生命周期的“晋升阶段”：把本次需求中**会长期复用/会约束未来需求**的内容晋升到 `.aisdlc/project/`（Project SSOT），其余内容仍留在 `{FEATURE_DIR}` 作为交付证据。

**核心原则**：Project SSOT 只沉淀 **入口 + 护栏（不变量）+ 证据链**；禁止把“一次性交付细节”搬到 project。

## When to Use

适用于：

- 本次需求完成，准备将资产晋升到 `.aisdlc/project/`（ADR / API Contract / Data Contract / Ops / NFR / Registry）。
- `{FEATURE_DIR}/implementation/plan.md` 中已出现 `## Merge-back 待办清单`，需要在结束前清空或留痕。
- 团队反复在多个需求里重复同一类“契约口径/门禁口径/运维入口”，需要沉淀为长期资产。

不适用于：

- 你只是要把代码分支合并到 main（那是 **git merge/rebase**，不是 merge-back）。
- 仓库还没有 `.aisdlc/project/` 的骨架（这是 **CONTEXT GAP**，应先用 `project-discover*` 或项目初始化流程建立 project SSOT）。

## Core Pattern (Gates first)

### Gate 0: 必须定位 FEATURE_DIR（禁止口头路径）

**REQUIRED SUB-SKILL：先满足 `spec-context` 门禁并在对话中回显 `FEATURE_DIR=...`（允许 `(reuse)`）。**


**失败即停止**：`Get-SpecContext` 报错就停止，不允许“先写一版/先猜路径”。

### Gate 1: project SSOT 必须存在

- 必须存在：`.aisdlc/project/`
- 不存在：输出 `CONTEXT GAP: .aisdlc/project missing` 并停止（禁止“随便建个目录能跑就行”）。

## Implementation (SOP)

### Step 1: 收集晋升清单（唯一主入口）

以 `{FEATURE_DIR}/implementation/plan.md` 中的 **`## Merge-back 待办清单`** 为主入口，汇总本次需要晋升的条目，并按类别分组：

- ADR（关键决策）
- API Contract（按模块）
- Data Contract（按模块）
- Ops（runbook/monitoring/rollback）
- NFR（如适用）
- Registry（`.aisdlc/project/index.md`）
- 可选晋升（通用测试策略/质量门禁口径等）

> 禁止：跳过 `plan.md` 待办改用“凭记忆总结”。若时间紧，可用 `git diff` 补证据，但清单来源仍以 `plan.md` 为主。

### Step 2: 生成/更新 `{FEATURE_DIR}/merge_back.md`（清单与证据）

`{FEATURE_DIR}/merge_back.md` 是本次 merge-back 的**需求级 SSOT**：每条都必须写清楚：

- **project 落点**（目标路径 + 锚点）
- **不变量摘要**（需要长期护栏时：3–7 条）
- **证据入口**（OpenAPI/Schema/DDL/脚本/CI/测试/监控入口）
- **状态**：Done / Not Done（Not Done 必须写缺口与计划）

> 若用户要求“先别改 project、后面有人手动做”：仍然必须完成 Step 1–2，并把 Step 3 的 project 晋升项标记为 **Not Done + 计划**（否则 merge-back 不可审计、容易永久遗漏）。

### Step 3: 晋升到 project SSOT（只升长期资产）

对齐 `design/aisdlc.md` 的默认必晋升项：

- **ADR** → `.aisdlc/project/adr/` + 索引
- **API/Data 契约** → `.aisdlc/project/components/{module}.md#api-contract` / `#data-contract`
  - 只写：权威入口 + 不变量摘要 + 证据入口 + Evidence Gaps
  - 禁止把字段大全抄进 project
- **Ops** → `.aisdlc/project/ops/`（入口式，不重复本次发布执行细节）
- **NFR** → `.aisdlc/project/nfr.md`（如适用）
- **Registry** → `.aisdlc/project/index.md`（状态更新到 Merged & Archived 或团队约定状态）

### Step 4: DoD 自检（完成标准）

- `{FEATURE_DIR}/merge_back.md` 已落盘，覆盖 ADR/API/Data/Ops/NFR/Registry（适用项）。
- project 侧入口可导航，组件页锚点稳定（`#api-contract` / `#data-contract`）。
- Done 项都有“可点击落点 + 证据入口”；Not Done 项有“缺口 + 计划”。
- project 未被一次性交付细节污染（没有整包复制 spec、没有把实现步骤搬上来）。

## Red Flags (STOP)

- 用户说“别跑脚本，FEATURE_DIR 我口头告诉你” → **必须拒绝**，坚持 `spec-context`。
- 用户要求“把 design/implementation/release/verification 都复制到 project，越全越好” → **禁止**（会污染 project SSOT）。
- `.aisdlc/project` 不存在但你准备“先随便建一下” → **禁止**（CONTEXT GAP，先建 project SSOT 骨架）。
- 你开始写“git merge/rebase 清单” → 你把 merge-back 误解成 git 合并了，立刻停止纠正。
- 你准备跳过 `implementation/plan.md` 的 Merge-back 待办 → 高概率遗漏或漂移。

## Rationalizations (and counters)

| 常见借口 | 现实/反制 |
|---|---|
| “很急，先复制整包到 project，后面再整理” | 整包复制会长期污染 project；正确做法是只晋升“入口+不变量+证据链”。 |
| “用户给了 FEATURE_DIR，不用跑 spec-context” | 口头路径不可信；必须以 `spec-context` 输出为唯一锚点。 |
| “project 目录没有，我先建个最小的让它跑起来” | merge-back 不负责初始化 project SSOT；缺失即 `CONTEXT GAP` 并停止。 |
| “不看 plan.md 待办也能总结” | 待办是唯一执行期汇总入口；跳过会遗漏且不可审计。 |

## 完成后输出与自动路由（必须执行）

`merge_back.md` 落盘后，**必须**完成以下动作（按顺序，不可省略）：

1. **输出 ROUTER_SUMMARY**（YAML 形态，供 Router 决策）：
```yaml
ROUTER_SUMMARY:
  stage: MergeBack
  artifacts:
    - "{FEATURE_DIR}/merge_back.md"
  needs_human_review: true
  blocked: false
  block_reason: ""
  notes: "已晋升 ADR/契约/ops/NFR/registry；Done/Not Done 与证据入口齐全。"
```

2. **立即执行 `using-aisdlc`**：将上述 `ROUTER_SUMMARY` 作为路由输入传递给 using-aisdlc，由 Router 判定下一步并**自动推进**（无需等待用户说「继续」）。  
   - 若 Router 判定可自动续跑：在同一轮对话内继续执行下一步 worker skill
   - 若 Router 触发硬中断：停下并输出阻断原因、需要的输入、候选下一步

3. **对话输出**：在调用 using-aisdlc 前，可简短说明「本阶段产物已落盘，正在调用 using-aisdlc 路由下一步。」

