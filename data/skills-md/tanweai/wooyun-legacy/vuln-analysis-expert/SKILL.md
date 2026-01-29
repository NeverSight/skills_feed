---
name: vuln-analysis-expert
description: WooYun漏洞分析专家系统。基于88,636个真实漏洞案例提炼的元思考方法论、测试流程、利用技巧、绕过方法。覆盖SQL注入、XSS、命令执行、逻辑漏洞、文件上传、未授权访问等主要漏洞类型。当用户进行漏洞挖掘、渗透测试、安全审计、代码审计时触发。
knowledge-base-size: 86MB / 1,978,052行 (15个分类 × 88,636案例)
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - WebSearch
  - Task
user-invocable: true
---

# WooYun 漏洞分析专家系统

```
┌─────────────────────────────────────────────────────────────────┐
│  🎯 知识来源: WooYun 88,636 真实漏洞案例 (2010-2016)             │
│  📊 知识库规模: 8大类型 × 50案例深度分析 = 4,973行方法论          │
│  ⚡ 核心价值: 元思考方法论 + 实战测试流程 + 绕过技巧库            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 一、漏洞类型全景图

| 漏洞类型 | 案例数 | 知识库 | 核心洞察 |
|----------|--------|--------|----------|
| **SQL注入** | 27,732 | [sql-injection.md](knowledge/sql-injection.md) | 代码与数据边界混淆 |
| **XSS跨站** | 7,532 | [xss.md](knowledge/xss.md) | 信任边界突破 |
| **命令执行** | 6,826 | [command-execution.md](knowledge/command-execution.md) | 数据到指令的跃迁 |
| **逻辑漏洞** | 8,292 | [logic-flaws.md](knowledge/logic-flaws.md) | 业务假设与行为偏差 |
| **文件上传** | 2,711 | [file-upload.md](knowledge/file-upload.md) | 执行攻击者代码 |
| **未授权访问** | 14,377 | [unauthorized-access.md](knowledge/unauthorized-access.md) | 访问控制缺失 |
| **信息泄露** | 7,337 | [info-disclosure.md](knowledge/info-disclosure.md) | 敏感数据暴露 |
| **文件遍历** | 2,854 | [file-traversal.md](knowledge/file-traversal.md) | 路径控制突破 |
| **SSRF** | ~3,000 | [ssrf.md](categories/ssrf.md) | 服务端请求伪造 |
| **CSRF** | ~1,200 | [csrf.md](categories/csrf.md) | 跨站请求伪造 |
| **XXE** | ~100 | [xxe.md](categories/xxe.md) | XML外部实体注入 |
| **配置错误** | ~3,500 | [misconfig.md](categories/misconfig.md) | 安全配置缺陷 |
| **RCE** | ~500 | [rce.md](categories/rce.md) | 远程代码执行 |

> **📦 完整案例库**: `categories/` 目录包含全部 88,636 个漏洞的详细提取（86MB）

---

## 二、元思考方法论框架

### 2.1 漏洞本质公式

```
漏洞 = 预期行为 - 实际行为
    = 开发者假设 ⊕ 攻击者输入 → 意外状态

核心问题链:
1. 数据从哪来? (输入源) → GET/POST/Cookie/Header/文件
2. 数据到哪去? (数据流) → 验证→处理→存储→输出
3. 在哪被信任? (信任边界) → 前端/后端/数据库/系统
4. 如何被处理? (处理逻辑) → 过滤/转义/验证/执行
5. 处理后去哪? (输出点) → HTML/SQL/命令/文件
```

### 2.2 攻击面映射模型

```
          ┌─────────────────────────────────────────┐
          │            应用攻击面                    │
          └─────────────────────────────────────────┘
                            │
    ┌───────────────────────┼───────────────────────┐
    │                       │                       │
┌───▼───┐              ┌────▼────┐             ┌────▼────┐
│ 输入层 │              │  处理层  │             │  输出层  │
├────────┤              ├─────────┤             ├─────────┤
│GET参数 │              │输入验证  │             │HTML页面 │
│POST数据│     ──►      │业务逻辑  │     ──►     │JSON响应 │
│Cookie  │              │数据库操作│             │文件下载 │
│HTTP头  │              │文件操作  │             │错误信息 │
│文件上传│              │系统调用  │             │日志记录 │
└────────┘              └─────────┘             └─────────┘
```

### 2.3 漏洞猎人认知层次

```
Level 1: 工具使用者 (10%)
├─ 会用扫描器和自动化工具
├─ 依赖已知漏洞特征
└─ 难以应对定制化场景

