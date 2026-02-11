---
name: sitemap-robots
description: Automated sitemap generation for all locale URLs, robots.txt configuration, and llms.txt for AI crawler optimization. Use when setting up sitemap.xml, configuring crawling rules, or improving discoverability for search engines and AI systems.
---

# Sitemap & Robots

## Sitemap Generation

```tsx
// app/sitemap.ts
import type { MetadataRoute } from 'next';
import { locales } from '@/i18n.config';
import { getServices, getProgrammes } from '@/lib/data';

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL!;
  
  // Static pages
  const staticPages = [
    '',
    '/about',
    '/services',
    '/book',
    '/pricing',
    '/programmes',
    '/testimonials',
    '/faq',
    '/policies',
    '/contact',
  ];

  // Generate URLs for all locales and static pages
  const staticUrls = locales.flatMap((locale) =>
    staticPages.map((page) => ({
      url: `${siteUrl}/${locale}${page}`,
      lastModified: new Date(),
      changeFrequency: page === '' ? 'weekly' : 'monthly' as const,
      priority: page === '' ? 1 : 0.8,
      alternates: {
        languages: Object.fromEntries(
          locales.map((loc) => [loc, `${siteUrl}/${loc}${page}`])
        ),
      },
    }))
  );

  // Dynamic programme pages
  const programmes = await getProgrammes('en');
  const programmeUrls = locales.flatMap((locale) =>
    programmes.map((programme) => ({
      url: `${siteUrl}/${locale}/programmes/${programme.slug}`,
      lastModified: new Date(programme.lastUpdated),
      changeFrequency: 'monthly' as const,
      priority: 0.7,
      alternates: {
        languages: Object.fromEntries(
          locales.map((loc) => [
            loc,
            `${siteUrl}/${loc}/programmes/${programme.slug}`,
          ])
        ),
      },
    }))
  );

  // Dynamic service pages (if you have individual service pages)
  const services = await getServices('en');
  const serviceUrls = locales.flatMap((locale) =>
    services.map((service) => ({
      url: `${siteUrl}/${locale}/services/${service.slug}`,
      lastModified: new Date(service.lastUpdated),
      changeFrequency: 'monthly' as const,
      priority: 0.7,
      alternates: {
        languages: Object.fromEntries(
          locales.map((loc) => [
            loc,
            `${siteUrl}/${loc}/services/${service.slug}`,
          ])
        ),
      },
    }))
  );

  return [...staticUrls, ...programmeUrls, ...serviceUrls];
}
```

## Robots.txt

```tsx
// app/robots.ts
import type { MetadataRoute } from 'next';

export default function robots(): MetadataRoute.Robots {
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL!;
  
  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        disallow: [
          '/api/',
          '/checkout/',
          '/_next/',
        ],
      },
    ],
    sitemap: `${siteUrl}/sitemap.xml`,
  };
}
```

## LLMs.txt for AI Crawlers

```txt
// public/llms.txt
# Studio Name - Pilates & Yoga Coaching

## About
Professional Pilates and Yoga coaching studio offering personalized 1:1 sessions, 
small group classes, and digital programmes. Evidence-informed approach focused on 
strength, mobility, posture, and stress relief.

## Languages
- Portuguese (pt-PT) - Default
- English (en)
- Turkish (tr)
- Spanish (es)
- French (fr)
- German (de)

## Important Pages
- Home: /[locale]/
- About: /[locale]/about
- Services: /[locale]/services
- Pricing: /[locale]/pricing
- Programmes: /[locale]/programmes
- Book: /[locale]/book
- FAQ: /[locale]/faq
- Contact: /[locale]/contact

## Services Offered
- 1:1 Pilates Sessions (mat and reformer)
- 1:1 Yoga Sessions
- Small Group Classes
- Online Coaching
- Digital Programmes (on-demand video courses)

## Booking
Sessions can be booked via the /book page. Available in-person and online.

## Contact
Email: hello@studioname.com
Location: Istanbul, Turkey

## Disclaimer
Content is educational and not medical advice. Consult a qualified professional 
before starting any exercise programme.
```

## Extended LLMs-Full.txt

```tsx
// scripts/generate-llms-full.ts
// Run this as a build step to generate comprehensive content

import { locales } from '@/i18n.config';
import { getServices, getProgrammes, getFAQs } from '@/lib/data';
import fs from 'fs';

async function generateLlmsFull() {
  let content = `# Studio Name - Complete Content Reference\n\n`;
  content += `Generated: ${new Date().toISOString()}\n\n`;

  // Services
  content += `## Services\n\n`;
  const services = await getServices('en');
  for (const service of services) {
    content += `### ${service.name}\n`;
    content += `${service.longDesc}\n`;
    content += `- Duration: ${service.duration}\n`;
    content += `- Price from: €${service.priceFrom}\n`;
    content += `- Delivery: ${service.delivery}\n`;
    content += `- Tags: ${service.tags.join(', ')}\n\n`;
  }

  // Programmes
  content += `## Digital Programmes\n\n`;
  const programmes = await getProgrammes('en');
  for (const programme of programmes) {
    content += `### ${programme.title}\n`;
    content += `- Level: ${programme.level}\n`;
    content += `- Duration: ${programme.durationText}\n`;
    content += `- Access: ${programme.accessLengthText}\n`;
    content += `- Equipment: ${programme.equipment.join(', ')}\n`;
    content += `- Outcomes: ${programme.outcomes.join('; ')}\n`;
    content += `- Price: €${programme.price}\n\n`;
  }

  // FAQs
  content += `## Frequently Asked Questions\n\n`;
  const faqs = await getFAQs('en');
  for (const group of faqs) {
    content += `### ${group.category}\n\n`;
    for (const item of group.items) {
      content += `**Q: ${item.question}**\n`;
      content += `A: ${item.answer}\n\n`;
    }
  }

  fs.writeFileSync('public/llms-full.txt', content);
  console.log('Generated llms-full.txt');
}

generateLlmsFull();
```

## Package.json Script

```json
{
  "scripts": {
    "generate:llms": "tsx scripts/generate-llms-full.ts",
    "build": "npm run generate:llms && next build"
  }
}
```

## Verification

After deployment, verify:
- `https://yoursite.com/sitemap.xml` - All locale URLs present
- `https://yoursite.com/robots.txt` - Sitemap reference correct
- `https://yoursite.com/llms.txt` - Human-readable summary
- Google Search Console - Submit sitemap
