---
name: x-algo-pipeline
description: Explain the complete X recommendation algorithm pipeline. Use when users ask how posts are ranked, how the algorithm works, or want an overview of the recommendation system.
---

# X Algorithm Pipeline

The X recommendation algorithm processes posts through an **8-stage pipeline** to generate the "For You" feed. Each stage transforms, filters, or scores the candidate posts.

## Pipeline Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         X RECOMMENDATION PIPELINE                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   User Request                                                              │
│        │                                                                    │
│        ▼                                                                    │
│   ┌─────────────┐                                                           │
│   │ 1. Query    │  Hydrate user features, action history, socialgraph       │
│   │   Hydration │                                                           │
│   └──────┬──────┘                                                           │
│          ▼                                                                  │
│   ┌─────────────┐  Thunder (in-network) + Phoenix (out-of-network)          │
│   │ 2. Sources  │  In-network: Posts from followed accounts                 │
│   │             │  Out-of-network: ML retrieval from all posts              │
│   └──────┬──────┘                                                           │
│          ▼                                                                  │
│   ┌─────────────┐                                                           │
│   │ 3. Candidate│  Fetch tweet text, author data, visibility status         │
│   │   Hydration │                                                           │
│   └──────┬──────┘                                                           │
│          ▼                                                                  │
│   ┌─────────────┐                                                           │
│   │ 4. Pre-Score│  Age, duplicates, safety, blocked authors                 │
│   │   Filtering │                                                           │
│   └──────┬──────┘                                                           │
│          ▼                                                                  │
│   ┌─────────────┐  Phoenix ML → WeightedScorer → AuthorDiversity → OON      │
│   │ 5. Scoring  │  Each scorer adds/adjusts candidate.score                 │
│   │             │                                                           │
│   └──────┬──────┘                                                           │
│          ▼                                                                  │
│   ┌─────────────┐                                                           │
│   │ 6. Selection│  TopKScoreSelector: Keep top N by final score             │
│   │             │                                                           │
│   └──────┬──────┘                                                           │
│          ▼                                                                  │
│   ┌─────────────┐                                                           │
│   │ 7. Post-    │  Conversation dedup, previously seen, keywords            │
│   │   Filtering │                                                           │
│   └──────┬──────┘                                                           │
│          ▼                                                                  │
│   ┌─────────────┐                                                           │
│   │ 8. Side     │  Logging, analytics, impression tracking                  │
│   │   Effects   │                                                           │
│   └──────┬──────┘                                                           │
│          ▼                                                                  │
│      Feed Response                                                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Stage Details

### 1. Query Hydration

Enriches the request with user context:

- User features (followed users, blocked users, muted users)
- User action sequence (engagement history for ML)
- Muted keywords
- Subscription status
- Bloom filters for seen posts

### 2. Sources

Two candidate sources provide posts:

#### Thunder Source (In-Network)

```rust
// home-mixer/sources/thunder_source.rs
// Posts from accounts the user follows
served_type: Some(pb::ServedType::ForYouInNetwork)
```

- Queries Thunder service with user's following list
- Returns recent posts from followed accounts
- Includes conversation context (ancestors, reply chains)

#### Phoenix Source (Out-of-Network)

```rust
// home-mixer/sources/phoenix_source.rs
fn enable(&self, query: &ScoredPostsQuery) -> bool {
    !query.in_network_only  // Disabled for "Following" tab
}
served_type: Some(pb::ServedType::ForYouPhoenixRetrieval)
```

- ML-based retrieval using user embedding
- Finds relevant posts from the entire corpus
- Enabled for "For You", disabled for "Following"

### 3. Candidate Hydration

Fetches full post data:

- Tweet text content
- Author information
- Media metadata (video duration)
- Visibility filtering results
- Subscription requirements

### 4. Pre-Score Filtering

Removes ineligible candidates before expensive ML scoring:

