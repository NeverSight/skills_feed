---
name: testing-team
description: Complete QA, playtesting, and code quality team for game development. Use when evaluating player experience, fun factor, game feel, code quality, test coverage, refactoring, performance testing, or build validation. Covers playtesting methodologies, UX research, unit/integration/e2e testing, code review, linting, accessibility, and continuous quality assurance. Triggers on requests for testing, QA, playtesting, code review, refactoring, bug tracking, or quality validation.
---

# Testing Team

Elite QA and playtesting specialists ensuring every build is fun, polished, and production-ready.

## Team Composition

| Role | Domain | Focus |
|------|--------|-------|
| **QA Lead** | Test strategy, release gates | Overall quality ownership |
| **Playtest Coordinator** | Fun factor, game feel | Player experience sessions |
| **UX Researcher** | Usability, player feedback | Data-driven UX decisions |
| **Code Quality Engineer** | Linting, patterns, refactoring | Clean, maintainable code |
| **Test Automation Engineer** | Unit, integration, e2e tests | Automated test coverage |
| **Performance Analyst** | Load testing, profiling | 60fps, fast loads |
| **Accessibility Specialist** | WCAG, inclusive design | Everyone can play |

## Playtesting Framework

### The Fun Factor Checklist

Before any build ships, validate these pillars:

```
□ ENGAGEMENT
  □ Does the core loop feel satisfying?
  □ Is there clear moment-to-moment feedback?
  □ Do players want "one more turn"?

□ CLARITY
  □ Do players understand what to do?
  □ Are goals and progress visible?
  □ Is the UI intuitive without tutorial?

□ PROGRESSION
  □ Does difficulty ramp appropriately?
  □ Are rewards meaningful and well-paced?
  □ Is there a sense of mastery over time?

□ JUICE
  □ Do interactions feel responsive?
  □ Are wins celebrated appropriately?
  □ Does the game have "weight" and polish?

□ FAIRNESS
  □ Do losses feel fair (not random/cheap)?
  □ Is RNG transparent to players?
  □ Are comeback mechanics present?
```

### Playtest Session Structure

```
SESSION TEMPLATE (45-60 minutes)

1. SETUP (5 min)
   - Fresh build, cleared save data
   - Screen recording enabled
   - Observer notes template ready

2. FIRST-TIME USER EXPERIENCE (15 min)
   - No guidance, observe natural behavior
   - Note: Where do they get stuck?
   - Note: What do they try first?
   - Note: Facial expressions, body language

3. GUIDED EXPLORATION (15 min)
   - Introduce features they missed
   - Ask: "What do you think this does?"
   - Ask: "How did that feel?"

4. FREE PLAY (10 min)
   - Let them play naturally
   - Note: What do they gravitate toward?
   - Note: What do they avoid?

5. DEBRIEF (10 min)
   - "What was most fun?"
   - "What was frustrating?"
   - "Would you play again? Why?"
   - "Rate 1-10: How fun was this?"
```

### Player Experience Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Session Length | >10 min | Analytics |
| Return Rate | >40% D1 | Analytics |
| Core Loop Completion | >80% | Funnel tracking |
| Rage Quit Rate | <5% | Session end analysis |
| Fun Rating | >7/10 | Post-session survey |
| Confusion Events | <3/session | Observer notes |
| "Aha!" Moments | >2/session | Observer notes |

## Code Quality Standards

### Linting & Formatting

```json
// .eslintrc.json for the project
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:react-hooks/recommended",
    "prettier"
  ],
  "rules": {
    "@typescript-eslint/no-unused-vars": "error",
    "@typescript-eslint/explicit-function-return-type": "warn",
    "react-hooks/exhaustive-deps": "error",
    "no-console": ["warn", { "allow": ["warn", "error"] }],
    "complexity": ["warn", 10],
    "max-lines-per-function": ["warn", 50]
  }
}
```

```json
// biome.json alternative
{
  "linter": {
    "rules": {
      "complexity": {
        "noExcessiveCognitiveComplexity": {
          "level": "warn",
          "options": { "maxAllowedComplexity": 15 }
        }
      },
      "correctness": {
        "useExhaustiveDependencies": "error"
      }
    }
  }
}
```

### Code Review Checklist

