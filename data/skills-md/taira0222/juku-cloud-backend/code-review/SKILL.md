---
name: code-review
description: コードレビューを実施するスキル（SDD仕様書整合性・コーディング規約・セキュリティ・テスト品質）
---

# Code Review Skill

## 目的

実装コードを4つの観点でレビューし、品質を保証する：

1. **SDD仕様書（design.md）との一貫性** - 仕様書と実装の整合性を検証
2. **コーディング規約遵守** - development-guidelines.mdに基づく設計・スタイルチェック
3. **セキュリティベストプラクティス** - 認証・認可・パラメータ検証・機密情報管理
4. **テストカバレッジ・品質** - テストの存在・カバレッジ・品質確認

## 入力

- **対象コード**: git diff、ファイルパス、またはディレクトリ
- **仕様書**: `.steering/[date]-[feature]/design.md`（存在する場合）
- **規約**: `docs/development-guidelines.md`
- **用語集**: `docs/glossary.md`

## 出力

マークダウン形式の詳細レビューレポート（重大度別・カテゴリ別）

## 実行手順

### Step 1: コンテキスト収集

1. **対象コードを特定**
   - git diffの場合: 変更されたファイルリストを取得
   - ファイル指定の場合: そのファイルを対象とする
   - ディレクトリ指定の場合: 配下の全Rubyファイル（*.rb）を対象とする

2. **対応する仕様書を検索**
   - PR説明に`.steering/`へのリンクがあれば使用
   - なければファイル名から機能名を推測し、`.steering/*-[feature]*/design.md`を検索
   - 複数マッチ時は最新（ディレクトリ名の日付で判定）
   - マッチなし時はSDD整合性チェックをスキップ

3. **参照ドキュメントを読み込み**
   - `docs/development-guidelines.md` - コーディング規約・セキュリティ要件
   - `docs/glossary.md` - ドメイン用語（用語の正確性チェック用）

### Step 2: SDD仕様書整合性チェック

**チェックリスト**: `checklists/sdd-consistency.md`

`.steering/*/design.md`が存在する場合、以下を検証：

1. **API仕様チェック**
   - design.mdのAPI定義とcontrollerを比較
   - HTTPメソッド、パス、パラメータ、レスポンス構造の一致確認
   - ステータスコードの一致確認

2. **データモデルチェック**
   - design.mdのテーブル定義とmigration/modelを比較
   - カラム名、型、制約、インデックスの一致確認
   - リレーション（belongs_to, has_many等）の一致確認

3. **ビジネスルールチェック**
   - design.mdのBR-XXX（ビジネスルール）とservice実装を照合
   - バリデーションロジックの一致確認

4. **テストケースチェック**
   - design.mdのTC-XXX（テストケース）とspec実装を照合
   - テスト網羅性の確認

**重要**: 仕様書が存在しない場合、このステップはスキップし、コーディング規約・セキュリティ・テストのみレビューします。

### Step 3: コーディング規約チェック

**チェックリスト**: `checklists/coding-standards.md`

1. **レイヤーアーキテクチャ**
   - Controller: 薄い、ビジネスロジックなし
   - Service: ビジネスロジック集約
   - Query: 複雑なクエリ分離
   - Model: Thin Model（validationsのみ）
   - Serializer: JSON整形（Alba）

2. **命名規則**
   - 変数・メソッド: `snake_case`
   - クラス: `PascalCase`
   - 定数: `UPPER_SNAKE_CASE`
   - 真偽値メソッド: `?`で終わる
   - 破壊的メソッド: `!`で終わる

3. **禁止パターン検出**
   - Fat Controller（Controllerにビジネスロジック記述）
   - Fat Model（Modelに複雑な処理）
   - マジックナンバー（定数化されていない数値）
   - ハードコーディング（設定値、URL等）
   - グローバル変数使用

4. **コードスタイル**
   - インデント（スペース2つ）
   - 行の長さ（120文字以下）
   - 文字列リテラル（ダブルクォート優先）
   - ハッシュ記法（新記法 `key: value`）

### Step 4: セキュリティレビュー

**チェックリスト**: `checklists/security.md`

