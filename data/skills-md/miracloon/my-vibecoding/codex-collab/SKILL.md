---
name: codex-collab
description: >
  【WHEN】当用户命令中明确包含"codex协作"、"codex协同"、"与codex合作"等指令时启用；
  【WHEN】当用户要求使用 codex MCP 工具进行代码分析、原型生成、review 等协作开发场景时启用。
  【WHEN NOT】不用于单独的代码实现任务、不用于纯文档编写、不用于不涉及 codex 的常规开发流程。
---

# Codex 协同开发 Skill

## 核心使命

当用户明确要求与 codex 协同时，你必须思考如何与 codex 进行协作，如何调用 Codex MCP 工具作为客观全面分析的保障。

## 协作流程（必须执行的 4 个步骤）

### 1. 需求分析与计划完善
在你对用户需求形成初步分析后，将用户需求、初始思路告知 codex，并要求其完善需求分析和实施计划。

### 2. 代码原型索取
在实施具体编码任务前，必须向 codex 索要代码实现原型。

**关键约束**：
- 要求 codex 仅给出 unified diff patch
- 严禁对代码做任何真实修改（使用 `sandbox="read-only"`）
- 获取原型后，以此为逻辑参考，重写为企业生产级代码
- 确保可读性极高、可维护性极高后，才能实施具体编程修改

### 3. 代码 Review
无论何时，只要完成切实编码行为后，必须立即使用 codex review 代码改动和对应需求完成程度。

### 4. 争辩与完善
- codex 只能给出参考，你必须有自己的思考
- 需要对 codex 的回答提出质疑
- 通过不断争辩以找到通向真理的唯一途径
- 最终使命是达成统一、全面、精准的意见

## Codex MCP 工具调用规范

### 工具参数

**必选参数**：
- `PROMPT` (string): 发送给 codex 的任务指令
- `cd` (Path): codex 执行任务的工作目录根路径

**可选参数**：
- `sandbox` (string): 沙箱策略
  - `"read-only"` (默认): 只读模式，最安全
  - `"workspace-write"`: 允许在工作区写入
  - `"danger-full-access"`: 完全访问权限
- `SESSION_ID` (UUID | null): 用于继续之前的会话以与 codex 进行多轮交互，默认为 `None`（开启新会话）
- `skip_git_repo_check` (boolean): 是否允许在非 Git 仓库中运行，默认 `False`
- `return_all_messages` (boolean): 是否返回所有消息（包括推理、工具调用等），默认 `False`

**返回值**：
```json
// 成功时
{
  "success": true,
  "SESSION_ID": "uuid-string",
  "agent_messages": "agent回复的文本内容",
  "all_messages": []
}

// 失败时
{
  "success": false,
  "error": "错误信息"
}
```

### 使用方式

**开启新对话**：
- 不传 `SESSION_ID` 参数（或传 `None`）
- 工具会返回新的 `SESSION_ID` 用于后续对话

**继续之前的对话**：
- 将之前返回的 `SESSION_ID` 作为参数传入
- 同一会话的上下文会被保留

### 调用规范

**必须遵守**：
- 每次调用 codex 工具时，必须保存返回的 `SESSION_ID`，以便后续继续对话
- `cd` 参数必须指向存在的目录，否则工具会静默失败
- 严禁 codex 对代码进行实际修改，使用 `sandbox="read-only"` 以避免意外
- 要求 codex 仅给出 unified diff patch

**推荐用法**：
- 如需详细追踪 codex 的推理过程和工具调用，设置 `return_all_messages=True`
- 对于精准定位、debug、代码原型快速编写等任务，优先使用 codex 工具

## 注意事项

### 会话管理
- 始终追踪 `SESSION_ID`，避免会话混乱
- 多轮对话时必须传递正确的 `SESSION_ID`

### 工作目录
- 确保 `cd` 参数指向正确且存在的目录
- 路径错误会导致工具静默失败

### 错误处理
- 检查返回值的 `success` 字段
- 处理可能的错误情况

### 协作原则
- codex 提供参考，你必须独立思考
- 通过争辩达成共识，而非盲从
- 最终目标是统一、全面、精准的解决方案
