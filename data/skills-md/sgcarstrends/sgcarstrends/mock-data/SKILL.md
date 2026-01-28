---
name: mock-data
description: Generate realistic mock data for testing using factories, fixtures, and Faker.js. Use when seeding test databases, creating test fixtures, or mocking API responses.
allowed-tools: Read, Edit, Write, Bash, Grep, Glob
---

# Mock Data Generation Skill

This skill helps you generate realistic mock data for testing, development, and seeding purposes.

## When to Use This Skill

- Creating test fixtures for unit/integration tests
- Seeding test databases
- Mocking API responses
- Generating sample data for development
- Creating realistic data for E2E tests
- Populating staging environments
- Testing edge cases with specific data patterns

## Tools & Libraries

### Faker.js

Primary library for generating realistic fake data:

```bash
# Install Faker
pnpm add -D @faker-js/faker
```

**Features:**
- Person data (names, emails, phone numbers)
- Addresses and locations
- Dates and times
- Commerce data (products, prices)
- Vehicle data
- Lorem ipsum text
- Custom locales (including Singapore)

## Basic Mock Data Patterns

### Simple Factories

```typescript
// apps/api/__tests__/factories/car.factory.ts
import { faker } from "@faker-js/faker";

export const createMockCar = (overrides = {}) => ({
  id: faker.string.uuid(),
  make: faker.vehicle.manufacturer(),
  model: faker.vehicle.model(),
  vehicleType: faker.helpers.arrayElement(["Passenger Car", "Goods Vehicle"]),
  fuelType: faker.helpers.arrayElement(["Petrol", "Diesel", "Electric", "Hybrid"]),
  month: faker.date.recent({ days: 365 }).toISOString().slice(0, 7),
  number: faker.number.int({ min: 1, max: 1000 }),
  ...overrides,
});

// Usage
const car = createMockCar({ make: "Toyota", model: "Corolla" });
```

### Factory Functions

```typescript
// apps/api/__tests__/factories/index.ts
import { faker } from "@faker-js/faker";

export const CarFactory = {
  build: (overrides = {}) => ({
    id: faker.string.uuid(),
    make: faker.vehicle.manufacturer(),
    model: faker.vehicle.model(),
    month: faker.date.recent({ days: 365 }).toISOString().slice(0, 7),
    number: faker.number.int({ min: 1, max: 1000 }),
    ...overrides,
  }),

  buildMany: (count: number, overrides = {}) => {
    return Array.from({ length: count }, () => CarFactory.build(overrides));
  },

  buildToyota: () => CarFactory.build({ make: "Toyota" }),

  buildElectric: () => CarFactory.build({ fuelType: "Electric" }),
};

export const COEFactory = {
  build: (overrides = {}) => ({
    id: faker.string.uuid(),
    month: faker.date.recent({ days: 365 }).toISOString().slice(0, 7),
    biddingNo: faker.number.int({ min: 1, max: 24 }),
    vehicleClass: faker.helpers.arrayElement(["A", "B", "C", "D", "E"]),
    quota: faker.number.int({ min: 100, max: 5000 }),
    bidsReceived: faker.number.int({ min: 1000, max: 10000 }),
    premiumAmount: faker.number.int({ min: 50000, max: 150000 }),
    ...overrides,
  }),

  buildMany: (count: number, overrides = {}) => {
    return Array.from({ length: count }, () => COEFactory.build(overrides));
  },

  buildCategoryA: () => COEFactory.build({ vehicleClass: "A" }),
};

export const BlogPostFactory = {
  build: (overrides = {}) => ({
    id: faker.string.uuid(),
    title: faker.lorem.sentence(),
    slug: faker.helpers.slugify(faker.lorem.sentence()),
    content: faker.lorem.paragraphs(3),
    excerpt: faker.lorem.paragraph(),
    publishedAt: faker.date.recent({ days: 30 }),
    authorId: faker.string.uuid(),
    ...overrides,
  }),

  buildMany: (count: number, overrides = {}) => {
    return Array.from({ length: count }, () => BlogPostFactory.build(overrides));
  },

  buildPublished: () => BlogPostFactory.build({
    publishedAt: faker.date.past(),
  }),

  buildDraft: () => BlogPostFactory.build({
    publishedAt: null,
  }),
};
```

