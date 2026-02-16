---
name: code-quality
description: Clean code principles, SOLID, and code review practices
domain: software-engineering
version: 1.0.0
tags: [clean-code, solid, refactoring, code-review, linting, metrics]
triggers:
  keywords:
    primary: [code quality, clean code, solid, refactor, code review, lint]
    secondary: [dry, kiss, yagni, code smell, technical debt, static analysis]
  context_boost: [maintainable, readable, best practice, standards]
  context_penalty: [deployment, infrastructure, devops]
  priority: high
---

# Code Quality

## Overview

Principles and practices for writing maintainable, readable, and reliable code.

---

## Clean Code Principles

### Meaningful Names

```typescript
// ❌ Cryptic names
const d = new Date();
const u = getU();
const arr = data.filter(x => x.s === 'a');

// ✅ Descriptive names
const currentDate = new Date();
const currentUser = getCurrentUser();
const activeUsers = users.filter(user => user.status === 'active');

// ❌ Hungarian notation (outdated)
const strName = 'John';
const arrItems = [];
const bIsActive = true;

// ✅ Let the type system handle types
const name = 'John';
const items: Item[] = [];
const isActive = true;
```

### Functions

```typescript
// ❌ Does too much
function processUserData(userId: string) {
  const user = db.findUser(userId);
  const orders = db.findOrders(userId);
  const total = orders.reduce((sum, o) => sum + o.amount, 0);
  sendEmail(user.email, `Your total: ${total}`);
  updateAnalytics(userId, total);
  return { user, orders, total };
}

// ✅ Single responsibility
function getUser(userId: string): User {
  return db.findUser(userId);
}

function getUserOrders(userId: string): Order[] {
  return db.findOrders(userId);
}

function calculateTotal(orders: Order[]): number {
  return orders.reduce((sum, o) => sum + o.amount, 0);
}

function sendOrderSummary(user: User, total: number): void {
  sendEmail(user.email, `Your total: ${total}`);
}

// ❌ Too many parameters
function createUser(name, email, age, role, department, manager, startDate) {}

// ✅ Use object parameter
interface CreateUserParams {
  name: string;
  email: string;
  age?: number;
  role: Role;
  department: string;
  managerId?: string;
  startDate: Date;
}

function createUser(params: CreateUserParams): User {}
```

### Comments

```typescript
// ❌ Redundant comment
// Increment counter by 1
counter++;

// ❌ Outdated comment (code changed, comment didn't)
// Returns the user's full name
function getUserEmail(user: User) {
  return user.email;
}

// ✅ Explains WHY, not WHAT
// Use binary search because the list is sorted and can have 100k+ items
const index = binarySearch(sortedItems, target);

// ✅ Warns about non-obvious behavior
// IMPORTANT: This function mutates the input array for performance reasons
function quickSort(arr: number[]): number[] {
  // ...
}

// ✅ TODO with context
// TODO(john): Remove after migration completes - tracking in JIRA-1234
const legacyAdapter = new LegacyAdapter();
```

---

## SOLID Principles

### Single Responsibility Principle

```typescript
// ❌ Multiple responsibilities
class UserManager {
  createUser(data: UserData) { /* DB logic */ }
  validateEmail(email: string) { /* Validation logic */ }
  sendWelcomeEmail(user: User) { /* Email logic */ }
  generateReport(users: User[]) { /* Report logic */ }
}

// ✅ Single responsibility each
class UserRepository {
  create(data: UserData): User { /* DB logic */ }
  findById(id: string): User | null { /* DB logic */ }
}

class UserValidator {
  validateEmail(email: string): boolean { /* Validation */ }
  validatePassword(password: string): ValidationResult { /* Validation */ }
}

class EmailService {
  sendWelcomeEmail(user: User): void { /* Email logic */ }
}

class UserReportGenerator {
  generate(users: User[]): Report { /* Report logic */ }
}
```

### Open/Closed Principle

