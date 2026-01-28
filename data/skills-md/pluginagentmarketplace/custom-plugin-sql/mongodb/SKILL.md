---
name: mongodb
description: MongoDB fundamentals including document model, CRUD operations, querying, indexing, and aggregation framework for NoSQL database applications.
sasmp_version: "1.3.0"
bonded_agent: 03-mongodb
bond_type: PRIMARY_BOND
---

# MongoDB Mastery

## Document Model Basics

```javascript
// MongoDB document (JSON-like structure)
{
  _id: ObjectId("507f1f77bcf86cd799439011"),
  firstName: "John",
  lastName: "Doe",
  email: "john@example.com",
  salary: 75000,
  department: "Engineering",
  skills: ["JavaScript", "Python", "SQL"],
  address: {
    street: "123 Main St",
    city: "New York",
    state: "NY"
  },
  joinDate: new Date("2023-01-15")
}
```

## Collection Operations

```javascript
// Create database and collection
use company_db

// Insert single document
db.employees.insertOne({
  firstName: "Jane",
  lastName: "Smith",
  email: "jane@example.com",
  salary: 80000
})

// Insert multiple documents
db.employees.insertMany([
  { firstName: "Bob", lastName: "Johnson", salary: 70000 },
  { firstName: "Alice", lastName: "Williams", salary: 85000 }
])

// Get document count
db.employees.countDocuments({})

// Validate collection
db.employees.validate()
```

## CRUD Operations

```javascript
// READ - Basic find
db.employees.find()

// Find by condition
db.employees.find({ salary: { $gt: 75000 } })

// Find with projection (select specific fields)
db.employees.find(
  { department: "Engineering" },
  { firstName: 1, lastName: 1, salary: 1, _id: 0 }
)

// Find one document
db.employees.findOne({ email: "john@example.com" })

// UPDATE - Update one document
db.employees.updateOne(
  { _id: ObjectId("...") },
  { $set: { salary: 90000 } }
)

// Update multiple documents
db.employees.updateMany(
  { department: "Engineering" },
  { $set: { bonus: 5000 } }
)

// DELETE - Delete documents
db.employees.deleteOne({ _id: ObjectId("...") })
db.employees.deleteMany({ department: "HR" })
```

## Query Operators

```javascript
// Comparison operators
db.employees.find({ salary: { $gt: 75000 } })      // Greater than
db.employees.find({ salary: { $gte: 75000 } })     // Greater than or equal
db.employees.find({ salary: { $lt: 75000 } })      // Less than
db.employees.find({ salary: { $lte: 75000 } })     // Less than or equal
db.employees.find({ salary: { $eq: 75000 } })      // Equal
db.employees.find({ salary: { $ne: 75000 } })      // Not equal

// Array operators
db.employees.find({ skills: "JavaScript" })        // Contains value
db.employees.find({ skills: { $in: ["Python", "Go"] } })    // Contains any
db.employees.find({ skills: { $all: ["JavaScript", "Python"] } })  // Contains all
db.employees.find({ skills: { $size: 3 } })        // Array size

// Element operators
db.employees.find({ phone: { $exists: true } })    // Field exists
db.employees.find({ salary: { $type: "number" } }) // Field type check

// String matching
db.employees.find({ email: { $regex: "gmail" } })  // Regular expression
```

## Sorting and Limiting

```javascript
// Sort by single field
db.employees.find().sort({ salary: -1 })           // Descending
db.employees.find().sort({ salary: 1 })            // Ascending

// Sort by multiple fields
db.employees.find().sort({ department: 1, salary: -1 })

// Limit and skip
db.employees.find().limit(10)                       // First 10 results
db.employees.find().skip(20).limit(10)              // Pagination
```

## Indexing

```javascript
// Create single field index
db.employees.createIndex({ email: 1 })

// Create unique index
db.employees.createIndex({ email: 1 }, { unique: true })

// Create compound index
db.employees.createIndex({ department: 1, salary: -1 })

// Create text index for search
db.employees.createIndex({ firstName: "text", lastName: "text" })

// List indexes
db.employees.getIndexes()

// Drop index
db.employees.dropIndex("email_1")

// Full text search with text index
db.employees.find({ $text: { $search: "john" } })
```

