---
name: reacticx
description: React Native animated component library reference for Reacticx - 90+ production-ready components with Reanimated and Skia. Triggers on reacticx, reactix, or requests for animated React Native UI components (shaders, carousels, bottom sheets, toggles, pickers, loaders, etc).
---

# Reacticx Component Library

Headless, animation-focused React Native component library with 90+ production-ready components.

**Docs:** https://www.reacticx.com/docs | **GitHub:** https://github.com/rit3zh/reacticx

## Setup

```bash
# Install core dependencies
npm install react-native-reanimated react-native-gesture-handler react-native-svg \
  expo-haptics expo-blur expo-symbols @expo/vector-icons @shopify/react-native-skia

# Initialize config (optional, for CLI)
npx reacticx init

# Add components
npx reacticx add <component-name>
npx reacticx add <component> --dir <path> --overwrite
npx reacticx list
npx reacticx list -c <category>
```

## Component Categories

### Shaders (8) - GPU-accelerated visual effects
Read [references/shaders.md](references/shaders.md) when working with shader components.

| Component | Install Name |
|-----------|-------------|
| Aurora | `aurora` |
| Chroma Ring | `chroma-ring` |
| Energy Orb | `energy-orb` |
| Siri Orb | `siri-orb` |
| Mesh Gradient | `mesh-gradient` |
| Grainy Gradient | `grainy-gradient` |
| Skia Ripple | `skia-ripple` |
| Wave Scrawler | `wave-scrawler` |

### Texts (6) - Animated typography
Read [references/texts.md](references/texts.md) when working with text animation components.

| Component | Install Name |
|-----------|-------------|
| Animated Text | `animated-text` |
| Dynamic Text | `dynamic-text` |
| Fade Text | `fade-text` |
| Gooey Text | `gooey-text` |
| Curved Marquee | `curved-marquee` |
| Staggered Text | `staggered-text` |

### Micro Interactions (9) - Interactive feedback elements
Read [references/micro-interactions.md](references/micro-interactions.md) when working with micro interaction components.

| Component | Install Name |
|-----------|-------------|
| Animated Scroll Progress | `animated-scroll-progress` |
| Animated Theme Toggle | `animated-theme-toggle` |
| Animated Countdown | `countdown` |
| Elastic Slider | `elastic-slider` |
| Flexi Button | `flexi-button` |
| Gooey Switch | `gooey-switch` |
| Hamburger | `hamburger` |
| Spin Button | `spin-button` |
| Stacked Chips | `stacked-chips` |

### Carousels & Scrollables (13)
Read [references/components-carousels.md](references/components-carousels.md) when working with carousel or scrollable components.

| Component | Install Name |
|-----------|-------------|
| Blur Carousel | `blur-carousel` |
| Cinematic Carousel | `cinematic-carousel` |
| Circular Carousel | `circular-carousel` |
| Circular List | `circular-list` |
| Material Carousel | `material-carousel` |
| Parallax Carousel | `parallax-carousel` |
| Rotate Carousel | `rotate-carousel` |
| Scale Carousel | `scale-carousel` |
| Tilt Carousel | `tilt-carousel` |
| Vertical Flow Carousel | `vertical-flow-carousel` |
| Vertical Page Carousel | `vertical-page-carousel` |
| Marquee | `marquee` |
| Matched Geometry | `matched-geometry` |

### Navigation & Layout (13)
Read [references/components-navigation.md](references/components-navigation.md) when working with navigation, tabs, sheets, or menu components.

| Component | Install Name |
|-----------|-------------|
| Accordion | `accordion` |
| Bottom Sheet | `bottom-sheet` |
| Bottom Sheet Stack | `bottom-sheet-stack` |
| Curved Bottom Tabs | `curved-bottom-tabs` |
| Dialog | `dialog` |
| Disclosure Group | `disclosure-group` |
| Dropdown | `dropdown` |
| Dynamic Island | `dynamic-island` |
| Morphing Tab Bar | `morphing-tabbar` |
| Segmented Control | `segmented-control` |
| Split View | `split-view` |
| Stack Aware Tabs | `stack-aware-tabs` |
| Tabs | `tabs` |

### Inputs & Controls (13)
Read [references/components-inputs.md](references/components-inputs.md) when working with buttons, inputs, pickers, or toggle components.

| Component | Install Name |
|-----------|-------------|
| Animated Input Bar | `animated-input-bar` |
| Button | `button` |
| CheckBox | `check-box` |
| Flip Card | `flip-card` |
| OTP Input | `otp-input` |
| Picker | `picker` |
| Ruler | `ruler` |
| Scrollable Search | `scrollable-search` |
| Search Bar | `search-bar` |
| Seekbar | `seekbar` |
| Stepper | `stepper` |
| Switch | `switch` |
| Theme Switch | `theme-switch` |

### Loaders (6)
Read [references/display-loaders.md](references/display-loaders.md) when working with loading indicators.

| Component | Install Name |
|-----------|-------------|
| Circle Loader | `circle-loader` |
| Circular Loader | `circular-loader` |
| Orbitdot Loader | `orbiting-dots` |
| Pulsing Loader | `pulsing-dots` |
| Rotating Square | `rotating-square` |
| Spinner Arc | `spinner-arc` |

### Progress & Transitions (5)
Read [references/display-progress.md](references/display-progress.md) when working with progress indicators or transition effects.

| Component | Install Name |
|-----------|-------------|
| Circular Progress | `circular-progress` |
| Progress | `progress` |
| Rolling Counter | `rolling-counter` |
| Shimmer | `shimmer` |
| Shimmer Wave Text | `shimmer-wave` |

### Content & Display (10)
Read [references/display-content.md](references/display-content.md) when working with avatars, badges, headers, toast, or display components.

| Component | Install Name |
|-----------|-------------|
| Animated Chip Group | `animated-chip` |
| Animated Header ScrollView | `animated-header-scrollview` |
| Animated Masked Text | `animated-masked-text` |
| Avatar / Avatar Group | `avatar` / `avatar-group` |
| Badge | `badge` |
| Empty State | `empty-state` |
| QR Code | `qr-code` |
| Title | `title` |
| Toast | `toast` |

### Effects & Visuals (7)
Read [references/display-effects.md](references/display-effects.md) when working with glow, ripple, cards, or visual effect components.

| Component | Install Name |
|-----------|-------------|
| Glow | `glow` |
| Infinite Menu | `infinite-menu` |
| Lanyard | `lanyard` |
| Pagination | `pagination` |
| Radial Intro | `radial-intro` |
| Ripple | `ripple` |
| Stack Cards | `stack-cards` |

## Common Dependencies

| Package | Used By |
|---------|---------|
| `react-native-reanimated` | Nearly all components |
| `react-native-gesture-handler` | Carousels, sliders, switches, ripple |
| `@shopify/react-native-skia` | Shaders, gooey effects, theme switch |
| `react-native-svg` | Loaders, glow, curved marquee |
| `expo-blur` | Text effects, carousels, headers |
| `expo-haptics` | Accordion, pagination, pickers |
| `react-native-worklets` | Many animation-heavy components |

## Key Notes

- Wrap with `GestureHandlerRootView` when using gesture-based components
- Configure `react-native-reanimated/plugin` in babel config
- Skia components require native module installation
- All animations target 60fps via Reanimated's UI thread
- Some blur effects (`expo-blur`) work best on iOS
- Import paths follow `@/components/{layer}/{name}` where layer is `base`, `molecules`, `organisms`, or `templates`
