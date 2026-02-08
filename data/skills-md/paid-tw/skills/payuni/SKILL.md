---
name: payuni
description: >
  Provides PAYUNi integration overview and guides users to the appropriate skill.
  Use when starting PAYUNi integration, setting up environment, or needing general guidance
  about 統一金流.
argument-hint: "[功能: checkout/query/webhook]"
user-invocable: true
---

# 統一金流整合指南

你的任務是幫助用戶設定統一金流(PAYUNi)環境並引導至適當的串接功能。

## 用戶需求分析

用戶輸入: `$ARGUMENTS`

根據用戶需求，判斷下一步：
- 若包含「串接」「checkout」「建立交易」「UPP」→ 引導使用 `/payuni-checkout`
- 若包含「查詢」「query」「訂單狀態」→ 引導使用 `/payuni-query`
- 若包含「webhook」「回調」「通知」→ 引導使用 `/payuni-webhook`
- 若無特定指定 → 提供以下環境設定引導

## 環境設定檢查

詢問用戶以下問題：

1. **專案框架**：你使用什麼框架？
   - PHP (Laravel / 原生 PHP / 其他)
   - Node.js (Express / Next.js / NestJS / 其他)
   - Python (Django / Flask / FastAPI / 其他)
   - 其他

2. **環境狀態**：是否已有統一金流商店帳號？
   - 是，已有測試環境帳號
   - 是，已有正式環境帳號
   - 否，需要申請

## 環境變數設定

引導用戶建立環境變數：

```bash
PAYUNI_MERCHANT_ID=你的商店代號
PAYUNI_HASH_KEY=你的HashKey
PAYUNI_HASH_IV=你的HashIV
PAYUNI_TEST_MODE=true  # test 模式，正式環境設為 false
```

**指導用戶:**
1. 在專案根目錄建立或編輯 `.env` 檔案
2. 加入上述環境變數
3. 確保 `.env` 已加入 `.gitignore`

## 下一步

完成環境設定後，根據用戶需求引導：

| 需求 | Skill | 說明 |
|------|-------|------|
| 建立支付頁面 | `/payuni-checkout` | UPP 幕前支付串接 |
| 查詢交易狀態 | `/payuni-query` | 交易查詢 API |
| 處理 Webhook | `/payuni-webhook` | 接收付款通知 |

## 環境資訊

| 環境 | API Base URL |
|------|--------------|
| 測試 | `https://sandbox-api.payuni.com.tw` |
| 正式 | `https://api.payuni.com.tw` |

## 支援的支付方式

- **信用卡**: 一次付清、分期付款
- **行動支付**: LINE Pay、Apple Pay、Google Pay
- **ATM**: WebATM、ATM 轉帳
- **超商**: 代碼繳費、條碼繳費

## 重要注意事項

1. HashKey 和 HashIV 必須保密，不可暴露在前端
2. PAYUNi 使用 AES-256-CBC 加密
3. 訂單編號不可重複
4. NotifyURL/ReturnURL 必須是 HTTPS（正式環境）
5. Webhook 需驗證簽名防止偽造

## 與其他金流比較

| 特性 | PAYUNi | 藍新 | 綠界 |
|------|--------|------|------|
| 加密方式 | AES-256-CBC | AES-256-CBC | AES-128-CBC |
| 簽章方式 | SHA256 (HashInfo) | SHA256 (TradeSha) | SHA256 (CheckMacValue) |
| API 版本 | 統一版本 | Version 參數 | Version 參數 |
