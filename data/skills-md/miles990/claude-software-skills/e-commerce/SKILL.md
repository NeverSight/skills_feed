---
name: e-commerce
description: E-commerce platforms, payment processing, and shopping cart patterns
domain: domain-applications
version: 1.0.0
tags: [e-commerce, payments, stripe, cart, checkout, inventory]
triggers:
  keywords:
    primary: [e-commerce, ecommerce, shopping cart, checkout, payment, stripe]
    secondary: [inventory, order, product catalog, discount, coupon, shipping]
  context_boost: [shop, store, buy, sell, transaction]
  context_penalty: [game, mobile, desktop]
  priority: high
---

# E-Commerce Development

## Overview

Building e-commerce applications with shopping carts, payment processing, inventory management, and order fulfillment.

---

## Shopping Cart

### Cart State Management

```typescript
interface CartItem {
  productId: string;
  variantId?: string;
  quantity: number;
  price: number;
  name: string;
  image: string;
}

interface Cart {
  id: string;
  items: CartItem[];
  subtotal: number;
  tax: number;
  shipping: number;
  total: number;
  discountCode?: string;
  discountAmount: number;
}

// Zustand cart store
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface CartStore {
  cart: Cart;
  addItem: (item: Omit<CartItem, 'quantity'>, quantity?: number) => void;
  updateQuantity: (productId: string, quantity: number) => void;
  removeItem: (productId: string) => void;
  clearCart: () => void;
  applyDiscount: (code: string) => Promise<void>;
}

const useCartStore = create<CartStore>()(
  persist(
    (set, get) => ({
      cart: createEmptyCart(),

      addItem: (item, quantity = 1) => {
        set((state) => {
          const existingIndex = state.cart.items.findIndex(
            (i) => i.productId === item.productId && i.variantId === item.variantId
          );

          const newItems = [...state.cart.items];
          if (existingIndex >= 0) {
            newItems[existingIndex].quantity += quantity;
          } else {
            newItems.push({ ...item, quantity });
          }

          return { cart: recalculateCart({ ...state.cart, items: newItems }) };
        });
      },

      updateQuantity: (productId, quantity) => {
        set((state) => {
          if (quantity <= 0) {
            return {
              cart: recalculateCart({
                ...state.cart,
                items: state.cart.items.filter((i) => i.productId !== productId),
              }),
            };
          }

          const newItems = state.cart.items.map((item) =>
            item.productId === productId ? { ...item, quantity } : item
          );

          return { cart: recalculateCart({ ...state.cart, items: newItems }) };
        });
      },

      removeItem: (productId) => {
        set((state) => ({
          cart: recalculateCart({
            ...state.cart,
            items: state.cart.items.filter((i) => i.productId !== productId),
          }),
        }));
      },

      clearCart: () => set({ cart: createEmptyCart() }),

      applyDiscount: async (code) => {
        const discount = await validateDiscountCode(code);
        set((state) => ({
          cart: recalculateCart({
            ...state.cart,
            discountCode: code,
            discountAmount: discount.amount,
          }),
        }));
      },
    }),
    { name: 'cart-storage' }
  )
);

function recalculateCart(cart: Cart): Cart {
  const subtotal = cart.items.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  );
  const tax = subtotal * 0.1; // 10% tax
  const shipping = subtotal > 100 ? 0 : 9.99;
  const total = subtotal + tax + shipping - cart.discountAmount;

  return { ...cart, subtotal, tax, shipping, total };
}
```

---

## Payment Processing

### Stripe Integration