Level 2: 模式识别者 (30%)
├─ 识别漏洞代码模式
├─ 理解漏洞触发原理
└─ 能够手工验证

Level 3: 逻辑分析者 (40%)
├─ 理解业务流程
├─ 发现设计缺陷
└─ 组合利用链

Level 4: 创造性思考者 (20%)
├─ 发现新攻击向量
├─ 绕过防护机制
└─ 0day挖掘能力
```

---

## 三、快速参考：漏洞类型速查

### 3.1 SQL注入速查

```
注入点识别:
├─ 高危参数: id, sort_id, username, password, search, keyword
├─ 测试向量: ' " ) ') ") -- # /*
└─ 数据库指纹: @@version(MSSQL) version()(MySQL) v$version(Oracle)

绕过技巧:
├─ 空格: /**/  %09  %0a  ()
├─ 关键字: SeLeCt  sel%00ect  /*!select*/
├─ 等号: LIKE  REGEXP  BETWEEN  IN
└─ 引号: 0x十六进制  char()  concat()

详见: knowledge/sql-injection.md (731行)
```

### 3.2 XSS速查

```
输出点识别:
├─ 用户内容: 昵称、签名、评论、留言
├─ 搜索回显: 搜索框、历史记录
├─ 文件属性: 文件名、描述、alt属性
└─ 邮件内容: 标题、正文、附件名

绕过技巧:
├─ 标签变形: <ScRiPt>  <script/x>  <script\n>
├─ 事件触发: onerror  onload  onmouseover  onfocus
├─ 编码绕过: HTML实体  JS Unicode  URL编码
└─ 协议利用: javascript:  data:  vbscript:

详见: knowledge/xss.md (745行)
```

### 3.3 命令执行速查

```
入口点识别:
├─ 系统命令: ping、traceroute、nslookup功能
├─ 文件操作: 压缩、解压、图片处理
├─ 代码执行: eval、assert、preg_replace(/e)
└─ 框架漏洞: Struts2、WebLogic、JBoss

命令拼接:
├─ Linux: ;  |  ||  &&  `  $()
└─ Windows: &  |  ||  &&

绕过技巧:
├─ 空格: ${IFS}  $IFS$9  %09  <  <>
├─ 关键字: ca\t  ca''t  c$@at  /???/??t
└─ 编码: $(printf "\x63\x61\x74")  `echo Y2F0|base64 -d`

详见: knowledge/command-execution.md (714行)
```

### 3.4 逻辑漏洞速查

```
漏洞模式:
├─ 密码重置: 验证码回显、步骤跳过、凭证可控
├─ 越权访问: 水平越权(ID遍历)、垂直越权(角色提权)
├─ 支付逻辑: 金额篡改、数量篡改、优惠叠加
└─ 验证码: 不刷新、可重用、可爆破、客户端验证

测试思路:
├─ 理解业务流程 → 画状态转换图
├─ 识别关键校验 → 哪些参数决定结果
├─ 尝试绕过 → 修改参数/跳过步骤/重放/并发
└─ 验证影响 → 证明危害范围

详见: knowledge/logic-flaws.md (508行)
```

### 3.5 文件上传速查

```
绕过检测:
├─ 前端验证: 修改JS/直接发包
├─ Content-Type: image/gif + PHP代码
├─ 扩展名: .php5 .phtml .pht .php. .php::$DATA
├─ 内容检测: GIF89a + <?php  或图片马
└─ 解析漏洞: /upload/1.asp;.jpg (IIS6)

解析漏洞:
├─ IIS 6.0: /test.asp/1.jpg  test.asp;.jpg
├─ Apache: .php.xxx (未知扩展名)
├─ Nginx: /1.jpg/1.php (cgi.fix_pathinfo)
└─ Tomcat: test.jsp%00.jpg

详见: knowledge/file-upload.md (471行)
```

### 3.6 未授权访问速查

```
访问类型:
├─ 后台未授权: 直接访问/admin /manager /console
├─ API未授权: 接口无鉴权、Token可预测
├─ 服务未授权: Redis/MongoDB/ES/Memcached
└─ IDOR: 水平越权访问他人数据

常见未授权服务:
├─ Redis: 6379 (写SSH公钥/Webshell)
├─ MongoDB: 27017 (数据库直接访问)
├─ Elasticsearch: 9200 (数据泄露/RCE)
├─ Memcached: 11211 (数据泄露)
└─ Docker: 2375 (容器逃逸)

详见: knowledge/unauthorized-access.md (605行)
```

