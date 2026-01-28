---
name: react-performance
description: Master React performance optimization with memoization, code splitting, profiling, and Web Vitals monitoring
sasmp_version: "2.0.0"
bonded_agent: 06-performance-optimization
bond_type: PRIMARY_BOND
input_validation:
  required_packages:
    - "react": ">=18.0.0"
    - "web-vitals": ">=3.0.0"
output_format:
  code_examples: jsx
  metrics_target:
    lcp: "<2.5s"
    fid: "<100ms"
    cls: "<0.1"
error_handling:
  patterns:
    - graceful_degradation
    - lazy_fallback
    - error_boundary
observability:
  logging: web_vitals
  metrics: ["lcp", "fid", "cls", "ttfb", "inp"]
---

# React Performance Optimization Skill

## Overview
Master React performance optimization techniques including memoization, code splitting, lazy loading, and profiling tools.

## Learning Objectives
- Identify performance bottlenecks
- Use React DevTools Profiler
- Implement memoization strategies
- Apply code splitting techniques
- Optimize bundle size

## React DevTools Profiler

### Profiling Steps
1. Open React DevTools
2. Go to Profiler tab
3. Click record button
4. Interact with app
5. Stop recording
6. Analyze flame graph

### Reading Results
- **Render duration**: Time spent rendering
- **Commits**: Number of renders
- **Flame graph**: Visual render tree
- **Ranked chart**: Components by render time

## Memoization

### React.memo
```jsx
// Prevent re-render if props unchanged
const ExpensiveComponent = React.memo(function ExpensiveComponent({ data }) {
  return <div>{data.value}</div>;
});

// Custom comparison
const Component = React.memo(
  ({ user }) => <div>{user.name}</div>,
  (prevProps, nextProps) => {
    return prevProps.user.id === nextProps.user.id;
  }
);
```

### useMemo
```jsx
function ProductList({ products, searchTerm }) {
  // Only re-filter when dependencies change
  const filteredProducts = useMemo(() => {
    console.log('Filtering...');
    return products.filter(p =>
      p.name.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }, [products, searchTerm]);

  return <div>{filteredProducts.map(renderProduct)}</div>;
}
```

### useCallback
```jsx
function Parent() {
  const [count, setCount] = useState(0);

  // Stable function reference
  const handleClick = useCallback(() => {
    setCount(c => c + 1);
  }, []);

  return <MemoizedChild onClick={handleClick} />;
}

const MemoizedChild = React.memo(({ onClick }) => {
  console.log('Child rendered');
  return <button onClick={onClick}>Click</button>;
});
```

## Code Splitting

### Route-Based Splitting
```jsx
import { lazy, Suspense } from 'react';
import { Routes, Route } from 'react-router-dom';

const Home = lazy(() => import('./pages/Home'));
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));

function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}
```

### Component-Based Splitting
```jsx
function ProductPage() {
  const [showReviews, setShowReviews] = useState(false);

  const Reviews = lazy(() => import('./Reviews'));

  return (
    <div>
      <ProductInfo />
      <button onClick={() => setShowReviews(true)}>
        Show Reviews
      </button>
      {showReviews && (
        <Suspense fallback={<Spinner />}>
          <Reviews />
        </Suspense>
      )}
    </div>
  );
}
```

## List Virtualization

### React Window
```jsx
import { FixedSizeList } from 'react-window';

function VirtualList({ items }) {
  return (
    <FixedSizeList
      height={600}
      itemCount={items.length}
      itemSize={50}
      width="100%"
    >
      {({ index, style }) => (
        <div style={style}>
          {items[index].name}
        </div>
      )}
    </FixedSizeList>
  );
}
```

## Image Optimization

### Lazy Loading
```jsx
function LazyImage({ src, alt }) {
  const [isLoaded, setIsLoaded] = useState(false);
  const [isInView, setIsInView] = useState(false);
  const imgRef = useRef();

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsInView(true);
          observer.disconnect();
        }
      },
      { threshold: 0.1 }
    );

    if (imgRef.current) observer.observe(imgRef.current);

    return () => observer.disconnect();
  }, []);

  return (
    <div ref={imgRef}>
      {isInView && (
        <img
          src={src}
          alt={alt}
          onLoad={() => setIsLoaded(true)}
          style={{ opacity: isLoaded ? 1 : 0 }}
        />
      )}
    </div>
  );
}
```

## Bundle Optimization

### Tree Shaking
```jsx
// Good: Named imports
import { Button, Input } from 'components';

// Bad: Import everything
import * as Components from 'components';
```

### Dynamic Imports
```jsx
async function exportData() {
  const XLSX = await import('xlsx');
  // Use XLSX only when needed
}
```

### Bundle Analysis
```bash
# Create React App
npm install --save-dev source-map-explorer
npm run build
npx source-map-explorer 'build/static/js/*.js'

# Vite
npm install --save-dev rollup-plugin-visualizer
```

## Common Mistakes

```jsx
// ❌ Overusing useMemo
const greeting = useMemo(() => `Hello ${name}`, [name]);

// ✅ Just compute
const greeting = `Hello ${name}`;

// ❌ Inline objects in deps
useEffect(() => {
  fetchData(filters);
}, [filters]); // New object every render!

// ✅ Memoize object
const filters = useMemo(() => ({ category, sort }), [category, sort]);

// ❌ Creating functions in render
{items.map(item => <Item onClick={() => handle(item.id)} />)}

// ✅ Use useCallback
const handle = useCallback((id) => {...}, []);
{items.map(item => <Item onClick={handle} id={item.id} />)}
```

## Web Vitals

### Measuring Performance
```jsx
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

function sendToAnalytics(metric) {
  console.log(metric);
}

getCLS(sendToAnalytics);
getFID(sendToAnalytics);
getFCP(sendToAnalytics);
getLCP(sendToAnalytics);
getTTFB(sendToAnalytics);
```

## Best Practices

1. **Profile before optimizing**
2. **Use React.memo for expensive components**
3. **Memoize only when beneficial**
4. **Split code at route boundaries**
5. **Virtualize long lists**
6. **Lazy load images**
7. **Monitor bundle size**

## When to Optimize

### DO Optimize
- Frequent renders
- Large lists (>100 items)
- Expensive calculations
- Heavy component trees

### DON'T Optimize
- Simple components
- Rare renders
- Cheap calculations
- Small lists (<50 items)

## Practice Exercises

1. Profile app with React DevTools
2. Optimize large product list
3. Implement code splitting
4. Build virtualized table
5. Optimize image gallery
6. Reduce bundle size
7. Measure Web Vitals

## Resources

- [React Performance](https://react.dev/learn/render-and-commit)
- [Web Vitals](https://web.dev/vitals/)
- [React Window](https://react-window.vercel.app)

---

**Difficulty**: Advanced
**Estimated Time**: 2-3 weeks
**Prerequisites**: React Hooks, Component Architecture
