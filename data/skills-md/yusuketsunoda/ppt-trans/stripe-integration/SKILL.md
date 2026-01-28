---
name: stripe-integration
description: Assists with Stripe payment implementation, debugging, and webhook handling. Covers subscriptions, one-time charges, and customer management. Activates when user mentions "payment", "webhook", "subscription", "決済エラー", "課金", "Stripe".
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
user-invocable: true
---

# Stripe Integration Skill

Stripe決済連携の実装・デバッグ・テストのためのスキル。

## When to Use This Skill

- Stripe決済機能を新規実装・改善する時
- Webhook処理でエラーが発生した時
- サブスクリプション管理を実装する時
- 決済フローのデバッグが必要な時
- Stripe CLIでローカルテストする時
- 課金プランの変更を実装する時

## 主要ファイル

| 役割 | ファイル |
|------|---------|
| Stripeクライアント | `src/lib/stripe/client.ts` |
| サブスクリプション | `src/lib/stripe/subscription-service.ts` |
| Webhook処理 | `src/app/api/stripe/webhook/route.ts` |
| ゲストチェックアウト | `src/app/api/stripe/guest-checkout/route.ts` |
| 決済アクション | `src/app/actions/payment.ts` |

## Webhook イベント

| イベント | 処理内容 |
|---------|---------|
| `checkout.session.completed` | 支払い完了 → プラン更新 |
| `customer.subscription.updated` | サブスク更新 → 期間更新 |
| `customer.subscription.deleted` | サブスク解約 → Freeに戻す |
| `invoice.payment_failed` | 支払い失敗 → 通知 |

## ローカルテスト

### Stripe CLI でWebhook転送
```bash
stripe listen --forward-to localhost:3000/api/stripe/webhook

# 別ターミナルでイベント送信
stripe trigger checkout.session.completed
```

### テスト用カード番号

| カード番号 | 用途 |
|-----------|------|
| 4242424242424242 | 成功 |
| 4000002500003155 | 3Dセキュア認証 |
| 4000000000009995 | 残高不足 |
| 4000000000000341 | カード拒否 |

## 環境変数

```bash
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
```

## プラン設計

| プラン | 月額 | 翻訳回数/月 | 最大ファイルサイズ |
|--------|------|------------|------------------|
| Free | ¥0 | 3回 | 10MB |
| Premium | ¥980 | 無制限 | 50MB |
| Business | ¥2,980 | 無制限 + API | 100MB |

## DBテーブル

```sql
-- profiles.stripe_customer_id: Stripe顧客ID
-- user_plans: プラン情報
-- stripe_events: Webhook履歴（重複防止）
```

## よくある問題

### 1. Webhookシグネチャ検証失敗
- **原因**: rawBodyが必要
- **対策**: `route.ts` で `request.text()` を使用

### 2. 二重課金
- **原因**: Webhookの重複配信
- **対策**: `stripe_events` で idempotency チェック

### 3. サブスク状態の不整合
- **原因**: Webhookミス
- **対策**: 定期的な `stripe.subscriptions.retrieve` で同期

## AI Assistant Instructions

このスキルが有効化された時:

1. **環境確認**: Stripe環境変数が設定されているか確認
2. **テストモード確認**: `sk_test_` / `pk_test_` を使用しているか確認
3. **Webhook検証**: シグネチャ検証が正しく実装されているか確認
4. **冪等性確認**: 二重課金防止の実装を確認

Always:
- テスト用カード番号（4242...）を使用する
- Webhookはidempotencyチェックを実装する
- rawBodyで署名検証する
- `stripe_events` テーブルで重複防止する

Never:
- 本番キー（`sk_live_`）をコードにハードコードしない
- Webhookシグネチャ検証をスキップしない
- ユーザー入力を検証せずにStripe APIに渡さない
