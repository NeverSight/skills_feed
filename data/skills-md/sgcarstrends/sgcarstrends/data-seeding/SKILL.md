---
name: data-seeding
description: Create or update database seed scripts for development and testing environments. Use when setting up test data or initializing development databases.
allowed-tools: Read, Edit, Write, Bash
---

# Data Seeding Skill

This skill helps you create and manage database seed scripts in `packages/database/`.

## When to Use This Skill

- Setting up development database with test data
- Creating seed data for testing
- Initializing demo environments
- Resetting database to known state
- Generating realistic sample data
- Testing data migration scripts

## Seed Script Structure

```
packages/database/
├── src/
│   └── seed/
│       ├── index.ts          # Main seed runner
│       ├── cars.ts           # Car data seeds
│       ├── coe.ts            # COE data seeds
│       ├── posts.ts          # Blog posts seeds
│       └── users.ts          # User seeds
├── scripts/
│   └── seed.ts               # Seed execution script
└── package.json
```

## Basic Seed Pattern

### Simple Seed Script

```typescript
// packages/database/src/seed/cars.ts
import { db } from "../index";
import { cars } from "../db/schema";
import { nanoid } from "nanoid";

export async function seedCars() {
  console.log("Seeding cars...");

  const carData = [
    {
      id: nanoid(),
      make: "Toyota",
      model: "Camry",
      vehicleClass: "Sedan",
      fuelType: "Petrol",
      month: "2024-01",
      number: 150,
    },
    {
      id: nanoid(),
      make: "Honda",
      model: "Civic",
      vehicleClass: "Sedan",
      fuelType: "Petrol",
      month: "2024-01",
      number: 120,
    },
    {
      id: nanoid(),
      make: "BMW",
      model: "3 Series",
      vehicleClass: "Sedan",
      fuelType: "Petrol",
      month: "2024-01",
      number: 80,
    },
  ];

  await db.insert(cars).values(carData);

  console.log(`✓ Seeded ${carData.length} cars`);
}
```

### Main Seed Runner

```typescript
// packages/database/src/seed/index.ts
import { db } from "../index";
import { seedCars } from "./cars";
import { seedCOE } from "./coe";
import { seedPosts } from "./posts";

export async function seed() {
  try {
    console.log("🌱 Starting database seed...\n");

    // Clear existing data (optional)
    await clearDatabase();

    // Run seed functions
    await seedCars();
    await seedCOE();
    await seedPosts();

    console.log("\n✅ Database seeded successfully!");
  } catch (error) {
    console.error("❌ Seed failed:", error);
    throw error;
  }
}

async function clearDatabase() {
  console.log("Clearing existing data...");

  // Delete in reverse order of dependencies
  await db.delete(posts);
  await db.delete(coe);
  await db.delete(cars);

  console.log("✓ Database cleared\n");
}

// Run if called directly
if (require.main === module) {
  seed()
    .then(() => process.exit(0))
    .catch(() => process.exit(1));
}
```

### Execution Script

```typescript
// packages/database/scripts/seed.ts
import { seed } from "../src/seed";

seed()
  .then(() => {
    console.log("Seed completed");
    process.exit(0);
  })
  .catch((error) => {
    console.error("Seed failed:", error);
    process.exit(1);
  });
```

Add to `package.json`:

```json
{
  "scripts": {
    "db:seed": "tsx scripts/seed.ts"
  }
}
```

Run seed:

```bash
pnpm -F @sgcarstrends/database db:seed
```

## Advanced Seed Patterns

### Seed with Relationships

```typescript
// packages/database/src/seed/posts.ts
import { db } from "../index";
import { users, posts } from "../db/schema";
import { nanoid } from "nanoid";

export async function seedPosts() {
  console.log("Seeding users and posts...");

  // First, create users
  const userData = [
    {
      id: nanoid(),
      name: "John Doe",
      email: "john@example.com",
    },
    {
      id: nanoid(),
      name: "Jane Smith",
      email: "jane@example.com",
    },
  ];

  const createdUsers = await db.insert(users).values(userData).returning();

  // Then, create posts with user references
  const postData = [
    {
      id: nanoid(),
      title: "First Blog Post",
      content: "This is the first blog post content.",
      authorId: createdUsers[0].id,
      published: true,
      publishedAt: new Date(),
    },
    {
      id: nanoid(),
      title: "Second Blog Post",
      content: "This is the second blog post content.",
      authorId: createdUsers[1].id,
      published: true,
      publishedAt: new Date(),
    },
  ];

  await db.insert(posts).values(postData);

  console.log(`✓ Seeded ${createdUsers.length} users and ${postData.length} posts`);
}
```

