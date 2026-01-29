---
name: code-standards
description: Next.js 16 App Router 與 TypeScript 編碼規範。為 AI 代理提供開發時的技術標準指導，確保程式碼品質、一致性和可維護性。
license: MIT
---

# Next.js 與 TypeScript 編碼規範

## 我的功能

- 提供專案統一的編碼標準
- 指導 AI 代理遵循最佳實踐
- 確保 TypeScript 嚴格模式和型別安全
- 統一元件設計、狀態管理和樣式撰寫方式

## 何時使用我

在以下情況下使用此技能：

- 撰寫新的 React 元件時
- 進行程式碼審查 (Code Review) 時
- 需要確認程式碼是否符合專案規範時
- 重構現有程式碼時
- 處理型別定義和介面設計時
- 建立新檔案或目錄結構時

## 核心技術棧

### 必須使用的套件

- **Next.js**: `^16.0.10` (App Router 模式)
- **React**: `^18.3.1`
- **Jotai**: `^2.16.0` (狀態管理)
- **Tailwind CSS**: `^3.4.19` (樣式)
- **TypeScript**: `^5.9.3` (嚴格模式)
- **i18next**: `^25.7.3` (國際化)
- **pnpm**: 套件管理器

### 禁止使用的套件

❌ Redux、Zustand、Recoil (已使用 Jotai)
❌ styled-components、emotion (已使用 Tailwind CSS)
❌ Material-UI、Ant Design (使用 Tailwind CSS)
❌ axios (使用原生 fetch)
❌ next-intl、next-i18next (已使用 react-i18next)

## 編碼規範總覽

詳細的編碼規範和最佳實踐，請參考 [`AGENTS.md`](./AGENTS.md) 檔案。

## 主要規範類別

### 1. 架構與檔案結構

- App Router 目錄結構
- 元件組織原則
- 型別定義規範

### 2. TypeScript 與型別安全

- 嚴格模式配置
- Interface vs Type 使用時機
- 避免 any 的具體做法

### 3. React 元件設計

- 函式元件優先
- Hooks 使用規則
- 效能最佳化

### 4. 狀態管理 (Jotai)

- Atom 定義標準
- 避免 props drilling
- 全域狀態最佳實踐

### 5. 樣式與 UI

- Tailwind CSS 使用規範
- 響應式設計原則
- 無障礙性要求

### 6. 效能最佳化

- Next.js 效能技巧
- React 效能最佳實踐
- 打包體積優化

### 7. 國際化 (i18n)

- i18next 配置標準
- 語言檔案管理
- 翻譯工作流程

### 8. 開發流程與工具

- 測試流程
- Git 工作流程整合
- 建置與部署規範

## 快速參考

### 常用模式

```typescript
// 元件模式
'use client';

import { useAtomValue } from 'jotai';
import type { ComponentProps } from '@/types';

export default function Component({ prop }: ComponentProps) {
  const data = useAtomValue(dataAtom);
  return <div>{data}</div>;
}

// 型別定義
interface UserData {
  id: string;
  name: string;
}

// 狀態管理
export const userDataAtom = atom<UserData[]>([]);
```

### 禁止模式

```typescript
// ❌ 錯誤：使用 any
function processData(data: any) {}

// ❌ 錯誤：直接修改 props
function Component({ data }: { data: any }) {
  data.modified = true; // 錯誤
}

// ❌ 錯誤：使用禁止套件
import styled from "styled-components";
```

## 驗證檢查清單

### 程式碼品質

- [ ] 使用 TypeScript 嚴格模式
- [ ] 避免 any 類型，使用具體型別
- [ ] 元件使用 'use client' 標記（如需要）
- [ ] 使用 interface 定義物件結構
- [ ] 正確使用 React Hooks

### 架構與組織

- [ ] 遵循 App Router 目錄結構
- [ ] 元件大小合理（建議 < 200 行）
- [ ] 正確使用路徑別名（@/）
- [ ] 適當的檔案組織

### 狀態管理

- [ ] 使用 Jotai atoms 而非 props drilling
- [ ] Atom 定義清晰且型別安全
- [ ] 避免直接修改狀態
- [ ] 使用適當的 Jotai hooks

### 樣式與 UI

- [ ] 使用 Tailwind CSS 類別
- [ ] 實現響應式設計
- [ ] 新增必要的 aria-label
- [ ] 避免內聯樣式（除非必要）

### 效能

- [ ] 使用適當的 React 最佳化（memo、useCallback）
- [ ] 避免不必要的重新渲染
- [ ] 使用動態導入（如適當）
- [ ] 優化圖片載入

## 相關技能

- [`git-workflow`](../git-workflow/SKILL.md) - Git 工作流程規範
- [`i18n-workflow`](../i18n-workflow/SKILL.md) - 多語言國際化流程
- [`readme-maintenance`](../readme-maintenance/SKILL.md) - README.md 維護指南

---

**這個技能確保您的程式碼始終符合專案標準並保持高品質！**
