---
name: nas-account-manager
description: 八德陽德扶輪社 Synology NAS 帳號建立與通知設定。當用戶提到 NAS 帳號、Synology Photos、社友帳號、QuickConnect 設定時使用此 skill。
---

# Synology NAS 社友帳號管理技能

八德陽德扶輪社 NAS 帳號建立與通知設定完整指南

## 重要提醒（必讀）

> ⚠️ **如果要使用 NAS 通知社友 Synology Photos 帳密，必須事前先完成電子郵件設定！**
>
> 事後再設定電子郵件無法批次通知已存在的使用者帳密。
> 「寄送歡迎訊息給新使用者」功能只會在建立新使用者時觸發。

---

## 一、NAS 電子郵件設定（必須先完成）

**路徑：** 控制台 → 通知設定 → 電子郵件

### 方法 A：使用 Gmail OAuth（推薦）

1. 服務提供者選擇「Gmail」
2. 點擊「登入」
3. 在彈出視窗中登入 Google 帳戶並授權
4. 完成後寄件人信箱會自動設定

### 方法 B：使用自訂 SMTP 伺服器

| 欄位 | 設定值 |
|------|--------|
| 服務提供者 | 自訂 SMTP 伺服器 |
| SMTP 伺服器 | smtp.gmail.com |
| SMTP 連接埠 | 587 |
| 需要驗證 | ✓ 勾選 |
| 使用者帳號 | your-email@gmail.com |
| 密碼 | 16位數應用程式密碼 |
| 需要安全連線 (SSL/TLS) | ✓ 勾選 |
| 寄件人信箱 | your-email@gmail.com |

### 取得 Gmail 應用程式密碼

1. 前往 https://myaccount.google.com/security
2. 點擊「兩步驟驗證」並啟用
3. 前往 https://myaccount.google.com/apppasswords
4. 產生應用程式密碼（16位數）

---

## 二、啟用歡迎訊息功能

**路徑：** 控制台 → 通知設定 → 電子郵件

往下滾動找到並勾選：

☑️ **寄送歡迎訊息給新使用者**

---

## 三、建立使用者帳號

**路徑：** 控制台 → 使用者 & 群組 → 使用者帳號

1. 點擊「新增」
2. 填入：
   - 名稱（帳號）
   - 描述（中文姓名）
   - 電子郵件
   - 密碼
3. 設定權限和應用程式存取（確保 Synology Photos 已啟用）
4. 完成建立

> 如果已啟用歡迎訊息，使用者會自動收到包含登入資訊的郵件。

---

## 四、Synology Photos App 下載連結

提供給社友的下載連結：

| 平台 | 連結 |
|------|------|
| iOS | https://apps.apple.com/app/synology-photos/id1484764501 |
| Android | https://play.google.com/store/apps/details?id=com.synology.projectkailash |

### App 登入設定

| 項目 | 值 |
|------|-----|
| QuickConnect ID | ptyt3502 |
| 帳號 | 使用者名稱 |
| 密碼 | 使用者密碼 |

---

## 五、已存在使用者的通知方式

對於已經建立但未收到通知的使用者，需要手動發送郵件：

1. 在「使用者帳號」頁面點擊「匯出」取得 Email 清單
2. 使用 Gmail 或其他郵件工具群發通知

---

## 六、本次設定的 NAS 資訊

| 項目 | 值 |
|------|-----|
| NAS 名稱 | PTYT_NAS |
| QuickConnect ID | ptyt3502 |
| 連線網址 | https://ptyt3502.tw6.quickconnect.to |
| 寄件人信箱 | yangte3500@gmail.com |
| 使用者數量 | 40 位 |

---

## 快速檢查清單

- [ ] 電子郵件設定完成
- [ ] 啟用「寄送歡迎訊息給新使用者」
- [ ] 建立使用者帳號
- [ ] 確認使用者有 Synology Photos 存取權限
- [ ] 提供 App 下載連結給社友

---

文件建立日期：2026/1/2