## Advanced Factories

### Class-Based Factories

```typescript
// apps/api/__tests__/factories/base.factory.ts
import { faker } from "@faker-js/faker";

export abstract class BaseFactory<T> {
  abstract build(overrides?: Partial<T>): T;

  buildMany(count: number, overrides?: Partial<T>): T[] {
    return Array.from({ length: count }, () => this.build(overrides));
  }

  buildList(items: Partial<T>[]): T[] {
    return items.map((item) => this.build(item));
  }
}

// Specific factory
export class CarFactory extends BaseFactory<Car> {
  build(overrides: Partial<Car> = {}): Car {
    return {
      id: faker.string.uuid(),
      make: faker.vehicle.manufacturer(),
      model: faker.vehicle.model(),
      month: faker.date.recent({ days: 365 }).toISOString().slice(0, 7),
      number: faker.number.int({ min: 1, max: 1000 }),
      ...overrides,
    };
  }

  buildToyota(): Car {
    return this.build({ make: "Toyota" });
  }

  buildWithHighRegistrations(): Car {
    return this.build({ number: faker.number.int({ min: 500, max: 1000 }) });
  }
}

// Usage
const carFactory = new CarFactory();
const cars = carFactory.buildMany(10);
const toyota = carFactory.buildToyota();
```

### Sequence Factories

```typescript
// apps/api/__tests__/factories/sequence.ts
import { faker } from "@faker-js/faker";

let sequenceCounters: Record<string, number> = {};

export const sequence = (name: string, fn: (n: number) => any) => {
  if (!sequenceCounters[name]) {
    sequenceCounters[name] = 0;
  }
  sequenceCounters[name]++;
  return fn(sequenceCounters[name]);
};

export const resetSequences = () => {
  sequenceCounters = {};
};

// Usage
export const UserFactory = {
  build: (overrides = {}) => ({
    id: sequence("user", (n) => `user-${n}`),
    email: sequence("email", (n) => `user${n}@example.com`),
    name: faker.person.fullName(),
    ...overrides,
  }),
};

// In tests
beforeEach(() => {
  resetSequences();
});

const user1 = UserFactory.build(); // { id: "user-1", email: "user1@example.com" }
const user2 = UserFactory.build(); // { id: "user-2", email: "user2@example.com" }
```

## Fixtures

### Static Fixtures

```typescript
// apps/api/__tests__/fixtures/cars.ts
export const toyotaCorollaFixture = {
  make: "Toyota",
  model: "Corolla",
  month: "2024-01",
  number: 150,
};

export const hondaCivicFixture = {
  make: "Honda",
  model: "Civic",
  month: "2024-01",
  number: 120,
};

export const popularCarsFixture = [
  toyotaCorollaFixture,
  hondaCivicFixture,
  {
    make: "BMW",
    model: "3 Series",
    month: "2024-01",
    number: 80,
  },
];

// Usage in tests
import { toyotaCorollaFixture } from "./fixtures/cars";

it("should process Toyota Corolla data", () => {
  const result = processCarData(toyotaCorollaFixture);
  expect(result.make).toBe("Toyota");
});
```

### JSON Fixtures

```typescript
// apps/api/__tests__/fixtures/cars.json
[
  {
    "make": "Toyota",
    "model": "Corolla",
    "month": "2024-01",
    "number": 150
  },
  {
    "make": "Honda",
    "model": "Civic",
    "month": "2024-01",
    "number": 120
  }
]

// Load in tests
import carsFixture from "./fixtures/cars.json";

it("should load fixture data", () => {
  expect(carsFixture).toHaveLength(2);
  expect(carsFixture[0].make).toBe("Toyota");
});
```

### Dynamic Fixtures

