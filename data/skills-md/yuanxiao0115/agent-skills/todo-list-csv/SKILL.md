---
name: todo-list-csv
description: Use when 需要一个“落盘的 TODO 清单/进度表（CSV）”并与 `update_plan` 严格同步（例如用户要求 checklist/进度跟踪/CSV）。
---

# Todo List CSV

## 目标

在需要修改项目时，用一个位于项目根目录的 CSV 文件把工作拆成可勾选的步骤；在推进过程中持续更新；全部完成后删除该 CSV，避免把临时清单遗留或提交进仓库。

## 触发条件

- 用户明确要求：TODO 清单 / checklist / 进度表 / CSV / “打勾追踪进度”
- 任务步骤较多（例如 ≥4 步）且你希望把进度**落盘**，便于跨会话/交接/回滚审计
- 你希望用脚本把 CSV → `update_plan` 保持“一处修改，两处同步”

## 何时不使用（避免误触发）

- 只有 1–2 步的简单任务（直接 `update_plan` 或不建 plan 即可）
- 纯研究/纯问答任务（优先用 `workflow/planning-with-files` 的 `notes.md`）
- 你不需要持久化清单（CSV 最终会被 `cleanup` 删除，适合“临时但可追踪”的任务）

## 与 `workflow/planning-with-files` 的分工

- `workflow/planning-with-files`：更适合“长任务/研究多/目标易漂移”，用 `task_plan.md`/`notes.md` 做工作记忆
- `workflow/todo-list-csv`：更适合“需要明确 checklist + 状态机 + 审计痕迹”，用 CSV 严格驱动 `update_plan`

## 工作流（CSV + update_plan 双轨同步）

### 0) 启用 update_plan 的条件

- 当任务包含 **≥2 个可独立验收步骤** 时，调用 `update_plan` 建立计划并在执行过程中持续更新。

### 1) 拆解步骤并建立 plan（与 CSV 一一对应）

- 拆成 3–12 条可验收步骤（动词开头，避免过长）。
- 立即调用 `update_plan` 建立初始 plan：第 1 步 `in_progress`，其余 `pending`。
- 保持 plan 的每个 `step` 文案与 CSV 的 `item` **完全一致**（便于同步与审计）。

### 2) 在项目根目录创建 `{任务名} TO DO list.csv`

- 确定“任务名”：优先取自用户请求的短标题；必要时做简化（去掉标点、过长截断）。
- 计算“项目根目录”：优先使用 Git 仓库根目录；非 Git 项目则使用当前工作目录作为根目录。
- 在项目根目录创建文件：`{任务名} TO DO list.csv`。

CSV 表头固定为（首行）：

`id,item,status,done_at,notes`

- `id`：从 1 开始的整数
- `item`：单条待办（与 plan 的 `step` 一致）
- `status`：`TODO` / `IN_PROGRESS` / `DONE`
- `done_at`：完成时间（ISO 8601，未完成留空）
- `notes`：可选备注（文件路径、验证方式、PR/commit 等）

### 3) 状态机与映射（核心约束）

- 仅允许状态流转：`TODO` → `IN_PROGRESS` → `DONE`（避免 `TODO` 直跳 `DONE`）。
- plan 映射：`TODO`→`pending`，`IN_PROGRESS`→`in_progress`，`DONE`→`completed`。
- 任意时刻 **最多 1 行** `IN_PROGRESS`；只要仍有未完成项，尽量保持 **恰好 1 行** `IN_PROGRESS`（与 plan 的唯一 `in_progress` 对齐）。

### 4) 推进时同步（每完成一项就同步一次）

- 完成当前 `IN_PROGRESS` 项后：
  1) 更新 CSV（推荐用脚本 `advance` 自动“完成当前项并启动下一项”）
  2) 从 CSV 生成 plan payload（`plan --normalize`）
  3) 调用 `update_plan` 使 plan 与 CSV 同步

### 5) 中途变更与暂停

- 新增步骤：只做“追加”，避免重排/重编号；同时更新 CSV 与 plan。
- 暂停等待反馈：保留 CSV；plan 当前步骤保持 `in_progress`，或追加“等待反馈”步骤并置为 `in_progress`。

### 6) 收尾与清理

- 确认所有行均为 `DONE`，再删除该 CSV 文件（脚本 `cleanup` 会在未全 DONE 时拒绝删除）。
- 调用 `update_plan` 将所有步骤标记为 `completed`，确保对话内计划闭环。

## 可选自动化脚本

使用 `scripts/todo_csv.py` 自动创建/更新/清理 CSV（优先用于避免手工编辑出错）。

示例命令：

- 创建清单（默认第 1 条为 IN_PROGRESS）：`python3 ~/.codex/skills/workflow/todo-list-csv/scripts/todo_csv.py init --title "修复登录 bug" --item "复现问题" "加回归测试" "修复实现" "运行测试/构建"`
- 计算路径：`python3 ~/.codex/skills/workflow/todo-list-csv/scripts/todo_csv.py path --title "修复登录 bug"`
- 从 CSV 生成 `update_plan` payload（推荐带 `--normalize`）：`python3 ~/.codex/skills/workflow/todo-list-csv/scripts/todo_csv.py plan --file "{csv_path}" --normalize --explanation "同步自 TODO CSV"`
- 启动指定步骤：`python3 ~/.codex/skills/workflow/todo-list-csv/scripts/todo_csv.py start --file "{csv_path}" --id 2`
- 推进一步（完成当前 IN_PROGRESS 并启动下一条 TODO）：`python3 ~/.codex/skills/workflow/todo-list-csv/scripts/todo_csv.py advance --file "{csv_path}" --notes "已通过单测"`
- 查看进度：`python3 ~/.codex/skills/workflow/todo-list-csv/scripts/todo_csv.py status --file "{csv_path}" --verbose`
- 全部完成后清理：`python3 ~/.codex/skills/workflow/todo-list-csv/scripts/todo_csv.py cleanup --file "{csv_path}"`
