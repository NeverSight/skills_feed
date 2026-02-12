---
name: ssl-checker
description: SSL证书检查器是一个用于检查SSL证书有效期的agent技能，它可以检查指定域名的SSL证书是否即将过期，返回检查结果，使用mcp-email发送即将过期的警告邮件给订阅者。
metadata:
  version: 1.0.0
  catalog: operator
  tags: ssl, certificate, monitoring
  author: kit101 <qkssk1711@163.com>
  createAt: 2026-02-02
---
# SSL证书检查器 (SSL Certificate Checker)

## 1. When (触发条件)
当用户明确要求检查某域名的SSL证书有效期时
- 检查your_domain.co的SSL证书有效期
【模糊触发】当用户指令中同时包含「域名」+「有效期」任意组合时，触发本Skill。

## 2. How (执行方式)

### 2.1 步骤
1. **读取参数**: 读取用户想要检查的域名清单和有效期警告阈值（默认30天）
2. **调用检查脚本**: 调用`scripts/ssl-checker.js`，调用方式通过`node scripts/ssl-checker.js`获取脚本使用说明
3. **解析检查结果**: 解析证书检查结果，包括域名、证书相关信息、证书有效期等
4. **判断是否需要发送警告通知**: 根据有效期和警告阈值判断是否需要发送告警通知
5. 若需要告警，则发送警告通知，警告通知发送方式请查看`references/notify.md`

## 3. What (输出结果)
### 3.1 主要输出
- 证书检查报告
- 告警通知结果

### 3.2 输出格式要求
- 严格遵循`references/report-template.txt`

## 功能特性
- 检查单个或多个域名的SSL证书有效期
- 计算证书剩余有效天数
- 识别即将过期的SSL证书（少于30天）
- 返回详细的证书信息（颁发者、有效期等）
- 使用MCP进行结果传递

## 输入参数
- `domains`: 要检查的域名数组（必需）
- `warningThreshold`: 警告阈值（可选，默认30天）

## 使用场景
- 监控线上服务SSL证书状态
- 预防因SSL证书过期导致的服务中断
- 定期检查企业所有域名的SSL证书状态

## 技术要求
- Node.js环境，内置的https模块
- 网络访问权限（用于连接目标服务器）