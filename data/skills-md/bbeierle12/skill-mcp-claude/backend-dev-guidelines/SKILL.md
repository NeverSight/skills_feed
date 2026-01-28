---
name: backend-dev-guidelines
description: Backend development guidelines for Node.js/Express/TypeScript applications. Layered architecture (Routes → Controllers → Services → Repositories), error handling, validation, middleware patterns, database access, and testing. Use when creating routes, endpoints, APIs, controllers, services, repositories, middleware, or working with backend code.
---

# Backend Development Guidelines

## Layered Architecture

```
Request Flow:
Client → Routes → Controllers → Services → Repositories → Database

src/
├── routes/           # Route definitions
├── controllers/      # Request handling
├── services/         # Business logic
├── repositories/     # Data access
├── middleware/       # Express middleware
├── validators/       # Input validation
├── types/           # TypeScript types
├── utils/           # Utilities
└── config/          # Configuration
```

## Layer Responsibilities

### Routes Layer
- Define endpoints
- Apply middleware
- Route to controllers

```typescript
// routes/users.routes.ts
import { Router } from 'express';
import { UserController } from '../controllers/user.controller';
import { validateRequest } from '../middleware/validate';
import { createUserSchema, updateUserSchema } from '../validators/user.validator';

const router = Router();
const controller = new UserController();

router.get('/', controller.getAll);
router.get('/:id', controller.getById);
router.post('/', validateRequest(createUserSchema), controller.create);
router.put('/:id', validateRequest(updateUserSchema), controller.update);
router.delete('/:id', controller.delete);

export default router;
```

### Controllers Layer
- Handle HTTP request/response
- Extract and validate input
- Call services
- Return responses

```typescript
// controllers/user.controller.ts
import { Request, Response, NextFunction } from 'express';
import { UserService } from '../services/user.service';

export class UserController {
  private userService = new UserService();

  getAll = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const users = await this.userService.findAll();
      res.json({ data: users });
    } catch (error) {
      next(error);
    }
  };

  getById = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const { id } = req.params;
      const user = await this.userService.findById(id);
      
      if (!user) {
        return res.status(404).json({ error: 'User not found' });
      }
      
      res.json({ data: user });
    } catch (error) {
      next(error);
    }
  };

  create = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const user = await this.userService.create(req.body);
      res.status(201).json({ data: user });
    } catch (error) {
      next(error);
    }
  };
}
```

### Services Layer
- Business logic
- Orchestrate operations
- Transaction management

```typescript
// services/user.service.ts
import { UserRepository } from '../repositories/user.repository';
import { CreateUserDto, UpdateUserDto } from '../types/user.types';
import { AppError } from '../utils/errors';

export class UserService {
  private userRepository = new UserRepository();

  async findAll() {
    return this.userRepository.findAll();
  }

  async findById(id: string) {
    return this.userRepository.findById(id);
  }

  async create(data: CreateUserDto) {
    // Business logic
    const existingUser = await this.userRepository.findByEmail(data.email);
    if (existingUser) {
      throw new AppError('Email already exists', 409);
    }

    // Hash password, etc.
    const hashedPassword = await hashPassword(data.password);
    
    return this.userRepository.create({
      ...data,
      password: hashedPassword,
    });
  }

  async update(id: string, data: UpdateUserDto) {
    const user = await this.userRepository.findById(id);
    if (!user) {
      throw new AppError('User not found', 404);
    }

    return this.userRepository.update(id, data);
  }
}
```

### Repositories Layer
- Database operations
- Query building
- Data mapping

```typescript
// repositories/user.repository.ts
import { prisma } from '../config/database';
import { User, CreateUserInput, UpdateUserInput } from '../types/user.types';

export class UserRepository {
  async findAll(): Promise<User[]> {
    return prisma.user.findMany({
      select: {
        id: true,
        email: true,
        name: true,
        createdAt: true,
      },
    });
  }

  async findById(id: string): Promise<User | null> {
    return prisma.user.findUnique({
      where: { id },
    });
  }

  async findByEmail(email: string): Promise<User | null> {
    return prisma.user.findUnique({
      where: { email },
    });
  }

  async create(data: CreateUserInput): Promise<User> {
    return prisma.user.create({
      data,
    });
  }

  async update(id: string, data: UpdateUserInput): Promise<User> {
    return prisma.user.update({
      where: { id },
      data,
    });
  }

  async delete(id: string): Promise<void> {
    await prisma.user.delete({
      where: { id },
    });
  }
}
```

## Middleware Patterns

### Error Handling Middleware

```typescript
// middleware/error.middleware.ts
import { Request, Response, NextFunction } from 'express';
import { AppError } from '../utils/errors';

export function errorHandler(
  error: Error,
  req: Request,
  res: Response,
  next: NextFunction
) {
  console.error('[Error]', {
    message: error.message,
    stack: error.stack,
    path: req.path,
    method: req.method,
  });

  if (error instanceof AppError) {
    return res.status(error.statusCode).json({
      error: error.message,
      code: error.code,
    });
  }

  // Don't expose internal errors
  res.status(500).json({
    error: 'Internal server error',
  });
}
```

