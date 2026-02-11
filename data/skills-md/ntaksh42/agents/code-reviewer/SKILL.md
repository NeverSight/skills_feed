---
name: code-reviewer
description: Automated code review with security, performance, and best practices analysis. Use when reviewing pull requests or analyzing code for vulnerabilities, performance issues, or maintainability concerns.
---

# Code Reviewer Skill

コードレビューを自動化し、包括的なフィードバックを提供するスキルです。

## 概要

このスキルは、プルリクエストや個別のコードファイルに対して、プロフェッショナルなコードレビューを実施します。セキュリティ、パフォーマンス、保守性、ベストプラクティスの観点から詳細な分析を行い、具体的な改善提案を提供します。

## 主な機能

- **包括的なコード分析**: セキュリティ、パフォーマンス、可読性、保守性の多角的レビュー
- **言語別ベストプラクティス**: 各プログラミング言語の規約とパターンに基づく評価
- **具体的な改善提案**: コード例を含む実装可能な修正案
- **重大度レベル付け**: Critical、High、Medium、Lowの4段階で問題を分類
- **自動検出**: バグ、セキュリティ脆弱性、パフォーマンスボトルネックの特定
- **コードメトリクス**: 複雑度、重複、テストカバレッジの分析
- **アーキテクチャ評価**: 設計パターンとSOLID原則の適用状況

## サポート言語

- **JavaScript/TypeScript**: React, Node.js, Next.js, Vue.js, Angular
- **Python**: Django, Flask, FastAPI, データ分析ライブラリ
- **Java**: Spring Boot, Jakarta EE, Android
- **Go**: 標準ライブラリ、主要フレームワーク
- **Rust**: Cargo、非同期プログラミング
- **C#**: .NET, ASP.NET Core, Unity
- **PHP**: Laravel, Symfony, WordPress
- **Ruby**: Rails, Sinatra
- **Swift**: iOS、macOS開発
- **Kotlin**: Android、JVM

その他50以上の言語に対応

## 使用方法

### 基本的なコードレビュー

```
このファイルをレビューしてください：
[ファイルパスまたはコード]
```

### プルリクエストレビュー

```
以下のPRをレビュー：
変更内容: [変更の説明]
ファイル: [変更されたファイルのリスト]

重点項目:
- セキュリティ
- パフォーマンス
- コードの可読性
```

### 特定観点のレビュー

```
セキュリティの観点からこのコードをレビュー:
- SQL インジェクション
- XSS 脆弱性
- 認証・認可の問題
- 機密情報の漏洩
```

### レガシーコードの改善提案

```
このレガシーコードのリファクタリング提案:
- モダンな書き方への変換
- パフォーマンス改善
- テスタビリティ向上
```

## レビュー観点

### 1. セキュリティ

**チェック項目**:
- OWASP Top 10脆弱性
- インジェクション攻撃（SQL、コマンド、XSS等）
- 認証・認可の実装
- データ検証と衛生化
- 暗号化とハッシュの適切な使用
- 機密情報のハードコーディング
- セッション管理
- CSRF、CORS設定
- 依存関係の脆弱性

**出力例**:
```markdown
## セキュリティ問題

### [CRITICAL] SQL インジェクション脆弱性
**場所**: user_controller.py:45
**問題**: ユーザー入力を直接SQLクエリに連結しています
**影響**: データベースの不正アクセス、データ漏洩の可能性

**現在のコード**:
```python
query = f"SELECT * FROM users WHERE username = '{username}'"
cursor.execute(query)
```

**推奨される修正**:
```python
query = "SELECT * FROM users WHERE username = ?"
cursor.execute(query, (username,))
```
```

### 2. パフォーマンス

**チェック項目**:
- アルゴリズムの時間計算量
- 不要なループやネスト
- データベースクエリの最適化（N+1問題）
- メモリリークの可能性
- 非効率なデータ構造
- キャッシュの活用
- 遅延読み込み
- バッチ処理の機会
- 非同期処理の活用

**出力例**:
```markdown
## パフォーマンス改善

### [HIGH] N+1クエリ問題
**場所**: blog_service.ts:78-85
**問題**: ループ内でデータベースクエリを実行しています

**影響**: 100記事で101回のクエリが実行され、レスポンス時間が大幅に増加

**現在のコード**:
```typescript
for (const post of posts) {
  post.author = await db.users.findById(post.authorId);
}
```

**推奨される修正**:
```typescript
const authorIds = posts.map(p => p.authorId);
const authors = await db.users.findByIds(authorIds);
const authorMap = new Map(authors.map(a => [a.id, a]));
posts.forEach(post => post.author = authorMap.get(post.authorId));
```

**効果**: クエリ数が101回→2回に削減、レスポンス時間50-90%改善
```

