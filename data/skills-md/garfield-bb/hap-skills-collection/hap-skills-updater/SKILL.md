---
name: hap-skills-updater
description: HAP Skills Collection 技能更新和维护技能。当用户提到"更新技能"、"维护技能"、"更新 hap-skills"、"更新 skill"等需求时使用。帮助用户更新和维护 HAP Skills Collection 中的 4 个核心技能。
license: MIT
---

# HAP Skills Collection 技能更新和维护

本技能帮助用户更新和维护 HAP Skills Collection 中的 4 个核心技能。

## 📋 核心技能列表

HAP Skills Collection 包含以下 4 个核心技能（需要从 GitHub 仓库更新）：

1. **hap-v3-api** - HAP V3 API 使用技能 ✅
2. **hap-view-plugin** - HAP 视图插件开发技能 ✅
3. **hap-frontend-project** - HAP 前端项目搭建技能 ⚠️（如果不存在，需要从仓库获取）
4. **hap-mcp-usage** - HAP MCP 使用指南 ✅

**注意**: 某些技能可能尚未在本地创建，更新时会自动从 GitHub 仓库同步。

## 📁 技能目录结构

```
.claude/skills/
├── hap-v3-api/
│   └── SKILL.md
├── hap-view-plugin/
│   └── SKILL.md
├── hap-frontend-project/
│   └── SKILL.md
└── hap-mcp-usage/
    └── SKILL.md
```

## 🔄 更新流程

### 步骤 1: 检查当前技能版本

在更新技能之前，先检查当前技能的状态：

```bash
# 检查技能文件是否存在
ls -la ~/.claude/skills/hap-v3-api/SKILL.md
ls -la ~/.claude/skills/hap-view-plugin/SKILL.md
ls -la ~/.claude/skills/hap-frontend-project/SKILL.md
ls -la ~/.claude/skills/hap-mcp-usage/SKILL.md

# 或者如果是从 GitHub 仓库克隆的
cd /path/to/hap-skills-collection
ls -la .claude/skills/*/SKILL.md
```

### 步骤 1.5: 检查并安装 HAP API 文档 MCP（新增）

**重要**: 在安装/更新技能时，必须检查用户是否已安装 **应用 API - API 文档 MCP**。

#### 检查 MCP 是否已安装

根据用户当前使用的平台检查 MCP 配置文件：

**Claude Code**:
```bash
# 检查是否已配置
claude mcp list | grep "应用 API - API 文档"
```

**Cursor**:
```bash
# 检查配置文件
cat ~/.cursor/mcp.json | grep "应用 API - API 文档"
# 或项目级
cat .cursor/mcp.json | grep "应用 API - API 文档"
```

**TRAE**:
```bash
# 检查配置文件
cat ~/.trae/mcp.json | grep "应用 API - API 文档"
# 或项目级
cat .trae/mcp.json | grep "应用 API - API 文档"
```

**Manus**:
```bash
# 检查配置文件
cat ~/.manus/mcp.json | grep "应用 API - API 文档"
```

**Coze**:
```bash
# 检查配置文件（注意配置文件名为 mcp_config.json）
cat ~/.coze/mcp_config.json | grep "应用 API - API 文档"
```

**其他平台**: 同理检查对应平台的配置文件

#### 如果未安装，自动安装 API 文档 MCP

**MCP 配置信息**:
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

**自动安装步骤**:

1. **识别平台**: 确定用户使用的 AI 工具（Claude Code / Cursor / TRAE / Manus / Coze 等）

2. **读取现有配置**: 增量更新，保留用户已有的 MCP 配置

3. **添加 API 文档 MCP**:
   - **Claude Code**: `claude mcp add "应用 API - API 文档" --command npx --args "-y,apifox-mcp-server@latest,--site-id=5442569"`
   - **Cursor/TRAE/Copilot/Antigravity/OpenCode**: 编辑 `mcp.json` 文件添加配置
   - **Manus**: 编辑 `~/.manus/mcp.json` 文件添加配置（JSON 格式，同 Cursor）
   - **Coze**: 编辑 `~/.coze/mcp_config.json` 文件添加配置（JSON 格式，可能使用不同的配置结构）
   - **Windsurf/Gemini CLI/Codex**: 软链接平台，自动同步 Claude 配置

4. **验证安装**: 检查配置文件是否包含 "应用 API - API 文档"

5. **提示重启**: 告知用户需要重启工具使配置生效

