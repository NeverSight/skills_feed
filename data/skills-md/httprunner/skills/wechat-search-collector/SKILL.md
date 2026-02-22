---
name: wechat-search-collector
description: 微信视频号搜索与结果遍历的自动化采集流程（Android），支持综合页搜索、个人页搜索等场景。
---

# 微信视频号搜索

## 约定

统一安装与执行目录：`~/.agents/skills/wechat-search-collector/`。执行前先进入该目录：

```bash
cd ~/.agents/skills/wechat-search-collector
```

- 使用 `android-adb` 执行设备操作；使用 `ai-vision` 从截图定位元素（不要用 `dump-ui`）。
- **关键**：所有 UI 操作（如点击、输入）必须使用 `plan-next` 进行规划和执行。严禁先执行 query 再使用返回坐标进行点击，因为存在坐标偏移问题。
- 优先复用 `references/commands.md` 的函数封装（`ADB`/`VISION`/`TASK`/`REPORT`），避免 `cd` 漂移。
- 产物目录：`TASK_ID` 存在则写 `~/.eval/<TASK_ID>/`，否则写 `~/.eval/debug/`（文件名带时间戳）。
- 结果采集与上报：使用 `result-bitable-reporter`；进入微信流程前必须 `collect-start`，结束时必须 `collect-stop` + `report`。

## 前置处理
- 读取设备序列号：使用环境变量 `SerialNumber`（或 `ADB devices` 自行确认）。
- 准备输出目录：`TASK_ID` 必须为数字；创建 `~/.eval/<TASK_ID>/`。
- 启动采集：执行 `REPORT collect-start --task-id <TASK_ID> --db-path ~/.eval/records.sqlite --table capture_results`（见 `references/commands.md`）。
- 可选拉取任务：用 `TASK claim` 从飞书领取任务；按 `Scene` 选择流程（综合页搜索 / 个人页搜索）。

## 共享子流程：滚动结果到触底（每滑动 5 次检测一次）
目标：避免视觉误判，优先用 sqlite `capture_results` 增量判断是否还有新增。

1) 进入某个关键词结果页后，记录基线 `LAST_COUNT`：
   `LAST_COUNT="$(REPORT stat --task-id <TASK_ID>)"`
2) 循环执行直到触底：
   - 滑动 5 次：`ADB -s <SERIAL> swipe 540 1800 540 400 --duration-ms 800`（循环 5 次；每次滑动后随机等待 500~1000ms）
   - 查询当前总行数：`CUR_COUNT="$(REPORT stat --task-id <TASK_ID>)"`
   - 若 `CUR_COUNT == LAST_COUNT` 连续出现 `N` 次（建议 `N=3`），判定触底；否则更新 `LAST_COUNT=CUR_COUNT` 并继续。
3) sqlite 判定不可用时，用 `ai-vision assert` 二值兜底（不确定必须判定为否），见 `references/commands.md`。

## 综合页搜索流程
适用于“在视频号综合页搜索单个或多个关键词并遍历结果”的需求。

### 1. 任务参数校验
- 任务信息必须提供搜索关键词（以逗号拆分为 `KEYWORDS`）

### 2. 启动微信
- 若当前已在微信内，先使用 `android-adb` 的 `back-home` 命令返回手机桌面。
- 回到桌面后再启动微信。

### 3. 进入 发现 -> 视频号
- 通过截图 + ai-vision 定位并点击 `发现` 与 `视频号` 入口。

### 4. 进入搜索界面
- 通过截图 + ai-vision 点击搜索框/放大镜进入搜索页；若被遮挡则先滑动后再定位。

### 5. 依次输入关键词并触发搜索
- 对关键词列表 `KEYWORDS` 逐个执行：清空输入框 -> 输入关键词 -> 触发搜索。
- 若未进入结果页，重试触发直到进入结果页。

### 6. 结果滚动到底并切换下一个关键词
- 每个关键词的结果页都执行“结果滚动到底”的滑动循环。
- 对每个关键词执行“共享子流程：滚动结果到触底（每滑动 5 次检测一次）”。
- 确认触底后：点击搜索框确保输入框激活 -> 清空 -> 输入下一个关键词 -> 触发搜索，直到完成所有关键词的遍历。

### 7. 场景后置处理
- 当综合页搜索任务成功完成后，调用 `piracy-handler`，实现盗版聚类筛查、子任务创建与 webhook 推送计划创建。
- 若综合页搜索流程失败或中断，不调用该编排器。

## 个人页搜索流程
适用于“先进入某账号个人页，再在个人页内检索多个关键词并遍历结果”的需求。

### 1. 任务参数校验
- 任务信息必须提供：账号名称（`ACCOUNT_NAME`）和搜索关键词（以逗号拆分为 `KEYWORDS`）

### 2. 启动微信
- 若当前已在微信内，先使用 `android-adb` 的 `back-home` 命令返回手机桌面。
- 回到桌面后再启动微信。

### 3. 进入 发现 -> 视频号
- 通过截图 + ai-vision 定位并点击 `发现` 与 `视频号` 入口。

### 4. 进入搜索界面
- 通过截图 + ai-vision 点击搜索框/放大镜进入搜索页；若被遮挡则先滑动后再定位。

### 5. 搜索账号并进入个人页
- 输入账号名称 `ACCOUNT_NAME` 并触发搜索
- 进入搜索结果后，若有目标账号则直接点击进入个人页
- 否则可先点击 `账号` Tab，然后在账号列表中点击目标账号进入个人页

### 6. 在个人页依次搜索关键词
- 对关键词列表 `KEYWORDS` 逐个执行：先点击个人页搜索框确保输入框激活 -> 清空 -> 输入关键词 -> 触发搜索 -> 滑动结果到底。
- 每个关键词的结果页都执行“结果滚动到底”的滑动循环。
- 对每个关键词执行“共享子流程：滚动结果到触底（每滑动 5 次检测一次）”。
- 每个关键词搜索前确认仍在该账号个人页；若误退出则重进个人页后继续。

### 7. 场景后置处理
- 个人页任务结束并进入终态（`success/error`）后，若任务存在 `GroupID`，调用 `piracy-handler` 做“是否就绪 + webhook 推送”。

## 任务结束后的收尾逻辑
- 若 `claim` 未获取任务，直接结束不做收尾。
- 所有关键词遍历完成后，使用 `android-adb` 的 `back-home` 命令返回手机桌面
- 无论任务成功、失败或中断，都必须执行以下动作（finally 语义）：
  - 调用 `result-bitable-reporter` 的 `collect-stop` 结束当前设备采集，并打印采集统计。
  - 调用 `result-bitable-reporter` 的 `report`，并带 `--task-id <TASK_ID>`，仅上报当前任务在 `capture_results` 中 `reported in (0,-1)` 的数据到飞书多维表格采集结果表。
- 调用 `feishu-bitable-task-manager` 更新该 `TaskID` 的字段：`Status` -> `success/failed/error`（基于任务执行结果）、`EndAt` ->`now`

## 备注与排障
- 点击不准：重新截图，让 ai-vision 提供更精确坐标（不要改用 `dump-ui`）。务必确认使用了 `plan-next` 而非 `query`。
- 异常流程（弹窗遮挡或步骤卡住）：先识别弹窗并关闭，再继续原步骤。处理命令见 `references/commands.md`。
- 任务超时限制：若单个任务执行时长超过 30 分钟，则终止执行，任务状态更新为 failed。
