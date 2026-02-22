---
name: security-guidelines
description: "IPA guideline-compliant security diagnostic and review skill for Laravel/React applications. Use when performing security checks during code implementation or review. Diagnoses 11 vulnerability types (SQL injection, XSS, CSRF, etc.), provides safe code examples, and performs checklist-based validation. Works in conjunction with .claude/rules/security/ to provide concrete diagnostic workflows during implementation phases. Triggers when: (1) reviewing code for security vulnerabilities, (2) implementing authentication/authorization, (3) handling user input/output, (4) working with sessions/cookies, (5) processing files or executing commands, (6) creating forms or APIs, (7) performing security audits."
---

# Security Guidelines

IPA準拠のセキュリティ診断・レビュースキル。Laravel + Reactアプリケーションの実装時・レビュー時に11種類の脆弱性を診断し、安全なコード例を提供する。

## Overview

このスキルは、IPAの「安全なウェブサイトの作り方 第7版」に基づき、以下の機能を提供する:

1. **脆弱性診断**: コードの脆弱性を11のカテゴリで検証
2. **安全なコード例提供**: Laravel/React固有の安全な実装パターン
3. **チェックリストベース検証**: 実装漏れの防止
4. **ルール連携**: `.claude/rules/security/` と連携した包括的なガイダンス

**重要**: このスキルは `.claude/rules/security/` のルールと**協調動作**する。rulesが「守るべき規約」を提供し、本スキルは「実行する診断ワークフロー」を提供する。

## Diagnostic Workflow

セキュリティ診断は以下のワークフローで実行する:

### Phase 1: Scope Identification

対象コードのスコープを特定:

1. **コード種別の判定**
   - Backend (Laravel): Controller, UseCase, Repository, Model
   - Frontend (React): Component, Hook, Form
   - API: Endpoint, Middleware

2. **関連する脆弱性カテゴリの特定**
   - 入力処理 → SQLインジェクション、OSコマンド、ディレクトリトラバーサル
   - 出力処理 → XSS
   - フォーム → CSRF
   - 認証/認可 → セッション管理、アクセス制御
   - ファイル操作 → ディレクトリトラバーサル
   - HTTPレスポンス → HTTPヘッダインジェクション

### Phase 2: Vulnerability Analysis

特定されたカテゴリごとに診断:

**診断方法**:
1. 該当する `references/*.md` を読み込む
2. 脆弱なパターンと照合
3. 安全なパターンとの差分を特定

**診断対象の11カテゴリ**:
- SQL Injection
- OS Command Injection
- Directory Traversal
- Cross-Site Scripting (XSS)
- Cross-Site Request Forgery (CSRF)
- Session Management
- HTTP Header Injection
- Mail Header Injection
- Clickjacking
- Access Control (IDOR)
- Authentication & Password Management

詳細は [references/vulnerability-catalog.md](references/vulnerability-catalog.md) を参照。

### Phase 3: Report & Remediation

診断結果をレポート:

**レポート形式**:
```markdown
## セキュリティ診断結果

### 検出された問題

#### [脆弱性名] (重要度: 高/中/低)

**問題箇所**:
[ファイルパス:行番号]

**脆弱性の説明**:
[なぜ危険なのか]

**現在のコード**:
```[language]
[脆弱なコード]
```

**推奨される修正**:
```[language]
[安全なコード]
```

**参考**: references/[該当ファイル].md
```

### Phase 4: Checklist Verification

最終確認としてチェックリストを実行:

1. [references/checklist.md](references/checklist.md) を読み込む
2. 該当するカテゴリのチェックリストを確認
3. 未実施項目があれば追加で指摘

## Quick Start

### コード実装時の使用

```
「このログイン処理のセキュリティをチェックして」
→ セッション管理、CSRF、パスワード管理を診断
```

### コードレビュー時の使用

```
「このPR全体のセキュリティレビューをして」
→ 変更されたファイルを分析し、関連する脆弱性を診断
```

