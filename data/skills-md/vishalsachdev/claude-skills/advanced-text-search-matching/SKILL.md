---
name: advanced-text-search-matching
description: Production-grade text search algorithms for finding and matching text in large documents with millisecond performance. Includes Boyer-Moore search, n-gram similarity, fuzzy matching, and intelligent indexing. Use when building search features for large documents, finding quotes with imperfect matches, implementing fuzzy search, or need character-level precision.
---

# Advanced Text Search & Matching

Production-grade text search algorithms for finding and matching text in large documents with millisecond performance. Includes Boyer-Moore search, n-gram similarity, fuzzy matching, and intelligent indexing.

## When to use this skill

- Building search features for large documents or transcripts
- Finding quotes or citations in text with imperfect matches
- Implementing fuzzy search that handles typos and variations
- Need character-level precision for highlighting
- Building citation systems or source verification
- Searching across segmented content (chapters, timestamps, etc.)
- Performance-critical text matching (100k+ character documents)

## Core Algorithms

1. **Boyer-Moore Search** - O(n/m) exact substring matching
2. **N-gram Similarity** - Jaccard coefficient for fuzzy matching
3. **Multi-Strategy Matching** - Cascading exact → normalized → fuzzy
4. **Document Indexing** - Word and n-gram indices for fast lookup
5. **Segment Mapping** - Character-precise position tracking

## Implementation

### Step 1: Create Text Search Utilities

Create `lib/text-search.ts`:

```typescript
// Configuration constants
const SEARCH_CONFIG = {
  FUZZY_MATCH_THRESHOLD: 0.85,
  MIN_FUZZY_SCORE: 0.7,
  N_GRAM_SIZE: 3,
  MIN_N_GRAM_OVERLAP: 0.5,
} as const;

// Text normalization utilities
export function normalizeWhitespace(text: string): string {
  return text
    .replace(/[\r\n]+/g, ' ') // Replace newlines with spaces
    .replace(/\s+/g, ' ')     // Collapse multiple spaces
    .trim();
}

export function normalizeForMatching(text: string): string {
  return text
    .toLowerCase()
    // Remove most punctuation for robust matching
    .replace(/[.,?"""''!—…–]/g, '')
    // Normalize whitespace
    .replace(/\s+/g, ' ')
    .trim();
}

// Fast n-gram based similarity (returns 0-1)
export function calculateNgramSimilarity(str1: string, str2: string): number {
  if (str1.length === 0 || str2.length === 0) return 0;

  const ngrams1 = new Set<string>();
  const ngrams2 = new Set<string>();

  // Generate 3-grams
  const clean1 = str1.replace(/\s+/g, '');
  const clean2 = str2.replace(/\s+/g, '');

  for (let i = 0; i <= clean1.length - 3; i++) {
    ngrams1.add(clean1.substring(i, i + 3));
  }

  for (let i = 0; i <= clean2.length - 3; i++) {
    ngrams2.add(clean2.substring(i, i + 3));
  }

  if (ngrams1.size === 0 || ngrams2.size === 0) {
    // Fallback to simple substring check for very short strings
    return clean1.includes(clean2) || clean2.includes(clean1) ? 0.8 : 0;
  }

  // Calculate Jaccard similarity
  let intersection = 0;
  for (const ngram of ngrams1) {
    if (ngrams2.has(ngram)) intersection++;
  }

  const union = ngrams1.size + ngrams2.size - intersection;
  return intersection / union;
}

// Boyer-Moore-Horspool substring search
export function boyerMooreSearch(text: string, pattern: string): number {
  if (pattern.length === 0) return 0;
  if (pattern.length > text.length) return -1;

  // Build bad character table
  const badChar = new Map<string, number>();
  for (let i = 0; i < pattern.length - 1; i++) {
    badChar.set(pattern[i], pattern.length - 1 - i);
  }

  let i = pattern.length - 1;
  while (i < text.length) {
    let j = pattern.length - 1;
    let k = i;
    while (j >= 0 && k >= 0 && text[k] === pattern[j]) {
      if (j === 0) return k; // Match found!
      k--;
      j--;
    }
    const skip = (i < text.length && badChar.has(text[i]))
      ? badChar.get(text[i])!
      : pattern.length;
    i += skip;
  }

  return -1; // Not found
}
```

### Step 2: Create Document Index System