```markdown
## PR Review Template

### Functionality
- [ ] Code does what the PR description claims
- [ ] Edge cases are handled
- [ ] Error states are managed gracefully
- [ ] No regressions in existing features

### Code Quality
- [ ] Functions are small and focused (<50 lines)
- [ ] Names are clear and descriptive
- [ ] No magic numbers (use constants)
- [ ] Complex logic has comments explaining "why"
- [ ] No duplicate code (DRY)
- [ ] TypeScript types are specific (no `any`)

### Performance
- [ ] No unnecessary re-renders (React)
- [ ] Heavy computations are memoized
- [ ] No memory leaks (cleanup in useEffect)
- [ ] Bundle size impact is acceptable

### Testing
- [ ] New code has tests
- [ ] Tests are meaningful (not just coverage)
- [ ] Tests run fast (<100ms each)

### Game-Specific
- [ ] Game feel is preserved
- [ ] Animation timing matches design
- [ ] Sound effects trigger correctly
- [ ] Mobile/touch interactions work
```

### Refactoring Patterns

**When to Refactor:**
```
RED FLAGS:
- Function > 50 lines
- File > 300 lines
- Cyclomatic complexity > 10
- More than 3 levels of nesting
- Repeated code blocks
- "Utils" file growing unbounded
- Props drilling > 3 levels
- useEffect with 5+ dependencies
```

**Safe Refactoring Process:**
```
1. Ensure tests exist (write them first if not)
2. Make ONE change at a time
3. Run tests after each change
4. Commit working states frequently
5. Review diff before finalizing
```

## Test Automation

### Test Pyramid for Games

```
        ╱╲
       ╱  ╲        E2E Tests (Playwright)
      ╱ 10%╲       - Full user flows
     ╱──────╲      - Critical paths only
    ╱        ╲
   ╱   20%    ╲    Integration Tests
  ╱────────────╲   - Component interactions
 ╱              ╲  - Store + UI together
╱      70%       ╲ Unit Tests (Vitest)
╲────────────────╱ - Pure functions
                   - Game logic
                   - Utilities
```

### Unit Test Examples

```typescript
// Game logic tests
import { describe, it, expect } from 'vitest';
import { calculateBet, hexDistance, spreadTrouble } from './game-engine';

describe('calculateBet', () => {
  it('returns 0 for fold', () => {
    expect(calculateBet(1000, 'fold')).toBe(0);
  });

  it('returns 10% of coins for call', () => {
    expect(calculateBet(1000, 'call')).toBe(100);
  });

  it('returns all coins for all_in', () => {
    expect(calculateBet(1000, 'all_in')).toBe(1000);
  });

  it('floors fractional amounts', () => {
    expect(calculateBet(1005, 'call')).toBe(100);
  });
});

describe('hexDistance', () => {
  it('returns 0 for same hex', () => {
    const hex = { q: 0, r: 0, s: 0 };
    expect(hexDistance(hex, hex)).toBe(0);
  });

  it('calculates adjacent hex distance as 1', () => {
    const a = { q: 0, r: 0, s: 0 };
    const b = { q: 1, r: -1, s: 0 };
    expect(hexDistance(a, b)).toBe(1);
  });
});
```

### Component Test Examples

```typescript
// Component tests with Testing Library
import { render, screen, fireEvent } from '@testing-library/react';
import { ResourceBar } from './ResourceBar';

describe('ResourceBar', () => {
  it('displays the resource value', () => {
    render(<ResourceBar value={500} label="Coins" icon="🪙" />);
    expect(screen.getByText('500')).toBeInTheDocument();
  });

  it('animates on value change', async () => {
    const { rerender } = render(<ResourceBar value={500} label="Coins" />);
    rerender(<ResourceBar value={600} label="Coins" />);
    
    // Check for delta indicator
    expect(screen.getByText('+100')).toBeInTheDocument();
  });
});
```

### E2E Test Examples

