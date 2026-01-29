---
name: gemini-watermark-remove
description: 移除 Google Gemini(Nano Banana)生成圖片中的浮水印，使用逆向 Alpha 混合演算法精確還原被覆蓋的像素
---
# Gemini 浮水印移除工具

移除 Google Gemini AI 生成圖片中的浮水印。完全在本地執行，無需上傳圖片至任何伺服器。

## 使用方式

### 方式一：npx（推薦）

```powershell
# 直接執行，無需安裝
npx gemini-watermark-remove <圖片路徑>

# 範例
npx gemini-watermark-remove image.png
npx gemini-watermark-remove image.png --output clean.png
npx gemini-watermark-remove image.png --mode large --gain 1.5
```

### 方式二：Node.js（npx 失敗時使用）

若 npx 執行失敗，可改用 Node.js 直接執行腳本：

```powershell
# 1. 先安裝相依套件
cd <skill目錄>
npm install

# 2. 執行腳本
node scripts/remove-watermark.js <圖片路徑>

# 範例
node scripts/remove-watermark.js image.png
node scripts/remove-watermark.js image.png --output clean.png
node scripts/remove-watermark.js image.png --mode large --gain 1.5
```

### 參數

| 參數             | 說明                                    | 預設值                    |
| ---------------- | --------------------------------------- | ------------------------- |
| `-o, --output` | 輸出檔案路徑                            | `{檔名}_clean.{副檔名}` |
| `-m, --mode`   | 遮罩模式:`auto`, `small`, `large` | `auto`                  |
| `-g, --gain`   | Alpha 增益值 (1.0-3.0)                  | `1.0`                   |

### 批次處理

```powershell
Get-ChildItem "*.png" | ForEach-Object { npx gemini-watermark-remove $_.FullName }
```

## 技術原理

**逆向 Alpha 混合演算法**：`原始像素 = (當前像素 - α × 浮水印顏色) / (1 - α)`

- **≤1024px**: 48×48 遮罩，邊距 32px
- **>1024px**: 96×96 遮罩，邊距 64px

## 連結

- npm: https://www.npmjs.com/package/gemini-watermark-remove
- GitHub: https://github.com/kevintsai1202/GeminiWatermarkRemoveSkill

## 授權

MIT License
