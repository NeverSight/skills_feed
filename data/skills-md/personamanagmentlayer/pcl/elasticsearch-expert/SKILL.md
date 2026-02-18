---
name: elasticsearch-expert
version: 1.0.0
description: Expert-level Elasticsearch, search, ELK stack, and full-text search
category: data
tags: [elasticsearch, search, elk, logstash, kibana, full-text-search]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(*)
---

# Elasticsearch Expert

Expert guidance for Elasticsearch, search optimization, ELK stack, and distributed search systems.

## Core Concepts

- Full-text search and inverted indexes
- Document-oriented storage
- RESTful API
- Distributed architecture with sharding
- ELK stack (Elasticsearch, Logstash, Kibana)
- Aggregations and analytics

## Index Management

```python
from elasticsearch import Elasticsearch

es = Elasticsearch(['http://localhost:9200'])

# Create index with mapping
mapping = {
    "mappings": {
        "properties": {
            "title": {"type": "text", "analyzer": "english"},
            "content": {"type": "text"},
            "author": {"type": "keyword"},
            "created_at": {"type": "date"},
            "views": {"type": "integer"}
        }
    }
}

es.indices.create(index='articles', body=mapping)

# Index document
doc = {
    "title": "Elasticsearch Guide",
    "content": "Complete guide to Elasticsearch",
    "author": "John Doe",
    "created_at": "2024-01-01",
    "views": 100
}

es.index(index='articles', id=1, body=doc)

# Bulk indexing
from elasticsearch.helpers import bulk

actions = [
    {"_index": "articles", "_id": i, "_source": doc}
    for i, doc in enumerate(documents)
]

bulk(es, actions)
```

## Search Queries

```python
# Full-text search
query = {
    "query": {
        "match": {
            "content": "elasticsearch guide"
        }
    }
}

results = es.search(index='articles', body=query)

# Boolean query
bool_query = {
    "query": {
        "bool": {
            "must": [
                {"match": {"content": "elasticsearch"}}
            ],
            "filter": [
                {"range": {"views": {"gte": 100}}}
            ],
            "should": [
                {"term": {"author": "john-doe"}}
            ],
            "must_not": [
                {"term": {"status": "draft"}}
            ]
        }
    }
}

# Multi-match query
multi_match = {
    "query": {
        "multi_match": {
            "query": "elasticsearch guide",
            "fields": ["title^2", "content"],  # Boost title
            "type": "best_fields"
        }
    }
}

# Fuzzy search
fuzzy = {
    "query": {
        "fuzzy": {
            "title": {
                "value": "elasticseerch",
                "fuzziness": "AUTO"
            }
        }
    }
}
```

## Aggregations

```python
# Aggregation query
agg_query = {
    "aggs": {
        "authors": {
            "terms": {
                "field": "author",
                "size": 10
            }
        },
        "avg_views": {
            "avg": {
                "field": "views"
            }
        },
        "views_histogram": {
            "histogram": {
                "field": "views",
                "interval": 100
            }
        },
        "date_histogram": {
            "date_histogram": {
                "field": "created_at",
                "calendar_interval": "month"
            }
        }
    }
}

result = es.search(index='articles', body=agg_query)
```

## Best Practices

- Design mappings carefully
- Use appropriate analyzers
- Implement proper sharding strategy
- Monitor cluster health
- Use bulk operations
- Implement pagination with search_after
- Cache frequently used queries

## Anti-Patterns

❌ Deep pagination with from/size
❌ Wildcard queries without prefix
❌ No replica shards
❌ Over-sharding
❌ Not using filters for exact matches
❌ Ignoring cluster yellow/red status

## Resources

- Elasticsearch Guide: https://www.elastic.co/guide/
- ELK Stack: https://www.elastic.co/elk-stack