### 3. コード品質

**チェック項目**:
- 命名規則の一貫性
- 関数の単一責任原則
- DRY原則（重複の排除）
- マジックナンバーの除去
- コメントの適切性
- エラーハンドリング
- 型安全性
- null/undefined チェック
- コードの複雑度（サイクロマティック複雑度）

**出力例**:
```markdown
## コード品質

### [MEDIUM] 関数が長すぎる（単一責任原則違反）
**場所**: order_processor.java:120-280
**問題**: processOrder() が160行あり、複数の責務を持っています

**リファクタリング提案**:
```java
// 現在: 1つの長い関数
public void processOrder(Order order) {
  // 検証ロジック (20行)
  // 在庫チェック (30行)
  // 支払い処理 (40行)
  // 通知送信 (25行)
  // ロギング (15行)
  // データベース更新 (30行)
}

// 推奨: 分割された関数
public void processOrder(Order order) {
  validateOrder(order);
  checkInventory(order);
  processPayment(order);
  sendNotifications(order);
  updateDatabase(order);
  logOrderProcessing(order);
}
```

**効果**: テスタビリティ向上、保守性改善、再利用性向上
```

### 4. アーキテクチャとデザインパターン

**チェック項目**:
- SOLID原則の適用
- デザインパターンの適切な使用
- レイヤーの分離（関心の分離）
- 依存性注入
- インターフェースの設計
- モジュール性
- スケーラビリティ
- 拡張性

### 5. テスト

**チェック項目**:
- テストの存在
- テストカバレッジ
- テストの品質（AAA パターン）
- エッジケースのカバー
- モックの適切な使用
- テストの独立性
- テストの可読性

### 6. エラーハンドリングとロギング

**チェック項目**:
- 適切な例外処理
- エラーメッセージの明確性
- スタックトレースの保持
- リソースのクリーンアップ
- ロギングレベルの適切性
- 機密情報の非ログ化

### 7. ドキュメンテーション

**チェック項目**:
- コメントの適切性
- API ドキュメント
- 複雑なロジックの説明
- TODO/FIXME の管理
- README の充実度

## レビュー出力形式

### 標準レビューレポート

```markdown
# コードレビュー結果

## サマリー
- **総合評価**: B+ (良好)
- **Critical問題**: 0件
- **High問題**: 2件
- **Medium問題**: 5件
- **Low問題**: 8件
- **改善提案**: 12件

## 重要な問題

### [HIGH] セキュリティ: CSRF保護の欠如
**ファイル**: api/routes.py:45-67
**説明**: POSTエンドポイントにCSRF保護がありません
**推奨**: FlaskのCSRF保護を有効化
**優先度**: 即時対応推奨

### [HIGH] パフォーマンス: 同期的なファイルI/O
**ファイル**: upload_handler.js:89
**説明**: 大きなファイルを同期的に読み込んでいます
**影響**: サーバーブロッキング、タイムアウトの可能性
**推奨**: 非同期I/Oまたはストリーミング処理に変更

## 改善提案

### コード重複の削減
3つのコントローラーで類似の検証ロジックが重複しています。
共通のバリデーターユーティリティの作成を推奨します。

### 型安全性の向上
TypeScriptの`any`型が15箇所で使用されています。
適切な型定義またはインターフェースの作成を推奨します。

## ベストプラクティス

✅ 適切に実装されている点:
- エラーハンドリングが適切
- 一貫した命名規則
- ユニットテストのカバレッジ良好（85%）

## 推奨アクション

1. **即時対応** (Critical/High):
   - CSRF保護の実装
   - 非同期I/Oへの変更

2. **短期対応** (Medium):
   - コード重複の削減
   - 型安全性の向上
   - 複雑な関数のリファクタリング

3. **長期改善** (Low):
   - ドキュメント拡充
   - テストカバレッジ向上
   - コードコメント改善
```

## 言語別チェックリスト

### JavaScript/TypeScript

- `==` の代わりに `===` を使用
- `var` の代わりに `const`/`let` を使用
- Promise の適切なエラーハンドリング
- async/await の適切な使用
- TypeScript: `any` の過度な使用回避
- React: useEffect の依存配列
- メモリリーク（イベントリスナー、タイマー）

### Python

