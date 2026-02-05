---
name: batch-processing
description: Collect-then-batch pattern for database operations achieving 30-40% throughput improvement. Includes graceful fallback to sequential processing when batch operations fail.
license: MIT
compatibility: TypeScript/JavaScript, Python
metadata:
  category: data-access
  time: 4h
  source: drift-masterguide
---

# Batch Processing

30-40% throughput improvement by batching database operations with graceful fallback.

## When to Use This Skill

- Processing multiple related records (invoices, orders, events)
- Network latency is significant (cloud databases)
- Writes are independent (no inter-record dependencies)
- You can implement fallback for reliability

## Core Concepts

Sequential processing is slow because each item requires multiple DB round trips. The solution is to collect all data first, then execute batch operations:

```
Sequential (slow):
Item 1 → DB → DB → DB
Item 2 → DB → DB → DB
Item 3 → DB → DB → DB

Batched (fast):
Item 1 → collect
Item 2 → collect
Item 3 → collect
All items → BATCH INSERT
```

Key insight: Sequential mapping (fuzzy matching needs context), but batched writes (independent operations).

## Implementation

### Python

```python
from decimal import Decimal
from typing import Dict, List
import time

class BatchProcessor:
    """
    Batch-optimized processor with fallback
    """
    
    def process_batch(self, items: List[Dict], user_id: str) -> Dict:
        start_time = time.perf_counter()
        
        # Collectors for batch operations
        transactions_to_create = []
        inventory_updates = {}
        failed_items = []
        items_processed = 0
        
        # Step 1: Process mappings sequentially (context-dependent)
        for idx, item in enumerate(items, 1):
            try:
                # Business logic that needs context
                mapping = self.find_or_create_mapping(item)
                
                # Collect for batch insert
                transactions_to_create.append({
                    "user_id": user_id,
                    "item_id": mapping['item_id'],
                    "quantity": float(item['quantity']),
                    "unit_cost": float(item['unit_price']),
                })
                
                # Aggregate inventory updates by item
                item_id = mapping['item_id']
                if item_id not in inventory_updates:
                    inventory_updates[item_id] = Decimal('0')
                inventory_updates[item_id] += Decimal(str(item['quantity']))
                
                items_processed += 1
                
            except Exception as e:
                failed_items.append({
                    "line": idx,
                    "error": str(e)
                })
                continue
        
        # Step 2: BATCH INSERT transactions
        if transactions_to_create:
            try:
                self.client.table("transactions").insert(
                    transactions_to_create
                ).execute()
            except Exception as e:
                # CRITICAL: Fallback to sequential on batch failure
                return self._fallback_to_sequential(items, user_id)
        
        # Step 3: BATCH UPDATE inventory (aggregate first)
        if inventory_updates:
            self._batch_update_inventory(inventory_updates)
        
        return {
            "status": "partial_success" if failed_items else "success",
            "items_processed": items_processed,
            "items_failed": len(failed_items),
            "failed_items": failed_items or None,
            "processing_time_seconds": round(time.perf_counter() - start_time, 2)
        }
    
    def _batch_update_inventory(self, updates: Dict[str, Decimal]):
        """Batch query, individual updates (Supabase limitation)"""
        item_ids = list(updates.keys())
        
        # Get current quantities in one query
        current = self.client.table("inventory").select(
            "id, quantity"
        ).in_("id", item_ids).execute()
        
        # Apply updates
        for item in current.data:
            item_id = item['id']
            new_qty = Decimal(str(item['quantity'])) + updates[item_id]
            self.client.table("inventory").update({
                "quantity": float(new_qty)
            }).eq("id", item_id).execute()
    
    def _fallback_to_sequential(self, items: List[Dict], user_id: str) -> Dict:
        """Fallback ensures data integrity when batch fails"""
        logger.warning("Falling back to sequential processing")
        # Process one at a time
        for item in items:
            self.process_single(item, user_id)
```

### TypeScript

```typescript
interface BatchResult {
  status: 'success' | 'partial_success' | 'failed';
  itemsProcessed: number;
  itemsFailed: number;
  failedItems?: { line: number; error: string }[];
  processingTimeMs: number;
}

class BatchProcessor {
  async processBatch(items: Item[], userId: string): Promise<BatchResult> {
    const startTime = Date.now();
    
    const transactionsToCreate: Transaction[] = [];
    const inventoryUpdates = new Map<string, number>();
    const failedItems: { line: number; error: string }[] = [];
    let itemsProcessed = 0;
    
    // Step 1: Process mappings sequentially
    for (let idx = 0; idx < items.length; idx++) {
      try {
        const mapping = await this.findOrCreateMapping(items[idx]);
        
        transactionsToCreate.push({
          userId,
          itemId: mapping.itemId,
          quantity: items[idx].quantity,
          unitCost: items[idx].unitPrice,
        });
        
        // Aggregate updates
        const current = inventoryUpdates.get(mapping.itemId) || 0;
        inventoryUpdates.set(mapping.itemId, current + items[idx].quantity);
        
        itemsProcessed++;
      } catch (error) {
        failedItems.push({ line: idx + 1, error: error.message });
      }
    }
    
    // Step 2: Batch insert
    if (transactionsToCreate.length > 0) {
      try {
        await this.db.transactions.insertMany(transactionsToCreate);
      } catch (error) {
        return this.fallbackToSequential(items, userId);
      }
    }
    
    // Step 3: Batch update inventory
    await this.batchUpdateInventory(inventoryUpdates);
    
    return {
      status: failedItems.length > 0 ? 'partial_success' : 'success',
      itemsProcessed,
      itemsFailed: failedItems.length,
      failedItems: failedItems.length > 0 ? failedItems : undefined,
      processingTimeMs: Date.now() - startTime,
    };
  }
}
```

## Usage Examples

### Invoice Processing

```python
processor = BatchProcessor()

result = processor.process_batch(
    items=invoice_data['line_items'],
    user_id=user_id
)

if result['status'] == 'partial_success':
    logger.warning(f"Some items failed: {result['failed_items']}")
```

## Best Practices

1. Sequential mapping, batched writes - fuzzy matching needs context, writes don't
2. Always implement fallback - batch operations can fail, sequential is reliable
3. Aggregate before update - combine multiple updates to same record
4. Handle partial success - one bad item shouldn't fail the entire batch
5. Chunk large batches - 500 records max to avoid timeouts

## Common Mistakes

- Batching operations that depend on each other's results
- No fallback when batch operations fail
- Not aggregating updates to the same record
- Collecting too many records before writing (memory pressure)
- Not logging individual items when batch fails (lose context)

## Related Patterns

- checkpoint-resume - Resume processing after failures
- idempotency - Prevent duplicate processing on retry
- dead-letter-queue - Handle failed items
