---
name: wms-module
description: |
  WMS NestJS module (倉儲管理 NestJS 模組). Use when working with warehouse management, inventory tracking (庫存追蹤), location management (儲位管理), stock transactions (庫存異動), batch management (批次管理), or warehouse maps (倉庫地圖). Covers LocationService, MaterialService, StockService, OrderService, WarehouseMapService. Keywords: WMS, warehouse, 倉儲, 庫存, 儲位, TypeORM, NestJS, inventory, batch, stock
---

# WMS Base NestJS Module (倉儲管理模組)

## Overview

`@rytass/wms-base-nestjs-module` 提供 NestJS 倉儲管理系統的基礎模組，支援儲位樹狀結構、物料管理、庫存異動追蹤、訂單管理及倉庫地圖功能。

## Quick Start

### 安裝

```bash
npm install @rytass/wms-base-nestjs-module
```

**Peer Dependencies:**
- `@nestjs/common` ^9.0.0 || ^10.0.0
- `@nestjs/typeorm` ^9.0.0 || ^10.0.0
- `typeorm` ^0.3.0

### 基本設定

```typescript
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { WMSBaseModule } from '@rytass/wms-base-nestjs-module';

@Module({
  imports: [
    TypeOrmModule.forRoot({
      type: 'postgres',
      // ... database config
    }),
    WMSBaseModule.forRoot({
      allowNegativeStock: false, // 預設: false, 禁止負庫存
    }),
  ],
})
export class AppModule {}
```

### 非同步設定

```typescript
import { WMSBaseModule, WMSBaseModuleAsyncOptions } from '@rytass/wms-base-nestjs-module';
import { ConfigService } from '@nestjs/config';

@Module({
  imports: [
    // useFactory 方式
    WMSBaseModule.forRootAsync({
      inject: [ConfigService],
      useFactory: (config: ConfigService) => ({
        allowNegativeStock: config.get('WMS_ALLOW_NEGATIVE_STOCK', false),
      }),
    }),

    // 或 useClass 方式（使用自訂 Factory）
    // WMSBaseModule.forRootAsync({
    //   useClass: WMSConfigFactory,
    // }),

    // 或 useExisting 方式（重用現有 Factory）
    // WMSBaseModule.forRootAsync({
    //   useExisting: ExistingWMSConfigFactory,
    // }),
  ],
})
export class AppModule {}
```

## Core Entities

模組提供以下基礎 Entity，皆可透過繼承擴展：

### LocationEntity (儲位)

```typescript
import { LocationEntity } from '@rytass/wms-base-nestjs-module';

// 基礎結構 - Table: 'locations'
@Entity('locations')
@TableInheritance({ column: { type: 'varchar', name: 'entityName' } })
@Tree('materialized-path')
class LocationEntity {
  @PrimaryColumn({ type: 'varchar' })
  id: string;

  @TreeChildren()
  children: LocationEntity[];

  @TreeParent()
  parent: LocationEntity;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;

  @DeleteDateColumn()
  deletedAt: Date | null;  // Soft delete
}
```

> 使用 TypeORM `@Tree('materialized-path')` 實作樹狀結構

### MaterialEntity (物料)

```typescript
import { MaterialEntity } from '@rytass/wms-base-nestjs-module';

// Table: 'materials'
@Entity('materials')
@TableInheritance({ column: { type: 'varchar', name: 'entityName' } })
class MaterialEntity {
  @PrimaryColumn({ type: 'varchar' })
  id: string;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;

  @DeleteDateColumn()
  deletedAt: Date | null;  // Soft delete

  @OneToMany(() => BatchEntity, batch => batch.material)
  batches: Relation<BatchEntity[]>;

  @OneToMany(() => StockEntity, stock => stock.material)
  stocks: Relation<StockEntity[]>;
}
```

### BatchEntity (批次)

```typescript
import { BatchEntity } from '@rytass/wms-base-nestjs-module';

// Table: 'batches'
// 複合主鍵: id + materialId
@Entity('batches')
class BatchEntity {
  @PrimaryColumn('varchar')
  id: string;

  @PrimaryColumn('varchar')
  materialId: string;

  @ManyToOne(() => MaterialEntity, material => material.batches)
  @JoinColumn({ name: 'materialId', referencedColumnName: 'id' })
  material: Relation<MaterialEntity>;

  @OneToMany(() => StockEntity, stock => stock.batch)
  stocks: Relation<StockEntity[]>;
}
```

