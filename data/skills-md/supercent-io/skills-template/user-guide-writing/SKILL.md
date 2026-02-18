---
name: user-guide-writing
description: Write clear and helpful user guides and tutorials for end users. Use when creating onboarding docs, how-to guides, or FAQ pages. Handles user-focused documentation, screenshots, step-by-step instructions.
tags: [user-guides, tutorials, documentation, onboarding, how-to, FAQ]
platforms: [Claude, ChatGPT, Gemini]
---

# User Guide Writing


## When to use this skill

- **신규 기능**: 사용자에게 새 기능 소개
- **온보딩**: 신규 사용자 교육
- **FAQ**: 자주 묻는 질문 정리

## Instructions

### Step 1: Quick Start Guide

```markdown
# Getting Started with MyApp

Welcome to MyApp! This guide will help you get up and running in 5 minutes.

## Step 1: Create an Account

1. Go to [https://myapp.com/signup](https://myapp.com/signup)
2. Enter your email and create a password
   - Password must be at least 8 characters
   - Include uppercase, lowercase, and numbers
3. Click "Sign Up"
4. Check your email for verification link
5. Click the link to verify your account

![Sign Up Form](images/signup.png)

## Step 2: Complete Your Profile

1. Click on your avatar in the top-right corner
2. Select "Profile Settings"
3. Add your name and profile picture
4. Click "Save Changes"

## Step 3: Create Your First Project

1. Click the "+ New Project" button
2. Enter a project name
3. Choose a template (or start from scratch)
4. Click "Create"

🎉 Congratulations! You're ready to start using MyApp.

## Next Steps

- [Watch the video tutorial](https://youtube.com/watch?v=xxx)
- [Explore features](docs/features.md)
- [Join our community](https://community.myapp.com)

## Need Help?

- 📧 Email: support@myapp.com
- 💬 Live chat: Available 9 AM - 5 PM EST
- 📚 [Help Center](https://help.myapp.com)
```

### Step 2: How-To Guide (작업 중심)

```markdown
# How to Export Your Data

This guide shows you how to export all your data from MyApp.

## Before You Start

- Exporting data may take 5-10 minutes depending on size
- You'll receive an email when the export is ready
- Exported data is in JSON format

## Step-by-Step Instructions

### 1. Navigate to Settings

Click on your profile picture in the top-right corner and select **Settings**.

![Settings Menu](images/settings-menu.png)

### 2. Go to Data Export

In the left sidebar, click on **Privacy & Data**.

Then scroll down to the **Export Data** section.

![Privacy & Data Page](images/privacy-data.png)

### 3. Request Export

Click the **Request Export** button.

A confirmation dialog will appear:

> **Export Your Data**
>
> We'll send you an email with a download link when your export is ready.
> This usually takes 5-10 minutes.
>
> [Cancel] [Confirm]

Click **Confirm** to proceed.

### 4. Check Your Email

You'll receive an email at your registered address with subject:
**"Your Data Export is Ready"**

The email contains a secure download link that expires in 7 days.

### 5. Download Your Data

Click the download link in the email.

A ZIP file will be downloaded containing:
- `profile.json` - Your profile information
- `projects.json` - All your projects
- `files/` - Uploaded files

## Troubleshooting

**Problem**: I didn't receive the email
- Check your spam folder
- Make sure your email is correct in Settings
- Try requesting again (you can request once per day)

**Problem**: Download link expired
- Request a new export from Settings

**Problem**: Export file is corrupted
- Try downloading again
- If issue persists, contact support@myapp.com

## Related Guides

- [How to Delete Your Account](delete-account.md)
- [Privacy Policy](privacy-policy.md)
- [Data Security](data-security.md)
```

### Step 3: FAQ (자주 묻는 질문)

