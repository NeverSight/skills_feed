---
name: skillsmp-search
description: Search and discover AI skills using the SkillsMP API. Supports keyword search and AI semantic search powered by Cloudflare AI. Use when users want to find AI skills, search for specific capabilities, or explore community-built AI tools. Triggers on "search skills", "find AI skills", "look up skills", "skills marketplace", "AI skills database".
---

# SkillsMP API Skill

Access the SkillsMP API for searching and discovering AI skills built by the community.

## Quick Start

### 1. Set API Key
```bash
export SKILLSMP_API_KEY="your-api-key-here"
```

### 2. Use the Python Client
```bash
# Search skills by keyword
python scripts/skillsmp_api.py search "SEO"

# AI semantic search
python scripts/skillsmp_api.py ai-search "How to create a web scraper"
```

### 3. Or Use Directly
```bash
# Keyword search
curl -X GET "https://skillsmp.com/api/v1/skills/search?q=SEO" \
-H "Authorization: Bearer $SKILLSMP_API_KEY"

# AI search
curl -X GET "https://skillsmp.com/api/v1/skills/ai-search?q=How+to+scrape+websites" \
-H "Authorization: Bearer $SKILLSMP_API_KEY"
```

## Bundled Resources

### Python Client (`scripts/skillsmp_api.py`)
A complete Python client with:
- `SkillsMPAPI` class for programmatic access
- CLI interface for quick searches
- Error handling and type hints
- Two search methods: `search()` and `ai_search()`

**Usage in your code:**
```python
from skillsmp_api import SkillsMPAPI

client = SkillsMPAPI()
results = client.search("SEO", sort_by="stars")
```

### API Reference (`references/api_reference.md`)
Complete documentation including:
- All endpoints and parameters
- Response formats
- Error codes
- Rate limits
- Best practices
- Additional examples

## When to Use This Skill

- **Finding specific skills**: Use keyword search for terms like "SEO", "web scraping", "data analysis"
- **Natural language queries**: Use AI search for questions like "How do I automate social media posting?"
- **Exploring**: Search with `sortBy=stars` for popular skills or `sortBy=recent` for new additions
- **Building integrations**: Use the Python client for programmatic access

## Error Handling

The API returns errors in this format:
```json
{
  "success": false,
  "error": {
    "code": "INVALID_API_KEY",
    "message": "The provided API key is invalid"
  }
}
```

Common error codes: `MISSING_API_KEY`, `INVALID_API_KEY`, `MISSING_QUERY`, `INTERNAL_ERROR`

## Best Practices

1. **Always use environment variables** for API keys
2. **Handle errors gracefully** - check the `success` field
3. **Use appropriate search type**:
   - Keyword search for specific terms
   - AI search for natural language questions
4. **Respect rate limits** - use pagination for large result sets
5. **Use the Python client** for complex operations

## References

- **Full API Documentation**: See `references/api_reference.md`
- **Python Client**: See `scripts/skillsmp_api.py`
- **API Website**: https://skillsmp.com/docs/api
- **Note**: SkillsMP is not affiliated with Anthropic