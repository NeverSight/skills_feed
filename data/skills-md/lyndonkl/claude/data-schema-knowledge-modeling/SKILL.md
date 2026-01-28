---
name: data-schema-knowledge-modeling
description: Use when designing database schemas, need to model domain entities and relationships clearly, building knowledge graphs or ontologies, creating API data models, defining system boundaries and invariants, migrating between data models, establishing taxonomies or hierarchies, user mentions "schema", "data model", "entities", "relationships", "ontology", "knowledge graph", or when scattered/inconsistent data structures need formalization.
---

# Data Schema & Knowledge Modeling

## Table of Contents
- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [What Is It](#what-is-it)
- [Workflow](#workflow)
- [Schema Types](#schema-types)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Purpose

Create rigorous, validated models of entities, relationships, and constraints that enable correct system implementation, knowledge representation, and semantic reasoning.

## When to Use

**Invoke this skill when you need to:**
- Design database schema (SQL, NoSQL, graph) for new application
- Model complex domain with many entities and relationships
- Build knowledge graph or ontology for semantic search/reasoning
- Define API data models and contracts
- Create taxonomies or classification hierarchies
- Establish data governance and canonical models
- Migrate legacy schemas to modern architectures
- Resolve ambiguity in domain concepts and relationships
- Enable data integration across systems
- Document system invariants and business rules

**Common trigger phrases:**
- "Design a schema for..."
- "Model the entities and relationships"
- "Create a knowledge graph"
- "What's the data model?"
- "Define the ontology"
- "How should we structure this data?"
- "Map relationships between..."
- "Design the API data model"

## What Is It

**Data schema & knowledge modeling** is the process of formally defining:

1. **Entities** - Things that exist (User, Product, Order, Organization)
2. **Attributes** - Properties of entities (name, price, status, createdAt)
3. **Relationships** - Connections between entities (User owns Order, Product belongsTo Category)
4. **Constraints** - Rules and invariants (unique email, price > 0, one primary address)
5. **Cardinality** - How many of each (one-to-many, many-to-many)

**Quick example:** E-commerce schema:
- **Entities**: User, Product, Order, Cart, Payment
- **Relationships**: User has many Orders, Order contains many Products (via OrderItems), User has one Cart
- **Constraints**: Email must be unique, Order total matches sum of OrderItems, Payment amount equals Order total
- **Result**: Unambiguous model that prevents data inconsistencies

## Workflow

Copy this checklist and track your progress:

```
Data Schema & Knowledge Modeling Progress:
- [ ] Step 1: Gather domain requirements and scope
- [ ] Step 2: Identify entities and attributes
- [ ] Step 3: Define relationships and cardinality
- [ ] Step 4: Specify constraints and invariants
- [ ] Step 5: Validate and document the model
```

**Step 1: Gather domain requirements and scope**

Ask user for domain description, core use cases (what queries/operations will this support), existing data (if migration/integration), performance/scale requirements, and technology constraints (SQL vs NoSQL vs graph database). Understanding use cases shapes the model - OLTP vs OLAP vs graph traversal require different designs. See [Schema Types](#schema-types) for guidance.

**Step 2: Identify entities and attributes**

Extract nouns from requirements (those are candidate entities). For each entity, list attributes with types and nullability. Use [resources/template.md](resources/template.md) for systematic entity identification. Verify each entity represents a distinct concept with independent lifecycle. Document entity purpose and examples.

**Step 3: Define relationships and cardinality**

Map connections between entities (one-to-one, one-to-many, many-to-many). For many-to-many, identify junction tables/entities. Specify relationship directionality and optionality (can X exist without Y?). Use [resources/methodology.md](resources/methodology.md) for complex relationship patterns like hierarchies, polymorphic associations, and temporal relationships.

**Step 4: Specify constraints and invariants**

Define uniqueness constraints, foreign key relationships, check constraints, and business rules. Document domain invariants (rules that must ALWAYS be true). Identify derived/computed attributes vs stored. Use [resources/methodology.md](resources/methodology.md) for advanced constraint patterns and validation strategies.

**Step 5: Validate and document the model**

Create `data-schema-knowledge-modeling.md` file with complete schema definition. Validate against use cases - can the schema support required queries/operations? Check for normalization (eliminate redundancy) or denormalization (optimize for specific queries). Self-assess using [resources/evaluators/rubric_data_schema_knowledge_modeling.json](resources/evaluators/rubric_data_schema_knowledge_modeling.json). Minimum standard: Average score ≥ 3.5.

## Schema Types

Choose based on use case and technology:

**Relational (SQL) Schema**
- **Best for:** Transactional systems (OLTP), strong consistency, complex queries with joins
- **Pattern:** Normalized tables, foreign keys, ACID transactions
- **Example use cases:** E-commerce orders, banking transactions, HR systems
- **Key decision:** Normalization level (3NF for consistency vs denormalized for read performance)

**Document/NoSQL Schema**
- **Best for:** Flexible/evolving structure, high write throughput, denormalized reads
- **Pattern:** Nested documents, embedded relationships, no joins
- **Example use cases:** Content management, user profiles, event logs
- **Key decision:** Embed vs reference (embed for 1-to-few, reference for 1-to-many)

**Graph Schema (Ontology)**
- **Best for:** Complex relationships, traversal queries, semantic reasoning, knowledge graphs
- **Pattern:** Nodes (entities), edges (relationships), properties on both
- **Example use cases:** Social networks, fraud detection, recommendation engines, scientific research
- **Key decision:** Property graph vs RDF triples

**Event/Time-Series Schema**
- **Best for:** Audit logs, metrics, IoT data, append-only data
- **Pattern:** Immutable events, time-based partitioning, aggregation tables
- **Example use cases:** User activity tracking, monitoring, financial transactions
- **Key decision:** Raw events vs pre-aggregated summaries

**Dimensional (Data Warehouse) Schema**
- **Best for:** Analytics (OLAP), aggregations, historical reporting
- **Pattern:** Fact tables + dimension tables (star/snowflake schema)
- **Example use cases:** Business intelligence, sales analytics, customer 360
- **Key decision:** Star schema (denormalized) vs snowflake (normalized dimensions)

## Common Patterns

**Pattern: Entity Lifecycle Modeling**
Track entity state changes explicitly. Example: Order (draft → pending → confirmed → shipped → delivered → completed/cancelled). Include status field, timestamps for each state, and transitions table if history needed.

**Pattern: Soft Deletes**
Never physically delete records - add `deletedAt` timestamp. Allows data recovery, audit compliance, and referential integrity. Filter `WHERE deletedAt IS NULL` in queries.

**Pattern: Polymorphic Associations**
Entity relates to multiple types. Example: Comment can be on Post or Photo. Options: (1) separate foreign keys (commentableType + commentableId), (2) junction tables per type, (3) single table inheritance.

**Pattern: Temporal/Historical Data**
Track changes over time. Options: (1) Effective/expiry dates per record, (2) separate history table, (3) event sourcing (store all changes as events). Choose based on query patterns.

**Pattern: Multi-tenancy**
Isolate data per customer. Options: (1) Separate databases (strong isolation), (2) Shared schema with tenantId column (efficient), (3) Separate schemas in same DB (balance). Add tenantId to all queries if shared.

**Pattern: Hierarchies**
Model trees/nested structures. Options: (1) Adjacency list (parentId), (2) Nested sets (left/right values), (3) Path enumeration (materialized path), (4) Closure table (all ancestor-descendant pairs). Trade-offs between read/write performance.

## Guardrails

**✓ Do:**
- Start with use cases - schema serves queries/operations
- Normalize first, then denormalize for specific performance needs
- Document all constraints and invariants explicitly
- Use meaningful, consistent naming conventions
- Consider future evolution - design for extensibility
- Validate model against ALL required use cases
- Model the real world accurately (don't force fit to technology)

**✗ Don't:**
- Design schema in isolation from use cases
- Premature optimization (denormalize before measuring)
- Skip constraint definitions (leads to data corruption)
- Use generic names (data, value, thing) - be specific
- Ignore cardinality and nullability
- Model implementation details in domain entities
- Forget about data migration path from existing systems
- Create circular dependencies between entities

## Quick Reference

**Resources:**
- `resources/template.md` - Structured process for entity identification, relationship mapping, and constraint definition
- `resources/methodology.md` - Advanced patterns: temporal modeling, graph ontologies, schema evolution, normalization strategies
- `resources/examples/` - Worked examples showing complete schema designs with validation
- `resources/evaluators/rubric_data_schema_knowledge_modeling.json` - Quality assessment before delivery

**When to choose which resource:**
- Simple domain (< 10 entities) → Start with template
- Complex domain or graph/ontology → Study methodology for advanced patterns
- Need to see examples → Review examples folder
- Before delivering to user → Always validate with rubric

**Expected deliverable:**
`data-schema-knowledge-modeling.md` file containing: domain description, complete entity definitions with attributes and types, relationship mappings with cardinality, constraint specifications, diagram (ERD/graph visualization), validation against use cases, and implementation notes.

**Common schema notations:**
- **ERD** (Entity-Relationship Diagram): Visual representation of entities and relationships
- **UML Class Diagram**: Object-oriented view with inheritance and associations
- **Graph Diagram**: Nodes and edges for graph databases
- **JSON Schema**: API/document structure with validation rules
- **SQL DDL**: Executable CREATE TABLE statements
- **Ontology (OWL/RDF)**: Semantic web knowledge representation
