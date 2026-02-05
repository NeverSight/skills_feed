---
name: slop-score
description: Analyzes text files for AI-generated writing patterns and returns JSON metrics. Run on drafts or essays to detect overused AI patterns like slop words, contrast structures, and suspicious trigrams. Use when checking writing for AI-like patterns or when asked to score a file for slop.
allowed-tools: Bash(bun *)
---

# Slop Score Analysis

Analyzes text for statistical patterns common in AI-generated writing.

## Usage

Run the analysis script on any text file:

```bash
bun run ./scripts/slop-score/analyze.js --all <filepath>
```

Always use the `--all` flag to include complete metrics.

## Output

Return the raw JSON output exactly as received. Do not summarize, interpret, or add commentary. The JSON output is the complete result.

### JSON Structure

```json
{
  "file": "path/to/file.md",
  "total_chars": 13548,
  "total_words": 2116,
  "slop_score": 6.26,
  "metrics": {
    "slop_words_per_1k": 3.31,
    "slop_trigrams_per_1k": 0,
    "ngram_repetition_score": 124.6,
    "not_x_but_y_per_1k_chars": 0.29,
    "lexical_diversity": {
      "mattr_500": 0.50,
      "type_token_ratio": 0.31,
      "unique_words": 654,
      "total_words": 2116
    },
    "vocab_level": 6.08,
    "avg_sentence_length": 9.97,
    "avg_paragraph_length": 24.43,
    "dialogue_frequency": 0.96
  },
  "slop_word_hits": [["paradoxically", 1], ["fundamentally", 1]],
  "slop_trigram_hits": [],
  "contrast_matches": [
    {
      "pattern_name": "S1_RE_NOT_DASH",
      "sentence": "The phone was not just a device-it was an extension of its owner.",
      "match_text": "not just a device-it was",
      "sentence_count": 1
    }
  ],
  "top_over_represented": {
    "words": [{"word": "flickered", "ratio": 5756.12, "count": 42}],
    "bigrams": [{"phrase": "heavier like", "ratio": 7364.33, "count": 5}],
    "trigrams": [{"phrase": "story it's epic", "ratio": 3058.81, "count": 3}]
  }
}
```

## Calibration Reference

Lower scores indicate more human-like writing:
- Human baseline: ~10
- Claude Sonnet 4.5: ~20
- GPT-4o: ~upper 40s
- Gemini 2.5 Flash: ~upper 70s