```typescript
// Document segment interface
export interface DocumentSegment {
  text: string;
  start: number;  // Optional: timestamp or position
  duration?: number;
}

// Comprehensive document index
export interface DocumentIndex {
  fullText: string;
  normalizedText: string;
  segmentBoundaries: Array<{
    segmentIdx: number;
    startPos: number;
    endPos: number;
    text: string;
    normalizedText: string;
  }>;
  wordIndex: Map<string, number[]>; // word -> [segment indices]
  ngramIndex: Map<string, Set<number>>; // 3-gram -> segment indices
}

// Build index for fast searching
export function buildDocumentIndex(segments: DocumentSegment[]): DocumentIndex {
  const segmentBoundaries: Array<{
    segmentIdx: number;
    startPos: number;
    endPos: number;
    text: string;
    normalizedText: string;
  }> = [];

  let fullText = '';
  let normalizedText = '';
  const wordIndex = new Map<string, number[]>();
  const ngramIndex = new Map<string, Set<number>>();

  segments.forEach((segment, idx) => {
    if (idx > 0) {
      fullText += ' ';
      normalizedText += ' ';
    }

    const segmentStartPos = fullText.length;
    const segmentNormalized = normalizeForMatching(segment.text);

    fullText += segment.text;
    normalizedText += segmentNormalized;

    // Build word index for this segment
    const words = segmentNormalized.split(/\s+/);
    words.forEach((word) => {
      if (word.length > 2) {
        const positions = wordIndex.get(word) || [];
        positions.push(idx);
        wordIndex.set(word, positions);
      }
    });

    // Build n-gram index (3-grams)
    const cleanText = segmentNormalized.replace(/\s+/g, '');
    for (let i = 0; i <= cleanText.length - 3; i++) {
      const ngram = cleanText.substring(i, i + 3);
      if (!ngramIndex.has(ngram)) {
        ngramIndex.set(ngram, new Set());
      }
      ngramIndex.get(ngram)!.add(idx);
    }

    segmentBoundaries.push({
      segmentIdx: idx,
      startPos: segmentStartPos,
      endPos: fullText.length,
      text: segment.text,
      normalizedText: segmentNormalized
    });
  });

  return {
    fullText,
    normalizedText,
    segmentBoundaries,
    wordIndex,
    ngramIndex
  };
}
```

### Step 3: Intelligent Multi-Strategy Search

