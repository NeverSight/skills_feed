---
name: refactor-cleaner
description: 死代碼清理與整合專家。用於移除未使用的程式碼、重複程式碼和重構。執行分析工具 (knip, depcheck, ts-prune) 識別死代碼並安全移除。
source: everything-claude-code (MIT License)
original_author: affaan-m
updated: 2026-01-22
---

# Refactor Cleaner (重構清理)

## When to Use

在以下情況使用此 Skill：
- 定期程式碼健康檢查
- 專案清理與整合
- 移除已廢棄功能
- 減少套件大小
- 整合重複程式碼

## When NOT to Use

- 正在開發新功能時
- 生產部署前夕
- 程式碼庫不穩定時
- 測試覆蓋率不足時

## 核心職責

1. **死代碼檢測** - 找出未使用的程式碼、exports、依賴
2. **重複消除** - 識別並整合重複程式碼
3. **依賴清理** - 移除未使用的套件和 imports
4. **安全重構** - 確保變更不破壞功能
5. **文件記錄** - 在 DELETION_LOG.md 追蹤所有刪除

## 檢測工具

```bash
# knip - 找出未使用的檔案、exports、依賴
npx knip

# depcheck - 識別未使用的 npm 依賴
npx depcheck

# ts-prune - 找出未使用的 TypeScript exports
npx ts-prune

# eslint - 檢查未使用的變數
npx eslint . --report-unused-disable-directives
```

## 重構流程

### 1. 分析階段

```
a) 平行執行檢測工具
b) 收集所有發現
c) 依風險分類:
   - 安全: 未使用的 exports、依賴
   - 小心: 可能透過動態 import 使用
   - 風險: 公開 API、共用工具
```

### 2. 風險評估

對每個要移除的項目：
- 搜尋所有引用 (grep)
- 確認無動態 imports
- 檢查是否為公開 API
- 審視 git 歷史了解原因
- 測試對建構/測試的影響

### 3. 安全移除流程

```
a) 只從「安全」項目開始
b) 一次移除一個類別:
   1. 未使用的 npm 依賴
   2. 未使用的內部 exports
   3. 未使用的檔案
   4. 重複程式碼
c) 每批次後執行測試
d) 每批次建立 git commit
```

### 4. 重複整合

```
a) 找出重複的元件/工具
b) 選擇最佳實作:
   - 功能最完整
   - 測試最完善
   - 最近使用的
c) 更新所有 imports 使用選定版本
d) 刪除重複
e) 驗證測試仍通過
```

## 刪除日誌格式

建立/更新 `docs/DELETION_LOG.md`：

```markdown
# 程式碼刪除日誌

## [YYYY-MM-DD] 重構作業

### 移除的依賴
- package-name@version - 最後使用: 從未, 大小: XX KB
- another-package@version - 已被取代: better-package

### 刪除的檔案
- src/old-component.tsx - 取代為: src/new-component.tsx
- lib/deprecated-util.ts - 功能移至: lib/utils.ts

### 整合的重複程式碼
- src/components/Button1.tsx + Button2.tsx -> Button.tsx
- 原因: 兩個實作完全相同

### 移除的 Exports
- src/utils/helpers.ts - 函數: foo(), bar()
- 原因: 程式碼庫中無引用

### 影響
- 刪除檔案: 15
- 移除依賴: 5
- 移除程式碼行數: 2,300
- 套件大小減少: ~45 KB

### 測試
- 所有單元測試通過
- 所有整合測試通過
- 手動測試完成
```

## 安全檢查清單

移除任何東西前：
- [ ] 執行檢測工具
- [ ] Grep 搜尋所有引用
- [ ] 檢查動態 imports
- [ ] 審視 git 歷史
- [ ] 確認非公開 API
- [ ] 執行所有測試
- [ ] 建立備份分支
- [ ] 記錄於 DELETION_LOG.md

每次移除後：
- [ ] 建構成功
- [ ] 測試通過
- [ ] 無 console 錯誤
- [ ] 提交變更
- [ ] 更新 DELETION_LOG.md

## 常見移除模式

### 1. 未使用的 Imports

```typescript
// 移除未使用的 imports
import { useState, useEffect, useMemo } from 'react' // 只用到 useState

// 只保留使用的
import { useState } from 'react'
```

### 2. 死代碼分支

```typescript
// 移除不可達程式碼
if (false) {
  // 永遠不會執行
  doSomething()
}

// 移除未使用的函數
export function unusedHelper() {
  // 程式碼庫中無引用
}
```

### 3. 重複元件

```typescript
// 多個相似元件
components/Button.tsx
components/PrimaryButton.tsx
components/NewButton.tsx

// 整合為一個
components/Button.tsx (使用 variant prop)
```

### 4. 未使用的依賴

```json
// 已安裝但未 import 的套件
{
  "dependencies": {
    "lodash": "^4.17.21",  // 無處使用
    "moment": "^2.29.4"    // 已被 date-fns 取代
  }
}
```

## 緊急恢復

如果移除後出錯：

```bash
# 1. 立即回滾
git revert HEAD
npm install
npm run build
npm test

# 2. 調查原因
# - 什麼失敗了?
# - 是動態 import?
# - 檢測工具遺漏了什麼?

# 3. 修正向前
# - 標記為「禁止移除」
# - 記錄為何檢測工具遺漏
# - 加上明確類型註解
```

## 最佳實踐

1. **從小處著手** - 一次移除一個類別
2. **頻繁測試** - 每批次後執行測試
3. **完整記錄** - 更新 DELETION_LOG.md
4. **保守行事** - 有疑慮就不移除
5. **Git Commits** - 每個邏輯移除批次一個 commit
6. **分支保護** - 總是在 feature branch 工作
7. **同儕審查** - 合併前讓刪除被審查
8. **監控生產** - 部署後觀察錯誤

## Pull Request 範本

```markdown
## 重構: 程式碼清理

### 摘要
死代碼清理，移除未使用的 exports、依賴和重複。

### 變更
- 移除 X 個未使用的檔案
- 移除 Y 個未使用的依賴
- 整合 Z 個重複元件
- 詳見 docs/DELETION_LOG.md

### 測試
- [x] 建構通過
- [x] 所有測試通過
- [x] 手動測試完成
- [x] 無 console 錯誤

### 影響
- 套件大小: -XX KB
- 程式碼行數: -XXXX
- 依賴: -X 套件

### 風險等級
低 - 僅移除可驗證的未使用程式碼

詳見 DELETION_LOG.md。
```

## 成功標準

清理作業後：
- 所有測試通過
- 建構成功
- 無 console 錯誤
- DELETION_LOG.md 已更新
- 套件大小已減少
- 生產環境無回歸
