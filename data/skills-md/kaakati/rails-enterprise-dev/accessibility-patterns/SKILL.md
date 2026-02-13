---
name: accessibility-patterns
description: "Expert accessibility decisions for iOS/tvOS: when to combine vs separate elements, label vs hint selection, Dynamic Type layout strategies, and WCAG AA compliance trade-offs. Use when implementing VoiceOver support, handling Dynamic Type, or ensuring accessibility compliance. Trigger keywords: accessibility, VoiceOver, Dynamic Type, WCAG, a11y, accessibilityLabel, accessibilityElement, accessibilityTraits, isAccessibilityElement, reduceMotion, contrast, focus"
version: "3.0.0"
---

# Accessibility Patterns — Expert Decisions

Expert decision frameworks for accessibility choices. Claude knows accessibilityLabel and VoiceOver — this skill provides judgment calls for element grouping, label strategies, and compliance trade-offs.

---

## Decision Trees

### Element Grouping Strategy

```
How should VoiceOver read this content?
├─ Logically related (card, cell, profile)
│  └─ Combine: .accessibilityElement(children: .combine)
│     Read as single unit
│
├─ Each part independently actionable
│  └─ Keep separate
│     User needs to interact with each
│
├─ Container with multiple actions
│  └─ Combine + custom actions
│     Single element with .accessibilityAction
│
├─ Decorative image with text
│  └─ Combine, image hidden
│     Image adds no meaning
│
└─ Image conveys different info than text
   └─ Keep separate with distinct labels
      Both need to be announced
```

**The trap**: Combining elements that have different actions. User can't interact with individual parts.

### Label vs Hint Decision

```
What should be in label vs hint?
├─ What the element IS
│  └─ Label
│     "Play button", "Submit form"
│
├─ What happens when activated
│  └─ Hint (only if not obvious)
│     "Double tap to start playback"
│
├─ Current state
│  └─ Value
│     "50 percent", "Page 3 of 10"
│
└─ Control behavior
   └─ Traits
      .isButton, .isSelected, .isHeader
```

### Dynamic Type Layout Strategy

```
How should layout adapt to larger text?
├─ Simple HStack (icon + text)
│  └─ Stay horizontal
│     Icons scale with text
│
├─ Complex HStack (image + multi-line)
│  └─ Stack vertically at xxxLarge
│     Check @Environment(\.dynamicTypeSize)
│
├─ Fixed-height cells
│  └─ Self-sizing
│     Remove height constraints
│
└─ Toolbar/navigation elements
   └─ Consider overflow menu
      Or scroll at extreme sizes
```

### Reduce Motion Response

```
What happens when Reduce Motion is enabled?
├─ Transition between screens
│  └─ Instant or simple fade
│     No slide/zoom animations
│
├─ Loading indicators
│  └─ Static or minimal
│     No bouncing/spinning
│
├─ Autoplay video/animation
│  └─ Don't autoplay
│     User controls playback
│
├─ Parallax/motion effects
│  └─ Disable completely
│     Can cause vestibular issues
│
└─ Essential animation (progress)
   └─ Keep but simplify
      Linear, no bounce
```

---

## NEVER Do

### VoiceOver Labels

**NEVER** include element type in labels:
```swift
// ❌ Redundant — VoiceOver announces "Submit button, button"
Button("Submit") { }
    .accessibilityLabel("Submit button")

// ✅ VoiceOver announces "Submit, button"
Button("Submit") { }
    .accessibilityLabel("Submit")

// ❌ Redundant — "Profile image, image"
Image("profile")
    .accessibilityLabel("Profile image")

// ✅ Describe what the image shows
Image("profile")
    .accessibilityLabel("John Doe's profile photo")
```

**NEVER** use generic labels:
```swift
// ❌ User has no idea what this does
Button(action: deleteItem) {
    Image(systemName: "trash")
}
.accessibilityLabel("Button")

// ❌ Still not helpful
Button(action: deleteItem) {
    Image(systemName: "trash")
}
.accessibilityLabel("Icon")

// ✅ Describe the action
Button(action: deleteItem) {
    Image(systemName: "trash")
}
.accessibilityLabel("Delete \(item.name)")
```

**NEVER** forget to label icon-only buttons:
```swift
// ❌ VoiceOver says nothing useful
Button(action: share) {
    Image(systemName: "square.and.arrow.up")
}
// VoiceOver: "Button" (no label!)

// ✅ Always label icon buttons
Button(action: share) {
    Image(systemName: "square.and.arrow.up")
}
.accessibilityLabel("Share")
```

### Element Visibility

