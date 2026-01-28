---
name: linebot-setup
description: LINE Bot Messaging API 設定與除錯指南。包含 LINE Developers Console 設定、Webhook URL 配置、SSL 憑證要求、常見錯誤排解。當用戶需要：(1) 建立新的 LINE Bot、(2) 設定 Webhook URL、(3) 排解 SSL 連線錯誤、(4) 排解 LINE Bot 無回應問題時使用此 skill。
---

# LINE Bot Messaging API 設定指南

## 快速檢查清單

設定 LINE Bot 前，確認以下條件：

1. **SSL 憑證**: 必須是有效的 CA 簽發憑證（不接受自簽憑證）
2. **憑證鏈完整**: 使用 fullchain.pem，不只是 cert.pem
3. **非 Cloudflare 代理**: LINE 可能無法連接 Cloudflare 代理的網域
4. **PHP 7.0+**: 若使用 PHP，需支援 `??` 運算子
5. **回應時間**: Webhook 必須在數秒內回應 200 OK

## 設定流程

### 1. LINE Developers Console 設定

1. 前往 https://developers.line.biz/console/
2. 建立 Provider（若無）
3. 建立 Messaging API Channel
4. 記錄：
   - **Channel ID**
   - **Channel Secret**（Basic settings）
   - **Channel Access Token**（Messaging API → Issue）

### 2. Webhook 設定

在 Messaging API 頁籤：
1. 設定 **Webhook URL**: `https://your-domain.com/webhook.php`
2. 開啟 **Use webhook**（綠色開關在右邊）
3. 點擊 **Verify** 測試連線

### 3. 關閉自動回應

在 LINE Official Account Manager（從 Console 連結）：
1. 進入「回應設定」
2. 關閉「自動回應訊息」
3. 關閉「加入好友的歡迎訊息」（如不需要）

## 常見錯誤排解

### SSL connection error

**症狀**: Verify 按鈕顯示 "An SSL connection error occurred"

**檢查步驟**:

```bash
# 檢查憑證是否為 CA 簽發
openssl s_client -connect your-domain.com:443 -servername your-domain.com 2>/dev/null | openssl x509 -noout -issuer

# 應顯示 Let's Encrypt、DigiCert 等，不是 self-signed

# 檢查憑證鏈完整性
openssl s_client -connect your-domain.com:443 -servername your-domain.com 2>/dev/null | grep -E "Certificate chain|depth="

# 應顯示 depth=0, depth=1, depth=2（完整鏈）
```

**解決方案**:
- 自簽憑證 → 取得 Let's Encrypt 憑證（見 references/ssl-letsencrypt.md）
- 憑證鏈不完整 → 使用 fullchain.pem 而非 cert.pem
- Cloudflare 代理 → 使用直連 IP 的網域

### Webhook 無回應（僅顯示已讀）

**症狀**: 發送訊息後只顯示已讀，無 Bot 回應

**檢查步驟**:

```bash
# 檢查 Webhook 是否收到請求
tail -f /path/to/webhook/debug.log

# 檢查 PHP 錯誤日誌
tail -f /var/log/apache2/error.log
```

**常見原因**:
1. **LINE 自動回應未關閉** → 到 Official Account Manager 關閉
2. **PHP 版本過低** → 確認 PHP 7.0+
3. **Webhook 回傳 500** → 檢查 PHP 錯誤日誌
4. **簽名驗證失敗** → 確認 Channel Secret 正確

### HTTP 500 錯誤

**檢查 PHP 版本相容性**:

```bash
# 檢查 PHP 版本
php -v

# 若使用 ?? 運算子，需 PHP 7.0+
# PHP 5.x 不支援：$var = $array['key'] ?? 'default';
# 改用：$var = isset($array['key']) ? $array['key'] : 'default';
```

### HTTP 401 Authentication failed

**症狀**: LINE API 回傳 `{"message":"Authentication failed..."}`

**原因**: Channel Access Token 無效或過期

**解決方案**:
1. 前往 LINE Developers Console
2. 進入 Messaging API 頁籤
3. 點擊 **Issue** 或 **Reissue** 產生新 Token
4. 更新 config.php 中的 `LINE_CHANNEL_ACCESS_TOKEN`

### Flex Message 圖片不顯示

**症狀**: 題目或解答應該有圖片但沒有顯示

**檢查步驟**:

```bash
# 確認圖片 URL 可訪問
curl -sI "https://your-domain.com/images/filename.png" | head -3
# 應顯示 HTTP/1.1 200 OK

# 確認圖片目錄存在
ls -la /path/to/images/
```

**常見原因**:
1. **圖片檔案不存在** → 檢查檔案是否已上傳
2. **URL 路徑錯誤** → 確認 JSON 中的 URL 與實際路徑一致
3. **重複加上 BASE_URL** → 如果 JSON 已是完整 URL，程式碼不應再加前綴

**修正程式碼**:
```php
// 判斷是否為完整 URL
$imageUrl = (strpos($q['question_image'], 'http') === 0)
    ? $q['question_image']
    : IMAGE_BASE_URL . '/' . $q['question_image'];
```

## 參考資源

- SSL 憑證取得流程：[references/ssl-letsencrypt.md](references/ssl-letsencrypt.md)
- Webhook PHP 範例：[references/webhook-example.md](references/webhook-example.md)
- LINE 官方文件：https://developers.line.biz/en/docs/messaging-api/
