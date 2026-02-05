---
name: order-builder
description: |
  Order calculation and discount engine (訂單計算與優惠引擎). Use when building shopping carts (購物車), applying discounts (折扣), pricing calculations (價格計算), or coupon systems (優惠券系統). Supports precise decimal calculations with Decimal.js. Keywords: 訂單, 購物車, 折扣, 優惠, 計算, order, cart, discount, coupon, pricing, Decimal.js
---

# Order Builder (訂單計算引擎)

## Overview

`@rytass/order-builder` 提供訂單計算與優惠政策應用引擎，支援複雜折扣邏輯、多階梯優惠和精確計算（Decimal.js）。

## Quick Start

### 安裝

```bash
npm install @rytass/order-builder
```

### 基本使用

```typescript
import { OrderBuilder, ValueDiscount, PercentageDiscount } from '@rytass/order-builder';

// 建立 Builder
const builder = new OrderBuilder({
  policies: [
    new ValueDiscount(100),           // 固定折 100 元
    new PercentageDiscount(0.1),      // 9 折
  ],
});

// 建立訂單
const order = builder.build({
  items: [
    { id: 'A', name: 'Product A', unitPrice: 500, quantity: 2 },
    { id: 'B', name: 'Product B', unitPrice: 300, quantity: 1 },
  ],
});

console.log(order.itemValue);       // 1300 (商品總額)
console.log(order.discountValue);   // 折扣金額
console.log(order.price);           // 最終價格
```

## Core Concepts

### Builder Pattern

```typescript
const builder = new OrderBuilder()
  .addPolicy(new ValueDiscount(100))
  .addPolicy(new PercentageDiscount(0.1));

// build() 後政策鎖定
const order = builder.build({ items: [...] });
```

### Order Properties

```typescript
order.price           // 最終價格
order.discountValue   // 總折扣額
order.itemValue       // 商品總額
order.itemQuantity    // 商品總數量
order.discounts       // 折扣說明陣列
order.itemRecords     // 品項記錄
order.logisticsRecord // 運費記錄（若有設定運費）
order.parent          // 父訂單（若為子訂單）
```

## Discount Policies

### DiscountOptions (折扣選項)

所有折扣類別都支援以下選項：

```typescript
interface DiscountOptions {
  id?: string;                    // 折扣識別碼
  onlyMatched?: boolean;          // 只計算符合條件的品項（預設: false）
  excludedInCalculation?: boolean; // 此折扣不計入折扣總額（預設: false）
}
```

> **注意：** `conditions` 是作為獨立的構造函數參數傳入，而非在 options 物件中。
> 自訂屬性（如 `name`）可透過泛型類型參數 `DiscountOptions<T>` 傳入。

### ValueDiscount (固定額折扣)

```typescript
import { ValueDiscount } from '@rytass/order-builder';

// 固定折 100 元
const discount = new ValueDiscount(100, {
  id: 'FLAT_100',
  name: '滿額折 100',
});

// 進階選項
const advancedDiscount = new ValueDiscount(50, {
  id: 'SPECIAL_50',
  onlyMatched: true,              // 只計算符合條件品項的金額
  excludedInCalculation: true,    // 此折扣不計入 discountValue
});
```

### PercentageDiscount (百分比折扣)

```typescript
import { PercentageDiscount } from '@rytass/order-builder';

// 9 折 (折 10%)
const discount = new PercentageDiscount(0.1, {
  id: 'DISCOUNT_10',
  name: '全館 9 折',
});
```

### StepValueDiscount (累積固定額折扣)

```typescript
import { StepValueDiscount } from '@rytass/order-builder';

// 每滿 1000 折 100 (累積計算)
// 例如：買 2500 元 → 折 200 (2 倍)
const discount = new StepValueDiscount(1000, 100, {
  id: 'STEP_DISCOUNT',
  name: '每滿千折百',
});

// 計算公式: discount = value * floor(itemValue / step)
// 2500 元時: 100 * floor(2500 / 1000) = 100 * 2 = 200

// 可選參數
const discountWithLimit = new StepValueDiscount(500, 50, {
  id: 'LIMITED_STEP',
  stepLimit: 3,       // 最多累積 3 次 (最多折 150)
  stepUnit: 'price',  // 'price' (金額) 或 'quantity' (數量)
  onlyMatched: true,  // 只計算符合條件的品項
});
```

> **注意**: 這是「累積折扣」模式，每達到 step 金額就累積一次折扣，不是「階梯式」選擇最高折扣。

