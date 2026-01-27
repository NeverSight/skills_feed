---
name: bedrock-knowledge-bases
description: Amazon Bedrock Knowledge Bases for RAG (Retrieval-Augmented Generation). Create knowledge bases with vector stores, ingest data from S3/web/Confluence/SharePoint, configure chunking strategies, query with retrieve and generate APIs, manage sessions. Use when building RAG applications, implementing semantic search, creating document Q&A systems, integrating knowledge bases with agents, optimizing chunking for accuracy, or querying enterprise knowledge.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
triggers:
  - RAG
  - knowledge base
  - vector database
  - semantic search
  - document retrieval
  - chunking
  - embeddings
  - OpenSearch
  - S3 vectors
  - Neptune GraphRAG
  - retrieve and generate
  - ingestion
  - data source
---

# Amazon Bedrock Knowledge Bases

Amazon Bedrock Knowledge Bases is a fully managed RAG (Retrieval-Augmented Generation) solution that handles data ingestion, embedding generation, vector storage, retrieval with reranking, source attribution, and session context management.

## Overview

### What It Does

Amazon Bedrock Knowledge Bases provides:
- **Data Ingestion**: Automatically process documents from S3, web, Confluence, SharePoint, Salesforce
- **Embedding Generation**: Convert text to vectors using foundation models
- **Vector Storage**: Store embeddings in multiple vector database options
- **Retrieval**: Semantic and hybrid search with metadata filtering
- **Generation**: RAG workflows with source attribution
- **Session Management**: Multi-turn conversations with context
- **Chunking Strategies**: Fixed, semantic, hierarchical, and custom chunking

### When to Use This Skill

Use this skill when you need to:
- Build RAG applications for document Q&A
- Implement semantic search over enterprise knowledge
- Create chatbots with knowledge bases
- Integrate retrieval with Bedrock Agents
- Configure optimal chunking strategies
- Query documents with source attribution
- Manage multi-turn conversations with context
- Optimize RAG performance and cost

### Key Capabilities

1. **Multiple Vector Store Options**: OpenSearch, S3 Vectors, Neptune, Pinecone, MongoDB, Redis
2. **Flexible Data Sources**: S3, web crawlers, Confluence, SharePoint, Salesforce
3. **Advanced Chunking**: Fixed-size, semantic, hierarchical, custom Lambda
4. **Hybrid Search**: Combine semantic (vector) and keyword search
5. **Session Management**: Built-in conversation context tracking
6. **GraphRAG**: Relationship-aware retrieval with Neptune Analytics
7. **Cost Optimization**: S3 Vectors for up to 90% storage savings

---

## Quick Start

### Basic RAG Workflow

```python
import boto3
import json

# Initialize clients
bedrock_agent = boto3.client('bedrock-agent', region_name='us-east-1')
bedrock_agent_runtime = boto3.client('bedrock-agent-runtime', region_name='us-east-1')

# 1. Create Knowledge Base
kb_response = bedrock_agent.create_knowledge_base(
    name='enterprise-docs-kb',
    description='Company documentation knowledge base',
    roleArn='arn:aws:iam::123456789012:role/BedrockKBRole',
    knowledgeBaseConfiguration={
        'type': 'VECTOR',
        'vectorKnowledgeBaseConfiguration': {
            'embeddingModelArn': 'arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-embed-text-v2:0'
        }
    },
    storageConfiguration={
        'type': 'OPENSEARCH_SERVERLESS',
        'opensearchServerlessConfiguration': {
            'collectionArn': 'arn:aws:aoss:us-east-1:123456789012:collection/kb-collection',
            'vectorIndexName': 'bedrock-knowledge-base-index',
            'fieldMapping': {
                'vectorField': 'bedrock-knowledge-base-default-vector',
                'textField': 'AMAZON_BEDROCK_TEXT_CHUNK',
                'metadataField': 'AMAZON_BEDROCK_METADATA'
            }
        }
    }
)

knowledge_base_id = kb_response['knowledgeBase']['knowledgeBaseId']
print(f"Knowledge Base ID: {knowledge_base_id}")

# 2. Add S3 Data Source
ds_response = bedrock_agent.create_data_source(
    knowledgeBaseId=knowledge_base_id,
    name='s3-documents',
    description='Company documents from S3',
    dataSourceConfiguration={
        'type': 'S3',
        's3Configuration': {
            'bucketArn': 'arn:aws:s3:::my-docs-bucket',
            'inclusionPrefixes': ['documents/']
        }
    },
    vectorIngestionConfiguration={
        'chunkingConfiguration': {
            'chunkingStrategy': 'FIXED_SIZE',
            'fixedSizeChunkingConfiguration': {
                'maxTokens': 512,
                'overlapPercentage': 20
            }
        }
    }
)

data_source_id = ds_response['dataSource']['dataSourceId']

# 3. Start Ingestion
ingestion_response = bedrock_agent.start_ingestion_job(
    knowledgeBaseId=knowledge_base_id,
    dataSourceId=data_source_id,
    description='Initial document ingestion'
)

print(f"Ingestion Job ID: {ingestion_response['ingestionJob']['ingestionJobId']}")

# 4. Query with Retrieve and Generate
response = bedrock_agent_runtime.retrieve_and_generate(
    input={
        'text': 'What is our vacation policy?'
    },
    retrieveAndGenerateConfiguration={
        'type': 'KNOWLEDGE_BASE',
        'knowledgeBaseConfiguration': {
            'knowledgeBaseId': knowledge_base_id,
            'modelArn': 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0',
            'retrievalConfiguration': {
                'vectorSearchConfiguration': {
                    'numberOfResults': 5,
                    'overrideSearchType': 'HYBRID'
                }
            }
        }
    }
)

print(f"Answer: {response['output']['text']}")
print(f"\nSources:")
for citation in response['citations']:
    for reference in citation['retrievedReferences']:
        print(f"  - {reference['location']['s3Location']['uri']}")
```

---

## Vector Store Options

