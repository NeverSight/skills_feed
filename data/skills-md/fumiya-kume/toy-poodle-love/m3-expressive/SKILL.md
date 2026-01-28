---
name: m3-expressive
description: |
  This skill should be used when the user asks to "implement Material 3 Expressive",
  "add spring animations", "use MotionScheme", "create expressive button",
  "add loading indicator", "implement FAB menu", "use shape morphing",
  "create floating toolbar", "add carousel", "implement ButtonGroup",
  "use MaterialShapes", "implement vibrant FAB", "add expressive UI",
  "configure MaterialExpressiveTheme", "use spring physics animation",
  "Material 3 Expressive を実装", "スプリングアニメーション", "MotionScheme を使用",
  "表現力豊かなボタン", "ローディングインジケーター", "FABメニュー",
  "シェイプモーフィング", "フローティングツールバー", "カルーセル",
  "ButtonGroup を追加", "MaterialShapes を使用", "Vibrant FAB",
  "MaterialExpressiveTheme を設定", "物理ベースアニメーション",
  or needs guidance on Material 3 Expressive implementation for Android
  with Jetpack Compose, including MotionScheme, spring animations,
  shape morphing, and new expressive components for Android API 24+.
version: 1.0.0
---

# Material 3 Expressive for Jetpack Compose

Android Jetpack Compose 向けの Material 3 Expressive 実装ガイド。Google I/O 2025 で発表された最新のデザインシステムアップデートです。

## Overview

**Target Platform**: Android API 24+ / Jetpack Compose 1.7+ / Kotlin 1.9+

**Design Philosophy**:
- Physics-based animations（物理ベースアニメーション）
- 35種類の新しいシェイプによる表現力豊かなUI
- Variable fonts によるダイナミックタイポグラフィ
- Extended color tokens による深いトーナルパレット
- 18,000人以上のユーザーリサーチに基づく設計

**Core Features**:
- **MotionScheme**: Spring-based animation system（standard/expressive）
- **MaterialShapes**: 35種類のシェイプ + モーフィングトランジション
- **New Components**: LoadingIndicator, ButtonGroup, FAB Menu, Floating Toolbar, Carousel
- **Enhanced Theming**: MaterialExpressiveTheme() による統合カスタマイズ

## Quick Start Checklist

Material 3 Expressive を実装する際の必須手順：

1. **依存関係を追加**
   ```kotlin
   // build.gradle.kts
   dependencies {
       // Material 3 Expressive (alpha)
       implementation("androidx.compose.material3:material3:1.4.0-alpha15")

       // または BOM を使用
       implementation(platform("androidx.compose:compose-bom:2024.12.01"))
       implementation("androidx.compose.material3:material3")
   }
   ```

2. **Experimental API のオプトインを追加**
   ```kotlin
   // ファイルレベル
   @file:OptIn(ExperimentalMaterial3ExpressiveApi::class)

   // または関数レベル
   @OptIn(ExperimentalMaterial3ExpressiveApi::class)
   @Composable
   fun MyExpressiveComponent() { ... }
   ```

3. **MaterialExpressiveTheme でアプリをラップ**
   ```kotlin
   @OptIn(ExperimentalMaterial3ExpressiveApi::class)
   @Composable
   fun MyApp() {
       MaterialExpressiveTheme(
           motionScheme = MotionScheme.expressive()
       ) {
           // App content
       }
   }
   ```

4. **MotionScheme を選択**
   - `MotionScheme.expressive()`: バウンス感のある活発なアニメーション（推奨）
   - `MotionScheme.standard()`: 落ち着いた控えめなアニメーション

## Core Concepts

| 概念 | 説明 | 用途 |
|------|------|------|
| **MotionScheme** | Spring-based animation system | 全体的なアニメーション制御 |
| **MaterialShapes** | 35種類の新しいシェイプ | ボタン、カード、コンポーネント |
| **Shape Morphing** | 形状間のスムーズな遷移 | 押下/選択状態の視覚効果 |
| **Spatial Specs** | 形状・境界変更用アニメーション | コンポーネントのサイズ変更 |
| **Effects Specs** | 色・透明度変更用アニメーション | 色のトランジション |

## Motion System

### Spring Physics

M3 Expressive は duration-based から physics-based へアニメーションを刷新：

