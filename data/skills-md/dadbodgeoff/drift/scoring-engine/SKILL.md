---
name: scoring-engine
description: Statistical scoring with z-scores, percentiles, freshness decay, and cross-category normalization. Rank and compare items with confidence scoring.
license: MIT
compatibility: TypeScript/JavaScript, Python
metadata:
  category: data-processing
  time: 6h
  source: drift-masterguide
---

# Scoring Engine

Statistical scoring for ranking and comparing items across categories.

## When to Use This Skill

- Ranking content by performance (views, engagement)
- Comparing items across categories with different baselines
- Need freshness decay for time-sensitive content
- Want confidence scores based on sample size

## Core Concepts

Use percentiles over mean/std for skewed data. Apply freshness decay for older content. Calculate confidence based on sample size. Normalize across categories for fair comparison.


## Implementation

### Python

```python
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import statistics
import math


@dataclass
class CategoryStats:
    """Statistical summary for a category."""
    category_key: str
    sample_count: int
    view_mean: float
    view_std: float
    view_p25: float
    view_p50: float
    view_p75: float
    view_p90: float
    view_min: float
    view_max: float
    outliers_removed: int = 0

    @classmethod
    def from_videos(cls, category_key: str, videos: List[Dict], remove_outliers: bool = True) -> "CategoryStats":
        if not videos:
            return cls._empty(category_key)

        views = [v.get("view_count", 0) for v in videos if v.get("view_count", 0) > 0]
        if not views:
            return cls._empty(category_key)

        outliers_removed = 0
        if remove_outliers and len(views) > 10:
            views, outliers_removed = cls._remove_outliers(views)

        sorted_views = sorted(views)
        n = len(sorted_views)

        return cls(
            category_key=category_key,
            sample_count=len(views),
            view_mean=statistics.mean(views),
            view_std=statistics.stdev(views) if len(views) > 1 else 0,
            view_p25=sorted_views[int(n * 0.25)],
            view_p50=sorted_views[int(n * 0.50)],
            view_p75=sorted_views[int(n * 0.75)],
            view_p90=sorted_views[int(n * 0.90)],
            view_min=min(views),
            view_max=max(views),
            outliers_removed=outliers_removed,
        )

    @staticmethod
    def _remove_outliers(values: List[float]) -> Tuple[List[float], int]:
        """Remove outliers using IQR method."""
        sorted_vals = sorted(values)
        n = len(sorted_vals)
        q1, q3 = sorted_vals[int(n * 0.25)], sorted_vals[int(n * 0.75)]
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        filtered = [v for v in values if lower <= v <= upper]
        return filtered, len(values) - len(filtered)

    @classmethod
    def _empty(cls, category_key: str) -> "CategoryStats":
        return cls(category_key=category_key, sample_count=0, view_mean=0, view_std=1,
                   view_p25=0, view_p50=0, view_p75=0, view_p90=0, view_min=0, view_max=0)


@dataclass
class PercentileThresholds:
    p25: float
    p50: float
    p75: float
    p90: float


def calculate_percentile_score(value: float, thresholds: PercentileThresholds) -> float:
    """Map value to 0-100 score based on percentile thresholds."""
    if value <= 0:
        return 0.0
    if value <= thresholds.p25:
        return 25 * (value / thresholds.p25) if thresholds.p25 > 0 else 0
    elif value <= thresholds.p50:
        return 25 + 25 * ((value - thresholds.p25) / (thresholds.p50 - thresholds.p25))
    elif value <= thresholds.p75:
        return 50 + 25 * ((value - thresholds.p50) / (thresholds.p75 - thresholds.p50))
    elif value <= thresholds.p90:
        return 75 + 15 * ((value - thresholds.p75) / (thresholds.p90 - thresholds.p75))
    else:
        excess = min(value - thresholds.p90, thresholds.p90 * 2)
        return 90 + 10 * (excess / (thresholds.p90 * 2))


def freshness_decay(hours_old: float, half_life: float = 24.0) -> float:
    """Exponential decay: factor = 0.5^(age/half_life)"""
    if hours_old <= 0:
        return 1.0
    return math.pow(0.5, hours_old / half_life)


def recency_boost(hours_old: float, boost_window: float = 6.0) -> float:
    """Extra boost for very fresh content (1.0-1.5)."""
    if hours_old >= boost_window:
        return 1.0
    return 1.5 - (0.5 * hours_old / boost_window)


def calculate_confidence(sample_size: int, score_variance: float = 0.0) -> int:
    """Confidence score (0-100) based on sample size and variance."""
    if sample_size <= 0:
        return 0
    sample_confidence = min(100, 25 * math.log10(sample_size + 1))
    variance_penalty = min(30, score_variance * 10)
    return max(0, min(100, int(sample_confidence - variance_penalty)))
```