```typescript
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2023-10-16',
});

// Create checkout session
async function createCheckoutSession(cart: Cart, customerId?: string) {
  const session = await stripe.checkout.sessions.create({
    mode: 'payment',
    customer: customerId,
    line_items: cart.items.map((item) => ({
      price_data: {
        currency: 'usd',
        product_data: {
          name: item.name,
          images: [item.image],
        },
        unit_amount: Math.round(item.price * 100),
      },
      quantity: item.quantity,
    })),
    discounts: cart.discountCode
      ? [{ coupon: cart.discountCode }]
      : undefined,
    shipping_address_collection: {
      allowed_countries: ['US', 'CA', 'GB'],
    },
    success_url: `${process.env.APP_URL}/checkout/success?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${process.env.APP_URL}/cart`,
    metadata: {
      cartId: cart.id,
    },
  });

  return session;
}

// Create payment intent (for custom checkout)
async function createPaymentIntent(amount: number, customerId?: string) {
  const paymentIntent = await stripe.paymentIntents.create({
    amount: Math.round(amount * 100),
    currency: 'usd',
    customer: customerId,
    automatic_payment_methods: { enabled: true },
  });

  return {
    clientSecret: paymentIntent.client_secret,
    paymentIntentId: paymentIntent.id,
  };
}

// Webhook handler
async function handleStripeWebhook(body: string, signature: string) {
  const event = stripe.webhooks.constructEvent(
    body,
    signature,
    process.env.STRIPE_WEBHOOK_SECRET!
  );

  switch (event.type) {
    case 'checkout.session.completed': {
      const session = event.data.object as Stripe.Checkout.Session;
      await fulfillOrder(session);
      break;
    }

    case 'payment_intent.succeeded': {
      const paymentIntent = event.data.object as Stripe.PaymentIntent;
      await handlePaymentSuccess(paymentIntent);
      break;
    }

    case 'payment_intent.payment_failed': {
      const paymentIntent = event.data.object as Stripe.PaymentIntent;
      await handlePaymentFailure(paymentIntent);
      break;
    }
  }
}
```

### React Stripe Elements

```tsx
import { loadStripe } from '@stripe/stripe-js';
import {
  Elements,
  PaymentElement,
  useStripe,
  useElements,
} from '@stripe/react-stripe-js';

const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_KEY!);

function CheckoutForm({ clientSecret }: { clientSecret: string }) {
  const stripe = useStripe();
  const elements = useElements();
  const [error, setError] = useState<string | null>(null);
  const [processing, setProcessing] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!stripe || !elements) return;

    setProcessing(true);
    setError(null);

    const { error: submitError } = await stripe.confirmPayment({
      elements,
      confirmParams: {
        return_url: `${window.location.origin}/checkout/success`,
      },
    });

    if (submitError) {
      setError(submitError.message || 'Payment failed');
      setProcessing(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <PaymentElement />
      {error && <div className="error">{error}</div>}
      <button type="submit" disabled={!stripe || processing}>
        {processing ? 'Processing...' : 'Pay Now'}
      </button>
    </form>
  );
}

function CheckoutPage() {
  const [clientSecret, setClientSecret] = useState('');

  useEffect(() => {
    fetch('/api/create-payment-intent', {
      method: 'POST',
      body: JSON.stringify({ amount: cart.total }),
    })
      .then((res) => res.json())
      .then((data) => setClientSecret(data.clientSecret));
  }, []);

  if (!clientSecret) return <Loading />;

  return (
    <Elements
      stripe={stripePromise}
      options={{ clientSecret, appearance: { theme: 'stripe' } }}
    >
      <CheckoutForm clientSecret={clientSecret} />
    </Elements>
  );
}
```

---

## Inventory Management

```typescript
interface Product {
  id: string;
  name: string;
  sku: string;
  price: number;
  inventory: number;
  lowStockThreshold: number;
  variants: ProductVariant[];
}

interface ProductVariant {
  id: string;
  name: string;
  sku: string;
  price: number;
  inventory: number;
  attributes: Record<string, string>;
}

// Inventory operations with optimistic locking
async function reserveInventory(items: CartItem[]): Promise<boolean> {
  return prisma.$transaction(async (tx) => {
    for (const item of items) {
      const product = await tx.product.findUnique({
        where: { id: item.productId },
        select: { inventory: true, version: true },
      });

      if (!product || product.inventory < item.quantity) {
        throw new Error(`Insufficient inventory for ${item.name}`);
      }

      // Optimistic locking with version check
      const updated = await tx.product.updateMany({
        where: {
          id: item.productId,
          version: product.version,
          inventory: { gte: item.quantity },
        },
        data: {
          inventory: { decrement: item.quantity },
          version: { increment: 1 },
        },
      });

      if (updated.count === 0) {
        throw new Error(`Concurrent modification for ${item.name}`);
      }
    }

    return true;
  });
}

// Release inventory (on order cancellation)
async function releaseInventory(orderId: string) {
  const order = await prisma.order.findUnique({
    where: { id: orderId },
    include: { items: true },
  });

  await prisma.$transaction(
    order.items.map((item) =>
      prisma.product.update({
        where: { id: item.productId },
        data: { inventory: { increment: item.quantity } },
      })
    )
  );
}

// Low stock alerts
async function checkLowStock() {
  const lowStockProducts = await prisma.product.findMany({
    where: {
      inventory: { lte: prisma.product.fields.lowStockThreshold },
    },
  });

  for (const product of lowStockProducts) {
    await sendLowStockAlert(product);
  }
}
```

