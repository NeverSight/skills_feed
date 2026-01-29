---
name: kuroco-docs
description: Kurocoドキュメントの検索・参照ガイド。使用キーワード：「Kurocoドキュメント」「Kuroco公式」「ドキュメント検索」「マニュアル」「チュートリアル」「リファレンス」「使い方」「やり方」「設定方法」「実装方法」「Kurocoヘルプ」「Kuroco仕様」「公式ガイド」「ドキュメント同期」「Kurocoの○○はどうやる」「Kurocoで○○したい」。ドキュメントから情報を探す場合に使用。
---

# Kurocoドキュメント検索ガイド

このSkillはKuroco公式ドキュメントの検索・参照を支援します。

## 重要: ドキュメントの確認（必ず最初に実行）

### 1. docsフォルダの存在確認

```bash
ls docs/
```

**docsフォルダが空または存在しない場合:**
→ ユーザーに「Kurocoドキュメントがまだ同期されていません。同期コマンドを実行してもよいですか？」と確認してから以下を実行：

```bash
bash scripts/sync-docs.sh
```

### 2. 同期日時の確認（1ヶ月チェック）

```bash
cat docs/.last_sync
```

このファイルには以下の形式で同期日時が記録されています：
- 1行目: Unixタイムスタンプ
- 2行目: 日時（YYYY-MM-DD HH:MM:SS）

**1ヶ月（30日 = 2592000秒）以上経過しているかチェック:**

```bash
last_sync=$(head -1 docs/.last_sync)
now=$(date +%s)
diff=$((now - last_sync))
if [ $diff -gt 2592000 ]; then echo "1ヶ月以上経過"; else echo "最新"; fi
```

**1ヶ月以上経過している場合:**
→ ユーザーに「Kurocoドキュメントの同期から1ヶ月以上経過しています。再同期しますか？」と確認してから実行

## ドキュメントの場所

```
docs/
```

## ディレクトリ構造

| ディレクトリ | 内容 | 主な用途 |
|-------------|------|---------|
| `tutorials/` | チュートリアル | 機能の使い方、実装手順、サンプルコード |
| `reference/` | リファレンス | API設定項目、Smartyプラグイン、フィルタークエリ、エラーコード |
| `management/` | 管理画面 | 管理画面の各機能（コンテンツ、メンバー、API、フォーム）の詳細説明 |
| `faq/` | FAQ | よくある質問と回答、トラブル解決のヒント |
| `about/` | Kurocoについて | 概要、料金プラン、制限事項、用語集 |
| `troubleshooting/` | トラブルシューティング | エラー解決、問題診断ガイド |
| `update/` | アップデート | リリースノート、新機能、ロードマップ |
| `information/` | お知らせ | 公式からのお知らせ、メンテナンス情報 |

## 検索方法

### 方法1: INDEX.mdを最初に確認（推奨）

```bash
cat docs/INDEX.md
```

INDEX.mdには以下が含まれています：
- **クイックリファレンス**: 目的別の重要ドキュメント一覧
- **ディレクトリ構造**: 各フォルダの説明
- **ファイル一覧**: 全ファイルのタイトルと説明

### 方法2: Grepツールでキーワード検索

Claude CodeのGrepツールを使用してください（Bashのgrepより高速・正確）：

```
# キーワードで検索（ファイルパスのみ）
Grep: pattern="エンドポイント" path="docs/"

# 内容も確認したい場合
Grep: pattern="エンドポイント" path="docs/" output_mode="content"

# 特定ディレクトリ内を検索
Grep: pattern="ログイン" path="docs/tutorials/"

# 正規表現で検索
Grep: pattern="filter.*query" path="docs/reference/"
```

### 方法3: Globツールでファイル検索

```
# 全マークダウンファイル一覧
Glob: pattern="**/*.md" path="docs/"

# tutorialsのファイル一覧
Glob: pattern="*.md" path="docs/tutorials/"
```

## 目的別クイックリファレンス

### API・エンドポイント設定
| ファイル | 内容 |
|----------|------|
| `tutorials/configure-endpoint.md` | エンドポイントの作成・設定方法 |
| `reference/endpoint-settings.md` | エンドポイント設定項目の詳細 |
| `reference/filter-query.md` | フィルタークエリの書き方 |
| `reference/api-cache.md` | APIキャッシュの設定 |
| `management/api-security.md` | APIセキュリティ（認証、CORS） |

### 認証・ログイン
| ファイル | 内容 |
|----------|------|
| `tutorials/login.md` | ログイン機能の実装 |
| `tutorials/signup.md` | 会員登録の実装 |
| `tutorials/how-to-use-password-reminder.md` | パスワードリマインダー |
| `tutorials/implementing-two-step-verification-on-login-form.md` | 二段階認証 |

### フロントエンド統合
| ファイル | 内容 |
|----------|------|
| `tutorials/beginners-guide.md` | ビギナーズガイド |
| `tutorials/integrate-kuroco-with-nuxt.md` | Nuxt.js/Next.jsでのコンテンツ表示 |
| `tutorials/integrate-login.md` | フロントエンドでのログイン実装 |
| `tutorials/corporate-sample-site-to-ssg.md` | SSG対応 |

### コンテンツ管理
| ファイル | 内容 |
|----------|------|
| `tutorials/adding-a-topics.md` | コンテンツ定義の作成 |
| `management/content-structure-topics.md` | コンテンツ構造の説明 |
| `tutorials/bulk-upload-in-csv.md` | CSVでの一括アップロード |
| `reference/uploading-files-using-the-api.md` | APIでのファイルアップロード |

### バッチ処理・自動化
| ファイル | 内容 |
|----------|------|
| `tutorials/how-to-use-batch.md` | バッチ処理の使い方 |
| `reference/smarty-plugin.md` | Smartyプラグイン一覧 |
| `reference/trigger-variables.md` | トリガー変数 |
| `tutorials/auto-run-github-with-contents-update.md` | GitHub Actions連携 |

### 外部サービス連携
| ファイル | 内容 |
|----------|------|
| `tutorials/send-slack-notification-after-a-form-has-been-submitted.md` | Slack通知 |
| `tutorials/how-to-link-sendgrid.md` | SendGrid連携 |
| `tutorials/firebase.md` | Firebase連携 |
| `management/stripe.md` | Stripe決済 |

## 検索のコツ

1. **まずINDEX.mdを確認**: 目的に合ったファイルが見つかりやすい
2. **日本語キーワード**: `エンドポイント`, `ログイン`, `コンテンツ`
3. **英語キーワード**: `Topics`, `Member`, `API`, `CORS`
4. **機能名**: `batch`, `webhook`, `trigger`, `smarty`
5. **ディレクトリを絞る**: `tutorials/`（実装方法）、`reference/`（仕様）、`management/`（管理画面）

## ドキュメント更新

```bash
# 最新ドキュメントを同期
bash scripts/sync-docs.sh
```

同期すると `docs/INDEX.md` も自動更新されます。
