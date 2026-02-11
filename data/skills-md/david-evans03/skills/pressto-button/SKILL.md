---
name: pressto-button
description: Tells you how to use the pressto button in react-native/expo apps
---

Usage

```tsx
import { PressableScale, PressableOpacity } from "pressto";

// Scales down on press
<PressableScale onPress={() => {}}>
  <Text>Scale</Text>
</PressableScale>

// Fades when pressed
<PressableOpacity onPress={() => {}}>
  <Text>Opacity</Text>
</PressableOpacity>
```

Supports standard Pressable props.

# pressto-button

For tap targets needing 60fps visual feedback without JS thread blocking.

Instructions

1. Import PressableScale (physical feedback) or PressableOpacity (subtle fade)
2. Wrap content and add onPress handler