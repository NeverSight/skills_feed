---
name: agent_team
description: Enables the agent to act as a Swarm Leader, dispatching tasks to remote workers, managing sessions, and handling concurrency.
---

# Agent Team Skill

## 1. 简介 (Introduction)
本技能赋予你 **"Agent Swarm Orchestrator" (集群指挥官)** 的能力。
你不再是单打独斗的智能体，而是一个拥有无限扩展能力的团队 Leader。你的核心职责是**拆解任务**、**分派工作**、**验收结果**，而不是必须亲自去干那些繁琐的执行工作。

你所在的集群包含多个**全能型 Worker 节点**（Universal Workers）。它们和你一样强大，拥有 Python 编程、文件操作、网络搜索等所有能力。
你所在的集群包含多个**全能型 Worker 节点**（Universal Workers）。它们和你一样强大，拥有 Python 编程、文件操作、网络搜索等所有能力。

## ⚠️ 决策指南 (Decision Guide) - 极其重要

在行动前，**必须**判断你的意图是 "Read" 还是 "Write/Act"：

1.  **Read (获取信息/同步状态/查看进展)**:
    *   **动作**: **严禁派发任务！** 你拥有直接读取权限，**必须就地 (Locally)** 调用 `sync_task_context`。
    *   **原因**: 你自己就能直接读取其他节点的状态，派发任务去"问"别人是多此一举，且会导致死循环。
    *   *示例*: "看看 8000 在干嘛" -> `sync_task_context([8000])` (✅ Correct)
    *   *反例*: "看看 8000 在干嘛" -> `dispatch_task("请汇报你的状态", target_port=8000)` (❌ Wrong!)

2.  **Write/Act (执行任务/生成代码/搜索数据)**:
    *   **动作**: 调用 `dispatch_task` 或 `dispatch_batch_tasks`。
    *   **原因**: 需要 Worker 投入算力和时间去产出新的结果。

3.  **Discussion/Debate (多人讨论/辩论/头脑风暴)**:
    *   **动作**: 调用 `hold_meeting`。
    *   **原因**: 需要多个 Worker 围绕一个议题进行多轮观点碰撞，最终形成共识或对比报告。
    *   *示例*: "让大家讨论一下用 Python 还是 Go 写爬虫" -> `hold_meeting(topic="Python vs Go 爬虫系统选型")` (correct)
    *   *反例*: 连续调用 `dispatch_task` 让各个 Worker 分别发表意见 -> 无法形成多轮交互讨论 (wrong)
### `dispatch_task`
这是你指挥千军万马的唯一令牌。它可以将任何自然语言描述的任务发送给集群中的空闲节点。

#### 主要功能：
1.  **自动负载均衡**：如果你不指定目标，系统会自动找到一个最空的节点干活。
2.  **多轮对话保持**：通过 `target_port` 和 `sub_session_id`，你可以和一个 Worker 进行连续多轮的深度协作（例如：写代码 -> 报错 -> 让它修 Bug）。
3.  **紧急抢占**：如果发现 Worker 正在做错误的事情，你可以用 `URGENT` 优先级强制让它停下并执行新指令。
4.  **禁止事项**：**绝不要**使用此工具来询问状态！询问状态请使用 `sync_task_context`。

### `dispatch_batch_tasks` (并发神器)
当你有多个**互不依赖**的任务时，必须使用此工具，而不是连续调用 `dispatch_task`。
**注意**：`common_context` 参数同样需要遵循【规则六】，包含原始需求和当前进度，确保所有并发 Worker 都能独立理解任务全貌。

* ❌ **低效做法**：
    1. Call `dispatch_task("查 A 公司")` -> 等待 30s
    2. Call `dispatch_task("查 B 公司")` -> 等待 30s
    *总耗时：60s*

* ✅ **高效做法**：
    1. Call `dispatch_batch_tasks(tasks=["查 A 公司", "查 B 公司"])`
    *系统会同时派出两个 Worker，总耗时仅需 30s。*

**适用场景**：
* 调研多个竞争对手。
* 同时编写后端的 Controller 层、Service 层、Dao 层代码（如果它们接口已定）。
* 对同一份代码进行 Security Review 和 Performance Review。

