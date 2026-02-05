---
name: fuzzy-matching
description: Multi-stage fuzzy matching pipeline for entity reconciliation. PostgreSQL trigram pre-filter, salient overlap check, and multi-factor similarity scoring.
license: MIT
compatibility: TypeScript/JavaScript, Python
metadata:
  category: data-processing
  time: 6h
  source: drift-masterguide
---

# Multi-Stage Fuzzy Matching

Production-grade fuzzy matching for inventory items, products, or entity reconciliation.

## When to Use This Skill

- Matching vendor SKUs to inventory items
- Entity reconciliation with varying name formats
- Product deduplication across sources
- Any scenario where exact matching misses valid matches

## Core Concepts

Three-stage pipeline: PostgreSQL trigram (fast pre-filter) → Salient overlap (quick filter) → Multi-factor similarity (expensive, accurate). Achieves O(log n) with proper indexing.


```
Stage 1: PostgreSQL Trigram (fast) → 50 candidates
Stage 2: Salient Overlap Check (fast) → ~20 candidates
Stage 3: Multi-Factor Similarity (expensive) → ranked results
```

## Implementation

### Python

```python
import re
import math
from typing import List, Dict, Optional, Set
from decimal import Decimal


class TextNormalizer:
    """Normalizes text for consistent matching."""
    
    BRAND_PATTERNS = [r'\bsysco\b', r'\bus foods\b', r'\bpremium\b', r'\bselect\b']
    UNIT_MAP = {
        'lb': 'pound', 'lbs': 'pound', 'oz': 'ounce',
        'kg': 'kilogram', 'g': 'gram', 'gal': 'gallon',
    }
    STOPWORDS = {'the', 'and', 'or', 'with', 'of', 'boneless', 'bnls', 'fresh', 'frozen'}

    def normalize_text(self, text: str) -> str:
        if not text:
            return ""
        normalized = text.lower().strip()
        
        for pattern in self.BRAND_PATTERNS:
            normalized = re.sub(pattern, '', normalized, flags=re.IGNORECASE)
        
        for variant, standard in self.UNIT_MAP.items():
            normalized = re.sub(r'\b' + variant + r'\b', standard, normalized, flags=re.IGNORECASE)
        
        normalized = re.sub(r'[^\w\s-]', ' ', normalized)
        return ' '.join(normalized.split())

    def tokenize(self, text: str) -> List[str]:
        normalized = self.normalize_text(text)
        tokens = re.split(r'[\s-]+', normalized)
        return [t for t in tokens if t and t not in self.STOPWORDS and len(t) >= 2]


class SimilarityCalculator:
    """Calculates multi-factor similarity scores."""
    
    WEIGHTS = {
        'name_similarity': 0.55,
        'token_similarity': 0.25,
        'size_similarity': 0.15,
        'category_similarity': 0.05,
    }

    def has_salient_overlap(self, tokens1: List[str], tokens2: List[str]) -> bool:
        """Quick pre-filter: do items share any salient words?"""
        salient1 = {t for t in tokens1 if len(t) >= 3}
        salient2 = {t for t in tokens2 if len(t) >= 3}
        if not salient1 or not salient2:
            return False
        return len(salient1 & salient2) > 0

    def trigram_cosine_similarity(self, text1: str, text2: str) -> float:
        if not text1 or not text2:
            return 0.0
        if text1 == text2:
            return 1.0

        def get_trigrams(text: str) -> Set[str]:
            padded = f"  {text}  "
            return {padded[i:i+3] for i in range(len(padded) - 2)}

        t1, t2 = get_trigrams(text1), get_trigrams(text2)
        intersection = t1 & t2
        if not intersection:
            return 0.0
        return len(intersection) / math.sqrt(len(t1) * len(t2))

    def weighted_jaccard_similarity(self, tokens1: List[str], tokens2: List[str]) -> float:
        if not tokens1 or not tokens2:
            return 0.0
        set1, set2 = set(tokens1), set(tokens2)
        if set1 == set2:
            return 1.0

        def weight(t: str) -> float:
            return 2.0 if len(t) >= 5 else 1.5 if len(t) >= 3 else 1.0

        intersection = set1 & set2
        union = set1 | set2
        return sum(weight(t) for t in intersection) / sum(weight(t) for t in union)

    def size_similarity(self, size1: Optional[Decimal], size2: Optional[Decimal]) -> float:
        if size1 is None or size2 is None:
            return 0.5
        if size1 == size2:
            return 1.0
        ratio = float(min(size1, size2) / max(size1, size2))
        if ratio >= 0.95: return 1.0
        if ratio >= 0.85: return 0.8
        if ratio >= 0.70: return 0.5
        return 0.0

    def calculate_advanced_similarity(self, item1: Dict, item2: Dict) -> float:
        name1 = item1.get('normalized_name', '')
        name2 = item2.get('normalized_name', '')
        
        name_sim = self.trigram_cosine_similarity(name1, name2)
        token_sim = self.weighted_jaccard_similarity(
            self.normalizer.tokenize(name1),
            self.normalizer.tokenize(name2)
        )
        size_sim = self.size_similarity(
            self.extract_size(name1),
            self.extract_size(name2)
        )
        cat_sim = 1.0 if item1.get('category') == item2.get('category') else 0.0

        return (
            self.WEIGHTS['name_similarity'] * name_sim +
            self.WEIGHTS['token_similarity'] * token_sim +
            self.WEIGHTS['size_similarity'] * size_sim +
            self.WEIGHTS['category_similarity'] * cat_sim
        )
```


