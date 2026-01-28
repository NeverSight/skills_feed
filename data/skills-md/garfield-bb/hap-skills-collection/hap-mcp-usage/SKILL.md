---
name: hap-mcp-usage
description: 明道云 HAP MCP 自动化配置技能。当用户提到"配置 MCP"、"HAP MCP"、"MCP 配置"、"添加 MCP"、"MCP 连接"等需求时**立即触发**。支持 9 种 AI 工具的自动化配置，配置完成后自动验证连通性。
license: MIT
---

# HAP MCP 自动化配置技能

本技能帮助用户在 9 种 AI 工具中**自动化配置** HAP MCP 服务器，并验证连通性。

## 🎯 技能触发场景

当用户说以下任何内容时，**立即使用本技能**：
- "配置这个 MCP"
- "添加 MCP 服务器"
- "帮我配置 HAP MCP"
- "设置 MCP 连接"
- 提供了包含 `hap-mcp-` 的配置信息
- 提供了包含 `HAP-Appkey` 和 `HAP-Sign` 的 URL

## 关于 HAP MCP

### 🌐 HAP 产品线说明

HAP 支持多个产品线和私有部署，**MCP URL 的 host 不同**：

| 产品线 | MCP URL 格式 | 说明 |
|--------|-------------|------|
| **明道云 HAP** | `https://api.mingdao.com/mcp?HAP-Appkey=xxx&HAP-Sign=xxx` | 官方 SaaS 服务 |
| **Nocoly HAP** | `https://www.nocoly.com/mcp?HAP-Appkey=xxx&HAP-Sign=xxx` | Nocoly SaaS 服务 |
| **私有部署 HAP** | `https://your-domain.com/mcp?HAP-Appkey=xxx&HAP-Sign=xxx` | ⚠️ **注意：调用 API 时需要在域名后加 `/api`** |

---

### 🔷 MCP 类型说明

HAP 提供两种不同类型的 MCP，**作用和使用场景完全不同**：

### 类型 1: HAP API 文档 MCP

**作用**: 让 AI 读懂 HAP 接口文档（只读，不执行操作）

**配置格式**（官方固定）:
```json
{
  "mcpServers": {
    "应用 API - API 文档": {
      "command": "npx",
      "args": ["-y", "apifox-mcp-server@latest", "--site-id=5442569"]
    }
  }
}
```

**适用场景**:
- 📖 查询 HAP API 文档
- 🛠️ 学习接口结构和参数
- 📝 生成 API 调用代码

### 🔶 类型 2: HAP 应用执行 MCP

**作用**: 让 AI 执行 HAP 应用接口（可操作真实数据）

**配置格式**（应用专属）:
```json
{
  "mcpServers": {
    "hap-mcp-应用名": {
      "url": "https://api.mingdao.com/mcp?HAP-Appkey=xxx&HAP-Sign=xxx"
    }
  }
}
```

**适用场景**:
- 🔍 查询应用真实数据
- ✏️ 创建/修改/删除记录
- 📊 数据统计和分析
- 🔄 执行工作流

---

## 🤖 AI 执行步骤（自动化配置）

当用户提供 MCP 配置时，AI 必须按以下步骤自动化完成配置：

### Step 1: 自动识别当前 AI 工具平台

**AI 必须自动检测**用户当前使用的是哪个 AI 工具（从以下 9 个平台中识别）：

1. **Claude Code** - Anthropic 官方 CLI
2. **TRAE** - 标准化 `.trae/` 目录
3. **Cursor** - 最流行的 AI 编辑器
4. **GitHub Copilot** - GitHub 官方工具
5. **Google Antigravity** - Google 实验工具
6. **OpenCode** - 开源 AI 工具
7. **Windsurf** - Codeium 出品
8. **Gemini CLI** - Google Gemini 命令行
9. **Codex** - OpenAI 编程助手

**自动识别方法**（按优先级）:

**⚠️ 关键原则**: 优先检测用户**当前正在使用**的 IDE,而不是仅检查已安装的 IDE。

#### 优先级 0: 检测当前运行的 IDE 工具（最高优先级）

**方法**: 通过环境变量、进程信息、上下文标识来判断用户当前正在使用的工具。

