---
name: supabase-migration-prep
description: Supabaseデータベースマイグレーションの準備を行うスキル。バックアップの作成と差分マイグレーションファイルの生成を実施します。ユーザーが「マイグレーションを準備」「バックアップと差分を作成」「マイグレーションファイルを生成」などのリクエストをした際に使用します。
---

# Supabase Migration Prep

Supabaseデータベースのマイグレーション前準備を自動化します。バックアップと差分マイグレーションファイルを生成します。

**注意**: マイグレーションは適用しません。準備のみを行います。

## 前提条件

**ローカルでスキーマを編集済みであること**:
- `supabase/schema.sql` などのローカルファイルを編集
- または `supabase/migrations/` に新規SQLファイルを追加

**重要**: 
- このスキルは `supabase start` でローカルインスタンスを起動します
- Docker Composeなど他のPostgreSQLが起動中の場合、ポート競合が発生する可能性があります
- 初回実行時はDockerイメージのダウンロードで時間がかかります

## 実行手順

### 1. PROJECT-REF確認

ユーザーに確認：
- PROJECT-REF（16文字の英数字、例: `abcdefghijklmnop`）
- マイグレーション名（オプション、デフォルト: `schema_update`）

**PROJECT-REF確認方法**:
- Dashboard URL: `https://supabase.com/dashboard/project/[YOUR-PROJECT-REF]`
- 設定: Dashboard → Settings → General → Reference ID

### 2. スクリプト実行

```bash
# run_in_terminal ツールを使用
bash .claude/skills/supabase-migration-prep/scripts/prepare_migration.sh <PROJECT_REF> [migration_name]
```

**例**:
```bash
bash .claude/skills/supabase-migration-prep/scripts/prepare_migration.sh abcdefghijklmnop add_profile_fields
```

スクリプトが自動実行：
1. バックアップディレクトリ作成
2. Supabase認証確認
3. プロジェクトリンク
4. 完全バックアップ作成（ロール、スキーマ、データを個別に取得）
5. ローカルSupabaseインスタンス起動（`supabase start`）
6. ローカルスキーマをインスタンスに適用（`supabase db reset`）
7. ローカルとリモートの差分確認
8. マイグレーションファイル生成

### 3. 完了報告

スクリプト出力から以下を確認してユーザーに報告：
- ✅ ロールバックアップ: `supabase/backup/roles_YYYYMMDD_HHMMSS.sql`
- ✅ スキーマバックアップ: `supabase/backup/schema_YYYYMMDD_HHMMSS.sql`
- ✅ データバックアップ: `supabase/backup/data_YYYYMMDD_HHMMSS.sql`
- ✅ マイグレーションファイル: `supabase/migrations/YYYYMMDDHHMMSS_<name>.sql`
- ⚠️ マイグレーション未適用（適用前に内容確認を推奨）
- ℹ️ ローカルインスタンス起動中（不要なら `npx supabase stop` で停止）

## トラブルシューティング

エラー発生時は、スクリプト出力のエラーメッセージを確認し、以下を試行：

- **認証エラー**: `npx supabase login` を再実行
- **リンクエラー**: `npx supabase unlink` 後に再実行
- **差分なし**: ローカルでスキーマ変更後に再実行

## 参考

詳細手順: [DATABASE_MIGRATION_CLOUD.md](/workspace/doc/development/DATABASE_MIGRATION_CLOUD.md)