```python
class FuzzyItemMatcher:
    """Complete 3-stage fuzzy matching pipeline."""
    
    THRESHOLDS = {
        'auto_match': 0.95,
        'review_match': 0.85,
        'min_similarity': 0.70,
        'trigram_filter': 0.3,
    }

    def __init__(self, db_client):
        self.client = db_client
        self.normalizer = TextNormalizer()
        self.calculator = SimilarityCalculator()

    def find_similar_items(
        self,
        target_name: str,
        user_id: str,
        category: Optional[str] = None,
        limit: int = 10,
    ) -> List[Dict]:
        normalized_target = self.normalizer.normalize_text(target_name)
        target_tokens = self.normalizer.tokenize(target_name)

        # Stage 1: PostgreSQL trigram (fast)
        candidates = self._trigram_search(normalized_target, user_id, category, 0.3, 50)
        if not candidates:
            return []

        # Stage 2: Salient overlap filter (fast)
        filtered = []
        for candidate in candidates:
            candidate_tokens = self.normalizer.tokenize(candidate['normalized_name'])
            if self.calculator.has_salient_overlap(target_tokens, candidate_tokens):
                filtered.append(candidate)
        if not filtered:
            return []

        # Stage 3: Advanced similarity (expensive)
        target_item = {'normalized_name': normalized_target, 'category': category}
        results = []
        for candidate in filtered:
            similarity = self.calculator.calculate_advanced_similarity(target_item, candidate)
            if similarity >= self.THRESHOLDS['min_similarity']:
                results.append({**candidate, 'similarity_score': similarity})

        results.sort(key=lambda x: x['similarity_score'], reverse=True)
        return results[:limit]

    def _trigram_search(self, name: str, user_id: str, category: Optional[str], threshold: float, limit: int) -> List[Dict]:
        result = self.client.rpc('find_similar_items', {
            'target_name': name,
            'target_user_id': user_id,
            'similarity_threshold': threshold,
            'result_limit': limit,
        }).execute()
        return result.data or []

    def get_match_recommendation(self, score: float) -> Dict:
        if score >= self.THRESHOLDS['auto_match']:
            return {'action': 'auto_match', 'confidence': 'high', 'needs_review': False}
        elif score >= self.THRESHOLDS['review_match']:
            return {'action': 'review', 'confidence': 'medium', 'needs_review': True}
        return {'action': 'create_new', 'confidence': 'low', 'needs_review': False}
```

### SQL Setup

```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;

ALTER TABLE inventory_items ADD COLUMN normalized_name TEXT;
CREATE INDEX idx_items_trgm ON inventory_items USING GIN (normalized_name gin_trgm_ops);

CREATE FUNCTION find_similar_items(target_name TEXT, target_user_id UUID, similarity_threshold FLOAT, result_limit INT)
RETURNS TABLE (id UUID, name TEXT, normalized_name TEXT, category TEXT, similarity_score FLOAT) AS $$
BEGIN
    RETURN QUERY
    SELECT i.id, i.name, i.normalized_name, i.category,
           similarity(i.normalized_name, target_name) as similarity_score
    FROM inventory_items i
    WHERE i.user_id = target_user_id
      AND similarity(i.normalized_name, target_name) > similarity_threshold
    ORDER BY similarity_score DESC
    LIMIT result_limit;
END;
$$ LANGUAGE plpgsql;
```

## Usage Examples

```python
matcher = FuzzyItemMatcher(db_client)

# Find matches for vendor SKU
matches = matcher.find_similar_items(
    target_name="BNLS CHKN BRST 10LB",
    user_id="user_123",
    category="poultry",
)

for match in matches:
    rec = matcher.get_match_recommendation(match['similarity_score'])
    print(f"{match['name']}: {match['similarity_score']:.2f} - {rec['action']}")
```

## Best Practices

1. Normalize on write - store normalized_name column
2. Start with conservative thresholds (0.95 auto-match)
3. Use domain-specific stopwords (industry terms)
4. Always have Python fallback if RPC fails
5. Tune weights based on your data characteristics

## Common Mistakes

- Computing normalization on every query (slow)
- Generic stopword lists missing domain terms
- Not handling size/unit variations
- Skipping the salient overlap filter (slow)

## Related Patterns

- deduplication (preventing duplicates)
- validation-quarantine (handling uncertain matches)
