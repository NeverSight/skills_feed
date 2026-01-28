---
name: customer-workspace
description: Customer workspace initialization skill (Japanese UI). Provides inbox (information accumulation), meeting minutes management, and auto-classification rules. Use for "setup customer workspace" or "add inbox feature" requests.
license: Complete terms in LICENSE.txt
metadata:
  author: yamapan (https://github.com/aktsmm)
---

# Customer Workspace Skill

顧客固有のワークスペースを初期化し、情報蓄積・議事録管理の仕組みを提供。

## When to use

- 顧客ごとのワークスペース初期化が必要なとき
- インボックス機能や議事録管理を追加したいとき
- 顧客情報の整理・自動分類ルールを導入したいとき

## 機能

| 機能                 | 説明                                         |
| -------------------- | -------------------------------------------- |
| **インボックス**     | チャット・メール等を貼るだけで自動分類・蓄積 |
| **議事録管理**       | Teams AI議事録→テンプレート変換              |
| **自動判定**         | 入力パターンから処理を自動振り分け           |
| **顧客プロファイル** | 顧客情報を一元管理                           |

---

## クイックスタート

### スクリプトで初期化（推奨）

```powershell
# 基本
.\scripts\Initialize-CustomerWorkspace.ps1 -CustomerName "ABC株式会社様"

# フルオプション
.\scripts\Initialize-CustomerWorkspace.ps1 `
  -CustomerName "ABC株式会社様" `
  -ContractType "MACC" `
  -ContractPeriod "2025/04 - 2028/03" `
  -KeyContacts "山田さん（インフラ担当）"
```

### 生成されるファイル

```
{workspace}/
├── .github/
│   ├── copilot-instructions.md    ← 自動判定ルール
│   └── prompts/                   ← inbox, 議事録変換
├── _inbox/{YYYY-MM}.md            ← インボックス
├── _customer/profile.md           ← 顧客プロファイル
└── _templates/                    ← テンプレート
```

---

## 日常運用

### 自動判定される入力

| パターン               | 処理           |
| ---------------------- | -------------- |
| 「AIによって生成」     | → 議事録変換   |
| 名前 + 日時 + 短文     | → インボックス |
| `From:` `Date:` を含む | → インボックス |
| 箇条書き・短文メモ     | → インボックス |
| 質問形式               | → 通常応答     |

### デフォルトタグ

`#network` `#cost` `#contract` `#proposal` `#ai` `#container` `#meeting` `#support` `#organization` `#deadline` `#internal`

該当なし → 内容から新規タグを動的生成

---

## 詳細リファレンス

- [インボックス詳細ルール](references/inbox-rules.md)
- [議事録変換ルール](references/meeting-minutes-rules.md)

## アセット

- `assets/_templates/` - テンプレートファイル
- `assets/inbox.prompt.md` - インボックスプロンプト
- `assets/convert-meeting-minutes.prompt.md` - 議事録変換プロンプト
- `assets/copilot-instructions.md` - 自動判定ルール
