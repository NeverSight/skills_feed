---
name: snapshot-aggregation
description: Daily compression of time-series data with merge logic for multiple pipeline runs, structured aggregation for dashboards, and storage estimation for capacity planning.
license: MIT
compatibility: TypeScript/JavaScript
metadata:
  category: data-access
  time: 4h
  source: drift-masterguide
---

# Snapshot Aggregation

Daily compression with merge logic and storage estimation for time-series data.

## When to Use This Skill

- Raw event data grows too fast for direct queries
- Need daily snapshots for historical dashboards
- Pipeline runs multiple times per day and needs merge logic
- Want storage estimation for capacity planning

## Core Concepts

Raw event data grows fast. Daily snapshots provide:
- Historical dashboards without querying millions of rows
- 90-day retention with minimal storage (~2-3KB/day)
- Multiple pipeline runs per day that merge correctly
- Storage estimation for capacity planning

Key insight: Multiple runs per day must merge correctly, not overwrite.

## Implementation

### TypeScript

```typescript
interface DailySnapshot {
  snapshotDate: string;           // YYYY-MM-DD
  totalArticles: number;
  totalEvents: number;
  totalClusters: number;
  avgRiskScore: number;
  maxRiskScore: number;
  categoryTotals: Record<string, number>;
  topHotspots: Hotspot[];         // Top 10 by risk
  keyEvents: KeyEvent[];          // Top 20 by risk
  countryStats: Record<string, CountryStats>;
  riskTrend: number;              // vs previous day
  pipelineRuns: number;           // How many runs merged
  createdAt: string;
  updatedAt: string;
}

interface Hotspot {
  country: string;
  countryCode: string;
  lat: number;
  lon: number;
  riskScore: number;
  eventCount: number;
  summary: string;
}

interface KeyEvent {
  id: string;
  title: string;
  country: string;
  riskScore: number;
  timestamp: string;
}

interface CountryStats {
  events: number;
  avgRisk: number;
  maxRisk: number;
  topCategory: string;
}

/**
 * Aggregate pipeline results into a daily snapshot
 */
function aggregateToSnapshot(
  result: PipelineResult,
  rawEvents: RawEvent[] = [],
  date: string = new Date().toISOString().split('T')[0]
): DailySnapshot {
  const { predictions, stats } = result;
  
  // Calculate category totals
  const categoryTotals: Record<string, number> = {};
  for (const pred of predictions) {
    if (pred.categoryCounts) {
      for (const [cat, count] of Object.entries(pred.categoryCounts)) {
        categoryTotals[cat] = (categoryTotals[cat] || 0) + count;
      }
    }
  }
  
  // Extract top 10 hotspots
  const topHotspots: Hotspot[] = predictions
    .slice(0, 10)
    .map(p => ({
      country: getCountryName(p.countryCode),
      countryCode: p.countryCode,
      lat: p.lat,
      lon: p.lon,
      riskScore: p.riskScore,
      eventCount: p.eventCount,
      summary: p.summary,
    }));
  
  // Extract key events (top 20 by risk)
  const keyEvents: KeyEvent[] = rawEvents
    .sort((a, b) => b.riskScore - a.riskScore)
    .slice(0, 20)
    .map(e => ({
      id: e.id,
      title: truncate(e.title, 120),
      country: e.country,
      riskScore: e.riskScore,
      timestamp: new Date().toISOString(),
    }));
  
  // Build country stats
  const countryStats: Record<string, CountryStats> = {};
  for (const pred of predictions) {
    const country = pred.countryCode;
    if (!countryStats[country]) {
      countryStats[country] = {
        events: 0,
        avgRisk: 0,
        maxRisk: 0,
        topCategory: pred.category,
      };
    }
    countryStats[country].events += pred.eventCount;
    countryStats[country].maxRisk = Math.max(
      countryStats[country].maxRisk, 
      pred.riskScore
    );
  }
  
  // Aggregate stats
  const totalEvents = predictions.reduce((sum, p) => sum + p.eventCount, 0);
  const avgRiskScore = predictions.length > 0
    ? Math.round(predictions.reduce((sum, p) => sum + p.riskScore, 0) / predictions.length)
    : 0;
  const maxRiskScore = predictions.length > 0
    ? Math.max(...predictions.map(p => p.riskScore))
    : 0;
  
  return {
    snapshotDate: date,
    totalArticles: stats.totalFetched,
    totalEvents,
    totalClusters: stats.clustersFormed,
    avgRiskScore,
    maxRiskScore,
    categoryTotals,
    topHotspots,
    keyEvents,
    countryStats,
    riskTrend: 0,
    pipelineRuns: 1,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  };
}

/**
 * Merge multiple snapshots from the same day
 */
function mergeSnapshots(
  existing: DailySnapshot, 
  incoming: DailySnapshot
): DailySnapshot {
  // Merge category totals (take max - later run has more complete data)
  const categoryTotals = { ...existing.categoryTotals };
  for (const [cat, count] of Object.entries(incoming.categoryTotals)) {
    categoryTotals[cat] = Math.max(categoryTotals[cat] || 0, count);
  }
  
  // Merge hotspots (keep top 10 by risk, dedupe by location)
  const allHotspots = [...existing.topHotspots, ...incoming.topHotspots];
  const uniqueHotspots = dedupeByKey(
    allHotspots, 
    h => `${h.lat.toFixed(1)},${h.lon.toFixed(1)}`
  );
  const topHotspots = uniqueHotspots
    .sort((a, b) => b.riskScore - a.riskScore)
    .slice(0, 10);
  
  // Merge key events (keep top 20 by risk, dedupe by ID)
  const allEvents = [...existing.keyEvents, ...incoming.keyEvents];
  const uniqueEvents = dedupeByKey(allEvents, e => e.id);
  const keyEvents = uniqueEvents
    .sort((a, b) => b.riskScore - a.riskScore)
    .slice(0, 20);
  
  // Merge country stats (take max values)
  const countryStats = { ...existing.countryStats };
  for (const [country, stats] of Object.entries(incoming.countryStats)) {
    if (!countryStats[country]) {
      countryStats[country] = stats;
    } else {
      countryStats[country] = {
        events: Math.max(countryStats[country].events, stats.events),
        avgRisk: Math.round(
          (countryStats[country].avgRisk + stats.avgRisk) / 2
        ),
        maxRisk: Math.max(countryStats[country].maxRisk, stats.maxRisk),
        topCategory: stats.maxRisk > countryStats[country].maxRisk
          ? stats.topCategory
          : countryStats[country].topCategory,
      };
    }
  }
  
  return {
    ...existing,
    totalArticles: existing.totalArticles + incoming.totalArticles,
    totalEvents: Math.max(existing.totalEvents, incoming.totalEvents),
    totalClusters: Math.max(existing.totalClusters, incoming.totalClusters),
    avgRiskScore: Math.round(
      (existing.avgRiskScore + incoming.avgRiskScore) / 2
    ),
    maxRiskScore: Math.max(existing.maxRiskScore, incoming.maxRiskScore),
    categoryTotals,
    topHotspots,
    keyEvents,
    countryStats,
    pipelineRuns: existing.pipelineRuns + 1,
    updatedAt: new Date().toISOString(),
  };
}

/**
 * Estimate storage size of a snapshot
 */
function estimateSnapshotSize(snapshot: DailySnapshot): number {
  return JSON.stringify(snapshot).length;
}

// Helpers
function truncate(str: string, maxLen: number): string {
  return str.length > maxLen ? str.slice(0, maxLen - 3) + '...' : str;
}

function dedupeByKey<T>(arr: T[], keyFn: (item: T) => string): T[] {
  const seen = new Set<string>();
  return arr.filter(item => {
    const key = keyFn(item);
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}
```

