---
name: dev-docs
description: 开发文档自动化生成和维护工具。在完成需求开发后自动生成需求文档(PRD)和API接口文档，在代码更新后自动维护CHANGELOG和API CHANGELOG。触发时机：用户说"生成文档"、"写文档"、"更新文档"，或提到PRD、API文档、changelog、需求文档时自动触发。
---

# 开发文档自动化工具

> **多平台支持**: 本文件可作为 Cursor IDE 的 Skill (`~/.cursor/skills/`) 或 Claude Code 的 Skill (`~/.claude/skills/`) 使用。

本技能帮助在开发过程中自动生成和维护项目文档，确保文档与代码保持同步。

## 核心工作流

### 流程 1：新功能开发完成 → 生成文档

当完成一个新功能的开发后，执行以下步骤：

1. **分析代码变更**
   - 识别新增/修改的文件
   - 提取新增的 API 接口
   - 识别数据模型变更

2. **生成需求文档** → `docs/requirements/REQ-{feature_name}.md`

3. **更新 API 文档** → `docs/api/API.md`

4. **更新 CHANGELOG** → `docs/CHANGELOG.md`

5. **更新 API CHANGELOG** → `docs/api/API_CHANGELOG.md`

### 流程 2：代码更新 → 更新文档

当对现有功能进行修改后：

1. **识别变更类型** (Added/Changed/Fixed/Removed)
2. **更新对应的需求文档**
3. **更新 API 文档**（如有接口变更）
4. **追加 CHANGELOG 条目**

---

## 文档模板

### 需求文档模板 (PRD)

文件位置：`docs/requirements/REQ-{feature_name}.md`

```markdown
# {功能名称} - 需求文档

## 文档信息
| 属性 | 值 |
|------|-----|
| 文档编号 | REQ-{编号} |
| 版本 | v1.0 |
| 创建日期 | {YYYY-MM-DD} |
| 最后更新 | {YYYY-MM-DD} |
| 作者 | {作者} |
| 状态 | 草稿/评审中/已批准/已实现 |

---

## 1. 功能概述

### 1.1 简要描述
{一句话描述该功能的核心目的}

### 1.2 关键词
{功能相关的关键术语}

---

## 2. 背景和目标

### 2.1 背景
{为什么需要这个功能？解决什么问题？}

### 2.2 目标
- 目标 1：{具体可衡量的目标}
- 目标 2：{具体可衡量的目标}

### 2.3 非目标
{明确声明此功能不做什么}

---

## 3. 功能需求

### 3.1 用户故事
| 编号 | 角色 | 需求 | 价值 |
|------|------|------|------|
| US-01 | 作为{角色} | 我希望{功能} | 以便{价值} |

### 3.2 功能清单
| 编号 | 功能名称 | 优先级 | 描述 |
|------|----------|--------|------|
| F-01 | {功能名} | P0/P1/P2 | {详细描述} |

### 3.3 业务规则
- BR-01：{业务规则描述}

---

## 4. 非功能需求

### 4.1 性能要求
- 响应时间：{具体指标}
- 吞吐量：{具体指标}

### 4.2 安全要求
- {安全相关要求}

### 4.3 兼容性
- {浏览器/系统兼容性要求}

---

## 5. UI/交互设计

### 5.1 页面布局
{描述或引用设计稿}

### 5.2 交互流程
{用户操作的步骤流程}

### 5.3 状态说明
| 状态 | 显示效果 | 触发条件 |
|------|----------|----------|
| {状态名} | {效果} | {条件} |

---

## 6. 数据模型

### 6.1 新增/修改的数据表
{使用 Mermaid ER 图或表格描述}

### 6.2 数据字段说明
| 字段名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| {字段} | {类型} | 是/否 | {说明} |

---

## 7. 验收标准

### 7.1 功能验收
- [ ] AC-01：{验收条件}
- [ ] AC-02：{验收条件}

### 7.2 测试用例
| 用例编号 | 描述 | 预期结果 |
|----------|------|----------|
| TC-01 | {测试步骤} | {预期结果} |

---

## 8. 时间节点

| 里程碑 | 计划日期 | 实际日期 | 状态 |
|--------|----------|----------|------|
| 需求评审 | {日期} | {日期} | {状态} |
| 开发完成 | {日期} | {日期} | {状态} |
| 测试完成 | {日期} | {日期} | {状态} |
| 上线发布 | {日期} | {日期} | {状态} |

---

## 附录

### A. 相关文档
- [API 文档](../api/API.md)
- [架构文档](../architecture.md)

### B. 变更历史
| 版本 | 日期 | 作者 | 变更说明 |
|------|------|------|----------|
| v1.0 | {日期} | {作者} | 初始版本 |
```

