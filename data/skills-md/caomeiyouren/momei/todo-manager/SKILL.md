---
name: todo-manager
description: 专门负责管理项目路线图 (roadmap.md) 和待办事项 (todo.md)。
version: 1.0.0
author: GitHub Copilot
---

# Todo Manager Skill (待办事项管理技能)

## 核心能力 (Core Capabilities)

-   **状态同步**: 实时更新 `docs/plan/todo.md` 中的任务状态（进行中、已完成）。
-   **任务拆解**: 将复杂需求拆解为 `todo.md` 中的原子化条目。
-   **版本规划**: 根据更改内容更新 `docs/plan/roadmap.md`。
-   **闭环检查**: 在任务完成前，核对所有 TODO 项是否已打勾。

## 指令 (Instructions)

1.  **路径感知**: 规划类操作（`todo.md`, `roadmap.md`）应在项目主根目录（`master` 分支）下执行。
2.  **首尾呼应**: 每个任务开始前必须将对应的 TODO 标记为 `in-progress`；完成后标记为 `completed`。
2.  **严禁遗漏**: 识别代码中的 `// TODO:` 注释，并将其同步到全局待办列表中。
3.  **文档一致**: 确保 `roadmap.md` 与实际开发进度保持同步。

## 使用示例 (Usage Example)

动作: 读取 `todo.md`，找到排名最高且未开始的任务，启动开发流程并将该条目标记为“开发中”。
