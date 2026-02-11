---
name: code-smell-detector
description: Detect code smells including long methods, large classes, duplicated code, and deep nesting. Use when identifying code quality issues or planning refactoring.
---

# Code Smell Detector Skill

コードの問題パターン（コードスメル）を検出するスキルです。

## 概要

保守性を低下させるコードパターンを検出し、リファクタリングを提案します。

## 検出するコードスメル

### 1. Long Method（長すぎるメソッド）

```javascript
// ❌ Bad: 100行のメソッド
function processOrder(order) {
  // 検証ロジック 20行
  // 在庫チェック 15行
  // 価格計算 20行
  // 決済処理 25行
  // メール送信 15行
  // ログ記録 5行
}

// ✅ Good: 分割
function processOrder(order) {
  validateOrder(order);
  checkInventory(order);
  const total = calculateTotal(order);
  processPayment(order, total);
  sendConfirmationEmail(order);
  logOrder(order);
}
```

### 2. Duplicate Code（重複コード）

```python
# ❌ Bad
def calculate_user_discount(user):
    if user.type == 'premium':
        return user.total * 0.9
    elif user.type == 'vip':
        return user.total * 0.8
    return user.total

def calculate_order_price(order):
    if order.user.type == 'premium':
        return order.total * 0.9
    elif order.user.type == 'vip':
        return order.total * 0.8
    return order.total

# ✅ Good
DISCOUNT_RATES = {
    'premium': 0.9,
    'vip': 0.8,
    'regular': 1.0
}

def apply_discount(total, user_type):
    rate = DISCOUNT_RATES.get(user_type, 1.0)
    return total * rate
```

### 3. Large Class（巨大クラス）

```java
// ❌ Bad: 1000行のクラス
class UserManager {
    void createUser() {}
    void updateUser() {}
    void deleteUser() {}
    void sendEmail() {}
    void generateReport() {}
    void processPayment() {}
    void managePermissions() {}
    // ... 50個のメソッド
}

// ✅ Good: 責務を分離
class UserRepository {
    void create(User user) {}
    void update(User user) {}
    void delete(String id) {}
}

class EmailService {
    void send(Email email) {}
}

class PaymentService {
    void process(Payment payment) {}
}
```

### 4. Magic Numbers（マジックナンバー）

```javascript
// ❌ Bad
if (user.age > 18 && user.score >= 75) {
  // ...
}

// ✅ Good
const ADULT_AGE = 18;
const PASSING_SCORE = 75;

if (user.age > ADULT_AGE && user.score >= PASSING_SCORE) {
  // ...
}
```

### 5. Deep Nesting（深いネスト）

```python
# ❌ Bad
def process(data):
    if data:
        if data.valid:
            if data.user:
                if data.user.active:
                    if data.amount > 0:
                        # 処理
                        return True
    return False

# ✅ Good: Early return
def process(data):
    if not data or not data.valid:
        return False

    if not data.user or not data.user.active:
        return False

    if data.amount <= 0:
        return False

    # 処理
    return True
```

### 6. Dead Code（デッドコード）

```typescript
// ❌ Bad
function calculatePrice(item: Item): number {
  const tax = 0.1; // 使われていない
  const oldPrice = item.price * 1.2; // 使われていない

  return item.price;
}

// ✅ Good
function calculatePrice(item: Item): number {
  return item.price;
}
```

### 7. Comment Smell（不適切なコメント）

```java
// ❌ Bad
// このメソッドはユーザーを取得します
public User getUser(String id) {
    // IDでデータベースを検索
    return database.find(id);
}

// ✅ Good: コードで表現
public User findUserById(String id) {
    return userRepository.findById(id);
}
```

### 8. Feature Envy（機能への羨望）

```python
# ❌ Bad: OrderクラスがUserの詳細を知りすぎ
class Order:
    def calculate_discount(self, user):
        if user.type == 'premium':
            return self.total * user.premium_rate
        elif user.type == 'vip':
            return self.total * user.vip_rate
        return self.total

# ✅ Good: Userに責務を移動
class User:
    def get_discount_rate(self):
        rates = {'premium': 0.9, 'vip': 0.8}
        return rates.get(self.type, 1.0)

class Order:
    def calculate_discount(self, user):
        return self.total * user.get_discount_rate()
```

### 9. Primitive Obsession（基本型への執着）

```typescript
// ❌ Bad
function sendEmail(to: string, subject: string, body: string) {
  // ...
}

sendEmail('user@example.com', 'Hello', 'Message');

// ✅ Good
class Email {
  constructor(
    public to: string,
    public subject: string,
    public body: string
  ) {}

  validate(): boolean {
    return /\S+@\S+\.\S+/.test(this.to);
  }
}

function sendEmail(email: Email) {
  if (!email.validate()) {
    throw new Error('Invalid email');
  }
  // ...
}
```

### 10. Switch Statement Smell

```java
// ❌ Bad
public double calculateArea(Shape shape) {
    switch (shape.getType()) {
        case CIRCLE:
            return Math.PI * shape.getRadius() * shape.getRadius();
        case RECTANGLE:
            return shape.getWidth() * shape.getHeight();
        case TRIANGLE:
            return 0.5 * shape.getBase() * shape.getHeight();
    }
    return 0;
}

// ✅ Good: ポリモーフィズム
interface Shape {
    double calculateArea();
}

class Circle implements Shape {
    public double calculateArea() {
        return Math.PI * radius * radius;
    }
}

class Rectangle implements Shape {
    public double calculateArea() {
        return width * height;
    }
}
```

## 検出レポート例

```markdown
## コードスメル検出レポート

### ファイル: user_service.py

#### [HIGH] Long Method
**場所**: Line 45-120 (76行)
**メソッド**: `process_user_registration`
**推奨**: 以下に分割
- `validate_user_data`
- `create_user_account`
- `send_welcome_email`
- `initialize_user_settings`

#### [MEDIUM] Duplicate Code
**場所**: Line 150-165, Line 200-215
**重複度**: 95%
**推奨**: 共通関数 `apply_user_discount` に抽出

#### [LOW] Magic Number
**場所**: Line 78
**コード**: `if age > 18`
**推奨**: `ADULT_AGE = 18` と定数化

### 統計
- Total Code Smells: 12
- High Priority: 3
- Medium Priority: 5
- Low Priority: 4
```

## バージョン情報

- スキルバージョン: 1.0.0