```typescript
// apps/api/__tests__/fixtures/dynamic.ts
import { faker } from "@faker-js/faker";

export const generateCarFixtures = (count: number, month: string) => {
  return Array.from({ length: count }, () => ({
    make: faker.vehicle.manufacturer(),
    model: faker.vehicle.model(),
    month,
    number: faker.number.int({ min: 1, max: 500 }),
  }));
};

// Usage
const januaryCars = generateCarFixtures(100, "2024-01");
const februaryCars = generateCarFixtures(100, "2024-02");
```

## Singapore-Specific Mock Data

### Singapore Locales

```typescript
// apps/api/__tests__/factories/singapore.ts
import { faker } from "@faker-js/faker";
import { fakerEN_SG } from "@faker-js/faker";

// Use Singapore locale
faker.setDefaultLocale("en_SG");

export const SingaporeAddressFactory = {
  build: () => ({
    street: faker.location.street(),
    postalCode: faker.location.zipCode("######"), // 6-digit postal code
    country: "Singapore",
  }),
};

export const SingaporePhoneFactory = {
  build: () => ({
    mobile: `+65 ${faker.helpers.arrayElement(["8", "9"])}${faker.string.numeric(7)}`,
    home: `+65 6${faker.string.numeric(7)}`,
  }),
};

// Singapore car makes (popular in Singapore)
export const SingaporeCarMakes = [
  "Toyota",
  "Honda",
  "Mercedes-Benz",
  "BMW",
  "Mazda",
  "Hyundai",
  "Kia",
  "Nissan",
  "Volkswagen",
  "Audi",
];

export const SingaporeCarFactory = {
  build: (overrides = {}) => ({
    make: faker.helpers.arrayElement(SingaporeCarMakes),
    model: faker.vehicle.model(),
    month: faker.date.recent({ days: 365 }).toISOString().slice(0, 7),
    number: faker.number.int({ min: 1, max: 500 }),
    ...overrides,
  }),
};
```

### COE Categories

```typescript
// apps/api/__tests__/factories/coe.ts
export const COECategories = {
  A: "Cars up to 1600cc & 97kW",
  B: "Cars above 1600cc or 97kW",
  C: "Goods Vehicles & Buses",
  D: "Motorcycles",
  E: "Open Category",
};

export const COEFactory = {
  build: (overrides = {}) => {
    const category = faker.helpers.arrayElement(["A", "B", "C", "D", "E"]);

    return {
      month: faker.date.recent({ days: 365 }).toISOString().slice(0, 7),
      biddingNo: faker.number.int({ min: 1, max: 24 }),
      vehicleClass: category,
      quota: faker.number.int({ min: 100, max: 5000 }),
      bidsReceived: faker.number.int({ min: 1000, max: 10000 }),
      premiumAmount: faker.number.int({ min: 30000, max: 150000 }),
      ...overrides,
    };
  },

  buildRealistic: () => {
    const category = faker.helpers.arrayElement(["A", "B"]) as "A" | "B";
    const basePrice = category === "A" ? 60000 : 90000;

    return COEFactory.build({
      vehicleClass: category,
      premiumAmount: basePrice + faker.number.int({ min: -10000, max: 30000 }),
    });
  },
};
```

## Database Seeding

### Seed Scripts

```typescript
// apps/api/scripts/seed.ts
import { db } from "../src/config/database";
import { cars, coe, posts } from "@sgcarstrends/database/schema";
import { CarFactory, COEFactory, BlogPostFactory } from "../__tests__/factories";

async function seed() {
  console.log("Seeding database...");

  // Clear existing data
  await db.delete(cars);
  await db.delete(coe);
  await db.delete(posts);

  // Seed cars
  const carData = CarFactory.buildMany(1000);
  await db.insert(cars).values(carData);
  console.log("✓ Seeded 1000 cars");

  // Seed COE
  const coeData = COEFactory.buildMany(240); // 24 bidding rounds * 10 months
  await db.insert(coe).values(coeData);
  console.log("✓ Seeded 240 COE records");

  // Seed blog posts
  const postData = BlogPostFactory.buildMany(50);
  await db.insert(posts).values(postData);
  console.log("✓ Seeded 50 blog posts");

  console.log("Seeding complete!");
}

seed().catch(console.error);
```