### StepPercentageDiscount (累積百分比折扣)

```typescript
import { StepPercentageDiscount } from '@rytass/order-builder';

// 每買 3 件累積一次 95 折 (複利計算)
// 例如：買 6 件 → 0.95^2 = 90.25 折
const discount = new StepPercentageDiscount(3, 0.95, {
  id: 'QUANTITY_DISCOUNT',
  name: '每 3 件折 5%',
  stepUnit: 'quantity',  // 以數量計算 step
});

// 計算公式: discountRate = value ^ floor(multiplier / step)
// discount = itemValue * (1 - discountRate)

// 以金額累積的範例
const priceBasedDiscount = new StepPercentageDiscount(1000, 0.95, {
  id: 'PRICE_STEP',
  name: '每滿千折 5%',
  stepUnit: 'price',    // 預設，以金額計算 step
  stepLimit: 5,         // 最多累積 5 次 (最多 0.95^5 ≈ 77.4 折)
});
```

> **注意**: 這是「累積複利折扣」模式，每達到 step 就額外乘以 value 折扣率。

### ItemGiveawayDiscount (贈品折扣)

```typescript
import { ItemGiveawayDiscount, ItemIncluded } from '@rytass/order-builder';

// 送 1 件 (從符合條件的品項中選最低價)
const discount = new ItemGiveawayDiscount(1, new ItemIncluded({ items: ['A'] }), {
  id: 'BUY_A_GET_FREE',
});

// 多種建構方式
// 1. value + conditions 陣列 + options
new ItemGiveawayDiscount(1, [new ItemIncluded({ items: ['A'] })], { id: 'GIVEAWAY_1' });

// 2. value + 單一 condition + options
new ItemGiveawayDiscount(1, new ItemIncluded({ items: ['A'] }), { id: 'GIVEAWAY_2' });

// 3. value + options (無條件)
new ItemGiveawayDiscount(1, { id: 'FREE_ONE', strategy: 'HIGH_PRICE_FIRST' });

// 4. 只有 value (送最低價 1 件)
new ItemGiveawayDiscount(1);

// 指定贈品選擇策略
const discountWithStrategy = new ItemGiveawayDiscount(2, new ItemIncluded({ items: ['B', 'C'] }), {
  strategy: 'LOW_PRICE_FIRST',  // 先送低價品（預設）
  // strategy: 'HIGH_PRICE_FIRST', // 先送高價品
  id: 'GET_2_FREE',
});
```

> **注意:** `value` 是贈品數量，不是折扣金額。例如 `new ItemGiveawayDiscount(2)` 表示「送 2 件最低價品項」。

### StepItemGiveawayDiscount (累積贈品折扣)

> **注意：** `StepItemGiveawayDiscount` 目前未從 index.ts 導出，若需使用請直接從原始碼路徑 import。

```typescript
// 目前無法從 @rytass/order-builder 直接 import
// 需從原始碼路徑 import（若專案支援）
import { StepItemGiveawayDiscount } from '@rytass/order-builder/src/policies/discount/step-item-giveaway-discount';

// 每買 3 件送 1 件（累積）
// 例如：買 7 件 → 送 2 件 (floor(7/3) = 2)
const discount = new StepItemGiveawayDiscount(3, 1, {
  id: 'BUY_3_GET_1',
  name: '每滿 3 件送 1 件',
  strategy: 'LOW_PRICE_FIRST',  // 'LOW_PRICE_FIRST' | 'HIGH_PRICE_FIRST'
});

// 計算公式: giveawayQuantity = value * floor(matchedQuantity / (step + value))
// stepLimit 計算: min(stepLimit, floor(matchedQuantity / (step + value)))
```

## Conditions

### PriceThreshold (金額閾值)

```typescript
import { PriceThreshold } from '@rytass/order-builder';

// 滿 1000 元
const condition = new PriceThreshold(1000);
```

### QuantityThreshold (數量閾值)

```typescript
import { QuantityThreshold } from '@rytass/order-builder';

// 滿 5 件
const condition = new QuantityThreshold(5);
```

### ItemIncluded (包含品項)