### Seed with Faker.js

```bash
pnpm -F @sgcarstrends/database add -D @faker-js/faker
```

```typescript
// packages/database/src/seed/realistic-data.ts
import { faker } from "@faker-js/faker";
import { db } from "../index";
import { cars } from "../db/schema";
import { nanoid } from "nanoid";

export async function seedRealisticCars(count: number = 100) {
  console.log(`Seeding ${count} realistic cars...`);

  const makes = ["Toyota", "Honda", "BMW", "Mercedes", "Audi", "Nissan", "Mazda"];
  const fuelTypes = ["Petrol", "Diesel", "Electric", "Hybrid"];
  const vehicleClasses = ["Sedan", "SUV", "Hatchback", "MPV"];

  const carData = Array.from({ length: count }, () => ({
    id: nanoid(),
    make: faker.helpers.arrayElement(makes),
    model: faker.vehicle.model(),
    vehicleClass: faker.helpers.arrayElement(vehicleClasses),
    fuelType: faker.helpers.arrayElement(fuelTypes),
    month: faker.date.between({ from: "2020-01-01", to: "2024-12-31" })
      .toISOString()
      .slice(0, 7),
    number: faker.number.int({ min: 10, max: 500 }),
  }));

  // Batch insert for performance
  const batchSize = 50;
  for (let i = 0; i < carData.length; i += batchSize) {
    const batch = carData.slice(i, i + batchSize);
    await db.insert(cars).values(batch);
  }

  console.log(`✓ Seeded ${count} realistic cars`);
}
```

### Seed from JSON File

```typescript
// packages/database/src/seed/from-file.ts
import { db } from "../index";
import { cars } from "../db/schema";
import { readFileSync } from "fs";
import { join } from "path";

export async function seedFromJSON() {
  console.log("Seeding from JSON file...");

  // Read data from JSON file
  const filePath = join(__dirname, "../../data/cars.json");
  const rawData = readFileSync(filePath, "utf-8");
  const carData = JSON.parse(rawData);

  await db.insert(cars).values(carData);

  console.log(`✓ Seeded ${carData.length} cars from JSON`);
}
```

Example JSON file:

```json
// packages/database/data/cars.json
[
  {
    "id": "car-1",
    "make": "Toyota",
    "model": "Camry",
    "vehicleClass": "Sedan",
    "fuelType": "Petrol",
    "month": "2024-01",
    "number": 150
  },
  {
    "id": "car-2",
    "make": "Honda",
    "model": "Civic",
    "vehicleClass": "Sedan",
    "fuelType": "Petrol",
    "month": "2024-01",
    "number": 120
  }
]
```

### Seed from CSV

```bash
pnpm -F @sgcarstrends/database add -D csv-parse
```

```typescript
// packages/database/src/seed/from-csv.ts
import { db } from "../index";
import { cars } from "../db/schema";
import { parse } from "csv-parse/sync";
import { readFileSync } from "fs";
import { join } from "path";
import { nanoid } from "nanoid";

export async function seedFromCSV() {
  console.log("Seeding from CSV file...");

  const filePath = join(__dirname, "../../data/cars.csv");
  const csvContent = readFileSync(filePath, "utf-8");

  const records = parse(csvContent, {
    columns: true,
    skip_empty_lines: true,
  });

  const carData = records.map((record: any) => ({
    id: nanoid(),
    make: record.make,
    model: record.model,
    vehicleClass: record.vehicle_class,
    fuelType: record.fuel_type,
    month: record.month,
    number: parseInt(record.number, 10),
  }));

  // Batch insert
  const batchSize = 100;
  for (let i = 0; i < carData.length; i += batchSize) {
    const batch = carData.slice(i, i + batchSize);
    await db.insert(cars).values(batch);
  }

  console.log(`✓ Seeded ${carData.length} cars from CSV`);
}
```