### 1. Amazon OpenSearch Serverless

**Best for**: Production RAG applications with auto-scaling requirements

**Benefits**:
- Fully managed, serverless operation
- Auto-scaling compute and storage
- High availability with multi-AZ deployment
- Fast query performance

**Configuration**:

```python
storageConfiguration={
    'type': 'OPENSEARCH_SERVERLESS',
    'opensearchServerlessConfiguration': {
        'collectionArn': 'arn:aws:aoss:us-east-1:123456789012:collection/kb-collection',
        'vectorIndexName': 'bedrock-knowledge-base-index',
        'fieldMapping': {
            'vectorField': 'bedrock-knowledge-base-default-vector',
            'textField': 'AMAZON_BEDROCK_TEXT_CHUNK',
            'metadataField': 'AMAZON_BEDROCK_METADATA'
        }
    }
}
```

### 2. Amazon S3 Vectors (Preview)

**Best for**: Cost-optimized, large-scale RAG applications

**Benefits**:
- Up to 90% cost reduction for vector storage
- Built-in vector support in S3
- Subsecond query performance
- Massive scale and durability

**Ideal Use Cases**:
- Large document collections (millions of chunks)
- Cost-sensitive applications
- Archival knowledge bases
- Low-to-medium QPS workloads

**Configuration**:

```python
storageConfiguration={
    'type': 'S3_VECTORS',
    's3VectorsConfiguration': {
        'bucketArn': 'arn:aws:s3:::my-vector-bucket',
        'prefix': 'vectors/'
    }
}
```

**Limitations**:
- Still in preview (no CloudFormation/CDK support yet)
- Not suitable for high QPS, millisecond-latency requirements
- Best for cost optimization over ultra-low latency

### 3. Amazon Neptune Analytics (GraphRAG)

**Best for**: Interconnected knowledge domains requiring relationship-aware retrieval

**Benefits**:
- Automatic graph creation linking related content
- Improved retrieval accuracy through relationships
- Comprehensive responses leveraging knowledge graph
- Explainable results with relationship context

**Use Cases**:
- Legal document analysis with case precedents
- Scientific research with paper citations
- Product catalogs with dependencies
- Organizational knowledge with team relationships

**Configuration**:

```python
storageConfiguration={
    'type': 'NEPTUNE_ANALYTICS',
    'neptuneAnalyticsConfiguration': {
        'graphArn': 'arn:aws:neptune-graph:us-east-1:123456789012:graph/g-12345678',
        'vectorSearchConfiguration': {
            'vectorField': 'embedding'
        }
    }
}
```

### 4. Amazon OpenSearch Service Managed Cluster

**Best for**: Existing OpenSearch infrastructure, advanced customization

**Configuration**:

```python
storageConfiguration={
    'type': 'OPENSEARCH_SERVICE',
    'opensearchServiceConfiguration': {
        'clusterArn': 'arn:aws:es:us-east-1:123456789012:domain/my-domain',
        'vectorIndexName': 'bedrock-kb-index',
        'fieldMapping': {
            'vectorField': 'embedding',
            'textField': 'text',
            'metadataField': 'metadata'
        }
    }
}
```

### 5. Third-Party Vector Databases

**Pinecone**:

```python
storageConfiguration={
    'type': 'PINECONE',
    'pineconeConfiguration': {
        'connectionString': 'https://my-index-abc123.svc.us-west1-gcp.pinecone.io',
        'credentialsSecretArn': 'arn:aws:secretsmanager:us-east-1:123456789012:secret:pinecone-api-key',
        'namespace': 'bedrock-kb',
        'fieldMapping': {
            'textField': 'text',
            'metadataField': 'metadata'
        }
    }
}
```

**MongoDB Atlas**:

```python
storageConfiguration={
    'type': 'MONGODB_ATLAS',
    'mongoDbAtlasConfiguration': {
        'endpoint': 'https://cluster0.mongodb.net',
        'credentialsSecretArn': 'arn:aws:secretsmanager:us-east-1:123456789012:secret:mongodb-creds',
        'databaseName': 'bedrock_kb',
        'collectionName': 'vectors',
        'vectorIndexName': 'vector_index',
        'fieldMapping': {
            'vectorField': 'embedding',
            'textField': 'text',
            'metadataField': 'metadata'
        }
    }
}
```

**Redis Enterprise Cloud**:

```python
storageConfiguration={
    'type': 'REDIS_ENTERPRISE_CLOUD',
    'redisEnterpriseCloudConfiguration': {
        'endpoint': 'redis-12345.c1.us-east-1-2.ec2.cloud.redislabs.com:12345',
        'credentialsSecretArn': 'arn:aws:secretsmanager:us-east-1:123456789012:secret:redis-creds',
        'vectorIndexName': 'bedrock-kb-index',
        'fieldMapping': {
            'vectorField': 'embedding',
            'textField': 'text',
            'metadataField': 'metadata'
        }
    }
}
```

---

## Data Source Configuration

### 1. Amazon S3

**Supported File Types**: PDF, TXT, MD, HTML, DOC, DOCX, CSV, XLS, XLSX

```python
bedrock_agent.create_data_source(
    knowledgeBaseId=knowledge_base_id,
    name='s3-technical-docs',
    description='Technical documentation from S3',
    dataSourceConfiguration={
        'type': 'S3',
        's3Configuration': {
            'bucketArn': 'arn:aws:s3:::my-docs-bucket',
            'inclusionPrefixes': ['docs/technical/', 'docs/manuals/'],
            'exclusionPrefixes': ['docs/archive/']
        }
    }
)
```

### 2. Web Crawler

**Automatic website scraping and indexing**:

```python
bedrock_agent.create_data_source(
    knowledgeBaseId=knowledge_base_id,
    name='company-website',
    description='Public company website content',
    dataSourceConfiguration={
        'type': 'WEB',
        'webConfiguration': {
            'sourceConfiguration': {
                'urlConfiguration': {
                    'seedUrls': [
                        {'url': 'https://www.example.com/docs'},
                        {'url': 'https://www.example.com/blog'}
                    ]
                }
            },
            'crawlerConfiguration': {
                'crawlerLimits': {
                    'rateLimit': 300  # Pages per minute
                }
            }
        }
    }
)
```

