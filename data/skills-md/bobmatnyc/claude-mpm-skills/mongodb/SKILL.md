---
name: mongodb
description: MongoDB - NoSQL document database with flexible schema design, aggregation pipelines, indexing strategies, and Spring Data integration
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Document-oriented NoSQL database with flexible schemas, powerful aggregation framework, horizontal scaling, and rich query language"
    when_to_use: "Building apps with flexible/evolving schemas, hierarchical data, real-time analytics, geospatial queries, or need horizontal scaling"
    quick_start: "1. Design documents (embedded vs referenced) 2. Create indexes for queries 3. Use aggregation for analytics 4. Implement proper connection pooling"
context_limit: 700
tags:
  - mongodb
  - nosql
  - database
  - document-database
  - aggregation
  - indexing
  - spring-data
  - schema-design
requires_tools: []
---

# MongoDB - Document Database Patterns

## Overview

MongoDB is a document-oriented NoSQL database that stores data in flexible, JSON-like documents. It excels at handling unstructured or semi-structured data, hierarchical relationships, and scenarios requiring horizontal scaling.

**Key Features**:
- Flexible schema (schemaless documents)
- Rich query language with secondary indexes
- Aggregation framework for analytics
- Horizontal scaling (sharding)
- Replica sets for high availability
- Change streams for real-time data
- Geospatial and full-text search

**When to Use MongoDB**:
- Rapidly evolving schemas
- Hierarchical/nested data (embedded documents)
- Real-time analytics with aggregation
- Geospatial applications
- Content management systems
- IoT data ingestion
- Catalog/inventory systems

**When NOT to Use MongoDB**:
- Complex multi-table joins (use RDBMS)
- ACID transactions across many documents (improved in 4.0+, but limited)
- Strict schema enforcement requirements

## Schema Design Fundamentals

### Document Structure

```javascript
// MongoDB document (BSON format)
{
  "_id": ObjectId("507f1f77bcf86cd799439011"),  // Primary key (auto-generated)
  "email": "alice@example.com",
  "name": "Alice Johnson",
  "profile": {                                   // Embedded document
    "bio": "Software developer",
    "avatar": "https://example.com/avatar.jpg",
    "social": {
      "twitter": "@alice",
      "github": "alice-dev"
    }
  },
  "tags": ["developer", "python", "mongodb"],    // Array field
  "createdAt": ISODate("2024-01-15T10:30:00Z"),
  "updatedAt": ISODate("2024-01-20T14:22:00Z")
}
```

### Embedded vs Referenced Documents

**Embedded (Denormalized)** - Store related data in same document:

```javascript
// Embedded: Good for 1:1 or 1:Few relationships
// User with embedded address
{
  "_id": ObjectId("..."),
  "name": "Alice",
  "address": {
    "street": "123 Main St",
    "city": "San Francisco",
    "zipCode": "94102"
  }
}

// Embedded: Order with line items (1:Many bounded)
{
  "_id": ObjectId("..."),
  "orderNumber": "ORD-2024-001",
  "customer": { "name": "Alice", "email": "alice@example.com" },
  "items": [
    { "productId": "SKU001", "name": "Widget", "quantity": 2, "price": 29.99 },
    { "productId": "SKU002", "name": "Gadget", "quantity": 1, "price": 49.99 }
  ],
  "total": 109.97
}
```

