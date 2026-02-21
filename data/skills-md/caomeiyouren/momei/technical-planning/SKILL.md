---
name: technical-planning
description: 进行技术方案设计、受影响文件寻找与改动风险分析。
version: 1.0.0
author: GitHub Copilot
---

# Technical Planning Skill (技术规划技能)

## 核心能力 (Core Capabilities)

-   **文件寻路**: 准确找到特定逻辑所在的文件位置，避免修改错误的副本。
-   **影响评估**: 识别修改全局 Composable、Store 或 API 时可能波及的页面或组件。
-   **契约定义**: 在动工前定义好 API 的路径、入参和返回结构。
-   **解耦建议**: 建议将紧耦合逻辑拆离，确保护合项目架构准则。

## 指令 (Instructions)

1.  **Worktree 感知**: 识别任务属性，在输出改动清单时，应明确改动应在哪个工作树（如 `../momei-dev`）中执行。
2.  **清单优先**: 在执行任何 `Do` 操作前，必须先输出一份包含“受影响文件”和“改动逻辑点”的清单。
2.  **路径验证**: 确保提及的文件路径在当前工作区真实存在。
3.  **模式沿用**: 优先参考项目中已有的相似实现模式。

## 使用示例 (Usage Example)

输入: "我们要加一个点赞功能。"
输出: "需要修改 `server/database/Post.ts` 添加字段，创建 `server/api/like.post.ts`，并在 `components/article-card.vue` 添加点赞按钮。"
