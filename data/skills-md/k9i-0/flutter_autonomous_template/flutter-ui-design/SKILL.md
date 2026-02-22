---
name: flutter-ui-design
description: Modern UI design guidelines for Flutter apps. Achieve refined visuals based on Material Design 3.
---

# Flutter UI Design Guidelines

## Purpose

This skill provides guidelines to make Flutter app UIs stand out from "typical defaults" and achieve professional, impressive designs.

## Typography

### Patterns to Avoid
- Using only default `Roboto`
- Monotonous font weights (Regular/Bold only)
- Uniform text sizes

### Recommended Approach

```dart
// Use modern fonts with Google Fonts
import 'package:google_fonts/google_fonts.dart';

// For titles: Distinctive display fonts
GoogleFonts.poppins(fontWeight: FontWeight.w700)
GoogleFonts.inter(fontWeight: FontWeight.w800)
GoogleFonts.plusJakartaSans()

// For body: Readable sans-serif
GoogleFonts.inter()
GoogleFonts.dmSans()

// Size hierarchy with contrast in mind
headlineLarge: 32sp, weight: 800
headlineMedium: 24sp, weight: 700
titleLarge: 20sp, weight: 600
bodyLarge: 16sp, weight: 400
labelSmall: 12sp, weight: 500
```

### Font Weight Usage
- Extreme contrast: Combine `w300` and `w800`
- Bold for headings (w600-w800), regular for body (w400)

## Color & Theme

### Patterns to Avoid
- Material Design default blue/purple
- Subtle, uniform color palettes
- Gray-only safe UIs

### Recommended Approach

```dart
// Dark theme: Deep background + vivid accents
ColorScheme.dark(
  surface: Color(0xFF0F0F14),        // Deep dark gray
  surfaceContainerHighest: Color(0xFF1A1A23),
  primary: Color(0xFF6366F1),         // Vivid indigo
  secondary: Color(0xFF22D3EE),       // Cyan accent
  tertiary: Color(0xFFF472B6),        // Pink accent
)

// Light theme: Clean white + vivid accents
ColorScheme.light(
  surface: Color(0xFFFAFAFC),
  surfaceContainerHighest: Color(0xFFF1F5F9),
  primary: Color(0xFF4F46E5),         // Indigo
  secondary: Color(0xFF0EA5E9),       // Sky blue
  tertiary: Color(0xFFEC4899),        // Pink
)
```

### Color Usage Points
- **Dominant Color**: Use one primary color boldly
- **Sharp Accents**: Use secondary color sparingly as accent
- **Semantic Colors**: Success=green, Error=red, Warning=yellow intuitively

## Elevation & Depth

### Patterns to Avoid
- Too flat designs
- Uniform elevation
- Overusing shadows

### Recommended Approach

```dart
// Cards with subtle depth
Card(
  elevation: 0,
  shape: RoundedRectangleBorder(
    borderRadius: BorderRadius.circular(16),
  ),
  color: theme.colorScheme.surfaceContainerHighest,
  child: ...
)

// Soft shadow (low contrast)
BoxDecoration(
  borderRadius: BorderRadius.circular(16),
  boxShadow: [
    BoxShadow(
      color: Colors.black.withOpacity(0.04),
      blurRadius: 10,
      offset: Offset(0, 4),
    ),
  ],
)

// Glassmorphism effect
ClipRRect(
  borderRadius: BorderRadius.circular(16),
  child: BackdropFilter(
    filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
    child: Container(
      color: Colors.white.withOpacity(0.1),
      child: ...
    ),
  ),
)
```

## Motion & Animation

### Patterns to Avoid
- Rigid UI without animations
- Excessive, scattered animations
- Inconsistent timing

### Recommended Approach

```dart
// Page transition: Smooth fade+slide
PageRouteBuilder(
  transitionDuration: Duration(milliseconds: 300),
  pageBuilder: (_, __, ___) => DestinationPage(),
  transitionsBuilder: (_, animation, __, child) {
    return FadeTransition(
      opacity: animation,
      child: SlideTransition(
        position: Tween<Offset>(
          begin: Offset(0, 0.05),
          end: Offset.zero,
        ).animate(CurvedAnimation(
          parent: animation,
          curve: Curves.easeOutCubic,
        )),
        child: child,
      ),
    );
  },
)

// List items: Staggered Animation
AnimatedList + interval-based delays

// Tap feedback: Subtle scale
Transform.scale(
  scale: isPressed ? 0.98 : 1.0,
  child: AnimatedContainer(
    duration: Duration(milliseconds: 100),
    ...
  ),
)
```

### Timing Guidelines
- **Short operations (tap)**: 100-150ms
- **Screen transitions**: 250-350ms
- **Complex animations**: 400-600ms
- **Curve**: Base on `easeOutCubic`, `easeInOutCubic`

## Layout & Spacing

### Patterns to Avoid
- Cramped UI
- Irregular padding
- Insufficient spacing between elements

### Recommended Approach

```dart
// 8px-based spacing system
const spacing = (
  xs: 4.0,
  sm: 8.0,
  md: 16.0,
  lg: 24.0,
  xl: 32.0,
  xxl: 48.0,
);

// Content area margins
Padding(
  padding: EdgeInsets.symmetric(horizontal: 20, vertical: 16),
  child: ...
)

// Card padding larger than outer
Card(
  child: Padding(
    padding: EdgeInsets.all(20),
    child: ...
  ),
)

// Gaps between elements
SizedBox(height: 16) // Between related elements
SizedBox(height: 32) // Between sections
```

## Components

### Buttons

```dart
// Primary button: Rounded corners + sufficient padding
FilledButton(
  style: FilledButton.styleFrom(
    padding: EdgeInsets.symmetric(horizontal: 24, vertical: 16),
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(12),
    ),
  ),
  child: Text('Action'),
)

// Outline button
OutlinedButton(
  style: OutlinedButton.styleFrom(
    side: BorderSide(color: theme.colorScheme.outline, width: 1.5),
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(12),
    ),
  ),
)
```

### Input Fields

```dart
TextField(
  decoration: InputDecoration(
    filled: true,
    fillColor: theme.colorScheme.surfaceContainerHighest,
    border: OutlineInputBorder(
      borderRadius: BorderRadius.circular(12),
      borderSide: BorderSide.none,
    ),
    focusedBorder: OutlineInputBorder(
      borderRadius: BorderRadius.circular(12),
      borderSide: BorderSide(
        color: theme.colorScheme.primary,
        width: 2,
      ),
    ),
    contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 16),
  ),
)
```

### FAB

```dart
FloatingActionButton(
  elevation: 2,
  shape: RoundedRectangleBorder(
    borderRadius: BorderRadius.circular(16),
  ),
  child: Icon(Icons.add),
)
```

## Background

### Recommended Techniques

```dart
// Gradient background
Container(
  decoration: BoxDecoration(
    gradient: LinearGradient(
      begin: Alignment.topLeft,
      end: Alignment.bottomRight,
      colors: [
        theme.colorScheme.surface,
        theme.colorScheme.surface.withOpacity(0.95),
      ],
    ),
  ),
)

// Subtle pattern (dots, grid)
CustomPaint(
  painter: DotPatternPainter(
    color: theme.colorScheme.outline.withOpacity(0.05),
    spacing: 20,
  ),
)
```

## Checklist

Checklist when implementing UI:

- [ ] Using fonts other than default
- [ ] Color palette has accent colors
- [ ] Appropriate margins/padding are set
- [ ] Interactions have feedback (animations)
- [ ] Component corner radii are unified (12-16px recommended)
- [ ] Text hierarchy (size/weight) is clear
