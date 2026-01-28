---
name: pptx-translation
description: Assists with PowerPoint translation feature implementation, debugging, and improvements. Covers PPTX processing, Claude API integration, and the full translation workflow. Activates when user mentions "translation error", "PPTX processing", "翻訳が動かない", "テキスト抽出エラー", "python-pptx".
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
user-invocable: true
---

# PPTX Translation Skill

PowerPoint翻訳機能の実装・デバッグ・改善のためのスキル。

## When to Use This Skill

- PPTX翻訳機能を新規実装・改善する時
- 翻訳処理でエラーが発生した時
- テキスト抽出が正しく動作しない時
- 翻訳後のPPTXが正しく生成されない時
- Python処理（python-pptx）のデバッグ時
- Claude API連携の問題を調査する時

## アーキテクチャ

```
┌─────────────────────────────────────────────────────────────┐
│ TypeScript (Next.js Server Actions)                         │
│   └─ src/app/actions/pptx/*.ts                              │
│       ├─ extractTextFromPPTXAction  → Python subprocess     │
│       ├─ translateFileAction        → Anthropic SDK (TS)    │
│       └─ applyTranslationsAction    → Python subprocess     │
└─────────────────────────────────────────────────────────────┘
```

**重要**: 翻訳処理はTypeScript + Anthropic SDK（`src/lib/translation/`）

## 主要ファイル

| 役割 | ファイル |
|------|---------|
| オーケストレーション | `src/app/actions/pptx/index.ts` |
| Python実行 | `src/app/actions/pptx/python-execution.ts` |
| 翻訳サービス | `src/lib/translation/translation-service.ts` |
| ベース翻訳クラス | `src/lib/translation/base-translator.ts` |
| PPTX生成 | `python_backend/generate_pptx.py` |

## 翻訳フロー

1. **アップロード** → Supabase Storageに保存
2. **テキスト抽出** → Python (python-pptx) でテキスト抽出
3. **翻訳** → Claude API (TypeScript) で翻訳
4. **PPTX生成** → Python で翻訳テキストを適用
5. **プレビュー生成** → スライド画像を生成
6. **ダウンロード** → Signed URLで配信

## デバッグ手順

### Python処理のテスト
```bash
source venv/bin/activate
python python_backend/generate_pptx.py \
  --input original.pptx \
  --translations translations.json \
  --output translated.pptx
```

### 翻訳APIのテスト
```typescript
// src/lib/translation/translation-service.ts をデバッグ
import { logger } from "@/lib/logger";
logger.debug("Translation request", { text, sourceLang, targetLang });
```

## よくある問題

### 1. 同一テキスト重複問題
- **症状**: 同じテキストが複数箇所にあると2つ目以降が翻訳されない
- **原因**: `generate_pptx.py` のbreakステートメント
- **対策**: breakを削除し、全マッチを処理

### 2. 大ファイルタイムアウト
- **症状**: 50枚超のスライドで処理がタイムアウト
- **対策**: `base-translator.ts` のmax_tokensを動的設定

### 3. 日本語フォント問題
- **症状**: 日本語がトーフ（□）で表示
- **対策**: `generate_pptx.py` で游ゴシック/メイリオを設定

## 制限事項

| 項目 | 制限値 |
|------|--------|
| 最大スライド数 | 50枚 |
| 最大ファイルサイズ | 50MB |
| 対応形式 | .pptx のみ（.ppt非対応）|
| 同時翻訳 | 3ファイル/ユーザー |

## AI Assistant Instructions

このスキルが有効化された時:

1. **問題の切り分け**: TypeScript処理かPython処理かを特定
2. **ログ確認**: `@/lib/logger` のデバッグ出力を確認
3. **段階的検証**: テキスト抽出 → 翻訳 → PPTX生成の順で検証
4. **venv有効化**: Python処理時は必ず `source venv/bin/activate`

Always:
- Python処理前に仮想環境を有効化する
- 翻訳はTypeScript（Claude API）で処理する
- エラー時はログを確認してから修正する

Never:
- Python側で翻訳処理を実装しない（TypeScriptで実装済み）
- venvなしでPythonスクリプトを実行しない
- 制限事項を超えるファイルを処理しようとしない