```markdown
# Frequently Asked Questions (FAQ)

## Account & Billing

### How do I change my email address?

1. Go to **Settings** > **Account**
2. Click **Change Email**
3. Enter your new email and password
4. Click **Update**
5. Verify your new email

### Can I use MyApp for free?

Yes! MyApp has a free tier that includes:
- Up to 3 projects
- 1 GB storage
- Basic features

[Compare plans](https://myapp.com/pricing)

### How do I cancel my subscription?

1. Go to **Settings** > **Billing**
2. Click **Cancel Subscription**
3. Follow the prompts

Your subscription will remain active until the end of the billing period.

## Features

### How do I collaborate with team members?

1. Open your project
2. Click the **Share** button
3. Enter team member's email
4. Choose their permission level (View, Edit, Admin)
5. Click **Send Invite**

They'll receive an email invitation.

### Can I export my projects?

Yes, see our [Export Guide](export-data.md).

### What file formats are supported?

- Images: JPG, PNG, GIF, SVG
- Documents: PDF, DOCX, TXT, MD
- Code: All text files

## Technical

### Is my data secure?

Yes! We use:
- 256-bit SSL encryption
- Regular security audits
- SOC 2 Type II certified
- GDPR compliant

[Read our Security Page](security.md)

### Can I use MyApp offline?

Currently, MyApp requires an internet connection. Offline mode is planned for Q2 2025.

### Browser compatibility?

MyApp works best on:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Still Have Questions?

- 📧 Email: support@myapp.com
- 💬 Live Chat (9 AM - 5 PM EST)
- 🎓 [Video Tutorials](tutorials.md)
- 👥 [Community Forum](https://community.myapp.com)
```

### Step 4: Tutorial (학습 중심)

```markdown
# Tutorial: Build Your First Dashboard

In this tutorial, you'll learn how to create a beautiful dashboard with charts and widgets.

**Time**: 15 minutes
**Difficulty**: Beginner
**Prerequisites**: MyApp account

## What You'll Build

![Final Dashboard](images/tutorial-dashboard.png)

## Step 1: Create a New Dashboard

Click **+ New Dashboard** and name it "Sales Dashboard".

## Step 2: Add a Chart Widget

1. Click **Add Widget** → **Chart**
2. Select **Bar Chart**
3. Configure data source:
   - Data: Monthly Sales
   - X-axis: Month
   - Y-axis: Revenue
4. Click **Add to Dashboard**

![Adding Chart Widget](images/add-chart.gif)

## Step 3: Add a Stats Widget

1. Click **Add Widget** → **Stat Card**
2. Choose metric: Total Revenue
3. Set comparison: vs. Last Month
4. Click **Add to Dashboard**

## Step 4: Arrange Widgets

Drag and drop widgets to arrange them.

**Pro Tip**: Hold Shift while resizing for precise control.

## Step 5: Save and Share

1. Click **Save Dashboard**
2. Click **Share** to invite team members

## Next Steps

Now that you've created your first dashboard, try:

- [Adding filters](filters.md)
- [Scheduling reports](reports.md)
- [Customizing themes](themes.md)

## Congratulations!

You've completed the tutorial. Happy dashboard building! 🎉
```

## Output format

```
docs/
├── getting-started.md      # Quick start
├── how-to/
│   ├── export-data.md
│   ├── invite-team.md
│   └── create-project.md
├── tutorials/
│   ├── first-dashboard.md
│   └── advanced-features.md
├── faq.md
└── images/
    ├── signup.png
    └── dashboard.png
```

## Constraints

### 필수 규칙 (MUST)

1. **스크린샷 포함**: 시각적 가이드
2. **단계별 지침**: 1, 2, 3 형식
3. **사용자 언어**: 전문 용어 지양

### 금지 사항 (MUST NOT)

1. **기술 용어 남발**: API, endpoint 등
2. **긴 문단**: 짧고 명확하게

## Best practices

1. **User-Centric**: 사용자 관점으로 작성
2. **Show, Don't Tell**: 스크린샷, GIF, 비디오
3. **Update Regularly**: UI 변경 시 문서도 업데이트

## References

- [Docs as Code](https://www.writethedocs.org/guide/docs-as-code/)
- [Good Docs Project](https://thegooddocsproject.dev/)

## Metadata

### 버전
- **현재 버전**: 1.0.0
- **최종 업데이트**: 2025-01-01
- **호환 플랫폼**: Claude, ChatGPT, Gemini

### 태그
`#user-guides` `#tutorials` `#documentation` `#onboarding` `#how-to` `#FAQ`

## Examples

### Example 1: Basic usage
<!-- Add example content here -->

### Example 2: Advanced usage
<!-- Add advanced example content here -->