### 3. Confluence

```python
bedrock_agent.create_data_source(
    knowledgeBaseId=knowledge_base_id,
    name='confluence-wiki',
    description='Company Confluence knowledge base',
    dataSourceConfiguration={
        'type': 'CONFLUENCE',
        'confluenceConfiguration': {
            'sourceConfiguration': {
                'hostUrl': 'https://company.atlassian.net/wiki',
                'hostType': 'SAAS',
                'authType': 'BASIC',
                'credentialsSecretArn': 'arn:aws:secretsmanager:us-east-1:123456789012:secret:confluence-creds'
            },
            'crawlerConfiguration': {
                'filterConfiguration': {
                    'type': 'PATTERN',
                    'patternObjectFilter': {
                        'filters': [
                            {
                                'objectType': 'Space',
                                'inclusionFilters': ['Engineering', 'Product'],
                                'exclusionFilters': ['Archive']
                            }
                        ]
                    }
                }
            }
        }
    }
)
```

### 4. SharePoint

```python
bedrock_agent.create_data_source(
    knowledgeBaseId=knowledge_base_id,
    name='sharepoint-docs',
    description='SharePoint document library',
    dataSourceConfiguration={
        'type': 'SHAREPOINT',
        'sharePointConfiguration': {
            'sourceConfiguration': {
                'siteUrls': [
                    'https://company.sharepoint.com/sites/Engineering',
                    'https://company.sharepoint.com/sites/Product'
                ],
                'tenantId': 'tenant-id',
                'domain': 'company',
                'authType': 'OAUTH2_CLIENT_CREDENTIALS',
                'credentialsSecretArn': 'arn:aws:secretsmanager:us-east-1:123456789012:secret:sharepoint-creds'
            }
        }
    }
)
```

### 5. Salesforce

```python
bedrock_agent.create_data_source(
    knowledgeBaseId=knowledge_base_id,
    name='salesforce-knowledge',
    description='Salesforce knowledge articles',
    dataSourceConfiguration={
        'type': 'SALESFORCE',
        'salesforceConfiguration': {
            'sourceConfiguration': {
                'hostUrl': 'https://company.my.salesforce.com',
                'authType': 'OAUTH2_CLIENT_CREDENTIALS',
                'credentialsSecretArn': 'arn:aws:secretsmanager:us-east-1:123456789012:secret:salesforce-creds'
            },
            'crawlerConfiguration': {
                'filterConfiguration': {
                    'type': 'PATTERN',
                    'patternObjectFilter': {
                        'filters': [
                            {
                                'objectType': 'Knowledge',
                                'inclusionFilters': ['Product_Documentation', 'Support_Articles']
                            }
                        ]
                    }
                }
            }
        }
    }
)
```

---

## Chunking Strategies

### 1. Fixed-Size Chunking

**Best for**: Simple documents with uniform structure

**How it works**: Splits text into chunks of fixed token size with overlap

**Parameters**:
- `maxTokens`: 200-8192 tokens (typically 512-1024)
- `overlapPercentage`: 10-50% (typically 20%)

**Configuration**:

```python
vectorIngestionConfiguration={
    'chunkingConfiguration': {
        'chunkingStrategy': 'FIXED_SIZE',
        'fixedSizeChunkingConfiguration': {
            'maxTokens': 512,
            'overlapPercentage': 20
        }
    }
}
```

**Use Cases**:
- Blog posts and articles
- Technical documentation with consistent formatting
- FAQs and Q&A content
- Simple text files

**Pros**:
- Fast and predictable
- No additional costs
- Easy to tune

**Cons**:
- May split semantic units awkwardly
- Doesn't respect document structure
- Can break context mid-sentence

### 2. Semantic Chunking

**Best for**: Documents without clear boundaries (legal, technical, academic)

**How it works**: Uses sentence similarity to group related content

**Parameters**:
- `maxTokens`: 20-8192 tokens (typically 300-500)
- `bufferSize`: Number of neighboring sentences (default: 1)
- `breakpointPercentileThreshold`: Similarity threshold (recommended: 95%)

**Configuration**:

```python
vectorIngestionConfiguration={
    'chunkingConfiguration': {
        'chunkingStrategy': 'SEMANTIC',
        'semanticChunkingConfiguration': {
            'maxTokens': 300,
            'bufferSize': 1,
            'breakpointPercentileThreshold': 95
        }
    }
}
```

**Use Cases**:
- Legal documents and contracts
- Academic papers
- Technical specifications
- Medical records
- Research reports

**Pros**:
- Preserves semantic meaning
- Better context preservation
- Improved retrieval accuracy

**Cons**:
- Additional cost (foundation model usage)
- Slower ingestion
- Less predictable chunk sizes

**Cost Consideration**: Semantic chunking uses foundation models for similarity analysis, incurring additional costs beyond storage and retrieval.

### 3. Hierarchical Chunking

**Best for**: Complex documents with nested structure

**How it works**: Creates parent and child chunks; retrieves child, returns parent for context

**Parameters**:
- `levelConfigurations`: Array of chunk sizes (parent → child)
- `overlapTokens`: Overlap between chunks

**Configuration**:

```python
vectorIngestionConfiguration={
    'chunkingConfiguration': {
        'chunkingStrategy': 'HIERARCHICAL',
        'hierarchicalChunkingConfiguration': {
            'levelConfigurations': [
                {
                    'maxTokens': 1500  # Parent chunk (comprehensive context)
                },
                {
                    'maxTokens': 300   # Child chunk (focused retrieval)
                }
            ],
            'overlapTokens': 60
        }
    }
}
```

