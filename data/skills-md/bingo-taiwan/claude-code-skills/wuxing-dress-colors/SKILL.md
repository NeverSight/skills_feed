---
name: wuxing-dress-colors
description: 五行穿衣功能開發指南。包含天干地支計算、五行穿衣吉凶算法、星座運勢相位計算。當用戶需要：(1) 開發五行相關功能、(2) 農曆/干支計算、(3) 占星學星座運勢時使用此 skill。
---

# 五行穿衣功能開發指南

## 專案資訊（新架構 2026-01-17）

| 項目 | 路徑/URL |
|------|----------|
| **Webhook URL** | `https://lt4.mynet.com.tw/linebot/wuxing/webhook.php` |
| **伺服器路徑** | `/home/lt4.mynet.com.tw/public_html/linebot/wuxing/` |
| **核心程式庫** | `/home/lt4.mynet.com.tw/linebot_core/` |

### 檔案結構

```
/home/lt4.mynet.com.tw/public_html/linebot/wuxing/
├── config.php               # 獨立設定
├── webhook.php              # Webhook 入口
├── handlers/
│   └── MainHandler.php      # 主處理器
├── lunar.php                # 農曆轉換、天干地支計算
├── wuxing.php               # 五行吉凶、星座運勢、Flex Message
└── data/
    ├── sessions.json
    └── analytics.json
```

## 核心算法

### 1. 五行穿衣 - 使用日地支（非日天干）

**重要**：五行穿衣的標準算法是使用「日地支」而非「日天干」。

```
日地支五行對應：
子、亥 → 水
丑、辰、未、戌 → 土
寅、卯 → 木
巳、午 → 火
申、酉 → 金
```

**五行吉凶公式**：
```
大吉色（旺運）= 我生者（當日五行所生的五行）
次吉色（好運）= 與當日五行相同
平平色 = 剋我者
較差色（耗能）= 生我者
不宜色（NG）= 我剋者
```

**五行相生順序**：木 → 火 → 土 → 金 → 水 → 木

**範例計算**：
- 午日（午=火）
- 大吉 = 火生土 → 土（黃色系）✓
- 次吉 = 火 → 火（紅色系）
- 不宜 = 火剋金 → 金（白色系）

**參考來源**：
- CSDN 五行穿衣通用算法：https://blog.csdn.net/ktucms/article/details/144280847

### 2. 星座運勢 - 基於占星學相位理論

使用當日太陽星座計算各星座吉凶：

**相位與吉凶對應**：
| 相位 | 角度 | 元素關係 | 吉凶 |
|------|------|----------|------|
| Trine（三分相） | 120° | 同元素 | 特吉 |
| Sextile（六分相） | 60° | 相容元素 | 次吉 |
| Square（四分相） | 90° | 挑戰元素 | 注意 |

**元素分組**：
- 火象：白羊、獅子、射手
- 土象：金牛、處女、魔羯
- 風象：雙子、天秤、水瓶
- 水象：巨蟹、天蠍、雙魚

**元素相容關係**：
- 火 ↔ 風（相容）
- 土 ↔ 水（相容）
- 火 × 水、土 × 風（挑戰）

**參考來源**：
- Cafe Astrology - Aspects: https://cafeastrology.com/articles/aspectsinastrology.html
- Astrologyk - Element Compatibility: https://astrologyk.com/zodiac/elements/compatibility

## 時區問題

伺服器可能使用 UTC 時區，導致日期計算錯誤。

**解決方案**：在程式開頭設定時區
```php
date_default_timezone_set('Asia/Taipei');
```

## 即時產圖時間參考

| 方法 | 耗時 | 適用場景 |
|------|------|----------|
| Flex Message 色塊 | < 5ms | 簡單色彩展示 ✅ |
| PHP GD 文字圖 | 10-50ms | 動態文字 ✅ |
| QuickChart API | 100-500ms | 圖表 ⚠️ |
| 外部 AI 繪圖 | 5-30秒 | ❌ 需異步 |

**LINE Webhook 建議在 1 秒內回應**

## 關鍵函數

### lunar.php
- `LunarCalendar::solarToLunar($year, $month, $day)` - 西曆轉農曆
- `LunarCalendar::getGanZhi($year, $month, $day)` - 取得干支（含 dayZhiIdx）
- `LunarCalendar::getFullDateInfo()` - 取得完整日期資訊

### wuxing.php
- `WuXing::calculateDressColors($dayZhiIdx)` - 計算五行穿衣顏色
- `WuXing::calculateZodiacHoroscope($month, $day)` - 計算星座運勢
- `WuXing::generateFlexMessage()` - 產生今日 Flex Message
- `WuXing::generateTomorrowFlexMessage()` - 產生明日 Flex Message

## 相關 Skill

- `linebot-architecture`：LINE Bot 架構規範（Flex Message 限制和技巧請參考此 skill）
- `linebot-setup`：LINE Bot 設定與除錯
- `quiz-builder`：題庫系統專用指南
