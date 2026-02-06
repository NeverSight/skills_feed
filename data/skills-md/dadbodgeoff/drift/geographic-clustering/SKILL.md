---
name: geographic-clustering
description: Grid-based geographic clustering with O(n) performance, medoid finding for map markers, and multi-factor risk scoring from event density, sentiment, and recency.
license: MIT
compatibility: TypeScript/JavaScript
metadata:
  category: data-access
  time: 5h
  source: drift-masterguide
---

# Geographic Clustering

Grid-based clustering with medoid finding and risk scoring from event density.

## When to Use This Skill

- Clustering thousands of geo-located events for visualization
- Need O(n) performance instead of O(n²) distance-based clustering
- Want actual data points as map markers (medoids, not synthetic centroids)
- Calculating risk scores from cluster characteristics

## Core Concepts

Grid-based clustering is much faster than distance-based algorithms:
- O(n) grouping by grid cell vs O(n²) for distance-based
- Medoid finding gives actual data point as center (better for map markers)
- Multi-factor risk scoring combines density, sentiment, and recency

## Implementation

### TypeScript

```typescript
interface ProcessedEvent {
  id: string;
  lat?: number;
  lon?: number;
  sentiment: number;
  seenDate: Date;
  sourceCountry: string;
}

interface Cluster {
  id: string;
  events: ProcessedEvent[];
  centroidLat: number;
  centroidLon: number;
  countryCode: string;
}

interface RiskPrediction {
  id: string;
  lat: number;
  lon: number;
  riskScore: number;
  sentiment: number;
  eventCount: number;
  topSignals: string[];
  summary: string;
  countryCode: string;
}

// Grid cell size in degrees (~100km at equator)
const GRID_SIZE = 1.0;

/**
 * Generate grid cell key for coordinates
 */
function getGridKey(lat: number, lon: number): string {
  const gridLat = Math.floor(lat / GRID_SIZE) * GRID_SIZE;
  const gridLon = Math.floor(lon / GRID_SIZE) * GRID_SIZE;
  return `${gridLat},${gridLon}`;
}

/**
 * Cluster events by geographic grid - O(n) complexity
 */
function clusterEvents(
  events: ProcessedEvent[], 
  minClusterSize: number = 3
): Cluster[] {
  const grid = new Map<string, ProcessedEvent[]>();

  // O(n) grouping by grid cell
  for (const event of events) {
    if (event.lat === undefined || event.lon === undefined) continue;
    
    const key = getGridKey(event.lat, event.lon);
    if (!grid.has(key)) {
      grid.set(key, []);
    }
    grid.get(key)!.push(event);
  }

  // Convert grid cells to clusters
  const clusters: Cluster[] = [];
  let clusterId = 1;

  for (const [key, clusterEvents] of grid) {
    if (clusterEvents.length < minClusterSize) continue;

    const centroidLat = clusterEvents.reduce((sum, e) => sum + (e.lat || 0), 0) 
                        / clusterEvents.length;
    const centroidLon = clusterEvents.reduce((sum, e) => sum + (e.lon || 0), 0) 
                        / clusterEvents.length;

    clusters.push({
      id: `cluster-${clusterId++}`,
      events: clusterEvents,
      centroidLat,
      centroidLon,
      countryCode: getDominantCountry(clusterEvents),
    });
  }

  return clusters;
}

/**
 * Find the medoid (most central actual point) in a cluster
 */
function findMedoid(events: ProcessedEvent[]): ProcessedEvent {
  if (events.length === 0) throw new Error('Cannot find medoid of empty cluster');
  if (events.length === 1) return events[0];

  const centroidLat = events.reduce((sum, e) => sum + (e.lat || 0), 0) / events.length;
  const centroidLon = events.reduce((sum, e) => sum + (e.lon || 0), 0) / events.length;

  let medoid = events[0];
  let minDist = Infinity;

  for (const event of events) {
    const dist = Math.hypot(
      (event.lat || 0) - centroidLat, 
      (event.lon || 0) - centroidLon
    );
    if (dist < minDist) {
      minDist = dist;
      medoid = event;
    }
  }

  return medoid;
}

/**
 * Get most common country code in cluster
 */
function getDominantCountry(events: ProcessedEvent[]): string {
  const counts: Record<string, number> = {};
  
  for (const event of events) {
    const country = event.sourceCountry || 'XX';
    counts[country] = (counts[country] || 0) + 1;
  }

  let maxCount = 0;
  let dominant = 'XX';
  
  for (const [country, count] of Object.entries(counts)) {
    if (count > maxCount) {
      maxCount = count;
      dominant = country;
    }
  }

  return dominant;
}

/**
 * Calculate risk score for a cluster (0-100)
 * Multi-factor: density + sentiment + recency
 */
function calculateRiskScore(cluster: Cluster): number {
  const eventCount = cluster.events.length;
  const avgSentiment = cluster.events.reduce((sum, e) => sum + e.sentiment, 0) 
                       / eventCount;

  // Factor 1: Event density (0-40 points)
  const eventFactor = Math.min(eventCount / 300, 1) * 40;

  // Factor 2: Sentiment (0-30 points)
  const sentimentFactor = Math.abs(Math.min(avgSentiment, 0)) * 30;

  // Factor 3: Recency (0-30 points)
  const now = Date.now();
  const avgAge = cluster.events.reduce((sum, e) => {
    return sum + (now - e.seenDate.getTime());
  }, 0) / eventCount;
  const hoursOld = avgAge / (1000 * 60 * 60);
  const recencyFactor = Math.max(0, 30 - hoursOld);

  const total = eventFactor + sentimentFactor + recencyFactor;
  return Math.round(Math.min(100, Math.max(0, total)));
}

/**
 * Convert clusters to risk predictions for API/UI
 */
function clustersToPredictions(clusters: Cluster[]): RiskPrediction[] {
  const predictions: RiskPrediction[] = [];

  for (const cluster of clusters) {
    const medoid = findMedoid(cluster.events);
    const riskScore = calculateRiskScore(cluster);
    const avgSentiment = cluster.events.reduce((sum, e) => sum + e.sentiment, 0) 
                         / cluster.events.length;

    const riskLevel = riskScore >= 80 ? 'Critical' 
                    : riskScore >= 60 ? 'High' 
                    : riskScore >= 40 ? 'Moderate' 
                    : 'Low';

    predictions.push({
      id: cluster.id,
      lat: medoid.lat || cluster.centroidLat,
      lon: medoid.lon || cluster.centroidLon,
      riskScore,
      sentiment: avgSentiment,
      eventCount: cluster.events.length,
      topSignals: generateSignals(cluster, riskScore),
      summary: `${riskLevel} risk in ${cluster.countryCode}: ${cluster.events.length} events`,
      countryCode: cluster.countryCode,
    });
  }

  return predictions.sort((a, b) => b.riskScore - a.riskScore);
}

function generateSignals(cluster: Cluster, riskScore: number): string[] {
  const signals: string[] = [];
  const avgSentiment = cluster.events.reduce((sum, e) => sum + e.sentiment, 0) 
                       / cluster.events.length;

  signals.push(`${cluster.events.length} events`);

  if (avgSentiment < -0.5) signals.push('Very negative tone');
  else if (avgSentiment < -0.2) signals.push('Negative tone');

  if (riskScore >= 80) signals.push('Critical risk');
  else if (riskScore >= 60) signals.push('High risk');

  return signals.slice(0, 3);
}
```

## Usage Examples

### Basic Clustering Pipeline

```typescript
async function processEvents() {
  const events = await fetchEvents();
  
  // Cluster geographically (min 3 events per cluster)
  const clusters = clusterEvents(events, 3);
  
  // Convert to predictions for map
  const predictions = clustersToPredictions(clusters);
  
  // Return top 50 for visualization
  return predictions.slice(0, 50);
}
```

## Best Practices

1. Grid-based O(n) - Much faster than distance-based for large datasets
2. Medoid vs Centroid - Use actual data point for map markers (won't be in ocean)
3. Multi-factor risk - Combine density, sentiment, and recency
4. Minimum cluster size - Filter noise with threshold (3+ events)
5. Configurable parameters - Make grid size and thresholds adjustable

## Common Mistakes

- Distance-based clustering on large datasets (O(n²) is too slow)
- Synthetic centroids for map markers (may be in invalid locations)
- Single-factor risk scoring (misses nuance)
- No minimum cluster size (noise becomes clusters)
- Hardcoded risk thresholds (should be configurable)

## Related Patterns

- deduplication - Deduplicate events before clustering
- batch-processing - Process clusters efficiently
- snapshot-aggregation - Aggregate cluster data for dashboards
