---
name: i18n-workflow
description: 多語言國際化開發流程與規範
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: internationalization
---

## 我的功能

- 提供多語言開發的標準化流程
- 確保五種語言 (繁中、簡中、英、日、韓) 的一致性
- 管理翻譯檔案的新增、更新和維護
- 協助實現語言持久化和即時切換

## 何時使用我

在以下情況下使用此技能：

- 新增使用者可見的文字或訊息時
- 修改現有文字內容時
- 新增新功能需要多語言支援
- 檢查翻譯完整性和一致性
- 設定語言切換功能

## 支援語言

本專案支援五種語言：

- **繁體中文 (zh-TW)** - 預設語言
- **簡體中文 (zh-CN)**
- **英文 (en)**
- **日文 (ja)**
- **韓文 (ko)**

## 檔案結構

```
src/i18n/
├── config.ts               # i18next 配置
└── locales/
    ├── zh-TW.json         # 繁體中文（預設）
    ├── zh-CN.json         # 簡體中文
    ├── en.json            # 英文
    ├── ja.json            # 日文
    └── ko.json            # 韓文
```

## 使用 i18next

### 在元件中使用

```typescript
'use client';

import { useTranslation } from 'react-i18next';

export default function Component() {
  const { t } = useTranslation();

  return (
    <div>
      <h1>{t('common.appName')}</h1>
      <p>{t('stats.speed')}</p>
      <button>{t('actions.save')}</button>
    </div>
  );
}
```

### 語言切換

```typescript
'use client';

import { useTranslation } from 'react-i18next';
import { useAtom } from 'jotai';
import { languageAtom } from '@/store/dataAtoms';

export default function LanguageSelector() {
  const { i18n } = useTranslation();
  const [language, setLanguage] = useAtom(languageAtom);

  const handleLanguageChange = (lang: string) => {
    i18n.changeLanguage(lang);
    setLanguage(lang as SupportedLanguage);
  };

  return (
    <select
      value={language}
      onChange={(e) => handleLanguageChange(e.target.value)}
    >
      <option value="zh-TW">繁體中文</option>
      <option value="zh-CN">简体中文</option>
      <option value="en">English</option>
      <option value="ja">日本語</option>
      <option value="ko">한국어</option>
    </select>
  );
}
```

## 新增翻譯流程

### 重要原則

⚠️ **必須同時更新所有五個語言檔案**

每次新增或修改翻譯時，必須確保所有語言檔案都有對應的翻譯內容。

### 步驟

#### 1. 確定翻譯 Key 結構

使用點號分隔的命名空間結構：

```
category.subcategory.key
```

範例：

- `common.appName` - 通用類別的應用程式名稱
- `stats.speed` - 統計類別的速度
- `actions.save` - 動作類別的儲存

#### 2. 在所有語言檔案中新增翻譯

```json
// zh-TW.json
{
  "newFeature": {
    "title": "新功能標題",
    "description": "新功能說明",
    "button": "確認"
  }
}

// zh-CN.json
{
  "newFeature": {
    "title": "新功能标题",
    "description": "新功能说明",
    "button": "确认"
  }
}

// en.json
{
  "newFeature": {
    "title": "New Feature Title",
    "description": "New feature description",
    "button": "Confirm"
  }
}

// ja.json
{
  "newFeature": {
    "title": "新機能タイトル",
    "description": "新機能の説明",
    "button": "確認"
  }
}

// ko.json
{
  "newFeature": {
    "title": "새 기능 제목",
    "description": "새 기능 설명",
    "button": "확인"
  }
}
```

#### 3. 在元件中使用

```typescript
'use client';

import { useTranslation } from 'react-i18next';

export default function NewFeature() {
  const { t } = useTranslation();

  return (
    <div>
      <h2>{t('newFeature.title')}</h2>
      <p>{t('newFeature.description')}</p>
      <button>{t('newFeature.button')}</button>
    </div>
  );
}
```

## 翻譯檔案結構規範

### 命名空間分類

```json
{
  "common": {
    "appName": "應用程式名稱",
    "loading": "載入中...",
    "error": "錯誤訊息"
  },
  "navigation": {
    "home": "首頁",
    "about": "關於",
    "settings": "設定"
  },
  "stats": {
    "speed": "速度",
    "acceleration": "加速度",
    "weight": "重量",
    "handling": "操控性"
  },
  "actions": {
    "save": "儲存",
    "cancel": "取消",
    "confirm": "確認",
    "delete": "刪除"
  },
  "messages": {
    "success": "操作成功",
    "error": "操作失敗",
    "warning": "警告訊息"
  }
}
```

### 保持結構一致

所有語言檔案必須保持相同的 JSON 結構：

```json
// ✅ 正確 - 所有語言有相同的 key
// zh-TW.json
{
  "user": {
    "profile": "個人資料",
    "settings": "設定"
  }
}

// en.json
{
  "user": {
    "profile": "Profile",
    "settings": "Settings"
  }
}

// ❌ 錯誤 - 結構不一致
// zh-TW.json
{
  "user": {
    "profile": "個人資料",
    "settings": "設定"
  }
}

// en.json
{
  "user": {
    "profile": "Profile"
    // 缺少 settings
  }
}
```

