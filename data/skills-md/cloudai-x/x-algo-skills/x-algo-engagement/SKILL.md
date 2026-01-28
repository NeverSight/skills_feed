---
name: x-algo-engagement
description: Reference for X algorithm engagement types and signals. Use when analyzing engagement metrics, action predictions, or understanding what signals the algorithm tracks.
---

# X Algorithm Engagement Signals

The X recommendation algorithm tracks **18 engagement action types** plus **1 continuous metric**. These are predicted by the Phoenix ML model and used to calculate weighted scores.

## PhoenixScores Struct

Defined in `home-mixer/candidate_pipeline/candidate.rs`:

```rust
pub struct PhoenixScores {
    // Positive engagement signals
    pub favorite_score: Option<f64>,
    pub reply_score: Option<f64>,
    pub retweet_score: Option<f64>,
    pub quote_score: Option<f64>,
    pub share_score: Option<f64>,
    pub share_via_dm_score: Option<f64>,
    pub share_via_copy_link_score: Option<f64>,
    pub follow_author_score: Option<f64>,

    // Engagement metrics
    pub photo_expand_score: Option<f64>,
    pub click_score: Option<f64>,
    pub profile_click_score: Option<f64>,
    pub vqv_score: Option<f64>,              // Video Quality View
    pub dwell_score: Option<f64>,
    pub quoted_click_score: Option<f64>,

    // Negative signals
    pub not_interested_score: Option<f64>,
    pub block_author_score: Option<f64>,
    pub mute_author_score: Option<f64>,
    pub report_score: Option<f64>,

    // Continuous actions
    pub dwell_time: Option<f64>,
}
```

## Action Types by Category

### Positive Engagement (High Value)

| Action            | Proto Name                | Description                         |
| ----------------- | ------------------------- | ----------------------------------- |
| **Favorite**      | `ServerTweetFav`          | User likes the post                 |
| **Reply**         | `ServerTweetReply`        | User replies to the post            |
| **Retweet**       | `ServerTweetRetweet`      | User reposts without comment        |
| **Quote**         | `ServerTweetQuote`        | User reposts with their own comment |
| **Follow Author** | `ClientTweetFollowAuthor` | User follows the post's author      |

### Sharing Actions

| Action                  | Proto Name                             | Description                          |
| ----------------------- | -------------------------------------- | ------------------------------------ |
| **Share**               | `ClientTweetShare`                     | Generic share action                 |
| **Share via DM**        | `ClientTweetClickSendViaDirectMessage` | User shares via direct message       |
| **Share via Copy Link** | `ClientTweetShareViaCopyLink`          | User copies link to share externally |

### Engagement Metrics

| Action            | Proto Name                    | Description                                                     |
| ----------------- | ----------------------------- | --------------------------------------------------------------- |
| **Photo Expand**  | `ClientTweetPhotoExpand`      | User expands photo to view                                      |
| **Click**         | `ClientTweetClick`            | User clicks on the post                                         |
| **Profile Click** | `ClientTweetClickProfile`     | User clicks author's profile                                    |
| **VQV**           | `ClientTweetVideoQualityView` | Video Quality View - user watches video for meaningful duration |
| **Dwell**         | `ClientTweetRecapDwelled`     | User dwells (pauses) on the post                                |
| **Quoted Click**  | `ClientQuotedTweetClick`      | User clicks on a quoted post                                    |

### Negative Signals

| Action             | Proto Name                   | Description                  |
| ------------------ | ---------------------------- | ---------------------------- |
| **Not Interested** | `ClientTweetNotInterestedIn` | User marks as not interested |
| **Block Author**   | `ClientTweetBlockAuthor`     | User blocks the author       |
| **Mute Author**    | `ClientTweetMuteAuthor`      | User mutes the author        |
| **Report**         | `ClientTweetReport`          | User reports the post        |

### Continuous Actions

| Action         | Proto Name  | Description                                  |
| -------------- | ----------- | -------------------------------------------- |
| **Dwell Time** | `DwellTime` | Continuous value: seconds spent viewing post |

## How Scores Are Obtained

The `PhoenixScorer` (`home-mixer/scorers/phoenix_scorer.rs`) calls the Phoenix prediction service:

1. **Input**: User history + candidate posts
2. **Output**: Log probabilities for each action type per candidate
3. **Conversion**: `probability = exp(log_prob)`

```rust
fn extract_phoenix_scores(&self, p: &ActionPredictions) -> PhoenixScores {
    PhoenixScores {
        favorite_score: p.get(ActionName::ServerTweetFav),
        reply_score: p.get(ActionName::ServerTweetReply),
        retweet_score: p.get(ActionName::ServerTweetRetweet),
        // ... maps each action to its probability
    }
}
```

## Signal Interpretation

- **Scores are probabilities** (0.0 to 1.0): P(user takes action | user sees post)
- **Higher = more likely**: A `favorite_score` of 0.15 means 15% predicted chance of like
- **Negative signals have negative weights**: High `report_score` reduces overall ranking
- **VQV requires minimum video duration**: Only applies to videos > `MIN_VIDEO_DURATION_MS`

## Related Skills

- `/x-algo-scoring` - How these signals are combined into a weighted score
- `/x-algo-ml` - How Phoenix model predicts these probabilities
