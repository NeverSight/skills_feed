---
name: vue-vite-testing
description: Comprehensive unit testing guide for Vue 3 + Vite projects using Vitest and Vue Test Utils. Use when writing or reviewing unit tests for Vue components, composables, Pinia stores, or TypeScript/JavaScript utilities in Vite-based projects. Covers test structure, best practices, mocking strategies, and Vue-specific testing patterns.
---

# Vue + Vite Unit Testing

## Overview

Generate comprehensive, production-ready unit tests for Vue 3 + Vite projects using Vitest framework. Follow industry best practices for testing Vue components, composables, Pinia stores, and TypeScript utilities with proper isolation, mocking, and edge case coverage.

## Testing Framework Setup

**Primary Stack:**
- **Vitest**: Fast unit test framework built for Vite
- **Vue Test Utils**: Official testing utility library for Vue components
- **@vitest/ui**: Optional UI for test visualization

**Import pattern:**
```typescript
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { mount, shallowMount } from '@vue/test-utils';
```

## Testing Workflow

Follow this systematic approach for all testing tasks:

### 1. Code Analysis Phase

**Before writing any tests:**
- Analyze the code structure and identify all public interfaces
- Identify external dependencies (APIs, stores, composables, modules)
- Note all possible code paths, conditions, and edge cases
- Ask clarifying questions about:
  - Missing type definitions or constants
  - Unclear business logic or validation rules
  - External API contracts or data structures
  - Expected error handling behaviors

**Only proceed to writing tests after full code understanding.**

### 2. Test Design Phase

**Plan test coverage:**
- Happy path scenarios (expected inputs and outputs)
- Error handling and failure modes
- Edge cases (empty arrays, null values, boundary conditions)
- Async operations (loading, success, error states)
- User interactions (clicks, inputs, form submissions)
- Lifecycle hooks and reactivity

**For Vue components, identify:**
- Props validation and default values
- Emitted events and their payloads
- Slots usage and content projection
- Computed properties and watchers
- Component lifecycle behavior

**For composables, identify:**
- Input parameters and return values
- State management and reactivity
- Side effects (API calls, localStorage, timers)
- Cleanup requirements

## Test Structure Standards

### Standard Test Template

```typescript
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';

describe('ModuleName or ComponentName', () => {
  // Top-level test variables
  let mockDependency: MockType;
  
  beforeEach(() => {
    // Reset state before each test
    mockDependency = createMockDependency();
  });

  afterEach(() => {
    // Cleanup after each test
    vi.clearAllMocks();
  });

  describe('method or feature name', () => {
    it('should handle happy path scenario', () => {
      // Arrange: Set up test data and mocks
      const input = { /* test data */ };
      
      // Act: Execute the code under test
      const result = functionUnderTest(input);
      
      // Assert: Verify expected outcomes
      expect(result).toBe(expectedValue);
    });

    it('should handle error case', async () => {
      // Arrange
      mockDependency.method.mockRejectedValue(new Error('test error'));
      
      // Act & Assert
      await expect(functionUnderTest()).rejects.toThrow('test error');
    });

    it('should handle edge case: empty input', () => {
      // Test edge cases
      expect(functionUnderTest([])).toEqual([]);
    });
  });
});
```

### AAA Pattern (Arrange-Act-Assert)

**Always structure individual tests using AAA:**

```typescript
it('should calculate total price correctly', () => {
  // Arrange: Set up test data
  const items = [
    { price: 100, quantity: 2 },
    { price: 50, quantity: 1 }
  ];
  
  // Act: Execute the function
  const total = calculateTotal(items);
  
  // Assert: Verify the result
  expect(total).toBe(250);
});
```

## Vue-Specific Testing Patterns

### 1. Component Testing

**Decide between mount vs shallowMount:**
- Use `mount()` for integration testing with child components
- Use `shallowMount()` for isolated unit testing (stubs child components)

```typescript
import { mount } from '@vue/test-utils';
import MyComponent from './MyComponent.vue';

describe('MyComponent', () => {
  it('should render with props', () => {
    const wrapper = mount(MyComponent, {
      props: {
        title: 'Test Title',
        count: 5
      }
    });
    
    expect(wrapper.find('h1').text()).toBe('Test Title');
    expect(wrapper.find('.count').text()).toBe('5');
  });

  it('should emit event on button click', async () => {
    const wrapper = mount(MyComponent);
    
    await wrapper.find('button').trigger('click');
    
    expect(wrapper.emitted('submit')).toBeTruthy();
    expect(wrapper.emitted('submit')[0]).toEqual([{ data: 'value' }]);
  });

  it('should handle v-model binding', async () => {
    const wrapper = mount(MyComponent, {
      props: {
        modelValue: 'initial'
      }
    });
    
    await wrapper.find('input').setValue('updated');
    
    expect(wrapper.emitted('update:modelValue')[0]).toEqual(['updated']);
  });
});
```

**See `references/component-testing.md` for complete component testing patterns including slots, provide/inject, and async components.**

### 2. Composables Testing