```bash
# 检测 Cursor（通过环境变量或进程）
if [ "$TERM_PROGRAM" = "cursor" ] || pgrep -x "Cursor" > /dev/null 2>&1; then
  echo "Cursor"
  exit 0
fi

# 检测 Claude Code（通过会话环境）
if [ -n "$CLAUDE_SESSION" ] || [ "$TERM_PROGRAM" = "claude" ]; then
  echo "Claude Code"
  exit 0
fi

# 检测 TRAE（通过环境变量）
if [ -n "$TRAE_SESSION" ] || [ "$TERM_PROGRAM" = "trae" ]; then
  echo "TRAE"
  exit 0
fi

# 检测 Windsurf（通过环境变量或进程）
if [ "$TERM_PROGRAM" = "windsurf" ] || pgrep -x "Windsurf" > /dev/null 2>&1; then
  echo "Windsurf"
  exit 0
fi

# 检测 Antigravity（通过环境变量）
if [ -n "$ANTIGRAVITY_SESSION" ] || [ "$TERM_PROGRAM" = "antigravity" ]; then
  echo "Google Antigravity"
  exit 0
fi

# 检测 Copilot（通过 VSCode 环境）
if [ "$TERM_PROGRAM" = "vscode" ] && pgrep -f "github.copilot" > /dev/null 2>&1; then
  echo "GitHub Copilot"
  exit 0
fi

# 检测 OpenCode
if [ "$TERM_PROGRAM" = "opencode" ] || pgrep -x "OpenCode" > /dev/null 2>&1; then
  echo "OpenCode"
  exit 0
fi

# 检测 Gemini CLI（通过命令行上下文）
if [ -n "$GEMINI_CLI_SESSION" ]; then
  echo "Gemini CLI"
  exit 0
fi

# 检测 Codex（通过命令行上下文）
if [ -n "$CODEX_SESSION" ]; then
  echo "OpenAI Codex"
  exit 0
fi
```

**识别逻辑**:
1. 检查 `$TERM_PROGRAM` 环境变量（许多 IDE 会设置此变量）
2. 检查 IDE 特定的会话环境变量
3. 检查是否有对应的 IDE 进程正在运行
4. 检查项目目录中的 IDE 特定文件（如 `.cursor/`、`.trae/`）

**重要提示**:
- ✅ **如果检测到当前运行的 IDE**,立即使用该平台的全局配置路径
- ✅ 即使其他 IDE 的配置目录存在,也优先使用当前 IDE
- ⚠️ 只有在无法检测当前 IDE 时,才进入下一优先级（检查已安装的 IDE）

#### 优先级 1: 检查已安装的 IDE（仅在优先级 0 失败时使用）

**⚠️ 警告**: 此方法只能检测**已安装**的 IDE,不能确定**当前使用**的 IDE。

```bash
# 检查配置目录是否存在（不推荐作为首选方法）

# Claude Code
[ -d ~/.claude ] && echo "Claude Code (已安装)"

# Cursor
[ -d ~/.cursor ] && echo "Cursor (已安装)"

# TRAE
[ -d ~/.trae ] && echo "TRAE (已安装)"

# Antigravity
[ -d ~/.gemini/antigravity ] && echo "Antigravity (已安装)"

# Windsurf
[ -d ~/.codeium/windsurf ] && echo "Windsurf (已安装)"

# OpenCode
[ -d ~/.config/opencode ] && echo "OpenCode (已安装)"

# Copilot
[ -d ~/.copilot ] && echo "GitHub Copilot (已安装)"

# Gemini CLI
which gemini && echo "Gemini CLI (已安装)"

# Codex
[ -d ~/.codex ] && echo "Codex (已安装)"
```

**使用策略**:
- 如果检测到**多个已安装的 IDE**,按以下优先级选择:
  1. Cursor（最流行）
  2. Claude Code（官方工具）
  3. TRAE（标准化）
  4. 其他平台
- ⚠️ 提示用户可能配置到了非当前使用的 IDE

#### 优先级 2: 检查项目级配置目录

```bash
# 检查当前项目目录
[ -d .cursor ] && echo "Cursor (项目级)"
[ -d .trae ] && echo "TRAE (项目级)"
[ -d .agent ] && echo "Antigravity (项目级)"
[ -d .claude ] && echo "Claude Code (项目级)"
```

#### 优先级 3: 如果所有检测都失败

