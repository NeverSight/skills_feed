---
name: json-content-management
description: JSON-driven content architecture for services, programmes, FAQs, testimonials, and policies with TypeScript interfaces and locale-aware data fetching. Use when defining content schemas, creating data utilities, adding new content types, or fetching localized business data.
---

# JSON Content Management

## Directory Structure

```
data/
├── pt-PT/
│   ├── services.json
│   ├── programmes.json
│   ├── testimonials.json
│   ├── faqs.json
│   └── policies.json
├── en/
│   └── ... (same structure)
├── tr/
├── es/
├── fr/
└── de/
```

## TypeScript Interfaces

```tsx
// types/index.ts

export interface Service {
  slug: string;
  name: string;
  shortDesc: string;
  longDesc: string;
  duration: string;
  priceFrom: number;
  tags: string[];
  delivery: 'in-person' | 'online' | 'both';
  lastUpdated: string;
}

export interface Programme {
  slug: string;
  title: string;
  type: 'single' | 'bundle';
  level: 'beginner' | 'intermediate' | 'advanced' | 'all';
  equipment: string[];
  outcomes: string[];
  durationText: string;
  accessLengthText: string;
  price: number;
  stripePriceId?: string;
  featured: boolean;
  lastUpdated: string;
}

export interface Testimonial {
  id: string;
  name: string;
  summary: string;
  detail: string;
  tag: string;
  featured: boolean;
}

export interface FAQGroup {
  category: string;
  items: {
    question: string;
    answer: string;
  }[];
}

export interface PolicySection {
  title: string;
  content: string;
}

export interface Policies {
  sections: PolicySection[];
  lastUpdated: string;
}
```

## Data Fetching Utilities

```tsx
// lib/data.ts
import { type Locale, defaultLocale } from '@/i18n.config';
import type { Service, Programme, Testimonial, FAQGroup, Policies } from '@/types';

async function loadData<T>(locale: Locale, filename: string): Promise<T> {
  try {
    const data = await import(`@/data/${locale}/${filename}`);
    return data.default as T;
  } catch {
    // Fallback to default locale
    const fallback = await import(`@/data/${defaultLocale}/${filename}`);
    return fallback.default as T;
  }
}

export async function getServices(locale: Locale): Promise<Service[]> {
  return loadData<Service[]>(locale, 'services.json');
}

export async function getServiceBySlug(
  locale: Locale,
  slug: string
): Promise<Service | undefined> {
  const services = await getServices(locale);
  return services.find((s) => s.slug === slug);
}

export async function getProgrammes(locale: Locale): Promise<Programme[]> {
  return loadData<Programme[]>(locale, 'programmes.json');
}

export async function getFeaturedProgrammes(locale: Locale): Promise<Programme[]> {
  const programmes = await getProgrammes(locale);
  return programmes.filter((p) => p.featured);
}

export async function getProgrammeBySlug(
  locale: Locale,
  slug: string
): Promise<Programme | undefined> {
  const programmes = await getProgrammes(locale);
  return programmes.find((p) => p.slug === slug);
}

export async function getTestimonials(locale: Locale): Promise<Testimonial[]> {
  return loadData<Testimonial[]>(locale, 'testimonials.json');
}

export async function getFeaturedTestimonials(locale: Locale): Promise<Testimonial[]> {
  const testimonials = await getTestimonials(locale);
  return testimonials.filter((t) => t.featured);
}

export async function getFAQs(locale: Locale): Promise<FAQGroup[]> {
  return loadData<FAQGroup[]>(locale, 'faqs.json');
}

export async function getPolicies(locale: Locale): Promise<Policies> {
  return loadData<Policies>(locale, 'policies.json');
}
```

## Example JSON Files

```json
// data/en/services.json
[
  {
    "slug": "pilates-1-1",
    "name": "1:1 Pilates Session",
    "shortDesc": "Personalized mat or reformer Pilates tailored to your goals",
    "longDesc": "A fully customized session focusing on your specific needs...",
    "duration": "60 min",
    "priceFrom": 75,
    "tags": ["strength", "posture", "flexibility"],
    "delivery": "both",
    "lastUpdated": "2025-01-15"
  }
]
```

```json
// data/en/faqs.json
[
  {
    "category": "Getting Started",
    "items": [
      {
        "question": "Do I need experience to start?",
        "answer": "No prior experience is needed. Sessions are adapted to your level."
      }
    ]
  }
]
```

## Usage in Server Components

```tsx
// app/[locale]/services/page.tsx
import { getServices } from '@/lib/data';
import { ServiceCard } from '@/components/cards/ServiceCard';

type Props = {
  params: Promise<{ locale: string }>;
};

export default async function ServicesPage({ params }: Props) {
  const { locale } = await params;
  const services = await getServices(locale as Locale);

  return (
    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      {services.map((service) => (
        <ServiceCard key={service.slug} service={service} locale={locale} />
      ))}
    </div>
  );
}
```

## Adding New Content Types

1. Define interface in `types/index.ts`
2. Create JSON files in each locale folder
3. Add fetch function in `lib/data.ts`
4. Use in components with proper typing
