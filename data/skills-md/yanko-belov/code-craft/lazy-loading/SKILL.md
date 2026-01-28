---
name: lazy-loading
description: Use when loading all data upfront. Use when initial page load is slow. Use when fetching data that might not be needed.
---

# Lazy Loading

## Overview

**Load data when needed, not before. Don't fetch what you might not use.**

Upfront loading wastes bandwidth, memory, and time. Load on demand for better performance and user experience.

## When to Use

- Dashboard loads all data at once
- Page fetches data for hidden tabs
- Loading "just in case" data
- Initial load is slow

## The Iron Rule

```
NEVER load data until it's actually needed.
```

**No exceptions:**
- Not for "we might need it"
- Not for "parallel is faster"
- Not for "simpler to load everything"
- Not for "it's not that much data"

## Detection: Eager Overload Smell

If you load everything upfront, STOP:

```typescript
// ❌ VIOLATION: Load everything upfront
async function loadDashboard(userId: string) {
  const [
    profile,
    preferences,
    notifications,    // User might not check
    recentActivity,   // Collapsed by default
    analytics,        // Expensive, rarely viewed
    recommendations,  // Below the fold
    fullHistory       // Paginated anyway
  ] = await Promise.all([
    fetchProfile(userId),
    fetchPreferences(userId),
    fetchNotifications(userId),
    fetchRecentActivity(userId),
    fetchAnalytics(userId),       // Takes 2 seconds!
    fetchRecommendations(userId),
    fetchFullHistory(userId)      // 10MB of data!
  ]);
  
  return { profile, preferences, notifications, ... };
}
```

Problems:
- Slowest fetch blocks everything
- Wastes resources on unused data
- Poor perceived performance

## The Correct Pattern: Load On Demand

```typescript
// ✅ CORRECT: Load critical data first, rest on demand

// Initial load - only what's immediately visible
async function loadDashboard(userId: string) {
  const [profile, preferences] = await Promise.all([
    fetchProfile(userId),
    fetchPreferences(userId)
  ]);
  
  return { profile, preferences };
}

// React component with lazy loading
function Dashboard({ userId }) {
  // Critical data loaded immediately
  const { profile, preferences } = useInitialData(userId);
  
  // Notifications: load when header mounts
  const notifications = useLazyQuery(
    () => fetchNotifications(userId),
    { loadOn: 'mount' }
  );
  
  // Analytics: load when tab is selected
  const [analyticsTab, setAnalyticsTab] = useState(false);
  const analytics = useLazyQuery(
    () => fetchAnalytics(userId),
    { loadOn: analyticsTab }
  );
  
  // History: load when scrolled into view
  const historyRef = useRef();
  const history = useLazyQuery(
    () => fetchHistory(userId),
    { loadOn: useIntersectionObserver(historyRef) }
  );
  
  return (
    <div>
      <Header profile={profile} notifications={notifications} />
      <Tabs>
        <Tab label="Overview">...</Tab>
        <Tab label="Analytics" onSelect={() => setAnalyticsTab(true)}>
          {analytics.loading ? <Skeleton /> : <AnalyticsChart data={analytics.data} />}
        </Tab>
      </Tabs>
      <div ref={historyRef}>
        {history.data && <HistoryList items={history.data} />}
      </div>
    </div>
  );
}
```

## Lazy Loading Techniques

### 1. Load on Interaction
```typescript
// Load when user clicks tab
const [showDetails, setShowDetails] = useState(false);
const details = useQuery(fetchDetails, { enabled: showDetails });

<Tab onClick={() => setShowDetails(true)}>
  {details.data ?? <Skeleton />}
</Tab>
```

### 2. Load on Scroll (Intersection Observer)
```typescript
function LazySection({ loadFn, children }) {
  const ref = useRef();
  const [loaded, setLoaded] = useState(false);
  const data = useQuery(loadFn, { enabled: loaded });
  
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => entry.isIntersecting && setLoaded(true)
    );
    observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);
  
  return <div ref={ref}>{data.data ? children(data.data) : <Skeleton />}</div>;
}
```

### 3. Load on Route
```typescript
// Next.js / React Router
const AnalyticsPage = lazy(() => import('./AnalyticsPage'));

<Route path="/analytics" element={
  <Suspense fallback={<Loading />}>
    <AnalyticsPage />
  </Suspense>
} />
```

### 4. Pagination / Infinite Scroll
```typescript
function OrderList() {
  const [page, setPage] = useState(1);
  const { data, hasMore } = useOrders({ page, limit: 20 });
  
  return (
    <>
      {data.map(order => <OrderRow key={order.id} order={order} />)}
      {hasMore && <button onClick={() => setPage(p => p + 1)}>Load More</button>}
    </>
  );
}
```

## Pressure Resistance Protocol

### 1. "We Might Need It"
**Pressure:** "Load it now in case user needs it"

**Response:** "Might" means probably won't. Load when they actually need it.

**Action:** Load on demand, not on speculation.

### 2. "Parallel Is Faster"
**Pressure:** "Loading everything in parallel is faster than sequential"

**Response:** Parallel loading of unneeded data is slower than not loading it.

**Action:** Parallelize what you need. Lazy load what you might need.

### 3. "Simpler to Load Everything"
**Pressure:** "One fetch function is simpler"

**Response:** Simple code that's slow and wasteful isn't simple.

**Action:** Structured lazy loading is maintainable and performant.

## Red Flags - STOP and Reconsider

- `Promise.all` with 5+ fetches on page load
- Fetching data for collapsed/hidden sections
- Loading full lists instead of paginating
- Slow initial page loads
- "Loading..." takes more than 1-2 seconds

**All of these mean: Implement lazy loading.**

## Quick Reference

| Eager (Usually Bad) | Lazy (Usually Good) |
|---------------------|---------------------|
| Load all on mount | Load visible content first |
| Fetch hidden tab data | Fetch when tab selected |
| Full list at once | Paginate / infinite scroll |
| Below-fold content | Intersection observer |

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "Might need it" | Load when you do need it. |
| "Parallel is faster" | Not loading is fastest. |
| "Simpler" | Slow isn't simple. |
| "It's not much data" | It adds up. Bandwidth costs. |
| "Better UX to have it ready" | Slow load is worse UX. |

## The Bottom Line

**Load what's visible. Defer the rest. Paginate large lists.**

Initial load = critical data only. Everything else loads on interaction, scroll, or navigation. Users shouldn't wait for data they won't see.
