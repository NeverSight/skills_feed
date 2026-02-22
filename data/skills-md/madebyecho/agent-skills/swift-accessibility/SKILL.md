---
name: swift-accessibility
description: >
  Automatically applies accessibility best practices to Swift projects
  (SwiftUI and UIKit). Use when working on iOS/macOS projects that need
  VoiceOver support, Dynamic Type, WCAG compliance, or accessibility audits.
  Triggers on Swift accessibility tasks, a11y improvements, or when the user
  mentions accessibility, VoiceOver, or Dynamic Type.
license: MIT
metadata:
  author: madebyecho
  version: "1.0.0"
---

# Swift Accessibility

Scan, fix, and audit accessibility in Swift projects. Detects missing VoiceOver labels, Dynamic Type issues, WCAG violations, and generates XCTest audit code. Supports both SwiftUI and UIKit with auto-detection per file. Covers all 9 Apple Accessibility Nutrition Label categories.

## When to Apply

Reference these guidelines when:
- Working on iOS/macOS projects that need accessibility support
- Adding VoiceOver, Voice Control, or Switch Control support
- Running an accessibility audit or a11y review
- Fixing Dynamic Type, contrast, or WCAG compliance issues
- Preparing for App Store Accessibility Nutrition Labels

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Missing VoiceOver Labels | CRITICAL | `p0-` |
| 2 | Missing Context and Discoverability | HIGH | `p1-` |
| 3 | Visual, Interaction, and System Setting Compliance | MEDIUM | `p2-` |

## Quick Reference

### 1. Missing VoiceOver Labels (CRITICAL)

- `p0-images-without-labels` — Images without `.accessibilityLabel` are invisible to VoiceOver
- `p0-icon-only-buttons` — Buttons with only an image and no label

### 2. Missing Context and Discoverability (HIGH)

- `p1-missing-hints` — Interactive elements without `.accessibilityHint`
- `p1-missing-identifiers` — Testable elements without `.accessibilityIdentifier`
- `p1-missing-input-labels` — Missing `accessibilityInputLabels` for Voice Control support
- `p1-small-touch-targets` — Touch targets below 44x44pt minimum (HIG requirement)
- `p1-color-only-information` — Color used as the only way to convey information

### 3. Visual, Interaction, and System Setting Compliance (MEDIUM)

- `p2-hardcoded-fonts` — Hardcoded font sizes that break Dynamic Type
- `p2-ungrouped-elements` — Related elements not grouped for VoiceOver
- `p2-missing-header-traits` — Section headers without `.isHeader` trait
- `p2-decorative-elements-visible` — Decorative elements not hidden from VoiceOver
- `p2-contrast-insufficient` — Colors that fail WCAG AA contrast ratios
- `p2-reduce-motion-ignored` — Animations that ignore the Reduce Motion setting
- `p2-bold-text-ignored` — Custom fonts that don't respond to Bold Text setting
- `p2-custom-actions-missing` — Gesture-only interactions without accessible alternatives
- `p2-dynamic-content-not-announced` — Content changes not posted as accessibility notifications
- `p2-modal-focus-management` — Custom modals without proper focus management or escape support

## Apple Accessibility Nutrition Label Coverage

| Nutrition Label | Rules Covering It |
|----------------|-------------------|
| VoiceOver | p0-*, p1-missing-hints, p1-missing-identifiers, p2-ungrouped-elements, p2-missing-header-traits, p2-decorative-elements-visible, p2-custom-actions-missing, p2-dynamic-content-not-announced, p2-modal-focus-management |
| Voice Control | p1-missing-input-labels, p1-missing-hints, p2-custom-actions-missing |
| Larger Text (Dynamic Type) | p2-hardcoded-fonts |
| Sufficient Contrast | p2-contrast-insufficient |
| Dark Interface | p2-contrast-insufficient (checks both modes) |
| Differentiate Without Color Alone | p1-color-only-information |
| Reduced Motion | p2-reduce-motion-ignored |
| Bold Text | p2-bold-text-ignored |
| Touch Target Size | p1-small-touch-targets |

## Workflow