```typescript
import { composableUnderTest } from './useFeature';

describe('useFeature composable', () => {
  it('should initialize with default state', () => {
    const { state, count } = composableUnderTest();
    
    expect(state.value).toBe('idle');
    expect(count.value).toBe(0);
  });

  it('should update reactive state', () => {
    const { increment, count } = composableUnderTest();
    
    increment();
    
    expect(count.value).toBe(1);
  });

  it('should handle async operations', async () => {
    const { fetchData, data, loading } = composableUnderTest();
    
    expect(loading.value).toBe(false);
    
    const promise = fetchData();
    expect(loading.value).toBe(true);
    
    await promise;
    expect(loading.value).toBe(false);
    expect(data.value).toBeDefined();
  });
});
```

**See `references/composables-testing.md` for advanced composable testing patterns including side effects and cleanup.**

### 3. Pinia Store Testing

```typescript
import { setActivePinia, createPinia } from 'pinia';
import { useMyStore } from './myStore';

describe('myStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('should initialize with default state', () => {
    const store = useMyStore();
    
    expect(store.items).toEqual([]);
    expect(store.loading).toBe(false);
  });

  it('should add item to store', () => {
    const store = useMyStore();
    const newItem = { id: 1, name: 'Test' };
    
    store.addItem(newItem);
    
    expect(store.items).toContainEqual(newItem);
  });

  it('should handle async actions', async () => {
    const store = useMyStore();
    
    await store.fetchItems();
    
    expect(store.loading).toBe(false);
    expect(store.items.length).toBeGreaterThan(0);
  });
});
```

**See `references/store-testing.md` for Pinia store testing patterns including getters, mutations, and actions.**

## Mocking Strategies

### External Dependencies

```typescript
// Mock API calls
vi.mock('@/api/users', () => ({
  fetchUsers: vi.fn(),
  createUser: vi.fn()
}));

// Mock composables
vi.mock('@/composables/useAuth', () => ({
  useAuth: vi.fn(() => ({
    user: { id: 1, name: 'Test User' },
    isAuthenticated: true,
    login: vi.fn(),
    logout: vi.fn()
  }))
}));

// Mock Vue Router
const mockRouter = {
  push: vi.fn(),
  replace: vi.fn()
};

const wrapper = mount(Component, {
  global: {
    mocks: {
      $router: mockRouter
    }
  }
});
```

### Timers and Delays

```typescript
import { vi } from 'vitest';

describe('setTimeout behavior', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('should execute callback after delay', () => {
    const callback = vi.fn();
    
    setTimeout(callback, 1000);
    
    expect(callback).not.toHaveBeenCalled();
    
    vi.advanceTimersByTime(1000);
    
    expect(callback).toHaveBeenCalledOnce();
  });
});
```

## Testing Best Practices

### 1. Test Isolation
- Each test should be independent and not rely on other tests
- Use `beforeEach` to reset state
- Clean up mocks with `vi.clearAllMocks()` or `vi.resetAllMocks()`

### 2. Descriptive Test Names
```typescript
// ✅ Good: Clear and descriptive
it('should display error message when API request fails', () => {});

// ❌ Bad: Vague and unclear
it('should work', () => {});
```

### 3. Avoid Test Logic
```typescript
// ❌ Bad: Contains loops and conditions
it('should validate all items', () => {
  for (const item of items) {
    if (item.type === 'special') {
      expect(validate(item)).toBe(true);
    }
  }
});

// ✅ Good: Simple and direct
it('should validate special item', () => {
  const specialItem = { type: 'special', value: 100 };
  expect(validate(specialItem)).toBe(true);
});

it('should validate normal item', () => {
  const normalItem = { type: 'normal', value: 50 };
  expect(validate(normalItem)).toBe(true);
});
```

### 4. Test Coverage Priority
1. **Critical business logic** (payment, authentication, data validation)
2. **Complex algorithms** (calculations, transformations)
3. **Error handling** (edge cases, failure modes)
4. **User interactions** (forms, buttons, navigation)
5. **Integration points** (API calls, external services)

### 5. Async Testing
```typescript
// ✅ Properly handle async operations
it('should fetch data successfully', async () => {
  const result = await fetchData();
  expect(result).toBeDefined();
});

// ✅ Use resolves/rejects for promises
await expect(fetchData()).resolves.toEqual(expectedData);
await expect(failingOperation()).rejects.toThrow('Error message');
```

## Complete Test Deliverables

When generating tests, always provide:

1. **Complete test suites** - No placeholders or "// TODO" comments
2. **All edge cases covered** - Empty inputs, null values, boundaries
3. **Proper imports** - All necessary test utilities and dependencies
4. **Appropriate mocks** - For external dependencies and side effects
5. **Clear test descriptions** - Self-documenting test names
6. **Proper cleanup** - afterEach hooks where needed

## Reference Files

For detailed examples and advanced patterns:

- **`references/component-testing.md`** - Comprehensive component testing patterns (slots, teleport, provide/inject, async components)
- **`references/composables-testing.md`** - Advanced composable testing (side effects, watchers, cleanup)
- **`references/store-testing.md`** - Pinia store testing patterns (getters, actions, state management)