---
name: x-algo-scoring
description: Calculate and explain X algorithm engagement scores. Use when analyzing post ranking, understanding score weights, engagement potential, or why one post ranks higher than another.
---

# X Algorithm Scoring

The X algorithm calculates a **weighted engagement score** for each post by combining predicted probabilities of 18 user actions. This score determines feed ranking.

## Weighted Score Formula

```
Score = Σ(weight × P(action)) for all 18 actions + offset
```

From `home-mixer/scorers/weighted_scorer.rs`:

```rust
fn compute_weighted_score(candidate: &PostCandidate) -> f64 {
    let s: &PhoenixScores = &candidate.phoenix_scores;
    let vqv_weight = Self::vqv_weight_eligibility(candidate);

    let combined_score = Self::apply(s.favorite_score, p::FAVORITE_WEIGHT)
        + Self::apply(s.reply_score, p::REPLY_WEIGHT)
        + Self::apply(s.retweet_score, p::RETWEET_WEIGHT)
        + Self::apply(s.photo_expand_score, p::PHOTO_EXPAND_WEIGHT)
        + Self::apply(s.click_score, p::CLICK_WEIGHT)
        + Self::apply(s.profile_click_score, p::PROFILE_CLICK_WEIGHT)
        + Self::apply(s.vqv_score, vqv_weight)
        + Self::apply(s.share_score, p::SHARE_WEIGHT)
        + Self::apply(s.share_via_dm_score, p::SHARE_VIA_DM_WEIGHT)
        + Self::apply(s.share_via_copy_link_score, p::SHARE_VIA_COPY_LINK_WEIGHT)
        + Self::apply(s.dwell_score, p::DWELL_WEIGHT)
        + Self::apply(s.quote_score, p::QUOTE_WEIGHT)
        + Self::apply(s.quoted_click_score, p::QUOTED_CLICK_WEIGHT)
        + Self::apply(s.dwell_time, p::CONT_DWELL_TIME_WEIGHT)
        + Self::apply(s.follow_author_score, p::FOLLOW_AUTHOR_WEIGHT)
        + Self::apply(s.not_interested_score, p::NOT_INTERESTED_WEIGHT)
        + Self::apply(s.block_author_score, p::BLOCK_AUTHOR_WEIGHT)
        + Self::apply(s.mute_author_score, p::MUTE_AUTHOR_WEIGHT)
        + Self::apply(s.report_score, p::REPORT_WEIGHT);

    Self::offset_score(combined_score)
}
```

## Action Weights by Category

### Positive Weights (Increase Score)

| Action              | Weight Constant              | Signal Type                    |
| ------------------- | ---------------------------- | ------------------------------ |
| Favorite            | `FAVORITE_WEIGHT`            | High value engagement          |
| Reply               | `REPLY_WEIGHT`               | High value engagement          |
| Retweet             | `RETWEET_WEIGHT`             | High value engagement          |
| Quote               | `QUOTE_WEIGHT`               | High value engagement          |
| Follow Author       | `FOLLOW_AUTHOR_WEIGHT`       | Very high value                |
| Share               | `SHARE_WEIGHT`               | Distribution signal            |
| Share via DM        | `SHARE_VIA_DM_WEIGHT`        | Distribution signal            |
| Share via Copy Link | `SHARE_VIA_COPY_LINK_WEIGHT` | Distribution signal            |
| Photo Expand        | `PHOTO_EXPAND_WEIGHT`        | Interest signal                |
| Click               | `CLICK_WEIGHT`               | Interest signal                |
| Profile Click       | `PROFILE_CLICK_WEIGHT`       | Interest signal                |
| VQV                 | `VQV_WEIGHT`                 | Video engagement (conditional) |
| Dwell               | `DWELL_WEIGHT`               | Attention signal               |
| Quoted Click        | `QUOTED_CLICK_WEIGHT`        | Interest signal                |
| Dwell Time          | `CONT_DWELL_TIME_WEIGHT`     | Continuous attention           |

### Negative Weights (Decrease Score)

| Action         | Weight Constant         | Signal Type        |
| -------------- | ----------------------- | ------------------ |
| Not Interested | `NOT_INTERESTED_WEIGHT` | Negative signal    |
| Block Author   | `BLOCK_AUTHOR_WEIGHT`   | Strong negative    |
| Mute Author    | `MUTE_AUTHOR_WEIGHT`    | Strong negative    |
| Report         | `REPORT_WEIGHT`         | Strongest negative |

## VQV Video Eligibility

Video Quality View (VQV) weight only applies if video meets minimum duration:

```rust
fn vqv_weight_eligibility(candidate: &PostCandidate) -> f64 {
    if candidate
        .video_duration_ms
        .is_some_and(|ms| ms > p::MIN_VIDEO_DURATION_MS)
    {
        p::VQV_WEIGHT
    } else {
        0.0  // No VQV contribution for short videos or non-videos
    }
}
```

## Score Offset Logic

Handles negative combined scores to ensure proper ranking:

```rust
fn offset_score(combined_score: f64) -> f64 {
    if p::WEIGHTS_SUM == 0.0 {
        combined_score.max(0.0)
    } else if combined_score < 0.0 {
        // Negative scores get scaled offset
        (combined_score + p::NEGATIVE_WEIGHTS_SUM) / p::WEIGHTS_SUM * p::NEGATIVE_SCORES_OFFSET
    } else {
        // Positive scores just add offset
        combined_score + p::NEGATIVE_SCORES_OFFSET
    }
}
```

## Score Normalization

After weighted scoring, scores are normalized (implementation in `util/score_normalizer.rs`, excluded from open source):

```rust
let weighted_score = Self::compute_weighted_score(c);
let normalized_weighted_score = normalize_score(c, weighted_score);
```

## Additional Scoring Stages

### 1. Author Diversity Scoring

Penalizes multiple posts from the same author to promote variety:

```rust
// From home-mixer/scorers/author_diversity_scorer.rs
fn multiplier(&self, position: usize) -> f64 {
    // First post from author: full score
    // Second post: score × decay_factor
    // Third post: score × decay_factor²
    (1.0 - self.floor) * self.decay_factor.powf(position as f64) + self.floor
}
```

Parameters: `AUTHOR_DIVERSITY_DECAY`, `AUTHOR_DIVERSITY_FLOOR`

### 2. Out-of-Network Scoring

Adjusts scores for posts from accounts user doesn't follow:

```rust
// From home-mixer/scorers/oon_scorer.rs
let updated_score = c.score.map(|base_score| match c.in_network {
    Some(false) => base_score * p::OON_WEIGHT_FACTOR,  // Reduced weight
    _ => base_score,  // Full weight for in-network
});
```

## Example Score Calculation

For a post with these predicted probabilities:

- `favorite_score`: 0.12 (12% chance of like)
- `reply_score`: 0.03 (3% chance of reply)
- `retweet_score`: 0.05 (5% chance of retweet)
- `not_interested_score`: 0.02 (2% chance of negative signal)

```
Weighted Score =
    0.12 × FAVORITE_WEIGHT +
    0.03 × REPLY_WEIGHT +
    0.05 × RETWEET_WEIGHT +
    0.02 × NOT_INTERESTED_WEIGHT (negative) +
    ... + offset
```

## PostCandidate Score Fields

```rust
pub struct PostCandidate {
    pub weighted_score: Option<f64>,  // After WeightedScorer
    pub score: Option<f64>,           // Final score after all scorers
    // ...
}
```

## Related Skills

- `/x-algo-engagement` - Reference for all 18 action types
- `/x-algo-pipeline` - Where scoring fits in the full pipeline
