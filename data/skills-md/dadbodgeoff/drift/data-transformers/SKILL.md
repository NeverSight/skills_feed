---
name: data-transformers
description: Centralized transformation logic for consistent data shaping across API routes. Includes aggregators, rankers, trend calculators, and data sanitizers.
license: MIT
compatibility: TypeScript/JavaScript
metadata:
  category: api
  time: 2h
  source: drift-masterguide
---

# Data Transformers

Centralized transformation logic for consistent data shaping across API routes.

## When to Use This Skill

- Data transformation is scattered across routes
- Need consistent output formats across endpoints
- Want testable, reusable transformation functions
- Building dashboards with aggregated data

## Core Concepts

Centralize all transformation logic in one place:
- Aggregators (category totals, counts)
- Rankers (top-N by score)
- Trend calculators (comparing periods)
- Sanitizers (validate and clean data)

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Raw Data   │────▶│ Transformers │────▶│  API Output │
└─────────────┘     └──────────────┘     └─────────────┘
```

## Implementation

### TypeScript

```typescript
// lib/transformers.ts

// ============================================
// Category Aggregation
// ============================================

interface CategoryTotals {
  [category: string]: number;
}

function aggregateCategories(
  items: Array<{ category: string; count?: number }>
): CategoryTotals {
  const totals: CategoryTotals = {};

  for (const item of items) {
    const category = item.category?.toUpperCase() || 'OTHER';
    totals[category] = (totals[category] || 0) + (item.count ?? 1);
  }

  return totals;
}

function categoriesToBreakdown(
  totals: CategoryTotals,
  previousTotals?: CategoryTotals
): Array<{ category: string; count: number; percentage: number; trend: string }> {
  const total = Object.values(totals).reduce((sum, count) => sum + count, 0);
  
  return Object.entries(totals)
    .map(([category, count]) => {
      let trend: 'increasing' | 'stable' | 'decreasing' = 'stable';
      
      if (previousTotals) {
        const prevCount = previousTotals[category] ?? 0;
        const change = count - prevCount;
        if (change > prevCount * 0.1) trend = 'increasing';
        else if (change < -prevCount * 0.1) trend = 'decreasing';
      }

      return {
        category,
        count,
        percentage: total > 0 ? count / total : 0,
        trend,
      };
    })
    .sort((a, b) => b.count - a.count);
}

// ============================================
// Ranking
// ============================================

interface Rankable {
  score: number;
  count: number;
}

function rankItems<T extends Rankable>(
  items: T[], 
  limit = 5
): (T & { rank: number })[] {
  return items
    .sort((a, b) => {
      if (b.score !== a.score) return b.score - a.score;
      return b.count - a.count;
    })
    .slice(0, limit)
    .map((item, index) => ({ ...item, rank: index + 1 }));
}

// ============================================
// Trend Calculation
// ============================================

type SimpleTrend = 'increasing' | 'stable' | 'decreasing';

function calculateTrend(current: number, previous: number): SimpleTrend {
  if (previous === 0) return 'stable';
  const change = (current - previous) / previous;
  
  if (change > 0.1) return 'increasing';
  if (change < -0.1) return 'decreasing';
  return 'stable';
}

function calculateRollingAverage(values: number[], window = 7): number {
  if (values.length === 0) return 0;
  const slice = values.slice(-window);
  return slice.reduce((sum, v) => sum + v, 0) / slice.length;
}

function calculatePercentChange(current: number, previous: number): number {
  if (previous === 0) return current > 0 ? 100 : 0;
  return ((current - previous) / previous) * 100;
}

// ============================================
// Data Sanitization
// ============================================

interface Hotspot {
  country: string;
  countryCode: string;
  lat: number;
  lon: number;
  riskScore: number;
  eventCount: number;
}

function sanitizeHotspot(raw: Partial<Hotspot>): Hotspot | null {
  if (!raw.country || !raw.countryCode) return null;
  
  return {
    country: raw.country,
    countryCode: raw.countryCode,
    lat: raw.lat ?? 0,
    lon: raw.lon ?? 0,
    riskScore: Math.min(100, Math.max(0, raw.riskScore ?? 0)),
    eventCount: Math.max(0, raw.eventCount ?? 0),
  };
}

function filterValidHotspots(hotspots: Partial<Hotspot>[]): Hotspot[] {
  return hotspots
    .map(sanitizeHotspot)
    .filter((h): h is Hotspot => h !== null);
}

// ============================================
// String Utilities
// ============================================

function truncate(str: string, maxLen: number): string {
  if (!str) return '';
  return str.length > maxLen ? str.slice(0, maxLen - 3) + '...' : str;
}

function slugify(str: string): string {
  return str
    .toLowerCase()
    .replace(/[^\w\s-]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .trim();
}

// ============================================
// Date Utilities
// ============================================

function formatRelativeTime(date: Date): string {
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);

  if (diffMins < 1) return 'just now';
  if (diffMins < 60) return `${diffMins}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays < 7) return `${diffDays}d ago`;
  return date.toLocaleDateString();
}

export {
  aggregateCategories,
  categoriesToBreakdown,
  rankItems,
  calculateTrend,
  calculateRollingAverage,
  calculatePercentChange,
  sanitizeHotspot,
  filterValidHotspots,
  truncate,
  slugify,
  formatRelativeTime,
};
```

## Usage Examples

### API Route

```typescript
// api/dashboard/route.ts
import { 
  aggregateCategories, 
  rankItems, 
  filterValidHotspots 
} from '@/lib/transformers';

export async function GET() {
  const rawData = await fetchFromDatabase();
  
  return Response.json({
    categories: aggregateCategories(rawData.predictions),
    topHotspots: rankItems(filterValidHotspots(rawData.hotspots), 5),
    trend: calculateTrend(rawData.todayCount, rawData.yesterdayCount),
  });
}
```

### Dashboard Component

```typescript
const breakdown = categoriesToBreakdown(
  currentTotals,
  previousTotals
);

// Returns:
// [
//   { category: 'MILITARY', count: 150, percentage: 0.45, trend: 'increasing' },
//   { category: 'POLITICAL', count: 100, percentage: 0.30, trend: 'stable' },
//   ...
// ]
```

## Best Practices

1. One file for all transformers - easy to find and test
2. Pure functions - no side effects, predictable output
3. Handle edge cases - empty arrays, missing fields, null values
4. Type safety - use TypeScript generics where appropriate
5. Export from types package - share across frontend and backend

## Common Mistakes

- Scattering transformation logic across routes
- Not handling edge cases (empty arrays, null values)
- Mutating input data instead of returning new objects
- Missing type guards for nullable returns
- Not testing transformers in isolation

## Related Patterns

- api-client - Use transformers in API responses
- validation-quarantine - Validate before transforming
- snapshot-aggregation - Aggregate data for dashboards
