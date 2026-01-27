---
name: code-quality
description: Opinionated constraints for writing maintainable, testable code. Apply MTE principles, avoid over-engineering, guide refactoring, and provide code review checklists. Use when users write code, refactor, or need code review. Triggers on keywords like "code quality", "refactor", "review", "MTE", "代码质量", "重构", "审查".
allowed-tools: Read, Write, Glob, Grep, Edit, Bash, AskUserQuestion
---

# Code Quality

编码和重构时的质量约束，确保代码可维护、可测试、适度扩展。

## Language

- Accept questions in both Chinese and English
- Always respond in Chinese

## Trigger Conditions

- 用户正在编写新代码
- 用户需要重构现有代码
- 用户需要 Code Review 检查清单
- 用户提到 MTE 原则、代码质量、避免过度设计

## 核心原则：MTE

所有代码必须遵循 **MTE 原则**：

| 原则 | 说明 | 检查点 |
|------|------|--------|
| **Maintainability** | 可维护性 | 职责单一、依赖清晰、易于理解 |
| **Testability** | 可测试性 | 核心逻辑可单元测试、依赖可 Mock |
| **Extensibility** | 可扩展性 | 预留合理扩展点、接口抽象 |

---

# Part 1: 编码约束

## 模块设计

### 单一职责

```
✅ 正确：一个类/函数只做一件事
- UserService: 用户业务逻辑
- UserRepository: 用户数据访问
- UserValidator: 用户数据校验

❌ 错误：一个类做多件事
- UserManager: 业务逻辑 + 数据访问 + 校验 + 发送邮件
```

### 依赖方向

```
┌─────────────────────────────────────┐
│           Interface Layer           │  ← 薄层，无业务逻辑
├─────────────────────────────────────┤
│           Service Layer             │  ← 业务逻辑（核心）
├─────────────────────────────────────┤
│           Domain Layer              │  ← 领域模型
├─────────────────────────────────────┤
│         Infrastructure Layer        │  ← 可替换
└─────────────────────────────────────┘

依赖规则：
- 外层依赖内层 ✅
- 内层依赖外层 ❌
- 依赖接口，不依赖实现 ✅
```

## 函数设计

### 函数长度

- **建议**：单个函数不超过 30 行
- **最大**：不超过 50 行
- **超过时**：拆分为多个小函数

### 参数数量

- **建议**：不超过 3 个参数
- **最大**：不超过 5 个参数
- **超过时**：使用参数对象

```typescript
// ❌ 参数过多
function createUser(name, email, age, role, department, manager) {}

// ✅ 使用参数对象
function createUser(params: CreateUserParams) {}
```

### 嵌套深度

- **建议**：不超过 2 层嵌套
- **最大**：不超过 3 层嵌套
- **超过时**：提取函数或使用早返回

```typescript
// ❌ 嵌套过深
if (a) {
  if (b) {
    if (c) {
      // ...
    }
  }
}

// ✅ 早返回
if (!a) return;
if (!b) return;
if (!c) return;
// ...
```

## 可测试性设计

> 详细的测试编写规范请参考 `/testing-guide`

### 核心原则

```
可测试代码的三个要素:
1. 依赖可注入 - 外部依赖通过参数传入
2. 纯函数优先 - 业务逻辑无副作用
3. 边界分离 - 业务逻辑与 IO 分离
```

### 依赖注入

```typescript
// ❌ 硬编码依赖
class UserService {
  private db = new Database();
  private mailer = new EmailService();
}

// ✅ 依赖注入
class UserService {
  constructor(
    private db: IDatabase,
    private mailer: IEmailService
  ) {}
}
```

### 纯函数优先

```typescript
// ❌ 有副作用，难测试
function calculateTotal(items) {
  const total = items.reduce((sum, item) => sum + item.price, 0);
  console.log(`Total: ${total}`);  // 副作用
  analytics.track('calculate');     // 副作用
  return total;
}

// ✅ 纯函数，易测试
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}
```

### 边界分离

