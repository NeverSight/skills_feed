---
name: rn-visual-testing
description: Visual testing skill for React Native apps across iPhone models. Use when testing app appearance on iPhone 11 through 17 (all variants including Pro, Pro Max, Plus, Mini, Air, and SE). Covers screenshot capture, simulator configuration, screen dimension validation, safe area handling, Dynamic Island/notch compatibility, and pixel-perfect verification across all iPhone screen sizes and resolutions.
---

# React Native Visual Testing for iPhone
Test React Native apps visually across iPhone 11–17 families.

## iPhone Screen Reference

### Logical Dimensions (Points) — Use These for Layout Testing

| Device Group | Width | Height | Scale | Physical | Diagonal |
|--------------|-------|--------|-------|----------|----------|
| **iPhone 11** | 414 | 896 | 2x | 828×1792 | 6.1" |
| **iPhone 11 Pro** | 375 | 812 | 3x | 1125×2436 | 5.85" |
| **iPhone 11 Pro Max** | 414 | 896 | 3x | 1242×2688 | 6.46" |
| **iPhone 12 mini / 13 mini** | 375 | 812 | 3x | 1080×2340 | 5.42" |
| **iPhone 12/12 Pro / 13/13 Pro** | 390 | 844 | 3x | 1170×2532 | 6.06" |
| **iPhone 12/13 Pro Max** | 428 | 926 | 3x | 1284×2778 | 6.68" |
| **iPhone 14 / 14 Pro / 15 / 15 Pro / 16 / 16e** | 393 | 852 | 3x | 1179×2556 | 6.1" |
| **iPhone 14 Plus / 15 Plus** | 428 | 926 | 3x | 1284×2778 | 6.7" |
| **iPhone 14 Pro Max / 15 Pro Max / 16 Plus** | 430 | 932 | 3x | 1290×2796 | 6.7" |
| **iPhone 16 Pro** | 402 | 874 | 3x | 1206×2622 | 6.3" |
| **iPhone 16 Pro Max / 17 Pro Max** | 440 | 956 | 3x | 1320×2868 | 6.9" |
| **iPhone 17 / 17 Pro** | 402 | 874 | 3x | 1206×2622 | 6.3" |
| **iPhone Air** | 420 | 912 | 3x | 1260×2736 | 6.5" |
| **iPhone SE (3rd gen)** | 375 | 667 | 2x | 750×1334 | 4.7" |

### Unique Logical Sizes to Test (Minimum Coverage)

For comprehensive testing, cover these 8 unique logical dimensions:

```
375×667  — iPhone SE (smallest, no notch, home button)
375×812  — iPhone 11 Pro, 12/13 mini (notch)
390×844  — iPhone 12/13/13 Pro (notch)
393×852  — iPhone 14/14 Pro/15/15 Pro/16/16e (Dynamic Island on Pro)
402×874  — iPhone 16 Pro/17/17 Pro (Dynamic Island)
414×896  — iPhone 11/11 Pro Max (notch, largest of this era)
428×926  — iPhone 12/13 Pro Max, 14 Plus (notch/Dynamic Island)
430×932  — iPhone 14 Pro Max/15 Pro Max/16 Plus (Dynamic Island)
440×956  — iPhone 16 Pro Max/17 Pro Max (largest current)
420×912  — iPhone Air (newest form factor)
```

## Testing Workflow

### 1. Configure Simulators

List available simulators:
```bash
xcrun simctl list devices available | grep -i iphone
```

Create missing simulators if needed:
```bash
xcrun simctl create "iPhone 15 Pro" "iPhone 15 Pro"
```

Boot simulator:
```bash
xcrun simctl boot "iPhone 15 Pro"
```

### 2. Run App on Simulator

```bash
npx react-native run-ios --simulator="iPhone 15 Pro"
```

Or for specific device:
```bash
npx react-native run-ios --device="iPhone 14"
```

### 3. Capture Screenshots

Using simctl:
```bash
xcrun simctl io booted screenshot ~/screenshots/iphone15pro_home.png
```

For all booted simulators:
```bash
for UDID in $(xcrun simctl list devices booted -j | jq -r '.devices[][] | select(.state=="Booted") | .udid'); do
  NAME=$(xcrun simctl list devices -j | jq -r ".devices[][] | select(.udid==\"$UDID\") | .name" | tr ' ' '_')
  xcrun simctl io $UDID screenshot ~/screenshots/${NAME}_$(date +%s).png
done
```

### 4. Set Demo Mode (Consistent Status Bar)

```bash
xcrun simctl status_bar booted override \
  --time "9:41" \
  --batteryState charged \
  --batteryLevel 100 \
  --cellularMode active \
  --cellularBars 4 \
  --wifiBars 3
```