**Use Cases**:
- Technical manuals with sections and subsections
- Academic papers with abstract, sections, and subsections
- Legal documents with articles and clauses
- Product documentation with categories and details

**How Retrieval Works**:
1. Query matches against child chunks (fast, focused)
2. Returns parent chunks (comprehensive context)
3. Best of both: precision retrieval + complete context

**Pros**:
- Optimal balance of precision and context
- Excellent for nested documents
- Better accuracy for complex queries

**Cons**:
- More complex configuration
- Larger storage footprint
- Requires understanding of document structure

### 4. Custom Chunking (Lambda)

**Best for**: Specialized domain logic, custom parsing requirements

**How it works**: Invoke Lambda function for custom chunking logic

**Configuration**:

```python
vectorIngestionConfiguration={
    'chunkingConfiguration': {
        'chunkingStrategy': 'NONE'  # Custom via Lambda
    },
    'customTransformationConfiguration': {
        'intermediateStorage': {
            's3Location': {
                'uri': 's3://my-kb-bucket/intermediate/'
            }
        },
        'transformations': [
            {
                'stepToApply': 'POST_CHUNKING',
                'transformationFunction': {
                    'transformationLambdaConfiguration': {
                        'lambdaArn': 'arn:aws:lambda:us-east-1:123456789012:function:custom-chunker'
                    }
                }
            }
        ]
    }
}
```

**Example Lambda Handler**:

```python
# Lambda function for custom chunking
import json

def lambda_handler(event, context):
    """
    Custom chunking logic for specialized documents

    Input: event contains document content and metadata
    Output: array of chunks with text and metadata
    """

    # Extract document content
    document = event['document']
    content = document['content']
    metadata = document.get('metadata', {})

    # Custom chunking logic (example: split by custom delimiter)
    chunks = []
    sections = content.split('---SECTION---')

    for idx, section in enumerate(sections):
        if section.strip():
            chunks.append({
                'text': section.strip(),
                'metadata': {
                    **metadata,
                    'chunk_id': f'section_{idx}',
                    'chunk_type': 'custom_section'
                }
            })

    return {
        'chunks': chunks
    }
```

**Use Cases**:
- Medical records with structured sections (SOAP notes)
- Financial documents with tables and calculations
- Code documentation with code blocks and explanations
- Domain-specific formats (HL7, FHIR, etc.)

**Pros**:
- Complete control over chunking logic
- Can handle any document format
- Integrate domain expertise

**Cons**:
- Requires Lambda development and maintenance
- Additional operational complexity
- Harder to debug and iterate

### Chunking Strategy Selection Guide

| Document Type | Recommended Strategy | Rationale |
|--------------|---------------------|-----------|
| Blog posts, articles | Fixed-size | Simple, uniform structure |
| Legal documents | Semantic | Preserve legal reasoning flow |
| Technical manuals | Hierarchical | Nested sections and subsections |
| Academic papers | Hierarchical | Abstract, sections, subsections |
| FAQs | Fixed-size | Independent Q&A pairs |
| Medical records | Custom Lambda | Structured sections (SOAP, HL7) |
| Code documentation | Custom Lambda | Code blocks + explanations |
| Product catalogs | Fixed-size | Uniform product descriptions |
| Research reports | Semantic | Preserve research narrative |

---

## Retrieval Operations

### 1. Retrieve API (Retrieval Only)

Returns raw retrieved chunks without generation.

**Use Cases**:
- Custom generation logic
- Debugging retrieval quality
- Building custom RAG pipelines
- Integrating with non-Bedrock models

```python
bedrock_agent_runtime = boto3.client('bedrock-agent-runtime', region_name='us-east-1')

response = bedrock_agent_runtime.retrieve(
    knowledgeBaseId='KB123456',
    retrievalQuery={
        'text': 'What are the benefits of hierarchical chunking?'
    },
    retrievalConfiguration={
        'vectorSearchConfiguration': {
            'numberOfResults': 5,
            'overrideSearchType': 'HYBRID',  # SEMANTIC, HYBRID
            'filter': {
                'andAll': [
                    {
                        'equals': {
                            'key': 'document_type',
                            'value': 'technical_guide'
                        }
                    },
                    {
                        'greaterThan': {
                            'key': 'publish_year',
                            'value': 2024
                        }
                    }
                ]
            }
        }
    }
)

# Process retrieved chunks
for result in response['retrievalResults']:
    print(f"Score: {result['score']}")
    print(f"Content: {result['content']['text']}")
    print(f"Location: {result['location']}")
    print(f"Metadata: {result.get('metadata', {})}")
    print("---")
```

### 2. Retrieve and Generate API (RAG)

Returns generated response with source attribution.

**Use Cases**:
- Complete RAG workflows
- Question answering
- Document summarization
- Chatbots with knowledge bases

```python
response = bedrock_agent_runtime.retrieve_and_generate(
    input={
        'text': 'Explain semantic chunking benefits and when to use it'
    },
    retrieveAndGenerateConfiguration={
        'type': 'KNOWLEDGE_BASE',
        'knowledgeBaseConfiguration': {
            'knowledgeBaseId': 'KB123456',
            'modelArn': 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0',
            'retrievalConfiguration': {
                'vectorSearchConfiguration': {
                    'numberOfResults': 5,
                    'overrideSearchType': 'HYBRID'
                }
            },
            'generationConfiguration': {
                'inferenceConfig': {
                    'textInferenceConfig': {
                        'temperature': 0.7,
                        'maxTokens': 2048,
                        'topP': 0.9
                    }
                },
                'promptTemplate': {
                    'textPromptTemplate': '''You are a helpful assistant. Answer the user's question based on the provided context.

Context: $search_results$

Question: $query$

Answer:'''
                }
            }
        }
    }
)

print(f"Generated Response: {response['output']['text']}")
print(f"\nSources:")
for citation in response['citations']:
    for reference in citation['retrievedReferences']:
        print(f"  - {reference['location']}")
        print(f"    Relevance Score: {reference.get('score', 'N/A')}")
```