- 尝试多个平台的配置（按流行度：Cursor → Claude Code → TRAE）
- 如果所有平台都失败，告知用户：
```
⚠️ 无法自动识别您使用的 AI 工具平台

已尝试的检测方法：
1. 检测当前运行的 IDE（环境变量、进程）
2. 检查已安装的 IDE（配置目录）
3. 检查项目级配置

可能原因：
1. 您使用的平台尚未被本技能支持
2. 配置目录不在默认位置
3. 环境变量未正确设置

📋 请手动配置：
[根据用户工具提供手动配置步骤]

💡 反馈建议：
如果您使用的是上述 9 个平台之一但仍无法识别，
请将以下信息反馈给 HAP Skills 开发团队：

- 您使用的工具名称和版本
- $TERM_PROGRAM 环境变量的值（如果有）
- 配置目录位置

反馈地址：
https://github.com/garfield-bb/hap-skills-collection/issues
```

**识别结果示例**:

**示例 1: 成功检测到当前运行的 IDE**
```
✅ 已识别当前使用的平台：Cursor
📁 配置目录：~/.cursor/
📄 配置文件：~/.cursor/mcp.json
🔍 检测方法：环境变量 $TERM_PROGRAM=cursor
```

**示例 2: 检测到多个已安装 IDE,选择最优**
```
✅ 已识别平台：Cursor（优先选择）
📁 配置目录：~/.cursor/
📄 配置文件：~/.cursor/mcp.json
⚠️ 注意：同时检测到 Claude Code、TRAE 已安装
💡 如果您当前使用的不是 Cursor,请手动指定平台
```

**示例 3: 无法确定当前 IDE,使用项目级配置**
```
✅ 已识别平台：Cursor（项目级）
📁 配置目录：.cursor/
📄 配置文件：.cursor/mcp.json
🔍 检测方法：发现项目目录中的 .cursor/ 文件夹
```

### Step 2: 解析 MCP 配置信息

从用户提供的配置中提取：
- **服务器名称**: 如 `hap-mcp-客户管理`
- **URL**: 包含 `HAP-Appkey` 和 `HAP-Sign` 的完整 URL
- **MCP 类型**: 根据配置格式判断是 API 文档 MCP 还是应用执行 MCP

**重要**: 如果服务器名称包含中文，需要为 Codex 平台生成英文名称：
- **原始名称**: `hap-mcp-客户管理` → 保留（用于其他平台）
- **英文名称**: `hap-mcp-customer-management` → 用于 Codex
- **转换规则**: 将中文部分翻译成英文拼音或英文单词，保持 kebab-case 格式

### Step 3: 根据平台自动化配置

根据识别到的平台，执行对应的配置步骤：

#### 🔧 Claude Code

**配置方式**: 命令行
```bash
# 添加 HTTP MCP 服务器
claude mcp add <server-name> --url "<server-url>"

# 示例
claude mcp add hap-mcp-客户管理 --url "https://api.mingdao.com/mcp?HAP-Appkey=xxx&HAP-Sign=xxx"
```

**验证命令**:
```bash
claude mcp list
```

#### 🔧 Cursor

**配置文件**: `.cursor/mcp.json`（项目级，推荐）或 `~/.cursor/mcp.json`（全局）

**自动化步骤**:
1. 检查并创建 `.cursor` 目录（如果不存在）
2. **读取现有配置文件**（如果存在）- **重要：保留所有已有配置**
3. **增量添加或更新** MCP 配置（不删除其他 MCP）
4. 保存到 `.cursor/mcp.json`
5. **启用 MCP 服务器**（确保配置生效）

**配置格式**:
```json
{
  "mcpServers": {
    // 保留用户已有的 MCP 配置
    "existing-mcp-server": {
      "url": "https://example.com/mcp"
    },
    // 新增 HAP MCP 配置
    "hap-mcp-应用名": {
      "url": "https://api.mingdao.com/mcp?HAP-Appkey=xxx&HAP-Sign=xxx"
    }
  }
}
```

**⚠️ 关键原则**:
- ✅ **增量更新**: 只添加或更新指定的 MCP，保留其他所有配置
- ❌ **禁止覆盖**: 不要清空或删除用户已有的 MCP 服务器

**注意**: 不需要 `"type": "http"` 字段（旧格式）

#### 🔧 TRAE

**配置文件**: `.trae/mcp.json`（项目级）或 `~/.trae/mcp.json`（全局）

**自动化步骤**:
1. 检查并创建 `.trae` 目录
2. 读取或创建 `mcp.json`
3. 添加 MCP 配置（格式同 Cursor）
4. 保存文件

