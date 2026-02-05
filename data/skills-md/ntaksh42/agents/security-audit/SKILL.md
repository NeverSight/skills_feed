---
name: security-audit
description: Perform security audits detecting OWASP Top 10 vulnerabilities, insecure dependencies, and security misconfigurations. Use when auditing applications for security vulnerabilities.
---

# Security Audit Skill

セキュリティ脆弱性を包括的に検出するスキルです。

## 概要

OWASP Top 10、CVE、セキュリティベストプラクティスに基づいて、コードとシステム設定のセキュリティ監査を実施します。

## 主な機能

- **OWASP Top 10 チェック**: SQLインジェクション、XSS、CSRF、認証欠陥等
- **依存関係の脆弱性**: 既知のCVEを持つライブラリの検出
- **機密情報漏洩**: ハードコードされたAPI キー、パスワード、トークン
- **暗号化評価**: 弱い暗号、不適切なハッシュアルゴリズム
- **認証・認可**: JWT、OAuth、セッション管理の問題
- **セキュアコーディング**: インプットバリデーション、出力エスケープ
- **HTTPS/TLS設定**: 証明書、暗号スイート、プロトコルバージョン
- **CORS/CSP設定**: セキュリティヘッダーの適切性
- **ファイルアップロード**: 拡張子、MIME タイプ検証
- **レート制限**: DDoS、ブルートフォース対策

## 使用方法

### 基本的なセキュリティ監査

```
このコードのセキュリティ監査を実施：
[コード]

重点項目:
- SQLインジェクション
- XSS
- 認証・認可
```

### OWASP Top 10 スキャン

```
OWASP Top 10 の観点で以下を監査：
[プロジェクトディレクトリ]

出力: 重大度別レポート
```

### 依存関係監査

```
package.json / requirements.txt の脆弱性チェック：
既知のCVEを検出
推奨アップデート提案
```

## チェック項目

### 1. インジェクション攻撃

**SQLインジェクション**:
```python
# ❌ 脆弱
query = f"SELECT * FROM users WHERE id = {user_id}"

# ✅ 安全
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (user_id,))
```

**コマンドインジェクション**:
```javascript
// ❌ 脆弱
exec(`ping ${userInput}`);

// ✅ 安全
execFile('ping', [userInput]);
```

**NoSQL インジェクション**:
```javascript
// ❌ 脆弱
db.users.find({ username: req.body.username });

// ✅ 安全
db.users.find({ username: { $eq: req.body.username } });
```

### 2. XSS (Cross-Site Scripting)

```javascript
// ❌ 脆弱
element.innerHTML = userInput;

// ✅ 安全
element.textContent = userInput;
// または
element.innerHTML = DOMPurify.sanitize(userInput);
```

### 3. 認証・セッション管理

```python
# ❌ 弱いパスワードハッシュ
password_hash = md5(password)

# ✅ 強力なハッシュ
password_hash = bcrypt.hashpw(password, bcrypt.gensalt(rounds=12))

# ❌ 予測可能なセッションID
session_id = str(user_id) + str(time.time())

# ✅ 暗号学的に安全
session_id = secrets.token_urlsafe(32)
```

### 4. 機密情報の露出

```javascript
// ❌ ハードコード
const API_KEY = "sk_live_abc123xyz";

// ✅ 環境変数
const API_KEY = process.env.API_KEY;

// ❌ ログに機密情報
console.log("User password:", password);

// ✅ 機密情報を除外
console.log("User authenticated:", userId);
```

### 5. アクセス制御

```javascript
// ❌ 不十分な認可チェック
app.delete('/api/users/:id', (req, res) => {
  User.delete(req.params.id);
});

// ✅ 適切な権限確認
app.delete('/api/users/:id', requireAuth, (req, res) => {
  if (req.user.id !== req.params.id && !req.user.isAdmin) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  User.delete(req.params.id);
});
```

### 6. セキュリティ設定ミス

```javascript
// ❌ 不適切なCORS
app.use(cors({ origin: '*' }));

// ✅ 適切なCORS
app.use(cors({
  origin: ['https://example.com'],
  credentials: true
}));

// ❌ 弱いCSP
helmet.contentSecurityPolicy({
  directives: { defaultSrc: ["'unsafe-inline'", "'unsafe-eval'"] }
});

// ✅ 強力なCSP
helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'"],
    styleSrc: ["'self'", "'unsafe-inline'"],
  }
});
```

## 出力例

```markdown
# セキュリティ監査レポート

## サマリー
- **Critical**: 2件
- **High**: 5件
- **Medium**: 8件
- **Low**: 3件

## Critical 問題

### [CRITICAL] SQLインジェクション脆弱性
**ファイル**: api/users.py:45
**問題**: ユーザー入力を直接SQL クエリに埋め込んでいます
**影響**: データベース全体への不正アクセス、データ漏洩
**CVE参照**: CWE-89

**脆弱なコード**:
```python
query = f"SELECT * FROM users WHERE username = '{username}'"
```

**修正案**:
```python
query = "SELECT * FROM users WHERE username = ?"
cursor.execute(query, (username,))
```

**優先度**: 即時修正必須

### [CRITICAL] ハードコードされたAPI キー
**ファイル**: config/api.js:12
**問題**: Stripe APIキーがコードに直接書かれています
**影響**: APIキーの漏洩、不正課金の可能性

**現在**:
```javascript
const stripeKey = "sk_live_abc123xyz";
```

**推奨**:
```javascript
const stripeKey = process.env.STRIPE_SECRET_KEY;
```

## High 問題

### [HIGH] 弱いパスワードハッシュ (MD5)
**ファイル**: auth/password.py:23
**問題**: MD5でパスワードをハッシュ化
**影響**: レインボーテーブル攻撃に脆弱

**推奨**: bcrypt または Argon2 使用

### [HIGH] XSS脆弱性
**ファイル**: views/profile.html:67
**問題**: ユーザー入力をエスケープせずに表示
**影響**: クロスサイトスクリプティング攻撃

## 依存関係の脆弱性

| パッケージ | バージョン | CVE | 重大度 | 推奨 |
|-----------|----------|-----|-------|------|
| lodash | 4.17.15 | CVE-2020-8203 | High | 4.17.21+ |
| axios | 0.18.0 | CVE-2020-28168 | Medium | 0.21.1+ |

## 推奨アクション

### 即時対応 (Critical/High):
1. SQLインジェクションの修正
2. ハードコードされたキーの削除
3. パスワードハッシュアルゴリズムの変更
4. XSS対策の実装
5. 依存関係の更新

### 短期対応 (Medium):
1. CORS設定の厳格化
2. CSP ヘッダーの追加
3. レート制限の実装

## セキュリティチェックリスト

- [ ] すべてのユーザー入力を検証・サニタイズ
- [ ] パラメータ化クエリを使用
- [ ] 強力な暗号化アルゴリズム使用
- [ ] 環境変数で機密情報管理
- [ ] HTTPS強制
- [ ] セキュリティヘッダー設定
- [ ] 依存関係を最新に保つ
- [ ] エラーメッセージで情報を漏らさない
```

## ベストプラクティス

1. **多層防御**: 複数のセキュリティレイヤーを実装
2. **最小権限の原則**: 必要最小限の権限のみ付与
3. **セキュアバイデフォルト**: デフォルト設定を安全に
4. **定期的な監査**: 継続的なセキュリティチェック
5. **依存関係管理**: 定期的なアップデートとスキャン

## バージョン情報

- スキルバージョン: 1.0.0
- 最終更新: 2025-01-22
