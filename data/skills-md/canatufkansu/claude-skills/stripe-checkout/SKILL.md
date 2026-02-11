---
name: stripe-checkout
description: Stripe Checkout integration for programme purchases with Server Actions, webhook signature verification, and success/cancel flows. Use when implementing payments, creating checkout sessions, handling webhooks, or setting up purchase flows.
---

# Stripe Checkout

## Environment Variables

```bash
# .env.local
STRIPE_SECRET_KEY=sk_test_... # or sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
```

## Environment Validation

```tsx
// lib/env.ts
import { z } from 'zod';

const stripeEnvSchema = z.object({
  STRIPE_SECRET_KEY: z.string().startsWith('sk_'),
  STRIPE_WEBHOOK_SECRET: z.string().startsWith('whsec_'),
});

export const stripeEnv = stripeEnvSchema.safeParse(process.env);

export function hasStripe(): boolean {
  return stripeEnv.success;
}
```

## Stripe Client

```tsx
// lib/stripe.ts
import Stripe from 'stripe';

if (!process.env.STRIPE_SECRET_KEY) {
  throw new Error('STRIPE_SECRET_KEY is not set');
}

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY, {
  apiVersion: '2024-12-18.acacia',
  typescript: true,
});
```

## Create Checkout Session (Server Action)

```tsx
// lib/actions/stripe.ts
'use server';

import { redirect } from 'next/navigation';
import { stripe } from '@/lib/stripe';
import { getProgrammeBySlug } from '@/lib/data';
import type { Locale } from '@/i18n.config';

interface CreateCheckoutParams {
  programmeSlug: string;
  locale: Locale;
}

export async function createCheckoutSession({
  programmeSlug,
  locale,
}: CreateCheckoutParams) {
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL!;
  const programme = await getProgrammeBySlug(locale, programmeSlug);

  if (!programme || !programme.stripePriceId) {
    throw new Error('Programme not found or not available for purchase');
  }

  const session = await stripe.checkout.sessions.create({
    mode: 'payment',
    payment_method_types: ['card'],
    line_items: [
      {
        price: programme.stripePriceId,
        quantity: 1,
      },
    ],
    success_url: `${siteUrl}/${locale}/checkout/success?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${siteUrl}/${locale}/checkout/cancel`,
    metadata: {
      programmeSlug,
      locale,
    },
    locale: getStripeLocale(locale),
  });

  if (session.url) {
    redirect(session.url);
  }

  throw new Error('Failed to create checkout session');
}

function getStripeLocale(locale: Locale): Stripe.Checkout.SessionCreateParams.Locale {
  const map: Record<Locale, Stripe.Checkout.SessionCreateParams.Locale> = {
    'pt-PT': 'pt',
    'en': 'en',
    'tr': 'tr',
    'es': 'es',
    'fr': 'fr',
    'de': 'de',
  };
  return map[locale] || 'auto';
}
```

## Buy Button Component

```tsx
// components/BuyButton.tsx
'use client';

import { useTransition } from 'react';
import { useLocale, useTranslations } from 'next-intl';
import { createCheckoutSession } from '@/lib/actions/stripe';
import { Button } from '@/components/ui/button';
import type { Locale } from '@/i18n.config';

interface BuyButtonProps {
  programmeSlug: string;
  price: number;
  disabled?: boolean;
}

export function BuyButton({ programmeSlug, price, disabled }: BuyButtonProps) {
  const [isPending, startTransition] = useTransition();
  const locale = useLocale() as Locale;
  const t = useTranslations('checkout');

  const handleBuy = () => {
    startTransition(async () => {
      await createCheckoutSession({ programmeSlug, locale });
    });
  };

  return (
    <Button
      onClick={handleBuy}
      disabled={disabled || isPending}
      size="lg"
      className="w-full"
    >
      {isPending ? t('processing') : `${t('buy')} - €${price}`}
    </Button>
  );
}
```

## Webhook Handler (Critical Security)