#### 🔧 GitHub Copilot

**配置文件**: `~/.copilot/mcp.json`

**自动化步骤**:
1. 检查并创建 `~/.copilot` 目录
2. 读取或创建 `mcp.json`
3. 添加 MCP 配置
4. 保存文件

**配置格式**: 同 Cursor

#### 🔧 Google Antigravity

**配置文件**: `~/.gemini/antigravity/config.json`

**自动化步骤**:
1. 检查并创建 `~/.gemini/antigravity` 目录（如果不存在）
2. **读取现有配置文件**（如果存在）- **重要：保留所有已有配置**
3. **增量添加或更新** MCP 配置（不删除其他 MCP）
4. 保存到 `~/.gemini/antigravity/config.json`
5. **启用 MCP 服务器**（需要重启 Antigravity）

**配置格式** (JSON):
```json
{
  "mcpServers": {
    // 保留用户已有的 MCP 配置
    "existing-mcp-server": {
      "url": "https://example.com/mcp"
    },
    // 新增 HAP MCP 配置
    "hap-mcp-应用名": {
      "url": "https://api.mingdao.com/mcp?HAP-Appkey=xxx&HAP-Sign=xxx"
    }
  }
}
```

**增量更新示例（Bash 脚本）**:
```bash
#!/bin/bash

# 1. 检查并创建配置目录
mkdir -p ~/.gemini/antigravity

# 2. 读取现有配置（如果不存在则创建默认结构）
if [ -f ~/.gemini/antigravity/config.json ]; then
  EXISTING_CONFIG=$(cat ~/.gemini/antigravity/config.json)
else
  EXISTING_CONFIG='{"mcpServers":{}}'
fi

# 3. 使用 jq 增量添加 MCP 配置（保留其他配置）
echo "$EXISTING_CONFIG" | jq --arg name "hap-mcp-客户管理" \
  --arg url "https://api.mingdao.com/mcp?HAP-Appkey=xxx&HAP-Sign=xxx" \
  '.mcpServers[$name] = {"url": $url}' > ~/.gemini/antigravity/config.json.tmp

# 4. 替换配置文件
mv ~/.gemini/antigravity/config.json.tmp ~/.gemini/antigravity/config.json

# 5. 验证配置
cat ~/.gemini/antigravity/config.json | jq '.mcpServers["hap-mcp-客户管理"]'
```

**⚠️ 关键原则**:
- ✅ **增量更新**: 只添加或更新指定的 MCP，保留其他所有配置
- ❌ **禁止覆盖**: 不要清空或删除用户已有的 MCP 服务器
- ✅ **重启工具**: 配置完成后需要重启 Antigravity 使配置生效

#### 🔧 OpenCode

**配置文件**: `~/.config/opencode/mcp.json`

**自动化步骤**:
1. 检查并创建目录
2. 读取或创建配置文件
3. 添加 MCP 配置
4. 保存文件

**配置格式**: 同 Cursor

#### 🔧 Windsurf

**配置文件**: `~/.codeium/windsurf/mcp.json`

**自动化步骤**:
1. 检查并创建目录
2. 读取或创建配置文件
3. 添加 MCP 配置
4. 保存文件

**配置格式**: 同 Cursor

#### 🔧 Gemini CLI

**配置文件**: `~/.gemini/config.json`

**配置方式**: 命令行或配置文件

**命令行方式**:
```bash
gemini mcp add <server-name> --url "<server-url>"
```

**配置文件方式**: 同 Cursor，在 `mcpServers` 中添加

**参考文档**: https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/mcp-server.md

#### 🔧 OpenAI Codex

**配置文件**: `~/.codex/config.toml`

**⚠️ 重要限制**: Codex 的 TOML 格式**不支持中文 key 名称**

**自动化步骤**:
1. **中文名称转换**: 如果服务器名称包含中文，转换为英文
   - 示例: `hap-mcp-客户管理` → `hap-mcp-customer-management`
   - 规则: 中文翻译成英文单词或拼音，使用 kebab-case 格式
2. 读取现有 `config.toml`
3. 添加 MCP 服务器配置（使用英文名称）
4. 保存文件

