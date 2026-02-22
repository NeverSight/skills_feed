---
name: ai-dev-workflow
description: 由文件串起完整的 AI 開發流程。涵蓋領域建模與程式碼組織（DDD）、行為驗證與自動測試（BDD）、以及 AI 開發規範設定（Agent 規範）。Use when (1) the project has .feature files, (2) the user asks to organize code by business features or define naming conventions, (3) creating or updating AGENTS.md / project rule files, (4) writing or implementing Gherkin scenarios, (5) starting a new project from scratch, or (6) the agent needs the full development lifecycle.
---

# AI Dev Workflow — Agent Skill

AI 根據 SPEC.md, AGENTS.md, features 中的 Gherkin .feature 文件，可以了解系統的全貌，並擁有行為驗證的能力

```
DDD（怎麼拆）→ BDD（做什麼 / 怎麼驗）→ Agent 規範（怎麼規範 AI）
```

## 按需參考

根據當前任務讀取對應的 reference：

- 需要組織程式碼結構或定義命名 → 讀 [references/ddd.md](references/ddd.md)
- 需要撰寫或實作 .feature → 讀 [references/bdd.md](references/bdd.md)
- 需要撰寫專案規範檔 → 讀 [references/agent-rules.md](references/agent-rules.md)

---

# Part A：如何產出需求與規範文件

> 完整的開發流程從文件開始。由使用者撰寫，或與 Agent 討論後產出。

## 產出流程

```
1. [DDD] 用業務思維切模組、定義命名，撰寫 SPEC.md
      ↓
2. [BDD] 按 DDD Bounded Context 和 Agent 合作撰寫 .feature 檔案（詳細行為規格）
      ↓
3. [規範] 將其餘 Agent 需要知道的需求與規範寫進 AGENTS.md（補充架構、UI 偏好與限制等）
      ↓
4. 全部交給 AI Agent
```

## 各組成的定位

| 方法論   | 產出文件                   | 解決什麼問題           | 詳細說明                               |
| :------- | :------------------------- | :--------------------- | :------------------------------------- |
| DDD      | SPEC.md 的「戰略設計」區塊 | 邊界、術語與溝通       | [references/ddd.md](references/ddd.md) |
| BDD      | features/\*.feature        | 怎麼驗證做對了         | [references/bdd.md](references/bdd.md) |
| 補充說明 | AGENTS.md 等專案規範檔     | 規範 AI 行為和實作細節 | [references/agent-rules.md]            |

## 文件的增量更新

```
新增功能 → 新增 .feature
修改功能 → 修改 .feature
刪除功能 → 刪除 .feature + 告知 Agent 清理程式碼
架構異動 → 修改 AGENTS.md
```

---

# Part B：Agent 的端到端開發流程

> 當規格文件已就緒，Agent 按以下流程自主開發。

## Phase 1：理解

```
1. 讀取 SPEC.md
   → 產品全貌、技術架構、功能需求
   → 戰略設計（Bounded Context, Ubiquitous Language, Context Map）

2. 讀取專案規範檔 AGENTS.md
   → 程式碼風格、架構規則、測試要求、禁止事項

3. 讀取 features/*.feature
   → 所有行為規格（可自動驗證的驗收標準）
```

> **在讀完所有規格文件之前，不要寫任何程式碼。**
> **若文件有缺漏，要求使用者補充文件，或詢問是否需要幫忙補充。**

## Phase 2：規劃

```
4. 理解 AGENTS.md 中的規範，依照規範中的要求規劃實作方式
5. 理解 Feature 間的依賴關係決定實作順序

```

## Phase 3：實作迴圈

> 以下驗證指令以 Node.js / JavaScript 專案為例，請依照 SPEC.md 和專案規範檔中指定的測試工具替換對應指令。

```
6. 選擇下一個 Feature
7. 實作 Step Definitions（Cucumber）
8. 實作讓 Scenario 通過的程式碼
9. 自我審查（符合 AGENT.md 規範、邊界情況、null 檢查、效能、a11y）
10. 執行驗證：
    a. npx tsc --noEmit    → 修復型別錯誤
    b. npx jest             → 修復單元測試
    c. npx cucumber-js      → 修復 BDD 測試
11. 失敗 → 分析錯誤 → 修復 → 回到 10
12. 通過 → 回到 6
```

## Phase 4：最終驗證

```
13. 完整測試 suite（所有 Feature + 所有 Jest）
14. 確認零失敗
15. 回報結果
```

---

## 場景指南

### A：全新專案

引導使用者完成 SPEC.md, AGENTS.md, features/\*.features 文件

### B：已有文件，從 0 開始建立新專案

```
Phase 1 → Phase 2 初始化專案（按 AGENTS.md 技術棧）→ Phase 3 → Phase 4 ...
```

### B：新增功能

```
讀新 .feature → 實作 → 新舊 .feature 全部通過
```

### C：修改既有功能

```
全部測試全綠 → 讀修改後的 .feature → 預期失敗 → 改實作 → 全綠
```

### D：修復 Bug

```
新 Scenario fail（重現 Bug）→ 修復 → 新 Scenario pass + 全綠
```

### E：重構

```
全綠（基線）→ 重構（不改外部行為）→ 仍然全綠
```

### F：刪除功能

```
使用者告知移除 → 刪 Step Definitions、程式碼、元件 → 剩餘測試全綠
```

---

## 開發原則

- **DDD**：明確劃分邊界 (Bounded Context)、統一命名 (Ubiquitous Language)、嚴格定義模組溝通 (Context Map)（詳見 [references/ddd.md](references/ddd.md)）
- **BDD**：.feature 是驗收標準、新舊都要通過、BDD + TDD 分層（詳見 [references/bdd.md](references/bdd.md)）
- **規範**：遵循 AGENTS.md 技術與偏好、不擅自加功能

## 卡住時的處理

| 症狀              | 處理方式             |
| :---------------- | :------------------- |
| .feature 描述不清 | 回報使用者，請求釐清 |
| 修一個破另一個    | 向使用者提出重構建議 |
| 任務太大或太複雜  | 拆成更小的子任務     |

## 完整專案結構

```
my-project/
├── SPEC.md                     ← 產品規格（Part A 產出）
├── AGENTS.md                   ← 專案與 Agent 規範（Part A 產出）
├── features/
│   ├── [context]/
│   │   ├── [feature].feature   ← BDD .feature（Part A 產出）
│   │   └── [feature].steps.ts  ← Step Definitions（Agent 實作）
├── src/                        ← 原始碼（Agent 實作，按 Context 分）
│   ├── [context-1]/
│   ├── [context-2]/
│   ├── shared/
│   └── __tests__/              ← 單元測試（Agent 撰寫）
└── package.json
```
