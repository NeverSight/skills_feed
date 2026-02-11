---
name: swiftui
description: SwiftUI framework for building user interfaces
version: 1.0
---

# SwiftUI Skill

## When to Use This Skill

Use this skill when:
- Building user interfaces with SwiftUI
- Working with SwiftUI views, modifiers, and layouts
- Implementing state management with @State, @Binding, @ObservableObject
- Creating animations and transitions
- Implementing navigation with NavigationStack, NavigationLink, TabView
- Working with data flow patterns (@Environment, @EnvironmentObject)
- Using SwiftUI controls (Button, TextField, Picker, etc.)
- Building cross-platform apps for iOS, macOS, watchOS, tvOS, visionOS

## Description
Complete SwiftUI framework documentation covering views, modifiers, layout, state management, animations, navigation, data flow, and all SwiftUI APIs for iOS, macOS, watchOS, tvOS, and visionOS.

## Quick Reference

### Core Components

### Accessibility
- `AccessibilityTraits`

### Animations
- `Animation`
- `AnyTransition`
- `Transition`

### Api Reference
- `Capsule`
- `Circle`
- `Commands`
- `ConfirmationDialog`
- `DisclosureGroup`
- `Ellipse`
- `ForEach`
- `Form`
- `FullScreenCover`
- `Gauge`
- `GeometryProxy`
- `GeometryReader`
- `GroupBox`
- `ImmersiveSpace`
- `List`
- `Menu`
- `MenuBarExtra`
- `ObservedObject`
- `OutlineGroup`
- `Published`
- `Rectangle`
- `RoundedRectangle`
- `Section`
- `SecureField`
- `SwiftUI`
- `Toolbar`
- `ToolbarItem`
- `ToolbarItemGroup`

### App Structure
- `DocumentGroup`
- `Scene`
- `Settings`
- `WindowGroup`

### Controls
- `Button`
- `DatePicker`
- `Picker`
- `Slider`
- `Stepper`
- `Toggle`

### Data Flow
- `FocusedSceneValue`
- `PreferenceKey`

### Drawing
- `Canvas`
- `Path`

### Essentials
- `App`
- `AppStorage`

### Gestures
- `DigitalCrownRotationalSensitivity`
- `DragGesture`
- `LongPressGesture`
- `MagnificationGesture`
- `RotationGesture`
- `TapGesture`

### Layout
- `Divider`
- `Grid`
- `GridRow`
- `HStack`
- `LazyHGrid`
- `LazyHStack`
- `LazyVGrid`
- `LazyVStack`
- `NavigationStack`
- `Spacer`
- `VStack`
- `ZStack`

### Navigation
- `Alert`
- `Link`
- `NavigationLink`
- `NavigationPath`
- `Popover`
- `Sheet`
- `Table`
- `TableColumn`
- `WKInterfaceObjectRepresentable`

### State Management
- `Binding`
- `Environment`
- `EnvironmentObject`
- `FocusState`
- `Observable`
- `ObservableObject`
- `SceneStorage`
- `State`
- `StateObject`

### Views
- `AccessibilityLabel`
- `Color`
- `ColorPicker`
- `ContextMenu`
- `Image`
- `Label`
- `NSViewControllerRepresentable`
- `NSViewRepresentable`
- `PreviewProvider`
- `ProgressView`
- `RealityView`
- `ScrollView`
- `Shape`
- `TabView`
- `Text`
- `TextEditor`
- `TextField`
- `TimelineView`
- `UIViewControllerRepresentable`
- `UIViewRepresentable`
- `View`
- `ViewModifier`


## Key Concepts

### Platform Support
- iOS 26.0+
- iPadOS 26.0+
- macOS 26.0+
- Mac Catalyst 26.0+
- visionOS 26.0+

### On-Device AI
All models run entirely on-device, ensuring privacy and offline capability.

## Usage Guidelines

1. Check model availability before use
2. Define clear instructions for the model's behavior
3. Use guided generation for structured outputs
4. Implement tool calling for dynamic capabilities
5. Handle errors appropriately

## Navigation

See the `references/` directory for detailed API documentation organized by category:
- `references/accessibility.md` - Accessibility
- `references/animations.md` - Animations
- `references/api_reference.md` - Api Reference
- `references/app_structure.md` - App Structure
- `references/controls.md` - Controls
- `references/data_flow.md` - Data Flow
- `references/drawing.md` - Drawing
- `references/essentials.md` - Essentials
- `references/gestures.md` - Gestures
- `references/layout.md` - Layout
- `references/navigation.md` - Navigation
- `references/state_management.md` - State Management
- `references/view_modifiers.md` - View Modifiers (18 modifiers including .sheet(), .frame(), .animation(), etc.)
- `references/views.md` - Views


## Best Practices

- **Prompting**: Be specific and clear in your prompts
- **Instructions**: Define the model's behavior upfront
- **Safety**: Enable guardrails for sensitive content
- **Localization**: Check supported languages for your use case
- **Performance**: Use prewarm() for better response times
- **Streaming**: Use streamResponse() for real-time user feedback

## Common Patterns

### Basic Session
```swift
let model = SystemLanguageModel(useCase: .general)
let session = LanguageModelSession(model: model)
let response = try await session.respond(to: Prompt("Your question"))
```

### Guided Generation
```swift
struct Recipe: Generable {
    let title: String
    let ingredients: [String]
}

let recipe = try await session.respond(
    generating: Recipe.self,
    prompt: Prompt("Create a pasta recipe")
)
```

### Tool Calling
```swift
struct WeatherTool: Tool {
    func call(arguments: String) async throws -> String {
        // Fetch weather data
    }
}

let session = LanguageModelSession(
    model: model,
    tools: [WeatherTool()]
)
```

## Reference Documentation

For complete API details, see the categorized documentation in the `references/` directory.
