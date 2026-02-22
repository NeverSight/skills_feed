---
name: app-store-screenshot-generation
description: Generate App Store and Google Play screenshot assets using each::sense AI. Create device-framed screenshots, feature highlights, localized versions, and promotional visuals optimized for iOS App Store and Google Play Store requirements.
metadata:
  author: eachlabs
  version: "1.0"
---

# App Store Screenshot Generation

Generate high-converting App Store and Google Play screenshot assets using each::sense. This skill creates images optimized for app store requirements, featuring device frames, feature callouts, and promotional visuals that drive downloads.

## Features

- **iOS App Store Screenshots**: iPhone and iPad device frames with proper dimensions
- **Google Play Screenshots**: Android device frames optimized for Play Store
- **Feature Highlights**: Screenshots with callout text and visual emphasis
- **Lifestyle Context**: App shown in real-world usage scenarios
- **Localized Screenshots**: Multi-language versions for global markets
- **App Preview Thumbnails**: Video preview poster frames
- **Before/After Comparisons**: Transformation showcases for utility apps
- **Onboarding Flows**: Multi-screen app walkthrough sequences
- **Dark/Light Mode Variants**: Both theme versions for completeness
- **A/B Test Variations**: Multiple creative approaches for optimization

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an iPhone App Store screenshot for a fitness tracking app showing the workout dashboard with an iPhone 15 Pro device frame, 1320x2868 pixels",
    "mode": "max"
  }'
```

## Screenshot Specifications

| Platform | Device | Dimensions | Aspect Ratio | Use Case |
|----------|--------|------------|--------------|----------|
| iOS App Store | iPhone 6.7" | 1320x2868 | ~1:2.17 | iPhone 15 Pro Max, 14 Pro Max |
| iOS App Store | iPad 12.9" | 2064x2752 | ~3:4 | iPad Pro screenshots |
| Google Play | Phone | 1080x1920 | 9:16 | Standard Android phone |

## Use Case Examples

### 1. iOS App Store Screenshot with Device Frame

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an iPhone App Store screenshot at 1320x2868 pixels. Show a sleek iPhone 15 Pro device frame displaying a meditation app interface with a calming gradient background, session timer, and breathing animation. Add headline text at the top: \"Find Your Inner Peace\". Clean, minimal design with soft purple and blue tones.",
    "mode": "max"
  }'
```

### 2. Google Play Screenshot

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a Google Play Store screenshot at 1080x1920 pixels. Show an Android phone displaying a recipe app with a food photo, ingredients list, and cooking steps. Include feature text: \"10,000+ Recipes at Your Fingertips\". Bright, appetizing color scheme with warm orange accents.",
    "mode": "max"
  }'
```

### 3. Feature Highlight Screenshot

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an iPhone App Store screenshot at 1320x2868 pixels for a banking app. Show iPhone device frame with the app dashboard displaying account balances and recent transactions. Add visual callouts pointing to key features: instant transfers, budget tracking, and bill reminders. Use professional blue color scheme. Headline: \"Smart Banking Made Simple\".",
    "mode": "max"
  }'
```

### 4. Lifestyle/Context Screenshot

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an iPhone App Store screenshot at 1320x2868 pixels showing a travel app in lifestyle context. Show a person holding an iPhone at an airport terminal, screen displaying flight boarding pass and gate information. Natural lighting, professional travel photography style. Include subtle text overlay: \"Your Journey Starts Here\". Blurred airport background for depth.",
    "mode": "max"
  }'
```

### 5. Localized Screenshot (Spanish)

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an iPhone App Store screenshot at 1320x2868 pixels for a language learning app, localized for Spanish market. Show iPhone device frame with Spanish lesson interface. All text in Spanish: headline \"Aprende Ingles en 10 Minutos al Dia\", feature callouts \"Lecciones Interactivas\" and \"Practica con Nativos\". Vibrant educational color scheme with green and yellow accents.",
    "mode": "max"
  }'
```

### 6. App Preview Video Thumbnail

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an App Preview video thumbnail at 1320x2868 pixels for a photo editing app. Show iPhone 15 Pro frame with the app interface mid-edit - a stunning portrait photo with editing tools visible. Add a prominent play button overlay in the center. Dramatic headline: \"Transform Your Photos\". Dynamic, creative composition that entices users to watch the preview.",
    "mode": "max"
  }'
```

### 7. Before/After Comparison Screenshot

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an iPhone App Store screenshot at 1320x2868 pixels for a photo enhancement app. Show a split-screen before/after comparison - left side shows original dark, grainy photo, right side shows the same photo enhanced with better lighting, color, and clarity. Include divider line with drag handle. Labels \"Before\" and \"After\" above each side. Headline at top: \"One Tap Enhancement\".",
    "mode": "max"
  }'
```

### 8. Onboarding Flow Screenshots

