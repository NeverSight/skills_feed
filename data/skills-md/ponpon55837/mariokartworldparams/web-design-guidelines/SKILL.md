---
name: web-design-guidelines
description: 審查 UI 程式碼是否符合網頁介面指南。當被要求「審查我的 UI」、「檢查無障礙性」、「稽核設計」、「審查 UX」或「檢查我的網站是否符合最佳實踐」時使用。
metadata:
  author: vercel
  version: "1.0.0"
  argument-hint: <file-or-pattern>
---

# 網頁介面指南

審查檔案是否符合網頁介面指南。

## 運作方式

1. 從下方來源網址獲取最新指南
2. 讀取指定的檔案（或提示使用者輸入檔案/模式）
3. 根據獲取的指南中的所有規則進行檢查
4. 以簡潔的 `檔案:行號` 格式輸出發現的問題

## 指南來源

每次審查前獲取最新指南：

```
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

使用 WebFetch 取得最新規則。獲取的內容包含所有規則和輸出格式說明。

## 使用方式

當使用者提供檔案或模式參數時：

1. 從上述來源網址獲取指南
2. 讀取指定的檔案
3. 套用獲取的指南中的所有規則
4. 使用指南中指定的格式輸出發現的問題

若未指定檔案，請詢問使用者要審查哪些檔案。