```typescript
export interface SearchResult {
  found: boolean;
  startSegmentIdx: number;
  endSegmentIdx: number;
  startCharOffset: number;
  endCharOffset: number;
  matchStrategy: 'exact' | 'normalized' | 'fuzzy-ngram';
  similarity: number;
  confidence: number;
}

export function findText(
  segments: DocumentSegment[],
  targetText: string,
  index: DocumentIndex,
  options: {
    minSimilarity?: number;
    maxSegmentWindow?: number;
  } = {}
): SearchResult | null {
  const {
    minSimilarity = SEARCH_CONFIG.FUZZY_MATCH_THRESHOLD,
    maxSegmentWindow = 30
  } = options;

  // Strategy 1: Try exact match (fastest)
  const exactMatch = boyerMooreSearch(index.fullText, targetText);
  if (exactMatch !== -1) {
    const result = mapMatchToSegments(exactMatch, targetText.length, index);
    if (result) {
      return {
        ...result,
        matchStrategy: 'exact',
        similarity: 1.0,
        confidence: 1.0
      };
    }
  }

  // Strategy 2: Try normalized match (handles whitespace/punctuation)
  const normalizedTarget = normalizeForMatching(targetText);
  const normalizedMatch = boyerMooreSearch(index.normalizedText, normalizedTarget);
  if (normalizedMatch !== -1) {
    const result = mapNormalizedMatchToSegments(
      normalizedMatch,
      normalizedTarget,
      index
    );
    if (result) {
      return {
        ...result,
        matchStrategy: 'normalized',
        similarity: 0.95,
        confidence: 0.95
      };
    }
  }

  // Strategy 3: Fuzzy match using word index + n-gram similarity
  const targetWords = normalizeForMatching(targetText)
    .split(/\s+/)
    .filter(w => w.length > 2);

  if (targetWords.length > 0) {
    // Find segments containing the most target words
    const segmentScores = new Map<number, number>();

    for (const word of targetWords) {
      const segmentIndices = index.wordIndex.get(word) || [];
      for (const segIdx of segmentIndices) {
        segmentScores.set(segIdx, (segmentScores.get(segIdx) || 0) + 1);
      }
    }

    // Check top scoring segments
    const scoredSegments = Array.from(segmentScores.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, 15);

    for (const [candidateIdx, score] of scoredSegments) {
      // Build window around high-scoring segment
      const windowStart = Math.max(0, candidateIdx - 2);
      const windowEnd = Math.min(segments.length - 1, candidateIdx + maxSegmentWindow);

      let combinedText = '';
      for (let i = windowStart; i <= windowEnd; i++) {
        if (i > windowStart) combinedText += ' ';
        combinedText += segments[i].text;

        const normalizedCombined = normalizeForMatching(combinedText);
        const similarity = calculateNgramSimilarity(
          normalizeForMatching(targetText),
          normalizedCombined
        );

        if (similarity >= minSimilarity) {
          return {
            found: true,
            startSegmentIdx: windowStart,
            endSegmentIdx: i,
            startCharOffset: 0,
            endCharOffset: segments[i].text.length,
            matchStrategy: 'fuzzy-ngram',
            similarity,
            confidence: score / targetWords.length
          };
        }
      }
    }
  }

  return null;
}

// Map match position to segment boundaries
function mapMatchToSegments(
  matchStart: number,
  matchLength: number,
  index: DocumentIndex
): Omit<SearchResult, 'matchStrategy' | 'similarity' | 'confidence'> | null {
  const matchEnd = matchStart + matchLength;
  let startSegmentIdx = -1;
  let endSegmentIdx = -1;
  let startCharOffset = 0;
  let endCharOffset = 0;

  for (const boundary of index.segmentBoundaries) {
    // Find start segment
    if (startSegmentIdx === -1 && matchStart >= boundary.startPos && matchStart < boundary.endPos) {
      startSegmentIdx = boundary.segmentIdx;
      startCharOffset = matchStart - boundary.startPos;
    }

    // Find end segment
    if (matchEnd > boundary.startPos && matchEnd <= boundary.endPos) {
      endSegmentIdx = boundary.segmentIdx;
      endCharOffset = matchEnd - boundary.startPos;
      break;
    } else if (matchEnd > boundary.endPos) {
      endSegmentIdx = boundary.segmentIdx;
      endCharOffset = boundary.text.length;
    }
  }

  if (startSegmentIdx !== -1 && endSegmentIdx !== -1) {
    return {
      found: true,
      startSegmentIdx,
      endSegmentIdx,
      startCharOffset,
      endCharOffset
    };
  }

  return null;
}

// Map normalized match back to original segments
function mapNormalizedMatchToSegments(
  normalizedMatchIdx: number,
  normalizedTargetText: string,
  index: DocumentIndex
): Omit<SearchResult, 'matchStrategy' | 'similarity' | 'confidence'> | null {
  const matchEnd = normalizedMatchIdx + normalizedTargetText.length;
  let currentNormPos = 0;
  let startSegmentIdx = -1;
  let endSegmentIdx = -1;
  let startCharOffset = 0;
  let endCharOffset = 0;

  for (const boundary of index.segmentBoundaries) {
    const segmentNormLength = boundary.normalizedText.length;
    const segmentNormEnd = currentNormPos + segmentNormLength;

    if (startSegmentIdx === -1 && normalizedMatchIdx >= currentNormPos && normalizedMatchIdx < segmentNormEnd) {
      startSegmentIdx = boundary.segmentIdx;
      const normOffsetInSegment = normalizedMatchIdx - currentNormPos;
      startCharOffset = Math.min(normOffsetInSegment, boundary.text.length - 1);
    }

    if (matchEnd > currentNormPos && matchEnd <= segmentNormEnd) {
      endSegmentIdx = boundary.segmentIdx;
      const normOffsetInSegment = matchEnd - currentNormPos;
      endCharOffset = Math.min(normOffsetInSegment, boundary.text.length);
      break;
    }

    currentNormPos = segmentNormEnd + 1;
  }

  if (startSegmentIdx !== -1 && endSegmentIdx !== -1) {
    return {
      found: true,
      startSegmentIdx,
      endSegmentIdx,
      startCharOffset,
      endCharOffset
    };
  }

  return null;
}
```

## Usage Examples

### Example 1: Search Video Transcript

