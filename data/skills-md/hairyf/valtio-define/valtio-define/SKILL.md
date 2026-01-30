---
name: valtio-define
description: Comprehensive skills for working with valtio-define
metadata:
  author: Hairyf
  version: "2025.01.29"
  source: Internal Documentation
---

> Based on valtio-define v1.0.1. A Valtio-based state management library with Pinia-like API for React applications.

## Overview

valtio-define provides a factory function for creating reactive stores with state, actions, and getters. Built on top of Valtio, it offers a familiar API similar to Pinia with full TypeScript support.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| defineStore | Core API for creating reactive stores | [core-define-store](references/core-define-store.md) |
| useStore | React hook for accessing store state | [core-use-store](references/core-use-store.md) |
| Types | TypeScript types and interfaces | [core-types](references/core-types.md) |

## Advanced Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| Subscriptions | Subscribe to state changes | [advanced-subscribe](references/advanced-subscribe.md) |
| Patch | Update state with patch operations | [advanced-patch](references/advanced-patch.md) |
| Signal | JSX component for inline reactive values | [advanced-signal](references/advanced-signal.md) |
| Store to State | Convert store to useState-like hooks | [advanced-store-to-state](references/advanced-store-to-state.md) |

## Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| Plugin System | Extend stores with plugins | [feature-plugin-system](references/feature-plugin-system.md) |
| Persistent Plugin | Persist state to storage | [feature-persistent-plugin](references/feature-persistent-plugin.md) |

## Quick Start

```tsx
import { defineStore, useStore } from 'valtio-define'

const store = defineStore({
  state: () => ({ count: 0 }),
  actions: {
    increment() { this.count++ },
  },
  getters: {
    doubled() { return this.count * 2 },
  },
})

function Counter() {
  const state = useStore(store)
  return (
    <div>
      <div>Count: {state.count}</div>
      <div>Doubled: {state.doubled}</div>
      <button onClick={store.increment}>Increment</button>
    </div>
  )
}
```