---

## Order Management

```typescript
enum OrderStatus {
  PENDING = 'pending',
  PAID = 'paid',
  PROCESSING = 'processing',
  SHIPPED = 'shipped',
  DELIVERED = 'delivered',
  CANCELLED = 'cancelled',
  REFUNDED = 'refunded',
}

interface Order {
  id: string;
  userId: string;
  status: OrderStatus;
  items: OrderItem[];
  subtotal: number;
  tax: number;
  shipping: number;
  total: number;
  shippingAddress: Address;
  billingAddress: Address;
  paymentIntentId: string;
  trackingNumber?: string;
  createdAt: Date;
  updatedAt: Date;
}

// Create order from checkout session
async function fulfillOrder(session: Stripe.Checkout.Session) {
  const order = await prisma.order.create({
    data: {
      userId: session.client_reference_id!,
      status: OrderStatus.PAID,
      paymentIntentId: session.payment_intent as string,
      subtotal: session.amount_subtotal! / 100,
      total: session.amount_total! / 100,
      shippingAddress: JSON.parse(session.metadata!.shippingAddress),
      items: {
        create: JSON.parse(session.metadata!.items),
      },
    },
  });

  // Reserve inventory
  await reserveInventory(order.items);

  // Send confirmation email
  await sendOrderConfirmation(order);

  // Notify fulfillment system
  await notifyFulfillment(order);

  return order;
}

// Order status updates
async function updateOrderStatus(orderId: string, status: OrderStatus) {
  const order = await prisma.order.update({
    where: { id: orderId },
    data: { status },
  });

  // Send notification
  await sendOrderStatusUpdate(order);

  return order;
}
```

---

## Product Catalog

```typescript
// Product search with filters
async function searchProducts(params: {
  query?: string;
  category?: string;
  minPrice?: number;
  maxPrice?: number;
  sortBy?: 'price' | 'name' | 'createdAt';
  sortOrder?: 'asc' | 'desc';
  page?: number;
  limit?: number;
}) {
  const {
    query,
    category,
    minPrice,
    maxPrice,
    sortBy = 'createdAt',
    sortOrder = 'desc',
    page = 1,
    limit = 20,
  } = params;

  const where: Prisma.ProductWhereInput = {
    status: 'active',
    ...(query && {
      OR: [
        { name: { contains: query, mode: 'insensitive' } },
        { description: { contains: query, mode: 'insensitive' } },
      ],
    }),
    ...(category && { categoryId: category }),
    ...(minPrice && { price: { gte: minPrice } }),
    ...(maxPrice && { price: { lte: maxPrice } }),
  };

  const [products, total] = await Promise.all([
    prisma.product.findMany({
      where,
      orderBy: { [sortBy]: sortOrder },
      skip: (page - 1) * limit,
      take: limit,
      include: {
        category: true,
        images: true,
        variants: true,
      },
    }),
    prisma.product.count({ where }),
  ]);

  return {
    products,
    pagination: {
      page,
      limit,
      total,
      totalPages: Math.ceil(total / limit),
    },
  };
}
```

---

## Related Skills

- [[payment-processing]] - Payment systems
- [[backend]] - API development
- [[database]] - Data modeling

