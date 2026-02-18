---
name: core-web-vitals
description: "Core Web Vitals計測・診断スキル。Lighthouse CLI、Bundle Analyzer、パフォーマンス問題の特定と対策。"
---

# Core Web Vitals 計測・診断

パフォーマンス計測と問題診断に特化。最適化パターンは `vercel-react-best-practices` を参照。

---

## 目標値

| 指標 | Good | Needs Improvement | Poor |
|------|------|-------------------|------|
| **LCP** (Largest Contentful Paint) | < 2.5s | 2.5s - 4.0s | > 4.0s |
| **INP** (Interaction to Next Paint) | < 200ms | 200ms - 500ms | > 500ms |
| **CLS** (Cumulative Layout Shift) | < 0.1 | 0.1 - 0.25 | > 0.25 |
| **FCP** (First Contentful Paint) | < 1.8s | 1.8s - 3.0s | > 3.0s |
| **TTFB** (Time to First Byte) | < 800ms | 800ms - 1800ms | > 1800ms |

---

## 計測コマンド

### Lighthouse CLI

```bash
# デスクトップ
npx lighthouse https://example.com --view --preset=desktop

# モバイル
npx lighthouse https://example.com --view --preset=perf --emulated-form-factor=mobile

# アクセシビリティのみ
npx lighthouse http://localhost:3000 --only-categories=accessibility --view

# JSON出力で詳細確認
npx lighthouse http://localhost:3000 --output=json | jq '.audits["largest-contentful-paint"]'
```

### Bundle Analyzer

```bash
# Next.js
npm run build
npx @next/bundle-analyzer

# 汎用
npx source-map-explorer 'dist/**/*.js'
```

### Vercel Speed Insights

```bash
# Vercelダッシュボードで確認
# Analytics > Speed Insights
```

---

## 問題別診断

### LCP が遅い (> 2.5s)

**原因特定:**
```bash
npx lighthouse URL --output=json | jq '.audits["largest-contentful-paint-element"]'
```

**主な原因と対策:**

| 原因 | 対策 |
|------|------|
| ヒーロー画像が重い | `next/image` + `priority` + WebP |
| Webフォント読み込み | `next/font` + `display: swap` |
| サーバー応答遅い | キャッシュ、CDN、DB最適化 |
| render-blocking JS | 動的インポート、defer |

### INP が遅い (> 200ms)

**原因特定:**
- Chrome DevTools > Performance > Interactions

**主な原因と対策:**

| 原因 | 対策 |
|------|------|
| 重いイベントハンドラ | `useTransition`、Web Worker |
| 過剰な再レンダリング | React DevTools Profiler確認 |
| 長いJSタスク | タスク分割、`requestIdleCallback` |

### CLS が高い (> 0.1)

**原因特定:**
```bash
npx lighthouse URL --output=json | jq '.audits["layout-shift-elements"]'
```

**主な原因と対策:**

| 原因 | 対策 |
|------|------|
| 画像サイズ未指定 | `width` / `height` 必須 |
| 動的コンテンツ挿入 | スケルトンで領域確保 |
| Webフォント切り替え | `font-display: swap` + fallback |
| 広告/埋め込み | 固定サイズコンテナ |

### FCP が遅い (> 1.8s)

**主な原因と対策:**

| 原因 | 対策 |
|------|------|
| 初期HTMLが大きい | Server Components、ストリーミング |
| render-blocking CSS | Critical CSS inline |
| TTFB が遅い | サーバー最適化 |

---

## チェックリスト

### 計測
- [ ] Lighthouse モバイル/デスクトップ両方確認
- [ ] 実機でも確認（エミュレーションと差異あり）
- [ ] 本番環境で計測（開発環境は参考値）

### 監視
- [ ] Vercel Speed Insights 設定
- [ ] アラート閾値設定（LCP > 3s等）
- [ ] 定期レポート確認

---

## 関連スキル

- **vercel-react-best-practices**: 最適化パターン（57ルール）
- **ui-ux-pro-max**: アクセシビリティ（WCAG コントラスト）