**When to Embed**:
- Data is queried together frequently
- Child data doesn't make sense without parent
- 1:1 or 1:Few relationships
- Child data is bounded (won't grow unbounded)
- Data doesn't need to be accessed independently

**Referenced (Normalized)** - Store references to other documents:

```javascript
// Referenced: Good for 1:Many unbounded or Many:Many
// User document
{
  "_id": ObjectId("user123"),
  "name": "Alice",
  "email": "alice@example.com"
}

// Posts collection (references user)
{
  "_id": ObjectId("post456"),
  "authorId": ObjectId("user123"),   // Reference to user
  "title": "MongoDB Schema Design",
  "content": "...",
  "commentCount": 42
}

// Comments collection (references post)
{
  "_id": ObjectId("comment789"),
  "postId": ObjectId("post456"),     // Reference to post
  "authorId": ObjectId("user999"),   // Reference to commenter
  "text": "Great article!",
  "createdAt": ISODate("2024-01-20T10:00:00Z")
}
```

**When to Reference**:
- Many:Many relationships
- 1:Many with unbounded growth (comments, logs)
- Data is accessed independently
- Document size would exceed 16MB limit
- Need atomic updates on referenced document

### Hybrid Pattern (Extended Reference)

```javascript
// Post with denormalized author info + reference
{
  "_id": ObjectId("post456"),
  "title": "MongoDB Best Practices",
  "content": "...",
  "author": {
    "_id": ObjectId("user123"),      // Reference for lookups
    "name": "Alice",                 // Denormalized for display
    "avatar": "https://..."          // Frequently needed fields
  },
  "commentCount": 42,
  "lastCommentAt": ISODate("...")
}
```

## Query Patterns

### Basic CRUD Operations

```javascript
// Find documents
db.users.find({ email: "alice@example.com" })
db.users.find({ age: { $gte: 18, $lte: 65 } })
db.users.find({ tags: { $in: ["developer", "designer"] } })

// Find with projection (select specific fields)
db.users.find(
  { status: "active" },
  { name: 1, email: 1, _id: 0 }  // Include name, email; exclude _id
)

// Find one
db.users.findOne({ email: "alice@example.com" })

// Insert
db.users.insertOne({ name: "Bob", email: "bob@example.com" })
db.users.insertMany([
  { name: "Charlie", email: "charlie@example.com" },
  { name: "Diana", email: "diana@example.com" }
])

// Update
db.users.updateOne(
  { email: "alice@example.com" },
  { $set: { name: "Alice Updated", updatedAt: new Date() } }
)

db.users.updateMany(
  { status: "inactive" },
  { $set: { archived: true } }
)

// Upsert (update or insert)
db.users.updateOne(
  { email: "new@example.com" },
  { $set: { name: "New User", createdAt: new Date() } },
  { upsert: true }
)

// Delete
db.users.deleteOne({ email: "bob@example.com" })
db.users.deleteMany({ status: "deleted" })
```

### Query Operators

```javascript
// Comparison
db.products.find({ price: { $gt: 100 } })        // Greater than
db.products.find({ price: { $gte: 100 } })       // Greater than or equal
db.products.find({ price: { $lt: 50 } })         // Less than
db.products.find({ price: { $lte: 50 } })        // Less than or equal
db.products.find({ price: { $ne: 0 } })          // Not equal
db.products.find({ category: { $in: ["A", "B"] } })   // In array
db.products.find({ category: { $nin: ["C", "D"] } })  // Not in array

// Logical
db.users.find({ $and: [{ age: { $gte: 18 } }, { status: "active" }] })
db.users.find({ $or: [{ role: "admin" }, { role: "moderator" }] })
db.users.find({ age: { $not: { $lt: 18 } } })

// Element
db.users.find({ middleName: { $exists: true } })  // Field exists
db.users.find({ age: { $type: "number" } })       // Field type

// Array
db.posts.find({ tags: "mongodb" })                // Contains element
db.posts.find({ tags: { $all: ["mongodb", "database"] } })  // Contains all
db.posts.find({ tags: { $size: 3 } })             // Array size
db.posts.find({ "tags.0": "featured" })           // First element

// Embedded documents
db.users.find({ "address.city": "San Francisco" })
db.users.find({ "profile.social.twitter": { $exists: true } })

// Regex
db.users.find({ name: { $regex: /^alice/i } })
db.users.find({ email: { $regex: /@example\.com$/ } })
```

### Update Operators

```javascript
// Field updates
db.users.updateOne(
  { _id: userId },
  {
    $set: { name: "New Name" },           // Set field value
    $unset: { temporaryField: "" },       // Remove field
    $rename: { oldName: "newName" },      // Rename field
    $inc: { loginCount: 1 },              // Increment
    $mul: { price: 1.1 },                 // Multiply
    $min: { lowestScore: 50 },            // Set if less than current
    $max: { highestScore: 100 },          // Set if greater than current
    $currentDate: { updatedAt: true }     // Set to current date
  }
)

// Array updates
db.posts.updateOne(
  { _id: postId },
  {
    $push: { tags: "new-tag" },           // Add to array
    $addToSet: { tags: "unique-tag" },    // Add if not exists
    $pop: { tags: 1 },                    // Remove last (-1 for first)
    $pull: { tags: "old-tag" },           // Remove specific value
    $pullAll: { tags: ["a", "b"] }        // Remove multiple values
  }
)

// Array with modifiers
db.posts.updateOne(
  { _id: postId },
  {
    $push: {
      comments: {
        $each: [comment1, comment2],      // Add multiple
        $sort: { createdAt: -1 },         // Sort after push
        $slice: -100                      // Keep only last 100
      }
    }
  }
)

// Positional update (update matched array element)
db.posts.updateOne(
  { _id: postId, "comments._id": commentId },
  { $set: { "comments.$.text": "Updated comment" } }
)

// Update all matching array elements
db.posts.updateOne(
  { _id: postId },
  { $set: { "comments.$[elem].read": true } },
  { arrayFilters: [{ "elem.userId": currentUserId }] }
)
```

## Indexing Strategies

### Index Types

```javascript
// Single field index
db.users.createIndex({ email: 1 })         // Ascending
db.users.createIndex({ createdAt: -1 })    // Descending

// Compound index
db.orders.createIndex({ customerId: 1, createdAt: -1 })

// Unique index
db.users.createIndex({ email: 1 }, { unique: true })

// Partial index (index subset of documents)
db.orders.createIndex(
  { createdAt: 1 },
  { partialFilterExpression: { status: "pending" } }
)

// TTL index (auto-delete old documents)
db.sessions.createIndex(
  { createdAt: 1 },
  { expireAfterSeconds: 3600 }  // Delete after 1 hour
)

// Text index (full-text search)
db.articles.createIndex({ title: "text", content: "text" })
// Query: db.articles.find({ $text: { $search: "mongodb tutorial" } })

// Geospatial index
db.locations.createIndex({ coordinates: "2dsphere" })
// Query: db.locations.find({
//   coordinates: {
//     $near: {
//       $geometry: { type: "Point", coordinates: [-122.4, 37.8] },
//       $maxDistance: 5000  // meters
//     }
//   }
// })

// Multikey index (for array fields - automatic)
db.posts.createIndex({ tags: 1 })

// Hashed index (for sharding)
db.users.createIndex({ email: "hashed" })
```

### Index Best Practices

```javascript
// ESR Rule for compound indexes: Equality, Sort, Range
// Query: find users where status = "active", sorted by createdAt, age > 18
// Index: { status: 1, createdAt: -1, age: 1 }
//        ^Equality   ^Sort          ^Range

// Covered queries (all fields in index)
db.users.createIndex({ email: 1, name: 1, status: 1 })
db.users.find(
  { email: "alice@example.com" },
  { name: 1, status: 1, _id: 0 }  // All fields from index
)
// Check with explain: "totalDocsExamined": 0

// Analyze query performance
db.users.find({ email: "alice@example.com" }).explain("executionStats")
// Look for:
// - IXSCAN (index scan) vs COLLSCAN (collection scan)
// - totalDocsExamined vs totalKeysExamined
// - executionTimeMillis

// List indexes
db.users.getIndexes()

// Drop index
db.users.dropIndex("email_1")
db.users.dropIndex({ email: 1, name: 1 })
```

## Aggregation Pipeline

### Pipeline Stages

```javascript
// Basic aggregation structure
db.orders.aggregate([
  { $match: { status: "completed" } },           // Filter (like WHERE)
  { $group: { _id: "$customerId", total: { $sum: "$amount" } } },  // Group
  { $sort: { total: -1 } },                      // Sort
  { $limit: 10 }                                 // Limit results
])

// Common stages
db.collection.aggregate([
  // $match - Filter documents
  { $match: { status: "active", createdAt: { $gte: ISODate("2024-01-01") } } },

  // $project - Reshape documents (include/exclude/compute fields)
  { $project: {
    name: 1,
    email: 1,
    fullName: { $concat: ["$firstName", " ", "$lastName"] },
    yearCreated: { $year: "$createdAt" }
  }},

  // $addFields - Add new fields (keeps existing)
  { $addFields: {
    totalPrice: { $multiply: ["$price", "$quantity"] }
  }},

  // $group - Group and aggregate
  { $group: {
    _id: "$category",
    count: { $sum: 1 },
    totalRevenue: { $sum: "$amount" },
    avgPrice: { $avg: "$price" },
    maxPrice: { $max: "$price" },
    products: { $push: "$name" },          // Collect into array
    uniqueTags: { $addToSet: "$tag" }      // Unique values
  }},

  // $sort
  { $sort: { totalRevenue: -1, count: 1 } },

  // $skip and $limit (pagination)
  { $skip: 20 },
  { $limit: 10 },

  // $unwind - Deconstruct array field
  { $unwind: "$tags" },
  // { tags: ["a", "b"] } becomes { tags: "a" }, { tags: "b" }

  // $lookup - Join collections
  { $lookup: {
    from: "users",
    localField: "authorId",
    foreignField: "_id",
    as: "author"
  }},
  { $unwind: "$author" },  // Convert single-element array to object

  // $facet - Multiple pipelines in parallel
  { $facet: {
    results: [{ $skip: 0 }, { $limit: 10 }],
    totalCount: [{ $count: "count" }]
  }}
])
```

### Real-World Aggregation Examples

```javascript
// Sales analytics by month
db.orders.aggregate([
  { $match: { status: "completed" } },
  { $group: {
    _id: {
      year: { $year: "$createdAt" },
      month: { $month: "$createdAt" }
    },
    totalSales: { $sum: "$amount" },
    orderCount: { $sum: 1 },
    avgOrderValue: { $avg: "$amount" }
  }},
  { $sort: { "_id.year": -1, "_id.month": -1 } }
])

// Top customers with order details
db.orders.aggregate([
  { $match: { createdAt: { $gte: ISODate("2024-01-01") } } },
  { $group: {
    _id: "$customerId",
    totalSpent: { $sum: "$amount" },
    orderCount: { $sum: 1 },
    lastOrder: { $max: "$createdAt" }
  }},
  { $sort: { totalSpent: -1 } },
  { $limit: 10 },
  { $lookup: {
    from: "customers",
    localField: "_id",
    foreignField: "_id",
    as: "customer"
  }},
  { $unwind: "$customer" },
  { $project: {
    customerName: "$customer.name",
    customerEmail: "$customer.email",
    totalSpent: 1,
    orderCount: 1,
    lastOrder: 1
  }}
])

// Product category performance with nested unwind
db.orders.aggregate([
  { $unwind: "$items" },
  { $lookup: {
    from: "products",
    localField: "items.productId",
    foreignField: "_id",
    as: "product"
  }},
  { $unwind: "$product" },
  { $group: {
    _id: "$product.category",
    totalRevenue: { $sum: { $multiply: ["$items.quantity", "$items.price"] } },
    unitsSold: { $sum: "$items.quantity" },
    uniqueProducts: { $addToSet: "$product._id" }
  }},
  { $addFields: {
    uniqueProductCount: { $size: "$uniqueProducts" }
  }},
  { $sort: { totalRevenue: -1 } }
])
```

## Transactions (MongoDB 4.0+)

```javascript
// Multi-document transaction
const session = client.startSession();

try {
  session.startTransaction();

  // Transfer money between accounts
  await accounts.updateOne(
    { _id: fromAccountId },
    { $inc: { balance: -amount } },
    { session }
  );

  await accounts.updateOne(
    { _id: toAccountId },
    { $inc: { balance: amount } },
    { session }
  );

  await transactions.insertOne(
    {
      from: fromAccountId,
      to: toAccountId,
      amount: amount,
      createdAt: new Date()
    },
    { session }
  );

  await session.commitTransaction();
} catch (error) {
  await session.abortTransaction();
  throw error;
} finally {
  session.endSession();
}
```

## Change Streams

```javascript
// Watch for changes in real-time
const changeStream = db.orders.watch([
  { $match: { "fullDocument.status": "pending" } }
]);

changeStream.on("change", (change) => {
  console.log("Change detected:", change.operationType);
  console.log("Document:", change.fullDocument);

  if (change.operationType === "insert") {
    // Process new pending order
    processNewOrder(change.fullDocument);
  }
});

// Resume from specific point (for fault tolerance)
const resumeToken = change._id;
const changeStream = db.orders.watch([], {
  resumeAfter: resumeToken,
  fullDocument: "updateLookup"  // Include full document on updates
});
```

## Spring Data MongoDB Integration

### Entity Class

```java
@Document(collection = "users")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class User {

    @Id
    private String id;  // Maps to _id

    @Indexed(unique = true)
    private String email;

    private String name;

    @Field("password_hash")  // Custom field name
    private String passwordHash;

    @DBRef  // Reference to another collection
    private List<Role> roles;

    private Address address;  // Embedded document

    private List<String> tags;

    @CreatedDate
    private LocalDateTime createdAt;

    @LastModifiedDate
    private LocalDateTime updatedAt;

    @Version
    private Long version;  // Optimistic locking
}

@Data
public class Address {
    private String street;
    private String city;
    private String zipCode;

    @GeoSpatialIndexed(type = GeoSpatialIndexType.GEO_2DSPHERE)
    private GeoJsonPoint location;
}
```

### Repository Interface

```java
public interface UserRepository extends MongoRepository<User, String> {

    // Derived queries
    Optional<User> findByEmail(String email);
    List<User> findByNameContainingIgnoreCase(String name);
    List<User> findByTagsContaining(String tag);

    // Custom query with @Query
    @Query("{ 'createdAt': { $gte: ?0 }, 'status': 'active' }")
    List<User> findActiveUsersCreatedAfter(LocalDateTime date);

    // Projection
    @Query(value = "{ 'email': ?0 }", fields = "{ 'name': 1, 'email': 1 }")
    Optional<UserSummary> findSummaryByEmail(String email);

    // Aggregation
    @Aggregation(pipeline = {
        "{ $match: { 'status': 'active' } }",
        "{ $group: { _id: '$country', count: { $sum: 1 } } }",
        "{ $sort: { count: -1 } }"
    })
    List<CountryStats> getActiveUsersByCountry();

    // Geospatial query
    List<User> findByAddressLocationNear(Point location, Distance distance);
}
```

### MongoTemplate for Complex Queries

```java
@Service
@RequiredArgsConstructor
public class UserService {

    private final MongoTemplate mongoTemplate;

    public List<User> searchUsers(UserSearchCriteria criteria) {
        Query query = new Query();

        if (criteria.getName() != null) {
            query.addCriteria(Criteria.where("name")
                .regex(criteria.getName(), "i"));
        }

        if (criteria.getTags() != null && !criteria.getTags().isEmpty()) {
            query.addCriteria(Criteria.where("tags")
                .in(criteria.getTags()));
        }

        if (criteria.getCreatedAfter() != null) {
            query.addCriteria(Criteria.where("createdAt")
                .gte(criteria.getCreatedAfter()));
        }

        query.with(Sort.by(Sort.Direction.DESC, "createdAt"));
        query.with(PageRequest.of(criteria.getPage(), criteria.getSize()));

        return mongoTemplate.find(query, User.class);
    }

    public AggregationResults<UserStats> getUserStatsByStatus() {
        Aggregation aggregation = Aggregation.newAggregation(
            Aggregation.match(Criteria.where("createdAt")
                .gte(LocalDateTime.now().minusMonths(1))),
            Aggregation.group("status")
                .count().as("count")
                .avg("loginCount").as("avgLogins"),
            Aggregation.sort(Sort.Direction.DESC, "count")
        );

        return mongoTemplate.aggregate(aggregation, "users", UserStats.class);
    }

    public void bulkUpdateStatus(List<String> userIds, String newStatus) {
        BulkOperations bulkOps = mongoTemplate.bulkOps(
            BulkOperations.BulkMode.UNORDERED, User.class);

        for (String userId : userIds) {
            Query query = Query.query(Criteria.where("_id").is(userId));
            Update update = Update.update("status", newStatus)
                .currentDate("updatedAt");
            bulkOps.updateOne(query, update);
        }

        bulkOps.execute();
    }
}
```

## Performance Optimization

### Connection Pooling

```java
// Spring Boot configuration
spring:
  data:
    mongodb:
      uri: mongodb://localhost:27017/mydb
      auto-index-creation: false  # Create indexes manually in production

# Connection pool settings (via URI)
# mongodb://localhost:27017/mydb?maxPoolSize=50&minPoolSize=10&maxIdleTimeMS=30000
```

### Query Optimization

```javascript
// Use projections to limit returned fields
db.users.find({ status: "active" }, { name: 1, email: 1 })

// Use hint to force specific index
db.users.find({ status: "active" }).hint({ status: 1, createdAt: -1 })

// Limit results for pagination
db.users.find().sort({ createdAt: -1 }).skip(20).limit(10)

// Use $exists: false for missing fields (can use index)
db.users.createIndex({ optionalField: 1 }, { sparse: true })
db.users.find({ optionalField: { $exists: true } })
```

### Schema Optimization

```javascript
// Avoid large arrays (cap at reasonable size)
// Use bucketing pattern for time-series data
{
  _id: "sensor1_2024-01-15",
  sensorId: "sensor1",
  date: ISODate("2024-01-15"),
  readings: [
    { ts: ISODate("..."), value: 23.5 },
    { ts: ISODate("..."), value: 24.1 },
    // ... up to N readings per bucket
  ],
  count: 288  // Track count for full bucket detection
}

// Pre-aggregate for reporting
{
  _id: "stats_2024-01",
  month: "2024-01",
  totalOrders: 1523,
  totalRevenue: 152300.50,
  avgOrderValue: 100.00,
  topProducts: ["SKU001", "SKU002", "SKU003"]
}
```

## Best Practices

### 1. Schema Design
```javascript
// Embed when: data is queried together, bounded arrays
// Reference when: unbounded arrays, many-to-many, independent access
// Use extended reference pattern for frequently accessed fields
```

### 2. Indexing
```javascript
// Create indexes for query patterns, not just fields
// Use compound indexes following ESR rule
// Monitor slow queries: db.setProfilingLevel(1, { slowms: 100 })
// Avoid indexing low-cardinality fields alone
```

### 3. Write Operations
```javascript
// Use bulk operations for multiple writes
// Avoid unbounded array growth
// Use write concern appropriate to durability needs
db.orders.insertOne(doc, { writeConcern: { w: "majority" } })
```

### 4. Read Operations
```javascript
// Always use projections to limit returned data
// Use explain() to verify index usage
// Prefer aggregation over multiple queries
// Use read preference for scaling reads
db.orders.find().readPref("secondaryPreferred")
```

### 5. Connection Management
```javascript
// Use connection pooling
// Set appropriate pool size (default: 100)
// Handle connection errors with retry logic
// Close connections properly on shutdown
```

## Common Pitfalls

**Unbounded array growth**:
```javascript
// BAD: Comments array grows forever
{ _id: "post1", comments: [...thousands of comments...] }

// GOOD: Separate collection with references
{ _id: "comment1", postId: "post1", text: "..." }
```

**Missing indexes**:
```javascript
// Always create indexes for query patterns
// Check with explain() - look for COLLSCAN (bad)
db.users.find({ email: "..." }).explain()
```

**Over-indexing**:
```javascript
// Each index adds write overhead
// Only index fields used in queries
// Monitor index usage: db.users.aggregate([{ $indexStats: {} }])
```

## Resources

- **MongoDB Documentation**: https://docs.mongodb.com/manual/
- **MongoDB University**: https://university.mongodb.com/
- **Schema Design Patterns**: https://www.mongodb.com/blog/post/building-with-patterns-a-summary
- **Aggregation Reference**: https://docs.mongodb.com/manual/reference/operator/aggregation/
- **Spring Data MongoDB**: https://docs.spring.io/spring-data/mongodb/docs/current/reference/html/

## Related Skills

When using MongoDB, consider these complementary skills:

- **spring-boot**: Java framework integration with Spring Data MongoDB
- **docker**: Running MongoDB in containers
- **nodejs**: MongoDB with Mongoose ODM
- **aggregation-pipelines**: Advanced analytics patterns
