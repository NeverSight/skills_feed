---
name: wpf-ui-shell
description: Create or refactor a .NET 8 WPF shell for a desktop widget host using CommunityToolkit.Mvvm and a custom viewmodel-first navigation service. Use when working on App.xaml, MainWindow/ShellWindow, shared ResourceDictionaries, runtime Light/Dark theming, or shell layout for widget-style apps. Avoid Prism, Frame navigation, and heavy region managers.
---

# Wpf Ui Shell

## Overview

Define the primary shell window, shared resources, and navigation contract for a WPF widget host app.

## Constraints

- Target .NET 8
- CommunityToolkit.Mvvm
- ViewModel-first navigation via a custom service
- No Prism, no Frame navigation, no heavy region manager
- Fluent-inspired design system using native WPF styles
- Light/Dark themes via ResourceDictionaries with runtime switching
- Single shell window as primary host; secondary windows for widgets/tools/dialogs

## Definition of done (DoD)

- Shell uses ContentControl host (not Frame) for navigation
- Navigation service updates CurrentViewModel, views resolve via DataTemplate
- Theme switching works at runtime without restart
- Secondary windows inherit shared resources
- Tray icon provides app access when shell is hidden

## Workflow

1. Locate shell files: `App.xaml`, shell window XAML/code-behind, and theme dictionaries.
2. Confirm the shell layout uses a `ContentControl` host (not `Frame`).
3. Define or update the navigation service and VM-to-view mapping.
4. Centralize shared styles in merged dictionaries and keep view XAML lean.
5. Add runtime theme switching by swapping merged dictionaries.
6. Ensure secondary windows inherit the same resources and chrome rules.

## Shell layout pattern

Use a minimal, durable layout with explicit regions and a content host:

```xml
<Grid>
  <Grid.RowDefinitions>
    <RowDefinition Height="Auto" />
    <RowDefinition Height="*" />
  </Grid.RowDefinitions>

  <DockPanel Grid.Row="0">
    <!-- Title bar / nav -->
  </DockPanel>

  <ContentControl Grid.Row="1"
                  Content="{Binding CurrentViewModel}" />
</Grid>
```

## ViewModel-first navigation

Map view models to views using DataTemplates in `App.xaml` (or a merged dictionary). The
navigation service updates `CurrentViewModel` on the shell VM.

```xml
<DataTemplate DataType="{x:Type vm:HomeViewModel}">
  <views:HomeView />
</DataTemplate>
```

## Resource dictionaries and themes

- Keep colors, brushes, typography, and control styles in merged dictionaries.
- Split themes into `Themes/Light.xaml` and `Themes/Dark.xaml`.
- Switch themes by replacing the theme dictionary at runtime.

## References

- `references/shell-layouts.md` for layout variants (title bar, nav, content host).
- `references/navigation-service.md` for VM-first navigation patterns.
- `references/theme-switching.md` for dictionary swap details.
- `references/design-system.md` for Fluent-inspired style guidance.
