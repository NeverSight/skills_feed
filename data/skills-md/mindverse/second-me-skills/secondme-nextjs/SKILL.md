---
name: secondme-nextjs
description: 基于配置和需求生成 Next.js 项目，支持 --quick 快速模式跳过 PRD 阶段
user-invocable: true
argument-hint: [--quick]
---

# SecondMe Next.js 项目生成

基于 `/secondme-init` 的配置和 `/secondme-prd` 的需求定义，生成完整的 Next.js 项目。

---

## 前置条件检查

### 1. 检查 state.json

首先检查 `.secondme/state.json` 是否存在：

- **不存在** → 提示：`请先运行 /secondme-init 初始化项目配置`
- **存在** → 继续

### 2. 检查执行模式

检查参数是否包含 `--quick`：

**快速模式 (--quick)**：
- 跳过 stage 检查
- 使用默认 PRD 配置
- 直接开始生成项目

**标准模式**：
- 检查 `stage >= "prd"`
- 如果 `stage == "init"` → 提示：`请先运行 /secondme-prd 定义需求，或使用 /secondme-nextjs --quick 快速生成`
- 如果 `stage >= "prd"` → 继续

---

## 读取配置

从 `.secondme/state.json` 读取：

```javascript
const state = {
  app_name: "secondme-tinder",  // 应用名称
  modules: ["auth", "chat", "profile"],  // 已选模块
  config: {
    client_id: "71658da7-659c-414a-abdf-cb6472037fc2",
    client_secret: "xxx",
    redirect_uri: "http://localhost:3000/api/auth/callback",
    redirect_uris: [...],
    database_url: "postgresql://...",
    allowed_scopes: [...]
  },
  api: {
    base_url: "https://app.mindos.com/gate/lab",
    oauth_url: "https://go.second.me/oauth/",
    token_endpoint: "...",
    access_token_ttl: 7200,
    refresh_token_ttl: 2592000
  },
  docs: {
    quickstart: "https://develop-docs.second.me/zh/docs",
    oauth2: "...",
    api_reference: "...",
    errors: "..."
  },
  prd: {
    summary: "应用概要",
    features: ["功能1", "功能2"],
    design_preference: "简约现代"
  }
}
```

**重要：** 所有 API 端点、文档链接均从 `state.api` 和 `state.docs` 读取，不要硬编码。

---

## 前端设计要求

**重要：** 在构建前端界面时，必须使用 `frontend-design:frontend-design` skill 来生成高质量的 UI 组件。

设计原则：
- **亮色主题**：仅使用亮色/浅色主题，不使用暗色/深色主题
- **简约优雅**：遵循极简设计理念，减少视觉噪音
- **产品特性驱动**：UI 设计应紧密结合要实现的功能特性
- **现代感**：采用当下流行的设计趋势，避免过时的 UI 模式
- **一致性**：保持整体视觉风格统一
- **响应式**：适配各种屏幕尺寸
- **中文界面**：所有用户可见的文字（按钮、提示、标签、说明等）必须使用中文
- **稳定优先**：避免复杂动画效果，仅使用简单的过渡动画（如 hover、fade），确保界面稳定流畅

---

## 项目生成流程

### 1. 初始化 Next.js 项目

在当前目录直接初始化 Next.js 项目：

```bash
npx create-next-app@latest . --typescript --tailwind --app --src-dir --import-alias "@/*" --yes
```

### 2. 安装依赖

```bash
npm install prisma @prisma/client
npx prisma init
```

### 3. 生成 .env.local

从 `state.config` 和 `state.api` 生成环境变量：

```env
# SecondMe OAuth2 配置
SECONDME_CLIENT_ID=[config.client_id]
SECONDME_CLIENT_SECRET=[config.client_secret]
SECONDME_REDIRECT_URI=[config.redirect_uri]

# 数据库
DATABASE_URL=[config.database_url]

# SecondMe API（从 state.api 读取）
SECONDME_API_BASE_URL=[api.base_url]
SECONDME_OAUTH_URL=[api.oauth_url]
SECONDME_TOKEN_ENDPOINT=[api.token_endpoint]
```

### 4. 生成 Prisma Schema

根据已选模块动态生成 `prisma/schema.prisma`。

#### auth 模块（必有）- User 表必须包含的字段

User 表必须包含 Token 相关字段用于存储和刷新用户凭证：

```prisma
model User {
  id                String   @id @default(cuid())
  secondmeUserId    String   @unique @map("secondme_user_id")
  accessToken       String   @map("access_token")
  refreshToken      String   @map("refresh_token")
  tokenExpiresAt    DateTime @map("token_expires_at")
  createdAt         DateTime @default(now()) @map("created_at")
  updatedAt         DateTime @updatedAt @map("updated_at")
  // 其他字段根据模块需求自行添加

  @@map("users")
}
```

#### 其他模块

根据已选模块（profile、chat、note）的实际需求，自行设计相应的数据库表结构和关联关系。

### 5. 生成代码

根据已选模块生成对应代码：

#### auth 模块

