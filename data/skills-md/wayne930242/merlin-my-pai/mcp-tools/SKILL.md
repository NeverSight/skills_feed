---
name: mcp-tools
description: MCP Tools 開發指南。Use when creating or modifying MCP server tools.
---

# MCP Tools 開發指南

本專案的 MCP Tools 位於 `pai-bot/src/mcp/tools/`。

## 架構模式

```
Service Layer (ts-results)     MCP Tool Layer
┌─────────────────────┐       ┌──────────────────────┐
│ Result<T, Error>    │  -->  │ { content, isError } │
└─────────────────────┘       └──────────────────────┘
```

## Service Layer

使用 `ts-results` 回傳 `Result<T, Error>`：

```typescript
import { Err, Ok, type Result } from "ts-results";

export async function getData(): Promise<Result<Data, Error>> {
  try {
    const data = await api.fetch();
    return Ok(data);
  } catch (error) {
    return Err(error instanceof Error ? error : new Error(String(error)));
  }
}
```

## MCP Tool Layer

### 1. 註冊工具

```typescript
import type { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

export function registerMyTools(server: McpServer): void {
  server.registerTool(
    "tool_name",                    // 命名：category_action
    {
      title: "Tool Title",
      description: "工具描述（中文）",
      inputSchema: {
        param: z.string().describe("參數說明"),
        optional: z.number().optional().describe("可選參數"),
      },
    },
    async ({ param, optional = 5 }) => {
      // 實作
    }
  );
}
```

### 2. 處理 Result

```typescript
async ({ query }) => {
  const result = await service.getData(query);

  if (result.err) {
    return {
      content: [{ type: "text", text: `錯誤: ${result.val.message}` }],
      isError: true,
    };
  }

  return {
    content: [{ type: "text", text: JSON.stringify(result.val, null, 2) }],
  };
}
```

### 3. 無 Result 的 Service（使用 try-catch）

```typescript
async ({ query }) => {
  try {
    const data = await legacyService.fetch(query);
    return {
      content: [{ type: "text", text: JSON.stringify(data, null, 2) }],
    };
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    return {
      content: [{ type: "text", text: `錯誤: ${message}` }],
      isError: true,
    };
  }
}
```

## 命名規範

| 類別 | 格式 | 範例 |
|------|------|------|
| 工具名稱 | `category_action` | `google_calendar_list`, `memory_search` |
| 函數名稱 | `registerXxxTools` | `registerGoogleTools` |

## 錯誤訊息格式

```typescript
`${Category} 錯誤: ${error.message}`
// 範例: "Google Calendar 錯誤: Invalid credentials"
```

## 註冊入口

在 `pai-bot/src/mcp/index.ts` 註冊：

```typescript
import { registerMyTools } from "./tools/my-tools";

export function createMcpServer(): McpServer {
  const server = new McpServer({ name: "pai-bot", version: "1.0.0" });
  registerMyTools(server);
  return server;
}
```

## Checklist

- [ ] Service 使用 `Result<T, Error>`
- [ ] Tool 處理 `result.err` 並回傳 `isError: true`
- [ ] 使用 Zod schema 定義參數
- [ ] 錯誤訊息包含分類前綴
- [ ] 在 `index.ts` 註冊