### StockEntity (庫存異動)

```typescript
import { StockEntity } from '@rytass/wms-base-nestjs-module';

// Table: 'stocks'
@Entity('stocks')
@TableInheritance({ column: { type: 'varchar', name: 'entityName' } })
class StockEntity {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ type: 'varchar' })
  materialId: string;

  @Column({ type: 'varchar' })
  batchId: string;

  @Column({ type: 'varchar' })
  locationId: string;

  @Column({ type: 'varchar' })
  orderId: string;

  @Column({ type: 'numeric' })
  quantity: number;     // 正數為入庫，負數為出庫

  @ManyToOne(() => MaterialEntity, material => material.stocks)
  @JoinColumn({ name: 'materialId', referencedColumnName: 'id' })
  material: Relation<MaterialEntity>;

  @ManyToOne(() => BatchEntity, batch => batch.stocks)
  @JoinColumn([
    { name: 'materialId', referencedColumnName: 'materialId' },
    { name: 'batchId', referencedColumnName: 'id' },
  ])
  batch: Relation<BatchEntity>;

  @ManyToOne(() => OrderEntity, order => order.stocks)
  @JoinColumn({ name: 'orderId', referencedColumnName: 'id' })
  order: Relation<OrderEntity>;

  @CreateDateColumn()
  createdAt: Date;
}
```

### OrderEntity (訂單)

```typescript
import { OrderEntity } from '@rytass/wms-base-nestjs-module';

// Table: 'orders'
@Entity('orders')
@TableInheritance({ column: { type: 'varchar', name: 'entityName' } })
class OrderEntity {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @OneToMany(() => StockEntity, stock => stock.order)
  stocks: Relation<StockEntity>[];
}
```

### WarehouseMapEntity (倉庫地圖)

> **注意：** `WarehouseMapService` 有從 index.ts 導出，可直接 import。但 `WarehouseMapEntity`、`MapRangeType`、`MapRangeColor`、`MapData` 等類型目前未從 index.ts 導出，需直接從原始碼路徑 import 或自行定義。

```typescript
// WarehouseMapService 可直接 import
import { WarehouseMapService } from '@rytass/wms-base-nestjs-module';

// WarehouseMapEntity 需從原始碼路徑 import（若必要）

// Table: 'warehouse_maps'
@Entity('warehouse_maps')
class WarehouseMapEntity {
  @PrimaryColumn('varchar')  // 對應 locationId
  id: string;

  @Column({ type: 'jsonb' })
  mapData: MapData;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
```

## Services

### LocationService (儲位服務)

```typescript
import { LocationService, LocationEntity } from '@rytass/wms-base-nestjs-module';

@Injectable()
export class WarehouseService {
  constructor(private readonly locationService: LocationService) {}

  // 建立儲位
  async createLocation() {
    // 建立根儲位
    const warehouse = await this.locationService.create({
      id: 'WAREHOUSE-A',
    });

    // 建立子儲位
    const zone = await this.locationService.create({
      id: 'ZONE-A1',
      parentId: 'WAREHOUSE-A',
    });

    return zone;
  }

  // 封存儲位 (Soft Delete)
  // 注意: 只有庫存為 0 的儲位才能封存
  async archiveLocation(id: string) {
    await this.locationService.archive(id);
    // 會連同所有子儲位一起封存
  }

  // 解除封存
  async unArchiveLocation(id: string) {
    const location = await this.locationService.unArchive(id);
    return location;
  }
}
```

### MaterialService (物料服務)

```typescript
import { MaterialService, MaterialEntity } from '@rytass/wms-base-nestjs-module';

@Injectable()
export class ProductService {
  constructor(private readonly materialService: MaterialService) {}

  // 建立物料
  async createMaterial() {
    const material = await this.materialService.create({
      id: 'SKU-001',
    });

    return material;
  }
}
```

### StockService (庫存服務)

