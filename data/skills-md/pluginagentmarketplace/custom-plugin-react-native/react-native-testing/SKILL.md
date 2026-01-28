---
name: react-native-testing
description: Master testing - Jest, Testing Library, Detox E2E, and CI/CD integration
sasmp_version: "1.3.0"
bonded_agent: 06-react-native-testing
bond_type: PRIMARY_BOND
version: "2.0.0"
updated: "2025-01"
---

# React Native Testing Skill

> Learn comprehensive testing strategies including unit tests, component tests, and E2E tests.

## Prerequisites

- React Native basics
- Understanding of async/await
- Familiarity with testing concepts

## Learning Objectives

After completing this skill, you will be able to:
- [ ] Configure Jest for React Native
- [ ] Write component tests with Testing Library
- [ ] Mock native modules and APIs
- [ ] Implement E2E tests with Detox/Maestro
- [ ] Set up CI/CD test pipelines

---

## Topics Covered

### 1. Jest Setup
```javascript
// jest.config.js
module.exports = {
  preset: 'react-native',
  setupFilesAfterEnv: ['@testing-library/jest-native/extend-expect'],
  transformIgnorePatterns: [
    'node_modules/(?!(react-native|@react-native)/)',
  ],
};
```

### 2. Component Testing
```tsx
import { render, screen, fireEvent } from '@testing-library/react-native';
import { Button } from './Button';

describe('Button', () => {
  it('calls onPress when pressed', () => {
    const onPress = jest.fn();
    render(<Button title="Click" onPress={onPress} />);

    fireEvent.press(screen.getByText('Click'));

    expect(onPress).toHaveBeenCalled();
  });
});
```

### 3. Hook Testing
```tsx
import { renderHook, act } from '@testing-library/react-native';
import { useCounter } from './useCounter';

describe('useCounter', () => {
  it('increments count', () => {
    const { result } = renderHook(() => useCounter());

    act(() => result.current.increment());

    expect(result.current.count).toBe(1);
  });
});
```

### 4. Mocking
```typescript
// Mock native module
jest.mock('@react-native-async-storage/async-storage', () => ({
  setItem: jest.fn(),
  getItem: jest.fn(),
}));

// Mock API
jest.mock('./api', () => ({
  fetchUser: jest.fn().mockResolvedValue({ id: '1', name: 'Test' }),
}));
```

### 5. E2E with Detox
```typescript
describe('Login', () => {
  beforeAll(async () => {
    await device.launchApp();
  });

  it('should login successfully', async () => {
    await element(by.id('email')).typeText('test@example.com');
    await element(by.id('password')).typeText('password');
    await element(by.id('login-btn')).tap();

    await expect(element(by.id('home'))).toBeVisible();
  });
});
```

---

## Quick Start Example

```tsx
// ProductCard.test.tsx
import { render, screen, fireEvent } from '@testing-library/react-native';
import { ProductCard } from './ProductCard';

const mockProduct = {
  id: '1',
  title: 'Test Product',
  price: 99.99,
};

describe('ProductCard', () => {
  it('renders product info', () => {
    render(<ProductCard {...mockProduct} onPress={jest.fn()} />);

    expect(screen.getByText('Test Product')).toBeOnTheScreen();
    expect(screen.getByText('$99.99')).toBeOnTheScreen();
  });

  it('handles press', () => {
    const onPress = jest.fn();
    render(<ProductCard {...mockProduct} onPress={onPress} />);

    fireEvent.press(screen.getByRole('button'));

    expect(onPress).toHaveBeenCalledWith('1');
  });
});
```

---

## Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| "Cannot find module" | Missing mock | Add jest.mock() |
| Async timeout | Missing await | Use waitFor() |
| Element not found | Wrong query | Check testID/role |

---

## Validation Checklist

- [ ] Unit tests pass
- [ ] Component tests cover interactions
- [ ] E2E tests complete flows
- [ ] Coverage meets threshold (80%+)

---

## Usage

```
Skill("react-native-testing")
```

**Bonded Agent**: `06-react-native-testing`