### 3. Multi-Turn Conversations with Session Management

Bedrock automatically manages conversation context across turns.

```python
# First turn - creates session automatically
response1 = bedrock_agent_runtime.retrieve_and_generate(
    input={
        'text': 'What is Amazon Bedrock Knowledge Bases?'
    },
    retrieveAndGenerateConfiguration={
        'type': 'KNOWLEDGE_BASE',
        'knowledgeBaseConfiguration': {
            'knowledgeBaseId': 'KB123456',
            'modelArn': 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0'
        }
    }
)

session_id = response1['sessionId']
print(f"Session ID: {session_id}")
print(f"Response: {response1['output']['text']}\n")

# Follow-up turn - reuse session for context
response2 = bedrock_agent_runtime.retrieve_and_generate(
    input={
        'text': 'What chunking strategies does it support?'
    },
    retrieveAndGenerateConfiguration={
        'type': 'KNOWLEDGE_BASE',
        'knowledgeBaseConfiguration': {
            'knowledgeBaseId': 'KB123456',
            'modelArn': 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0'
        }
    },
    sessionId=session_id  # Continue conversation with context
)

print(f"Follow-up Response: {response2['output']['text']}")

# Third turn
response3 = bedrock_agent_runtime.retrieve_and_generate(
    input={
        'text': 'Which strategy would you recommend for legal documents?'
    },
    retrieveAndGenerateConfiguration={
        'type': 'KNOWLEDGE_BASE',
        'knowledgeBaseConfiguration': {
            'knowledgeBaseId': 'KB123456',
            'modelArn': 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0'
        }
    },
    sessionId=session_id
)

print(f"Third Response: {response3['output']['text']}")
```

### 4. Advanced Metadata Filtering

Filter retrieval by metadata attributes for precision.

```python
response = bedrock_agent_runtime.retrieve(
    knowledgeBaseId='KB123456',
    retrievalQuery={
        'text': 'Security best practices for production deployments'
    },
    retrievalConfiguration={
        'vectorSearchConfiguration': {
            'numberOfResults': 10,
            'overrideSearchType': 'HYBRID',
            'filter': {
                'andAll': [
                    {
                        'equals': {
                            'key': 'document_type',
                            'value': 'security_guide'
                        }
                    },
                    {
                        'greaterThanOrEquals': {
                            'key': 'publish_year',
                            'value': 2024
                        }
                    },
                    {
                        'in': {
                            'key': 'category',
                            'value': ['production', 'security', 'compliance']
                        }
                    }
                ]
            }
        }
    }
)
```

**Supported Filter Operators**:
- `equals`: Exact match
- `notEquals`: Not equal
- `greaterThan`, `greaterThanOrEquals`: Numeric comparison
- `lessThan`, `lessThanOrEquals`: Numeric comparison
- `in`: Match any value in array
- `notIn`: Not match any value in array
- `startsWith`: String prefix match
- `andAll`: Combine filters with AND
- `orAll`: Combine filters with OR

---

## Ingestion Management

### 1. Start Ingestion Job

```python
ingestion_response = bedrock_agent.start_ingestion_job(
    knowledgeBaseId=knowledge_base_id,
    dataSourceId=data_source_id,
    description='Monthly document sync',
    clientToken='unique-idempotency-token-123'
)

job_id = ingestion_response['ingestionJob']['ingestionJobId']
print(f"Ingestion Job ID: {job_id}")
```

### 2. Monitor Ingestion Job

```python
# Get job status
job_status = bedrock_agent.get_ingestion_job(
    knowledgeBaseId=knowledge_base_id,
    dataSourceId=data_source_id,
    ingestionJobId=job_id
)

print(f"Status: {job_status['ingestionJob']['status']}")
print(f"Started: {job_status['ingestionJob']['startedAt']}")
print(f"Updated: {job_status['ingestionJob']['updatedAt']}")

if 'statistics' in job_status['ingestionJob']:
    stats = job_status['ingestionJob']['statistics']
    print(f"Documents Scanned: {stats['numberOfDocumentsScanned']}")
    print(f"Documents Indexed: {stats['numberOfDocumentsIndexed']}")
    print(f"Documents Failed: {stats['numberOfDocumentsFailed']}")

# Wait for completion
import time

while True:
    status = bedrock_agent.get_ingestion_job(
        knowledgeBaseId=knowledge_base_id,
        dataSourceId=data_source_id,
        ingestionJobId=job_id
    )

    current_status = status['ingestionJob']['status']

    if current_status in ['COMPLETE', 'FAILED']:
        print(f"Ingestion job {current_status}")
        break

    print(f"Status: {current_status}, waiting...")
    time.sleep(30)
```

### 3. List Ingestion Jobs

```python
list_response = bedrock_agent.list_ingestion_jobs(
    knowledgeBaseId=knowledge_base_id,
    dataSourceId=data_source_id,
    maxResults=50
)

for job in list_response['ingestionJobSummaries']:
    print(f"Job ID: {job['ingestionJobId']}")
    print(f"Status: {job['status']}")
    print(f"Started: {job['startedAt']}")
    print(f"Updated: {job['updatedAt']}")
    print("---")
```

---

## Integration with Bedrock Agents

### 1. Agent with Knowledge Base Action