```bash
# First onboarding screen
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create iPhone App Store screenshot 1 of 3 for a habit tracking app onboarding flow, 1320x2868 pixels. Show iPhone device frame with welcome screen - friendly illustration of person achieving goals, headline \"Build Better Habits\", subtitle \"Track your daily progress and reach your goals\". Include pagination dots showing first of three screens. Motivational, energetic color scheme.",
    "session_id": "onboarding-habit-app"
  }'

# Second onboarding screen (same session for consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create screenshot 2 of 3 for the same habit tracking app. Show the habit dashboard with streak counters, progress rings, and daily checklist. Headline \"Stay Consistent\", subtitle \"Visual progress keeps you motivated\". Maintain same style and pagination dots showing second screen.",
    "session_id": "onboarding-habit-app"
  }'

# Third onboarding screen
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create screenshot 3 of 3 for the habit tracking app. Show reminder notifications and weekly statistics view. Headline \"Never Miss a Day\", subtitle \"Smart reminders at the perfect time\". Same style, pagination dots showing third screen. Include a subtle call-to-action feel.",
    "session_id": "onboarding-habit-app"
  }'
```

### 9. Dark Mode/Light Mode Variants

```bash
# Light mode version
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an iPhone App Store screenshot at 1320x2868 pixels for a notes app - LIGHT MODE version. Show iPhone 15 Pro silver device frame with the app in light theme: white background, clean typography, organized note cards. Headline \"Capture Every Idea\". Bright, clean, minimalist aesthetic.",
    "session_id": "notes-app-themes"
  }'

# Dark mode version (same session)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create the same notes app screenshot but in DARK MODE. Show iPhone 15 Pro space black device frame with dark theme interface: dark gray background, same layout as light mode but inverted colors. Headline \"Easy on Your Eyes\". Elegant, sophisticated dark aesthetic. Maintain visual consistency with light mode version.",
    "session_id": "notes-app-themes"
  }'
```

### 10. A/B Test Screenshot Variations

```bash
# Variation A - Feature-focused
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create iPhone App Store screenshot at 1320x2868 pixels for a workout app - VARIATION A (feature-focused). Show iPhone device frame with workout library screen displaying exercise thumbnails. Headline emphasizing features: \"500+ Workouts, Zero Equipment\". Clean, informative design focusing on app content and variety.",
    "mode": "eco"
  }'

# Variation B - Benefit-focused
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create iPhone App Store screenshot at 1320x2868 pixels for a workout app - VARIATION B (benefit-focused). Show iPhone device frame with progress tracking screen showing weight loss chart and achievements. Headline emphasizing results: \"Transform Your Body in 30 Days\". Motivational, aspirational design focusing on outcomes.",
    "mode": "eco"
  }'

# Variation C - Social proof
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create iPhone App Store screenshot at 1320x2868 pixels for a workout app - VARIATION C (social proof). Show iPhone device frame with community feed showing user transformations and testimonials. Headline: \"Join 2 Million Active Users\". Community-focused design with user photos and star ratings visible.",
    "mode": "eco"
  }'
```

## Best Practices

### Screenshot Design
- **Safe Zones**: Keep important content away from edges - avoid top 20% for status bar area
- **Text Hierarchy**: Use large, readable headlines (minimum 40pt equivalent)
- **Device Frames**: Use current-generation device mockups (iPhone 15 Pro, Pixel 8)
- **Contrast**: Ensure text is readable over any background elements
- **Consistency**: Maintain same style, fonts, and color scheme across all screenshots

### App Store Optimization
- **First Screenshot**: Make it your strongest - it's often the only one users see
- **Feature Callouts**: Highlight 1-2 key features per screenshot
- **Localization**: Translate all text for target markets, not just headlines
- **Seasonal Updates**: Refresh screenshots for major app updates

### iPad Screenshots
- **Landscape Option**: iPad supports landscape screenshots for certain apps
- **Utilize Space**: Take advantage of larger canvas for more detailed UI
- **Split View**: Show multitasking capabilities if applicable

## Mode Selection

Ask your users before generating:

**"Do you want fast drafts for iteration, or final quality for submission?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final App Store submission, polished assets | Slower | Highest |
| `eco` | Quick drafts, A/B test variations, concept exploration | Faster | Good |

## Multi-Turn Screenshot Iteration

Use `session_id` to iterate on screenshot designs:

```bash
# Initial screenshot
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an iPhone App Store screenshot at 1320x2868 for a podcast app with episode list view",
    "session_id": "podcast-screenshot-v1"
  }'

# Iterate based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Add a headline saying \"Your Daily Commute Companion\" and change the background to a gradient purple",
    "session_id": "podcast-screenshot-v1"
  }'

# Request variation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create 2 more variations with different headline angles - one focusing on discovery, one on offline listening",
    "session_id": "podcast-screenshot-v1"
  }'
```

## iPad Screenshot Generation

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an iPad App Store screenshot at 2064x2752 pixels for a design app. Show iPad Pro device frame with the canvas workspace, featuring drawing tools, layers panel, and color picker. Professional creative app interface. Headline: \"Design Without Limits\". Take advantage of the larger screen to show detailed UI.",
    "mode": "max"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt to comply with store guidelines |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |
| Dimension mismatch | Wrong aspect ratio | Use exact specifications from the table above |

## Related Skills

- `each-sense` - Core API documentation
- `meta-ad-creative-generation` - Facebook/Instagram ad creatives
- `product-photo-generation` - E-commerce product shots