```typescript
import {
  StockService,
  StockFindDto,
  StockFindAllDto,
  StockSorter,
} from '@rytass/wms-base-nestjs-module';

@Injectable()
export class InventoryService {
  constructor(private readonly stockService: StockService) {}

  // 查詢庫存數量 (回傳加總數量)
  // find() 可選傳入 manager 參數供交易使用
  async getStockQuantity(locationId: string, materialId: string): Promise<number> {
    return this.stockService.find({
      locationIds: [locationId],
      materialIds: [materialId],
      exactLocationMatch: true, // 只查詢該儲位，不包含子儲位
    });
  }

  // 查詢儲位樹下的總庫存 (包含所有子儲位)
  async getTotalStock(locationId: string): Promise<number> {
    return this.stockService.find({
      locationIds: [locationId],
      // exactLocationMatch: false (預設) - 包含所有子儲位
    });
  }

  // 查詢庫存異動記錄
  async getTransactionLogs(options: StockFindAllDto) {
    return this.stockService.findTransactions({
      locationIds: ['WAREHOUSE-A'],
      materialIds: ['SKU-001'],
      batchIds: ['BATCH-001'],
      offset: 0,
      limit: 20,  // 最大 100
      sorter: StockSorter.CREATED_AT_DESC,
    });
    // 回傳: StockCollectionDto { transactionLogs, total, offset, limit }
  }
}
```

**StockFindDto 參數:**

| 參數 | 類型 | 說明 |
|------|------|------|
| `locationIds` | `string[]` | 儲位 ID 列表 |
| `materialIds` | `string[]` | 物料 ID 列表 |
| `batchIds` | `string[]` | 批次 ID 列表 |
| `exactLocationMatch` | `boolean` | `true`: 只查詢指定儲位；`false` (預設): 包含子儲位 |

**StockFindAllDto 額外參數:**

| 參數 | 類型 | 預設值 | 說明 |
|------|------|--------|------|
| `offset` | `number` | `0` | 分頁偏移 |
| `limit` | `number` | `20` | 每頁筆數 (最大 100) |
| `sorter` | `StockSorter` | `CREATED_AT_DESC` | 排序方式 |

**StockCollectionDto 回傳結構:**

```typescript
interface StockCollectionDto {
  transactionLogs: StockTransactionLogDto[];
  total: number;
  offset: number;
  limit: number;
}

// 泛型版本，排除關聯欄位
type StockTransactionLogDto<Stock extends StockEntity = StockEntity> = Omit<
  Stock,
  'material' | 'batch' | 'location' | 'order'
>;

// 實際包含欄位（以預設 StockEntity 為例）:
// { id, materialId, batchId, locationId, orderId, quantity, createdAt }
// 注意: 原始碼 Omit 了 'location'，但 StockEntity 實際上沒有 location relation
// （只有 locationId 欄位），這是防禦性設計
```

### OrderService (訂單服務)

```typescript
import {
  OrderService,
  OrderEntity,
  OrderCreateDto,
  BatchCreateDto,
} from '@rytass/wms-base-nestjs-module';
import { Entity, Column } from 'typeorm';

// 擴展訂單 Entity
@Entity('custom_orders')
export class CustomOrderEntity extends OrderEntity {
  @Column()
  orderNumber: string;

  @Column()
  type: 'INBOUND' | 'OUTBOUND';
}

@Injectable()
export class OrderManagementService {
  constructor(private readonly orderService: OrderService) {}

  // 建立入庫訂單
  async createInboundOrder() {
    const order = await this.orderService.createOrder(CustomOrderEntity, {
      order: {
        orderNumber: 'IN-2024-001',
        type: 'INBOUND',
      },
      batches: [
        {
          id: 'BATCH-001',
          materialId: 'SKU-001',
          locationId: 'ZONE-A1',
          quantity: 100, // 正數: 入庫
        },
      ],
    });

    return order;
  }

  // 建立出庫訂單
  async createOutboundOrder() {
    const order = await this.orderService.createOrder(CustomOrderEntity, {
      order: {
        orderNumber: 'OUT-2024-001',
        type: 'OUTBOUND',
      },
      batches: [
        {
          id: 'BATCH-001',
          materialId: 'SKU-001',
          locationId: 'ZONE-A1',
          quantity: -50, // 負數: 出庫
        },
      ],
    });

    return order;
    // 若 allowNegativeStock: false 且庫存不足，會拋出 StockQuantityNotEnoughError
  }

  // 檢查是否可建立庫存異動
  async canCreateStock(batch: BatchCreateDto): Promise<boolean> {
    return this.orderService.canCreateStock(batch);
  }
}
```

**BatchCreateDto:**

```typescript
interface BatchCreateDto {
  id: string;
  materialId: string;
  locationId: string;
  quantity: number;
}
```