**NEVER** hide interactive elements from accessibility:
```swift
// ❌ User can't access this control
Button("Settings") { }
    .accessibilityHidden(true)  // Why would you do this?

// ✅ Every interactive element must be accessible
// Only hide truly decorative elements
Image("decorative-pattern")
    .accessibilityHidden(true)  // This is OK — adds nothing
```

**NEVER** leave decorative images accessible:
```swift
// ❌ VoiceOver reads meaningless "image"
Image("background-gradient")
// VoiceOver: "Image"

// ✅ Hide decorative elements
Image("background-gradient")
    .accessibilityHidden(true)
```

### Dynamic Type

**NEVER** use fixed font sizes for user content:
```swift
// ❌ Doesn't respect user's text size preference
Text("Hello, World!")
    .font(.system(size: 16))  // Never scales!

// ✅ Use Dynamic Type styles
Text("Hello, World!")
    .font(.body)  // Scales automatically

// ✅ Custom font with scaling
Text("Custom")
    .font(.custom("MyFont", size: 16, relativeTo: .body))
```

**NEVER** truncate text at larger sizes without alternative:
```swift
// ❌ Content disappears at larger text sizes
Text(longContent)
    .lineLimit(2)
    .font(.body)
// At xxxLarge, user sees "Lorem ips..."

// ✅ Allow expansion or provide full content path
Text(longContent)
    .lineLimit(dynamicTypeSize >= .xxxLarge ? nil : 2)
    .font(.body)

// Or use "Read more" expansion
```

### Reduce Motion

**NEVER** ignore reduce motion for essential navigation:
```swift
// ❌ User with vestibular disorders feels sick
.transition(.slide)
// Reduce Motion enabled, but still slides

// ✅ Respect reduce motion
@Environment(\.accessibilityReduceMotion) var reduceMotion

.transition(reduceMotion ? .opacity : .slide)
```

**NEVER** autoplay video when reduce motion is enabled:
```swift
// ❌ Autoplay ignores user preference
VideoPlayer(player: player)
    .onAppear { player.play() }  // Always autoplays

// ✅ Check reduce motion
VideoPlayer(player: player)
    .onAppear {
        if !UIAccessibility.isReduceMotionEnabled {
            player.play()
        }
    }
```

### Color and Contrast

**NEVER** convey information by color alone:
```swift
// ❌ Color-blind users can't distinguish states
Circle()
    .fill(isOnline ? .green : .red)  // Only color differs

// ✅ Use shape/icon in addition to color
HStack {
    Circle()
        .fill(isOnline ? .green : .red)
    Text(isOnline ? "Online" : "Offline")
}
// Or
Image(systemName: isOnline ? "checkmark.circle.fill" : "xmark.circle.fill")
    .foregroundColor(isOnline ? .green : .red)
```

---

## Essential Patterns

### Accessible Card Component

```swift
struct AccessibleCard: View {
    let item: Item
    let onTap: () -> Void
    let onDelete: () -> Void
    let onShare: () -> Void

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(item.title)
                .font(.headline)

            Text(item.description)
                .font(.body)
                .foregroundColor(.secondary)

            Text(item.date, style: .date)
                .font(.caption)
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)

        // Combine all text for VoiceOver
        .accessibilityElement(children: .combine)
        .accessibilityLabel("\(item.title). \(item.description). \(item.date.formatted())")
        .accessibilityAddTraits(.isButton)

        // Custom actions instead of hidden buttons
        .accessibilityAction(.default) { onTap() }
        .accessibilityAction(named: "Delete") { onDelete() }
        .accessibilityAction(named: "Share") { onShare() }
    }
}
```

### Dynamic Type Adaptive Layout

```swift
struct AdaptiveProfileView: View {
    @Environment(\.dynamicTypeSize) private var dynamicTypeSize

    let user: User

    var body: some View {
        if dynamicTypeSize.isAccessibilitySize {
            // Vertical layout for accessibility sizes
            VStack(alignment: .leading, spacing: 12) {
                profileImage
                userInfo
            }
        } else {
            // Horizontal layout for standard sizes
            HStack(spacing: 16) {
                profileImage
                userInfo
            }
        }
    }

    private var profileImage: some View {
        Image(user.avatarName)
            .resizable()
            .scaledToFill()
            .frame(width: imageSize, height: imageSize)
            .clipShape(Circle())
            .accessibilityLabel("\(user.name)'s profile photo")
    }

    private var userInfo: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(user.name)
                .font(.headline)
            Text(user.title)
                .font(.subheadline)
                .foregroundColor(.secondary)
        }
    }

    private var imageSize: CGFloat {
        dynamicTypeSize.isAccessibilitySize ? 80 : 60
    }
}

extension DynamicTypeSize {
    var isAccessibilitySize: Bool {
        self >= .accessibility1
    }
}
```

