---
name: apifox
description: ABC 医疗云 API 文档查询工具。读取和查询 ABC API 的 OpenAPI 规范文档（4209 个接口），支持按模块、路径、方法搜索，自动解析 $ref 引用。使用场景：(1) 查询 API 接口定义 (2) 搜索特定功能接口 (3) 导出接口文档摘要 (4) 查看接口统计信息
---

# Apifox Skill

本 skill 提供 ABC 医疗云 API 文档查询功能，统一通过 `apifox.py` 调用。

## 环境配置

### 必需的环境变量

使用前需要配置 Apifox Access Token：

```bash
# 设置 Apifox Access Token（必需）
export APIFOX_ACCESS_TOKEN="你的 Apifox Access Token"

# 设置项目 ID（可选，默认为 4105462）
export APIFOX_PROJECT_ID="4105462"
```

### 获取 Apifox Access Token

1. 登录 [Apifox](https://apifox.com)
2. 进入账号设置 > API 访问令牌
3. 创建新的访问令牌
4. 复制 Token 并配置到环境变量

### 依赖安装

```bash
# 安装 Python 依赖
pip3 install requests
```

### 工作原理

apifox 直接通过 HTTP 请求调用 Apifox API：

1. **首次使用**：从 Apifox API 获取 OpenAPI 文档
2. **本地缓存**：数据保存到插件目录下的 `cache/` 文件夹
3. **缓存持久**：缓存永久有效，需要手动刷新获取最新文档

### 配置示例

```bash
# 在 ~/.bashrc 或 ~/.zshrc 中添加
export APIFOX_ACCESS_TOKEN="apt_xxxxxxxxxxxxxxx"
export APIFOX_PROJECT_ID="4105462"

# 重新加载配置
source ~/.bashrc  # 或 source ~/.zshrc
```

## 使用方式

```bash
./scripts/apifox <command> [参数]
```

> **说明**：`./scripts/apifox` 是 shell wrapper，会自动检测并使用系统中可用的 Python 解释器（python3 或 python）。

所有命令默认返回 JSON 格式输出。

## API 模块说明

ABC 医疗云 API 文档包含以下模块：

| 模块 | 接口数量 | 说明 |
|------|---------|------|
| api | 2506 | HTTP API 接口 |
| rpc | 1338 | RPC 服务接口 |
| api-weapp | 294 | 小程序 API 接口 |
| api-device | 29 | 设备接口 |
| api-mp | 17 | 公众号接口 |
| api-external | 14 | 外部接口 |

## 命令列表

### 文档管理

| 命令 | 说明 |
|------|------|
| `read_oas` | 读取完整 OpenAPI 规范（约 5MB JSON） |
| `refresh_oas` | 刷新/更新最新文档（显示缓存状态） |
| `cache_status` | 查看缓存状态和版本 |
| `clear_cache` | 清除本地缓存（需要 `--force` 参数） |

### 接口查询

| 命令 | 说明 |
|------|------|
| `list_paths` | 列出接口路径（支持模块和方法过滤） |
| `search_paths` | 搜索接口（关键词匹配） |
| `get_path` | 获取单个接口详情（自动解析 $ref） |
| `list_modules` | 列出所有模块及接口统计 |

### 数据分析

| 命令 | 说明 |
|------|------|
| `stats` | 显示统计信息（接口总数、模块分布） |
| `export_summary` | 导出接口摘要（JSON/Markdown） |

## 使用示例

### 查询接口详情

```bash
# 获取指定接口的完整定义
./scripts/apifox get_path \
    --path "/api/global-auth/login/sms" \
    --method POST

# 获取接口但不解析 $ref（更快）
./scripts/apifox get_path \
    --path "/api/global-auth/login/sms" \
    --method POST \
    --include_refs false
```

### 搜索接口

```bash
# 搜索登录相关接口
./scripts/apifox search_paths --keyword "login"

# 搜索 api 模块中的用户相关接口
./scripts/apifox search_paths --keyword "user" --module api

# 列出所有 POST 接口
./scripts/apifox list_paths --method post --limit 20
```

### 模块查询

```bash
# 列出所有模块及统计
./scripts/apifox list_modules

# 列出小程序接口（前 20 个）
./scripts/apifox list_paths --module api-weapp --limit 20
```

### 统计信息

```bash
# 查看基本统计
./scripts/apifox stats

# 查看详细统计（包含各模块详情）
./scripts/apifox stats --detail
```

### 缓存管理

```bash
# 查看缓存状态
./scripts/apifox cache_status

# 刷新文档（强制从 API 重新获取最新数据）
./scripts/apifox refresh_oas

# 清除缓存
./scripts/apifox clear_cache --force
```

### 导出摘要

```bash
# 导出所有 API 模块接口摘要到 Markdown
./scripts/apifox export_summary --module api --output api_summary.md --format markdown

# 导出为 JSON
./scripts/apifox export_summary --output full_summary.json --format json
```

## 输出格式

所有命令返回 JSON 格式：

```json
{
  "success": true,
  "data": "返回的数据"
}
```

错误时返回：

```json
{
  "success": false,
  "error": "错误信息"
}
```

## Claude 使用方式

当用户需要查询 API 文档时：

1. **理解需求**：确定要查询的接口或模块
2. **构建命令**：根据需求选择合适的命令和参数
3. **执行脚本**：使用 Bash 工具运行
4. **分析结果**：解析返回的接口定义

示例工作流：
```
用户: "查看短信登录接口的定义"

Claude:
1. ./scripts/apifox search_paths --keyword "login sms"
2. 从结果中找到相关接口路径
3. ./scripts/apifox get_path --path "/api/global-auth/login/sms" --method POST
4. 分析返回的请求/响应结构
```

## 性能说明

- **HTTP 请求**：首次使用或手动刷新时，通过 HTTP 请求从 Apifox API 获取
- **本地缓存**：数据缓存到插件目录，后续使用无需网络请求
- **缓存持久**：缓存永久有效，需要手动刷新获取最新文档
- **搜索性能**：基于内存索引，毫秒级响应

## 数据获取流程

### 首次使用

```bash
# 配置环境变量后首次运行
./scripts/apifox stats

# 输出示例：
# 正在从 Apifox 获取项目 4105462 的 OpenAPI 文档...
# API 端点: https://api.apifox.com/v1/projects/4105462/export/openapi
# ✓ 成功获取 OpenAPI 文档
#   接口数量: 4274
```

### 后续使用

```bash
# 从本地缓存加载，秒级响应
./scripts/apifox stats
# 从本地缓存加载 OpenAPI 数据...
```

### 手动刷新

```bash
# 强制从 API 重新获取最新文档
./scripts/apifox refresh_oas

# 输出示例：
# 正在刷新 OpenAPI 文档...
# 正在从 Apifox 获取项目 4105462 的 OpenAPI 文档...
# ✓ 成功获取 OpenAPI 文档
#   接口数量: 4274
```

### 查看缓存状态

```bash
./scripts/apifox cache_status
```

## 文件结构

```
scripts/
├── apifox.py           # 统一入口脚本
├── apifox_client.py    # API 文档客户端
├── cache_manager.py    # 缓存管理器
└── requirements.txt    # Python 依赖

references/
├── openapi-structure.md    # OpenAPI 结构说明
├── common-queries.md       # 常见查询示例
└── api-modules.md          # API 模块分类
```
