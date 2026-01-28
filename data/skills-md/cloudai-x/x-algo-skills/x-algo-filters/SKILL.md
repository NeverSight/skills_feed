---
name: x-algo-filters
description: Explain why posts get filtered from the X feed. Use when analyzing why a post was removed, not shown, or filtered out of recommendations.
---

# X Algorithm Filters

The X algorithm applies **12 filters** to remove posts that shouldn't appear in a user's feed. Filters run at multiple stages of the pipeline.

## Filter Summary

| Filter                         | Purpose                                  | Source File                         |
| ------------------------------ | ---------------------------------------- | ----------------------------------- |
| `AgeFilter`                    | Remove posts older than max age          | `age_filter.rs`                     |
| `PreviouslySeenPostsFilter`    | Remove posts user has seen               | `previously_seen_posts_filter.rs`   |
| `PreviouslyServedPostsFilter`  | Remove posts already served in session   | `previously_served_posts_filter.rs` |
| `DropDuplicatesFilter`         | Remove duplicate tweet IDs               | `drop_duplicates_filter.rs`         |
| `RetweetDeduplicationFilter`   | Remove duplicate retweets                | `retweet_deduplication_filter.rs`   |
| `DedupConversationFilter`      | Keep only best post per conversation     | `dedup_conversation_filter.rs`      |
| `SelfTweetFilter`              | Remove user's own posts                  | `self_tweet_filter.rs`              |
| `AuthorSocialgraphFilter`      | Remove blocked/muted authors             | `author_socialgraph_filter.rs`      |
| `MutedKeywordFilter`           | Remove posts with muted keywords         | `muted_keyword_filter.rs`           |
| `VFFilter`                     | Safety/visibility filtering              | `vf_filter.rs`                      |
| `CoreDataHydrationFilter`      | Remove posts missing required data       | `core_data_hydration_filter.rs`     |
| `IneligibleSubscriptionFilter` | Remove subscription posts user can't see | `ineligible_subscription_filter.rs` |

## Filter Details

### 1. AgeFilter

Removes posts older than a configured maximum age using Snowflake ID timestamp extraction.

```rust
// home-mixer/filters/age_filter.rs
pub struct AgeFilter {
    pub max_age: Duration,
}

fn is_within_age(&self, tweet_id: i64) -> bool {
    snowflake::duration_since_creation_opt(tweet_id)
        .map(|age| age <= self.max_age)
        .unwrap_or(false)
}
```

**Why filtered**: Post is too old. Snowflake IDs encode creation timestamp.

### 2. PreviouslySeenPostsFilter

Uses **Bloom filters** and explicit seen IDs from the client to filter posts the user has already viewed.

```rust
// home-mixer/filters/previously_seen_posts_filter.rs
let (removed, kept) = candidates.into_iter().partition(|c| {
    get_related_post_ids(c).iter().any(|&post_id| {
        query.seen_ids.contains(&post_id)
            || bloom_filters
                .iter()
                .any(|filter| filter.may_contain(post_id))
    })
});
```

**Why filtered**: User has already seen this post (tracked via Bloom filter or explicit ID list).

### 3. PreviouslyServedPostsFilter

Removes posts already served in the current session (for "load more" / infinite scroll).

```rust
// home-mixer/filters/previously_served_posts_filter.rs
fn enable(&self, query: &ScoredPostsQuery) -> bool {
    query.is_bottom_request  // Only for pagination requests
}

// Checks served_ids from request
get_related_post_ids(c).iter().any(|id| query.served_ids.contains(id))
```

**Why filtered**: Post was already served earlier in this session.

### 4. DropDuplicatesFilter

Simple deduplication by tweet ID within the candidate set.

```rust
// home-mixer/filters/drop_duplicates_filter.rs
let mut seen_ids = HashSet::new();
for candidate in candidates {
    if seen_ids.insert(candidate.tweet_id) {
        kept.push(candidate);
    } else {
        removed.push(candidate);
    }
}
```

**Why filtered**: Duplicate tweet ID from multiple sources.

### 5. RetweetDeduplicationFilter

Prevents showing the same underlying post multiple times (as original or as different retweets).