1. **認証・認可**
   - `authenticate_user!`の使用確認
   - `require_admin_role!`等の適切な配置
   - before_actionでの認証・認可制御

2. **パラメータ検証**
   - Strong Parameters使用確認（ホワイトリスト方式）
   - `permit!`の使用禁止

3. **機密情報管理**
   - ENV変数使用確認
   - ハードコーディングされた機密情報（パスワード、API Key等）の検出
   - `.env`ファイルのコミット確認

4. **セキュリティリスク**
   - SQLインジェクションリスク（パラメータ化クエリ使用確認）
   - XSSリスク（サニタイゼーション確認）
   - パスワード・トークンのハッシュ化（bcrypt, JWT有効期限）

### Step 5: テスト品質チェック

**チェックリスト**: `checklists/testing.md`

1. **テストファイル存在確認**
   - 変更されたファイルに対応するspecファイルの存在確認

2. **カバレッジ推定**
   - Modelテスト: validations, associations, scopesのテスト存在
   - Serviceテスト: 正常系、異常系、エッジケースのテスト存在
   - Requestテスト: 成功ケース、エラーケース、認証・認可のテスト存在

3. **テスト品質**
   - RSpec形式（describe, context, it）の使用確認
   - AAAパターン（Arrange, Act, Assert）の遵守確認
   - FactoryBot使用確認
   - 1テスト1アサーションの原則確認

4. **エッジケースカバレッジ**
   - 境界値テスト
   - nil/空文字列/空配列のテスト
   - 並行処理のテスト（必要に応じて）

5. **N+1問題回避のテスト**
   - `includes`, `preload`, `eager_load`の使用確認

### Step 6: レポート生成

**テンプレート**: `templates/review-report.md`

1. **結果を重大度別に分類**
   - **Critical**: マージ前に必ず修正（仕様違反、セキュリティ問題、必須テスト欠如）
   - **Warning**: 対処すべき（N+1クエリ、マジックナンバー、エッジケーステスト欠如）
   - **Info**: 推奨（ドキュメント改善、リファクタリング機会）

2. **カテゴリ別にグループ化**
   - SDD仕様書整合性
   - コーディング規約
   - セキュリティ
   - テスト品質

3. **ファイル別に問題を整理**
   - 各問題に`templates/issue-format.md`のフォーマットを適用
   - ファイルパス、行番号、問題説明、推奨対応を含める

4. **サマリーと次のアクション**
   - Executive Summary（重大度別の問題数集計）
   - Must Fix Before Merge（Critical問題リスト）
   - Should Address（Warning問題リスト）
   - Recommended（Info問題リスト）
   - 自動ツール（RuboCop, Brakeman, RSpec+Coverage）実行の推奨

## 参照ファイル

- [guide.md](./guide.md) - 詳細なレビューガイドライン・ベストプラクティス
- [checklists/sdd-consistency.md](./checklists/sdd-consistency.md) - SDD仕様書検証ルール
- [checklists/coding-standards.md](./checklists/coding-standards.md) - コーディング規約チェックリスト
- [checklists/security.md](./checklists/security.md) - セキュリティレビューチェックリスト
- [checklists/testing.md](./checklists/testing.md) - テスト品質チェックリスト
- [templates/review-report.md](./templates/review-report.md) - レビューレポートテンプレート
- [templates/issue-format.md](./templates/issue-format.md) - 個別問題フォーマット

## 使い方

このスキルは通常 `/code-review` エージェント経由で呼び出されます。

```bash
# PR全体をレビュー（git diff使用）
/code-review

# 特定ファイルをレビュー
/code-review app/controllers/api/v1/reports_controller.rb

# 複数ファイルをレビュー
/code-review app/controllers/api/v1/reports_controller.rb app/services/reports/generate_service.rb

# 特定機能をレビュー（.steering/配下）
/code-review .steering/20250131-student-report/

# ディレクトリ全体をレビュー
/code-review app/services/reports/
```

## 注意事項

- レビューは対象ファイル数により数分かかる場合があります
- Critical問題が見つかった場合、マージ前に必ず修正してください
- このスキルは自動ツール（RuboCop, Brakeman等）の補完として使用します
- 既存ツールも併用することで、より包括的な品質保証が可能です