### Environment-Specific Seeding

```typescript
// apps/api/scripts/seed-env.ts
import { db } from "../src/config/database";
import { CarFactory, COEFactory } from "../__tests__/factories";

async function seedForEnvironment(env: string) {
  const counts = {
    development: { cars: 1000, coe: 240 },
    test: { cars: 100, coe: 24 },
    staging: { cars: 10000, coe: 1000 },
  };

  const config = counts[env as keyof typeof counts] || counts.development;

  console.log(`Seeding ${env} environment...`);

  await db.insert(cars).values(CarFactory.buildMany(config.cars));
  await db.insert(coe).values(COEFactory.buildMany(config.coe));

  console.log(`✓ Seeded ${config.cars} cars and ${config.coe} COE records`);
}

const env = process.env.NODE_ENV || "development";
seedForEnvironment(env).catch(console.error);
```

## API Response Mocking

### Mock API Responses

```typescript
// apps/api/__tests__/mocks/api-responses.ts
export const mockLTACarResponse = {
  records: [
    {
      month: "2024-01",
      make: "TOYOTA",
      fuel_type: "Petrol",
      vehicle_type: "Passenger Car",
      number: 150,
    },
    {
      month: "2024-01",
      make: "HONDA",
      fuel_type: "Petrol",
      vehicle_type: "Passenger Car",
      number: 120,
    },
  ],
};

export const mockLTACOEResponse = {
  records: [
    {
      month: "2024-01",
      bidding_no: "1",
      vehicle_class: "A",
      quota: 1000,
      bids_received: 5000,
      premium: 65000,
    },
  ],
};

export const mockErrorResponse = {
  error: {
    code: "INTERNAL_ERROR",
    message: "An error occurred",
  },
};

// Usage in tests
import { mockLTACarResponse } from "./mocks/api-responses";

vi.spyOn(global, "fetch").mockResolvedValue({
  ok: true,
  json: async () => mockLTACarResponse,
} as Response);
```

### Dynamic Mock Generators

```typescript
// apps/api/__tests__/mocks/generators.ts
import { faker } from "@faker-js/faker";

export const generateMockLTAResponse = (recordCount: number) => ({
  records: Array.from({ length: recordCount }, () => ({
    month: faker.date.recent({ days: 365 }).toISOString().slice(0, 7),
    make: faker.vehicle.manufacturer().toUpperCase(),
    fuel_type: faker.helpers.arrayElement(["Petrol", "Diesel", "Electric"]),
    vehicle_type: "Passenger Car",
    number: faker.number.int({ min: 1, max: 500 }),
  })),
});

// Usage
const response = generateMockLTAResponse(100);
```

## Testing with Mock Data

### Using Factories in Tests

```typescript
// apps/api/__tests__/routes/cars.test.ts
import { describe, it, expect, beforeEach } from "vitest";
import { db } from "../../src/config/database";
import { CarFactory } from "../factories";
import app from "../../src/index";

describe("GET /api/v1/cars/makes", () => {
  beforeEach(async () => {
    // Seed with factory data
    const cars = CarFactory.buildMany(100);
    await db.insert(cars).values(cars);
  });

  it("should return list of makes", async () => {
    const res = await app.request("/api/v1/cars/makes");

    expect(res.status).toBe(200);
    expect(await res.json()).toHaveLength(expect.any(Number));
  });
});
```

### Using Fixtures in Tests

```typescript
// apps/api/__tests__/services/coe.test.ts
import { describe, it, expect } from "vitest";
import { calculateCOEPremium } from "../../src/services/coe";
import { mockCOEData } from "../fixtures/coe";

describe("calculateCOEPremium", () => {
  it("should calculate premium correctly", () => {
    const result = calculateCOEPremium(mockCOEData);

    expect(result).toBeGreaterThan(0);
  });
});
```

