---
name: frontend-conventions
description: Convenciones y patrones para el desarrollo frontend con React + Mantine
---

# Frontend Conventions

## Stack
- React 19 + TypeScript
- Vite 6.x
- Mantine v7 + TailwindCSS
- TanStack Query v5
- Zustand v5
- React Hook Form + Zod

## Estructura de Carpetas

```
frontend/src/
├── app/                    # Configuración global
│   ├── providers.tsx       # MantineProvider, QueryProvider, etc.
│   ├── router.tsx          # React Router config
│   └── App.tsx
│
├── modules/                # Módulos de negocio
│   ├── core/               # Auth, Layout, Config
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── services/
│   │   └── stores/
│   │
│   └── delivery/           # Módulo principal
│       ├── components/     # Componentes del módulo
│       ├── hooks/          # Custom hooks (useViajes, etc.)
│       ├── services/       # API calls
│       ├── stores/         # Zustand stores
│       ├── types/          # TypeScript types
│       └── pages/          # Páginas/rutas
│
├── shared/                 # Compartido entre módulos
│   ├── components/         # Componentes genéricos
│   ├── hooks/              # Hooks reutilizables
│   └── utils/              # Utilidades
│
└── lib/                    # Configuraciones
    ├── api.ts              # Cliente HTTP base
    ├── queryClient.ts      # TanStack Query config
    └── auth.ts             # Better-Auth client
```

## Convenciones de Código

### Componentes

```tsx
// ✅ Correcto: Functional component con TypeScript
interface ViajeCardProps {
  viaje: Viaje;
  onEdit?: (id: string) => void;
}

export function ViajeCard({ viaje, onEdit }: ViajeCardProps) {
  return (
    <Card>
      {/* ... */}
    </Card>
  );
}
```

### Hooks de TanStack Query

```tsx
// hooks/useViajes.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { viajesApi } from '../services/viajes.api';

export function useViajes(filters?: ViajesFilters) {
  return useQuery({
    queryKey: ['viajes', filters],
    queryFn: () => viajesApi.getAll(filters),
  });
}

export function useCreateViaje() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: viajesApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['viajes'] });
    },
  });
}
```

### Stores (Zustand)

```tsx
// stores/delivery.store.ts
import { create } from 'zustand';

interface DeliveryState {
  selectedTurno: 'DIA' | 'NOCHE' | null;
  setTurno: (turno: 'DIA' | 'NOCHE') => void;
}

export const useDeliveryStore = create<DeliveryState>((set) => ({
  selectedTurno: null,
  setTurno: (turno) => set({ selectedTurno: turno }),
}));
```

### API Services

```tsx
// services/viajes.api.ts
import { api } from '@/lib/api';
import type { Viaje, CreateViajeDto } from '../types/viaje.types';

export const viajesApi = {
  getAll: (filters?: ViajesFilters) => 
    api.get<Viaje[]>('/api/delivery/viajes', { params: filters }),
  
  getById: (id: string) => 
    api.get<Viaje>(`/api/delivery/viajes/${id}`),
  
  create: (data: CreateViajeDto) => 
    api.post<Viaje>('/api/delivery/viajes', data),
  
  update: (id: string, data: Partial<CreateViajeDto>) => 
    api.patch<Viaje>(`/api/delivery/viajes/${id}`, data),
  
  delete: (id: string) => 
    api.delete(`/api/delivery/viajes/${id}`),
};
```

## Mantine UI Patterns

### Usar componentes de Mantine, no HTML nativo

```tsx
// ❌ Incorrecto
<button className="...">Click</button>
<input type="text" />

// ✅ Correcto
<Button>Click</Button>
<TextInput label="Nombre" />
```

### Tables con @mantine/core

```tsx
import { Table } from '@mantine/core';

<Table striped highlightOnHover>
  <Table.Thead>
    <Table.Tr>
      <Table.Th>Fecha</Table.Th>
      <Table.Th>Motoquero</Table.Th>
    </Table.Tr>
  </Table.Thead>
  <Table.Tbody>
    {viajes.map((viaje) => (
      <Table.Tr key={viaje.id}>
        <Table.Td>{viaje.fecha}</Table.Td>
        <Table.Td>{viaje.motoquero.nombre}</Table.Td>
      </Table.Tr>
    ))}
  </Table.Tbody>
</Table>
```

### Modales y Drawers

```tsx
import { useDisclosure } from '@mantine/hooks';
import { Modal, Drawer } from '@mantine/core';

function ViajesPage() {
  const [opened, { open, close }] = useDisclosure(false);
  
  return (
    <>
      <Button onClick={open}>Nuevo Viaje</Button>
      
      <Drawer opened={opened} onClose={close} title="Nuevo Viaje">
        <ViajeForm onSuccess={close} />
      </Drawer>
    </>
  );
}
```

## Formularios

Usar React Hook Form + Zod + Mantine:

```tsx
import { useForm, zodResolver } from '@mantine/form';
import { z } from 'zod';

const viajeSchema = z.object({
  motoqueroId: z.string().min(1, 'Seleccione un motoquero'),
  direcciones: z.array(z.string()).min(1, 'Ingrese al menos una dirección'),
});

function ViajeForm() {
  const form = useForm({
    initialValues: { motoqueroId: '', direcciones: [''] },
    validate: zodResolver(viajeSchema),
  });
  
  return (
    <form onSubmit={form.onSubmit(handleSubmit)}>
      <Select
        label="Motoquero"
        {...form.getInputProps('motoqueroId')}
      />
      {/* ... */}
    </form>
  );
}
```

## Rutas

```tsx
// app/router.tsx
import { createBrowserRouter } from 'react-router-dom';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <MainLayout />,
    children: [
      { index: true, element: <DashboardPage /> },
      {
        path: 'delivery',
        children: [
          { path: 'viajes', element: <ViajesPage /> },
          { path: 'motoqueros', element: <MotosPage /> },
          { path: 'liquidaciones', element: <LiquidacionesPage /> },
        ],
      },
      {
        path: 'config',
        children: [
          { path: 'parametros', element: <ParametrosPage /> },
          { path: 'usuarios', element: <UsuariosPage /> },
        ],
      },
    ],
  },
  { path: '/login', element: <LoginPage /> },
]);
```
