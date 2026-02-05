---
name: frontend-design
description: Create distinctive, production-grade mobile interfaces with exceptional design quality for React Native + Expo applications. Use this skill when building mobile screens, components, or user experiences. Generates polished, platform-native code that delivers modern 2025 mobile aesthetics with professional execution.
---

This skill guides creation of distinctive, production-grade mobile interfaces that set the standard for modern React Native design. Implement real working code with exceptional attention to mobile-specific design patterns, platform conventions, and sophisticated visual execution.

The user provides mobile interface requirements: a screen, component, flow, or experience to build. They may include context about the purpose, user workflow, or technical constraints.

## Mobile Design Thinking

Before coding, understand the mobile context and commit to a sophisticated design direction:
- **Purpose**: What user problem does this solve? What's the core mobile interaction?
- **Platform Identity**: Choose a design language that feels intentional and modern:
  - **Refined minimalism** with precision spacing, elegant typography, and subtle animations
  - **Luxury depth** with layered surfaces, sophisticated gradients, and material blur effects
  - **Gestural fluidity** with natural transitions, haptic feedback, and motion choreography
  - **Technical precision** with monospaced accents, data visualization, and clean hierarchy
  - **Neo-brutalist** with bold typography, high contrast, and geometric patterns
  - Each direction should feel purposeful and contemporary for 2025 mobile design
- **Platform Constraints**: iOS/Android patterns, performance, accessibility, touch targets (min 44pt)
- **Signature Moment**: What's the one interaction that will feel delightful and memorable?

**CRITICAL**: Mobile design demands intentionality at every scale—from micro-interactions to full-screen compositions. Precision in spacing, typography, and motion separates professional work from generic implementations.

Then implement working React Native/Expo code that is:
- Production-grade with proper TypeScript types
- Platform-native with iOS/Android considerations
- Visually sophisticated with modern 2025 aesthetics
- Performance-optimized with proper component patterns
- Accessible with proper touch targets and screen reader support

## Mobile Design Excellence Guidelines

Focus on mobile-native excellence:

### Typography & Hierarchy
- **System fonts with character**: Use SF Pro (iOS) or Roboto (Android) as base, but explore custom fonts via `expo-font` for distinctive brand moments
- **Dynamic Type support**: Respect iOS/Android accessibility preferences with proper `allowFontScaling`
- **Scale with purpose**: Establish clear hierarchy with font sizes that work at mobile reading distances (15-17pt for body text)
- **Readability first**: Line heights of 1.4-1.5 for body text, generous letter-spacing for uppercase labels

### Color & Visual System
- **Dark mode excellence**: Design for both light and dark themes from the start—not as an afterthought
- **Gradient sophistication**: Use `expo-linear-gradient` for depth and dimensionality, not decoration
- **Adaptive color**: Leverage platform semantic colors where appropriate, custom brand colors where it matters
- **Color contrast**: Ensure WCAG AA compliance (4.5:1 for text, 3:1 for UI components)

### Motion & Animation
- **Native performance**: Use `react-native-reanimated` for 60fps animations on the UI thread
- **Meaningful motion**: Every animation should communicate state, guide attention, or provide feedback
- **Spring physics**: Natural, spring-based animations feel more organic than linear easing
- **Micro-interactions**: Button press states, loading indicators, success confirmations—details matter
- **Choreography**: Stagger animations with proper delays for sophisticated reveals

### Spatial Design & Layout
- **Platform patterns**: Respect iOS Human Interface Guidelines and Material Design principles
- **Touch targets**: Minimum 44pt × 44pt for all interactive elements
- **Breathing room**: Generous padding (16-24pt) around content, especially near screen edges
- **Safe areas**: Properly handle notches, home indicators, and status bars with `SafeAreaView`
- **Asymmetric balance**: Dynamic layouts that feel intentional, not template-based

### Surface & Depth
- **Layering**: Use shadows, borders, and blur to create hierarchy without heavy decoration
- **Blur effects**: Platform-specific blur (iOS: `expo-blur`, Android: subtle overlays) for modern depth
- **Card design**: Rounded corners (16-24pt radius), subtle shadows, proper elevation
- **Glass morphism**: Translucent surfaces with backdrop blur for premium feel (iOS 26+ liquid glass tabs)

### Platform-Specific Excellence
- **iOS Fluidity**:
  - Native gestures (swipe to go back, pull to refresh)
  - SF Symbols for icons where appropriate
  - Liquid glass tab bars with auto-minimize behavior
  - Haptic feedback via `expo-haptics` for tactile responses
  
- **Android Material**:
  - Ripple effects for touch feedback
  - Edge-to-edge layouts with proper insets
  - Material elevation system
  - Platform-specific navigation patterns

### Modern 2025 Techniques
- **Bento grids**: Asymmetric card layouts with varied sizes for visual interest
- **Neumorphism refinement**: Soft shadows and subtle highlights (use sparingly)
- **Data visualization**: Clean charts and graphs with thoughtful color choices
- **Scroll-driven animations**: Content that responds to user interaction
- **Variable blur intensity**: Surfaces that adapt to context
- **Monospace accents**: Technical data (addresses, hashes, amounts) in monospace fonts

**CRITICAL**: Mobile design is not web design shrunk down. Embrace platform conventions, optimize for touch, and respect the unique constraints and capabilities of mobile devices. Every pixel, every animation, every interaction should feel purposeful and refined.

NEVER use generic mobile patterns: cookie-cutter card lists, default system fonts without intention, flat colors without depth, stiff linear animations, cramped layouts with insufficient touch targets, or designs that ignore platform-specific patterns.

