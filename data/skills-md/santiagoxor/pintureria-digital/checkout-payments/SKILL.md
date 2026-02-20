---
name: checkout-payments
description: Specialized skill for working with checkout and payment systems including MercadoPago integration, order management, address validation, and checkout flow. Use when implementing checkout improvements, integrating payment methods, debugging payment issues, or optimizing checkout process.
---

# Checkout and Payments

## Quick Start

When working with checkout:

1. Validate cart data before creating order
2. Validate shipping address
3. Create order in database
4. Integrate with MercadoPago
5. Handle payment webhooks
6. Update order status

## Key Files

- `src/app/checkout/` - Checkout pages
- `src/components/Checkout/` - Checkout components
- `src/lib/integrations/mercadopago/` - MercadoPago integration
- `src/lib/business/orders/` - Order logic
- `src/hooks/useCheckout.ts` - Checkout hook

## Common Patterns

### Create Order

```typescript
import { createOrder } from '@/lib/business/orders/order-service';
import { createPayment } from '@/lib/integrations/mercadopago';

export async function POST(request: NextRequest) {
  const { items, shippingAddress, paymentMethod } = await request.json();
  
  const order = await createOrder({
    items,
    shippingAddress,
    status: 'pending_payment',
  });
  
  const payment = await createPayment({
    transaction_amount: order.total,
    description: `Orden #${order.id}`,
    payer: {
      email: order.customer_email,
    },
  });
  
  await updateOrder(order.id, {
    payment_id: payment.id,
    payment_status: 'pending',
  });
  
  return NextResponse.json({ order, payment });
}
```

### Validate Address

```typescript
import { validateAddress } from '@/lib/business/logistics/address-validation';

const validation = await validateAddress({
  street: 'Av. Corrientes 1234',
  city: 'Buenos Aires',
  postalCode: 'C1043AAX',
  country: 'AR',
});

if (!validation.isValid) {
  return { errors: validation.errors };
}
```

### MercadoPago Wallet

```typescript
import { initMercadoPago, Wallet } from '@mercadopago/sdk-react';

function CheckoutPayment() {
  const [paymentData, setPaymentData] = useState(null);
  
  useEffect(() => {
    initMercadoPago('YOUR_PUBLIC_KEY');
  }, []);
  
  return (
    <Wallet
      initialization={{ preferenceId: paymentData?.preference_id }}
      onSubmit={onSubmit}
    />
  );
}
```

## Order States

- `pending_payment` - Waiting for payment
- `paid` - Paid
- `processing` - Processing
- `shipped` - Shipped
- `delivered` - Delivered
- `cancelled` - Cancelled
- `refunded` - Refunded
