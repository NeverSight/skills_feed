---
name: send-email
description: "Send emails via SMTP with support for HTML formatting, file attachments, and email templates. Use when users ask to: (1) Send an email, (2) Email someone, (3) Send a notification, (4) Use email templates, or (5) Send files via email."
dependencies: python>=3.8, markdown>=3.4.0
---

# Send Email

Send emails via SMTP using Python with support for plain text, HTML formatting, file attachments, and template-based emails.

## Key Features

- **Default Sender Email**: Automatically uses `agent_skill_test@126.com` when no sender is specified
- **Automatic Markdown to HTML**: Detects Markdown content and converts to beautifully styled HTML
- **Multiple Email Providers**: Supports Gmail, Outlook, QQ Mail, 163/126 Mail, and custom SMTP
- **File Attachments**: Attach multiple files to emails
- **Email Templates**: Use template files with variable substitution

## Interactive Email Sending Flow

This skill guides you through the email sending process step by step.

### Step 1: Collect Basic Email Information

Ask the user for the following required information. If any is missing, prompt the user to provide it:

| Information | Description | Example |
|-------------|-------------|---------|
| **Recipient** (`--to`) | Email address to send to | `user@example.com` |
| **Subject** (`--subject`) | Email subject line | `Monthly Report` |
| **Content** (`--content`) | Email body text or HTML | `Hello, here is your report.` |

**IMPORTANT - Default Sender Email Behavior**:

**If the user does NOT specify a sender email in their initial request, AUTOMATICALLY use `agent_skill_test@126.com` as the default sender. DO NOT ask the user which email to send from.**

Only ask the user for a different sender email if they explicitly mention wanting to use their own email address.

When using the default `agent_skill_test@126.com`, proceed directly to Step 2 and ask for the 126 email authorization code.

### Step 2: Identify Email Provider and Collect Credentials

Based on the sender's email address domain, identify the email provider and request the appropriate credentials.

#### Email Provider Detection

```
@gmail.com, @googlemail.com   → Gmail
@outlook.com, @hotmail.com, @live.com, @office365.com → Outlook/Office 365
@qq.com, @vip.qq.com          → QQ Mail
@163.com, @126.com            → NetEase Mail
@aliyun.com, @aliyun-inc.com  → Aliyun Mail
@sendgrid.net, @*.sendgrid.net → SendGrid
@*.mailgun.org                → Mailgun
Other domains                  → Custom SMTP (ask for server, port, username, password)
```

#### Provider-Specific Credential Requirements

**Gmail (@gmail.com, @googlemail.com)**
- **Password Type**: App Password (NOT account password)
- **Prerequisite**: Two-factor authentication (2FA) must be enabled
- **How to get App Password**:
  1. Go to https://myaccount.google.com/apppasswords
  2. Sign in to your Google Account
  3. Select "Mail" and "Other (Custom name)" → Enter a name like "SMTP Script"
  4. Click "Generate" → Copy the 16-character password
- **SMTP Server**: `smtp.gmail.com`
- **Port**: `587` (TLS) or `465` (SSL)
- **Username**: Your full Gmail address

**Outlook / Office 365 (@outlook.com, @hotmail.com, @live.com, @office365.com)**
- **Password Type**: Account password (same as web login)
- **SMTP Server**: `smtp.office365.com`
- **Port**: `587` (TLS)
- **Username**: Your full Outlook/Office 365 email address

**QQ Mail (@qq.com, @vip.qq.com)**
- **Password Type**: SMTP Authorization Code (NOT account password)
- **How to get Authorization Code**:
  1. Login to QQ Mail at https://mail.qq.com
  2. Click "Settings" (设置) → "Account" (账户)
  3. Find "POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV Service"
  4. Open "POP3/SMTP Service" or "IMAP/SMTP Service"
  5. Click "Generate Authorization Code" (生成授权码)
  6. Verify identity via SMS → Copy the generated code
