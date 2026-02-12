---
name: widgetkit
description: Build iOS/macOS/watchOS/visionOS widgets, Live Activities, watch complications, and controls using Apple's WidgetKit framework. Use when creating widget extensions, timeline providers, configurable widgets, Lock Screen widgets, Smart Stack widgets, Live Activities with ActivityKit, interactive widgets with buttons/toggles, or watch complications. Covers all widget families (systemSmall/Medium/Large/ExtraLarge, accessoryCircular/Rectangular/Inline/Corner) and rendering modes.
---

# WidgetKit Development Skill

Build glanceable, timely experiences across Apple platforms using WidgetKit.

## Quick Start

### Create Widget Extension
1. File → New → Target → Widget Extension
2. Deselect "Include Live Activity" and "Include Configuration App Intent" for static widgets
3. Widget requires: `Widget` protocol, `TimelineProvider`, and SwiftUI views

### Minimal Widget Structure

```swift
@main
struct MyWidget: Widget {
    var body: some WidgetConfiguration {
        StaticConfiguration(
            kind: "com.app.mywidget",
            provider: Provider()
        ) { entry in
            MyWidgetView(entry: entry)
        }
        .configurationDisplayName("My Widget")
        .description("Shows key information")
        .supportedFamilies([.systemSmall, .systemMedium])
    }
}

struct Provider: TimelineProvider {
    func placeholder(in context: Context) -> SimpleEntry {
        SimpleEntry(date: .now)
    }
    
    func getSnapshot(in context: Context, completion: @escaping (SimpleEntry) -> Void) {
        completion(SimpleEntry(date: .now))
    }
    
    func getTimeline(in context: Context, completion: @escaping (Timeline<SimpleEntry>) -> Void) {
        let entry = SimpleEntry(date: .now)
        let nextUpdate = Calendar.current.date(byAdding: .minute, value: 15, to: .now)!
        completion(Timeline(entries: [entry], policy: .after(nextUpdate)))
    }
}

struct SimpleEntry: TimelineEntry {
    let date: Date
}
```

## Widget Families & Sizes

| Family | Platforms | Use Case |
|--------|-----------|----------|
| `systemSmall` | iOS, iPadOS, macOS, visionOS | Single tap target, glanceable info |
| `systemMedium` | iOS, iPadOS, macOS, visionOS | Multiple data points, interactive elements |
| `systemLarge` | iOS, iPadOS, macOS, visionOS | Rich content, multiple interactions |
| `systemExtraLarge` | iPadOS, macOS, visionOS | Dashboard-style layouts |
| `accessoryCircular` | iOS Lock Screen, watchOS | Minimal info, gauge-style |
| `accessoryRectangular` | iOS Lock Screen, watchOS | 2-3 lines of text |
| `accessoryInline` | iOS Lock Screen, watchOS | Single line text + optional image |
| `accessoryCorner` | watchOS only | Corner complications |

### Adapt to Widget Family

```swift
struct MyWidgetView: View {
    @Environment(\.widgetFamily) var family
    
    var body: some View {
        switch family {
        case .systemSmall: CompactView()
        case .systemMedium: MediumView()
        case .systemLarge: DetailedView()
        case .accessoryCircular: GaugeView()
        case .accessoryRectangular: RectangularView()
        default: CompactView()
        }
    }
}
```

## Rendering Modes

Widgets render differently based on context:

| Mode | When Used | Behavior |
|------|-----------|----------|
| `fullColor` | Home Screen (iOS 17-), macOS desktop | Full color preserved |
| `accented` | Home Screen tinted/clear, visionOS, watchOS | Divides into accent + primary groups |
| `vibrant` | Lock Screen, StandBy | Desaturated, blurred effect |

```swift
@Environment(\.widgetRenderingMode) var renderingMode

var body: some View {
    switch renderingMode {
    case .fullColor: FullColorView()
    case .accented: AccentedView()
    case .vibrant: VibrantView()
    @unknown default: FullColorView()
    }
}
```

## Interactivity

### Buttons & Toggles (iOS 17+)
```swift
Button(intent: RefreshIntent()) {
    Label("Refresh", systemImage: "arrow.clockwise")
}

Toggle(isOn: $isEnabled, intent: ToggleIntent()) {
    Text("Enable")
}
```

### Deep Links
```swift
MyWidgetView()
    .widgetURL(URL(string: "myapp://detail/123")!)

// Or for multiple links in larger widgets:
Link(destination: URL(string: "myapp://item/1")!) {
    ItemView()
}
```

## Configuration Types

| Type | Use Case |
|------|----------|
| `StaticConfiguration` | No user configuration needed |
| `AppIntentConfiguration` | User-configurable (iOS 17+) |
| `ActivityConfiguration` | Live Activities |

## Reference Documentation

- **[Timeline & Updates](references/timelines.md)**: Timeline providers, reload policies, push updates
- **[Interactivity](references/interactivity.md)**: Buttons, toggles, App Intents, deep links
- **[Live Activities](references/live-activities.md)**: ActivityKit, Dynamic Island, Lock Screen
- **[Design Guidelines](references/design-guidelines.md)**: HIG best practices, layout, typography
- **[Platform Specifics](references/platforms.md)**: iOS, watchOS, macOS, visionOS differences
- **[Dimensions](references/dimensions.md)**: Exact sizes for all widget families per device

## Key Constraints

- **No real-time updates**: Use timelines; system batches updates
- **Limited budget**: ~40-70 refreshes/day depending on usage
- **No continuous animations**: Only transition animations up to 2 seconds
- **SwiftUI only**: UIKit views not supported
- **Stateless**: No persistent state between renders
- **No network in views**: Fetch data in timeline provider only

## Common Patterns

### Share Data with Main App
```swift
// Use App Groups
let sharedDefaults = UserDefaults(suiteName: "group.com.app.shared")

// Or shared container
let containerURL = FileManager.default.containerURL(
    forSecurityApplicationGroupIdentifier: "group.com.app.shared"
)
```

### Force Widget Refresh
```swift
import WidgetKit
WidgetCenter.shared.reloadTimelines(ofKind: "com.app.mywidget")
WidgetCenter.shared.reloadAllTimelines()
```

### Placeholder for Sensitive Content
```swift
.privacySensitive() // Redacts when device locked
```
