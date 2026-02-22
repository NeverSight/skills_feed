---
name: maui-ui-best-practices
description: Defines recommended UI/UX patterns, layout strategies, styling conventions, accessibility rules, and performance guidelines for .NET MAUI applications.
---

# .NET MAUI — UI Best Practices Skill

## Purpose

This skill defines the recommended UI/UX patterns, layout strategies, styling conventions, accessibility rules, and performance guidelines for .NET MAUI applications. It ensures that all generated UI code is consistent, maintainable, responsive, and aligned with modern cross-platform design expectations.

The goal is to help agents produce clean, scalable, and accessible XAML and C# UI code across Android, iOS, Windows, and MacCatalyst.

## Core Principles

1. **Simplicity first**
   Use minimal layout nesting, clear structure, and predictable patterns.
2. **Consistency**
   Centralize styles, colors, and fonts in `Resources/Styles`.
3. **Responsiveness**
   Use adaptive layouts (`OnIdiom`, `OnPlatform`, `Grid`, `FlexLayout`) to support all devices.
4. **Accessibility**
   Provide semantic properties, proper contrast, and screen reader support.
5. **Performance**
   Prefer compiled bindings, lightweight controls, and efficient layout containers.

## Categories of Rules

- Layout & Structure
- Styling & Theming
- Controls & Components
- Accessibility
- Performance

Each rule is stored in the `rules/` directory and should be applied whenever generating UI code.

## Agent Usage Guidelines

- When generating XAML, follow the layout and styling rules.
- When creating new pages, apply consistent structure:
  - Root layout should be `Grid` or `VerticalStackLayout`.
  - Avoid deeply nested layouts.
  - Use styles instead of inline properties.
- When generating controls, prefer reusable components in `/Views/Controls`.
- When asked to “make the UI responsive,” apply idiom/platform conditions.
- When asked to “improve performance,” apply rules from the performance category.

## Out of Scope

- Business logic (covered in other skills)
- Authentication UI flows (covered in `maui-authentication`)
- Deployment or platform packaging