```typescript
// ❌ Must modify to add new payment methods
class PaymentProcessor {
  process(payment: Payment) {
    if (payment.type === 'credit') {
      // Credit card logic
    } else if (payment.type === 'paypal') {
      // PayPal logic
    } else if (payment.type === 'crypto') {
      // Crypto logic - had to modify existing code!
    }
  }
}

// ✅ Open for extension, closed for modification
interface PaymentMethod {
  process(amount: number): Promise<PaymentResult>;
}

class CreditCardPayment implements PaymentMethod {
  async process(amount: number): Promise<PaymentResult> { /* ... */ }
}

class PayPalPayment implements PaymentMethod {
  async process(amount: number): Promise<PaymentResult> { /* ... */ }
}

// New payment method - no modification to existing code
class CryptoPayment implements PaymentMethod {
  async process(amount: number): Promise<PaymentResult> { /* ... */ }
}

class PaymentProcessor {
  constructor(private method: PaymentMethod) {}

  async process(amount: number): Promise<PaymentResult> {
    return this.method.process(amount);
  }
}
```

### Liskov Substitution Principle

```typescript
// ❌ Violates LSP - Square breaks Rectangle contract
class Rectangle {
  constructor(public width: number, public height: number) {}

  setWidth(w: number) { this.width = w; }
  setHeight(h: number) { this.height = h; }
  getArea() { return this.width * this.height; }
}

class Square extends Rectangle {
  setWidth(w: number) {
    this.width = w;
    this.height = w; // Unexpected side effect!
  }
  setHeight(h: number) {
    this.width = h;
    this.height = h; // Unexpected side effect!
  }
}

// ✅ Proper abstraction
interface Shape {
  getArea(): number;
}

class Rectangle implements Shape {
  constructor(private width: number, private height: number) {}
  getArea() { return this.width * this.height; }
}

class Square implements Shape {
  constructor(private side: number) {}
  getArea() { return this.side * this.side; }
}
```

### Interface Segregation Principle

```typescript
// ❌ Fat interface
interface Worker {
  work(): void;
  eat(): void;
  sleep(): void;
  attendMeeting(): void;
  writeReport(): void;
}

// Robot can't eat or sleep!
class Robot implements Worker {
  work() { /* ... */ }
  eat() { throw new Error('Robots do not eat'); }  // Forced to implement
  sleep() { throw new Error('Robots do not sleep'); }
  // ...
}

// ✅ Segregated interfaces
interface Workable {
  work(): void;
}

interface Eatable {
  eat(): void;
}

interface Sleepable {
  sleep(): void;
}

class Human implements Workable, Eatable, Sleepable {
  work() { /* ... */ }
  eat() { /* ... */ }
  sleep() { /* ... */ }
}

class Robot implements Workable {
  work() { /* ... */ }
}
```

### Dependency Inversion Principle

```typescript
// ❌ High-level depends on low-level
class OrderService {
  private db = new MySQLDatabase();  // Concrete dependency
  private mailer = new SendGridMailer();  // Concrete dependency

  createOrder(data: OrderData) {
    const order = this.db.insert('orders', data);
    this.mailer.send(data.email, 'Order confirmed');
    return order;
  }
}

// ✅ Depend on abstractions
interface Database {
  insert(table: string, data: unknown): unknown;
  find(table: string, query: unknown): unknown[];
}

interface Mailer {
  send(to: string, message: string): void;
}

class OrderService {
  constructor(
    private db: Database,
    private mailer: Mailer
  ) {}

  createOrder(data: OrderData) {
    const order = this.db.insert('orders', data);
    this.mailer.send(data.email, 'Order confirmed');
    return order;
  }
}

// Now we can inject any implementation
const service = new OrderService(
  new PostgresDatabase(),
  new SESMailer()
);
```

---

## Code Review Best Practices

### What to Look For

```markdown
## Code Review Checklist

### Correctness
- [ ] Logic is correct and handles edge cases
- [ ] Error handling is appropriate
- [ ] No obvious bugs or regressions

### Design
- [ ] Code is at the right abstraction level
- [ ] No unnecessary complexity
- [ ] Follows existing patterns in codebase

### Readability
- [ ] Clear naming and intent
- [ ] Comments explain "why" not "what"
- [ ] Code is self-documenting where possible

### Testing
- [ ] Adequate test coverage
- [ ] Tests are meaningful (not just coverage padding)
- [ ] Edge cases are tested

### Performance
- [ ] No obvious N+1 queries or inefficiencies
- [ ] Appropriate data structures used
- [ ] Caching considered if needed

### Security
- [ ] Input validation present
- [ ] No secrets in code
- [ ] Authentication/authorization correct
```

