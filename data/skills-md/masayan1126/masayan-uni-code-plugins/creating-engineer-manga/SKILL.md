---
name: creating-engineer-manga
description: Generates Nano Banana Pro prompts for 4-panel engineer humor comics. Use when user mentions "漫画作成", "エンジニア漫画", "4コマ", or "あるある".
---

# エンジニアあるある漫画作成

> **注**: 生成したプロンプトを画像生成AIに入力する際は、キャラクターの元画像を一緒に添付してください。

## ワークフロー

1. **アイデア確認**: `progress/ideas.md` をチェックし、漫画関連のアイデアがあれば提案（または新規入力）
2. **パターン選択**（対話形式で確認）:
   - 日常系4コマ（デフォルト）: 起承転結、ほのぼの
   - バトル系縦スクロール: 4-6コマ、ダイナミック
   - キャラ固定ギャグ: 2-4コマ、表情重視
3. **AIっぽさ緩和オプション確認**: [ANTI_AI_STYLE.md](../ANTI_AI_STYLE.md) 参照
   - 「ベタ塗り」「デフォルメされたフォルム」を含めるか確認
4. **プロンプト生成**: PROMPT_TEMPLATE.md 使用
5. **Xポスト文面生成**: ハッシュタグ付き
6. **成果物保存**:
   - プロンプト: `output/engineer-manga/{タイトル}.md`（ディレクトリがなければ作成）
   - 生成画像: `output/engineer-manga/images/{タイトル}.png`
7. **進捗更新**: `progress/ideas.md` を更新（完了したアイデアにチェック）

## 参照ファイル

- [PATTERNS.md](PATTERNS.md): パターン定義
- [PROMPT_TEMPLATE.md](PROMPT_TEMPLATE.md): テンプレート
- [EXAMPLES.md](EXAMPLES.md): サンプル

## 必須ルール

- テキストは日本語
- 画像上部にタイトル配置
- 手書き風テイスト
- エンジニアに共感されるユーモア

## 長編制作時の注意（画像生成AI使用時）

複数ページの漫画を制作する場合：

- **1ページずつ生成**: 一度に多くのページを生成しない（一貫性が崩壊しやすい）
- **キャラ画像の再添付**: 画像生成AIへの入力ごとにキャラクター設定画を再添付
- **品質の細かな確認**: 小さな単位で生成し、各ページの品質を高く保つ