- **SMTP Server**: `smtp.qq.com`
- **Port**: `587` (TLS) or `465` (SSL)
- **Username**: Your full QQ email address

**NetEase 163 Mail (@163.com)**
- **Password Type**: SMTP Authorization Code (NOT account password)
- **How to get Authorization Code**:
  1. Login to 163 Mail at https://mail.163.com
  2. Click "Settings" (设置) → "POP3/SMTP/IMAP"
  3. Click "Open" next to "IMAP/SMTP Service"
  4. Verify identity → Click "Get Authorization Code" (获取授权码)
  5. Copy the 16-character authorization code
- **SMTP Server**: `smtp.163.com`
- **Port**: `465` (SSL) or `994` (IMAP)
- **Username**: Your full 163 email address

**NetEase 126 Mail (@126.com)**
- **Password Type**: SMTP Authorization Code (NOT account password)
- **How to get Authorization Code**:
  1. Login to 126 Mail at https://mail.126.com
  2. Click "Settings" (设置) → "POP3/SMTP/IMAP"
  3. Enable "IMAP/SMTP Service"
  4. Copy the authorization password displayed
- **SMTP Server**: `smtp.126.com`
- **Port**: `465` (SSL) or `25` (SSL)
- **Username**: Your full 126 email address

**SendGrid**
- **Password Type**: API Key (as password)
- **How to get API Key**:
  1. Login to SendGrid at https://app.sendgrid.com
  2. Go to Settings → API Keys
  3. Click "Create API Key"
  4. Set permissions → Click "Create & View"
  5. Copy the API key (only shown once)
- **SMTP Server**: `smtp.sendgrid.net`
- **Port**: `587` (TLS) or `465` (SSL)
- **Username**: `apikey` (literally this string)

**Mailgun**
- **Password Type**: SMTP credentials from dashboard
- **How to get Credentials**:
  1. Login to Mailgun at https://app.mailgun.com
  2. Go to Sending → Domains
  3. Select your domain
  4. Copy SMTP username and password from the page
- **SMTP Server**: `smtp.mailgun.org`
- **Port**: `587` (TLS)
- **Username**: From Mailgun dashboard

**Custom SMTP (Other domains)**
Ask the user to provide:
- SMTP Server Address
- SMTP Port
- Username
- Password

### Step 3: Auto-detect and Handle Markdown Content

