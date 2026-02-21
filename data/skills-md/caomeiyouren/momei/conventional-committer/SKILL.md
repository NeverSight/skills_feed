---
name: conventional-committer
description: 暂存更改并生成符合 Conventional Commits 规范的提交消息。
version: 1.0.0
author: GitHub Copilot
tools: ["terminal"]
---

# Conventional Committer Skill (规范提交技能)

## 能力 (Capabilities)

-   **暂存 (Staging)**: 将修改后的文件添加到 git 暂存区。
-   **消息生成**: 创建遵循 `type(scope): description` 格式的提交消息 (例如: `feat(auth): add login page`)。
-   **提交 (Committing)**: 执行 `git commit`。

## 指令 (Instructions)

0.  **Worktree 感知**: 提交前确认当前所在目录（如 `../momei-dev`），确保提交是在正确的分支和上下文中进行的。
1.  **规范对齐**: 在提交前必须确认遵循 [开发规范 - 提交规模与原子化改动](../../../docs/standards/development.md#27-提交规模与原子化改动-commit-scale--atomic-changes)。
2.  **规模校验**: 强制检查本次改动的文件数量。原则上文件数 **不要超过 10 个**；对应的功能点必须单一。
3.  **任务关联**: 每次提交应且仅应关联 [待办事项 (Todo)](../../../docs/plan/todo.md) 中的一个原子条目。
4.  **提交前检查**: 在执行任何 git 提交操作前，确认 `@code-auditor` 已经通过了 `pnpm typecheck`, `pnpm lint` 和必要的**定向测试**。
5.  **验证状态**: 检查 `git status` 查看哪些内容需要暂存。
6.  **生成消息**: 分析更改以确定 `type` (feat, fix, docs, style, refactor, test, perf, build, ci, chore, revert), `scope` (可选, 例如: 组件名, 模块) 和 `description`。消息描述统一使用**中文**。
7.  **提交**: 运行 `git commit -m "..."`。
8.  **验证**: 确保消息符合 `commitlint.config.ts`。

## 使用示例 (Usage Example)

输入: "提交新的用户资料功能。"
动作: `git add .`, 分析变更, 生成消息 `feat(user): 实现带有头像上传功能的用户个人资料页面`, `git commit`。
