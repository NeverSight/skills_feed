---
name: governance-docs-codex-review
description: >
  【WHEN】当需要对“治理层文档”进行 Codex 审阅并输出 vN-review.md 时调用。
  【WHEN NOT】不用于提案生成；不用于落地修改；不用于业务/代码设计。
---

# Codex 治理层文档审阅（可拔插）

## 目标
- 只输出“打分制简报”到：docs/dev_notes/governance-docs-revision/v{N}-review.md
- 评分只包含两项：
  1) 问题解决（针对用户诉求/不满点/新增内容需求）
  2) 规则遵守（是否破坏 @governance-docs-standard）

## 输入（由调用方提供）
- 本次审阅对应的版本号：v{N}
- 治理层文档清单：
  - README.md: {README_PATH}
  - CLAUDE.md: {CLAUDE_PATH}
  - 其他治理层文档: {GOVERNANCE_DOCS_LIST}
- 用户诉求摘要（可直接引用 v{N}.md 的“背景”段）

## Step 0：同步 AGENTS.md（仅在 Codex 审阅时自动做）
- 通过 git 判断 {CLAUDE_PATH} 是否相对上一次提交发生变化：
  - 若变化：将 {CLAUDE_PATH} 的内容完整复制覆盖到 AGENTS.md
  - 若无变化：不处理
> 目的：让 Codex 默认加载的 AGENTS.md 与 CLAUDE.md 保持一致，仅在审阅时自动同步，节省日常上下文成本。

## Step 1：调用 Codex 进行审阅
- 让 Codex 按“治理层文档清单”逐一检查，并以 @governance-docs-standard 为唯一规范依据。
- 检查重点（不扩展成更多维度）：
  - 问题解决：用户诉求是否被有效覆盖
  - 规则遵守：术语一致/去重引用/边界清晰/CLAUDE 是否被污染

## Step 2：生成 v{N}-review.md（固定格式）
- 复审对象：治理层文档清单
- 评分（0-5）：
  1) 问题解决：扣分点 + 证据位置 + 修复建议（若有）
  2) 规则遵守：扣分点 + 证据位置 + 修复建议（若有）
- 总结：一句话结论 + 最关键的 1-3 个修复建议（若有）

## 证据位置书写约定（建议）
- 统一使用：{文件路径}#章节标题（或按项目约定使用行号范围）