```typescript
import { ItemIncluded } from '@rytass/order-builder';

// 購物車包含 A 或 B (基本用法)
const condition = new ItemIncluded({ items: ['A', 'B'] });

// 指定數量閾值
const conditionWithThreshold = new ItemIncluded({
  items: ['A', 'B'],
  threshold: 3,  // 需要 A 或 B 合計至少 3 件
});

// 使用函式判斷
const conditionWithFn = new ItemIncluded({
  isMatchedItem: (item) => item.category === 'special',
  threshold: 1,
});

// 指定 scope (搜尋的屬性)
const conditionWithScope = new ItemIncluded({
  items: ['sku-001', 'sku-002'],
  scope: ['sku', 'id'],  // 優先檢查 sku，沒有再檢查 id
});

// 搭配子條件
const conditionWithSubConditions = new ItemIncluded({
  items: ['A'],
  conditions: [new PriceThreshold(500)],  // 包含 A 且小計需達 500
});
```

### ItemRequired (必須包含)

```typescript
import { ItemRequired } from '@rytass/order-builder';

// 購物車必須包含 A（數量至少 1）
const conditionSimple = new ItemRequired('A');

// 購物車必須包含 A 且數量 >= 2（使用物件格式）
const condition = new ItemRequired({ id: 'A', quantity: 2 });

// 批量需求：A 至少 2 件、B 至少 1 件
const conditionMultiple = new ItemRequired([
  { id: 'A', quantity: 2 },
  'B',  // 字串會自動轉為 { id: 'B', quantity: 1 }
]);
```

### ItemExcluded (排除品項)

```typescript
import { ItemExcluded } from '@rytass/order-builder';

// 排除特定品項（不參與此折扣）
const condition = new ItemExcluded({ items: ['excluded-item-1', 'excluded-item-2'] });

// 使用函式判斷排除
const conditionWithFilter = new ItemExcluded({
  isMatchedItem: (item) => item.category === 'special',
});

// 指定 scope (搜尋的屬性)
const conditionWithScope = new ItemExcluded({
  items: ['sku-001'],
  scope: ['sku', 'id'],
});
```

### QuantityRequired (數量需求)

```typescript
import { QuantityRequired } from '@rytass/order-builder';

// 指定品項總數量需達到 5
const condition = new QuantityRequired(5, ['item-a', 'item-b']);

// 不指定品項，計算全部品項數量
const conditionAll = new QuantityRequired(10);
```

### CouponValidator (優惠券)

```typescript
import { ValueDiscount, CouponValidator } from '@rytass/order-builder';

const couponDiscount = new ValueDiscount(50, {
  id: 'COUPON_50',
  conditions: [new CouponValidator('SAVE50')],
});

// 使用優惠券
const order = builder.build({
  items: [...],
  coupons: ['SAVE50'],
});
```

## Configuration Options

### OrderBuilder Options

```typescript
new OrderBuilder({
  policies?: Policy[];
  policyPickStrategy?: 'order-based' | 'item-based';  // 預設: 'item-based'
  discountMethod?: 'price-weighted-average' | 'quantity-weighted-average';  // 預設: 'price-weighted-average'
  roundStrategy?: RoundStrategyType | [RoundStrategyType, number];  // 預設: 'every-calculation'
  logistics?: OrderLogistics;
});
```

### Policy Pick Strategy（折扣選擇策略）

當訂單符合多個折扣政策時，決定如何選擇最佳折扣：

| 策略 | 預設 | 說明 |
|------|------|------|
| `item-based` | ✓ | 針對每個品項分別選擇最佳折扣組合（**最優解**）|
| `order-based` | | 選擇整體折扣最高的單一政策 |

**策略差異範例：**

```typescript
// 假設訂單有 A、B 兩品項
// 政策 1: A 折 50 元
// 政策 2: B 折 100 元

// item-based（預設）: A 套用政策 1、B 套用政策 2 → 總折扣 150
// order-based: 只選擇政策 2 → 總折扣 100

new OrderBuilder({
  policyPickStrategy: 'item-based',  // 推薦，可獲得最大折扣
});
```

### Discount Method（折扣分配方式）

決定如何將整體折扣分配到各品項：

| 方法 | 預設 | 說明 |
|------|------|------|
| `price-weighted-average` | ✓ | 按金額加權分配折扣 |
| `quantity-weighted-average` | | 按數量加權分配折扣 |

### Round Strategy（四捨五入策略）

| 策略 | 預設 | 說明 |
|------|------|------|
| `every-calculation` | ✓ | 每次計算都四捨五入 |
| `final-price-only` | | 只在最終價格四捨五入 |
| `no-round` | | 不四捨五入 |

**精度設定：**

```typescript
new OrderBuilder({
  roundStrategy: 'final-price-only',         // 預設精度 0（整數）
  // 或指定精度
  roundStrategy: ['final-price-only', 2],    // 小數後 2 位
});
```