## 語言持久化

### 使用 Jotai atomWithStorage

```typescript
// store/dataAtoms.ts
import { atomWithStorage } from "jotai/utils";

export const languageAtom = atomWithStorage<SupportedLanguage>(
  "mario-kart-language",
  "zh-TW",
);
```

### 語言持久化 Hook

```typescript
// hooks/useLanguagePersistence.ts
"use client";

import { useEffect } from "react";
import { useAtom } from "jotai";
import { useTranslation } from "react-i18next";
import { languageAtom } from "@/store/dataAtoms";

export function useLanguagePersistence() {
  const [language] = useAtom(languageAtom);
  const { i18n } = useTranslation();

  useEffect(() => {
    if (language && i18n.language !== language) {
      i18n.changeLanguage(language);
    }
  }, [language, i18n]);
}
```

## 翻譯品質原則

### 1. 準確性

- 翻譯必須準確傳達原意
- 避免使用機器翻譯的生硬表達
- 符合目標語言的語言習慣

### 2. 一致性

- 相同概念使用相同翻譯
- 建立專案術語表
- 統一專有名詞的翻譯

### 3. 簡潔性

- 避免冗長的翻譯
- 使用簡潔清晰的表達
- 考慮 UI 空間限制

### 4. 文化適應

- 考慮不同文化背景
- 避免文化敏感內容
- 適應當地使用習慣

## 動態翻譯

### 帶參數的翻譯

```json
// zh-TW.json
{
  "greeting": "你好，{{name}}！",
  "itemCount": "共 {{count}} 個項目"
}
```

```typescript
// 使用
const { t } = useTranslation();

<p>{t('greeting', { name: '使用者' })}</p>
<p>{t('itemCount', { count: 10 })}</p>
```

### 複數形式處理

```json
// en.json
{
  "items": "{{count}} item",
  "items_other": "{{count}} items"
}
```

```typescript
const { t } = useTranslation();

<p>{t('items', { count: 1 })}</p>  // "1 item"
<p>{t('items', { count: 5 })}</p>  // "5 items"
```

## 檢查清單

在提交翻譯前，請確認：

- [ ] 所有五個語言檔案都已更新
- [ ] JSON 格式正確，沒有語法錯誤
- [ ] 所有語言檔案結構一致
- [ ] 翻譯準確且符合語言習慣
- [ ] 使用 `t()` 函式而非硬編碼文字
- [ ] 語言切換功能正常運作
- [ ] localStorage 正確儲存語言設定
- [ ] 測試所有語言的顯示效果

## 常見問題

### Q: 如何處理長文字翻譯？

A: 將長文字拆分為多個 key，或使用換行符號：

```json
{
  "longText": "這是第一段文字。\n這是第二段文字。"
}
```

### Q: 如何處理 HTML 標籤？

A: 使用 `Trans` 組件：

```typescript
import { Trans } from 'react-i18next';

<Trans i18nKey="richText">
  This is <strong>bold</strong> text.
</Trans>
```

### Q: 如何確保翻譯完整性？

A: 建立自動化腳本檢查所有語言檔案是否有相同的 key 結構。

### Q: 如何處理圖片中的文字？

A: 為不同語言準備不同的圖片，根據當前語言動態載入。

## 測試流程

### 1. 手動測試

```bash
# 啟動開發伺服器
pnpm dev

# 測試步驟：
1. 切換到每種語言
2. 檢查所有頁面的文字顯示
3. 確認語言設定被正確儲存
4. 重新載入頁面確認語言保持
```

### 2. JSON 格式驗證

```bash
# 使用 JSON linter 檢查語法
pnpm lint
```

### 3. 翻譯覆蓋率檢查

建立腳本檢查所有語言檔案的 key 是否一致：

```typescript
// scripts/check-i18n.ts
const fs = require("fs");

const languages = ["zh-TW", "zh-CN", "en", "ja", "ko"];
const locales = {};

languages.forEach((lang) => {
  locales[lang] = JSON.parse(
    fs.readFileSync(`src/i18n/locales/${lang}.json`, "utf-8"),
  );
});

// 檢查 key 一致性
// ... 實作邏輯
```

## 最佳實踐

### 1. 早期國際化

從專案開始就使用 `t()` 函式，避免後期大規模重構。

### 2. 翻譯文件化

建立翻譯指南文件，說明專案特定的術語翻譯。

### 3. 版本控制

使用 Git 追蹤翻譯檔案變更，便於審查和回溯。

### 4. 團隊協作

- 指定語言負責人審核翻譯
- 使用 Pull Request 審查翻譯變更
- 建立翻譯討論群組

### 5. 持續優化

- 收集使用者反饋
- 定期審查和優化翻譯
- 保持翻譯與功能同步更新

## 參考資源

- [i18next 官方文件](https://www.i18next.com/)
- [react-i18next 文件](https://react.i18next.com/)
- [Google 國際化指南](https://developers.google.com/international/)
- [W3C 國際化最佳實踐](https://www.w3.org/International/)
