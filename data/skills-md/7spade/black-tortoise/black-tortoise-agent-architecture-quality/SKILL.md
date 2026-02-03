---
name: black-tortoise-agent-architecture-quality
description: 企業級結構與品質守則，強化高內聚低耦合、單一職責、奧卡姆剃刀與 Signals-first。Use when reviewing code for architecture violations, enforcing DDD boundaries, or ensuring quality standards in Black-Tortoise project.
---

# Black-Tortoise Agent Architecture & Quality Skill

## 使用時機

- 進行架構/設計審視或重構時，需確認層次與品質守則。
- PR 前的結構 sanity check，聚焦高風險違規（跨層依賴、肥介面、重複抽象、RxJS 狀態）。

## 作業步驟（最小化）

1. **定位規範**：依 `docs/INDEX.md` 讀取對應 `AGENTS.md` / `README.md`，鎖定層次邊界與禁止事項。
2. **拆解/排序**：`sequentialthinking/*` 單次列出審查項目與優先序。
3. **查證**：
   - API/框架：`context7/*`（resolve → get docs 一輪）。
   - CLI/schema：`angular-cli/*`。
4. **品質掃描**：必要時 `codacy/*` 取嚴重/高優先議題。
5. **判斷原則**：
   - 高內聚低耦合；單一職責；介面最小暴露。
   - 奧卡姆剃刀：刪除多餘抽象/層級；避免過度設定。
   - Signals-first；禁 RxJS 狀態；禁止 `as any`。
   - 層次單向：Presentation → Application → Domain → Infrastructure。
6. **產出**：
   - 假設/風險 → 問題清單（含檔案鏈結）→ 最小修正步驟 → 驗證建議（lint / architecture:gate / tests）。

## MCP 防迴圈

- 同議題對同一 MCP 只呼叫一次；無新資訊即停。
- context7：`resolve-library-id` → `get-library-docs` 一次完成。
- Software-planning-mcp：僅在需要計畫更新時使用 `start_planning` / `save_plan` 一次。
- sequentialthinking：初次拆解/排序用，不在同一步重入。
- 不巢狀或遞迴 `agent/runSubagent`。

## 禁止事項

- 跨能力深層 import、逆向依賴、肥介面、重複抽象。
- 引入 RxJS 狀態管理或 `as any`。
- 以「大改」取代最小修正；不可破壞可刪除性。

## 範例輸入

- 「審查 overview capability 最近改動，列出高耦合點與最小修正」
- 「重構 tasks store，確保 Signals-first 並降低介面暴露」