---

### API 文档模板

文件位置：`docs/api/API.md`

```markdown
# {项目名称} API 接口文档

## 文档信息
| 属性 | 值 |
|------|-----|
| 版本 | v{版本号} |
| 最后更新 | {YYYY-MM-DD} |
| 基础URL | {API基础路径} |

---

## 1. 概述

### 1.1 简介
{API 的用途和范围}

### 1.2 基础信息
- **协议**: HTTPS
- **数据格式**: JSON
- **字符编码**: UTF-8

---

## 2. 认证方式

### 2.1 认证类型
{JWT / API Key / OAuth 等}

### 2.2 认证方式
```
Authorization: Bearer {token}
```

### 2.3 获取 Token
{获取认证 Token 的方式}

---

## 3. 接口列表

### 3.1 {模块名称}

#### {接口名称}

| 属性 | 值 |
|------|-----|
| 路径 | `{HTTP方法} {路径}` |
| 认证 | 是/否/可选 |
| 描述 | {接口功能描述} |

**请求参数**

| 参数名 | 位置 | 类型 | 必填 | 描述 |
|--------|------|------|------|------|
| {参数} | path/query/body | {类型} | 是/否 | {描述} |

**请求示例**
```json
{
  "field": "value"
}
```

**响应参数**

| 参数名 | 类型 | 描述 |
|--------|------|------|
| {参数} | {类型} | {描述} |

**响应示例**
```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

---

## 4. 数据模型

### 4.1 {模型名称}

| 字段名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| {字段} | {类型} | 是/否 | {描述} |

---

## 5. 错误码说明

| 错误码 | HTTP状态码 | 描述 | 解决方案 |
|--------|------------|------|----------|
| 0 | 200 | 成功 | - |
| 10001 | 400 | 参数错误 | 检查请求参数 |
| 10002 | 401 | 未授权 | 检查认证信息 |
| 10003 | 403 | 禁止访问 | 检查权限 |
| 10004 | 404 | 资源不存在 | 检查请求路径 |
| 10005 | 500 | 服务器错误 | 联系管理员 |

---

## 6. 调用示例

### 6.1 cURL
```bash
curl -X POST "{base_url}/api/endpoint" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'
```

### 6.2 Python
```python
import requests

response = requests.post(
    "{base_url}/api/endpoint",
    headers={"Authorization": f"Bearer {token}"},
    json={"key": "value"}
)
print(response.json())
```

### 6.3 JavaScript
```javascript
const response = await fetch("{base_url}/api/endpoint", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${token}`,
    "Content-Type": "application/json"
  },
  body: JSON.stringify({ key: "value" })
});
const data = await response.json();
```
```

---

### CHANGELOG 模板

文件位置：`docs/CHANGELOG.md`

遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/) 格式：

```markdown
# Changelog

本文件记录项目的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### Added
- {新增的功能}

### Changed
- {修改的功能}

### Fixed
- {修复的问题}

### Removed
- {移除的功能}

---

## [1.0.0] - {YYYY-MM-DD}

### Added
- 初始版本发布
- {功能1}
- {功能2}

---

[Unreleased]: {repo_url}/compare/v1.0.0...HEAD
[1.0.0]: {repo_url}/releases/tag/v1.0.0
```

---

### API CHANGELOG 模板

文件位置：`docs/api/API_CHANGELOG.md`

```markdown
# API Changelog

本文件记录 API 接口的所有变更。

## [Unreleased]

### 新增接口
- `{METHOD} {path}` - {描述}

### 接口变更
- `{METHOD} {path}` - {变更说明}

### 废弃接口
- `{METHOD} {path}` - 将在 v{版本} 移除，请使用 {替代接口}

### 移除接口
- `{METHOD} {path}` - {原因}

---

## [1.0.0] - {YYYY-MM-DD}

### 新增接口
- `POST /api/xxx` - {描述}
- `GET /api/xxx` - {描述}
```

---

## 执行步骤

### 步骤 1：初始化文档结构

首次使用时，检查并创建文档目录结构：

```
docs/
├── CHANGELOG.md           # 项目变更日志
├── architecture.md        # 架构文档（已存在）
├── api/
│   ├── API.md            # API 接口文档
│   └── API_CHANGELOG.md  # API 变更日志
└── requirements/
    └── REQ-{feature}.md  # 各功能的需求文档
```

### 步骤 2：分析代码变更

1. 检查 git status 获取变更文件列表
2. 分析新增/修改的 API 接口
3. 识别数据模型变更
4. 提取功能名称和描述