### 特定の脆弱性に対するチェック

```
「XSS対策ができているか確認して」
→ references/xss.md を参照して診断
```

## Vulnerability Categories

11種類の脆弱性の詳細は、以下のreferencesファイルを参照:

### Injection Vulnerabilities
- **SQL Injection**: See [references/injection.md](references/injection.md#sql-injection)
- **OS Command Injection**: See [references/injection.md](references/injection.md#os-command-injection)
- **Directory Traversal**: See [references/injection.md](references/injection.md#directory-traversal)

### XSS Vulnerabilities
- **Cross-Site Scripting**: See [references/xss.md](references/xss.md)
  - Laravel/Blade XSS prevention
  - React XSS prevention
  - Content Security Policy (CSP)

### CSRF & Session
- **CSRF**: See [references/csrf-session.md](references/csrf-session.md#csrf)
- **Session Management**: See [references/csrf-session.md](references/csrf-session.md#session-management)

### HTTP Header Vulnerabilities
- **HTTP Header Injection**: See [references/http-headers.md](references/http-headers.md#http-header-injection)
- **Mail Header Injection**: See [references/http-headers.md](references/http-headers.md#mail-header-injection)
- **Clickjacking**: See [references/http-headers.md](references/http-headers.md#clickjacking)

### Access Control & Authentication
- **Access Control (IDOR)**: See [references/access-control.md](references/access-control.md#idor)
- **Password Management**: See [references/access-control.md](references/access-control.md#password-management)

### Comprehensive Checklist
- **Implementation Checklist**: See [references/checklist.md](references/checklist.md)

## Integration with Rules

このスキルは `.claude/rules/security/` のルールと以下のように連携する:

| Rules | Skills |
|-------|--------|
| 常にコンテキストに読み込まれる | 診断時にトリガーされる |
| 「守るべき規約」を定義 | 「実行する診断ワークフロー」を提供 |
| 静的なガイドライン | 動的な診断プロセス |
| コーディング時の参照 | レビュー時の実行 |

**使い分け**:
- **実装中**: Rules が自動的に適用される
- **レビュー時**: このスキルを明示的に起動して診断を実行

## Best Practices

### 診断の優先順位

**高優先度** (重大な影響):
1. SQL Injection
2. XSS
3. CSRF
4. Access Control (IDOR)
5. Session Management

**中優先度** (重要):
6. OS Command Injection
7. Directory Traversal
8. Password Management

**低優先度** (推奨):
9. HTTP Header Injection
10. Mail Header Injection
11. Clickjacking

### 診断の範囲

**最小スコープ**: 単一の関数/メソッド
**推奨スコープ**: 単一のファイルまたは機能
**最大スコープ**: Pull Request全体

**注意**: スコープが大きすぎる場合は、機能ごとに分割して診断することを推奨。

### False Positive の回避

以下のケースでは誤検知を避ける:

1. **Laravel の標準機能を正しく使用している場合**:
   - `{{ }}` によるエスケープ
   - `@csrf` ディレクティブ
   - `Hash::make()` によるパスワードハッシュ
   - Laravel Policy による認可チェック

2. **React の標準機能を正しく使用している場合**:
   - JSX のデフォルトエスケープ
   - DOMPurify によるサニタイズ

これらが正しく使用されている場合は「✅ 安全」と判定する。

## Resources

### references/

脆弱性カテゴリごとの詳細資料:

- `vulnerability-catalog.md`: 11種類の脆弱性の概要
- `injection.md`: SQLインジェクション、OSコマンド、ディレクトリトラバーサル
- `xss.md`: XSS対策（Laravel/React）
- `csrf-session.md`: CSRF、セッション管理
- `http-headers.md`: HTTPヘッダ系脆弱性
- `access-control.md`: アクセス制御、認証、パスワード管理
- `checklist.md`: 包括的な実装チェックリスト