**OrderCreateDto:**

```typescript
type OrderDto<O extends OrderEntity = OrderEntity> = DeepPartial<Omit<O, 'stocks'>>;

type OrderCreateDto<O extends OrderEntity = OrderEntity> = {
  order: OrderDto<O>;
  batches: BatchCreateDto[];
};
```

### WarehouseMapService (倉庫地圖服務)

> **注意：** `WarehouseMapService` 有從 index.ts 導出，可直接 import。但 `MapRangeType` 和 `MapRangeColor` 目前未從 index.ts 導出，需自行定義或直接使用字串值。

```typescript
import { WarehouseMapService } from '@rytass/wms-base-nestjs-module';
// MapRangeType/MapRangeColor 可直接使用字串值或自行定義 enum

// 可自行定義 enum 或使用字串常數
enum MapRangeType {
  RECTANGLE = 'RECTANGLE',
  POLYGON = 'POLYGON',
}

enum MapRangeColor {
  RED = 'RED',
  YELLOW = 'YELLOW',
  GREEN = 'GREEN',
  BLUE = 'BLUE',
  BLACK = 'BLACK',
}

@Injectable()
export class MapService {
  constructor(private readonly warehouseMapService: WarehouseMapService) {}

  // 更新倉庫地圖
  async updateMap(locationId: string) {
    const map = await this.warehouseMapService.updateMap(
      locationId,
      // backgrounds: 背景圖片
      [
        {
          id: 'bg-1',
          filename: 'warehouse-floor.png',
          x: 0,
          y: 0,
          width: 1000,
          height: 800,
        },
      ],
      // ranges: 區域標記
      [
        // 矩形區域
        {
          id: 'zone-a1',
          type: MapRangeType.RECTANGLE,
          color: MapRangeColor.GREEN,
          x: 100,
          y: 100,
          width: 200,
          height: 150,
        },
        // 多邊形區域
        {
          id: 'zone-special',
          type: MapRangeType.POLYGON,
          color: MapRangeColor.YELLOW,
          points: [
            { x: 400, y: 100 },
            { x: 500, y: 100 },
            { x: 550, y: 200 },
            { x: 400, y: 200 },
          ],
        },
      ],
    );

    return map;
  }

  // 取得地圖資料
  async getMap(locationId: string) {
    return this.warehouseMapService.getMapById(locationId);
    // 若不存在回傳: { id, backgrounds: [], ranges: [] }
  }

  // 刪除地圖
  async deleteMap(locationId: string) {
    await this.warehouseMapService.deleteMapById(locationId);
  }
}
```

## Custom Entities (擴展 Entity)

透過 `forRoot` 或 `forRootAsync` 傳入自訂 Entity：

```typescript
import {
  WMSBaseModule,
  LocationEntity,
  MaterialEntity,
  StockEntity,
  BatchEntity,
  OrderEntity,
} from '@rytass/wms-base-nestjs-module';
import { Entity, Column } from 'typeorm';

// 擴展儲位
@Entity('custom_locations')
export class CustomLocationEntity extends LocationEntity {
  @Column()
  name: string;

  @Column({ nullable: true })
  description: string;
}

// 擴展物料
@Entity('custom_materials')
export class CustomMaterialEntity extends MaterialEntity {
  @Column()
  name: string;

  @Column()
  sku: string;
}

// 模組設定
@Module({
  imports: [
    WMSBaseModule.forRoot({
      locationEntity: CustomLocationEntity,
      materialEntity: CustomMaterialEntity,
      stockEntity: StockEntity,  // 使用預設
      batchEntity: BatchEntity,  // 使用預設
      orderEntity: OrderEntity,  // 使用預設
      allowNegativeStock: false,
    }),
  ],
})
export class AppModule {}
```

## Data Types

### MapData

```typescript
interface MapData {
  id: string;
  backgrounds: MapBackground[];
  ranges: (MapRectangleRange | MapPolygonRange)[];
}

interface MapBackground {
  id: string;
  filename: string;
  x: number;
  y: number;
  height: number;
  width: number;
}

interface MapRange {
  id: string;
  type: MapRangeType;
  color: string;
}

interface MapRectangleRange extends MapRange {
  x: number;
  y: number;
  width: number;
  height: number;
}

interface MapPolygonRange extends MapRange {
  points: MapPolygonRangePoint[];
}

interface MapPolygonRangePoint {
  x: number;
  y: number;
}
```

