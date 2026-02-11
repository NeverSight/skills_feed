---
name: secondme
description: 一站式创建 SecondMe 集成项目，依次执行初始化、需求定义、项目生成
user-invocable: true
argument-hint: [--quick]
---

# SecondMe 一站式项目创建

将 `secondme-init` → `secondme-prd` → `secondme-nextjs` 三个步骤合并为一个完整流程。

**工具使用：** 收集用户输入时使用 `AskUserQuestion` 工具。

---

## 参数说明

| 参数 | 说明 |
|------|------|
| (无参数) | 完整流程：初始化 → PRD → 生成项目 |
| `--quick` | 快速流程：初始化 → 跳过 PRD → 生成项目 |

---

## 执行流程

### 环境检查（首次执行前）

**重要提醒：** 当前目录将作为项目根目录，Next.js 项目会直接在此目录中初始化。

1. 显示当前工作目录路径，让用户确认：
   ```
   📂 当前工作目录: /path/to/current/dir

   ⚠️  Next.js 项目将直接在此目录中初始化，请确保你已在一个新建的空文件夹中运行。
   ```

2. 检查当前目录内容（除 `.secondme/`、`.git/`、`CLAUDE.md`、`.claude/` 等配置文件外）：
   - **如果目录为空或仅有配置文件**：继续
   - **如果存在其他文件**：发出警告并使用 `AskUserQuestion` 让用户确认是否继续

---

### 阶段 0：检测当前状态

检查 `.secondme/state.json` 是否存在：

**如果存在**，读取 `stage` 字段判断进度：

| stage | 说明 | 操作 |
|-------|------|------|
| `init` | 已完成初始化 | 询问：从 PRD 阶段继续，还是重新开始？ |
| `prd` | 已完成 PRD | 询问：直接生成项目，还是重新定义 PRD？ |
| `ready` | 项目已生成 | 询问：重新生成项目，还是全部重新开始？ |

**如果不存在**，从阶段 1 开始。

---

### 阶段 1：项目初始化

执行 `secondme-init` 的完整流程：

1. 收集 App Info 或手动输入凭证（如果用户没有凭证，引导前往 https://develop.second.me 注册并创建 App）
2. 解析 Scopes，推断功能模块
3. 收集数据库连接串
4. 确认模块选择
5. 生成 `.secondme/state.json`（包含 `api`、`docs` 配置）
6. 生成 `CLAUDE.md`

**完成标志：** `stage` 设为 `"init"`

---

### 阶段 2：产品需求定义

**如果使用 `--quick` 参数**：跳过此阶段，直接进入阶段 3。

**否则**，执行 `secondme-prd` 的完整流程：

1. 展示已选模块的 API 能力
2. 收集应用目标和目标用户
3. 根据模块针对性提问（chat/profile/note）
4. 收集设计偏好
5. 确认需求摘要
6. 更新 `state.json` 的 `prd` 字段

**完成标志：** `stage` 设为 `"prd"`

---

### 阶段 3：生成 Next.js 项目

执行 `secondme-nextjs` 的完整流程：

1. 读取 `state.json` 中的配置和 PRD
2. 在当前目录初始化 Next.js 项目
3. 安装依赖（Prisma）
4. 生成 `.env.local`（从 `state.api` 读取端点）
5. 生成 Prisma Schema（User 表必含 Token 字段）
6. 根据模块生成代码
7. 使用 `frontend-design:frontend-design` skill 生成 UI

**完成标志：** `stage` 设为 `"ready"`

---

## 快速模式 vs 完整模式

```
完整模式 (/secondme)
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  阶段 1     │ →  │  阶段 2     │ →  │  阶段 3     │
│  初始化     │    │  PRD 定义   │    │  生成项目   │
└─────────────┘    └─────────────┘    └─────────────┘

快速模式 (/secondme --quick)
┌─────────────┐    ┌─────────────┐
│  阶段 1     │ →  │  阶段 3     │
│  初始化     │    │  生成项目   │
└─────────────┘    └─────────────┘
```

---

## 输出结果

流程完成后显示：

```
🎉 SecondMe 项目创建完成！

项目信息：
- 应用名称: [app_name]
- 已选模块: auth, chat, profile
- 数据库: PostgreSQL

启动步骤:
1. npm install
2. npx prisma db push
3. npm run dev

项目将在 http://localhost:3000 启动

提示：
- .secondme/ 目录包含敏感配置，请添加到 .gitignore
- 如需修改配置，可单独运行 /secondme-init
- 如需重新定义需求，可单独运行 /secondme-prd
```

---

## 单独使用子命令

如果只需要执行某个阶段，可以单独使用：

| 命令 | 说明 |
|------|------|
| `/secondme-init` | 仅执行初始化 |
| `/secondme-prd` | 仅执行 PRD 定义 |
| `/secondme-nextjs` | 仅执行项目生成 |
| `/secondme-nextjs --quick` | 跳过 PRD 检查，直接生成 |

---

## 错误恢复

如果流程中断：
- 已完成的阶段数据会保存在 `state.json`
- 重新运行 `/secondme` 会检测进度并询问是否继续
- 可以选择从中断点继续，或重新开始某个阶段

---

## 设计原则提醒

生成的项目遵循以下设计原则：
- **亮色主题**：仅使用浅色主题
- **简约优雅**：极简设计，减少视觉噪音
- **中文界面**：所有用户可见文字使用中文
- **稳定优先**：避免复杂动画，仅用简单过渡效果