```python
bedrock_agent = boto3.client('bedrock-agent', region_name='us-east-1')

# Create agent with knowledge base
agent_response = bedrock_agent.create_agent(
    agentName='customer-support-agent',
    description='Customer support agent with knowledge base access',
    instruction='''You are a customer support agent. When answering questions:
1. Search the knowledge base for relevant information
2. Provide accurate answers based on retrieved context
3. Cite your sources
4. Admit when you don't know something''',
    foundationModel='anthropic.claude-3-sonnet-20240229-v1:0',
    agentResourceRoleArn='arn:aws:iam::123456789012:role/BedrockAgentRole'
)

agent_id = agent_response['agent']['agentId']

# Associate knowledge base with agent
kb_association = bedrock_agent.associate_agent_knowledge_base(
    agentId=agent_id,
    agentVersion='DRAFT',
    knowledgeBaseId='KB123456',
    description='Company documentation knowledge base',
    knowledgeBaseState='ENABLED'
)

# Prepare and create alias
bedrock_agent.prepare_agent(agentId=agent_id)

alias_response = bedrock_agent.create_agent_alias(
    agentId=agent_id,
    agentAliasName='production',
    description='Production alias'
)

agent_alias_id = alias_response['agentAlias']['agentAliasId']

# Invoke agent (automatically queries knowledge base)
bedrock_agent_runtime = boto3.client('bedrock-agent-runtime', region_name='us-east-1')

response = bedrock_agent_runtime.invoke_agent(
    agentId=agent_id,
    agentAliasId=agent_alias_id,
    sessionId='session-123',
    inputText='What is our return policy for defective products?'
)

for event in response['completion']:
    if 'chunk' in event:
        chunk = event['chunk']
        print(chunk['bytes'].decode())
```

### 2. Agent with Multiple Knowledge Bases

```python
# Associate multiple knowledge bases
bedrock_agent.associate_agent_knowledge_base(
    agentId=agent_id,
    agentVersion='DRAFT',
    knowledgeBaseId='KB-PRODUCT-DOCS',
    description='Product documentation'
)

bedrock_agent.associate_agent_knowledge_base(
    agentId=agent_id,
    agentVersion='DRAFT',
    knowledgeBaseId='KB-SUPPORT-ARTICLES',
    description='Support knowledge articles'
)

bedrock_agent.associate_agent_knowledge_base(
    agentId=agent_id,
    agentVersion='DRAFT',
    knowledgeBaseId='KB-COMPANY-POLICIES',
    description='Company policies and procedures'
)

# Agent automatically searches all knowledge bases and combines results
```

---

## Best Practices

### 1. Chunking Strategy Selection

**Decision Framework**:

1. **Simple, uniform documents** → Fixed-size chunking
   - Blog posts, articles, simple FAQs
   - Fast, predictable, cost-effective

2. **Documents without clear boundaries** → Semantic chunking
   - Legal documents, contracts, academic papers
   - Preserves semantic meaning, better accuracy
   - Consider additional cost

3. **Nested, hierarchical documents** → Hierarchical chunking
   - Technical manuals, product docs, research papers
   - Best balance of precision and context
   - Optimal for complex structures

4. **Specialized formats** → Custom Lambda chunking
   - Medical records (HL7, FHIR), code docs, custom formats
   - Complete control, domain expertise
   - Higher operational complexity

**Tuning Guidelines**:

- **Fixed-size**: Start with 512 tokens, 20% overlap
- **Semantic**: Start with 300 tokens, bufferSize=1, threshold=95%
- **Hierarchical**: Parent 1500 tokens, child 300 tokens, overlap 60 tokens
- **Custom**: Test extensively with domain experts

### 2. Retrieval Optimization

**Number of Results**:
- Start with 5-10 results
- Increase if answers lack detail
- Decrease if too much noise

**Search Type**:
- **SEMANTIC**: Pure vector similarity (faster, good for conceptual queries)
- **HYBRID**: Vector + keyword (better recall, recommended for production)

**Use Hybrid Search** when:
- Queries contain specific terms or names
- Need to match exact keywords
- Domain has specialized vocabulary

**Use Semantic Search** when:
- Purely conceptual queries
- Prioritizing speed over perfect recall
- Well-embedded domain knowledge

**Metadata Filters**:
- Always use when applicable
- Dramatically improves precision
- Reduces retrieval latency
- Examples: document_type, publish_date, category, author

### 3. Cost Optimization

**S3 Vectors**:
- Use for large-scale knowledge bases (millions of chunks)
- Up to 90% cost savings vs. OpenSearch
- Ideal for cost-sensitive applications
- Trade-off: Slightly higher latency

**Semantic Chunking**:
- Incurs foundation model costs during ingestion
- Consider cost vs. accuracy benefit
- May not be worth it for simple documents
- Best for complex, high-value content

**Ingestion Frequency**:
- Schedule ingestion during off-peak hours
- Use incremental updates when possible
- Don't re-ingest unchanged documents

**Model Selection**:
- Use smaller embedding models when accuracy permits
- Titan Embed Text v2 is cost-effective
- Consider Cohere Embed for multilingual

**Token Usage**:
- Monitor generation token usage
- Set appropriate maxTokens limits
- Use prompt templates to control verbosity

### 4. Session Management

**Always Reuse Sessions**:
- Pass `sessionId` for follow-up turns
- Bedrock handles context automatically
- No manual conversation history needed

**Session Lifecycle**:
- Sessions expire after inactivity (default: 60 minutes)
- Create new session for unrelated conversations
- Use unique sessionId per user/conversation

**Context Limits**:
- Monitor conversation length
- Long sessions may hit context limits
- Consider summarization for very long conversations

### 5. GraphRAG with Neptune

**When to Use**:
- Interconnected knowledge domains
- Relationship-aware queries
- Need for explainability
- Complex knowledge graphs

**Benefits**:
- Automatic graph creation
- Improved accuracy through relationships
- Comprehensive answers
- Explainable results

**Considerations**:
- Higher setup complexity
- Neptune Analytics costs
- Best for domains with rich relationships

### 6. Data Source Management

**S3 Best Practices**:
- Organize with clear prefixes
- Use inclusion/exclusion filters
- Maintain consistent metadata
- Version documents when updating

**Web Crawler**:
- Set appropriate rate limits
- Use robots.txt for guidance
- Monitor for broken links
- Schedule regular re-crawls

**Confluence/SharePoint**:
- Filter by spaces/sites
- Exclude archived content
- Use fine-grained permissions
- Schedule incremental syncs

**Metadata Enrichment**:
- Add custom metadata to documents
- Include: document_type, publish_date, category, author, version
- Enables powerful filtering
- Improves retrieval precision