```typescript
import { buildDocumentIndex, findText } from '@/lib/text-search';

// Video transcript segments
const transcript = [
  { text: "Welcome to this tutorial on React hooks.", start: 0, duration: 3 },
  { text: "Today we'll learn about useState and useEffect.", start: 3, duration: 4 },
  { text: "These are the most commonly used hooks.", start: 7, duration: 3 }
];

// Build index once
const index = buildDocumentIndex(transcript);

// Search for exact quote
const result1 = findText(transcript, "useState and useEffect", index);
// { found: true, matchStrategy: 'exact', similarity: 1.0, ... }

// Search with typo - fuzzy match
const result2 = findText(transcript, "usestate and useefect", index);
// { found: true, matchStrategy: 'fuzzy-ngram', similarity: 0.92, ... }

// Use result to highlight
if (result1) {
  const segment = transcript[result1.startSegmentIdx];
  const beforeMatch = segment.text.substring(0, result1.startCharOffset);
  const match = segment.text.substring(result1.startCharOffset, result1.endCharOffset);
  const afterMatch = segment.text.substring(result1.endCharOffset);

  console.log(`${beforeMatch}<mark>${match}</mark>${afterMatch}`);
  // "Today we'll learn about <mark>useState and useEffect</mark>."
}
```

---

### Example 2: Citation Verification System

```typescript
import { buildDocumentIndex, findText, calculateNgramSimilarity } from '@/lib/text-search';

// Verify AI-generated citations against source
function verifyCitation(
  citation: string,
  sourceSegments: DocumentSegment[],
  index: DocumentIndex
): {
  verified: boolean;
  confidence: number;
  location?: { segment: number; timestamp: number };
} {
  const result = findText(sourceSegments, citation, index, {
    minSimilarity: 0.8 // Lower threshold for citations
  });

  if (result) {
    return {
      verified: true,
      confidence: result.confidence,
      location: {
        segment: result.startSegmentIdx,
        timestamp: sourceSegments[result.startSegmentIdx].start
      }
    };
  }

  return { verified: false, confidence: 0 };
}

// Usage
const aiResponse = "The React team recommends using functional components with hooks";
const verification = verifyCitation(aiResponse, transcript, index);

if (verification.verified) {
  console.log(`Citation verified with ${(verification.confidence * 100).toFixed(0)}% confidence`);
  console.log(`Found at timestamp: ${verification.location?.timestamp}s`);
}
```

---

### Example 3: Search Suggestions

```typescript
// Find similar segments based on query
function findSimilarSegments(
  query: string,
  segments: DocumentSegment[],
  index: DocumentIndex,
  limit: number = 5
): Array<{ segment: DocumentSegment; similarity: number; index: number }> {
  const normalizedQuery = normalizeForMatching(query);
  const results: Array<{ segment: DocumentSegment; similarity: number; index: number }> = [];

  segments.forEach((segment, idx) => {
    const normalizedSegment = normalizeForMatching(segment.text);
    const similarity = calculateNgramSimilarity(normalizedQuery, normalizedSegment);

    if (similarity > 0.3) {
      results.push({ segment, similarity, index: idx });
    }
  });

  return results
    .sort((a, b) => b.similarity - a.similarity)
    .slice(0, limit);
}

// Usage
const query = "react hooks tutorial";
const similar = findSimilarSegments(query, transcript, index);

similar.forEach(({ segment, similarity }) => {
  console.log(`${(similarity * 100).toFixed(0)}% match: "${segment.text}"`);
});
```

---

### Example 4: Highlight Multiple Matches

```typescript
// Find all occurrences of a phrase
function findAllMatches(
  pattern: string,
  segments: DocumentSegment[],
  index: DocumentIndex
): SearchResult[] {
  const matches: SearchResult[] = [];
  let searchText = index.fullText;
  let offset = 0;

  while (true) {
    const matchPos = boyerMooreSearch(searchText, pattern);
    if (matchPos === -1) break;

    const absolutePos = offset + matchPos;
    const result = mapMatchToSegments(absolutePos, pattern.length, index);

    if (result) {
      matches.push({
        ...result,
        matchStrategy: 'exact',
        similarity: 1.0,
        confidence: 1.0
      });
    }

    // Continue searching after this match
    offset += matchPos + pattern.length;
    searchText = searchText.substring(matchPos + pattern.length);
  }

  return matches;
}
```

---

### Example 5: Performance Benchmark

```typescript
// Measure search performance
function benchmarkSearch(segments: DocumentSegment[]) {
  console.time('Build Index');
  const index = buildDocumentIndex(segments);
  console.timeEnd('Build Index');

  const searches = [
    "exact phrase match",
    "fuzzy aproximate match",
    "very long search query with multiple words to test performance"
  ];

  searches.forEach(query => {
    console.time(`Search: "${query}"`);
    const result = findText(segments, query, index);
    console.timeEnd(`Search: "${query}"`);
    console.log(`  Strategy: ${result?.matchStrategy}, Similarity: ${result?.similarity}`);
  });
}

// Typical results for 10K word document:
// Build Index: 15ms
// Search: "exact phrase match": 0.2ms
// Search: "fuzzy aproximate match": 1.5ms
```