The script automatically detects if the email content is in Markdown format by looking for common patterns:
- Headers (`#`, `##`, `###`)
- Bold/italic text (`**bold**`, `*italic*`)
- Lists (`- item` or `1. item`)
- Code blocks (```)
- Links (`[text](url)`)

If Markdown is detected, the content is automatically converted to beautifully styled HTML with:
- Professional typography and spacing
- Color-coded headers
- Styled tables and code blocks
- Responsive design for email clients

**You don't need to manually specify `--content-type html` for Markdown content** - it's handled automatically!

### Step 4: Collect Optional Information (if needed)

- `--from-name`: Display name for sender (e.g., "John Doe")
- `--content-type html`: For HTML formatted emails (defaults to plain text, but auto-converts Markdown)
- `--attach`: File path(s) to attach (can specify multiple)
- `--template`: Use template file instead of content
- `--template-vars`: JSON string of template variables

### Step 5: Confirm and Send

Before sending, confirm with the user:

```
Ready to send:
From: [Sender Email]
To: [Recipient Email]
Subject: [Subject]
Content Type: [Plain/HTML]
Attachments: [List of attachments or None]

Proceed to send? (y/n)
```

If confirmed, execute the send_email.py script with all collected parameters.

## Example Conversations

### Example 1: Basic Gmail Email

**User**: Send an email to john@example.com with subject "Hello"

**Skill**: I can help you send that email. I need a few more details:

1. **Content**: What should the email body contain?
2. **Sender Email**: What email address should I send from?

**User**: The content is "Hi John, just saying hello!" and send from myemail@gmail.com

**Skill**: I detected you're using Gmail. For Gmail, you need an App Password (not your regular password).

To get your App Password:
1. Go to https://myaccount.google.com/apppasswords
2. Sign in and create an App Password for "Mail"
3. Copy the 16-character password

**Please provide your Gmail App Password:**

**User**: abcd efgh ijkl mnop

**Skill**: Ready to send:
- From: myemail@gmail.com
- To: john@example.com
- Subject: Hello
- Content: Hi John, just saying hello!

Proceed to send? (y/n)

---

### Example 2: Markdown Content with Default Sender

**User**: 发一封邮件给 manager@company.com,主题是"AR眼镜行业分析",内容是 [用户提供的 Markdown 报告]

**Skill**: 我来帮您发送这封邮件。检测到您没有指定发件人邮箱,我将使用默认邮箱 `agent_skill_test@126.com` 发送。

同时,我发现您的内容是 Markdown 格式,将自动转换为美观的 HTML 格式,让报告更易读。

为了使用 126 邮箱发送,我需要您提供 **SMTP 授权码**。

获取授权码步骤:
1. 登录 126 邮箱 → 设置 → POP3/SMTP/IMAP
2. 启用 "IMAP/SMTP 服务"
3. 复制显示的授权密码

**请提供 agent_skill_test@126.com 的授权码:**

**User**: [提供授权码]

**Skill**: 准备发送邮件:
- 发件人: agent_skill_test@126.com
- 收件人: manager@company.com
- 主题: AR眼镜行业分析
- 格式: Markdown → HTML (自动转换)
- 内容预览: 包含标题、列表、表格等格式化内容

确认发送? (y/n)

---

### Example 3: Default Sender with Missing Content

**User**: 发邮件给 user@company.com，主题是项目报告

**Skill**: 我需要收集邮件内容：

**邮件正文是什么？**

**User**: 项目已完成，所有里程碑都已达成。

**Skill**: 我将使用默认邮箱 `agent_skill_test@126.com` 发送。

为了使用 126 邮箱发送，我需要您提供 **SMTP 授权码**。

获取授权码步骤：
1. 登录 126 邮箱 → 设置 → POP3/SMTP/IMAP
2. 启用 "IMAP/SMTP 服务"
3. 复制显示的授权密码

**请提供 agent_skill_test@126.com 的授权码：**

**User**: [提供授权码]

**Skill**: 准备发送邮件：
- 发件人: agent_skill_test@126.com
- 收件人: user@company.com
- 主题: 项目报告
- 内容: 项目已完成，所有里程碑都已达成。

确认发送？(y/n)

---

### Example 4: User Specifies Custom Sender Email

**User**: Send a report to boss@company.com from myname@outlook.com about Q4 results, with attachment /home/user/q4_report.pdf

**Skill**: I'll help you send that email. Please provide the email content:

**What should the email say about the Q4 results?**

**User**: Please find attached the Q4 financial report. Let me know if you have any questions.

**Skill**: I see you're using Outlook. You'll need your Outlook account password (same as web login).

**Please provide your Outlook password:**

**User**: mypassword123

**Skill**: Ready to send:
- From: myname@outlook.com
- To: boss@company.com
- Subject: Q4 results
- Content: Please find attached the Q4 financial report. Let me know if you have any questions.
- Attachment: /home/user/q4_report.pdf

Proceed to send? (y/n)

---

### Example 5: Custom SMTP

**User**: Send email to test@domain.com from my@domain.com

**Skill**: I need to gather some information:

1. **Subject**: What is the email subject?
2. **Content**: What is the email body?

**User**: Subject is Test Email, content is Hello World

**Skill**: Since you're using a custom domain (my@domain.com), I'll need your SMTP configuration:

1. **SMTP Server**: What is your SMTP server address?
2. **SMTP Port**: What port should I use?
3. **Username**: What is your SMTP username?
4. **Password**: What is your SMTP password?

**User**: Server is smtp.mydomain.com, port 587, username is my@domain.com, password is secret

**Skill**: Ready to send:
- From: my@domain.com
- To: test@domain.com
- Subject: Test Email
- Content: Hello World
- SMTP Server: smtp.mydomain.com:587

Proceed to send? (y/n)

## Script Command Reference

Once all information is collected, execute the script with appropriate parameters:

### Basic Command

```bash
python3 scripts/send_email.py \
  --to recipient@example.com \
  --subject "Email Subject" \
  --content "Email body content" \
  --smtp-server smtp.gmail.com \
  --smtp-port 587 \
  --username your@email.com \
  --password your-password-or-app-password
```

### HTML Email

```bash
python3 scripts/send_email.py \
  --to recipient@example.com \
  --subject "Email Subject" \
  --content "<h1>Hello</h1><p>HTML content</p>" \
  --content-type html \
  --smtp-server smtp.gmail.com \
  --smtp-port 587 \
  --username your@email.com \
  --password your-password
```

### Email with Attachments

```bash
python3 scripts/send_email.py \
  --to recipient@example.com \
  --subject "Email Subject" \
  --content "Email body" \
  --attach /path/to/file1.pdf \
  --attach /path/to/file2.csv \
  --smtp-server smtp.gmail.com \
  --smtp-port 587 \
  --username your@email.com \
  --password your-password
```

### Email with Template

```bash
python3 scripts/send_email.py \
  --to recipient@example.com \
  --subject "Email Subject" \
  --template assets/simple-notification.html \
  --template-vars '{"title":"Notification","message":"Your report is ready!"}' \
  --content-type html \
  --smtp-server smtp.gmail.com \
  --smtp-port 587 \
  --username your@email.com \
  --password your-password
```

### SSL Connection (instead of TLS)

```bash
python3 scripts/send_email.py \
  --to recipient@example.com \
  --subject "Email Subject" \
  --content "Email body" \
  --smtp-server smtp.gmail.com \
  --smtp-port 465 \
  --use-ssl \
  --username your@email.com \
  --password your-password
```

## SMTP Server Configuration Reference

| Provider | SMTP Server | Port | Encryption | Password Type | Username |
|----------|-------------|------|------------|---------------|----------|
| Gmail | smtp.gmail.com | 587 | TLS | App Password | Full email |
| Gmail | smtp.gmail.com | 465 | SSL | App Password | Full email |
| Outlook | smtp.office365.com | 587 | TLS | Account Password | Full email |
| QQ Mail | smtp.qq.com | 587 | TLS | Authorization Code | Full email |
| QQ Mail | smtp.qq.com | 465 | SSL | Authorization Code | Full email |
| 163 Mail | smtp.163.com | 465 | SSL | Authorization Code | Full email |
| 163 Mail | smtp.163.com | 994 | SSL | Authorization Code | Full email |
| 126 Mail | smtp.126.com | 465 | SSL | Authorization Code | Full email |
| 126 Mail | smtp.126.com | 25 | SSL | Authorization Code | Full email |
| SendGrid | smtp.sendgrid.net | 587 | TLS | API Key | `apikey` |
| SendGrid | smtp.sendgrid.net | 465 | SSL | API Key | `apikey` |
| Mailgun | smtp.mailgun.org | 587 | TLS | SMTP Password | From dashboard |

## Installation

Before using this skill, install the required Python dependencies:

```bash
pip install -r requirements.txt
```

This installs the `markdown` library (version ≥3.4.0) which is required for automatic Markdown to HTML conversion.

## Resources

### scripts/send_email.py

Main Python script for sending emails. Supports:
- Plain text and HTML content
- Multiple file attachments
- Email templates with variable substitution
- TLS and SSL encryption
- Custom sender names

### references/smtp-servers.md

Common SMTP server configurations including Gmail, Outlook, 126, QQ, 163, SendGrid, Mailgun, and Aliyun.

### assets/

Email templates:
- `simple-notification.html` - Basic notification template
- `report-summary.html` - Professional report template with metrics grid