### 7. Monitoring and Debugging

**Enable CloudWatch Logs**:
```python
# Monitor retrieval quality
# Track: query latency, retrieval scores, generation quality
# Set alarms for: high latency, low scores, high error rates
```

**Test Retrieval Quality**:
```python
# Use retrieve API to debug
response = bedrock_agent_runtime.retrieve(
    knowledgeBaseId='KB123456',
    retrievalQuery={'text': 'test query'}
)

# Analyze retrieval scores
for result in response['retrievalResults']:
    print(f"Score: {result['score']}")
    print(f"Content preview: {result['content']['text'][:200]}")
```

**Common Issues**:

1. **Low Retrieval Scores**:
   - Check chunking strategy
   - Verify embedding model
   - Ensure documents are properly ingested
   - Consider semantic or hierarchical chunking

2. **Irrelevant Results**:
   - Add metadata filters
   - Use hybrid search
   - Refine chunking strategy
   - Increase numberOfResults

3. **Missing Information**:
   - Verify data source configuration
   - Check ingestion job status
   - Ensure documents are not excluded by filters
   - Increase numberOfResults

4. **Slow Retrieval**:
   - Use metadata filters to narrow scope
   - Optimize vector database configuration
   - Consider S3 Vectors for cost over latency
   - Reduce numberOfResults

### 8. Security Best Practices

**IAM Permissions**:
- Use least privilege for Knowledge Base role
- Separate roles for data sources, ingestion, retrieval
- Enable VPC endpoints for private connectivity

**Data Encryption**:
- All data encrypted at rest (AWS KMS)
- Data encrypted in transit (TLS)
- Use customer-managed KMS keys for compliance

**Access Control**:
- Use IAM policies to control who can query
- Implement fine-grained access control
- Monitor access with CloudTrail

**PII Handling**:
- Use Bedrock Guardrails for PII redaction
- Implement data masking for sensitive fields
- Consider custom Lambda for advanced PII handling

---

## Complete Production Example

### End-to-End RAG Application