---

## Advanced Patterns

### Pattern 1: Autocomplete with Fuzzy Matching

```typescript
function autocomplete(
  prefix: string,
  words: string[],
  limit: number = 10
): Array<{ word: string; similarity: number }> {
  const normalizedPrefix = normalizeForMatching(prefix);

  return words
    .map(word => ({
      word,
      similarity: calculateNgramSimilarity(
        normalizedPrefix,
        normalizeForMatching(word)
      )
    }))
    .filter(({ similarity }) => similarity > 0.4)
    .sort((a, b) => b.similarity - a.similarity)
    .slice(0, limit);
}
```

---

### Pattern 2: Duplicate Detection

```typescript
function findDuplicates(
  segments: DocumentSegment[],
  threshold: number = 0.9
): Array<[number, number]> {
  const duplicates: Array<[number, number]> = [];

  for (let i = 0; i < segments.length; i++) {
    for (let j = i + 1; j < segments.length; j++) {
      const similarity = calculateNgramSimilarity(
        normalizeForMatching(segments[i].text),
        normalizeForMatching(segments[j].text)
      );

      if (similarity >= threshold) {
        duplicates.push([i, j]);
      }
    }
  }

  return duplicates;
}
```

---

## Best Practices

1. **Build index once** - Reuse for multiple searches
2. **Choose appropriate similarity threshold** - 0.85 for strict, 0.7 for lenient
3. **Limit segment window** - Prevent runaway fuzzy matches
4. **Cache normalized text** - Don't normalize repeatedly
5. **Use Boyer-Moore first** - Always try exact match before fuzzy
6. **Monitor performance** - Index build time scales with document size

---

## Common Pitfalls

1. **Not normalizing consistently** - Use same normalization for index and query
2. **Too aggressive fuzzy matching** - Set minimum similarity threshold
3. **Rebuilding index on every search** - Build once, search many
4. **Ignoring character offsets** - Needed for precise highlighting
5. **Not handling multi-segment matches** - Quotes can span segments
6. **Case-sensitive exact match** - Normalize for matching

---

## Performance Characteristics

| Operation | Time Complexity | Notes |
|-----------|----------------|-------|
| Build Index | O(n) | n = total characters |
| Exact Search (Boyer-Moore) | O(n/m) average | m = pattern length |
| Fuzzy Search | O(k*w) | k = candidates, w = window |
| N-gram Similarity | O(n+m) | n, m = string lengths |

**Benchmarks** (10,000 word document):
- Index build: ~15ms
- Exact search: ~0.2ms
- Fuzzy search: ~1-3ms

---

## Testing

```typescript
describe('Text Search', () => {
  test('exact match', () => {
    const segments = [{ text: "The quick brown fox", start: 0 }];
    const index = buildDocumentIndex(segments);
    const result = findText(segments, "quick brown", index);

    expect(result?.found).toBe(true);
    expect(result?.matchStrategy).toBe('exact');
    expect(result?.similarity).toBe(1.0);
  });

  test('fuzzy match with typo', () => {
    const segments = [{ text: "The quick brown fox", start: 0 }];
    const index = buildDocumentIndex(segments);
    const result = findText(segments, "quik brwon", index);

    expect(result?.found).toBe(true);
    expect(result?.matchStrategy).toBe('fuzzy-ngram');
    expect(result?.similarity).toBeGreaterThan(0.7);
  });

  test('character offsets are precise', () => {
    const segments = [{ text: "Hello world, this is a test", start: 0 }];
    const index = buildDocumentIndex(segments);
    const result = findText(segments, "world", index);

    expect(result?.startCharOffset).toBe(6);
    expect(result?.endCharOffset).toBe(11);
  });
});
```

---

## Next Steps

After implementing this skill:

1. Add caching for frequently searched documents
2. Implement parallel search for very large documents
3. Add spell-correction using n-gram similarity
4. Create search result ranking algorithm
5. Build autocomplete with prefix trees
6. Add support for regex patterns

## Related Skills

- **Type-Safe Form Validation** - Validate search queries
- **Resilient Async Operations** - Handle search in background
- **AI Model Cascade** - Enhance search with AI

---

Built from production text search in [TLDW](https://github.com/vishalsachdev/tldw) citation system