### Enums

```typescript
enum MapRangeType {
  RECTANGLE = 'RECTANGLE',
  POLYGON = 'POLYGON',
}

enum MapRangeColor {
  RED = 'RED',
  YELLOW = 'YELLOW',
  GREEN = 'GREEN',
  BLUE = 'BLUE',
  BLACK = 'BLACK',
}

enum StockSorter {
  CREATED_AT_DESC = 'CREATED_AT_DESC',
  CREATED_AT_ASC = 'CREATED_AT_ASC',
}
```

## Error Handling

```typescript
import {
  LocationNotFoundError,
  LocationCannotArchiveError,
  LocationAlreadyExistedError,
  StockQuantityNotEnoughError,
} from '@rytass/wms-base-nestjs-module';
```

**錯誤代碼表:**

| Code | Error | Description |
|------|-------|-------------|
| 100 | LocationNotFoundError | 儲位不存在 |
| 101 | LocationCannotArchiveError | 儲位無法封存 (庫存不為 0) |
| 102 | LocationAlreadyExistedError | 儲位已存在 |
| 200 | StockQuantityNotEnoughError | 庫存數量不足 |

```typescript
@Injectable()
export class SafeLocationService {
  constructor(private readonly locationService: LocationService) {}

  async safeArchive(id: string) {
    try {
      await this.locationService.archive(id);
    } catch (error) {
      if (error instanceof LocationCannotArchiveError) {
        throw new Error('無法封存儲位，請先清空庫存');
      }
      if (error instanceof LocationNotFoundError) {
        throw new Error('儲位不存在');
      }
      throw error;
    }
  }
}
```

## Configuration Options

```typescript
interface WMSBaseModuleOptions {
  // 自訂 Entity (皆為選填)
  stockEntity?: new () => StockEntity;
  locationEntity?: new () => LocationEntity;
  materialEntity?: new () => MaterialEntity;
  batchEntity?: new () => BatchEntity;
  orderEntity?: new () => OrderEntity;
  warehouseMapEntity?: new () => WarehouseMapEntity;

  // 選項
  allowNegativeStock?: boolean;  // 預設: false
}

// Async Options
interface WMSBaseModuleAsyncOptions {
  imports?: ModuleMetadata['imports'];
  inject?: InjectionToken[];
  useFactory?: (...args: any[]) => Promise<WMSBaseModuleOptions> | WMSBaseModuleOptions;
  useClass?: Type<WMSBaseModuleOptionsFactory>;
  useExisting?: Type<WMSBaseModuleOptionsFactory>;
}

// Options Factory Interface
interface WMSBaseModuleOptionsFactory {
  createWMSBaseModuleOptions(): Promise<WMSBaseModuleOptions> | WMSBaseModuleOptions;
}
```

## Symbol Tokens

可用於依賴注入的 Symbol Tokens：

```typescript
import {
  // Repository Tokens
  RESOLVED_TREE_LOCATION_REPO,   // TreeRepository<LocationEntity>
  RESOLVED_MATERIAL_REPO,        // Repository<MaterialEntity>
  RESOLVED_BATCH_REPO,           // Repository<BatchEntity>
  RESOLVED_ORDER_REPO,           // Repository<OrderEntity>
  RESOLVED_STOCK_REPO,           // Repository<StockEntity>
  RESOLVED_WAREHOUSE_MAP_REPO,   // Repository<WarehouseMapEntity>

  // Entity Provider Tokens
  PROVIDE_LOCATION_ENTITY,
  PROVIDE_MATERIAL_ENTITY,
  PROVIDE_BATCH_ENTITY,
  PROVIDE_ORDER_ENTITY,
  PROVIDE_STOCK_ENTITY,
  PROVIDE_WAREHOUSE_MAP_ENTITY,

  // Options Tokens
  WMS_MODULE_OPTIONS,            // WMSBaseModuleOptions
  ALLOW_NEGATIVE_STOCK,          // boolean
} from '@rytass/wms-base-nestjs-module';

// 使用範例
@Injectable()
export class CustomService {
  constructor(
    @Inject(RESOLVED_TREE_LOCATION_REPO)
    private readonly locationRepo: TreeRepository<LocationEntity>,

    @Inject(RESOLVED_STOCK_REPO)
    private readonly stockRepo: Repository<StockEntity>,

    @Inject(ALLOW_NEGATIVE_STOCK)
    private readonly allowNegativeStock: boolean,
  ) {}
}
```