### 步骤 3：生成/更新文档

根据变更类型执行相应操作：

| 变更类型 | 操作 |
|----------|------|
| 新功能 | 创建需求文档 + 更新 API 文档 + 追加 CHANGELOG |
| 功能修改 | 更新需求文档 + 更新 API 文档 + 追加 CHANGELOG |
| Bug 修复 | 追加 CHANGELOG (Fixed) |
| 接口变更 | 更新 API 文档 + 追加 API CHANGELOG |

### 步骤 4：验证文档

- 检查 Markdown 格式正确
- 确保链接有效
- 验证版本号一致

---

## 自动化脚本

本技能提供两个自动化脚本，位于 `scripts/` 目录下。

### 脚本 1：analyze_changes.py - 分析 Git 变更

自动分析 Git 变更并生成文档更新建议。

**用法**

```bash
# 分析当前未提交的变更
python scripts/analyze_changes.py

# 分析从指定 commit 到 HEAD 的变更
python scripts/analyze_changes.py --since HEAD~5

# 输出为 JSON 格式
python scripts/analyze_changes.py --json

# 保存到文件
python scripts/analyze_changes.py --output changes_report.txt
```

**输出内容**

- 变更文件列表（Added/Modified/Deleted）
- API 变更检测（识别新增/修改/删除的接口）
- 建议更新的文档列表
- CHANGELOG 条目建议
- API CHANGELOG 条目建议

### 脚本 2：update_docs.py - 更新文档

提供命令行工具来更新各类文档。

**初始化文档目录**

```bash
python scripts/update_docs.py init
```

**更新 CHANGELOG**

```bash
# 添加新功能
python scripts/update_docs.py changelog -t added -m "新增用户认证功能"

# 记录变更
python scripts/update_docs.py changelog -t changed -m "优化PDF解析性能"

# 记录修复
python scripts/update_docs.py changelog -t fixed -m "修复日期格式解析错误"

# 记录移除
python scripts/update_docs.py changelog -t removed -m "移除旧版API支持"
```

**更新 API CHANGELOG**

```bash
# 新增接口
python scripts/update_docs.py api -t add -e "POST /api/users" -d "创建用户"

# 接口变更
python scripts/update_docs.py api -t change -e "GET /api/users" -d "新增分页参数"

# 废弃接口
python scripts/update_docs.py api -t deprecate -e "GET /api/old" -d "将在v2.0移除"

# 移除接口
python scripts/update_docs.py api -t remove -e "DELETE /api/legacy" -d "已废弃"
```

**创建需求文档**

```bash
# 创建新的需求文档
python scripts/update_docs.py req -n "user-auth" -t "用户认证功能" -a "Jem"

# 强制覆盖已存在的文档
python scripts/update_docs.py req -n "user-auth" --force
```

---

## 典型工作流

### 工作流 1：新功能开发

```bash
# 1. 开发完成后，分析代码变更
python scripts/analyze_changes.py

# 2. 创建需求文档
python scripts/update_docs.py req -n "feature-name" -t "功能标题"
# 编辑生成的需求文档，填写详细内容

# 3. 更新 CHANGELOG
python scripts/update_docs.py changelog -t added -m "新增XX功能"

# 4. 如果有新 API，更新 API 文档
python scripts/update_docs.py api -t add -e "POST /api/xxx" -d "接口描述"

# 5. 提交代码和文档
git add .
git commit -m "feat: 新增XX功能"
```

### 工作流 2：Bug 修复

```bash
# 1. 修复完成后，更新 CHANGELOG
python scripts/update_docs.py changelog -t fixed -m "修复XX问题"

# 2. 提交
git add .
git commit -m "fix: 修复XX问题"
```

### 工作流 3：API 变更

```bash
# 1. 更新 API CHANGELOG
python scripts/update_docs.py api -t change -e "GET /api/xxx" -d "变更说明"

# 2. 手动更新 API.md 中的接口详情

# 3. 更新 CHANGELOG
python scripts/update_docs.py changelog -t changed -m "更新XX接口"
```

---

## 最佳实践

1. **及时更新**：每次代码提交前检查是否需要更新文档
2. **版本同步**：CHANGELOG 版本号与 Git Tag 保持一致
3. **清晰描述**：变更说明要具体，避免模糊的描述如"修复bug"
4. **关联引用**：需求文档和 API 文档互相引用
5. **中文注释**：所有文档和代码注释使用中文
6. **先分析后更新**：使用 analyze_changes.py 先分析变更，再使用 update_docs.py 更新