## React Native Implementation Standards

### Component Patterns
```typescript
// Use TypeScript for all components with proper types
interface ButtonProps {
  onPress: () => void;
  title: string;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
}

// Leverage react-native-reanimated for performance
import Animated, { useAnimatedStyle, withSpring } from 'react-native-reanimated';

// Implement proper platform-specific behavior
import { Platform, StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  shadow: Platform.select({
    ios: { shadowColor: '#000', shadowOffset: { width: 0, height: 4 }, shadowOpacity: 0.15, shadowRadius: 12 },
    android: { elevation: 8 },
  }),
});
```

### Essential Libraries for 2025 Mobile Design
- **Navigation**: `expo-router` (file-based routing with native stack)
- **Animations**: `react-native-reanimated` (60fps UI thread animations)
- **Gestures**: `react-native-gesture-handler` (native touch handling)
- **Gradients**: `expo-linear-gradient` (smooth, performant gradients)
- **Blur**: `expo-blur` (iOS native blur, Android fallbacks)
- **Haptics**: `expo-haptics` (tactile feedback)
- **Safe Areas**: `react-native-safe-area-context` (proper notch/inset handling)
- **Icons**: `lucide-react-native` or `@expo/vector-icons` (vector icons)
- **Fonts**: `expo-font` (custom typography loading)

### Mobile-Specific Considerations

**Performance**:
- Use `FlatList` or `FlashList` for long lists, never `ScrollView` with `.map()`
- Memoize components with `React.memo` and callbacks with `useCallback`
- Optimize images with proper sizing and `resizeMode`
- Use `react-native-reanimated` instead of `Animated` for better performance

**Accessibility**:
- Add `accessibilityLabel` to all interactive elements
- Ensure `accessibilityRole` is set correctly (button, link, header, etc.)
- Support `accessibilityHint` for complex interactions
- Test with VoiceOver (iOS) and TalkBack (Android)

**Touch Interaction**:
- Minimum 44pt × 44pt touch targets
- Provide immediate visual feedback on press
- Use `activeOpacity` or scale animations for buttons
- Implement proper gesture handling with `PanGestureHandler`, `TapGestureHandler`

**Visual Feedback**:
- Haptic feedback on important actions (success, error, selection)
- Loading states for async operations
- Skeleton screens while data loads
- Optimistic UI updates for better perceived performance

### Design System Integration

Build components that integrate with a cohesive design system:

```typescript
// Theme-aware components
import { useColorScheme } from 'react-native';

const theme = useColorScheme(); // 'light' | 'dark'

// Consistent spacing
const SPACING = {
  xs: 4, sm: 8, md: 16, lg: 24, xl: 32, xxl: 48
};

// Consistent typography
const TYPOGRAPHY = {
  display: { fontSize: 36, lineHeight: 44, fontWeight: '800' },
  title: { fontSize: 24, lineHeight: 32, fontWeight: '700' },
  body: { fontSize: 16, lineHeight: 24, fontWeight: '400' },
};

// Consistent border radius
const RADIUS = {
  sm: 8, md: 12, lg: 16, xl: 24, full: 999
};
```

### Example: Production-Grade Mobile Button

```typescript
import React from 'react';
import { Pressable, Text, View, StyleSheet, Platform } from 'react-native';
import Animated, { useAnimatedStyle, useSharedValue, withSpring } from 'react-native-reanimated';
import { impactAsync, ImpactFeedbackStyle } from 'expo-haptics';
import { LinearGradient } from 'expo-linear-gradient';

interface ModernButtonProps {
  onPress: () => void;
  title: string;
  variant?: 'gradient' | 'solid';
  disabled?: boolean;
}

export function ModernButton({ onPress, title, variant = 'gradient', disabled }: ModernButtonProps) {
  const scale = useSharedValue(1);
  
  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
  }));
  
  const handlePressIn = () => {
    scale.value = withSpring(0.96, { damping: 15, stiffness: 400 });
  };
  
  const handlePressOut = () => {
    scale.value = withSpring(1, { damping: 15, stiffness: 400 });
  };
  
  const handlePress = async () => {
    await impactAsync(ImpactFeedbackStyle.Medium);
    onPress();
  };
  
  return (
    <Animated.View style={[animatedStyle]}>
      <Pressable
        onPress={handlePress}
        onPressIn={handlePressIn}
        onPressOut={handlePressOut}
        disabled={disabled}
        accessibilityRole="button"
        accessibilityLabel={title}
      >
        {variant === 'gradient' ? (
          <LinearGradient
            colors={['#FF8A65', '#FF6B6B']}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 1 }}
            style={styles.button}
          >
            <Text style={styles.text}>{title}</Text>
          </LinearGradient>
        ) : (
          <View style={[styles.button, styles.solidButton]}>
            <Text style={styles.text}>{title}</Text>
          </View>
        )}
      </Pressable>
    </Animated.View>
  );
}

const styles = StyleSheet.create({
  button: {
    paddingVertical: 18,
    paddingHorizontal: 24,
    borderRadius: 24,
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: 56,
    ...Platform.select({
      ios: {
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.15,
        shadowRadius: 12,
      },
      android: { elevation: 8 },
    }),
  },
  solidButton: {
    backgroundColor: '#FF8A65',
  },
  text: {
    fontSize: 17,
    fontWeight: '600',
    color: '#FFFFFF',
    letterSpacing: 0.2,
  },
});
```

**Remember**: Exceptional mobile design requires mastery of platform conventions, performance optimization, and sophisticated visual execution. Create interfaces that feel native, responsive, and refined—worthy of a professional 2025 mobile application.