### Giving Feedback

```markdown
# Good Review Comments

## ✅ Specific and actionable
"This loop has O(n²) complexity. Consider using a Map for O(n) lookup."

## ✅ Explain the why
"Let's extract this to a separate function - it makes the logic easier
to test and the main function more readable."

## ✅ Offer alternatives
"Instead of mutating the array, consider using `filter()` which returns
a new array: `const active = items.filter(i => i.active)`"

## ✅ Distinguish severity
- "nit: " - Minor style issue, optional
- "suggestion: " - Good to have, not blocking
- "blocking: " - Must fix before merge

# Avoid

## ❌ Vague criticism
"This code is confusing"

## ❌ Personal attacks
"You always make this mistake"

## ❌ No explanation
"Use a different approach"
```

---

## Code Metrics

### Cyclomatic Complexity

```typescript
// High complexity (10+) - hard to test and maintain
function processOrder(order: Order): Result {
  if (order.status === 'pending') {           // +1
    if (order.paymentMethod === 'card') {     // +1
      if (order.amount > 1000) {              // +1
        // ...
      } else if (order.amount > 100) {        // +1
        // ...
      } else {
        // ...
      }
    } else if (order.paymentMethod === 'cash') {  // +1
      // ...
    }
  } else if (order.status === 'processing') {  // +1
    // ...
  }
  // ... more branches
}

// Lower complexity - extract conditions
function processOrder(order: Order): Result {
  const processor = getProcessor(order.paymentMethod);
  const tier = getPricingTier(order.amount);
  return processor.process(order, tier);
}
```

### Metrics to Track

| Metric | Target | Why |
|--------|--------|-----|
| Cyclomatic Complexity | < 10 per function | Testability |
| Function Length | < 50 lines | Readability |
| File Length | < 400 lines | Maintainability |
| Test Coverage | > 80% | Confidence |
| Duplication | < 3% | DRY principle |

---

## Linting & Formatting

### ESLint Configuration

```javascript
// .eslintrc.js
module.exports = {
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
  ],
  rules: {
    // Prevent bugs
    'no-unused-vars': 'error',
    '@typescript-eslint/no-floating-promises': 'error',
    '@typescript-eslint/no-misused-promises': 'error',

    // Code quality
    'complexity': ['warn', 10],
    'max-lines-per-function': ['warn', 50],
    'max-depth': ['warn', 3],

    // Consistency
    'prefer-const': 'error',
    'no-var': 'error',
  }
};
```

### Pre-commit Hooks

```json
// package.json
{
  "husky": {
    "hooks": {
      "pre-commit": "lint-staged"
    }
  },
  "lint-staged": {
    "*.{ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,md}": [
      "prettier --write"
    ]
  }
}
```

---

## Related Skills

- [[refactoring]] - Improving existing code
- [[testing-strategies]] - Ensuring quality through tests
- [[design-patterns]] - Proven solutions

---

## Sharp Edges（常見陷阱）

> 這些是程式碼品質中最常見且代價最高的錯誤

### SE-1: 過度工程 (Over-engineering)
- **嚴重度**: high
- **情境**: 為了「未來可能需要」而增加不必要的抽象和複雜度
- **原因**: YAGNI 原則被忽視、設計模式濫用、「萬一以後要...」的心態
- **症狀**:
  - 簡單功能需要改動 10+ 個檔案
  - 新人看不懂架構
  - 程式碼比需求複雜 10 倍
- **檢測**: `Factory.*Factory|Abstract.*Abstract|interface.*\{.*\}(?=.*interface.*\{.*\})|Strategy.*Strategy`
- **解法**: YAGNI（You Aren't Gonna Need It）、先寫最簡單的實作、需要時再重構

### SE-2: 命名不一致
- **嚴重度**: medium
- **情境**: 同一個概念在不同地方用不同名稱，或不同概念用相似名稱
- **原因**: 沒有統一術語、多人開發沒有對齊、複製貼上沒改名
- **症狀**:
  - `user`, `customer`, `client`, `account` 指同一件事
  - 搜尋不到相關程式碼
  - 新人經常問「這個和那個有什麼差別？」