### OrderLogistics（運費設定）

```typescript
interface OrderLogistics {
  price: number;                          // 運費（必填）
  name?: string;                          // 物流名稱（可選）
  threshold?: number;                     // 免運門檻金額（可選）
  freeConditions?: Condition | Condition[]; // 免運條件（可選）
}
```

**運費範例：**

```typescript
import { OrderBuilder, PriceThreshold, ItemIncluded } from '@rytass/order-builder';

// 基本運費設定
new OrderBuilder({
  logistics: {
    price: 60,
    name: '宅配',
  },
});

// 滿額免運
new OrderBuilder({
  logistics: {
    price: 60,
    name: '宅配',
    threshold: 1000,  // 滿 1000 免運
  },
});

// 條件免運
new OrderBuilder({
  logistics: {
    price: 60,
    name: '宅配',
    freeConditions: [
      new PriceThreshold(1000),         // 滿 1000 免運
      new ItemIncluded(['vip-product']), // 或購買 VIP 商品免運
    ],
  },
});
```

## Order Methods

### 動態調整

```typescript
const order = builder.build({ items: initialItems });

// 新增品項 (單一或多個)
order.addItem({ id: 'C', name: 'Product C', unitPrice: 200, quantity: 1 });
order.addItem([
  { id: 'D', name: 'Product D', unitPrice: 100, quantity: 2 },
  { id: 'E', name: 'Product E', unitPrice: 150, quantity: 1 },
]);

// 移除品項 - 多種方式
// 1. 依 ID 和數量移除
order.removeItem('A', 2);  // 移除 A 商品 2 件

// 2. 依品項物件移除
order.removeItem({ id: 'B', name: 'Product B', unitPrice: 300, quantity: 1 });

// 3. 批次移除多個品項
order.removeItem([
  { id: 'C', name: 'Product C', unitPrice: 200, quantity: 1 },
]);

// 新增優惠券
order.addCoupon('SAVE50');

// 移除優惠券
order.removeCoupon('SAVE50');
```

### 子訂單

```typescript
// 篩選特定品項的子訂單
const subOrder = order.subOrder({
  subItems: ['A', 'B'],           // 子訂單包含的品項 ID
  subCoupons: ['COUPON1'],        // 子訂單使用的優惠券（可選）
  subPolicies: [new ValueDiscount(50)],  // 子訂單額外政策（可選）
  itemScope: 'id',                // 'id'（預設）或 'uuid'，指定篩選依據
});

console.log(subOrder.price);   // 只計算子訂單的價格
console.log(subOrder.parent);  // 父訂單參照
```

## Complete Example

```typescript
import {
  OrderBuilder,
  ValueDiscount,
  PercentageDiscount,
  StepValueDiscount,
  PriceThreshold,
  ItemRequired,
  CouponValidator,
} from '@rytass/order-builder';

// 定義折扣政策
const policies = [
  // 全館 95 折
  new PercentageDiscount(0.05, {
    id: 'GLOBAL_95',
    name: '全館 95 折',
  }),

  // 每滿千折 50 (累積)
  new StepValueDiscount(1000, 50, {
    id: 'STEP_DISCOUNT',
    name: '每滿千折 50',
  }),

  // 特定商品折扣
  new ValueDiscount(100, {
    id: 'PRODUCT_A_DISCOUNT',
    name: '購買 A 商品折 100',
    conditions: [new ItemRequired('product-a', 1)],
  }),

  // 優惠券折扣
  new ValueDiscount(200, {
    id: 'COUPON_200',
    name: '優惠券折 200',
    conditions: [new CouponValidator('SAVE200')],
  }),
];

// 建立 Builder
const builder = new OrderBuilder({
  policies,
  discountMethod: 'price-weighted-average',
  roundStrategy: 'final-price-only',
});

// 建立訂單
const order = builder.build({
  items: [
    { id: 'product-a', name: '商品 A', unitPrice: 1500, quantity: 1 },
    { id: 'product-b', name: '商品 B', unitPrice: 800, quantity: 2 },
    { id: 'product-c', name: '商品 C', unitPrice: 300, quantity: 3 },
  ],
  coupons: ['SAVE200'],
});

// 查看結果
console.log('商品總額:', order.itemValue);
console.log('折扣金額:', order.discountValue);
console.log('最終價格:', order.price);
console.log('應用的折扣:');
order.discounts.forEach(d => {
  console.log(`  - ${d.name}: -${d.value}`);
});

// 動態調整
order.addItem({ id: 'product-d', name: '商品 D', unitPrice: 500, quantity: 1 });
console.log('新增商品後價格:', order.price);

order.removeCoupon('SAVE200');
console.log('移除優惠券後價格:', order.price);
```

