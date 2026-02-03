---
name: streaming-recommendations
description: Recommends movies and TV shows to watch on streaming services. Gives 3-5 curated picks based on genre, mood, format, and streaming platform. Use when the user asks what to watch, wants streaming recommendations, or needs help picking a movie or show.
metadata:
  version: "1.0"
  author: adamcobb
  tags:
    - entertainment
    - streaming
    - recommendations
---

# Streaming Recommendations

Recommend 3-5 movies or TV shows to watch on streaming services, tailored to the user's genre, mood, format preference, and available platforms.

## When to Use

- User asks "what should I watch?"
- User wants movie or TV show recommendations
- User mentions streaming services and wants suggestions
- User describes a mood or genre and wants entertainment picks

## Process

### Step 1: Parse the Request

Extract any preferences the user already provided. Look for these four dimensions:

| Dimension | Examples |
|-----------|---------|
| **Format** | Movie, TV show, or either |
| **Genre** | Action, comedy, sci-fi, drama, horror, thriller, documentary, animation, romance, fantasy, mystery, crime |
| **Streaming service** | Netflix, Hulu, Disney+, HBO Max, Prime Video, Apple TV+, Peacock, Paramount+, Tubi, or "any" |
| **Mood / vibe** | Light & fun, intense & gripping, thought-provoking, heartwarming, dark & gritty, nostalgic, suspenseful |

### Step 2: Ask What's Missing

If any of the four dimensions are missing, ask **one multiple-choice question at a time** in this priority order. Skip any dimension already provided:

1. **Format** — "Are you in the mood for a movie or a TV show?"
   - Movie
   - TV show
   - Either is fine

2. **Genre** — "What genre sounds good?"
   - Action / Adventure
   - Comedy
   - Drama
   - Sci-Fi / Fantasy
   - Horror / Thriller
   - Documentary
   - Surprise me

3. **Streaming service** — "Which service are you watching on?"
   - Netflix
   - Hulu / Disney+
   - HBO Max
   - Prime Video
   - Apple TV+
   - Peacock / Paramount+
   - Any / I have them all

4. **Mood** — "What vibe are you going for?"
   - Light & fun
   - Intense & gripping
   - Thought-provoking
   - Heartwarming
   - Dark & gritty
   - Surprise me

If the user provides all four upfront (e.g., "recommend a funny movie on Netflix, something light"), skip straight to Step 3.

"Surprise me" on genre or mood means pick freely — lean toward highly-rated or trending picks.

### Step 3: Search for Recommendations

**Always use web search** to find current recommendations. Streaming catalogs change constantly — never rely solely on training data.

Build search queries combining the user's filters:
- Example: `"best light comedy movies on Netflix 2026"`
- Example: `"top intense sci-fi TV shows on HBO Max 2026"`

Search 2-3 queries to cross-reference availability and find quality picks. Prioritize:
- Currently available on the specified service (verify availability)
- Well-rated (IMDb 7.0+ or Rotten Tomatoes 75%+)
- Mix of well-known and lesser-known titles for variety
- Matches the stated mood/vibe, not just the genre

### Step 4: Present as Rich Cards

Return **3-5 recommendations** using this format for each:

```
### {emoji} Title (Year)
**Genre:** Genre1, Genre2 | **Rating:** Score (Source)
**Streaming on:** Service Name

Synopsis in 2-3 sentences. Spoiler-free. Written to sell the vibe, not just
summarize the plot. Make it compelling.

**Why you'll like it:** One sentence connecting this pick back to the user's
stated mood and preferences.
```

**Formatting rules:**
- Use `🎬` for movies, `📺` for TV shows
- Rating from IMDb (e.g., "8.2 IMDb") or Rotten Tomatoes (e.g., "94% RT") — whichever the search surfaces
- Synopsis: 2-3 sentences, spoiler-free, emphasize tone and vibe over plot details
- "Why you'll like it": Directly reference the user's mood or preferences — this is what makes it feel personal

### Example Output

> **You asked for:** An intense sci-fi TV show on Netflix
>
> ### 📺 3 Body Problem (2024)
> **Genre:** Sci-Fi, Mystery | **Rating:** 7.7 IMDb
> **Streaming on:** Netflix
>
> A mystery that spans decades and continents as a group of brilliant scientists confront the greatest threat in humanity's history. The stakes escalate relentlessly, blending real physics with jaw-dropping sci-fi concepts.
>
> **Why you'll like it:** You wanted intense and gripping — this one doesn't let you breathe from the first episode.
>
> ---
>
> ### 📺 Silo (2023)
> **Genre:** Sci-Fi, Drama | **Rating:** 8.0 IMDb
> **Streaming on:** Apple TV+
>
> In a ruined and toxic future, thousands live in a giant underground silo. When the sheriff investigates what's outside, she uncovers shocking truths that could destroy the community.
>
> **Why you'll like it:** Slow-burn intensity that builds and builds — perfect for that edge-of-your-seat craving.

## Key Principles

- **Always search the web** — streaming catalogs change; never guess availability
- **One question at a time** — don't overwhelm with multiple questions
- **Personalize the "why"** — tie every recommendation back to what the user asked for
- **Spoiler-free always** — never reveal plot twists or endings
- **Variety matters** — mix popular and under-the-radar picks
- **Verify availability** — if unsure a title is on the stated service, say so
- **One and done** — present the picks and let the user take it from there; don't prompt for follow-up
