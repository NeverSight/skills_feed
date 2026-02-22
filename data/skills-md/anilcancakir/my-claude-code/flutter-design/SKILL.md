---
name: flutter-design
description: "Flutter/Dart implementation patterns for Refactoring UI principles. COMPANION skill for mobile-app-design-mastery. ALWAYS activate for: Flutter theming, ThemeData, ColorScheme, TextTheme, BoxDecoration, Material 3, Flutter shadows, Flutter spacing, Flutter typography, Flutter dark mode, Flutter components, Flutter styling, Dart UI, Widget decoration. Provides ThemeData setup, color schemes, typography styles, spacing utilities, decoration patterns. Turkish: Flutter tema, Flutter renk, Flutter tasarım, Dart UI, widget stil. English: Flutter theming, Material Design, Flutter styling, widget decoration."
---

# Flutter Design Patterns

Flutter/Dart implementation companion for **mobile-app-design-mastery** skill. Translates Refactoring UI principles into Flutter code.

> **Prerequisite:** This skill provides Flutter-specific syntax. For mobile design theory and decision-making, reference `mobile-app-design-mastery` skill.

---

## ⚠️ CRITICAL: Project Theme First

**ALWAYS check existing theme configuration before creating new styles.**

If the project has `ThemeData`, `AppColors`, `AppTextStyles`, or similar—**USE THEM**:

```dart
// Check lib/core/theme/ or lib/config/
// Common patterns:
AppColors.primary
AppTextStyles.headline
AppSpacing.md
context.theme.colorScheme.primary
```

**Priority order:**

1. **Project-defined theme** (AppColors, AppTextStyles, custom ThemeExtension)
2. **Theme.of(context)** access
3. **Hardcoded values** as last resort only

---

## ThemeData Setup (Material 3)

```dart
MaterialApp(
  theme: ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.fromSeed(
      seedColor: Colors.blue, // Brand color
      brightness: Brightness.light,
    ),
    textTheme: _textTheme,
  ),
  darkTheme: ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.fromSeed(
      seedColor: Colors.blue,
      brightness: Brightness.dark,
    ),
    textTheme: _textTheme,
  ),
);
```

---

## Color Access Patterns

```dart
// ✅ CORRECT: Use ColorScheme
final colors = Theme.of(context).colorScheme;
Container(color: colors.primary)
Text('Hello', style: TextStyle(color: colors.onSurface))

// ✅ With extension
extension BuildContextX on BuildContext {
  ColorScheme get colors => Theme.of(this).colorScheme;
}
// Usage: context.colors.primary

// ❌ AVOID: Hardcoded colors
Container(color: Colors.blue) // Ignores theme
```

**ColorScheme roles:**

| Role | Light Mode | Dark Mode | Use Case |
|------|------------|-----------|----------|
| `primary` | Brand color | Lighter brand | CTAs, active states |
| `onPrimary` | White | Dark | Text on primary |
| `surface` | White | Gray-900 | Cards, sheets |
| `onSurface` | Gray-900 | White | Body text |
| `surfaceContainerHighest` | Gray-100 | Gray-800 | Elevated surfaces |
| `outline` | Gray-400 | Gray-600 | Borders |
| `error` | Red | Light red | Error states |

---

## Typography (TextTheme)

**Material 3 Type Scale:**

| Style | Size (sp) | Use Case |
|-------|-----------|----------|
| `displayLarge` | 57 | Hero text |
| `displayMedium` | 45 | Large display |
| `displaySmall` | 36 | Display |
| `headlineLarge` | 32 | Large headings |
| `headlineMedium` | 28 | Page titles |
| `headlineSmall` | 24 | Section titles |
| `titleLarge` | 22 | Card titles |
| `titleMedium` | 16 | Subtitles |
| `titleSmall` | 14 | Small titles |
| `bodyLarge` | 16 | Emphasis body |
| `bodyMedium` | 14 | Default body |
| `bodySmall` | 12 | Secondary text |
| `labelLarge` | 14 | Buttons |
| `labelMedium` | 12 | Labels |
| `labelSmall` | 11 | Captions |