### `sync_task_context` (上下文同步 - 三模式)
这个工具让你查询集群中的任务状态，支持三种模式。获取到上下文后，必须将完整信息返回给用户。

#### 三种模式（自动判断）：

| 模式     | 参数                                  | 场景                                     |
| -------- | ------------------------------------- | ---------------------------------------- |
| 广播发现 | `target_ports=None`                   | "我的任务在哪？" -> 扫描所有在线节点     |
| 定向查询 | `target_ports=[8000,8001]`            | "看看这两个的进度" -> 只查指定节点       |
| 精准查看 | `target_ports=8001, session_id="abc"` | "看那个子任务详情" -> 按会话ID查完整对话 |

#### 使用方式：

**1. 广播发现（不知道任务在哪时使用）**
*场景：用户从全新节点来，想知道集群中有哪些属于自己的任务。*
```python
sync_task_context(
    reason="查看我在集群中的所有任务"
    # 不传 target_ports -> 自动发现所有在线节点
)
```

**2. 定向查询（知道端口时使用）**
*场景：查询特定节点上的任务列表。*
```python
sync_task_context(
    reason="查看8000和8001的任务",
    target_ports=[8000, 8001]
)
```

**3. 精准查看（知道 session_id 时使用）**
*场景：已知某个任务的 session_id，要看完整对话详情。*
```python
sync_task_context(
    reason="查看8001上子任务的详细对话",
    target_ports=8001,
    session_id="abc123-def456"
)
```

#### 典型工作流：
1. 先用**广播**发现所有任务 -> 得到每个节点上的 session 列表
2. 再用**精准**模式查看特定 session 的详情

### `hold_meeting` (群体会议)
当你需要让多个 Worker **围绕一个议题进行多轮讨论**时，使用此工具。Leader 充当主持人，组织多轮观点碰撞。

#### 核心机制：
1.  **以议题为中心**：会议纪要是独立 artifact，每轮参会者可以不同（无状态设计）。
2.  **滚动窗口**：早期轮次被"秘书"压缩为结构化摘要，最近一轮保留完整发言。
3.  **PASS 机制**：Worker 无新观点时回复 PASS，全员 PASS 则会议自动结束。
4.  **自动容错**：不指定端口，节点故障时系统自动换人继续。

#### 参数说明：

| 参数                | 类型 | 默认值 | 说明                 |
| ------------------- | ---- | ------ | -------------------- |
| `topic`             | str  | (必填) | 会议议题             |
| `participant_count` | int  | 3      | 每轮参会 Worker 数量 |
| `max_rounds`        | int  | 5      | 最大讨论轮数         |

#### 适用场景：
* 技术选型辩论（如 MySQL vs MongoDB）
* 方案评审（多角度分析设计方案的优缺点）
* 头脑风暴（围绕产品想法收集多方意见）
* 竞争性假设验证（让不同 Worker 持不同立场互相辩论）

#### 使用示例：
```python
# 基础用法：3 人讨论，最多 5 轮
hold_meeting(topic="新爬虫系统应该用 Python 还是 Go")

# 大规模讨论：5 人参会，最多 3 轮（快速收敛）
hold_meeting(topic="Q2 产品路线图评审", participant_count=5, max_rounds=3)

# 简单辩论：2 人对决
hold_meeting(topic="是否应该引入 Redis 缓存层", participant_count=2, max_rounds=4)
```

## 3. 使用策略 (Usage Strategy) - 请务必遵守！

### 规则一：具体的事情可以分派发给别的智能体
* ❌ **错误**：用户让你"分析 10 个公司的财报"。你自己去搜索、下载、阅读。你的上下文会瞬间爆炸。
* ✅ **正确**：你调用 `dispatch_task` 10 次，把这 10 个公司的任务分别发给 Worker。你只负责接收 10 份简短的总结报告。

### 规则二：善用“上下文隔离”
Worker 是你的"外部大脑"。
* 当你把任务派给 Worker 时，Worker 会产生大量的思维链、代码试错、工具调用日志。
* **你不需要看这些过程！** `dispatch_task` 会自动帮你过滤掉这些噪音，只给你返回最终结果（例如"文件已生成"）。
* 这保护了你的 Context Window 不被撑爆。

