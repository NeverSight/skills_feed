---
name: prisma
description: Prisma ORM and PostgreSQL database operations. Use when working with database schema, migrations, queries, or the @projectx/db package.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash(pnpm:*), Bash(npx prisma:*)
---

# Prisma Database Operations

## Database Package Location

The Prisma schema and client are in `packages/db/`.

## Schema Location

```
packages/db/
├── prisma/
│   ├── schema.prisma    # Database schema
│   ├── migrations/      # Migration history
│   └── seed.ts          # Seed script
└── src/
    └── lib/
        ├── prisma.service.ts           # NestJS Prisma service
        └── [model]/                    # Repository services
            └── [model]-repository.service.ts
```

## Common Commands

```bash
# Generate Prisma client after schema changes
pnpm prisma:generate

# Create and apply migration (development)
pnpm prisma:migrate:dev

# Apply migrations (production)
pnpm prisma:migrate

# Seed the database
pnpm prisma:seed

# Open Prisma Studio
pnpm --filter @projectx/db exec prisma studio
```

## Schema Patterns

### Basic Model

```prisma
model Product {
  id          String   @id @default(cuid())
  name        String
  description String?
  price       Decimal  @db.Decimal(10, 2)
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

  // Relations
  categoryId  String
  category    Category @relation(fields: [categoryId], references: [id])
  orderItems  OrderItem[]

  @@index([categoryId])
  @@map("products")
}
```

### PostGIS Geometry Support

```prisma
model Location {
  id        String   @id @default(cuid())
  name      String
  // PostGIS geometry stored as Unsupported type
  point     Unsupported("geometry(Point, 4326)")

  @@map("locations")
}
```

### Enums

```prisma
enum OrderStatus {
  PENDING
  PROCESSING
  SHIPPED
  DELIVERED
  CANCELLED
}
```

## Repository Pattern

### Creating a Repository Service

```typescript
// packages/db/src/lib/product/product-repository.service.ts
import { Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma.service';
import { Prisma, Product } from '@prisma/client';

@Injectable()
export class ProductRepositoryService {
  constructor(private readonly prisma: PrismaService) {}

  async findAll(params?: {
    skip?: number;
    take?: number;
    cursor?: Prisma.ProductWhereUniqueInput;
    where?: Prisma.ProductWhereInput;
    orderBy?: Prisma.ProductOrderByWithRelationInput;
  }): Promise<Product[]> {
    return this.prisma.product.findMany(params);
  }

  async findById(id: string): Promise<Product | null> {
    return this.prisma.product.findUnique({
      where: { id },
      include: { category: true },
    });
  }

  async create(data: Prisma.ProductCreateInput): Promise<Product> {
    return this.prisma.product.create({ data });
  }

  async update(id: string, data: Prisma.ProductUpdateInput): Promise<Product> {
    return this.prisma.product.update({
      where: { id },
      data,
    });
  }

  async delete(id: string): Promise<Product> {
    return this.prisma.product.delete({ where: { id } });
  }
}
```

## Query Patterns

### Filtering and Pagination

```typescript
const products = await prisma.product.findMany({
  where: {
    name: { contains: 'shirt', mode: 'insensitive' },
    price: { gte: 10, lte: 100 },
    category: { name: 'Clothing' },
  },
  skip: 0,
  take: 20,
  orderBy: { createdAt: 'desc' },
  include: { category: true },
});
```

### Transactions

```typescript
const [order, inventory] = await prisma.$transaction([
  prisma.order.create({ data: orderData }),
  prisma.inventory.update({
    where: { productId },
    data: { quantity: { decrement: quantity } },
  }),
]);
```

### Raw SQL (for PostGIS)

```typescript
const nearbyLocations = await prisma.$queryRaw`
  SELECT id, name, ST_AsGeoJSON(point) as geojson
  FROM locations
  WHERE ST_DWithin(
    point,
    ST_SetSRID(ST_MakePoint(${lng}, ${lat}), 4326)::geography,
    ${radiusMeters}
  )
`;
```

## Migration Workflow

1. **Modify schema.prisma** with your changes
2. **Generate migration**: `pnpm prisma:migrate:dev --name descriptive_name`
3. **Review migration** in `prisma/migrations/`
4. **Test locally** before committing
5. **Apply in production**: `pnpm prisma:migrate`

## Seeding

```typescript
// packages/db/prisma/seed.ts
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  // Upsert to avoid duplicates
  await prisma.category.upsert({
    where: { slug: 'electronics' },
    update: {},
    create: {
      name: 'Electronics',
      slug: 'electronics',
    },
  });
}

main()
  .catch(console.error)
  .finally(() => prisma.$disconnect());
```

## Best Practices

1. **Use repository services** instead of direct Prisma calls in controllers
2. **Always include `@@map`** for explicit table names
3. **Add indexes** for frequently queried fields
4. **Use transactions** for related operations
5. **Name migrations descriptively** (e.g., `add_product_inventory`)
6. **Validate data** at the application layer before database operations