```kotlin
// Spring の主要パラメータ
// Stiffness: バネの硬さ（高いほど速く収束）
// Damping Ratio: 減衰率（1.0で臨界減衰、低いほどバウンス）

val customSpring = spring<Float>(
    stiffness = Spring.StiffnessMedium,
    dampingRatio = Spring.DampingRatioMediumBouncy
)
```

### MotionScheme 種類

| Scheme | Damping | 特徴 | 用途 |
|--------|---------|------|------|
| `expressive()` | 低い | オーバーシュート、バウンス | ヒーローモーメント、主要インタラクション |
| `standard()` | 高い | 控えめ、機能的 | ユーティリティアプリ |

### Spring Speeds

| Speed | 用途 |
|-------|------|
| `fast` | 小さなコンポーネント（Switch, Checkbox） |
| `default` | 中間サイズのコンポーネント（Button, Card） |
| `slow` | フルスクリーン遷移、大きなアニメーション |

詳細: [references/motion-system.md](references/motion-system.md)

## Shape Library

### 35種類の MaterialShapes

M3 Expressive は丸角長方形を超えた多様なシェイプを提供：

```kotlin
// 使用例
IconButton(
    onClick = { },
    shape = MaterialShapes.Cookie9Sided
) {
    Icon(Icons.Default.Add, contentDescription = null)
}
```

### Shape Morphing

押下時やチェック状態でシェイプがスムーズに変化：

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun MorphingIconButton() {
    var isChecked by remember { mutableStateOf(false) }

    IconToggleButton(
        checked = isChecked,
        onCheckedChange = { isChecked = it }
    ) {
        Icon(
            imageVector = if (isChecked) Icons.Filled.Favorite else Icons.Outlined.FavoriteBorder,
            contentDescription = null
        )
    }
}
```

詳細: [references/shape-library.md](references/shape-library.md)

## New Components

### LoadingIndicator

`CircularProgressIndicator` に代わる新しいローディング表示：

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun LoadingExample() {
    // 基本的なローディング
    LoadingIndicator()

    // コンテナ付き
    ContainedLoadingIndicator(
        containerColor = MaterialTheme.colorScheme.primaryContainer
    )
}
```

詳細: [references/loading-indicators.md](references/loading-indicators.md)

### ButtonGroup

接続されたボタン群による選択UI：

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun ButtonGroupExample() {
    var selectedIndex by remember { mutableIntStateOf(0) }

    ButtonGroup {
        ToggleButton(
            checked = selectedIndex == 0,
            onCheckedChange = { selectedIndex = 0 }
        ) {
            Text("Option 1")
        }
        ToggleButton(
            checked = selectedIndex == 1,
            onCheckedChange = { selectedIndex = 1 }
        ) {
            Text("Option 2")
        }
    }
}
```

詳細: [references/button-group.md](references/button-group.md)

### FloatingActionButtonMenu

展開式 FAB メニュー：

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun FABMenuExample() {
    var expanded by remember { mutableStateOf(false) }

    FloatingActionButtonMenu(
        expanded = expanded,
        button = {
            ToggleFloatingActionButton(
                checked = expanded,
                onCheckedChange = { expanded = it }
            ) {
                Icon(
                    imageVector = if (expanded) Icons.Default.Close else Icons.Default.Add,
                    contentDescription = "Toggle menu"
                )
            }
        }
    ) {
        FloatingActionButtonMenuItem(
            onClick = { /* action */ },
            icon = { Icon(Icons.Default.Edit, null) },
            text = { Text("Edit") }
        )
        FloatingActionButtonMenuItem(
            onClick = { /* action */ },
            icon = { Icon(Icons.Default.Share, null) },
            text = { Text("Share") }
        )
    }
}
```

詳細: [references/fab-components.md](references/fab-components.md)

### Floating Toolbar

水平/垂直フローティングツールバー：

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun FloatingToolbarExample() {
    var expanded by remember { mutableStateOf(true) }

    HorizontalFloatingToolbar(
        expanded = expanded,
        floatingActionButton = {
            FloatingToolbarDefaults.VibrantFloatingActionButton(
                onClick = { /* action */ }
            ) {
                Icon(Icons.Default.Add, contentDescription = null)
            }
        }
    ) {
        IconButton(onClick = { }) {
            Icon(Icons.Default.Edit, contentDescription = "Edit")
        }
        IconButton(onClick = { }) {
            Icon(Icons.Default.Delete, contentDescription = "Delete")
        }
    }
}
```

詳細: [references/floating-toolbar.md](references/floating-toolbar.md)

### Carousel

複数アイテム表示のカルーセル：

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun CarouselExample() {
    val items = listOf("Item 1", "Item 2", "Item 3", "Item 4")

    HorizontalMultiBrowseCarousel(
        state = rememberCarouselState { items.count() },
        modifier = Modifier.height(200.dp),
        preferredItemWidth = 150.dp
    ) { index ->
        Card(
            modifier = Modifier.fillMaxSize()
        ) {
            Text(
                text = items[index],
                modifier = Modifier.padding(16.dp)
            )
        }
    }
}
```

