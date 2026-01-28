---
name: backend-conventions
description: Convenciones y patrones para el desarrollo backend con Fastify + Prisma
---

# Backend Conventions

## Stack
- Node.js 22 LTS
- Fastify 5.x
- TypeScript 5.x
- Prisma ORM 6.x
- Zod para validación
- Better-Auth para autenticación

## Estructura de Carpetas

```
backend/src/
├── app.ts                  # Configuración Fastify
├── index.ts                # Entry point
│
├── modules/                # Módulos de negocio
│   ├── core/
│   │   ├── auth/           # Better-Auth config
│   │   │   ├── auth.config.ts
│   │   │   └── auth.routes.ts
│   │   ├── users/
│   │   │   ├── users.controller.ts
│   │   │   ├── users.service.ts
│   │   │   └── users.schemas.ts
│   │   └── config/
│   │       ├── config.controller.ts
│   │       └── config.service.ts
│   │
│   └── delivery/
│       ├── viajes/
│       │   ├── viajes.controller.ts
│       │   ├── viajes.service.ts
│       │   └── viajes.schemas.ts
│       ├── motoqueros/
│       ├── liquidaciones/
│       └── maps/
│
├── lib/
│   ├── prisma.ts           # Prisma client singleton
│   ├── errors.ts           # Custom errors
│   └── logger.ts           # Logger config
│
└── plugins/                # Plugins Fastify
    ├── auth.ts             # Auth middleware
    ├── cors.ts
    └── errorHandler.ts

prisma/
├── schema.prisma
└── migrations/
```

## Convenciones de Código

### Controllers

```typescript
// modules/delivery/viajes/viajes.controller.ts
import { FastifyPluginAsync } from 'fastify';
import { viajesService } from './viajes.service';
import { createViajeSchema, updateViajeSchema } from './viajes.schemas';

export const viajesController: FastifyPluginAsync = async (fastify) => {
  // GET /api/delivery/viajes
  fastify.get('/', async (request, reply) => {
    const viajes = await viajesService.findAll(request.query);
    return viajes;
  });

  // GET /api/delivery/viajes/:id
  fastify.get('/:id', async (request, reply) => {
    const { id } = request.params as { id: string };
    const viaje = await viajesService.findById(id);
    if (!viaje) {
      return reply.status(404).send({ error: 'Viaje no encontrado' });
    }
    return viaje;
  });

  // POST /api/delivery/viajes
  fastify.post('/', {
    schema: { body: createViajeSchema },
  }, async (request, reply) => {
    const viaje = await viajesService.create(request.body, request.user.id);
    return reply.status(201).send(viaje);
  });

  // PATCH /api/delivery/viajes/:id
  fastify.patch('/:id', {
    schema: { body: updateViajeSchema },
  }, async (request, reply) => {
    const { id } = request.params as { id: string };
    const viaje = await viajesService.update(id, request.body, request.user.id);
    return viaje;
  });

  // DELETE /api/delivery/viajes/:id
  fastify.delete('/:id', async (request, reply) => {
    const { id } = request.params as { id: string };
    await viajesService.delete(id);
    return reply.status(204).send();
  });
};
```

### Services

```typescript
// modules/delivery/viajes/viajes.service.ts
import { prisma } from '@/lib/prisma';
import { mapsService } from '../maps/maps.service';
import { auditService } from '@/modules/core/audit/audit.service';
import type { CreateViajeDto, UpdateViajeDto } from './viajes.schemas';

export const viajesService = {
  async findAll(filters?: ViajesFilters) {
    return prisma.viaje.findMany({
      where: {
        turno: filters?.turno,
        estado: filters?.estado,
        fecha: {
          gte: filters?.fechaDesde,
          lte: filters?.fechaHasta,
        },
      },
      include: {
        motoquero: true,
        direcciones: true,
      },
      orderBy: { fecha: 'desc' },
    });
  },

  async findById(id: string) {
    return prisma.viaje.findUnique({
      where: { id },
      include: {
        motoquero: true,
        direcciones: true,
      },
    });
  },

  async create(data: CreateViajeDto, userId: string) {
    // 1. Calcular km para cada dirección
    const direccionesConKm = await Promise.all(
      data.direcciones.map(async (dir) => ({
        direccion: dir,
        km: await mapsService.calcularDistancia(dir),
      }))
    );

    // 2. Encontrar la más lejana
    const masLejana = direccionesConKm.reduce((max, curr) => 
      curr.km > max.km ? curr : max
    );

    // 3. Crear viaje
    const viaje = await prisma.viaje.create({
      data: {
        fecha: data.fecha ?? new Date(),
        turno: data.turno,
        motoqueroId: data.motoqueroId,
        kmTotal: masLejana.km,
        cantidadPedidos: data.direcciones.length,
        direcciones: {
          create: direccionesConKm.map((d, i) => ({
            direccion: d.direccion,
            direccionNorm: normalizarDireccion(d.direccion),
            km: d.km,
            esMasLejana: d.direccion === masLejana.direccion,
          })),
        },
      },
      include: { direcciones: true, motoquero: true },
    });

    // 4. Auditar
    await auditService.log({
      userId,
      action: 'CREATE',
      entity: 'Viaje',
      entityId: viaje.id,
      data: viaje,
    });

    return viaje;
  },

  async update(id: string, data: UpdateViajeDto, userId: string) {
    const before = await this.findById(id);
    
    const viaje = await prisma.viaje.update({
      where: { id },
      data,
      include: { direcciones: true, motoquero: true },
    });

    await auditService.log({
      userId,
      action: 'UPDATE',
      entity: 'Viaje',
      entityId: id,
      data: { before, after: viaje },
    });

    return viaje;
  },

  async delete(id: string) {
    await prisma.viaje.delete({ where: { id } });
  },
};
```