```rust
// home-mixer/filters/retweet_deduplication_filter.rs
match candidate.retweeted_tweet_id {
    Some(retweeted_id) => {
        // Remove if we've already seen this tweet (as original or retweet)
        if seen_tweet_ids.insert(retweeted_id) {
            kept.push(candidate);
        } else {
            removed.push(candidate);
        }
    }
    None => {
        // Mark original tweet ID as seen
        seen_tweet_ids.insert(candidate.tweet_id as u64);
        kept.push(candidate);
    }
}
```

**Why filtered**: Another version of this post (original or retweet) already included.

### 6. DedupConversationFilter

Keeps only the highest-scored post per conversation thread.

```rust
// home-mixer/filters/dedup_conversation_filter.rs
fn get_conversation_id(candidate: &PostCandidate) -> u64 {
    // Conversation root = minimum ancestor ID, or self if no ancestors
    candidate
        .ancestors
        .iter()
        .copied()
        .min()
        .unwrap_or(candidate.tweet_id as u64)
}

// Keeps highest score per conversation_id
```

**Why filtered**: Another post in same conversation thread has higher score.

### 7. SelfTweetFilter

Removes the user's own posts from their "For You" feed.

```rust
// home-mixer/filters/self_tweet_filter.rs
let viewer_id = query.user_id as u64;
let (kept, removed) = candidates
    .into_iter()
    .partition(|c| c.author_id != viewer_id);
```

**Why filtered**: Post authored by the viewing user.

### 8. AuthorSocialgraphFilter

Removes posts from authors the user has blocked or muted.

```rust
// home-mixer/filters/author_socialgraph_filter.rs
let muted = viewer_muted_user_ids.contains(&author_id);
let blocked = viewer_blocked_user_ids.contains(&author_id);
if muted || blocked {
    removed.push(candidate);
}
```

**Why filtered**: Author is in user's blocked or muted list.

### 9. MutedKeywordFilter

Removes posts containing keywords the user has muted.

```rust
// home-mixer/filters/muted_keyword_filter.rs
let tweet_text_token_sequence = self.tokenizer.tokenize(&candidate.tweet_text);
if matcher.matches(&tweet_text_token_sequence) {
    removed.push(candidate);  // Matches muted keywords
}
```

**Why filtered**: Post text contains muted keyword(s).

### 10. VFFilter (Visibility Filtering)

Safety-based filtering using the visibility filtering service.

```rust
// home-mixer/filters/vf_filter.rs
fn should_drop(reason: &Option<FilteredReason>) -> bool {
    match reason {
        Some(FilteredReason::SafetyResult(safety_result)) => {
            matches!(safety_result.action, Action::Drop(_))
        }
        Some(_) => true,
        None => false,
    }
}
```

**Why filtered**: Safety violation detected (spam, abuse, policy violation, etc.).

### 11. CoreDataHydrationFilter

Removes posts that failed to hydrate required data.

```rust
// home-mixer/filters/core_data_hydration_filter.rs
let (kept, removed) = candidates
    .into_iter()
    .partition(|c| c.author_id != 0 && !c.tweet_text.trim().is_empty());
```

**Why filtered**: Missing author ID or empty tweet text (hydration failed).

### 12. IneligibleSubscriptionFilter

Removes subscription-only posts from authors the user isn't subscribed to.

```rust
// home-mixer/filters/ineligible_subscription_filter.rs
let (kept, removed) = candidates.into_iter().partition(|candidate| {
    match candidate.subscription_author_id {
        Some(author_id) => subscribed_user_ids.contains(&author_id),
        None => true,  // Not a subscription post, keep it
    }
});
```

**Why filtered**: Post requires subscription to author, user not subscribed.

## Filter Result Structure

All filters return:

```rust
pub struct FilterResult<T> {
    pub kept: Vec<T>,     // Candidates that passed
    pub removed: Vec<T>,  // Candidates that were filtered out
}
```

## Conditional Filter Enabling

Some filters only run in certain contexts:

```rust
// PreviouslyServedPostsFilter only runs on pagination
fn enable(&self, query: &ScoredPostsQuery) -> bool {
    query.is_bottom_request
}
```

## Bloom Filter Deduplication

`PreviouslySeenPostsFilter` uses Bloom filters for efficient "seen" tracking:

- Client sends Bloom filter entries with request
- Server reconstructs filters via `BloomFilter::from_entry`
- Uses `may_contain()` (probabilistic) for fast lookup
- Falls back to explicit `seen_ids` for definitive checks

## Related Skills

- `/x-algo-pipeline` - Where filters fit in the full pipeline
- `/x-algo-engagement` - Understanding what data filters check against