```typescript
// ❌ 业务逻辑混合 IO
async function processOrder(orderId) {
  const order = await db.findOrder(orderId);  // IO
  if (order.total > 1000) {                   // 业务逻辑
    order.discount = 0.1;
  }
  await db.save(order);                       // IO
  await email.send(order.user, 'confirmed');  // IO
}

// ✅ 分离业务逻辑
function applyDiscount(order) {  // 纯业务逻辑，可测试
  if (order.total > 1000) {
    return { ...order, discount: 0.1 };
  }
  return order;
}

async function processOrder(orderId) {
  const order = await db.findOrder(orderId);
  const updated = applyDiscount(order);  // 调用纯函数
  await db.save(updated);
  await email.send(order.user, 'confirmed');
}
```

> **编写测试时**：参考 `/testing-guide` 获取断言质量、Mock 策略、变异测试等详细指导

## 避免过度设计

### YAGNI 原则

> You Aren't Gonna Need It - 你不会需要它

```typescript
// ❌ 过度设计：为假设需求添加配置
const config = {
  maxRetries: 3,
  retryDelay: 1000,
  enableCache: true,
  cacheExpiry: 3600,
  enableRateLimit: false,  // 从未使用
  rateLimitWindow: 60000,  // 从未使用
  enableMetrics: false,    // 从未使用
  metricsEndpoint: '',     // 从未使用
};

// ✅ 只添加当前需要的配置
const config = {
  maxRetries: 3,
  retryDelay: 1000,
  cacheExpiry: 3600,
};
```

### 抽象时机

```
❌ 过早抽象：
- 只有一个实现就创建接口
- 只有一处使用就提取函数
- 只有两个相似场景就创建基类

✅ 适时抽象（Rule of Three）：
- 3 个以上实现时考虑接口
- 3 处以上重复时考虑提取
- 3 个以上相似场景时考虑基类
```

### 简单方案优先

```typescript
// ❌ 过度设计：简单场景用复杂模式
class UserFactory {
  createAdmin() { return new AdminUser(); }
  createMember() { return new MemberUser(); }
  createGuest() { return new GuestUser(); }
}

// ✅ 简单场景用简单方案
function createUser(role: 'admin' | 'member' | 'guest') {
  return { role, permissions: getPermissions(role) };
}
```

## 设计模式使用

### 使用原则

- **必要时才用**：解决实际问题，不为炫技
- **说明理由**：为什么选择这个模式
- **保持一致**：相同问题用相同模式

### 推荐场景

| 场景 | 推荐模式 | 使用条件 |
|------|----------|----------|
| 对象创建 | Factory / Builder | 创建逻辑复杂、多种类型 |
| 行为扩展 | Strategy / Template | 算法可替换、流程步骤可变 |
| 结构适配 | Facade / Adapter | 简化接口、适配第三方 |
| 状态管理 | State / Observer | 状态驱动、事件通知 |

---

# Part 2: 重构指导

## 重构触发条件

当代码出现以下 **Code Smells** 时考虑重构：

### 必须重构

| 问题 | 指标 | 重构方向 |
|------|------|----------|
| 函数过长 | > 50 行 | 提取函数 |
| 参数过多 | > 5 个 | 参数对象 |
| 嵌套过深 | > 3 层 | 早返回、提取函数 |
| 重复代码 | 3+ 处 | 提取公共逻辑 |
| 上帝类 | > 500 行 | 拆分职责 |

### 建议重构

| 问题 | 描述 | 重构方向 |
|------|------|----------|
| 特性依恋 | 频繁访问其他类数据 | 移动方法 |
| 数据泥团 | 多个参数总是一起出现 | 提取类 |
| 霰弹式修改 | 一个改动影响多处 | 集中逻辑 |
| 平行继承 | 每次加子类要加配套类 | 合并层次 |

## 重构流程

```
1. 确保测试覆盖
   │
   ├── 有测试 → 继续
   └── 无测试 → 先补充测试
   │
   ▼
2. 小步重构
   │
   ├── 每次只改一件事
   ├── 每步都能运行
   └── 每步都运行测试
   │
   ▼
3. 验证行为不变
   │
   ├── 测试全部通过
   └── 手动验证关键路径
   │
   ▼
4. 提交代码
```

