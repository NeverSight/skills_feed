---
name: market-sentiment
description: Aggregate news from popular cryptocurrency RSS feeds, analyze sentiment of articles, and calculate an overall market sentiment score with detailed explanation. Use when assessing crypto market sentiment for trading decisions, research, or monitoring trends from RSS sources.
---

# Crypto Market Sentiment

## Overview

This skill enables aggregation of news from popular cryptocurrency RSS feeds, performs sentiment analysis on the articles, and computes a market sentiment score ranging from -1 (highly negative) to +1 (highly positive), along with evidence-based explanations.

## Workflow

Follow these steps to analyze crypto market sentiment:

1. **Select RSS Feeds**: Choose popular crypto RSS feeds (see references/rss_feeds.md for a curated list).
2. **Fetch News**: Retrieve recent articles from the selected feeds.
3. **Analyze Sentiment**: Classify each article's sentiment as positive (+1), negative (-1), or neutral (0) based on content keywords and context.
4. **Calculate Score**: Compute the average sentiment score across all articles.
5. **Generate Explanation**: Provide evidence from the news items supporting the score.

## Sentiment Classification Guidelines

- **Positive (+1)**: News about adoption, launches, partnerships, ETF approvals, price rallies, regulatory wins, or technological breakthroughs.
- **Negative (-1)**: News about hacks, crashes, regulatory crackdowns, liquidations, delays, or criticisms.
- **Neutral (0)**: Factual updates, mixed outcomes, or speculative content without clear bias.

## Output Format

The skill outputs:
- **Sentiment Score**: Numerical value between -1 and 1.
- **Explanation**: Breakdown by feed/source, key positive/negative drivers, and overall market implications.

## Resources

### scripts/
- `sentiment_analyzer.py`: Python script to fetch RSS feeds, parse articles, and compute sentiment score. Run with `python sentiment_analyzer.py` to get automated results.

### references/
- `rss_feeds.md`: List of popular crypto RSS feeds with URLs and descriptions.
- `sentiment_examples.md`: Examples of sentiment classification for common news types.