### Validation Middleware

```typescript
// middleware/validate.middleware.ts
import { Request, Response, NextFunction } from 'express';
import { ZodSchema } from 'zod';

export function validateRequest(schema: ZodSchema) {
  return (req: Request, res: Response, next: NextFunction) => {
    try {
      schema.parse({
        body: req.body,
        query: req.query,
        params: req.params,
      });
      next();
    } catch (error) {
      res.status(400).json({
        error: 'Validation failed',
        details: error.errors,
      });
    }
  };
}
```

### Authentication Middleware

```typescript
// middleware/auth.middleware.ts
import { Request, Response, NextFunction } from 'express';
import { verifyToken } from '../utils/jwt';

export async function authenticate(
  req: Request,
  res: Response,
  next: NextFunction
) {
  try {
    const token = req.headers.authorization?.replace('Bearer ', '');
    
    if (!token) {
      return res.status(401).json({ error: 'No token provided' });
    }

    const payload = await verifyToken(token);
    req.user = payload;
    next();
  } catch (error) {
    res.status(401).json({ error: 'Invalid token' });
  }
}
```

## Input Validation

```typescript
// validators/user.validator.ts
import { z } from 'zod';

export const createUserSchema = z.object({
  body: z.object({
    email: z.string().email(),
    password: z.string().min(8),
    name: z.string().min(2).max(100),
  }),
});

export const updateUserSchema = z.object({
  params: z.object({
    id: z.string().uuid(),
  }),
  body: z.object({
    name: z.string().min(2).max(100).optional(),
    email: z.string().email().optional(),
  }),
});

export type CreateUserDto = z.infer<typeof createUserSchema>['body'];
export type UpdateUserDto = z.infer<typeof updateUserSchema>['body'];
```

## Error Handling

```typescript
// utils/errors.ts
export class AppError extends Error {
  constructor(
    message: string,
    public statusCode: number = 500,
    public code?: string
  ) {
    super(message);
    this.name = 'AppError';
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string) {
    super(`${resource} not found`, 404, 'NOT_FOUND');
  }
}

export class ValidationError extends AppError {
  constructor(message: string) {
    super(message, 400, 'VALIDATION_ERROR');
  }
}

export class UnauthorizedError extends AppError {
  constructor(message = 'Unauthorized') {
    super(message, 401, 'UNAUTHORIZED');
  }
}
```

## Testing

### Unit Tests (Services)

```typescript
// services/user.service.test.ts
import { UserService } from './user.service';
import { UserRepository } from '../repositories/user.repository';

jest.mock('../repositories/user.repository');

describe('UserService', () => {
  let service: UserService;
  let mockRepository: jest.Mocked<UserRepository>;

  beforeEach(() => {
    mockRepository = new UserRepository() as jest.Mocked<UserRepository>;
    service = new UserService();
    (service as any).userRepository = mockRepository;
  });

  describe('create', () => {
    it('should throw if email exists', async () => {
      mockRepository.findByEmail.mockResolvedValue({ id: '1', email: 'test@test.com' });

      await expect(service.create({
        email: 'test@test.com',
        password: 'password',
        name: 'Test',
      })).rejects.toThrow('Email already exists');
    });

    it('should create user if email is unique', async () => {
      mockRepository.findByEmail.mockResolvedValue(null);
      mockRepository.create.mockResolvedValue({
        id: '1',
        email: 'new@test.com',
        name: 'Test',
      });

      const result = await service.create({
        email: 'new@test.com',
        password: 'password',
        name: 'Test',
      });

      expect(result.email).toBe('new@test.com');
    });
  });
});
```

### Integration Tests (Routes)

```typescript
// routes/users.routes.test.ts
import request from 'supertest';
import { app } from '../app';

describe('Users API', () => {
  describe('GET /api/users', () => {
    it('should return all users', async () => {
      const response = await request(app)
        .get('/api/users')
        .expect(200);

      expect(response.body.data).toBeInstanceOf(Array);
    });
  });

  describe('POST /api/users', () => {
    it('should create a user', async () => {
      const response = await request(app)
        .post('/api/users')
        .send({
          email: 'test@test.com',
          password: 'password123',
          name: 'Test User',
        })
        .expect(201);

      expect(response.body.data.email).toBe('test@test.com');
    });

    it('should validate input', async () => {
      await request(app)
        .post('/api/users')
        .send({
          email: 'invalid-email',
        })
        .expect(400);
    });
  });
});
```

## Resource Files

For detailed patterns, see:
- [database-patterns.md](resources/database-patterns.md)
- [authentication.md](resources/authentication.md)
- [error-handling.md](resources/error-handling.md)
- [testing.md](resources/testing.md)