## Advanced Types

### Exported Enums

```typescript
// 折扣類型
enum Discount {
  PERCENTAGE = 'PERCENTAGE',
  VALUE = 'VALUE',
  STEP_VALUE = 'STEP_VALUE',
  STEP_PERCENTAGE = 'STEP_PERCENTAGE',
  ITEM_GIVEAWAY = 'ITEM_GIVEAWAY',
  STEP_ITEM_GIVEAWAY = 'STEP_ITEM_GIVEAWAY',
}

// 政策前綴
enum PolicyPrefix {
  DISCOUNT = 'DISCOUNT',
}
```

### Core Types

```typescript
// 訂單品項
interface OrderItem {
  id: string;
  name: string;
  unitPrice: number;
  quantity: number;
  conditionRef?: string | string[] | ((..._: unknown[]) => boolean);
}

// 扁平化品項（quantity = 1，有獨立 uuid）
interface FlattenOrderItem extends OrderItem {
  uuid: string;
}

// 品項記錄（折扣結果）
interface OrderItemRecord<Item extends OrderItem> {
  itemId: string;
  appliedPolicies: Policy[];
  originItem: Item;
  initialValue: number;
  discountValue: number;
  finalPrice: number;
  discountRecords: ItemDiscountRecord[];
}

// 基本品項（最小化）
interface BaseOrderItem {
  id: string;
  quantity: number;
  conditionRef?: string | string[] | ((..._: unknown[]) => boolean);
}
```

### Constants（常數）

```typescript
import { ORDER_LOGISTICS_ID, ORDER_LOGISTICS_NAME } from '@rytass/order-builder';

// 運費品項的固定 ID
ORDER_LOGISTICS_ID = '__LOGISTICS__';

// 運費品項的預設名稱
ORDER_LOGISTICS_NAME = 'logistics';
```

### Policy & Condition Interfaces

```typescript
// 政策介面
interface Policy<T extends ObjRecord = ObjRecord> {
  id: string;
  prefix: PolicyPrefix;
  conditions?: Condition[];
  matchedItems(order: Order): FlattenOrderItem[];
  valid(order: Order): boolean;
  resolve<TT extends T>(order: Order, ..._: unknown[]): TT[];
  description(..._: unknown[]): PolicyResult<T>;
}

// 條件介面
type Condition<T extends ObjRecord = ObjRecord, Options extends ObjRecord = ObjRecord> = {
  satisfy(order: Order, ..._: unknown[]): boolean;
  matchedItems?: (order: Order) => FlattenOrderItem[];
  readonly options?: Options;
} & T;

// 折扣政策描述結果
interface PolicyDiscountDescription {
  id: string;
  type: Discount;
  value: number;
  discount: number;
  conditions: Condition[];
  appliedItems: FlattenOrderItem[];
  matchedTimes: number;
  policy: BaseDiscount;
}
```

### Discount Options Types

```typescript
// 基本折扣選項
interface DiscountOptions {
  id?: string;
  name?: string;
  conditions?: Condition[];
  onlyMatched?: boolean;
  excludedInCalculation?: boolean;
}

// Step 折扣選項
interface StepDiscountOptions extends DiscountOptions {
  stepUnit: 'quantity' | 'price';
  stepLimit?: number;
}

// 贈品策略
type ItemGiveawayStrategy = 'LOW_PRICE_FIRST' | 'HIGH_PRICE_FIRST';
```

## Dependencies

- `decimal.js` ^10.6.0 (精確計算)

## Troubleshooting

### 折扣未生效

檢查條件是否滿足：
```typescript
// 確認優惠券已加入
order.addCoupon('COUPON_CODE');

// 確認品項符合條件
// ItemRequired('A', 2) 需要品項 A 數量 >= 2
```

### 金額計算不精確

使用正確的 roundStrategy：
```typescript
new OrderBuilder({
  roundStrategy: 'final-price-only',  // 推薦
});
```

### 多重折扣衝突

預設使用 `item-based` 策略，會自動選擇每個品項的最佳折扣組合。

如需改為「整體擇優」模式（只選一個最高折扣政策）：

```typescript
new OrderBuilder({
  policyPickStrategy: 'order-based',
});
```
