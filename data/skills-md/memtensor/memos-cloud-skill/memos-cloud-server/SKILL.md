---
name: memos-cloud-server
description: MemOS Cloud Server API skill. Provides the agent with capabilities to add, search, delete messages and add feedback to MemOS cloud memory.
user-invocable: true
metadata: {"openclaw":{"emoji":"☁️","os":["darwin","linux","win32"],"requires":{"bins":["python3"],"env":["MEMOS_API_KEY", "MEMOS_USER_ID"]}}}
---

# MemOS Cloud Server Skill

**ZH-CN:** 本技能允许 Agent 直接调用 MemOS 云平台 API，实现记忆的检索、添加、删除以及反馈功能。
**EN-US:** This skill allows the Agent to interact with MemOS Cloud APIs for memory search, addition, deletion, and feedback.

## ⚠️ 初始化与安全铁律 / Setup & Safety Rules (MUST READ)

**ZH-CN:** 在执行任何 API 操作前，你（Agent）必须确保环境变量已配置：
**EN-US:** Before executing any API operations, you (the Agent) must ensure the following environment variables are configured:

1. **获取凭证 / Obtain Credentials**：
   - 必须配置 `MEMOS_API_KEY`（MemOS云服务的API Key）和 `MEMOS_USER_ID`（当前用户的唯一标识符）。
2. **自动配置 / Auto Configuration**：
   - 如果不存在，提示用户将这些变量存到全局环境变量中（例如配置在 `~/.zshrc` 或 `~/.bashrc` 中）。

## 🛠 核心接口及命令 / Core Commands

可以通过 `memos_cloud.py` 脚本直接执行操作。脚本会自动读取环境变量 `MEMOS_API_KEY`。所有操作的请求和返回都会以 JSON 格式输出。

### 1. 检索记忆 / Search Memory (`/v1/search/memory`)

- **ZH:** 检索与用户查询相关的长期记忆。
- **EN:** Search for long-term memories relevant to the user's query.

**用法 / Usage:**
```bash
python3 skills/memos-cloud-server/memos_cloud.py search <user_id> "<query>" [--conversation-id <id>]
```
**示例 / Example:**
```bash
python3 skills/memos-cloud-server/memos_cloud.py search "$MEMOS_USER_ID" "Python 相关的项目经历"
```

### 2. 添加记忆 / Add Message (`/v1/add/message`)

- **ZH:** 用于储存多轮对话中的高价值内容到云端。
- **EN:** Used to store high-value content from multi-turn conversations to the cloud.
- `conversation_id`: 必填，当前对话的 ID。
- `messages`: 必填，必须是合法的 JSON 字符串，包含 `role` 和 `content` 字段的列表。

**用法 / Usage:**
```bash
python3 skills/memos-cloud-server/memos_cloud.py add_message <user_id> <conversation_id> '<messages_json_string>'
```
**示例 / Example:**
```bash
python3 skills/memos-cloud-server/memos_cloud.py add_message "$MEMOS_USER_ID" "topic-123" '[{"role":"user","content":"我喜欢吃苹果"},{"role":"assistant","content":"好的，我记住了"}]'
```

### 3. 删除记忆 / Delete Memory (`/v1/delete/memory`)

- **ZH:** 删除云端存储的记忆。根据接口规范，必须传入 `memory_ids` 列表。
- **EN:** Delete stored memories on the cloud. According to the API spec, `memory_ids` is strictly required.

**用法 / Usage:**
```bash
# 按记忆ID列表删除 / Delete by Memory IDs (comma-separated)
python3 skills/memos-cloud-server/memos_cloud.py delete "id1,id2,id3"
```

### 4. 添加反馈 / Add Feedback (`/v1/add/feedback`)

- **ZH:** 向云端添加关于某次对话的反馈，用于修正或强化记忆。
- **EN:** Add feedback regarding a conversation to correct or reinforce memory in the cloud.

**用法 / Usage:**
```bash
python3 skills/memos-cloud-server/memos_cloud.py add_feedback <user_id> <conversation_id> "<feedback_content>" [--allow-knowledgebase-ids "kb1,kb2"]
```
**示例 / Example:**
```bash
python3 skills/memos-cloud-server/memos_cloud.py add_feedback "$MEMOS_USER_ID" "topic-123" "刚才的回答不够详细"
```