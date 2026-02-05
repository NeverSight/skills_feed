---
name: community-feed
description: Social feed with batch queries, cursor pagination, trending algorithms, and engagement tracking. Efficient database queries for infinite scroll feeds.
license: MIT
compatibility: TypeScript/JavaScript, Python
metadata:
  category: data-processing
  time: 6h
  source: drift-masterguide
---

# Community Feed

Social feed with trending algorithms, cursor pagination, and engagement tracking.

## When to Use This Skill

- Building social feeds with infinite scroll
- Need trending/hot content algorithms
- Implementing like/engagement systems
- Want efficient pagination for large datasets

## Core Concepts

Cursor pagination beats offset for large datasets. Batch-load relationships to avoid N+1. Store trending scores as computed columns for efficient sorting.


## Implementation

### Python

```python
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional, List, Dict
import base64
import json


@dataclass
class PaginatedPosts:
    posts: List[Dict]
    total_count: int
    has_more: bool
    next_cursor: Optional[str]


class CommunityFeedService:
    """Service for community feed with cursor pagination."""

    def __init__(self, db):
        self.db = db

    async def get_feed(
        self,
        feed_type: str = "trending",
        viewer_id: Optional[str] = None,
        cursor: Optional[str] = None,
        limit: int = 20,
        tags: Optional[List[str]] = None,
    ) -> PaginatedPosts:
        cursor_data = self._parse_cursor(cursor) if cursor else None

        query = self.db.table("community_posts").select(
            "*",
            "assets!inner(url, asset_type)",
            "users!inner(id, display_name, avatar_url)",
        )

        if tags:
            query = query.contains("tags", tags)

        # Feed-specific ordering
        if feed_type == "following" and viewer_id:
            following = await self._get_following_ids(viewer_id)
            if not following:
                return PaginatedPosts(posts=[], total_count=0, has_more=False, next_cursor=None)
            query = query.in_("user_id", following)

        if feed_type == "trending":
            query = query.order("trending_score", desc=True)
            if cursor_data:
                query = query.lt("trending_score", cursor_data["score"])
        else:
            query = query.order("created_at", desc=True)
            if cursor_data:
                query = query.lt("created_at", cursor_data["created_at"])

        # Fetch one extra to check has_more
        query = query.limit(limit + 1)
        result = query.execute()
        posts = result.data or []

        has_more = len(posts) > limit
        if has_more:
            posts = posts[:limit]

        # Batch load viewer's likes
        if viewer_id and posts:
            liked_ids = await self._get_liked_post_ids(viewer_id, [p["id"] for p in posts])
            for post in posts:
                post["is_liked_by_viewer"] = post["id"] in liked_ids

        next_cursor = None
        if has_more and posts:
            next_cursor = self._generate_cursor(posts[-1], feed_type)

        return PaginatedPosts(
            posts=posts,
            total_count=await self._get_total_count(tags),
            has_more=has_more,
            next_cursor=next_cursor,
        )

    async def _get_following_ids(self, user_id: str) -> List[str]:
        result = self.db.table("user_follows").select("following_id").eq("follower_id", user_id).execute()
        return [r["following_id"] for r in (result.data or [])]

    async def _get_liked_post_ids(self, user_id: str, post_ids: List[str]) -> set:
        result = self.db.table("post_likes").select("post_id").eq("user_id", user_id).in_("post_id", post_ids).execute()
        return {r["post_id"] for r in (result.data or [])}

    def _parse_cursor(self, cursor: str) -> dict:
        try:
            return json.loads(base64.b64decode(cursor).decode())
        except:
            return {}

    def _generate_cursor(self, post: dict, feed_type: str) -> str:
        if feed_type == "trending":
            data = {"score": post.get("trending_score", 0)}
        else:
            data = {"created_at": post["created_at"]}
        return base64.b64encode(json.dumps(data).encode()).decode()
```


```python
# Engagement operations
async def like_post(self, post_id: str, user_id: str) -> bool:
    existing = self.db.table("post_likes").select("id").eq("post_id", post_id).eq("user_id", user_id).execute()
    if existing.data:
        return False  # Already liked

    self.db.table("post_likes").insert({
        "post_id": post_id,
        "user_id": user_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }).execute()

    # Atomic increment
    self.db.rpc("increment_like_count", {"post_id": post_id}).execute()
    return True

async def unlike_post(self, post_id: str, user_id: str) -> bool:
    result = self.db.table("post_likes").delete().eq("post_id", post_id).eq("user_id", user_id).execute()
    if not result.data:
        return False

    self.db.rpc("decrement_like_count", {"post_id": post_id}).execute()
    return True


# Trending algorithm
def calculate_trending_score(
    like_count: int,
    comment_count: int,
    view_count: int,
    created_at: datetime,
    is_featured: bool = False,
) -> float:
    """
    Trending score = engagement / age^decay
    Higher engagement + newer = higher score
    """
    engagement = like_count * 1.0 + comment_count * 2.0 + view_count * 0.1
    age_hours = max((datetime.now(timezone.utc) - created_at).total_seconds() / 3600, 0.1)
    score = engagement / (age_hours ** 1.5)
    return score * 1.5 if is_featured else score
```

### SQL Schema

```sql
CREATE TABLE community_posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    title VARCHAR(200) NOT NULL,
    like_count INTEGER DEFAULT 0,
    comment_count INTEGER DEFAULT 0,
    view_count INTEGER DEFAULT 0,
    is_featured BOOLEAN DEFAULT FALSE,
    tags TEXT[] DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    -- Computed trending score
    trending_score FLOAT GENERATED ALWAYS AS (
        (like_count + comment_count * 2 + view_count * 0.1) / 
        POWER(GREATEST(EXTRACT(EPOCH FROM (NOW() - created_at)) / 3600, 0.1), 1.5)
    ) STORED
);

CREATE INDEX idx_posts_trending ON community_posts(trending_score DESC);
CREATE INDEX idx_posts_created ON community_posts(created_at DESC);

-- Atomic increment functions
CREATE FUNCTION increment_like_count(post_id UUID) RETURNS VOID AS $$
BEGIN UPDATE community_posts SET like_count = like_count + 1 WHERE id = post_id; END;
$$ LANGUAGE plpgsql;
```

## Usage Examples

```python
feed_service = CommunityFeedService(db)

# Get trending feed
result = await feed_service.get_feed(feed_type="trending", viewer_id="user_123", limit=20)
for post in result.posts:
    print(f"{post['title']} - {post['like_count']} likes")

# Load next page
if result.has_more:
    next_page = await feed_service.get_feed(feed_type="trending", cursor=result.next_cursor)

# Like a post
await feed_service.like_post("post_456", "user_123")
```

## Best Practices

1. Use cursor pagination over offset for large datasets
2. Batch-load relationships to avoid N+1 queries
3. Store trending score as computed column for efficient sorting
4. Use atomic database functions for counter updates
5. Cache total counts (expensive to compute)

## Common Mistakes

- Using offset pagination (slow for large offsets)
- N+1 queries for author/like data
- Computing trending score on every query
- Non-atomic counter updates (race conditions)

## Related Patterns

- analytics-pipeline (event tracking)
- intelligent-cache (caching feeds)
