---
name: nanobanana-image
description: Nano Banana 2 (Google Gemini API) を使って画像を生成・編集するスキル。「画像を生成して」「イラストを作って」「○○の絵を描いて」「画像を作成」「この画像を編集して」「この画像をもとに○○を作って」「generate an image」「create a picture」「edit this image」などの依頼があった場合に使用。テキストからの生成、参照画像からの生成、画像編集、Google検索グラウンディングによる最新情報を反映した画像生成に対応。「最新の○○」「トレンドを反映」「リアルタイム情報」といった依頼にも対応可能。
---

# Nano Banana 2 Image Generation

Google Gemini APIを使用した画像生成・編集スキル。Nano Banana 2 により、Pro品質の画像をFlash速度で生成可能。

## 前提条件

環境変数 `NANOBANANA_SKILL_GOOGLE_API_KEY` が設定されていること。

未設定の場合は以下を案内：
1. [Google AI Studio](https://aistudio.google.com/) でAPIキーを取得
2. `~/.claude/settings.json` に追加：
```json
{
  "env": {
    "NANOBANANA_SKILL_GOOGLE_API_KEY": "取得したAPIキー"
  }
}
```

## モデル

| モデル | ID | 特徴 |
|--------|-----|------|
| Nano Banana 2 | `flash` (デフォルト) | Pro品質×Flash速度・高精度テキスト・4K対応・0.5K対応 |
| Nano Banana Pro | `pro` | 高度なコンテキスト対応・推論強化・4K対応 |

## ワークフロー

画像生成後は `open` コマンドでプレビューを提案：

```bash
python scripts/generate_image.py "プロンプト" -o image.png && open image.png
```

## 基本コマンド

```bash
# テキストから画像生成
python scripts/generate_image.py "夕焼けのビーチで遊ぶ犬" -o dog.png

# 参照画像から生成（image-to-image）
python scripts/generate_image.py "この画像をアニメ風にして" -i reference.png -o anime.png

# 複数参照画像（最大14枚）
python scripts/generate_image.py "これらを組み合わせてロゴを作成" -i logo1.png -i logo2.png -o new_logo.png

# Google検索グラウンディング（最新情報を反映）
python scripts/generate_image.py "2026年の最新ファッショントレンド" --search -o fashion.png

# オプション指定
python scripts/generate_image.py "横長の風景" --aspect 16:9 -o landscape.png
python scripts/generate_image.py "詳細な建築物" --size 4K -o building.png
python scripts/generate_image.py "かわいい猫" -n 3 -o cat.png  # → cat_1.png, cat_2.png, cat_3.png

# Nano Banana Proを使用
python scripts/generate_image.py "複雑なシーン" -m pro -o scene.png
```

## オプション一覧

| オプション | 説明 |
|------------|------|
| `-o, --output` | 出力ファイルパス（デフォルト: output.png） |
| `-m, --model` | モデル選択: `flash` (デフォルト) / `pro` |
| `-i, --input` | 参照画像パス（複数指定可、最大14枚） |
| `-n, --count` | 生成する画像の数 |
| `--aspect` | アスペクト比: 1:1, 16:9, 9:16, 4:3, 3:4, 1:4, 4:1, 21:9 等 |
| `--size` | 画像サイズ: 0.5K, 1K, 2K, 4K |
| `--search` | Google検索グラウンディングを使用（最新情報を反映） |

## プロンプトの基本

- **具体的に**: 「猫」→「窓辺で日向ぼっこする白い猫」
- **スタイル指定**: 「写実的」「アニメ風」「油絵風」「ミニマリスト」
- **構図指定**: 「クローズアップ」「俯瞰」「正面から」
- **テキスト含有**: Nano Banana 2 は高精度テキストレンダリングに対応
- **編集時**: 「〇〇を追加して」「〇〇を削除して」「〇〇を変更して」

**詳細なプロンプトガイド**: [references/prompt-guide.md](references/prompt-guide.md)
- フォトリアリスティック、イラスト/ステッカー、テキスト含有、商品写真、ミニマルデザインの5パターン

## エラー対応

| エラー | 対処 |
|--------|------|
| 401 Unauthorized | APIキーを確認・再取得 |
| 429 Rate Limit | 少し待って再試行 |
| コンテンツポリシー違反 | プロンプトを修正（暴力・成人向け等を避ける） |
| 画像が生成されない | プロンプトをより具体的に |