**示例 - Cursor 平台**:
```bash
# 读取现有配置
EXISTING_CONFIG=$(cat ~/.cursor/mcp.json 2>/dev/null || echo '{"mcpServers":{}}')

# 添加 API 文档 MCP（增量更新）
cat > ~/.cursor/mcp.json <<EOF
{
  "mcpServers": {
    $(echo "$EXISTING_CONFIG" | jq -r '.mcpServers | to_entries | map("\"\(.key)\": \(.value|tojson)") | join(",")'),
    "应用 API - API 文档": {
      "command": "npx",
      "args": ["-y", "apifox-mcp-server@latest", "--site-id=5442569"]
    }
  }
}
EOF

# 验证安装
cat ~/.cursor/mcp.json | grep "应用 API - API 文档"
```

**示例 - Manus 平台**:
```bash
# 检查并创建 Manus 配置目录
mkdir -p ~/.manus

# 读取现有配置
EXISTING_CONFIG=$(cat ~/.manus/mcp.json 2>/dev/null || echo '{"mcpServers":{}}')

# 添加 API 文档 MCP（增量更新）
cat > ~/.manus/mcp.json <<EOF
{
  "mcpServers": {
    $(echo "$EXISTING_CONFIG" | jq -r '.mcpServers | to_entries | map("\"\(.key)\": \(.value|tojson)") | join(",")'),
    "应用 API - API 文档": {
      "command": "npx",
      "args": ["-y", "apifox-mcp-server@latest", "--site-id=5442569"]
    }
  }
}
EOF

# 验证安装
cat ~/.manus/mcp.json | grep "应用 API - API 文档"
```

**示例 - Coze 平台**:
```bash
# 检查并创建 Coze 配置目录
mkdir -p ~/.coze

# 读取现有配置
EXISTING_CONFIG=$(cat ~/.coze/mcp_config.json 2>/dev/null || echo '{"mcpServers":{}}')

# 添加 API 文档 MCP（增量更新）
# 注意: Coze 可能使用 mcp_config.json 而不是 mcp.json
cat > ~/.coze/mcp_config.json <<EOF
{
  "mcpServers": {
    $(echo "$EXISTING_CONFIG" | jq -r '.mcpServers | to_entries | map("\"\(.key)\": \(.value|tojson)") | join(",")'),
    "应用 API - API 文档": {
      "command": "npx",
      "args": ["-y", "apifox-mcp-server@latest", "--site-id=5442569"]
    }
  }
}
EOF

# 验证安装
cat ~/.coze/mcp_config.json | grep "应用 API - API 文档"
```

**告知用户**（以 Cursor 为例，其他平台类似）:
```
✅ HAP API 文档 MCP 已安装

📋 配置信息：
- 平台：Cursor / Manus / Coze / [平台名称]
- MCP 名称：应用 API - API 文档
- 配置文件：~/.cursor/mcp.json / ~/.manus/mcp.json / ~/.coze/mcp_config.json
- 已保留其他 MCP 配置

💡 下一步：
- 重启 [工具名称] 使配置生效
- 现在可以使用 MCP 查询 HAP API 文档了

📖 用途说明：
- 让 AI 读懂 HAP 接口文档（只读，不执行操作）
- 查询 API 文档、学习接口结构、生成 API 调用代码
```

### 步骤 2: 更新技能文件

#### 方式一：从 GitHub 仓库更新（推荐）

```bash
# 1. 克隆或更新仓库
git clone https://github.com/garfield-bb/hap-skills-collection.git
# 或如果已存在
cd hap-skills-collection
git pull origin main

# 2. 确保本地技能目录存在
mkdir -p ~/.claude/skills

# 3. 复制所有技能到本地技能目录（包括缺失的技能）
cp -r .claude/skills/hap-v3-api ~/.claude/skills/ 2>/dev/null || echo "hap-v3-api 已存在或不存在"
cp -r .claude/skills/hap-view-plugin ~/.claude/skills/ 2>/dev/null || echo "hap-view-plugin 已存在或不存在"
cp -r .claude/skills/hap-frontend-project ~/.claude/skills/ 2>/dev/null || echo "hap-frontend-project 已存在或不存在"
cp -r .claude/skills/hap-mcp-usage ~/.claude/skills/ 2>/dev/null || echo "hap-mcp-usage 已存在或不存在"

# 4. 验证更新（检查实际存在的技能）
ls -la ~/.claude/skills/hap-*/SKILL.md 2>/dev/null
```

#### 方式二：手动更新单个技能

