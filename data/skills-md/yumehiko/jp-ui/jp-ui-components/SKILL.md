---
name: jp-ui-components
description: jp-uiのコンポーネント作成とStorybook Page作成のルールを守るためのスキル。Base UIラッパーの方針、render/useRenderの維持、レイアウト/余白/幅ルールを適用する。
---

# jp-ui Components

## 方針

- 既存のPageに合わせる: `src/pages/ColorsPage.*`, `src/pages/IconsPage.*`, `src/pages/TypesettingPage.*` を基準にする。
- Pageは基本「背景・文字色・上下余白」を持つラッパーで、**中身は適切なmax-widthのコンテナで中央寄せ**する。
- 「幅を満たす系（Field, InputBoxなど）」も、**コンテナの幅はmax-widthで制限し、要素はコンテナ幅100%** にする。
- ルールを守らない実装が出やすいので、**幅・中央寄せ・コンテナ構造は明示的にコード化**する。

## 実装ルール（必須）

1) **Pageラッパー**
   - `padding` と `background`/`color` を指定する。
   - 例: `padding: 32px 16px 80px; background-color: var(--surface); color: var(--on-surface);`

2) **中央寄せコンテナ**
   - `max-width` は **デフォルト 640px** とする。
   - 特別な指定がある場合のみ、その数値を使う（例: 一覧/グリッドで `max-width: 960px`）。
   - `margin: 0 auto; width: 100%;` を指定する。

3) **幅を満たす系アイテム（Field, InputBox など）**
   - **コンテナ内で `width: 100%`** とし、コンテナのmax-widthで制約する。
   - 画面全幅に引き伸ばさない。必ず中央寄せコンテナの中に置く。

## コンポーネント作成ルール（必須）

1) **Base UIラッパーが原則**
   - Base UIコンポーネントは原則ラッパーTSXを作り、利用体験を統一する（className自動付与・variant/slotの共通化など）。
   - 例外として、ラッパーが不要なほど単純な場合のみBase UIを直接使用する。

2) **render/useRenderの維持**
   - Base UIの`render`の仕組みは壊さない。`className` が関数のときも必ずマージする。
   - 自前コンポーネントは`useRender`を使い、`render`を透過できるAPIにする。

3) **テンプレ利用**
   - Base UIラッパーは `templates/base-ui-wrapper.tsx` をベースに作成する。
   - 自前コンポーネントは `templates/custom-use-render.tsx` をベースに作成する。

4) **Exampleを正にする**
   - 各コンポーネントには `Example.tsx` を同階層に作り、**Exampleを実装例の正**とする。
   - Storybookの`Default`は `render: () => <Example />` を基本とする。
   - `docs/llm` は Example を元に自動生成されるため、**Exampleが実装例の唯一の情報源**になる。
   - 同一ディレクトリに複数コンポーネントがある場合は `*Example.tsx` で区別して良い。

## 推奨構成（最小形）

```tsx
// src/pages/FooPage.tsx
import styles from './FooPage.module.css';

export function FooPage() {
  return (
    <div className={styles.Page}>
      <div className={styles.Container}>
        {/* contents */}
      </div>
    </div>
  );
}
```

```css
/* src/pages/FooPage.module.css */
.Page {
  padding: 32px 16px 80px;
  background-color: var(--surface);
  color: var(--on-surface);
}

.Container {
  width: 100%;
  max-width: 640px; /* default. override when specified */
  margin: 0 auto;
}
```

## 追加メモ

- 既存Pageの実装に合わせて、`display: grid` や `gap` は必要に応じて追加する。
- ルールがぶれそうな場合は、**Containerの責務をコメントで短く明示**する。
