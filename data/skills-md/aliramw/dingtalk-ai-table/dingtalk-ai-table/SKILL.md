---
name: dingtalk-ai-table
description: 钉钉 AI 表格（多维表）操作技能。使用 mcporter CLI 连接钉钉 MCP server 执行表格创建、数据表管理、字段操作、记录增删改查。需要配置 DINGTALK_MCP_URL 凭证。使用场景：创建 AI 表格、管理数据表结构、批量导入导出数据、自动化库存/项目管理等表格操作任务。
version: 0.3.5
metadata:
  openclaw:
    requires:
      env:
        - DINGTALK_MCP_URL
      bins:
        - mcporter
    primaryEnv: DINGTALK_MCP_URL
    homepage: https://github.com/aliramw/dingtalk-ai-table
---

# 钉钉 AI 表格操作

通过 MCP 协议连接钉钉 AI 表格 API，执行表格和数据操作。

## ⚠️ 安全须知

**安装前请阅读：**

1. **本技能需要外部 CLI 工具** - 需安装 `mcporter` (npm/bun 全局安装)
2. **需要配置认证凭证** - Streamable HTTP URL 包含访问令牌，请妥善保管
3. **脚本审查建议** - `scripts/` 目录包含 Python 辅助脚本，建议先审查再运行
4. **测试环境优先** - 首次使用建议在测试表格中验证，确认无误后再操作生产数据

### 🔒 安全加固措施（v0.3.4+）

脚本已实施以下安全保护：

| 保护措施 | 说明 |
|----------|------|
| **路径沙箱** | `resolve_safe_path()` 防止目录遍历攻击，限制文件访问在 `OPENCLAW_WORKSPACE` 内 |
| **UUID 验证** | 严格验证 dentryUuid 格式，防止无效输入 |
| **文件扩展名白名单** | 仅允许 `.json` / `.csv` 文件 |
| **文件大小限制** | JSON 最大 10MB，CSV 最大 50MB，防止 DoS |
| **字段类型白名单** | 仅允许预定义的字段类型 |
| **命令超时** | mcporter 命令超时限制（60-120 秒） |
| **输入清理** | 自动去除空白、验证空值 |

**配置建议：**
```bash
# 设置工作目录限制（推荐）
export OPENCLAW_WORKSPACE=/Users/marila/.openclaw/workspace
```

## 前置要求

### 安装 mcporter CLI

本技能依赖 `mcporter` 工具。安装前请确认来源可信：

- **官方仓库**: https://github.com/mcporter/mcporter (请验证)
- **npm 包**: `npm install -g mcporter`

```bash
# 使用 npm 安装
npm install -g mcporter

# 或使用 bun 安装
bun install -g mcporter
```

验证安装：
```bash
mcporter --version
```

> **注意**: 全局安装的 CLI 工具具有用户级执行权限，请确保从可信来源安装。

### 配置 MCP Server

**获取 Streamable HTTP URL：**

1. 访问钉钉 MCP 广场：https://mcp.dingtalk.com/#/detail?mcpId=1060&detailType=marketMcpDetail
2. 在页面**右侧**点击“获取 MCP Server 配置”按钮，然后找到 `Streamable HTTP URL`
3. 复制该 URL 并用于下方配置

**方式一：使用 mcporter config（推荐）**

```bash
# 添加钉钉 AI 表格服务器配置（持久化存储）
mcporter config add dingtalk-ai-table --url "<Streamable_HTTP_URL>"
```

**方式二：使用环境变量**

```bash
# 临时设置（当前终端会话有效）
export DINGTALK_MCP_URL="<Streamable_HTTP_URL>"
```

将 `<Streamable_HTTP_URL>` 替换为实际获取的完整 URL。

> **⚠️ 凭证安全**: Streamable HTTP URL 包含访问令牌，等同于密码：
> - 不要提交到版本控制系统
> - 不要分享给他人
> - 推荐使用 `mcporter config` 持久化存储，避免在命令历史中暴露

### 基本命令模式

所有操作通过 `mcporter call dingtalk-ai-table <tool>` 执行：

```bash
# 获取文档根节点
mcporter call dingtalk-ai-table get_root_node_of_my_document --output json

# 创建 AI 表格
mcporter call dingtalk-ai-table create_base_app filename="表格名" target="<rootDentryUuid>" --output json

# 搜索可访问的表格
mcporter call dingtalk-ai-table search_accessible_ai_tables keyword="关键词" --output json
```

## 核心工作流

### 创建表格并初始化

```bash
# 1. 获取根节点
ROOT_UUID=$(mcporter call dingtalk-ai-table get_root_node_of_my_document --output json | jq -r '.rootDentryUuid')

# 2. 创建表格
mcporter call dingtalk-ai-table create_base_app filename="我的表格" target="$ROOT_UUID" --output json

# 3. 记录返回的 dentryUuid 用于后续操作
```

### 数据表操作