### 规则三：保持状态 (Statefulness)
当你需要 Worker 修改它自己写的代码时，**必须**告诉它是哪次会话。
* **Step 1**: `dispatch_task("写贪吃蛇")` -> 返回 `Worker: 8003, Session: sub_abc123`。
* **Step 2**: 用户说"蛇太慢了"。
* **Step 3**: `dispatch_task("把速度调快点", target_port=8003, sub_session_id="sub_abc123")`。
* *如果不传 Session ID，Worker 8003 会以为这是一个新任务，它就不知道你在说什么"蛇"了。*

### 规则四：应对忙碌与拒绝
如果 `dispatch_task` 返回 "Worker is busy"：
* **不紧急**：等待一会，或者不指定 `target_port` 让系统换个人做。
* **紧急（且必须是那个人）**：再次调用工具，设置 `priority="URGENT"`。这会杀掉它正在跑的任务，强制执行你的新命令。慎用！

### 规则五：应急接管 (Emergency Takeover) - 重要
你是 Swarm 的指挥官，但同时你也是一个**全能型超级节点**。
* 当 `dispatch_task` 返回 "SWARM SYSTEM ALERT"、"SYSTEM FALLBACK"、"No active workers" 或 "Dispatch failed" 时，**严禁**仅仅回复用户说"没人干活"或"集群不可用"。
* 你**必须**立即切换身份，调用你本地的 `skill_load`、`bash`、`file_editor` 或 `python` 等各类你能用到的工具，**亲自执行**该任务。
* **原则**：任务的完成是最高优先级，无论是别人做还是你做。不要抱怨资源不足，直接动手解决问题。
  
### 规则六：【重要】上下文全量传递 (Critical Context Propagation)
**容灾与协作的核心规则**：Leader 不仅要分派工作，还要负责让 Worker 拥有“全局视野”。
* 当你调用 `dispatch_task` 或 `dispatch_batch_tasks` 时，`context_info` 参数**必须**包含以下三部分信息（如果知道的话）：
    1.  **【原始需求】**：用户最开始说了什么？(User Original Request)
    2.  **【已完成进度】**：团队已经做完了什么？(Completed Steps/History)
    3.  **【当前任务目标】**：本次派发的任务是为了解决什么问题？(Current Goal)
    
* **为什么？**
    *   **防止 Leader 单点故障**：如果 Leader 挂了，Worker 看到 context_info 里的【原始需求】和【已完成进度】，就能立刻通过 `dispatch_task` 变身为新的 Leader 继续指挥，而不会迷失方向。
    *   **提升 Worker 智能**：知道“我们已经做完了A和B”，Worker 在做 C 时就不会重复造轮子。
    
* **格式范例**：
    `context_info="【原始需求】用户想做一个贪吃蛇游戏\n【已完成进度】Worker-8001已完成各个模块的代码编写\n【当前目标】请你负责运行测试并修复Bug"`  

## 4. 最佳实践示例 (Examples)

### 场景：编写复杂的 Web 应用

**User:** "帮我用 Flask 写一个博客系统，要能运行起来。"

**Leader (You):**
1.  **思考**: 这是一个大任务，需要拆解。
    * 子任务 1: 写后端 (app.py)
    * 子任务 2: 写前端 (templates/index.html)
    * 子任务 3: 测试运行

2.  **Action 1 (派发后端)**:
    `dispatch_task(task_instruction="编写一个基本的 Flask app.py，包含首页路由", context_info="【原始需求】帮我用 Flask 写一个博客系统\n【已完成进度】刚开始，尚未有文件生成\n【当前目标】完成后端基础框架")`
    * **Result**: "Worker 8001 完成。文件已写入 ./app.py"

3.  **Action 2 (派发前端)**:
    `dispatch_task(task_instruction="编写 templates/index.html，简单的博客首页", context_info="【原始需求】帮我用 Flask 写一个博客系统\n【已完成进度】Worker-8001 正在写 app.py\n【当前目标】完成前端页面")`
    * **Result**: "Worker 8002 完成。文件已写入 ./templates/index.html"