## Data Types

```javascript
// String
{ name: "John Doe" }

// Number (Int32, Int64, Double)
{ age: 30, salary: 75000.50 }

// Boolean
{ active: true }

// Date
{ createdDate: new Date() }

// Array
{ skills: ["JavaScript", "Python"] }

// Object/Embedded document
{ address: { city: "NYC", state: "NY" } }

// ObjectID
{ _id: ObjectId() }

// Null
{ phone: null }

// Regular Expression
{ email: /gmail/ }
```

## Bulk Operations

```javascript
// Initialize bulk operation
let bulk = db.employees.initializeUnorderedBulkOp()

// Add multiple operations
bulk.find({ department: "Engineering" }).update({ $set: { bonus: 5000 } })
bulk.find({ salary: { $lt: 50000 } }).update({ $inc: { salary: 2000 } })
bulk.insert({ firstName: "New", lastName: "Employee" })
bulk.find({ _id: ObjectId("...") }).removeOne()

// Execute bulk
bulk.execute()
```

## Aggregation Pipeline (Data Processing)

```javascript
// Basic pipeline stages
db.employees.aggregate([
  { $match: { salary: { $gt: 75000 } } },     // Filter
  { $group: {                                  // Group & aggregate
      _id: "$department",
      avgSalary: { $avg: "$salary" },
      count: { $sum: 1 }
  }},
  { $sort: { avgSalary: -1 } },                // Sort
  { $limit: 5 }                                // Limit results
])

// Projection stage (reshape documents)
db.employees.aggregate([
  { $project: {
      fullName: { $concat: ["$firstName", " ", "$lastName"] },
      salary: 1,
      yearing_salary: { $multiply: ["$salary", 12] },
      _id: 0
  }}
])

// Unwind arrays for analysis
db.employees.aggregate([
  { $unwind: "$skills" },                      // Expand skills array
  { $group: {
      _id: "$skills",
      count: { $sum: 1 }
  }},
  { $sort: { count: -1 } }
])

// Lookup (similar to SQL JOIN)
db.orders.aggregate([
  { $lookup: {
      from: "customers",
      localField: "customerId",
      foreignField: "_id",
      as: "customerInfo"
  }},
  { $unwind: "$customerInfo" },
  { $project: {
      orderId: 1,
      "customerInfo.name": 1,
      "customerInfo.email": 1,
      amount: 1
  }}
])

// Complex multi-stage pipeline
db.sales.aggregate([
  { $match: { date: { $gte: new Date("2023-01-01") } } },
  { $group: {
      _id: { month: { $month: "$date" }, year: { $year: "$date" } },
      totalSales: { $sum: "$amount" },
      avgSale: { $avg: "$amount" },
      ordersCount: { $sum: 1 }
  }},
  { $sort: { "_id.year": 1, "_id.month": 1 } },
  { $project: {
      month: "$_id.month",
      year: "$_id.year",
      totalSales: { $round: ["$totalSales", 2] },
      avgSale: { $round: ["$avgSale", 2] },
      ordersCount: 1,
      _id: 0
  }}
])
```

## Transactions (ACID)

```javascript
// Start a session
const session = db.getMongo().startSession()
session.startTransaction()

try {
  // Multiple operations in transaction
  db.accounts.updateOne(
    { _id: "account1" },
    { $inc: { balance: -100 } },
    { session: session }
  )

  db.accounts.updateOne(
    { _id: "account2" },
    { $inc: { balance: 100 } },
    { session: session }
  )

  // All succeed or all fail
  session.commitTransaction()
} catch (error) {
  session.abortTransaction()
  throw error
} finally {
  session.endSession()
}
```

## Update Operators