**配置格式** (TOML):
```toml
# ✅ 正确 - 使用英文名称
[mcp_servers."hap-mcp-customer-management"]
url = "https://api.mingdao.com/mcp?HAP-Appkey=xxx&HAP-Sign=xxx"

# ❌ 错误 - 中文名称不支持
# [mcp_servers."hap-mcp-客户管理"]
# url = "https://api.mingdao.com/mcp?HAP-Appkey=xxx&HAP-Sign=xxx"
```

**名称转换示例**:
- `hap-mcp-客户管理` → `hap-mcp-customer-management`
- `hap-mcp-订单系统` → `hap-mcp-order-system`
- `hap-mcp-人力资源` → `hap-mcp-hr` 或 `hap-mcp-human-resources`
- `hap-mcp-财务管理` → `hap-mcp-finance-management`

### Step 4: 启用并验证 MCP 连通性

**重要**: 配置完成后，必须**启用 MCP 服务器并验证**是否可以正常连接。

#### 4.1 启用 MCP 服务器

**大多数平台**需要重启工具才能使 MCP 配置生效：
- Claude Code: 命令行添加后自动生效
- Cursor / TRAE / Copilot 等: 需要重启工具

**提示用户**:
```
⚠️ 请重启 [工具名称] 使 MCP 配置生效
```

#### 4.2 验证连通性（必须执行）

**⚠️ 关键要求**: 配置完成后，AI **必须自动验证** MCP 是否可以正常连接。

**验证流程**:

1. **等待用户重启工具**（如果需要）
   ```
   ⚠️ 配置已保存，请重启 [工具名称] 使配置生效

   重启完成后，我将自动验证 MCP 连接...
   ```

2. **调用 MCP 工具验证**
   - 尝试调用：`get_app_info`（获取应用信息）
   - 或调用：`get_app_worksheets_list`（获取工作表列表）

3. **检查返回结果**
   - ✅ **成功**：返回应用信息（应用名称、工作表列表等）
     ```
     ✅ MCP 配置成功！已验证连通性

     📋 配置信息：
     - 平台：[平台名称]
     - 服务器名称：[MCP 名称]
     - 配置文件：[配置文件路径]

     ✅ 连通性验证通过：
     - 应用名称：[应用名]
     - 工作表数量：[数量] 个

     💡 现在可以使用 MCP 工具操作数据了！
     ```

   - ❌ **失败**：返回错误信息 → 进入故障诊断流程（见 4.3）

**验证示例代码**:
```javascript
// 尝试调用 MCP 工具
try {
  const result = await mcpClient.call('get_app_info');

  if (result.success) {
    console.log('✅ MCP 连接成功！');
    console.log('应用名称：', result.appName);
    console.log('工作表数量：', result.worksheets.length);
    return { success: true, data: result };
  }
} catch (error) {
  console.error('❌ MCP 连接失败：', error.message);
  return { success: false, error: error };
}
```

#### 4.3 连接失败诊断与兼容性检测

**如果 MCP 连接失败**，AI 必须按以下步骤诊断并向用户报告：

##### 第一步：基础检查

**诊断清单**:
1. **检查工具是否重启**: 大多数平台需要重启才能加载新配置
2. **检查鉴权信息**:
   - `HAP-Appkey` 和 `HAP-Sign` 是否正确
   - URL 是否完整且格式正确
3. **检查应用状态**:
   - 应用是否已启用 MCP 功能
   - 应用是否可以正常访问
4. **检查网络连接**: 确认可以访问 `api.mingdao.com`
5. **检查配置格式**:
   - JSON 格式是否正确（Cursor/TRAE 等）
   - TOML 格式是否正确（Codex）
   - 中文名称是否已转换（Codex）

##### 第二步：平台兼容性检测

**如果基础检查都通过，仍然连接失败**，可能是平台兼容性问题：

**兼容性检测标准**:
- ✅ **已验证兼容**: Claude Code, Cursor, TRAE（这 3 个平台已经过充分测试）
- ⚠️ **理论兼容**: Antigravity, OpenCode, Windsurf, Copilot, Gemini CLI, Codex（配置格式相同，但可能需要额外步骤）
- ❌ **可能不兼容**: 如果所有检查都通过但仍无法连接，该平台可能尚未完全支持