### Reduce Motion Wrapper

```swift
struct MotionSafeAnimation<Content: View>: View {
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    let fullAnimation: Animation
    let reducedAnimation: Animation
    let content: Content

    init(
        full: Animation = .spring(),
        reduced: Animation = .linear(duration: 0.2),
        @ViewBuilder content: () -> Content
    ) {
        self.fullAnimation = full
        self.reducedAnimation = reduced
        self.content = content()
    }

    var body: some View {
        content
            .animation(reduceMotion ? reducedAnimation : fullAnimation, value: UUID())
    }
}

// Usage
struct AnimatedButton: View {
    @State private var isPressed = false
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    var body: some View {
        Button("Tap Me") { }
            .scaleEffect(isPressed ? 0.95 : 1.0)
            .animation(reduceMotion ? nil : .spring(), value: isPressed)
            .onLongPressGesture(minimumDuration: .infinity, pressing: { pressing in
                isPressed = pressing
            }, perform: {})
    }
}
```

### Accessible Form

```swift
struct AccessibleForm: View {
    @State private var email = ""
    @State private var password = ""
    @State private var emailError: String?
    @FocusState private var focusedField: Field?

    enum Field: Hashable {
        case email, password
    }

    var body: some View {
        Form {
            Section {
                TextField("Email", text: $email)
                    .focused($focusedField, equals: .email)
                    .textContentType(.emailAddress)
                    .keyboardType(.emailAddress)
                    .accessibilityLabel("Email address")
                    .accessibilityValue(email.isEmpty ? "Empty" : email)

                if let error = emailError {
                    Text(error)
                        .font(.caption)
                        .foregroundColor(.red)
                        .accessibilityLabel("Error: \(error)")
                }

                SecureField("Password", text: $password)
                    .focused($focusedField, equals: .password)
                    .textContentType(.password)
                    .accessibilityLabel("Password")
                    .accessibilityHint("Minimum 8 characters")
            }

            Button("Sign In") {
                signIn()
            }
            .accessibilityLabel("Sign in")
            .accessibilityHint("Double tap to sign in with entered credentials")
        }
        .onSubmit {
            switch focusedField {
            case .email:
                focusedField = .password
            case .password:
                signIn()
            case nil:
                break
            }
        }
        .onChange(of: emailError) { _, error in
            if error != nil {
                // Announce error to VoiceOver
                UIAccessibility.post(notification: .announcement,
                    argument: "Error: \(error ?? "")")
            }
        }
    }
}
```

---

## Quick Reference

### WCAG AA Requirements

| Criterion | Requirement | iOS Implementation |
|-----------|-------------|-------------------|
| 1.4.3 Contrast | 4.5:1 normal, 3:1 large | Use semantic colors |
| 1.4.4 Resize Text | 200% without loss | Dynamic Type support |
| 2.1.1 Keyboard | All functionality | VoiceOver navigation |
| 2.4.7 Focus Visible | Clear focus indicator | @FocusState |
| 2.5.5 Target Size | 44x44pt minimum | .frame(minWidth:minHeight:) |

### Accessibility Traits

| Trait | When to Use |
|-------|-------------|
| .isButton | Custom tappable views |
| .isHeader | Section titles |
| .isSelected | Currently selected item |
| .isLink | Navigates to URL |
| .isImage | Meaningful images |
| .playsSound | Audio triggers |
| .startsMediaSession | Video/audio playback |
| .adjustable | Swipe up/down to change value |

### Focus Notifications

| Notification | Use Case |
|--------------|----------|
| .screenChanged | Major UI change, new screen |
| .layoutChanged | Minor UI update |
| .announcement | Status message |
| .pageScrolled | Scroll position changed |

### Red Flags

| Smell | Problem | Fix |
|-------|---------|-----|
| "Button" in label | Redundant | Remove type from label |
| Icon without label | Inaccessible | Add accessibilityLabel |
| .accessibilityHidden(true) on control | Can't interact | Remove or rethink |
| .font(.system(size:)) | Doesn't scale | Use .font(.body) |
| Color-only status | Color-blind exclusion | Add icon or text |
| Animation ignores reduceMotion | Vestibular issues | Check environment |
| Decorative image without hidden | Noisy VoiceOver | accessibilityHidden(true) |
| Combined elements with separate actions | Can't interact individually | Keep separate or use custom actions |
