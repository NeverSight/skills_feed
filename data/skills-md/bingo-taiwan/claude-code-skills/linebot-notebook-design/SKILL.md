---
name: linebot-notebook-design
description: LINE Bot Flex Message 筆記樣式設計指南。包含 Flex Message 限制、卡片結構設計、圖片生成規範（matplotlib）、常見錯誤排解。適用於教育類、知識卡片類的 LINE Bot 開發。
---

# LINE Bot Flex Message 筆記樣式設計指南

## 概述

本 skill 記錄 LINE Bot Flex Message 圖文筆記的設計規範與最佳實踐，以「元素週期表筆記」專案為範例。適用於教育類、知識卡片類的 LINE Bot 開發。

## LINE Bot Flex Message 限制

| 項目 | 限制 |
|------|------|
| JSON 大小 | 最大 **50KB** |
| Carousel 卡片數 | 最多 **12 張** |
| Box 巢狀層級 | 最多 **10 層** |
| 單張卡片寬度 | 建議 **280px** |
| Hero 圖片比例 | 建議 **4:3** 或 **16:9** |
| **Hero aspectMode** | 只支援 **"cover"** 或 **"fit"**（不支援 "contain"！） |
| Button label | 最多 **20 字元**（超過會截斷） |
| 圖片格式 | JPEG, PNG（不支援 GIF 動圖） |
| 圖片大小 | 建議 < **300KB** |
| 圖片來源 | 必須是 **HTTPS** URL |

### aspectMode 血淚教訓

LINE API 回傳 HTTP 400 錯誤：
```json
{"message":"invalid property","property":"/contents/1/hero/aspectMode"}
```

**原因**：使用了 `"aspectMode": "contain"`，但 LINE hero 圖片只支援：
- `"cover"` - 填滿區域，可能裁切
- `"fit"` - 完整顯示，可能留白

**修正**：將所有 `"contain"` 改為 `"fit"`

### 不支援的屬性（重要！）

LINE Flex Message **不支援**以下屬性，使用會導致 HTTP 400 錯誤：

| 不支援屬性 | 解決方案 |
|-----------|----------|
| `borderWidth` | 移除，改用 `separator` |
| `borderColor` | 移除，改用 `backgroundColor` |
| `aspectMode: "contain"` | 改用 `"fit"` |
| CSS 動畫 | 不支援 |
| SVG 嵌入 | 不支援 |

### Bubble Size 限制

| Size | 最大高度 | 適用場景 |
|------|---------|---------|
| nano | ~120px | 極小卡片 |
| micro | ~165px | 小型通知 |
| kilo | ~300px | 一般用途 |
| mega | ~450px | 內容較多 |
| **giga** | ~600px | **最大尺寸** |

**注意**：內容超過限制時會被截斷，按鈕可能無法顯示！

---

## 卡片結構設計

### 標準 Flex Message 卡片結構

```
┌─────────────────────────┐
│       Hero 區域          │  ← 圖片或漸層背景
│    （圖片/符號/標題）     │
├─────────────────────────┤
│       Content 區域       │
│  ┌───────────────────┐  │
│  │ 標題 + 副標題      │  │
│  └───────────────────┘  │
│  ┌───────────────────┐  │
│  │ 資訊表格/內文      │  │
│  └───────────────────┘  │
│  ┌───────────────────┐  │
│  │ 化學式/重點框      │  │
│  └───────────────────┘  │
│  ┌───────────────────┐  │
│  │ 標籤/按鈕          │  │
│  └───────────────────┘  │
└─────────────────────────┘
```

### Hero 區域設計

**配色建議（Material Design）**：

| 用途 | 淺色 | 深色 |
|------|------|------|
| 紅/粉 | #FFCDD2 | #EF9A9A |
| 橘 | #FFE0B2 | #FFCC80 |
| 藍 | #BBDEFB | #90CAF9 |
| 綠 | #C8E6C9 | #A5D6A7 |
| 紫 | #E1BEE7 | #CE93D8 |
| 青 | #B2EBF2 | #80DEEA |

### 色塊模擬技巧

用 Box + backgroundColor 模擬色塊：

```php
[
    'type' => 'box',
    'layout' => 'vertical',
    'contents' => [],
    'width' => '28px',
    'height' => '28px',
    'backgroundColor' => '#FF5733',
    'cornerRadius' => '6px',
]
```

### 導航按鈕設計

**Flex Message JSON 實作**：

```json
{
  "type": "separator",
  "margin": "lg"
},
{
  "type": "box",
  "layout": "horizontal",
  "contents": [
    {
      "type": "button",
      "action": {
        "type": "message",
        "label": "📋 元素目錄",
        "text": "元素目錄"
      },
      "style": "primary",
      "height": "sm",
      "flex": 1
    },
    {
      "type": "button",
      "action": {
        "type": "message",
        "label": "下一個 ➡️",
        "text": "元素 2"
      },
      "style": "secondary",
      "height": "sm",
      "flex": 1,
      "margin": "sm"
    }
  ],
  "margin": "lg"
}
```

### 兩欄按鈕設計（重要教育原則）

當元素數量較多時，使用兩欄按鈕可節省空間。

**閱讀順序原則**：必須是「由上到下」（先左欄再右欄），不是「由左至右」！