Execute these 5 phases in order. Load rule files on-demand — only read a rule when its content is needed for the current phase.

### Phase 1: Project Discovery

1. Glob for `**/*.swift` to find all Swift source files
2. Classify each file as **SwiftUI** (`import SwiftUI`), **UIKit** (`import UIKit`), or **mixed**
3. Grep for existing accessibility usage to understand current coverage:
   - SwiftUI: `.accessibilityLabel`, `.accessibilityHint`, `.accessibilityIdentifier`, `.accessibilityHidden`, `.accessibilityInputLabels`, `accessibilityReduceMotion`
   - UIKit: `isAccessibilityElement`, `accessibilityLabel`, `accessibilityIdentifier`, `UIAccessibility.isReduceMotionEnabled`, `adjustsFontForContentSizeCategory`
4. Report: total files, framework breakdown, current accessibility coverage percentage

### Phase 2: Issue Detection

Scan files for anti-patterns. Read rules from `rules/` directory for detection patterns.

For each issue found, record: file path, line number, priority, description, and suggested fix.

### Phase 3: Automated Fixes

Apply fixes using Edit tool, following these rules:

1. **Never overwrite** existing accessibility code — only add missing properties
2. **Add `[VERIFY]` comment markers** on generated labels where semantic accuracy needs human review:
   ```swift
   .accessibilityLabel("Settings icon") // [VERIFY] confirm label matches intent
   ```
3. **Preserve formatting** — match the indentation and style of surrounding code
4. **Group related fixes** — apply all fixes to a single view/element together

Fix application order:
1. P0 Critical fixes first
2. P1 High fixes
3. P2 Medium fixes (comprehensive mode only)

### Phase 4: Audit Test Generation

Load `assets/audit-template.swift` and generate an XCTest file for the project.

1. Create `AccessibilityAuditTests.swift` in the project's test target directory
2. Add a test method for each view/screen that was modified
3. Use `performAccessibilityAudit()` with appropriate audit types
4. Include navigation setup to reach each view being tested

Match the project's existing test framework and patterns.

### Phase 5: Report

Output a structured summary:

```
## Accessibility Audit Report

### Issues Found
| Priority | Category | Count |
|----------|----------|-------|
| P0 Critical | ... | ... |
| P1 High | ... | ... |
| P2 Medium | ... | ... |

### Changes Applied
- **Files modified**: [list]
- **Issues fixed**: [count] of [total]
- **Test file generated**: [path]

### Accessibility Nutrition Label Readiness
| Feature | Status |
|---------|--------|
| VoiceOver | Ready / Needs Work |
| Voice Control | Ready / Needs Work |
| Larger Text | Ready / Needs Work |
| Sufficient Contrast | Needs Manual Review |
| Differentiate Without Color | Ready / Needs Work |
| Reduced Motion | Ready / Needs Work |

### Manual Review Required
Items marked with [VERIFY] that need human confirmation:
- [list of VERIFY items with file:line references]

### Next Steps
- [ ] Run VoiceOver testing (see assets/checklist.md)
- [ ] Review [VERIFY] markers and update labels
- [ ] Run generated accessibility tests
- [ ] Test with Dynamic Type at all sizes (up to AX5)
- [ ] Test in both Light and Dark modes
- [ ] Enable Increase Contrast + Bold Text + Reduce Transparency and verify
- [ ] Enable Reduce Motion and verify animations
- [ ] Test with Voice Control ("Show Names", "Show Numbers")
```

## Configuration

- **Standard mode** (default): Fixes P0 and P1 issues, reports P2
- **Comprehensive mode**: Fixes all priority levels — invoke with "comprehensive" or "full audit"

## Supporting Files

Loaded on-demand during execution:

- `rules/` — Individual detection and fix rules per issue category (16 rules)
- `references/swiftui-patterns.md` — Full SwiftUI accessibility modifier catalog
- `references/uikit-patterns.md` — Full UIKit accessibility API catalog
- `references/wcag-guidelines.md` — WCAG AA and Apple HIG reference
- `assets/audit-template.swift` — XCTest accessibility audit template
- `assets/checklist.md` — Manual verification checklist