- **檢測**: `(user|customer|client|account).*=.*find|(get|fetch|retrieve|load).*User`
- **解法**: 建立術語表（Ubiquitous Language）、Code Review 時檢查命名、重構統一命名

### SE-3: 深層巢狀 (Deep Nesting)
- **嚴重度**: medium
- **情境**: if-else 或 callback 巢狀超過 3-4 層，難以閱讀
- **原因**: 沒有提早 return、沒有抽取函數、callback hell
- **症狀**:
  - 需要橫向捲動才能看到程式碼
  - 很難追蹤哪個 `}` 對應哪個 `{`
  - Cyclomatic complexity 超高
- **檢測**: `\{.*\{.*\{.*\{|if.*if.*if.*if|\.then\(.*\.then\(.*\.then\(`
- **解法**: Guard clause（提早 return）、抽取函數、使用 async/await 取代 callback

### SE-4: 神奇數字/字串 (Magic Numbers)
- **嚴重度**: medium
- **情境**: 程式碼中直接使用意義不明的數字或字串
- **原因**: 懶得定義常數、「只用一次不用抽出來」
- **症狀**:
  - 看到 `86400` 不知道是什麼（一天的秒數）
  - 修改時需要全域搜尋 replace
  - 同一個數字在不同地方意義不同但值相同
- **檢測**: `\b(86400|3600|1000|60000|1024|65535)\b|status\s*===?\s*['"][^'"]+['"]`
- **解法**: 抽取為有意義名稱的常數、使用 enum、集中管理設定值

### SE-5: 大泥球 (Big Ball of Mud)
- **嚴重度**: critical
- **情境**: 程式碼沒有明確架構，所有東西混在一起，到處都有依賴
- **原因**: 沒有模組化設計、趕時間「先 work 再說」、缺乏重構
- **症狀**:
  - 改 A 會壞 B
  - 單一檔案 1000+ 行
  - 所有東西都 import 所有東西
- **檢測**: `import.*from.*\.\.\/\.\.\/\.\.\/|require\(.*\.\..*\.\..*\.\.\)|lines.*>\s*1000`
- **解法**: 分層架構、明確的模組邊界、定期重構、嚴格的 import 規則

---

## Validations

### V-1: 禁止 console.log (生產代碼)
- **類型**: regex
- **嚴重度**: medium
- **模式**: `console\.(log|debug|info)\(`
- **訊息**: console.log should not be in production code
- **修復建議**: Use a proper logger (winston, pino) or remove debug statements
- **適用**: `*.ts`, `*.js`

### V-2: 禁止 any 類型
- **類型**: ast
- **嚴重度**: high
- **模式**: `TSAnyKeyword`
- **訊息**: 'any' type defeats TypeScript's type safety
- **修復建議**: Use specific type, 'unknown', or generic type parameter
- **適用**: `*.ts`, `*.tsx`

### V-3: 函數參數過多
- **類型**: regex
- **嚴重度**: medium
- **模式**: `function\s+\w+\s*\([^)]*,\s*[^)]*,\s*[^)]*,\s*[^)]*,\s*[^)]*\)|=>\s*\([^)]*,\s*[^)]*,\s*[^)]*,\s*[^)]*,\s*[^)]*\)`
- **訊息**: Function has more than 4 parameters - consider using an object
- **修復建議**: Replace multiple params with single options object: `function(options: Options)`
- **適用**: `*.ts`, `*.js`

### V-4: TODO 無追蹤
- **類型**: regex
- **嚴重度**: low
- **模式**: `//\s*TODO(?!.*#\d|.*JIRA|.*\w+-\d+)`
- **訊息**: TODO comment without tracking reference
- **修復建議**: Add issue reference: `// TODO(#123): description` or create ticket
- **適用**: `*.ts`, `*.js`, `*.tsx`, `*.jsx`

### V-5: 深層 import 路徑
- **類型**: regex
- **嚴重度**: medium
- **模式**: `import.*from\s+['"]\.\.\/\.\.\/\.\.\/|require\s*\(\s*['"]\.\.\/\.\.\/\.\.\/`
- **訊息**: Deep relative imports indicate poor module boundaries
- **修復建議**: Use path aliases: `import { X } from '@/modules/x'`
- **適用**: `*.ts`, `*.js`, `*.tsx`, `*.jsx`