## Best Practices

### 1. Keep Factories Simple

```typescript
// ❌ Too complex
export const ComplexCarFactory = {
  build: async (overrides = {}) => {
    const make = await fetchMakeFromDatabase(); // Don't do async operations
    const model = complexCalculation(make); // Don't do complex logic
    return { make, model, ...overrides };
  },
};

// ✅ Simple and synchronous
export const SimpleCarFactory = {
  build: (overrides = {}) => ({
    make: faker.vehicle.manufacturer(),
    model: faker.vehicle.model(),
    ...overrides,
  }),
};
```

### 2. Use Realistic Data

```typescript
// ❌ Unrealistic test data
const car = { make: "test", model: "test", number: 99999999 };

// ✅ Realistic test data
const car = CarFactory.build({
  make: "Toyota",
  model: "Corolla",
  number: 150,
});
```

### 3. Don't Over-Mock

```typescript
// ❌ Mocking everything
vi.spyOn(db, "insert").mockResolvedValue([]);
vi.spyOn(redis, "get").mockResolvedValue(null);
vi.spyOn(fetch, "fetch").mockResolvedValue({});

// ✅ Only mock external dependencies
vi.spyOn(fetch, "fetch").mockResolvedValue(mockResponse);
// Let db and redis work normally in integration tests
```

### 4. Isolate Test Data

```typescript
// ❌ Shared mutable state
const sharedCar = CarFactory.build();

it("test 1", () => {
  sharedCar.number = 100; // Mutates shared state
});

it("test 2", () => {
  expect(sharedCar.number).toBe(100); // Depends on test 1
});

// ✅ Independent test data
it("test 1", () => {
  const car = CarFactory.build();
  car.number = 100;
});

it("test 2", () => {
  const car = CarFactory.build();
  expect(car.number).toBeGreaterThan(0);
});
```

## Troubleshooting

### Faker Generating Same Data

```typescript
// Issue: Faker generates same data in tests
// Solution: Use unique identifiers or sequences

import { sequence } from "./sequence";

const user1 = UserFactory.build(); // Same email
const user2 = UserFactory.build(); // Same email

// Fix with sequence
export const UserFactory = {
  build: (overrides = {}) => ({
    email: sequence("email", (n) => `user${n}@example.com`),
    ...overrides,
  }),
};
```

### Factory Data Not Matching Schema

```typescript
// Issue: Factory generates invalid data
// Solution: Use Zod schema validation in factory

import { z } from "zod";

const carSchema = z.object({
  make: z.string().min(1),
  model: z.string().min(1),
  month: z.string().regex(/^\d{4}-\d{2}$/),
  number: z.number().int().min(0),
});

export const CarFactory = {
  build: (overrides = {}) => {
    const data = {
      make: faker.vehicle.manufacturer(),
      model: faker.vehicle.model(),
      month: faker.date.recent({ days: 365 }).toISOString().slice(0, 7),
      number: faker.number.int({ min: 1, max: 1000 }),
      ...overrides,
    };

    return carSchema.parse(data); // Validates before returning
  },
};
```

## References

- Faker.js Documentation: https://fakerjs.dev
- Test Fixtures Pattern: https://martinfowler.com/bliki/TestFixture.html
- Factory Pattern: https://en.wikipedia.org/wiki/Factory_method_pattern
- Related files:
  - `apps/api/scripts/seed.ts` - Database seeding
  - Root CLAUDE.md - Testing guidelines

## Best Practices Summary

1. **Use Factories**: Create reusable factory functions for common entities
2. **Realistic Data**: Generate data that resembles production
3. **Fixtures for Static**: Use fixtures for known test cases
4. **Factories for Dynamic**: Use factories for varied test scenarios
5. **Isolate Test Data**: Each test should have independent data
6. **Seed Databases**: Use factories to seed dev/test databases
7. **Singapore-Specific**: Use appropriate locales and realistic values
8. **Keep Simple**: Factories should be synchronous and straightforward
