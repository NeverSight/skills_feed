---
name: lark-mcp
description: 集成飞书/Feishu 服务，操作多维表格、文档、消息、群组等。当用户提到飞书、Feishu、Lark 或需要操作飞书相关功能时使用。
---

# Lark MCP (飞书集成)

## ⚠️ 必读：前5条关键规则 + 重要经验

**重要经验：使用用户身份创建资源**
```yaml
# ⭐ 关键：使用 useUAT: true 创建用户可访问的资源
useUAT: true   # ✅ 用户身份 - 创建者=当前用户，您可以直接访问
useUAT: false  # ❌ 租户身份 - 创建者=飞书助手，您无法直接访问
```

**经验总结（来自实际测试）：**
1. **Bitable 创建权限问题** - 使用 useUAT: false 创建的 Base，创建者是"飞书助手"，当前用户无法访问
2. **外部邮箱权限限制** - 通过 API 添加外部邮箱权限会失败（错误码 1063001）
3. **解决方案** - 使用 useUAT: true 创建资源，创建者自动获得 full_access 权限
4. **文档权限** - 同样适用，使用用户身份创建文档

**1. 服务器名称必须精确**
```bash
✅ mcp__lark-mcp__tool_name
❌ mcp__lark_mcp__ (错误：下划线)
❌ lark-mcp__ (错误：缺少前缀)
```

**2. 嵌套参数结构**
```yaml
path:           # URL路径参数（必需）
  app_token: ...
  table_id: ...
params:         # URL查询参数（可选）
  user_id_type: "open_id"
data:           # 请求体（可选）
  fields: {...}
useUAT: false   # 默认使用租户token
```

**3. 消息 content 必须是字符串**
```bash
❌ content: {"text": "hello"}
✅ content: '{"text": "hello"}'
```

**4. 过滤条件 value 必须是数组**
```bash
❌ value: "已完成"
✅ value: ["已完成"]
```

**5. ID 类型不能混淆**
```
open_id   - 用户ID（推荐）
chat_id   - 群聊ID
app_token - 表格应用ID
table_id  - 表格ID
record_id - 记录ID
```

## 快速开始

### 示例1：查询多维表格记录

```yaml
工具: mcp__lark-mcp__bitable_v1_appTableRecord_search
path:
  app_token: "your_app_token"  # 需要替换为实际的 Base 应用 ID（从 URL 获取）
  table_id: "your_table_id"    # 需要替换为实际的表格 ID（从 URL 获取）
params:
  page_size: 20
data:
  filter:
    conjunction: "and"
    conditions:
      - field_name: "状态"
        operator: "is"
        value: ["已完成"]
```

### 示例2：发送文本消息到群组

```yaml
工具: mcp__lark-mcp__im_v1_message_create
data:
  receive_id: "oc_xxxxx"  # 需要替换为实际的群组 chat_id
  msg_type: "text"
  content: '{"text": "消息内容"}'
params:
  receive_id_type: "chat_id"
```

### 示例3：搜索文档

```yaml
工具: mcp__lark-mcp__docx_builtin_search
data:
  search_key: "关键词"
  count: 10
useUAT: true
```

## 工具分类

### 多维表格 (Bitable)
- `bitable_v1_app_create` - 创建 Base 应用
- `bitable_v1_appTable_list` - 列出所有表格
- `bitable_v1_appTable_create` - 创建新表格
- `bitable_v1_appTableField_list` - 获取字段列表
- `bitable_v1_appTableRecord_search` - 查询记录
- `bitable_v1_appTableRecord_create` - 创建记录
- `bitable_v1_appTableRecord_update` - 更新记录

详细指南：[reference/bitable.md](reference/bitable.md)

### 消息 (Messages)
- `im_v1_message_create` - 发送消息
- `im_v1_message_list` - 获取聊天历史
- `im_v1_chat_create` - 创建群组
- `im_v1_chat_list` - 获取群组列表
- `im_v1_chatMembers_get` - 获取群成员

详细指南：[reference/messages.md](reference/messages.md)

### 文档 (Documents)
- `docx_builtin_search` - 搜索文档
- `docx_builtin_import` - 导入文档
- `docx_v1_document_rawContent` - 获取文档内容

详细指南：[reference/documents.md](reference/documents.md)

### 群组 (Groups)
- `im_v1_chat_create` - 创建群组
- `im_v1_chatMembers_get` - 获取成员列表
- `im_v1_chat_list` - 获取群组列表

详细指南：[reference/groups.md](reference/groups.md)

### 权限 (Permissions)
- `drive_v1_permissionMember_create` - 添加协作者权限

详细指南：[reference/permissions.md](reference/permissions.md)

### 联系人 (Contacts)
- `contact_v3_user_batchGetId` - 通过邮箱/手机号获取用户ID

