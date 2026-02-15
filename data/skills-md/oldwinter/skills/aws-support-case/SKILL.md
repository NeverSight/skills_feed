---
name: aws-support-case
description: This skill should be used when users need to manage AWS Support cases via CLI. It handles listing cases (recent 2 weeks, unresolved), viewing case details with bilingual display (English-Chinese line by line), creating new cases with auto-detected service/category, replying to cases, and attachment handling. Triggers on requests mentioning "AWS support", "support case", "工单", "support ticket", or AWS technical support inquiries.
---

# AWS Support Case Manager

## Overview

Manage AWS Support cases through CLI with intelligent features: auto-detect service/category when creating cases, translate Chinese to English for submissions, and display case communications in bilingual format (English original followed by Chinese translation).

## Prerequisites

- AWS CLI configured with default profile
- AWS Support API access (requires Business or Enterprise Support plan for some features)
- All commands must use `--region us-east-1` (Support API only available in this region)

## Core Workflows

### 1. List Cases

**List recent 2 weeks cases:**
```bash
aws support describe-cases \
  --region us-east-1 \
  --after-time "$(date -u -v-14d '+%Y-%m-%dT%H:%M:%SZ' 2>/dev/null || date -u -d '14 days ago' '+%Y-%m-%dT%H:%M:%SZ')" \
  --include-resolved-cases \
  --output json
```

**List unresolved cases only:**
```bash
aws support describe-cases \
  --region us-east-1 \
  --no-include-resolved-cases \
  --output json
```

**Display format:** Present cases in a clear table with columns: Case ID | Subject | Status | Created | Severity

### 2. View Case Details (Bilingual Display)

To view a case with communications:
```bash
aws support describe-communications \
  --region us-east-1 \
  --case-id "case-XXXXXXXX" \
  --output json
```

**Bilingual Display Format:** When displaying case communications, format each message as follows:

```
---
[Sender] | [Timestamp]
---

> Original English text line 1
> 中文翻译第一行

> Original English text line 2
> 中文翻译第二行

---
```

Translation guidelines:
- Translate each sentence/paragraph, placing English original first with `>` prefix
- Chinese translation immediately follows on the next line with `>` prefix
- Preserve technical terms (service names, error codes, ARNs) without translation
- Maintain formatting (bullet points, numbered lists) in both languages

### 3. Create New Case

**Step 1: Query available services and categories**
```bash
aws support describe-services --region us-east-1 --output json
```

**Step 2: Auto-detect service and category**

Analyze the user's description (Chinese or English) to identify:
- **Service code**: Match keywords to AWS services (e.g., "EC2实例" → `amazon-ec2`, "S3存储桶" → `amazon-s3`)
- **Category code**: Match issue type (e.g., "性能慢" → `performance`, "无法连接" → `connectivity`, "配额提升" → `limits`)

**Step 3: Translate and create**

If user provides Chinese description:
1. Translate to professional, native English
2. Use technical AWS terminology appropriately
3. Keep specific identifiers (account IDs, resource ARNs, error codes) unchanged

```bash
aws support create-case \
  --region us-east-1 \
  --subject "Translated English subject" \
  --communication-body "Translated English description with full details" \
  --service-code "detected-service" \
  --category-code "detected-category" \
  --severity-code "low|normal|high|urgent|critical" \
  --language "en"
```

**Severity selection guide:**
| Severity | When to use |
|----------|-------------|
| low | General questions, non-urgent inquiries |
| normal | Production system has minor issues |
| high | Production system significantly impaired |
| urgent | Production system severely impaired |
| critical | Production system down (Enterprise only) |

### 4. Reply to Case

**Step 1: Translate if needed**

If user provides Chinese reply, translate to professional English while preserving:
- Technical details and identifiers
- Specific error messages or logs
- Resource names and ARNs

**Step 2: Send reply**
```bash
aws support add-communication-to-case \
  --region us-east-1 \
  --case-id "case-XXXXXXXX" \
  --communication-body "Translated English reply"
```

### 5. Handle Attachments

**Upload attachment:**
```bash
# First, base64 encode the file
BASE64_DATA=$(base64 -i /path/to/file)

# Add to attachment set
aws support add-attachments-to-set \
  --region us-east-1 \
  --attachments fileName="filename.ext",data="$BASE64_DATA"
```

This returns an `attachmentSetId` to use when replying:
```bash
aws support add-communication-to-case \
  --region us-east-1 \
  --case-id "case-XXXXXXXX" \
  --communication-body "Please see the attached file" \
  --attachment-set-id "ATTACHMENT_SET_ID"
```

**Download attachment:**
```bash
aws support describe-attachment \
  --region us-east-1 \
  --attachment-id "attachment-id"
```

### 6. Close/Resolve Case

```bash
aws support resolve-case \
  --region us-east-1 \
  --case-id "case-XXXXXXXX"
```

## Service Detection Keywords

| Keywords (CN/EN) | Service Code |
|------------------|--------------|
| EC2, 实例, 虚拟机 | amazon-ec2 |
| S3, 存储桶, 对象存储 | amazon-s3 |
| RDS, 数据库, MySQL, PostgreSQL | amazon-rds |
| Lambda, 函数, 无服务器 | aws-lambda |
| VPC, 网络, 子网, 安全组 | amazon-vpc |
| ECS, 容器, Docker | amazon-ecs |
| EKS, Kubernetes, K8s | amazon-eks |
| CloudFront, CDN, 分发 | amazon-cloudfront |
| Route53, DNS, 域名 | amazon-route53 |
| IAM, 权限, 角色, 策略 | aws-iam |
| 账单, 费用, billing | aws-billing |
| 账户, 账号, account | account-management |

## Category Detection Keywords

| Keywords (CN/EN) | Category Code |
|------------------|---------------|
| 咨询, 指导, 如何, how to | general-guidance |
| 慢, 性能, 延迟, performance, latency | performance |
| 连接, 访问, 超时, connect, timeout | connectivity |
| 安全, 漏洞, security | security |
| 配置, 设置, configuration | configuration |
| 限额, 配额, 提升, limit, quota | limits |

## Resources

Refer to `references/aws-support-cli-reference.md` for complete CLI command reference and additional options.