**向用户报告兼容性问题**:
```
❌ MCP 配置已保存，但连通性验证失败

📋 配置信息：
- 平台：[平台名称]
- 配置文件：[配置文件路径]
- 配置格式：已验证正确
- 鉴权信息：已验证正确

⚠️ 可能的原因：

1️⃣ 平台兼容性问题
   → 您使用的 [平台名称] 可能需要额外的配置步骤
   → 当前已验证兼容的平台：Claude Code, Cursor, TRAE

2️⃣ 需要手动启用
   → 某些平台需要在工具设置中手动启用 MCP 服务器
   → 请检查 [平台名称] 的 MCP 设置选项

3️⃣ 平台版本问题
   → 请确保您使用的是最新版本的 [平台名称]
   → MCP 功能可能需要特定版本支持

🔧 建议操作：

1. **手动配置验证**
   → 打开配置文件：[配置文件路径]
   → 确认配置已正确保存
   → 手动检查 [平台名称] 的 MCP 设置

2. **查看平台文档**
   → 访问 [平台名称] 官方文档
   → 查找 MCP Server 配置说明
   → 可能需要额外的启用步骤

3. **反馈给开发团队**（重要！）
   → 您的反馈将帮助我们改进兼容性
   → 请将以下信息反馈到 GitHub:

   ---
   平台：[平台名称]
   版本：[平台版本]
   错误信息：[详细错误]
   配置文件：[配置文件路径]
   MCP 服务器：[MCP 名称]

   反馈地址：
   https://github.com/garfield-bb/hap-skills-collection/issues
   ---

💡 临时解决方案：

如果您急需使用 MCP 功能，建议：
- 尝试在 Claude Code 或 Cursor 中配置（已验证兼容）
- 或按照上述手动配置步骤操作
- 等待开发团队针对 [平台名称] 的兼容性更新
```

##### 第三步：常见错误速查

**常见错误及解决方案**:

| 错误类型 | 可能原因 | 解决方案 |
|---------|---------|---------|
| 鉴权失败 | Appkey/Sign 错误 | 重新从 HAP 获取正确的鉴权信息 |
| 连接超时 | 网络问题 | 检查网络连接，尝试访问 api.mingdao.com |
| MCP 未找到 | 工具未重启 | 重启 AI 工具使配置生效 |
| 配置格式错误 | JSON/TOML 语法错误 | 检查并修正配置文件格式 |
| 中文 key 错误 | Codex 使用了中文名称 | 将服务器名称转换为英文 |
| **平台不兼容** | **平台尚未完全支持 MCP** | **手动配置 + 反馈开发团队** |

**提供给用户的诊断步骤**:
```
❌ MCP 连接失败，请按以下步骤排查：

1. 确认已重启 [工具名称]
   → 大多数工具需要重启才能加载新的 MCP 配置

2. 检查鉴权信息
   → HAP-Appkey: [显示前5位]...
   → HAP-Sign: [显示前5位]...
   → 如果不确定，请重新从 HAP 应用获取

3. 验证配置文件
   → 位置: [配置文件路径]
   → 格式: [JSON/TOML]
   → 打开文件检查是否有语法错误

4. 测试网络连接
   → 尝试访问: https://api.mingdao.com
   → 确认网络可以访问明道云 API

5. 检查应用设置
   → 登录 HAP 应用
   → 确认 MCP 功能已启用
   → 检查 API 权限设置

如果以上步骤都无法解决，请提供错误信息以便进一步诊断。
```

### Step 5: 向用户报告结果（简洁版）

配置完成并验证后，AI 应该**直接告知结果**，不要过度详细。

#### ✅ 成功时（简洁报告）:

```
✅ 已安装好 MCP！连通性验证通过。

📋 基本信息：
- 应用：[应用名称]
- 工作表：[数量] 个

💡 现在可以使用 MCP 工具操作数据了
```

**详细版本**（如果用户需要）:
```
✅ MCP 配置成功！已验证连通性

📋 配置信息：
- 平台：[平台名称]（自动识别）
- 服务器名称：[MCP 名称]
- 配置文件：[配置文件路径]
- 已保留其他 MCP 配置

✅ 连通性验证通过：
- 应用名称：[应用名]
- 工作表数量：[数量] 个

💡 MCP 已启用并可正常使用
```

#### ❌ 失败时（提供诊断和反馈）:

**如果是常见错误**（鉴权、网络等）:
```
❌ MCP 配置已保存，但连接验证失败

错误原因：[错误类型]
[诊断步骤 - 见 Step 4.3]
```

