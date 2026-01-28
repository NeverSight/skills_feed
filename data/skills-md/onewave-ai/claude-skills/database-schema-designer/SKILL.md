---
name: database-schema-designer
description: Design optimized database schemas for SQL and NoSQL databases including tables, relationships, indexes, and constraints. Creates ERD diagrams, migration scripts, and data modeling best practices. Use when users need database design, schema optimization, or data architecture planning.
---

# Database Schema Designer

Design optimized, scalable database schemas with proper relationships and indexes.

## Instructions

When a user needs database schema design:

1. **Gather Requirements**:
   - What type of database (PostgreSQL, MySQL, MongoDB, etc.)?
   - What is the application domain?
   - What are the main entities/resources?
   - What queries will be most common?
   - Expected data volume and growth?
   - Performance requirements?
   - Specific constraints or compliance needs?

2. **Design Schema Following Best Practices**:

   **For SQL Databases**:
   - Identify entities and their attributes
   - Define primary keys (prefer UUIDs for distributed systems)
   - Establish relationships (1:1, 1:N, N:M)
   - Normalize to 3NF (unless denormalization needed for performance)
   - Add appropriate indexes
   - Define foreign key constraints
   - Include timestamps (created_at, updated_at)
   - Add soft delete flags if needed
   - Plan for data archival

   **For NoSQL Databases**:
   - Design for access patterns (query-first approach)
   - Embed vs reference decision
   - Plan for denormalization
   - Design indexes for common queries
   - Consider document size limits
   - Plan for eventual consistency

3. **Generate Complete Schema**:

   **SQL Schema Output**:
   ```sql
   -- [Entity Name] Table
   -- Purpose: [Description]

   CREATE TABLE [table_name] (
     id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
     [field_name] [TYPE] [CONSTRAINTS],
     created_at TIMESTAMP NOT NULL DEFAULT NOW(),
     updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
     deleted_at TIMESTAMP
   );

   -- Indexes
   CREATE INDEX idx_[table]_[field] ON [table]([field]);
   CREATE INDEX idx_[table]_[field1]_[field2] ON [table]([field1], [field2]);

   -- Foreign Keys
   ALTER TABLE [child_table]
     ADD CONSTRAINT fk_[constraint_name]
     FOREIGN KEY ([foreign_key_field])
     REFERENCES [parent_table](id)
     ON DELETE CASCADE;
   ```

   **NoSQL Schema Output** (MongoDB example):
   ```javascript
   // [Collection Name]
   // Purpose: [Description]

   {
     _id: ObjectId,
     [field_name]: [type],

     // Embedded document
     [embedded_object]: {
       field1: type,
       field2: type
     },

     // Reference
     [related_id]: ObjectId,  // Ref to [other_collection]

     created_at: ISODate,
     updated_at: ISODate
   }

   // Indexes
   db.[collection].createIndex({ field: 1 })
   db.[collection].createIndex({ field1: 1, field2: -1 })
   db.[collection].createIndex({ field: "text" })  // Text search
   ```

4. **Create Entity Relationship Diagram** (text format):
   ```
   ┌─────────────────────┐
   │      users          │
   ├─────────────────────┤
   │ id (PK)             │
   │ email (UNIQUE)      │
   │ name                │
   │ created_at          │
   └──────────┬──────────┘
              │
              │ 1:N
              │
   ┌──────────▼──────────┐
   │      posts          │
   ├─────────────────────┤
   │ id (PK)             │
   │ user_id (FK)        │
   │ title               │
   │ content             │
   │ created_at          │
   └──────────┬──────────┘
              │
              │ N:M (via post_tags)
              │
   ┌──────────▼──────────┐
   │       tags          │
   ├─────────────────────┤
   │ id (PK)             │
   │ name (UNIQUE)       │
   └─────────────────────┘
   ```

5. **Provide Migration Scripts**:
   ```sql
   -- Migration: create_users_table
   -- Date: 2024-01-15

   BEGIN;

   CREATE TABLE users (
     id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
     email VARCHAR(255) NOT NULL UNIQUE,
     name VARCHAR(255) NOT NULL,
     password_hash VARCHAR(255) NOT NULL,
     created_at TIMESTAMP NOT NULL DEFAULT NOW(),
     updated_at TIMESTAMP NOT NULL DEFAULT NOW()
   );

   CREATE INDEX idx_users_email ON users(email);
   CREATE INDEX idx_users_created_at ON users(created_at);

   COMMIT;
   ```

   ```sql
   -- Rollback
   BEGIN;
   DROP TABLE users;
   COMMIT;
   ```

6. **Format Complete Output**:
   ```
   🗄️ DATABASE SCHEMA DESIGN
   Database: [PostgreSQL/MySQL/MongoDB/etc.]
   Domain: [Application type]

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   📋 ENTITY RELATIONSHIP DIAGRAM
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   [ASCII ERD]

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   📊 TABLE DEFINITIONS
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   [SQL CREATE TABLE statements]

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   🔗 RELATIONSHIPS
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   [Foreign key constraints]

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ⚡ INDEXES
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   [Index definitions with rationale]

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   🔄 MIGRATION SCRIPTS
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   [Up and down migrations]

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   💡 OPTIMIZATION NOTES
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   Performance Considerations:
   • [Index strategy]
   • [Partitioning recommendations]
   • [Denormalization opportunities]

   Scaling Strategy:
   • [Sharding approach]
   • [Read replicas]
   • [Caching layer]

   Data Integrity:
   • [Constraint strategy]
   • [Validation rules]
   • [Audit logging]
   ```

7. **Schema Design Best Practices**:

   **Naming Conventions**:
   - Use snake_case for table and column names
   - Pluralize table names (users, posts)
   - Use descriptive foreign key names (user_id, not uid)
   - Prefix indexes (idx_table_column)
   - Prefix constraints (fk_, uk_, ck_)

   **Data Types**:
   - Use appropriate types (INT vs BIGINT, VARCHAR vs TEXT)
   - Consider storage size
   - Use ENUM for fixed sets of values
   - Use JSON/JSONB for flexible attributes
   - Use proper date/time types (TIMESTAMP vs DATETIME)

   **Indexes**:
   - Index foreign keys
   - Index columns in WHERE clauses
   - Composite indexes for multi-column queries
   - Consider covering indexes
   - Monitor index usage and remove unused ones

   **Relationships**:
   - Always use foreign keys in relational DBs
   - Cascade deletes where appropriate
   - Consider soft deletes for audit trails
   - Use junction tables for many-to-many

   **Performance**:
   - Denormalize for read-heavy workloads
   - Partition large tables
   - Use materialized views for complex queries
   - Consider read replicas
   - Plan for archival of old data

## Example Triggers

- "Design a database schema for an e-commerce platform"
- "Create SQL tables for a blog system"
- "Help me design a MongoDB schema for a social network"
- "Optimize this database schema for performance"
- "Generate migration scripts for my schema"

## Output Quality

Ensure schemas:
- Follow normalization principles (unless deliberately denormalized)
- Include all necessary constraints
- Have appropriate indexes
- Use proper data types
- Include timestamps
- Have clear relationships
- Consider scalability
- Include migration scripts
- Follow naming conventions
- Are documented with comments
- Consider performance implications
- Include rollback capability

Generate production-ready, optimized database schemas that scale.