## Environment-Specific Seeds

### Development Seeds

```typescript
// packages/database/src/seed/dev.ts
import { seedCars } from "./cars";
import { seedCOE } from "./coe";
import { seedRealisticCars } from "./realistic-data";

export async function seedDevelopment() {
  console.log("🔧 Seeding development environment...\n");

  // Small, predictable dataset
  await seedCars();
  await seedCOE();

  console.log("\n✅ Development seed complete!");
}
```

### Testing Seeds

```typescript
// packages/database/src/seed/test.ts
export async function seedTesting() {
  console.log("🧪 Seeding test environment...\n");

  // Minimal, deterministic data for tests
  const testCar = {
    id: "test-car-1",
    make: "Toyota",
    model: "Camry",
    vehicleClass: "Sedan",
    fuelType: "Petrol",
    month: "2024-01",
    number: 100,
  };

  await db.insert(cars).values([testCar]);

  console.log("\n✅ Test seed complete!");
}
```

### Staging Seeds

```typescript
// packages/database/src/seed/staging.ts
export async function seedStaging() {
  console.log("🎭 Seeding staging environment...\n");

  // Larger, realistic dataset similar to production
  await seedRealisticCars(1000);
  await seedRealisticCOE(500);
  await seedRealisticPosts(50);

  console.log("\n✅ Staging seed complete!");
}
```

### Conditional Seeding

```typescript
// packages/database/src/seed/index.ts
import { seedDevelopment } from "./dev";
import { seedTesting } from "./test";
import { seedStaging } from "./staging";

export async function seed() {
  const env = process.env.NODE_ENV || "development";

  switch (env) {
    case "development":
      await seedDevelopment();
      break;
    case "test":
      await seedTesting();
      break;
    case "staging":
      await seedStaging();
      break;
    default:
      throw new Error(`No seed strategy for environment: ${env}`);
  }
}
```

## Idempotent Seeds

### Upsert Pattern

```typescript
// packages/database/src/seed/idempotent.ts
import { db } from "../index";
import { cars } from "../db/schema";

export async function seedIdempotent() {
  console.log("Seeding with upsert...");

  const carData = [
    {
      id: "fixed-id-1",
      make: "Toyota",
      model: "Camry",
      month: "2024-01",
      number: 150,
    },
  ];

  // Use onConflictDoUpdate for upsert
  await db
    .insert(cars)
    .values(carData)
    .onConflictDoUpdate({
      target: cars.id,
      set: {
        make: carData[0].make,
        model: carData[0].model,
        number: carData[0].number,
        updatedAt: new Date(),
      },
    });

  console.log("✓ Upserted cars");
}
```

### Check Before Insert

```typescript
export async function seedIfEmpty() {
  console.log("Checking if database needs seeding...");

  const existingCars = await db.select().from(cars).limit(1);

  if (existingCars.length > 0) {
    console.log("Database already has data, skipping seed");
    return;
  }

  console.log("Database is empty, proceeding with seed");
  await seedCars();
}
```

## Performance Optimization

### Batch Inserts

```typescript
export async function seedLargeDataset() {
  const totalRecords = 10000;
  const batchSize = 1000;

  console.log(`Seeding ${totalRecords} records in batches of ${batchSize}...`);

  for (let i = 0; i < totalRecords; i += batchSize) {
    const batch = generateBatch(batchSize);

    await db.insert(cars).values(batch);

    console.log(`Progress: ${Math.min(i + batchSize, totalRecords)}/${totalRecords}`);
  }

  console.log("✓ Large dataset seeded");
}

function generateBatch(size: number) {
  return Array.from({ length: size }, () => ({
    id: nanoid(),
    make: "Toyota",
    model: "Camry",
    month: "2024-01",
    number: 100,
  }));
}
```

### Use Transactions

```typescript
import { db } from "../index";

export async function seedWithTransaction() {
  console.log("Seeding with transaction...");

  await db.transaction(async (tx) => {
    // All or nothing
    await tx.insert(cars).values([...carData]);
    await tx.insert(coe).values([...coeData]);
    await tx.insert(posts).values([...postData]);
  });

  console.log("✓ Transaction seed complete");
}
```

## Utility Functions

### Generate Realistic Dates

