---
name: skill-forge-base
description: Skill Forge 基础设施。初始化数据库、运行 Dashboard 服务器、管理学习历史。
---

# Skill Forge Base - 基础设施与运行环境

此 Skill 管理 **Skill Forge** 学习环境。负责初始化系统、提供用户界面（Dashboard、答题、历史记录）以及管理数据库。

## 核心能力

1.  **系统初始化**：自动创建 `~/.skill-forge` 环境。
2.  **Dashboard 服务**：在 `localhost:3457` 运行 Web 界面。
3.  **历史与分析**：追踪学习进度和错题。

详细的架构和数据库 Schema 请参阅 [ARCHITECTURE.md](resources/ARCHITECTURE.md)。

## 使用说明

### 1. 初始化系统
任何操作之前，确保系统已初始化。此操作是幂等的（可重复执行）。

```bash
# 运行服务器时会自动触发初始化
node lib/server.js
```

### 2. 启动 Dashboard
要打开主界面进行答题或查看历史：

```bash
# 启动服务器（后台运行）
node lib/server.js &

# 打开 Dashboard
open "http://localhost:3457/dashboard"
```

### 3. 查看历史
要查看学习历史和生成报告：

1.  打开 Dashboard (`/dashboard`)。
2.  导航到"历史记录"部分。
3.  或通过 API 验证：`curl http://localhost:3457/api/history`

## 依赖
- **Node.js**: >= 14.0.0
- **SQLite3**: 数据存储
- **数据目录**: `~/.skill-forge/` (与 `skill-forge-quiz` 共享)