詳細: [references/carousel.md](references/carousel.md)

## Theming

### MaterialExpressiveTheme

```kotlin
@OptIn(ExperimentalMaterial3ExpressiveApi::class)
@Composable
fun MyApp() {
    MaterialExpressiveTheme(
        colorScheme = dynamicColorScheme(LocalContext.current),
        typography = Typography,
        shapes = Shapes,
        motionScheme = MotionScheme.expressive()
    ) {
        Surface(
            modifier = Modifier.fillMaxSize(),
            color = MaterialTheme.colorScheme.background
        ) {
            MainContent()
        }
    }
}
```

詳細: [references/theming.md](references/theming.md)

## Common Errors

| エラー | 原因 | 解決策 |
|--------|------|--------|
| `Unresolved reference: MaterialExpressiveTheme` | 依存関係が古い | `material3:1.4.0-alpha15` 以上を使用 |
| `This declaration is experimental` | OptIn 未指定 | `@OptIn(ExperimentalMaterial3ExpressiveApi::class)` を追加 |
| `Unresolved reference: MotionScheme` | Compose バージョン不足 | compose-bom 2024.12.01 以上を使用 |
| `Shape morphing not working` | Theme 設定不足 | `MaterialExpressiveTheme` でラップ |
| `LoadingIndicator not found` | Import 不足 | `import androidx.compose.material3.LoadingIndicator` |
| `ButtonGroup compilation error` | Kotlin バージョン | Kotlin 1.9+ を使用 |

## Additional Resources

### References
- [Motion System](references/motion-system.md) - Spring physics, MotionScheme 詳細
- [Shape Library](references/shape-library.md) - 35種類のシェイプ、モーフィング
- [Typography](references/typography.md) - Variable fonts, type scale
- [Color System](references/color-system.md) - Design tokens, palettes
- [Loading Indicators](references/loading-indicators.md) - LoadingIndicator コンポーネント
- [Button Group](references/button-group.md) - ButtonGroup 実装
- [FAB Components](references/fab-components.md) - FAB Menu, Vibrant FAB
- [Floating Toolbar](references/floating-toolbar.md) - ツールバーコンポーネント
- [Carousel](references/carousel.md) - カルーセル実装
- [Expressive Menus](references/expressive-menus.md) - 新メニューシステム
- [Theming](references/theming.md) - MaterialExpressiveTheme カスタマイズ
- [Migration Guide](references/migration-guide.md) - M3 → M3 Expressive 移行
- [Troubleshooting](references/troubleshooting.md) - トラブルシューティング

### Examples
- [Basic Setup](examples/basic-setup.kt) - テーマ設定基本
- [Motion Scheme](examples/motion-scheme-examples.kt) - MotionScheme 使用例
- [Shape Morphing](examples/shape-morphing-button.kt) - シェイプモーフィング
- [Loading Indicator](examples/loading-indicator-example.kt) - ローディング
- [Button Group](examples/button-group-example.kt) - ボタングループ
- [FAB Menu](examples/fab-menu-example.kt) - FAB メニュー
- [Floating Toolbar](examples/floating-toolbar-example.kt) - ツールバー
- [Carousel](examples/carousel-example.kt) - カルーセル
- [Expressive List](examples/expressive-list-example.kt) - リストアイテム
- [Complete Screen](examples/complete-screen-example.kt) - 完全な画面例

### External Resources
- [Material Design 3 in Compose](https://developer.android.com/develop/ui/compose/designsystems/material3)
- [M3 Expressive Motion System](https://m3.material.io/blog/m3-expressive-motion-theming)
- [Compose Material 3 Releases](https://developer.android.com/jetpack/androidx/releases/compose-material3)
- [Material 3 Expressive Catalog (GitHub)](https://github.com/meticha/material-3-expressive-catalog)