Reset to normal:
```bash
xcrun simctl status_bar booted clear
```

## Visual Testing Tools

### Detox (Recommended for E2E)

```javascript
// e2e/visual.test.js
describe('Visual Tests', () => {
  beforeAll(async () => {
    await device.launchApp();
    await device.setStatusBar({
      time: '9:41',
      batteryLevel: 100,
      batteryState: 'full',
    });
  });

  it('should match home screen baseline', async () => {
    await device.takeScreenshot('home_screen');
  });
});
```

### React Native Owl

```javascript
// owl.config.json
{
  "ios": {
    "workspace": "ios/YourApp.xcworkspace",
    "scheme": "YourApp",
    "device": "iPhone 15 Pro"
  },
  "baseline": ".owl/baseline",
  "screenshots": ".owl/screenshots"
}
```

```javascript
// __tests__/Home.owl.js
import { takeScreenshot } from 'react-native-owl';

describe('Home Screen', () => {
  it('matches baseline', async () => {
    const screen = await takeScreenshot('home');
    expect(screen).toMatchBaseline();
  });
});
```

## Critical Checkpoints

### Safe Area Validation

Verify content respects safe areas on all devices:
```javascript
import { useSafeAreaInsets } from 'react-native-safe-area-context';

// Test that insets are applied correctly:
// - iPhone SE: no top inset (home button device)
// - iPhone 11/12/13: ~47pt top (notch)  
// - iPhone 14 Pro+: ~59pt top (Dynamic Island)
```

### Dynamic Island / Notch Compatibility

| Device | Top Element |
|--------|-------------|
| iPhone SE | No notch, 20pt status bar |
| iPhone 11–13 (non-Pro 14) | Notch, ~47pt safe area |
| iPhone 14 Pro+ / 15 Pro+ / 16+ | Dynamic Island, ~59pt safe area |

### Orientation Testing

Test both portrait and landscape:
```bash
xcrun simctl io booted screenshot --type=png ~/portrait.png
xcrun simctl spawn booted notifyutil -s com.apple.springboard.orientation 1
sleep 1
xcrun simctl io booted screenshot --type=png ~/landscape.png
```

## Automated Multi-Device Script

```bash
#!/bin/bash
# test-all-iphones.sh

DEVICES=(
  "iPhone SE (3rd generation)"
  "iPhone 11"
  "iPhone 12 mini"
  "iPhone 13 Pro"
  "iPhone 14"
  "iPhone 14 Pro Max"
  "iPhone 15"
  "iPhone 15 Pro Max"
  "iPhone 16"
  "iPhone 16 Pro Max"
)

SCREENSHOTS_DIR="./visual-tests/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$SCREENSHOTS_DIR"

for DEVICE in "${DEVICES[@]}"; do
  echo "Testing on $DEVICE..."
  
  # Boot and wait
  xcrun simctl boot "$DEVICE" 2>/dev/null || true
  sleep 5
  
  # Set demo mode
  xcrun simctl status_bar "$DEVICE" override --time "9:41" --batteryState charged --batteryLevel 100
  
  # Build and run
  npx react-native run-ios --simulator="$DEVICE" --no-packager &
  sleep 30
  
  # Capture screenshot
  SAFE_NAME=$(echo "$DEVICE" | tr ' ()' '_')
  xcrun simctl io "$DEVICE" screenshot "$SCREENSHOTS_DIR/${SAFE_NAME}.png"
  
  # Shutdown
  xcrun simctl shutdown "$DEVICE"
done

echo "Screenshots saved to $SCREENSHOTS_DIR"
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Layout clips on iPhone SE | Use flexbox, avoid fixed heights >667pt |
| Content under Dynamic Island | Use `SafeAreaView` or `useSafeAreaInsets()` |
| Different font rendering | Check `allowFontScaling` prop |
| Status bar overlap | Set `StatusBar` translucent and handle insets |
| Inconsistent screenshots | Enable demo mode before capture |
| Bottom home indicator overlap | Check `SafeAreaView` bottom inset |

## Pixel-Perfect Checklist

1. ☐ Text readable at all sizes (no truncation)
2. ☐ Touch targets ≥44pt on all devices
3. ☐ Images scale correctly (use `resizeMode`)
4. ☐ Safe areas respected (top and bottom)
5. ☐ Horizontal scrolling only where intended
6. ☐ No content under notch/Dynamic Island
7. ☐ Home indicator area clear
8. ☐ Landscape mode functional (if supported)
9. ☐ Dark mode appearance correct
10. ☐ Dynamic Type/font scaling handled
