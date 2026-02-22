---
name: backend-logic-expert
description: 专注于 Nitro API、业务逻辑封装、Better-Auth 集成与权限校验。
version: 1.0.0
author: GitHub Copilot
---

# Backend Logic Expert Skill (后端逻辑专家技能)

## 核心能力 (Core Capabilities)

-   **Nitro Handler**: 编写标准的 `defineEventHandler`，利用 Nuxt 4 的服务端特性。
-   **业务流**: 在 `server/utils/` 或 `server/logic/` 中封装可重用的业务逻辑函数，保持 Handler 简洁。
-   **输入验证**: 使用 Zod 编写严格的 Schema，对 `query`, `body`, `params` 进行全量校验。
-   **鉴权与权限**: 集成 Better-Auth，在 API 头部强制执行权限检查中间件。
-   **错误处理**: 使用 `createError` 抛出具有语义化错误码和消息的响应。

## 指令 (Instructions)

1.  **标准化响应**: 统一返回格式，严禁直接返回裸数据。
2.  **安全隔离**: API 逻辑与持久化逻辑分离，敏感操作必须通过 Service 层进行。
3.  **异步安全**: 妥善处理 Promise，避免未捕获的异常导致进程崩溃。
4.  **日志记录**: 对关键业务操作记录审计日志。

## 使用示例 (Usage Example)

输入: "实现用户登录 API。"
动作: 编写 Zod 验证，调用 Better-Auth 接口，并处理登录成功后的 Session 注入。