**如果是兼容性问题**:
```
⚠️ MCP 配置已保存，但在您的平台上可能需要手动启用

📋 已完成：
- 配置文件：[路径]
- 配置格式：已验证正确
- 鉴权信息：已验证正确

⚠️ 可能原因：
您使用的 [平台名称] 可能需要额外配置步骤

🔧 建议操作：
1. 检查 [平台名称] 的 MCP 设置
2. 手动启用 MCP 服务器
3. 参考平台官方文档

📞 重要：请反馈此问题
如果您按照上述步骤操作仍无法使用，请将以下信息反馈到：
https://github.com/garfield-bb/hap-skills-collection/issues

反馈信息模板：
---
平台：[平台名称]
版本：[平台版本]
错误：无法连接 MCP
配置文件：[路径]
---

您的反馈将帮助我们改进对 [平台名称] 的支持！
```

---

## 📋 配置文件位置速查表

| 平台 | 项目级配置 | 全局配置 | 格式 |
|------|-----------|---------|------|
| **Claude Code** | - | 命令行配置 | 命令 |
| **Cursor** | `.cursor/mcp.json` | `~/.cursor/mcp.json` | JSON |
| **TRAE** | `.trae/mcp.json` | `~/.trae/mcp.json` | JSON |
| **GitHub Copilot** | - | `~/.copilot/mcp.json` | JSON |
| **Antigravity** | - | `~/.gemini/antigravity/config.json` | JSON |
| **OpenCode** | - | `~/.config/opencode/mcp.json` | JSON |
| **Windsurf** | - | `~/.codeium/windsurf/mcp.json` | JSON |
| **Gemini CLI** | - | `~/.gemini/config.json` | JSON |
| **Codex** | - | `~/.codex/config.toml` | TOML |

**推荐策略**:
- 支持项目级配置的平台（Cursor, TRAE）：优先使用项目级
- 其他平台：使用全局配置

---

## ⚠️ 重要注意事项

### AI 执行原则（核心要求）

#### ✅ 必须做到

1. **🔍 自动识别平台** - 不要询问用户，直接检测当前平台
   - **优先级 0（最高）**: 检测**当前正在运行**的 IDE 工具
     - 检查环境变量（$TERM_PROGRAM 等）
     - 检查 IDE 特定的会话变量
     - 检查是否有对应的进程正在运行
   - **优先级 1**: 检查已安装的 IDE（仅在优先级 0 失败时）
     - 检查配置目录（~/.cursor, ~/.trae, ~/.claude 等）
     - 检查命令行工具（claude, gemini 等）
   - **优先级 2**: 检查项目级配置目录
   - **关键原则**: 优先使用用户**当前正在使用**的 IDE,而不是仅检查已安装的 IDE
   - 如果识别失败，尝试多个平台配置（Cursor → Claude Code → TRAE）

2. **🤖 自动化执行** - 直接完成配置，不要只告诉步骤
   - 读取现有配置
   - 增量添加新配置
   - 保存文件
   - 不需要询问"是否需要我帮您配置"

3. **✅ 必须验证连通性** - 配置后自动调用 MCP 工具验证
   - 调用 `get_app_info` 或 `get_app_worksheets_list`
   - 成功：简洁告知"已安装好"
   - 失败：进入诊断流程

4. **🔧 兼容性检测** - 如果验证失败且基础检查通过
   - 判断可能是平台兼容性问题
   - 提示用户手动配置
   - **重要：告知用户反馈给开发团队**
   - 提供 GitHub Issues 链接

5. **📋 增量更新** - 只添加或更新指定的 MCP，保留用户所有已有配置

6. **🔠 中文转换** - Codex 平台必须将中文服务器名称转换为英文

7. **📝 格式检查** - 确保 JSON/TOML 格式正确

8. **🔄 提示重启** - 提示用户重启工具使配置生效（大多数平台需要）

#### ❌ 不要做

1. **❌ 不要询问用户平台** - 必须自动识别，不要问"您使用的是哪个工具？"

2. **❌ 不要只告诉步骤** - 不要说"您可以这样配置..."，要直接执行

3. **❌ 不要跳过验证** - 配置后必须验证连通性

4. **❌ 不要直接放弃** - 验证失败时提供诊断，检测兼容性问题

5. **❌ 不要覆盖配置** - 禁止清空或删除用户已有的 MCP 服务器（致命错误！）

6. **❌ 不要忘记反馈** - 兼容性问题时，必须引导用户反馈

7. **❌ 不要误判平台** - 即使检测到多个 IDE 已安装,也要优先使用当前运行的 IDE

