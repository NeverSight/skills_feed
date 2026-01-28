---
name: material-design
description: Provides Google Material Design 3 (Material You) guidelines with dynamic color system, adaptive design, and accessibility focus. Activates when user mentions "Material You", "Material Design", "Google style", "マテリアルデザイン", "アクセシビリティ".
allowed-tools: Read, Grep, Glob, Edit, Write
user-invocable: true
---

# Material Design 3 (Material You)

このプロジェクトでは **Apple風ダークモード** を基本採用していますが、Material Design 3スタイルが必要な場合はこのスキルを使用してください。

## When to Use This Skill

- Material Design 3スタイルのUIコンポーネントを作成する時
- 動的カラーシステム（Material You）を実装する時
- Google風のデザインが明示的に要求された時
- アクセシビリティ重視のコンポーネントを作成する時
- State Layersやリップルエフェクトを実装する時

## 詳細なガイドライン

UIコンポーネント編集時は `.claude/rules/ui-design.md` が自動適用されます。

Material Design 3の詳細な実装が必要な場合は、以下の公式リソースを参照:

- [Material Design 3](https://m3.material.io/)
- [Color Roles](https://m3.material.io/styles/color/roles)
- [Components](https://m3.material.io/components)

## カラーロールシステム（簡略）

```typescript
const colorRoles = {
  primary: '#6750A4',
  onPrimary: '#FFFFFF',
  secondary: '#625B71',
  surface: '#FEF7FF',
  error: '#B3261E',
};
```

## 主要原則

1. **カラーロールシステム** を使用（直接色指定しない）
2. **アクセシビリティファースト** - コントラスト4.5:1以上
3. **State Layers** でインタラクティブ状態を表現
4. **タッチターゲット** 最小48x48dp

## AI Assistant Instructions

このスキルが有効化された時:

1. **デフォルト確認**: このプロジェクトはApple風が基本。Material Designが明示的に要求されているか確認
2. **カラーロール使用**: 直接色指定ではなくsemantic tokensを使用
3. **アクセシビリティ検証**: コントラスト比を確認

Always:
- カラーロールシステム（primary, secondary, surface等）を使用する
- タッチターゲットは最小48x48dpを確保する
- State Layers（hover: 8%, pressed: 12%等）を実装する
- コントラスト比4.5:1以上を確保する

Never:
- 直接色コード（#RRGGBB）をハードコードしない
- アクセシビリティ要件を無視しない
- Apple風デザインと混在させない（どちらかに統一）