如果只需要更新某个特定技能：

```bash
# 更新单个技能
cp /path/to/hap-skills-collection/.claude/skills/hap-v3-api/SKILL.md ~/.claude/skills/hap-v3-api/SKILL.md

# 更新所有 4 个技能
for skill in hap-v3-api hap-view-plugin hap-frontend-project hap-mcp-usage; do
  cp /path/to/hap-skills-collection/.claude/skills/$skill/SKILL.md ~/.claude/skills/$skill/SKILL.md
done
```

### 步骤 3: 验证更新

更新后，验证技能是否正确加载：

```bash
# 检查文件大小和修改时间
ls -lh ~/.claude/skills/hap-*/SKILL.md

# 检查文件内容（查看前几行）
head -10 ~/.claude/skills/hap-v3-api/SKILL.md
```

## 📝 更新检查清单

更新技能时，请检查以下内容：

### ✅ 通用检查项

- [ ] 技能文件存在且可读
- [ ] SKILL.md 文件格式正确（包含 frontmatter）
- [ ] 技能名称和描述正确
- [ ] 文件编码为 UTF-8
- [ ] 没有语法错误
- [ ] **HAP API 文档 MCP 已安装（新增）**

### ✅ MCP 配置检查（新增）

- [ ] 检查平台的 MCP 配置文件
- [ ] 确认是否已安装 "应用 API - API 文档"
- [ ] 如果未安装，自动安装 API 文档 MCP
- [ ] 增量更新，保留用户已有的 MCP 配置
- [ ] 提示用户重启工具使配置生效

### ✅ 内容检查项

- [ ] **hap-v3-api**: 
  - [ ] API 使用工作流完整
  - [ ] Filter 筛选器语法正确
  - [ ] 鉴权配置说明清晰
  - [ ] 示例代码可运行

- [ ] **hap-view-plugin**:
  - [ ] 开发流程步骤完整（7步）
  - [ ] 模板选择说明清晰
  - [ ] 字段类型处理正确
  - [ ] API 集成说明完整

- [ ] **hap-frontend-project**:
  - [ ] HAP 后台配置指导完整
  - [ ] 前端项目结构清晰
  - [ ] API 集成最佳实践正确
  - [ ] 数据渲染优化说明

- [ ] **hap-mcp-usage**:
  - [ ] 两种 MCP 类型说明清晰
  - [ ] Cursor 自动化配置流程正确
  - [ ] 配置文件位置准确（~/.cursor/mcp.json）
  - [ ] 密钥提取方法正确

## 🤖 AI 助手更新指南

当用户需要更新技能时，AI 应该：

### 1. 识别更新需求

用户可能说：
- "更新 hap-skills"
- "更新技能"
- "同步最新的 skill"
- "更新 hap-v3-api 技能"

### 2. 执行更新操作

**如果用户有本地仓库：**

```bash
# 检查仓库位置
cd /path/to/hap-skills-collection

# 拉取最新更新
git pull origin main

# 复制技能文件
cp -r .claude/skills/* ~/.claude/skills/

# 验证更新
ls -la ~/.claude/skills/hap-*/SKILL.md

# ⚠️ 重要：检查并安装 HAP API 文档 MCP
# （见步骤 1.5）
```

**如果用户没有本地仓库：**

```bash
# 克隆仓库
git clone https://github.com/garfield-bb/hap-skills-collection.git /tmp/hap-skills-collection

# 确保本地技能目录存在
mkdir -p ~/.claude/skills

# 复制 4 个核心技能文件（只复制存在的）
for skill in hap-v3-api hap-view-plugin hap-frontend-project hap-mcp-usage; do
  if [ -d "/tmp/hap-skills-collection/.claude/skills/$skill" ]; then
    cp -r /tmp/hap-skills-collection/.claude/skills/$skill ~/.claude/skills/
    echo "✅ 已更新 $skill"
  else
    echo "⚠️  $skill 在仓库中不存在，跳过"
  fi
done

# 验证更新（只显示实际存在的技能）
ls -la ~/.claude/skills/hap-*/SKILL.md 2>/dev/null

# ⚠️ 重要：检查并安装 HAP API 文档 MCP
# （见步骤 1.5）
```

**⚠️ 关键提醒**:
- 更新技能后，**必须检查** HAP API 文档 MCP 是否已安装
- 如果未安装，**自动帮用户安装**（见步骤 1.5）
- 安装后提示用户重启工具使配置生效

### 3. 验证更新结果