```javascript
// $set - set field value
db.employees.updateOne(
  { _id: ObjectId("...") },
  { $set: { salary: 90000 } }
)

// $inc - increment field
db.employees.updateOne(
  { _id: ObjectId("...") },
  { $inc: { salary: 5000 } }
)

// $push - add to array
db.employees.updateOne(
  { _id: ObjectId("...") },
  { $push: { skills: "Kubernetes" } }
)

// $addToSet - add to array if not exists
db.employees.updateOne(
  { _id: ObjectId("...") },
  { $addToSet: { skills: "Docker" } }
)

// $pull - remove from array
db.employees.updateOne(
  { _id: ObjectId("...") },
  { $pull: { skills: "COBOL" } }
)

// $unset - remove field
db.employees.updateOne(
  { _id: ObjectId("...") },
  { $unset: { phone: "" } }
)

// Combination updates
db.employees.updateOne(
  { _id: ObjectId("...") },
  {
    $set: { updatedAt: new Date() },
    $inc: { salary: 5000 },
    $push: { performanceRatings: 4.5 }
  }
)
```

## Array Queries

```javascript
// Query array elements
db.employees.find({ skills: "Python" })        // Has Python skill

// Query array with conditions
db.employees.find({
  skills: { $elemMatch: { $eq: "JavaScript" } }
})

// Array position operators
db.orders.updateOne(
  { _id: ObjectId("..."), "items.sku": "SKU123" },
  { $set: { "items.$.quantity": 5 } }          // Update matching item
)

// Multiple array criteria
db.orders.find({
  items: { $elemMatch: {
    sku: "SKU123",
    quantity: { $gt: 3 }
  }}
})
```

## Real-World Examples

### E-commerce Product Catalog
```javascript
db.products.insertOne({
  _id: ObjectId(),
  sku: "PROD-001",
  name: "Laptop",
  price: 999.99,
  stock: 50,
  categories: ["Electronics", "Computers"],
  specs: {
    cpu: "Intel i7",
    ram: "16GB",
    storage: "512GB SSD"
  },
  reviews: [
    { userId: "user1", rating: 5, comment: "Great!" },
    { userId: "user2", rating: 4, comment: "Good value" }
  ],
  lastUpdated: new Date()
})

// Update stock with transaction
session.startTransaction()
db.products.updateOne({ sku: "PROD-001" }, { $inc: { stock: -1 } }, { session })
db.orders.insertOne({ productId: ObjectId(), quantity: 1 }, { session })
session.commitTransaction()
```

### User Profiles with Flexible Schema
```javascript
db.users.insertOne({
  _id: ObjectId(),
  username: "john_doe",
  email: "john@example.com",
  profile: {
    firstName: "John",
    lastName: "Doe",
    bio: "Software engineer",
    socialLinks: {
      github: "john-doe",
      twitter: "@johndoe"
    }
  },
  preferences: {
    theme: "dark",
    notifications: true,
    language: "en"
  },
  metadata: {
    createdAt: new Date(),
    lastLogin: new Date(),
    loginCount: 42
  }
})

// Flexible update - can add new fields
db.users.updateOne(
  { username: "john_doe" },
  { $set: { "profile.avatar": "url", "preferences.emailFrequency": "weekly" } }
)
```

## Performance Tips

```javascript
// Create indexes for common queries
db.employees.createIndex({ email: 1 })
db.employees.createIndex({ department: 1, salary: -1 })

// Use explain to optimize queries
db.employees.find({ salary: { $gt: 75000 } }).explain("executionStats")

// Projection to reduce data transfer
db.employees.find(
  { salary: { $gt: 75000 } },
  { firstName: 1, lastName: 1, salary: 1, _id: 0 }
)

// Batch writes for bulk inserts
db.employees.insertMany(largeArray, { ordered: false })

// Aggregation optimization (match early)
db.orders.aggregate([
  { $match: { status: "completed" } },        // Early filter
  { $lookup: { from: "customers", ... } },
  { $group: { _id: "$customerId", total: { $sum: "$amount" } } }
])
```

## Next Steps

Learn NoSQL design patterns, denormalization strategies, and advanced schema design in the `nosql-design` skill.
