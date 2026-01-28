---
name: apple-design
description: Provides Apple-style modern UI design guidelines with monotone dark mode, blue accent colors, and minimal refined interface. Activates when user mentions "dark mode", "minimal UI", "Apple style", "ダークモード", "ミニマルデザイン", "UIコンポーネント作成".
allowed-tools: Read, Grep, Glob, Edit, Write
user-invocable: true
---

# Apple Design System

このプロジェクトのデフォルトUIスタイル。

## When to Use This Skill

- 新規UIコンポーネントを作成する時（デフォルト）
- ダークモードのデザインを実装する時
- ミニマルで洗練されたインターフェースを作成する時
- アニメーションやトランジションを実装する時
- 既存コンポーネントのスタイルを統一する時

## 詳細なガイドライン

UIコンポーネント編集時は `.claude/rules/ui-design.md` が自動適用されます。

## デザイン哲学

1. **ミニマリズム**: 必要最小限の要素で最大の効果
2. **明確な階層**: 視覚的な優先順位が一目で分かる
3. **流動性**: スムーズなアニメーションと自然な動き
4. **余白の美学**: 適切なスペーシングで呼吸する空間

## カラーパレット（簡略）

```typescript
const colors = {
  background: '#000000',
  card: '#1C1C1E',
  accent: '#0A84FF',
  text: '#FFFFFF',
  textSecondary: '#EBEBF5',
};
```

## 主要原則

- モノトーン（黒・グレー・白）を基調
- アクセントカラーは青系（#0A84FF）のみ
- ミニマルでクリーンなデザイン
- アニメーション: 200-300ms
- タッチターゲット: 最小44x44px

## AI Assistant Instructions

このスキルが有効化された時:

1. **デフォルト適用**: このプロジェクトの標準スタイル
2. **カラーパレット確認**: モノトーン基調、青系アクセントのみ
3. **余白の確認**: 適切なスペーシングで「呼吸する空間」を確保

Always:
- ダークモード（背景#000000）を基本にする
- アクセントカラーは青系（#0A84FF）のみ使用する
- アニメーションは200-300msで自然な動きにする
- タッチターゲットは最小44x44pxを確保する
- 余白を十分に取り、視覚的な階層を明確にする

Never:
- 派手な色やグラデーションを使用しない
- 複数のアクセントカラーを混在させない
- アニメーションを過度に長くしない（300ms超）
- Material Designスタイルと混在させない