## Usage Examples

### Save Daily Snapshot

```typescript
async function saveDailySnapshot(result: PipelineResult) {
  const today = new Date().toISOString().split('T')[0];
  
  const newSnapshot = aggregateToSnapshot(result, result.rawEvents, today);
  
  // Check for existing snapshot today
  const { data: existing } = await supabase
    .from('daily_snapshots')
    .select('*')
    .eq('snapshot_date', today)
    .single();
  
  if (existing) {
    // Merge with existing
    const merged = mergeSnapshots(existing, newSnapshot);
    await supabase
      .from('daily_snapshots')
      .update(merged)
      .eq('snapshot_date', today);
  } else {
    // Insert new
    await supabase
      .from('daily_snapshots')
      .insert(newSnapshot);
  }
  
  console.log(`Snapshot size: ${estimateSnapshotSize(newSnapshot)} bytes`);
}
```

### Database Schema

```sql
CREATE TABLE daily_snapshots (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  snapshot_date DATE UNIQUE NOT NULL,
  total_articles INTEGER DEFAULT 0,
  total_events INTEGER DEFAULT 0,
  avg_risk_score INTEGER DEFAULT 0,
  max_risk_score INTEGER DEFAULT 0,
  category_totals JSONB DEFAULT '{}',
  top_hotspots JSONB DEFAULT '[]',
  key_events JSONB DEFAULT '[]',
  country_stats JSONB DEFAULT '{}',
  pipeline_runs INTEGER DEFAULT 1,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_snapshots_date ON daily_snapshots(snapshot_date DESC);
```

## Best Practices

1. Structured aggregation - Not just counts, but top-N lists and breakdowns
2. Merge logic - Multiple runs per day combine correctly
3. Deduplication - Hotspots/events dedupe by key before merging
4. Storage estimation - Track size for capacity planning
5. Retention policy - Auto-cleanup old snapshots (90 days)

## Common Mistakes

- Simple daily counts (lose detail for dashboards)
- Overwriting on multiple runs (lose data)
- No deduplication in merge (duplicate hotspots)
- Unbounded arrays (memory issues)
- No retention policy (storage grows forever)

## Related Patterns

- batch-processing - Process events before aggregation
- geographic-clustering - Cluster events for hotspots
- checkpoint-resume - Track which data has been aggregated