```tsx
// app/api/webhooks/stripe/route.ts
import { headers } from 'next/headers';
import { NextResponse } from 'next/server';
import { stripe } from '@/lib/stripe';
import type Stripe from 'stripe';

export async function POST(request: Request) {
  const body = await request.text();
  const headersList = await headers();
  const signature = headersList.get('stripe-signature');

  if (!signature) {
    return NextResponse.json({ error: 'Missing signature' }, { status: 400 });
  }

  let event: Stripe.Event;

  try {
    // CRITICAL: Always verify webhook signature
    event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    );
  } catch (err) {
    console.error('Webhook signature verification failed:', err);
    return NextResponse.json({ error: 'Invalid signature' }, { status: 400 });
  }

  switch (event.type) {
    case 'checkout.session.completed': {
      const session = event.data.object as Stripe.Checkout.Session;
      await handleSuccessfulPayment(session);
      break;
    }
    case 'payment_intent.payment_failed': {
      const paymentIntent = event.data.object as Stripe.PaymentIntent;
      console.error('Payment failed:', paymentIntent.id);
      break;
    }
  }

  return NextResponse.json({ received: true });
}

async function handleSuccessfulPayment(session: Stripe.Checkout.Session) {
  const { programmeSlug, locale } = session.metadata || {};
  const customerEmail = session.customer_details?.email;

  // Grant access to programme
  // - Save to database
  // - Send confirmation email
  // - Generate access credentials

  console.log('Payment successful:', {
    sessionId: session.id,
    programmeSlug,
    customerEmail,
    locale,
  });
}
```

## Success Page

```tsx
// app/[locale]/checkout/success/page.tsx
import { stripe } from '@/lib/stripe';
import { getTranslations } from 'next-intl/server';
import { redirect } from 'next/navigation';

type Props = {
  params: Promise<{ locale: string }>;
  searchParams: Promise<{ session_id?: string }>;
};

export default async function CheckoutSuccessPage({
  params,
  searchParams,
}: Props) {
  const { locale } = await params;
  const { session_id } = await searchParams;
  const t = await getTranslations('checkout');

  if (!session_id) {
    redirect(`/${locale}`);
  }

  const session = await stripe.checkout.sessions.retrieve(session_id);

  if (session.payment_status !== 'paid') {
    redirect(`/${locale}/checkout/cancel`);
  }

  return (
    <div className="container mx-auto px-4 py-16 text-center">
      <h1 className="text-3xl font-bold mb-4">{t('success.title')}</h1>
      <p className="text-muted-foreground mb-8">{t('success.message')}</p>
      <p className="text-sm">
        {t('success.emailSent', { email: session.customer_details?.email })}
      </p>
    </div>
  );
}
```

## Cancel Page

```tsx
// app/[locale]/checkout/cancel/page.tsx
import { getTranslations } from 'next-intl/server';
import Link from 'next/link';
import { Button } from '@/components/ui/button';

export default async function CheckoutCancelPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const t = await getTranslations('checkout');

  return (
    <div className="container mx-auto px-4 py-16 text-center">
      <h1 className="text-3xl font-bold mb-4">{t('cancel.title')}</h1>
      <p className="text-muted-foreground mb-8">{t('cancel.message')}</p>
      <Button asChild>
        <Link href={`/${locale}/programmes`}>{t('cancel.backToProgrammes')}</Link>
      </Button>
    </div>
  );
}
```

## Conditional Rendering (No Stripe)

```tsx
// components/ProgrammeCard.tsx
import { hasStripe } from '@/lib/env';
import { BuyButton } from './BuyButton';
import { Button } from '@/components/ui/button';
import Link from 'next/link';

export function ProgrammeCard({ programme, locale }) {
  return (
    <div>
      {/* Programme details */}
      
      {hasStripe() ? (
        <BuyButton programmeSlug={programme.slug} price={programme.price} />
      ) : (
        <Button asChild variant="outline">
          <Link href={`/${locale}/contact`}>Contact to Purchase</Link>
        </Button>
      )}
    </div>
  );
}
```

## Testing Webhooks Locally

```bash
# Install Stripe CLI
stripe listen --forward-to localhost:3000/api/webhooks/stripe

# Use the webhook signing secret from CLI output
```