## Complete Example

```typescript
import { Module, Injectable } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import {
  WMSBaseModule,
  LocationService,
  MaterialService,
  StockService,
  OrderService,
  OrderEntity,
  StockSorter,
} from '@rytass/wms-base-nestjs-module';
import { Entity, Column } from 'typeorm';

// 自訂訂單
@Entity('warehouse_orders')
export class WarehouseOrderEntity extends OrderEntity {
  @Column()
  orderNumber: string;

  @Column()
  type: 'INBOUND' | 'OUTBOUND' | 'TRANSFER';

  @Column({ nullable: true })
  note: string;
}

// 倉儲服務
@Injectable()
export class WarehouseManagementService {
  constructor(
    private readonly locationService: LocationService,
    private readonly materialService: MaterialService,
    private readonly stockService: StockService,
    private readonly orderService: OrderService,
  ) {}

  // 初始化倉庫結構
  async initializeWarehouse() {
    const warehouse = await this.locationService.create({ id: 'WH-001' });
    const zoneA = await this.locationService.create({ id: 'WH-001-A', parentId: 'WH-001' });
    const zoneB = await this.locationService.create({ id: 'WH-001-B', parentId: 'WH-001' });

    return { warehouse, zoneA, zoneB };
  }

  // 入庫作業
  async inbound(materialId: string, locationId: string, quantity: number, batchId: string) {
    // 確保物料存在
    await this.materialService.create({ id: materialId });

    // 建立入庫訂單
    const order = await this.orderService.createOrder(WarehouseOrderEntity, {
      order: {
        orderNumber: `IN-${Date.now()}`,
        type: 'INBOUND',
      },
      batches: [{
        id: batchId,
        materialId,
        locationId,
        quantity, // 正數
      }],
    });

    return order;
  }

  // 出庫作業
  async outbound(materialId: string, locationId: string, quantity: number, batchId: string) {
    // 檢查庫存
    const stock = await this.stockService.find({
      locationIds: [locationId],
      materialIds: [materialId],
      batchIds: [batchId],
      exactLocationMatch: true,
    });

    if (stock < quantity) {
      throw new Error(`庫存不足: 現有 ${stock}, 需要 ${quantity}`);
    }

    // 建立出庫訂單
    const order = await this.orderService.createOrder(WarehouseOrderEntity, {
      order: {
        orderNumber: `OUT-${Date.now()}`,
        type: 'OUTBOUND',
      },
      batches: [{
        id: batchId,
        materialId,
        locationId,
        quantity: -quantity, // 負數
      }],
    });

    return order;
  }

  // 查詢庫存
  async getInventory(locationId: string) {
    const total = await this.stockService.find({ locationIds: [locationId] });
    const logs = await this.stockService.findTransactions({
      locationIds: [locationId],
      limit: 10,
      sorter: StockSorter.CREATED_AT_DESC,
    });

    return { total, recentLogs: logs.transactionLogs };
  }
}

// 模組
@Module({
  imports: [
    TypeOrmModule.forRoot({
      type: 'postgres',
      host: 'localhost',
      database: 'wms',
      entities: [WarehouseOrderEntity],
      synchronize: true,
    }),
    WMSBaseModule.forRoot({
      orderEntity: WarehouseOrderEntity,
      allowNegativeStock: false,
    }),
  ],
  providers: [WarehouseManagementService],
})
export class WarehouseModule {}
```

## Troubleshooting

### 負庫存錯誤

如果 `allowNegativeStock: false`，出庫數量超過庫存會拋出 `StockQuantityNotEnoughError`。
先查詢庫存再執行出庫操作。

### 交易失敗

`createOrder` 使用資料庫交易，任何批次失敗都會回滾整個訂單。
確保所有批次資料正確再提交。

### 倉位無法封存

當嘗試封存一個仍有庫存的倉位時，會拋出 `LocationCannotArchiveError`。
需先將庫存移出（出庫或調撥）後才能封存倉位。

### 倉位已存在錯誤

建立儲位時，若 ID 已存在（含已封存的），會拋出 `LocationAlreadyExistedError`。
可以先解除封存 (`unArchive`) 或使用不同的 ID。