| 文件 | 说明 |
|------|------|
| `src/app/api/auth/login/route.ts` | OAuth 登录跳转 |
| `src/app/api/auth/callback/route.ts` | OAuth 回调处理 |
| `src/app/api/auth/logout/route.ts` | 登出处理 |
| `src/lib/auth.ts` | 认证工具函数 |
| `src/components/LoginButton.tsx` | 登录按钮组件 |

#### profile 模块

| 文件 | 说明 |
|------|------|
| `src/app/api/user/info/route.ts` | 获取用户信息 |
| `src/app/api/user/shades/route.ts` | 获取兴趣标签 |
| `src/components/UserProfile.tsx` | 用户资料组件 |

#### chat 模块

| 文件 | 说明 |
|------|------|
| `src/app/api/chat/route.ts` | 流式聊天 API |
| `src/app/api/sessions/route.ts` | 会话列表 API |
| `src/components/ChatWindow.tsx` | 聊天界面组件 |

#### act 模块

| 文件 | 说明 |
|------|------|
| `src/app/api/act/route.ts` | 流式动作判断 API（结构化 JSON 输出） |
| `src/lib/act.ts` | Act API 工具函数（发送 actionControl、解析 SSE JSON 结果） |

#### note 模块

| 文件 | 说明 |
|------|------|
| `src/app/api/note/route.ts` | 添加笔记 API |

### 6. 更新 state.json

```json
{
  "stage": "ready",
  ...
}
```

---

## 技术栈

- **框架：** Next.js 14+ (App Router)
- **语言：** TypeScript
- **样式：** Tailwind CSS
- **数据库 ORM：** Prisma
- **前端设计：** 使用 `frontend-design:frontend-design` skill 生成
- **API 调用：** fetch
- **状态管理：** React hooks
- **运行端口：** 必须使用 3000 端口

---

## 常见问题与注意事项

### CSS @import 顺序问题

**问题：** 在 `globals.css` 中使用 `@import url(...)` 引入 Google Fonts 会导致构建失败。

**错误信息：**
```
@import rules must precede all rules aside from @charset and @layer statements
```

**原因：** Tailwind CSS 的 `@import "tailwindcss"` 展开后生成大量规则，导致后续的 `@import url(...)` 不再是第一个。

**正确做法：**

1. **使用 `<link>` 标签（推荐）：** 在 `layout.tsx` 中引入
   ```tsx
   <head>
     <link rel="preconnect" href="https://fonts.googleapis.com" />
     <link href="https://fonts.googleapis.com/css2?family=..." rel="stylesheet" />
   </head>
   ```

2. **使用 `next/font`（最佳实践）：**
   ```tsx
   import { Noto_Sans_SC } from 'next/font/google'
   const notoSans = Noto_Sans_SC({ subsets: ['latin'], weight: ['400', '500'] })
   ```

### 构建验证

**重要：** 每次完成代码修改后，必须运行以下命令验证构建：

```bash
npm run build
```

特别关注：
- CSS 解析错误
- TypeScript 类型错误
- 导入路径错误

### WebView OAuth 认证问题

**问题：** 在 WebView 环境中（如移动端 App 内嵌页面、微信小程序等），OAuth state 验证可能失败，因为 WebView 与系统浏览器之间的存储不共享。

**解决方案：** 使用宽松的 state 验证，验证失败时记录警告但继续处理登录流程。

```tsx
// 之前：验证失败直接拒绝
if (!isValidState) {
  return NextResponse.redirect('/?error=invalid_state');
}

// 之后：验证失败记录警告，继续处理
if (!isValidState) {
  console.warn('OAuth state 验证失败，可能是跨 WebView 场景');
  // 继续处理，不阻止登录
}
```

**注意：** 这种方式降低了 CSRF 防护，仅建议在可信的 WebView 环境中使用

---

## 输出结果

```
✅ Next.js 项目已生成！

已生成模块: auth, chat, profile
数据库: PostgreSQL

启动步骤:
1. npm install
2. npx prisma db push
3. npm run dev

项目将在 http://localhost:3000 启动
```

---

## API 响应格式

**重要：所有 SecondMe API 响应都遵循统一格式：**

```json
{
  "code": 0,
  "data": { ... }
}
```

> **本地路由与上游 API 的关系：** Next.js 本地路由（如 `/api/secondme/user/shades`）作为代理层，
> 将请求转发到上游 SecondMe API（`{state.api.base_url}/api/secondme/...`），并**透传上游的响应格式**。
> 前端代码调用本地路由即可，无需直接访问上游 API。

**前端代码必须正确提取数据：**

```typescript
// ✅ 正确写法（调用 Next.js 本地路由，响应格式与上游一致）
const response = await fetch('/api/secondme/user/shades');
const result = await response.json();
if (result.code === 0) {
  const shades = result.data.shades;
  shades.map(item => ...)
}
```

---

## 官方文档

从 `state.docs` 读取文档链接：

| 文档 | 配置键 |
|------|--------|
| 快速入门 | `docs.quickstart` |
| OAuth2 指南 | `docs.oauth2` |
| API 参考 | `docs.api_reference` |
| 错误码 | `docs.errors` |
