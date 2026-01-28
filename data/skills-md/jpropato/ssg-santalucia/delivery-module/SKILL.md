---
name: delivery-module
description: Reglas de negocio y lógica específica del módulo de Delivery
---

# Módulo Delivery - Reglas de Negocio

## Entidades Principales

### Motoquero
- Tiene nombre, estado (activo/inactivo), turnos asignados
- Un motoquero puede trabajar en DÍA, NOCHE o AMBOS
- Solo aparece en el selector de viajes si está asignado al turno correspondiente

### Viaje
- Representa una salida del motoquero con uno o varios pedidos
- Tiene turno (DÍA/NOCHE) auto-detectado por hora del sistema
- Contiene múltiples direcciones pero solo se computa la más lejana
- Estados: BORRADOR → CONFIRMADO → LIQUIDADO

### Liquidación
- Agrupa viajes de un período (mes) y turno
- Genera ranking por km totales
- Aplica multiplicadores según posición
- Estados: BORRADOR → CERRADA → ABONADA

## Cálculo de Kilómetros

### Regla Principal
Solo se computan km de **IDA** (Local → dirección más lejana).
NO es ida y vuelta.

### Cálculo con múltiples direcciones
```typescript
// Pseudocódigo
const direcciones = ['Dir A', 'Dir B', 'Dir C'];
const kmPorDireccion = await Promise.all(
  direcciones.map(d => mapsService.calcularDistancia(d))
);
// [3.2, 5.1, 4.0]

const kmViaje = Math.max(...kmPorDireccion); // 5.1 km
```

### Caché de direcciones
- Antes de consultar Google Maps, buscar en tabla `DireccionCache`
- Normalizar dirección: mayúsculas, sin acentos, sin puntos
- Si existe y tiene < 90 días, usar valor cacheado
- Si no existe o expiró, consultar y guardar

## Turnos

### Definición
- **DÍA**: Hora del viaje < hora de corte (configurable, default 18:00)
- **NOCHE**: Hora del viaje >= hora de corte

### Auto-detección
```typescript
function detectarTurno(fecha: Date): 'DIA' | 'NOCHE' {
  const horaCorte = await configService.get('hora_corte_turno'); // "18:00"
  const [h, m] = horaCorte.split(':').map(Number);
  
  const hora = fecha.getHours();
  const minutos = fecha.getMinutes();
  
  if (hora < h || (hora === h && minutos < m)) {
    return 'DIA';
  }
  return 'NOCHE';
}
```

### Filtro de motoqueros
Al cargar un viaje, solo mostrar motoqueros que tengan el turno actual en su array de `turnos`.

## Liquidación Mensual

### Flujo
1. Usuario selecciona TURNO (Día o Noche)
2. Sistema obtiene viajes CONFIRMADOS del mes para ese turno
3. Agrupa por motoquero y suma km totales
4. Genera RANKING (mayor a menor km)
5. Asigna MULTIPLICADOR según posición
6. Calcula pago: `km × multiplicador × precio_km`
7. Identifica mayor cantidad de PEDIDOS → asigna BONO
8. Admin puede AJUSTAR manualmente
9. Confirma → Liquidación CERRADA
10. Marca como ABONADA cuando se paga

### Fórmula de Pago
```typescript
interface LiquidacionItem {
  motoqueroId: string;
  kmTotales: number;
  cantidadViajes: number;
  cantidadPedidos: number;
  ranking: number;
  multiplicador: number;
  subtotal: number;     // km × multiplicador × precio_km
  bono: number;         // 0 o (20 × precio_nafta)
  total: number;        // subtotal + bono
}

function calcularLiquidacion(viajes: Viaje[], params: LiquidacionParams) {
  // 1. Agrupar por motoquero
  const porMotoquero = groupBy(viajes, 'motoqueroId');
  
  // 2. Calcular totales
  const items = Object.entries(porMotoquero).map(([motoId, viajes]) => ({
    motoqueroId: motoId,
    kmTotales: sum(viajes, 'kmTotal'),
    cantidadViajes: viajes.length,
    cantidadPedidos: sum(viajes, 'cantidadPedidos'),
  }));
  
  // 3. Ordenar por km (ranking)
  items.sort((a, b) => b.kmTotales - a.kmTotales);
  
  // 4. Asignar multiplicadores
  const multiplicadores = [
    params.multiplicador1, // 5
    params.multiplicador2, // 3
    params.multiplicador3, // 2
  ];
  
  items.forEach((item, i) => {
    item.ranking = i + 1;
    item.multiplicador = multiplicadores[i] ?? params.multiplicadorDefault; // 1
    item.subtotal = item.kmTotales * item.multiplicador * params.precioKm;
  });
  
  // 5. Asignar bono al de más pedidos
  const maxPedidos = Math.max(...items.map(i => i.cantidadPedidos));
  const ganadoresBono = items.filter(i => i.cantidadPedidos === maxPedidos);
  const bono = params.multiplicadorBono * params.precioNafta; // 20 * 1200 = 24000
  const bonoPorGanador = bono / ganadoresBono.length;
  
  ganadoresBono.forEach(item => {
    item.bono = bonoPorGanador;
  });
  
  // 6. Calcular totales
  items.forEach(item => {
    item.total = item.subtotal + (item.bono ?? 0);
  });
  
  return items;
}
```

### Ajustes Manuales
- Admin puede modificar la liquidación antes de cerrarla
- Los ajustes se guardan en `datosAjustados` (JSON)
- Los datos reales permanecen en `datosReales` (JSON)
- Todo cambio queda auditado

### Estados de Liquidación
```
BORRADOR → CERRADA → ABONADA
              ↓
          REABIERTA → CERRADA (v2)
```

## Parámetros del Sistema

Guardados en tabla `Config`:

| Key | Tipo | Ejemplo |
|-----|------|---------|
| `precio_km` | Decimal | 150 |
| `precio_nafta_super` | Decimal | 1200 |
| `multiplicador_bono` | Integer | 20 |
| `hora_corte_turno` | String | "18:00" |
| `multiplicador_ranking_1` | Integer | 5 |
| `multiplicador_ranking_2` | Integer | 3 |
| `multiplicador_ranking_3` | Integer | 2 |
| `multiplicador_ranking_default` | Integer | 1 |
| `direccion_local` | String | "Av. X 123, Caseros" |

## Auditoría

Todo cambio debe registrarse en `AuditLog`:

```typescript
await auditService.log({
  userId: request.user.id,
  action: 'CREATE' | 'UPDATE' | 'DELETE',
  entity: 'Viaje' | 'Motoquero' | 'Liquidacion',
  entityId: entity.id,
  data: { before, after }, // Para UPDATE
});
```

## Generación de PDF

La liquidación debe poder exportarse a PDF con:
- Encabezado (nombre pizzería, período, turno)
- Parámetros aplicados
- Tabla de ranking con km, multiplicadores, subtotales
- Sección de bono
- Resumen por motoquero
- Detalle de viajes (anexo opcional)
- Firma/fecha de generación