- `AgeFilter` - Too old
- `DropDuplicatesFilter` - Duplicate IDs
- `VFFilter` - Safety violations
- `AuthorSocialgraphFilter` - Blocked/muted authors
- `CoreDataHydrationFilter` - Missing data
- `IneligibleSubscriptionFilter` - Subscription required

### 5. Scoring (4 Stages)

#### a) PhoenixScorer

```rust
// home-mixer/scorers/phoenix_scorer.rs
// Calls Phoenix ML to predict engagement probabilities
```

Produces `phoenix_scores` with 18 action probabilities.

#### b) WeightedScorer

```rust
// home-mixer/scorers/weighted_scorer.rs
// Combines probabilities into single score
weighted_score = Σ(weight × P(action))
```

Produces `weighted_score` from action predictions.

#### c) AuthorDiversityScorer

```rust
// home-mixer/scorers/author_diversity_scorer.rs
// Penalizes multiple posts from same author
multiplier = (1 - floor) × decay^position + floor
```

Adjusts scores to promote variety.

#### d) OONScorer

```rust
// home-mixer/scorers/oon_scorer.rs
// Adjusts out-of-network post scores
if !in_network: score *= OON_WEIGHT_FACTOR
```

Balances in-network vs out-of-network content.

### 6. Selection

```rust
// home-mixer/selectors/top_k_score_selector.rs
pub struct TopKScoreSelector;

impl Selector<ScoredPostsQuery, PostCandidate> for TopKScoreSelector {
    fn score(&self, candidate: &PostCandidate) -> f64 {
        candidate.score.unwrap_or(f64::NEG_INFINITY)
    }
    fn size(&self) -> Option<usize> {
        Some(params::TOP_K_CANDIDATES_TO_SELECT)
    }
}
```

Keeps top K posts by final score.

### 7. Post-Score Filtering

Fine-grained filtering after selection:

- `DedupConversationFilter` - One post per conversation
- `RetweetDeduplicationFilter` - One version per underlying post
- `PreviouslySeenPostsFilter` - Remove seen posts
- `PreviouslyServedPostsFilter` - Remove from current session
- `MutedKeywordFilter` - User keyword mutes
- `SelfTweetFilter` - Remove own posts

### 8. Side Effects

Non-blocking operations after response:

- Impression logging
- Analytics events
- Cache updates

## Data Flow Summary

```
Candidates start with:
├── tweet_id, author_id (from Sources)
├── tweet_text, metadata (from Hydration)
├── phoenix_scores (from PhoenixScorer)
├── weighted_score (from WeightedScorer)
├── score (from AuthorDiversity + OON)
└── Final ranking by score
```

## PostCandidate Structure

```rust
pub struct PostCandidate {
    pub tweet_id: i64,
    pub author_id: u64,
    pub tweet_text: String,
    pub in_reply_to_tweet_id: Option<u64>,
    pub retweeted_tweet_id: Option<u64>,
    pub retweeted_user_id: Option<u64>,
    pub phoenix_scores: PhoenixScores,      // ML predictions
    pub weighted_score: Option<f64>,         // After WeightedScorer
    pub score: Option<f64>,                  // Final score
    pub served_type: Option<ServedType>,     // Source type
    pub in_network: Option<bool>,            // Following or not
    pub ancestors: Vec<u64>,                 // Conversation context
    pub video_duration_ms: Option<i32>,      // For VQV eligibility
    pub visibility_reason: Option<FilteredReason>,
    pub subscription_author_id: Option<u64>,
    // ...
}
```

## Source Configuration

| Tab       | Thunder (In-Network) | Phoenix (Out-of-Network) |
| --------- | -------------------- | ------------------------ |
| For You   | Enabled              | Enabled                  |
| Following | Enabled              | Disabled                 |

## Related Skills

- `/x-algo-scoring` - Detailed scoring formula
- `/x-algo-filters` - All filter implementations
- `/x-algo-engagement` - Action types and signals
- `/x-algo-ml` - Phoenix ML model architecture
