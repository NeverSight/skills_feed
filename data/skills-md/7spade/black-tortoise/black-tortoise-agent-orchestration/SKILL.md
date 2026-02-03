---
name: black-tortoise-agent-orchestration
description: Orchestrate Black-Tortoise 代理的子代理與 MCP 工具，確保 DDD/Signals-first 流程與最小改動。Use when coordinating multiple agents or MCP tools, planning complex multi-step workflows, or ensuring minimal surgical changes.
---

# Black-Tortoise Agent Orchestration Skill

## 使用時機

- 使用 `Black-Tortoise` 代理處理多步驟任務（規劃 → 實作 → 驗證）。
- 需要在單一回合內協調多個 MCP（angular-cli, Software-planning-mcp, sequentialthinking, context7, codacy）。

## 作業流程（最小化）

1. **定位規則**：依 `docs/INDEX.md` 讀取對應 `AGENTS.md` → `README.md`。
2. **拆解**：呼叫 `sequentialthinking/*` 取得步驟；若需正式計畫，用 `Software-planning-mcp/*` 的 `start_planning` / `save_plan`。
3. **查證**：
   - API / 框架：`context7/*`（resolve-library-id → get-library-docs）。
   - Angular CLI / schematics：`angular-cli/*`。
4. **實作護欄**：
   - 單向依賴：Presentation → Application → Domain → Infrastructure。
   - Signals-first，禁止 RxJS 狀態管理與 `as any`。
   - 保持可刪除性，最小改動。
5. **品質**：必要時用 `codacy/*` 取得分析，再給出可行修正；建議執行 `pnpm run lint`、`pnpm run architecture:gate`（不自動執行）。
6. **子代理切換**：
   - 計畫：`agent/runSubagent` → `Planning mode instructions`
   - 除錯：`agent/runSubagent` → `debug`
   - 安全/品質：`agent/runSubagent` → `SE: Security`

## MCP 防迴圈守則

- 同一議題對同一 MCP 只呼叫一次；若無新資訊，立即停止重複。
- context7：`resolve-library-id` 後接 `get-library-docs` 一輪完成，避免重跑。
- Software-planning-mcp：`start_planning` / `save_plan` 僅在計畫需要更新時執行一次。
- sequentialthinking：用於初次拆解/優先序，不在同一步驟重入。
- 避免巢狀或互相遞迴的 `agent/runSubagent` ；一次只切換一個子代理，完成後返回主代理。

## 輸出要求

- 先列假設與風險，再給具體步驟（含檔案路徑）。
- 指出需驗證的指令或測試。
- 保持簡潔，避免重複、避免跨域耦合。

## 範例輸入

- 「為 tasks capability 增加列表排序，先給計畫再實作」
- 「查 Angular Material 20 中 mat-table 的 sticky 行為，提供修正步驟」

## 範例輸出要點

- 片段化步驟 + 路徑鏈結
- 指定需查閱的 `AGENTS.md` / `README.md`
- 提醒執行 lint / architecture gate / relevant tests