```python
import boto3
import json
from typing import List, Dict, Optional

class BedrockKnowledgeBaseRAG:
    """Production RAG application with Amazon Bedrock Knowledge Bases"""

    def __init__(self, region_name: str = 'us-east-1'):
        self.bedrock_agent = boto3.client('bedrock-agent', region_name=region_name)
        self.bedrock_agent_runtime = boto3.client('bedrock-agent-runtime', region_name=region_name)

    def create_knowledge_base(
        self,
        name: str,
        description: str,
        role_arn: str,
        vector_store_config: Dict,
        embedding_model: str = 'amazon.titan-embed-text-v2:0'
    ) -> str:
        """Create knowledge base with vector store"""

        response = self.bedrock_agent.create_knowledge_base(
            name=name,
            description=description,
            roleArn=role_arn,
            knowledgeBaseConfiguration={
                'type': 'VECTOR',
                'vectorKnowledgeBaseConfiguration': {
                    'embeddingModelArn': f'arn:aws:bedrock:us-east-1::foundation-model/{embedding_model}'
                }
            },
            storageConfiguration=vector_store_config
        )

        return response['knowledgeBase']['knowledgeBaseId']

    def add_s3_data_source(
        self,
        knowledge_base_id: str,
        name: str,
        bucket_arn: str,
        inclusion_prefixes: List[str],
        chunking_strategy: str = 'FIXED_SIZE',
        chunking_config: Optional[Dict] = None
    ) -> str:
        """Add S3 data source with chunking configuration"""

        if chunking_config is None:
            chunking_config = {
                'maxTokens': 512,
                'overlapPercentage': 20
            }

        vector_ingestion_config = {
            'chunkingConfiguration': {
                'chunkingStrategy': chunking_strategy
            }
        }

        if chunking_strategy == 'FIXED_SIZE':
            vector_ingestion_config['chunkingConfiguration']['fixedSizeChunkingConfiguration'] = chunking_config
        elif chunking_strategy == 'SEMANTIC':
            vector_ingestion_config['chunkingConfiguration']['semanticChunkingConfiguration'] = chunking_config
        elif chunking_strategy == 'HIERARCHICAL':
            vector_ingestion_config['chunkingConfiguration']['hierarchicalChunkingConfiguration'] = chunking_config

        response = self.bedrock_agent.create_data_source(
            knowledgeBaseId=knowledge_base_id,
            name=name,
            description=f'S3 data source: {name}',
            dataSourceConfiguration={
                'type': 'S3',
                's3Configuration': {
                    'bucketArn': bucket_arn,
                    'inclusionPrefixes': inclusion_prefixes
                }
            },
            vectorIngestionConfiguration=vector_ingestion_config
        )

        return response['dataSource']['dataSourceId']

    def ingest_data(self, knowledge_base_id: str, data_source_id: str) -> str:
        """Start ingestion job and wait for completion"""

        import time

        # Start ingestion
        response = self.bedrock_agent.start_ingestion_job(
            knowledgeBaseId=knowledge_base_id,
            dataSourceId=data_source_id,
            description='Automated ingestion'
        )

        job_id = response['ingestionJob']['ingestionJobId']

        # Wait for completion
        while True:
            status_response = self.bedrock_agent.get_ingestion_job(
                knowledgeBaseId=knowledge_base_id,
                dataSourceId=data_source_id,
                ingestionJobId=job_id
            )

            status = status_response['ingestionJob']['status']

            if status == 'COMPLETE':
                print(f"Ingestion completed successfully")
                if 'statistics' in status_response['ingestionJob']:
                    stats = status_response['ingestionJob']['statistics']
                    print(f"Documents indexed: {stats.get('numberOfDocumentsIndexed', 0)}")
                break
            elif status == 'FAILED':
                print(f"Ingestion failed")
                break

            print(f"Ingestion status: {status}")
            time.sleep(30)

        return job_id

    def query(
        self,
        knowledge_base_id: str,
        query: str,
        model_arn: str = 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0',
        num_results: int = 5,
        search_type: str = 'HYBRID',
        metadata_filter: Optional[Dict] = None,
        session_id: Optional[str] = None
    ) -> Dict:
        """Query knowledge base with retrieve and generate"""

        retrieval_config = {
            'type': 'KNOWLEDGE_BASE',
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': knowledge_base_id,
                'modelArn': model_arn,
                'retrievalConfiguration': {
                    'vectorSearchConfiguration': {
                        'numberOfResults': num_results,
                        'overrideSearchType': search_type
                    }
                },
                'generationConfiguration': {
                    'inferenceConfig': {
                        'textInferenceConfig': {
                            'temperature': 0.7,
                            'maxTokens': 2048
                        }
                    }
                }
            }
        }

        # Add metadata filter if provided
        if metadata_filter:
            retrieval_config['knowledgeBaseConfiguration']['retrievalConfiguration']['vectorSearchConfiguration']['filter'] = metadata_filter

        # Build request
        request = {
            'input': {'text': query},
            'retrieveAndGenerateConfiguration': retrieval_config
        }

        # Add session if provided
        if session_id:
            request['sessionId'] = session_id

        response = self.bedrock_agent_runtime.retrieve_and_generate(**request)

        return {
            'answer': response['output']['text'],
            'citations': response.get('citations', []),
            'session_id': response['sessionId']
        }

    def multi_turn_conversation(
        self,
        knowledge_base_id: str,
        queries: List[str],
        model_arn: str = 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0'
    ) -> List[Dict]:
        """Execute multi-turn conversation with context"""

        session_id = None
        conversation = []

        for query in queries:
            result = self.query(
                knowledge_base_id=knowledge_base_id,
                query=query,
                model_arn=model_arn,
                session_id=session_id
            )

            session_id = result['session_id']

            conversation.append({
                'query': query,
                'answer': result['answer'],
                'citations': result['citations']
            })

        return conversation


# Example Usage
if __name__ == '__main__':
    rag = BedrockKnowledgeBaseRAG(region_name='us-east-1')

    # Create knowledge base
    kb_id = rag.create_knowledge_base(
        name='production-docs-kb',
        description='Production documentation knowledge base',
        role_arn='arn:aws:iam::123456789012:role/BedrockKBRole',
        vector_store_config={
            'type': 'OPENSEARCH_SERVERLESS',
            'opensearchServerlessConfiguration': {
                'collectionArn': 'arn:aws:aoss:us-east-1:123456789012:collection/kb-collection',
                'vectorIndexName': 'bedrock-kb-index',
                'fieldMapping': {
                    'vectorField': 'bedrock-knowledge-base-default-vector',
                    'textField': 'AMAZON_BEDROCK_TEXT_CHUNK',
                    'metadataField': 'AMAZON_BEDROCK_METADATA'
                }
            }
        }
    )

    # Add data source
    ds_id = rag.add_s3_data_source(
        knowledge_base_id=kb_id,
        name='technical-docs',
        bucket_arn='arn:aws:s3:::my-docs-bucket',
        inclusion_prefixes=['docs/'],
        chunking_strategy='HIERARCHICAL',
        chunking_config={
            'levelConfigurations': [
                {'maxTokens': 1500},
                {'maxTokens': 300}
            ],
            'overlapTokens': 60
        }
    )

    # Ingest data
    rag.ingest_data(kb_id, ds_id)

    # Single query
    result = rag.query(
        knowledge_base_id=kb_id,
        query='What are the best practices for RAG applications?',
        metadata_filter={
            'equals': {
                'key': 'document_type',
                'value': 'best_practices'
            }
        }
    )

    print(f"Answer: {result['answer']}")
    print(f"\nSources:")
    for citation in result['citations']:
        for ref in citation['retrievedReferences']:
            print(f"  - {ref['location']}")

    # Multi-turn conversation
    conversation = rag.multi_turn_conversation(
        knowledge_base_id=kb_id,
        queries=[
            'What is hierarchical chunking?',
            'When should I use it?',
            'What are the configuration parameters?'
        ]
    )

    for turn in conversation:
        print(f"\nQ: {turn['query']}")
        print(f"A: {turn['answer']}")
```

---

## Related Skills

### Amazon Bedrock Core Skills
- **bedrock-guardrails**: Content safety, PII redaction, hallucination detection
- **bedrock-agents**: Agentic workflows with tool use and knowledge bases
- **bedrock-flows**: Visual workflow builder for generative AI
- **bedrock-model-customization**: Fine-tuning, reinforcement fine-tuning, distillation
- **bedrock-prompt-management**: Prompt versioning and deployment

### AWS Infrastructure Skills
- **opensearch-serverless**: Vector database configuration and management
- **neptune-analytics**: GraphRAG configuration and queries
- **s3-management**: S3 bucket configuration for data sources and vectors
- **iam-bedrock**: IAM roles and policies for Knowledge Bases

### Observability Skills
- **cloudwatch-bedrock-monitoring**: Monitor Knowledge Bases metrics and logs
- **bedrock-cost-optimization**: Track and optimize Knowledge Bases costs

---

## Additional Resources

### Official Documentation
- [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/)
- [Knowledge Bases User Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)
- [Chunking Strategies](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-chunking.html)
- [Boto3 Knowledge Bases API](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent.html)

### Best Practices
- [Building Cost-Effective RAG with S3 Vectors](https://aws.amazon.com/blogs/machine-learning/building-cost-effective-rag-applications-with-amazon-bedrock-knowledge-bases-and-amazon-s3-vectors/)
- [Advanced Parsing and Chunking](https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-knowledge-bases-now-supports-advanced-parsing-chunking-and-query-reformulation-giving-greater-control-of-accuracy-in-rag-based-applications/)

### Research Document
- `/mnt/c/data/github/skrillz/AMAZON-BEDROCK-COMPREHENSIVE-RESEARCH-2025.md` - Section 2 (Complete Knowledge Bases research)