## 重构约束

### 安全约束

- [ ] **重构前必须有测试覆盖**
- [ ] **每步重构后运行测试**
- [ ] **不在重构中添加新功能**
- [ ] **不在添加功能时重构**

### 范围约束

- [ ] 单次重构只改一类问题
- [ ] 单次 PR 只包含一个重构主题
- [ ] 大范围重构需要分阶段进行

### 风险评估

| 风险等级 | 条件 | 策略 |
|----------|------|------|
| 低 | 有完善测试、改动局部 | 直接重构 |
| 中 | 部分测试、影响多处 | 先补测试 |
| 高 | 无测试、核心逻辑 | 逐步添加测试后重构 |

---

# Part 3: Code Review 清单

## Review 前置检查

- [ ] PR 描述清晰说明改动内容和原因
- [ ] CI 通过（测试、lint、build）
- [ ] 改动范围合理（单一主题）

## 代码质量检查

### MTE 原则

- [ ] **M - 可维护性**
  - [ ] 函数职责单一
  - [ ] 命名清晰准确
  - [ ] 依赖关系清晰

- [ ] **T - 可测试性**
  - [ ] 核心逻辑有测试
  - [ ] 依赖可以 Mock
  - [ ] 边界条件覆盖

- [ ] **E - 可扩展性**
  - [ ] 预留合理扩展点
  - [ ] 不为假设需求设计
  - [ ] 配置合理

### 代码规范

- [ ] 函数长度 < 50 行
- [ ] 参数数量 < 5 个
- [ ] 嵌套深度 < 3 层
- [ ] 无重复代码
- [ ] 无硬编码敏感信息

### 错误处理

- [ ] 边界条件处理
- [ ] 错误信息有意义
- [ ] 不吞掉异常

### 安全检查

- [ ] 无 SQL 注入风险
- [ ] 无 XSS 风险
- [ ] 敏感数据加密/脱敏
- [ ] 权限控制正确

## Review 反馈分级

| 级别 | 标记 | 含义 | 要求 |
|------|------|------|------|
| 阻塞 | `[Blocker]` | 必须修复才能合并 | 安全问题、逻辑错误 |
| 建议 | `[Suggestion]` | 建议修改但不阻塞 | 代码风格、小优化 |
| 疑问 | `[Question]` | 需要作者解释 | 不理解的设计决策 |
| 赞 | `[Nice]` | 写得好的地方 | 鼓励好的实践 |

---

# Part 4: 应用场景

## 场景 1: 编写新代码

当用户编写新代码时，自动应用以下约束：

1. **模块设计**：检查职责是否单一
2. **函数设计**：检查长度、参数、嵌套
3. **可测试性**：检查依赖是否可注入
4. **避免过度设计**：检查是否 YAGNI

## 场景 2: 重构现有代码

当用户要求重构时：

1. **评估风险**：检查测试覆盖
2. **识别问题**：找出 Code Smells
3. **制定计划**：确定重构步骤
4. **小步执行**：每步运行测试

## 场景 3: Code Review

当用户要求审查代码时：

1. **使用清单**：逐项检查
2. **分级反馈**：区分阻塞和建议
3. **说明理由**：解释为什么这样建议

---

## Constraints

### 编码约束

- [ ] **函数不超过 50 行**
- [ ] **参数不超过 5 个**
- [ ] **嵌套不超过 3 层**
- [ ] **依赖通过注入，不硬编码**
- [ ] **核心逻辑可单元测试**

### 设计约束

- [ ] **每个模块职责单一**
- [ ] **依赖方向：外层依赖内层**
- [ ] **不为假设需求设计**
- [ ] **3 个以上相似场景才抽象**

### 重构约束

- [ ] **重构前必须有测试**
- [ ] **每步重构后运行测试**
- [ ] **不在重构中添加功能**

### Review 约束

- [ ] **区分阻塞和建议**
- [ ] **反馈需要说明理由**
- [ ] **安全问题必须阻塞**