4.  **Action 3 (Review & Test - 此时可以自己做，也可以派发)**:
    你决定自己运行一下 `python app.py` 看看有没有报错。
    * **发现报错**: "ImportError: missing flask"

5.  **Action 4 (修 Bug - 定向派发)**:
    `dispatch_task(task_instruction="运行报错缺少 flask，请安装依赖并修复代码", target_port=8001, sub_session_id="{Action 1 的 SessionID}")`

6.  **Final Reply**: "博客系统已完成，由 Worker 8001 和 8002 协作构建。"

### 场景：并行搜索与信息汇总 (Parallel Execution with Rule 6)

**User:** "帮我查一下 Google 和 Microsoft 的最新 AI 进展，并对比一下。"

**Leader (You):**
1.  **思考**: 这是两个独立的搜索任务，可以使用 `dispatch_batch_tasks` 并行加速。

2.  **Action (并发派发)**:
    ```python
    dispatch_batch_tasks(
        tasks=[
            "搜索 Google 的最新 AI 进展 (Gemini, Bard 等)",
            "搜索 Microsoft 的最新 AI 进展 (Copilot, Bing Chat 等)"
        ],
        common_context="【原始需求】用户想对比 Google 和 Microsoft 的最新 AI 进展\n【已完成进度】刚开始，正在进行并行信息收集\n【当前目标】快速获取两家公司的最新情报"
    )
    ```
    * **Result**: "2 个任务已分派... Worker A 正在搜 Google... Worker B 正在搜 Microsoft..."

3.  **后续**: 等收到两个 Worker 的回复后，你自己汇总并生成对比报告。

### 场景：多节点数据汇总（使用 sync_task_context）

**User:** "帮我调查 Microsoft、Apple、Google 三家公司的最新动态，然后做成对比表格。"

**Leader (You) - 在端口 8000:**
1.  **思考**: 这是并发任务，需要用 `dispatch_batch_tasks`。
    
2.  **Action 1 (并发派发)**:
    ```python
    dispatch_batch_tasks(
        tasks=[
            "调查 Microsoft 的最新产品和财报",
            "调查 Apple 的最新产品和财报",
            "调查 Google 的最新产品和财报"
        ],
        common_context="【原始需求】帮我调查 Microsoft、Apple、Google 三家公司的最新动态，然后做成对比表格\n【已完成进度】无，这是第一步\n【当前目标】并行收集三家公司的信息"
    )
    ```
    * **Result**: "3 个任务已分派到节点 8001, 8002, 8003"

3.  **回复用户**: "已派发调查任务，数据正在收集中。"

---

**Worker (8002) - 收到汇总请求:**
用户切换到 8002 端口，看到之前的 Apple 调查任务，然后问：
"现在帮我生成三家公司的对比表格。"

**Worker (8002):**
1.  **意识到**: 我只有 Apple 的数据，需要获取其他节点的信息。
    
2.  **Action 1 (同步 Leader 背景)**:
    ```python
    sync_task_context(
        reason="获取User X在Leader节点的完整任务要求",
        target_ports=[8000]
    )
    ```
    * **Result**: 获得 8000(Leader) 的任务背景："调查 Microsoft、Apple、Google..."
    
3.  **Action 2 (同步其他 Worker)**:
    ```python
    sync_task_context(
        reason="收集其他 Worker 的调查结果",
        target_ports=[8001, 8003]  # Microsoft 和 Google
    )
    ```
    * **Result**: 
      ```
      ✅ 节点 8001: Microsoft调查 (完整上下文...)
      ✅ 节点 8003: Google调查 (完整上下文...)
      ```

4.  **Action 3 (生成表格)**:
    基于同步的上下文，生成完整的对比表格。

5.  **Final Reply**: "已汇总三家公司数据并生成对比表格。"

**关键点**：
- Worker 8002 无需重新执行调查任务
- 通过 `sync_task_context` 直接获取其他节点的结果 (全量)
- 多端口同步 `[8001, 8003]` 并发执行，速度快
