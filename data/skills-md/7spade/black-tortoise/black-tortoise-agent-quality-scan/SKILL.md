---
name: black-tortoise-agent-quality-scan
description: 快速盤點近期改動的品質風險，利用 codacy / context7 / sequentialthinking 制定最小修正。Use when scanning recent changes for quality issues, running static analysis, or planning remediation with Codacy/Context7 tools.
---

# Black-Tortoise Agent Quality Scan Skill

## 使用時機

- PR 前後，想快速列出高風險點（lint/type/test 失敗、API 誤用、層次違規）。
- 需要縮小改動面積並產出可執行的修正清單。

## 作業流程

1. **範圍鎖定**：用 `search/changes` 或 git diff 決定掃描檔案；若無 diff，聚焦當前功能目錄。
2. **規則定位**：依 `docs/INDEX.md` 讀取對應 `AGENTS.md` / `README.md`，確認層次邊界與禁止事項。
3. **問題蒐集**：
   - 啟用 `codacy/*` 取得分析；記錄嚴重/高優先事項。
   - 若有框架 API 疑慮，透過 `context7/*` 查官方簽章。
4. **拆解與排序**：用 `sequentialthinking/*` 產出最小修正步驟（先高風險、低成本）。
5. **建議修正**：針對每項問題給出最小可執行修正與檔案路徑；避免跨層改動。
6. **驗證**：建議執行 `pnpm run lint`、`pnpm run architecture:gate`、相關 tests（除非要求，不自動執行）。

## 輸出格式

- 假設/風險 → 問題清單（含檔案鏈結） → 建議修正步驟 → 建議驗證。
- 標註若需使用者決策的項目（如變更 API、調整設定）。

## 禁止事項

- 以增加範圍為代價的過度修正；保持最小改動。
- 引入 RxJS 狀態管理或 `as any`。
- 破壞層次單向依賴或跨能力深層 import。