```typescript
// Playwright e2e tests
import { test, expect } from '@playwright/test';

test.describe('Game Flow', () => {
  test('complete a full day cycle', async ({ page }) => {
    await page.goto('/game');
    
    // Verify initial state
    await expect(page.getByText('Day 1')).toBeVisible();
    await expect(page.getByText('Morning')).toBeVisible();
    
    // Advance through phases
    await page.getByRole('button', { name: /advance/i }).click();
    await expect(page.getByText('Action')).toBeVisible();
    
    // Place a bet
    await page.getByTestId('water-pot').click();
    await page.getByRole('button', { name: /call/i }).click();
    
    // Continue to resolution
    await page.getByRole('button', { name: /advance/i }).click();
    await expect(page.getByText('Resolution')).toBeVisible();
    
    // Verify score changed
    const score = await page.getByTestId('score').textContent();
    expect(parseInt(score || '0')).toBeGreaterThan(0);
  });

  test('hex interaction works', async ({ page }) => {
    await page.goto('/game');
    
    // Click a hex
    await page.getByTestId('hex-0-0').click();
    
    // Verify selection
    await expect(page.getByTestId('hex-0-0')).toHaveClass(/selected/);
  });
});
```

### Test Commands

```bash
# Run all tests
bun run test

# Watch mode
bun run test:watch

# Coverage report
bun run test:coverage

# E2E tests
bun run test:e2e

# Type checking
bun run check-types
```

## Performance Testing

### Metrics & Budgets

| Metric | Budget | Tool |
|--------|--------|------|
| First Contentful Paint | <1.5s | Lighthouse |
| Time to Interactive | <3s | Lighthouse |
| Frame Rate | 60fps stable | Chrome DevTools |
| JS Bundle | <200KB gzipped | Bundlesize |
| Memory (gameplay) | <100MB | Chrome DevTools |
| Animation Jank | 0 dropped frames | Performance panel |

### Performance Checklist

```markdown
## Per-Build Performance Review

### Initial Load
- [ ] Bundle size within budget
- [ ] No render-blocking resources
- [ ] Images optimized and lazy-loaded
- [ ] Fonts preloaded

### Runtime
- [ ] 60fps during gameplay
- [ ] No memory leaks (check after 10 min play)
- [ ] Animations use GPU (transform/opacity only)
- [ ] Large lists are virtualized

### Mobile
- [ ] Touch response <100ms
- [ ] No janky scrolling
- [ ] Battery usage reasonable
```

## Build Validation Gates

### Pre-Merge Checklist

```yaml
# CI Pipeline Gates
quality_gates:
  - name: "Lint"
    command: "bun run lint"
    required: true
    
  - name: "Type Check"
    command: "bun run check-types"
    required: true
    
  - name: "Unit Tests"
    command: "bun run test"
    required: true
    coverage_threshold: 70%
    
  - name: "Build"
    command: "bun run build"
    required: true
    
  - name: "Bundle Size"
    max_size: "200KB"
    required: true
    
  - name: "E2E Smoke"
    command: "bun run test:e2e --grep @smoke"
    required: true
```

### Release Readiness

```markdown
## Release Checklist

### Code Quality
- [ ] All tests passing
- [ ] No TypeScript errors
- [ ] No ESLint errors
- [ ] Code coverage >70%

### Functionality
- [ ] All features work as designed
- [ ] No P0/P1 bugs open
- [ ] Regression suite passing

### Performance
- [ ] Lighthouse score >90
- [ ] 60fps confirmed
- [ ] Load time <3s

### Player Experience
- [ ] Playtest feedback addressed
- [ ] Fun rating >7/10
- [ ] No confusion points remaining

### Accessibility
- [ ] Keyboard navigation works
- [ ] Screen reader compatible
- [ ] Color contrast passes
- [ ] Reduced motion supported
```

## Bug Tracking Template

```markdown
## Bug Report

**Title:** [Brief description]

**Severity:** P0 (Blocker) | P1 (Critical) | P2 (Major) | P3 (Minor)

**Environment:**
- Build: [version/commit]
- Browser: [name + version]
- Device: [desktop/mobile + specs]

**Steps to Reproduce:**
1. 
2. 
3. 

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happens]

**Frequency:** Always | Sometimes | Rare

**Screenshots/Video:**
[Attach here]

**Additional Context:**
[Console errors, network logs, etc.]
```

## Reference Documents

- [Playtesting Methods](references/playtesting.md) - Session formats, feedback collection
- [Test Automation Guide](references/test-automation.md) - Vitest, Playwright patterns
- [Code Quality Patterns](references/code-quality.md) - Refactoring, clean code
- [Performance Profiling](references/performance.md) - Debugging slowness
