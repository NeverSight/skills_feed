---
name: spec-plan
description: "当用户希望进行 Spec 驱动开发（Spec-first / Spec-driven development）时，你 MUST 使用此 Skill：先把需求与约束收敛为一份可实施、可评审的 Spec，再进入实现。该 Skill 最终只生成 1 个 Spec 文件写入 /docs/specs/，并进行 1 次 git commit（仅提交该 Spec）。本 Skill 不写实现代码。"
---

# Spec-Plan Workflow (Spec-driven)

## 输出物（强制）
- 仅一个文件：`docs/specs/spec{n}_<slug>.md`
- 仅一次提交：只提交该 spec（不生成 design、不额外 commit）

---

## 0) 建立仓库上下文（必须做）
在提问前先快速扫一遍（减少无效问题）：
- 目录：`README*`, `docs/`, `src/`, `packages/`, `configs/`
- 是否已有 `docs/specs/` 与命名规则/模版
- `git log -n 20 --oneline` 了解近期方向与约束
- 基本约定：API 风格/配置方式/CI 门槛（知道“怎么跑”即可）

> 若无法访问仓库：明确说明“缺少仓库上下文”，请用户粘贴目录树/相关模块/现有接口示例；同时继续推进，使用 `TBD` 标注不确定项。

---

### 提问规则（强制）
- 只问 **关键 / 核心 / 有歧义** 的问题（会影响实现路径、范围或接口）
- **分组提问方式**：每轮最多问 **3 个**「最关键、最阻塞」的问题；用户回答后，模型必须先用 **2–4 句**复述：
  - ✅ 已确认的信息
  - ⚠️ 仍待明确（TBD）的关键点
- 在完成复述后，模型必须进行一次 **关键歧义自检**：
  - 判断当前信息是否仍存在 **会影响实现路径、范围或接口的关键不确定性**
  - 若 **存在**，进入下一轮继续追问（仍遵循每轮最多 3 个的问题限制）
  - 若 **不存在**，立即停止提问并进入下一阶段
- 全程严格去重与合并相近问题，累计问题总数 **不超过 10 个**，确保聚焦而不发散
- 问题优先采用 **多选形式**，并提供 `Other / 不确定`

### 你必须优先搞清的点（从上往下问）
1) 用户/场景：谁用？何时触发？现在怎么做？最大痛点？
2) 成功标准：怎样算成功？验收口径是什么？
3) 范围边界：必须做/不做/可选（YAGNI：可选放 Future Work）
4) 输入输出：UI/API/CLI/配置/任务？对外契约是什么？
5) 约束：兼容性/性能/权限/合规/依赖系统/上线窗口
6) 风险：失败点、回滚要求、数据一致性要求

---

## 2) 方案收敛（必须给 2-3 个）
当信息够用时，给出 2-3 个方案，并明确推荐方案。
每个方案包含：
- 适用前提
- 优点
- 缺点/风险
- 复杂度（低/中/高）
- 影响模块/大概改动点
- Future Work（明确这次不做的）

> 推荐方案必须解释“为何在当前约束下最合适”，避免过度设计。

---

## 3) Spec 写作（可评审、可实施）
### Spec 必须具备
- 可实现：模块改动点、接口契约、数据结构、边界条件
- 可验收：Acceptance Criteria（对齐 FR/NFR）
- 可发布：上线/迁移/回滚/兼容策略
- 不确定项：正文标 `TBD`，末尾 `Open Questions` 汇总

### Spec 结构（精简版）
1. Background（痛点与现状）
2. Goals / Non-goals（防止范围膨胀）
3. Use Cases（关键用户路径）
4. Requirements（FR / NFR：最小必要）
5. Proposed Solution（推荐方案 + 关键决策 + 备选方案简述）
6. Architecture & Data Flow（流程/时序/边界）
7. Interfaces / Data Model（如适用：API、事件、存储变更）
8. Error Handling & Edge Cases（幂等/重试/降级/一致性）
9. Rollout / Migration / Rollback（发布与回退）
10. Work Breakdown（按顺序的任务拆解 + Done Definition）
11. Testing Notes（关键用例与覆盖范围说明）
12. Acceptance Criteria（Checklist）
13. Open Questions（汇总 TBD）
14. Future Work（可选）

---

## 4) 落盘规则（强制）
### 目录与编号
- 目录：`docs/specs/`（不存在则创建）
- 编号自增：
  - 扫描 `docs/specs/` 下匹配 `spec(\d+)_` 的文件
  - `n = max_n + 1`；若无则 `n = 1`

### 文件名 slug（snake_case）
- 文件名：`spec{n}_<slug>.md`
- 规则：小写；空格/连字符→`_`；去特殊字符；合并连续 `_`
- 中文主题：优先简短英文/拼音；否则用语义清晰英文兜底

---

## 5) 唯一一次提交（强制）
完成并确认 spec 后：
1) `git status --porcelain` 确认变更
2) `git add docs/specs/spec{n}_<slug>.md`
3) `git commit -m "docs: add spec{n} <slug>"`（若仓库有规范则遵循）

对话中必须返回：
- spec 文件路径
- Spec 标题 + 3-5 行摘要
- Top 3 Open Questions（如有）

结束语（必须）：
**“Spec 已生成并一次性提交。Ready to set up for implementation?”**