- PEP 8 スタイルガイド準拠
- list/dict comprehension の適切な使用
- `with` 文によるリソース管理
- 型ヒントの使用（Python 3.5+）
- グローバル変数の回避
- 例外の適切なキャッチ（broad exceptの回避）

### Java

- ストリーム API の活用
- Optional の適切な使用
- リソースの try-with-resources
- equals() と hashCode() のオーバーライド
- 不変オブジェクトの推奨
- スレッドセーフティ

### Go

- エラーハンドリングの徹底
- defer による リソースクリーンアップ
- goroutine リーク の回避
- context の適切な使用
- ポインタ vs 値のレシーバー
- race condition の回避

## カスタムルール

プロジェクト固有のルールを定義可能：

```
カスタムレビュールール:
- すべてのAPI エンドポイントにレート制限を実装
- データベース移行はロールバック可能に
- すべての公開関数にJSDocコメント必須
- エラーレスポンスは標準フォーマットに従う
```

## 自動化との統合

### CI/CD パイプライン

```yaml
# .github/workflows/code-review.yml
name: Automated Code Review
on: [pull_request]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Code Review
        run: |
          # Claude による自動レビュー
          claude-code review --pr ${{ github.event.pull_request.number }}
```

### pre-commit hook

```bash
#!/bin/bash
# .git/hooks/pre-commit
claude-code review --staged --quick
```

## 使用例

### 例1: 新機能の追加PR

**入力**:
```
以下のPRをレビューしてください：

タイトル: ユーザー認証機能の追加
変更ファイル:
- src/auth/login.ts (新規)
- src/auth/jwt.ts (新規)
- src/middleware/auth.ts (新規)
- src/routes/api.ts (変更)

変更内容:
- JWT ベースの認証を実装
- ログインエンドポイントを追加
- 認証ミドルウェアを作成
```

**出力**: セキュリティ、トークン管理、エラーハンドリングの包括的レビュー

### 例2: バグ修正のレビュー

**入力**:
```
このバグ修正をレビュー:
問題: ユーザーリストの読み込みが遅い
修正内容: クエリの最適化とキャッシング追加
```

**出力**: パフォーマンス改善の検証、キャッシュ戦略の評価、エッジケースの確認

### 例3: リファクタリング

**入力**:
```
このリファクタリングをレビュー:
変更: 500行の関数を10個の小さな関数に分割
目的: 保守性とテスタビリティの向上
```

**出力**: SOLID原則の適用状況、命名の適切性、モジュール分割の妥当性

## ベストプラクティス

### レビュー実施のタイミング

1. **プルリクエスト作成時**: 変更の全体像を把握
2. **コミット前**: 早期の問題発見
3. **定期的なコード監査**: 既存コードの改善機会発見
4. **リファクタリング前**: 改善優先順位の決定

### 効果的なレビューのコツ

1. **コンテキストを提供**: 変更の目的と背景を説明
2. **重点項目を指定**: 特に注目してほしい観点を明示
3. **段階的にレビュー**: 大きな変更は小さな単位に分割
4. **フィードバックを活用**: 指摘事項を次のコードに反映

### レビュー結果の活用

1. **優先順位付け**: Critical → High → Medium → Low の順に対応
2. **チームで共有**: レビュー結果をチームの学習材料に
3. **自動化**: 繰り返し指摘される問題は linter ルール化
4. **メトリクス追跡**: 問題発生率の推移を監視

## 制限事項

- **実行テストは不可**: コードの静的分析のみ（実際の実行は行わない）
- **ビジネスロジックの正確性**: 要件との整合性は人間の判断が必要
- **完全性の保証なし**: すべてのバグや問題を検出できるわけではない
- **プロジェクト固有のルール**: デフォルトでは一般的なベストプラクティスのみ

## 統合ツール

- **GitHub/GitLab**: PR コメントとして自動投稿
- **Linters**: ESLint, Pylint, RuboCop等との併用推奨
- **Static Analyzers**: SonarQube, CodeClimate等の補完
- **Security Scanners**: Snyk, OWASP Dependency-Check との併用

## バージョン情報

- スキルバージョン: 1.0.0
- 最終更新: 2025-01-22

---

**使用例**:

```
このPRをレビューしてください：

ファイル: src/payment/processor.py

変更内容: クレジットカード決済処理の実装

重点チェック項目:
- セキュリティ（カード情報の取り扱い）
- エラーハンドリング
- トランザクション管理
- PCI DSS 準拠
```

このプロンプトで、包括的なコードレビューレポートが生成されます！
