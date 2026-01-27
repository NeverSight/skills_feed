---
name: frontend-developer-skill
description: Comprehensive frontend development specialist for building modern web applications with React, Vue, Angular, and modern tooling including state management, testing, and performance optimization
---

# Frontend Developer Skill

## Purpose

Provides complete frontend development expertise for building production-ready web applications with modern frameworks (React, Vue, Next.js), comprehensive tooling setup, state management patterns, testing infrastructure, and performance optimization strategies.

## When to Use

- Building new React, Vue, or Angular applications from scratch
- Setting up modern frontend tooling (Vite, ESLint, Prettier, testing frameworks)
- Implementing state management with Redux Toolkit, Zustand, or Context API
- Configuring authentication flows with token management and protected routes
- Optimizing bundle size and performance for production deployments
- Creating component libraries and design systems
- Setting up comprehensive testing (unit, integration, E2E)

## Quick Start

**Invoke this skill when:**
- Building React, Vue, or Angular applications
- Setting up frontend tooling (Vite, ESLint, Prettier)
- Implementing state management (Redux Toolkit, Zustand, Context)
- Configuring authentication flows
- Optimizing bundle size and performance
- Setting up testing (Vitest, Jest, Playwright)

**Do NOT invoke when:**
- Only backend API needed → Use backend-developer
- Database optimization → Use database-optimizer
- DevOps/deployment only → Use devops-engineer
- UI/UX design without code → Use ui-designer

## Decision Framework

### Framework Selection

```
Frontend Framework Selection
├─ New Project (greenfield)
│   ├─ Needs SEO + server-side rendering
│   │   ├─ Team knows React → Next.js 14+
│   │   ├─ Team knows Vue → Nuxt.js 3+
│   │   └─ Team flexible → Next.js (ecosystem advantage)
│   │
│   ├─ SPA without SSR requirements
│   │   ├─ React experience → React 18+ (Vite)
│   │   ├─ Vue experience → Vue 3 (Vite)
│   │   └─ Enterprise/complex forms → Angular 15+
│   │
│   └─ Static site (blog, docs)
│       └─ Astro, Next.js SSG, or Vite + React
│
└─ Existing Project
    └─ Continue with existing framework (consistency)
```

### State Management Selection

| Scenario | Library | Bundle Size | Use Case |
|----------|---------|-------------|----------|
| Simple local state | useState, useReducer | 0 KB | Component-level state |
| Shared state (2-3 components) | Context API | 0 KB | Theme, auth, simple global |
| Medium app (<10 slices) | Zustand | ~1 KB | Most apps, good DX |
| Large app (10+ slices) | Redux Toolkit | ~11 KB | Enterprise, time-travel debug |
| Server state | TanStack Query | ~12 KB | API data, caching |

### Styling Approach

```
Styling Decision
├─ Rapid prototyping → Tailwind CSS
├─ Component library → Radix UI + Tailwind
├─ Dynamic theming → CSS-in-JS (Styled Components, Emotion)
├─ Large team → CSS Modules or Tailwind + Design Tokens
└─ Performance-critical → Plain CSS / SCSS
```

## Best Practices

1. **Use functional components** - Modern React pattern
2. **Leverage hooks** - Avoid class components when possible
3. **Memoize expensive operations** - Use useMemo, useCallback
4. **Lazy load components** - Reduce initial bundle size
5. **Type everything** - Leverage TypeScript
6. **Test thoroughly** - Unit, integration, and E2E tests
7. **Optimize images** - Use modern formats and lazy loading
8. **Implement error boundaries** - Catch errors gracefully
9. **Make it accessible** - ARIA labels, keyboard navigation
10. **Monitor performance** - Track Core Web Vitals

## Common Patterns

### Custom Hooks

```typescript
function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(url)
      .then(res => res.json())
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [url]);

  return { data, loading, error };
}
```

### Container/Presentational

```typescript
// Presentational (dumb)
const UserList = ({ users, onUserClick }: UserListProps) => (
  <ul>
    {users.map(user => (
      <li key={user.id} onClick={() => onUserClick(user.id)}>
        {user.name}
      </li>
    ))}
  </ul>
);

// Container (smart)
const UserListContainer = () => {
  const { users, fetchUsers } = useUsers();
  useEffect(() => fetchUsers(), [fetchUsers]);
  return <UserList users={users} onUserClick={handleClick} />;
};
```

## Troubleshooting

### Common Issues

**State not updating**
- Check if using correct setter
- Verify dependency arrays in useEffect
- Ensure components are re-rendering

**Component not re-rendering**
- Check for unnecessary re-renders
- Verify memoization is working
- Review prop changes

**Performance issues**
- Profile with React DevTools
- Check for large bundle sizes
- Review unnecessary re-renders
- Implement code splitting

**Tests failing**
- Verify test setup
- Check mock implementations
- Review async handling
- Ensure proper cleanup

## Quality Checklist

### Architecture
- [ ] Framework choice justified
- [ ] State management clear (server vs client state separated)
- [ ] Component structure logical
- [ ] Code splitting implemented

### Code Quality
- [ ] TypeScript strict mode enabled
- [ ] ESLint + Prettier configured
- [ ] Tests exist for critical paths
- [ ] No prop drilling (use state management)

### Performance
- [ ] Bundle size optimized (<200KB gzipped)
- [ ] Expensive operations memoized
- [ ] Images optimized (lazy loading, WebP)
- [ ] Third-party libraries evaluated

### Testing
- [ ] Testing framework configured
- [ ] Critical paths tested
- [ ] E2E tests exist

### Security
- [ ] Environment variables secured
- [ ] Input sanitization
- [ ] Auth tokens secure
- [ ] Dependencies audited

## Integration Patterns

### react-specialist
- **Handoff:** frontend-developer sets up tooling → react-specialist implements complex component logic
- **Tools:** Both use React; frontend-developer handles ecosystem tooling

### nextjs-developer
- **Handoff:** When SSR/SEO required → hand off for Next.js-specific features
- **Tools:** frontend-developer uses Vite/CRA; nextjs-developer uses Next.js App Router

### backend-developer
- **Handoff:** frontend-developer implements API client → backend-developer provides API contracts
- **Tools:** frontend-developer uses Axios/Fetch, TanStack Query

### frontend-ui-ux-engineer
- **Handoff:** frontend-developer sets up component structure → frontend-ui-ux-engineer styles
- **Tools:** Both use React; frontend-ui-ux-engineer adds Framer Motion, Tailwind design tokens

## Additional Resources

- **Detailed Technical Reference**: See [REFERENCE.md](REFERENCE.md)
- **Code Examples & Patterns**: See [EXAMPLES.md](EXAMPLES.md)
