---
name: newebpay-refund
description: >
  Implements NewebPay refund functionality for credit cards and e-wallets.
  Use when building refund processing, transaction cancellation, or return
  payment features for 藍新金流.
argument-hint: "[類型: 信用卡/電子錢包]"
context: fork
agent: general-purpose
disable-model-invocation: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
user-invocable: true
---

# 藍新金流退款任務

你的任務是在用戶的專案中實作藍新金流退款功能。

## Step 1: 確認退款類型

用戶輸入: `$ARGUMENTS`

詢問用戶：

1. **退款類型**：需要處理什麼類型的退款？
   - 信用卡退款 (CreditCard/Close API)
   - 電子錢包退款 - LINE Pay, 台灣 Pay 等 (EWallet/Refund API)
   - 兩者都需要

2. **退款情境**：
   - 全額退款
   - 部分退款
   - 自動退款（與訂單系統整合）

## Step 2: 確認環境

確認專案已設定 NewebPay 環境變數：
- `NEWEBPAY_MERCHANT_ID`
- `NEWEBPAY_HASH_KEY`
- `NEWEBPAY_HASH_IV`

## Step 3: 建立退款模組

根據退款類型建立對應的功能。

**信用卡退款核心功能:**
- `refundCreditCard(orderNo, amount)` - 信用卡退款

**電子錢包退款核心功能:**
- `refundEWallet(tradeNo, orderNo, amount)` - 電子錢包退款

## Step 4: 整合到應用

建議整合方式：
- **管理後台**: 訂單詳情頁加入退款按鈕
- **API 端點**: `POST /api/orders/:orderNo/refund`
- **退款記錄**: 建立退款記錄表追蹤

---

## 信用卡退款

### API 端點

| 環境 | URL |
|------|-----|
| 測試 | `https://ccore.newebpay.com/API/CreditCard/Close` |
| 正式 | `https://core.newebpay.com/API/CreditCard/Close` |

### PostData_ 內容

| 參數 | 類型 | 必填 | 說明 |
|------|------|:----:|------|
| RespondType | String | ✓ | `JSON` |
| Version | String | ✓ | `1.1` |
| Amt | Number | ✓ | 退款金額 |
| MerchantOrderNo | String | ✓ | 原訂單編號 |
| TimeStamp | Number | ✓ | Unix timestamp |
| IndexType | Number | ✓ | `1` (使用訂單編號) |
| CloseType | Number | ✓ | `2` (退款) |

---

## 電子錢包退款

### API 端點

| 環境 | URL |
|------|-----|
| 測試 | `https://ccore.newebpay.com/API/EWallet/Refund` |
| 正式 | `https://core.newebpay.com/API/EWallet/Refund` |

### PostData_ 內容

| 參數 | 類型 | 必填 | 說明 |
|------|------|:----:|------|
| RespondType | String | ✓ | `JSON` |
| Version | String | ✓ | `1.0` |
| TimeStamp | Number | ✓ | Unix timestamp |
| TradeNo | String | ✓ | 藍新交易序號 |
| MerchantOrderNo | String | ✓ | 原訂單編號 |
| Amt | Number | ✓ | 退款金額 |

---

## 詳細參考文件

- [程式碼範例 (PHP/Node.js)](references/code-examples.md)

---

## 常見錯誤

| 代碼 | 說明 | 解決方式 |
|------|------|---------|
| CRE10001 | 無此交易紀錄 | 確認訂單編號/交易序號正確 |
| CRE10002 | 已退款或取消 | 交易已被處理過 |
| CRE10003 | 退款金額錯誤 | 退款金額不可大於原交易金額 |
| CRE10004 | 超過可退款期限 | 信用卡一般為 180 天內 |

## 注意事項

1. **退款期限**: 信用卡一般為交易後 180 天內
2. **部分退款**: 可退款金額 ≤ 原交易金額
3. **退款次數**: 同一筆交易可多次部分退款
4. **電子錢包**: 需使用藍新交易序號 (TradeNo)
