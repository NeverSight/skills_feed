---
name: payment-help
description: >
  Analyzes user requirements and recommends the best Taiwan payment gateway.
  Provides comparison between NewebPay, ECPay, and PAYUNi based on specific needs.
  Use when choosing a payment solution or comparing 金流服務.
argument-hint: "[業務類型/需求]"
user-invocable: true
---

# 台灣金流選擇與推薦

你的任務是幫助用戶選擇最適合的台灣第三方支付金流服務。

## 了解用戶需求

用戶輸入: `$ARGUMENTS`

根據用戶輸入分析需求，若無明確指定則詢問以下問題：

1. **業務類型**：你的業務類型是什麼？
   - 一般電商（實體商品）
   - 數位商品/服務
   - SaaS 訂閱制
   - 實體店面 + 線上
   - 其他

2. **預計月交易量**：
   - < 100 筆
   - 100-1,000 筆
   - 1,000-10,000 筆
   - > 10,000 筆

3. **需要的功能**（可複選）：
   - 信用卡支付
   - LINE Pay
   - Apple Pay / Google Pay
   - ATM 轉帳
   - 超商代碼/條碼
   - 電子發票
   - 定期定額扣款

## 金流比較分析

| 功能特色 | NewebPay 藍新 | ECPay 綠界 | PAYUNi 統一 |
|---------|--------------|-----------|-------------|
| **市場定位** | 中大型電商 | 台灣最大 | 統一集團 |
| **信用卡** | ✅ | ✅ | ✅ |
| **LINE Pay** | ✅ | ✅ | ✅ |
| **Apple Pay** | ✅ | ✅ | ✅ |
| **Google Pay** | ✅ | ✅ | ✅ |
| **ATM 轉帳** | ✅ | ✅ | ✅ |
| **超商代碼** | ✅ | ✅ | ✅ |
| **電子發票** | ❌ | ✅ 內建 | ❌ |
| **定期定額** | ✅ | ✅ | ✅ |
| **API 文件** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **系統穩定性** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

## 推薦決策樹

```
需要電子發票？
├─ 是 → 推薦 ECPay（內建發票功能）
└─ 否
   ├─ 高流量/穩定性優先？
   │  ├─ 是 → 推薦 NewebPay
   │  └─ 否
   │     ├─ 統一集團相關？
   │     │  ├─ 是 → 推薦 PAYUNi
   │     │  └─ 否 → 三者皆可
   └─ 快速上線？
      └─ 三者整合難度相近
```

## 情境推薦

### 需要電子發票
**推薦: ECPay**
- 金流 + 發票一站整合
- 減少開發工作量
- 使用 `/ecpay` 開始

### 高流量電商 / 穩定性優先
**推薦: NewebPay**
- 系統穩定性高
- API 文件完整
- 使用 `/newebpay` 開始

### 統一集團相關業務
**推薦: PAYUNi**
- 統一企業體系
- 與 7-11 系統整合佳
- 使用 `/payuni` 開始

### 快速上線 / 一般需求
**任一皆可**
- 整合難度相近
- 建議從 NewebPay 開始（文件最完整）

## 可用的 Skills

### NewebPay (藍新金流)

| Skill | 功能 |
|-------|------|
| `/newebpay` | 環境設定與總覽 |
| `/newebpay-checkout` | MPG 支付串接 |
| `/newebpay-query` | 交易查詢 |
| `/newebpay-refund` | 退款處理 |

### ECPay (綠界科技)

| Skill | 功能 |
|-------|------|
| `/ecpay` | 串接指南 |

### PAYUNi (統一金流)

| Skill | 功能 |
|-------|------|
| `/payuni` | 串接指南 |