#### 📊 成功报告（简洁版）

配置成功后，直接说：
```
✅ 已安装好 MCP！连通性验证通过。

应用：[应用名]
工作表：[数量] 个

现在可以使用 MCP 工具操作数据了
```

**不要**说太多技术细节，除非用户主动询问。

#### ⚠️ 失败报告（提供反馈）

如果是兼容性问题：
```
⚠️ 配置已保存，但可能需要手动启用

您使用的 [平台] 可能需要额外配置步骤。

请手动检查 MCP 设置，或反馈此问题：
https://github.com/garfield-bb/hap-skills-collection/issues

您的反馈将帮助我们改进兼容性！
```

### 配置优先级

1. **项目级配置** - 如果平台支持（Cursor, TRAE）
2. **全局配置** - 其他平台或用户明确要求

### 安全提示

- 🔐 提醒用户保护 `HAP-Appkey` 和 `HAP-Sign`
- 🔐 不要将配置文件提交到 Git（建议添加到 `.gitignore`）
- 🔐 定期检查和更新鉴权信息

---

## 📚 配置示例

### 示例 1: Cursor 项目级配置

**用户提供**:
```json
{"hap-mcp-客户管理":{"url":"https://api.mingdao.com/mcp?HAP-Appkey=abc123&HAP-Sign=xyz789"}}
```

**AI 执行**:
1. 创建 `.cursor` 目录（如果不存在）
2. **读取现有 `.cursor/mcp.json` 并保留所有已有配置**
3. **增量添加**新的 HAP MCP 配置:
```json
{
  "mcpServers": {
    // 保留所有已有的 MCP 配置
    "existing-server-1": { "url": "..." },
    "existing-server-2": { "url": "..." },
    // 新增 HAP MCP
    "hap-mcp-客户管理": {
      "url": "https://api.mingdao.com/mcp?HAP-Appkey=abc123&HAP-Sign=xyz789"
    }
  }
}
```
4. 保存文件
5. 提示用户重启 Cursor
6. 等待用户重启后，调用 `get_app_info` 验证连通性
7. 如果失败，提供详细的诊断步骤
8. 报告结果给用户

### 示例 2: Claude Code 命令行配置

**用户提供**: 同上

**AI 执行**:
```bash
claude mcp add hap-mcp-客户管理 --url "https://api.mingdao.com/mcp?HAP-Appkey=abc123&HAP-Sign=xyz789"
```

验证:
```bash
claude mcp list
```

### 示例 3: Codex TOML 配置（中文名称转换）

**用户提供**:
```json
{"hap-mcp-客户管理":{"url":"https://api.mingdao.com/mcp?HAP-Appkey=abc123&HAP-Sign=xyz789"}}
```

**AI 执行**:
1. 识别服务器名称包含中文: `hap-mcp-客户管理`
2. 转换为英文名称: `hap-mcp-customer-management`
3. 编辑 `~/.codex/config.toml`:
```toml
[mcp_servers."hap-mcp-customer-management"]
url = "https://api.mingdao.com/mcp?HAP-Appkey=abc123&HAP-Sign=xyz789"
```
4. 向用户说明名称转换:
```
✅ MCP 配置成功！

📋 配置信息：
- 平台：Codex
- 原始名称：hap-mcp-客户管理
- 转换后名称：hap-mcp-customer-management（Codex 不支持中文 key）
- 配置文件：~/.codex/config.toml

💡 说明：Codex 的 TOML 格式不支持中文 key 名称，已自动转换为英文。
```

---

## 🎯 总结

本技能的核心价值：
1. **自动化** - 用户只需提供配置，AI 自动完成所有步骤
2. **全平台支持** - 支持 9 种主流 AI 工具
3. **增量更新** - 只添加新配置，保留用户所有已有 MCP
4. **启用验证** - 配置后启用并验证连通性，确保可用
5. **失败诊断** - 连接失败时提供详细诊断和解决方案
6. **错误处理** - 清晰的错误信息和用户指导

**关键原则**:
- ✅ 增量更新，不覆盖已有配置
- ✅ 配置后必须启用并验证
- ✅ 失败时提供诊断步骤，不直接放弃
- ✅ Codex 平台自动转换中文名称

**记住**: 用户说"配置 MCP"时，不要问"需要我帮您配置吗？"，而是立即执行配置流程！