```dart
// ✅ CORRECT: Use TextTheme
Text('Title', style: Theme.of(context).textTheme.headlineMedium)

// With extension
extension BuildContextX on BuildContext {
  TextTheme get textTheme => Theme.of(this).textTheme;
}
// Usage: context.textTheme.bodyMedium
```

---

## Spacing System (4dp Grid)

Create reusable spacing constants:

```dart
abstract class AppSpacing {
  static const double xs = 4;
  static const double sm = 8;
  static const double md = 12;
  static const double base = 16;
  static const double lg = 24;
  static const double xl = 32;
  static const double xxl = 48;
  
  // SizedBox shortcuts
  static const SizedBox gapXs = SizedBox(height: xs, width: xs);
  static const SizedBox gapSm = SizedBox(height: sm, width: sm);
  static const SizedBox gapMd = SizedBox(height: md, width: md);
  static const SizedBox gapBase = SizedBox(height: base, width: base);
  static const SizedBox gapLg = SizedBox(height: lg, width: lg);
}

// Usage
Padding(padding: EdgeInsets.all(AppSpacing.base))
Column(children: [widget1, AppSpacing.gapMd, widget2])
```

---

## BoxDecoration Patterns

### Card (Flat)

```dart
Container(
  decoration: BoxDecoration(
    color: colors.surface,
    borderRadius: BorderRadius.circular(12),
    border: Border.all(color: colors.outline.withOpacity(0.2)),
  ),
)
```

### Card (Elevated)

```dart
Container(
  decoration: BoxDecoration(
    color: colors.surface,
    borderRadius: BorderRadius.circular(12),
    boxShadow: [
      BoxShadow(
        color: Colors.black.withOpacity(0.08),
        blurRadius: 10,
        offset: const Offset(0, 2),
      ),
    ],
  ),
)
```

### Input Field

```dart
Container(
  decoration: BoxDecoration(
    color: colors.surface,
    borderRadius: BorderRadius.circular(8),
    border: Border.all(color: colors.outline),
  ),
)
```

---

## Shadow Scale

```dart
abstract class AppShadows {
  static List<BoxShadow> sm = [
    BoxShadow(
      color: Colors.black.withOpacity(0.05),
      blurRadius: 4,
      offset: const Offset(0, 1),
    ),
  ];
  
  static List<BoxShadow> md = [
    BoxShadow(
      color: Colors.black.withOpacity(0.08),
      blurRadius: 8,
      offset: const Offset(0, 2),
    ),
  ];
  
  static List<BoxShadow> lg = [
    BoxShadow(
      color: Colors.black.withOpacity(0.1),
      blurRadius: 16,
      offset: const Offset(0, 4),
    ),
  ];
  
  static List<BoxShadow> xl = [
    BoxShadow(
      color: Colors.black.withOpacity(0.15),
      blurRadius: 24,
      offset: const Offset(0, 8),
    ),
  ];
}

// Usage
Container(decoration: BoxDecoration(boxShadow: AppShadows.md))
```

---

## Anti-Patterns

```dart
// ❌ NEVER
Colors.blue                    // Hardcoded, ignores theme
TextStyle(fontSize: 16)        // Not from TextTheme
SizedBox(height: 17)           // Off 4dp grid
EdgeInsets.only(top: 20, left: 8)  // Asymmetric without reason

// ✅ INSTEAD
context.colors.primary
context.textTheme.bodyLarge
SizedBox(height: 16)           // On grid
EdgeInsets.all(16)             // Symmetric
```

---

## Reference Files

| Topic | File |
|-------|------|
| ThemeData & ColorScheme | [theming.md](references/theming.md) |
| Widget recipes | [widgets.md](references/widgets.md) |
| ThemeExtension patterns | [extensions.md](references/extensions.md) |
