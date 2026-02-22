---
name: build-error-resolver
description: 建構與 TypeScript 錯誤修復專家。當建構失敗或出現類型錯誤時主動使用。僅修復建構/類型錯誤，最小化 diff，不做架構修改。專注於快速讓建構通過。
source: everything-claude-code (MIT License)
original_author: affaan-m
updated: 2026-01-22
---

# Build Error Resolver (建構錯誤修復)

## When to Use

在以下情況使用此 Skill：
- `npm run build` 失敗
- `npx tsc --noEmit` 顯示錯誤
- 類型錯誤阻礙開發
- Import/模組解析錯誤
- 設定檔錯誤
- 依賴版本衝突

## 核心原則

1. **最小化修改** - 只做必要的最小改動
2. **不重構** - 不改動無關的程式碼
3. **不改架構** - 只修錯誤，不做設計變更
4. **快速迭代** - 修一個錯誤，驗證，繼續下一個

## 診斷指令

```bash
# TypeScript 類型檢查 (無輸出)
npx tsc --noEmit

# 顯示所有錯誤
npx tsc --noEmit --pretty --incremental false

# 檢查特定檔案
npx tsc --noEmit path/to/file.ts

# Next.js 建構
npm run build

# ESLint 檢查
npx eslint . --ext .ts,.tsx,.js,.jsx
```

## 錯誤修復流程

### 1. 收集所有錯誤
```bash
npx tsc --noEmit --pretty
```

### 2. 分類錯誤
- 類型推斷失敗
- 缺少類型定義
- Import/Export 錯誤
- 設定錯誤
- 依賴問題

### 3. 按優先級修復
- 阻礙建構：先修
- 類型錯誤：依序修
- 警告：有時間再修

## 常見錯誤模式與修復

### 1. 類型推斷失敗

```typescript
// 錯誤: Parameter 'x' implicitly has an 'any' type
function add(x, y) { return x + y }

// 修復: 加上類型註解
function add(x: number, y: number): number { return x + y }
```

### 2. Null/Undefined 錯誤

```typescript
// 錯誤: Object is possibly 'undefined'
const name = user.name.toUpperCase()

// 修復: Optional chaining
const name = user?.name?.toUpperCase()

// 或: Null check
const name = user && user.name ? user.name.toUpperCase() : ''
```

### 3. 缺少屬性

```typescript
// 錯誤: Property 'age' does not exist on type 'User'
interface User { name: string }
const user: User = { name: 'John', age: 30 }

// 修復: 新增屬性到 interface
interface User {
  name: string
  age?: number
}
```

### 4. Import 錯誤

```typescript
// 錯誤: Cannot find module '@/lib/utils'

// 修復 1: 檢查 tsconfig paths
{
  "compilerOptions": {
    "paths": { "@/*": ["./src/*"] }
  }
}

// 修復 2: 使用相對路徑
import { formatDate } from '../lib/utils'

// 修復 3: 安裝缺少的套件
npm install @/lib/utils
```

### 5. 類型不符

```typescript
// 錯誤: Type 'string' is not assignable to type 'number'
const age: number = "30"

// 修復: 轉型
const age: number = parseInt("30", 10)
```

### 6. Generic 限制

```typescript
// 錯誤: Type 'T' is not assignable to type 'string'
function getLength<T>(item: T): number {
  return item.length
}

// 修復: 加上限制
function getLength<T extends { length: number }>(item: T): number {
  return item.length
}
```

### 7. React Hook 錯誤

```typescript
// 錯誤: React Hook cannot be called conditionally
function MyComponent() {
  if (condition) {
    const [state, setState] = useState(0) // 錯誤!
  }
}

// 修復: Hook 移到頂層
function MyComponent() {
  const [state, setState] = useState(0)
  if (!condition) return null
  // 使用 state
}
```

### 8. Async/Await 錯誤

```typescript
// 錯誤: 'await' only allowed within async functions
function fetchData() {
  const data = await fetch('/api/data')
}

// 修復: 加上 async
async function fetchData() {
  const data = await fetch('/api/data')
}
```

### 9. 模組未找到

```typescript
// 錯誤: Cannot find module 'react'

// 修復: 安裝依賴
npm install react
npm install --save-dev @types/react
```

## 最小化修改策略

### 做:
- 加上缺少的類型註解
- 加上必要的 null checks
- 修復 imports/exports
- 安裝缺少的依賴
- 更新類型定義

### 不做:
- 重構無關程式碼
- 改變架構
- 重新命名變數/函數
- 新增功能
- 改變邏輯流程
- 優化效能

## 建構錯誤報告格式

```markdown
# 建構錯誤修復報告

**日期:** YYYY-MM-DD
**建構目標:** Next.js Production / TypeScript Check
**初始錯誤:** X
**已修復錯誤:** Y
**建構狀態:** 通過 / 失敗

## 已修復錯誤

### 1. [錯誤類別]
**位置:** `src/components/Card.tsx:45`
**錯誤訊息:**
Parameter 'market' implicitly has an 'any' type.

**修復:**
+function formatMarket(market: Market) {
-function formatMarket(market) {

**修改行數:** 1

## 驗證步驟

1. TypeScript 檢查通過: `npx tsc --noEmit`
2. Next.js 建構成功: `npm run build`
3. 無新錯誤產生
```

## 錯誤優先級

### 嚴重 (立即修復)
- 建構完全失敗
- 開發伺服器無法啟動
- 生產部署被阻擋

### 高 (盡快修復)
- 單一檔案失敗
- 新程式碼的類型錯誤
- Import 錯誤

### 中 (有空修復)
- Linter 警告
- 已棄用 API 使用
- 非嚴格類型問題

## 快速參考指令

```bash
# 檢查錯誤
npx tsc --noEmit

# 清除快取重建
rm -rf .next node_modules/.cache
npm run build

# 安裝缺少的依賴
npm install

# 自動修復 ESLint
npx eslint . --fix

# 驗證 node_modules
rm -rf node_modules package-lock.json
npm install
```

## 成功標準

- `npx tsc --noEmit` 回傳 code 0
- `npm run build` 成功完成
- 無新錯誤產生
- 修改行數最小化 (< 受影響檔案的 5%)
- 開發伺服器正常運作
- 測試仍然通過
