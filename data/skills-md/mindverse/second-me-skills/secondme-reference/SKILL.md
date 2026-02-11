---
name: secondme-reference
description: SecondMe API 技术参考文档，供开发时查阅
user-invocable: true
---

# SecondMe API 技术参考

本文档包含 SecondMe API 的完整技术参考信息，供开发时查阅。

---

## API 基础 URL

```
https://app.mindos.com/gate/lab
```

---

## OAuth2 授权 URL

```
https://go.second.me/oauth/
```

---

## OAuth2 流程

```
1. 用户点击登录 → 跳转到 SecondMe 授权页面
2. 用户授权 → 重定向回你的应用（带 authorization_code）
3. 后端用 code 换取 access_token 和 refresh_token
4. 使用 access_token 调用 SecondMe API
5. Token 过期时使用 refresh_token 刷新
```

---

## Token 有效期

| Token 类型 | 前缀 | 有效期 |
|-----------|------|--------|
| 授权码 | `lba_ac_` | 5 分钟 |
| Access Token | `lba_at_` | 2 小时 |
| Refresh Token | `lba_rt_` | 30 天 |

---

## 权限列表（Scopes）

| 权限 | 说明 |
|------|------|
| `user.info` | 用户基础信息 |
| `user.info.shades` | 用户兴趣标签 |
| `user.info.softmemory` | 用户软记忆 |
| `note.add` | 添加笔记 |
| `chat` | 聊天功能 |
| `chat` | 结构化动作判断（Act） |

---

## API 响应格式与处理

**重要：所有 SecondMe API 响应都遵循统一格式：**

```json
{
  "code": 0,
  "data": { ... }  // 实际数据在 data 字段内
}
```

**前端代码必须正确提取数据：**

```typescript
// 注意：以下 /api/secondme/... 是 Next.js 本地路由（由 secondme-nextjs skill 生成），
// 本地路由会代理请求到上游 SecondMe API，并透传上游的响应格式。

// ❌ 错误写法 - 直接使用响应会导致 .map is not a function
const response = await fetch('/api/secondme/user/shades');  // Next.js 本地路由
const shades = await response.json();
shades.map(item => ...)  // 错误！

// ✅ 正确写法 - 提取 data 字段内的数据
const response = await fetch('/api/secondme/user/shades');  // Next.js 本地路由
const result = await response.json();
if (result.code === 0) {
  const shades = result.data.shades;  // 正确！
  shades.map(item => ...)
}
```

---

## 各 API 的数据路径

> 以下路径均为上游 SecondMe API 路径，完整 URL = `{base_url}/api/secondme{path}`
> 其中 `base_url` 来自 `state.api.base_url`（默认 `https://app.mindos.com/gate/lab`）

| 上游 API 路径 | 数据路径 | 类型 |
|--------------|---------|------|
| `/api/secondme/user/info` | `result.data` | object（含 email, name, avatarUrl, route 等字段） |
| `/api/secondme/user/shades` | `result.data.shades` | array |
| `/api/secondme/user/softmemory` | `result.data.list` | array |
| `/api/secondme/chat/session/list` | `result.data.sessions` | array |
| `/api/secondme/chat/session/messages` | `result.data.messages` | array |
| `/api/secondme/act/stream` | SSE 流式 JSON（需拼接 delta） | SSE stream |
| `/api/secondme/note/add` | `result.data.noteId` | number |

---

## Act API（结构化动作判断）

Act API 是独立于 Chat API 的接口，约束模型仅输出合法 JSON 对象，适用于情感分析、意图分类等结构化决策场景。权限使用 `chat` scope。

### 端点（上游 API）

```
POST {base_url}/api/secondme/act/stream
```

### 请求参数

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| message | string | 是 | 用户消息内容 |
| actionControl | string | 是 | 动作控制说明（20-8000 字符），定义 JSON 结构与判断规则 |
| appId | string | 否 | 应用 ID |
| sessionId | string | 否 | 会话 ID，不提供则自动生成 |
| systemPrompt | string | 否 | 系统提示词，仅新会话首次有效 |

### actionControl 示例

```
仅输出合法 JSON 对象，不要解释。
输出结构：{"is_liked": boolean}。
当用户明确表达喜欢或支持时 is_liked=true，否则 is_liked=false。
```

### 响应格式（SSE）

```
event: session
data: {"sessionId": "labs_sess_xxx"}

data: {"choices": [{"delta": {"content": "{\"is_liked\": true}"}}]}

data: [DONE]
```

### 前端处理示例

```typescript
// 调用 Act API 进行结构化判断（通过 Next.js 本地路由代理到上游）
const response = await fetch('/api/secondme/act/stream', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    message: userMessage,
    actionControl: '仅输出合法 JSON。结构：{"intent": "like"|"dislike"|"neutral"}。根据用户表达判断意图。信息不足时返回 {"intent": "neutral"}。'
  })
});

// 拼接 SSE 流中的 delta content，最终 JSON.parse 得到结果
```

### Chat vs Act 使用场景

| 场景 | 使用 API | 原因 |
|------|---------|------|
| 自由对话 | `/chat/stream` | 返回自然语言文本 |
| 情感/意图判断 | `/act/stream` | 返回结构化 JSON |
| 是/否决策 | `/act/stream` | 返回 `{"result": boolean}` |
| 多分类判断 | `/act/stream` | 返回 `{"category": "..."}` |
| 内容生成 | `/chat/stream` | 需要长文本输出 |

---

## 开发注意事项

### State 参数

**直接忽略 `state` 参数验证。** 在回调处理时不需要验证 state，直接处理授权码即可。

### CSS @import 规则顺序

**重要：** 在 CSS 文件中，`@import` 语句必须放在文件的最开头（只能在 `@charset` 和 `@layer` 之后）。如果在其他 CSS 规则之后使用 `@import`，会导致解析错误。

```css
/* 正确写法 - @import 放在最前面 */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC&display=swap');

:root {
  --primary-color: #000;
}

/* 错误写法 - @import 不能放在其他规则之后 */
:root {
  --primary-color: #000;
}
@import url('...'); /* 这会报错！ */
```

---

## 官方文档链接

| 文档 | 地址 |
|------|------|
| 快速入门 | https://develop-docs.second.me/zh/docs |
| 认证概述 | https://develop-docs.second.me/zh/docs/authentication |
| OAuth2 指南 | https://develop-docs.second.me/zh/docs/authentication/oauth2 |
| SecondMe API 参考 | https://develop-docs.second.me/zh/docs/api-reference/secondme |
| OAuth2 API 参考 | https://develop-docs.second.me/zh/docs/api-reference/oauth |
| 错误码参考 | https://develop-docs.second.me/zh/docs/errors |