### Wiki (知识库)
- `wiki_v1_node_search` - 搜索 Wiki 节点
- `wiki_v2_space_getNode` - 获取节点信息

## 认证说明

### Token 类型
- **useUAT: true** - 用户访问令牌（用户操作）
- **useUAT: false** - 租户访问令牌（后台操作，默认）

### 获取 ID

**从 URL 获取：**
```
https://xxx.feishu.cn/base/appxxxxx?table=tblxxxxx
                         ↑app_token    ↑table_id
```

**获取用户 open_id：**
```yaml
工具: mcp__lark-mcp__contact_v3_user_batchGetId
data:
  emails: ["user@example.com"]  # 需要替换为实际的用户邮箱
params:
  user_id_type: "open_id"
```

### user_id_type 参数
始终使用 `"open_id"`（最通用，推荐）。

可选值：`"open_id"` | `"union_id"` | `"user_id"`

## 核心工作流

### 工作流1：创建多维表格并添加记录（用户可访问版本）

```
任务进度：
- [ ] 步骤1: 创建 Base 应用（⭐ useUAT: true）
- [ ] 步骤2: 创建表格和字段
- [ ] 步骤3: 插入记录
- [ ] 步骤4: 验证数据
```

**步骤1: 创建 Base 应用**
```yaml
工具: mcp__lark-mcp__bitable_v1_app_create
data:
  name: "项目管理"  # 可以修改为您需要的名称
  time_zone: "Asia/Shanghai"
useUAT: true  # ⭐ 重要：使用用户身份，确保您可以直接访问
```

**步骤2: 创建表格和字段**
```yaml
工具: mcp__lark-mcp__bitable_v1_appTable_create
path:
  app_token: "bascnxxxxxx"  # 需要替换为步骤1返回的实际 app_token
data:
  table:
    name: "表格名称"
    default_view_name: "默认视图"
    fields:
      - field_name: "姓名"
        ui_type: "Text"
      - field_name: "年龄"
        ui_type: "Number"
      - field_name: "状态"
        ui_type: "SingleSelect"
        property:
          options:
            - name: "进行中"
            - name: "已完成"
```

**注意：** 创建成功后，响应中会返回 `table_id`，保存它用于下一步。

**步骤3: 插入记录**
```yaml
工具: mcp__lark-mcp__bitable_v1_appTableRecord_create
path:
  app_token: "bascnxxxxxx"  # 需要替换为步骤1返回的实际值
  table_id: "tblxxxxxx"     # 需要替换为步骤2返回的实际值
data:
  fields:
    姓名: "张三"
    年龄: 25
    状态: "进行中"
```

**步骤4: 验证数据**
```yaml
工具: mcp__lark-mcp__bitable_v1_appTableRecord_search
path:
  app_token: "bascnxxxxxx"  # 需要替换为实际的 app_token
  table_id: "tblxxxxxx"     # 需要替换为实际的 table_id
params:
  page_size: 10
```

### 工作流2：查询表格并发送消息

```
任务进度：
- [ ] 步骤1: 查询表格数据
- [ ] 步骤2: 处理查询结果
- [ ] 步骤3: 构造消息
- [ ] 步骤4: 发送到群组
```

**步骤1: 查询数据**
```yaml
工具: mcp__lark-mcp__bitable_v1_appTableRecord_search
path:
  app_token: "bascnxxxxxx"  # 需要替换为实际的 app_token
  table_id: "tblxxxxxx"     # 需要替换为实际的 table_id
params:
  page_size: 10
data:
  filter:
    conjunction: "and"
    conditions:
      - field_name: "状态"
        operator: "is"
        value: ["待处理"]
```

**步骤2: 处理查询结果**

查询成功后，响应中包含 `data.items` 数组，每项包含记录的 `fields`。

```yaml
# 响应结构示例
data:
  items:
    - record_id: "recxxxx"
      fields:
        任务名称: "完成文档"
        状态: "待处理"
```

**步骤3: 构造消息**

根据查询结果构造消息内容：

```yaml
# 示例：构造文本消息
message = "找到 " + items.length + " 个待处理任务：\n"
for each item in items:
  message += "- " + item.fields["任务名称"] + "\n"
```

**步骤4: 发送消息**
```yaml
工具: mcp__lark-mcp__im_v1_message_create
data:
  receive_id: "oc_xxxxx"  # 需要替换为实际的群组 chat_id
  msg_type: "text"
  content: '{"text": "处理结果：..."}'
params:
  receive_id_type: "chat_id"
```

### 工作流3：搜索文档并获取内容

```
任务进度：
- [ ] 步骤1: 搜索文档
- [ ] 步骤2: 获取 document_id
- [ ] 步骤3: 提取文档内容
- [ ] 步骤4: 处理文本
```