---

## 四、通用渗透测试流程

### 4.1 信息收集阶段

```bash
# 子域名枚举
subfinder -d target.com -o subs.txt
amass enum -d target.com

# 端口扫描
nmap -sV -sC -p- target.com

# 目录枚举
dirsearch -u https://target.com -w wordlist.txt
ffuf -u https://target.com/FUZZ -w wordlist.txt

# JS分析
cat urls.txt | grep "\.js$" | xargs -I{} curl -s {} | grep -E "(api|endpoint|secret)"

# 历史数据
waybackurls target.com | grep "="
```

### 4.2 漏洞探测优先级

```
1. 高危快速检测 (立即验证)
   ├─ SQL注入 (sqlmap --risk=1 --level=1)
   ├─ 命令执行 (ping外带/时间延迟)
   └─ 文件上传 (直接上传PHP)

2. 中危系统检测 (逐一验证)
   ├─ XSS (手工+自动化)
   ├─ 未授权访问 (目录扫描)
   └─ 逻辑漏洞 (业务流程分析)

3. 低危完整覆盖 (补充验证)
   ├─ 信息泄露 (.git/.svn/备份文件)
   ├─ 配置错误 (默认口令/未授权服务)
   └─ 敏感信息 (错误页面/注释)
```

---

## 五、防御视角：常见修复方案

| 漏洞类型 | 核心防御 | 具体措施 |
|----------|----------|----------|
| SQL注入 | 参数化查询 | PreparedStatement/ORM |
| XSS | 输出编码 | HTML实体编码/CSP |
| 命令执行 | 避免拼接 | execFile代替exec/白名单 |
| 文件上传 | 严格校验 | 白名单扩展名/重命名/隔离 |
| 未授权 | 访问控制 | 认证+授权+会话管理 |
| 逻辑漏洞 | 服务端校验 | 关键逻辑后端验证 |

---

## 六、工具推荐

### 6.1 自动化扫描

```bash
# SQL注入
sqlmap -u "URL" --batch --random-agent

# XSS
dalfox url "URL" --silence
xsstrike -u "URL"

# 目录扫描
dirsearch -u URL -e php,asp,aspx,jsp
ffuf -u URL/FUZZ -w wordlist.txt -mc 200,301,302

# 漏洞扫描
nuclei -u URL -t cves/
```

### 6.2 手工测试

```bash
# Burp Suite - 代理拦截+重放
# HackBar - 浏览器插件编码解码
# curl - 命令行HTTP请求
# sqlmap --proxy - 配合Burp使用
```

---

## 七、知识库详细索引

| 文件 | 行数 | 内容概要 |
|------|------|----------|
| [sql-injection.md](knowledge/sql-injection.md) | 731 | 注入点识别、数据库指纹、绕过技巧、Payload库 |
| [xss.md](knowledge/xss.md) | 745 | 输出点分类、上下文分析、绕过方法、DOM XSS |
| [command-execution.md](knowledge/command-execution.md) | 714 | 入口点、拼接符、绕过技巧、无回显检测 |
| [logic-flaws.md](knowledge/logic-flaws.md) | 508 | 密码重置、越权、支付、验证码绕过 |
| [file-upload.md](knowledge/file-upload.md) | 471 | 检测绕过、解析漏洞、高危CMS |
| [unauthorized-access.md](knowledge/unauthorized-access.md) | 605 | 后台/API/服务未授权、IDOR |
| [info-disclosure.md](knowledge/info-disclosure.md) | 602 | 泄露类型、敏感路径、利用链 |
| [file-traversal.md](knowledge/file-traversal.md) | 597 | 参数名、Payload编码、敏感文件 |

---

`★ 核心洞察 ─────────────────────────────────────`
**漏洞挖掘的本质是寻找"开发者假设"与"攻击者输入"之间的偏差**

从88,636个真实案例中提炼的关键认知:
1. **边界思维**: 所有漏洞都发生在信任边界上
2. **数据流追踪**: 跟踪数据从输入到输出的完整路径
3. **假设挑战**: 质疑每一个"理所当然"的校验
4. **组合利用**: 单个低危漏洞可组合成高危攻击链

真正的漏洞猎人思考的是"为什么这里会有漏洞"，而不仅仅是"这里有没有漏洞"。
`─────────────────────────────────────────────────`
