---
name: json-ld-schemas
description: JSON-LD structured data for Organization, Person, Service, Product, FAQPage, and BreadcrumbList with reusable components. Use when implementing schema.org markup, adding rich snippets, or improving search engine understanding of page content.
---

# JSON-LD Schemas

## Base JsonLd Component

```tsx
// components/seo/JsonLd.tsx
interface JsonLdProps {
  data: Record<string, unknown>;
}

export function JsonLd({ data }: JsonLdProps) {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}
    />
  );
}
```

## Organization Schema

```tsx
// components/seo/OrganizationJsonLd.tsx
import { JsonLd } from './JsonLd';

interface OrganizationJsonLdProps {
  locale: string;
}

export function OrganizationJsonLd({ locale }: OrganizationJsonLdProps) {
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL;
  
  const data = {
    '@context': 'https://schema.org',
    '@type': 'LocalBusiness',
    '@id': `${siteUrl}/#organization`,
    name: 'Studio Name',
    url: siteUrl,
    logo: `${siteUrl}/logo.png`,
    image: `${siteUrl}/studio.jpg`,
    description: 'Professional Pilates and Yoga coaching',
    priceRange: '$$',
    areaServed: {
      '@type': 'City',
      name: 'Istanbul',
    },
    availableLanguage: ['Portuguese', 'English', 'Turkish', 'Spanish', 'French', 'German'],
    sameAs: [
      'https://instagram.com/studioname',
      'https://facebook.com/studioname',
    ],
    contactPoint: {
      '@type': 'ContactPoint',
      telephone: '+90-xxx-xxx-xxxx',
      contactType: 'customer service',
      availableLanguage: ['Portuguese', 'English', 'Turkish'],
    },
  };

  return <JsonLd data={data} />;
}
```

## Person Schema (Trainer)

```tsx
// components/seo/PersonJsonLd.tsx
export function PersonJsonLd() {
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL;
  
  const data = {
    '@context': 'https://schema.org',
    '@type': 'Person',
    '@id': `${siteUrl}/#trainer`,
    name: 'Trainer Name',
    jobTitle: 'Certified Pilates & Yoga Instructor',
    description: 'Experienced instructor specializing in...',
    image: `${siteUrl}/trainer.jpg`,
    url: `${siteUrl}/about`,
    sameAs: ['https://linkedin.com/in/trainername'],
    knowsAbout: [
      'Pilates',
      'Yoga',
      'Posture Correction',
      'Strength Training',
      'Mobility',
    ],
    hasCredential: [
      {
        '@type': 'EducationalOccupationalCredential',
        name: 'Certified Pilates Instructor',
        credentialCategory: 'Professional Certification',
      },
    ],
  };

  return <JsonLd data={data} />;
}
```

## Service Schema

```tsx
// components/seo/ServiceJsonLd.tsx
import type { Service } from '@/types';

interface ServiceJsonLdProps {
  service: Service;
  locale: string;
}

export function ServiceJsonLd({ service, locale }: ServiceJsonLdProps) {
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL;
  
  const data = {
    '@context': 'https://schema.org',
    '@type': 'Service',
    '@id': `${siteUrl}/${locale}/services/${service.slug}`,
    name: service.name,
    description: service.longDesc,
    provider: {
      '@id': `${siteUrl}/#organization`,
    },
    areaServed: {
      '@type': 'City',
      name: 'Istanbul',
    },
    serviceType: service.tags.join(', '),
    offers: {
      '@type': 'Offer',
      price: service.priceFrom,
      priceCurrency: 'EUR',
      availability: 'https://schema.org/InStock',
    },
  };

  return <JsonLd data={data} />;
}
```

## Product Schema (Programmes)

```tsx
// components/seo/ProductJsonLd.tsx
import type { Programme } from '@/types';

interface ProductJsonLdProps {
  programme: Programme;
  locale: string;
}

export function ProductJsonLd({ programme, locale }: ProductJsonLdProps) {
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL;
  
  const data = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    '@id': `${siteUrl}/${locale}/programmes/${programme.slug}`,
    name: programme.title,
    description: programme.outcomes.join('. '),
    category: 'Digital Fitness Programme',
    offers: {
      '@type': 'Offer',
      price: programme.price,
      priceCurrency: 'EUR',
      availability: 'https://schema.org/InStock',
      url: `${siteUrl}/${locale}/programmes/${programme.slug}`,
    },
    brand: {
      '@id': `${siteUrl}/#organization`,
    },
  };

  return <JsonLd data={data} />;
}
```

## FAQPage Schema

```tsx
// components/seo/FAQPageJsonLd.tsx
import type { FAQGroup } from '@/types';

interface FAQPageJsonLdProps {
  faqs: FAQGroup[];
}

export function FAQPageJsonLd({ faqs }: FAQPageJsonLdProps) {
  const allQuestions = faqs.flatMap((group) =>
    group.items.map((item) => ({
      '@type': 'Question',
      name: item.question,
      acceptedAnswer: {
        '@type': 'Answer',
        text: item.answer,
      },
    }))
  );

  const data = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: allQuestions,
  };

  return <JsonLd data={data} />;
}
```

## BreadcrumbList Schema

```tsx
// components/seo/BreadcrumbJsonLd.tsx
interface BreadcrumbItem {
  name: string;
  href: string;
}

interface BreadcrumbJsonLdProps {
  items: BreadcrumbItem[];
  locale: string;
}

export function BreadcrumbJsonLd({ items, locale }: BreadcrumbJsonLdProps) {
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL;
  
  const data = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: items.map((item, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      name: item.name,
      item: `${siteUrl}/${locale}${item.href}`,
    })),
  };

  return <JsonLd data={data} />;
}
```

## WebPage Schema

```tsx
// components/seo/WebPageJsonLd.tsx
interface WebPageJsonLdProps {
  title: string;
  description: string;
  locale: string;
  path: string;
  lastUpdated?: string;
}

export function WebPageJsonLd({
  title,
  description,
  locale,
  path,
  lastUpdated,
}: WebPageJsonLdProps) {
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL;
  
  const data = {
    '@context': 'https://schema.org',
    '@type': 'WebPage',
    name: title,
    description,
    url: `${siteUrl}/${locale}${path}`,
    inLanguage: locale,
    isPartOf: {
      '@type': 'WebSite',
      '@id': `${siteUrl}/#website`,
      name: 'Studio Name',
      url: siteUrl,
    },
    ...(lastUpdated && { dateModified: lastUpdated }),
  };

  return <JsonLd data={data} />;
}
```

## Usage in Pages

```tsx
// app/[locale]/services/page.tsx
export default async function ServicesPage({ params }: Props) {
  const { locale } = await params;
  const services = await getServices(locale as Locale);

  return (
    <>
      <OrganizationJsonLd locale={locale} />
      <BreadcrumbJsonLd
        locale={locale}
        items={[
          { name: 'Home', href: '' },
          { name: 'Services', href: '/services' },
        ]}
      />
      {/* Page content */}
    </>
  );
}
```