**步骤1: 搜索**
```yaml
工具: mcp__lark-mcp__docx_builtin_search
data:
  search_key: "项目报告"
  count: 10
useUAT: true
```

**步骤2: 获取 document_id**

搜索成功后，从响应中提取第一个文档的 `document_id`：

```yaml
# 响应结构示例
data:
  items:
    - document_id: "doxcnxxxxxx"  # ← 保存这个
      title: "项目报告"
      ...
```

**步骤3: 获取内容**
```yaml
工具: mcp__lark-mcp__docx_v1_document_rawContent
path:
  document_id: "doxcnxxxxxx"  # 需要替换为步骤2获取的实际 document_id
params:
  lang: 0
useUAT: true
```

## 常见错误排查

### 错误1: "tool not found"
**原因**: 服务器名称拼写错误
**解决**: 确保使用 `mcp__lark-mcp__` 前缀（注意连字符）

### 错误2: "invalid request"
**原因**: 参数嵌套错误
**解决**: 检查 path/params/data 层级，path 参数通常必需

### 错误3: "field not found"
**原因**: 字段名错误或 ID 类型错误
**解决**:
- 确认 `field_name` 与表格字段名完全一致
- 确认使用正确的 ID 类型（app_token vs table_id）

### 错误4: "permission denied"
**原因**: 权限不足或 token 类型错误
**解决**:
- 检查应用是否有该资源的访问权限
- 用户操作使用 `useUAT: true`
- 后台操作使用 `useUAT: false`

### 错误5: 消息发送失败
**原因**: content 格式错误或 receive_id_type 错误
**解决**:
- content 必须是 JSON 字符串，不是对象
- 发送到群组使用 `receive_id_type: "chat_id"`
- 发送到用户使用 `receive_id_type: "open_id"`

## 参数校验清单

使用前检查：
- [ ] 服务器名称：`mcp__lark-mcp__tool_name`
- [ ] path 参数必需且正确（app_token, table_id, record_id 等）
- [ ] content 是 JSON 字符串（消息相关）
- [ ] value 是数组（过滤条件）
- [ ] 枚举值精确匹配（user_id_type, operator 等）
- [ ] ID 类型正确（open_id vs chat_id vs app_token）
- [ ] useUAT 设置正确（用户 true，后台 false）

## 实践中遇到的问题

### 问题1: 创建的 Base 无法访问

**现象：**
- 使用 `useUAT: false` 创建 Base 应用
- 创建者显示为"飞书助手"
- 当前用户无法直接访问，权限受限

**解决方案：**
```yaml
useUAT: true   # ✅ 用户身份 - 创建者=当前用户，可直接访问
useUAT: false  # ❌ 租户身份 - 需要额外设置权限
```

### 问题2: API 添加权限失败

**现象：**
- 通过 `drive_v1_permissionMember_create` 添加邮箱权限
- 错误码：1063001 (Invalid parameter)
- 无法通过 API 授予外部用户访问权限

**根本原因：**
- 租户身份创建的资源，API 权限添加有限制
- 外部邮箱权限可能不支持通过 API 操作

**最佳实践：**
- 优先使用用户身份（`useUAT: true`）创建资源
- 创建者自动获得 `full_access` 权限
- 避免后续复杂的权限配置

### 问题3: 字段类型不匹配

**现象：**
- Bitable 查询时 "field not found"
- 使用了错误的字段 ID 类型

**解决方案：**
```yaml
# 从 URL 获取正确的 ID（appxxxxx 和 tblxxxxx 是需要替换的占位符）
https://xxx.feishu.cn/base/appxxxxx?table=tblxxxxx
                         ↑app_token    ↑table_id

# 查询前先获取字段列表确认字段名
工具: mcp__lark-mcp__bitable_v1_appTableField_list
```

### 问题4: 群主身份问题

**现象：**
- 使用 `useUAT: true` 创建群组
- 创建者仍显示为应用机器人（app_id）
- 消息发送者 `sender_type` 为 "app"，不是 "user"

**根本原因：**
- `useUAT: true` 只是使用用户权限/令牌操作
- 系统记录的"创建者"始终是应用本身
- 这是飞书 API 的设计机制

**解决方案：**
```yaml
# 必须明确指定 owner_id
工具: mcp__lark-mcp__im_v1_chat_create
data:
  owner_id: "ou_xxxxx"  # 指定用户为群主
  user_id_list: ["ou_xxxxx"]
```

**注意：** 不指定 `owner_id` 时，群主默认为应用机器人。

## 参考文档

- [多维表格操作指南](reference/bitable.md)
- [消息发送指南](reference/messages.md)
- [文档操作指南](reference/documents.md)
- [群组管理指南](reference/groups.md)
- [权限管理指南](reference/permissions.md)
- [Bitable 查询示例](examples/bitable-queries.md)
- [消息格式示例](examples/message-formats.md)
