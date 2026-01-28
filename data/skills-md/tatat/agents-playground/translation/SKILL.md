---
name: translation
description: Translate text between languages while preserving meaning and context
---

# Translation

Translate text between languages accurately.

## Capabilities

- Translate between 100+ languages
- Preserve formatting and structure
- Handle technical terminology
- Maintain tone and style

## Supported Languages

| Code | Language |
|------|----------|
| en | English |
| ja | Japanese |
| zh | Chinese (Simplified) |
| ko | Korean |
| es | Spanish |
| fr | French |
| de | German |
| pt | Portuguese |
| ru | Russian |
| ar | Arabic |

## Translation Modes

### Literal
- Word-for-word accuracy
- Preserves original structure
- Use for: technical docs, legal texts

### Natural
- Native-sounding output
- Adapts idioms and expressions
- Use for: marketing, creative content

### Technical
- Domain-specific terminology
- Consistent glossary usage
- Use for: software, medical, legal

## Request Format

```json
{
  "text": "Text to translate",
  "source_lang": "en",
  "target_lang": "ja",
  "mode": "natural",
  "glossary": {
    "API": "API",
    "endpoint": "エンドポイント"
  }
}
```

## Best Practices

1. Provide context for ambiguous terms
2. Use glossaries for consistent terminology
3. Review translations for domain accuracy
4. Consider cultural adaptation for marketing