```python
def combine_scores(
    scores: Dict[str, float],
    weights: Dict[str, float],
) -> Tuple[float, int]:
    """Combine multiple scores with weights."""
    if not scores:
        return 0.0, 0

    total_weight = 0.0
    weighted_sum = 0.0

    for name, score in scores.items():
        weight = weights.get(name, 1.0)
        weighted_sum += score * weight
        total_weight += weight

    if total_weight == 0:
        return 0.0, 0

    combined = weighted_sum / total_weight
    confidence = calculate_confidence(len(scores) * 10)
    return combined, confidence


class ScoringEngine:
    """Enterprise-grade scoring engine."""

    def __init__(self, redis_client):
        self.redis = redis_client
        self._stats_cache: Dict[str, CategoryStats] = {}

    async def build_category_stats(self, category_key: str, videos: List[Dict]) -> CategoryStats:
        stats = CategoryStats.from_videos(category_key, videos, remove_outliers=True)
        self._stats_cache[category_key] = stats
        return stats

    def score_item(
        self,
        views: int,
        hours_old: float,
        stats: CategoryStats,
    ) -> Tuple[float, int]:
        thresholds = PercentileThresholds(
            p25=stats.view_p25, p50=stats.view_p50,
            p75=stats.view_p75, p90=stats.view_p90,
        )

        view_score = calculate_percentile_score(views, thresholds)
        freshness = freshness_decay(hours_old)
        recency = recency_boost(hours_old)

        # Velocity score
        velocity = views / max(hours_old, 1.0)
        velocity_thresholds = PercentileThresholds(
            p25=stats.view_p25/24, p50=stats.view_p50/24,
            p75=stats.view_p75/24, p90=stats.view_p90/24,
        )
        velocity_score = calculate_percentile_score(velocity, velocity_thresholds)

        # Combine
        scores = {"views": view_score, "velocity": velocity_score}
        weights = {"views": 0.6, "velocity": 0.4}
        combined, confidence = combine_scores(scores, weights)

        final_score = min(100, combined * freshness * recency)
        return final_score, confidence
```

## Usage Examples

```python
engine = ScoringEngine(redis_client)

# Build category stats
videos = await fetch_category_videos("gaming")
stats = await engine.build_category_stats("gaming", videos)

# Score individual items
for video in videos:
    hours_old = (datetime.now() - video["created_at"]).total_seconds() / 3600
    score, confidence = engine.score_item(
        views=video["view_count"],
        hours_old=hours_old,
        stats=stats,
    )
    print(f"{video['title']}: {score:.1f} (confidence: {confidence}%)")
```

## Best Practices

1. Remove outliers before calculating statistics
2. Use percentiles over mean/std for skewed data
3. Apply freshness decay for time-sensitive content
4. Calculate confidence based on sample size
5. Cache category statistics (expensive to compute)

## Common Mistakes

- Using mean/std for highly skewed data
- Not removing outliers (extreme values dominate)
- Forgetting freshness decay (old content ranks too high)
- Ignoring confidence (treating all scores equally)

## Related Patterns

- analytics-pipeline (data collection)
- community-feed (applying scores to feeds)