```typescript
function generateMonthRange(start: string, end: string): string[] {
  const months = [];
  let current = new Date(start);
  const endDate = new Date(end);

  while (current <= endDate) {
    months.push(current.toISOString().slice(0, 7));
    current.setMonth(current.getMonth() + 1);
  }

  return months;
}

// Usage
const months = generateMonthRange("2020-01", "2024-12");
```

### Generate Sequential IDs

```typescript
function generateSequentialId(prefix: string, index: number): string {
  return `${prefix}-${String(index).padStart(5, "0")}`;
}

// Usage
const id = generateSequentialId("car", 42); // "car-00042"
```

## Testing Seeds

```typescript
// packages/database/src/seed/__tests__/seed.test.ts
import { describe, it, expect, beforeEach } from "vitest";
import { db } from "../../index";
import { cars } from "../../db/schema";
import { seedCars } from "../cars";

describe("Seed Scripts", () => {
  beforeEach(async () => {
    // Clear data before each test
    await db.delete(cars);
  });

  it("seeds cars successfully", async () => {
    await seedCars();

    const result = await db.select().from(cars);

    expect(result.length).toBeGreaterThan(0);
    expect(result[0].make).toBeDefined();
  });

  it("creates valid data", async () => {
    await seedCars();

    const [car] = await db.select().from(cars).limit(1);

    expect(car.id).toBeTruthy();
    expect(car.make).toBeTruthy();
    expect(car.number).toBeGreaterThanOrEqual(0);
  });
});
```

## CLI for Selective Seeding

```typescript
// packages/database/scripts/seed-cli.ts
import { seedCars } from "../src/seed/cars";
import { seedCOE } from "../src/seed/coe";
import { seedPosts } from "../src/seed/posts";

const seeders = {
  cars: seedCars,
  coe: seedCOE,
  posts: seedPosts,
  all: async () => {
    await seedCars();
    await seedCOE();
    await seedPosts();
  },
};

const target = process.argv[2] as keyof typeof seeders;

if (!target || !seeders[target]) {
  console.error("Usage: pnpm db:seed [cars|coe|posts|all]");
  process.exit(1);
}

seeders[target]()
  .then(() => {
    console.log(`✅ Seeded ${target} successfully`);
    process.exit(0);
  })
  .catch((error) => {
    console.error(`❌ Seed failed:`, error);
    process.exit(1);
  });
```

Add to `package.json`:

```json
{
  "scripts": {
    "db:seed": "tsx scripts/seed-cli.ts all",
    "db:seed:cars": "tsx scripts/seed-cli.ts cars",
    "db:seed:coe": "tsx scripts/seed-cli.ts coe",
    "db:seed:posts": "tsx scripts/seed-cli.ts posts"
  }
}
```

## Common Seed Data

### COE Seed Data

```typescript
// packages/database/src/seed/coe.ts
import { db } from "../index";
import { coe } from "../db/schema";
import { nanoid } from "nanoid";

export async function seedCOE() {
  console.log("Seeding COE data...");

  const coeData = [
    {
      id: nanoid(),
      biddingNo: 1,
      month: "2024-01",
      vehicleClass: "A",
      quota: 1000,
      bidsReceived: 1200,
      premium: "95000.00",
    },
    {
      id: nanoid(),
      biddingNo: 1,
      month: "2024-01",
      vehicleClass: "B",
      quota: 800,
      bidsReceived: 900,
      premium: "105000.00",
    },
  ];

  await db.insert(coe).values(coeData);

  console.log(`✓ Seeded ${coeData.length} COE records`);
}
```

## References

- Related files:
  - `packages/database/src/seed/` - Seed scripts
  - `packages/database/scripts/seed.ts` - Seed runner
  - `packages/database/CLAUDE.md` - Database package documentation

## Best Practices

1. **Idempotent**: Seeds should be safe to run multiple times
2. **Environment-Specific**: Different seed data for dev/test/staging
3. **Realistic Data**: Use Faker for realistic test data
4. **Batch Inserts**: Use batching for large datasets
5. **Relationships**: Seed in correct order (parent tables first)
6. **Transactions**: Use transactions for atomic seeding
7. **Clear First**: Option to clear existing data
8. **Logging**: Provide clear progress feedback
