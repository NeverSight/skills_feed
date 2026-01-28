---
name: code-simplifier
description: |
  簡化與精煉代碼，提升清晰度、一致性和可維護性，同時保留所有功能。
  預設聚焦於最近修改的代碼，除非另有指示。

  觸發時機：
  - 完成功能實作後，需要清理代碼
  - 發現代碼過於複雜或難以理解
  - 重構既有代碼以提升可讀性
  - 用戶提到「簡化」、「simplify」、「清理」、「refactor」

allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Grep
  - Glob
---

# Code Simplifier Protocol

## 1. 核心原則

**「簡單就是力量」**

- 保持功能完整性：簡化不等於刪減功能
- 提升可讀性：代碼應該一目了然
- 減少認知負擔：降低理解代碼所需的心智模型複雜度
- 遵循 DRY 原則：消除重複，但不過度抽象

---

## 2. 簡化檢查清單

### 2.1 命名改善

```typescript
// ❌ 模糊命名
const d = new Date();
const arr = users.filter(u => u.active);
const handleClick = () => { /* 複雜邏輯 */ };

// ✅ 清晰命名
const currentDate = new Date();
const activeUsers = users.filter(user => user.isActive);
const handleUserRegistration = () => { /* 複雜邏輯 */ };
```

### 2.2 函數拆分

```typescript
// ❌ 過長函數（超過 30 行）
function processOrder(order: Order) {
  // 驗證
  // 計算價格
  // 處理付款
  // 發送通知
  // 更新庫存
  // ...100 行
}

// ✅ 單一職責
function processOrder(order: Order) {
  validateOrder(order);
  const total = calculateTotal(order);
  await processPayment(order, total);
  await sendConfirmation(order);
  await updateInventory(order);
}
```

### 2.3 條件簡化

```typescript
// ❌ 巢狀條件
if (user) {
  if (user.isActive) {
    if (user.hasPermission) {
      doSomething();
    }
  }
}

// ✅ 早期返回
if (!user) return;
if (!user.isActive) return;
if (!user.hasPermission) return;
doSomething();
```

### 2.4 消除魔法數字

```typescript
// ❌ 魔法數字
if (status === 1) { ... }
setTimeout(fn, 86400000);

// ✅ 具名常數
const STATUS_ACTIVE = 1;
const ONE_DAY_MS = 24 * 60 * 60 * 1000;

if (status === STATUS_ACTIVE) { ... }
setTimeout(fn, ONE_DAY_MS);
```

### 2.5 減少巢狀層級

```typescript
// ❌ 深層巢狀
users.forEach(user => {
  user.orders.forEach(order => {
    order.items.forEach(item => {
      if (item.inStock) {
        processItem(item);
      }
    });
  });
});

// ✅ 扁平化處理
const allItems = users
  .flatMap(user => user.orders)
  .flatMap(order => order.items)
  .filter(item => item.inStock);

allItems.forEach(processItem);
```

---

## 3. React 組件簡化

### 3.1 Props 解構

```typescript
// ❌ 重複存取 props
function UserCard(props: UserCardProps) {
  return (
    <div>
      <h1>{props.user.name}</h1>
      <p>{props.user.email}</p>
      <span>{props.user.role}</span>
    </div>
  );
}

// ✅ 解構 + 展開
function UserCard({ user }: UserCardProps) {
  const { name, email, role } = user;
  return (
    <div>
      <h1>{name}</h1>
      <p>{email}</p>
      <span>{role}</span>
    </div>
  );
}
```

### 3.2 條件渲染

```typescript
// ❌ 冗長的三元運算
{isLoading ? <Spinner /> : error ? <Error message={error} /> : data ? <Content data={data} /> : null}

// ✅ 早期返回
if (isLoading) return <Spinner />;
if (error) return <Error message={error} />;
if (!data) return null;
return <Content data={data} />;
```

### 3.3 自訂 Hook 抽取

```typescript
// ❌ 組件內混雜大量邏輯
function UserDashboard() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetch('/api/users')
      .then(res => res.json())
      .then(data => setUsers(data))
      .catch(err => setError(err))
      .finally(() => setLoading(false));
  }, []);

  // ... 渲染邏輯
}

// ✅ 抽取 Hook
function useUsers() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => { /* fetch 邏輯 */ }, []);

  return { users, loading, error };
}

function UserDashboard() {
  const { users, loading, error } = useUsers();
  // ... 純粹的渲染邏輯
}
```

---

## 4. 簡化流程

### 步驟 1：識別目標

```bash
# 找出最近修改的檔案
git diff --name-only HEAD~5

# 或指定範圍
git diff --name-only main...HEAD
```

### 步驟 2：分析複雜度

檢查以下指標：
- 函數長度（> 30 行需關注）
- 巢狀深度（> 3 層需關注）
- 認知複雜度
- 重複代碼模式

### 步驟 3：逐步簡化

1. 先提取常數
2. 重命名變數/函數
3. 拆分長函數
4. 簡化條件邏輯
5. 消除重複

### 步驟 4：驗證

```bash
# 確保類型正確
npm run typecheck

# 確保測試通過
npm test

# 確保風格一致
npm run lint
```

---

## 5. 禁止事項

### ❌ 過度簡化

```typescript
// 不要為了簡化而犧牲可讀性
// ❌ 過度壓縮
const r = u.filter(x => x.a && x.b.c > 5).map(x => x.d);

// ✅ 保持可讀
const activeUsersWithHighScore = users
  .filter(user => user.isActive && user.stats.score > 5)
  .map(user => user.name);
```

### ❌ 過早抽象

```typescript
// 不要為只用一次的邏輯建立工具函數
// ❌ 不必要的抽象
const isValidAge = (age: number) => age >= 18;
if (isValidAge(user.age)) { ... }

// ✅ 直接寫
if (user.age >= 18) { ... }
```

### ❌ 改變行為

```typescript
// 簡化不應改變功能行為
// ❌ 簡化時意外改變邏輯
// 原本：|| 是短路運算
const name = user.name || 'Anonymous';

// 錯誤簡化：?? 只處理 null/undefined
const name = user.name ?? 'Anonymous';
// 如果 user.name 是空字串 ''，行為會不同！
```

---

## 6. 與其他 Skills 整合

| 階段 | 整合 Skill | 說明 |
|------|-----------|------|
| 簡化前 | `/read-before-edit` | 完整理解現有代碼 |
| 簡化中 | `/type-checker` | 確保類型正確 |
| 簡化後 | `/rigorous_testing` | 確保功能不變 |
| 提交前 | `/pre-commit-validator` | 完整品質檢查 |

---

## 7. 快速指令

```bash
# 找出長函數
grep -rn "function" --include="*.ts" | head -20

# 找出深巢狀（多個縮排）
grep -rn "^        " --include="*.tsx" | head -20

# 找出 TODO/FIXME
grep -rn "TODO\|FIXME" --include="*.ts" --include="*.tsx"
```

---

## 8. 記住

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   🎯 簡單 ≠ 簡陋                                                │
│                                                                 │
│   📖 代碼是寫給人看的，順便讓機器執行                           │
│                                                                 │
│   ⚖️ 平衡簡潔與可讀性                                           │
│                                                                 │
│   🔄 簡化後必須測試，確保行為不變                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```