```
正確（由上到下）：        錯誤（由左至右）：
21 Sc | 39 Y             21 Sc | 22 Ti
22 Ti | 40 Zr            23 V  | 24 Cr
23 V  | 41 Nb            25 Mn | 26 Fe
...                      ...
閱讀：21→22→23...→39→40   閱讀：21→22→23→24...
```

**奇數元素處理**：最後一個元素旁邊加 `filler` 佔位。

```json
{
  "type": "box",
  "layout": "horizontal",
  "contents": [
    {
      "type": "button",
      "action": { "label": "71 Lu 鎦", "text": "元素 71" },
      "style": "secondary",
      "flex": 1
    },
    {
      "type": "filler",
      "flex": 1
    }
  ]
}
```

---

## 圖片生成規範（matplotlib）

### 基本設定

```python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

# 中文字體（必須）
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
```

### 圖片尺寸標準

| 用途 | figsize | DPI | 輸出尺寸 |
|------|---------|-----|----------|
| 一般圖片 | (14, 10) | 150 | ~2100×1500px |
| 週期表 | (14, 7) | 120 | ~1680×840px |
| 小圖示 | (2, 2) | 150 | ~300×300px |

### 字體大小標準（LINE Bot 手機可讀）

```python
FONT_TITLE = 30   # 主標題、單字元元素符號
FONT_LARGE = 22   # 雙字元元素符號
FONT_MEDIUM = 18  # 一般文字
FONT_SMALL = 14   # 次要資訊（最小值）
```

**重要**：LINE Bot 圖片在手機上**無法放大**，字體必須足夠大！

### 儲存函數

```python
def save_fig(fig, filename):
    """儲存圖片"""
    filepath = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(filepath, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none', pad_inches=0.02)
    plt.close(fig)
    print(f"已儲存: {filename}")
```

---

## 常見錯誤與修正

### 1. Text 欄位不能為空字串

**症狀**：LINE Bot 無反應，API 回傳 HTTP 400

```json
// ❌ 錯誤：空字串會導致 HTTP 400
{"type": "text", "text": ""}

// ✅ 正確：使用佔位符
{"type": "text", "text": "－"}
```

### 2. 長文字必須加 wrap: true

```json
// ❌ 錯誤：長文字會被截斷
{"type": "text", "text": "很長的化學式..."}

// ✅ 正確：允許折行
{"type": "text", "text": "很長的化學式...", "wrap": true}
```

### 3. Button label 太長

改用 Box + Text（支援折行）：

```php
// ✅ 改用 box + text
['type' => 'box', 'contents' => [
    ['type' => 'text', 'text' => '很長的文字...', 'wrap' => true]
], 'action' => [...]]
```

### 4. LINE 圖片快取問題

更新圖片後 LINE 仍顯示舊版時，在 URL 加上版本參數：

```json
"image_url": "https://lt4.mynet.com.tw/linebot/images/H.png?v=2"
```

### 5. matplotlib 特殊字符顯示為方框

某些 Unicode 字符在微軟正黑體中不支援：

| 問題字符 | 解決方案 |
|----------|----------|
| − (U+2212) | 改用 `-` (普通連字符) |
| ₂ (U+2082) | 改用 `2` (普通數字) |
| ₃ (U+2083) | 改用 `3` (普通數字) |

### 6. 診斷 LINE API 錯誤

當 LINE Bot 按鈕無反應時：

**1. 檢查 debug.log**：
```bash
tail -50 /path/to/linebot/debug.log
```

**2. 解讀 property 路徑**：
- `/contents/0/body/contents/5/contents/1/text`
- 代表 → carousel 第 1 張卡片 → body → 第 6 個元素 → 第 2 個子元素 → text

**3. 常見 HTTP 狀態碼**：
| 狀態碼 | 原因 |
|--------|------|
| 400 | JSON 格式錯誤或欄位無效 |
| 401 | Channel Access Token 過期 |
| 429 | 請求次數超限 |

---

## 檔案命名規範

### 圖片檔案

```
# 週期表（每個元素一張，高亮該元素）
periodic_table_{symbol}.png
例：periodic_table_H.png, periodic_table_He.png

# 價電子圖
electron_{symbol}.png
例：electron_H.png, electron_He.png

# 內容圖片
{element}_{topic}.png
例：H_combustion.png, H_fuel_cell.png
```

### JSON 資料檔

```
# 元素筆記資料
elements/{atomic_number}_{symbol}.json
例：elements/001_H.json, elements/002_He.json

# 目錄資料
menu/groups.json
```

---

## 導航流程設計

```
主選單
    │
    ▼
元素目錄（按族分類 Carousel）
    │
    ├── 1A族 → [H] [Li] [Na] [K] ...
    ├── 2A族 → [Be] [Mg] [Ca] ...
    └── ...
          │
          ▼
    元素筆記（4張卡片 Carousel）
          │
          ├── 卡片1: 基本資訊
          ├── 卡片2: 特性1
          ├── 卡片3: 特性2
          └── 卡片4: 特性3 + 導航按鈕
                      │
                      ├── [⬅️ 上一個] [➡️ 下一個]
                      ├── [📋 元素目錄]
                      └── [🏠 主選單]
```

---

## 相關 Skills

- `linebot-architecture`：LINE Bot 架構規範（憲法）
- `quiz-builder`：題庫系統專用指南
- `linebot-setup`：LINE Bot Messaging API 設定與除錯