```bash
# 创建数据表（可带初始字段）
mcporter call dingtalk-ai-table add_base_table \
  --args '{"dentryUuid":"<表格 UUID>","name":"新数据表","fields":[{"name":"字段 1","type":"text"},{"name":"字段 2","type":"number"}]}' \
  --output json

# 列出所有数据表
mcporter call dingtalk-ai-table list_base_tables dentry-uuid="<表格 UUID>" --output json

# 重命名数据表
mcporter call dingtalk-ai-table update_base_tables \
  --args '{"dentryUuid":"<UUID>","oldSheetIdOrName":"原表名","newName":"新表名"}' \
  --output json

# 删除数据表
mcporter call dingtalk-ai-table delete_base_table \
  --args '{"dentryUuid":"<UUID>","sheetIdOrName":"表名"}' \
  --output json
```

### 字段操作

```bash
# 查看字段列表
mcporter call dingtalk-ai-table list_base_field \
  --args '{"dentryUuid":"<UUID>","sheetIdOrName":"表名"}' \
  --output json

# 添加字段（支持类型：text, number, singleSelect, multipleSelect, date, user, attachment）
mcporter call dingtalk-ai-table add_base_field \
  --args '{"dentryUuid":"<UUID>","sheetIdOrName":"表名","addField":{"name":"字段名","type":"text"}}' \
  --output json

# 删除字段
mcporter call dingtalk-ai-table delete_base_field \
  --args '{"dentryUuid":"<UUID>","sheetIdOrName":"表名","fieldIdOrName":"字段名"}' \
  --output json
```

### 记录操作

```bash
# 查询记录
mcporter call dingtalk-ai-table search_base_record \
  --args '{"dentryUuid":"<UUID>","sheetIdOrName":"表名"}' \
  --output json

# 添加记录
mcporter call dingtalk-ai-table add_base_record \
  --args '{"dentryUuid":"<UUID>","sheetIdOrName":"表名","records":[{"fields":{"字段 1":"值 1","字段 2":100}}]}' \
  --output json

# 更新记录
mcporter call dingtalk-ai-table update_records \
  --args '{"dentryUuid":"<UUID>","sheetIdOrName":"表名","records":[{"id":"记录 ID","fields":{"字段":"新值"}}]}' \
  --output json

# 删除记录
mcporter call dingtalk-ai-table delete_base_record \
  --args '{"dentryUuid":"<UUID>","sheetIdOrName":"表名","recordIds":["记录 ID1","记录 ID2"]}' \
  --output json
```

## 支持的字段类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `text` | 文本 | `{"name":"姓名","type":"text"}` |
| `number` | 数字 | `{"name":"数量","type":"number"}` |
| `singleSelect` | 单选 | `{"name":"状态","type":"singleSelect"}` |
| `multipleSelect` | 多选 | `{"name":"标签","type":"multipleSelect"}` |
| `date` | 日期 | `{"name":"日期","type":"date"}` |
| `user` | 人员 | `{"name":"负责人","type":"user"}` |
| `attachment` | 附件 | `{"name":"文件","type":"attachment"}` |

## 使用脚本

对于批量操作，使用 `scripts/` 目录中的工具脚本：

```bash
# 批量添加字段
python scripts/bulk_add_fields.py <dentryUuid> <sheetName> fields.json

# 批量导入记录（支持 CSV 和 JSON）
python scripts/import_records.py <dentryUuid> <sheetName> data.csv
python scripts/import_records.py <dentryUuid> <sheetName> data.json [batch_size]
```

> **🔒 脚本安全特性**:
> - ✅ 路径沙箱：防止目录遍历攻击（`../etc/passwd` 等）
> - ✅ UUID 格式验证：严格校验输入格式
> - ✅ 文件扩展名白名单：仅允许 `.json` / `.csv`
> - ✅ 文件大小限制：JSON 10MB / CSV 50MB
> - ✅ 字段类型白名单：防止无效类型注入
> - ✅ 命令超时保护：60-120 秒自动终止
>
> **测试验证**: 运行 `python3 tests/test_security.py` 执行 25 项安全测试
>
> **⚠️ 注意事项**: 
> - 脚本仅调用 `mcporter` 命令和处理本地文件，无网络请求
> - 首次运行前建议审查脚本源码
> - 处理敏感数据时请在受控环境中执行

## 参考文档

- **API 详情**: 见 [references/api-reference.md](references/api-reference.md)
- **错误码说明**: 见 [references/error-codes.md](references/error-codes.md)

## 注意事项

1. **dentryUuid 识别**: 创建表格后返回多个 ID，使用 `uuid` 字段作为 `dentryUuid` 参数
2. **表名匹配**: 默认创建的表名为"数据表"，操作前需确认实际表名
3. **字段值格式**: 单选/多选字段返回对象格式 `{"name":"选项","id":"xxx"}`
4. **日期格式**: 日期字段使用 Unix 时间戳（毫秒）或 `YYYY-MM-DD` 格式
5. **批量操作**: 添加/删除记录支持批量，单次最多 1000 条