更新后，AI 应该：
- ✅ 检查所有 4 个技能文件是否存在
- ✅ 验证文件大小是否合理（不应该为 0）
- ✅ 检查文件修改时间是否为最新
- ✅ 读取文件前几行验证格式正确
- ✅ **检查 HAP API 文档 MCP 是否已安装（新增）**
- ✅ **如果未安装，自动安装 API 文档 MCP**

### 4. 告知用户

更新完成后，AI 应该告知用户：
- ✅ 已更新的技能列表（4 个核心技能）
- ✅ 更新来源（GitHub 仓库）
- ✅ 技能文件位置（~/.claude/skills/）
- ✅ **HAP API 文档 MCP 安装状态**（已安装 / 已跳过 / 刚安装）
- ⚠️ 可能需要重启 AI 工具才能生效

**完整的用户反馈示例**:
```
✅ HAP Skills 更新完成！

📋 已更新技能：
1. ✅ hap-v3-api - HAP V3 API 使用技能
2. ✅ hap-view-plugin - HAP 视图插件开发技能
3. ✅ hap-frontend-project - HAP 前端项目搭建技能
4. ✅ hap-mcp-usage - HAP MCP 使用指南

📦 MCP 配置：
✅ 应用 API - API 文档 MCP 已安装
   - 平台：Cursor
   - 配置文件：~/.cursor/mcp.json
   - 用途：让 AI 读懂 HAP 接口文档

💡 下一步：
- 重启 Cursor 使所有配置生效
- 现在可以使用最新的 HAP 技能了

📚 技能位置：
~/.claude/skills/
├── hap-v3-api/
├── hap-view-plugin/
├── hap-frontend-project/
└── hap-mcp-usage/
```

## 🔍 技能文件格式规范

每个技能文件（SKILL.md）应该遵循以下格式：

```markdown
---
name: skill-name
description: 技能描述，说明何时使用此技能
license: MIT
---

# 技能标题

技能正文内容...
```

### Frontmatter 字段说明

- **name**: 技能名称，必须与目录名一致
- **description**: 技能描述，说明使用场景和触发关键词
- **license**: 许可证（通常为 MIT）

## 📊 技能更新记录

记录每次更新的内容：

### 2026-01-14
- ✅ 初始版本，包含 4 个核心技能
- ✅ 建立更新流程和检查清单

## 🛠️ 故障排查

### 问题 1: 技能文件不存在

**症状**: `ls: ~/.claude/skills/hap-xxx/SKILL.md: No such file or directory`

**解决方案**:
```bash
# 创建技能目录
mkdir -p ~/.claude/skills/hap-v3-api
mkdir -p ~/.claude/skills/hap-view-plugin
mkdir -p ~/.claude/skills/hap-frontend-project
mkdir -p ~/.claude/skills/hap-mcp-usage

# 从仓库复制文件
cp /path/to/hap-skills-collection/.claude/skills/*/SKILL.md ~/.claude/skills/*/
```

### 问题 2: 技能文件格式错误

**症状**: AI 无法识别技能

**解决方案**:
1. 检查 frontmatter 格式是否正确
2. 确保文件编码为 UTF-8
3. 检查是否有语法错误

### 问题 3: 更新后技能未生效

**症状**: 更新文件后，AI 仍使用旧版本

**解决方案**:
1. 重启 AI 工具（Claude Code CLI、Cursor 等）
2. 清除缓存（如果工具支持）
3. 验证文件修改时间是否为最新

## 📚 相关资源

- **GitHub 仓库**: https://github.com/garfield-bb/hap-skills-collection
- **技能文档**: 每个技能的 SKILL.md 文件
- **更新日志**: GitHub 仓库的 commit 历史

## 💡 最佳实践

1. **定期更新**: 建议每周或每月更新一次技能
2. **版本控制**: 使用 git 管理技能文件，便于回滚
3. **备份**: 更新前备份现有技能文件
4. **验证**: 更新后验证技能是否正常工作
5. **文档同步**: 更新技能时同步更新 README.md

## 🎯 使用场景

当用户提到以下内容时，使用此技能：

- "更新 hap-skills"
- "同步最新的技能"
- "更新 skill"
- "维护技能"
- "检查技能版本"
- "更新 hap-v3-api"
- "更新视图插件技能"

---

**注意**: 此技能仅用于更新和维护 HAP Skills Collection 中的 4 个核心技能。如果需要添加新技能或修改技能内容，请参考各技能的 SKILL.md 文件。
