---
name: design
description: Design system skills for modern Apple platform UI including Liquid Glass, animations, and visual design patterns. Use when implementing new design language features.
allowed-tools: [Read, Write, Edit, Glob, Grep, AskUserQuestion]
---

# Design Skills

Skills for implementing Apple's modern design systems across platforms.

## When This Skill Activates

Use this skill when the user:
- Asks about Liquid Glass design
- Wants to implement modern Apple UI effects
- Needs guidance on visual design patterns
- Asks about materials, transparency, or blur effects
- Wants to create fluid animations

## Available Skills

### liquid-glass/
Comprehensive Liquid Glass implementation for iOS 26+, macOS 26+.
- SwiftUI `.glassEffect()` API
- AppKit `NSGlassEffectView`
- GlassEffectContainer patterns
- Morphing transitions
- Interactive effects
- Button styles

## Key Principles

### 1. Platform Consistency
- Follow Apple Human Interface Guidelines
- Use system-provided APIs
- Respect user appearance preferences

### 2. Performance
- Use GlassEffectContainer for multiple effects
- Limit number of glass effects per view
- Consider GPU resources

### 3. Visual Hierarchy
- Glass effects create depth and layering
- Use tints to indicate prominence
- Combine with appropriate shadows

## Reference Documentation

- `/Users/ravishankar/Downloads/docs/SwiftUI-Implementing-Liquid-Glass-Design.md`
- `/Users/ravishankar/Downloads/docs/AppKit-Implementing-Liquid-Glass-Design.md`