### Schemas (Zod)

```typescript
// modules/delivery/viajes/viajes.schemas.ts
import { z } from 'zod';

export const createViajeSchema = z.object({
  motoqueroId: z.string().cuid(),
  turno: z.enum(['DIA', 'NOCHE']),
  fecha: z.coerce.date().optional(),
  direcciones: z.array(z.string().min(5)).min(1),
});

export const updateViajeSchema = z.object({
  motoqueroId: z.string().cuid().optional(),
  turno: z.enum(['DIA', 'NOCHE']).optional(),
  fecha: z.coerce.date().optional(),
  kmTotal: z.number().positive().optional(),
  estado: z.enum(['BORRADOR', 'CONFIRMADO']).optional(),
});

export type CreateViajeDto = z.infer<typeof createViajeSchema>;
export type UpdateViajeDto = z.infer<typeof updateViajeSchema>;
```

### Registrar Rutas

```typescript
// app.ts
import Fastify from 'fastify';
import cors from '@fastify/cors';
import { authPlugin } from './plugins/auth';
import { errorHandler } from './plugins/errorHandler';

// Modules
import { authRoutes } from './modules/core/auth/auth.routes';
import { viajesController } from './modules/delivery/viajes/viajes.controller';
import { motoquerosController } from './modules/delivery/motoqueros/motoqueros.controller';
import { liquidacionesController } from './modules/delivery/liquidaciones/liquidaciones.controller';

export async function buildApp() {
  const app = Fastify({ logger: true });

  // Plugins
  await app.register(cors, { origin: true });
  await app.register(authPlugin);
  app.setErrorHandler(errorHandler);

  // Routes
  await app.register(authRoutes, { prefix: '/api/auth' });
  
  // Protected routes
  await app.register(async (protectedApp) => {
    protectedApp.addHook('onRequest', protectedApp.authenticate);
    
    await protectedApp.register(viajesController, { prefix: '/api/delivery/viajes' });
    await protectedApp.register(motoquerosController, { prefix: '/api/delivery/motoqueros' });
    await protectedApp.register(liquidacionesController, { prefix: '/api/delivery/liquidaciones' });
  });

  return app;
}
```

## Manejo de Errores

```typescript
// lib/errors.ts
export class AppError extends Error {
  constructor(
    public statusCode: number,
    public message: string,
    public code?: string
  ) {
    super(message);
  }
}

export class NotFoundError extends AppError {
  constructor(entity: string, id: string) {
    super(404, `${entity} con id ${id} no encontrado`, 'NOT_FOUND');
  }
}

export class ValidationError extends AppError {
  constructor(message: string) {
    super(400, message, 'VALIDATION_ERROR');
  }
}

// plugins/errorHandler.ts
export const errorHandler: FastifyErrorHandler = (error, request, reply) => {
  if (error instanceof AppError) {
    return reply.status(error.statusCode).send({
      error: error.code,
      message: error.message,
    });
  }

  // Prisma errors
  if (error.code === 'P2025') {
    return reply.status(404).send({
      error: 'NOT_FOUND',
      message: 'Registro no encontrado',
    });
  }

  // Default
  request.log.error(error);
  return reply.status(500).send({
    error: 'INTERNAL_ERROR',
    message: 'Error interno del servidor',
  });
};
```

## Prisma Best Practices

```typescript
// lib/prisma.ts
import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

export const prisma = globalForPrisma.prisma ?? new PrismaClient({
  log: process.env.NODE_ENV === 'development' ? ['query', 'error', 'warn'] : ['error'],
});

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma;
}
```

## Comandos Útiles

```bash
# Desarrollo
npm run dev                 # Iniciar servidor con hot reload
npm run build               # Build para producción
npm run start               # Iniciar producción

# Prisma
npx prisma generate         # Generar cliente
npx prisma migrate dev      # Crear migración
npx prisma migrate deploy   # Aplicar migraciones
npx prisma studio           # GUI para ver datos
npx prisma db push          # Sync schema sin migración

# Tests
npm run test                # Correr tests
npm run test:watch          # Tests en watch mode
```
